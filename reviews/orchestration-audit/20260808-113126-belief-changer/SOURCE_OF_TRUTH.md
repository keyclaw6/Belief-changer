# SOURCE OF TRUTH — discovered precedence chain

Precedence is declared in `loop/config.yaml` ("SOLE authority for routes,
models, and parameters... nothing in PROGRAM.md overrides this file"),
`loop/PROGRAM.md` §1 ("the pi agent definitions in `.pi/agents/` pin the same
models. No value elsewhere overrides config."), and `AGENTS.md` (on-disk).
The chain from highest to lowest, as declared:

| # | Source | Authority | Scope | Status |
|---|---|---|---|---|
| S-1 | `docs/VISION.md` Part I | AGENTS.md: required reading; product-intent exception to doc policy | product vision | Current |
| S-2 | `docs/BOOK-FACTORY-VISION.md` | founder-owned lock | factory expected result | Current |
| S-3 | `docs/AUTO-TUNING-LOOP.md` | founder-locked North Star | loop purpose | Current |
| S-4 | `loop/PROGRAM.md` | AGENTS.md: "sole operational runbook"; self-declared | loop execution | Current |
| S-5 | `loop/config.yaml` | PROGRAM §1 + file header: "SOLE authority for routes, models, and parameters"; nothing overrides it | routes/models/params | Current |
| S-6 | `prompts/*.md`, `loop/prompts/*.md`, `.pi/agents/*.md` | AGENTS.md truth hierarchy: "Code and prompts — implementation truth"; PROGRAM §1: prompts are the real tuning surface, .pi agents are thin wrappers | role behavior | Current |
| S-7 | `AGENTS.md` (repo instructions) | repository convention | cross-cutting rules, content rules | Current |
| S-8 | `production-books/` | AGENTS.md truth hierarchy: product artifacts, not truth | output evidence | Current |
| S-9 | `calibration/`, `analysis/`, historical `_rounds/`, archived `loop/preflight/runs-2026-07-sol-era/` | marked retired/historical in PROGRAM/HANDOFF | history | Historical (excluded unless loaded) |

**Unresolved authority:** no complete instruction-precedence chain is declared
for simultaneous activation of AGENTS.md rules, PROGRAM.md steps, and role
prompts beyond the routing/parameter authority granted to config.yaml.
`prompts/style-guide.md` declares "Where Part B is more specific, Part B wins"
and the FIDELITY DOCTRINE (corpus wins over softer house rules) — internal
style-guide precedence only.

## Seed requirement ledger (lead-extracted; verified by spec archaeologist)

| ID | Strength | Source | Requirement |
|---|---|---|---|
| R-001 | MUST | AGENTS.md Sacred + research-agent.md Standing law | Research depth unlimited; no search/fetch ceilings; filter after, never upfront |
| R-002 | MUST | research-agent.md Priority order + Standing law | Lived experience is the primary target; forums/recovery communities; Reddit excluded without explicit authorization |
| R-003 | MUST | research-agent.md §6 + sources/README.md | Provenance (6 elements), character-for-character quotes, no fabricated/composite quotes |
| R-004 | MUST | research-agent.md §7 | Completion criterion clears across ≥3 materially distinct personas before synthesis |
| R-005 | MUST | master-plan-skill-v2.md Exact inputs | Plan-writer receives exactly 4 files (style guide, brief, lived-experience, scientific-evidence); no reference contamination |
| R-006 | MUST | master-plan-skill-v2.md Fresh review gate + PROGRAM §3 | Plan-reviewer gate must end with standalone `fit to write from` before writing |
| R-007 | MUST | chapter-writer.md + PROGRAM §3 | Chapter-writer receives exactly 4 inputs; card is semantic authority; only valid output is chapter or exact refusal line |
| R-008 | MUST | PROGRAM §1 + AGENTS.md | Zero deterministic validation; every check done by role agents per prompts |
| R-009 | MUST | PROGRAM §1 + config.yaml | Every role is a fresh spawned pi sub-agent carrying only its role prompt + listed inputs; no host system prompt |
| R-010 | MUST | config.yaml + AGENTS.md Route law | Routing: CC proxy carries writer (muse, high, temp 0.7, no max_tokens), research orchestrator (MiniMax M3), plan-writer (Kimi K3), plan-reviewer (luna); openai-sub carries research sub-agents (luna max), judges (luna high), trace-analyzer (luna high), hypothesizer (sol high) |
| R-011 | MUST | config.yaml + AGENTS.md + HANDOFF | No fallback route coded; on route/credential failure STOP and escalate to founder |
| R-012 | MUST | PROGRAM §1 + AGENTS.md | One commit per iteration on campaign branch; only founder merges to main |
| R-013 | MUST | PROGRAM §3 Error handling + chapter-writer.md | Writer refusal → saved to `traces/chapter-NN/refusal.md`, no chapter file, iteration INCONCLUSIVE |
| R-014 | MUST | PROGRAM §2 | Preflight judge battery must pass before trusting campaign verdicts |
| R-015 | SHOULD | style-guide.md (founder-owned) | Mantra verbatim repetition law, banned register, anatomy, metrics |
| R-016 | MUST | PROGRAM §3 Error handling | Sub-agent failure: retry once with same inputs; still failing → INCONCLUSIVE or escalate to founder |
