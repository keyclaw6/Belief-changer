# Open Questions — loop hardening backlog

> Deferred design decisions and parked founder ideas. Items 1 and 2 were
> **REJECTED by the founder on 2026-08-12** — the current behavior is accepted
> as-is. Item 3 records an accepted design choice. Items 4–5 are parked
> (2026-09-04). Kept here as a record of the decisions. Nothing in the loop
> reads this file as a hypothesis source.

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

## 4. Chapter reviewer after each written chapter — PARKED (founder, 2026-09-04)

Idea: after the writer returns chapter N, a fresh `chapter-reviewer` sub-agent
reads the accepted master plan, chapter N's card, and the written chapter, and
returns feedback on plan fidelity — including "lengthen"/"shorten" against the
card's word budget — before the orchestrator writes the final `chapter-NN.md`
(mirrors the plan-writer → plan-reviewer loop that already exists).

Status: not built, not a hypothesis. It is a factory-architecture change (new
role contract under `prompts/`, PROGRAM §4 Step 3 Writing stage today is
"writer only, chapter 01 → last", a `.pi/agents/` adapter, a HARNESS capability
row, a founder-chosen model in `loop/config.yaml`, and on Cursor a change to
`scripts/loop-runner/write_replicate.py`). It therefore needs a founder-
authorized PROGRAM edit and its own baseline; the hypothesizer may not propose
it and it must never sit in `loop/inbox/`.

Try condition: after the 019 Spark 1.3 baseline census AND after the one-
sentence writer word-budget line has had its chance. Earn it with evidence: a
plan-fidelity class (`compliance-missing`, `journey-incomplete`, or delivered
length still > 20 % under plan) persisting at prompt level — i.e. when
PROGRAM §5's 3-strike PIVOT from prompt → structure fires for that class.
Try once, as a baseline (research + plan reused, writing stage changed, two
books, full panel). Reviewer sees plan + card + chapter only — never GSBS,
never a judge prompt (judges measure; the reviewer is a factory component).
Cap: one review, one rewrite per chapter, no open loop.

Also: `prompts/style-guide.md` already says "the chapter reviewer judges the
actual text" — a reviewer that does not exist. Fix that sentence when the
writer-budget line lands, or when this item is built, whichever is first.

## 5. Factory robustness (resume-after-stop) — harness work, not a loop iteration

Robustness is a harness property: the conversation must resume from the
furthest on-disk marker after any stop. Improvements are made only in the
harness bindings — pi: `pi-goal-x` goal settings (`/sisyphus-direct`,
`/goal-direct`, `agent_settled`), `pi-provider-fallback`; Cursor:
`.cursor/hooks/loop-continue.py` and its `loop_limit`s — or as a thin
durability layer (Temporal-style) that re-enters the same conversation.
Never a Makefile / `run_factory.py` / cron driver, never a continue-loop
encoded in prompts or skills, never a change to the KEEP object. Evidence
for a fix is a stall in `loop/state.md`'s journal or a hook log; the fix is
made outside campaign iterations (like judge calibration) and needs no
baseline because it changes no factory prompt.
