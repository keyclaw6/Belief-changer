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
| factory-orchestrator | agent conversation that loops plan-writer ↔ plan-reviewer then chapter-writer ↔ chapter-reviewer | Muse Spark 1.3 contributor (OpenCode Go primary; same chain as the writer) |
| chapter-writer | strongest prose + long context, no completion cap | Muse Spark 1.3 contributor (OpenCode Go primary; Zen contributor-free then Vercel contributor fallback) |
| plan-writer | strong structured reasoning, long coherent output | Muse Spark 1.3 contributor (OpenCode Go primary; Zen contributor-free then Vercel contributor fallback) |
| hypothesizer | high reasoning, bounded multi-change precision under the convergence budget | GPT-6 Astra (Experiential HTTP); fallback Claude Fable 5.1 |
| plan-reviewer | independent clean-context review, high reasoning | Muse Spark 1.3 contributor (same Go→Zen→Vercel chain as the writer) |
| chapter-reviewer | plan-fidelity + length vs card budget; never sees GSBS | Muse Spark 1.3 contributor (same Go→Zen→Vercel chain as the writer) |
| judges (chapter lanes + comparison + book-arc + carr-distance) | reference-sighted scoring, repeatable verdicts | Cursor live panel: Composer 2.5. Other harnesses: Muse Spark 1.3 contributor |
| trace-analyzer | reads traces, maps clusters to components | Muse Spark 1.3 contributor |
| research lead + sub-agents | cheapest-adequate, high parallelism, needs web | Muse Spark 1.3 contributor |

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
| **pi coding agent** | `.pi/agents/*.md` (frontmatter `model:`) | the `subagent` tool | Factory conversation: `.pi/agents/factory-orchestrator.md` on Muse Spark 1.3 (`/sisyphus-direct` on `prompts/factory-orchestrator.md`). Auto-research is a separate PROGRAM conversation that starts factory sessions. Muse Spark roles pin `opencode-go/muse-spark-1.3-contributor`. Export `PI_PROVIDER_FALLBACK_CONFIG` to `.pi/provider-fallback.json`. Preflight: `scripts/loop-runner/run_preflight.sh`. Hypothesizer: Cursor/HTTP GPT-6 Astra (`hypothesize.py`); this pi adapter stays `opencode/claude-fable-5-1:high`. |
| Hyperagent | spawn roles per the capability table above | the `task` tool | map each role to a model the workspace can reach; no `.pi/` files used; run preflight by spawning the judge role directly against `loop/preflight/inputs/` per PROGRAM §2 |
| opencode | judges, trace-analyzer, plan-reviewer, research sub-agents, and (via the opencode harness's own reach) the `task` tool | the `task` sub-agent tool, pinned to `opencode-go/muse-spark-1.3-contributor` for plan-reviewer/trace-analyzer/research (`alibaba-token-plan/deepseek-v4-flash-0731` failed judge repeatability 2026-08-17 — historical note only) | clean-context sub-agent per role call holding only its role prompt + the exact named inputs; no `.pi/` files used; run preflight by spawning the judge role directly against `loop/preflight/inputs/` per PROGRAM §2. Writer/plan-writer/plan-reviewer: primary `opencode-go/muse-spark-1.3-contributor` at `https://opencode.ai/zen/go/v1/responses`; mid-chain Zen `muse-spark-1.3-contributor-free`; last fallback Vercel `meta/muse-spark-1.3-contributor`. |
| Cursor | **Factory:** a Muse Spark 1.3 `factory` / `factory-orchestrator` conversation (OpenCode `opencode run --agent factory` or pi with `.pi/agents/factory-orchestrator.md`). **Auto-research:** this Cursor conversation hypothesizes, applies factory-file changes, starts one factory conversation per subject, then judges (`judge_replicate.py`, composer-2.5). It does **not** itself run plan-writer ↔ plan-reviewer or chapter loops. Hypothesizer: `scripts/loop-runner/hypothesize.py` (GPT-6 Astra via Experiential; Claude Fable 5.1 on quota/no-response). | Cursor `agent` CLI / Task spawn + OpenCode/pi factory session | PROGRAM §2 preflight is spawned directly against `loop/preflight/inputs/` (do not run `run_preflight.sh`). Factory start (one book): `dotenvx run -f .env -- opencode run --dir "$PWD" --agent factory --model opencode-go/muse-spark-1.3-contributor --variant xhigh --auto --title "factory $SLUG" "Read prompts/factory-orchestrator.md. SLUG=$SLUG. Research is on disk. Plan loop then chapter loops until FACTORY DONE."` Start both subjects as two factory sessions (`f$I-$SLUG`). Judge a subject when that factory session prints `FACTORY DONE` (or leftover `write_replicate.py` exits). One judge runner at a time. See `loop/subjects.md`. Writer/plan-writer/chapter-reviewer **inside** the factory conversation: Go `muse-spark-1.3-contributor` → Zen `muse-spark-1.3-contributor-free` → Vercel `meta/muse-spark-1.3-contributor`. **Hypothesizer spawn:** `dotenvx run -f .env -- env ITER=NNN python3 -u scripts/loop-runner/hypothesize.py`. Apply every listed change. Record `hypothesis-metadata.json`. **Conversation robustness:** auto-research may live in this Cursor chat; the factory is a different Muse Spark conversation. Do not make this Grok chat the plan/chapter loop. Thin durability for auto-research: `.cursor/hooks/loop-continue.py` on `stop` / `subagentStop` while `loop/state.md` is `IN PROGRESS`. User `aborted` is a halt. |

## Conversation robustness (factory and research)

The **factory** is a Muse Spark 1.3 agent conversation (`prompts/factory-orchestrator.md`).
The **auto-research loop** is a different conversation (`loop/PROGRAM.md`):
hypothesize, apply, start the factory, judge, KEEP/REVERT. Role runners are
tools a conversation starts; they do not replace it. Do not add a hidden
process driver (`run_factory.py`). Temporal (or similar) is allowed only as
thin durability that resumes the same conversation; `loop/PROGRAM.md`
remains the auto-research sequencer, and `prompts/factory-orchestrator.md`
remains the factory sequencer.

**pi (this repo's 0.84.x binding):** `npm:pi-goal-x` (peers `>=0.83 <0.85`).
`/goal-direct` and `/sisyphus-direct` create a focused goal with autoContinue
on; continuation queues on `agent_settled` (after retries and compaction), not
`agent_end`. Goals persist under `.pi/goals/`. Resume a killed process with
`pi --resume <session.jsonl>`.

```bash
export PI_PROVIDER_FALLBACK_CONFIG="$(pwd)/.pi/provider-fallback.json"
pi
```

- Factory (one book: plan loop then chapter loops): a Muse Spark 1.3 session
  with `prompts/factory-orchestrator.md` (OpenCode `--agent factory`, or pi
  `.pi/agents/factory-orchestrator.md` + `/sisyphus-direct`). Spawn each role
  as a fresh sub-agent; wait for that unit's on-disk marker; then the next
  unit. Do not exit while the book is unfinished.
- Auto-research (PROGRAM iteration: hypothesize → factory → judge → KEEP):
  `/sisyphus-direct` on `loop/PROGRAM.md`. That conversation starts factory
  sessions; it does not itself write chapters.
- Research (open-ended until artifacts exist): `/goal-direct` — execute
  `prompts/research-agent.md` as research lead. Spawn `.pi/agents/researcher.md`
  miners in parallel; no search/fetch ceilings; stop only when the accepted
  research artifacts the runbook names are on disk.

Do not use `@latent-variable/pi-auto-continue` (`agent_end`, naive "continue").
Do not use timer `/loop` extensions. `npm:pi-agent-goal` is the same
conversation-goal design but peer-blocked on pi ≥0.81 (`<0.81` ceiling).
Fallback if `pi-goal-x` cannot load: `npm:@narumitw/pi-goal` (also
`agent_settled`).

**Cursor:** auto-research may live in this conversation. The factory is a
Muse Spark 1.3 session — start it, wait for `FACTORY DONE`, then judge.
Do not run plan/chapter loops here. Start each factory session in its own
tmux session (`f$I-$SLUG`). `$W` = iteration worktree, `$I` = NNN:

```bash
tmux new -d -s f$I-$SLUG "cd $W && dotenvx run -f .env -- opencode run --dir $W \
  --agent factory --model opencode-go/muse-spark-1.3-contributor --variant xhigh --auto \
  --title factory-$I-$SLUG \
  \"Read prompts/factory-orchestrator.md. SLUG=$SLUG ITER=$I REPLICATE=a. Research is on disk. Plan loop then chapter loops until FACTORY DONE.\" \
  >> loop/iterations/$I/factory-$SLUG.log 2>&1"
pid=$(tmux list-panes -t "f$I-$SLUG" -F '#{pane_pid}' 2>/dev/null)
[ -n "$pid" ] && tail --pid="$pid" -f /dev/null
```

Same wait pattern for `judge_replicate.py` (`j$I-$SLUG`). `tail --pid` blocks
until that shell exits. No sleep loop. Do not use `tmux wait-for`. Thin
durability for auto-research: `.cursor/hooks/loop-continue.py` on `stop`
and `subagentStop` re-enters this conversation while `loop/state.md` is
`IN PROGRESS` (skip `aborted`). It must **not** tell this chat to write
chapters. The founder can walk away; a user abort still halts.

**Preflight is harness-coupled:** judge repeatability depends on the model and
sampling, so re-run preflight when the *harness or model* changes, not only
when a judge prompt changes.
