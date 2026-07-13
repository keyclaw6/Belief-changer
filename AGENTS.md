# AGENTS.md

## Mission
Generate high-quality, Allen Carr "Easyway"-style belief-change books — free, open-source, nonprofit, in every language and format (EPUB, audiobook), delivered on a self-evolving community website. Correcting misaligned beliefs changes behavior automatically, without willpower.
**Required reading: `docs/VISION.md` Part I** — the canonical founder vision every change in this repo serves. Read it before your first task here.

## Priorities
When priorities conflict: 1. Method integrity. 2. Quality. 3. Simplicity. 4. Reach. 5. Cost.
Method integrity means: non-shaming framing, willpower-free logic, original text only (learn the mechanism, never reproduce copyrighted prose), and evidence-graded research. A book that violates these has failed regardless of polish.

## Truth Hierarchy
1. `openspec/specs/` — behavior and method truth. Read the relevant spec before changing pipeline or content behavior; author changes under `openspec/changes/<slug>/`.
2. Code and prompts — implementation truth. Keep them legible instead of describing them in prose.
3. Books under `production-books/` — product artifacts, not truth about the system.
4. `docs/` — only what agents cannot succeed without.

## Golden Principles (YAGNI)
This repo is agents-native: optimize for the next agent run. Every line is a liability.
- Implement only what a spec scenario requires. No speculative capability or future-proofing.
- Smallest diff that satisfies the scenario. Prefer deleting to adding.
- No new abstraction until the third concrete use. No wrapper around a wrapper.
- Delete, don't deprecate — dead code, prompts, and docs go in the change that obsoletes them.
- One obvious way: follow the nearest similar pattern; fix bad patterns everywhere, never fork a second style.
- Files stay small (≤260 lines code, this file ≤130 — validator-enforced).
- One-shot scripts are deleted after execution.

## Documentation Policy
Write no documentation by default. A doc must be load-bearing (an agent cannot complete a real task from code + specs alone), generated, or curated reference material. Never write docs that restate code, specs, or prompts. `docs/VISION.md` is the product-intent exception. Update or delete stale docs in the same change that invalidates them.

## Content Rules
- The global style guide and the method principles in `openspec/specs/method-integrity/` bind every writing agent. Style-guide changes are founder-approved only.
- `production-books/<slug>/` layout (brief, research/sources/, lived-experience.md, scientific-evidence.md, framing, master plan, chapters) is a stable external contract — agent skills depend on these paths. Do not restructure it.
- Published books are immutable artifacts; corrections produce new versions.

## Dependencies
Understand or recreate: prefer dependencies fully reasoned about in-repo; reimplement small subsets over adopting frameworks. Model access goes through the founder's endpoints — the LiteLLM proxy (`belief-changer` virtual key, by alias) or the founder's OpenRouter key (calibration) — always via env vars; no provider keys in this repo.

## Environment Files
Real `.env*` files (not placeholder examples) are dotenvx-encrypted source of truth and are committed. Never commit `.env.keys` or `DOTENV_PRIVATE_KEY`; Kristian's machine keeps the one shared private key at `~/.config/dotenvx/.env.keys` and its public key at `~/.config/dotenvx/public.env`. Reuse that keypair for every env file and use `dotenvx run -- <command>` or `dotenvx set KEY value` instead of plaintext secrets.

## Code Intelligence
Use the codebase-memory-mcp tools: blast-radius (`detect_changes`) before modifying existing code, `search_graph`/`trace_path` when exploring, `manage_adr` for architecture decisions instead of docs.

## Repo Map
- `production-books/<slug>/` — the per-book workshop. Published output targets the future site (see `docs/VISION.md`); the retired root `books/` held reference texts now in `analysis/reference-books/`.
- `prompts/` — the pipeline's prompt assets. `openspec/` — specs and changes.
- `scripts/` — gates and tooling (`check.sh` is the canonical gate). `docs/` — VISION.md and the minimal load-bearing set.

## Workflow
1. Read the relevant spec domain first; check `openspec/changes/` for collisions.
2. Behavior or method change → openspec change first; validate with `openspec validate <slug> --strict`.
3. Every new test cites the spec scenario it proves, or is marked infra.
4. Gate everything with `bash scripts/check.sh`. Trust real exit codes only.
5. Conventional Commits, straight to `main`, push after each logical change.

## Harness Rule
When a task fails or confuses, don't just retry: name the missing capability (context, spec, test, tool, check), then fix it as part of the task or record it in the active exec plan.
