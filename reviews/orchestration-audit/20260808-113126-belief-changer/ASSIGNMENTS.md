# ASSIGNMENT REGISTER

All reviewers: GPT-5.6 Terra medium, read-only, no writes outside their own
report (returned in final message; lead persists shards to `workers/<id>.md`).
Every reviewer must read the on-disk `AGENTS.md` (the injected session copy is
stale), the canonical spec set (docs/VISION.md Part I, BOOK-FACTORY-VISION,
AUTO-TUNING-LOOP, loop/PROGRAM.md, loop/config.yaml), SOURCE_OF_TRUTH.md,
SYSTEM_MAP.md, the skill's audit-method.md, and report with exact file:line
evidence. Independence groups: ambiguity interpreters never see each other's
outputs; the skeptical verifier authors none of the candidates it verifies;
the coverage closer holds no original assignment.

| Worker | Reviewer role | Exact scope | Unique output path | Independence group |
|---|---|---|---|---|
| AOG-RES-01 | Research-stage entity reviewer | `prompts/research-agent.md`, `.pi/agents/researcher.md`, `scripts/loop-runner/web_tools.py`, `research/sources/README.md`, config research fields, round-1 artifacts as historical evidence | workers/aog-res-01.md | primary |
| AOG-PLAN-01 | Planning-stage entity reviewer | `prompts/master-plan-skill-v2.md`, `prompts/master-plan-reviewer-v2.md`, `.pi/agents/plan-writer.md`, `.pi/agents/plan-reviewer.md`, `production-books/_template/master-plan.md` + `master-plan-review.md`, config planner/review fields | workers/aog-plan-01.md | primary |
| AOG-CHAP-01 | Chapter-writing entity reviewer | `prompts/chapter-writer.md`, `.pi/agents/chapter-writer.md`, `prompts/style-guide.md` (as loaded craft contract), PROGRAM §3 writing stage, config writer fields | workers/aog-chap-01.md | primary |
| AOG-XSYS-01 | Identity/boundary/authority/handoff | orchestrator role, research→plan→chapters transitions, spawn authority, routing law config vs `.pi` pins, parameter enforcement, refusal/retry paths | workers/aog-xs-01.md | primary |
| AOG-CONF-01 | Instruction-conflict + precedence | AGENTS.md, PROGRAM.md, HANDOFF.md, config.yaml, all in-scope prompts + .pi agents; simultaneous-activation conflicts | workers/aog-conf-01.md | primary |
| AOG-BLOAT-01 | Complexity/duplication/stale | `prompts/chapter-reviewer.md`, `prompts/book-analysis-agent.md`, `_rounds/`, `_template/`, `reference-alignment.md`, dead config keys, cross-doc drift, duplication | workers/aog-bloat-01.md | primary |
| AOG-DRY-01 | Dry-run — research | W1 happy path + failure path (spawn failure, thin slot, fetch failure) to terminal synthesis | workers/aog-dry-01.md | dry-run |
| AOG-DRY-02 | Dry-run — book writing | W2 plan loop + W3 sequential chapters, refusal path, reviewer-block path | workers/aog-dry-02.md | dry-run |
| AOG-AMB-01..03 | Independent ambiguity interpreters | shortlist of consequential candidates (lead-curated after wave 1) | workers/aog-amb-NN.md | AMB (isolated) |
| AOG-VER-01 | Skeptical verifier | all Critical/High/Medium candidates + sampled Low | workers/aog-ver-01.md | VER (post-hoc) |
| AOG-CLOSE-01 | Coverage closer | full coverage audit of the run | workers/aog-close-01.md | CLOSE (post-hoc) |
