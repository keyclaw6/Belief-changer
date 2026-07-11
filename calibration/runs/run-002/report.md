# Run report — run-002

**Stage:** A **Scope:** normalized plan + chapters 1–3 **Verdict:** BLOCKED AT WRITER ENDPOINT

## What ran

Run-002 inherits run-001's accepted research and framing unchanged. H-039 is the sole amendment and invalidates only the plan and downstream chapters.

Native GPT-5.6 Sol at `ultra` generated a normalized 21-chapter, 60,000-word plan. R1 was 11,512 words and review blocked only contradictory M-06 routing and the missing C-21 device. R2 resolved those but introduced one evidence typo; its fresh review additionally found an instruction/threshold conflict and a closing image borrowed from the style guide. R3 resolved all three defects and its final fresh review returned `fit to write from`. All candidates and reviews are preserved under `planning/`.

## Objective results (`metrics.json`)

Pending Chapters 1–3.

## Judge results (`judgments/judge-summary.json`)

Pending Chapters 1–3.

## Gate verdict

Master-plan gate: PASS on cycle 3 of 3. Stage A remains pending Chapters 1–3, objective evals, and blind judging.

## Diagnosis

Normalization removed run-001's failure mechanism: none of run-002's blockers involved occurrence counts, duplicated audit/state matrices, repeated SUMMARY wording, or cross-table arithmetic. The plan shrank from run-001's 16,405–19,166 words to 11,512–11,712 words while retaining a coherent arc and exact 60,000-word budget.

It did not make planning one-shot reliable. Two semantic contradictions, one borrowed analogy, and one whole-artifact rewrite regression still required the full three cycles. Therefore H-039's at-most-one-revision prediction failed even though the plan gate passed. The downstream claim remains untested until isolated writers can produce accepted chapters from the normalized cards.

## Hypothesis outcomes

H-039: `TESTING`. Mechanism supported for eliminating denormalized-bookkeeping failures; cycle-count prediction falsified; downstream sufficiency pending Chapters 1–3.

## Amendments proposed for next run

None until completed chapters and blind judgments expose a concrete failure.

## Escalations

The exact Opus 4.6 reasoning-none Chapter 1 request was rejected before generation with HTTP 402. OpenRouter reports `$75.181592239` total usage against `$75.00` total credit; only 147 completion tokens were affordable after input. LiteLLM is not configured. See `calibration/ESCALATION.md`. No writer substitution or undersized generation was attempted.
