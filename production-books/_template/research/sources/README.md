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
````

Add only the excerpts and evidence items genuinely needed. If exact wording
cannot be verified, recapture it, convert it to an unquoted interpretation, or
reject it. State the exact bounded permitted and prohibited inference wording in
`Use / limits` before an intervention unit may reuse it; an inference is not a
quotation.
