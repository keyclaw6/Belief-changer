# HANDOFF — campaign-001 operator transfer (2026-07-29)

The auto-tuning loop's operator role moves from the Hyperagent sandbox to a
founder-controlled VPS. Git is the state machine; this file plus §0 Recovery
of `loop/PROGRAM.md` is everything a fresh operator needs.

**Update 2026-08-07:** the founder runs the loop from their main machine;
every provider call routes through the Command Code proxy loopback (see
Routes below). No OpenRouter or OpenAI OAuth credential is needed anymore.

## Why the transfer

The previous environment's egress proxy had per-session network entitlement
(detached processes randomly lose all network), cut long HTTP responses, and
had unstable credential tooling. All worked around (see Hard-won lessons),
but a stable machine removes the whole failure class.

## Exact position

- **Preflight: recalibration REQUIRED (2026-08-07).** The judge role moved to
  `gpt-5.6-luna` (reasoning high) through the Command Code proxy. The
  Sol-era battery is archived at `loop/preflight/runs-2026-07-sol-era/`.
  Run `scripts/loop-runner/run_preflight.sh` fresh and confirm PASS before
  trusting any campaign verdict. (The old `results.md` records the Sol era.)
- **Baseline 000, Stage: Research, round 1: 7/12 commissions complete.**
  - Lead plan + parameter block: `production-books/quit-sugar/research/_rounds/round-1/lead/response.md`
  - Commissions: `_rounds/round-1/commissions/K-01..K-12.md`
  - DONE: K-01..K-05 (DeepSeek era), K-06, K-07 (MiniMax era) —
    `_rounds/round-1/subagents/K-NN/response.md`
  - MISSING: K-08..K-12 (K-08/K-09 died to a network-entitlement loss;
    no checkpoints — they restart from their commissions)
- Framing and master-plan artifacts exist on disk, but their reviews are not
  clean — a fresh operator re-runs those stages' gates per PROGRAM §3.
- **Next actions, in order:**
  1. `bash scripts/loop-runner/run_preflight.sh` (judge recalibration on
     Luna high — 18 calls through the Command Code proxy)
  2. Run the research stage per PROGRAM §3: the orchestrator (pi) resumes
     from the round-1 packets already on disk (the K-01..K-12 commissions
     and subagent results are seed material), then relentlessly searches
     and spawns `researcher` sub-agents until the completion criterion in
     `prompts/research-agent.md` clears across at least three personas.
  3. Synthesis into `production-books/quit-sugar/research/` per
     `prompts/research-agent.md` §9, then the independent evidence editor
     gate (§10) — the `evidence-editor` sub-agent, `ACCEPTED FOR FRAMING`
     required.
  4. Then PROGRAM §3 continues: framing → plan → reference-alignment →
     plan cards → chapters → validity gates → judges → trace analysis →
     A/A check → BASELINE row. Commit after every stage on campaign-001.

## Routes (loop/config.yaml is the SOLE authority)

- Every role is a spawned pi sub-agent (`.pi/agents/*.md`, `subagent` tool),
  a thin wrapper over its contract prompt in `prompts/` or `loop/prompts/`,
  with the model pinned per `loop/config.yaml`:
  - `researcher` — `MiniMaxAI/MiniMax-M3`; search/fetch via
    `scripts/loop-runner/web_tools.py`.
  - `framing`, `framing-reviewer`, `evidence-editor`, `judge`,
    `trace-analyzer`, `hypothesizer`, `plan-reviewer` — `gpt-5.6-luna`.
  - `plan-writer` — `moonshotai/Kimi-K3`.
  - `chapter-writer` — `meta/muse-spark-1.2-contributor`.

Route change 2026-08-07 (founder): writer, research, and planner all run
through the founder's Command Code proxy loopback, and so do all GPT roles;
no fallback route is coded. Auth for every role is `COMMANDCODE_API_KEY`,
or the Command Code CLI login (`~/.commandcode/auth.json`) when the env var
is absent. Use dotenvx per AGENTS.md; never commit values.
On any Command Code route failure (missing credential, proxy down, model
not listed or not in plan — HTTP 401): STOP and escalate to the founder —
there is no fallback route.

## The harness (scripts/loop-runner/)

All machine-independent (BC_REPO env var or auto-detected from script
location; scratch state under `.loop-work/`, gitignored):

- `web_tools.py` — search/fetch primitives for the research orchestrator and
  sub-agents (`python3 scripts/loop-runner/web_tools.py search|fetch`).

**One-time pi setup (sub-agents):**
1. Copy the subagent extension from the installed pi package into
   `~/.pi/agent/extensions/subagent/` (`examples/extensions/subagent/index.ts`
   + `agents.ts`) and raise the caps to `MAX_PARALLEL_TASKS = 10` and
   `MAX_CONCURRENCY = 10` (founder decision 2026-08-08 — the orchestrator may
   spawn ten sub-agents at a time).
2. Symlink every repo agent into the user agent scope (the extension's
   default agent scope is `user`, so project-local discovery alone is not
   enough):
   `for f in .pi/agents/*.md; do ln -sf "$PWD/$f" ~/.pi/agent/agents/$(basename "$f"); done`
The repo's `.pi/agents/*.md` files stay canonical; the symlinks follow them.
- `run_preflight.sh` — the §2 judge battery (re-run only after judge edits).
- `queue_runner.sh` + `daemon.sh` — file-queue job runner (jobs in
  `.loop-work/queue/pending/*.job`); useful on the VPS for detached
  operation but optional — plain foreground runs are fine on a stable box.

## Hard-won lessons (encoded in the harness — do not undo)

1. **Always stream.** Non-streamed long responses were cut at ~4 min by the
   old proxy, while the upstream billed the full run ($8 lost). Streaming
   is on everywhere; keep it.
2. **Custom User-Agent required** — Cloudflare bans default Python UA
   (error 1010) on opencode.ai. `loop-runner/1.0` is set everywhere.
3. **Checkpoint everything long.** Research sub-agents write every packet to
   the bank files as they go; a lost sub-agent loses at most its current
   task, never the accumulated research.
4. **Retries must never re-bill doomed work**: distinguish operator-side
   network failures (patient waits, no retry budget) from API failures
   (3x 30/60/120s per PROGRAM).
5. **Judges are calibrated; leave them alone.** Any suspected judge defect
   stops the campaign for the founder (PROGRAM §5), full stop.

## Constitution reminders (read before acting)

Read in order: `AGENTS.md` → `docs/BOOK-FACTORY-VISION.md` →
`docs/AUTO-TUNING-LOOP.md` → `loop/PROGRAM.md` → `loop/config.yaml`.
Research depth is sacred and unlimited. One causal change per iteration.
Evidence decides KEEP/REVERT. One commit per iteration on campaign-001.
Only the founder merges to main.
