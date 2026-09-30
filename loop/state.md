# Current operational state — v2

- **Status:** ACTIVE — iteration 054 replacement v2 repeatability baseline is running.
- **Legacy campaign:** campaign-001, completed through 050; preserved without rewriting results.
- **Iteration 053:** aborted before the first successful factory model response; it does not count as completed.
- **Iteration 054:** preregistered in `loop/iterations/054/hypothesis.md`; no writing-system intervention is active.
- **Excluded partial run:** `iter054-sugar-a` is preserved as diagnostic evidence only. It reached validated chapter-2 review, then stopped after the deterministic state-editor chapter-ID defect repeated. Root cause and repair are recorded in `loop/history/iter054-state-editor-repair.md`.
- **Current counted run:** `iter054-sugar-a-r1`, using repaired commit `c05a8be3`. Startup re-proof succeeded: the first independent evidence review returned `ACCEPT` with zero findings and exact DeepSeek/OpenCode-Go metadata.
- **Pi session:** `363bee36-1634-4d2d-8aef-ef9fedf074e8`; this same saved top-level Pi session is active and must be preserved.
- **Worker invariant:** one persistent top-level Pi Coding Agent per active book.
- **Model-provider invariant:** OpenCode Go only. Generator: `muse-spark-1.3-contributor`, family `meta`, route `opencode-go`. Independent evaluator: `deepseek-v4.1-flash`, family `deepseek`, route `opencode-go-deepseek-v4.1-flash`.
- **Champion:** `factory/champion.json`; no validated v2 release.
- **Calibration:** pending actual human ratings for the configured DeepSeek evaluation instrument.
- **Heartbeat:** enabled hourly as a watchdog after the repaired successor re-proved a successful live model response plus durable factory advancement. It must leave healthy Pi progress alone and repair only evidence-backed blockers under `skills/running-auto-research-loop/SKILL.md`.
- **Next action:** allow the current Pi factory call to continue to verified `COMPLETE_UNRELEASED`; then freeze the required outer autoresearch judgment/decision/learning boundary before starting the next replicate.
- **Effectiveness:** not established by software tests, model judgments, or this exploratory campaign.
