"""Exact full-context writer authority for the H-F01 control arm only."""
import json
import os
import re
from pathlib import Path

import candidate_pair as CP
import grounded_evidence as GE
import pair_store as PS
import writer_operation as WO

AUTHORITY = "hf01-control"
STYLE = "prompts/style-guide.md"
FIELD = re.compile(r"^- \*\*(.+?):\*\*\s*(.*)$", re.M)
CHAPTER = re.compile(r"^###\s+(?:C|CH)-0*(\d+)\b[^\n]*$", re.M)
LOCATOR = re.compile(r"S-\d{3}#E-\d{3}")
EVIDENCE_ID = re.compile(r"EV-[A-Z]\d{2}")


class ControlAuthorityError(RuntimeError):
    pass
def assignment(manifest):
    keys = ("schema", "accepted_generation", "accepted_pair_hash",
            "accepted_evaluation_hash", "entries", "outputs", "evaluation", "run")
    return {key: manifest[key] for key in keys}


def _draft_paths(manifest):
    book = manifest["run"]["book"]
    return [f"{book}/chapters/chapter-{number:02d}.md"
            for number in manifest["run"]["chapters"]]
def _section(plan, number):
    matches = [match for match in CHAPTER.finditer(plan) if int(match.group(1)) == number]
    if len(matches) != 1:
        raise ControlAuthorityError(f"chapter {number}: current plan section is missing or ambiguous")
    following = CHAPTER.search(plan, matches[0].end())
    return plan[matches[0].start():following.start() if following else len(plan)].strip()


def _field(section, name):
    matches = [value.strip() for field, value in FIELD.findall(section) if field == name]
    if len(matches) != 1 or not matches[0]:
        raise ControlAuthorityError(f"current plan field is missing or ambiguous: {name}")
    return matches[0]
def _row(plan, evidence_id):
    matches = []
    for line in plan.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 5 and cells[0] == evidence_id:
            matches.append(cells)
    if len(matches) != 1:
        raise ControlAuthorityError(f"plan evidence row is missing or ambiguous: {evidence_id}")
    _, finding, sources, permitted, prohibited = matches[0]
    locators = LOCATOR.findall(sources)
    if not locators or len(locators) != len(set(locators)):
        raise ControlAuthorityError(f"plan evidence locators are invalid: {evidence_id}")
    return {"id": evidence_id, "finding": finding, "locators": locators,
            "permitted_inference": permitted, "prohibited_inference": prohibited}


def _packet(manifest, locator):
    source = locator.split("#", 1)[0].lower()
    folder = Path(manifest["run"]["book"]) / "research/sources"
    matches = [item["path"] for item in CP._members(manifest)
               if item.get("group") == "product" and Path(item["path"]).parent == folder
               and Path(item["path"]).name.startswith(source + "-")]
    if len(matches) != 1:
        raise ControlAuthorityError(f"candidate source packet is missing or ambiguous: {source}")
    return matches[0]
def _continuity(value, number):
    match = re.fullmatch(
        r"receives\s+(.+?);\s+hands\s+(?:C|CH)-\d+\s+(.+?)(?:\.\s*)?", value)
    if not match:
        raise ControlAuthorityError(f"chapter {number}: plan continuity is malformed")
    entering, leaving = (item.strip() for item in match.groups())
    return {"entering_state": f"RS-{number - 1:02d} | {entering}",
            "leaving_state": f"RS-{number:02d} | {leaving}", "continuity": value}


def _control_review(candidate, manifest, files):
    tree = CP.candidate_tree(candidate)
    book, selected = manifest["run"]["book"], manifest["run"]["chapters"]
    plan_path, brief_path = f"{book}/master-plan.md", f"{book}/00-brief.md"
    plan = files[plan_path].decode("utf-8")
    records = []
    for number in selected:
        section = _section(plan, number)
        fields = {name: _field(section, name)
                  for name in ("Belief job", "Evidence", "Guardrails", "Continuity")}
        transition = _continuity(fields["Continuity"], number)
        rows = [_row(plan, item) for item in EVIDENCE_ID.findall(fields["Evidence"])]
        assigned, packets = {}, set()
        for row in rows:
            bounds = {key: row[key] for key in
                      ("id", "finding", "permitted_inference", "prohibited_inference")}
            for locator in row["locators"]:
                path = _packet(manifest, locator)
                packets.add(path)
                assigned.setdefault(locator, {"plan_entries": [],
                    "chapter_guardrails": fields["Guardrails"]})["plan_entries"].append(bounds)
                if path not in files:
                    files[path] = CP.require_member(
                        candidate, tree / path, "product", manifest).read_bytes()
        chapter_id = f"C-{number:02d}"
        card = (f"### {chapter_id} — H-F01 control review state\n"
                f"- **Entering belief:** {transition['entering_state']}\n"
                f"- **Leaving belief:** {transition['leaving_state']}")
        try:
            GE.assigned_records({path: files[path].decode("utf-8") for path in packets}, assigned)
        except (GE.EvidenceError, UnicodeError) as exc:
            raise ControlAuthorityError(
                f"chapter {number}: control source authority is invalid: {exc}") from exc
        records.append({"chapter": number, "plan_context": {
            "path": plan_path, "sha256": PS.sha(section.encode()), "text": section},
            "reader_state_card": card, "declared_transition": transition,
            "assignment": {"packets": sorted(packets), "authority": {
                "target": chapter_id, "basis": "H-F01 control current-plan authority",
                "belief_job": fields["Belief job"], "safety_limits": fields["Guardrails"],
                "subject_contract": {"path": brief_path,
                    "sha256": PS.sha(files[brief_path])}, "assigned_evidence": assigned}}})
    return records
def capture(candidate, book, selected):
    root, manifest = Path(candidate).absolute(), CP.load(candidate)
    tree, run = CP.candidate_tree(candidate), manifest["run"]
    if manifest["state"] != "CANDIDATE" or Path(book).absolute() != tree / run["book"] \
            or list(selected) != run["chapters"]:
        raise ControlAuthorityError("H-F01 control target differs from its candidate assignment")
    plan, brief = f"{run['book']}/master-plan.md", f"{run['book']}/00-brief.md"
    try:
        files = {path: CP.require_member(candidate, tree / path, manifest=manifest).read_bytes()
                 for path in (STYLE, plan, brief)}
        review = _control_review(candidate, manifest, files)
        inventory = PS.exact_tree(tree, CP._members(manifest))
    except (CP.PairError, PS.StoreError, OSError) as exc:
        raise ControlAuthorityError(f"H-F01 control authority capture failed: {exc}") from exc
    return {"manifest": manifest, "files": files, "pair_inventory": inventory,
            "control_review": review}


def _body(candidate, captured):
    root, manifest = Path(candidate).absolute(), captured["manifest"]
    run, files = manifest["run"], captured["files"]
    plan = f"{run['book']}/master-plan.md"
    return {
        "schema": 1, "authority": AUTHORITY,
        "operation": {"root": str(root), "experiment_id": run["experiment_id"],
                      "iteration_id": run["iteration_id"],
                      "accepted_generation": manifest["accepted_generation"]},
        "book": run["book"], "chapters": run["chapters"],
        "manifest_assignment_sha256": PS.state_hash(assignment(manifest)),
        "pair_inventory": captured["pair_inventory"],
        "selected_draft_paths": _draft_paths(manifest),
        "full_style_guide": {"path": STYLE, "sha256": PS.sha(files[STYLE])},
        "full_master_plan": {"path": plan, "sha256": PS.sha(files[plan])},
        "subject_contract": {"path": f"{run['book']}/00-brief.md",
                             "sha256": PS.sha(files[f"{run['book']}/00-brief.md"])},
        "control_review": captured["control_review"],
        "source_packets": {path: PS.sha(files[path]) for path in sorted(files)
                           if "/research/sources/" in path},
    }


def persist(candidate, captured):
    root, path = Path(candidate).absolute(), Path(candidate).absolute() / WO.RECEIPT
    try:
        manifest = CP.load(candidate)
        if manifest["state"] not in ("CANDIDATE", "WRITER_HANDOFF") \
                or assignment(manifest) != assignment(captured["manifest"]):
            raise ControlAuthorityError("H-F01 control operation identity changed")
        current = PS.exact_tree(CP.candidate_tree(candidate), CP._members(manifest))
        if current != captured["pair_inventory"]:
            raise ControlAuthorityError("H-F01 control pair changed before handoff")
        evidence = CP.evidence_tree(candidate)
        if not os.path.lexists(evidence):
            evidence.mkdir(); PS.safe_dir(evidence, root); PS._sync(root)
        else:
            PS.safe_dir(evidence, root)
        body = _body(candidate, captured)
        body["receipt_hash"] = PS.state_hash(body)
        data = PS.json_bytes(body)
        operation = {"group": "operation", "path": WO.RECEIPT,
                     "sha256": PS.sha(data), "receipt_hash": body["receipt_hash"]}
        if manifest["state"] == "CANDIDATE":
            updated = {**manifest, "state": "WRITER_HANDOFF", "operation": operation}
            PS.exact_layout(root, manifest, {".pair.json.rf02-tmp": PS.json_bytes(updated)})
            PS.write_json(CP._manifest_path(root), updated)
        elif manifest.get("operation") != operation:
            raise ControlAuthorityError("H-F01 control receipt identity changed")
        if os.path.lexists(path):
            if PS._safe_file(path, root).read_bytes() != data:
                raise ControlAuthorityError("H-F01 control receipt already differs")
        else:
            PS.write(path, data)
        return body["receipt_hash"]
    except (CP.PairError, PS.StoreError, OSError) as exc:
        raise ControlAuthorityError(f"H-F01 control receipt failed: {exc}") from exc


def require_resume(candidate, book, selected, expected_hash):
    root, manifest = Path(candidate).absolute(), CP.load(candidate)
    tree, operation = CP.candidate_tree(candidate), manifest.get("operation")
    try:
        raw = WO.read(candidate, operation)
        receipt = json.loads(raw)
        value = dict(receipt)
        recorded = value.pop("receipt_hash")
        current = PS.exact_tree(tree, CP._members(manifest))
    except (WO.OperationError, CP.PairError, PS.StoreError, OSError,
            json.JSONDecodeError, TypeError, KeyError) as exc:
        raise ControlAuthorityError(f"H-F01 control resume authority failed: {exc}") from exc
    drafts = _draft_paths(manifest)
    expected = value.get("pair_inventory") or []
    stable = {item["path"]: item["sha256"] for item in expected
              if isinstance(item, dict) and item.get("path") not in drafts}
    current_stable = {item["path"]: item["sha256"] for item in current
                      if item["path"] not in drafts}
    run, plan = manifest["run"], f"{manifest['run']['book']}/master-plan.md"
    brief = f"{manifest['run']['book']}/00-brief.md"
    descriptors = (("full_style_guide", STYLE), ("full_master_plan", plan),
                   ("subject_contract", brief))
    identity = value.get("operation") == {
        "root": str(root), "experiment_id": run["experiment_id"],
        "iteration_id": run["iteration_id"],
        "accepted_generation": manifest["accepted_generation"]}
    if value.get("authority") != AUTHORITY or recorded != expected_hash \
            or operation.get("receipt_hash") != expected_hash or not identity \
            or Path(book).absolute() != tree / run["book"] \
            or list(selected) != run["chapters"] or value.get("book") != run["book"] \
            or value.get("chapters") != run["chapters"] \
            or value.get("manifest_assignment_sha256") != PS.state_hash(assignment(manifest)) \
            or value.get("selected_draft_paths") != drafts \
            or [(item.get("group"), item.get("path")) for item in expected] \
               != [(item["group"], item["path"]) for item in current] \
            or stable != current_stable or any(value.get(name) != {
                "path": path, "sha256": PS.sha(CP.require_member(
                    candidate, tree / path, manifest=manifest).read_bytes())}
                for name, path in descriptors):
        raise ControlAuthorityError("H-F01 control authority drifted after handoff")
    files = {path: CP.require_member(candidate, tree / path, manifest=manifest).read_bytes()
             for path in (STYLE, plan, brief)}
    review = _control_review(candidate, manifest, files)
    sources = {path: PS.sha(files[path]) for path in sorted(files)
               if "/research/sources/" in path}
    if value.get("control_review") != review or value.get("source_packets") != sources:
        raise ControlAuthorityError("H-F01 control review authority drifted after handoff")
    return receipt


def load(candidate):
    manifest = CP.load(candidate)
    try:
        value = json.loads(WO.read(candidate, manifest.get("operation")))
        expected = value["receipt_hash"]
    except (WO.OperationError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ControlAuthorityError(f"H-F01 control authority is invalid: {exc}") from exc
    return require_resume(candidate, CP.candidate_tree(candidate) / manifest["run"]["book"],
                          manifest["run"]["chapters"], expected)
