# Future autoresearch hypotheses

These are **unfrozen, untested hypotheses**, not active factory rules. The host autoresearch controller may select, refine, reject, or combine them only after reading the current durable evidence and `loop/prompts/hypothesizer.md`. Do not silently apply them to production prompts.

## Writing-system hypotheses from 2026-09-29 review

### W1 — authored-naturalness restraint
Current v2 already says to stop when the chapter's work is done and not pad to a quota. Test whether one additional lightweight instruction improves natural structure without weakening argument coverage:

> Let the material and the reader's live objection determine the order and natural stopping point. Do not add a preview, recap, lesson, CTA, or symmetry merely to make the chapter feel complete.

Hold brief, research, accepted plan and generator constant. Evaluate task quality separately from authored naturalness. Include at least one chapter where explicit structure is genuinely useful; over-applying this rule must be allowed to lose there.

### W2 — refinement-utility chapter reviewer
Compare the current comprehensive reviewer with a bounded refinement-utility variant that defaults to KEEP/ACCEPT when a careful revision is not materially better, names at most 1–2 high-leverage non-truth/safety defects, identifies protected strengths, states the reader consequence, and asks for the smallest repair.

Truth, attribution and safety checks remain non-negotiable and may still require all necessary findings. Judge this hypothesis by the quality of the resulting revision, not by the sophistication of the critique.

Test convergence explicitly: one writer→reviewer→writer cycle by default; a second stylistic/editorial cycle only when a concrete inherited defect remains.

### W3 — authored naturalness as an outer evaluation dimension
Test whether a separate blinded evaluator can distinguish useful authored naturalness from superficial anti-AI styling. The evaluator should ask whether this specific reader, evidence and purpose appear to determine order, emphasis, amount of explanation and stopping point.

Do not turn this into banned words, forced irregularity, typo injection, random sentence-length variation or detector optimization. Run AB/BA order reversal for important comparisons.

### W4 — exemplars only from real project edit pairs
Do not introduce few-shot prose exemplars yet. When real Belief-Changer model-draft → human-edit → final-used pairs exist, test whether narrowly extracted cadence/structure examples improve writing while holding facts fixed.

Explicitly audit vocabulary, factual assumptions, metaphors, scope and argument moves for leakage from exemplars. Reject the exemplar architecture if style gains depend on importing those contents.

## Evidence priority

Synthetic model-vs-model judgments are provisional. Real model draft → human edit → final used output from this project should outrank them when available.

These hypotheses must not override truth, safety, source traceability, reader usefulness, experiment independence, or the existing Pi/OpenCode-Go runtime boundary.
