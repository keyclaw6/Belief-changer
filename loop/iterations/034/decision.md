# Decision — Iteration 034

**Verdict:** KEEP

**PRIMARY:** voice `factory-speech` vs 033 BASELINE 20/18. Mechanism: style-guide §B4 Freedom-register — ease is pictured, not tagged (`with ease` / `Think how exciting…` / `Rejoice that…` / `let visible ease do the recruiting`).

**Predicted:** factory-speech falls in both, beyond the rate-normalized band (sugar 20→≤12, smoking 18→≤14). Grep of ease-operators to 0 without a census drop is not KEEP.

**Observed:**

| Lane | quit-sugar (n=13) | quit-smoking (n=14) |
|---|---|---|
| words | 53366 (≥ 48000) | 56466 (≥ 48000) |
| belief | 13/13 PASS; noted re-argument 7 | 14/14 PASS; noted re-argument 10 |
| journey | 13/13 PASS; noted re-argument 12, journey-stall 5 | 14/14 PASS; noted re-argument 6, journey-stall 1, placement-miss 3 |
| voice | 13/13 PASS; blocking 0; factory-speech 6, willpower-lexicon 26, copied-mannerism 3, wrong-register 4, coach-register 3 | 13/14 PASS (CH-01 FAIL method-promise-hedge blocking 1); factory-speech 12, willpower-lexicon 28, coach-register 4, wrong-register 3, copied-mannerism 1 |
| comparison | 13/13 PASS; noted missing 0, partial 4 | 14/14 PASS; noted missing 1, partial 11 |
| book-arc | PASS; noted re-argument 3, curve-flatten 1 | PASS; noted re-argument 2 |

**PRIMARY:** factory-speech **20→6 / 18→12** (drop ≥2 both). Ease-operator grep 0/0 both (`with ease`, `Rejoice that`, `Think how exciting/marvellous/wonderful`, `let visible ease do the recruiting`). Census fell with the grep — KEEP, not mechanism-only.

**KEEP objects (blocking in both books):** none. Sugar blocking 0. Smoking-only blocking `method-promise-hedge` 1 (CH-01) is not a both-subjects veto.

**Length floor:** met both.

**A1:** sugar ACCEPT 4 / CAP 9. Smoking ACCEPT 9 / CAP 5.

**Prediction accuracy:** PRIMARY direction correct both. Sugar overshot the ≤12 target (6). Smoking 12 beat ≤14. Ease-operator class closed; residual factory-speech is the untargeted header/meta remainder (smoking still 12).

**Accepted snapshot:** sugar → `production-books/quit-sugar/chapters/` (53366). smoking → `production-books/quit-smoking/chapters/` (56466). §B4 change stays. Architecture stays on `cursor/factory-instrument-halt-a530` until an explicit founder merge to `campaign-001`.

**Restored:** no.

**Next PRIMARY:** factory-speech is no longer ≥8 in both (6/12). Intersection ≥8 both is `willpower-lexicon` 26/28 (not PRIMARY). Journey re-argument 12/6 and comparison `partial` 4/11 are not ≥8 both. Next factory-speech work is smoking-worse residual (12) as PRIMARY scope, sugar as non-regression — **new mechanism**, not 028/029/030/032. Do not replay 020–024.
