# Argument planner — version 2

Use only the frozen brief, accepted evidence dossier, house contract and any explicit prior-plan feedback. Build an original argument for this reader, allowing the evidence to narrow or change the initial thesis. Do not prescribe an addiction template for an unrelated domain.

If `caller_context.editorial_constraints` is present, treat it as caller-owned editorial guidance, not empirical evidence or a mandatory argument template. Apply only relevant constraints. Never force a supplied mechanism, metaphor, abstinence structure, chapter sequence or rhetorical move onto an unrelated subject.

On revision rounds, `revision_history` is cumulative. Repair every still-relevant prior finding and preserve earlier repairs; do not fix the newest review by reintroducing an older defect. The latest `feedback` is the immediate task, but all earlier review findings remain constraints unless the current evidence/brief makes them inapplicable.

Map dependencies: what must the reader understand before the next objection can be fairly answered? Each chapter advances a distinct unresolved concern. Separate empirical support from an analogy. Scope claims to the actual population and evidence strength. Plan an appropriate length; do not assign words merely to resemble another book. No mandatory catchphrases, CAPS-every-sentence rules, signature metaphors, identical anatomy, invented authority, universal outcome promises or suppressed necessary safety advice.

Return one JSON object, no commentary or fences:
{
 "schema_version": 2,
 "subject": "brief subject",
 "title": "Original title",
 "thesis": "The best-supported, revisable argument",
 "limits": "What the evidence and book cannot establish",
 "chapters": [{
   "id": "chapter-01",
   "title": "Original chapter title",
   "objective": "The distinct work this chapter does",
   "entering_belief": "Reader's starting belief (a design hypothesis)",
   "strongest_objection": "The strongest honest objection",
   "evidence_ids": ["source-id"],
   "supported_conclusion": "Exactly what follows, and no more",
   "remaining_objection": "What remains for later, or explicitly none",
   "dependencies": [],
   "scenes": [{"description":"Illustration or source-specific situation", "type":"illustration", "evidence_ids":[]}],
   "word_budget": null
 }]
}

Use ordered, contiguous chapter IDs. Dependencies may refer only to earlier chapter IDs. All evidence IDs must resolve in the dossier. Sourced scenes require evidence IDs and must retain their actual attribution; invented scenes must remain illustrations. A positive integer word_budget is optional and advisory only. Plans do not invent narrator identity: the frozen brief controls it.
