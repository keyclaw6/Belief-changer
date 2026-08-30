# Factory runbook — iteration 016 (hands-off)

Work only in `/home/kab/quit-sugar-iter-016`. Prompts are already applied.

You are the factory executor. This is an **agent conversation**: start each role runner, catch the on-disk marker, start the next unit in the **same** session. Do not drive quality. Pass only the official plan-reviewer's findings on revision.

**Do not die between units.** After a runner exits, immediately start the next unit.

## Hard rules

- Do not edit `loop/PROGRAM.md`, `loop/judges/`, `docs/AUTO-TUNING-LOOP.md`, `docs/BOOK-FACTORY-VISION.md`, models/routes, `prompts/research-agent.md`.
- Do not reopen CA-01. Do not ban the Willpower Method. Keep IN THIS CHAPTER.
- Do not paste GSBS prose. Do not clone 20 rooms.
- Do not apply 015 job-ownership, instruction-headline, evidence-ID-only, or W3.
- Writer/plan-writer: Muse Spark Zen contributor-free via dotenvx. Judges: `judge_replicate.py` (composer-2.5 ask).
- After plan is `fit to write from`, rebuild `loop/reference-alignment.md` (15 rows). This is judge wiring, not a quality inject.

## Commands

```bash
export BC_REPO=/home/kab/quit-sugar-iter-016
export ITER=016
cd "$BC_REPO"
export PLAN_TRACE_DIR="$BC_REPO/loop/iterations/016/plan-traces"
```

1. Research: `bash scripts/loop-runner/research_reuse.sh prompts/chapter-writer.md quit-sugar loop/iterations/016/change.diff` then copy accepted research into both replicate `traces/research/` dirs.
2. Plan write → plan review until last line is exactly `fit to write from`.
3. Alignment table. Copy plan to replicate traces.
4. Write A, snapshot chapters, wipe live chapters, write B, snapshot, leave live as B.
5. Judge A then B.
6. `loop/state.md` Status stays `IN PROGRESS` until the panel finishes.
