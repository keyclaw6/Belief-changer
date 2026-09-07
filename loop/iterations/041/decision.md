# Decision — Iteration 041

**Verdict:** BASELINE

First dual-subject rejudge of frozen 037 under the 2026-09-06 Carr-distance
instrument. No factory wording change, no new hypothesis, no plan rewrite.
037 chapters copied identically (sugar 54612w / smoking 57583w) with 037
plans. Judges: Muse Spark 1.3 contributor via opencode-run
(`scripts/loop-runner/judge_replicate_spark.py`, parallelism 4),
recalibrated 2026-09-07 (29/29 PASS). Panel: 54 sugar + 58 smoking reports,
zero retries needed beyond per-call acceptance (no empty replies this run).

**Predicted:** n/a (measurement).

**Observed:**

| Lane | quit-sugar (n=13) | quit-smoking (n=14) |
|---|---|---|
| words | 54612 | 57583 |
| belief | 13/13 PASS; noted re-argument 1 | 14/14 PASS; noted 0 |
| journey | 13/13 PASS; noted re-argument 1 | 14/14 PASS; noted 0 |
| voice | 13/13 PASS; blocking 0; noted factory-speech 6, literary-stylization 5 | 14/14 PASS; blocking 0; noted factory-speech 9, literary-stylization 1 |
| comparison | 13/13 PASS; noted partial 3, missing 0 | 14/14 PASS; noted partial 4, missing 2 |
| book-arc | PASS; noted re-argument 1 | PASS; noted re-argument 1 |
| carr-distance | score 60, deficit 40 | score 72, deficit 28 |

Blocking census is 0 in every lane of both books. willpower-lexicon and
copied-mannerism are gone as classes (dropped by the instrument).

**New dual-subject floor (this instrument, Muse Spark judges):**
- voice `factory-speech` noted 6/9
- voice `literary-stylization` noted 5/1
- comparison `partial` 3/4 (smoking also `missing` 2, sugar 0)
- book-arc `re-argument` 1/1
- Carr-distance deficit 40/28 (sugar 60, smoking 72)
- No noted class ≥ 12 in both books → empty KEEP-eligible census
  intersection. Per CONTINUE.md, 042 scores on Carr-distance
  `score-deficit` + comparison `partial`, never on factory-speech.

**Carr-distance reasons (the distance to close):**
- Sugar: scare banished to an appendix instead of run-then-disowned in the
  argument; belief-free sensory catalogue ("Market air cool. Canvas shades
  flapping") vs plain table-talk; repeated mid-argument clinician
  disclaimers + private vocabulary (Nibbler, Sweet Con) vs flat commands
  with only Little/Big Monster.
- Smoking: method promise inside a soft contract vs flat dogmatic elation;
  fragment-chain sensory inventory ("Kettle on. Click. Cup out.") vs one
  plain voice; mid-argument clinician disclaimers vs routing difficulty
  back to the method.

**Carried factory:** 030 HEADER exemption, 036 RE-ARGUMENT finding, 037
LENGTHEN, 038 OVERCLAIM, style-guide §B4 + §B5 op 9, CH-01 flat-promise
card rule + style-guide Part B plain-Carr + runtime Carr DEFAULT lock
(unmeasured — no book has been generated with them), this instrument.

**Trace analysis:** skipped — no new generation; 037 traces unchanged. First
noise sample on this instrument is this single rejudge (no second replicate;
repeatability was verified in preflight, not here).

**Next:** 042 — regenerate plans + chapters under the current files so the
CH-01 rule and Part B fire. PRIMARY: Carr-distance `score-deficit`
(secondary: comparison `partial`). Research reuse applies (no research-stage
change). Do not replay 039/040. Do not PRIMARY factory-speech,
willpower-lexicon, or re-argument.
