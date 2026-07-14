#!/usr/bin/env python3
"""Validate intervention-ready synthesis before framing or planning."""
import argparse
import re
import sys
from pathlib import Path

import validate_subject_contract as subject

ENTRY_HEADING = re.compile(r"^###\s+(LEU-\d{3}|SEU-\d{3}|GAP-\d{3})\s*$", re.MULTILINE)
FIELD = re.compile(r"^-\s+\*\*([^*:\n]+):\*\*\s*(.*?)\s*$", re.MULTILINE)
SOURCE_FILE = re.compile(r"^[sS]-(\d{3})-.+\.md$")
EVIDENCE_HEADING = re.compile(r"^###\s+(E-\d{3})\s*$", re.MULTILINE)
EXCERPT_HEADING = re.compile(r"^###\s+(C-\d{3})\s*$", re.MULTILINE)
LOCATORS = re.compile(r"S-\d{3}#E-\d{3}(?:,\s*S-\d{3}#E-\d{3})*")
GRADES = {"SUPPORTED", "MIXED", "CONTESTED", "n/a"}
UNIT_FIELDS = {
    "Situation", "Reader wording", "Implicated belief", "Emotion",
    "Permitted inference", "Prohibited inference", "Source locator",
    "Evidence grade",
}
GAP_FIELDS = {"Implicated belief", "Missing support", "Owner"}
PACKET_FIELDS = {
    "Source ID", "URL", "Title", "Source type", "Retrieved (UTC)", "Disposition",
}
RIGHTS_FIELDS = {
    "access / license": ("Access / license basis", "License / quotation basis"),
    "excerpt / redistribution": (
        "Excerpt / redistribution basis", "License / quotation basis",
    ),
    "attribution": ("Required attribution",),
    "retention / deletion sensitivity": (
        "Retention / deletion sensitivity", "Retention / deletion status",
    ),
    "privacy / personal data": ("Privacy / personal-data basis", "Privacy judgment"),
}
EVIDENCE_FIELDS = {
    "Kind", "Text", "Excerpt ID", "Locator", "Persona tags", "Bank slots",
    "Evidence grade", "Use / limits",
}
PLACEHOLDER = re.compile(r"<[^>\n]+>|\b(?:tbd|todo|pending|unresolved)\b", re.I)
RIGHTS_PLACEHOLDER = re.compile(r"<[^>\n]+>|\b(?:tbd|todo|pending|unresolved|fill\s+in)\b", re.I)
UNRESOLVED_RIGHTS = {"unknown", "n/a", "none", "not available"}


class ContractError(ValueError):
    pass

class ResearchGap(ContractError):
    pass


def _fields(body, owner):
    fields = {}
    for name, value in FIELD.findall(body):
        if name in fields:
            raise ContractError(f"{owner}: duplicate field {name}")
        fields[name] = value.strip()
    return fields


def _require_fields(
    fields, required, owner, reject_placeholders=True, allow_extras=False
):
    missing = required - fields.keys()
    extras = fields.keys() - required
    if missing:
        raise ContractError(f"{owner}: missing field {sorted(missing)[0]}")
    if extras and not allow_extras:
        raise ContractError(f"{owner}: unknown field {sorted(extras)[0]}")
    for name, value in fields.items():
        if not value or (reject_placeholders and PLACEHOLDER.search(value)):
            raise ContractError(f"{owner}: unresolved field {name}")


def _blocks(text, heading):
    for match in heading.finditer(text):
        next_heading = re.search(r"^###\s+", text[match.end():], re.MULTILINE)
        end = match.end() + next_heading.start() if next_heading else len(text)
        yield match.group(1), text[match.end():end]


def _rights(fields, owner):
    url = fields["URL"].strip().casefold()
    if RIGHTS_PLACEHOLDER.search(fields["URL"]) or url in UNRESOLVED_RIGHTS:
        raise ContractError(f"{owner}: unresolved field URL")
    for label, names in RIGHTS_FIELDS.items():
        value = next((fields[name] for name in names if name in fields), None)
        if value is None:
            raise ContractError(f"{owner}: missing {label} basis")
        normalized = value.strip().casefold()
        if (not value or RIGHTS_PLACEHOLDER.search(value) or normalized in
                UNRESOLVED_RIGHTS - ({"n/a"} if label == "attribution" else set())):
            raise ContractError(f"{owner}: unresolved {label} basis")


def _excerpts(text, owner):
    excerpts = {}
    for excerpt_id, body in _blocks(text, EXCERPT_HEADING):
        fields = _fields(body, f"{owner}#{excerpt_id}")
        _require_fields(fields, {"Locator", "Capture method"}, owner, True, True)
        content = FIELD.sub("", body)
        content = re.sub(r"^```(?:text)?\s*$", "", content, flags=re.MULTILINE)
        content = re.sub(r"^```\s*$", "", content, flags=re.MULTILINE).strip()
        if not content or RIGHTS_PLACEHOLDER.search(content):
            raise ContractError(f"{owner}#{excerpt_id}: unresolved excerpt content")
        excerpts[excerpt_id] = content
    if not excerpts:
        raise ContractError(f"{owner}: missing minimum retained excerpt")
    return excerpts


def _packet_index(sources):
    index = {}
    for path in sorted(sources.glob("*.md")):
        if path.name == "README.md":
            continue
        source_match = SOURCE_FILE.fullmatch(path.name)
        if source_match is None:
            raise ContractError(f"invalid source packet filename: {path.name}")
        source_id = f"S-{source_match.group(1)}"
        text = path.read_text(encoding="utf-8")
        header = text.split("## Minimum retained excerpt", 1)[0]
        fields = _fields(header, source_id)
        _require_fields(fields, PACKET_FIELDS, source_id, True, True)
        _rights(fields, source_id)
        if fields["Source ID"] != source_id:
            raise ContractError(f"{source_id}: Source ID does not match filename")
        if RIGHTS_PLACEHOLDER.search(fields["Disposition"]) or not fields["Disposition"].startswith("ACCEPTED"):
            raise ContractError(f"{source_id}: rejected material must stay out of Git")
        excerpts = _excerpts(text, source_id)
        found_evidence = False
        for evidence_id, body in _blocks(text, EVIDENCE_HEADING):
            found_evidence = True
            owner = f"{source_id}#{evidence_id}"
            evidence = _fields(body, owner)
            _require_fields(evidence, EVIDENCE_FIELDS, owner, True)
            if evidence["Excerpt ID"] not in excerpts:
                raise ContractError(f"{owner}: unknown excerpt")
            if evidence["Kind"] not in {"EXACT_QUOTE", "INTERPRETATION"}:
                raise ContractError(f"{owner}: invalid evidence kind")
            if RIGHTS_PLACEHOLDER.search(evidence["Text"]):
                raise ContractError(f"{owner}: unresolved evidence text")
            if (evidence["Kind"] == "EXACT_QUOTE" and
                    evidence["Text"] not in excerpts[evidence["Excerpt ID"]]):
                raise ContractError(f"{owner}: exact quote is absent from excerpt")
            grades = set(re.findall(
                r"SUPPORTED|MIXED|CONTESTED|n/a", evidence["Evidence grade"]
            ))
            if not grades:
                raise ContractError(f"{owner}: invalid evidence grade")
            if owner in index:
                raise ContractError(f"duplicate source locator: {owner}")
            index[owner] = {
                "kind": evidence["Kind"], "text": evidence["Text"],
                "grades": grades, "limits": evidence["Use / limits"],
            }
        if not found_evidence:
            raise ContractError(f"{source_id}: missing evidence item")
    return index


def _entries(paths, beliefs, packet_items):
    units = {}
    gaps = {}
    known = set(beliefs)
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for entry_id, body in _blocks(text, ENTRY_HEADING):
            if entry_id in units or entry_id in gaps:
                raise ContractError(f"duplicate evidence entry: {entry_id}")
            fields = _fields(body, entry_id)
            if entry_id.startswith("GAP-"):
                _require_fields(fields, GAP_FIELDS, entry_id)
                if fields["Owner"] != "research":
                    raise ContractError(f"{entry_id}: gap owner must be research")
                gaps[entry_id] = fields
            else:
                _require_fields(fields, UNIT_FIELDS, entry_id)
                wording = fields["Reader wording"]
                if not ((wording.startswith('"') and wording.endswith('"')) or
                        (wording.startswith("“") and wording.endswith("”"))):
                    raise ContractError(f"{entry_id}: reader wording must be quoted")
                if fields["Evidence grade"] not in GRADES:
                    raise ContractError(f"{entry_id}: invalid evidence grade")
                if entry_id.startswith("SEU-") and fields["Evidence grade"] == "n/a":
                    raise ContractError(f"{entry_id}: scientific unit needs a grade")
                locator_text = fields["Source locator"]
                if LOCATORS.fullmatch(locator_text) is None:
                    raise ContractError(f"{entry_id}: invalid source locator")
                items = []
                for locator in locator_text.split(", "):
                    if locator not in packet_items:
                        raise ContractError(f"{entry_id}: unknown source locator {locator}")
                    items.append(packet_items[locator])
                declared = fields["Evidence grade"]
                grades = set().union(*(item["grades"] for item in items))
                if declared not in grades:
                    raise ContractError(f"{entry_id}: grade is not grounded in source evidence")
                reader_wording = wording[1:-1]
                if not any(
                    item["kind"] == "EXACT_QUOTE" and item["text"] == reader_wording
                    for item in items
                ):
                    raise ContractError(f"{entry_id}: reader wording is not grounded")
                for name in ("Situation", "Emotion"):
                    if not any(
                        fields[name] in item["text"] or fields[name] in item["limits"]
                        for item in items
                    ):
                        raise ContractError(f"{entry_id}: {name.lower()} is not grounded")
                for name in ("Permitted inference", "Prohibited inference"):
                    if not any(fields[name] in item["limits"] for item in items):
                        raise ContractError(f"{entry_id}: {name.lower()} is not permitted")
                for name in UNIT_FIELDS - {"Evidence grade"}:
                    if fields[name].casefold() in {"n/a", "none", "not available", "unknown"}:
                        raise ContractError(f"{entry_id}: unsupported field must route as a gap")
                units[entry_id] = fields
            belief = fields["Implicated belief"].strip('"“”')
            if belief not in known:
                raise ContractError(f"{entry_id}: belief is not in the completed brief")
    return units, gaps


def require_research_contract(book):
    book = Path(book)
    brief = subject.require_subject_contract(book, "research-synthesis")
    beliefs = subject.belief_set(brief.read_text(encoding="utf-8"))
    research = book / "research"
    paths = [research / "lived-experience.md", research / "scientific-evidence.md"]
    for path in paths:
        if not path.is_file():
            raise ContractError(f"missing synthesis: {path}")
    packet_items = _packet_index(research / "sources")
    units, gaps = _entries(paths, beliefs, packet_items)
    covered = {fields["Implicated belief"].strip('"“”') for fields in units.values()}
    routed = {fields["Implicated belief"].strip('"“”') for fields in gaps.values()}
    missing = set(beliefs) - covered - routed
    if missing:
        raise ContractError(f"belief lacks a supported unit or research gap: {sorted(missing)[0]}")
    if gaps:
        raise ResearchGap("research gaps block downstream work: " + ", ".join(sorted(gaps)))
    return tuple(units)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True, help="production-books/<slug> directory")
    args = parser.parse_args(argv)
    try:
        units = require_research_contract(args.book)
    except (ContractError, OSError, subject.ContractError) as exc:
        print(f"research-contract: STOP — {exc}", file=sys.stderr)
        return 1
    print(f"research-contract: {len(units)} units cover the completed brief")
    return 0


if __name__ == "__main__":
    sys.exit(main())
