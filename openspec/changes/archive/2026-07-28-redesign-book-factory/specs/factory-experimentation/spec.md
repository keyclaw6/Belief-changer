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

#### Scenario: Direct GSBS Stage A readiness is authorized separately
WHEN the founder authorizes readiness for the direct H-F01 quit-sugar
product-calibration lineage while postponing its execution
THEN RF-20's failed `rf20-attempt-5` lineage MUST remain terminal and unchanged
AND `rf20-successor-reader-state-1` MUST NOT run, be reinterpreted as passing, or
become a prerequisite
AND the H-F01 authority MUST identify this as a distinct lineage before any call.

#### Scenario: Offline readiness does not start H-F01
WHEN the Windows runtime and Muse route reach reviewed offline readiness but the
founder postpones experiment execution
THEN RF-21 MUST remain `READY` and unstarted
AND no H-F01 arm snapshot, causal authority, treatment artifact, planning call,
review call, commission call, provider call, or model call may be created
AND `READY` MUST fail closed at snapshot preparation, authority freeze, and
RF-21 dispatch
AND only a later explicit founder start recorded by moving RF-21 to
`IN_PROGRESS` may prepare the arms, enter execution, and freeze the immutable
pre-call authority
AND RF-21 and RF-22 dispatch MUST require the named stage to be `IN_PROGRESS`.

#### Scenario: H-F01 authority is frozen before RF-21
WHEN H-F01 reaches RF-21's first call boundary
THEN an immutable authority MUST already bind the hypothesis, causal chain,
changed bundle, frozen variables, exact inputs, falsifier, pinned clean source worktree and commit,
executable hashes, both arm identities, exact allowed treatment diff, full route
law, fixed 40-call ceiling, and exactly six writer calls
AND both pre-RF21 pairs MUST equal the same accepted pair
AND every non-treatment research, configuration, style, safety, and evaluation
byte MUST match across arms
AND the exact offset-matched GSBS file paths and hashes MUST be evaluation-only
AND every RF-21 through RF-25 call counted under H-F01 MUST bind this authority.

#### Scenario: H-F01 is rebound to the authorized Windows root
WHEN the founder-authorized RF-21 readiness state is prepared
THEN the authority MUST bind the execution root exactly as
`C:\Users\Kristian Bilstrup\Documents\Belief-changer`
AND every repository-owned, authority-bearing, or persistent H-F01 input,
output, receipt, command, and resume target, plus every pinned RF-02-isolated
operation root, MUST be inside that pinned Windows root
AND only the already-required fresh native transport MAY use a bounded
OS-managed ephemeral scratch cwd outside it and copy transport schemas there
AND that cwd and those schema copies MUST remain non-authoritative and
non-persistent and MUST NOT replace or relocate any authority-bound artifact
AND `/home/kab/Belief-changer-minimal-loop` MUST be rejected before any input is
read, hashed, written, or sent to a model
AND the rebind MUST NOT itself mark RF-21 complete, authorize chapter prose, or
authorize product promotion.

#### Scenario: H-F01 writer settings are identical and route-verifiable
WHEN any of the three fresh control or three fresh treatment drafts is generated
THEN its writer request MUST use `model: meta/muse-spark-1.1`,
`reasoning: {effort: high}`, `temperature: 0.7`, and
`provider: {allow_fallbacks: false}`
AND the request body MUST omit `max_tokens`, `models`, and `fallbacks`
AND those four settings and omissions MUST be byte-identical across exactly all
six writer calls while the arm-specific context remains authority-bound
AND every request MUST send `X-OpenRouter-Metadata: enabled`
AND each response MUST capture its response model plus OpenRouter router metadata
AND that evidence MUST show requested model `meta/muse-spark-1.1`, direct routing,
first-and-only attempt, provider `Meta`, and actual model
`meta/muse-spark-1.1-20260709`
AND any missing routing metadata, fallback, retry to another endpoint, provider
or model mismatch, or seventh writer call MUST reject the batch
AND the full RF-21–RF-25 lineage MUST remain within the 40-call ceiling.

#### Scenario: Muse account and capability preflight fails closed
GIVEN no H-F01 chapter prose has been requested
WHEN the authority-bound OpenRouter preflight runs for the authenticated account
THEN official and account-visible metadata MUST resolve `meta/muse-spark-1.1` to
canonical slug `meta/muse-spark-1.1-20260709` with context `1048576`,
`max_completion_tokens: null`, prompt price `$1.25/M`, completion price
`$4.25/M`, exactly one Meta provider, mandatory reasoning, supported efforts
`xhigh`, `high`, `medium`, `low`, and `minimal`, and support for `reasoning`,
`temperature`, and `max_tokens`
AND the key MUST be valid, enabled, unexpired, authorized for the model, and have
enough account credit and key spend allowance for the declared six-call bound
AND the account and current request location MUST be affirmatively eligible for
the model's US-only availability without proxying, region spoofing, or another
geographic bypass
AND any absent, stale, contradictory, ineligible, or underfunded result MUST stop
before prose without buying credit or invoking another free or paid model,
provider, account, or route.

#### Scenario: H-F01 evidence makes no model-comparative claim
WHEN H-F01 is recorded, judged, or reported
THEN Muse MUST remain a frozen variable shared by control and treatment
AND any support or refutation MUST apply only to the declared
planning-to-writing handoff hypothesis
AND the result MUST NOT claim Muse is better or worse than Opus, claim any model
superiority, or promote a product because of the writer-route change.

#### Scenario: RF-21 and RF-22 dispatch is durable and authority-bound
WHEN the resumable coordinator is explicitly started with native dispatch
THEN it MUST run exactly two RF-21 and four RF-22 calls in fresh reference-blind
native contexts after the authority freezes and before chapter generation
AND every immutable task and result MUST bind the authority, exact inputs,
output identity, route, reasoning, command, thread identity, and artifact hashes
AND an interrupted call with no durable result MUST stop as ambiguous rather
than replay
AND resume MUST recompute the same six calls, commission-set receipt, and exact
treatment artifact hashes before accepting the RF-21/RF-22 receipt.

### Requirement: Research-isolated causal treatment
The existing causal-bundle lifecycle SHALL expose an executable research
treatment surface by importing the same research coordinator used by the book
pipeline, not by creating a second research runner or campaign. A research
experiment SHALL declare its research hypothesis and exact changed research
bundle, freeze subject/input, model, planning, commission, writing, safety, and
evaluation variables, and prepare isolated control and treatment RF-02 candidate
roots. Both arms SHALL pass the production research preflight and produce
current research seals before comparative judgment. Fake transports or native
test editors MUST remain import-only test seams and MUST NOT be selectable by
the production or causal command surface. The control's research prompt,
evidence-editor prompt, and research configuration bytes SHALL still equal
their accepted RF-02 snapshot before either arm dispatches and when the final
gate revalidates the decision. Preflight, accepted-baseline verification, and
completed-run lookup MAY inspect `CANDIDATE` or `SEALED` arms read-only; every
research execution or mutation route MUST remain `CANDIDATE`-only.

Research-source eligibility, privacy, safety, originality, traceability,
scientific lineage, inference bounds, deduplication, belief/persona/slot
coverage, and independent evidence judgment SHALL be hard gates rather than
reward dimensions. Comparison, when used, SHALL be anonymous, independent, and
task-hash-bound. A downstream chapter or book effect SHALL be bound only when
the research hypothesis preregisters it as necessary, and SHALL compare exact
anonymous downstream outputs from both current sealed arms under identical
frozen planning, commissioning, writing, model, input, safety, and evaluation
processes. A one-arm product PASS or status snippet MUST NOT count as a paired
effect. Promotion remains one atomic named-human decision under the existing
RF-02 gate, with an explicit named-human receipt bound to the tested pair,
causal record, evidence, and both research seals.

#### Scenario: A research treatment is prepared for isolated comparison
WHEN the existing causal command receives a declared research hypothesis and
one exact research-only changed bundle
THEN it MUST create isolated control and treatment RF-02 roots from identical
subject/input/model/planning/commission/writing/safety/evaluation and independent
evidence-editor hashes
AND it MUST call the same non-injectable production preflight and research
facade as the standalone `start` route
AND only the declared research-agent prompt may differ
AND neither arm may change the independent evidence-editor contract that hard-gates it
AND both arms MUST carry valid research seals and pass every research hard gate
before a blind independent research-quality or reader/belief-coverage comparison
can be accepted
AND the blind judge SHALL return only anonymous side preference or tie plus its
reason; deterministic code SHALL map `B`, `A`, or `TIE` to supported, refuted,
or inconclusive only after judgment
AND a preregistered downstream effect MUST be evaluated before accepting the
research change when the hypothesis depends on that effect
AND the decision gate MUST recompute current control-baseline identity, both
sealed research candidates, hard gates, blind comparison, and any paired
downstream comparison before recording or promoting the result.

#### Scenario: A writing treatment is prepared
WHEN the declared changed bundle owns planning, commission, writing, or revision
rather than research
THEN both arms MUST bind the same exact accepted research seal
AND any research byte, seal, assignment, or coverage difference MUST reject the
purported writing experiment as confounded.

#### Scenario: A purported causal decision mixes research and writing changes
WHEN one changed bundle alters research and any planning, commission, writing,
revision, model, input, safety, or evaluation variable
THEN the run MUST fail schema/preflight validation before dispatch
AND research and writing changes MAY be optimized only in separate causal runs.

#### Scenario: Research causal readiness is verified without starting a run
WHEN RF-32 proves the research treatment surface offline
THEN it MUST use captured no-network transports and isolated temporary fixtures
without invoking the real campaign entrypoint
AND it MUST NOT append a causal result, make a control/treatment decision,
promote research or product, mutate accepted production, create an H-F01
authority or artifact, move RF-21 or a later READY stage to `IN_PROGRESS`, or
perform a provider, account, credit, eligibility, Muse, DeepSeek, or OpenRouter
call
AND the real production and causal routes without the environment key and later
explicit founder start MUST stop before writes, network, or native dispatch.

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

#### Scenario: Windows immutable authority uses native durable identity
WHEN a final immutable authority file is validated on Windows
THEN it MUST be a regular, single-link, non-reparse file with the native
read-only attribute set
AND validation MUST NOT depend on distinctions among POSIX read-only submodes
that Windows does not preserve
AND stable handle/path identity MUST compare device, file identity, mode, link
count, size, and modification time plus the bound bytes and hashes
AND MUST NOT reject an unchanged file because NTFS reports different change
times through path and open-handle metadata.

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

#### Scenario: H-F01 reaches the atomic gate boundary
WHEN the coordinator has frozen the product decision and causal record
THEN it MUST emit the existing RF-02 gate continuation with the unified integer
Carr/gate iteration, exact sealed treatment hash, exact accepted root, and a
pinned UTC decision timestamp
AND a `PROMOTE` decision MUST additionally require explicit promotion authority
AND the coordinator MUST describe the candidate only as awaiting or having an
emitted gate command until that atomic gate actually succeeds.

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

#### Scenario: H-F01 blind decision is recomputed
WHEN both H-F01 arms have passed all-six grounded, near-copy, and whole-opening
review and are sealed
THEN frozen evidence MUST bind both sealed arm hashes, exact GSBS file hashes,
ordinary control/treatment absolute diagnostic tasks, three anonymous
treatment-versus-offset-matched-GSBS chapter panels, and one anonymous
treatment-versus-GSBS whole-opening panel
AND each panel MUST use the same two fresh reader identities with opposite A/B
order and an envelope-bound mapping from anonymous choice to treatment support
AND the six absolute plus eight GSBS native task/result records MUST bind the
pre-RF21 authority, task/input/output, route, reasoning, command, and thread
AND a pre-call marker without a durable result MUST stop as ambiguous rather
than replay
AND support MUST require at least five of six treatment-over-GSBS chapter votes
plus both treatment-over-GSBS whole-opening votes
AND material disagreement MUST be `INCONCLUSIVE`
AND control/treatment observations MUST remain a separately named causal
diagnostic rather than a parity result
AND a named-human approval bound to both arms, GSBS, blind evidence, and Carr
evidence MUST be present after those receipts and before promotion.

#### Scenario: Reference diagnostic follows blind freeze
WHEN H-F01 requires the reference-sighted Carr craft diagnostic
THEN an immutable receipt for the complete blind task and verdict set MUST exist
first
AND the six fresh native Carr task/result records MUST bind that authority and
blind receipt plus exact model, route, reasoning, command, and thread identity
AND an interrupted Carr call without a durable result MUST stop as ambiguous
AND the diagnostic MUST NOT alter or decide the blind evidence.

#### Scenario: A candidate is too close to the matched reference
WHEN isolated word-sequence comparison crosses the near-copy tripwire
THEN the candidate MUST fail integrity
AND no preference, reader-effect, or craft score may override that failure.

### Requirement: Blind and independent judgment
Reader-effect and sequence evaluators SHALL remain blind to condition identity,
text provenance, reference-as-ground-truth context, historical scores, and judge
verdicts. Reference prose SHALL NOT enter ordinary product experiments. Direct
GSBS Stage A is the sole declared exception: an evaluator receives the exact
offset-matched GSBS text only as one anonymous A/B candidate, with its identity,
hashes, and treatment-support mapping kept outside the judge payload.

The paired instrument SHALL receive exactly one task containing anonymous A/B
content with exact fields `schema`, `instrument: blind-product-effect`, `mode`,
`subject`, `fresh_context: true`, `candidates`, and `task_sha256`. Its task hash
SHALL bind that exact content, and its verdict SHALL emit exactly `schema`,
`task_sha256`, `mode`, `preferred`, `confidence`, and `decisive_reason`. It SHALL
make no independent absolute, sufficiency, sequence, or link observation. It
SHALL select a side only for a material relative difference in enacted causal
effect and SHALL return `TIE` when neither side has a clearly stronger enacted
path, including when both are similarly strong or similarly weak.

The absolute instrument SHALL receive exactly one content task with exact fields
`schema`, `instrument: blind-product-effect-absolute`, `mode`, `subject`,
`fresh_context: true`, `chapters`, and `task_sha256`; chapter mode SHALL contain
exactly one chapter and whole-opening mode at least two. Its verdict SHALL contain
only `schema`, `task_sha256`, `mode`, `observation`, and `confidence`. Chapter
sequence links SHALL all be `NOT_APPLICABLE`. Neither a chapter nor a whole
opening SHALL `MEET` with unresolved belief work. Whole-opening links SHALL use
only `ABSENT`, `PARTIAL`, or `CLEAR`; a downstream `CLEAR` SHALL be enacted after
and from a non-`ABSENT` prerequisite; and the opening SHALL `MEET` if and only if
all three links are `CLEAR`.

Each task and envelope SHALL reject missing, extra, contradictory, or stale
fields and hashes. An absolute envelope SHALL keep scope, stable content ID,
content hash, and tested-pair binding outside the judge payload. Calibration
envelopes SHALL be non-promotable with a null tested-pair hash; ordinary
envelopes SHALL require a sealed tested-pair hash. The two task and verdict
schemas SHALL never cross-validate. Both rubric files SHALL be sealed among the
candidate's evaluation inputs.

H-F04 MAY submit a matched reference chapter or opening only as an anonymous,
unlabeled, non-promotable diagnostic. The evaluator MUST NOT receive its identity
or provenance, and neither reference text nor any calibration verdict may flow
into generation. Correcting either instrument starts a new calibration lineage.

#### Scenario: H-F04 calibrates on a reference-as-candidate
WHEN a matched reference chapter or opening is submitted to the blind instrument
THEN it MUST be anonymized, isolated from generation and promotion, and recorded
only as calibration evidence
AND neither its text nor verdict may flow into research, framing, planning,
commissioning, writing, review, or revision.

#### Scenario: One-content absolute assessment is strict
WHEN a chapter or whole opening is submitted to the absolute instrument
THEN its task, envelope, and verdict MUST have exact fields and current hash
bindings
AND chapter sequence links MUST be `NOT_APPLICABLE`
AND whole-opening sufficiency MUST be `MEETS` if and only if all links are
`CLEAR`, with downstream `CLEAR` enacted after and from its prerequisite
AND missing, extra, overlong, mode-inapplicable, stale, or contradictory fields
MUST fail closed.

#### Scenario: Paired comparison stays comparison-only
WHEN two anonymous contents are submitted to the paired instrument
THEN its verdict MUST contain preference, confidence, and one decisive relative
reason but no absolute observation, sufficiency, or link fields
AND no material enacted-effect difference MUST produce `TIE`
AND an absolute verdict MUST be rejected by the paired contract.

#### Scenario: Split verdicts do not cross-validate
WHEN a paired verdict is submitted to the absolute contract or an absolute
verdict is submitted to the paired contract
THEN exact schema validation MUST reject it.

#### Scenario: A failed calibration lineage remains terminal
WHEN frozen calibration evidence fails a preregistered terminal control gate
THEN that lineage MUST remain a terminal `FAIL` without retry, relaxation,
reinterpretation, or continuation
AND no product run may start from that lineage
AND further calibration MUST use a newly founder/root-approved hypothesis and
control lineage.

#### Scenario: Evaluator disagreement is too large
WHEN repeat variance or evaluator disagreement is comparable to the intended
treatment effect
THEN the instrument MUST be recalibrated
AND it MUST NOT make a promotion decision until its reliability is established.

### Requirement: Minimal experiment record
Each run SHALL record only its hypothesis and causal chain, linked change set,
frozen variables, input hashes or commits, grounded audit result, blind chapter
result, blind sequence result, reference-sighted diagnostic, decision, and
falsification outcome. A materially changed instrument, model, threshold, or
campaign contract SHALL begin a new results lineage; rewards from different
lineages MUST NOT be compared numerically.

The final H-F01 record MUST reproduce the preregistered hypothesis, causal chain,
changed bundle, frozen variables, exact inputs, and falsifier byte-for-byte apart
from decision-derived input and evidence bindings added by the frozen decision.

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

### Requirement: Founder validation ladder
The factory MUST NOT claim complete-book or zero-tuning reliability from three
sugar chapters. Stage A SHALL test the quit-sugar opening directly against GSBS;
Stage B SHALL test the complete quit-sugar book at parity; only after Stage B
passes SHALL Stage C test untouched caffeine with zero tuning.

#### Scenario: Opening success is described narrowly
WHEN the sugar H-F01 opening passes
THEN the result SHALL be described as support for the tested handoff hypothesis
AND NOT as proof of complete-book or zero-tuning reliability.

#### Scenario: The founder validation ladder advances
WHEN direct GSBS Stage A passes every product and human gate
THEN Stage B SHALL test complete quit-sugar book parity
AND only after Stage B passes SHALL Stage C test untouched caffeine with zero
tuning.
