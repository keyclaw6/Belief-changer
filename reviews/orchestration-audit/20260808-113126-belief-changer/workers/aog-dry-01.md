# Worker shard — AOG-DRY-01 (research-stage dry-run simulator)

- Reviewer: GPT-5.6 Terra medium sub-agent (nickname Galileo), read-only; no external effects invoked
- Scenarios: happy path W1; miner transport failure; thin lane cannot clear §7; Bing outage; concurrent bank writes

## Verdicts
- Happy path: COMPLETES-WITH-RISK (handoff correctly named; receiver's exact-four-input contract coherent; risk = F-02)
- Miner transport failure: COMPLETES-WITH-RISK (retry-once then INCONCLUSIVE defined; checkpoint claim works only if F-02 fixed)
- Thin lane / genuine scarcity: BLOCKED (F-01)
- Bing outage: UNDEFINED (F-03)
- Concurrent bank writes: UNDEFINED (F-02)

## Findings

### F-01 (HIGH) — "Genuine scarcity" termination can produce syntheses the plan-writer must reject as thin; no actor/transition returns work to research or escalates
Evidence: research-agent.md:41-45,189-194 (scarcity endpoint); master-plan-skill-v2.md:7-14 (plan-writer stops on thin input); PROGRAM.md:171-177 (only plan-review revision cycles defined). Scarcity is decided by the research lead, but the next mandatory consumer can reject the output; no return path defined.

### F-02 (MEDIUM) — No unique-writer/lock/append-atomicity/merge contract for up to 10 concurrent miners writing shared banks and source packets
Evidence: research-agent.md:48-52,80-85 (parallel dispatch); researcher.md:27-30 ("append, dedupe"); sources/README.md:3-5 (same packet enriched by repeated URL use). Concurrent read-dedupe-write can lose entries or corrupt packets.

### F-03 (MEDIUM) — Bing search failure has no defined retry, alternate discovery path, or escalation; sustained failure leaves W1 without a defined terminal
Evidence: web_tools.py:31-56 (sole search backend; errors returned as data); research-agent.md:80-91 (relentless discovery required); PROGRAM.md:46-54 (no-fallback law governs credentials/routes, not web discovery). Cannot honestly be called "genuine scarcity" when the tool, not the source universe, is unavailable.

## Question
- HANDOFF.md:120-122 says API failures get "3x 30/60/120s per PROGRAM" while PROGRAM.md:71-74 says a failed role is retried once — competing retry budgets, unspecified nesting. Applied explicit PROGRAM rule.

## Integrity
- No files written; no services called; current on-disk syntheses are templates, not completed handoffs (K-08..K-12 missing).
