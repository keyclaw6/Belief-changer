#!/usr/bin/env python3
"""Validate the independent semantic authority review bound to framing.md."""
import hashlib
import re
from pathlib import Path

FIELD = re.compile(r"^-\s+\*\*([^*:\n]+):\*\*\s*(.*?)\s*$", re.M)
REQUIRED = {
    "Reviewer role", "Independence", "Reviewed artifact", "Framing SHA-256",
    "Invented pedigree", "Unsupported danger", "Evidence overreach", "Verdict",
}
FINDINGS = ("Invented pedigree", "Unsupported danger", "Evidence overreach")


class ContractError(ValueError):
    pass


def require_framing_review(book, framing, framing_roles):
    book, framing = Path(book), Path(framing)
    path = book / "framing-review.md"
    if not path.is_file() or not path.read_text(encoding="utf-8").strip():
        raise ContractError(f"missing or empty semantic review: {path}")
    fields = {}
    for name, value in FIELD.findall(path.read_text(encoding="utf-8")):
        if name in fields:
            raise ContractError(f"duplicate review field: {name}")
        fields[name] = value.strip()
    missing, extra = REQUIRED - fields.keys(), fields.keys() - REQUIRED
    if missing:
        raise ContractError(f"missing review field: {sorted(missing)[0]}")
    if extra:
        raise ContractError(f"unknown review field: {sorted(extra)[0]}")
    role = fields["Reviewer role"].casefold()
    if not all(token in role for token in ("independent", "high-reasoning", "native", "planning-family", "reviewer")):
        raise ContractError("reviewer must be an independent high-reasoning native planning-family role")
    if role in {value.casefold() for value in framing_roles.values()}:
        raise ContractError("semantic reviewer must be distinct from planner and writer")
    independence = fields["Independence"].casefold()
    if "framing planner" not in independence or "writer" not in independence:
        raise ContractError("review must declare independence from framing planner and writer")
    if fields["Reviewed artifact"] != "complete framing.md":
        raise ContractError("review must inspect complete framing.md")
    digest = hashlib.sha256(framing.read_bytes()).hexdigest()
    if fields["Framing SHA-256"] != digest:
        raise ContractError("review is not bound to the current complete framing.md")
    for name in FINDINGS:
        if not fields[name].startswith("PASS — ") or len(fields[name]) <= len("PASS — "):
            raise ContractError(f"blocking semantic review finding: {name}")
    if fields["Verdict"] != "ACCEPTED FOR PLANNING":
        raise ContractError("semantic review verdict is not ACCEPTED FOR PLANNING")
    return path
