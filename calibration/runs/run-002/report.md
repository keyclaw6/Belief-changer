# Run report — run-002

**Stage:** A **Scope:** normalized plan + chapters 1–3 **Verdict:** FAIL

## What ran

Run-002 inherits run-001's accepted research and framing unchanged. H-039 is the sole amendment and invalidates only the plan and downstream chapters.

Native GPT-5.6 Sol at `ultra` generated a normalized 21-chapter, 60,000-word plan. R1 was 11,512 words and review blocked only contradictory M-06 routing and the missing C-21 device. R2 resolved those but introduced one evidence typo; its fresh review additionally found an instruction/threshold conflict and a closing image borrowed from the style guide. R3 resolved all three defects and its final fresh review returned `fit to write from`. All candidates and reviews are preserved under `planning/`.

A funded replacement key then ran Chapter 1 R1 through Opus 4.6 with reasoning disabled (`0` reported reasoning tokens). The 2,265-word draft preserved M-01/M-06 and I-01 but received `REVISE`: M-02 case infidelity, a self-contradictory cake comparison, unsupported EV-08 expansion, an unsupported ease guarantee, omitted SC-08, and no separate ALL-CAPS landing. Prose metrics were also materially off-target (about 47 you/your per 1,000 words, 3% questions, 45% short sentences, 10.5-word average). No reviewer defect traced to context removed from the normalized plan.

Opus regenerated the whole chapter as R2 from the same accepted plan and the R1 review, again with reasoning disabled (`0` reported reasoning tokens). R2 is 2,504 words. A fresh Sol `ultra` reviewer returned `ACCEPT`: M-01, M-02, M-06, and I-01 are character-exact; required anatomy, evidence, and scenes are present; and it found no invented evidence, illicit repetition, job drift, or guardrail breach. Rhythm remains more staccato than the guide's norm, but the reviewer judged the residual metric misses non-blocking. The exact accepted artifact is promoted to `production-books/quit-sugar/chapters/chapter-01.md`.

The requested first-prose bird's-eye checkpoint returned `GO`: the artifact tests H-039 without a new method change, preserves reference blindness and method integrity, and makes Chapter 2—not more process work—the correct next artifact.

Chapter 2 R1 then ran through the unchanged Opus baseline with accepted Chapter 1 as its sole continuity artifact. The 3,341-word draft received fresh `REVISE` for six blockers: DEF-01/DEF-02 drift; premature LX-P03; wrong-chapter AN-10; omitted EV-17 and SC-07; unsupported comparative, quantified, or universal claims; and the banned phrase “gives up.” M-09, I-02, anatomy, length, direct address, question rate, and cross-chapter repetition passed. Its 39.1% short-sentence rate and 12.9-word mean remained a quality weakness.

Whole-artifact Chapter 2 R2 corrected those six blockers but expanded to 3,611 words. Its fresh review returned `REVISE`: it echoed M-06 and invoked M-07 before their scheduled ownership, repeated RV-08 verbatim in two unlicensed body locations, omitted DEF-04 and the advisory-box treatment, leaked `AN-08` into reader prose, universalized a lived setup, and remained long and staccato. R3 is the final allowed Chapter 2 revision; it receives both prior reviews so known defects cannot disappear between rounds.

Final Chapter 2 R3 received both accumulated reviews and again used Opus 4.6 with reasoning disabled. Its fresh reviewer found **zero blocking defects**: all assigned definitions, safety boundaries, evidence, scenes, analogies, exercise, continuity duties, M-09, and I-02 were present and faithful, with no illicit full-sentence repetition. It nevertheless returned `REVISE` because the draft expanded again to 3,761 words and retained 36.7% sub-eight-word sentences. Two badly failed quality checks trigger rejection under the fixed contract, so run-002 stops at the three-cycle gate.

## Objective results (`metrics.json`)

Not run: the chapter gate failed before Chapters 1–3 were complete.

## Judge results (`judgments/judge-summary.json`)

Not run: blind judging requires accepted Chapters 1–3.

## Gate verdict

Master-plan gate: PASS on cycle 3 of 3. Chapter 1: PASS on cycle 2 of 3. Chapter 2: FAIL after `REVISE` on cycle 3 of 3. Run-002 fails before objective evals or blind judging.

## Diagnosis

Normalization removed run-001's failure mechanism: none of run-002's blockers involved occurrence counts, duplicated audit/state matrices, repeated SUMMARY wording, or cross-table arithmetic. The plan shrank from run-001's 16,405–19,166 words to 11,512–11,712 words while retaining a coherent arc and exact 60,000-word budget.

It did not make planning one-shot reliable. Two semantic contradictions, one borrowed analogy, and one whole-artifact rewrite regression required the full three cycles. H-039's at-most-one-revision prediction is therefore refuted even though the plan gate passed. Chapter 1 provides one accepted downstream sufficiency sample, and Chapter 2 R3 provides a second semantic-sufficiency sample because its reviewer found every assigned method/evidence duty present.

Chapter 2 R1 is a second discriminating context test. Every omitted, premature, drifted, or prohibited element was unambiguous in the permitted plan/style inputs, including the chapter ownership of LX-P03 and AN-10. The observed mechanism is writer selection and boundary execution, not deleted plan information. R2 therefore changes only one input—the fresh R1 review—and predicts correction without any method-asset amendment; acceptance or a new execution defect will measure writer-review convergence, while only a failure traceable to absent/ambiguous plan context counts against H-039.

R2 falsified one-pass convergence for Chapter 2: it repaired the R1 list but created or retained independent selection, routing, repetition, and completeness defects. R3 then resolved the semantic surface but falsified the explicit size/rhythm prediction. Length moved in the wrong direction across revisions—3,341 → 3,611 → 3,761 words—while short-sentence density improved only from 39.1% → 37.3% → 36.7%. The most supported mechanism is task interference in whole-artifact revision: coverage repairs accreted prose while craft compression remained subordinate. This is distinct from missing plan context and from a reviewer false negative because the final reviewer explicitly certified zero blocking defects and measured both craft failures.

## Hypothesis outcomes

### H-039 — normalized agentic master plan

- **Pre-registered mechanism, lever, controls, prediction:** Duplicated exact representations caused run-001's plan-review failures. Normalize shared decisions once while holding accepted research/framing and Sol `ultra` fixed; predict plan acceptance in at most one substantive revision and Chapter 1 in the same run.
- **Result / deciding evidence:** Run-002 plan reviews contained zero occurrence-count, audit/state-matrix, repeated-SUMMARY, or cross-table-arithmetic blockers. The 21-chapter, 60,000-word plan passed, but only on cycle 3 after unrelated semantic repairs and one rewrite regression. Chapter 1 R2 received fresh `ACCEPT`. Chapter 2 R3 received `REVISE` after the maximum cycle, but its reviewer found zero blocking defects and certified every assigned semantic duty; rejection was solely for length and short-sentence density.
- **Causal verdict:** `MIXED`. The bookkeeping mechanism is supported and no context starvation appeared through two chapters; the at-most-one-revision prediction is refuted, Stage A was not reached, and blind parity remains unknown.
- **Rival explanations / signal risk:** A later chapter may still expose missing lean-card context, so two chapters cannot prove universal sufficiency. Chapter 2's final semantic pass could reflect accumulated reviews rather than the normalized plan alone. Fresh reviews reduce memory contamination, but same-model planning and one writer model remain sampling confounds.
- **Next discriminating test:** Retire H-039 as the active lever. Keep its normalized plan fixed and isolate the observed prose-convergence failure under H-040; only later missing/ambiguous semantic context can reopen the normalization question.

## Amendments proposed for next run

H-040 tests one generic change: after a fresh reviewer certifies zero blocking method/evidence defects but rejects craft metrics, dispatch a fresh Opus 4.6/no-reasoning **prose-only compression edit** of that certified draft. Hold research, framing, plan, prior chapter, writer model, reasoning, and reviewer fixed. The edit may cut, combine, and smooth but may not add arguments, evidence, devices, or semantic work. Predict one pass inside 2,550–3,450 words, materially lower short-sentence density, no new blocking defect, and fresh `ACCEPT`.

## Escalations

Resolved. A funded replacement OpenRouter key authorized the unchanged request; the endpoint autopsy remains in `calibration/ESCALATION.md`.
