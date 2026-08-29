# Decision — Iteration 015

**Verdict:** REVERT

**Predicted:** Voice noted `factory-speech` drops in both books vs 014 (17 / 38) **and** book-arc noted `re-argument` drops in both (5 / 4). Blocking `factory-speech` stays 0. Belief / journey / book-arc stay PASS.

**Observed:** Predicted X. Observed Y (A: noted factory-speech 17→20, book-arc re-argument 5→6, blocking factory-speech 0→1, voice 15/16 FAIL ch05; B: noted factory-speech 38→13, book-arc re-argument 4→5, blocking factory-speech 0→3, voice 14/16 FAIL ch14+ch15). **Wrong** on the KEEP conjunction. Belief 16/16, journey 16/16, book-arc PASS both (hold). `trap-question-label` 3/1→0/0 (closed; not the KEEP object).

## Evidence

Census (`loop/iterations/015/census-a.txt`, `census-b.txt`):

| Class | 014 A / B | 015 A / B |
|---|---|---|
| Voice blocking `factory-speech` | 0 / 0 | 1 / 3 |
| Voice noted `factory-speech` | 17 / 38 | 20 / 13 |
| Book-arc noted `re-argument` | 5 / 4 | 6 / 5 |

Panel complete both books (49/49 + 49/49). Writers: Muse Spark contributor-free / opencode. Judges: composer-2.5.

## Why REVERT

1. Targeted conjunction failed. Noted `factory-speech` did not drop in both (A rose). Book-arc `re-argument` rose in both.
2. PROGRAM veto / same-class regression: blocking `factory-speech` was 0 last iteration and is >0 in **both** new books (class name, not identical local form). A ch05 announces the chapter job at the verdict peak; B ch14–15 paste numbered instruction-spine prefixes onto assigned I-lines.
3. Trace analysis: local blocking forms are one-book (writer-prompt hydra); noted re-argument is both-books plan signal. Neither KEEP object improved in both books.

Do not promote the four prompt files. Do not copy chapters into `production-books/`. Campaign factory stays at 014 KEEP.

**Founder halt:** do not start 016 unless asked.
