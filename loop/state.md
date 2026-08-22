# Loop State — the live checkpoint

> The orchestrator updates this file at every stage boundary and before any
> long wait. A fresh agent reads it first (PROGRAM §0) and can continue the
> run from exactly here.

## Position

- **Iteration:** 006
- **Stage:** HYPOTHESIZER — 005 REVERT recorded. Continue through 008.
- **Status:** IN PROGRESS
- **Campaign branch:** `campaign-001`
- **Last completed unit:** iter-005 REVERT (records on campaign).
- **Next unit:** hypothesizer 006 → worktree → apply → write/judge/decide.

## If you died / were stopped

005 REVERT recorded. Resume hypothesizer 006. Do not repeat 005 Binding-craft wording. Stop after 008 recorded.

## Journal

| Time (UTC) | What happened | Next |
|---|---|---|
| 2026-08-22 | iter-005 REVERT: voice 0/18, book-arc FAIL. Writer silent-execution insufficient. | hypothesizer 006 |
