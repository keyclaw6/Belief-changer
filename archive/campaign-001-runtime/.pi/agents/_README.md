These files are the **pi coding agent's adapter** for factory roles and the
auto-research loop. They are harness-specific plumbing, not the loop's
definition.

- The **harness-neutral source of truth** for each role is its contract prompt
  under `prompts/`, `loop/prompts/`, or `loop/judges/`. The factory sequencer
  is `prompts/factory-orchestrator.md`. The auto-research runbook is
  `loop/PROGRAM.md`.
- Each file here is a thin pi wrapper: it points at that contract prompt and
  pins a model (the frontmatter `model:`), which is pi's spawn-time binding for
  the role. Muse Spark roles pin
  `opencode-go/muse-spark-1.3-contributor`. Per-call fallback to Vercel
  `vercel/meta/muse-spark-1.3-contributor` is `.pi/provider-fallback.json`
  (extension `pi-provider-fallback` in `.pi/settings.json`) plus PROGRAM §1.
  Pi reads that JSON only when `PI_PROVIDER_FALLBACK_CONFIG` points at it
  (otherwise it looks in `~/.pi/agent/extensions/provider-fallback.json`).
  Empty `opencode.fallbacks` is required: the plugin looks up same-provider
  IDs first; the Vercel model lives under `vercel`, so it must be enabled
  there for cross-provider failover.
- Under a different harness, the same contract prompts are spawned directly by
  that harness's own spawn capability; these `.pi/` files are not used.

See `loop/HARNESS.md` for the role→capability map, the spawn contract, and how
model precedence (config vs this adapter) is resolved.

Conversation robustness for the **factory orchestrator** is a Muse Spark 1.3
session (`factory-orchestrator.md`, OpenCode `--agent factory`, or
`/sisyphus-direct` on that prompt). Auto-research (`loop/PROGRAM.md`) is a
separate conversation. Do not put a continue-loop into `prompts/` or these
role files.
