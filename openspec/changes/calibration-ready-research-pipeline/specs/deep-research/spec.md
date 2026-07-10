## ADDED Requirements

### Requirement: Model-led multi-agent research
Research SHALL be led by a fresh top-reasoning research model that chooses its
own decomposition, personas, source families, searches, tools, delegation,
recursion, and stopping decisions. The lead MUST delegate substantive work to
multiple fresh-context subagents when independent exploration improves depth,
and MAY add, redirect, or retire subagents at any time. The repository schemas
are evidence outputs, not a prescribed workflow; no caller, prompt, framework,
matrix, or deterministic program may impose a scout→worker→specialist sequence
or require pre-collection row filling.

#### Scenario: Research begins
- **WHEN** a filled brief enters research
- **THEN** the lead receives the research prompt and blind brief and organizes the research itself
- **THEN** the caller does not prescribe roles, search order, persona count, assignment count, or recursion depth

#### Scenario: The lead discovers a gap
- **WHEN** evidence is thin, contradictory, or misses a materially distinct reader
- **THEN** the lead commissions whatever fresh specialist or retrieval work it judges most likely to close the gap

### Requirement: Independent blind research sources
Research agents SHALL use lived-experience, scientific, and investigative
sources independent of the calibration reference. They MUST NOT receive or use
reference books, files under `analysis/`, calibration reference text, judge
outputs, Allen Carr/Easyway derivatives, prose-pattern analyses, or prior book
prose. The exact-input brief MUST contain only product facts and MUST NOT contain
reference identity or paths, aggregate reference targets, or run instructions.

#### Scenario: A forbidden source or input appears
- **WHEN** an agent receives or returns reference-derived or Easyway-derived research material
- **THEN** the material and every dependent finding are rejected before synthesis

#### Scenario: A search result names a possible source
- **WHEN** only a search summary or model recollection is visible
- **THEN** it may guide discovery but does not count as evidence or an exact quotation

### Requirement: Rights-safe and privacy-safe evidence
An accepted source SHALL have a documented access, excerpt, retention,
redistribution, attribution, and privacy basis compatible with the repository's
`CC-BY-SA-4.0` content scope. Discovery MAY inspect ordinary public metadata and
source policies, but evidence MUST NOT be captured, retained, synthesized, or
counted until that basis passes. Research MUST NOT evade access controls,
security challenges, rate limits, or source terms.

Public Git MUST NOT contain full community posts, bulk user dumps, private or
sensitive identity mappings, or deletion-sensitive/nonredistributable user
content. The run uses only the minimum excerpt needed for evidence, minimizes
identifiers except where lawful attribution requires them, and records the
source's own license or other quotation basis. No external evidence store is
introduced for run-001; material needing one remains outside Git and outside run
evidence.

#### Scenario: Source terms require deletion or forbid redistribution
- **WHEN** a source cannot support the retained excerpt and provenance contract
- **THEN** it is rejected and does not contribute to a bank or synthesis

#### Scenario: A source contains first-person experience
- **WHEN** an excerpt is otherwise permitted
- **THEN** the packet retains only the necessary passage and locator, applies the required attribution, and excludes unrelated identifiers or profile data

#### Scenario: Reddit is proposed
- **WHEN** the run lacks documented Reddit authorization covering access, retention, and output
- **THEN** Reddit and Reddit-derived evidence are excluded without a browser, feed, snippet, or stealth workaround

### Requirement: Lean provenance records
Every accepted URL SHALL have one packet under `research/sources/` containing a
stable source ID, URL, title, retrieval date, source type, rights/privacy basis,
required attribution, minimum retained excerpt, precise locator, and evidence
items tagged by persona and bank. Repeated use of a URL SHALL enrich that packet
rather than duplicate it. `research/research-log.md` MUST record model calls,
meaningful search/source decisions, rejected source families, and exact runtime
model/reasoning/allowance metadata without duplicating that metadata in every
bank cell or prescribing the model's process.

#### Scenario: Wording is labeled as an exact quote
- **WHEN** an evidence item claims exact wording
- **THEN** it appears character-for-character in the retained excerpt and carries a locator

#### Scenario: Exact wording cannot be verified
- **WHEN** wording is absent or altered
- **THEN** it is recaptured, converted to an unquoted interpretation, or rejected

### Requirement: Model-judged bank sufficiency
The lead SHALL fill all ten style-guide research banks deeply enough to support
belief-changing framing and planning across every materially distinct persona it
discovers. The lead chooses its own working targets and MUST report final source,
quote, persona, and bank coverage. Counts are diagnostics, not stopping quotas:
duplicate sources, unsupported interpretations, and weak filler do not establish
sufficiency, while a fixed numeric matrix MUST NOT force artificial work.

#### Scenario: A bank has many weak items
- **WHEN** volume is high but the material is generic, repetitive, or misses the strongest reader objection
- **THEN** the bank remains insufficient and the lead performs deeper research

#### Scenario: One persona remains thin
- **WHEN** aggregate research is strong but a materially distinct persona lacks specific evidence
- **THEN** research continues for that persona before final acceptance

### Requirement: Traceable synthesis and independent review
The lead SHALL synthesize accepted packets into `research/lived-experience.md`
for Banks 1–6, 9, and 10 and `research/scientific-evidence.md` for Banks 7–8.
Every synthesized item MUST name source IDs; lived evidence MUST carry persona
tags and scientific evidence MUST carry `SUPPORTED`, `MIXED`, or `CONTESTED`.
After synthesis, one fresh allowed top-reasoning reviewer SHALL receive the blind
brief, prompt, log, packets, and both syntheses and judge substantive depth,
rights/privacy compliance, provenance, bank coverage, and usefulness for belief
change. It either accepts the research or commissions/regenerates the missing
work; the operator does not patch evidence by hand.

#### Scenario: Synthesis contains an untraceable claim
- **WHEN** an item cannot be traced to an accepted packet
- **THEN** the reviewer rejects it and framing remains blocked

#### Scenario: Scientific sources disagree
- **WHEN** credible evidence materially conflicts
- **THEN** the synthesis preserves the disagreement as `CONTESTED`

### Requirement: Unrestricted quality and reconstructable arms
Every research model SHALL run at its highest supported reasoning mode and with
the greatest completion allowance actually authorized for that call after input
context. The caller MUST request the endpoint maximum first when the API permits
it, use an exact provider/key ceiling rather than an arbitrary lower cap when
required, and continue agentically whenever `finish_reason=length`. Research
MUST NOT be stopped, narrowed, ranked, or selected because of cost, tokens,
latency, wall time, search count, or subagent count.

Every arm MUST record the requested and actual model IDs, reasoning setting,
requested/authorized allowance, finish reason, usage/cost when available, chosen
strategy, accepted sources, verified quotes, bank/persona coverage, and rejected
yield. Comparisons hold the blind objective and quality bar fixed while each arm
chooses its own method, and rank only evidence depth, insight, fidelity, rigor,
coverage, and synthesis quality.

#### Scenario: The key authorizes less than the endpoint maximum
- **WHEN** the endpoint rejects its theoretical maximum and returns a lower exact allowance
- **THEN** the caller uses that greatest available allowance, records the ceiling, and does not reduce the research objective

#### Scenario: An OSS framework is proposed
- **WHEN** a framework would replace prompt-structured delegation
- **THEN** it is adopted only after a same-objective trial proves a research-quality or reliability gain without prescribing model reasoning or breaking the file contract
