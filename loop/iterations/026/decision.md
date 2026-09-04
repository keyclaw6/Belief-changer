# Decision — Iteration 026

**Verdict:** KEEP

**Predicted:** voice `factory-speech` falls in both versus 025 (A 18, B 16) by a drop of 2+ at the same 13-chapter n, from a selective Part B ban on chatbot openers, throat-clearing, summary closers, and stacked-triplet padding.

**Observed:**

| Lane | Replicate A | Replicate B |
|---|---|---|
| words | 50404 (≥ 48000) | 49067 (≥ 48000) |
| belief | 13/13 PASS; noted re-argument 4 (was 9) | 13/13 PASS; noted re-argument 10 (was 6) |
| journey | 13/13 PASS; noted re-argument 5 (was 12) | 13/13 PASS; noted re-argument 15 (was 10), journey-stall 3 (B-only) |
| voice | 13/13 PASS; blocking 0; noted factory-speech 13 (was 18), willpower-lexicon 36, coach-register 8, trap-question-label 5 (A-only), wrong-register 2, copied-mannerism 1 | 13/13 PASS; blocking 0; noted factory-speech 8 (was 16), willpower-lexicon 34, coach-register 6, copied-mannerism 4, wrong-register 2 |
| comparison | 13/13 PASS; noted missing 4 (was 3), partial 11 | 13/13 PASS; noted missing 4 (was 3), partial 8 |
| book-arc | PASS; noted re-argument 3, curve-flatten 1, pre-debut-spend 2 | PASS; noted re-argument 4 |

**KEEP objects (PRIMARY):** voice `factory-speech` 18→13 (A) and 16→8 (B). Same n. Drop ≥ 2 both. Length floor met both.

**New material failure class in both books:** none. `trap-question-label` 5 is A-only. `journey-stall` 3 is B-only. Comparison `missing` rose 3→4 both (same class: G06-M2, G15-M1, G20-M2 still missing; G04-M1 moved PARTIAL→MISSING).

**Prediction accuracy:** partial. PRIMARY fell in both. 025 leaks were mostly ease-operators and card titles, not the named chatbot phrases; the count still moved. Record as KEEP with a partial prediction.

**Belief-mechanic FAIL re-judge:** none.

**Accepted snapshot:** replicate A chapters → `production-books/quit-sugar/chapters/`. Factory change (`prompts/style-guide.md` §B5 operator 12 + §B9 bullet) is the new accepted craft. 3-strike clock on this component resets. Consecutive no-KEEP resets to 0.

**Skip:** 027 coach-register anti-slop (`coach-register` 8/6, not ≥8 both). 028 method-promise hedges (still 0/0).
