# `.pi/agents/` — the pi-harness adapter

These files are the **pi coding agent's adapter** for the auto-research loop's
roles. They are harness-specific plumbing, not the loop's definition.

- The **harness-neutral source of truth** for each role is its contract prompt
  under `prompts/`, `loop/prompts/`, or `loop/judges/`, plus the runbook
  `loop/PROGRAM.md`.
- Each file here is a thin pi wrapper: it points at that contract prompt and
  pins a model (the frontmatter `model:`), which is pi's spawn-time binding for
  the role.
- Under a different harness, the same contract prompts are spawned directly by
  that harness's own spawn capability; these `.pi/` files are not used.

See `loop/HARNESS.md` for the role→capability map, the spawn contract, and how
model precedence (config vs this adapter) is resolved.
