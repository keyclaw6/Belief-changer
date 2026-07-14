"""Run, score, and gate one candidate iteration."""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "eval"))
sys.path.insert(0, str(HERE.parent))
import evallib as E          # noqa: E402
import model_endpoint as ME   # noqa: E402
import loopcfg               # noqa: E402
import judges                # noqa: E402
import legacy_guard as LG     # noqa: E402
import candidate_pair as CP   # noqa: E402
import pair_store as PS        # noqa: E402
import manual_dispatch as MD    # noqa: E402
CARD_RE = re.compile(r"^###\s+CH-0*(\d+)\b", re.M)


def chapter_title(plan_text, n):
    m = re.search(rf"^###\s+CH-0*{n}\s+—\s+(.+?)\s*$", plan_text, re.M)
    return m.group(1).strip() if m else f"Chapter {n}"


def build_writer_prompt(writer_tmpl, style_guide, plan_text, prev_chapter, slug, n, title):
    """Assemble the full writer context: filled prompt + its three ONLY inputs."""
    filled = (writer_tmpl.replace("[N]", str(n)).replace("[SLUG]", slug)
              .replace("[WORKING TITLE]", title).replace("[TITLE]", title.upper())
              .replace("[N-1]", str(n - 1)))
    parts = [filled,
             "\n\n===== INPUT 1: STYLE GUIDE (prompts/style-guide.md) =====\n", style_guide,
             "\n\n===== INPUT 2: MASTER PLAN (master-plan.md) =====\n", plan_text]
    if prev_chapter is not None:
        parts += [f"\n\n===== INPUT 3: PREVIOUS CHAPTER (chapter-{n-1:02d}.md) =====\n",
                  prev_chapter]
    else:
        parts += ["\n\n===== INPUT 3: (none — this is Chapter 1) =====\n"]
    parts += ["\n\n===== API OUTPUT CONTRACT (supersedes any save/report "
              "instructions above) =====\n",
              "You are running over a raw API with no filesystem. Return ONE "
              "thing: the complete final chapter text in book prose, starting "
              "with the chapter heading line. No preamble, no completion "
              "report, no word counts, no code fences. Your entire reply is "
              "saved verbatim as the chapter file."]
    return "".join(parts)


def _clean_chapter(raw: str) -> str:
    text = (raw or "").strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text
def write_chapters(cfg, book, sel, candidate, source_root=None):
    """Dispatch the writer for each selected chapter, fresh context each time."""
    base_url, key = judges.endpoint()
    if not key:
        MD.writer(cfg, source_root or candidate, book, sel)
        return False
    source_root = Path(source_root or ".")
    style_guide = (source_root / "prompts/style-guide.md").read_text(encoding="utf-8")
    writer_tmpl = (source_root / "prompts/chapter-writer.md").read_text(encoding="utf-8")
    plan_text = (book / "master-plan.md").read_text(encoding="utf-8")
    slug = book.name
    ch_dir = book / "chapters"
    LG.require_output(candidate, ch_dir)
    ch_dir.mkdir(parents=True, exist_ok=True)
    model = cfg["writer_model"]
    reasoning = cfg.get("writer_reasoning", "none")
    for n in sel:
        title = chapter_title(plan_text, n)
        prev_path = ch_dir / f"chapter-{n-1:02d}.md"
        prev = prev_path.read_text(encoding="utf-8") if (n > 1 and prev_path.is_file()) else None
        content = build_writer_prompt(writer_tmpl, style_guide, plan_text, prev, slug, n, title)
        print(f"[run] writing ch{n} ({title!r}) via {model} ...")
        raw = ME.chat(base_url, key, model, content, reasoning, max_tokens=16000, temperature=0.7)
        text = _clean_chapter(raw)
        nwords = len(E.words(text))
        if nwords < 800:
            raise SystemExit(f"[run] writer returned {nwords} words for ch{n} — that is a "
                             "report or refusal, not a chapter. NOT saved. Re-dispatch "
                             "(check the API OUTPUT CONTRACT reached the model).")
        out = ch_dir / f"chapter-{n:02d}.md"
        LG.require_output(candidate, out)
        out.write_text(text + "\n", encoding="utf-8")
        print(f"[run] wrote {out} ({nwords} words)")
    return True

def run_step(cmd, cwd=None):
    print(f"[run] $ {' '.join(cmd)}")
    return subprocess.run(cmd, check=False, cwd=cwd).returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--book", required=True)
    ap.add_argument("--chapters", default="1-3")
    ap.add_argument("--iter", type=int, required=True)
    ap.add_argument("--hypothesis", default="")
    ap.add_argument("--no-write", action="store_true", help="skip RUN; score+gate existing chapters")
    ap.add_argument("--score-now", action="store_true",
                    help="skip the stop-for-review pause and score immediately after writing")
    ap.add_argument("--config", default=None)
    ap.add_argument("--accepted-root")
    ap.add_argument("--promote-pair", action="store_true",
                    help="forward explicit human promotion approval to the gate")
    ap.add_argument("--decision-timestamp",
                    help="pinned UTC timestamp forwarded unchanged to the atomic gate")
    ap.add_argument("--initialize-accepted-store", action="store_true",
                    help="explicitly freeze repo-root bootstrap inputs behind the atomic pointer")
    ap.add_argument("--add-book-to-accepted-store", action="store_true",
                    help="atomically add one complete workshop to the accepted operation view")
    LG.add_arguments(ap)
    a = ap.parse_args()
    if a.initialize_accepted_store and a.add_book_to_accepted_store:
        ap.error("choose one accepted-store operation")

    store_operation = a.initialize_accepted_store or a.add_book_to_accepted_store
    candidate = LG.require_authorized(
        a, entrypoint="run_iteration.py",
        pre_rf23_stage="RF-02" if store_operation else None)
    target = Path(a.accepted_root or LG.REPO_ROOT).absolute()
    if store_operation:
        target = LG.require_store_target(candidate, target)
        if LG.dry_run(a, "run_iteration.py"):
            return
        try:
            action = CP.initialize if a.initialize_accepted_store else CP.add_book
            generation = action(target, a.book, a.config or "loop/config.yaml")
        except CP.PairError as exc:
            label = "setup" if a.initialize_accepted_store else "workshop addition"
            raise SystemExit(f"run: accepted-store {label} failed closed: {exc}") from exc
        print(f"[run] accepted generation {generation}")
        return
    if a.rf_dry_run:
        config_path = Path(a.config) if a.config else loopcfg.find_config()
        book = Path(a.book)
        LG.require_targets(candidate, config_path, book, book / "chapters")
        loopcfg.load(config_path)
        LG.dry_run(a, "run_iteration.py")
        return
    if not a.decision_timestamp:
        ap.error("candidate execution requires --decision-timestamp for resumable gating")
    if not os.path.lexists(candidate / CP.MANIFEST):
        try:
            CP.snapshot(candidate, target, a.book, a.chapters,
                        a.config or "loop/config.yaml", a.iter)
        except CP.PairError as exc:
            raise SystemExit(f"run: candidate snapshot failed closed: {exc}") from exc
    manifest = CP.load(candidate)
    try:
        CP.assert_run(candidate, manifest, a.book, a.chapters, a.iter,
                      a.config or "loop/config.yaml")
    except CP.PairError as exc:
        raise SystemExit(f"run: resume rejected: {exc}") from exc
    tree = CP.candidate_tree(candidate)
    config_path = CP.candidate_path(candidate, manifest["run"]["config"])
    book = tree / manifest["run"]["book"]
    CP.require_member(candidate, config_path, "config", manifest)
    LG.require_targets(candidate, config_path, book, book / "chapters")
    cfg = loopcfg.load(config_path)
    cfg = dict(cfg)
    evidence = CP.evidence_tree(candidate)
    cfg.update(scores_dir=str(evidence / "scores"),
               results_tsv=str(evidence / "results.tsv"),
               tasks_dir=str(evidence / "iterations"))
    LG.require_config_targets(candidate, cfg, "scores_dir", "results_tsv", "tasks_dir")
    ch_dir = book / "chapters"
    plan = book / "master-plan.md"
    try:
        PS.safe_dir(ch_dir, tree)
        CP.require_member(candidate, plan, "product", manifest)
        CP.require_member(candidate, tree / "prompts/style-guide.md", "config", manifest)
        CP.require_member(candidate, tree / "prompts/chapter-writer.md", "config", manifest)
        CP.require_member(candidate, tree / "prompts/chapter-reviewer.md", "config", manifest)
    except (CP.PairError, PS.StoreError) as exc:
        raise SystemExit(f"run: incomplete explicit pair: {exc}") from exc
    upper = len([p for p in ch_dir.glob("chapter-*.md")]) if ch_dir.is_dir() else 0
    nums = [int(m) for m in CARD_RE.findall(plan.read_text(encoding="utf-8"))]
    upper = max(upper, max(nums) if nums else 0)
    sel = E.parse_range(a.chapters, upper or 99)
    try:
        for n in sel:
            CP.require_member(candidate, ch_dir / f"chapter-{n:02d}.md", "product", manifest)
            if n > 1:
                CP.require_member(candidate, ch_dir / f"chapter-{n-1:02d}.md",
                                  "product", manifest)
    except CP.PairError as exc:
        raise SystemExit(f"run: incomplete explicit pair: {exc}") from exc

    if not a.no_write:
        wrote = write_chapters(cfg, book, sel, candidate, tree)
        if not wrote:
            print("[run] stopping before SCORE (no chapters were written). "
                  "Write them manually per the instructions above, then replay:")
            print(f"[run]   {MD.resume(a, HERE, sys.executable or 'python3')}")
            sys.exit(2)
        if not a.score_now:
            print("[run] First drafts written. PROGRAM §4.1: run <=2 reviewer cycles per "
                  f"chapter now ({MD.reviewer(tree)}; after the "
                  "2nd REVISE proceed with the latest draft and note residual blockers in "
                  "loop/learnings.md). Then resume:")
            print(f"[run]   {MD.resume(a, HERE, sys.executable or 'python3')}")
            print("[run] (Scoring first drafts directly is only for controls/baselines: "
                  "re-run with --score-now.)")
            sys.exit(0)

    try:
        if manifest["state"] == "CANDIDATE":
            tested_hash = CP.seal(candidate)
        elif manifest["state"] == "SEALED" and CP.status(candidate) == "SEALED":
            tested_hash = manifest["tested_hash"]
            CP.verify_sealed(candidate, tested_hash)
        else:
            raise CP.PairError(f"cannot resume decided pair {CP.status(candidate)}")
    except CP.PairError as exc:
        raise SystemExit(f"run: candidate sealing failed closed: {exc}") from exc
    print(f"[run] sealed exact evaluation pair {tested_hash}")
    py = sys.executable or "python3"
    auth = LG.forward_arguments(a)
    rc_score = run_step([py, str(HERE.parent / "score.py"), "--book", str(book),
                         "--chapters", a.chapters, "--iter", str(a.iter),
                         "--config", str(config_path),
                         "--tested-pair-hash", tested_hash] + auth, cwd=tree)
    if rc_score == 3:
        print("[run] WAITING FOR JUDGE VERDICTS — dispatch the emitted task files as fresh")
        print("      native Sol subagents (see [judges] lines above), save the JSON verdicts,")
        print("      then replay the pinned run command:")
        print(f"[run]   {MD.resume(a, HERE, py)}")
        sys.exit(3)
    if rc_score != 0:
        print(f"[run] score.py exited {rc_score}; not gating.")
        sys.exit(rc_score)
    # Step 3 GATE.
    pair_args = ["--tested-pair-hash", tested_hash,
                 "--accepted-root", str(target),
                 "--decision-timestamp", a.decision_timestamp]
    if a.promote_pair:
        pair_args.append("--promote-pair")
    rc_gate = run_step([py, str(HERE.parent / "gate.py"), "--iter", str(a.iter),
                        "--hypothesis", a.hypothesis, "--config", str(config_path)]
                       + auth + pair_args, cwd=tree)
    print("[run] Gate exit 0 = decision made (verdict is in the row/stdout, incl. REVERT). "
          "The pair is already promoted or retained as rejected evidence.")
    sys.exit(rc_gate)


if __name__ == "__main__":
    main()
