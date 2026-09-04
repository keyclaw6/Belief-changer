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
| chapter-writer | strongest prose + long context, no completion cap | Muse Spark 1.3 contributor (OpenCode Go primary; Zen contributor-free then Vercel contributor fallback) |
| plan-writer | strong structured reasoning, long coherent output | Muse Spark 1.3 contributor (OpenCode Go primary; Zen contributor-free then Vercel contributor fallback) |
| hypothesizer | high reasoning, bounded multi-change precision under the convergence budget | Claude Fable 5.1 (harness sub-agent; Cursor Task) |
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
| **pi coding agent** | `.pi/agents/*.md` (frontmatter `model:`) | the `subagent` tool | endpoint/auth/route bindings are the `[PI BINDING]` fields in `loop/config.yaml`. Muse Spark roles pin `opencode-go/muse-spark-1.3-contributor` (OpenCode Go Responses API, `OPENCODE_GO_API_KEY`). Cursor HTTP (`muse_client.py`) is Go contributor (`OPENCODE_GO_API_KEY`) → Zen contributor-free (`OPENCODE_API_KEY`) → Vercel contributor (`AI_GATEWAY_API_KEY`). 403/401/402 fall through immediately; 429 retries up to 4 × 90s on that route, then next. Never rotate the Go key onto Zen. Official pi has no native fallback chain; this repo installs `pi-provider-fallback` and `pi-goal-x` project-locally (`.pi/settings.json`). Export `PI_PROVIDER_FALLBACK_CONFIG` to `.pi/provider-fallback.json` so the extension reads the repo chain (Vercel contributor enabled as the other-provider fallback; OpenCode / OpenCode Go same-provider fallbacks stay empty). The plugin is session-sticky; each chapter is a fresh spawn, so the next unit still starts on Go. PROGRAM §1 is the harness-neutral retry if the extension does not fire. Preflight runs via `scripts/loop-runner/run_preflight.sh`. Hypothesizer: `opencode/claude-fable-5-1:high` — verify the pi opencode provider exposes this id before a pi run; Cursor is the active harness. Factory and research stay one pi conversation — see **Conversation robustness** below. |
| Hyperagent | spawn roles per the capability table above | the `task` tool | map each role to a model the workspace can reach; no `.pi/` files used; run preflight by spawning the judge role directly against `loop/preflight/inputs/` per PROGRAM §2 |
| opencode | judges, trace-analyzer, plan-reviewer, research sub-agents, and (via the opencode harness's own reach) the `task` tool | the `task` sub-agent tool, pinned to `opencode-go/deepseek-v4-flash` for judges/trace-analyzer/plan-reviewer (`alibaba-token-plan/deepseek-v4-flash-0731` failed judge repeatability 2026-08-17 — keep that note); research sub-agents stay on `alibaba-token-plan/deepseek-v4-flash-0731` | clean-context sub-agent per role call holding only its role prompt + the exact named inputs; no `.pi/` files used; run preflight by spawning the judge role directly against `loop/preflight/inputs/` per PROGRAM §2 (18/18 PASS on 2026-08-17 with judges pinned to `opencode-go/deepseek-v4-flash`). Writer/plan-writer: primary `opencode-go/muse-spark-1.3-contributor` at `https://opencode.ai/zen/go/v1/responses`; mid-chain Zen `muse-spark-1.3-contributor-free`; last fallback Vercel `meta/muse-spark-1.3-contributor`. |
| Cursor | judges spawned as fresh `agent --model composer-2.5` processes; Muse Spark writer/plan-writer via OpenCode Go then Zen contributor-free then Vercel HTTP; hypothesizer as a fresh Cursor Task (`claude-fable-5-1-thinking-high`) | Cursor `agent` CLI / Task spawn | PROGRAM §2 preflight is spawned directly against `loop/preflight/inputs/` (do not run `run_preflight.sh`). Durable runners: `scripts/loop-runner/write_replicate.py`, `judge_replicate.py`, `census_judgments.py` (not `/tmp`). Start each runner in its own tmux session; wait with `while tmux has-session -t $sess; do sleep 60; done` (do not use `tmux wait-for`). Write A and B at once (`w$I$r`); judge A when write A exits, judge B when write B exits. Judges run 8-wide inside the runner and wait for each `agent` to exit; one judge runner at a time. Writer/plan-writer: Go `muse-spark-1.3-contributor` (`OPENCODE_GO_API_KEY`) → Zen `muse-spark-1.3-contributor-free` (`OPENCODE_API_KEY`) → Vercel `meta/muse-spark-1.3-contributor` (`AI_GATEWAY_API_KEY`). 403/401/402 fall through immediately; 429 retries up to 4 × 90s on that route, then next. Never the non-contributor alias. Never rotate the Go key onto Zen. **Hypothesizer spawn:** a fresh Cursor Task, model `claude-fable-5-1-thinking-high`. Prompt = `loop/prompts/hypothesizer.md` verbatim, then the three PROGRAM input paths, then: "Read-only. Do not edit any file. Return the complete hypothesis as your final message. Nothing else." The orchestrator writes `loop/iterations/NNN/hypothesis.md` unchanged and sidecar `hypothesis-metadata.json` `{model, harness, spawn: "cursor-task"}`. A Cursor Task carries Cursor's system prompt, exactly as `agent --model composer-2.5` judges already do — accepted harness baggage, not a per-iteration confound. **Conversation robustness:** this live conversation is the orchestrator. Durability is `.cursor/hooks.json` `stop` / `subagentStop` (`.cursor/hooks/loop-continue.py`) — Cursor's `agent_settled`: while `loop/state.md` is `IN PROGRESS` and the turn `completed`, inject PROGRAM §0 resume. User `aborted` is a halt. After a runner **exits**, start the next unit here (`needs changes first` → next plan-write; last chapter written → snapshot). Do not spawn a background Task and end the parent turn. Do not `block_until_ms: 0` a multi-chapter runner and AwaitShell the first OK line — that unit is the process exit. Do not add a process driver. |

## Conversation robustness (factory and research)

The orchestrator is an **agent conversation**. Role runners are tools that
conversation starts; they do not replace it. Do not add a hidden process
driver. Temporal (or similar) is allowed only as thin durability that
resumes this same conversation; `loop/PROGRAM.md` remains the sequencer.

**pi (this repo's 0.84.x binding):** `npm:pi-goal-x` (peers `>=0.83 <0.85`).
`/goal-direct` and `/sisyphus-direct` create a focused goal with autoContinue
on; continuation queues on `agent_settled` (after retries and compaction), not
`agent_end`. Goals persist under `.pi/goals/`. Resume a killed process with
`pi --resume <session.jsonl>`.

```bash
export PI_PROVIDER_FALLBACK_CONFIG="$(pwd)/.pi/provider-fallback.json"
pi
```

- Factory (ordered PROGRAM units): `/sisyphus-direct` — run one iteration of
  `loop/PROGRAM.md` to KEEP or REVERT. Spawn each role as a fresh sub-agent;
  wait for that unit's on-disk marker; then the next unit. Do not exit while
  `loop/state.md` is `IN PROGRESS`.
- Research (open-ended until artifacts exist): `/goal-direct` — execute
  `prompts/research-agent.md` as research lead. Spawn `.pi/agents/researcher.md`
  miners in parallel; no search/fetch ceilings; stop only when the accepted
  research artifacts the runbook names are on disk.

Do not use `@latent-variable/pi-auto-continue` (`agent_end`, naive "continue").
Do not use timer `/loop` extensions. `npm:pi-agent-goal` is the same
conversation-goal design but peer-blocked on pi ≥0.81 (`<0.81` ceiling).
Fallback if `pi-goal-x` cannot load: `npm:@narumitw/pi-goal` (also
`agent_settled`).

**Cursor:** this conversation is the orchestrator. Do not detach the factory
into a background Task and stop. Start each runner in its own tmux session so
a dropped tool stream does not kill the writer or judge. `$W` = iteration
worktree, `$I` = NNN, `$r` = a|b:

```bash
tmux new -d -s w$I$r "cd $W && dotenvx run -f .env -- env BC_REPO=$W ITER=$I REPLICATE=$r \
  python3 scripts/loop-runner/write_replicate.py >> loop/iterations/$I/write-$r.log 2>&1"
while tmux has-session -t w$I$r 2>/dev/null; do sleep 60; done
```

Same pattern for `judge_replicate.py` (`j$I$r`). Do not use `tmux wait-for`
(a signal is consumed by the first waiter; a resumed wait blocks forever).
Re-run the wait verbatim on resume — it is stateless. Then check markers:
chapter files in `replicate-$r/chapters/`, last log line `OK chapter-NN`.
Judges run 8-wide inside one runner and wait for each `agent` to exit; one judge runner at a time. Thin
durability: `.cursor/hooks/loop-continue.py` on `stop` and `subagentStop`
re-enters this conversation while `loop/state.md` is `IN PROGRESS` (skip
`aborted`). That is the Cursor binding of pi's `agent_settled`. The founder
can walk away; a user abort still halts.

**Preflight is harness-coupled:** judge repeatability depends on the model and
sampling, so re-run preflight when the *harness or model* changes, not only
when a judge prompt changes.
