"""Extract only exact assigned locator records from mixed source packets."""
import re

import pair_store as PS

LOCATOR = re.compile(r"^(S-\d{3})#(E-\d{3})$")
FIELD = re.compile(r"^- \*\*(.+?):\*\*\s*(.*)$")
REQUIRED_EVIDENCE = {"Kind", "Text", "Excerpt ID", "Locator", "Persona tags",
                     "Bank slots", "Evidence grade", "Use / limits"}


class EvidenceError(RuntimeError):
    pass


def _fields(text):
    values, current = {}, None
    for line in text.splitlines():
        match = FIELD.match(line)
        if match:
            current, value = match.groups()
            if current in values:
                raise EvidenceError(f"duplicate packet field: {current}")
            values[current] = value.strip()
        elif not line.strip():
            current = None
        elif current and line.strip() and not line.startswith(("#", "```", ">")):
            values[current] = f"{values[current]} {line.strip()}".strip()
    return values


def _section(text, heading):
    pattern = re.compile(rf"^###\s+{re.escape(heading)}\s*$", re.M)
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise EvidenceError(f"packet locator section {heading} is missing or ambiguous")
    following = re.search(r"^###\s+\S", text[matches[0].end():], re.M)
    end = matches[0].end() + following.start() if following else len(text)
    return text[matches[0].start():end].strip()


def _excerpt_text(section):
    fence = re.search(r"```(?:text)?\s*\n(.*?)\n```", section, re.S)
    if fence:
        return fence.group(1)
    quoted = [re.sub(r"^>\s?", "", line) for line in section.splitlines()
              if line.startswith(">")]
    if quoted:
        return "\n".join(quoted)
    raise EvidenceError("assigned excerpt has no retained text")


def _source(text, wanted):
    prefix = text.split("\n## ", 1)[0]
    metadata = _fields(prefix)
    if metadata.get("Source ID") != wanted:
        return None
    required = {"Source ID", "URL", "Title", "Source type", "Retrieved (UTC)",
                "Required attribution", "Disposition"}
    if not required <= set(metadata) or metadata.get("Disposition") != "ACCEPTED" \
            or not any("basis" in key.casefold() or "license" in key.casefold()
                       for key in metadata) \
            or not any("retention" in key.casefold() for key in metadata) \
            or not any("privacy" in key.casefold() for key in metadata):
        raise EvidenceError(f"source {wanted} provenance metadata is malformed")
    return metadata


def extract(text, locator, path, authority):
    match = LOCATOR.fullmatch(locator)
    if not match:
        raise EvidenceError(f"invalid assigned locator: {locator}")
    source_id, evidence_id = match.groups()
    source = _source(text, source_id)
    if source is None:
        return None
    evidence_section = _section(text, evidence_id)
    evidence = _fields(evidence_section)
    if set(evidence) != REQUIRED_EVIDENCE or evidence["Excerpt ID"] == "" \
            or evidence["Kind"] not in ("EXACT_QUOTE", "INTERPRETATION"):
        raise EvidenceError(f"assigned evidence {locator} metadata is malformed")
    excerpt_id = evidence["Excerpt ID"]
    if not re.fullmatch(r"C-\d{3}", excerpt_id):
        raise EvidenceError(f"assigned evidence {locator} excerpt is malformed")
    excerpt_section = _section(text, excerpt_id)
    excerpt_fields = _fields(excerpt_section)
    if set(excerpt_fields) != {"Locator", "Capture method"}:
        raise EvidenceError(f"assigned excerpt {excerpt_id} metadata is malformed")
    body = {"locator": locator, "path": path, "source": source,
            "excerpt": {"id": excerpt_id, **excerpt_fields,
                        "Text": _excerpt_text(excerpt_section)},
            "evidence": {"id": evidence_id, **evidence}, "authority": authority}
    return {**body, "record_sha256": PS.state_hash(body)}


def assigned_records(packets, assigned):
    records, used = [], set()
    for locator, authority in sorted(assigned.items()):
        found = []
        for path, text in packets.items():
            record = extract(text, locator, path, authority)
            if record is not None:
                found.append(record)
        if len(found) != 1:
            raise EvidenceError(f"assigned locator {locator} is missing or ambiguous")
        records.extend(found)
        used.add(found[0]["path"])
    if used != set(packets):
        raise EvidenceError("packet assignment contains no exact assigned locator")
    return records
