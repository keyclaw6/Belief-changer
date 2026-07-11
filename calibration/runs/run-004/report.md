# Run report — run-004

**Stage:** A **Scope:** Chapter 2 editor-context A/B **Verdict:** PASS

## What will run

Run-004 starts both arms from the exact run-003 Chapter 2 candidate and its exact `REVISE` review. Both use Opus 4.6 at reasoning `none`, the endpoint's maximum output allowance, the same prose-edit objective, and locked semantics.

Arm A is the full-context control: writer prompt, style guide, plan, Chapter 1, candidate, and review. Arm B is the minimal-context treatment: style guide, candidate, and review. Separate fresh Sol `ultra` reviewers receive their normal full blind inputs, with multi-agent orchestration disabled but no time or reasoning cap.

The run-boundary bird's-eye audit returned `GO`: context is the only assigned arm difference, the concurrent control removes the generic extra-pass confound, and both outputs are real reference-blind prose.

## Pre-registered decision rule

- `SUPPORTED`: B = `ACCEPT`, A = `REVISE`, and B has no semantic blocker.
- `REFUTED`: A = `ACCEPT`, B = `REVISE`, or B introduces a blocker attributable to omitted context.
- `INCONCLUSIVE`: matching verdicts. Either accepted arm may advance Stage A, but matching results cannot rank context.

## Results

Both Opus calls completed with reasoning disabled and zero reported reasoning tokens. Both artifacts were sealed before either review was opened. Separate unrestricted Sol `ultra` reviewers returned `ACCEPT` with zero blocking defects.

| Measure | Arm A — full context | Arm B — minimal context | Target |
|---|---:|---:|---:|
| Verdict | `ACCEPT` | `ACCEPT` | `ACCEPT` |
| Artifact words (`wc -w`) | 3,299 | 3,275 | 2,550–3,450 |
| You/your | 28.2/1k | 29.7/1k | 25–33/1k |
| Questions | 10.7% | 9.8% | 8–10% |
| Sentences under 8 words | 24.2% | 22.5% | ~20% |
| Average sentence | 17.2 words | 18.1 words | 15–17 |
| Blocking defects | 0 | 0 | 0 |

### H-041 causal verdict

`INCONCLUSIVE` by the preregistered rule: matching `ACCEPT` verdicts cannot rank full versus minimal context. The concurrent control does show that context reduction was not necessary for convergence. Both arms improved the H-040 craft failures after receiving the exact measured review, so the strongest remaining mechanism is feedback iteration or stochastic resampling, not demonstrated context interference.

Arm A is promoted. This is a control-default decision: because the treatment earned no causal advantage, the factory does not adopt an unproven context omission. Arm B remains preserved as an accepted experimental artifact. No post-hoc claim that Arm A is intrinsically superior is made.

## Gate verdict

PASS. Chapter 2 now has a fresh accepted artifact at `production-books/quit-sugar/chapters/chapter-02.md`. Stage A proceeds to Chapter 3.
