# ADJUDICATION LEDGER

Row classes: VERIFIED-ACCEPTED / VERIFIED-DOWNGRADED / VERIFIED-CONVERTED-QUESTION / VERIFIED-REJECTED.

| Candidate ID | Source shard(s) | Proposed severity | Verifier verdict | Row class | Final disposition | Rationale |
|---|---|---|---|---|---|---|
| C1 Reddit contradiction (CONF-001, BLOAT-001) | aog-conf-01, aog-bloat-01, aog-amb-01..03 (E2) | HIGH | ACCEPT | VERIFIED-ACCEPTED | F-01 HIGH | Mirrors don't literally satisfy the mandate; no authorization path defined |
| C2 W2 revision loop not realizable (DRY-02 #1+#2) | aog-dry-02, aog-amb-01..03 (E3) | HIGH | ACCEPT | VERIFIED-ACCEPTED | F-02 HIGH | No compliant revision handback; 4th-cycle behavior undefined |
| C3 Miner write target undefined (RES-001) | aog-res-01, aog-amb-01..03 (E1) | HIGH | ACCEPT | VERIFIED-ACCEPTED | F-03 HIGH | Semantic banks, no writable files/schema; interpreters diverge on target |
| C4 Config params unenforceable (CHAP-001, XSYS-001, BLOAT-003, CONF-002 xhigh) | aog-chap-01, aog-xs-01, aog-bloat-01, aog-conf-01; PLAN-01 dissents on xhigh | HIGH | ACCEPT | VERIFIED-ACCEPTED | F-04 HIGH | Spawn path passes model/tools only; reasoning/temperature unenforceable; xhigh-vs-max is one symptom |
| C5 Concurrent miner writes (DRY-01 F-02) | aog-dry-01 | MEDIUM | ACCEPT | VERIFIED-ACCEPTED | F-05 MEDIUM | No exclusivity/merge protocol; append+dedupe not atomic |
| C6 Scarcity→thin rejection (DRY-01 F-01) | aog-dry-01 | MEDIUM | ACCEPT | VERIFIED-ACCEPTED | F-06 MEDIUM | No return-to-research or escalation transition |
| C7 Bing outage (DRY-01 F-03) | aog-dry-01 | MEDIUM | ACCEPT | VERIFIED-ACCEPTED | F-07 MEDIUM | Sole backend; no retry/alternate/escalation |
| C8 Stale chapter-reviewer (BLOAT-002) | aog-bloat-01; aog-conf-01 dissents (historical-only) | MEDIUM | ACCEPT | VERIFIED-ACCEPTED | F-08 MEDIUM | production-books/README.md:32 is actionable operator guidance |
| C9 Refusal action code (XSYS-002, DRY-02 #3) | aog-xs-01, aog-dry-02, aog-amb-01..03 (E4) | HIGH (XSYS) / MEDIUM (DRY-02) | REJECT | VERIFIED-REJECTED | O-01 observation | Runbook defines capture→finding→INCONCLUSIVE; action code is a label, not a dispatch contract; unvalidated owner is agentic trust |
| C10 Alignment rebuild gate (DRY-02 #4) | aog-dry-02 | MEDIUM | REJECT | VERIFIED-REJECTED | REJECTED | Rebuild is explicit orchestrator duty; no-determinism is declared design; no second mechanical check is not a defect |
| C11 Preflight outer provider hardcode (closer) | aog-close-01 | (new) | n/a (lead adjudicated) | VERIFIED-CONVERTED-QUESTION | O-04 observation + Q-03 | Outer pi session uses commandcode; spawned judge route is governed by agent pin openai-sub — verify at run time whether wrapper model availability matters |
