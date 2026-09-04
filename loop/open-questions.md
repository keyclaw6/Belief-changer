# Open Questions — loop hardening backlog

> Deferred design decisions and parked founder ideas. Items 1 and 2 were
> **REJECTED by the founder on 2026-08-12** — the current behavior is accepted
> as-is. Item 3 records an accepted design choice. Items 4–7 are parked
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

## 5. Factory robustness (resume-after-stop) — DONE (2026-09-04, 021+)

Robustness is a harness property: the conversation must resume from the
furthest on-disk marker after any stop. 019/020 breaks were inside a runner
or a tool-call stream (judge hang, Muse 429, write stream drop, judge
`exit -9`), not a conversation death the stop hook missed. Three native
fixes, no Temporal:

1. `judge_replicate.py`: 600s timeout, one in-runner retry, a failed judge
   does not abort siblings.
2. `muse_client.py`: 429 in the transient set, 90s × up to 4 on that route.
3. Each runner starts in its own tmux session; the conversation waits with
   `while tmux has-session; do sleep 60; done` (not `tmux wait-for`).

Never a Makefile / `run_factory.py` / cron driver, never a continue-loop
encoded in prompts or skills, never a change to the KEEP object. No hook
or `loop-continue.py` change. Revisit Temporal only if the journal shows a
conversation death the hook did not re-enter.

## 6. Anti-slop skills (stop-slop, avoid-ai-writing) — PARKED (founder, 2026-09-04)

Two public skills that strip generic LLM tells from prose:
<https://github.com/hardikpandya/stop-slop> (bans throat-clearing, adverbs,
binary contrasts, rhetorical "What if", lazy extremes, em dashes; 1–10
scoring) and <https://github.com/conorbronsdon/avoid-ai-writing>
(rewrite/detect/edit modes; chatbot openers, promotional inflation,
"leverage/delve/tapestry", 72 pattern categories). Neither repo is cloned
here; both are referenced by URL only.

Status: not a hypothesis now, never in `loop/inbox/`. When tried, the form
is a **selective import** of a short filtered list into
`prompts/style-guide.md` Part B as one bound change within the
hypothesizer's budget. Not a new skill file, not a fifth writer input
(that is a PROGRAM Step 3 edit and is not authorized here). Never imported
into a judge.

**Do not paste wholesale, do not fight the Carr reframe.** Several core
rules in both skills attack the method itself and must not be imported:
the ban on "Not X. It's Y." and its split-sentence form (the
rescuer-as-perpetrator inversion, style-guide §4 and §5.4 "doing TO
you vs. doing FOR you"); the ban on every/always/never and flat verdicts
(fidelity doctrine; hedging the assigned verdict is already BLOCKING);
the ban on questions (Carr's live question is 0 in the voice judge; only
the stage-direction label is noted); the ban on short fragments and on
all adverbs (surface metrics the panel is forbidden to score); any 1–10
"authenticity" scoring. What plausibly survives: chatbot openers and
throat-clearing, the coach/hollow-intensifier phrases the voice judge
already lists under `coach-register`, promotional vocabulary, summary
closers, stacked-triplet padding, and hedges on the method promise.

**Judge-blindness risk, accepted:** the panel has no "slop" class and must
not get one (North Star: judges do not score "sounding literary" divorced
from belief-change effect). KEEP reads the PRIMARY class only. The import
can register only through `factory-speech` (blocking variant), the two
hedge classes, or noted `coach-register` counts; only the first three can
carry a KEEP. Both books may read better and the iteration still be
REVERT. That is the KEEP object working, not a judge defect. REVERT never
deletes the idea; record the result here.

Try condition: after the 019 Spark 1.3 baseline census, and only when the
census PRIMARY is `factory-speech`, `assigned-verdict-hedge`, or
`method-promise-hedge`. Rides as a secondary bound change beside the
primary hypothesis, never as a standalone iteration. A belief-mechanic or
journey PRIMARY is never a trigger.

## 7. Write replicate A and B in parallel — AUTHORIZED 2026-09-04, built for 021+

Why it was serial: PROGRAM §4 Step 3 wrote A into the live
`production-books/quit-sugar/chapters/`, snapshotted, wiped, then wrote B
into the same directory. Two replicates at once collided on
`chapter-NN.md`. Within one book chapters stay sequential (each spawn
receives the previous chapter); that does not change.

Not a measurement risk: A and B start from identical inputs and judges
already read from the replicate tree. Caveat: two Muse streams double
instantaneous Zen load → more 429s (item 5's 90s retry covers it) and a
likelier Go→Zen or Zen→Vercel fallback on one replicate, logged as the
existing route confound.

Shape: each replicate writes/reads
`loop/iterations/NNN/replicate-{a,b}/chapters/`. Live dir is filled once at
Step 6 from replicate A on KEEP. Two `write_replicate.py` processes, one
tmux session each. No worktrees. Judge A starts when write A's session
ends — wait on A's session alone, not on both.

Status: AUTHORIZED 2026-09-04, built for 021+. `write_replicate.py` uses
the replicate chapter tree. `judge_replicate.py` runs 8-wide, one runner
at a time. Pi adapter unchanged.
