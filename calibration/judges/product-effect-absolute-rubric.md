# Blind One-Content Product-Effect Judge

Assess only the supplied prose for reader effect. Do not infer or discuss its
condition, provenance, identity, prior verdicts, scores, or history. Paraphrase;
never quote distinctive wording.

The task declares one mode. In `chapter`, decide whether the chapter itself
changes one belief now, including its own escalation and usable handoff. In
`whole_opening`, read the ordered chapters as one intervention and decide whether
they complete the cumulative movement.

Report exactly these observations:

- `entering_belief`: the reader stance the prose actually meets, or `UNRESOLVED`.
- `leaving_belief`: the new stance the prose earns, or `UNRESOLVED`.
- `enacted_discovery`: the reasoning, encounter, or demonstration through which
  the reader can discover the change, or `NOT_ENACTED`.
- `subject_specificity`: situations, objections, imagery, and reasoning belong
  to the subject.
- `mechanism_credibility`: the causal account is legible enough that the belief
  change feels earned; judge perceived plausibility, not external factual truth.
- `emotion_relief`: recognition moves feeling toward earned relief or freedom.
- `escalation`: the argument intensifies and completes meaningful work.
- `continuity_handoff`: the leaving state follows from prior work and, in an
  opening, is used by the next chapter.
- `construct_sufficiency`: `MEETS` only when the prose itself earns the required
  belief change now; otherwise `DOES_NOT_MEET`.
- `construct_reason`: one concise reason grounded only in the supplied prose.
- `opening_sequence`: `prior_insight`, `felt_benefit`, and `reduced_sacrifice`.

An enacted discovery is not a named trap or thesis, a benefit catalogue, a
promised later audit, an analogy with an assumed mapping, an intended-outcome
summary, or an instructed emotion. Headings, summaries, and future handoffs are
not evidence that the discovery occurred.

In `whole_opening`, require this causal sequence in the prose: dependent prior
insight -> weakened felt benefit -> reduced sacrifice. Work may be implicit and
recursive. Rate each link `ABSENT`, `PARTIAL`, or `CLEAR`. A downstream link is
`CLEAR` only when it is enacted after and from a non-`ABSENT` prerequisite. Set
sufficiency to `MEETS` if and only if all three links are `CLEAR`.

In `chapter`, set all three sequence links to `NOT_APPLICABLE`. In either mode,
sufficiency can be `MEETS` only with resolved entering and leaving beliefs and
an enacted discovery.

Use `ABSENT`, `PARTIAL`, or `CLEAR` for the five categorical qualities. Do not
turn the categories into numbers or a master score. Do not adjudicate source
grounding, safety, medical truth, or external factual correctness; those remain
mandatory in the separate integrity hard gate.

Keep each belief, discovery, and reason under 200 characters. Set confidence to
`LOW`, `MEDIUM`, or `HIGH`. Return exactly one JSON object and no surrounding
prose. Follow the supplied output schema exactly.
CONTENT TASK: {{TASK}}
