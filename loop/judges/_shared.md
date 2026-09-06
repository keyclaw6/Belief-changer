# Judge shared law — census, blocking vs noted, KEEP object

Every chapter judge, the book-arc judge, and the Carr-distance judge
obeys this file. Lane prompts add class tests; they do not weaken
these rules.

## What success is

Belief change: the assigned false belief inverts so stopping feels like
escape, not sacrifice. Warm to the person, harsh to the trap. The reader
does the work. The book is cumulative and original (Carr's method, never
Carr's sentences). Sentence length, literary polish, and grep-only craft
labels are not success.

## Two severities

| Severity | Fails the chapter/book? | Appears in CLUSTER CENSUS? |
|---|---|---|
| **BLOCKING** | YES. `PASS` requires zero BLOCKING counts. | YES |
| **NOTED** | NO. Twenty NOTED and zero BLOCKING is `PASS`. | YES |

Never FAIL a unit for a NOTED class. Never invent a class named after a
scene ID, mantra ID, chapter number, or local metaphor. Same job = same
class even when the scene token changes.

`PASS`/`FAIL` is a gate on BLOCKING only. KEEP reads census counts in both
books, not chapter PASS rate.

## CLUSTER CENSUS (mandatory, exact header)

Emit once after PASS/FAIL and after any assigned-verdict lines, before
gap write-ups. Every class in your lane's closed list appears, including
zeros. Integer counts. One quoted sentence per count later in the report.

```
CLUSTER CENSUS
lane: <belief | voice | journey | comparison | book-arc | carr-distance>
scope: <chapter-NN | book | probe>
verdict: <PASS | FAIL>
blocking:
<class> <n>
noted:
<class> <n>
```

`verdict: FAIL` iff any blocking count is ≥ 1. Do not list a class under
both buckets except `factory-speech` (voice): that class splits
per-quote by the lane's sentence test.

Repeatability: same PASS/FAIL and the same BLOCKING class set. NOTED
counts may differ by ±1 per class **per chapter report**. Gap titles
need not match. That declared noise is ±13 on a 13-chapter book: it is
not a KEEP band.

**Book-level KEEP band:** compare **rates**, not raw sums, when chapter
counts differ. Rate = class count / chapter count (chapter lanes) or
the single book-level count (book-arc, carr-distance). A same-n drop
of 1–3 is inside noise (not material). Material improvement is a rate
drop of **≥ 25% and ≥ 4 counts** at n≈13, or a drop on a BLOCKING
class, comparison `missing`/`partial` (book totals), or Carr-distance
`score-deficit`. A noted class whose baseline in either book is below
12 sits inside this band for PRIMARY selection — do not use it as the
KEEP object. `re-argument` is never PRIMARY.

PASS test (real GSBS as both texts, including a late chapter with its
real previous chapter): all counts 0, verdict PASS. Carr-distance
probe: GSBS vs GSBS = score 100, score-deficit 0. Carr-method
recurrence (Little Monster, brainwashing, freedom refrain) is not a
finding. A sharpening opportunity in Carr is not a finding.

Also run, as founder-guided calibration not as KEEP: (a) Carr as OUR
text against a functionally matched other Carr chapter — counts need
not be zero, but the test must not invent BLOCKING on Carr-method
recurrence; (b) one genuinely defective positive control (a hedge on the
assigned method promise) that must fire. Source identity alone is not
the sole calibration standard.

Cap BLOCKING gap write-ups at 5. NOTED classes do not consume gap slots
and do not flip assigned-line MATERIAL. Assigned-line MATERIAL is allowed
only when the matching BLOCKING class test fires.
