# Loop State — the live checkpoint

> The orchestrator updates this file at every stage boundary and before any
> long wait. A fresh agent reads it first (PROGRAM §0) and can continue the
> run from exactly here.
>
> Two rules keep it honest:
> - **`Status` is exactly `IDLE` or `IN PROGRESS`** (verbatim — no other token).
> - **This file can lag real work.** The on-disk markers — research bank files,
>   `production-books/quit-sugar/chapters/`, `loop/iterations/NNN/judgments/` —
>   are the ground truth. If they disagree with what's written here, trust the
>   markers and resume from the furthest point they support (PROGRAM §0).
>   Write the *next* unit before starting it, so a crash mid-unit never loses it.
> - **Only final-named files are markers.** The orchestrator writes to
>   `<name>.partial` and renames when complete; a `.partial` file is unfinished
>   work to discard and redo, never a completed unit (PROGRAM §4 Step 3).
>
> **Single operator.** One orchestrator drives the loop at a time. There is no
> locking or ownership token: if you can edit this file, you are the driver. On
> resume, the previous run is by definition no longer running — just continue
> from the markers.

## Position

- **Iteration:** 000 (baseline)
- **Stage:** not started
- **Status:** IDLE — no run in flight
- **Campaign branch:** `campaign-001` (created from `main` when the campaign starts)
- **Last completed unit:** preflight (PROGRAM §2) re-run PASS on 2026-08-14
  with the DeepSeek V4 Flash judge model — 18/18 checks correct
  (`loop/preflight/runs-2026-08-14-deepseek-v4-flash/`): 6/6 PASS-test,
  6/6 repeatability (identical verdict blocks both runs), 6/6 voice probes
  (hedges flagged, bounded claims + present-doubt not flagged).
- **Next unit:** baseline research (§3)

## If you died / were stopped

Nothing was in flight. Preflight is current (2026-08-14, DeepSeek V4 Flash).
Start the baseline at PROGRAM §3, Stage: Research — create the campaign branch
first (`git branch campaign-001 main && git checkout campaign-001`).

## Journal

| Time (UTC) | What happened | Next |
|---|---|---|
| 2026-08-12 | Loop state file created; preflight already PASS (2026-08-07) | baseline research |
| 2026-08-14 | Preflight re-run PASS on DeepSeek V4 Flash (18/18 checks) — prior runs dirs (runs2–runs8) stale on gpt-5.6-sol/gpt-5.6-luna | baseline research |
