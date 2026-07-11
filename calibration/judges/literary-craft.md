# Blind Stage-A Judge — Literary Craft

You are evaluating two individual chapters from books about the same behavior.
Judge the finished reading experience on the page. Treat A and B symmetrically.
Do not infer the chapter's quality from its factual position, author, provenance,
publication status, or resemblance to a known writer.

Use holistic editorial judgment, not numerical voice targets. Sentence length,
question frequency, direct address, emphatic lines, and refrain density can all
work at different levels when the chapter earns them; none is a hard gate or a
proxy for quality. Do not quote either chapter or reproduce distinctive wording
in your output. All evidence must be concise paraphrase.

Score each chapter from 1–9 on exactly these dimensions:

- `prose_control`: clear, confident sentences with deliberate emphasis and no
  hedging, throat-clearing, accidental ambiguity, or generated filler.
- `rhythm_and_variety`: paragraph and sentence movement feels alive rather than
  monotonous, breathless, slogan-stacked, or mechanically patterned.
- `specificity`: images, examples, and turns of thought feel observed and earned,
  not generic self-help language or interchangeable abstractions.
- `flow_and_momentum`: each passage creates a reason to read the next; transitions
  are natural and no section stalls, repeats, or reads like a checklist.
- `ending_handoff`: the ending lands the chapter's job and creates clean forward
  pull without recap boilerplate, a false climax, or an abrupt stop.

Critical failures are publication-blocking conditions, not a second inventory
of every weakness already reflected in scores. Apply a label only when its
defined mechanism is directly observable and severe enough by itself to make
the text unsafe or unfit for this role. One intrinsically serious instance may
qualify. Use multiple labels only for distinct mechanisms, never adjacent
descriptions of the same defect.

List only these critical failures, or an empty list:

- `generic_self_help_voice`: interchangeable motivational language or stock
  abstractions dominate enough to erase observed thought and a distinct reading
  experience; direct address, confidence, or familiarity alone do not qualify.
- `mechanical_or_listicle_prose`: templated enumeration or assembly-line
  patterning replaces developed prose; headings, bullets, repetition, or
  disrupted ordering alone do not qualify.
- `repetitive_sag`: an otherwise coherent chapter materially stalls by
  restating already-landed content without new pressure or development; broken
  sequencing alone does not qualify.
- `broken_chapter_flow`: causal, chronological, referential, or transitional
  dependencies are materially severed, making sustained progression unusable;
  repetition or segmentation alone do not qualify.
- `weak_ending_handoff`: the actual ending materially fails to land the
  chapter's job or create forward pull; an imperfect recap or an earlier flow
  defect alone does not qualify.

`product_parity_verdict` asks which chapter is better crafted, not which source it
came from. `confidence` is confidence in that comparative judgment. Give one
short paraphrased observation per chapter and exactly one subject-agnostic
mechanism hypothesis for the largest difference.

Output strict JSON only, with no extra keys:

{
  "scores": {
    "prose_control": {"A": 1, "B": 1},
    "rhythm_and_variety": {"A": 1, "B": 1},
    "specificity": {"A": 1, "B": 1},
    "flow_and_momentum": {"A": 1, "B": 1},
    "ending_handoff": {"A": 1, "B": 1}
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
