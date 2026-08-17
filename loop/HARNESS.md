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

`loop/config.yaml` holds the founder's *preferred* models as defaults and is
the loop's tuning surface. A harness substitutes what it has, per role:

| Role | Capability the role needs | Config default |
|---|---|---|
| chapter-writer | strongest prose + long context, no completion cap | Muse Spark 1.2 contributor |
| plan-writer | strong structured reasoning, long coherent output | Muse Spark 1.2 contributor |
| hypothesizer | high reasoning, single-causal-change precision | Muse Spark 1.2 contributor |
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
3. A failed role is retried once, then INCONCLUSIVE or escalate (PROGRAM §1).

## Model precedence (resolves config vs adapter)

`loop/config.yaml` is the loop-edited authority for *which model a role should
use*. The harness adapter resolves that to a concrete provider/model. The trace
`metadata.json` for each call records the model that *actually* ran; an
intended-vs-actual mismatch is logged as a **confound**, not read as a result.

## Per-harness bindings

| Harness | Role adapter | Spawn mechanism | Notes |
|---|---|---|---|
| **pi coding agent** | `.pi/agents/*.md` (frontmatter `model:`) | the `subagent` tool | endpoint/auth/route bindings are the `[PI BINDING]` fields in `loop/config.yaml`; preflight runs via `scripts/loop-runner/run_preflight.sh` |
| Hyperagent | spawn roles per the capability table above | the `task` tool | map each role to a model the workspace can reach; no `.pi/` files used; run preflight by spawning the judge role directly against `loop/preflight/inputs/` per PROGRAM §2 |
| opencode | judges, trace-analyzer, research sub-agents, and (via the opencode harness's own reach) the `task` tool | the `task` sub-agent tool, pinned to `alibaba-token-plan/deepseek-v4-flash-0731` | clean-context sub-agent per role call holding only its role prompt + the exact named inputs; no `.pi/` files used; run preflight by spawning the judge role directly against `loop/preflight/inputs/` per PROGRAM §2. Writer/plan-writer/hypothesizer route via the Command Code proxy `http://127.0.0.1:3050/v1/chat/completions`. |
| other | *(add a row when a harness is used)* | its spawn capability | |

**Preflight is harness-coupled:** judge repeatability depends on the model and
sampling, so re-run preflight when the *harness or model* changes, not only
when a judge prompt changes.
