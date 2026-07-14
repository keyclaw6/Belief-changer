# factory-experimentation spec

## ADDED Requirements

### Requirement: Causal-bundle experiment
Each experiment SHALL declare one causal hypothesis, the linked artifacts that
instantiate its mechanism, frozen variables, predicted artifact and reader
effects, decisive success and failure signals, and a falsification outcome.
One hypothesis MAY change multiple linked artifacts; unrelated changes MUST NOT
enter the same treatment.

#### Scenario: A structural hypothesis crosses an artifact boundary
WHEN the claimed mechanism requires coordinated changes to planning, commission,
and runtime handoff
THEN those linked changes MAY form one declared treatment
AND model, research, safety, reference blindness, and unrelated style rules MUST
remain frozen unless the hypothesis explicitly owns them.

### Requirement: Candidate isolation and atomic promotion
Every candidate run SHALL write configuration and product outputs to an isolated,
reproducible snapshot before promotion. A rejected candidate MUST NOT alter the
current production chapters or accepted factory configuration. An accepted
candidate SHALL promote the tested configuration and product together.
Each immutable generation SHALL be a complete factory operation view that
preserves the stable external layout, including every canonical configuration
asset and every complete `production-books/<slug>/` workshop present in that
view: briefs, research sources and syntheses, framing, plans, plan reviews,
commissions, chapters, and future workshops all retain their established paths.
A factory or agent operation SHALL receive and pin that operation root
once, then use the unchanged stable relative paths beneath it for every read and
write. It MUST NOT reconstruct a view from a caller-selected file subset or mix
paths from multiple generations. Reference-sighted evaluation inputs SHALL
remain in the sealed evaluation tree and MUST NOT enter the generation-blind
factory view. Adding a new complete workshop SHALL extend the accepted view by
one atomic generation switch without rewriting or discarding accepted history.
Candidate preparation MUST NOT perform accepted-store setup or extension.
Before promotion, the gate SHALL persist one immutable canonical decision that
binds the sealed pair, verified score receipt, input-history digest, assigned
timestamp, exact serialized row bytes, exact next-history digest, verdict, and
human approval. A resumed gate SHALL reuse that decision byte-for-byte.
Promotion SHALL require that canonical decision and the exact bound next-history
bytes; neither input may be optional or reconstructed by the promotion caller.

#### Scenario: The accepted-generation store is initialized
WHEN an operator explicitly initializes the store from the existing stable factory layout
THEN setup MUST expose either no accepted generation or one complete validated
generation at every injected interruption boundary
AND MUST NOT change the bytes, file types, or link targets of the source
configuration, prompts, or production-book paths.

#### Scenario: RF-02 maintains its isolated store before prose readiness
WHEN RF-02 is `READY`, RF-23 is not `READY`, and an explicitly authorized caller
targets its isolated root for accepted-store setup or complete-workshop extension
THEN that non-prose operation MAY execute
BUT candidate preparation, default loop execution, scoring, gating, model calls,
and prose writes MUST remain blocked until their own readiness requirements pass.

#### Scenario: A second book is added
WHEN a complete new `production-books/<slug>/` workshop is introduced after the
accepted store already contains history
THEN an explicit extension operation SHALL create a new complete operation view
that retains all prior workshops and accepted history
AND SHALL expose it with one atomic generation switch without reinitialization.

#### Scenario: An operation root contains an unsafe path
WHEN any root, intermediate directory, or file is outside its boundary, aliased,
symlinked, special, or multiply linked
THEN the operation MUST fail before parsing configuration, hashing file content,
globbing, traversing the path, or opening any outside file.

#### Scenario: A treatment is rejected
WHEN any decisive gate rejects a treatment
THEN its prose MAY remain under its experiment snapshot for evidence
BUT current production chapters and accepted configuration MUST remain
byte-identical to their pre-run state.

#### Scenario: A treatment is promoted
WHEN every required gate passes and the founder or named human approves the
direct reading comparison
THEN the exact tested configuration and exact tested product SHALL promote in
one atomic action
AND the accepted decision/results row SHALL already be inside that complete
generation before the single visibility switch.

#### Scenario: Promotion is killed at an atomic boundary
WHEN the process is forcibly killed after history preparation, generation
materialization, pointer preparation, pointer replacement, or immediately before
an owned experiment-root atomic-write replacement
THEN rerunning the same promotion with the same canonical decision and exact
history bytes SHALL finish idempotently as the exact old or exact new generation
AND recovery SHALL remove only an exact, in-root, single-link regular staging
name whose content, owner, and current manifest state prove it belongs to that
pending write
AND unknown, aliased, multiply linked, malformed, or state-inconsistent extras
MUST fail exact-layout validation without being removed.

#### Scenario: A manual agent is dispatched
WHEN an agent operation cannot dispatch through the configured model endpoint
THEN its instructions SHALL establish the pinned operation root as the working
directory and name all prompt, plan, chapter, and output paths relative to it
AND the agent MUST NOT resolve those inputs from the repository root
AND its printed resume command SHALL replay the pinned book, chapter selection,
iteration, hypothesis, configuration, experiment root, redesign authorization,
RF stage, supplied accepted root, and promotion intent, changing only to add
`--no-write`, with shell-safe quoting and no secret or irrelevant environment.

### Requirement: Separated product evidence
Factory acceptance SHALL separate four evidence layers: integrity, blind chapter
reader effect, blind whole-opening or whole-book sequence, and downstream
reference-sighted Carr craft distance. Source grounding, safety, originality,
word-sequence near-copy protection, and non-shaming/no-willpower method integrity
SHALL be hard requirements. Carr craft distance SHALL remain diagnostic and MUST
NOT alone decide promotion. The word-sequence near-copy check SHALL remain an
isolated mechanical comparison against the matched reference and SHALL reject a
candidate that crosses its configured tripwire without exposing reference prose
to generation or blind product evaluators.
Non-mantra phrase repetition SHALL be a repair signal rather than an
experiment-nullifying gate; exact assigned-mantra fidelity MAY remain a chapter
or publication gate.
All deterministic scoring and gate recomputation SHALL use one canonical scoring
core. A retired parallel scoring executable or duplicate scoring fixture MUST
NOT remain as a second behavior path; frozen historical artifacts remain
readable evidence.

#### Scenario: Likeness improves without reader effect
WHEN reference-sighted craft scores improve but blind judges do not find the
assigned belief transition or cumulative sequence
THEN the treatment MUST NOT be promoted on the likeness score alone.

#### Scenario: A candidate is too close to the matched reference
WHEN isolated word-sequence comparison crosses the near-copy tripwire
THEN the candidate MUST fail integrity
AND no preference, reader-effect, or craft score may override that failure.

### Requirement: Blind and independent judgment
Reader-effect and sequence evaluators SHALL remain blind to condition identity,
text provenance, reference-as-ground-truth context, historical scores, and judge
verdicts. In product experiments they SHALL NOT receive reference prose. The
H-F04 instrument calibration MAY submit a matched reference chapter or opening
as an anonymous candidate solely to measure the instrument ceiling; the
evaluator MUST NOT be told its identity or provenance, and the calibration MUST
not pair it with labeled reference ground truth. Each decisive pair SHALL use at
least two fresh independent contexts and, where available, two model families or
one model family plus a founder/human judgment. Reference-sighted diagnosis
SHALL run only after blind evidence is frozen.

#### Scenario: H-F04 calibrates on a reference-as-candidate
WHEN a matched reference chapter or opening is submitted to the blind instrument
THEN it MUST be anonymized as an ordinary candidate, isolated from all generation
contexts and promotion decisions, and recorded only as calibration evidence
AND neither its text nor the resulting verdict may flow into research, framing,
planning, commissioning, writing, review, or revision.

#### Scenario: Evaluator disagreement is too large
WHEN repeat variance or evaluator disagreement is comparable to the intended
treatment effect
THEN the instrument MUST be recalibrated
AND it MUST NOT make a promotion decision until its decision reliability is
established.

### Requirement: Minimal experiment record
Each run SHALL record only its hypothesis and causal chain, linked change set,
frozen variables, input hashes or commits, grounded audit result, blind chapter
result, blind sequence result, reference-sighted diagnostic, decision, and
falsification outcome. A materially changed instrument, model, threshold, or
campaign contract SHALL begin a new results lineage; rewards from different
lineages MUST NOT be compared numerically.

#### Scenario: The experiment record grows beyond decision evidence
WHEN a proposed record is a dashboard, direction audit, per-call micro-ledger,
or intermediate-artifact score
THEN it MUST be omitted unless a concrete failing test proves it is necessary.

### Requirement: Legacy loop pause
The existing `PROGRAM.md` product loop SHALL be fail-closed while this redesign
is in progress. It MUST NOT generate or mutate plans, commissions, chapters, or
production products before RF-23 is explicitly `READY` under the dependencies in
the authoritative ledger. No chapter prose may be generated before that state.
RF-00 SHALL be the first implementation task and SHALL install one executable
readiness guard in `PROGRAM.md` and every inventoried legacy entrypoint capable
of product generation, configuration/product promotion, or related writes.
Every later implementation task SHALL depend on RF-00 directly or transitively.
Read-only inspection, implementation verification, and isolated anonymous H-F04
calibration are permitted. RF-21 and RF-22 MAY create only their redesign-
controlled plan and commission candidates inside RF-02's isolated snapshot once
their own dependencies pass; they MUST NOT invoke the legacy loop or mutate the
accepted production state.

#### Scenario: The legacy loop is invoked before redesign readiness
WHEN an operator or automation attempts a current-PROGRAM product iteration
before RF-23 is `READY`
THEN the attempt MUST STOP without a model generation call or product mutation
AND the ledger remains the controlling recovery state.

#### Scenario: An authorized isolated redesign path is exercised
WHEN a redesign caller supplies explicit stage authorization, the requested
stage is ready under the ledger, RF-23 is `READY` whenever the request would
generate chapter prose, and the candidate root is isolated from accepted
production and configuration paths
THEN the guard MAY permit the stage's dry-run or execution boundary
AND it MUST still reject any target under the accepted current-product path.

### Requirement: Operator context protection
The root operator SHALL orchestrate paths, compact evidence, task state, and
decisions, and SHALL NOT read complete chapters, complete books, or reference
prose. Fresh subagents SHALL perform prose-heavy generation and reading. Human
reading gates SHALL be performed by the founder or another named human and
returned as a compact verdict.

#### Scenario: A root decision needs prose evidence
WHEN a decision requires reading a complete product artifact
THEN a fresh product-reading subagent or named human MUST perform that reading
AND return a compact evidence matrix or verdict to the root.

### Requirement: Reliability claim
The factory MUST NOT claim any-subject or founder-free whole-book reliability
from three sugar chapters. After a successful sugar opening, it SHALL pass
contrasting-subject opening tests and at least one complete-book coherence and
integrity gate before the vision is declared achieved.

#### Scenario: Opening success is generalized
WHEN the sugar H-F01 opening passes
THEN the result SHALL be described as support for the tested handoff hypothesis
AND NOT as proof of cross-subject or whole-book reliability.
