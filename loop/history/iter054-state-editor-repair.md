# Iteration 054 runtime repair — state-editor target identity

## Incident

The first live 054 baseline attempt, `iter054-sugar-a`, successfully proved startup: the saved top-level Pi session existed, OpenCode Go was active, real Muse Spark 1.3 and DeepSeek V4.1 Flash calls returned the expected metadata, and durable factory results advanced through chapter 2 review.

The run then stopped at `state-editor-ch02-r01`. Four bounded attempts returned the same validation fingerprint:

`State belongs to another chapter`

No chapter-2 state result was accepted or written. The partial run is preserved as diagnostic evidence and is excluded from the 054 baseline sample.

## Root cause

`prompts/reader-state.md` hardcoded `"chapter_id":"chapter-01"` in the output example while later-chapter state tasks did not expose a separate authoritative target ID. Muse repeatedly copied the example instead of the actual chapter-2 identity.

## Mechanical repair

- `scripts/bc_factory/runs.py` now freezes `inputs.target_chapter_id` for every state-editor task.
- `prompts/reader-state.md` now requires copying that exact input verbatim and no longer contains a hardcoded chapter-01 output example.
- `scripts/eval/tests/test_v2.py` adds a non-first-chapter regression test proving chapter 2 receives and exposes the correct target ID.

This is a deterministic runtime-identity repair, not a writing-system intervention or evidence/judge change. Generator/evaluator models, routes, research inputs, and the 054 hypothesis are unchanged.

## Validation and continuation

- focused regression: PASS;
- mandatory `bash scripts/check.sh`: PASS;
- failed run preserved: `iter054-sugar-a`;
- replacement counted replicate: `iter054-sugar-a-r1`;
- the same saved Pi session `363bee36-1634-4d2d-8aef-ef9fedf074e8` must be resumed; no replacement worker;
- heartbeat remains disabled until the successor run again proves a successful real model response plus durable factory advancement.
## Successor startup proof

The mechanical repair was committed and pushed as `c05a8be3`. The exact saved Pi session `363bee36-1634-4d2d-8aef-ef9fedf074e8` was resumed from its dedicated `pi-runtime` session store; no replacement top-level session was created.

Replacement counted run `iter054-sugar-a-r1` was prepared from the same quit-sugar brief/research and the fresh READY preflight. Its first real result is `evidence-reviewer-r01`: `ACCEPT`, zero findings, metadata `deepseek-v4.1-flash` / `deepseek` / `opencode-go-deepseek-v4.1-flash` / `http-v2`. This re-proved a successful live model response plus durable factory advancement after the repair.

The hourly watchdog was re-enabled only after that proof.

