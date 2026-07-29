# HANDOFF — campaign-001 operator transfer (2026-07-29)

The auto-tuning loop's operator role moves from the Hyperagent sandbox to a
founder-controlled VPS. Git is the state machine; this file plus §0 Recovery
of `loop/PROGRAM.md` is everything a fresh operator needs.

## Why the transfer

The previous environment's egress proxy had per-session network entitlement
(detached processes randomly lose all network), cut long HTTP responses, and
had unstable credential tooling. All worked around (see Hard-won lessons),
but a stable machine removes the whole failure class.

## Exact position

- **Preflight: PASS** (`loop/preflight/results.md`, runs8 + battery traces).
  Judges are calibrated and repeatable; do not edit them (founder-guided only).
- **Baseline 000, Stage: Research, round 1: 7/12 commissions complete.**
  - Lead plan + parameter block: `production-books/quit-sugar/research/_rounds/round-1/lead/response.md`
  - Commissions: `_rounds/round-1/commissions/K-01..K-12.md`
  - DONE: K-01..K-05 (DeepSeek era), K-06, K-07 (MiniMax era) —
    `_rounds/round-1/subagents/K-NN/response.md`
  - MISSING: K-08..K-12 (K-08/K-09 died to a network-entitlement loss;
    no checkpoints — they restart from their commissions)
- **Next actions, in order:**
  1. `python3 scripts/loop-runner/research_round.py --round 1`
     (skips done commissions, runs the 5 missing ones, batches of 4)
  2. `python3 scripts/loop-runner/research_round.py --round 2`
     (lead integrates all 12 results → gap-fill commissions or
     `SYNTHESIZE READY`; iterate rounds until ready)
  3. Synthesis into `production-books/quit-sugar/research/` per
     `prompts/research-agent.md` §9, then the independent evidence editor
     gate (§10) — a fresh GPT role call, `ACCEPTED FOR FRAMING` required.
  4. Then PROGRAM §3 continues: framing → plan → reference-alignment →
     commissions → chapters → validity gates → judges → trace analysis →
     A/A check → BASELINE row. Commit after every stage on campaign-001.

## Routes (loop/config.yaml is the SOLE authority)

- GPT roles (framing/commissioner/judges/analyzer/hypothesizer/evidence
  editor/plan reviewer): Codex backend Responses endpoint, streaming,
  `OPENAI_OAUTH_TOKEN` (+ chatgpt-account-id decoded from its JWT —
  `scripts/loop-runner/gpt_role_call.py` does everything).
- Research: `minimax-m3` via opencode Go chat completions
  (`OPENCODE_GO_API_KEY`) with ORCHESTRATOR-EXECUTED web tools —
  `scripts/loop-runner/research_toolloop_call.py` (founder route switch
  2026-07-29; the Go gateway has no native web tools).
- Planner: `kimi-k3` via opencode Go — `scripts/loop-runner/opencode_call.py`.
- Writer: Muse Spark 1.1 via OpenRouter (`OPENROUTER_API_KEY`) —
  `scripts/loop-runner/openrouter_call.py --role writer`. NOTE: the
  OpenRouter key sits at $8.73 of a $10 limit — raise it before the
  writing stage (20 chapters) or writer calls will be refused.

Required env vars: `OPENAI_OAUTH_TOKEN`, `OPENROUTER_API_KEY`,
`OPENCODE_GO_API_KEY`. Use dotenvx per AGENTS.md; never commit values.
On any OpenAI 401: STOP and ask the founder to refresh the token.

## The harness (scripts/loop-runner/)

All machine-independent (BC_REPO env var or auto-detected from script
location; scratch state under `.loop-work/`, gitignored):

- `gpt_role_call.py` — one fresh clean GPT role call; saves request
  (auth REDACTED), SSE, response.md, metadata.
- `research_toolloop_call.py` — MiniMax research with local
  web_search/web_fetch (DuckDuckGo + GET), **checkpoint.json after every
  tool round** — kill/restart loses at most one round. Unlimited depth.
- `research_round.py` — one research round: lead → parse `=== COMMISSION
  K-NN ===` fences → run each as a fresh subagent call (skip-done,
  RESEARCH_MAX_PARALLEL=4, 15s stagger).
- `opencode_call.py`, `openrouter_call.py` — planner / writer transports.
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
3. **OpenRouter Responses API requires `store: false`.**
4. **Checkpoint everything long.** research_toolloop persists transcript
   per round; resume is automatic from `checkpoint.json`.
5. **Retries must never re-bill doomed work**: distinguish operator-side
   network failures (patient waits, no retry budget) from API failures
   (3x 30/60/120s per PROGRAM).
6. **Judges are calibrated; leave them alone.** Any suspected judge defect
   stops the campaign for the founder (PROGRAM §5), full stop.

## Constitution reminders (read before acting)

Read in order: `AGENTS.md` → `docs/BOOK-FACTORY-VISION.md` →
`docs/AUTO-TUNING-LOOP.md` → `loop/PROGRAM.md` → `loop/config.yaml`.
Research depth is sacred and unlimited. One causal change per iteration.
Evidence decides KEEP/REVERT. One commit per iteration on campaign-001.
Only the founder merges to main.
