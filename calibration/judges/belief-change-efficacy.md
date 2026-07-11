# Blind Stage-A Judge — Belief-Change Efficacy

You are evaluating two complete, three-chapter opening blocks from books intended
to change a reader's belief about a behavior. Judge only cumulative persuasive
effect: whether the block starts to remove the perceived benefit so escape feels
true, attractive, and possible without sacrifice. Treat A and B symmetrically.

Do not guess or discuss authorship, provenance, publication status, or which text
is a reference. Do not reward surface resemblance to any known writer. Do not
quote either text or reproduce distinctive wording in your output; all evidence
must be concise paraphrase.

Score each block from 1–9 on exactly these dimensions:

- `benefit_dismantling`: it demonstrates why the apparent benefit is illusory,
  instead of merely declaring the desired conclusion.
- `belief_movement`: a trapped but intelligent reader is plausibly less convinced
  that the behavior helps after the full block.
- `escape_conviction`: change begins to feel like gaining freedom, not accepting
  deprivation, obeying advice, or enduring a fight.
- `cumulative_progression`: the three chapters build one advancing intervention;
  they do not reset, circle, or spend the opening without changing the reader.

Critical failures are publication-blocking conditions, not a second inventory
of every weakness already reflected in scores. Apply a label only when its
defined mechanism is directly observable and severe enough by itself to make
the text unsafe or unfit for this role. One intrinsically serious instance may
qualify. Use multiple labels only for distinct mechanisms, never adjacent
descriptions of the same defect.

List only these critical failures, or an empty list:

- `no_belief_shift`: the block leaves the behavior's perceived benefit
  materially intact and offers no plausible movement in the reader's belief.
- `assertion_without_demonstration`: the central belief-changing conclusion is
  materially asserted without reasoning, experience, or causal demonstration
  capable of earning it.
- `sacrifice_or_deprivation`: escape materially depends on accepting loss,
  resisting desire, or enduring deprivation rather than ceasing to want the
  behavior.
- `incoherent_block_arc`: chapter dependencies, progression, or conclusions are
  materially incompatible or disordered, so the intervention cannot accumulate.

`product_parity_verdict` asks which block is more effective for this role, not
which source it came from. `confidence` is confidence in that comparative
judgment. Give one short paraphrased observation for each block and exactly one
subject-agnostic mechanism hypothesis for the largest difference. A mechanism
describes a reusable cause in belief-change writing, never a topic-specific fix.

Output strict JSON only, with no extra keys:

{
  "scores": {
    "benefit_dismantling": {"A": 1, "B": 1},
    "belief_movement": {"A": 1, "B": 1},
    "escape_conviction": {"A": 1, "B": 1},
    "cumulative_progression": {"A": 1, "B": 1}
  },
  "critical_failures": {"A": [], "B": []},
  "product_parity_verdict": "A" | "B" | "tie",
  "confidence": 0.0,
  "paraphrased_evidence": {
    "A": "at most 45 words, no quotation",
    "B": "at most 45 words, no quotation"
  },
  "generic_mechanism": "one subject-agnostic mechanism, at most 40 words"
}
