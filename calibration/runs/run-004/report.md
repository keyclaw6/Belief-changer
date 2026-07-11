# Run report — run-004

**Stage:** A **Scope:** Chapter 2 editor-context A/B **Verdict:** IN PROGRESS

## What will run

Run-004 starts both arms from the exact run-003 Chapter 2 candidate and its exact `REVISE` review. Both use Opus 4.6 at reasoning `none`, the endpoint's maximum output allowance, the same prose-edit objective, and locked semantics.

Arm A is the full-context control: writer prompt, style guide, plan, Chapter 1, candidate, and review. Arm B is the minimal-context treatment: style guide, candidate, and review. Separate fresh Sol `ultra` reviewers receive their normal full blind inputs, with multi-agent orchestration disabled but no time or reasoning cap.

The run-boundary bird's-eye audit returned `GO`: context is the only assigned arm difference, the concurrent control removes the generic extra-pass confound, and both outputs are real reference-blind prose.

## Pre-registered decision rule

- `SUPPORTED`: B = `ACCEPT`, A = `REVISE`, and B has no semantic blocker.
- `REFUTED`: A = `ACCEPT`, B = `REVISE`, or B introduces a blocker attributable to omitted context.
- `INCONCLUSIVE`: matching verdicts. Either accepted arm may advance Stage A, but matching results cannot rank context.

## Results

Pending both generations and both unrestricted fresh reviews.

## Gate verdict

Pending.
