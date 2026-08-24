# Judge shared law — census, blocking vs noted, KEEP object

Every chapter judge and the book-arc judge obeys this file. Lane prompts
add class tests; they do not weaken these rules.

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
lane: <belief | voice | journey | book-arc>
scope: <chapter-NN | book | probe>
verdict: <PASS | FAIL>
blocking:
<class> <n>
noted:
<class> <n>
```

`verdict: FAIL` iff any blocking count is ≥ 1. Do not list a class under
both buckets except `willpower-lexicon` and `factory-speech` (voice): those
split per-quote by the lane's sentence test.

Repeatability: same PASS/FAIL and the same BLOCKING class set. NOTED
counts may differ by ±1 per class. Gap titles need not match.

PASS test (real GSBS as both texts): all counts 0, verdict PASS. A
sharpening opportunity in Carr is not a finding.

Cap BLOCKING gap write-ups at 5. NOTED classes do not consume gap slots
and do not flip assigned-line MATERIAL. Assigned-line MATERIAL is allowed
only when the matching BLOCKING class test fires.
