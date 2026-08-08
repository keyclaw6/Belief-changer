# Dry run — W2 Planning stage (terminal traces)

Simulator: AOG-DRY-02 (Lovelace). No external effects invoked.

## DR-W2-happy — planning + review cycles — BLOCKED (F-02)

| # | Role | Decision / tool / handoff | Output / state after | Evidence |
|---|---|---|---|---|
| 1 | Orchestrator | Spawns plan-writer with exactly 4 files (style guide, brief, lived, sci) | candidate master-plan.md | PROGRAM.md:171-176; plan-writer.md:8-17; config.yaml:36-43 |
| 2 | Plan-writer | Builds cards + inventories; writes candidate | candidate plan exists | master-plan-skill-v2.md:7-20 |
| 3 | Orchestrator | Spawns plan-reviewer (plan + 4 files) | review artifact | plan-reviewer.md:8-14; master-plan-reviewer-v2.md:98-109 |
| 4 | Plan-reviewer | Returns BLOCK lines + `needs changes first` | review identifies plan-owned corrections | master-plan-reviewer-v2.md:80-109; PROGRAM.md:174-177 |
| 5 | Orchestrator → plan-writer | **No compliant handoff exists**: a fresh planning call allows only the original four files and forbids other context; cannot receive the candidate plan or the reviewer's blockers | W2 blocks at its first real revision | master-plan-skill-v2.md:7-14,143-150; spawn task injection index.ts:294-330 |
| 6 | Orchestrator | (hypothetical) if review ends `fit to write from` | accept plan; rebuild alignment if changed | PROGRAM.md:175-177; master-plan-reviewer-v2.md:100-109 |

Terminal state: NOT reachable on the revision path. The reviewer's blockers live in master-plan-review.md; neither the reviewer file nor PROGRAM defines a legal way to compile them into the writer's next four-input call.

## DR-W2-failB — persistent plan BLOCK at cycle 4 — UNDEFINED (F-02)

Cycles 1-3: reviewer keeps returning valid BLOCK; planner skill says re-dispatch "up to three cycles" (master-plan-skill-v2.md:141-150). At cycle 4: re-dispatch violates the stated limit; stopping violates "No review-cycle limit can waive a blocker" (master-plan-reviewer-v2.md:98-109) and PROGRAM's "until fit to write from" (PROGRAM.md:171-177). No escalation or INCONCLUSIVE rule for persistent substantive blockers.

## DR-W2-failC — spawn/transport/route failure — COMPLETES

Retry same role once with same inputs (PROGRAM.md:204-208); retry succeeds → resume; retry fails (transport) → INCONCLUSIVE; route/credential failure → escalate to founder (PROGRAM.md:207-208; config.yaml:6-16). Boundary explicit.
