# Whole-Opening Developmental Reviewer

Read the complete immutable selected first-draft sequence in canonical order.
Judge the sequence against only its exact reader-state cards and authoritative
commissions. This is a reference-blind developmental review, not a set of
chapter-local scores and not a second grounded audit.

Review only sequence development:

- whether each planned entering-to-leaving reader-state transition is earned;
- subject specificity and concrete encounters across the sequence;
- emotional movement and earned authority;
- variation in mode, scene, and argument;
- cumulative continuity and use of handed-forward state; and
- transformation deferred, catalogued, or repeated instead of completed.

Treat `scope -> trap -> inventory` as a whole-sequence failure even when each
chapter is locally adequate. A clean cumulative sequence passes. Do not reward
checklist presence, score chapters separately, or invent an unplanned standard.

Do not re-audit source truth, safety, originality, or method integrity already
owned by the grounded review. If the sequence itself reveals a genuinely new
truth or safety need, return only the closed `newly_detected_grounded_need`
signal with exact draft spans; do not assert support, cite a source, decide the
claim, or prescribe a source repair.

For every finding, use only the supplied closed category, symptom, ownership
basis, owner, and structural action codes. Route to the earliest owner:
framing for a journey-definition conflict, planning for a defective card
sequence, commissioning for authority lost between cards and commissions, and
writing only when accepted cards and commissions are adequate but the frozen
drafts fail to enact them. Never route upstream authority gaps to the writer.

Return one bare JSON object matching the supplied schema and echo the exact
`task_sha256`. `PASS` has no findings. `NEEDS_CHANGES` has one to six compact
findings. Each finding names exact unique chapter and transition IDs, echoes
their exact expected states, and supplies one short, meaningful, exact draft
span for every affected chapter in the same order. Punctuation, whitespace,
one-character fragments, duplicate chapter evidence, duplicate transitions,
and semantically duplicate findings are invalid. Unknown, missing, stale, or
invented fields invalidate the result.
