# Preflight — Judge Calibration Battery (campaign-001)

Date: 2026-08-07. Judge model per config: gpt-5.6-luna, reasoning high,
through the Command Code proxy (founder route change 2026-08-07). Raw traces
in `loop/preflight/runs/` (request.json with Authorization REDACTED,
response.sse, response.md, metadata.json). Inputs in `loop/preflight/inputs/`.
The Sol-era battery (2026-07-28) is archived at
`loop/preflight/runs-2026-07-sol-era/`.

## Overall: PASS

| Check | Result |
|---|---|
| 1. PASS test (real GSBS ch-02 as both texts, 2x per judge) | **PASS** — 6/6 runs returned PASS |
| 2. Repeatability (identical generated chapter, identical context, 2x per judge) | **PASS** — belief-mechanic PASS/PASS, reader-journey PASS/PASS, voice-emotion FAIL/FAIL with byte-identical per-moment verdict blocks (founder amendment 2026-07-28 option C satisfied) |
| 3. Voice honesty probe (6 passage pairs) | **PASS** — both hedged core-verdict probes flagged; both bounded empirical claims and both reader-present-doubt acknowledgments not flagged |

## Notes

- voice-emotion legitimately FAILs the repeatability article (run-012
  generated ch-01): the assigned instruction moment reads as
  instruction-register/compliance paperwork. Both runs flag the identical
  moment and failure class.
- Judge calls ran ~5-12s each through the proxy; no rate limiting observed
  on gpt-5.6-luna.
