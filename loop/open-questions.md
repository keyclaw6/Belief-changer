# Open Questions — loop hardening backlog

> Deferred design decisions from the 2026-08-12 orchestration audit (second
> pass). These are genuine design choices, not defects — they need a founder
> decision, so they are recorded here rather than guessed at. None blocks a
> run; each is a spend/robustness consideration once the campaign is under way.

## 1. Stop-guards are technically in the loop's editable surface

`loop/config.yaml` tells the loop it "can hypothesize changes to any value,"
and that file also holds the campaign brakes `strike_limit` (3) and
`max_consecutive_no_improvement` (5). The loop could, in principle, tune those
away instead of fixing the factory. PROGRAM §5 restates the same numbers in
prose, so there are also two copies that can drift.

**Founder decision needed:** should the stop-guards be founder-fixed (read-only
to the loop, like the judges), or is the current "founder reviews every merge
to main" control enough? Recommended: mark them founder-fixed.

## 2. Unbounded LLM loops

Three places let a sub-agent loop with no built-in exit:
- **Plan-review** repeats "until fit to write from" with no round cap.
- **Research** is never declared stuck (depth is sacred) and is excluded from
  the no-progress watchdog — a diverging-but-moving research stage has no
  escalation path.
- **Trace-analyzer** has no explicit retry/INCONCLUSIVE rule, and Step 6's
  decision gate keys on judge reports only.

**Founder decision needed:** whether to add caps/escalation (e.g. plan-review
round cap; a research content-watchdog that escalates after N barren cycles
while never capping productive depth; trace-analyzer retry + validity gate).
These trade unbounded thoroughness against silent spend.

## 3. Single-operator has no concurrency guard (accepted)

The loop is deliberately single-operator: one orchestrator at a time, resume
always continues from markers, no locking. This is simpler and correct for the
intended use. The accepted risk: if two drivers are ever started against the
same campaign, nothing prevents conflicting writes. If parallel orchestrators
ever become a real need, a lease/heartbeat guard would be added then.
