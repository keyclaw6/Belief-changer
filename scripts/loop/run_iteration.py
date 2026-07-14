"""Convenience wrapper: RUN (write chapters) -> SCORE -> GATE, one command.

Optional. Everything it does can be done by hand (see PROGRAM.md manual mode).
Writer calls go through the SAME OpenRouter plumbing as the judges
(scripts/eval/model_endpoint.chat) with the writer model from loop/config.yaml.
Fresh context per chapter: the writer sees ONLY the style guide + master plan +
the immediately previous chapter, exactly as prompts/chapter-writer.md dictates.

  python3 scripts/loop/run_iteration.py --book production-books/quit-sugar \
      --chapters 1-3 --iter 7 --hypothesis "H-001 word budgets"
  python3 scripts/loop/run_iteration.py ... --no-write   # skip RUN, just score+gate

No writer key -> prints exact manual-mode dispatch instructions and stops before
scoring (nothing to score). Never fabricates chapter prose.
"""
import argparse
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


def write_chapters(cfg, book, sel, candidate):
    """Dispatch the writer for each selected chapter, fresh context each time."""
    base_url, key = judges.endpoint()
    if not key:
        _manual_instructions(cfg, book, sel)
        return False
    style_guide = Path("prompts/style-guide.md").read_text(encoding="utf-8")
    writer_tmpl = Path("prompts/chapter-writer.md").read_text(encoding="utf-8")
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
        # Generous ceiling: a full chapter is a few thousand words of completion.
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


def _manual_instructions(cfg, book, sel):
    print("[run] NO writer key (OPENROUTER_API_KEY / LITELLM_API_KEY) — MANUAL MODE.")
    print("[run] Dispatch prompts/chapter-writer.md once PER CHAPTER, fresh context each,")
    print(f"      with writer model {cfg['writer_model']} (reasoning={cfg.get('writer_reasoning','none')}).")
    print("      The writer sees ONLY: prompts/style-guide.md + the book master-plan.md +")
    print("      the immediately previous chapter (none for ch1). Save each to")
    print(f"      {book}/chapters/chapter-NN.md (zero-padded), then run:")
    print(f"        python3 scripts/loop/score.py --book {book} --chapters "
          f"{sel[0]}-{sel[-1]} --iter <N>")
    print(f"        python3 scripts/loop/gate.py --iter <N> --hypothesis \"...\"")


def run_step(cmd):
    print(f"[run] $ {' '.join(cmd)}")
    return subprocess.run(cmd, check=False).returncode


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
    LG.add_arguments(ap)
    a = ap.parse_args()

    candidate = LG.require_authorized(a, entrypoint="run_iteration.py")
    config_path = Path(a.config) if a.config else loopcfg.find_config()
    LG.require_targets(candidate, config_path)
    cfg = loopcfg.load(config_path)
    book = Path(a.book)
    LG.require_targets(candidate, book, book / "chapters")
    LG.require_config_targets(candidate, cfg, "scores_dir", "results_tsv", "tasks_dir")
    if LG.dry_run(a, "run_iteration.py"):
        return
    ch_dir = book / "chapters"
    # Parse the range against however many chapters exist (or the plan's CH count).
    upper = len([p for p in ch_dir.glob("chapter-*.md")]) if ch_dir.is_dir() else 0
    plan = book / "master-plan.md"
    if plan.is_file():
        nums = [int(m) for m in CARD_RE.findall(plan.read_text(encoding="utf-8"))]
        upper = max(upper, max(nums) if nums else 0)
    sel = E.parse_range(a.chapters, upper or 99)

    # Step 1 RUN.
    if not a.no_write:
        wrote = write_chapters(cfg, book, sel, candidate)
        if not wrote:
            print("[run] stopping before SCORE (no chapters were written). "
                  "Write them manually per the instructions above, then re-run with --no-write.")
            sys.exit(2)
        if not a.score_now:
            print("[run] First drafts written. PROGRAM §4.1: run <=2 reviewer cycles per "
                  "chapter now (fresh subagents on prompts/chapter-reviewer.md; after the "
                  "2nd REVISE proceed with the latest draft and note residual blockers in "
                  "loop/learnings.md). Then resume:")
            print(f"[run]   python3 scripts/loop/run_iteration.py --book {book} --chapters "
                  f"{a.chapters} --iter {a.iter} --no-write --hypothesis \"{a.hypothesis}\"")
            print("[run] (Scoring first drafts directly is only for controls/baselines: "
                  "re-run with --score-now.)")
            sys.exit(0)

    py = sys.executable or "python3"
    auth = LG.forward_arguments(a)
    # Step 2 SCORE.
    rc_score = run_step([py, str(HERE.parent / "score.py"), "--book", str(book),
                         "--chapters", a.chapters, "--iter", str(a.iter),
                         "--config", str(config_path)] + auth)
    if rc_score == 3:
        print("[run] WAITING FOR JUDGE VERDICTS — dispatch the emitted task files as fresh")
        print("      native Sol subagents (see [judges] lines above), save the JSON verdicts,")
        print("      then re-run score.py and gate.py with the same --iter.")
        sys.exit(3)
    if rc_score != 0:
        print(f"[run] score.py exited {rc_score}; not gating.")
        sys.exit(rc_score)
    # Step 3 GATE.
    rc_gate = run_step([py, str(HERE.parent / "gate.py"), "--iter", str(a.iter),
                        "--hypothesis", a.hypothesis, "--config", str(config_path)] + auth)
    print("[run] Gate exit 0 = decision made (verdict is in the row/stdout, incl. REVERT). "
          "Now RECORD: write the hypothesis outcome into loop/learnings.md, run any "
          "printed revert commands, then COMMIT per PROGRAM §4.5.")
    sys.exit(rc_gate)


if __name__ == "__main__":
    main()
