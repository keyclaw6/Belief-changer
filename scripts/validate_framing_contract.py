#!/usr/bin/env python3
"""Validate framing's belief graph, earned authority, and reader journey."""
import argparse, re, sys
from pathlib import Path
import validate_research_contract as research
import validate_subject_contract as subject
HEADING = re.compile(r"^###\s+([A-Z]+-\d{2})(?:\s+—[^\n]+)?\s*$", re.M)
FIELD = re.compile(r"^-\s+\*\*([^*:\n]+):\*\*\s*(.*?)\s*$", re.M)
PLAYBOOK = re.compile(r"^(\d+)\.\s+\*\*([^*:\n]+):\*\*\s*(.*?)\s*$", re.M)
PLACEHOLDER = re.compile(r"<[^>\n]+>|\[\s*(?:tbd|todo|fill)[^\]]*\]", re.I)
UNRESOLVED = {"", "-", "—", "?", "n/a", "not applicable", "none", "pending", "tbd", "todo", "unknown", "undecided", "unresolved", "to be decided", "to be determined"}
STATE = re.compile(r"^(RS-\d{2})\s+\|\s+(.+)$")
UNIT_REFS = re.compile(r"(?:LEU|SEU)-\d{3}(?:,\s*(?:LEU|SEU)-\d{3})*")
GRAPH_REFS = re.compile(r"BG-\d{2}(?:,\s*BG-\d{2})*")
FORMAT_FIELDS = {"Format", "Redefinition decision"}
PERSONA_FIELDS = {"Function", "Load-bearing belief", "Dialect"}
PLAYBOOK_FIELDS = (
    "Load-bearing false belief", "Illusory benefit and inversion", "Justifications to demolish",
    "Engineered villain", "Physical or chemical reality and science weight",
    "Natural baseline or root and replacement", "Behavior-specific analogies", "Escape routes to foreclose",
    "Strongest seductive scene", "Moment of revelation",
)
MANTRA_FIELDS = {
    "Trap-namer", "Illusion-namer", "Mechanism characters", "Sensory definition", "Named anti-method",
    "Named conflict model", "Named positive authority", "Terminal mantra", "Claim block",
}
JOURNEY_FIELDS = {
    "Belief nodes resolved", "Entering belief", "Subject-specific encounter", "Discovery mechanism",
    "Emotional turn", "Leaving belief", "Handed-forward state", "Reserved work",
}
class ContractError(ValueError):
    pass
def _filled(value, owner, allow_none=False):
    clean = value.strip()
    bare = clean.strip('"“”').casefold().rstrip(".?!").strip()
    unresolved = UNRESOLVED - ({"none"} if allow_none else set())
    if PLACEHOLDER.search(clean) or bare in unresolved:
        raise ContractError(f"{owner}: unresolved value")
    return clean
def _fields(body, required, owner, allow_none=()):
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
        _filled(value, f"{owner}.{name}", name in allow_none)
    return found
def _blocks(body, prefix):
    headings = list(HEADING.finditer(body))
    matches = [match for match in headings if match.group(1).startswith(prefix + "-")]
    if len(matches) != len(headings):
        raise ContractError(f"{prefix}: invalid block heading")
    seen = set()
    for index, match in enumerate(matches):
        item_id = match.group(1)
        if item_id in seen:
            raise ContractError(f"duplicate block: {item_id}")
        seen.add(item_id)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        yield item_id, body[match.end():end]
def _legacy_contract(sections):
    metadata = _fields(sections["Contract metadata"], {"Planner role", "Writer role"}, "metadata")
    planner, writer = metadata["Planner role"].casefold(), metadata["Writer role"].casefold()
    if "high-reasoning" not in planner or "native" not in planner:
        raise ContractError("metadata: planner must be high-reasoning and native")
    if planner == writer or "writer" not in writer:
        raise ContractError("metadata: planner and writer roles must be distinct")
    format_body = sections["Format and scope decisions"]
    header = format_body.split("###", 1)[0]
    format_fields = _fields(header, FORMAT_FIELDS, "format")
    if not format_fields["Format"].casefold().startswith(("pocket", "full-length")):
        raise ContractError("format: choose pocket or full-length")
    personas = list(_blocks(format_body[len(header):], "P"))
    if not 3 <= len(personas) <= 6:
        raise ContractError("personas: require 3–6")
    for item_id, body in personas:
        _fields(body, PERSONA_FIELDS, item_id)
    answers = PLAYBOOK.findall(sections["Style-guide Section 10 adaptation playbook"])
    if len(answers) != 10 or tuple(name for _, name, _ in answers) != PLAYBOOK_FIELDS:
        raise ContractError("playbook: all ten named answers are required in order")
    for number, (_, _, value) in enumerate(answers, 1):
        _filled(value, f"playbook.{number}")
    _fields(sections["Mantra seeds"], MANTRA_FIELDS, "mantras")
    _filled(sections["Personal-experience use"], "personal experiences")
    _fields(sections["Fork positions"], {f"Fork {n}" for n in range(1, 6)}, "forks")
    return metadata
def _quoted(value, owner):
    if len(value) < 3 or (value[0], value[-1]) not in {('\"', '\"'), ('“', '”')}:
        raise ContractError(f"{owner}: belief must be quoted")
    return value[1:-1].strip()
def _graph(body, beliefs):
    nodes = {}
    for node_id, block in _blocks(body, "BG"):
        fields = _fields(block, {"Kind", "Belief", "Depends on"}, node_id, {"Depends on"})
        kind = fields["Kind"].casefold()
        if kind not in {"primary", "subordinate"}:
            raise ContractError(f"{node_id}: invalid belief kind")
        deps = set() if fields["Depends on"].casefold() == "none" else set(
            GRAPH_REFS.fullmatch(fields["Depends on"]).group(0).replace(" ", "").split(",")
        ) if GRAPH_REFS.fullmatch(fields["Depends on"]) else None
        if deps is None:
            raise ContractError(f"{node_id}: invalid dependency list")
        nodes[node_id] = {"kind": kind, "belief": _quoted(fields["Belief"], node_id), "deps": deps}
    if len(nodes) != len(beliefs) or {node["belief"] for node in nodes.values()} != set(beliefs):
        raise ContractError("belief graph must cover the completed brief exactly once")
    primaries = [key for key, node in nodes.items() if node["kind"] == "primary"]
    if len(primaries) != 1 or nodes[primaries[0]]["belief"] != beliefs[0]:
        raise ContractError("belief graph must identify the brief's primary belief")
    if any(node["kind"] != "subordinate" for key, node in nodes.items() if key != primaries[0]):
        raise ContractError("belief graph mislabels a subordinate belief")
    for key, node in nodes.items():
        if key in node["deps"] or not node["deps"] <= nodes.keys():
            raise ContractError(f"{key}: invalid dependency")
    visiting, reached = set(), set()
    def visit(key):
        if key in visiting:
            raise ContractError("belief graph contains a cycle")
        if key in reached:
            return
        visiting.add(key)
        for dep in nodes[key]["deps"]:
            visit(dep)
        visiting.remove(key)
        reached.add(key)
    visit(primaries[0])
    if reached != nodes.keys():
        raise ContractError("belief graph has an unconnected belief")
    return nodes
def _unit_details(book, accepted):
    details = {}
    for name in ("lived-experience.md", "scientific-evidence.md"):
        text = (book / "research" / name).read_text(encoding="utf-8")
        for item_id, body in research._blocks(text, research.ENTRY_HEADING):
            if item_id in accepted:
                details[item_id] = research._fields(body, item_id)
    return details
def _authority(body, target, units):
    moves = {}
    required = {"Basis", "Subject-specific move", "Evidence units", "Claim", "Danger claim", "Limits"}
    for item_id, block in _blocks(body, "AU"):
        fields = _fields(block, required, item_id, {"Evidence units", "Danger claim"})
        basis = fields["Basis"].casefold()
        if basis in moves or basis not in {"recognition", "bounded lived pattern", "logic"}:
            raise ContractError(f"{item_id}: invalid or duplicate authority basis")
        if target.casefold() not in fields["Subject-specific move"].casefold():
            raise ContractError(f"{item_id}: authority move is not subject-specific")
        if basis == "logic":
            if fields["Evidence units"].casefold() != "none" or fields["Danger claim"].casefold() != "none":
                raise ContractError(f"{item_id}: logic cannot invent evidence or danger")
        else:
            match = UNIT_REFS.fullmatch(fields["Evidence units"])
            refs = match.group(0).replace(" ", "").split(",") if match else []
            if not refs or not set(refs) <= units.keys():
                raise ContractError(f"{item_id}: unknown evidence unit")
            if fields["Claim"] not in {units[ref]["Permitted inference"] for ref in refs}:
                raise ContractError(f"{item_id}: claim exceeds permitted inference")
            if fields["Limits"] not in {units[ref]["Prohibited inference"] for ref in refs}:
                raise ContractError(f"{item_id}: evidence limits are not preserved")
            danger = fields["Danger claim"]
            if danger.casefold() != "none" and danger not in {
                units[ref]["Permitted inference"] for ref in refs if ref.startswith("SEU-")
            }:
                raise ContractError(f"{item_id}: unsupported danger claim")
        moves[basis] = fields
    if set(moves) != {"recognition", "bounded lived pattern", "logic"}:
        raise ContractError("authority: recognition, bounded lived pattern, and logic are required")
def _state(value, owner):
    match = STATE.fullmatch(value)
    if not match: raise ContractError(f"{owner}: invalid reader state")
    meaning = re.sub(r"[^\w]+", " ", match.group(2).casefold()).strip()
    if not meaning: raise ContractError(f"{owner}: unresolved reader-state meaning")
    return match.group(1), meaning
def _journey(body, target, nodes):
    stages = []
    for item_id, block in _blocks(body, "CH"):
        fields = _fields(block, JOURNEY_FIELDS, item_id)
        refs_match = GRAPH_REFS.fullmatch(fields["Belief nodes resolved"])
        refs = set(refs_match.group(0).replace(" ", "").split(",")) if refs_match else set()
        if not refs or not refs <= nodes.keys():
            raise ContractError(f"{item_id}: invalid resolved belief nodes")
        entering = _state(fields["Entering belief"], f"{item_id}.Entering belief")
        leaving = _state(fields["Leaving belief"], f"{item_id}.Leaving belief")
        if entering[1] == leaving[1]:
            raise ContractError(f"{item_id}: entering and leaving beliefs must be distinct states")
        if fields["Handed-forward state"] != fields["Leaving belief"]:
            raise ContractError(f"{item_id}: handoff must equal the leaving state")
        if target.casefold() not in fields["Subject-specific encounter"].casefold():
            raise ContractError(f"{item_id}: encounter is not subject-specific")
        stages.append((item_id, fields, refs, entering, leaving))
    if len(stages) < 2:
        raise ContractError("journey: at least two argument-bearing stages are required")
    resolved, state_ids, meaning_ids = set(), {}, {}
    for index, (item_id, fields, refs, entering, leaving) in enumerate(stages):
        for state_id, meaning in (entering, leaving):
            if state_id in state_ids and state_ids[state_id] != meaning:
                raise ContractError(f"{item_id}: state ID maps to two meanings")
            if meaning in meaning_ids and meaning_ids[meaning] != state_id:
                raise ContractError(f"{item_id}: duplicate belief meaning under a new state ID")
            state_ids[state_id], meaning_ids[meaning] = meaning, state_id
        if refs & resolved:
            raise ContractError(f"{item_id}: duplicates resolved belief work")
        resolved |= refs
        future = set().union(*(later[2] for later in stages[index + 1:])) if index + 1 < len(stages) else set()
        reserved = set(re.findall(r"BG-\d{2}", fields["Reserved work"]))
        if reserved != future:
            raise ContractError(f"{item_id}: reserved work must name exactly the future belief nodes")
        if index:
            previous = stages[index - 1][1]
            if fields["Entering belief"] != previous["Handed-forward state"]:
                raise ContractError(f"{item_id}: entering state does not follow the prior handoff")
            for name in ("Subject-specific encounter", "Discovery mechanism"):
                if fields[name].casefold() == previous[name].casefold():
                    raise ContractError(f"{item_id}: adjacent stages duplicate {name.lower()}")
    if resolved != nodes.keys():
        raise ContractError("journey does not resolve every belief graph node")
def require_framing_contract(book):
    book = Path(book)
    accepted = research.require_research_contract(book)
    brief = subject._sections((book / "00-brief.md").read_text(encoding="utf-8"))
    beliefs = subject.belief_set((book / "00-brief.md").read_text(encoding="utf-8"))
    path = book / "framing.md"
    if not path.is_file() or not path.read_text(encoding="utf-8").strip():
        raise ContractError(f"missing or empty framing: {path}")
    sections = subject._sections(path.read_text(encoding="utf-8"))
    required = {
        "Contract metadata", "Format and scope decisions",
        "Style-guide Section 10 adaptation playbook", "Mantra seeds",
        "Personal-experience use", "Fork positions", "Belief graph",
        "Evidence-honest authority strategy", "Cumulative reader-state journey",
    }
    missing = required - sections.keys()
    if missing:
        raise ContractError(f"missing section: {sorted(missing)[0]}")
    metadata = _legacy_contract(sections)
    nodes = _graph(sections["Belief graph"], beliefs)
    _authority(sections["Evidence-honest authority strategy"], brief["Target behavior"], _unit_details(book, accepted))
    _journey(sections["Cumulative reader-state journey"], brief["Target behavior"], nodes)
    import validate_framing_review as review
    try: review.require_framing_review(book, path, metadata)
    except review.ContractError as exc: raise ContractError(f"authority review not ready: {exc}") from exc
    return path
def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    args = parser.parse_args(argv)
    try:
        path = require_framing_contract(args.book)
    except (ContractError, OSError, research.ContractError, subject.ContractError) as exc:
        print(f"framing-contract: STOP — {exc}", file=sys.stderr)
        return 1
    print(f"framing-contract: {path} is ready for planning")
    return 0
if __name__ == "__main__":
    sys.exit(main())
