# Preflight — Judge Calibration Battery on composer-2.5 (Cursor harness)

Date: 2026-08-24. Harness: Cursor (`agent --model composer-2.5 --mode ask`, not fast).
Each call was a fresh process; `_shared.md` then `loop/judges/`, inputs from `loop/preflight/inputs/`.
Census redesign in the judge prompts. Fresh runs dir.

## VERDICT: PREFLIGHT 18/18 PASS

## Result table (18 calls)

| # | Check | Judge | Run | Expected | Observed | PASS/FAIL |
|---|-------|-------|-----|----------|----------|-----------|
| 1 | PASS test | belief-mechanic | run1 | PASS, all counts 0 | PASS, all 0 | OK |
| 2 | PASS test | belief-mechanic | run2 | PASS, all counts 0 | PASS, all 0 | OK |
| 3 | PASS test | voice-emotion | run1 | PASS, all counts 0 | PASS, all 0 | OK |
| 4 | PASS test | voice-emotion | run2 | PASS, all counts 0 | PASS, all 0 | OK |
| 5 | PASS test | reader-journey | run1 | PASS, all counts 0 | PASS, all 0 | OK |
| 6 | PASS test | reader-journey | run2 | PASS, all counts 0 | PASS, all 0 | OK |
| 7 | Repeatability | belief-mechanic | run1 | same blocking set as run8 | PASS, blocking empty | OK |
| 8 | Repeatability | belief-mechanic | run2 | same as run7 | PASS, blocking empty | OK |
| 9 | Repeatability | voice-emotion | run1 | same blocking set as run10 | PASS, blocking empty | OK |
| 10 | Repeatability | voice-emotion | run2 | same as run9 | PASS, blocking empty | OK |
| 11 | Repeatability | reader-journey | run1 | same blocking set as run12 | PASS, blocking empty | OK |
| 12 | Repeatability | reader-journey | run2 | same as run11 | PASS, blocking empty | OK |
| 13 | Voice probe | voice-emotion | p1 hedged-core-verdict | FAIL blocking assigned-verdict-hedge | FAIL, assigned-verdict-hedge 1 | OK |
| 14 | Voice probe | voice-emotion | p2 hedged-method-promise | FAIL blocking method-promise-hedge | FAIL, method-promise-hedge 1 | OK |
| 15 | Voice probe | voice-emotion | p3 bounded-empirical-claim | PASS (must not FAIL) | PASS, hedges 0 | OK |
| 16 | Voice probe | voice-emotion | p4 bounded-source-limit | PASS (must not FAIL) | PASS, hedges 0 | OK |
| 17 | Voice probe | voice-emotion | p5v2 reader-present-doubt | PASS (must not FAIL) | PASS, hedges 0 | OK |
| 18 | Voice probe | voice-emotion | p6v2 reader-present-doubt | PASS (must not FAIL) | PASS, hedges 0 | OK |

## Check-by-check verdict

1. **PASS test — PASS (6/6).** Real GSBS chapter-02 as both texts. All census counts 0.
2. **Repeatability — PASS (3/3).** Same PASS/FAIL and identical BLOCKING class sets. Voice noted counts differ within ±1 (`coach-register` 2 vs 1; `wrong-register` 1 vs 0). Voice blocking empty both times — the generated-ch01 instruction clinician clause is no longer BLOCKING under the new instruction-register boundary.
3. **Voice honesty probe — PASS (6/6).** P1 fires `assigned-verdict-hedge`. P2 fires `method-promise-hedge`. P3–P6 do not FAIL; noted classes do not flip them.

## Notes

- P1 also noted `wrong-register 1` on the same hedged verdict; that did not replace the required blocking class.
- Instrument unchanged from campaign 001–008 (composer-2.5). Prompt change is the variable.
