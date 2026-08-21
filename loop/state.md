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

- **Iteration:** 005 (pivot: writer-prompt Binding craft after plan-skill 3-strike)
- **Stage:** HYPOTHESIZER — 004 REVERT recorded. Founder authorized through 008. Spawning hypothesizer for 005.
- **Status:** IN PROGRESS
- **Campaign branch:** `campaign-001`
- **Last completed unit:** iter-004 REVERT (records on campaign; factory change not promoted).
- **Next unit:** hypothesizer → worktree iter-005 → apply → plan/write/judge/decide. Continue through 008; stop after 008.

## If you died / were stopped

004 REVERT is recorded. Plan-skill has 3 consecutive REVERTs on re-argument class — pivot off plan-skill. Resume at 005 hypothesizer (prefer writer-prompt Binding craft). Continue through 008 then STOP. Writer: Vercel Muse Spark. Judges: composer-2.5. Do not re-run 001–004. Do not start 009. Do not restore the project stop hook.

## Journal

| Time (UTC) | What happened | Next |
|---|---|---|
| 2026-08-21 | EXEC-004 COMPLETE. Panel 64/64: belief 21/21, reader 16/21, voice 3/21, book-arc FAIL. A01 closed; class mutated. **REVERT.** Plan-skill 3-strike — pivot. | hypothesizer 005 |
