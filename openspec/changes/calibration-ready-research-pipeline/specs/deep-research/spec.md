## ADDED Requirements

### Requirement: Structured research decomposition
Research SHALL use a fresh-context agentic council with at least four separate architecture specialists: persona discovery, community discovery, scientific-source mapping, and investigative-source mapping. Specialists receive only the research prompt, filled brief, and one focus assignment; the architecture lead receives only the prompt, brief, and visible specialist artifacts; the architecture reviewer receives only the prompt, brief, and complete candidate architecture; collection workers receive only the prompt, brief, and one approved assignment; and the synthesis lead receives only the prompt, brief, approved research log, and accepted packets. No role receives hidden reasoning or unrelated agent context. The lead records a community × persona × bank-slot coverage matrix before collection and commissions targeted follow-ups for uncovered cells. Assignment focus defines responsibility, not a token, output, search, time, subagent, or spend limit.

#### Scenario: Research begins
- **WHEN** a book with a filled brief enters research
- **THEN** the lead records communities, provisional personas, bank-slot assignments, numeric targets, and worker IDs before any broad synthesis

#### Scenario: A worker receives an unfocused task
- **WHEN** a proposed worker assignment omits its community/source scope, persona scope, or bank slots
- **THEN** the assignment is rejected and narrowed before the worker runs

#### Scenario: A matrix row relies on shorthand or an excluded population
- **WHEN** a row says `same`/`as above`, names an unverified community, or uses a population excluded by the brief's non-goals
- **THEN** the lead repeats all required fields or replaces the scope before collection

#### Scenario: A matrix row groups banks or fallback scopes
- **WHEN** a row contains more than one bank, more than one community/source family, or an implicit fallback scope
- **THEN** the lead splits it into independently dispatchable one-bank, one-scope rows before collection

#### Scenario: A no-web lead proposes a named community
- **WHEN** the first lead call cannot retrieve and verify the community
- **THEN** its rows remain `CANDIDATE — VALIDATION REQUIRED`
- **THEN** a retrieval-capable lead pass verifies the canonical URL and topical fit before the rows become `READY`

#### Scenario: A lead interprets source floors as community floors
- **WHEN** a bank requires items from two or more sources
- **THEN** sources mean distinct underlying URLs/documents within the focused assignment
- **THEN** the lead does not duplicate every matrix cell across communities before observing a coverage gap

#### Scenario: Persona segmentation is capped for efficiency
- **WHEN** the lead or caller considers excluding a materially distinct persona to reduce calls, tokens, output length, time, or cost
- **THEN** the persona remains in scope and receives the research needed for equal qualitative sufficiency

### Requirement: Independent research sources
Research workers SHALL use lived-experience communities and scientific or investigative sources, and MUST NOT receive or use reference books, files under `analysis/`, calibration reference text, judge outputs, Allen Carr/Easyway derivatives, or prose-pattern analyses. Search-result summaries MAY guide discovery but MUST NOT be treated as verbatim evidence unless their exact returned excerpt is saved.

The exact-input brief MUST contain only product facts and MUST NOT contain reference identity/paths, aggregate reference targets, or calibration run instructions.

#### Scenario: A forbidden source appears
- **WHEN** a worker returns an Easyway-derived source or any reference/analysis material
- **THEN** the source and every dependent finding are rejected and the affected coverage cells remain unfilled

#### Scenario: A brief leaks calibration metadata
- **WHEN** a role's brief names the reference, a reference/calibration path, a reference-derived aggregate, or run instructions
- **THEN** the caller rejects the brief and removes that metadata before dispatch

### Requirement: Provenance-preserving source packets
Every distinct accepted URL SHALL have one source packet under `research/sources/`, and every search/call/source capture MUST be recorded in `research/research-log.md`. A packet MUST record a stable source ID, URL, title, retrieval date, community/source type, query and assignment ID, model and reasoning configuration, captured raw excerpt or text, and evidence items tagged by persona and bank slot.

#### Scenario: A worker captures a quote
- **WHEN** wording is labeled as an exact quote
- **THEN** the wording appears verbatim in the packet's captured source text and carries a source locator

#### Scenario: A quote cannot be verified
- **WHEN** returned wording cannot be found verbatim in captured source text
- **THEN** it is recaptured, converted to an explicitly labeled interpretation without quotation marks, or rejected

#### Scenario: The same URL is revisited
- **WHEN** another assignment yields evidence from an already accepted URL
- **THEN** the existing packet is enriched and the new visit is logged instead of creating a duplicate source file

### Requirement: Measurable bank sufficiency
The lead SHALL declare numeric coverage targets before research and MUST require both those targets and the qualitative sufficiency tests in the research prompt to pass. Every selected persona MUST pass its applicable targets; duplicate sources or unsupported interpretations MUST NOT count toward coverage.

#### Scenario: A numeric target is met with weak material
- **WHEN** a bank reaches its item count but fails the prompt's qualitative sufficiency test
- **THEN** the bank remains incomplete and the lead commissions a targeted follow-up

#### Scenario: One persona is underrepresented
- **WHEN** any selected persona fails an applicable bank target
- **THEN** research MUST NOT close even if aggregate item counts are high

### Requirement: Complete two-file synthesis
The lead SHALL synthesize accepted source packets into `research/lived-experience.md` for Banks 1–6, 9, and 10 and `research/scientific-evidence.md` for Banks 7–8. Every synthesized bullet MUST name its bank and source IDs; lived evidence MUST carry persona tags, and scientific evidence MUST carry SUPPORTED, MIXED, or CONTESTED.

#### Scenario: Synthesis contains an untraceable bullet
- **WHEN** a synthesized bullet lacks accepted source IDs or cannot be traced to their packets
- **THEN** the bullet is removed or re-sourced before framing begins

#### Scenario: A contested claim is synthesized
- **WHEN** sources materially disagree on a scientific claim
- **THEN** the claim is tagged CONTESTED and the disagreement is preserved rather than averaged away

### Requirement: Unrestricted agentic quality review
Every research model SHALL run at its highest supported reasoning mode with the maximum completion/output allowance available from the selected endpoint after input context. Research MUST NOT be stopped, narrowed, ranked, or selected because of tokens, cost, latency, wall time, search count, or subagent count. Before worker dispatch and before final synthesis, a fresh allowed top-reasoning reviewer SHALL audit the complete artifact and either approve it or return a complete corrected artifact; deterministic code MUST NOT plan, render, or validate the research reasoning path.

#### Scenario: A model approaches a provider output ceiling
- **WHEN** a research role reaches or may reach the selected endpoint's completion ceiling
- **THEN** the caller continues the work agentically or selects a larger-capacity endpoint
- **THEN** the caller does not shorten the research task or lower its quality target

#### Scenario: A lead self-certifies a weak architecture
- **WHEN** a candidate architecture claims compliance but contains weak personas, communities, source scopes, queries, or assignments
- **THEN** a fresh top-reasoning research reviewer regenerates the complete artifact or commissions another specialist
- **THEN** the operator does not repair the artifact by hand or replace model judgment with a deterministic validator

### Requirement: Reconstructable research-arm measurement
Every research arm SHALL record the exact runtime model ID, highest supported reasoning configuration, maximum output allowance, substantive objective, chosen strategy/search settings, usage and cost when available, accepted sources, verified quotes, filled bank/persona cells, and rejected or unverifiable items. Model or orchestration comparisons MUST hold the blind brief, substantive objective, exclusions, access, and quality bar fixed while allowing every arm to choose whatever reasoning path, searches, tools, and agentic follow-ups maximize quality.

The caller MUST verify endpoint metadata before dispatch, record request/response metadata after the call, and persist artifact-ready role output when the role has no direct filesystem access. A research role MUST NOT treat its inability to inspect invisible request metadata or write directly to the caller's filesystem as a research blocker.

#### Scenario: A bare model call cannot inspect its request
- **WHEN** an approved research role runs without direct endpoint-metadata or repository-write tools
- **THEN** the caller supplies the verified request configuration, records actual response metadata, and persists the role's returned artifact blocks
- **THEN** the role continues its assigned planning or collection work

#### Scenario: Research models are compared
- **WHEN** H-009 compares two allowed researcher models
- **THEN** the report separates raw-yield measures from synthesis quality and ranks only community/persona coverage, source depth, verified evidence, insight, scientific rigor, and synthesis quality
- **THEN** usage, cost, and latency are descriptive metadata and do not influence the winner

#### Scenario: An OSS framework is proposed for adoption
- **WHEN** H-011 proposes replacing prompt-structured handoffs
- **THEN** adoption is rejected unless a same-blind-objective comparison shows a measurable quality gain in depth, coverage, provenance, insight, or orchestration reliability without breaking the file contract or replacing model judgment
