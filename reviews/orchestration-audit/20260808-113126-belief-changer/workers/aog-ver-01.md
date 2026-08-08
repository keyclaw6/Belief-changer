# Worker shard — AOG-VER-01 (skeptical finding verifier)

- Reviewer: GPT-5.6 Terra medium sub-agent (nickname Hubble), read-only, post-hoc (authored none of the candidates)
- Re-verified: all mandatory factory, loop, prompt, agent-wrapper, source-packet, spawn-extension, and audit-map sources

## Per-candidate verdicts

| Candidate | Verdict | Strongest counterargument / basis |
|---|---|---|
| C1 Reddit contradiction (HIGH) | ACCEPT | Mirrors do not literally satisfy the mandate; active rules both require and prohibit Reddit absent an authorization path. Evidence re-verified: AGENTS.md:14; AUTO-TUNING-LOOP.md:127-132; research-agent.md:35,59-62; researcher.md:24-25 |
| C2 W2 revision loop not realizable (HIGH) | ACCEPT | A blocked plan cannot legally receive its candidate + blockers on the next plan-writer call (task text and disk reads are "other context"); cycle termination also contradictory. Evidence: master-plan-skill-v2.md:7-14,150; master-plan-reviewer-v2.md:101-103; PROGRAM.md:171-177; spawn task injection in index.ts:294-330 |
| C3 Miner write target undefined (HIGH) | ACCEPT | "Ten banks" are semantic categories, not defined writable files; historic work orders show both packets and raw-bank lines, confirming rather than resolving the ambiguity. Evidence: research-agent.md:82-85,141-158; researcher.md:9-10,27-28; sources/README.md:3-5; historic K-01.md:30-35 |
| C4 Config params unenforceable (HIGH) | ACCEPT | Standard spawned-role path supplies only model/tools/system prompt/task; cannot enforce writer reasoning/temperature or plan-reviewer reasoning; only preflight reads judge parameters; `:max` suffix covers the research miner only. Evidence: config.yaml:2-3,14-16,28,43,64-65; agents.ts:58-71; index.ts:294-330; run_preflight.sh:13-23 |
| C5 Concurrent miner writes (MEDIUM) | ACCEPT | "Append, dedupe by URL" is not a concurrency guarantee; no assignment ownership, lock, or atomic merge protocol. Evidence: research-agent.md:48-52,82-85; researcher.md:27-28; HANDOFF.md:89-104 |
| C6 Scarcity→thin rejection (MEDIUM) | ACCEPT | Documented scarcity permits synthesis while thin input requires the planner to stop; no runbook transition classifies or resolves that expected handoff failure; INCONCLUSIVE is specified for role/transport failure, not this contract conflict. Evidence: research-agent.md:41-45,187-194; master-plan-skill-v2.md:7-14; PROGRAM.md:204-212 |
| C7 Bing outage undefined terminal (MEDIUM) | ACCEPT | Bing RSS is the only discovery backend; a returned search error has no defined retry/alternate/escalation; known-URL fetch does not restore discovery. Evidence: web_tools.py:31-56; research-agent.md:80-91; PROGRAM.md:71-78 |
| C8 Stale chapter-reviewer actionable (MEDIUM) | ACCEPT | Obsolete reviewer-loop instructions remain directly actionable for operators, contradicting the live writer→judges flow and citing a nonexistent runbook section; inert in the campaign runner but not inert as user-facing operating guidance. Evidence: chapter-reviewer.md:3; production-books/README.md:28-32; PROGRAM.md:179-212 |
| C9 Refusal action code (proposed HIGH) | REJECT | Action code is not shown to be a dispatch contract; runbook expressly defines refusal handling as capture→finding→INCONCLUSIVE; "repair_owner_and_regenerate_downstream" is a misleading label at most; model-selected ownership does not cause an automatic unsafe repair. Evidence: chapter-writer.md:21-27,119-122; PROGRAM.md:204-212 |
| C10 Alignment rebuild gate (MEDIUM) | REJECT | Rebuild is an explicit orchestrator duty and deterministic validation is deliberately prohibited; the candidate assumes the orchestrator skips that duty; absence of a second mechanical check is not a defect under the declared design. Evidence: PROGRAM.md:71-78,171-177; book-arc.md:9-20 |

## Limitations
- Static contract review only; no model calls, spawning, searches, or runtime execution.
- No files written.
