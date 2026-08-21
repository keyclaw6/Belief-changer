## Failure evidence
Cluster 1 A01 tight-shoes flagship re-performed — positional spread C03→C07, book-arc Gap 1 (arc FAIL on 5 new gaps despite 002 Cluster 5 closure). Judge finds flagship inversion scene A01 runs at full argue-then-compress length twice instead of compressing to token: C03 *"Imagine you wear tight shoes. All day. They pinch… Does it? Or does it merely end a discomfort you created by wearing tight shoes?"* then C07 *"Imagine you wear tight shoes. All day. Too small. Pinching… Does that relief prove tight shoes give you pleasure?"* Per-chapter reader judges C03 and C07 both PASS — failure invisible locally, visible only as arc curve mistiming at mechanism hinge before Nibbler debut.

## Root cause
`prompts/master-plan-skill-v2.md` causes this. Trace analysis verifies: C03 card line 12 assigns *"Scenes: A01 tight shoes preview (job: frame benefit as suspect)"* and C07 card line 12 assigns *"Scenes: A01 tight shoes full (job: rescuer-as-perpetrator)"* — same ID re-staged at full length with a new job. Current factory state `### Scene and analogy bank` defines only `stable ID + description + job(s) + constraint` and `### Compact chapter cards` permits `one or more concrete scene/analogy IDs and the argumentative job each performs` with no debut binding. Iter-003 bound evidence rows and chapter jobs (lines 104-121) but left **scene/analogy ID re-assignment unconstrained**, so cards legally re-own A01 `full` and writer faithfully re-performs downstream (`chapter-07.md` lines 145-165). This is the same failure class as 002 re-argument but triggered by scene ID, not evidence row — not a model execution error.

## Targeted fix
Edit ONE file: `prompts/master-plan-skill-v2.md`, section `### Scene and analogy bank`.

**Replace:**
```
### Scene and analogy bank

Define each concrete scene or analogy once with:

- stable ID and a concrete, writable description of the scene or analogy;
- the argumentative job or jobs it performs;
- any safety, originality, or subject-specific constraint on its use.

Chapter cards reference scene/analogy IDs and the job each performs; they never copy the full scene or analogy into the card.
```

**With:**
```
### Scene and analogy bank

Define each concrete scene or analogy once with:

- stable ID and a concrete, writable description of the scene or analogy;
- the single argumentative job it performs and the debut chapter ID where it is staged at full argue-then-compress length;
- any safety, originality, or subject-specific constraint on its use.

A scene/analogy staged at full length once may never be staged again at full length with a new job — after debut it may appear only as a compressed token (its frozen name in one clause, e.g., `that tight-shoes relief`), never re-argued. Chapter cards after the debut chapter may reference the ID only in token form; they never copy the full scene into the card and never assign a second full staging of the same ID.
```

This supersedes the current scene-bank definition. No other file is edited. This is different from failed iter-002 (Mantra sheet debut-once/echo-by-token for mantras+evidence+scenes) which left scene-bank description free, and from failed iter-003 (Compact cards job/evidence re-own ban) which explicitly left scene-bank re-assignment and seam ownership free per 003 lesson.

**Why this component:** The trace analyzer names **plan-card** as root for this cluster and verifies C09 card clean for Cluster 2 / writer traces faithful for Cluster 1 — the defect is card authorship (second full A01 assignment), not writer-prompt craft or model initiative, so fixing writer-prompt would leave the illegal second `full` assignment legal.

## Predicted impact
**What will improve:** Cluster 1 will close because C07 can no longer legally re-own A01 at full length — it must echo `tight-shoes` as one-clause token, preserving the C03 inversion and keeping the mechanism hinge timing intact before Nibbler debut; mutational re-argument via scene IDs is blocked, distinct from closed job/evidence re-argument.

**What might regress:** If a scene truly needs two distinct full jobs, the token rule would force compression where a second full staging was structurally needed — mitigated because the bank now requires the planner to choose the single strongest job and debut chapter upfront rather than splitting it.

**How we'll know it worked:** The book-arc judge should no longer flag A01 duplication (Gap 1) and chapter 7 should contain only a token echo of tight-shoes, not the 20-line re-staging at lines 145-165; voice C07 scaffold from announced re-performance should also fall.
