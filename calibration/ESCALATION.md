# Calibration escalation — run-002 writer endpoint

**Date:** 2026-07-11

**Run:** `calibration/runs/run-002/`

**Branch:** `calibration-lab`

## Completed before the block

Run-002's normalized R3 master plan passed its final fresh review with `fit to write from`. The accepted plan and all three candidate/review pairs are committed in `5915b9f`.

## Blocking condition

The first real Chapter 1 request used the authenticated OpenRouter route `anthropic/claude-opus-4.6`, `reasoning.effort: none`, and the model's catalog maximum `max_tokens: 128000`. OpenRouter rejected it before generation with HTTP 402. No chapter text or provider generation metadata was produced.

The authenticated credit endpoint reports:

- total credits: `$75.00`
- total usage: `$75.181592239`

The key-detail endpoint's `$10` per-key limit and `$1.806546899` key usage are not account credit; its apparent `$8.193453101` remainder did not authorize the request. The 402 response calculated only 147 affordable completion tokens after input, which cannot produce the 2,800-word chapter and is not a quality-valid fallback.

`LITELLM_BASE_URL` and `LITELLM_API_KEY` are absent in the runtime. A separate `ANTHROPIC_API_KEY` is present, but it was not used: direct Anthropic is not one of the two model routes authorized by `AGENTS.md`/HARNESS §2, and the founder specifically supplied the disposable OpenRouter key for calibration.

## Founder action required

Provide one of:

1. usable OpenRouter account credit or a replacement OpenRouter key;
2. the founder LiteLLM base URL and `belief-changer` virtual key via environment variables; or
3. explicit authorization to use the existing direct Anthropic environment credential for the fixed Opus 4.6 reasoning-none baseline, with provider provenance recorded in run-002.

On resolution, resume the unchanged Chapter 1 request. Do not regenerate research, framing, or the accepted plan; do not substitute Muse or another writer for the Opus baseline.
