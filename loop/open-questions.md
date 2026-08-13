# Open Questions — loop hardening backlog

> Deferred design decisions from the 2026-08-12 orchestration audit (second
> pass). Items 1 and 2 were **REJECTED by the founder on 2026-08-12** — the
> current behavior is accepted as-is. Item 3 records an accepted design choice.
> Kept here as a record of the decisions.

## 1. Stop-guards are technically in the loop's editable surface — REJECTED

`loop/config.yaml` tells the loop it "can hypothesize changes to any value,"
and that file also holds the campaign brakes `strike_limit` (3) and
`max_consecutive_no_improvement` (5). The loop could, in principle, tune those
away instead of fixing the factory. PROGRAM §5 restates the same numbers in
prose, so there are also two copies that can drift.

**Founder decision (2026-08-12): REJECTED** — leave as-is. The stop-guards stay
in the editable config; founder reviews every merge to main, which is the
accepted control.

## 2. Unbounded LLM loops — REJECTED

Three places let a sub-agent loop with no built-in exit: plan-review (no round
cap), research (never declared stuck; depth is sacred), and trace-analyzer (no
explicit retry/INCONCLUSIVE rule, and Step 6's gate keys on judges only).

**Founder decision (2026-08-12): REJECTED** — leave as-is. Unbounded
thoroughness is intentional; the founder would rather the loop run long than
cap depth.

## 3. Single-operator has no concurrency guard (accepted)

The loop is deliberately single-operator: one orchestrator at a time, resume
always continues from markers, no locking. Accepted risk: if two drivers are
ever started against the same campaign, nothing prevents conflicting writes.
If parallel orchestrators ever become a real need, a lease/heartbeat guard
would be added then.
