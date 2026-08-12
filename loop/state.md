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
- **Last completed unit:** none — preflight must be RE-RUN (the judge model
  changed to DeepSeek V4 Flash on 2026-08-12; the 2026-08-07 PASS was on
  gpt-5.6-luna, now void per `loop/HARNESS.md`).
- **Next unit:** preflight (PROGRAM §2), then baseline research (§3)

## If you died / were stopped

Nothing was in flight. Run preflight first (PROGRAM §2 — re-required after the
model change), then start the baseline at PROGRAM §3, Stage: Research.

## Journal

| Time (UTC) | What happened | Next |
|---|---|---|
| 2026-08-12 | Loop state file created; preflight already PASS (2026-08-07) | baseline research |
