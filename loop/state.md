# Current operational state — v2

- **Status:** REPAIR READY — iteration 054 is active; the first partial run `iter054-sugar-a` is excluded after a deterministic state-editor identity failure.
- **Legacy campaign:** campaign-001, completed through 050; preserved without rewriting results.
- **Iteration 053:** aborted before the first successful factory model response; it does not count as completed.
- **Iteration 054:** fresh replacement v2 repeatability baseline is preregistered in `loop/iterations/054/hypothesis.md`.
- **Current repair:** `iter054-sugar-a` reached validated chapter-2 review, then `state-editor-ch02-r01` failed four times with `State belongs to another chapter`. Root cause and validated repair are recorded in `loop/history/iter054-state-editor-repair.md`. The partial run is diagnostic only and does not count toward the 054 sample.
- **Next counted run:** `iter054-sugar-a-r1`, using the repaired factory while preserving the same saved top-level Pi session.
- **Pi session:** `363bee36-1634-4d2d-8aef-ef9fedf074e8`; resume this session, do not create a replacement worker.
- **Worker invariant:** one persistent top-level Pi Coding Agent per active book.
- **Model-provider invariant:** OpenCode Go only. Generator: `muse-spark-1.3-contributor`, family `meta`, route `opencode-go`. Independent evaluator: `deepseek-v4.1-flash`, family `deepseek`, route `opencode-go-deepseek-v4.1-flash`.
- **Champion:** `factory/champion.json`; no validated v2 release.
- **Calibration:** pending actual human ratings for the configured DeepSeek evaluation instrument.
- **Heartbeat:** temporarily disabled during the runtime repair. Re-enable only after `iter054-sugar-a-r1` again demonstrates a successful real model response and durable factory advancement.
- **Effectiveness:** not established by software tests, model judgments, or this exploratory campaign.
