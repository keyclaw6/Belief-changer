# Worker shard — AOG-BLOAT-01 (complexity/duplication/stale reviewer)

- Reviewer: GPT-5.6 Terra medium sub-agent (nickname Aquinas), read-only
- Scope: full inventories under prompts/, .pi/agents/, loop/, production-books/_template/, scripts/loop-runner/

## Candidates

### CAND-AOG-BLOAT-01-001 — Reddit depth rule has incompatible maintenance copies (CONFIRMED-DEFECT, HIGH/HIGH)

Evidence: AGENTS.md:14 requires reaching Reddit; docs/AUTO-TUNING-LOOP.md:99-104 likewise; prompts/research-agent.md:82-85 dispatches miners; .pi/agents/researcher.md:20-25 prohibits Reddit without explicit authorization. Duplicate policy cluster with opposing default behavior; no precedence resolution. (Duplicate symptom of CAND-AOG-CONF-01-001 — merged.)

### CAND-AOG-BLOAT-01-002 — Dead chapter-review workflow remains as an actionable prompt and current workflow instruction (MATERIAL-RISK, MEDIUM/HIGH)

Evidence:
- prompts/chapter-reviewer.md:3 directs a post-draft writer-reviewer loop and cites nonexistent PROGRAM §4.1 (PROGRAM.md:127-300 has §4 Steps 1-7; no §4.1)
- PROGRAM.md:179-212 defines writing as sequential writer calls; :214-251 sends chapters to judges
- production-books/README.md:32 still tells operators "a reviewer loop critiques each before moving on"

Orphaned actionable prompt + README prescribe a removed stage; an operator can invoke the stale reviewer and confuse its verdict with the current judge process. No live reference prevents manual loading.

### CAND-AOG-BLOAT-01-003 — config.yaml presents unconsumed parameter fields as sole runtime authority (MATERIAL-RISK, MEDIUM/HIGH)

Evidence: config.yaml:12-15,24-26,41-43 define endpoint/auth/reasoning/temperature; :31-32 unlimited search/fetch limits; no repo consumer outside config; run_preflight.sh reads only judge_model/judge_reasoning; role models pinned in .pi/agents/*.md:5. (Duplicate symptom of CAND-AOG-CHAP-01-001 + CAND-AOG-XSYS-01-001 — merged.)

## Passes / observations
- No-fallback and role-route copies consistent; input-list copies consistent
- book-analysis-agent.md: separate analysis workflow, still cited (VISION.md:158)
- _rounds/ is active seed material explicitly retained (HANDOFF.md:29-43)
- reference-alignment.md correctly blank pre-baseline; Sol-era preflight explicitly archived
- daemon.sh/queue_runner.sh optional VPS path explicitly documented (HANDOFF.md:106-108)
- Observation: _template/master-plan-review.md:3 stale Sol comment (body current)
- Observation: research-agent.md:84 "(§5)" cross-ref — reviewer judged §5 = ten-bank section (disagrees with lead's reading that banks are §4; low materiality either way)

## Integrity
- No files written; no services called.
