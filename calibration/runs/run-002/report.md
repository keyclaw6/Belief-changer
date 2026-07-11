# Run report — run-002

**Stage:** A **Scope:** normalized plan + chapters 1–3 **Verdict:** IN PROGRESS

## What ran

Run-002 inherits run-001's accepted research and framing unchanged. H-039 is the sole amendment and invalidates only the plan and downstream chapters.

Native GPT-5.6 Sol at `ultra` generated a normalized 21-chapter, 60,000-word plan. R1 was 11,512 words and review blocked only contradictory M-06 routing and the missing C-21 device. R2 resolved those but introduced one evidence typo; its fresh review additionally found an instruction/threshold conflict and a closing image borrowed from the style guide. R3 resolved all three defects and its final fresh review returned `fit to write from`. All candidates and reviews are preserved under `planning/`.

A funded replacement key then ran Chapter 1 R1 through Opus 4.6 with reasoning disabled (`0` reported reasoning tokens). The 2,265-word draft preserved M-01/M-06 and I-01 but received `REVISE`: M-02 case infidelity, a self-contradictory cake comparison, unsupported EV-08 expansion, an unsupported ease guarantee, omitted SC-08, and no separate ALL-CAPS landing. Prose metrics were also materially off-target (about 47 you/your per 1,000 words, 3% questions, 45% short sentences, 10.5-word average). No reviewer defect traced to context removed from the normalized plan.

Opus regenerated the whole chapter as R2 from the same accepted plan and the R1 review, again with reasoning disabled (`0` reported reasoning tokens). R2 is 2,504 words. A fresh Sol `ultra` reviewer returned `ACCEPT`: M-01, M-02, M-06, and I-01 are character-exact; required anatomy, evidence, and scenes are present; and it found no invented evidence, illicit repetition, job drift, or guardrail breach. Rhythm remains more staccato than the guide's norm, but the reviewer judged the residual metric misses non-blocking. The exact accepted artifact is promoted to `production-books/quit-sugar/chapters/chapter-01.md`.

The requested first-prose bird's-eye checkpoint returned `GO`: the artifact tests H-039 without a new method change, preserves reference blindness and method integrity, and makes Chapter 2—not more process work—the correct next artifact.

Chapter 2 R1 then ran through the unchanged Opus baseline with accepted Chapter 1 as its sole continuity artifact. The 3,341-word draft received fresh `REVISE` for six blockers: DEF-01/DEF-02 drift; premature LX-P03; wrong-chapter AN-10; omitted EV-17 and SC-07; unsupported comparative, quantified, or universal claims; and the banned phrase “gives up.” M-09, I-02, anatomy, length, direct address, question rate, and cross-chapter repetition passed. Its 39.1% short-sentence rate and 12.9-word mean remained a quality weakness.

Whole-artifact Chapter 2 R2 corrected those six blockers but expanded to 3,611 words. Its fresh review returned `REVISE`: it echoed M-06 and invoked M-07 before their scheduled ownership, repeated RV-08 verbatim in two unlicensed body locations, omitted DEF-04 and the advisory-box treatment, leaked `AN-08` into reader prose, universalized a lived setup, and remained long and staccato. R3 is the final allowed Chapter 2 revision; it receives both prior reviews so known defects cannot disappear between rounds.

## Objective results (`metrics.json`)

Pending Chapters 1–3.

## Judge results (`judgments/judge-summary.json`)

Pending Chapters 1–3.

## Gate verdict

Master-plan gate: PASS on cycle 3 of 3. Chapter 1: PASS on cycle 2 of 3. Chapter 2: REVISE on cycle 2 of 3. Stage A remains pending accepted Chapters 2–3, objective evals, and blind judging.

## Diagnosis

Normalization removed run-001's failure mechanism: none of run-002's blockers involved occurrence counts, duplicated audit/state matrices, repeated SUMMARY wording, or cross-table arithmetic. The plan shrank from run-001's 16,405–19,166 words to 11,512–11,712 words while retaining a coherent arc and exact 60,000-word budget.

It did not make planning one-shot reliable. Two semantic contradictions, one borrowed analogy, and one whole-artifact rewrite regression still required the full three cycles. Therefore H-039's at-most-one-revision prediction failed even though the plan gate passed. Chapter 1 now provides one positive downstream sufficiency sample: an isolated writer corrected all execution defects from the lean card and a review, without a plan or prompt amendment. Chapters 2–3 and blind product judgments are still required before a causal verdict.

Chapter 2 R1 is a second discriminating context test. Every omitted, premature, drifted, or prohibited element was unambiguous in the permitted plan/style inputs, including the chapter ownership of LX-P03 and AN-10. The observed mechanism is writer selection and boundary execution, not deleted plan information. R2 therefore changes only one input—the fresh R1 review—and predicts correction without any method-asset amendment; acceptance or a new execution defect will measure writer-review convergence, while only a failure traceable to absent/ambiguous plan context counts against H-039.

R2 falsified one-pass convergence for Chapter 2: it repaired the R1 list but created or retained independent selection, routing, repetition, and completeness defects. This does not count against H-039 because DEF-04, mantra debut schedules, analogy ownership, and non-mantra repetition rules were all available. The remaining alternative is writer reliability under a large but sufficient context. R3 holds every asset and runtime setting constant, adds the accumulated reviews, and predicts no known defect plus compliance with the target length band.

## Hypothesis outcomes

### H-039 — normalized agentic master plan

- **Pre-registered mechanism, lever, controls, prediction:** Duplicated exact representations caused run-001's plan-review failures. Normalize shared decisions once while holding accepted research/framing and Sol `ultra` fixed; predict plan acceptance in at most one substantive revision and Chapter 1 in the same run.
- **Result / deciding evidence:** Run-002 plan reviews contained zero occurrence-count, audit/state-matrix, repeated-SUMMARY, or cross-table-arithmetic blockers. The 21-chapter, 60,000-word plan passed, but only on cycle 3 after unrelated semantic repairs and one rewrite regression. Chapter 1 R1 failed on supplied-context execution defects; whole-artifact R2 corrected all six and received fresh `ACCEPT` without changing the lean plan, writer prompt, style guide, model, or reasoning mode. Chapter 2 R1 failed on six directly supplied or contradicted execution defects. R2 repaired those but introduced or retained a new set of routing, repetition, completeness, and craft failures; again no blocker required information deleted by normalization.
- **Causal verdict:** `INCONCLUSIVE` overall, with the bookkeeping submechanism supported and one positive downstream-sufficiency sample. The plan cycle-count prediction is falsified. Chapter 1 acceptance is evidence against context starvation, but Chapters 2–3 and blind judgments are still required.
- **Rival explanations / signal risk:** False positive—Chapter 1's entry-contract card is sufficient while later cards or continuity seams are starved. False negative—independent writer defects are blamed on normalization despite supplied context. Same-model planning and a single accepted chapter remain sampling confounds; fresh reviews reduce memory contamination.
- **Next discriminating test:** Run the final whole-artifact Chapter 2 R3 from both accumulated reviews with every asset, model, and reasoning setting fixed. If accepted, generate Chapter 3 with only accepted prior-chapter continuity and run objective and blind pairwise judgments. Count against H-039 only failures traceable to context deliberately removed by normalization.

## Amendments proposed for next run

None until completed chapters and blind judgments expose a concrete failure.

## Escalations

Resolved. A funded replacement OpenRouter key authorized the unchanged request; the endpoint autopsy remains in `calibration/ESCALATION.md`.
