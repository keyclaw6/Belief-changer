# Worker shard — AOG-DRY-02 (book-writing stage dry-run simulator)

- Reviewer: GPT-5.6 Terra medium sub-agent (nickname Lovelace), read-only; no external effects
- Scenarios: W2 planning/review cycles; W3 sequential writing; writer refusal; persistent plan BLOCK; spawn failure; skipped alignment rebuild

## Verdicts

| Scenario | Verdict |
|---|---|
| W2 planning/review cycles | BLOCKED |
| W3 sequential writing | COMPLETES |
| Writer route refusal | COMPLETES-WITH-RISK |
| Persistent plan-review BLOCK at cycle 4 | UNDEFINED |
| Spawn transport/route failure | COMPLETES |
| Skipped alignment rebuild | COMPLETES-WITH-RISK |

## Findings

### 1 (HIGH) — W2 has no compliant revision handback
The planner call is restricted to exactly four inputs and no other context (master-plan-skill-v2.md:7-14); the review output is neither among them nor a permitted read, and the candidate plan is also absent on a revision call. After a `needs changes first` review, no defined actor can convey the blockers/candidate plan to a fresh plan-writer (PROGRAM.md:171-177 says hand back until "fit to write from"). W2 blocks at its first real revision. Reviewer's blockers live in master-plan-review.md; neither the reviewer file nor PROGRAM defines a legal way to compile them into the writer's next four-input call.

### 2 (HIGH) — The fourth review cycle has incompatible instructions and no tie-breaker
Planner contract permits "up to three cycles" (master-plan-skill-v2.md:150); reviewer says no cycle limit may waive a blocker (master-plan-reviewer-v2.md:101-103); PROGRAM requires continuing until acceptance (:171-177). No source selects stop, escalation, or a fourth dispatch.

### 3 (MEDIUM) — A refusal's owner is trusted without validation; repair action never consumed
Writer must name the earliest repair owner and emits `repair_owner_and_regenerate_downstream` (chapter-writer.md:21-27); no role validates the claim or dispatches repair; PROGRAM records the named owner as the iteration finding and ends INCONCLUSIVE (:204-212). A wrong model-selected owner can misdirect later diagnosis. Terminal behavior safely stops downstream writing; the unvalidated diagnostic attribution is the risk.

### 4 (MEDIUM) — Skipped alignment rebuild has no freshness gate and can silently poison judging
Alignment must be rebuilt after an accepted plan change (PROGRAM.md:73-76,171-177; reference-alignment.md:22-26); judges consume the table as their real-chapter/skeleton input (book-arc.md:9-18) and are not instructed to verify it reflects the current plan. A stale existing file permits apparently valid but misaligned verdicts. Missing file would eventually fail a judge call (INCONCLUSIVE); stale existing file is the dangerous case.

## Healthy confirmations
- W3 rolling window is defined and usable: only the immediately previous chapter crosses the writer-to-writer seam; cards + plan inventories provide durable semantic continuity
- Judge receiver contracts explicit and sufficient if alignment is current
- Spawn/transport failure boundary explicit: retry once; route/credential failure escalates; other repeated failures INCONCLUSIVE

## Integrity
- No files written; no services called.
