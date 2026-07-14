#!/usr/bin/env python3
"""Validate an independent, hash-bound cumulative master-plan review."""
import argparse
import hashlib
import re
import sys
from pathlib import Path

FIELD = re.compile(r"^-\s+\*\*([^*:\n]+):\*\*\s*(.*?)\s*$")
ROLE = "independent high-reasoning native planning-family reviewer"
INDEPENDENCE = "fresh context; independent of master-plan author, framing planner, and chapter writer"
BLINDNESS = "PASS — no reference prose, analysis, calibration, chapters, prior reviews, or judge output received"
META = {
    "Reviewer role", "Fresh-context independence", "Exact runtime model ID",
    "Reasoning configuration", "Reference blindness", "Reviewed plan",
    "Master-plan SHA-256", "Reviewed framing", "Framing SHA-256",
}
CHECKS = (
    "First-three cumulative walk", "Whole-book cumulative walk",
    "Opening persuasive work", "Deferred catalogue or future investigation",
    "Adjacent discovery modes", "Leaving-belief handoffs",
    "Writer-facing authority", "Other material blocker",
)
VERDICTS = {"fit to write from", "needs changes first"}
LOCATION = re.compile(r"(?:C-\d{2}(?:,\s*C-\d{2})*|whole-book)")
PLACEHOLDER = re.compile(r"<[^>\n]+>|^\s*(?:tbd|todo|pending|unresolved|unknown)\s*$", re.I)
UNFINISHED = re.compile(
    r"\b(?:pending|todos?|tbds?|incomplete|unfinished|unreviewed|"
    r"not(?:[\s-]+yet)?[\s-]+reviewed(?:[\s-]+yet)?|not\s+(?:yet\s+)?complete|"
    r"await(?:s|ing)\s+review|to\s+be\s+reviewed)\b",
    re.I,
)
RESOLVED_NEGATION = re.compile(
    r"\b(?:no|zero|without|not)\s+(?:pending|todos?|tbds?|incomplete|unfinished|unreviewed)\b",
    re.I,
)
MODEL = re.compile(r"gpt-5\.6-sol")
POOL = "<!-- Required reviewer: GPT-5.6 Sol | gpt-5.6-sol | fresh native Codex subagent -->"


class ContractError(ValueError):
    pass


def _digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _unfinished(value):
    return UNFINISHED.search(RESOLVED_NEGATION.sub("", value)) is not None


def _parse(text):
    nonblank = [(index, line) for index, line in enumerate(text.splitlines()) if line.strip()]
    if not nonblank or nonblank[-1][1] not in VERDICTS:
        raise ContractError("review must end with an exact standalone verdict")
    verdict_index, verdict = nonblank[-1]
    fields = {}
    for index, line in enumerate(text.splitlines()):
        if not line.strip() or line == POOL:
            continue
        if line.startswith("# Master Plan Review — ") and "<" not in line:
            continue
        if line in {"## Review identity and binding", "## Cumulative reader-walk findings"}:
            continue
        if index == verdict_index and line == verdict:
            continue
        match = FIELD.fullmatch(line)
        if match is None:
            raise ContractError("review contains unstructured or malformed content")
        name, value = match.groups()
        if name in fields:
            raise ContractError(f"duplicate review field: {name}")
        if not value or PLACEHOLDER.search(value):
            raise ContractError(f"unresolved review field: {name}")
        fields[name] = value
    required = META | set(CHECKS)
    missing, extra = required - fields.keys(), fields.keys() - required
    if missing:
        raise ContractError(f"missing review field: {sorted(missing)[0]}")
    if extra:
        raise ContractError(f"unknown review field: {sorted(extra)[0]}")
    return fields, verdict


def validate_review(text, plan, framing):
    fields, verdict = _parse(text)
    if fields["Reviewer role"] != ROLE or "writer" in fields["Reviewer role"].casefold():
        raise ContractError("reviewer must be an independent planning-family reviewer, not a writer")
    if MODEL.fullmatch(fields["Exact runtime model ID"]) is None:
        raise ContractError("runtime model must be the exact native planning-review model gpt-5.6-sol")
    if fields["Reasoning configuration"] != "xhigh":
        raise ContractError("planning review must use xhigh reasoning")
    if fields["Fresh-context independence"] != INDEPENDENCE:
        raise ContractError("review does not establish fresh-context independence")
    if fields["Reference blindness"] != BLINDNESS:
        raise ContractError("review does not establish reference blindness")
    if fields["Reviewed plan"] != "complete master-plan.md" or fields["Reviewed framing"] != "exact accepted framing.md":
        raise ContractError("review does not cover the exact complete plan and accepted framing")
    if fields["Master-plan SHA-256"] != _digest(plan):
        raise ContractError("review is stale for master-plan.md")
    if fields["Framing SHA-256"] != _digest(framing):
        raise ContractError("review is stale for accepted framing.md")
    blocked = False
    for name in CHECKS:
        value = fields[name]
        if value.startswith("PASS — "):
            detail = value[len("PASS — "):].strip()
            if _unfinished(detail):
                raise ContractError(f"unresolved cumulative review finding: {name}")
            if (name == "Other material blocker" and detail == "none") or len(detail) >= 12:
                continue
        if value.startswith("BLOCK — plan | "):
            parts = [part.strip() for part in value.split("|", 2)]
            correction = parts[2].split(";", 1) if len(parts) == 3 else ()
            if (len(parts) == 3 and LOCATION.fullmatch(parts[1]) and len(correction) == 2
                    and all(len(part.strip()) >= 8 for part in correction)):
                blocked = True
                continue
        raise ContractError(f"malformed cumulative review finding: {name}")
    expected = "needs changes first" if blocked else "fit to write from"
    if verdict != expected:
        raise ContractError(f"verdict must be {expected}")
    return verdict


def require_master_plan_review(book, plan=None, framing=None):
    book = Path(book)
    path = book / "master-plan-review.md"
    if not path.is_file() or not path.read_text(encoding="utf-8").strip():
        raise ContractError(f"missing or empty master plan review: {path}")
    plan = Path(plan) if plan else book / "master-plan.md"
    framing = Path(framing) if framing else book / "framing.md"
    verdict = validate_review(path.read_text(encoding="utf-8"), plan, framing)
    if verdict != "fit to write from":
        raise ContractError("master plan review verdict is needs changes first")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    args = parser.parse_args(argv)
    try:
        path = require_master_plan_review(args.book)
    except (ContractError, OSError) as exc:
        print(f"master-plan-review: STOP — {exc}", file=sys.stderr)
        return 1
    print(f"master-plan-review: {path} is fit to write from")
    return 0


if __name__ == "__main__":
    sys.exit(main())
