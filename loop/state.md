# Current operational state — v2

- **Status:** STOPPED — iteration 053 aborted before the first successful factory model response.
- **Legacy campaign:** campaign-001, completed through 050; preserved without rewriting results.
- **Aborted campaign attempt:** the authorized 053–057 campaign was stopped by the owner after 053 failed at startup. 053 is not a completed iteration and 054–057 were never started.
- **Active architecture:** truth-first factory v2.
- **Worker invariant:** one persistent top-level Pi Coding Agent per requested book.
- **Model-provider invariant:** OpenCode Go only. No OpenCode Zen, Vercel, ChatGPT, OpenCodex/OpenCode-CLI worker, or alternate-provider fallback.
- **Champion:** factory/champion.json; no validated v2 release at migration.
- **Evaluator:** DeepSeek V4.1 Flash (`deepseek-v4.1-flash`) through OpenCode Go, family `deepseek`, using the same `OPENCODE_GO_API_KEY` as the factory. This is independent from the Meta/Muse generator family.
- **Calibration:** pending actual human ratings for the configured DeepSeek V4.1 Flash evaluation instrument.
- **Heartbeat:** disabled. Before any future autoresearch campaign or recurring schedule, read `skills/running-auto-research-loop/SKILL.md` and prove a successful Pi/OpenCode-Go model response plus durable state advancement before arming the heartbeat.
- **Next action:** none until separately authorized. Preserve the 053 preregistration and abort record as historical evidence.
- **Effectiveness:** not established by software tests, model judgments, or the aborted optimization campaign.
