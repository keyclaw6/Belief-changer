# Dry run — W3 Writing stage (terminal traces)

Simulator: AOG-DRY-02 (Lovelace). No external effects invoked.

## DR-W3-happy — sequential chapter writing — COMPLETES

| # | Role | Decision / tool / handoff | Output / state after | Evidence |
|---|---|---|---|---|
| 1 | Orchestrator | Rebuilds reference-alignment before judging when plan changed | alignment reflects cards | PROGRAM.md:175-177; reference-alignment.md:5-26 |
| 2 | Orchestrator → chapter-writer Ch.01 | Exactly 4 inputs: plan, Ch.01 card, style guide, plan book-core | chapter-01.md; becomes rolling prior | PROGRAM.md:179-188; chapter-writer.md:8-16 |
| 3 | Chapter-writer | Card = semantic authority; resolves IDs vs plan inventories; 4th input only for seam | complete chapter or refusal | chapter-writer.md:3-19,112-122 |
| 4 | Orchestrator → chapter-writer Ch.N | Same 4-input spawn, sequentially; prior chapter is the only writer-to-writer seam | chapters complete | PROGRAM.md:179-188; chapter-writer.md:13-16 |
| 5 | Orchestrator → judges | Chapters + CHAPTER CONTEXT + rebuilt alignment + prior chapter | judge reports; missing report after retry → INCONCLUSIVE | PROGRAM.md:216-250; reader-journey.md:8-19; book-arc.md:9-18 |

Terminal state reached: rolling window defined and usable; judge receiver contracts explicit and sufficient if alignment is current.

## DR-W3-failA — canonical writer refusal — COMPLETES-WITH-RISK (O-01)

Writer emits the one-line refusal with earliest owner (chapter-writer.md:17-27); orchestrator saves to traces/chapter-NN/refusal.md, writes no chapter, does not continue (chapter-writer.md:119-122; PROGRAM.md:209-212); terminal INCONCLUSIVE. No role validates refusal format or verifies "earliest stage" ownership; no transition consumes `repair_owner_and_regenerate_downstream` (PROGRAM.md:204-212). Terminal behavior safely stops downstream; unvalidated diagnostic attribution is the risk.

## DR-W3-failC — spawn/transport/route failure — COMPLETES

Retry once; transport failure → INCONCLUSIVE; route/credential → escalate to founder (PROGRAM.md:204-208; config.yaml:6-16).

## DR-W3-edge — skipped alignment rebuild — COMPLETES-WITH-RISK (recorded, rejected as finding)

Writers don't consume alignment, so chapters still generate; judges consume a stale table with no freshness check (book-arc.md:9-18). Rejected as a finding: rebuild is an explicit orchestrator duty and no-determinism is declared design (VERIFIED-REJECTED, C10).
