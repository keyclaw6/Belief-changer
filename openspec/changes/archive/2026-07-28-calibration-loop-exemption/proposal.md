# calibration-loop-exemption

## Why
The auto-tuning loop (`loop/PROGRAM.md`, North Star `docs/AUTO-TUNING-LOOP.md`)
generates whole calibration books on a campaign branch and gates them with a
reference-sighted judge panel. The production chapter gate (fresh reviewer,
iterate to ACCEPT, commit to `main`) was written for production books and, read
literally, forces the old reviewer loop into calibration runs and commits
unaccepted calibration chapters to `main`. External review (2026-07-28)
flagged this as an execution blocker: a conscientious operator must either
violate the spec or corrupt the calibration design.

## What Changes
- `book-pipeline` — the chapter writing loop requirement gains a calibration
  exemption: loop-generated candidates use the loop's judge gate on the
  campaign branch and are never published or advanced as accepted chapters.
  Production books keep the reviewer-ACCEPT gate unchanged.

## Capabilities

### Modified Capabilities
- `book-pipeline` — chapter writing loop requirement (calibration exemption)
- `book-pipeline` — master plan artifact requirement (reviewer identity generalized from stale "Opus")

## Status
Applied to `openspec/specs/book-pipeline/spec.md` and archived in the same
change (the loop that needs the exemption already exists).
