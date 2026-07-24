"""Generate and gate one selected commission set inside an RF-02 candidate."""
import json, os, re, sys
from pathlib import Path
HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))
import validate_commission_contract as CC  # noqa: E402
import validate_research_contract as RC  # noqa: E402
import validate_subject_contract as SC  # noqa: E402
import validate_master_plan_review as MPR  # noqa: E402
import candidate_pair as CP  # noqa: E402
import pair_store as PS  # noqa: E402
RECEIPT = "commission-set-audit.json"
AUDIT_PASS = "COMMISSION SET PASS"
AUDIT_BLOCKED = re.compile(r"COMMISSION SET BLOCKED\nOwner: (?:brief|research/synthesis|framing|plan|commission/context|prose|revision|evaluation)\nGap: .+", re.S)
CARD = r"^###\s+{prefix}-0*{number}\b[^\n]*$"
NEXT_CARD = re.compile(r"^###\s+(?:C|CH)-\d+\b", re.M)
LOCATOR = re.compile(r"^(S-\d{3})#(E-\d{3})$")
PLAN_FIELD = re.compile(r"^- \*\*([^*:\n]+):\*\*\s*(.*?)\s*$", re.M)
UNIT_ID = re.compile(r"\b(?:LEU|SEU)-\d{3}\b")
EVIDENCE_ID = re.compile(r"\bE-\d+\b")
class CommissionSetError(RuntimeError): pass
class ResearchDispatchGap(CommissionSetError):
    def __init__(self, chapter, code, gap):
        self.chapter, self.code, self.gap = chapter, code, gap
        super().__init__(f"RESEARCH GAP\nOwner: research/synthesis\nChapter: {chapter}\n"
                         f"Code: {code}\nGap: {gap}")
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


def _evidence_ledger(plan):
    match = re.search(r"(?ms)^## Evidence ledger\s*$\n(.*?)(?=^## |\Z)", plan)
    if not match:
        raise CommissionSetError("accepted plan has no canonical evidence ledger")
    lines = match.group(1).splitlines()
    required = {"ID", "Research unit IDs", "Source ID", "Permitted inference",
                "Prohibited inference"}
    for index, line in enumerate(lines):
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and required <= set(cells):
            headings, rows = cells, {}
            for row in lines[index + 2:]:
                if not row.lstrip().startswith("|"):
                    break
                values = [cell.strip() for cell in row.strip().strip("|").split("|")]
                if len(values) != len(headings):
                    raise CommissionSetError("accepted evidence ledger row shape is invalid")
                record = dict(zip(headings, values))
                evidence_id = record.get("ID")
                if evidence_id in rows or not evidence_id or EVIDENCE_ID.fullmatch(evidence_id) is None:
                    raise CommissionSetError("accepted evidence ledger ID is invalid or duplicated")
                rows[evidence_id] = record
            return rows
    raise CommissionSetError("accepted evidence ledger lacks research-unit authority columns")


def _chapter_fields(card, chapter):
    fields = dict(PLAN_FIELD.findall(card))
    for name in ("Evidence IDs and required limits", "Guardrails"):
        if not fields.get(name):
            raise ResearchDispatchGap(chapter, "plan_need_missing",
                                      f"accepted card lacks {name}")
    return fields


def _locators(value):
    return sorted(set(re.findall(r"S-\d{3}#E-\d{3}", value)))


def _expected_research_binding(report, plan, card, chapter):
    """Derive chapter authority only from the sealed inventory and accepted card."""
    seal = report["seal_identity"]
    inventory = report.get("inventory", {}) if isinstance(report, dict) else {}
    units = inventory.get("units", {}) if isinstance(inventory, dict) else {}
    if not isinstance(units, dict) or not units or not isinstance(seal, str):
        raise ResearchDispatchGap(chapter, "research_inventory_invalid",
                                  "sealed intervention-unit inventory is inconsistent")
    accepted_units = set(units)
    fields, ledger = _chapter_fields(card, chapter), _evidence_ledger(plan)
    evidence_text = fields["Evidence IDs and required limits"]
    evidence_ids = sorted(set(EVIDENCE_ID.findall(evidence_text)))
    if not evidence_ids and not evidence_text.casefold().startswith("none"):
        raise ResearchDispatchGap(chapter, "plan_need_invalid",
                                  "card names no resolvable evidence-ledger ID")
    needs = {}
    for evidence_id in evidence_ids:
        row = ledger.get(evidence_id)
        if row is None:
            raise ResearchDispatchGap(chapter, "plan_need_invalid",
                                      f"card evidence ID is absent from ledger: {evidence_id}")
        unit_ids = sorted(set(UNIT_ID.findall(row["Research unit IDs"])))
        if not unit_ids:
            raise ResearchDispatchGap(chapter, "plan_need_invalid",
                                      f"ledger row has no accepted research unit: {evidence_id}")
        missing = set(unit_ids) - accepted_units
        if missing:
            raise ResearchDispatchGap(chapter, "unit_missing",
                                      f"{evidence_id} names absent unit {sorted(missing)[0]}")
        required_limits, safety, locators = set(), set(), set()
        permitted_values, prohibited_values = set(), set()
        for unit_id in unit_ids:
            unit = units[unit_id]
            if not isinstance(unit, dict):
                raise ResearchDispatchGap(chapter, "unit_invalid", f"{unit_id} is malformed")
            try:
                permitted = unit["permitted_inference"]
                prohibited = unit["prohibited_inference"]
                boundary = unit["safety"]
                unit_locators = sorted(unit["locators"])
            except (KeyError, TypeError) as exc:
                raise ResearchDispatchGap(chapter, "unit_invalid",
                                          f"{unit_id} lacks inference or safety authority") from exc
            if not all(isinstance(item, str) and item for item in
                       (permitted, prohibited, boundary)) \
                    or not unit_locators or len(unit_locators) != len(set(unit_locators)) \
                    or any(not isinstance(item, str) or LOCATOR.fullmatch(item) is None
                           for item in unit_locators):
                raise ResearchDispatchGap(chapter, "inference_mismatch",
                                          f"{evidence_id} widens {unit_id}")
            permitted_values.add(permitted)
            prohibited_values.add(prohibited)
            required_limits.update((f"Permitted inference: {permitted}",
                                    f"Prohibited inference: {prohibited}"))
            locators.update(unit_locators)
            if boundary.strip().casefold() not in {"n/a", "none"}:
                safety.add(boundary)
        if row["Permitted inference"] != "; ".join(sorted(permitted_values)) \
                or row["Prohibited inference"] != "; ".join(sorted(prohibited_values)):
            raise ResearchDispatchGap(chapter, "inference_mismatch",
                                      f"{evidence_id} differs from sealed inference bounds")
        if sorted(locators) != _locators(row["Source ID"]):
            raise ResearchDispatchGap(chapter, "locator_mismatch",
                                      f"{evidence_id} locator differs from its sealed units")
        if any(item not in fields["Guardrails"] for item in safety):
            raise ResearchDispatchGap(chapter, "safety_mismatch",
                                      f"{evidence_id} does not preserve a unit safety boundary")
        needs[evidence_id] = {"unit_ids": unit_ids, "locators": sorted(locators),
                              "required_limits": sorted(required_limits),
                              "safety": sorted(safety)}
    expected = {"seal_sha256": seal, "needs": needs}
    return expected


def _research_binding(report, plan, card, chapter, authority, packets):
    expected = _expected_research_binding(report, plan, card, chapter)
    if authority.get("research") != expected:
        raise ResearchDispatchGap(chapter, "binding_stale",
                                  "chapter research binding does not match its current seal and card")
    assigned = set(authority.get("assigned_evidence", {}))
    required_locators = {locator for need in expected["needs"].values()
                         for locator in need["locators"]}
    if assigned != required_locators:
        raise ResearchDispatchGap(chapter, "assignment_mismatch",
                                  "assigned evidence differs from plan-owned research needs")
    if any(not any(_packet_has(text, locator) for text in packets.values())
           for locator in required_locators):
        raise ResearchDispatchGap(chapter, "packet_missing",
                                  "an assigned research locator is absent from accepted packets")
    return expected


def bind_research_authority(root, assignments):
    """Attach plan-owned sealed research bindings to upstream planner assignments."""
    manifest = CP.load(root)
    book = manifest["run"]["book"]
    plan = _member_text(root, manifest, f"{book}/master-plan.md")
    report = RC.inspect_research(CP.candidate_tree(root) / book, require_seal=True)
    if not report.get("ok"):
        raise CommissionSetError("current sealed research is required")
    normalized = _canonical(assignments)
    for chapter in _selection(manifest):
        record = normalized.get(chapter)
        if not isinstance(record, dict) or not isinstance(record.get("authority"), dict):
            raise CommissionSetError(f"{chapter}: assignment shape is invalid")
        card = _section(plan, "C", int(chapter[2:]))
        authority = dict(record["authority"])
        authority["research"] = _expected_research_binding(
            report, plan, card, chapter)
        record["authority"] = authority
    return normalized


def _assignment_inputs(root, manifest, assignments, plan, cards):
    assignments = _canonical(assignments)
    selected = _selection(manifest)
    if not isinstance(assignments, dict) or set(assignments) != set(selected):
        raise CommissionSetError("assignments must name every and only selected chapter")
    book = manifest["run"]["book"]
    book_path = CP.candidate_tree(root) / book
    try:
        report = RC.inspect_research(book_path, require_seal=True)
    except (RC.ContractError, OSError, TypeError, KeyError) as exc:
        raise ResearchDispatchGap(selected[0], "research_seal_invalid", str(exc)) from exc
    if not isinstance(report, dict) or not report.get("ok") or not report.get("seal_identity"):
        gap = "; ".join(report.get("blockers", ())) if isinstance(report, dict) else "invalid report"
        raise ResearchDispatchGap(selected[0], "research_seal_invalid", gap)
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
        _research_binding(report, plan, cards[chapter]["plan"], chapter,
                          authority, chapter_packets)
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
    cards = {chapter: {
        "plan": _section(plan, "C", int(chapter[2:])),
        "state": _section(framing, "CH", int(chapter[2:])),
    } for chapter in _selection(manifest)}
    normalized, packets, evidence = _assignment_inputs(
        root, manifest, assignments, plan, cards)
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
        "research_seals": {chapter: record["authority"]["research"]["seal_sha256"]
                           for chapter, record in inputs["assignments"].items()},
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


def require_chapter_research(root, number, captured_receipt=None):
    """Recheck one chapter's current sealed authority immediately before dispatch."""
    chapter = f"C-{number:02d}"
    try:
        receipt_file = PS._safe_file(_receipt_path(root), Path(root).absolute())
        receipt_bytes = receipt_file.read_bytes()
        if captured_receipt is None:
            require_writer_eligible(root)
        elif not isinstance(captured_receipt, bytes) or receipt_bytes != captured_receipt:
            raise CommissionSetError(
                "commission audit receipt changed after writer-authority capture")
        receipt = json.loads(receipt_bytes)
        recorded = dict(receipt)
        receipt_hash = recorded.pop("receipt_hash", None)
        if receipt_hash != PS.state_hash(recorded) or receipt.get("state") != "PASSED" \
                or receipt.get("audit", {}).get("result") != AUDIT_PASS:
            raise CommissionSetError("commission audit receipt is missing or invalid")
        manifest, _ = _ready_manifest(root)
        if chapter not in _selection(manifest):
            raise ResearchDispatchGap(chapter, "chapter_unassigned",
                                      "chapter is outside the audited commission set")
        plan = _member_text(root, manifest, f"{manifest['run']['book']}/master-plan.md")
        record = receipt["assignments"][chapter]
        authority, packets = record["authority"], {}
        prefix = Path(manifest["run"]["book"]) / "research/sources"
        for relative in record["packets"]:
            path = Path(relative)
            if path.parent != prefix or path.suffix != ".md" or path.name == "README.md":
                raise CommissionSetError(f"{chapter}: packet path is outside its accepted source bank")
            packets[relative] = _member_text(root, manifest, relative)
        book = CP.candidate_tree(root) / manifest["run"]["book"]
        report = RC.inspect_research(book, require_seal=True)
        if not report.get("ok") or not report.get("seal_identity"):
            raise ResearchDispatchGap(chapter, "research_seal_invalid",
                                      "; ".join(report.get("blockers", ())))
        binding = _research_binding(report, plan, _section(plan, "C", number),
                                    chapter, authority, packets)
        if receipt.get("bindings", {}).get("research_seals", {}).get(chapter) \
                != binding["seal_sha256"]:
            raise ResearchDispatchGap(chapter, "binding_stale",
                                      "commission receipt binds another research seal")
        return binding, packets
    except ResearchDispatchGap:
        raise
    except (CommissionSetError, CP.PairError, PS.StoreError, OSError,
            json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ResearchDispatchGap(chapter, "authority_invalid", str(exc)) from exc


def chapter_gap_request(root, number):
    """Return a reviewed-plan gap before commissions; never bless stale audit state."""
    chapter = f"C-{number:02d}"
    manifest, _ = _ready_manifest(root)
    if chapter not in _selection(manifest):
        raise CommissionSetError(f"{chapter}: chapter is outside the selected commission set")
    if os.path.lexists(_receipt_path(root)):
        try:
            require_writer_eligible(root)
        except CommissionSetError as exc:
            raise CommissionSetError(
                f"{chapter}: stale/invalid commission audit requires its owning stage") from exc
        raise CommissionSetError(f"{chapter}: research is adequate; no gap request exists")
    book = manifest["run"]["book"]
    plan_relative = f"{book}/master-plan.md"
    plan = _member_text(root, manifest, plan_relative)
    card = _section(plan, "C", number)
    tree = CP.candidate_tree(root)
    try:
        MPR.require_master_plan_review(tree / book, tree / plan_relative,
                                       tree / f"{book}/framing.md")
    except (MPR.ContractError, OSError, UnicodeError) as exc:
        raise CommissionSetError(
            f"{chapter}: plan is not independently accepted for research gap-fill: {exc}") from exc
    report = RC.inspect_research(CP.candidate_tree(root) / book, require_seal=True)
    if not report.get("ok") or not report.get("seal_identity"):
        raise CommissionSetError(f"{chapter}: no current sealed corpus can receive gap-fill")
    try:
        _expected_research_binding(report, plan, card, chapter)
    except ResearchDispatchGap as gap:
        proven = gap
    else:
        raise CommissionSetError(f"{chapter}: research is adequate; no gap request exists")
    details = {
        "unit_missing": ("Accepted chapter need names an intervention-ready unit "
                         "absent from the current sealed corpus."),
    }
    detail = details.get(proven.code)
    if detail is None:
        raise CommissionSetError(
            f"{chapter}: {proven.code} requires its owning stage, not targeted research")
    book_path = CP.candidate_tree(root) / book
    seal = RC.research_seal_identity(book_path)
    if seal != report["seal_identity"]:
        raise CommissionSetError(f"{chapter}: research seal identity changed during gap proof")
    return {"schema": 1, "research_seal_sha256": seal,
            "chapter_id": chapter,
            "plan": {"path": plan_relative, "sha256": _sha_text(plan)},
            "card": {"path": f"{plan_relative}#{chapter}", "sha256": _sha_text(card)},
            "gaps": [{"code": proven.code, "detail": detail}]}


def rebind_research(root, assignments):
    """Rebind only unchanged semantic needs after full current-seal validation."""
    manifest, _ = _ready_manifest(root)
    try:
        old = json.loads(PS._safe_file(
            _receipt_path(root), Path(root).absolute()).read_text(encoding="utf-8"))
        recorded = dict(old)
        receipt_hash = recorded.pop("receipt_hash", None)
        if receipt_hash != PS.state_hash(recorded) or old.get("state") != "PASSED" \
                or old.get("audit", {}).get("result") != AUDIT_PASS:
            raise CommissionSetError("commission audit receipt cannot be rebound")
        previous, proposed = old.get("assignments"), _canonical(assignments)
        for chapter in _selection(manifest):
            before = previous[chapter]["authority"]["research"]
            after = proposed[chapter]["authority"]["research"]
            before_assignment = _canonical(previous[chapter])
            after_assignment = _canonical(proposed[chapter])
            before_assignment["authority"]["research"].pop("seal_sha256", None)
            after_assignment["authority"]["research"].pop("seal_sha256", None)
            if before.get("needs") != after.get("needs") \
                    or before_assignment != after_assignment:
                raise ResearchDispatchGap(chapter, "semantic_rebind_forbidden",
                                          "changed research needs require downstream regeneration")
        inputs = _inputs(root, manifest, proposed)
        commissions = _validated_commissions(root, manifest, inputs)
        _, inputs["pair_hash"] = _ready_manifest(root)
        receipt = {"schema": 1, "state": "PASSED", "operation": _operation(manifest),
                   "assignments": inputs["assignments"],
                   "bindings": _bindings(manifest, inputs, commissions),
                   "audit": old["audit"]}
        receipt["receipt_hash"] = PS.state_hash(receipt)
        PS.write_json(_receipt_path(root), receipt)
        return require_writer_eligible(root)
    except ResearchDispatchGap:
        raise
    except (CommissionSetError, CP.PairError, PS.StoreError, OSError,
            json.JSONDecodeError, KeyError, TypeError) as exc:
        raise CommissionSetError(f"deterministic research rebind blocked: {exc}") from exc
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
