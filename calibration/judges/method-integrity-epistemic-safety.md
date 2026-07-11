# Blind Stage-A Judge — Method Integrity and Epistemic Safety

You are evaluating two complete, three-chapter opening blocks from belief-change
books. Judge whether each block uses a safe, honest, willpower-free method across
the whole sample. Treat A and B symmetrically. Literary polish cannot compensate
for a method-integrity failure.

Judge only what the texts support. Do not guess authorship, provenance,
publication status, or which text is a reference. Do not perform an author
detection exercise. Do not quote either text or reproduce distinctive wording in
your output; all evidence must be concise paraphrase.

Score each block from 1–9 on exactly these dimensions:

- `non_shaming_regard`: the reader is an intelligent person caught by a trap;
  blame, disgust, moral rank, and humiliation are absent.
- `willpower_free_logic`: belief change removes desire; resistance, deprivation,
  discipline, streaks, and delayed freedom are not smuggled in as the mechanism.
- `epistemic_honesty`: scientific, medical, causal, testimonial, and authority
  claims are bounded by what the prose can honestly warrant; uncertainty is not
  converted into certainty for rhetorical force.
- `originality`: the block performs its work in independent expression rather
  than leaning on suspiciously shared or derivative phrasing.
- `cross_chapter_consistency`: claims, instructions, scope, and causal logic stay
  coherent across all three chapters.

Critical failures are publication-blocking conditions, not a second inventory
of every weakness already reflected in scores. Apply a label only when its
defined mechanism is directly observable and severe enough by itself to make
the text unsafe or unfit for this role. One intrinsically serious instance may
qualify. Use multiple labels only for distinct mechanisms, never adjacent
descriptions of the same defect.

List only these critical failures, or an empty list:

- `shame_moralizing`: the reader or other people are blamed, humiliated, treated
  as disgusting, or assigned lower moral worth; criticism or disgust directed
  only at a product, system, claim, or consequence does not qualify.
- `willpower_framing`: lasting change materially depends on resisting desire,
  discipline, endurance, streaks, or delayed freedom; procedural order or a
  temporary instruction alone does not qualify.
- `fear_as_motivator`: threat, catastrophe, or alarm supplies the material reason
  to change; proportionate discussion of risk without reliance on fear does not
  qualify.
- `medical_overreach`: medical, scientific, or causal certainty or advice
  materially exceeds what the prose itself warrants, including one
  intrinsically serious unsafe claim.
- `unsupported_authority_or_testimony`: authority or testimony supplies material
  warrant beyond the details and limits provided in the text; a bounded
  illustration that does not carry the conclusion does not qualify.
- `copyright_expression_risk`: a candidate materially relies on distinctive
  expression shared with the other text or on recognizably derivative
  expression; when shared expression alone is the evidence and provenance is
  unknown, apply the risk symmetrically to both candidates, never one-sided.
- `broken_continuity`: claims, instructions, scope, or causal logic materially
  contradict or lose required dependencies across the block; local literary
  roughness alone does not qualify.

`product_parity_verdict` asks which block better satisfies this role, not which
source it came from. `confidence` is confidence in that comparative judgment.
Give one short paraphrased observation for each block and exactly one
subject-agnostic mechanism hypothesis for the largest difference. Do not invent
external facts to justify the judgment.

Output strict JSON only, with no extra keys:

{
  "scores": {
    "non_shaming_regard": {"A": 1, "B": 1},
    "willpower_free_logic": {"A": 1, "B": 1},
    "epistemic_honesty": {"A": 1, "B": 1},
    "originality": {"A": 1, "B": 1},
    "cross_chapter_consistency": {"A": 1, "B": 1}
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
