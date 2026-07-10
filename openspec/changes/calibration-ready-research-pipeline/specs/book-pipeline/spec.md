## ADDED Requirements

### Requirement: Role model isolation
The pipeline SHALL resolve exact model IDs at runtime and MUST preserve the founder-approved role boundaries. Research leads and workers MUST use DeepSeek V4 Pro, MiniMax M3, or GPT‑5.6 Luna; planners, plan reviewers, and chapter reviewers MUST use Gemini 3.1 Pro, GPT‑5.6 Sol, or Grok 4.5; every non-writer call MUST use that model's highest supported reasoning mode. Claude Opus 4.6 MUST be used only for chapter writing and MUST run with reasoning disabled.

#### Scenario: Opus is assigned outside chapter writing
- **WHEN** a run config assigns Opus to research, planning, review, judging, or synthesis
- **THEN** the affected stage stops before the model call

#### Scenario: A non-writer model is below top reasoning
- **WHEN** runtime model metadata reports a higher supported reasoning mode than the requested one
- **THEN** the stage stops and corrects the request before the model call

## MODIFIED Requirements

### Requirement: Brief artifact
The brief defines the behavior, reader, scope, and non-goals for one book. It lives at `production-books/<slug>/00-brief.md` and is the first artifact filled. Every book SHALL have a brief at `production-books/<slug>/00-brief.md`, and it MUST be the first artifact filled before any downstream step proceeds. Fork decisions MAY be deferred to framing when the brief explicitly says so.

#### Scenario: Planning begins without a brief
- **WHEN** the research, framing, or master-plan step runs and `00-brief.md` is missing or empty
- **THEN** the step stops and the brief is completed first

### Requirement: Raw research sources
Raw source material SHALL be stored one file per distinct source in `production-books/<slug>/research/sources/`. Each source file MUST use a stable source ID and preserve its URL, retrieval metadata, captured evidence, and bank/persona tags; every search, model call, and accepted or rejected source MUST be logged in `research/research-log.md`.

#### Scenario: A source is found but not logged
- **WHEN** a source file is added to `research/sources/`
- **THEN** an entry recording its search/assignment, model config, provenance, disposition, and file is added to `research/research-log.md`

#### Scenario: A URL is captured by multiple workers
- **WHEN** an accepted source URL already has a source file
- **THEN** the existing source file is enriched and the new visit is logged instead of creating a second source file

### Requirement: Synthesized research
Accepted raw sources SHALL be synthesized into the two curated, traceable files `research/lived-experience.md` and `research/scientific-evidence.md`. The lived file MUST carry Banks 1–6, 9, and 10 with persona tags; the scientific file MUST carry Banks 7–8 with SUPPORTED/MIXED/CONTESTED grades. Every bullet MUST name source IDs that trace to files in `research/sources/`.

#### Scenario: Synthesis cites an unsourced claim
- **WHEN** a bullet in `lived-experience.md` or `scientific-evidence.md` cannot be traced to an accepted source file
- **THEN** the bullet is removed or re-sourced during synthesis
- **THEN** framing remains blocked until both files are fully source-traceable

### Requirement: Framing artifact
Framing adapts the global style guide to one behavior. It lives at `production-books/<slug>/framing.md` and is completed after research synthesis and before the master plan. The framer SHALL receive exactly the brief, framing template, style guide, and two synthesized research files. Framing MUST record personas, the format decision, the redefinition decision if any, the §10 playbook answers, mantra seeds, and a position for every §4 fork.

#### Scenario: Framing omits a fork position
- **WHEN** `framing.md` does not state a position for a §4 fork
- **THEN** framing is incomplete
- **THEN** the master-plan step does not begin until every fork position is recorded

#### Scenario: Framing lacks the brief
- **WHEN** the framer is not given the filled `00-brief.md`
- **THEN** the framing call stops rather than inferring reader, scope, or non-goals

### Requirement: Master plan artifact
The master plan is the chapter-by-chapter blueprint and sole carrier of book-specific deliberate repetition. It SHALL be produced at `production-books/<slug>/master-plan.md` from exactly the master-plan prompt, style guide, brief, framing, lived-experience synthesis, and scientific-evidence synthesis. The planner MUST NOT receive reference books, `analysis/`, calibration reference text, judge outputs, or other chapters. The plan MUST NOT be considered final until a fresh allowed plan reviewer at top reasoning records a review in `master-plan-review.md` ending `fit to write from`.

#### Scenario: A master plan is drafted
- **WHEN** `master-plan.md` is drafted
- **THEN** it is not final
- **THEN** a fresh allowed non-Opus reviewer records issues in `master-plan-review.md` and review iterates until the verdict is `fit to write from`

#### Scenario: A planner is given forbidden reference context
- **WHEN** a planner input includes a reference book, an `analysis/` file, calibration reference text, or judge output
- **THEN** the planning call stops and the forbidden input is removed

#### Scenario: A chapter is written before the plan is fit
- **WHEN** a chapter-writing step runs and `master-plan-review.md` does not end `fit to write from`
- **THEN** the chapter step does not proceed

### Requirement: Chapter writing loop
Chapters SHALL be written one at a time, in order, each by a fresh-context Opus 4.6 writer with reasoning disabled that sees only the style guide, master plan, and immediately previous chapter. Each chapter MUST be reviewed by a fresh allowed non-Opus reviewer at top reasoning and iterated to ACCEPT before advancing.

#### Scenario: A writer is given extra chapter context
- **WHEN** a chapter writer receives chapters other than the immediately previous one
- **THEN** the anti-repetition design is violated and the call is rejected

#### Scenario: A production chapter is accepted
- **WHEN** a chapter outside calibration receives reviewer ACCEPT
- **THEN** the chapter is committed to `main` immediately
- **THEN** the book README status is updated and the next chapter may begin

#### Scenario: A calibration chapter is accepted
- **WHEN** a chapter inside a HARNESS calibration run receives reviewer ACCEPT
- **THEN** the next chapter may begin without an individual `main` commit
- **THEN** all artifacts are committed together in the run-level `calibration-lab` commit required by HARNESS §6
