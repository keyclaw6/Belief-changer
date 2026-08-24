# HARNESS — running the loop in any agent harness

> The auto-research loop is **harness-neutral**. It runs in any agent harness
> that can (a) read this repo, (b) spawn a fresh sub-agent per role, (c) write
> files, and (d) run a repo script over `python3`/`bash`. The pi coding agent
> is ONE such harness, not the definition of the loop.
>
> To run the loop in a new harness: open the repo, read `loop/PROGRAM.md`, and
> say "run preflight" or "run the loop." The harness supplies the spawn +
> file + shell capabilities; everything else is in this repo.

## What is portable vs harness-specific

- **Portable (the loop itself):** `loop/PROGRAM.md` (the runbook), the role
  contract prompts (`prompts/`, `loop/prompts/`, `loop/judges/`), the
  git/worktree/state/ledger mechanics, and `scripts/check.sh` +
  `scripts/loop-runner/research_reuse.sh` + `scripts/loop-runner/web_tools.py`
  (plain `bash`/`python3`, no harness API).
- **Harness-specific (the adapter):** how a role is actually spawned and how a
  model is reached. That is the only part a harness supplies.

## Role → capability map (guidance, not a provider lock)

`loop/config.yaml` holds the founder's *preferred* models as defaults.
Models and routes are founder-only; the loop must not hypothesize a model
change. A harness substitutes what it has, per role:

| Role | Capability the role needs | Config default |
|---|---|---|
| chapter-writer | strongest prose + long context, no completion cap | Muse Spark 1.2 contributor-free (OpenCode Zen); Vercel contributor fallback |
| plan-writer | strong structured reasoning, long coherent output | Muse Spark 1.2 contributor-free (OpenCode Zen); Vercel contributor fallback |
| hypothesizer | high reasoning, single-causal-change precision | Muse Spark 1.2 contributor-free (OpenCode Zen); Vercel contributor fallback |
| plan-reviewer | independent clean-context review, high reasoning | DeepSeek V4 Flash |
| judges (3 + book-arc) | reference-sighted scoring, repeatable verdicts | DeepSeek V4 Flash |
| trace-analyzer | reads traces, maps clusters to components | DeepSeek V4 Flash |
| research lead + sub-agents | cheapest-adequate, high parallelism, needs web | DeepSeek V4 Flash |

A harness maps each role to the closest model it can reach. Research sub-agents
go on the harness's cheapest-adequate model at high parallelism — never cap
search/fetch depth to save cost.

## The spawn contract (every harness)

Every role call, on every harness, obeys:

1. Spawn a **fresh** sub-agent carrying ONLY its role contract prompt and the
   exact inputs the runbook names for that call — **no host system prompt, no
   shared context with sibling roles.** (This clean-context rule is what makes
   the loop's measurements valid; a role spawned with host baggage breaks the
   evidence.)
2. The orchestrator hands inputs and collects the output; the orchestrator
   writes files (honoring the `.partial` → rename convention, PROGRAM §4).
3. A failed role is retried once on the primary, then once on the
   `*_fallback_model` if the error is route/quota/unavailable (PROGRAM §1).
   The next unit starts on the primary.

## Model precedence (resolves config vs adapter)

`loop/config.yaml` is the loop-edited authority for *which model a role should
use*. The harness adapter resolves that to a concrete provider/model. The trace
`metadata.json` for each call records the model that *actually* ran; an
intended-vs-actual mismatch is logged as a **confound**, not read as a result.

## Per-harness bindings

| Harness | Role adapter | Spawn mechanism | Notes |
|---|---|---|---|
| **pi coding agent** | `.pi/agents/*.md` (frontmatter `model:`) | the `subagent` tool | endpoint/auth/route bindings are the `[PI BINDING]` fields in `loop/config.yaml`. Muse Spark roles pin `opencode/muse-spark-1.2-contributor-free` (OpenCode Zen Responses API, `OPENCODE_API_KEY`). Per-call fallback is Vercel `vercel/meta/muse-spark-1.2-contributor` (`AI_GATEWAY_API_KEY`). Official pi has no native fallback chain; this repo installs `pi-provider-fallback` project-locally (`.pi/settings.json`). Export `PI_PROVIDER_FALLBACK_CONFIG` to `.pi/provider-fallback.json` so the extension reads the repo chain (Vercel contributor enabled as the other-provider fallback; OpenCode same-provider fallbacks stay empty). The plugin is session-sticky; each chapter is a fresh spawn, so the next unit still starts on Zen. PROGRAM §1 is the harness-neutral retry if the extension does not fire. Preflight runs via `scripts/loop-runner/run_preflight.sh` |
| Hyperagent | spawn roles per the capability table above | the `task` tool | map each role to a model the workspace can reach; no `.pi/` files used; run preflight by spawning the judge role directly against `loop/preflight/inputs/` per PROGRAM §2 |
| opencode | judges, trace-analyzer, plan-reviewer, research sub-agents, and (via the opencode harness's own reach) the `task` tool | the `task` sub-agent tool, pinned to `opencode-go/deepseek-v4-flash` for judges/trace-analyzer/plan-reviewer (`alibaba-token-plan/deepseek-v4-flash-0731` failed judge repeatability 2026-08-17 — keep that note); research sub-agents stay on `alibaba-token-plan/deepseek-v4-flash-0731` | clean-context sub-agent per role call holding only its role prompt + the exact named inputs; no `.pi/` files used; run preflight by spawning the judge role directly against `loop/preflight/inputs/` per PROGRAM §2 (18/18 PASS on 2026-08-17 with judges pinned to `opencode-go/deepseek-v4-flash`). Writer/plan-writer/hypothesizer: primary `opencode/muse-spark-1.2-contributor-free` at `https://opencode.ai/zen/v1/responses`; fallback Vercel `meta/muse-spark-1.2-contributor`. |
| Cursor | judges spawned as fresh `agent --model composer-2.5` processes; Muse Spark roles via OpenCode Zen then Vercel HTTP | Cursor `agent` CLI / Task spawn | PROGRAM §2 preflight is spawned directly against `loop/preflight/inputs/` (do not run `run_preflight.sh`). Writer/plan-writer/hypothesizer: primary `muse-spark-1.2-contributor-free` at `https://opencode.ai/zen/v1/responses`, auth `OPENCODE_API_KEY`; on route/quota/unavailable, one retry at Vercel `meta/muse-spark-1.2-contributor` (`AI_GATEWAY_API_KEY`). Never the non-contributor alias. |

**Preflight is harness-coupled:** judge repeatability depends on the model and
sampling, so re-run preflight when the *harness or model* changes, not only
when a judge prompt changes.
