# Local deployment and recovery

Normal commands and outer ownership are in
`skills/running-auto-research-loop/SKILL.md`. The installed native durable
controller owns the outer process service; no watchdog or second scheduler drives
normal progress. Its receipt and session survive the originating client. A genuine
crash still requires explicit resume of that same job after outcome reconciliation.

## Provisioned host

The entrypoint discovers paths into ignored `.loop-work/deployment.json`. This
host's concrete Pi is `/home/kab/.local/share/mise/installs/pi/0.99.2/pi/pi`, private
agent directory `/home/kab/.local/share/belief-changer/pi-runtime`, credential file
`/home/kab/.config/belief-changer-go.env`, and native controller
`/home/kab/.local/bin/opencode-rdc`. These are repairable deployment values, not
scientific authority. The controller imports its owner-only env file without
printing values. Do not use the Pi shim that changes global mise configuration.
`ocx provider quota --json` observes available provider quotas; unknown dollar or
usage values remain unknown. No purchases or paid-overage configuration changes.

## Resume the logical work

`progress.json` retains per-iteration scope, exact source quotation and frozen
hypothesis/allocation digest. APPROVED is an operator assertion checked against the
actual human source, never consent created by a hash. Campaign state holds only
its fixed boundary, stop intent and validated checkpoint pointers. An owner stop
is persisted before the native controller cancels its owned service/descendants.
A completed campaign cannot start another cycle.

Pi's launcher uses a real PTY and one native history under `.loop-work/pi/` per
logical book. Initial research inputs/source are frozen before inference. The
preparation-to-run handoff checks exact source/brief/context identity. Research or
remediation manifest links preserve one book slot/session, including previous
independent findings. Independent books never inherit each other's conversations.
The launcher automatically resumes each selected snapshot. Native Pi restores
header `cwd`, so the locked launcher retains the old header in its local log and
rebinds only that field; transcript bytes remain unchanged.

Kernel ownership fences the live Pi parent. Direct semantic HTTP stages also hold
the existing task execution lock; a surviving stage prevents a duplicate launch.
Inspect the actual owner/result before reconciling an orphan lock. Never remove a
live lock or assume that a missing receipt means no model request occurred. Saved
raw responses and accepted results replay by exact task/config identity. Missing
remote responses remain unknown; an explicit new attempt retains earlier receipts.

For pre-launcher or damaged native sessions, prove the owner is idle, preserve the
original, recover from intact history/frozen artifacts and record any context loss.
Do not regenerate accepted work, switch models or reset genuine negative findings.
Old snapshots remain inspectable/executable with their own runtime; current code
is not copied over historical contracts. A source repair during qualifying work
requires the affected live path to be demonstrated again.

## Deployment checks

```bash
BC_PI_EXECUTABLE=/absolute/concrete/pi bash scripts/check.sh
```

Opt-in installed-Pi tests use actual native PTY/tools/session behavior with dummy
credentials and network isolation; they make no inference. Ordinary offline tests
skip those checks. Neither certifies live providers or prose. Research access and
fresh substantive preflight are owned by `docs/RESEARCH-ACCESS.md`.
