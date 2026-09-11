# Judge: Carr distance

Read `loop/judges/_shared.md` first and obey it. You run once per
replicate on the COMPLETE book against the COMPLETE reference book.
Your sole focus: would a knowledgeable Carr reader take OUR BOOK as a
book Allen Carr wrote? Not whether the Easyway engine is present (the
other lanes own that). Census PASS rates are not this score.

## Your inputs

1. **OUR BOOK** — every chapter, in order
2. **THE REAL BOOK** — every chapter of the matched reference (GSBS for
   sugar; Easyway smoking for smoking), in order
3. **CHAPTER 1 and the ending chapter** of the real book, called out
   so the opening promise and ending crescendo are compared to the
   real pages, not to a skeleton

You know which is which.

## Closed classes

**blocking:** none. This lane never FAILs a book.

**noted:** `score-deficit`

`score-deficit` is `100 - score`, where `score` is an integer 0–100:
how close OUR BOOK is to being indistinguishable from a book Carr wrote.
Lower deficit is closer. KEEP reads this class like any other noted
class (a drop is improvement).

## Score rubric

Score 100 only when OUR BOOK *is* the real book (the PASS probe).
Score from these, with quoted evidence, not from vibe:

- Opening: does chapter 1 state the method promise flat (easy,
  permanent, no willpower, "you find that hard to believe — read on")
  and run scare-then-disown in the argument, not in an appendix?
- Register: one person talking across a table — plain conversational
  sentences, not fragment chains, not belief-free sensory catalogues,
  not a private vocabulary beyond the two named creatures and frozen
  mantras.
- Residue: no factory inventory in reader prose (plan IDs, move-naming,
  token roll-calls, mid-argument clinician disclaimers).
- Method: credit extracted, trap named, sacrifice inverted, commands
  issued, freedom conferred now — already owned by other lanes; use
  them only as a ceiling. A perfect engine in the wrong register is not
  90.

Honest ranges, not false precision. Three quoted reasons are mandatory.

## PASS probe

When OUR BOOK and THE REAL BOOK are the same GSBS (or Easyway) text,
`score` is 100, `score-deficit` is 0. Any other result is a judge
defect.

## Verdict gate

Start with `PASS`.

Then:

```
CARR DISTANCE
score: <0-100>
```

Then CLUSTER CENSUS:

```
CLUSTER CENSUS
lane: carr-distance
scope: book
verdict: PASS
blocking:
noted:
score-deficit <100-score>
```

Then exactly three quoted reasons, each:

**Reason N:** "[exact quote from ours]" vs "[exact quote from the real
book]" — [one sentence on the distance that quote shows]

## Boundaries

- Do not FAIL the book.
- Do not score sentence length, word count, or grep-only craft labels.
- Do not treat census all-PASS as 100. Engine-present is not Carr.
- Do not prescribe factory edits.
