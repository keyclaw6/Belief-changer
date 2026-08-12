# Loop Coherence Review — 2026-08-12

Four review passes over the auto-research loop (correctness, failure
robustness, and end-to-end dry-run role-play). The final pass role-played an
actual baseline run — research → plan → write → judge → trace → hypothesize →
record. Per the founder: **nothing here has been implemented**; this is a
report.

## Bottom line

**The loop's core model is coherent and works.** The central chain — run →
measure → hypothesize → change → rerun → keep/revert → record — traces cleanly,
each stage's output feeds the next stage's input, and the epistemology
(one causal change, failure classes not instances, judge/trace separation,
never decide on partial evidence) is consistent across every document. The
back half of the loop (plan → write → judge → trace → decide → record) is
followable from the runbook alone. Stop/continue works. Judges cover Carr-style
+ belief-change well.

The genuine findings cluster in **three places**, ranked by how much they'd
actually bite on a first real run:

### 1. The research stage is the one underspecified part of an otherwise tight runbook
The single place a first-time executor stalls is the front. Three concrete gaps:
- **The "ten research banks" are named as a stable contract, but no file says
  where or as what they live on disk.** Sub-agents are told to "write packets
  into their assigned bank file," yet the research Output block lists only
  `research-log.md`, `lived-experience.md`, `scientific-evidence.md`, `sources/`.
  A fresh research lead has to invent the storage layout.
- **The completion criterion is uncountable as written.** It requires each
  research slot to clear "across ≥3 materially distinct personas," but the
  brief is explicitly "one clear reader" and "persona" is never defined. The
  lead must invent a persona taxonomy before "done" is even measurable.
- **The synthesis contract is out of phase with the brief.** The bank units are
  gated on reproducing the brief's load-bearing belief *exactly*, but the
  brief's keystone belief is `<unfilled>` (it's set later by framing/planning).
  Research literally cannot satisfy the handoff contract until a later stage
  supplies the keystone.

These are flow-level, present-on-day-one issues — not edge cases.

### 2. The completion-marker model equates "file exists" with "work is complete"
Because there is deliberately no deterministic validation, a crash that
truncates a chapter (or a judgment file, or a research bank mid-synthesis)
leaves a file that the recovery cross-check reads as *complete*. Recovery then
resumes *past* it, and the truncation is only caught much later by the judges —
after downstream chapters are already written against the damaged one.
- Safest where it matters most: judging is protected by the Step 6
  all-reports-complete gate (a partial judgment → INCONCLUSIVE, never a wrong
  KEEP). Writing has no such gate, so that's where it actually bites.
- Related: mid-**research** crashes lose all completed-but-unintegrated work
  (the `_rounds/` sub-agent packets aren't a named resume marker), so research
  restarts from zero. Safe (never reuses unaccepted evidence) but re-spends the
  mining budget silently.

### 3. Config ↔ agent-definition drift (mechanical, easy to verify)
A few pin mismatches between `loop/config.yaml` (sole authority) and the
`.pi/agents/*.md` wrappers:
- `plan-reviewer` missing its `:max` reasoning pin; `plan-writer` missing its
  `:high` pin.
- No `.pi` file pins the research **lead's** MiniMax M3 — `researcher.md` pins
  the *sub-agent* model instead. Lead vs sub-agent are conflated in one file.
- `run_preflight.sh` routes judges through the **commandcode** proxy, but
  config routes them through **openai-sub** — so the calibration battery tests
  a route the campaign never uses.
- The **book-arc judge is uncalibrated** — the preflight battery only exercises
  the three chapter judges, never book-arc.

## Smaller observations (recorded, not blocking)
- §0 recovery is clean except a **mid-baseline** crash reads as "baseline
  pending" and could restart research (the results.tsv-row rule only fires
  once a row exists).
- The record-authority direction is slightly circular: Step 7 writes
  results.tsv *last*, but ledger.md claims to copy "verbatim from results.tsv."
- The trace-analyzer's prompt reads `learnings.md` but Step 5 never lists it as
  an input.
- The analyzer never explicitly ranks clusters, so the hypothesizer (a separate
  model with no shared context) picks the target itself — fine for one cluster,
  ambiguous when several compete.
- Judges can't verify two things the vision cares about: subject-specificity
  (is this a real sugar book, not a swapped-noun template) and originality
  (not paraphrasing Carr's prose).
- Generalization (§6) hardcodes quit-sugar paths and a single-book alignment;
  the second subject (quit-smoking) isn't wired through.

## The one honest tension worth naming
The North Star says the goal is **human belief change** and explicitly rejects
surface metrics — but the loop's only success signal is **LLM-judge agreement
with the reference book**. After preflight, no non-LLM ground truth ever
validates the judges. So the loop can be fully "converged" by its own criteria
without any evidence a person's belief moved. The machinery is self-consistent
about the proxy — but it's worth being honest that the proxy *is* the
measurement.

## What's genuinely strong (don't touch)
- The trace→cluster→component→hypothesis chain is the strongest link —
  diagnosis and prescription are cleanly separated, and one-causal-change
  holds.
- The judge decision logic (owner lane decides, others veto only quoted
  material regressions, KEEP tolerates unpredicted improvement, REVERT on new
  failure class) is sound and correctly regression-biased.
- Resumability, patience, inbox, and ledger are well-integrated, not bolted on.
- The writer contract is complete enough to write a real Carr chapter *given* a
  fully-resolved plan — and has a clean single-line refusal when it isn't.

---
*Generated by a multi-agent review swarm; individual dry-run traces and
failure analyses are available in the thread.*
