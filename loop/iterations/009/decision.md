# Decision — Iteration 009

**Verdict:** BASELINE

Instrument baseline after the 2026-08-24 judge census redesign. No factory hypothesis. Two independent 18-chapter books from the accepted 000 plan.

**Predicted:** n/a (measurement).

**Observed:**

| Lane | Replicate A | Replicate B |
|---|---|---|
| belief | 18/18 PASS, blocking 0 | 18/18 PASS, blocking 0 |
| journey | 18/18 PASS; noted stall 5, re-argument 11, placement-miss 1 | 18/18 PASS; noted stall 4, re-argument 14, placement-miss 1 |
| voice | 11/18 PASS; blocking factory-speech 18, instruction-paperwork 2 | 11/18 PASS; blocking factory-speech 19, instruction-paperwork 5 |
| book-arc | PASS; noted re-argument 7, curve-flatten 1, pre-debut-spend 2 | PASS; noted re-argument 8, curve-flatten 1, pre-debut-spend 1 |

**KEEP objects (blocking in both books):** `factory-speech` (merged blocking 37), `instruction-paperwork` (merged blocking 7).

**Noise floor:** Voice chapter FAIL overlap is ch01 only. Failure *classes* match across books. Replicate-a ch09 Vercel fallback does not explain factory-speech (same class on Zen chapters; B ch09 PASS).

**Prediction accuracy:** n/a.

**Accepted snapshot:** replicate A chapters → `production-books/quit-sugar/chapters/`.
