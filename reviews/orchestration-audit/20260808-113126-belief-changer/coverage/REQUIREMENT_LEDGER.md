# REQUIREMENT LEDGER

Dispositions: IMPLEMENTED / PARTIAL / GAP / CONFLICT / NOT-APPLICABLE / QUESTION.

| ID | Strength | Requirement | Implementation mapping | Test / dry run | Disposition |
|---|---|---|---|---|---|
| R-001 | MUST | Research depth unlimited; no search/fetch ceilings | research-agent.md Standing law + web_tools.py per-call bounds only | DRY-W1-happy (step 2) | IMPLEMENTED |
| R-002 | MUST | Lived experience primary; forums/Reddit/support communities | research-agent.md priority + rights gate | DRY-W1-happy | CONFLICT → F-01 (Reddit require vs prohibit) |
| R-003 | MUST | Provenance (6 elements); exact quotes; no fabrication | research-agent.md §6 + sources/README.md schema | DRY-W1-happy | IMPLEMENTED (integration risk F-03) |
| R-004 | MUST | Completion criterion ≥3 personas before synthesis | research-agent.md §7 | DRY-W1-happy/failure-B | PARTIAL → F-06 (scarcity→thin conflict) |
| R-005 | MUST | Plan-writer exact 4 inputs; no contamination | master-plan-skill-v2.md:5-14 + wrapper | DRY-W2-happy | IMPLEMENTED (revision handback broken → F-02) |
| R-006 | MUST | Reviewer gate ends `fit to write from` | master-plan-reviewer-v2.md + PROGRAM §3 | DRY-W2 | PARTIAL → F-02 (revision loop not realizable; 4th-cycle undefined) |
| R-007 | MUST | Chapter-writer exact 4 inputs; card authority; refusal line | chapter-writer.md + PROGRAM §3 | DRY-W3 | IMPLEMENTED (refusal label drift → O-01) |
| R-008 | MUST | Zero deterministic validation | no deterministic validators found in pipeline | DRY-W3 | IMPLEMENTED |
| R-009 | MUST | Roles are fresh spawned pi sub-agents, clean context | PROGRAM §1 + extension spawn | DRY-W1/W2/W3 | IMPLEMENTED |
| R-010 | MUST | Routing per config (CC vs openai-sub split) | config.yaml + .pi pins match; spawn path passes model only | DRY-W1/W2/W3 | PARTIAL → F-04 (reasoning/temperature unenforceable) |
| R-011 | MUST | No fallback route; failure escalates to founder | no fallback coded; escalation mechanism undefined | DRY-W3 failure-C | IMPLEMENTED (mechanism gap → Q-01) |
| R-012 | MUST | One commit per iteration on campaign branch | PROGRAM §1 | n/a (audit, pre-baseline) | IMPLEMENTED |
| R-013 | MUST | Refusal → trace, no chapter, INCONCLUSIVE | PROGRAM §3 error handling | DRY-W3 refusal | IMPLEMENTED |
| R-014 | MUST | Preflight judge battery passes before verdicts | run_preflight.sh | n/a (battery pending) | PARTIAL → O-04 (outer provider hardcode) |
| R-015 | SHOULD | Style-guide binding craft (mantras, registers, anatomy) | style-guide.md + chapter-writer.md | DRY-W3 | IMPLEMENTED |
| R-016 | MUST | Sub-agent failure: retry once, then INCONCLUSIVE/escalate | PROGRAM §3 error handling | DRY-W1 failure-A, DRY-W3 failure-C | IMPLEMENTED (wording conflict → Q-02) |

Coverage note: R-002 conflict and R-004/R-006/R-010 partials are the finding-bearing rows; the rest are healthy.
