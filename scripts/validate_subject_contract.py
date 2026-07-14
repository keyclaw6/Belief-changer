#!/usr/bin/env python3
"""Fail-closed gate for downstream book work that consumes 00-brief.md."""
import argparse
import re
import sys
from pathlib import Path


STAGES = ("research-synthesis", "framing", "planning")
SCALAR_FIELDS = (
    "Target behavior",
    "Intended reader",
    "Destination",
    "Exclusions",
    "Safety perimeter",
)
BELIEF_FIELDS = ("Primary false belief", "Subordinate beliefs")
FORKS = (
    "Outcome (Fork 2)",
    "Void (Fork 5)",
    "Science weight (Fork 3)",
    "Villain (Fork 4)",
    "Inner state (Fork 1)",
)
HEADING = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
FORK_LINE = re.compile(r"^-\s+\*\*(.+?):\*\*\s*(.+?)\s*$")
QUOTED_BELIEF = re.compile(r'^-\s+(?:"[^"\n]+"|“[^”\n]+”)$')
PLACEHOLDER = re.compile(
    r"<[^>\n]+>|\b(?:tbd|todo|unknown|unresolved|undecided)\b|"
    r"\b(?:choose|decide|fill in)\b|\s\|\s|\bversus\b|\bvs\.?\b|"
    r"\[\s*(?:fill|todo|tbd)[^\]]*\]",
    re.IGNORECASE,
)
UNRESOLVED_VALUES = {
    "pending",
    "pending research",
    "pending review",
    "to be confirmed",
    "to be decided",
    "to be determined",
    "tbc",
}


class ContractError(ValueError):
    pass


def _sections(text):
    matches = list(HEADING.finditer(text))
    sections = {}
    for index, match in enumerate(matches):
        name = match.group(1).strip()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        if name in sections:
            raise ContractError(f"duplicate section: {name}")
        sections[name] = text[match.end():end].strip()
    return sections


def _unresolved(value):
    clean = value.strip()
    bare = re.sub(r"^-\s+", "", clean).strip()
    if len(bare) >= 2 and (bare[0], bare[-1]) in {('"', '"'), ("“", "”")}:
        bare = bare[1:-1].strip()
    normalized = bare.casefold().rstrip(".?!").strip()
    return (
        not clean
        or normalized in {
            "", "-", "—", "?", "none", "n/a", "not applicable",
            *UNRESOLVED_VALUES,
        }
        or re.fullmatch(r"[.?!]+", bare) is not None
        or PLACEHOLDER.search(clean) is not None
    )


def _require_content(sections, name):
    if name not in sections:
        raise ContractError(f"missing section: {name}")
    if _unresolved(sections[name]):
        raise ContractError(f"unresolved section: {name}")
    return sections[name]


def _validate_forks(sections):
    body = _require_content(sections, "Fork decisions")
    found = {}
    for line in (line.strip() for line in body.splitlines() if line.strip()):
        match = FORK_LINE.fullmatch(line)
        if match is None:
            raise ContractError("Fork decisions must contain only named fork bullets")
        name, value = match.groups()
        if name in found:
            raise ContractError(f"duplicate fork decision: {name}")
        found[name] = value
    for name in FORKS:
        if name not in found:
            raise ContractError(f"missing fork decision: {name}")
        if _unresolved(found[name]):
            raise ContractError(f"unresolved fork decision: {name}")
    extras = set(found) - set(FORKS)
    if extras:
        raise ContractError(f"unknown fork decision: {sorted(extras)[0]}")


def _validate_beliefs(sections, name, minimum, maximum):
    body = _require_content(sections, name)
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    if not minimum <= len(lines) <= maximum:
        raise ContractError(f"{name} must contain {minimum}–{maximum} beliefs")
    for line in lines:
        if QUOTED_BELIEF.fullmatch(line) is None:
            raise ContractError(f"{name} beliefs must be quoted reader-language bullets")
        if _unresolved(line):
            raise ContractError(f"unresolved belief in: {name}")


def validate_text(text):
    sections = _sections(text)
    for name in SCALAR_FIELDS:
        _require_content(sections, name)
    _validate_forks(sections)
    _validate_beliefs(sections, "Primary false belief", 1, 1)
    _validate_beliefs(sections, "Subordinate beliefs", 3, 5)


def require_subject_contract(book, stage):
    if stage not in STAGES:
        raise ContractError(f"unknown downstream stage: {stage}")
    brief = Path(book) / "00-brief.md"
    if not brief.is_file():
        raise ContractError(f"missing brief: {brief}")
    text = brief.read_text(encoding="utf-8")
    if not text.strip():
        raise ContractError(f"empty brief: {brief}")
    validate_text(text)
    return brief


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True, help="production-books/<slug> directory")
    parser.add_argument("--stage", required=True, choices=STAGES)
    args = parser.parse_args(argv)
    try:
        brief = require_subject_contract(args.book, args.stage)
    except (ContractError, OSError) as exc:
        print(f"subject-contract: STOP — {exc}", file=sys.stderr)
        return 1
    print(f"subject-contract: {brief} is complete for {args.stage}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
