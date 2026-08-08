# AGENTS.md

## Mission
Generate high-quality, Allen Carr "Easyway"-style belief-change books — free, open-source, nonprofit, in every language and format (EPUB, audiobook), delivered on a self-evolving community website. Correcting misaligned beliefs changes behavior automatically, without willpower.
**Required reading: `docs/VISION.md` Part I** — the canonical founder vision every change in this repo serves. Read it before your first task here.

## Book Factory Vision Lock
`docs/BOOK-FACTORY-VISION.md` is the founder-owned expected result for the book factory. Every agent working on the factory, calibration, harness, research, planning, writing, reviewing, or judging MUST read it before acting and hold its work against it. No agent may edit, delete, rename, supersede, reinterpret away, or weaken that file without an explicit founder instruction.

## Auto-Tuning Loop Lock
`docs/AUTO-TUNING-LOOP.md` is the founder-locked North Star for the auto-research loop that tunes the book factory. Every agent working on the loop, judges, research, or factory tuning MUST read it before acting. No agent may weaken or reinterpret away that file without an explicit founder instruction.

**Sacred: Research depth is unlimited.** The deep search must be as wide and deep as still brings results. No artificial limits on search count or fetch count. Allow 1,000+ searches and 1,000+ fetched resources. Filter afterwards, never limit upfront. DeepSeek V4 Pro is essentially free; the constraint is quality, not cost. The research must reach forums, Reddit, support communities, and niche spaces where people with shame confess and narrate their experience honestly. This lived-experience material is what makes the book feel like it was written by someone who truly understands the reader. No agent may impose search or fetch ceilings that prevent reaching this material.

## Priorities
When priorities conflict: 1. Method integrity. 2. Quality. 3. Simplicity. 4. Reach. 5. Cost.
Method integrity means: **Carr-fidelity** — the Easyway method executed exactly as Allen Carr practices it (his warmth to the reader, his commands, his full-force scares delivered then disowned, his certainty), original text only (learn the mechanism, never reproduce copyrighted prose), and evidence-graded research. The factory matches Carr before any house twist is applied. A book that violates these has failed regardless of polish.

## Truth Hierarchy
1. Code and prompts — implementation truth. Keep them legible instead of describing them in prose.
2. Books under `production-books/` — product artifacts, not truth about the system.
3. `docs/` — only what agents cannot succeed without.

## Golden Principles (YAGNI)
This repo is agents-native: optimize for the next agent run. Every concept must
serve a current requirement or concrete risk.
- Implement only what a spec scenario requires. No speculative capability or future-proofing.
- Make the smallest clear change that satisfies the scenario. Remove genuinely
  redundant code instead of adding another path.
- No new abstraction until the third concrete use. No wrapper around a wrapper.
- Delete, don't deprecate — dead code, prompts, and docs go in the change that obsoletes them.
- One obvious way: follow the nearest similar pattern; fix bad patterns everywhere, never fork a second style.
- One-shot scripts are deleted after execution.

## Documentation Policy
Write no documentation by default. A doc must be load-bearing (an agent cannot complete a real task from code + specs alone), generated, or curated reference material. Never write docs that restate code, specs, or prompts. `docs/VISION.md` is the product-intent exception. Update or delete stale docs in the same change that invalidates them.

## Content Rules
- The global style guide and the method principles bind every writing agent. Style-guide changes on `main` are founder-approved only; the auto-tuning loop may amend the style guide on its campaign branch, and winning amendments merge in founder-reviewed batches.
- `production-books/<slug>/` layout (brief, research/sources/, lived-experience.md, scientific-evidence.md, master plan, chapters) is a stable external contract — agent skills depend on these paths. Do not restructure it.
- Calibration research runs through the auto-tuning loop (`loop/PROGRAM.md`) on the routes in `loop/config.yaml`. Planning consumes only accepted research artifacts.
- Published books are immutable artifacts; corrections produce new versions.

## Auto-tuning campaign
An explicit founder request to run the loop authorizes iterations. `loop/PROGRAM.md` is the sole operational runbook. `loop/config.yaml` is the sole model-route and parameter source. During a campaign, only files the runbook marks editable may change, on the campaign branch. Judges, trace analysis, hypothesizing, plan review, writer, research, and planner all run as spawned pi sub-agents (`.pi/agents/*.md`) — judges, the trace analyzer, the hypothesizer, and the research sub-agents through the OpenAI subscription (openai-sub), the rest through the founder's Command Code proxy loopback — all per config. A role call carries only its role prompt and listed inputs: no hosted agent, no host system prompt. Calibration candidates produced by the loop use the runbook's judge gate and are not published or advanced as accepted book chapters.

## Dependencies
Understand or recreate: prefer dependencies fully reasoned about in-repo; reimplement small subsets over adopting frameworks. Model access goes through the founder's endpoints and always via environment variables; no provider keys belong in this repo. Route law (founder route change 2026-08-07): the founder's Command Code proxy loopback carries ONLY the writer calls (no `max_tokens`, no fallbacks), MiniMax M3 research, and Kimi K3 planning — all exactly as configured in `loop/config.yaml`, authenticated by `COMMANDCODE_API_KEY` (operator environment, or the Command Code CLI login when unset). No fallback route is coded: on credential or proxy failure the executor stops and calls the founder. Judging, trace analysis, hypothesizing, and the research sub-agents run through the OpenAI subscription route (openai-sub provider) — clean contexts with only the role prompt, never a hosted agent with its own system prompt; plan review and the rest of the loop stay on the Command Code proxy.

## Environment Files
Real `.env*` files (not placeholder examples) are dotenvx-encrypted source of truth and are committed. Never commit `.env.keys` or `DOTENV_PRIVATE_KEY`; Kristian's machine keeps the one shared private key at `~/.config/dotenvx/.env.keys` and its public key at `~/.config/dotenvx/public.env`. Reuse that keypair for every env file and use `dotenvx run -- <command>` or `dotenvx set KEY value` instead of plaintext secrets.

## Code Intelligence
Use the codebase-memory-mcp tools: blast-radius (`detect_changes`) before modifying existing code, `search_graph`/`trace_path` when exploring, `manage_adr` for architecture decisions instead of docs.

## Repo Map
- `production-books/<slug>/` — the per-book workshop. Published output targets the future site (see `docs/VISION.md`); the retired root `books/` held reference texts now in `analysis/reference-books/`.
- `prompts/` — the pipeline's prompt assets.
- `loop/` — the auto-tuning loop: `loop/PROGRAM.md` (runbook), judges, loop prompts, config, results, learnings, iterations; `calibration/reference/gsbs/` — the extracted real book; `calibration/` also holds retired-lab archaeology.
- `scripts/` — gates and tooling (`check.sh` is the canonical gate). `docs/` — VISION.md and the minimal load-bearing set.

## Workflow
1. Gate everything with `bash scripts/check.sh`. Trust real exit codes only.
2. Conventional Commits, straight to `main`, push after each logical change. The auto-tuning loop is the explicit exception: it commits one per iteration on its campaign branch (`loop/PROGRAM.md` §1); only the founder merges winning amendments to `main`.

## Calibration Recovery
The auto-tuning loop is `loop/PROGRAM.md`. After any context compaction, task resume, or operator handoff, follow its §0 Recovery: read the runbook, the North Star, the tail of `loop/learnings.md`, and the last data row of `loop/results.tsv`; state the last iteration, its verdict, and the next hypothesis before acting.

## Harness Rule
When a task fails or confuses, don't just retry: name the missing capability (context, spec, test, tool, check), then fix it as part of the task or record it in the active exec plan.
