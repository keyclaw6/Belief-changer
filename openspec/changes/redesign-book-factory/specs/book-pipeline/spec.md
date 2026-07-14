# book-pipeline delta

## MODIFIED Requirements

### Requirement: Brief artifact
The brief is the first artifact filled and is a completed subject contract. It
SHALL live at `production-books/<slug>/00-brief.md`, SHALL be completed before
downstream work, and SHALL name the target behavior, reader, fork decisions,
destination, exclusions, safety perimeter, one primary false belief, and three
to five subordinate beliefs in reader language. Missing, empty, placeholder, or
unresolved fields MUST NOT pass.

#### Scenario: Planning begins without a brief
WHEN the framing or master-plan step runs and `00-brief.md` is missing or empty
THEN the step MUST STOP
AND the brief MUST be completed first.

#### Scenario: Downstream work starts from an incomplete subject contract
WHEN the primary false belief, subordinate beliefs, destination, exclusions, or
safety perimeter is missing or unresolved
THEN research synthesis, framing, and planning MUST STOP
AND the brief MUST be completed before work resumes.

### Requirement: Synthesized research
Raw sources SHALL be synthesized into the two curated, traceable files
`research/lived-experience.md` (why people do the behavior, why they cannot stop,
shame, and testimonials) and `research/scientific-evidence.md` (studies and
mechanisms, each graded SUPPORTED, MIXED, or CONTESTED). Every bullet in both
files MUST trace to a source in `research/sources/`, and both files SHALL feed
framing and master planning. In addition to source IDs and evidence grades, the
synthesis SHALL expose intervention-ready units where the sources support them:
concrete situation, reader wording, implicated belief, emotion, permitted
inference, prohibited inference, and source locator. Coverage SHALL be checked
against the brief's belief set rather than a generic source-count quota. Source
retention SHALL preserve the existing rights/privacy gate: access, excerpt,
retention, redistribution, attribution, and privacy basis must pass; only the
minimum permitted excerpt is retained; deletion-sensitive,
nonredistributable, or personally identifying user content MUST NOT be committed.

#### Scenario: Synthesis cites an unsourced claim
WHEN a bullet in `lived-experience.md` or `scientific-evidence.md` cannot be
traced to a source in `research/sources/`
THEN the bullet MUST be removed or re-sourced during synthesis
BECAUSE the synthesis must be fully source-traceable.

#### Scenario: Research material fails rights or privacy review
WHEN a source cannot be lawfully and safely excerpted, retained, redistributed,
attributed, or committed without exposing deletion-sensitive or personally
identifying content
THEN that material MUST stay out of tracked research artifacts
AND it MUST NOT count as evidence coverage.

#### Scenario: A planned belief lacks usable evidence
WHEN the synthesis cannot supply a traceable situation, observation, or bounded
inference needed to intervene on a named belief
THEN the gap MUST be reported to the research owner
AND downstream artifacts MUST NOT invent the missing material.

### Requirement: Framing artifact
Framing adapts the global style guide to one behavior and SHALL live at
`production-books/<slug>/framing.md` after accepted research synthesis and before
the master plan. It SHALL retain personas, the format decision, any redefinition
decision, all style-guide §10 playbook answers, mantra seeds, and an explicit
position for every §4 fork. It SHALL additionally resolve the belief graph,
subject-specific evidence-honest authority strategy, and cumulative reader
journey. Every planned argument-bearing chapter SHALL identify an entering
belief, subject-specific encounter, discovery mechanism, emotional turn,
leaving belief, and handed-forward state.

#### Scenario: Framing omits a fork position
WHEN `framing.md` does not state a position for a §4 fork
THEN framing is incomplete
AND the master-plan step MUST NOT begin until every fork position is recorded.

#### Scenario: Framing contains an unresolved reader transition
WHEN a planned argument-bearing chapter lacks a distinct entering belief,
discovery, leaving belief, or handoff
THEN framing is incomplete
AND master planning MUST NOT begin.

### Requirement: Master plan artifact
The master plan is the chapter-by-chapter blueprint and the sole carrier of the
book's deliberate repetition schedule, instruction spine, and curves. It SHALL
live at `production-books/<slug>/master-plan.md`, SHALL be produced by the
master-plan skill from the style guide, accepted research, and framing, and
SHALL remain the whole-book semantic authority for sequence, budgets, evidence
allocation, deliberate repetition, instructions, variation, and continuity.
Each argument-bearing chapter card SHALL specify its entering belief, concrete
encounter, enacted discovery, emotional turn, leaving belief, assumptions handed
forward, and work reserved elsewhere. A chapter card MUST NOT use setup, topic
coverage, or a catalogue for later demolition as its primary belief job. The
plan SHALL NOT be final until an independent planning review recorded in
`master-plan-review.md` ends with `fit to write from`. This replaces the prior
Opus-specific reviewer assignment so that plan writing and plan review can use
independent model families.

#### Scenario: A master plan is drafted
WHEN `master-plan.md` is drafted
THEN it is NOT final
AND an independent review MUST be recorded in `master-plan-review.md` and
iterated until the verdict is `fit to write from`.

#### Scenario: A chapter is commissioned or written before the plan is fit
WHEN `master-plan-review.md` does not end `fit to write from`
THEN chapter commissioning and chapter writing MUST NOT proceed.

#### Scenario: The opening defers its persuasive work
WHEN any of the first three primary chapter jobs is to define a future
investigation, catalogue claims for later demolition, or leave the reader only
willing to keep reading
THEN plan review MUST reject the plan.

#### Scenario: The cumulative reader walk is unresolved
WHEN adjacent chapters duplicate their principal discovery mode, fail to build
on the preceding leaving belief, or contain unresolved writer-facing authority
THEN plan review MUST end `needs changes first`
AND chapter commissioning and writing MUST NOT begin.

### Requirement: Chapter writing loop
Chapters SHALL be written in order by fresh-context writers. A writer SHALL see
only the compact generic writer contract, the authoritative target commission,
and the immediately previous chapter, and SHALL NOT receive the complete style
guide, complete master plan, reference prose, judge feedback, or unassigned
source packets. All chapters selected for an experimental batch SHALL be
generated and frozen before developmental review or revision begins.
This intentionally replaces the prior full-style-guide/full-master-plan writer
context, per-chapter review-before-advancing sequence, immediate chapter commit,
and README-update requirement with commission context, frozen-batch review, and
atomic configuration/product promotion.

#### Scenario: Writer context contains whole-book inventory
WHEN a writer call contains the complete master plan, complete style guide, or
unassigned packet material
THEN the call violates the writer-context contract
AND its output MUST NOT enter an accepted batch.

#### Scenario: A writer is given extra chapter context
WHEN a chapter writer receives chapters other than the immediately previous one
THEN the anti-repetition context contract is violated
AND its output MUST NOT enter an accepted batch.

#### Scenario: Review begins before the draft batch is frozen
WHEN any selected first draft has not been generated and snapshotted
THEN developmental review and revision MUST NOT begin.

## ADDED Requirements

### Requirement: Chapter commission artifact
Each chapter SHALL have an authoritative semantic commission at
`production-books/<slug>/commissions/chapter-NN.md`. The commissioner SHALL see
the accepted plan, target card, established reader state, and only the assigned
source packets. The commission SHALL carry the completed belief transition,
source-grounded situation and reader wording, permitted mechanism, emotional
movement, empirical and safety limits, exact frozen tokens, reserved work, and
received/handed-forward state without prescribing prose. `COMMISSION BLOCKED`
MUST stop writing.

#### Scenario: A commission cannot ground its assignment
WHEN the assigned packet conflicts with the plan, cannot support the intended
inference, contains an unresolved ID, or requires another chapter's work
THEN the commissioner MUST return `COMMISSION BLOCKED` with the owning gap
AND the chapter writer MUST NOT run.

### Requirement: Split chapter review
Grounded review and developmental review SHALL be separate fresh contexts.
Grounded review SHALL see the chapter, commission, assigned packets, and
evidence/safety contract and SHALL block unsupported claims, unsafe claims,
originality failures, or ownership leakage. Developmental review SHALL see the
complete frozen batch and its planned reader states, SHALL remain reference
blind, and SHALL report failed transitions, sequence defects, emotional movement,
and handoff failures.

#### Scenario: A grounded blocker remains
WHEN grounded review identifies a material source, safety, originality, or
ownership defect
THEN the product MUST NOT proceed to acceptance evaluation
AND a review-cycle cap MUST NOT waive the blocker.

### Requirement: Owner-routed repair
Every accepted defect SHALL route to research, synthesis, framing, plan,
commission, prose, revision, or evaluation according to the earliest owning
stage. Prose-owned defects SHALL receive one defect-scoped repair from the
original writer before any cross-family editorial escalation. Upstream repairs
SHALL invalidate and regenerate only causally downstream artifacts.

#### Scenario: Review finds an upstream defect
WHEN a review finding depends on missing or contradictory upstream authority
THEN the finding MUST return to that stage owner
AND the writer MUST NOT improvise or rewrite around it.

#### Scenario: Targeted prose repair fails
WHEN one defect-scoped repair leaves the accepted prose-owned defect unresolved
THEN a distinct editorial model MAY synthesize a repair
AND whole-artifact resampling MUST NOT be the automatic fallback.
