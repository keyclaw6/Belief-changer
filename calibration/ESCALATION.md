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

### Controlled causal check

To test whether requesting the catalog maximum itself caused a false rejection, the operator repeated the complete Chapter 1 request with everything held fixed except `max_tokens`, reduced from 128,000 to 8,000—still well above the 2,800-word chapter target. OpenRouter returned the same HTTP 402 and the same 147-token affordability ceiling. This refutes reservation size as the operative cause. The authenticated key is valid, but account funding is the binding cause; changing the key's separate internal spending limit cannot create account credit.

`LITELLM_BASE_URL` and `LITELLM_API_KEY` are absent in the runtime. An initial name-only environment check falsely reported `ANTHROPIC_API_KEY` as present; a non-empty check proved that it is defined but empty, and the direct API correctly returned an authentication error. Claude Code 2.1.146 reports an existing Claude Pro login and accepts the exact `--model claude-opus-4-6 --thinking disabled` controls, but a live zero-cost connectivity call returned 401 because the stored OAuth credential is stale. Reauthentication now requires the user's browser approval.

## Founder action required

Provide one of:

1. usable OpenRouter account credit or a replacement OpenRouter key;
2. the founder LiteLLM base URL and `belief-changer` virtual key via environment variables; or
3. refresh the existing Claude Pro login in the browser and authorize its Claude Code route for the fixed Opus 4.6 thinking-disabled baseline, with provider provenance recorded in run-002.

On resolution, resume the unchanged Chapter 1 request. Do not regenerate research, framing, or the accepted plan; do not substitute Muse or another writer for the Opus baseline.
