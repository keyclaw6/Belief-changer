# Source Packets

Store one Markdown packet per distinct accepted URL, named
`<source-id>-<descriptive-slug>.md`. Repeated use enriches the same packet.
Rejected sources stay in `../research-log.md` rather than becoming packets.

Before retaining content, establish access, excerpt, retention, redistribution,
attribution, and privacy rights. Packets contain only the minimum passage needed
for evidence—not full community posts, bulk user dumps, profiles, or unrelated
personal data. Deletion-sensitive or nonredistributable user content stays out
of Git and does not count as run evidence.

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
- **License / quotation basis:** <source license or documented legal basis>
- **Required attribution:** <author/organization/handle if required; otherwise n/a>
- **Retention / deletion status:** <why this excerpt can remain in public Git>
- **Privacy judgment:** <why retained text/identifiers are necessary and appropriate>
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
reject it.
