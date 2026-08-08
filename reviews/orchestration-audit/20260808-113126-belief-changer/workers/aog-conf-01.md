# Worker shard — AOG-CONF-01 (instruction-conflict + precedence reviewer)

- Reviewer: GPT-5.6 Terra medium sub-agent (nickname Jason), read-only
- Scope: all instruction layers active in research + book-writing stages

## Candidates

### CAND-AOG-CONF-01-001 — Required Reddit research conflicts with an active prohibition (CONFIRMED-DEFECT, HIGH/HIGH)

Evidence:
- docs/AUTO-TUNING-LOOP.md:129 — lived-experience lane "must go into forums, Reddit, support communities"
- AGENTS.md:13 — research "must reach forums, Reddit, support communities"
- prompts/research-agent.md:35 — target includes "Reddit and its reachable mirrors/archives"
- prompts/research-agent.md:60-61 — "Reddit is excluded without explicit Reddit authorization"
- .pi/agents/researcher.md:24-25 — same prohibition for spawned miners

A normal campaign has no explicit Reddit authorization; simultaneously required to reach Reddit and forbidden from using it. Mirrors/archives are named alternatives but not declared equivalent to the "must reach Reddit" requirement. No authorization/precedence resolution path specified.

### CAND-AOG-CONF-01-002 — Plan-review reasoning value contradicts config authority (CONFIRMED-DEFECT, MEDIUM/HIGH)

Evidence:
- loop/config.yaml:2-4 sole authority; :55 proxy accepts low/medium/high/max; :64-65 plan_reviewer_reasoning: max
- prompts/master-plan-skill-v2.md:143-145 requires config route/model but also `xhigh` reasoning
- loop/PROGRAM.md:37-39 no value overrides config

Planning gate can send invalid `xhigh`, violate the prompt by sending `max`, or silently translate — no declared rule. (Disputed by AOG-PLAN-01 as non-material; see adjudication.)

## Passes
- Route/model split consistent across AGENTS.md, PROGRAM, HANDOFF, config, all live .pi pins
- Research lead (MiniMax/CC) vs miners (Luna/openai-sub) consistently distinguished
- Plan-review five-file contract consistent; intro is shorthand not a competing contract
- chapter-reviewer.md has no live reference (historical); book-analysis-agent.md still cited by VISION for the separate analysis phase
- On-disk AGENTS.md contains no evidence-editor/framing-gate reference; research-agent.md:87 explicitly says no separate evidence-editor gate

## Integrity
- No files written; no services called.
