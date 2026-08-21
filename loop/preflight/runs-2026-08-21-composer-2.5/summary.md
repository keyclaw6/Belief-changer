# Preflight — Judge Calibration Battery on composer-2.5 (Cursor harness)

Date: 2026-08-21. Harness: Cursor (`agent --model composer-2.5 --mode ask`, not fast).
Each call was a fresh process; rubric from `loop/judges/`, inputs from `loop/preflight/inputs/`.
No judge prompt, input, or PROGRAM.md edited.

## VERDICT: PREFLIGHT 18/18 PASS

## Result table (18 calls)

| # | Check | Judge | Run | Expected | Observed | PASS/FAIL |
|---|-------|-------|-----|----------|----------|-----------|
| 1 | PASS test | belief-mechanic | run1 | PASS | PASS | OK |
| 2 | PASS test | belief-mechanic | run2 | PASS | PASS | OK |
| 3 | PASS test | voice-emotion | run1 | PASS | PASS | OK |
| 4 | PASS test | voice-emotion | run2 | PASS | PASS | OK |
| 5 | PASS test | reader-journey | run1 | PASS | PASS | OK |
| 6 | PASS test | reader-journey | run2 | PASS | PASS | OK |
| 7 | Repeatability | belief-mechanic | run1 | same as run8 | PASS | OK |
| 8 | Repeatability | belief-mechanic | run2 | same as run7 | PASS | OK |
| 9 | Repeatability | voice-emotion | run1 | same as run10 | FAIL (instruction MATERIAL) | OK |
| 10 | Repeatability | voice-emotion | run2 | same as run9 | FAIL (instruction MATERIAL) | OK |
| 11 | Repeatability | reader-journey | run1 | same as run12 | PASS | OK |
| 12 | Repeatability | reader-journey | run2 | same as run11 | PASS | OK |
| 13 | Voice probe | voice-emotion | p1 hedged-core-verdict | FAIL (must flag) | FAIL — hedge flagged MATERIAL | OK |
| 14 | Voice probe | voice-emotion | p2 hedged-method-promise | FAIL (must flag) | operative FAIL — method promise MATERIAL | OK |
| 15 | Voice probe | voice-emotion | p3 bounded-empirical-claim | PASS (must not flag) | PASS | OK |
| 16 | Voice probe | voice-emotion | p4 bounded-source-limit | PASS (must not flag) | PASS | OK |
| 17 | Voice probe | voice-emotion | p5v2 reader-present-doubt | PASS (must not flag) | PASS | OK |
| 18 | Voice probe | voice-emotion | p6v2 reader-present-doubt | PASS (must not flag) | PASS | OK |

## Check-by-check verdict

1. **PASS test — PASS (6/6).** All three chapter judges returned PASS on the real GSBS chapter-02 fixture given as both texts, twice per judge. No manufactured material gap.
2. **Repeatability — PASS (3/3).** belief-mechanic: PASS/PASS with identical ASSIGNED-TRANSITION blocks (all OK / NONE ASSIGNED). voice-emotion: FAIL/FAIL with the same highest-impact failure class both times (assigned instruction reads as clinical consent/compliance paperwork — Gap 1 MATERIAL). Both runs also mark `unassigned passages` MATERIAL (Two Reports case-study register). Founder amendment 2026-07-28 option C satisfied. reader-journey: PASS/PASS.
3. **Voice honesty probe — PASS (6/6 functional intents).** Both hedges flagged (p1 core verdict, p2 method promise). Both bounded empirical/source-limit passages and both reader-present-doubt acknowledgments not flagged.

## Notes

- **probe-p2 preamble.** The judge prefixed a one-line process note before `**FAIL**`. Operative verdict is FAIL; ASSIGNED-MOMENT block marks primary-job promise MATERIAL. Same class of header noise as the 2026-08-17 DeepSeek battery; functional intent met.
- **voice-emotion repeatability.** Both runs share Gap 1 (instruction MATERIAL) as the highest-impact class. The additional `unassigned passages: MATERIAL` is present in both runs here (in 2026-08-17 DeepSeek it appeared only in run2). Decision-relevant class is identical.
- No judge prompt, input, or PROGRAM.md edited. Fresh runs dir.
