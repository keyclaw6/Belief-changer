# book-pipeline Specification

## Purpose
TBD - created by archiving change init-baseline-specs. Update Purpose after archive.
## Requirements
### Requirement: Per-book folder contract
Each book occupies one folder `production-books/<slug>/` with a fixed layout. The layout is a stable external contract — agent skills hard-code these paths — and must not be restructured. Each book SHALL occupy exactly one folder `production-books/<slug>/` with a fixed layout, and that layout MUST NOT be restructured.

#### Scenario: A new book is started
WHEN a new book is begun
THEN its folder is created by copying the template (`cp -r production-books/_template production-books/<slug>`)
AND the slug is lowercase-hyphenated (e.g. `quit-gaming`).

#### Scenario: The folder layout is proposed to change
WHEN a change would restructure the per-book layout (renaming `research/sources/`, `lived-experience.md`, `scientific-evidence.md`, `framing.md`, `master-plan.md`, `chapters/`, or `00-brief.md`)
THEN the change is rejected
BECAUSE external agent skills depend on these exact paths.

### Requirement: Brief artifact
The brief defines the behavior, reader, and fork decisions for one book. It lives at `production-books/<slug>/00-brief.md` and is the first artifact filled. Every book SHALL have a brief at `production-books/<slug>/00-brief.md`, and it MUST be the first artifact filled before any downstream step proceeds.

#### Scenario: Planning begins without a brief
WHEN the framing or master-plan step runs and `00-brief.md` is missing or empty
THEN the step must STOP and the brief must be completed first.

### Requirement: Raw research sources
Raw source material (scrapes, threads, studies, transcripts — any format) is dumped into `production-books/<slug>/research/sources/`, one file per source, with each search logged in `research/research-log.md`. This is the raw material bank the synthesis step digests. Raw source material SHALL be stored one file per source in `production-books/<slug>/research/sources/`, and each added source MUST be logged in `research/research-log.md`.

#### Scenario: A source is found but not logged
WHEN a source file is added to `research/sources/`
THEN an entry recording it is added to `research/research-log.md`
SO THAT the order and provenance of sources is preserved.

### Requirement: Synthesized research
The raw sources are synthesized into two curated, traceable files: `research/lived-experience.md` (why people do it, why they can't stop, shame, testimonials) and `research/scientific-evidence.md` (studies and mechanisms, each graded SUPPORTED/MIXED/CONTESTED). These feed the framing and master-plan steps. Raw sources SHALL be synthesized into the two curated, traceable files `research/lived-experience.md` and `research/scientific-evidence.md`, and every bullet in them MUST be traceable to a source in `research/sources/`.

#### Scenario: Synthesis cites an unsourced claim
WHEN a bullet in `lived-experience.md` or `scientific-evidence.md` cannot be traced back to a source in `research/sources/`
THEN the bullet is removed or re-sourced during synthesis
BECAUSE the synthesis must be fully source-traceable.

### Requirement: Framing artifact
Framing adapts the global style guide to one behavior. It lives at `production-books/<slug>/framing.md` and is completed after research synthesis and before the master plan. It records personas, the format decision, the redefinition decision (if any), the §10 playbook answers, mantra seeds, and fork positions. Framing SHALL be recorded at `production-books/<slug>/framing.md` after research synthesis and before the master plan, and it MUST state a position for every §4 fork.

#### Scenario: Framing omits a fork position
WHEN `framing.md` does not state a position for a §4 fork
THEN the framing is incomplete
AND the master-plan step must not begin until every fork position is recorded.

### Requirement: Master plan artifact
The master plan is the chapter-by-chapter blueprint and the sole carrier of the book's deliberate repetition (mantra schedule, instruction spine, curves). It lives at `production-books/<slug>/master-plan.md` and is produced by the master-plan skill from the style guide, research, and framing. The master plan SHALL be produced at `production-books/<slug>/master-plan.md` and MUST NOT be considered final until an Opus review recorded in `master-plan-review.md` ends "fit to write from".

#### Scenario: A master plan is drafted
WHEN `master-plan.md` is drafted
THEN it is NOT final
AND an Opus sub-agent review is REQUIRED, recorded in `master-plan-review.md`, iterated until the verdict is "fit to write from".

#### Scenario: A chapter is written before the plan is fit
WHEN a chapter-writing step runs and `master-plan-review.md` does not end "fit to write from"
THEN the chapter step must not proceed.

### Requirement: Chapter writing loop
Chapters are written one at a time, in order, each by a fresh-context writer that sees only the master plan + the immediately previous chapter + the style guide, then reviewed by a fresh reviewer, iterated to ACCEPT before advancing. Chapters SHALL be written one at a time, in order, each by a fresh-context writer seeing only the master plan, the immediately previous chapter, and the style guide, and each chapter MUST be iterated to reviewer ACCEPT before advancing.

#### Scenario: A writer is given extra chapter context
WHEN a chapter-writer receives chapters other than the immediately previous one
THEN the anti-repetition design is violated
BECAUSE the extra context drives LLM repetition that the design exists to suppress.

#### Scenario: A chapter is accepted
WHEN the reviewer returns ACCEPT for a chapter
THEN the chapter is committed to `main` immediately
AND the book README status is updated
AND the next chapter may begin.

