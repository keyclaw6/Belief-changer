# Decision — Iteration 017

**Verdict:** REVERT

**Predicted:** Voice noted `trap-question-label` 3/1 → 0/0 both. Blocking `factory-speech` stays 0/0. Belief / journey / book-arc stay PASS.

**Observed:** Predicted X. Observed Y (A: trap-question 3→0, blocking factory-speech 0→1, voice 14/15 FAIL ch09, journey 14/15 FAIL ch12; B: trap-question 1→1, blocking factory-speech 0→1, voice 14/15 FAIL ch01). **Wrong** on the KEEP gate. Belief 15/15 and book-arc PASS both.

## Evidence

Census (`loop/iterations/017/census-a.txt`, `census-b.txt`):

| Class | 014 A / B | 017 A / B |
|---|---|---|
| Voice noted `trap-question-label` | 3 / 1 | 0 / 1 |
| Voice blocking `factory-speech` | 0 / 0 | 1 / 1 |
| Voice noted `factory-speech` | 17 / 38 | 18 / 10 |

Panel complete both books (46/46 + 46/46). Writers: Muse Spark contributor-free / opencode. Judges: composer-2.5. Plan reused (014).

## Why REVERT

1. KEEP object failed. Trap-question closed in A (3→0) and stayed 1 in B (`Ask the simplest Socratic trap — …` — not the 014 formula, still the census class).
2. PROGRAM veto: blocking `factory-speech` was 0 last accepted comparison and is >0 in **both** new books. A ch09 announces the chapter job at the primary-job landing (`the one belief move this chapter had to make and it is made`). B ch01 speaks the house posture as policy (`I am warm to you and vicious to the trap`). Same class name, different local forms.
3. Named 015 instruction serials stayed closed. A’s blocking is the verdict-landing *family* under a new string after W1 stripped `land one short verdict`.

Do not promote the two prompt files. Do not copy chapters into `production-books/`. Campaign factory stays at 014 KEEP.

**Founder halt:** do not start 018 unless asked.
