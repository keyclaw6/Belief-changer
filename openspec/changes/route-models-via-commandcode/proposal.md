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
  listed ids that the founder's plan covers (`deepseek/deepseek-v4-pro`,
  `MiniMaxAI/MiniMax-M3`, `moonshotai/Kimi-K3`); auth env is
  `COMMANDCODE_API_KEY` with the Command
  Code CLI login (`~/.commandcode/auth.json`) when the env var is absent.
- Transports: `openrouter_call.py` → `writer_call.py` (writer-only; the
  Responses-API research branch is deleted), `opencode_call.py` →
  `planner_call.py`; `research_toolloop_call.py` keeps its tool loop. The
  OpenRouter fallback branch in `research_round.py` is deleted.
- GPT roles stay on the OpenAI subscription OAuth route, unchanged.
- Route law text updated in AGENTS.md, docs/VISION.md, loop/PROGRAM.md, and
  loop/HANDOFF.md.

## Impact
- Affected specs: `model-access` (new capability).
- Affected code: `scripts/loop-runner/*`, `loop/config.yaml`.
- Verified live 2026-08-07: proxy health OK, 52 models listed, free/cheap
  model smoke tests and writer/researcher/planner payload shapes pass.
