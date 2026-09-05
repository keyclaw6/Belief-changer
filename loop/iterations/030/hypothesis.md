## Failure evidence

Census class: **`factory-speech`** (voice) in both **027 accepted** books: A 13 / B 16. Blocking 0/0. ≥8 both.

028 style-guide operator 11: INCONCLUSIVE (13→18 / 16→10). 029 style-guide B10: INCONCLUSIVE (13→9 / 16→18). Both still emitted `IN THIS CHAPTER` on every chapter. 029 A ch09 blocked on a numbered plan-index (`10. IGNORE ANYONE WHO QUIT BY WILLPOWER`) at a mantra echo. Style-guide + factory-speech strike 2 — do not change style-guide again.

## Root cause

**PRIMARY — chapter-reviewer `prompts/chapter-reviewer.md`.** The writer still emits workshop headers and numbered plan-index lines. The reviewer may only flag JOB/MANTRA/INSTRUCTION/ID/LENGTH and is forbidden from style notes, so those leaks survive the one rewrite. 028/029 proved the writer-facing style-guide does not stop them.

## Targeted fix

**Change 1 (PRIMARY) — `prompts/chapter-reviewer.md` — class `factory-speech` (voice) — component chapter-reviewer (`HEADER` finding).**

Add one finding type: `HEADER` — draft opens with `IN THIS CHAPTER`, or prints a numbered plan-index with no spoken body. Numbered ALL-CAPS instruction plus one spoken rationale is not HEADER. ACCEPT requires no HEADER. Still one rewrite. No style-guide edit. No judge edit. No 020–024 wording. No GSBS.

**Why this component:** 028/029 already spent two style-guide mechanisms on this class. The rewrite gate is the unused component that can force the header out after draft.

## Predicted impact

**PRIMARY:** voice `factory-speech` (noted + blocking) falls in BOTH books versus 027 (A 13, B 16) by ≥2 at the same n.

**Possible regressions:** reviewer may REVISE more often and thin the instruction spine if it misreads a spoken ALL-CAPS command as plan-index. Length floor ≥48000. A 028-style formula-repetition leak can still raise the class.

**How we'll know it worked:** `factory-speech` must fall by ≥2 in BOTH replicates versus 027. Grep for "IN THIS CHAPTER" is not KEEP.
