# Source Packets

Store one Markdown packet per distinct accepted URL, named
`<source-id>-<descriptive-slug>.md`. Repeated use enriches the same packet.
Rejected material never becomes a packet. The log may retain only a policy-level
source-family rejection reason, never its URL, excerpt, source ID, or personal data.

Before retaining content, establish access, excerpt, retention, redistribution,
attribution, and privacy rights. Packets contain only the minimum permitted excerpt
for evidence—not full community posts, bulk user dumps, profiles, or unrelated
personal data. Deletion-sensitive or nonredistributable user content stays out
of Git and does not count as evidence coverage. Do not create a packet for
rejected material.

A search summary may guide discovery but is not evidence. An exact quote is
usable only when it appears character-for-character in the retained excerpt.

## Packet schema

````markdown
# S-001 — <Source title>

- **Source ID:** S-001
- **URL:** <canonical URL>
- **Title:** <page, paper, report, thread, or transcript title>
- **Source type:** <community | study | report | transcript | investigative>
- **Retrieved (UTC):** <YYYY-MM-DDTHH:MM:SSZ>
- **Discovery lane:** <LIVED_EXPERIENCE | SCIENCE_MECHANISM | INDUSTRY_CULTURE | COUNTER_CORPUS | DIALECT_SENSORY>
- **Source family:** <specific source family used for aggregate rejection/diversity accounting>
- **Author / organization:** <author or responsible organization used for diversity accounting>
- **Fetched URL:** <canonical URL actually fetched; must match URL>
- **Fetched content SHA-256:** <sha256 of the captured fetched content>
- **Corroboration count:** <positive integer; duplicates raise this without adding coverage>
- **Story identity:** <stable non-identifying story key, or n/a>
- **Study lineage:** <stable underlying-study key, or n/a>
- **Study design / class:** <design/class for scientific material, or n/a>
- **Deletion sensitivity:** NOT_DELETION_SENSITIVE
- **Personal-data retention:** <NONE | MINIMAL_REQUIRED_ATTRIBUTION>
- **Access / license basis:** <why access is permitted and the governing license or basis>
- **Excerpt / redistribution basis:** <why this minimum excerpt may be committed publicly>
- **Required attribution:** <author/organization/handle if required; otherwise n/a>
- **Retention / deletion sensitivity:** <why retention is permitted and whether deletion sensitivity exists>
- **Privacy / personal-data basis:** <why the minimum retained text and identifiers are appropriate>
- **Disposition:** ACCEPTED

## Minimum retained excerpt

### C-001

- **Locator:** <page, heading, paragraph, timestamp, or equivalent>
- **Capture method:** <page text | transcript | PDF text | permitted exact snippet>
- **Content SHA-256:** <sha256 of the exact retained excerpt text below>

```text
<minimum unchanged passage needed to support the evidence items>
```

## Evidence items

### E-001

- **Kind:** EXACT_QUOTE | INTERPRETATION
- **Text:** <verbatim wording or an unquoted interpretation>
- **Excerpt ID:** C-001
- **Locator:** <precise locator>
- **Persona tags:** <P-01, ... | ALL>
- **Bank slots:** <Bank 1, ...>
- **Evidence grade:** SUPPORTED | MIXED | CONTESTED | n/a
- **Use / limits:** <what this supports and what it does not establish>
- **Brief beliefs:** <exact brief belief | another exact brief belief>
- **Style slots:** <canonical slot ID | another canonical slot ID>
- **Safety relevance:** <exact brief safety perimeter when applicable, otherwise NONE>
- **Situation:** <concrete situation this evidence supports>
- **Emotion:** <exact emotion or body-state this evidence supports>
- **Grade rationale:** <why the grade fits this exact claim>
- **Scope:** <population, setting, design, and transfer limits>
- **Counterevidence:** <material disagreement or the bounded reason none applies>
- **Permitted inference:** <exact bounded inference available to synthesis and units>
- **Prohibited inference:** <exact inference the source does not permit>
- **Testimonial qualification:** <NOT_CANDIDATE | QUALIFIED; numbers=...; sensory=...; authority_conflict=...>
````

Add only the excerpts and evidence items genuinely needed. If exact wording
cannot be verified, recapture it, convert it to an unquoted interpretation, or
reject it. State the exact bounded permitted and prohibited inference wording in
`Use / limits` before an intervention unit may reuse it; an inference is not a
quotation.

Canonical style-slot IDs are `LOAD_BEARING_BELIEF`, `INVERSION`,
`JUSTIFICATION_MENU`, `ENGINEERED_VILLAIN`, `SCIENCE_WEIGHT`,
`ROOT_DIRECTION`, `ANALOGY_SET`, `ESCAPE_ROUTES`, `SEDUCTIVE_SCENE`,
`REVELATION`, `SENSORY_DIALECT`, `MANTRA_SEEDS`, `TESTIMONIAL`, and
`EVIDENCE_LEDGER`.
