## MODIFIED Requirements

### Requirement: Master plan artifact
The master plan SHALL be the chapter-by-chapter blueprint and sole carrier of book-specific deliberate repetition. It SHALL be produced at `production-books/<slug>/master-plan.md` from exactly the master-plan prompt, style guide, brief, framing, lived-experience synthesis, and scientific-evidence synthesis. The planner MUST NOT receive reference books, `analysis/`, calibration reference text, judge outputs, or other chapters.

The plan MUST use one authoritative representation per book decision. It MUST contain the false belief, fork and redefinition decisions, safety perimeter, a compact source-traceable evidence ledger, 6–10 original frozen mantras with chapter-level debut/echo routing, an exact instruction spine, a coherent whole-book arc, and compact chapter cards. Each chapter card MUST state one belief job, target personas, referenced evidence and limits, a concrete scene or original analogy job, referenced mantra/instruction IDs, guardrails, and one integer word budget. The chapter budgets MUST state an exact valid total.

The plan MUST NOT require occurrence-count arithmetic, duplicated audit or cumulative-state matrices, repeated full mantra or evidence text in chapter cards, prewritten chapter previews/theses/landings/SUMMARY prose, or generic style rules copied into every card. Chapter prose anatomy and density SHALL be applied by the chapter writer from the style guide and judged on the generated chapter.

The plan MUST NOT be considered final until a fresh allowed non-Opus plan reviewer at top reasoning records a review in `master-plan-review.md` ending `fit to write from`. Review SHALL block blindness, method-integrity, evidence-honesty, missing-context, invalid-length, unsafe-instruction, or incoherent whole-book architecture failures. Review MUST NOT block solely because a deleted duplicate representation, exact occurrence count, or prewritten prose component is absent.

#### Scenario: A normalized master plan is drafted
- **WHEN** `master-plan.md` defines shared decisions once and chapter cards reference those authoritative entries
- **THEN** a fresh allowed non-Opus reviewer judges whether the blueprint is sufficient to write a coherent, method-safe, evidence-honest book
- **THEN** the reviewer does not request duplicate audit tables, occurrence arithmetic, or prewritten chapter prose

#### Scenario: A planner is given forbidden reference context
- **WHEN** a planner input includes a reference book, an `analysis/` file, calibration reference text, or judge output
- **THEN** the planning call stops and the forbidden input is removed

#### Scenario: A plan omits writer-critical semantic context
- **WHEN** a chapter card lacks its belief job, personas, evidence/limits, scene or analogy job, mantra/instruction routing, guardrails, or integer budget
- **THEN** the plan review ends `needs changes first`

#### Scenario: A plan is coherent without deleted bookkeeping
- **WHEN** every authoritative entry resolves, the arc and budgets are coherent, and all blocking quality dimensions pass
- **THEN** the reviewer may end `fit to write from` without occurrence counts, duplicate matrices, or prewritten chapter anatomy

#### Scenario: A chapter is written before the plan is fit
- **WHEN** a chapter-writing step runs and `master-plan-review.md` does not end `fit to write from`
- **THEN** the chapter step does not proceed
