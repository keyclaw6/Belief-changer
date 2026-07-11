# Run report — run-NNN

**Stage:** A | B | C **Scope:** <what ran> **Verdict:** PASS | FAIL <gate summary>

## What ran
<stages executed, cycles used per gate (plan review N/3, chapter reviews N/3 each), anything re-generated and why — one paragraph>

## Objective results (`metrics.json`)
<key rows: total/mean words vs ref ratio, mantra check, repetition law, originality overlap — table or bullets, numbers not adjectives>

## Judge results (`judgments/judge-summary.json`)
<both control verdicts; equal-role macro preference; per-role rates; same-model replica agreement; A/B-order instability; critical failures; explicit source-verification and cross-family limits>

## Gate verdict
<each HARNESS §5 gate for this stage: pass/fail with the number>

## Diagnosis (ranked, each gap mapped to its owning generic asset)
1. <gap — mechanism — owning asset>
2. …

## Hypothesis outcomes
For each tested hypothesis record:
- **Pre-registered mechanism, lever, controls, prediction:** <what was expected and what stayed fixed>
- **Result / deciding evidence:** <raw numbers, judgments, artifact links>
- **Causal verdict:** <SUPPORTED | REFUTED | INCONCLUSIVE, with why>
- **Rival explanations / signal risk:** <confounds and false-positive/false-negative paths>
- **Next discriminating test:** <what would separate the remaining causes>

REFUTED still requires the failure autopsy in HARNESS §10; never convert an uninstantiated lever, insensitive measurement, or confounded run into a false negative. Never convert reviewer compliance without predicted blind product movement into a false positive.

## Amendments proposed for next run
<≤1 lever (or attributed batch): asset, change, hypothesis it tests>

## Escalations
<none | what and why>

## Framing/fork decisions taken this run (calibration book only)
<decisions the operator made that a founder would normally gate — logged for async review>
