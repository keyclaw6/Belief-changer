# Factory runbook — iteration 015 (hands-off)

Work only in `/home/kab/quit-sugar-iter-015`. Prompts are already applied. `hypothesis.md` and `change.diff` are already written.

You are the factory executor. This is an agent conversation: you start each role runner, catch the finished artifact, then start the next one. You do **not** drive quality. You pass **only** the official plan-reviewer's findings back on revision, then write A, write B, judge both. You do **not** grep the plan for Voice/Maya. You do **not** inject KEEP lists into `PLAN_REVIEW`. You do **not** KEEP/REVERT/census.

**Do not die between units.** After a runner exits, immediately start the next unit in the same conversation. `needs changes first` means snapshot that review and start the next plan-write in this same session — never nohup a review and end the turn.

## Hard rules

- Do not edit `loop/PROGRAM.md`, `loop/judges/`, `docs/AUTO-TUNING-LOOP.md`, `docs/BOOK-FACTORY-VISION.md`, models/routes in `loop/config.yaml`, `prompts/research-agent.md`.
- Do not reopen CA-01. Do not ban the Willpower Method. Keep IN THIS CHAPTER.
- Do not paste GSBS prose. Do not clone 20 rooms.
- If `research_reuse.sh` prints RERUN because of `set -o pipefail` + `find | grep` SIGPIPE, **REUSE** anyway: this hypothesis did not touch `research-agent.md` or the brief, and `production-books/quit-sugar/research/` exists.
- Writer/plan-writer: Muse Spark Zen `muse-spark-1.2-contributor-free` via dotenvx `.env`. Fallback is already in `muse_client.py`. Never non-contributor.
- Judges: `scripts/loop-runner/judge_replicate.py` (`agent --trust --model composer-2.5 --mode ask`).
- `write_replicate.py` skips chapters that already have `response.md` + live file. On Muse disconnect, restart the same command.
- Hung `agent` judge: kill it, discard `.partial`, restart `judge_replicate.py` (skips complete `response.md`).
- Alignment: after the plan is `fit to write from`, rebuild `loop/reference-alignment.md` yourself (PROGRAM: orchestrator table, not a role). Map each compact-card primary job to a GSBS chapter by belief-move. Every plan chapter must have a row. This is judge wiring, not a quality inject.

## Commands

```bash
export BC_REPO=/home/kab/quit-sugar-iter-015
export ITER=015
cd "$BC_REPO"
export PLAN_TRACE_DIR="$BC_REPO/loop/iterations/015/plan-traces"
mkdir -p "$PLAN_TRACE_DIR"
mkdir -p loop/iterations/015/replicate-a/traces/research
mkdir -p loop/iterations/015/replicate-b/traces/research
```

1. Research: `bash scripts/loop-runner/research_reuse.sh prompts/chapter-writer.md quit-sugar loop/iterations/015/change.diff` then copy accepted research into both replicate `traces/research/` dirs.
2. Plan write: `dotenvx run -f .env -- env BC_REPO="$BC_REPO" PLAN_TRACE_DIR="$PLAN_TRACE_DIR" python3 -u scripts/loop-runner/plan_write.py`
3. Plan review: `dotenvx run -f .env -- env BC_REPO="$BC_REPO" PLAN_TRACE_DIR="$PLAN_TRACE_DIR" PLAN_ROUND=review-1 python3 -u scripts/loop-runner/plan_review.py`
4. If `production-books/quit-sugar/master-plan-review.md` last non-empty line is not exactly `fit to write from`, set `PLAN_CANDIDATE`, `PLAN_REVIEW`, `PLAN_ROUND=revision-N` and rerun plan_write then plan_review. Pass **only** that reviewer file. Repeat until the last line is `fit to write from`. Stay in this conversation until that line exists.
5. Rebuild `loop/reference-alignment.md`. Copy accepted plan to `loop/iterations/015/replicate-a/traces/plan.md` (writer also copies if missing).
6. Write A: `dotenvx run -f .env -- env BC_REPO="$BC_REPO" ITER=015 REPLICATE=a python3 -u scripts/loop-runner/write_replicate.py`
7. Snapshot A chapters to `loop/iterations/015/replicate-a/chapters/`. Delete live `production-books/quit-sugar/chapters/chapter-*.md` only (keep plan and research).
8. Write B: `REPLICATE=b` same writer. Snapshot B chapters. Leave live chapters as B. Copy plan to `replicate-b/traces/plan.md`.
9. Judge A then B: `dotenvx run -f .env -- env BC_REPO="$BC_REPO" ITER=015 REPLICATE=a python3 -u scripts/loop-runner/judge_replicate.py` (then `b`). Skip existing `response.md`.
10. Update `loop/state.md` at stage boundaries (Planning / Writing A / Writing B / Judging). Status stays `IN PROGRESS`.

## Done

Write `loop/iterations/015/FACTORY-DONE.md`:
- plan review last line
- chapter counts A and B
- judgment file counts A and B (expect 3 per chapter + book-arc)
- any retries/fallbacks
- do not KEEP, REVERT, census, or edit `learnings.md` / `results.tsv`
