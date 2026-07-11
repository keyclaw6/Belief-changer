# Calibration escalation — repeated evidence and chapter-ownership failure

**Date:** 2026-07-11

**Branch:** calibration-lab

**Stage:** A

**Status:** RESOLVED FOR CALIBRATION TEST — H-046 authorized under HARNESS §1; canon merge remains founder-approved

## Trigger

HARNESS §11 requires a stop after three semantic production runs show no gate progress on the same failing dimension. That threshold is met:

| Run | Product attempt | Repeated dimension | Outcome |
|---|---|---|---|
| run-005 | Chapter 3 ordinary cycles | unassigned developmental/advertising causation and promised effects | final R3 REVISE |
| run-006 | whole-rewrite vs scoped-edit A/B | both arms retained universalized installation and premature C-10 mechanism claims | both Sol REVISE; no convergent arm |
| run-008 | one Opus repair after two raw independent Sol reviews | C-10 cue/attention/pull mechanism survived explicit feedback; new evidence-fidelity defects appeared | both fresh Sol REVISE; H-045 refuted |

Run-007 is excluded from the semantic count: Grok returned a regional 403 before inference, no writer ran, and usage stayed unchanged.

No Chapter 3 artifact is promoted. Chapters 1–2 remain the last accepted product artifacts.

## Evidence and causal conclusion

### The plan is not missing the boundary

C-03 assigns EV-01, EV-02, and EV-11: reported reasons, assigned jobs, and felt addiction language. It explicitly forbids claiming advertising created every belief. C-10 alone owns the mixed-evidence anticipation/closure mechanism; C-13 owns bounded commercial optimization; C-15 owns clinical addiction discussion.

The writer repeatedly had this exact context. In run-008 it additionally received two raw Sol reviews that independently named the same boundary. The resulting prose still said the felt grip rises when assumptions are active, introduced cue/attention explanations, and implied that the pull quiets with the assumptions. Feedback incompleteness is therefore refuted as the sufficient cause.

### The smallest remaining generic owner

The shared writer prompt says both "Assertion, not hedging" and that contested evidence must follow the spec. Across repeated generations, firm persuasive completion is dominating the distributed evidence and chapter-ownership limits.

This does not justify a Chapter 3 instruction, sugar-specific fact, new state machine, evidence checklist artifact, or another revision loop. It justifies testing one explicit priority rule in the shared writer prompt.

### Measurement reliability

- Independent Sol-ultra reviews consistently cited exact plan/evidence conflicts and found objective quotation/repetition defects.
- Gemini 3.1 Pro high remains useful for blind product judging, but its positive chapter-review evidence is unreliable in this sample. In run-006 it undercounted both artifacts by roughly 460–500 words while accepting them. In run-008 it called an altered EV-11 quotation exact and missed the C-10 mechanism.
- Grok 4.5 cannot run from this region through the verified OpenRouter/xAI route.

## Proposed one-lever amendment

HARNESS §1 authorizes adding the following behavior-agnostic rule to "prompts/chapter-writer.md" for a calibration-only test immediately after the current assertion rule. Any later merge into canon "main" remains founder-approved:

> **Evidence and chapter ownership outrank assertiveness.** State the assigned belief reframe firmly, but never turn a lived report, analogy, scene, cultural observation, or plausible explanation into a causal mechanism, prevalence or exposure claim, diagnosis, universal pathway, or promised effect unless the current chapter card owns that claim and the evidence ledger's permitted inference supports it. If either condition is absent, stop at the card's observable or belief-level claim—or report the gap; never fill it with persuasive inference.

Add one matching self-check sentence in the existing procedure:

> Trace every causal, mechanism, prevalence, diagnosis, and promised-effect assertion to the current chapter card and a permitted evidence inference; cut it or report a gap if either trace is missing.

These two sentences are one priority-hierarchy lever in one generic asset. They do not prescribe research steps, chapter content, or deterministic prose construction.

## Required validation — H-046

Do not patch Chapter 3 again. If approved:

1. change only the two generic writer-prompt sentences above;
2. hold research, framing, normalized master plan, style guide, reviewer prompt, Opus 4.6 route, reasoning none, and reference blindness fixed;
3. regenerate Chapters 1–3 from fresh writer contexts, sequentially for continuity, without showing any old chapter draft or review;
4. run the normal independent review and objective gates on all three chapters;
5. run the full Stage-A blind pairwise panel against evaluator-only reference chapters before making a causal success claim.

The amendment is not supported merely because Chapter 3 passes. It must eliminate the target evidence/job blockers across the fresh three-chapter sample and produce the preregistered blind product movement. It remains provisional until later chapters and the zero-amendment caffeine holdout.

This multi-chapter restart is the anti-overfit test: the calibration specimen supplies failure evidence, but the candidate factory rule contains no sugar or Chapter 3 logic.

## Calibration-only decision recorded

HARNESS §1 explicitly grants the operator full design authority on "calibration-lab" and says to decide, log, and proceed; HARNESS §11 reserves founder approval for merging prompt changes into canon "main". The exact generic amendment above is therefore authorized for H-046 on the calibration branch only. It is not approved for "main".

H-046 will regenerate Chapters 1–3 from fresh contexts under one frozen prompt version. No old draft or review enters a first-draft call, and no shared change is allowed between chapters. A winning calibration result will be brought back for founder-approved canon merge only after the required product, stability, and holdout evidence.

The calibration-only amendment was committed at "88b6889"; this records the experiment version, not approval for canon "main".

---

## Previous resolved escalation — run-002 writer endpoint

**Resolved:** 2026-07-11. A funded replacement OpenRouter key authorized the unchanged Opus request. Chapter 1 R1 completed as `gen-1783758658-B2u97iZ82TBKd7A1BXkR`; this section remains as the endpoint failure autopsy.

**Run:** `calibration/runs/run-002/`

### Completed before the block

Run-002's normalized R3 master plan passed its final fresh review with `fit to write from`. The accepted plan and all three candidate/review pairs are committed in `5915b9f`.

### Blocking condition

The first real Chapter 1 request used the authenticated OpenRouter route `anthropic/claude-opus-4.6`, `reasoning.effort: none`, and the model's catalog maximum `max_tokens: 128000`. OpenRouter rejected it before generation with HTTP 402. No chapter text or provider generation metadata was produced.

The authenticated credit endpoint reported:

- total credits: `$75.00`
- total usage: `$75.181592239`

The key-detail endpoint's `$10` per-key limit and `$1.806546899` key usage were not account credit; its apparent `$8.193453101` remainder did not authorize the request. The 402 response calculated only 147 affordable completion tokens after input, which could not produce the 2,800-word chapter and was not a quality-valid fallback.

#### Controlled causal check

To test whether requesting the catalog maximum itself caused a false rejection, the operator repeated the complete Chapter 1 request with everything held fixed except `max_tokens`, reduced from 128,000 to 8,000—still well above the 2,800-word chapter target. OpenRouter returned the same HTTP 402 and the same 147-token affordability ceiling. This refuted reservation size as the operative cause. The authenticated key was valid, but account funding was the binding cause; changing the key's separate internal spending limit could not create account credit.

`LITELLM_BASE_URL` and `LITELLM_API_KEY` were absent in the runtime. An initial name-only environment check falsely reported `ANTHROPIC_API_KEY` as present; a non-empty check proved that it was defined but empty, and the direct API correctly returned an authentication error. Claude Code 2.1.146 reported an existing Claude Pro login and accepted the exact `--model claude-opus-4-6 --thinking disabled` controls, but a live zero-cost connectivity call returned 401 because the stored OAuth credential was stale. Reauthentication required the user's browser approval.

### Resolution

A funded replacement OpenRouter key ran the unchanged Chapter 1 request without regenerating research, framing, or the accepted plan and without substituting Muse or another writer.
