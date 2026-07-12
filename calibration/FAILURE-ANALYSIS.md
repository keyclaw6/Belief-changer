# Calibration failure analysis and successor handoff

## Executive conclusion

The root orchestrator failed. It turned a simple product-learning loop into a pre-prose artifact-validation program.
Subagents were used as hands, but the root gave them too many serial micro-boundaries and treated nearly every uncertainty as something that had to be eliminated before a draft could exist. That preserved provenance while starving the experiment of product evidence.

The failure was not insufficient model quality, lack of access, or a need for more reasoning. There is no external blocker.
The failure was orchestration: pre-prose certainty was optimized ahead of a frozen Chapters 1–3 product sample.

The successor must preserve method integrity, source honesty, blindness, and run-level causal records while deleting the assumption that every transport detail, review result, and intermediate artifact deserves its own experiment boundary.

The governing product law remains [HARNESS true north](HARNESS.md#true-north-and-compaction-recovery) and the [Stage-A sequencing law](HARNESS.md#6-the-run-lifecycle-every-run-no-exceptions). Once accepted inputs and a usable handoff exist, the next real evidence is prose.

## Exact stopped boundary

Accepted product base at the stop: `calibration-lab` at `e9aeca03ecc72707a0de382db70aebfb36477b31`.
The later stop/handoff commit preserves this analysis, stopped-state records, and commission evidence; it does not semantically accept the commissions, authorize prose, or create an H-050 result.

Accepted and committed:

- H-050's generic planner/reviewer contract is frozen at `b00115dfb085cc7ea9084ff5e1d1b8218ae8c865`.
- The bounded S-021 corrections to framing and lived synthesis are accepted at `f862fd27eff3aa97822b6561e8e1f1c5db0f6b6e`.
- The accepted master-plan R2 is promoted at `d9279d4c4960b0b1daca5e4fdd2cbcc04835a0e1`.
- Its independent review says `fit to write from` in [master-plan-r2-review.md](runs/run-014/planning/master-plan-r2-review.md).
- The accepted production plan is [production-books/quit-sugar/master-plan.md](../production-books/quit-sugar/master-plan.md).
- The last accepted prose remains Chapter 1 from run-002 and Chapter 2 from run-004.

Generated and preserved by the stop handoff, but unaccepted:

- [run-014 CH-01 commission](runs/run-014/commissions/chapter-01.md).
- [run-014 CH-02 commission](runs/run-014/commissions/chapter-02.md).
- [run-014 CH-03 commission](runs/run-014/commissions/chapter-03.md).
- All three are readable, have the expected chapter title, and contain no `COMMISSION BLOCKED` marker.
- Those checks are mechanical only; no whole-set semantic/source audit has accepted them.

Not produced:

- No run-013 or run-014 chapter, run-014 metric, grounded prose audit, product panel, or H-050 causal result.

Current durable records now explicitly mark calibration `STOPPED`: [STATE.md](STATE.md), the [run-014 report](runs/run-014/report.md), and the [final ledger row](runs/LEDGER.md). They preserve the accepted product base and the unresolved resume gate without implying commission acceptance.

The three commission candidates were untracked at the moment of stop. The handoff commit preserves them as evidence without semantic acceptance. Do not treat preservation as a PASS or overwrite them on resume. The unrelated `Belief-changer/` path remains protected and out of scope.

## Evidence that orchestration went poorly

Runs 013–014 used approximately 22 model calls and 2.12 million input tokens without producing a new chapter. The count is conservative because run-013's final direction audit is not included in the 598,002-token subtotal.

Run-013 used at least 11 calls and 598,002 input tokens: an H-050 contract audit, three complete plan generations, three complete plan reviews, three commission calls, and one whole-set audit.

It ended `INCONCLUSIVE_INPUT_AUTHORITY_CONFLICT_NO_PROSE`; see the [run-013 report](runs/run-013/report.md) and [manifest](runs/run-013/manifest.json).

Run-014 used 11 calls and about 1,522,596 input tokens through the current commissions: one direction audit, two source-repair editor calls, one full-file repair review, two plan generations, two plan reviews, and three commission calls.

At the moment of stop, before the handoff commit preserved the commission set, run-014 already contained 82 files and about 2.2 MB under [runs/run-014](runs/run-014/), with 12 prior commits after the run-013 boundary.

Runs 013–014 added 25 commits after the run-012 product panel without adding a chapter; the sequence runs from `49e4f14` through `e9aeca0`.

The two-line production correction at `f862fd2` arrived with more than one thousand lines of records. Plan commits `806dfbb`, `c479f24`, and `c250e48` each added roughly 2,300–3,000 lines before prose.

Before this handoff, [STATE.md](STATE.md) called itself concise but was about 32 KB and duplicated manifest history, hashes, usage, and diagnostics. It became another context burden instead of a compass.

This violated the repository's own warning that deterministic and documentary bloat is a failure mode; see [HARNESS tooling doctrine](HARNESS.md#13-tooling-doctrine-prompts-over-determinism).

## Legitimate quality catches

Not all delay was waste.

Run-012's complete batch and v2.3 panel were necessary product evidence. They showed efficacy `0.25`, craft failures for Chapters 2–3, material invention in all three drafts, and a favorable method-integrity contrast that could not waive those failures; see the [run-012 report](runs/run-012/report.md).

The run-013 [commission-set audit](runs/run-013/audits/commission-set-audit.md) caught a real source-authority defect: S-021 did not support assigning a 15-plus-year duration to separately reported daily management actions. Writing from that fusion would have violated evidence ownership.

The run-014 [R1 plan review](runs/run-014/planning/master-plan-r1-review.md) caught two material defects before writing:

- CH-18 would have forced an invented first-person voice.
- M-10 routing contradicted the CH-23 card.

Generating the three commissions simultaneously was correct. Freezing all drafts before chapter review remains correct. Keeping product judges blind to packets while retaining a grounded audit remains correct.

These safeguards should stay; they do not justify the surrounding process expansion.

## Avoidable waste and root causes

### 1. Pre-prose certainty replaced the product sample

The root treated plan acceptance, transport validity, exact hashes, direction audits, and commission acceptance as successive products. They are prerequisites, not the outcome. The result was abundant reproducibility evidence and almost no evidence that the book improved.

### 2. An upstream defect was followed by another downstream plan

Once run-013's audit showed that accepted syntheses conflicted with S-021, the owning defect was known. R3 could not reconcile incompatible authorities; it satisfied packet authority and failed a synthesis-only reviewer. The root should have moved directly to source correction; see [direction-cycle-cap.md](runs/run-013/audits/direction-cycle-cap.md).

### 3. The clean-rerun law over-invalidated accepted structure

After a two-line correction, the root prohibited reuse of run-013's accepted R2 architecture. A fresh plan introduced unrelated CH-18 and M-10 defects, cost another cycle, and added stochastic resampling as a causal rival. A bounded full-plan revision plus complete review would have preserved unaffected architecture.

### 4. A missing terminal LF caused semantic resampling

Input-repair R1 was semantically plausible but rejected because its diff lacked a final newline. The root then commissioned a 310,797-input-token editor and 666,187-input-token review. A raw-preserving deterministic envelope repair or complete-file output would have avoided resampling meaning.

### 5. Per-call artifacts and micro-commits became the work

Almost every call acquired an assembled prompt, wrapper, input manifest, command metadata, raw stream, stderr, mechanical validation, final artifact, four record updates, and a commit. Git is canonical, but the [HARNESS records law](HARNESS.md#10-observability--records) requires reconstructability, not maximal ceremony.

### 6. A stale deterministic gate blocked a valid review

The canonical gate required live outcome-only reviews to repeat the literal model roster. A valid Sol review failed until `0d2c6f4c54990312a4dd165849a34246b3ccd3a9` removed the requirement. This was validator debt from restating documentation as a live-artifact contract.

### 7. STATE became a second manifest

The root copied micro-boundary history into [STATE.md](STATE.md), obscuring the only recovery facts that matter: accepted product, hypothesis, accepted inputs, next artifact, and blocker. Recovery became slower and more drift-prone.

### 8. The writer contract and experiment handoff disagree

The live [chapter-writer prompt](../prompts/chapter-writer.md) says the writer's only semantic source is the complete master plan plus style guide and previous chapter.
It explicitly tells the writer to resolve IDs from the master plan and says everything needed must be there.

H-049/H-050 execution instead built source-grounded authoritative semantic commissions and intended the writer to receive the current commission, style guide, and previous chapter while excluding the master plan.
That commission-only contract is recorded in the [run-012 manifest](runs/run-012/manifest.json) and carried forward by [run-014](runs/run-014/manifest.json).

This mismatch is unresolved.
Sending the stale writer prompt with a commission in place of the master plan creates conflicting instructions.
Sending both plan and commission widens context, breaks the held-constant H-050 handoff, and may recreate the plan-inventory interference the commissions were designed to remove.

## False-positive and false-negative risks

False-positive risks:

- Treating `fit to write from`, `77/77`, direction-audit `GO`, or a valid commission title as product improvement.
- Treating commission composition feasibility as H-050 support before prose and blind judging exist.
- Treating blind integrity preference as source fidelity; run-012's judges could not see packets.
- Attributing a better run-014 product solely to H-050 after source inputs and the sampled plan changed.
- Treating the three current commissions as accepted because none emitted `COMMISSION BLOCKED`.

False-negative risks:

- Rejecting useful judge instruments because stochastic secondary labels or tie-boundary scores differ across fresh contexts.
- Rejecting semantically usable output for a lossless transport defect such as a missing terminal LF.
- Letting brittle tests reject valid outcome artifacts for omitted documentation text.
- Making H-050 `INCONCLUSIVE` for any grounded defect and then failing to collect the separate blind product signal.
- Stopping a whole product batch for a localized input conflict instead of correcting the owning input and resuming the shortest valid downstream path.

## Unresolved writer-input fork

No Opus call is authorized until the root explicitly chooses Option A or Option B and records why.
Silence or an implicit wrapper override is not a choice.

### Option A — preserve run-014 H-050 continuity

Use the current frozen `prompts/chapter-writer.md` bytes but dispatch the held-constant commission-only runtime inputs used by H-049/H-050:

- Writer prompt.
- Complete style guide.
- Current chapter's accepted semantic commission.
- Immediately previous run-014 chapter only; none for Chapter 1.

Do not include the master plan or raw packets.
The dispatch wrapper must state that the supplied commission is the authoritative semantic work order for this experiment despite stale prompt references to `master-plan.md`.

Benefit: preserves the intended H-050 source-grounded handoff and run-014 causal continuity.
Risk: the prompt text remains internally inconsistent, so a writer violation may make H-050 attribution ambiguous or `INCONCLUSIVE`.

### Option B — fix the generic writer contract and start a new run

Amend [prompts/chapter-writer.md](../prompts/chapter-writer.md) behavior-agnostically so its declared inputs and ID-resolution instructions explicitly use the authoritative semantic commission rather than the complete master plan.
Independently review and freeze that one generic contract change.
Start a new run, reuse accepted upstream research, framing, and planning artifacts unless the writer-contract change truly invalidates them, and regenerate only causally invalidated downstream work.

Benefit: restores one unambiguous factory interface and is more likely to produce interpretable writing behavior.
Cost: sacrifices run-014 H-050 causal continuity because the writer prompt becomes a second lever.
Run-014 must then close as an implementation-boundary stop, not as H-050 support or refutation.

**Recommendation:** after the founder explicitly resumes calibration, prefer and record Option B because one unambiguous universal writer interface matters more than salvaging run-014 attribution. Choose and record either Option A or Option B before auditing the preserved commissions; the audit is independent of that writer fork, and both the recorded choice and a whole-set PASS remain mandatory before any Opus call.

## Successor operating rules

1. One run means one product batch, not one infrastructure or input-repair episode.
2. Follow one visible critical path: accepted inputs → plan → commissions → Chapters 1–3 → measurement.
3. Allow at most one correction cycle at an owning pre-prose layer before an explicit root or founder decision.
4. Fix defects at their nearest owner and regenerate only genuinely invalidated downstream artifacts.
5. Never turn a lossless transport defect into a semantic resample; preserve raw bytes and record deterministic envelope repair.
6. Use one small transport recorder with uniform filenames: input manifest, raw stream, final artifact, compact metadata.
7. Keep `STATE.md` to the five recovery facts and put history only in run manifests and reports.
8. Commit coherent boundaries: accepted input repair, accepted plan, accepted commission set, frozen prose batch, completed measurement.
9. Keep the validated v2.3 judge instrument frozen; do not resume judge-taxonomy research during a product iteration.
10. Once three readable drafts exist, always collect objective, grounded, and blind product evidence even when one gate fails.
11. A failed grounded audit blocks promotion and causal attribution, but it does not erase the separate product signal.
12. Direction auditors test whether the next action creates or evaluates product; they do not ratify an already elaborate process.

## Exact resume gate and order

While calibration is `STOPPED`, there is no immediate artifact and no authorized call.

After the founder explicitly resumes calibration, follow this order without substitution:

1. Choose Option A or Option B and record the decision and causal consequence.
2. Freeze and verify the preserved run-014 commission candidates against their handoff hashes.
3. Run one whole-set audit of those commissions against:

- The accepted production master plan.
- Their exact assigned accepted packets.
- The frozen generic commissioner contract.
- H-050's composition-feasibility contract.

The audit is writer-fork-independent: it reports only `PASS` or `BLOCK` per chapter and for the set and does not rewrite anything.
Do not add another plan, reviewer, schema, prompt audit, direction audit, or record migration between the recorded fork choice and this audit.

After that audit:

- If any commission is materially blocked, make zero Opus calls, fix the nearest owning artifact once, and re-audit only the causally invalidated set. Revisit the recorded fork only if that correction changes its stated writer interface or causal boundary.
- If the set passes, execute the already recorded Option A or Option B writer path.
- Only a recorded fork choice plus whole-set PASS authorizes an Opus 4.6 reasoning-disabled Chapters 1–3 batch.
- Freeze all three readable first drafts before any chapter review or revision.
- Run objective metrics, grounded audits, and the frozen blind panel before forming another hypothesis.

Until both conditions are met—whole-set commission PASS and explicit writer-input choice—make zero Opus calls.

This document is the successor's stop sign and shortest safe route back to product evidence.
