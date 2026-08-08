# WORKFLOW LEDGER

| Workflow | Governing source | Initial trigger | Terminal state | Scenarios | Verdicts | Finding IDs | Coverage |
|---|---|---|---|---|---|---|---|
| W1 Research | PROGRAM §3 Stage: Research + research-agent.md | baseline/iteration research start | syntheses written; handoff to plan-writer | happy; miner transport failure; thin lane/scarcity; Bing outage; concurrent writes | COMPLETES-WITH-RISK; COMPLETES-WITH-RISK; BLOCKED; UNDEFINED; UNDEFINED | F-03, F-05, F-06, F-07 | COMPLETE (dry-runs/w1-research.md) |
| W2 Planning | PROGRAM §3 Stage: Planning + master-plan skills | accepted research syntheses | `master-plan-review.md` ends `fit to write from` | happy; revision handback; persistent BLOCK at cycle 4; spawn failure | BLOCKED; BLOCKED; UNDEFINED; COMPLETES | F-02 | COMPLETE (dry-runs/w2-planning.md) |
| W3 Writing | PROGRAM §3 Stage: Writing | accepted plan | all chapters written | happy sequential; writer refusal; spawn failure; skipped alignment rebuild | COMPLETES; COMPLETES-WITH-RISK; COMPLETES; COMPLETES-WITH-RISK | O-01; Q-01 | COMPLETE (dry-runs/w3-writing.md) |
| W4 Judge/trace/hypothesize | PROGRAM §3 Steps 4-6 | chapters complete | trace-analysis + hypothesis | not simulated (consumer scope) | — | — | OUT-OF-SCOPE (declared limitation) |
