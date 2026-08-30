# Factory runbook — iteration 018 (hands-off)

Work only in `/home/kab/quit-sugar-iter-018`. The one-line writer never-surface clause is already applied. Do not edit prompts further.

You are the factory executor. Agent conversation: start each role runner, catch the on-disk marker, start the next unit in the **same** session. Do not drive quality. Do not die between units. Do not wait for the parent. After the panel, finish decide + campaign records yourself.

## Hard rules

- Do not edit `loop/PROGRAM.md`, `loop/judges/`, `docs/AUTO-TUNING-LOOP.md`, `docs/BOOK-FACTORY-VISION.md`, models/routes, `prompts/research-agent.md`.
- Do not apply 015/016/017 NO-GO families (formula deletion W1/S1–S5, echo-ID, density, job-ownership, instruction-headline, evidence-ID, W3, Carr extras).
- Writer: Muse Spark Zen contributor-free via dotenvx. Judges: `judge_replicate.py` (composer-2.5 ask).
- **Plan reuse:** do **not** run `plan_write.py`. Keep the 014 15-chapter `production-books/quit-sugar/master-plan.md`. Copy it into both replicate `traces/plan.md`. Keep existing `loop/reference-alignment.md` (014 15 rows).
- KEEP vs 014: `trap-question-label` 3/1 → 0/0 both. Veto: blocking `factory-speech` 0/0. Named 015/017 kills in either book → do not KEEP.
- Do not start 019.

## Env (required)

```bash
export BC_REPO=/home/kab/quit-sugar-iter-018
export ITER=018
cd "$BC_REPO"
ln -sfn ~/.config/dotenvx/.env.keys "$BC_REPO/.env.keys"
unset DOTENV_PRIVATE_KEY_FILE
```

Decrypt via the symlink. Do **not** set `DOTENV_PRIVATE_KEY_FILE` at the keys file — that broke 017 until unset.

## Commands

1. Research: `bash scripts/loop-runner/research_reuse.sh prompts/chapter-writer.md quit-sugar loop/iterations/018/change.diff` then copy accepted research into both replicate `traces/research/` dirs.
2. Plan: REUSE (copy `production-books/quit-sugar/master-plan.md` → `loop/iterations/018/replicate-{a,b}/traces/plan.md`).
3. Wipe live `production-books/quit-sugar/chapters/chapter-*.md` (keep README).
   `dotenvx run -f .env -- env BC_REPO="$BC_REPO" ITER=018 REPLICATE=a python3 scripts/loop-runner/write_replicate.py`
   Snapshot A → `loop/iterations/018/replicate-a/chapters/`. Wipe live chapters. Write B (`REPLICATE=b`). Snapshot B. Leave live as B.
4. Judge A then B: `dotenvx run -f .env -- env BC_REPO="$BC_REPO" ITER=018 REPLICATE=a python3 scripts/loop-runner/judge_replicate.py` (then `b`).
5. Census both: `python3 scripts/loop-runner/census_judgments.py loop/iterations/018/replicate-a/judgments` (then b). Write `census.md`.
6. Trace analysis → `decision.md` → append `learnings.md` / `ledger.md` / `results.tsv` LAST → copy records onto `/home/kab/Belief-changer` (iterations/018 + those four loop files only; no `prompts/`, no live chapters) → commit on `campaign-001`: `loop(iter-018): KEEP|REVERT|INCONCLUSIVE — trap-question prefix ban`.
7. `loop/state.md` Status stays `IN PROGRESS` until Step 6 finishes, then `IDLE`. Founder halt: do not start 019.
