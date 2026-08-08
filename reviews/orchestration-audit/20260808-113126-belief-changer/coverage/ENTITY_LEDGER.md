# ENTITY LEDGER (grouped rows with exact anchors; full rows for authority-bearing candidates)

Every behavior-bearing line in the in-scope surface belongs to exactly one row below (grouped granularity). Reviewer counts are recorded in the work register; candidates reference the exact lines.

| Artifact | Entity rows (anchor) | Type | Disposition | Finding/Question | Reviewer |
|---|---|---|---|---|---|
| prompts/research-agent.md | §Goal-§8 (lines 1-218); 52 entities | doctrine | PASS except lines 82-90 (miner write target), 35/59-62 (Reddit), 41-45,189-194 (scarcity) | F-01, F-03, F-06 | AOG-RES-01 |
| .pi/agents/researcher.md | lines 1-30; 11 entities | role wrapper | PASS except lines 9-10,24-28 (bank target, Reddit) | F-01, F-03 | AOG-RES-01 |
| scripts/loop-runner/web_tools.py | lines 1-84; 9 entities | tool contract | PASS except lines 31-56 (sole backend, no retry) | F-07 | AOG-RES-01 |
| production-books/quit-sugar/research/sources/README.md | lines 1-59; 11 entities | packet contract | PASS (schema) | contributes F-03 | AOG-RES-01 |
| loop/config.yaml research fields | lines 18-34 | config | PASS (coherent) | — | AOG-RES-01 |
| production-books/quit-sugar/research/_rounds/round-1/ | sampled lead + commissions + responses | historical | OUT-OF-SCOPE (history/seed) | — | AOG-RES-01 |
| prompts/master-plan-skill-v2.md | lines 3-154; 14 grouped entities | plan-writer contract | PASS except lines 7-14,143-150 (revision handback, xhigh, 3-cycle cap) | F-02, F-04 | AOG-PLAN-01 |
| prompts/master-plan-reviewer-v2.md | lines 3-109; 10 grouped entities | plan-reviewer contract | PASS except lines 98-109 (no-waive vs cycle cap) | F-02 | AOG-PLAN-01 |
| .pi/agents/plan-writer.md + plan-reviewer.md | full | wrappers | PASS (pins match config; reasoning suffix absent → F-04) | F-04 | AOG-PLAN-01 |
| production-books/_template/master-plan.md + master-plan-review.md | full | templates | PASS (template lags card schema → O-02; Sol comment → O-03) | O-02, O-03 | AOG-PLAN-01 |
| prompts/chapter-writer.md | lines 1-122; 20 entities | writer contract | PASS except lines 21-27 (action-code label) | O-01 | AOG-CHAP-01 |
| .pi/agents/chapter-writer.md | full | wrapper | PASS except model-only pin | F-04 | AOG-CHAP-01 |
| prompts/style-guide.md | lines 1-642, writer-facing binding parts (§Fidelity, Part A, §B1-B10) | craft contract | PASS; lines 570,576 "reviewer/chapter reviewer" historical prose | O-05 | AOG-CHAP-01 |
| loop/PROGRAM.md §1, §3 | lines 37-78,171-212 | runbook | PASS except lines 171-177 (revision handback), 204-212 (refusal→INCONCLUSIVE only) | F-02, O-01 | AOG-CHAP-01, AOG-DRY-02 |
| prompts/chapter-reviewer.md | lines 1-42 | dead prompt | OUT-OF-SCOPE-as-live; actionable residue | F-08 | AOG-BLOAT-01 |
| prompts/book-analysis-agent.md | full | separate workflow | OUT-OF-SCOPE (VISION-cited analysis phase) | — | AOG-BLOAT-01 |
| production-books/README.md | line 32 | operator workflow | FINDING (stale reviewer loop instruction) | F-08 | AOG-BLOAT-01 |
| loop/reference-alignment.md | lines 1-31 | alignment table | PASS (correctly blank pre-baseline) | — | AOG-BLOAT-01 |
| scripts/loop-runner/daemon.sh + queue_runner.sh | full | optional VPS machinery | OUT-OF-SCOPE (optional, documented) | — | AOG-BLOAT-01 |
| ~/.pi/agent/extensions/subagent/{index,agents}.ts | spawn path | runtime | FINDING basis (model/tools only) | F-04 | AOG-XSYS-01 |
| loop/judges/*, loop/prompts/* | consumer contracts | consumer-only | OUT-OF-SCOPE (consumers; referenced) | — | AOG-XSYS-01 |

Limitations: full-row granularity applied to authority-bearing entities; grouped rows elsewhere. `scripts/check.sh` + `validate_repo.py` are repo-health gates, not pipeline behavior — verified working (exit 0), OUT-OF-SCOPE for behavior review.
