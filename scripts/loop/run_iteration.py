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
    return "".join(parts)


def write_chapters(cfg, book, sel):
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
        out = ch_dir / f"chapter-{n:02d}.md"
        out.write_text(raw.strip() + "\n", encoding="utf-8")
        print(f"[run] wrote {out} ({len(E.words(raw))} words)")
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
    ap.add_argument("--config", default=None)
    a = ap.parse_args()

    cfg = loopcfg.load(a.config) if a.config else loopcfg.load(loopcfg.find_config())
    book = Path(a.book)
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
        wrote = write_chapters(cfg, book, sel)
        if not wrote:
            print("[run] stopping before SCORE (no chapters were written). "
                  "Write them manually per the instructions above, then re-run with --no-write.")
            sys.exit(2)

    py = sys.executable or "python3"
    # Step 2 SCORE.
    rc_score = run_step([py, str(HERE.parent / "score.py"), "--book", str(book),
                         "--chapters", a.chapters, "--iter", str(a.iter)]
                        + (["--config", a.config] if a.config else []))
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
                        "--hypothesis", a.hypothesis]
                       + (["--config", a.config] if a.config else []))
    print("[run] Now do Step 4 RECORD by hand: append the results.tsv row is automatic, "
          "but WRITE the hypothesis outcome (pass or fail) into loop/learnings.md.")
    sys.exit(rc_gate)


if __name__ == "__main__":
    main()
