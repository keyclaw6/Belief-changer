# Worker shard — AOG-AMB-01 (independent ambiguity interpreter)

- Reviewer: GPT-5.6 Terra medium sub-agent (nickname Noether), read-only, isolated

## E1 — Miner packet write target
Primary: orchestrator must supply the exact bank path per work order; no default ten-bank filename mapping in the role contract. Fixed packet format/location = one Markdown file per accepted URL under production-books/<slug>/research/sources/ (sources/README.md schema); ten-bank content later synthesized into lived-experience.md + scientific-evidence.md. Alternatives: (a) task-local per-bank file with packets appended (sources/ only a ledger) — changes location/persistence; (b) assigned file IS the per-URL source packet; Bank-slot fields route it into multiple semantic banks — changes write target/layout. No higher-priority source supplies the missing bank-to-path mapping.

## E2 — Reddit authorization
Primary: direct Reddit prohibited without external authorization; reachable mirrors/archives remain permissible substitutes; completion criterion (§7) requires populated slots across ≥3 personas, not direct reddit.com access, so a run can complete without direct Reddit. Alternative: "must go into Reddit" adds a direct-Reddit requirement; without authorization the run cannot complete and stays blocked — changes termination and routing/authority. No process or actor that grants the authorization is defined anywhere read.

## E3 — Plan-review cycle limit
Primary: continue cycling after a third BLOCK; acceptance regardless excluded by reviewer contract; PROGRAM "until" resolves cycle behavior in favor of continued review. Alternative: "up to three cycles" is a hard cap; after the third BLOCK stop and escalate — changes termination and escalation.

## E4 — Writer refusal action code
Primary: `repair_owner_and_regenerate_downstream` identifies the repair owner and dependency direction; operative orchestrator rule is to record it as the iteration finding and end INCONCLUSIVE — no same-iteration repair dispatch. Alternative: the action code is executable routing (dispatch owner, repair, regenerate within the same iteration) — changes state, routing, output, termination. PROGRAM.md provides the higher failure-handling rule (INCONCLUSIVE) and does not prescribe same-iteration repair.

## Integrity
- No files written; no services called; did not inspect other interpreters' outputs.
