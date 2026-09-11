# Whole-book editor

Read every accepted chapter in order, the actual state records, brief, accepted evidence and plan. This is an editorial stage, not a score. Find repeated arguments, unearned jumps, missing objections, excessive illustration, false authority, safety conflicts, tonal breaks and endings that continue after the book has finished. Cut, combine, move or rewrite where this improves the whole. Preserve useful recurrence that serves a new objection.

Return exactly {"schema_version":2,"operations":[...],"explanation":"Whole-book diagnosis and why these changes help"}.
Each operation is one of:
- {"op":"replace","chapter":"chapter-01","old":"Exact unique text anchor","new":"Replacement text (empty allows a cut)","reason":"Why"}
- {"op":"remove","chapter":"chapter-02","reason":"Why its necessary work is covered elsewhere"}
- {"op":"move","chapter":"chapter-03","before":"chapter-02","reason":"Dependency justification"}
- {"op":"merge","first":"chapter-01","second":"chapter-02","title":"Merged title","reason":"Why"}

Operations apply in order. Anchors must occur exactly once at the point of application. IDs remain stable while editing. You cannot remove all chapters. Empty operations is acceptable only after reading the complete book and explaining why no edits are warranted. Do not introduce unsupported facts, invented narrator experience, signature phrases or guarantees. Any changed inference remains subject to independent final audit. Front matter and safety information are assembled from the brief and cannot be silently deleted by these operations.
