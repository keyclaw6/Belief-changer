# Proposal: route-models-via-commandcode

## Why
Founder route change 2026-08-07: the OpenRouter credential is exhausted/dead
and model access moves to the founder's Command Code proxy
(MAXeaglet/commandcode-proxy) loopback, authenticated with the founder's
Command Code credential. One route, no coded fallback: on credential or proxy
failure the executor stops and calls the founder.

## What Changes
- `loop/config.yaml` (sole route authority): writer, research, and planner
  endpoints move to the Command Code proxy; model ids move to the proxy's
  listed ids that the founder's plan covers (`meta/muse-spark-1.2-contributor`
  per founder choice, `MiniMaxAI/MiniMax-M3`, `moonshotai/Kimi-K3`); auth env is
  `COMMANDCODE_API_KEY` with the Command
  Code CLI login (`~/.commandcode/auth.json`) when the env var is absent.
- The GPT roles (judges, analyzer, hypothesizer, framing, evidence editor,
  plan reviewer) move from the OpenAI subscription OAuth
  Responses endpoint to the same proxy as chat completions. Only
  `gpt-5.6-luna` is in the founder's plan (verified 2026-08-07; Sol/Terra
  and all other GPT ids return MODEL_NOT_IN_PLAN), so every role starts on
  Luna; reasoning `xhigh` maps to the proxy's `max`.
- Transports: `openrouter_call.py` → `writer_call.py` (writer-only; the
  Responses-API research branch is deleted), `opencode_call.py` →
  `planner_call.py`; `research_toolloop_call.py` keeps its tool loop. The
  OpenRouter fallback branch in `research_round.py` is deleted.
- `gpt_role_call.py` switches from the Codex-backend Responses API to chat
  completions; the JWT account-id machinery is deleted.
- Route law text updated in AGENTS.md, docs/VISION.md, loop/PROGRAM.md, and
  loop/HANDOFF.md.

## Impact
- Affected specs: `model-access` (new capability).
- Affected code: `scripts/loop-runner/*`, `loop/config.yaml`.
- Verified live 2026-08-07: proxy health OK, 52 models listed, free/cheap
  model smoke tests and writer/researcher/planner payload shapes pass.
- Judge model change (Sol → Luna) is a judge edit: the §2 preflight battery
  must be re-run before campaign verdicts trust the new judges.
