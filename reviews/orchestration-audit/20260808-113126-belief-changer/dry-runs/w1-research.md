# Dry run — W1 Research stage (terminal traces)

Simulator: AOG-DRY-01 (Galileo). No external effects invoked.

## DR-W1-happy — baseline research happy path — COMPLETES-WITH-RISK

| # | Role | Decision / tool / handoff | Output / state after | Retry / stop | Evidence |
|---|---|---|---|---|---|
| 1 | pi lead | Reads recovery state; uses round-1 seed (K-01..K-07), fills parameter block from brief | defined scope + persona/slot map | preflight must pass before verdicts | HANDOFF.md:29-49; PROGRAM.md:107-125; research-agent.md:70-103 |
| 2 | pi lead | Discovers communities via web_tools.py; prioritizes lived experience | community map + targeted gaps | unlimited search/fetch | research-agent.md:13-29,104-116; web_tools.py:31-68 |
| 3 | pi lead → researcher sub-agents | Spawns up to 10 in parallel (subagent tool); miners route Luna/max openai-sub | per-miner packets + bank entries; gap reports | role failure: retry once; then INCONCLUSIVE/escalate | research-agent.md:48-52,118-139; researcher.md:8-30; PROGRAM.md:41-78 |
| 4 | pi lead | Integrates; checks §7 slots across ≥3 personas; dispatches gap-fills | repeatable bank-audit state | cannot stop at volume floors | research-agent.md:38-45,160-168,187-210 |
| 5 | pi lead | Synthesizes | research-log.md, lived-experience.md, scientific-evidence.md, sources/ | no evidence-editor gate | research-agent.md:88-91,212-218 |
| 6 | pi lead → plan-writer | Supplies exactly the 4 files | plan-writer can locate/parse/trust inputs | stops on missing/thin input | plan-writer.md:8-17; master-plan-skill-v2.md:5-20; PROGRAM.md:171-177 |

Terminal state reached: syntheses written; receiver contract coherent. Verdict COMPLETES-WITH-RISK (F-05 concurrent-write risk during parallel collection). Note: current on-disk syntheses are templates, not completed handoffs (K-08..K-12 missing) — baseline pending.

## DR-W1-failA — miner transport failure after partial packets — COMPLETES-WITH-RISK

Persisted packets remain (HANDOFF.md:117-119 checkpoint claim); lead respawns once with identical inputs (PROGRAM.md:71-74,204-208); retry succeeds → resume integration; retry fails → INCONCLUSIVE (or escalate on route/credential). State guarantee holds only if F-05 fixed.

## DR-W1-failB — thin lane cannot clear §7 — BLOCKED (F-06)

Lead must dispatch targeted gap-fills (research-agent.md:38-45,187-194); may document genuine scarcity (:41-55) with NO named decider; scarcity-marked syntheses reach plan-writer who must stop if thin (master-plan-skill-v2.md:7-14); PROGRAM defines no transition back to research or founder (PROGRAM.md:171-177).

## DR-W1-failC — Bing outage — UNDEFINED (F-07)

web_tools.py:31-56 returns error data; every coded discovery search uses the same Bing backend; fetch only helps known URLs; cannot truthfully call "genuine scarcity"; no retry/alternate/escalation defined; route-law no-fallback governs credentials, not web tools (PROGRAM.md:46-54).

## DR-W1-edge — two miners write one bank concurrently — UNDEFINED (F-05)

Parallel spawn allowed up to 10 (research-agent.md:48-52,80-85); each miner independently appends+dedupes (researcher.md:27-30); same URL's packet enriched by repeated use (sources/README.md:3-5); no lock/merge/exclusivity; lead cannot prove concurrent packets retained.

## Questions
- Q-02: HANDOFF.md:120-122 "3x 30/60/120s per PROGRAM" vs PROGRAM.md:71-74 "retried once" — nested transport retries or competing budgets unspecified.
