#!/usr/bin/env python3
"""Inspect and fail closed on the complete, sealed research contract."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import validate_subject_contract as subject


SCHEMA = 1
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SOURCE_FILE = re.compile(r"^[sS]-(\d{3})-.+\.md$")
ENTRY_HEADING = re.compile(r"^###\s+(LEU-\d{3}|SEU-\d{3}|GAP-\d{3})\s*$", re.MULTILINE)
EVIDENCE_HEADING = re.compile(r"^###\s+(E-\d{3})\s*$", re.MULTILINE)
EXCERPT_HEADING = re.compile(r"^###\s+(C-\d{3})\s*$", re.MULTILINE)
FIELD = re.compile(r"^-\s+\*\*([^*:\n]+):\*\*\s*(.*?)\s*$", re.MULTILINE)
LOCATOR = re.compile(r"S-\d{3}#E-\d{3}")
BANK_LINE = re.compile(r"^-\s+\[Bank\s+(\d+)\](?:\s+\[(SUPPORTED|MIXED|CONTESTED)\])?\s+(.+)$")
PLACEHOLDER = re.compile(r"<[^>\n]+>|\b(?:tbd|todo|pending|unresolved|fill\s+in)\b", re.I)
RIGHTS_UNKNOWN = {"", "unknown", "none", "not available", "pending", "tbd", "todo"}

LANES = {
    "LIVED_EXPERIENCE",
    "SCIENCE_MECHANISM",
    "INDUSTRY_CULTURE",
    "COUNTER_CORPUS",
    "DIALECT_SENSORY",
}
GRADES = {"SUPPORTED", "MIXED", "CONTESTED", "n/a"}
SLOTS = {
    "LOAD_BEARING_BELIEF",
    "INVERSION",
    "JUSTIFICATION_MENU",
    "ENGINEERED_VILLAIN",
    "SCIENCE_WEIGHT",
    "ROOT_DIRECTION",
    "ANALOGY_SET",
    "ESCAPE_ROUTES",
    "SEDUCTIVE_SCENE",
    "REVELATION",
    "SENSORY_DIALECT",
    "MANTRA_SEEDS",
    "TESTIMONIAL",
    "EVIDENCE_LEDGER",
}
FLOORS = {
    "FULL-LENGTH": {
        "lived_experience": 500,
        "scientific_claims": 200,
        "verbatim_justifications": 100,
        "analogies": 50,
        "dialect_sensory": 100,
        "testimonials": 5,
    },
    "POCKET": {
        "lived_experience": 200,
        "scientific_claims": 80,
        "verbatim_justifications": 40,
        "analogies": 20,
        "dialect_sensory": 40,
        "testimonials": 3,
    },
}
PACKET_FIELDS = {
    "Source ID", "URL", "Title", "Source type", "Retrieved (UTC)", "Disposition",
}
PACKET_MACHINE_FIELDS = {
    "Discovery lane", "Source family", "Author / organization", "Fetched URL",
    "Fetched content SHA-256", "Corroboration count", "Story identity", "Study lineage", "Study design / class",
    "Deletion sensitivity", "Personal-data retention",
}
RIGHTS_FIELDS = {
    "access / license": ("Access / license basis", "License / quotation basis"),
    "excerpt / redistribution": ("Excerpt / redistribution basis", "License / quotation basis"),
    "attribution": ("Required attribution",),
    "retention / deletion": ("Retention / deletion sensitivity", "Retention / deletion status"),
    "privacy / personal data": ("Privacy / personal-data basis", "Privacy judgment"),
}
EVIDENCE_FIELDS = {
    "Kind", "Text", "Excerpt ID", "Locator", "Persona tags", "Bank slots",
    "Evidence grade", "Use / limits",
}
EVIDENCE_MACHINE_FIELDS = {
    "Brief beliefs", "Style slots", "Safety relevance", "Grade rationale", "Scope",
    "Counterevidence", "Permitted inference", "Prohibited inference",
    "Testimonial qualification", "Situation", "Emotion",
}
UNIT_FIELDS = {
    "Situation", "Reader wording", "Implicated belief", "Persona IDs", "Emotion",
    "Permitted inference", "Prohibited inference", "Style slots", "Safety boundary",
    "Source locator", "Evidence grade",
}
GAP_FIELDS = {"Implicated belief", "Missing support", "Owner"}
REVIEW_CHECKS = {
    "fetch_fidelity",
    "rights_privacy",
    "originality",
    "scientific_rigor",
    "inference_bounds",
    "deduplication",
    "carr_intervention_utility",
    "counter_corpus",
    "belief_persona_safety_slots",
    "source_traceability",
}
AUTHORITY_KEYS = {
    "prompt", "evidence_editor", "configuration", "sanitized_receipt_hashes",
}


class ContractError(ValueError):
    pass


class ResearchGap(ContractError):
    pass


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha_bytes(value):
    return hashlib.sha256(value).hexdigest()


def _sha_json(value):
    return _sha_bytes(_canonical(value))


def _sha_file(path):
    return _sha_bytes(Path(path).read_bytes())


def _json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _clean(value):
    return value.strip().strip("\"\u201c\u201d")


def _lineage_key(value):
    """Treat spelling case and whitespace as non-identity for study lineage."""
    return " ".join(str(value).casefold().split())


def _split(value):
    if not isinstance(value, str):
        return []
    return [part.strip().strip("\"\u201c\u201d") for part in re.split(r"\s*(?:,|\||;)\s*", value) if part.strip()]


def _canonical_url(value):
    try:
        parsed = urlsplit(value.strip())
        host = parsed.hostname
        port = parsed.port
        username = parsed.username
    except (AttributeError, UnicodeError, ValueError) as exc:
        raise ContractError("accepted source has an invalid URL") from exc
    if parsed.scheme not in ("http", "https") or not parsed.netloc or username or not host:
        raise ContractError("accepted source has an invalid URL")
    host = host.casefold()
    if host in {"reddit.com", "www.reddit.com"} or host.endswith(".reddit.com"):
        raise ContractError("accepted source uses an excluded Reddit domain")
    query = parse_qsl(parsed.query, keep_blank_values=True)
    query = [(key, item) for key, item in query
             if not key.casefold().startswith("utm_")]
    canonical_host = f"[{host}]" if ":" in host else host
    netloc = canonical_host if port is None else f"{canonical_host}:{port}"
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((parsed.scheme.casefold(), netloc, path,
                       urlencode(sorted(query)), ""))


def _fields(body):
    result, duplicates = {}, []
    for name, value in FIELD.findall(body):
        if name in result:
            duplicates.append(name)
        else:
            result[name] = value.strip()
    return result, duplicates


def _blocks(text, heading):
    matches = list(heading.finditer(text))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        yield match.group(1), text[match.end():end]


def _excerpt_blocks(text):
    """Excerpt bodies stop at the evidence section, not at the next excerpt only."""
    matches = list(EXCERPT_HEADING.finditer(text))
    evidence_heading = re.search(r"^##\s+Evidence items\s*$", text, re.MULTILINE)
    evidence_start = evidence_heading.start() if evidence_heading else len(text)
    for index, match in enumerate(matches):
        next_start = matches[index + 1].start() if index + 1 < len(matches) else evidence_start
        yield match.group(1), text[match.end():next_start]


def _artifact_files(book, include_coverage=False, include_review=False):
    book = Path(book)
    paths = [
        book / "00-brief.md",
        book / "research/lived-experience.md",
        book / "research/scientific-evidence.md",
    ]
    paths.extend(sorted((book / "research/sources").glob("*.md")))
    paths = [path for path in paths if path.name != "README.md"]
    if include_coverage:
        paths.extend([book / "research/research-log.md", book / "research/research-coverage.json"])
    if include_review:
        paths.append(book / "research/research-review.json")
    return paths


def _binding_map(book, paths):
    book = Path(book)
    result = {}
    for path in paths:
        if path.is_file():
            result[path.relative_to(book).as_posix()] = _sha_file(path)
    return dict(sorted(result.items()))


def _brief(book, blockers):
    path = Path(book) / "00-brief.md"
    beliefs, boundary = (), ""
    if not path.is_file():
        blockers.append("brief: missing 00-brief.md")
        return beliefs, boundary
    text = path.read_text(encoding="utf-8")
    try:
        sections = subject._sections(text)
    except subject.ContractError as exc:
        blockers.append(f"brief: {exc}")
        sections = {}
    for name in subject.SCALAR_FIELDS:
        try:
            subject._require_content(sections, name)
        except subject.ContractError as exc:
            blockers.append(f"brief: {exc}")
    try:
        subject._validate_forks(sections)
    except subject.ContractError as exc:
        blockers.append(f"brief: {exc}")
    for name, minimum, maximum in (("Primary false belief", 1, 1), ("Subordinate beliefs", 3, 5)):
        try:
            subject._validate_beliefs(sections, name, minimum, maximum)
        except subject.ContractError as exc:
            blockers.append(f"brief: {exc}")
    try:
        beliefs = subject.belief_set(text)
    except subject.ContractError:
        pass
    if "Safety perimeter" in sections and not subject._unresolved(sections["Safety perimeter"]):
        boundary = subject.scalar_value(sections, "Safety perimeter")
    if subject.PLACEHOLDER.search(text):
        blockers.append("brief: unresolved placeholder content remains")
    return beliefs, boundary


def _excerpt_content(body):
    content = FIELD.sub("", body)
    content = re.sub(r"^```(?:text)?\s*$", "", content, flags=re.MULTILINE)
    content = re.sub(r"^```\s*$", "", content, flags=re.MULTILINE)
    return content.strip()


def _packets(book, blockers):
    root = Path(book) / "research/sources"
    packets, evidence = {}, {}
    missing_machine = invalid_excerpt_hash = rejected = 0
    if not root.is_dir():
        blockers.append("provenance: missing research/sources directory")
        return packets, evidence, {"rejected_packets": 0}
    urls, excerpts_seen, evidence_seen, stories = {}, {}, {}, {}
    seen_source_ids = set()
    for path in sorted(root.glob("*.md")):
        if path.name == "README.md":
            continue
        match = SOURCE_FILE.fullmatch(path.name)
        if match is None:
            blockers.append("provenance: invalid accepted packet filename")
            continue
        source_id = f"S-{match.group(1)}"
        if source_id in seen_source_ids:
            blockers.append(f"deduplication: duplicate Source ID across packet files ({source_id})")
            continue
        seen_source_ids.add(source_id)
        text = path.read_text(encoding="utf-8")
        header = text.split("## Minimum retained excerpt", 1)[0]
        fields, duplicates = _fields(header)
        disposition = fields.get("Disposition", "")
        if not disposition.startswith("ACCEPTED"):
            rejected += 1
            continue
        if duplicates:
            blockers.append(f"provenance: accepted packet {source_id} has duplicate fields")
        missing = PACKET_FIELDS - fields.keys()
        if missing or fields.get("Source ID") != source_id:
            blockers.append(f"provenance: accepted packet {source_id} has invalid identity fields")
        rights_bad = False
        for names in RIGHTS_FIELDS.values():
            value = next((fields.get(name) for name in names if name in fields), None)
            normalized = (value or "").strip().casefold()
            if value is None or PLACEHOLDER.search(value) or normalized in RIGHTS_UNKNOWN:
                rights_bad = True
        if rights_bad:
            blockers.append(f"eligibility: accepted packet {source_id} lacks resolved rights/privacy bases")
        machine_missing = PACKET_MACHINE_FIELDS - fields.keys()
        unresolved_machine = [name for name in PACKET_MACHINE_FIELDS
                              if not fields.get(name) or PLACEHOLDER.search(fields.get(name, ""))]
        if machine_missing or unresolved_machine:
            missing_machine += 1
        lane = fields.get("Discovery lane", "")
        if lane and lane not in LANES:
            blockers.append(f"provenance: accepted packet {source_id} has invalid discovery lane")
        url = fields.get("URL", "")
        fetched = fields.get("Fetched URL", "")
        try:
            canonical = _canonical_url(url)
            parsed_url = urlsplit(canonical)
            domain = parsed_url.hostname or ""
        except (ContractError, UnicodeError, ValueError, TypeError):
            canonical, domain, parsed_url = "", "", None
        try:
            fetched_canonical = _canonical_url(fetched)
        except (ContractError, UnicodeError, ValueError, TypeError):
            fetched_canonical = ""
        title = fields.get("Title", "").strip()
        source_type = fields.get("Source type", "").strip().casefold()
        retrieved = fields.get("Retrieved (UTC)", "").strip()
        if not title or PLACEHOLDER.search(title) or source_type not in {
                "community", "study", "report", "transcript", "investigative"} \
                or re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", retrieved) is None:
            blockers.append(f"provenance: accepted packet {source_id} has invalid title/type/retrieval identity")
        if not canonical or parsed_url is None or parsed_url.scheme not in {"http", "https"} \
                or not domain or not fetched_canonical or fetched_canonical != canonical:
            blockers.append(f"fetch provenance: accepted packet {source_id} URL is not fetch-bound")
        if canonical in urls:
            blockers.append("deduplication: duplicate canonical URL among accepted packets")
        elif canonical:
            urls[canonical] = source_id
        fetch_hash = fields.get("Fetched content SHA-256", "")
        if HEX64.fullmatch(fetch_hash) is None:
            blockers.append(f"fetch provenance: accepted packet {source_id} has invalid fetched-content hash")
        corroboration = fields.get("Corroboration count", "")
        if re.fullmatch(r"[1-9]\d*", corroboration) is None:
            blockers.append(
                f"deduplication: accepted packet {source_id} has invalid corroboration count")
        privacy_mode = fields.get("Personal-data retention", "")
        if fields.get("Deletion sensitivity") != "NOT_DELETION_SENSITIVE" \
                or privacy_mode not in {"NONE", "MINIMAL_REQUIRED_ATTRIBUTION"} \
                or (privacy_mode == "MINIMAL_REQUIRED_ATTRIBUTION" and
                    fields.get("Required attribution", "").strip().casefold() in {"", "n/a"}):
            blockers.append(f"eligibility: accepted packet {source_id} has unsafe retention/privacy status")
        excerpt_map = {}
        for excerpt_id, body in _excerpt_blocks(text):
            if excerpt_id in excerpt_map:
                blockers.append(
                    f"fetch provenance: accepted packet {source_id} has duplicate excerpt ID {excerpt_id}")
                continue
            excerpt_fields, excerpt_dupes = _fields(body)
            content = _excerpt_content(body)
            declared = excerpt_fields.get("Content SHA-256", "")
            actual = _sha_bytes(content.encode("utf-8")) if content else ""
            if excerpt_dupes or not excerpt_fields.get("Locator") or not excerpt_fields.get("Capture method") or not content:
                blockers.append(f"fetch provenance: accepted packet {source_id} has an incomplete retained excerpt")
            if not declared or declared != actual:
                invalid_excerpt_hash += 1
            if actual in excerpts_seen:
                blockers.append("deduplication: duplicate retained excerpt among accepted packets")
            elif actual:
                excerpts_seen[actual] = source_id
            excerpt_map[excerpt_id] = content
        if not excerpt_map:
            blockers.append(f"fetch provenance: accepted packet {source_id} has no retained excerpt")
        packet_evidence = []
        evidence_ids = set()
        for evidence_id, body in _blocks(text, EVIDENCE_HEADING):
            locator = f"{source_id}#{evidence_id}"
            if evidence_id in evidence_ids:
                blockers.append(f"evidence: accepted packet {source_id} has duplicate evidence ID {evidence_id}")
                continue
            evidence_ids.add(evidence_id)
            item, dupes = _fields(body)
            packet_evidence.append(locator)
            if dupes or EVIDENCE_FIELDS - item.keys():
                blockers.append(f"evidence: {locator} has an incomplete base schema")
            machine_complete = not (EVIDENCE_MACHINE_FIELDS - item.keys())
            if not machine_complete:
                missing_machine += 1
            kind = item.get("Kind", "")
            if kind not in {"EXACT_QUOTE", "INTERPRETATION"}:
                blockers.append(f"evidence: {locator} has invalid kind")
            excerpt_id = item.get("Excerpt ID", "")
            if excerpt_id not in excerpt_map:
                blockers.append(f"evidence: {locator} does not bind a retained excerpt")
            elif kind == "EXACT_QUOTE" and item.get("Text", "") not in excerpt_map[excerpt_id]:
                blockers.append(f"evidence: {locator} exact quote is absent from its retained excerpt")
            grade = item.get("Evidence grade", "").strip()
            grade_tokens = {grade} if grade in GRADES else set()
            if not grade_tokens:
                blockers.append(f"evidence: {locator} must declare exactly one canonical grade")
            dedupe_banks = [int(number) for number in re.findall(
                r"Bank\s+(\d+)", item.get("Bank slots", ""))]
            dedupe_lineage = (fields.get("Study lineage", "").casefold()
                              if any(bank in (7, 8) for bank in dedupe_banks) else "")
            item_hash = _sha_json({
                "text": " ".join(item.get("Text", "").casefold().split()),
                "permitted": " ".join(item.get("Permitted inference", "").casefold().split()),
                "prohibited": " ".join(item.get("Prohibited inference", "").casefold().split()),
                "scientific_lineage": dedupe_lineage,
            })
            if machine_complete and item_hash in evidence_seen:
                blockers.append("deduplication: duplicate evidence meaning among accepted items")
            elif machine_complete:
                evidence_seen[item_hash] = locator
            beliefs = _split(item.get("Brief beliefs", ""))
            personas = _split(item.get("Persona tags", ""))
            banks = [int(number) for number in re.findall(r"Bank\s+(\d+)", item.get("Bank slots", ""))]
            slots = _split(item.get("Style slots", ""))
            if machine_complete:
                if any(slot not in SLOTS for slot in slots) or not slots:
                    blockers.append(f"evidence: {locator} has invalid style-slot authority")
                required_values = ("Text", "Locator", "Permitted inference", "Prohibited inference",
                                   "Situation", "Emotion", "Safety relevance")
                if any(not item.get(name, "").strip() or PLACEHOLDER.search(item.get(name, ""))
                       for name in required_values):
                    blockers.append(f"evidence: {locator} lacks resolved intervention/inference authority")
                scientific = any(bank in (7, 8) for bank in banks)
                lineage = fields.get("Study lineage", "").casefold()
                design = fields.get("Study design / class", "").casefold()
                if scientific and (grade == "n/a" or lineage in {"", "n/a", "not applicable"}
                                   or design in {"", "n/a", "not applicable"}):
                    blockers.append(f"science: {locator} lacks graded study lineage authority")
            testimonial = item.get("Testimonial qualification", "")
            if testimonial and testimonial != "NOT_CANDIDATE" and re.fullmatch(
                    r"QUALIFIED;\s*numbers=.+;\s*sensory=.+;\s*authority_conflict=.+", testimonial) is None:
                blockers.append(f"evidence: {locator} has invalid testimonial qualification")
            evidence[locator] = {
                "packet_id": source_id,
                "kind": kind,
                "text": item.get("Text", ""),
                "personas": personas,
                "banks": banks,
                "beliefs": beliefs,
                "slots": slots,
                "grade": item.get("Evidence grade", ""),
                "grades": sorted(grade_tokens),
                "permitted_inference": item.get("Permitted inference", ""),
                "prohibited_inference": item.get("Prohibited inference", ""),
                "safety": item.get("Safety relevance", ""),
                "situation": item.get("Situation", ""),
                "emotion": item.get("Emotion", ""),
                "testimonial": testimonial,
                "machine_complete": machine_complete,
            }
        if not packet_evidence:
            blockers.append(f"evidence: accepted packet {source_id} has no evidence item")
        story = fields.get("Story identity", "")
        if story and story.casefold() not in {"n/a", "not applicable"}:
            if story in stories:
                blockers.append("deduplication: duplicate lived-story identity among accepted packets")
            else:
                stories[story] = source_id
        packets[source_id] = {
            "path": path.relative_to(Path(book)).as_posix(),
            "url": canonical,
            "domain": domain,
            "lane": lane,
            "corroboration_count": int(corroboration) if corroboration.isdigit() else 0,
            "source_family": fields.get("Source family", ""),
            "author": fields.get("Author / organization", ""),
            "evidence": packet_evidence,
            "story_identity": story,
            "study_lineage": fields.get("Study lineage", ""),
            "study_design": fields.get("Study design / class", ""),
        }
    if rejected:
        blockers.append(f"eligibility: {rejected} rejected source packet(s) were retained")
    if missing_machine:
        blockers.append(f"provenance: {missing_machine} accepted packet/evidence record(s) lack machine fields")
    if invalid_excerpt_hash:
        blockers.append(f"fetch provenance: {invalid_excerpt_hash} retained excerpt(s) lack a current content hash")
    return packets, evidence, {"rejected_packets": rejected}


def _persona_map(text, beliefs, blockers):
    section = re.search(r"^##\s+Persona map\s*$([\s\S]*?)(?=^##\s+|\Z)", text, re.MULTILINE)
    personas = {}
    if not section:
        blockers.append("coverage: missing persona map")
        return personas
    rows = [line.strip() for line in section.group(1).splitlines() if line.strip().startswith("|")]
    for row in rows[2:]:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        if len(cells) != 5 or re.fullmatch(r"P-\d{2,3}", cells[0]) is None:
            blockers.append("coverage: persona map lacks machine-readable applicable beliefs")
            continue
        persona, context, applicable, banks, sources = cells
        mapped = list(beliefs) if applicable == "ALL" else _split(applicable)
        if not context or any(belief not in beliefs for belief in mapped) or not mapped:
            blockers.append(f"coverage: persona {persona} has invalid belief applicability")
        personas[persona] = {
            "context": context,
            "beliefs": mapped,
            "banks": [int(value) for value in re.findall(r"\d+", banks)],
            "sources": sorted(set(re.findall(r"S-\d{3}", sources))),
        }
    if len(personas) < 3:
        blockers.append(f"coverage: fewer than three materially distinct personas ({len(personas)})")
    contexts = [" ".join(item["context"].casefold().split()) for item in personas.values()]
    if len(contexts) != len(set(contexts)):
        blockers.append("coverage: persona functions are not materially distinct")
    return personas


def _bank_entries(path, evidence, packets, blockers):
    if not path.is_file():
        blockers.append(f"synthesis: missing {path.name}")
        return []
    entries = []
    seen_meaning, used_locators = set(), defaultdict(set)
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = BANK_LINE.fullmatch(line.strip())
        if not match:
            continue
        bank, grade, body = int(match.group(1)), match.group(2), match.group(3)
        personas_match = re.search(r"Persona IDs:\s*(.*?)(?:\s+[\u2014-]\s+Source IDs:|$)", body)
        sources_match = re.search(r"Source IDs:\s*(.*?)(?:\s+[\u2014-]\s+|$)", body)
        personas = _split(personas_match.group(1)) if personas_match else []
        locators = sorted(set(LOCATOR.findall(sources_match.group(1)))) if sources_match else []
        meaning = _sha_bytes(re.sub(r"\s+[\u2014-]\s+Persona IDs:.*$", "", body).casefold().encode("utf-8"))
        if meaning in seen_meaning:
            blockers.append(f"deduplication: {path.name} repeats a synthesis meaning")
        seen_meaning.add(meaning)
        if any(locator in used_locators[bank] for locator in locators):
            blockers.append(f"deduplication: {path.name} reuses evidence to inflate Bank {bank}")
        used_locators[bank].update(locators)
        if not personas or not locators:
            blockers.append(f"synthesis: {path.name}:{number} lacks persona or evidence locators")
        items = [evidence[locator] for locator in locators if locator in evidence]
        if len(items) != len(locators):
            blockers.append(f"synthesis: {path.name}:{number} cites unknown evidence")
        if any(bank not in item["banks"] for item in items):
            blockers.append(f"synthesis: {path.name}:{number} widens an evidence bank assignment")
        if any(not item["machine_complete"] for item in items):
            blockers.append(f"synthesis: {path.name}:{number} relies on legacy unbounded evidence")
        packet_ids = sorted({item["packet_id"] for item in items})
        lanes = sorted({packets[item["packet_id"]]["lane"] for item in items if item["packet_id"] in packets})
        lineages = sorted({_lineage_key(packets[item["packet_id"]]["study_lineage"])
                           for item in items if item["packet_id"] in packets and
                           _lineage_key(packets[item["packet_id"]]["study_lineage"])
                           not in {"", "n/a", "not applicable"}})
        if bank == 7 and grade != "CONTESTED" and len(lineages) < 2:
            blockers.append(f"science: {path.name}:{number} non-CONTESTED Bank 7 claim lacks two independent lineages")
        entries.append({
            "bank": bank,
            "grade": grade,
            "personas": personas,
            "locators": locators,
            "packet_ids": packet_ids,
            "lanes": lanes,
            "lineages": lineages,
            "qualified_testimonial": any(item["testimonial"].startswith("QUALIFIED;") for item in items),
            "counter_quote": any(item["kind"] == "EXACT_QUOTE" and
                                 packets.get(item["packet_id"], {}).get("lane") == "COUNTER_CORPUS"
                                 for item in items),
        })
    return entries


def _units(book, beliefs, boundary, evidence, packets, blockers):
    units, gaps = {}, {}
    for name in ("lived-experience.md", "scientific-evidence.md"):
        path = Path(book) / "research" / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for entry_id, body in _blocks(text, ENTRY_HEADING):
            fields, dupes = _fields(body)
            if entry_id in units or entry_id in gaps:
                blockers.append(f"units: duplicate intervention entry {entry_id}")
                continue
            if entry_id.startswith("GAP-"):
                if dupes or GAP_FIELDS - fields.keys() or fields.get("Owner") != "research/synthesis":
                    blockers.append(f"units: {entry_id} has invalid research-gap schema")
                gaps[entry_id] = dict(fields)
                continue
            missing = UNIT_FIELDS - fields.keys()
            unresolved = [name for name in UNIT_FIELDS
                          if not fields.get(name, "").strip()
                          or PLACEHOLDER.search(fields.get(name, ""))]
            if dupes or missing or unresolved:
                blockers.append(f"units: {entry_id} lacks complete intervention authority")
                continue
            belief = _clean(fields.get("Implicated belief", ""))
            personas = _split(fields.get("Persona IDs", ""))
            slots = _split(fields.get("Style slots", ""))
            locators = LOCATOR.findall(fields.get("Source locator", ""))
            grade = fields.get("Evidence grade", "")
            if belief not in beliefs:
                blockers.append(f"units: {entry_id} belief is absent from completed brief")
            if not personas or not slots or any(slot not in SLOTS for slot in slots):
                blockers.append(f"units: {entry_id} lacks persona/style-slot authority")
            if fields.get("Safety boundary", "") != boundary:
                blockers.append(f"units: {entry_id} does not preserve the brief safety perimeter")
            items = [evidence[locator] for locator in locators if locator in evidence]
            if not locators or len(items) != len(locators):
                blockers.append(f"units: {entry_id} has unknown source locator")
            if grade not in GRADES or entry_id.startswith("SEU-") and grade == "n/a":
                blockers.append(f"units: {entry_id} has invalid evidence grade")
            if items and not any(grade in item["grades"] for item in items):
                blockers.append(f"units: {entry_id} grade is not source-grounded")
            wording = fields.get("Reader wording", "")
            quoted = len(wording) >= 2 and wording[0] in {'"', '\u201c'} and wording[-1] in {'"', '\u201d'}
            if not quoted or not any(item["kind"] == "EXACT_QUOTE" and item["text"] == _clean(wording) for item in items):
                blockers.append(f"units: {entry_id} reader wording is not exact-source grounded")
            for raw, normalized in (("Situation", "situation"), ("Emotion", "emotion")):
                if fields.get(raw) and not any(fields[raw] == item[normalized] for item in items):
                    blockers.append(f"units: {entry_id} {raw.casefold()} widens source authority")
            for raw, normalized in (("Permitted inference", "permitted_inference"),
                                    ("Prohibited inference", "prohibited_inference")):
                if fields.get(raw) and not any(fields[raw] == item[normalized] for item in items):
                    blockers.append(f"units: {entry_id} {raw.casefold()} widens source authority")
            for persona in personas:
                if not any(persona in item["personas"] or "ALL" in item["personas"] for item in items):
                    blockers.append(f"units: {entry_id} persona is not source-grounded")
            if not any(belief in item["beliefs"] for item in items):
                blockers.append(f"units: {entry_id} belief is not evidence-bound")
            if any(not set(slots).issubset(item["slots"]) for item in items):
                blockers.append(f"units: {entry_id} widens style-slot authority")
            if entry_id.startswith("SEU-") and grade != "CONTESTED" \
                    and any(7 in item["banks"] for item in items):
                lineages = {_lineage_key(packets[item["packet_id"]]["study_lineage"])
                            for item in items if item["packet_id"] in packets and
                            _lineage_key(packets[item["packet_id"]]["study_lineage"])
                            not in {"", "n/a", "not applicable"}}
                if len(lineages) < 2:
                    blockers.append(f"science: {entry_id} lacks two independent study lineages")
            public = dict(fields)
            public.update({
                "kind": entry_id[:3],
                "belief": belief,
                "personas": personas,
                "slots": slots,
                "safety": fields.get("Safety boundary", ""),
                "locators": locators,
                "permitted_inference": fields.get("Permitted inference", ""),
                "prohibited_inference": fields.get("Prohibited inference", ""),
                "evidence_grade": grade,
            })
            units[entry_id] = public
    if gaps:
        blockers.append(f"units: {len(gaps)} unresolved GAP unit(s) block downstream work")
    return units, gaps


def _coverage(book, preset=None):
    blockers = []
    beliefs, boundary = _brief(book, blockers)
    packets, evidence, rejection_counts = _packets(book, blockers)
    lived_path = Path(book) / "research/lived-experience.md"
    science_path = Path(book) / "research/scientific-evidence.md"
    lived_text = lived_path.read_text(encoding="utf-8") if lived_path.is_file() else ""
    personas = _persona_map(lived_text, beliefs, blockers)
    lived = _bank_entries(lived_path, evidence, packets, blockers)
    science = _bank_entries(science_path, evidence, packets, blockers)
    units, gap_units = _units(book, beliefs, boundary, evidence, packets, blockers)
    if not any(unit_id.startswith("LEU-") for unit_id in units):
        blockers.append("units: no accepted lived-experience intervention unit")
    if not any(unit_id.startswith("SEU-") for unit_id in units):
        blockers.append("units: no accepted scientific intervention unit")
    log = Path(book) / "research/research-log.md"
    log_text = log.read_text(encoding="utf-8") if log.is_file() else ""
    if not log.is_file():
        blockers.append("authority: missing research-log.md")
    if preset is None:
        match = re.search(r"FORMAT PRESET:\s*(FULL-LENGTH|POCKET)\b", log_text)
        preset = match.group(1) if match else None
    if preset not in FLOORS:
        blockers.append("coverage: missing canonical FULL-LENGTH or POCKET preset")
        preset = "FULL-LENGTH"
    all_entries = lived + science
    banks = {str(number): sum(item["bank"] == number for item in all_entries) for number in range(1, 11)}
    for number, count in banks.items():
        if not count:
            blockers.append(f"coverage: Bank {number} has no accepted synthesis entry")
    actual = {
        "lived_experience": sum(item["bank"] in {1, 2, 3, 4, 5, 9, 10} for item in lived),
        "scientific_claims": sum(item["bank"] in {7, 8} for item in science),
        "verbatim_justifications": sum(item["bank"] == 1 and item["counter_quote"] for item in lived),
        "analogies": sum(item["bank"] == 6 for item in lived),
        "dialect_sensory": sum(item["bank"] == 9 for item in lived),
        "testimonials": sum(item["bank"] == 10 and item["qualified_testimonial"] for item in lived),
    }
    floor_report = {}
    gaps = []
    for name, minimum in FLOORS[preset].items():
        floor_report[name] = {"actual": actual[name], "minimum": minimum}
        if actual[name] < minimum:
            message = f"coverage: {preset} floor {name} is {actual[name]}/{minimum}"
            blockers.append(message)
            gaps.append({"kind": "floor", "target": name, "message": message})
    belief_persona = {belief: [] for belief in beliefs}
    for persona, record in personas.items():
        for belief in record["beliefs"]:
            if belief in belief_persona:
                belief_persona[belief].append(persona)
    unit_pairs = {(unit["belief"], persona) for unit in units.values() for persona in unit["personas"]}
    for belief, applicable in belief_persona.items():
        if not applicable:
            blockers.append(f"coverage: brief belief has no applicable persona ({belief})")
            gaps.append({"kind": "belief_persona", "target": f"{belief} / UNASSIGNED",
                         "message": "lead must assign at least one relevant persona"})
        for persona in applicable:
            if (belief, persona) not in unit_pairs:
                blockers.append(f"coverage: brief belief/persona lacks intervention unit ({belief} / {persona})")
                gaps.append({"kind": "belief_persona", "target": f"{belief} / {persona}",
                             "message": "accepted intervention unit required"})
    slot_personas = defaultdict(set)
    selected_locators = {locator for entry in all_entries for locator in entry["locators"]}
    selected_locators.update(
        locator for unit in units.values() for locator in unit["locators"])
    for locator in sorted(selected_locators):
        item = evidence.get(locator)
        if item is None:
            continue
        for slot in item["slots"]:
            slot_personas[slot].update(persona for persona in item["personas"] if persona != "ALL")
            if "ALL" in item["personas"]:
                slot_personas[slot].update(personas)
    slots = {slot: sorted(slot_personas[slot]) for slot in sorted(SLOTS)}
    for slot, covered in slots.items():
        if len(covered) < 3:
            blockers.append(f"coverage: style slot {slot} reaches {len(covered)}/3 distinct personas")
            gaps.append({"kind": "slot", "target": slot,
                         "message": f"accepted source-bounded material required for {3-len(covered)} more persona(s)"})
    if not any(item["counter_quote"] for item in lived):
        blockers.append("coverage: strongest pro-behavior counter-corpus is absent")
    if not boundary or not any(unit["safety"] == boundary for unit in units.values()):
        blockers.append("coverage: brief safety perimeter is not bound to accepted units")
    lane_evidence = defaultdict(list)
    for packet_id, packet in packets.items():
        if packet.get("lane"):
            lane_evidence[packet["lane"]].append(
                (packet.get("domain", ""), packet.get("author", ""), packet_id))
    diversity = {}
    for lane in sorted(LANES):
        rows = lane_evidence.get(lane, [])
        top_domain = max(Counter(row[0] for row in rows).values(), default=0)
        top_author = max(Counter(row[1] for row in rows).values(), default=0)
        domain_share = top_domain / len(rows) if rows else 0
        author_share = top_author / len(rows) if rows else 0
        diversity[lane] = {"entries": len(rows), "top_domain_share": domain_share,
                           "top_author_share": author_share}
        if not rows:
            blockers.append(f"coverage: discovery lane {lane} has no accepted evidence")
        elif domain_share > .5 or author_share > .5:
            blockers.append(f"coverage: discovery lane {lane} exceeds the 50% source-diversity limit")
    science_lineages = sorted({_lineage_key(packet["study_lineage"])
                               for packet in packets.values()
                               if _lineage_key(packet["study_lineage"])
                               not in {"", "n/a", "not applicable"}})
    counts = {
        "packets": len(packets),
        "evidence_items": len(evidence),
        "lived_bank_entries": len(lived),
        "scientific_bank_entries": len(science),
        "leu": sum(unit_id.startswith("LEU-") for unit_id in units),
        "seu": sum(unit_id.startswith("SEU-") for unit_id in units),
        "gap": len(gap_units),
        "personas": len(personas),
        **rejection_counts,
    }
    corpus_bindings = _binding_map(book, _artifact_files(book))
    corpus_sha = _sha_json(corpus_bindings)
    return {
        "blockers": sorted(set(blockers)),
        "gaps": gaps,
        "counts": counts,
        "banks": banks,
        "floors": floor_report,
        "personas": personas,
        "belief_persona": belief_persona,
        "slots": slots,
        "safety": {"boundary": boundary, "covered_units": sorted(
            unit_id for unit_id, unit in units.items() if unit["safety"] == boundary and boundary)},
        "diversity": diversity,
        "science_lineages": science_lineages,
        "preset": preset,
        "corpus_sha256": corpus_sha,
        "inventory": {"packets": packets, "evidence": evidence, "units": units},
    }


def build_coverage(book, preset, scarcity_requests=None):
    """Return the exact derived coverage artifact; never writes or waives a hard gate."""
    derived = _coverage(book, preset)
    requests = scarcity_requests or []
    valid_requests = []
    floor_targets = {gap["target"] for gap in derived["gaps"] if gap["kind"] == "floor"}
    for request in requests:
        if not isinstance(request, dict) or set(request) != {"floor", "attempts_sha256", "demonstrated_ceiling"}:
            raise ContractError("scarcity request shape is invalid")
        floor = request["floor"]
        if floor not in floor_targets or HEX64.fullmatch(str(request["attempts_sha256"])) is None \
                or not isinstance(request["demonstrated_ceiling"], int) \
                or request["demonstrated_ceiling"] != derived["floors"][floor]["actual"]:
            raise ContractError("scarcity request does not bind an unmet numeric floor and demonstrated ceiling")
        valid_requests.append(request)
    non_floor = [item for item in derived["blockers"] if not item.startswith("coverage: ") or " floor " not in item]
    requested = {item["floor"] for item in valid_requests}
    status = "PASS" if not non_floor and floor_targets == requested else "BLOCKED"
    return {
        "schema": SCHEMA,
        "status": status,
        "preset": derived["preset"],
        "corpus_sha256": derived["corpus_sha256"],
        "counts": derived["counts"],
        "banks": derived["banks"],
        "floors": derived["floors"],
        "personas": derived["personas"],
        "belief_persona": derived["belief_persona"],
        "slots": derived["slots"],
        "safety": derived["safety"],
        "diversity": derived["diversity"],
        "science_lineages": derived["science_lineages"],
        "gaps": derived["gaps"],
        "scarcity_requests": valid_requests,
    }


def _authority(book, authority):
    if not isinstance(authority, dict) or set(authority) != AUTHORITY_KEYS:
        raise ContractError("research authority shape is invalid")
    book = Path(book).absolute()
    if book.parent.name != "production-books" or not book.name:
        raise ContractError("research authority book is outside production-books/<slug>")
    root = book.parents[1]
    for key, expected_path in (("prompt", "prompts/research-agent.md"),
                               ("evidence_editor", "prompts/research-evidence-editor.md"),
                               ("configuration", "loop/config.yaml")):
        record = authority[key]
        if not isinstance(record, dict) or set(record) != {"path", "sha256"} \
                or record["path"] != expected_path or HEX64.fullmatch(str(record["sha256"])) is None:
            raise ContractError(f"research authority {key} binding is invalid")
        path = root / expected_path
        if not path.is_file() or _sha_file(path) != record["sha256"]:
            raise ContractError(f"research authority {key} binding is stale")
    receipts = authority["sanitized_receipt_hashes"]
    if not isinstance(receipts, list) or not receipts or receipts != sorted(set(receipts)) \
            or any(HEX64.fullmatch(str(value)) is None for value in receipts):
        raise ContractError("sanitized receipt hashes are invalid")
    return authority


def candidate_identity(book, authority):
    """Hash the exact corpus, log, coverage, prompt/config, and sanitized receipts."""
    authority = _authority(book, authority)
    paths = _artifact_files(book, include_coverage=True)
    required = {"00-brief.md", "research/lived-experience.md", "research/scientific-evidence.md",
                "research/research-log.md", "research/research-coverage.json"}
    bindings = _binding_map(book, paths)
    if not required.issubset(bindings) or not any(key.startswith("research/sources/") for key in bindings):
        raise ContractError("candidate identity lacks required research artifacts")
    return _sha_json({"bindings": bindings, "authority": authority})


def _verify_coverage(book, derived):
    path = Path(book) / "research/research-coverage.json"
    if not path.is_file():
        raise ContractError("missing research-coverage.json")
    document = _json(path)
    if not isinstance(document, dict) or document.get("schema") != SCHEMA:
        raise ContractError("research coverage schema is invalid")
    expected = build_coverage(book, document.get("preset"), document.get("scarcity_requests"))
    if document != expected:
        raise ContractError("research coverage is stale or not derived from current corpus")
    if document["status"] != "PASS":
        raise ContractError("research coverage verdict is not PASS")
    return document


def _finding_hash(waiver):
    return _sha_json({key: waiver[key] for key in
                      ("floor", "attempts_sha256", "demonstrated_ceiling", "finding")})


def _verify_review(book, candidate, coverage):
    path = Path(book) / "research/research-review.json"
    if not path.is_file():
        raise ContractError("missing independent research review")
    review = _json(path)
    expected_keys = {"schema", "status", "task_sha256", "candidate_sha256", "verdict_sha256",
                     "gaps", "checks", "scarcity_waivers", "editor_provenance",
                     "editor_receipt_sha256"}
    if not isinstance(review, dict) or set(review) != expected_keys or review.get("schema") != SCHEMA:
        raise ContractError("independent research review schema is invalid")
    if review["status"] != "PASS" or review["gaps"] != []:
        raise ContractError("independent research review did not PASS")
    if HEX64.fullmatch(str(review["task_sha256"])) is None or review["candidate_sha256"] != candidate:
        raise ContractError("independent research review candidate/task binding is invalid")
    checks = review["checks"]
    if not isinstance(checks, dict) or set(checks) != REVIEW_CHECKS \
            or any(value != "PASS" for value in checks.values()):
        raise ContractError("independent research review hard checks did not all PASS")
    requests = {item["floor"]: item for item in coverage["scarcity_requests"]}
    waivers = review["scarcity_waivers"]
    if not isinstance(waivers, list) or {item.get("floor") for item in waivers} != set(requests):
        raise ContractError("independent scarcity findings do not match numeric requests")
    for waiver in waivers:
        if not isinstance(waiver, dict) or set(waiver) != {
                "floor", "attempts_sha256", "demonstrated_ceiling", "finding", "finding_sha256"}:
            raise ContractError("scarcity waiver shape is invalid")
        request = requests[waiver["floor"]]
        if waiver["attempts_sha256"] != request["attempts_sha256"] \
                or waiver["demonstrated_ceiling"] != request["demonstrated_ceiling"] \
                or not waiver["finding"] or waiver["finding_sha256"] != _finding_hash(waiver):
            raise ContractError("scarcity waiver is not hash-bound to demonstrated search attempts")
    verdict = {key: review[key] for key in ("status", "checks", "gaps", "scarcity_waivers")}
    if review["verdict_sha256"] != _sha_json(verdict):
        raise ContractError("independent research review verdict binding is invalid")
    provenance = review["editor_provenance"]
    provenance_keys = {"kind", "judge_identity", "model", "reasoning_effort",
                       "fresh_ephemeral_context", "thread_id", "input_sha256",
                       "output_schema_sha256", "usage"}
    if not isinstance(provenance, dict) or set(provenance) != provenance_keys \
            or provenance.get("kind") not in {
                "native-codex-subscription", "captured-native-test-double"} \
            or provenance.get("fresh_ephemeral_context") is not True \
            or provenance.get("judge_identity") != "research-evidence-editor" \
            or any(not provenance.get(key) for key in (
                "model", "reasoning_effort", "thread_id", "input_sha256", "output_schema_sha256")) \
            or provenance.get("kind") == "native-codex-subscription" and (
                provenance.get("model") != "gpt-5.6-sol"
                or provenance.get("reasoning_effort") != "xhigh"):
        raise ContractError("independent research review provenance is invalid")
    receipt = _sha_json({"task_sha256": review["task_sha256"],
                         "verdict_sha256": review["verdict_sha256"],
                         "provenance": provenance})
    if review["editor_receipt_sha256"] != receipt:
        raise ContractError("independent research editor receipt binding is invalid")
    return review


def build_seal(book, authority):
    """Build a seal only from current PASS coverage and a PASS independent review."""
    derived = _coverage(book)
    coverage = _verify_coverage(book, derived)
    candidate = candidate_identity(book, authority)
    review = _verify_review(book, candidate, coverage)
    non_floor = [item for item in derived["blockers"] if not item.startswith("coverage: ") or " floor " not in item]
    if non_floor:
        raise ContractError("research hard gates remain: " + "; ".join(non_floor))
    bindings = _binding_map(book, _artifact_files(book, include_coverage=True, include_review=True))
    seal = {
        "schema": SCHEMA,
        "status": "SEALED",
        "bindings": bindings,
        "authority": _authority(book, authority),
        "corpus_sha256": derived["corpus_sha256"],
        "candidate_sha256": candidate,
        "coverage_sha256": bindings["research/research-coverage.json"],
        "review_sha256": bindings["research/research-review.json"],
        "review_task_sha256": review["task_sha256"],
        "review_verdict_sha256": review["verdict_sha256"],
        "editor_receipt_sha256": review["editor_receipt_sha256"],
    }
    seal["identity"] = _sha_json(seal)
    return seal


def _verify_seal(book, derived):
    path = Path(book) / "research/research-seal.json"
    if not path.is_file():
        raise ContractError("missing current research seal")
    seal = _json(path)
    expected_keys = {"schema", "status", "identity", "bindings", "authority", "corpus_sha256",
                     "candidate_sha256", "coverage_sha256", "review_sha256",
                     "review_task_sha256", "review_verdict_sha256",
                     "editor_receipt_sha256"}
    if not isinstance(seal, dict) or set(seal) != expected_keys or seal.get("schema") != SCHEMA \
            or seal.get("status") != "SEALED":
        raise ContractError("research seal schema/verdict is invalid")
    identity = seal.pop("identity")
    if HEX64.fullmatch(str(identity)) is None or identity != _sha_json(seal):
        raise ContractError("research seal identity is invalid")
    seal["identity"] = identity
    expected = build_seal(book, seal["authority"])
    if seal != expected:
        raise ContractError("research seal is stale or artifact bindings changed")
    return seal


def inspect_research(book, require_seal=True):
    """Return one aggregate report; accepted authority exists only with a current seal."""
    book = Path(book)
    derived = _coverage(book)
    blockers = list(derived["blockers"])
    candidate = seal_identity = None
    coverage_path = book / "research/research-coverage.json"
    review_path = book / "research/research-review.json"
    seal_path = book / "research/research-seal.json"
    acceptance = {
        "coverage": "MISSING" if not coverage_path.is_file() else "PRESENT",
        "review": "MISSING" if not review_path.is_file() else "PRESENT",
        "seal": "MISSING" if not seal_path.is_file() else "PRESENT",
    }
    if coverage_path.is_file():
        try:
            coverage = _verify_coverage(book, derived)
            acceptance["coverage"] = coverage["status"]
            if seal_path.is_file():
                authority = _json(seal_path).get("authority")
                candidate = candidate_identity(book, authority)
        except (ContractError, OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            blockers.append(f"coverage/review: {exc}")
    elif require_seal:
        blockers.append("coverage/review: missing research-coverage.json")
    if seal_path.is_file():
        try:
            seal = _verify_seal(book, derived)
            candidate = seal["candidate_sha256"]
            seal_identity = seal["identity"]
            acceptance["review"] = "PASS"
            acceptance["seal"] = "CURRENT"
            # A valid seal resolves only explicitly reviewed numeric scarcity blockers.
            coverage = _json(book / "research/research-coverage.json")
            waived = {item["floor"] for item in _json(book / "research/research-review.json")["scarcity_waivers"]}
            blockers = [item for item in blockers if not (
                item.startswith("coverage: ") and " floor " in item and
                any(f"floor {floor} " in item for floor in waived))]
        except (ContractError, OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            blockers.append(f"seal: {exc}")
            acceptance["seal"] = "INVALID"
    elif require_seal:
        blockers.append("seal: missing current research seal")
    blockers = sorted(set(blockers))
    status = "PASS" if not blockers and (not require_seal or seal_identity is not None) else "BLOCKED"
    return {
        "ok": status == "PASS",
        "status": status,
        "blockers": blockers,
        "gaps": derived["gaps"],
        "counts": derived["counts"],
        "coverage": {key: derived[key] for key in
                     ("banks", "floors", "personas", "belief_persona", "slots", "safety",
                      "diversity", "science_lineages", "preset")},
        "inventory": derived["inventory"],
        "corpus_sha256": derived["corpus_sha256"],
        "candidate_sha256": candidate,
        "seal_identity": seal_identity,
        "acceptance": acceptance,
    }


def require_research_contract(book):
    report = inspect_research(book, require_seal=True)
    if not report["ok"]:
        message = "; ".join(report["blockers"])
        if report["counts"]["gap"]:
            raise ResearchGap(message)
        raise ContractError(message)
    return tuple(sorted(report["inventory"]["units"]))


def research_seal_identity(book):
    report = inspect_research(book, require_seal=True)
    if not report["ok"] or not report["seal_identity"]:
        raise ContractError("research seal is not current: " + "; ".join(report["blockers"]))
    return report["seal_identity"]


def _packet_index(sources):
    """Legacy read helper retained for diagnostics; it confers no acceptance."""
    book = Path(sources).parent.parent
    blockers = []
    _, evidence, _ = _packets(book, blockers)
    return evidence


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True, help="production-books/<slug> directory")
    parser.add_argument("--inspect", action="store_true", help="print the aggregate report as JSON")
    args = parser.parse_args(argv)
    report = inspect_research(args.book, require_seal=not args.inspect)
    if args.inspect:
        # ASCII escaping is deliberate: redirected output remains valid JSON on
        # Windows consoles whose active code page cannot represent source text.
        print(json.dumps(report, sort_keys=True, ensure_ascii=True))
    if not report["ok"]:
        if not args.inspect:
            print("research-contract: STOP - " + "; ".join(report["blockers"]), file=sys.stderr)
        return 1
    print(f"research-contract: {len(report['inventory']['units'])} sealed units cover the completed brief")
    return 0


if __name__ == "__main__":
    sys.exit(main())
