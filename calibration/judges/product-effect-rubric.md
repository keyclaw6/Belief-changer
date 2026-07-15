# Blind Product-Effect Judge

Judge two anonymous candidates, `A` and `B`, only for reader effect; no separate
reference block belongs in the task. Do not infer or discuss condition, provenance,
reference identity, prior verdicts, scores, or history. Do not reward resemblance
to a known writer. Paraphrase; never quote distinctive wording.

The task declares one mode. In `chapter`, decide which chapter more clearly
changes one belief now, including its own escalation and usable handoff. In
`whole_opening`, read each ordered opening as one intervention and choose the
stronger cumulative movement, not merely the stronger isolated chapters.

For each candidate report exactly these observations:

- `entering_belief`: the reader stance the prose actually meets, or
  `UNRESOLVED` if it cannot be inferred.
- `leaving_belief`: the new stance the prose earns, or `UNRESOLVED`.
- `enacted_discovery`: the reasoning, encounter, or demonstration by which the
  reader can discover the change, or `NOT_ENACTED` when it is only asserted.
- `subject_specificity`: situations, objections, imagery, and reasoning belong
  to the subject.
- `mechanism_credibility`: the presented prose makes its causal account legible
  enough that the belief change feels earned; assess reader-perceived
  plausibility and persuasion, not external factual correctness.
- `emotion_relief`: recognition moves feeling toward earned relief or freedom.
- `escalation`: the argument intensifies and completes meaningful work.
- `continuity_handoff`: the leaving state follows from prior work and, in an
  opening, is used by the next chapter.

Do not adjudicate source grounding, safety, medical truth, or external factual
correctness in this product-effect layer. Those remain mandatory in the separate
integrity hard gate.

Use `ABSENT`, `PARTIAL`, or `CLEAR` for the final five fields. `ABSENT` means the
quality is missing or contradicted; `PARTIAL` means visible but incompletely
earned; `CLEAR` means specific and convincingly enacted. Do not turn these
categories into numbers or a master score.

Choose `A`, `B`, or `TIE` by reader-perceived causal legibility and earned
persuasion from the presented prose. In chapter mode choose on direct
belief-changing effect; in whole-opening mode choose on cumulative sequence.
Keep every belief or discovery paraphrase under 200 characters and the decisive
reason under 400 characters. Return exactly one JSON object and no surrounding
prose:

```json
{
  "schema": 1,
  "task_sha256": "copy from task",
  "mode": "chapter",
  "observations": {
    "A": {
      "entering_belief": "concise paraphrase",
      "leaving_belief": "concise paraphrase",
      "enacted_discovery": "concise paraphrase",
      "subject_specificity": "CLEAR",
      "mechanism_credibility": "CLEAR",
      "emotion_relief": "PARTIAL",
      "escalation": "CLEAR",
      "continuity_handoff": "PARTIAL"
    },
    "B": {
      "entering_belief": "concise paraphrase",
      "leaving_belief": "concise paraphrase",
      "enacted_discovery": "concise paraphrase",
      "subject_specificity": "PARTIAL",
      "mechanism_credibility": "PARTIAL",
      "emotion_relief": "ABSENT",
      "escalation": "PARTIAL",
      "continuity_handoff": "ABSENT"
    }
  },
  "preferred": "A",
  "confidence": "MEDIUM",
  "decisive_reason": "one concise product-effect reason"
}
```
ANONYMOUS TASK: {{TASK}}
