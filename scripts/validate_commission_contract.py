#!/usr/bin/env python3
"""Validate a free-form semantic commission against its assigned authority."""
import re


REQUIRED = {
    "assumptions received", "entering belief", "leaving belief", "situation",
    "reader wording", "permitted mechanism", "emotional turn",
    "empirical limits", "safety limits", "handoff",
    "assumptions handed forward", "reserved work",
}
SOURCE_OWNED = {"situation", "reader wording", "permitted mechanism", "empirical limits"}
SOURCE_STATUS = {"EXACT_QUOTE", "INTERPRETATION"}
QUOTABLE_SEMANTICS = {"entering belief", "leaving belief"}
IDENTIFIER = re.compile(
    r"\b(?:S-\d{3}#E-\d{3}|(?:LEU|SEU|GAP)-\d{3}|"
    r"(?:RS|BG|CH|AU|C|E|M|I|P|S)-\d{2,3})\b"
)
QUOTE = re.compile(r'"([^"\n]+)"|“([^”\n]+)”')
ANATOMY = re.compile(
    r"(?im)^[ \t]*(?:#{1,6}\s*)?(?:opening|(?:section|scene)\s+\d+"
    r"(?:\s*[—:-].*)?|conclusion|summary)\s*:?[ \t]*$|"
    r"^[ \t]*(?:\d+[.)]|first[:,]|then[:,]|next[:,]|finally[:,])"
)
DRAFT_DIRECTION = re.compile(
    r"(?im)^[ \t]*(?:(?:open|begin|start|close|end) (?:the chapter|with|by)\b|"
    r"(?:write|say) (?:this|these|the following|exactly)\b|"
    r"ask the reader(?:\s*:|\s+to\b)).*$"
)


class ContractError(ValueError):
    pass


def _blocked(text, blocker):
    expected = (
        f"COMMISSION BLOCKED\nOwner: {blocker['owner']}\n"
        f"Gap: {blocker['gap']}"
    )
    if text != expected:
        raise ContractError("COMMISSION BLOCKED must name the exact owning gap")
    return "blocked"


def _quote_spans(value):
    return {match.group(1) or match.group(2) for match in QUOTE.finditer(value)}


def _evidence(authority, required, text):
    evidence = authority.get("assigned_evidence", {})
    grounded = set()
    source_quotes = set()
    for locator, binding in evidence.items():
        if not re.fullmatch(r"S-\d{3}#E-\d{3}", locator):
            raise ContractError(f"invalid assigned evidence locator: {locator}")
        values, statuses = binding.get("values", {}), binding.get("statuses", {})
        provenance = binding.get("provenance", "")
        for name, value in values.items():
            status = statuses.get(name)
            if name not in SOURCE_OWNED or required.get(name) != value or status not in SOURCE_STATUS:
                raise ContractError(f"COMMISSION BLOCKED required for unsupported source-owned field: {name}")
            if name not in provenance or status not in provenance:
                raise ContractError(f"assigned evidence provenance does not bind {name}: {locator}")
            grounded.add(name)
            if status == "EXACT_QUOTE":
                source_quotes.add(value)
        if locator not in provenance or provenance not in text:
            raise ContractError(f"commission lacks assigned evidence provenance: {locator}")
    missing = SOURCE_OWNED - grounded
    if missing:
        raise ContractError(
            f"COMMISSION BLOCKED required for unsupported source-owned field: {sorted(missing)[0]}"
        )
    return evidence, source_quotes


def validate_text(text, authority):
    """Return ``commission`` or ``blocked``; raise on authority leakage."""
    text = text.strip()
    blocker = authority.get("blocker")
    if blocker:
        return _blocked(text, blocker)
    if text.startswith("COMMISSION BLOCKED"):
        raise ContractError("COMMISSION BLOCKED has no supplied owning gap")
    target = authority["target"]
    if not text.startswith(f"AUTHORITATIVE SEMANTIC COMMISSION — {target}\n"):
        raise ContractError("missing exact authoritative commission title")
    required = authority.get("required", {})
    missing_keys = REQUIRED - required.keys()
    if missing_keys:
        raise ContractError(f"authority lacks {sorted(missing_keys)[0]}")
    for name, value in required.items():
        if value not in text:
            raise ContractError(f"commission lacks assigned {name}")
    evidence, source_quotes = _evidence(authority, required, text)
    resolved_ids = authority.get("resolved_ids", {})
    for identifier in IDENTIFIER.findall(text):
        if identifier.startswith("GAP-"):
            raise ContractError(f"COMMISSION BLOCKED required for research gap: {identifier}")
        if identifier in evidence:
            continue
        if identifier not in resolved_ids:
            raise ContractError(f"unresolved or unassigned ID: {identifier}")
        if resolved_ids[identifier] not in text:
            raise ContractError(f"ID lacks its resolved meaning: {identifier}")
    allowed_quotes = source_quotes | set(authority.get("frozen_tokens", ()))
    for name in QUOTABLE_SEMANTICS:
        allowed_quotes.add(required[name])
        allowed_quotes.update(_quote_spans(required[name]))
    quotes = []
    for match in QUOTE.finditer(text):
        quote = match.group(1) or match.group(2)
        quotes.append(quote)
        if quote not in allowed_quotes:
            raise ContractError("quote is not assigned source or frozen text")
    if required["reader wording"] not in quotes:
        raise ContractError("assigned reader wording must remain an exact quotation")
    for token in authority.get("frozen_tokens", ()):
        if text.count(token) != 1:
            raise ContractError(f"frozen token must appear exactly once: {token}")
    for phrase in authority.get("forbidden", ()):
        if phrase.casefold() in text.casefold():
            raise ContractError(f"unassigned or prohibited material: {phrase}")
    if ANATOMY.search(text) or DRAFT_DIRECTION.search(text):
        raise ContractError("commission contains outline anatomy or drafted prose")
    return "commission"
