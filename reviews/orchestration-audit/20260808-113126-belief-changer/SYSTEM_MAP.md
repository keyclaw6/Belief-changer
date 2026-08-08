# SYSTEM MAP — factory roles, contracts, and workflows (research + book writing)

## Roles

| Role | Is | Contract prompt | Model / route (config) | Tools | Writable state |
|---|---|---|---|---|---|
| Orchestrator (pi coding agent session) | not spawned; the session | `loop/PROGRAM.md`; research phase additionally uses `prompts/research-agent.md` as its operating doctrine | MiniMax M3 via CC proxy (research phase); otherwise operator-chosen | `subagent` tool, `web_tools.py`, `scripts/check.sh` | campaign branch: research/, plans, chapters, traces |
| `researcher` (spawned) | sub-agent | `.pi/agents/researcher.md` (+ doctrine context per task) | openai-sub gpt-5.6-luna:max | `web_tools.py`, read/write | its assigned output bank file (path per task) |
| `plan-writer` (spawned) | sub-agent | `.pi/agents/plan-writer.md` → `prompts/master-plan-skill-v2.md` | commandcode moonshotai/Kimi-K3 | read/write | `master-plan.md` |
| `plan-reviewer` (spawned) | sub-agent | `.pi/agents/plan-reviewer.md` → `prompts/master-plan-reviewer-v2.md` | commandcode gpt-5.6-luna | read/write | `master-plan-review.md` verdict |
| `chapter-writer` (spawned) | sub-agent | `.pi/agents/chapter-writer.md` → `prompts/chapter-writer.md` | commandcode meta/muse-spark-1.2-contributor | read/write | chapter file or refusal |
| judge / trace-analyzer / hypothesizer | spawned consumers (out of scope) | `.pi/agents/*.md` → `loop/judges/*`, `loop/prompts/*` | openai-sub luna high / luna high / sol high | read / read,write / read,write | judgments, trace-analysis, hypothesis |

## Workflows

- **W1 Research:** orchestrator fills parameter block (§1) → discovers communities (§2) → spawns researcher sub-agents in parallel (up to 10, one work order each) per lane/persona/community (§3) → integrates, names gaps, re-dispatches → synthesizes (§8) into `research-log.md`, `lived-experience.md`, `scientific-evidence.md`, `sources/` when §7 completion criterion clears across ≥3 personas.
- **W2 Planning:** orchestrator spawns plan-writer (exactly 4 inputs) → spawns plan-reviewer (plan + 4 inputs) → hands back to plan-writer until `master-plan-review.md` ends `fit to write from` (up to 3 cycles per skill) → rebuild `loop/reference-alignment.md` when plan changed.
- **W3 Writing:** orchestrator spawns chapter-writer one chapter at a time, ch 01 → last; each spawn = exactly 4 inputs (master plan, chapter card, style guide, previous chapter; ch 01 gets plan book-core). Refusal → `traces/chapter-NN/refusal.md`, no chapter file, INCONCLUSIVE.
- **W4 (consumer)** Judges/trace/hypothesizer run after writing; not entity-reviewed here.

## Contract edges (handoffs)

- Research → planning: `production-books/<slug>/research/lived-experience.md` + `scientific-evidence.md` (accepted syntheses) are the only research artifacts the plan-writer/reviewer may read.
- Planning → writing: `master-plan.md` (chapter cards + plan-wide inventories) + `master-plan-review.md` verdict.
- Writing → judging: chapter files + CHAPTER CONTEXT copied from the accepted card.

## Parameter/routing surface (config.yaml)

- Declared fields for writer (endpoint, auth env, reasoning high, temperature 0.7), researcher/planner endpoints, gpt_endpoint, per-role models/reasoning.
- Only consumer found: `run_preflight.sh` reads `judge_model`/`judge_reasoning`. No code consumer for endpoint/temperature/reasoning fields of writer/researcher/planner (candidate — verify).
