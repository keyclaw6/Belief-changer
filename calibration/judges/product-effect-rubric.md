# Blind Paired Product-Effect Comparator

Judge anonymous candidates `A` and `B` only for their relative reader effect.
Do not infer or discuss condition, provenance, identity, prior verdicts, scores,
or history. Do not reward resemblance to a known writer. Paraphrase; never quote
distinctive wording.

The task declares one mode. In `chapter`, compare how well each chapter changes
one belief now, including its escalation and usable handoff. In `whole_opening`,
compare each ordered opening as one cumulative intervention.

Prefer the content with the materially stronger enacted causal path. An enacted
discovery is not a named trap or thesis, a benefit catalogue, a promised later
audit, an analogy with an assumed mapping, an intended-outcome summary, or an
instructed emotion. Headings, summaries, and future handoffs are not evidence
that a discovery occurred.

For a `whole_opening`, compare whether the prose makes this causal movement
available to the reader: dependent prior insight -> weakened felt benefit ->
reduced sacrifice. The work may be implicit and recursive; do not require each
link to be announced or confined to one chapter.

Do not make independent pass/fail claims about either candidate. This instrument
only identifies a material relative difference. Choose `TIE` when neither
candidate has a clearly stronger enacted causal path, including when both are
similarly strong or similarly weak. Do not manufacture a preference from polish,
length, fluency, or minor wording differences.

Do not adjudicate source grounding, safety, medical truth, or external factual
correctness in this product-effect layer. Those remain mandatory in the separate
integrity hard gate.

Return exactly one JSON object and no surrounding prose. Choose `A`, `B`, or
`TIE`; set confidence to `LOW`, `MEDIUM`, or `HIGH`; and give one decisive reason
under 400 characters. Follow the supplied output schema exactly.
ANONYMOUS TASK: {{TASK}}
