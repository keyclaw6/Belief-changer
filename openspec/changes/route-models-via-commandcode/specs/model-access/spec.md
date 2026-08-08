# model-access spec

## ADDED Requirements

### Requirement: Single founder-approved model route
Every factory provider model call — writer, research, planner, and all GPT
roles (judging, trace analysis, hypothesizing, framing, evidence editing,
plan review) — SHALL route only through the founder-
approved Command Code proxy loopback, authenticated with the founder's
Command Code credential supplied via `COMMANDCODE_API_KEY` or the Command
Code CLI login. Role calls carry only the role prompt and listed inputs.
No fallback provider route SHALL exist in code.

#### Scenario: Credential or proxy unavailable
WHEN the Command Code credential is missing, the proxy is unreachable, or the
required model is absent from the proxy model list
THEN the run MUST stop before any content call
AND the executor MUST report to the founder instead of switching providers.
