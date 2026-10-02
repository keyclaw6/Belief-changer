# Reusable Pi book factory

One saved top-level Pi `factory-orchestrator` owns a logical book. It loads the
research contract when researching, then calls the frozen CLI's semantic role
executors directly. Those executors isolate each role's inputs, use the configured
model family and validate actual outputs. Evidence and final reviews use the
independent external profile.

There are no intermediate Pi stage controllers or subagent extension. Role
judgment remains in `prompts/`; factory mechanics remain in `scripts/bc_factory/`.
The factory returns at verified `COMPLETE_UNRELEASED`. Outer autoresearch lives
under `loop/` and `scripts/bc_autoresearch/`, outside this runtime.
