# Tasks

- [x] 1. Verify proxy reachability and model list with the founder's Command Code token (2026-08-07: health OK, 52 models listed).
- [x] 2. Smoke-test free/cheap models through the proxy (`poolside/laguna-s-2.1-free`, `deepseek/deepseek-v4-flash`).
- [x] 3. Rewire `loop/config.yaml` and the loop-runner transports; delete the OpenRouter research fallback.
- [x] 4. Update route-law text: AGENTS.md, docs/VISION.md, loop/PROGRAM.md, loop/HANDOFF.md.
- [x] 5. Prove the rewired transports live through the proxy (writer, planner, research tool loop).
- [x] 6. Move the GPT roles (judge battery included) to the proxy on `gpt-5.6-luna`; prove a judge call live.
- [x] 7. `bash scripts/check.sh` green.
