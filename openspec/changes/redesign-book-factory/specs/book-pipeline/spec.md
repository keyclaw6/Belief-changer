# book-pipeline delta

## MODIFIED Requirements

### Requirement: Brief artifact
The brief SHALL be the first artifact filled and a completed subject contract. It
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
The master plan SHALL be the chapter-by-chapter blueprint and the sole carrier of the
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

### Requirement: Executable research candidate lifecycle
Research SHALL run through one Windows-safe, resumable coordinator inside one
pinned RF-02 candidate operation root. Its lifecycle SHALL be `PREFLIGHT`,
`PLAN`, five parallel discovery lanes, `FILTER/DEDUPE`, `COVERAGE`, bounded
`TARGETED_GAP_FILL`, `SYNTHESIS`, `INDEPENDENT_REVIEW`, and `SEALED`, with
`BLOCKED` as a truthful terminal or resumable stop. The model lead SHALL decide
subject-specific questions, personas, source families, relevance, evidence
meaning, and gap priorities. Deterministic code SHALL own state, provenance,
eligibility, deduplication, ceilings, validation, and fail-closed transitions.
Research that is incomplete, rejected, over ceiling, unsafe, unprovenanced, or
unreviewed MUST NOT be represented as accepted.

The only production start route SHALL use the completed subject contract and an
environment-only `OPENROUTER_API_KEY`. It SHALL expose no provider key argument,
fake transport, model override, editor override, or native-test backend. After
preflight, the fixed breadth route SHALL use `deepseek/deepseek-v4-pro` with
`reasoning: {effort: xhigh}` and the current OpenRouter server-tool forms
`openrouter:web_search` and `openrouter:web_fetch`, each under explicit per-call
and total limits. The key SHALL occur only in the request authorization header
and MUST NOT enter prompts, hashes, state, receipts, logs, or artifacts.

#### Scenario: Production research starts without its environment key
GIVEN a completed candidate subject contract
AND `OPENROUTER_API_KEY` is absent
WHEN the production research `start` route is invoked
THEN it MUST exit nonzero before any file or directory write, socket or network
operation, provider/account preflight, or native-agent launch
AND no CLI argument or repository file may substitute for the missing key.

#### Scenario: The one research coordinator is interrupted or reaches a ceiling
WHEN the candidate lifecycle is interrupted after dispatch intent is durable
THEN resume MUST reuse every exact completed result and retain unchanged packet
hashes without rerunning unaffected lanes
AND every reused provider and editor result MUST be revalidated against its
exact durable request/task, reservation, route/model, usage, fetch proof,
canonical eligible payload, and verdict invariants rather than trusting a
recomputed outer hash
AND a pre-call marker without one complete, validated, durable result MUST stop
as ambiguous rather than replay
AND call, server-tool, output-token, retained-result, cost, and gap-round ceilings
MUST be reserved before parallel work and end `BLOCKED` when exhausted
AND usage, quota, activity, a cleared floor, or a stopped budget MUST NOT create
a PASS or seal.

#### Scenario: The lead performs initial source discovery
WHEN the completed query and coverage plan enters discovery
THEN fresh contexts MUST fan out across lived experience, scientific and
mechanistic evidence, industry and cultural receipts, the strongest
pro-behavior objection or counter-corpus, and subject dialect and sensory
language
AND a search hit MUST be treated only as a lead
AND retained evidence MUST match a captured fetch by canonical URL, locator,
fetched-content hash, and unchanged minimum excerpt
AND a claim recalled by a model or present only in a search summary MUST NOT
count as retrieved evidence.

#### Scenario: A discovered source fails rights or privacy eligibility
WHEN access, excerpt, retention, redistribution, attribution, deletion
sensitivity, or privacy/personal-data basis fails before retention
THEN no packet, source ID, URL, title, handle, identity, excerpt, provider
payload, or source-specific digest for that material may enter candidate
research
AND durable rejection evidence SHALL contain only a policy-level source-family
reason and aggregate count
AND a late independent-review rejection MUST first persist a content-free purge
intent so any interrupted scrub completes idempotently before resume can perform
another action
AND rejected material MUST NOT contribute to any bank, floor, persona, belief,
slot, safety, or diversity result.

#### Scenario: Eligible evidence duplicates a retained source or study
WHEN canonical or normalized URLs, fetched content, excerpts, evidence meaning,
stories, or scientific lineage duplicate an eligible retained candidate
THEN the coordinator MUST collapse the duplicate before IDs or coverage are
assigned and record corroboration without inflating coverage
AND scientific evidence MUST identify design/class, underlying study lineage,
grade rationale, scope, counterevidence, and permitted and prohibited inference
AND mirrors, reviews, or reports of one study MUST count as one lineage
AND a non-`CONTESTED` Bank 7 claim MUST have at least two genuinely independent
lineages.

#### Scenario: Coverage is recomputed from retained evidence
WHEN filtering or synthesis completes
THEN one shared inspection core MUST derive coverage from parsed accepted
packets, evidence items, syntheses, and intervention-ready units rather than
trusting model or log PASS labels
AND it MUST aggregate all brief, provenance, grade/inference, source-diversity,
testimonial, counter-corpus, safety, and LEU/SEU/GAP blockers
AND it MUST derive all ten banks, every applicable style slot, every brief
belief across each relevant persona, and a spread of at least three materially
distinct personas
AND the selected FULL-LENGTH or POCKET floors for lived experience, scientific
claims, verbatim pro-behavior justifications, analogies, dialect/sensory items,
and testimonial candidates MUST commission gaps when missed but MUST NOT be
sufficient for acceptance when met
AND no lane may clear while more than half of its accepted entries come from one
site, domain, or author.

#### Scenario: A numeric floor is genuinely scarce
WHEN exhaustive rights-clean retrieval cannot meet one applicable numeric floor
THEN only that numeric floor MAY be waived by a hash-bound independent-review
finding that binds the search attempts and demonstrated true ceiling
AND belief, persona, safety, provenance, source-eligibility, intervention-unit,
slot, or review gaps MUST NOT be waived as scarcity.

#### Scenario: Coverage or independent review proves a research gap
WHEN the derived coverage report or evidence editor identifies a precise thin
belief, persona, bank, slot, source family, safety boundary, counter-corpus, or
inference defect
THEN the lead SHALL commission only that demonstrated gap in the next bounded
round and preserve every unaffected accepted packet hash
AND it MUST NOT rerun the whole corpus, patch evidence by hand, invent support,
or turn repeated activity into acceptance
AND a remaining gap or exhausted round ceiling MUST end `BLOCKED`.

#### Scenario: Research is independently accepted and sealed
WHEN synthesis and coverage claim completeness
THEN a fresh evidence editor from an independent model family MUST review the
exact candidate digest for fetch fidelity, rights/privacy, originality,
scientific rigor, inference bounds, deduplication, Carr-intervention utility,
counter-corpus strength, and belief/persona/safety/slot coverage
AND review rejection MUST return structured targeted gaps to the bounded loop
AND a PASS MUST bind the editor task, verdict, and candidate hashes
AND no candidate byte may change between that PASS and sealing
AND the seal MUST bind the completed brief, prompt and configuration, sanitized
call receipts, packet inventory, syntheses, derived coverage report, research
log, and independent review
AND any missing, rejected, incomplete, changed, or stale binding MUST fail
closed.

#### Scenario: The current quit-sugar corpus is inspected under the new contract
WHEN the shared inspection core evaluates the preserved current corpus
THEN it MUST return one aggregate failure that includes the missing intended
reader and unresolved brief fields, 23 packets and 47 evidence items, 57 lived
bank bullets and 12 scientific bank bullets, zero LEU/SEU/GAP units, and no
current independent review or seal
AND its historical all-bank PASS log MUST NOT authorize framing or suppress any
current blocker.

#### Scenario: Offline readiness is tested without a production research run
WHEN RF-32 exercises captured transports or native-Codex simulations
THEN fake transports and editors MUST be reachable only through import-time test
seams in temporary non-production roots, never through the production CLI or
causal campaign entrypoint
AND the test MUST NOT touch an accepted production book, invoke a provider or
account endpoint, generate chapter prose, promote research or product, append a
real experiment result, or change an H-F01/RF-21-or-later execution state.

### Requirement: Accepted research and immediate chapter adequacy
One accepted, current whole-book research seal SHALL be mandatory before
framing, planning, commissioning, or writing. Each source-owned need in an
accepted plan/card SHALL bind accepted intervention-unit IDs and exact packet
locators. Immediately before each durable chapter-writer dispatch, the runtime
SHALL revalidate seal freshness and prove that the chapter's assigned packet
set satisfies every applicable source-owned need and safety boundary. The writer
SHALL receive only the accepted, relevant, assigned, source-bounded material;
the full corpus and unassigned packets MUST remain absent.

#### Scenario: A downstream stage has no current accepted research seal
WHEN framing, planning, commissioning, or writing is requested from missing,
incomplete, rejected, tampered, or stale research
THEN the stage MUST stop before its model or durable write boundary
AND an old research log, packet count, synthesis file, or historic verdict MUST
NOT substitute for the current seal.

#### Scenario: A chapter's assigned research is inadequate at dispatch
WHEN the immediate pre-writer check finds a missing required unit or locator, an
unassigned source, a widened inference, a safety mismatch, or a stale binding
THEN that chapter MUST NOT reach the writer callback
AND the check SHALL emit one structured research-owned targeted gap
AND writer dispatch MUST NOT itself start research or rerun the whole corpus.

#### Scenario: An audited pre-writer candidate resolves one demonstrated unit gap
GIVEN the candidate is still in RF-02 `CANDIDATE` state before durable writer
handoff
AND either the current independent master-plan review proves exactly one
`unit_missing` gap before commission audit or the current commission audit's
immediate adequacy adapter proves that same gap
WHEN the operator explicitly starts targeted research with a request bound to
the current research seal and exact master-plan and chapter-card hashes
THEN the coordinator SHALL skip the lead plan and five initial discovery lanes
AND run only bounded gap discovery, eligibility/deduplication, intervention-unit
synthesis, derived coverage, independent evidence review, and resealing
AND every previously accepted packet and intervention-unit byte MUST remain
unchanged while the extension uses a distinct fetched canonical source
AND a changed seal MUST stale the prior commission-set audit so commission
bindings are regenerated or deterministically rebound and the complete set is
audited again before writer-authority capture
AND rotation from a completed chapter gap to a distinct next request MUST resume
idempotently whether interruption occurs before or after request-file replacement
AND a stale commission audit, stale plan review, or changed plan/card byte MUST
NOT authorize targeted research
AND a targeted start from `WRITER_HANDOFF` or any later state MUST reject rather
than rewind writer authority.

#### Scenario: A chapter's assigned research is adequate at dispatch
WHEN the current seal verifies and every source-owned plan/card need and safety
boundary is satisfied by the exact assigned accepted units and packet locators
THEN only that compact accepted assignment MAY enter the chapter commission and
writer handoff
AND whole-book research MUST NOT be duplicated merely to authorize the chapter.

#### Scenario: A later chapter follows an earlier chapter in one audited batch
GIVEN writer authority was captured from one complete current commission audit
before the batch began
WHEN an earlier selected chapter has been durably accepted and the next chapter
is ready for dispatch
THEN the runtime SHALL compare the current commission-audit receipt byte-for-byte
with the captured receipt and revalidate the current research seal, assigned
units, packet locators, plan/card bindings, and safety limits for that chapter
AND the expected earlier chapter output MUST NOT by itself stale the captured
authority
AND any changed receipt, research, plan, card, commission, assignment, seal, or
source-owned need MUST block before the next writer callback.

#### Scenario: Accepted research changes after downstream artifacts exist
WHEN a new research seal changes any prior seal binding
THEN every old research-bound framing, plan, commission, and writer eligibility
receipt MUST become stale
AND unchanged framing or plan bytes MAY receive a new binding only through
deterministic revalidation that proves all source-owned needs, beliefs, safety
limits, and inference bounds still hold
AND a semantic mismatch MUST route to its earliest owning stage and invalidate
only causally downstream artifacts
AND no stale receipt may be relabeled as current.
