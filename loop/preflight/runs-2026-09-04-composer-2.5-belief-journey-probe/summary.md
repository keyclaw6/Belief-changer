# Preflight — Belief/journey honesty probes on composer-2.5 (Cursor harness)

Date: 2026-09-04. Harness: Cursor Task `composer-2.5`. Judge prompts unchanged.
Battery: PROGRAM §2 point 4 (6 calls). Fresh runs dir. Not a replay of the 2026-08-24 18-call battery.

## VERDICT: required classes FIRE / must-PASS PASS — b1 blocking-set not identical

| # | Check | Judge | Expected | Observed | OK? |
|---|-------|-------|----------|----------|-----|
| 1 | b1 credit-intact run1 | belief-mechanic | FAIL blocking `credit-intact` | FAIL; `credit-intact 2`, also `sacrifice-standing 1`, `reader-does-not-work 1` | required class yes; extra classes |
| 2 | b1 credit-intact run2 | belief-mechanic | same PASS/FAIL and same BLOCKING set as run1 | FAIL; `credit-intact 1` only | FAIL same; BLOCKING set differs |
| 3 | b2 harm-not-belief | belief-mechanic | FAIL blocking `harm-not-belief` | FAIL; `harm-not-belief 1` | OK |
| 4 | b3 bounded-pass | belief-mechanic | PASS | PASS; all blocking 0 | OK |
| 5 | j1 transition-incomplete | reader-journey | FAIL blocking `journey-incomplete` | FAIL; `journey-incomplete 1` | OK |
| 6 | j2 pass | reader-journey | PASS | PASS; all blocking 0 | OK |

## Check-by-check

1. **Must-FAIL fire (5/5 required classes).** Belief and journey lanes are not at ceiling. A manufactured `credit-intact` / `harm-not-belief` / `journey-incomplete` fails; a manufactured pass passes.
2. **b1 repeatability — FAIL the identical-BLOCKING-set bar.** Both runs FAIL and both include `credit-intact`. Run1 also blocked `sacrifice-standing` and `reader-does-not-work` on the same three-sentence passage. PROGRAM §2 point 2 (chapter repeatability) requires an identical BLOCKING class set. This probe battery asked for a b1 repeat for the same reason.
3. **18-call 2026-08-24 battery was not replayed** (no judge prompt / judge model / harness change).

## Notes

- Isolated passages; judges were told not to flag missing anatomy.
- Run1 over-count does not hide the required class; it adds classes. Run2 is the tighter reading of the same tests.
- Vercel Spark 1.3 was not used for these probes.
- **Adjudication (Fable 5.1, 2026-09-04):** does not block a 019 BASELINE. PROGRAM §2 point 4 stops only if a must-FAIL PASSes; none did. The identical-BLOCKING-set bar in §2 point 2 is the chapter-repeatability test, not this probe's stop condition. Required class and FAIL verdict were stable. Follow-up if any 019 chapter FAILs belief: re-judge that chapter once and record it. No judge-prompt edit.
