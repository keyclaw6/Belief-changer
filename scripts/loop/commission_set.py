"""Generate and gate one selected commission set inside an RF-02 candidate."""
import json, os, re, sys
from pathlib import Path
HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))
import validate_commission_contract as CC  # noqa: E402
import validate_subject_contract as SC  # noqa: E402
import candidate_pair as CP  # noqa: E402
import pair_store as PS  # noqa: E402
RECEIPT = "commission-set-audit.json"
AUDIT_PASS = "COMMISSION SET PASS"
AUDIT_BLOCKED = re.compile(r"COMMISSION SET BLOCKED\nOwner: (?:brief|research/synthesis|framing|plan|commission/context|prose|revision|evaluation)\nGap: .+", re.S)
CARD = r"^###\s+{prefix}-0*{number}\b[^\n]*$"
NEXT_CARD = re.compile(r"^###\s+(?:C|CH)-\d+\b", re.M)
LOCATOR = re.compile(r"^(S-\d{3})#(E-\d{3})$")
class CommissionSetError(RuntimeError): pass
def _canonical(value):
    try:
        return json.loads(json.dumps(value, sort_keys=True))
    except (TypeError, ValueError) as exc: raise CommissionSetError("assignment record is not canonical JSON") from exc
def _sha_text(text): return PS.sha(text.encode("utf-8"))
def _ready_manifest(root, recover=True):
    try:
        manifest = (CP.load if recover else CP.inspect)(root); return manifest, CP._actual(root, manifest)[0]
    except (CP.PairError, PS.StoreError) as exc: raise CommissionSetError(str(exc)) from exc
def _generation_manifest(root):
    tree = CP.candidate_tree(root)
    try: manifest = CP.load(root); actual = {path.relative_to(tree).as_posix() for path in PS.tree_files(tree)}
    except (CP.PairError, PS.StoreError, OSError) as exc: raise CommissionSetError(str(exc)) from exc
    declared = {item["path"] for item in CP._members(manifest)}; missing = declared - actual
    if actual | missing != declared or not missing <= set(_commission_paths(manifest).values()): raise CommissionSetError("candidate partial commission layout is invalid")
    return manifest if missing else _ready_manifest(root)[0]
def _selection(manifest): return [f"C-{number:02}" for number in manifest["run"]["chapters"]]
def _commission_paths(manifest):
    book = manifest["run"]["book"]
    return {chapter: f"{book}/commissions/chapter-{int(chapter[2:]):02}.md"
            for chapter in _selection(manifest)}
def _section(text, prefix, number):
    match = re.search(CARD.format(prefix=prefix, number=number), text, re.M)
    if not match:
        raise CommissionSetError(f"accepted {prefix} card is missing for chapter {number:02}")
    following = NEXT_CARD.search(text, match.end())
    return text[match.start():following.start() if following else len(text)].strip()
def _member_text(root, manifest, relative, group="product"):
    path = CP.candidate_tree(root) / relative
    try:
        return CP.require_member(root, path, group, manifest).read_text(encoding="utf-8")
    except (CP.PairError, OSError, UnicodeError) as exc:
        raise CommissionSetError(str(exc)) from exc
def _packet_has(text, locator):
    match = LOCATOR.fullmatch(locator)
    if not match:
        return False
    source, item = match.groups()
    source_ok = re.search(rf"^(?:#\s+{source}\b|- \*\*Source ID:\*\*\s+{source}\b)",
                          text, re.M)
    return bool(source_ok and re.search(rf"^###\s+{item}\b", text, re.M))
def _assignment_inputs(root, manifest, assignments):
    assignments = _canonical(assignments)
    selected = _selection(manifest)
    if not isinstance(assignments, dict) or set(assignments) != set(selected):
        raise CommissionSetError("assignments must name every and only selected chapter")
    book = manifest["run"]["book"]
    prefix = Path(book) / "research/sources"
    packets_by_chapter, evidence = {}, {}
    for chapter in selected:
        record = assignments[chapter]
        if not isinstance(record, dict) or set(record) != {"packets", "authority"}:
            raise CommissionSetError(f"{chapter}: assignment shape is invalid")
        packets, authority = record["packets"], record["authority"]
        if not isinstance(packets, list) or len(packets) != len(set(packets)) \
                or not all(isinstance(path, str) for path in packets):
            raise CommissionSetError(f"{chapter}: packet assignment is invalid")
        if not isinstance(authority, dict) or authority.get("target") != chapter:
            raise CommissionSetError(f"{chapter}: authority targets another chapter")
        if not packets and not authority.get("blocker"):
            raise CommissionSetError(f"{chapter}: grounded commission has no assigned packet")
        chapter_packets = {}
        for relative in packets:
            path = Path(relative)
            if path.parent != prefix or path.suffix != ".md" or path.name == "README.md":
                raise CommissionSetError(f"{chapter}: packet path is outside its accepted source bank")
            text = _member_text(root, manifest, relative)
            chapter_packets[relative] = text
            evidence[relative] = text
        for locator in authority.get("assigned_evidence", {}):
            if not any(_packet_has(text, locator) for text in chapter_packets.values()):
                raise CommissionSetError(f"{chapter}: assigned evidence is absent: {locator}")
        packets_by_chapter[chapter] = chapter_packets
    return assignments, packets_by_chapter, dict(sorted(evidence.items()))
def _inputs(root, manifest, assignments):
    book = manifest["run"]["book"]
    try:
        SC.require_subject_contract(CP.candidate_tree(root) / book, "commissioning")
    except (SC.ContractError, OSError) as exc:
        raise CommissionSetError(f"accepted commissioning inputs are not fit: {exc}") from exc
    plan = _member_text(root, manifest, f"{book}/master-plan.md")
    review = _member_text(root, manifest, f"{book}/master-plan-review.md")
    framing = _member_text(root, manifest, f"{book}/framing.md")
    commissioner = _member_text(root, manifest, "prompts/chapter-commissioner.md", "config")
    auditor = _member_text(root, manifest, "prompts/commission-set-auditor.md", "config")
    normalized, packets, evidence = _assignment_inputs(root, manifest, assignments)
    cards = {chapter: {
        "plan": _section(plan, "C", int(chapter[2:])),
        "state": _section(framing, "CH", int(chapter[2:])),
    } for chapter in _selection(manifest)}
    return {"plan": plan, "review": review, "framing": framing,
            "commissioner": commissioner, "auditor": auditor,
            "assignments": normalized, "packets": packets,
            "evidence": evidence, "cards": cards}
def _declare_outputs(root, manifest):
    if manifest["state"] != "CANDIDATE":
        raise CommissionSetError("commissions require a mutable CANDIDATE operation")
    expected = set(_commission_paths(manifest).values())
    existing = {item["path"] for item in manifest["entries"] + manifest["outputs"]}; additions = expected - existing
    tree = CP.candidate_tree(root)
    for relative in additions:
        if os.path.lexists(tree / relative):
            raise CommissionSetError(f"undeclared commission output already exists: {relative}")
    updated = dict(manifest)
    updated["outputs"] = [*manifest["outputs"], *({"group": "product", "path": path} for path in sorted(additions))]
    try:
        PS.exact_layout(root, manifest, {".pair.json.rf02-tmp": PS.json_bytes(updated)})
        PS.write_json(CP._manifest_path(root), updated)
        return CP.load(root)
    except (PS.StoreError, CP.PairError, OSError) as exc:
        raise CommissionSetError(str(exc)) from exc
def _write_commission(root, manifest, relative, text):
    tree, path, data = CP.candidate_tree(root), CP.candidate_tree(root) / relative, (text.rstrip() + "\n").encode("utf-8")
    parent = path.parent
    try:
        if os.path.lexists(parent):
            PS.safe_dir(parent, tree)
        else:
            PS.safe_dir(parent.parent, tree)
            parent.mkdir()
        if os.path.lexists(path):
            if PS._safe_file(path, tree).read_bytes() != data: raise CommissionSetError(f"durable commission output differs: {relative}")
            return
        PS.write(path, data)
    except (PS.StoreError, OSError) as exc:
        raise CommissionSetError(str(exc)) from exc
def _operation(manifest):
    return {"schema": manifest["schema"], "accepted_generation": manifest["accepted_generation"],
            "accepted_pair_hash": manifest["accepted_pair_hash"], "run": manifest["run"],
            "accepted_evaluation_hash": manifest["accepted_evaluation_hash"],
            "commission_paths": _commission_paths(manifest)}
def _bindings(manifest, inputs, commissions):
    return {
        "candidate_pair_sha256": inputs["pair_hash"],
        "operation_sha256": PS.state_hash(_operation(manifest)),
        "plan_sha256": _sha_text(inputs["plan"]),
        "review_sha256": _sha_text(inputs["review"]),
        "framing_sha256": _sha_text(inputs["framing"]),
        "selection_sha256": PS.state_hash(_selection(manifest)),
        "assignment_sha256": PS.state_hash(inputs["assignments"]),
        "evidence": {path: _sha_text(text) for path, text in inputs["evidence"].items()},
        "commissions": {chapter: _sha_text(text) for chapter, text in commissions.items()},
        "commissioner_prompt_sha256": _sha_text(inputs["commissioner"]),
        "auditor_prompt_sha256": _sha_text(inputs["auditor"]),
    }
def _receipt_path(root):
    return CP.evidence_tree(root) / RECEIPT
def _write_receipt(root, value):
    evidence = CP.evidence_tree(root)
    try:
        if os.path.lexists(evidence):
            PS.safe_dir(evidence, root)
        else:
            PS.safe_dir(root)
            evidence.mkdir()
        temp = _receipt_path(root).with_name(f".{RECEIPT}.rf02-tmp")
        if os.path.lexists(temp):
            raise CommissionSetError("commission audit receipt staging file already exists")
        PS.write_json(_receipt_path(root), value)
    except (PS.StoreError, OSError) as exc:
        raise CommissionSetError(str(exc)) from exc
def _validated_commissions(root, manifest, inputs):
    commissions = {}
    for chapter, relative in _commission_paths(manifest).items():
        text = _member_text(root, manifest, relative).strip()
        try:
            status = CC.validate_text(text, inputs["assignments"][chapter]["authority"])
        except CC.ContractError as exc:
            raise CommissionSetError(f"{chapter}: invalid commission: {exc}") from exc
        if status != "commission":
            raise CommissionSetError(f"{chapter}: COMMISSION BLOCKED")
        commissions[chapter] = text
    return commissions
def require_writer_eligible(root, recover=True):
    """Fail closed unless the current complete set matches its fresh audit receipt."""
    manifest, _ = _ready_manifest(root, recover)
    try:
        raw = PS._safe_file(_receipt_path(root), Path(root).absolute()).read_text(encoding="utf-8")
        receipt = json.loads(raw)
    except (CP.PairError, PS.StoreError, OSError, json.JSONDecodeError) as exc:
        raise CommissionSetError(f"commission audit receipt is missing or invalid: {exc}") from exc
    if receipt.get("schema") != 1 or receipt.get("state") != "PASSED" \
            or receipt.get("audit", {}).get("result") != AUDIT_PASS:
        raise CommissionSetError("commission set has no passing whole-set audit")
    if receipt["audit"].get("sha256") != _sha_text(AUDIT_PASS):
        raise CommissionSetError("commission audit verdict hash mismatch")
    recorded = dict(receipt)
    receipt_hash = recorded.pop("receipt_hash", None)
    if receipt_hash != PS.state_hash(recorded):
        raise CommissionSetError("commission audit receipt hash mismatch")
    inputs = _inputs(root, manifest, receipt.get("assignments"))
    commissions = _validated_commissions(root, manifest, inputs)
    _, inputs["pair_hash"] = _ready_manifest(root, recover)
    if receipt.get("operation") != _operation(manifest) \
            or receipt.get("bindings") != _bindings(manifest, inputs, commissions):
            raise CommissionSetError("commission audit receipt is stale or hash-mismatched")
    return receipt_hash
def inspect_writer_eligible(root): return require_writer_eligible(root, False)
def generate(root, assignments, commissioner_runner, audit_runner):
    manifest = _generation_manifest(root)
    if os.path.lexists(_receipt_path(root)):
        raise CommissionSetError("commission audit receipt already exists")
    inputs = _inputs(root, manifest, assignments)
    manifest = _declare_outputs(root, manifest)
    for chapter in _selection(manifest):
        request = {"role": "fresh high-reasoning commissioning editor",
                   "fresh_context": True, "reasoning": "high", "reference_blind": True,
                   "prompt": inputs["commissioner"], "target": chapter,
                   "accepted_plan": inputs["plan"], "target_card": inputs["cards"][chapter]["plan"],
                   "state_card": inputs["cards"][chapter]["state"],
                   "assigned_packets": inputs["packets"][chapter]}
        text = commissioner_runner(request)
        if not isinstance(text, str):
            raise CommissionSetError(f"{chapter}: commissioner returned no text")
        try:
            status = CC.validate_text(text, inputs["assignments"][chapter]["authority"])
        except CC.ContractError as exc:
            raise CommissionSetError(f"{chapter}: invalid commission: {exc}") from exc
        _write_commission(root, manifest, _commission_paths(manifest)[chapter], text)
        if status != "commission":
            raise CommissionSetError(f"{chapter}: COMMISSION BLOCKED")
    commissions = _validated_commissions(root, manifest, inputs)
    _, inputs["pair_hash"] = _ready_manifest(root)
    audit_request = {"role": "fresh high-reasoning commission-set auditor",
                     "fresh_context": True, "reasoning": "high", "reference_blind": True,
                     "prompt": inputs["auditor"], "selection": _selection(manifest),
                     "commissions": commissions, "accepted_cards": inputs["cards"],
                     "assignments": inputs["assignments"], "assigned_evidence": inputs["evidence"]}
    audit = audit_runner(audit_request)
    if not isinstance(audit, str):
        raise CommissionSetError("whole-set auditor returned no text")
    audit = audit.strip()
    state = "PASSED" if audit == AUDIT_PASS else "BLOCKED" if AUDIT_BLOCKED.fullmatch(audit) else None
    if state is None:
        raise CommissionSetError("whole-set audit returned an invalid verdict")
    receipt = {"schema": 1, "state": state, "operation": _operation(manifest),
               "assignments": inputs["assignments"],
               "bindings": _bindings(manifest, inputs, commissions),
               "audit": {"result": audit, "sha256": _sha_text(audit)}}
    receipt["receipt_hash"] = PS.state_hash(receipt)
    _write_receipt(root, receipt)
    if state != "PASSED":
        raise CommissionSetError("whole-set commission audit blocked")
    return require_writer_eligible(root)
