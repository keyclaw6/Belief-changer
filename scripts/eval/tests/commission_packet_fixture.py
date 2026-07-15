"""Accepted source-packet fixture with exact excerpt and evidence metadata."""


def packet(source, item, marker):
    return f"""# {source} — Fixture
- **Source ID:** {source}
- **URL:** https://example.test/{source.lower()}
- **Title:** Fixture source {source}
- **Source type:** report
- **Retrieved (UTC):** 2026-07-15T00:00:00Z
- **Access / license basis:** fixture text may be retained
- **Required attribution:** fixture
- **Retention / deletion status:** stable fixture; no deletion duty
- **Privacy judgment:** no personal data
- **Disposition:** ACCEPTED
## Minimum retained excerpt
### C-001
- **Locator:** fixture paragraph
- **Capture method:** fixture text

```text
{marker}
```
## Evidence items
### {item}
- **Kind:** INTERPRETATION
- **Text:** {marker}
- **Excerpt ID:** C-001
- **Locator:** fixture paragraph
- **Persona tags:** ALL
- **Bank slots:** Bank 1
- **Evidence grade:** SUPPORTED
- **Use / limits:** supports only this bounded fixture statement
"""
