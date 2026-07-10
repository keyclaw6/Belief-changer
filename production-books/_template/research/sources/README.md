# Source Packets

Store one Markdown packet per distinct **accepted URL** in this folder. Name it `<source-id>-<descriptive-slug>.md` (for example, `s-001-community-thread.md`). A repeat visit enriches the existing packet and gets a new research-log row; it never creates a duplicate packet. Rejected or unverifiable sources remain in `../research-log.md` with their disposition.

Search summaries may guide discovery, but they are not evidence unless the exact returned excerpt is preserved below. An exact quote is valid only when its wording appears verbatim in a captured block and its evidence item links that capture and locator.

Before retrieval, verify that the access method, automation, excerpt use, durable retention, deletion handling, and redistribution of packet content are permitted. Do not store a source whose terms require ungranted approval or conflict with an open Git repository.

## Source packet schema

````markdown
# S-001 — <Source title>

- **Source ID:** S-001
- **URL:** <canonical URL>
- **Title:** <page, thread, paper, transcript, or report title>
- **Retrieved (UTC):** <YYYY-MM-DDTHH:MM:SSZ>
- **Community / source type:** <community and platform | study | report | transcript | investigative source>
- **Access / retention basis:** <permission, license, and current policy URL/version>
- **Deletion / refresh obligations:** none — otherwise this source cannot become a repository packet; an approved alternative storage design must remain outside durable Git
- **Query ID:** Q-001
- **Assignment ID:** A-001
- **Worker ID:** W-001
- **Runtime model ID:** <exact provider/model returned at runtime>
- **Reasoning config:** <highest supported exact request setting>
- **Maximum output allowance:** <endpoint maximum after input context>
- **Search settings:** <engine, filters, date range, limits>
- **Research-log event IDs:** <L-001, ...>
- **Disposition:** ACCEPTED

## Visit history

| Retrieved UTC | Assignment / worker | Query ID / query | Runtime model / reasoning / max output | Search settings | Capture IDs | Log event ID |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## Captured raw source text

### C-001

- **Retrieved (UTC):** <YYYY-MM-DDTHH:MM:SSZ>
- **Source locator:** <heading, paragraph, post, page, timestamp, or returned-snippet position>
- **Capture method:** <page text | transcript | PDF text | exact search excerpt>

```text
<unaltered raw excerpt or captured text>
```

## Evidence items

### E-001

- **Evidence ID:** E-001
- **Kind:** EXACT_QUOTE | INTERPRETATION
- **Text:** <verbatim wording found in the linked capture, or an unquoted interpretation>
- **Capture ID:** C-001
- **Locator:** <precise heading, paragraph, post, page, or timestamp>
- **Persona tags:** <P-01, ...>
- **Bank slots:** <Bank 1, ...>
- **Evidence grade:** <SUPPORTED | MIXED | CONTESTED | n/a>
- **Use / limits:** <what this supports and what it does not establish>
````

Add capture and evidence-item blocks as needed. Every item must carry persona and bank tags; never move an unverifiable quote into either synthesis.
