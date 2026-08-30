# Factory runbook — iteration 017 (hands-off)

Work only in `/home/kab/quit-sugar-iter-017`. Prompts already applied (trap-question isolation).

You are the factory executor. Agent conversation: start each role runner, catch the on-disk marker, start the next unit in the **same** session. Do not drive quality.

**Do not die between units.**

## Hard rules

- Do not edit `loop/PROGRAM.md`, `loop/judges/`, `docs/AUTO-TUNING-LOOP.md`, `docs/BOOK-FACTORY-VISION.md`, models/routes, `prompts/research-agent.md`.
- Do not apply 015/016 NO-GO families (echo-ID-only, density, job-ownership, instruction-headline, evidence-ID, W3, Carr extras).
- Writer: Muse Spark Zen contributor-free via dotenvx. Judges: `judge_replicate.py` (composer-2.5 ask).
- **Plan reuse:** do **not** run `plan_write.py`. Keep the 014 15-chapter `production-books/quit-sugar/master-plan.md`. Copy it into both replicate `traces/plan.md`. Keep existing `loop/reference-alignment.md` (014 15 rows).
- KEEP vs 014: `trap-question-label` 3/1 → 0/0 both. Veto: blocking `factory-speech` 0/0; named 015 kills in either book → do not KEEP.

## Commands

```bash
export BC_REPO=/home/kab/quit-sugar-iter-017
export ITER=017
cd "$BC_REPO"
```

1. Research: `bash scripts/loop-runner/research_reuse.sh prompts/chapter-writer.md quit-sugar loop/iterations/017/change.diff` then copy accepted research into both replicate `traces/research/` dirs.
2. Plan: REUSE (copy `production-books/quit-sugar/master-plan.md` → `loop/iterations/017/replicate-{a,b}/traces/plan.md`).
3. Wipe live `production-books/quit-sugar/chapters/chapter-*.md` (keep README). Write A, snapshot to `replicate-a/chapters/`, wipe live, write B, snapshot, leave live as B.
4. Judge A then B.
5. `loop/state.md` Status stays `IN PROGRESS` until the panel finishes.
