# Live re-judge — iter-008 book on redesigned judges

Date: 2026-08-24. Instrument: Cursor `composer-2.5 --mode ask` (same as campaign 001–008).
Book: `loop/iterations/008/traces/chapter-NN/response.md` (20 chapters).
Alignment: `loop/iterations/007/reference-alignment.md`.

## Expected vs observed

| Signal | Old instrument (iter-008) | New instrument | Match? |
|---|---|---|---|
| Voice PASS rate | 5/20 | **17/20**, then **18/20** after method-promise-hedge scope patch on ch16 | yes — trap labels no longer FAIL |
| Trap-question *labels* | 17/20 chapters FAIL | **noted** sum **40** across 13 chapters; never blocking | yes |
| Book-arc | FAIL (hydra: scene IDs, pre-debut, double jobs) | **PASS** — blocking 0; noted `re-argument 6`, `pre-debut-spend 5`, `skeleton-hole 1` | yes |
| Belief | 19/20 | ch01 and ch16 both **PASS**, blocking empty | yes (spot check) |
| Assigned-verdict / method hedges | P1/P2 FAIL | P1/P2 still FAIL after redesign and after patch | yes |
| Remaining voice FAIL | mixed craft labels | **ch07** blocking `factory-speech 3` (assigned-verdict meta); **ch09** blocking `factory-speech 1` (broken M-07 echo) | yes — real remaining factory leaks |

## Voice census (blocking classes that still FAIL a chapter)

- ch07: `factory-speech 3` — "We have reached the verdict this chapter exists to land…"
- ch09: `factory-speech 1` — M-07 pasted as a broken appositive
- ch16 first pass: `method-promise-hedge 1` on "Maybe a little. Briefly." (withdrawal myth). **False positive.** Prompt patched; re-judge **PASS**, `trap-question-label 8` noted, method-promise-hedge 0.

## KEEP object

A later iteration that cuts trap-question labels would read noted `trap-question-label` 40 → lower in both replicates, without a PASS-rate collapse. Book-arc KEEP can now see `re-argument` / `pre-debut-spend` fall without a hydra FAIL. Factory-speech inside assigned verdict/mantra lines remains a blocking target (ch07, ch09).
