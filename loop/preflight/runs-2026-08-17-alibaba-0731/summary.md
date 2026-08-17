# Preflight — Judge Calibration Battery re-run on alibaba-token-plan/deepseek-v4-flash-0731 (opencode harness)

Date: 2026-08-17. Harness: opencode. Judge model: `alibaba-token-plan/deepseek-v4-flash-0731`
(each call spawned as a clean-context `task` sub-agent pinned to that model; judge rubric served
verbatim from `loop/judges/`, inputs verbatim from `loop/preflight/inputs/`). Mirrors the
2026-08-14 DeepSeek V4 Flash battery layout and inputs.

## VERDICT: BLOCKED — not 18/18

Repeatability is not demonstrated on this model sample. Two of three chapter judges produced
conflicting PASS/FAIL across two identical runs of the identical generated chapter.

## Result table (18 calls)

| # | Check | Judge | Run | Expected | Observed | PASS/FAIL |
|---|-------|-------|-----|----------|----------|-----------|
| 1 | PASS test | belief-mechanic | run1 | PASS | PASS | OK |
| 2 | PASS test | belief-mechanic | run2 | PASS | PASS | OK |
| 3 | PASS test | voice-emotion | run1 | PASS | PASS | OK |
| 4 | PASS test | voice-emotion | run2 | PASS | PASS | OK |
| 5 | PASS test | reader-journey | run1 | PASS | PASS | OK |
| 6 | PASS test | reader-journey | run2 | PASS | PASS | OK |
| 7 | Repeatability | belief-mechanic | run1 | same as run8 | PASS (false-named OK) | **CONFLICT** |
| 8 | Repeatability | belief-mechanic | run2 | same as run7 | FAIL (false-named MATERIAL) | **CONFLICT** |
| 9 | Repeatability | voice-emotion | run1 | same as run10 | FAIL (instruction MATERIAL) | **CONFLICT** |
| 10 | Repeatability | voice-emotion | run2 | same as run9 | PASS token, but instruction MATERIAL (block identical to run9) | **CONFLICT** |
| 11 | Repeatability | reader-journey | run1 | same as run12 | PASS | OK |
| 12 | Repeatability | reader-journey | run2 | same as run11 | PASS | OK |
| 13 | Voice probe | voice-emotion | p1 hedged-core-verdict | FAIL (must flag) | FAIL — hedged verdict flagged MATERIAL | OK |
| 14 | Voice probe | voice-emotion | p2 hedged-method-promise | FAIL (must flag) | flagged (primary-job promise MATERIAL) but header PASS — contradiction | PARTIAL |
| 15 | Voice probe | voice-emotion | p3 bounded-empirical-claim | PASS (must not flag) | PASS | OK |
| 16 | Voice probe | voice-emotion | p4 bounded-source-limit | PASS (must not flag) | PASS | OK |
| 17 | Voice probe | voice-emotion | p5v2 reader-present-doubt | PASS (must not flag) | PASS | OK |
| 18 | Voice probe | voice-emotion | p6v2 reader-present-doubt | PASS (must not flag) | PASS | OK |

## Failure list (blocks the battery)

- **belief-mechanic repeatability (rows 7–8):** run1 = PASS, all components OK; run2 = FAIL,
  `false belief named: MATERIAL`. Identical inputs. PASS/FAIL and verdict lines diverge —
  repeatability FAILS (this judge returned PASS/PASS on 2026-08-14).
- **voice-emotion repeatability (rows 9–10):** run1 first token FAIL, run2 first token PASS,
  although both verdict blocks mark `instruction: MATERIAL` and identify the identical
  failure class (assigned-instruction reads as consent-form/compliance paperwork — the known
  legitimate FAIL on this article). The required "same PASS/FAIL both times" is violated;
  the "same highest-impact failure class both times" carve-out IS satisfied.
- **probe-p2 conformance (row 14):** the hedge was correctly flagged (primary-job promise
  MATERIAL, Voice Gap 1), but the report header says PASS while the mandatory block is not all
  OK — a header/block contradiction. Functional probe intent met; report is internally
  inconsistent.

## Notes

- Repeatability failures are model sampling inconsistency on `alibaba-token-plan/deepseek-v4-flash-0731`
  at judge temperature/generation; they are NOT judge-prompt or input defects, so no judge or
  input was edited. Per PROGRAM §2 and the hard rule, a failing check stops the battery at
  BLOCKED — judge repair (a founder-guided activity) is never done inside a run.
- The PASS test (6/6) and the voice honesty probe (6/6 functional intents) are clean; only the
  repeatability check fails on this model.
- Input substitutions: none — all 18 calls used the existing inputs in `loop/preflight/inputs/`.