# Run report — run-002

**Stage:** A **Scope:** normalized plan + chapters 1–3 **Verdict:** IN PROGRESS

## What ran

Run-002 inherits run-001's accepted research and framing unchanged. H-039 is the sole amendment and invalidates only the plan and downstream chapters.

Native GPT-5.6 Sol at `ultra` generated a normalized 21-chapter, 60,000-word plan. R1 was 11,512 words and review blocked only contradictory M-06 routing and the missing C-21 device. R2 resolved those but introduced one evidence typo; its fresh review additionally found an instruction/threshold conflict and a closing image borrowed from the style guide. R3 resolved all three defects and its final fresh review returned `fit to write from`. All candidates and reviews are preserved under `planning/`.

A funded replacement key then ran Chapter 1 R1 through Opus 4.6 with reasoning disabled (`0` reported reasoning tokens). The 2,265-word draft preserved M-01/M-06 and I-01 but received `REVISE`: M-02 case infidelity, a self-contradictory cake comparison, unsupported EV-08 expansion, an unsupported ease guarantee, omitted SC-08, and no separate ALL-CAPS landing. Prose metrics were also materially off-target (about 47 you/your per 1,000 words, 3% questions, 45% short sentences, 10.5-word average). No reviewer defect traced to context removed from the normalized plan.

## Objective results (`metrics.json`)

Pending Chapters 1–3.

## Judge results (`judgments/judge-summary.json`)

Pending Chapters 1–3.

## Gate verdict

Master-plan gate: PASS on cycle 3 of 3. Chapter 1: REVISE on cycle 1 of 3. Stage A remains pending accepted Chapters 1–3, objective evals, and blind judging.

## Diagnosis

Normalization removed run-001's failure mechanism: none of run-002's blockers involved occurrence counts, duplicated audit/state matrices, repeated SUMMARY wording, or cross-table arithmetic. The plan shrank from run-001's 16,405–19,166 words to 11,512–11,712 words while retaining a coherent arc and exact 60,000-word budget.

It did not make planning one-shot reliable. Two semantic contradictions, one borrowed analogy, and one whole-artifact rewrite regression still required the full three cycles. Therefore H-039's at-most-one-revision prediction failed even though the plan gate passed. The downstream claim remains untested until isolated writers can produce accepted chapters from the normalized cards.

## Hypothesis outcomes

### H-039 — normalized agentic master plan

- **Pre-registered mechanism, lever, controls, prediction:** Duplicated exact representations caused run-001's plan-review failures. Normalize shared decisions once while holding accepted research/framing and Sol `ultra` fixed; predict plan acceptance in at most one substantive revision and Chapter 1 in the same run.
- **Result / deciding evidence:** Run-002 plan reviews contained zero occurrence-count, audit/state-matrix, repeated-SUMMARY, or cross-table-arithmetic blockers. The 21-chapter, 60,000-word plan passed, but only on cycle 3 after unrelated semantic repairs and one rewrite regression. Chapter 1 R1 then failed on execution defects even though every needed mantra, evidence limit, scene, instruction, and anatomy rule was present in its permitted inputs.
- **Causal verdict:** `INCONCLUSIVE` overall, with the bookkeeping submechanism supported and no current evidence of downstream context starvation. The plan cycle-count prediction is falsified; accepted Chapters 1–3 and blind judgments are still required.
- **Rival explanations / signal risk:** False positive—lean cards pass review but starve isolated writers. False negative—three semantic/rewrite defects are incorrectly attributed to normalization despite no deleted-field blocker. Same-model planning remains a confound; fresh reviews reduce memory contamination.
- **Next discriminating test:** Keep R3 plan, style guide, and writer prompt fixed; generate and blindly judge Chapters 1–3. Count against H-039 only failures traceable to context deliberately removed by normalization.

## Amendments proposed for next run

None until completed chapters and blind judgments expose a concrete failure.

## Escalations

Resolved. A funded replacement OpenRouter key authorized the unchanged request; the endpoint autopsy remains in `calibration/ESCALATION.md`.
