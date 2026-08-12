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

## Position

- **Iteration:** 000 (baseline)
- **Stage:** not started
- **Status:** IDLE — no run in flight
- **Owner:** none — when a run starts, the orchestrator writes a unique run
  token here (e.g. `run-<timestamp>-<rand>`) BEFORE setting `IN PROGRESS`, and
  clears it back to `none` when the run ends or parks. A resuming agent that
  finds `IN PROGRESS` must verify no *other* live orchestrator holds this token
  before continuing (PROGRAM §0) — this prevents two actors driving one run.
- **Last completed unit:** preflight (§2) — PASS 2026-08-07 (`loop/preflight/results.md`)
- **Next unit:** baseline research (PROGRAM §3, Stage: Research)

## If you died / were stopped

Nothing was in flight. Preflight already passed; start the baseline at
PROGRAM §3, Stage: Research.

## Journal

| Time (UTC) | What happened | Next |
|---|---|---|
| 2026-08-12 | Loop state file created; preflight already PASS (2026-08-07) | baseline research |
