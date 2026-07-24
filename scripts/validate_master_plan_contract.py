#!/usr/bin/env python3
"""Validate semantic chapter-card transitions before commissioning."""
import argparse
import re
import sys
from pathlib import Path
import master_plan_contract_context as context
import validate_research_contract as research


CARD = re.compile(r"^###\s+(C-\d{2})\s+—[^\n]+$", re.M)
FIELD = context.FIELD
META = re.compile(r"^\*\*([^*:\n]+):\*\*\s*(.*?)\s*$", re.M)
ARC_ROW = re.compile(r"^\|\s*(C-\d{2})\s*\|.*\|\s*(\d+)\s*\|\s*$", re.M)
PLACEHOLDER = re.compile(
    r"<[^>\n]+>|\[\s*(?:tbd|todo|fill)[^\]]*\]|"
    r"\b(?:tbd|todo|unknown|unresolved|undecided|pending)\b",
    re.I,
)
ARGUMENT_JOB = re.compile(r"^enacted transition\s+—\s+.+$", re.I)
NON_ARGUMENT_JOB = re.compile(
    r"^non-argument\s+—\s+(?:definition|safety|recap|bridge|hand-off)\b.*$",
    re.I,
)
DEFERRED_JOB = re.compile(
    r"\b(?:setup|topic coverage|catalogu(?:e|ing)|future investigation|"
    r"prospectus|later demolition|keep reading)\b",
    re.I,
)
BASE_FIELDS = {
    "Primary persuasive job", "Objection / justification resolved",
    "Arc and curve", "Target personas / reader voice",
    "Evidence IDs and required limits", "Mantras", "Instruction",
    "Concrete scene / original analogy", "Structural responsibility",
    "Guardrails", "Continuity intent", "Word budget",
}
TRANSITION_FIELDS = {
    "Entering belief", "Concrete subject-specific encounter",
    "Enacted discovery", "Emotional turn", "Leaving belief",
    "Assumptions handed forward", "Work reserved elsewhere",
}
ALLOW_NONE = {
    "Evidence IDs and required limits", "Mantras", "Instruction",
    "Structural responsibility", "Objection / justification resolved",
    "Work reserved elsewhere",
}
CANONICAL = ("Evidence ledger", "Mantra sheet", "Instruction spine",
             "Arc and length map", "Compact chapter cards")
EVIDENCE_COLUMNS = (
    "ID", "Finding / lived material", "Research unit IDs", "Source ID",
    "Grade or outcome tier", "Scope and limit", "Permitted inference",
    "Prohibited inference",
)


ContractError = context.ContractError


def _is_none(value):
    bare = value.strip().casefold().rstrip(".?!").strip()
    return bare == "none" or bare.startswith(("none —", "none by design"))


def _filled(value, owner, allow_none=False):
    clean = value.strip()
    bare = clean.casefold().rstrip(".?!").strip()
    if PLACEHOLDER.search(clean) or not clean:
        raise ContractError(f"{owner}: unresolved value")
    if bare in {"-", "—", "?", "n/a", "not applicable"} or _is_none(clean):
        if not allow_none:
            raise ContractError(f"{owner}: unresolved value")
    return clean


def _fields(body, required, owner):
    found = {}
    for name, value in FIELD.findall(body):
        if name in found:
            raise ContractError(f"{owner}: duplicate field {name}")
        found[name] = value.strip()
    missing, extra = required - found.keys(), found.keys() - required
    if missing:
        raise ContractError(f"{owner}: missing field {sorted(missing)[0]}")
    if extra:
        raise ContractError(f"{owner}: unknown field {sorted(extra)[0]}")
    for name, value in found.items():
        _filled(value, f"{owner}.{name}", name in ALLOW_NONE)
    return found


def _positive(value, owner):
    if not value.isdigit() or int(value) <= 0:
        raise ContractError(f"{owner}: invalid positive integer")
    return int(value)


def _defined_ids(text, prefix):
    ids = re.findall(rf"(?m)^\|\s*({prefix}-\d+)\s*\|", text)
    if len(ids) != len(set(ids)):
        raise ContractError(f"{prefix}: duplicate plan-wide inventory ID")
    return set(ids)


def _check_refs(fields, definitions, owner):
    for name, prefix in (
        ("Evidence IDs and required limits", "E"),
        ("Mantras", "M"),
        ("Instruction", "I"),
    ):
        value = fields[name]
        if _is_none(value):
            continue
        refs = set(re.findall(rf"\b{prefix}-\d+\b", value))
        if not refs or not refs <= definitions[prefix]:
            raise ContractError(f"{owner}.{name}: unresolved plan-wide ID")


def _research_ledger(text, report):
    """Bind every accepted plan evidence row to the sealed unit inventory."""
    body = context.sections(text, CANONICAL)["Evidence ledger"]
    table = [line for line in body.splitlines() if line.lstrip().startswith("|")]
    if len(table) < 3:
        raise ContractError("evidence ledger is missing its canonical table")
    headings = tuple(cell.strip() for cell in table[0].strip().strip("|").split("|"))
    if headings != EVIDENCE_COLUMNS:
        raise ContractError("evidence ledger header must bind Research unit IDs")
    units = report.get("inventory", {}).get("units", {}) if isinstance(report, dict) else {}
    if not isinstance(units, dict):
        raise ContractError("sealed research unit inventory is malformed")
    seen = set()
    for line in table[2:]:
        values = tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
        if len(values) != len(headings):
            raise ContractError("evidence ledger row shape is invalid")
        row = dict(zip(headings, values))
        evidence_id = row["ID"]
        if re.fullmatch(r"E-\d+", evidence_id) is None or evidence_id in seen:
            raise ContractError("evidence ledger ID is invalid or duplicated")
        seen.add(evidence_id)
        unit_ids = sorted(set(re.findall(r"\b(?:LEU|SEU)-\d{3}\b",
                                         row["Research unit IDs"])))
        if not unit_ids or any(unit_id not in units for unit_id in unit_ids):
            raise ContractError(f"{evidence_id}: research unit is absent from current seal")
        locators, permitted_values, prohibited_values = set(), set(), set()
        for unit_id in unit_ids:
            unit = units[unit_id]
            try:
                unit_locators = unit["locators"]
                permitted = unit["permitted_inference"]
                prohibited = unit["prohibited_inference"]
            except (KeyError, TypeError) as exc:
                raise ContractError(f"{evidence_id}: sealed unit authority is malformed") from exc
            if not isinstance(unit_locators, list) or not unit_locators \
                    or not isinstance(permitted, str) or not permitted \
                    or not isinstance(prohibited, str) or not prohibited:
                raise ContractError(f"{evidence_id}: inference limits differ from sealed units")
            locators.update(unit_locators)
            permitted_values.add(permitted)
            prohibited_values.add(prohibited)
        if row["Permitted inference"] != "; ".join(sorted(permitted_values)) \
                or row["Prohibited inference"] != "; ".join(sorted(prohibited_values)):
            raise ContractError(f"{evidence_id}: inference limits differ from sealed units")
        row_locators = set(re.findall(r"S-\d{3}#E-\d{3}", row["Source ID"]))
        if row_locators != locators:
            raise ContractError(f"{evidence_id}: locators differ from sealed units")
    if not seen:
        raise ContractError("evidence ledger has no evidence rows")


def validate_text(text, framing_text=None):
    metadata = dict(META.findall(text))
    target = _filled(metadata.get("Target behavior", ""), "metadata.Target behavior")
    planned_count = _positive(metadata.get("Planned chapter count", ""), "metadata.Planned chapter count")
    total_budget = _positive(metadata.get("Total planned word budget", ""), "metadata.Total planned word budget")
    sections = context.sections(text, CANONICAL, "Compact chapter cards")
    card_section, arc_section = sections["Compact chapter cards"], sections["Arc and length map"]
    headings = list(CARD.finditer(card_section))
    if not headings:
        raise ContractError("chapter cards: none found")
    expected_ids = [f"C-{index:02d}" for index in range(1, len(headings) + 1)]
    card_ids = [match.group(1) for match in headings]
    if card_ids != expected_ids or planned_count != len(card_ids):
        raise ContractError("chapter cards: IDs/count do not match the planned sequence")
    arc_rows = ARC_ROW.findall(arc_section)
    if len(ARC_ROW.findall(text)) != len(arc_rows):
        raise ContractError("arc-map rows may appear only in the canonical arc section")
    if len(arc_rows) != len(card_ids) or len({row[0] for row in arc_rows}) != len(arc_rows):
        raise ContractError("arc map must allocate exactly one budget per chapter card")
    arc_budgets = dict(arc_rows)
    if set(arc_budgets) != set(card_ids):
        raise ContractError("arc map must allocate exactly one budget per chapter card")
    definitions = {}
    for name, prefix in zip(CANONICAL[:3], "EMI"):
        definitions[prefix] = _defined_ids(sections[name], prefix)
        all_rows = re.findall(rf"(?m)^\|\s*{prefix}-\d+\s*\|", text)
        own_rows = re.findall(rf"(?m)^\|\s*{prefix}-\d+\s*\|", sections[name])
        if len(all_rows) != len(own_rows):
            raise ContractError(f"{prefix}: plan-wide inventory rows must stay in {name}")
    cards, arguments, state_ids, meaning_ids = [], [], {}, {}
    for index, match in enumerate(headings):
        card_id = match.group(1)
        end = headings[index + 1].start() if index + 1 < len(headings) else len(card_section)
        body = card_section[match.end():end]
        if FIELD.sub("", body).strip():
            raise ContractError(f"{card_id}: cards may contain only permitted semantic fields")
        raw_fields = dict(FIELD.findall(body))
        job = _filled(raw_fields.get("Primary persuasive job", ""), f"{card_id}.Primary persuasive job")
        if DEFERRED_JOB.search(job):
            raise ContractError(f"{card_id}: setup, coverage, catalogue, or deferred work cannot be the primary job")
        argument = ARGUMENT_JOB.fullmatch(job) is not None
        if not argument and NON_ARGUMENT_JOB.fullmatch(job) is None:
            raise ContractError(f"{card_id}: primary job must be an enacted transition or a necessary non-argument function")
        required = BASE_FIELDS | (TRANSITION_FIELDS if argument else set())
        fields = _fields(body, required, card_id)
        budget = _positive(fields["Word budget"], f"{card_id}.Word budget")
        if budget != _positive(arc_budgets[card_id], f"arc.{card_id}.Word budget"):
            raise ContractError(f"{card_id}: card budget does not match arc map")
        _check_refs(fields, definitions, card_id)
        cards.append((card_id, fields))
        if argument:
            entering = context.state(fields["Entering belief"], f"{card_id}.Entering belief")
            leaving = context.state(fields["Leaving belief"], f"{card_id}.Leaving belief")
            for state_id, meaning in (entering, leaving):
                if state_id in state_ids and state_ids[state_id] != meaning:
                    raise ContractError(f"{card_id}: reader-state ID maps to two beliefs")
                if meaning in meaning_ids and meaning_ids[meaning] != state_id:
                    raise ContractError(f"{card_id}: one belief uses two reader-state IDs")
                state_ids[state_id], meaning_ids[meaning] = meaning, state_id
            if entering[1] == leaving[1]:
                raise ContractError(f"{card_id}: entering and leaving beliefs must differ")
            if fields["Assumptions handed forward"] != fields["Leaving belief"]:
                raise ContractError(f"{card_id}: handed-forward assumptions must equal the leaving belief")
            if target.casefold() not in fields["Concrete subject-specific encounter"].casefold():
                raise ContractError(f"{card_id}: encounter is not subject-specific")
            arguments.append((index, card_id, fields, entering, leaving))
    if sum(int(fields["Word budget"]) for _, fields in cards) != total_budget:
        raise ContractError("chapter budgets do not equal Total planned word budget")
    positions = {card_id: index for index, (card_id, _) in enumerate(cards)}
    for arg_index, (position, card_id, fields, _, _) in enumerate(arguments):
        reserved = fields["Work reserved elsewhere"]
        refs = set(re.findall(r"\bC-\d{2}\b", reserved))
        if reserved.casefold().startswith("none —"):
            if refs:
                raise ContractError(f"{card_id}: final reservation cannot name a chapter")
        elif not refs or any(ref not in positions or positions[ref] <= position for ref in refs):
            raise ContractError(f"{card_id}: reserved work must name only future chapter cards")
        if arg_index:
            previous = arguments[arg_index - 1][2]
            if fields["Entering belief"] != previous["Assumptions handed forward"]:
                raise ContractError(f"{card_id}: entering belief breaks the prior handoff")
            if context.normalized(fields["Enacted discovery"]) == context.normalized(previous["Enacted discovery"]):
                raise ContractError(f"{card_id}: adjacent cards duplicate the enacted discovery mode")
    if framing_text is not None:
        accepted = context.framing_states(framing_text)
        planned = {card_id: (entering, leaving, context.state(fields["Assumptions handed forward"], f"{card_id}.handoff"))
                   for _, card_id, fields, entering, leaving in arguments}
        if planned != accepted:
            raise ContractError("plan transitions do not match the accepted framing journey")
    return tuple(card_id for _, card_id, *_ in arguments)


def require_master_plan_contract(book, framing=None):
    path = Path(book) / "master-plan.md"
    if not path.is_file() or not path.read_text(encoding="utf-8").strip():
        raise ContractError(f"missing or empty master plan: {path}")
    framing = Path(framing) if framing else Path(book) / "framing.md"
    if not framing.is_file() or not framing.read_text(encoding="utf-8").strip():
        raise ContractError(f"missing or empty accepted framing: {framing}")
    text = path.read_text(encoding="utf-8")
    validate_text(text, framing.read_text(encoding="utf-8"))
    try:
        report = research.inspect_research(book, require_seal=True)
    except (research.ContractError, OSError) as exc:
        raise ContractError(f"accepted research is not current: {exc}") from exc
    if not isinstance(report, dict) or not report.get("ok") \
            or not isinstance(report.get("seal_identity"), str) \
            or not report["seal_identity"]:
        blockers = report.get("blockers", ()) if isinstance(report, dict) else ()
        detail = "; ".join(str(item) for item in blockers) or "missing accepted seal"
        raise ContractError(f"accepted research is not current: {detail}")
    _research_ledger(text, report)
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    args = parser.parse_args(argv)
    try:
        path = require_master_plan_contract(args.book)
    except (ContractError, OSError) as exc:
        print(f"master-plan-contract: STOP — {exc}", file=sys.stderr)
        return 1
    print(f"master-plan-contract: {path} has complete semantic chapter cards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
