# model-access spec

## ADDED Requirements

### Requirement: Single founder-approved model route
Factory provider model calls (writer, research, planner) SHALL route only
through the founder-approved Command Code proxy loopback, authenticated with
the founder's Command Code credential supplied via `COMMANDCODE_API_KEY` or
the Command Code CLI login. GPT roles run as fresh clean calls on the OpenAI
subscription OAuth route and NEVER through the proxy. No fallback provider
route SHALL exist in code.

#### Scenario: Credential or proxy unavailable
WHEN the Command Code credential is missing, the proxy is unreachable, or the
required model is absent from the proxy model list
THEN the run MUST stop before any content call
AND the executor MUST report to the founder instead of switching providers.
