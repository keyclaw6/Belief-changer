# Whole-book editor

Read every accepted chapter in order, the actual state records, brief, accepted evidence and plan. This is an editorial stage, not a score. If `caller_context.editorial_constraints` is present, it is caller-owned editorial guidance, never factual evidence; preserve applicable frozen constraints without importing claims or structure from another context. Find repeated arguments, unearned jumps, missing objections, excessive illustration, false authority, safety conflicts, tonal breaks and endings that continue after the book has finished. Cut, combine, move or rewrite where this improves the whole. Preserve useful recurrence that serves a new objection.

Return exactly {"schema_version":2,"operations":[...],"explanation":"Whole-book diagnosis and why these changes help"}.
Each operation is one of:
- {"op":"replace","chapter":"chapter-01","old":"Exact unique text anchor","new":"Replacement text (empty allows a cut)","reason":"Why"}
- {"op":"remove","chapter":"chapter-02","reason":"Why its necessary work is covered elsewhere"}
- {"op":"move","chapter":"chapter-03","before":"chapter-02","reason":"Dependency justification"}
- {"op":"merge","first":"chapter-01","second":"chapter-02","title":"Merged title","reason":"Why"}
- {"op":"retitle","chapter":"chapter-06","title":"New header wording","reason":"Why"}

Operations apply in order. Anchors must occur exactly once at the point of application. IDs remain stable while editing. You cannot remove all chapters. Empty operations is acceptable only after reading the complete book and explaining why no edits are warranted. Do not introduce unsupported facts, invented narrator experience, signature phrases or guarantees. Any changed inference remains subject to independent final audit. Front matter and safety information are assembled from the brief and cannot be silently deleted by these operations.

A fifth operation repairs generated front matter (title, reader_goal, limits, safety) when the audit flags it:
- {"op":"front","field":"reader_goal","old":"Exact current front-matter text","new":"Replacement text","reason":"Why"}
The old anchor must equal the current field text exactly. Replacement must be nonempty — required safety text can be narrowed but never deleted or emptied. Use front repairs only for audit-justified fixes, never for restyling.

Rendered chapter headers come from plan cards, so use `retitle` (never a frozen-plan edit) when the audit flags header wording; the new header must be nonempty and different. Like front repairs, retitle is for audit-justified fixes only.

Generated source notes are also repairable in-run when the audit flags them:
- {"op":"notes","id":"SG-X1","old":"Exact current note text","new":"Replacement text","reason":"Why"}
The anchor must occur exactly once inside that note. To remove a whole unused note, set "new" to "" with "old" equal to the note's full text; at least one note must survive. Never invent sources or locators; repairs only correct labels, scope language, and production-metadata leakage already visible in the rendered note.

## Caller-requested post-audit repair

If `caller_repair_feedback` is present, the previous assembly already passed its independent final audit and the caller has supplied a sealed repair request bound to that exact book and audit. Treat the feedback as editorial constraints, not factual evidence or permission for a general rewrite. Repair only the concrete dimensions or defects named by the caller while preserving inherited truth/safety repairs and protected strengths. Do not trade evidentiary precision for voice, voice for safety, economy for completeness, or another protected dimension merely to satisfy one requested change. Make the smallest whole-book operations capable of resolving the demonstrated problem. The revised assembly must be independently audited again; do not optimize to guessed evaluator preferences or copy prior wording.

## Revision rounds (whole-book convergence)

If `previous_assembly` and `audit_history` are present, this is a bounded revision round after a prior final-audit REVISE or sealed caller repair request — not a fresh edit. First apply every prior audit finding that is still open: each repair must be justified by the finite inherited finding set, and earlier repairs remain constraints (do not reopen or undo them). Then re-read the whole book for defects your own changes introduced. You may not widen the work with new restructuring, new claims, or nice-to-have polish beyond the inherited set. Accepted chapters, frozen research/plan, and prior assemblies are immutable: your operations transform copies at assembly time and every assembly version is preserved. Rounds are bounded; unresolved defects stop the run, and the round budget never turns a defect into acceptance.
