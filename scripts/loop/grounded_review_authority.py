"""Resolve exact RF-09/RF-11 authority into isolated RF-12 tasks."""
import json
from pathlib import Path

import candidate_pair as CP
import commission_set as CS
import draft_batch_state as DS
import first_draft_batch as FB
import grounded_evidence as GE
import grounded_review_contract as C
import hf01_control_authority as HCA
import loopcfg
import pair_store as PS
import writer_operation as WO


class AuthorityError(RuntimeError):
    pass


def _base(root, supplied_cfg):
    frozen = FB.require_frozen_batch(root)
    manifest, tree = CP.load(root), CP.candidate_tree(root)
    writer = json.loads(WO.read(root, manifest["operation"]))
    audit_path = CP.evidence_tree(root) / CS.RECEIPT
    audit_bytes = PS._safe_file(audit_path, root).read_bytes()
    audit = json.loads(audit_bytes)
    audit_body = {key: value for key, value in audit.items() if key != "receipt_hash"}
    wanted = {"path": f"evidence/{CS.RECEIPT}",
              "receipt_hash": audit.get("receipt_hash"), "sha256": PS.sha(audit_bytes)}
    if writer["audit"] != wanted or audit.get("receipt_hash") != PS.state_hash(audit_body) \
            or audit.get("state") != "PASSED":
        raise AuthorityError("RF-09 commission authority is stale or invalid")
    prompt_file = CP.require_member(root, tree / C.PROMPT, "config", manifest)
    prompt = prompt_file.read_text(encoding="utf-8")
    cfg_path = CP.require_member(root, tree / manifest["run"]["config"], "config", manifest)
    cfg, reviewer = loopcfg.load(cfg_path), None
    reviewer = C.model(cfg)
    if supplied_cfg is not None and C.model(supplied_cfg) != reviewer:
        raise AuthorityError("grounded reviewer runtime metadata differs from pinned config")
    config = {"path": manifest["run"]["config"], "sha256": PS.sha(cfg_path.read_bytes()),
              "values_sha256": PS.state_hash(cfg)}
    operation = {"id": PS.state_hash({"root": str(root), "run": manifest["run"],
                                       "batch": frozen["batch"]["operation"]}),
                 "batch_sha256": PS.state_hash(frozen["batch"]["operation"]),
                 "rf11_receipt_hash": frozen["receipt_hash"],
                 "rf09_receipt_hash": audit["receipt_hash"]}
    return frozen, manifest, tree, writer, audit, prompt, reviewer, config, operation


def _commission(root, number, base):
    _, manifest, tree, writer, audit, _, _, _, _ = base
    chapter = f"C-{number:02d}"
    commissions = {item["chapter"]: item for item in writer.get("commissions", [])}
    item = commissions.get(number)
    if not isinstance(item, dict):
        raise AuthorityError(f"chapter {number}: commission binding is missing")
    data = CP.require_member(root, tree / item["path"], "product", manifest).read_bytes()
    normalized = PS.sha(data.decode("utf-8").strip().encode("utf-8"))
    if PS.sha(data) != item.get("sha256") \
            or audit["bindings"]["commissions"].get(chapter) != normalized:
        raise AuthorityError(f"chapter {number}: commission hash is stale")
    return item, data


def _draft(root, number, frozen):
    drafts = {item["chapter"]: item for item in frozen["batch"]["drafts"]}
    path = DS.folder(root) / f"chapter-{number:02d}.md"
    data = PS._safe_file(path, DS.folder(root)).read_bytes()
    if number not in drafts or PS.sha(data) != drafts[number]["sha256"]:
        raise AuthorityError(f"chapter {number}: frozen snapshot hash is stale")
    return data


def _evidence(root, assignment, base):
    _, manifest, tree, _, audit, _, _, _, _ = base
    packets = {}
    for relative in assignment.get("packets", []):
        data = CP.require_member(root, tree / relative, "product", manifest).read_bytes()
        if audit["bindings"]["evidence"].get(relative) != PS.sha(data):
            raise AuthorityError(f"assigned packet hash is stale: {relative}")
        packets[relative] = data.decode("utf-8")
    assigned = assignment.get("authority", {}).get("assigned_evidence", {})
    if not isinstance(assigned, dict) or not assigned:
        raise AuthorityError("chapter assignment has no assigned evidence")
    try:
        return GE.assigned_records(packets, assigned)
    except GE.EvidenceError as exc:
        raise AuthorityError(str(exc)) from exc


def _task(root, number, base, assignment):
    frozen, manifest, _, _, _, prompt, reviewer, config, operation = base
    commission_meta, commission_data = _commission(root, number, base)
    draft_data = _draft(root, number, frozen)
    identity = {"operation": operation, "generation": manifest["accepted_generation"],
                "config": config, "selection": manifest["run"]["chapters"],
                "chapter": number}
    task = C.make_task(identity, reviewer, prompt, draft_data.decode("utf-8"),
                       commission_data.decode("utf-8"), assignment,
                       _evidence(root, assignment, base))
    task["context"]["commission_sha256"] = PS.sha(commission_data)
    task["context"]["commission_path"] = commission_meta["path"]
    body = {key: value for key, value in task.items() if key != "task_sha256"}
    task["task_sha256"] = PS.state_hash(body)
    return C.task(task)


def _control_load(root, supplied_cfg, frozen, manifest, tree, writer):
    authority = HCA.load(root)
    prompt_file = CP.require_member(root, tree / C.PROMPT, "config", manifest)
    prompt = prompt_file.read_text(encoding="utf-8")
    cfg_path = CP.require_member(root, tree / manifest["run"]["config"], "config", manifest)
    cfg, reviewer = loopcfg.load(cfg_path), None
    reviewer = C.model(cfg)
    if supplied_cfg is not None and C.model(supplied_cfg) != reviewer:
        raise AuthorityError("grounded reviewer runtime metadata differs from pinned config")
    config = {"path": manifest["run"]["config"], "sha256": PS.sha(cfg_path.read_bytes()),
              "values_sha256": PS.state_hash(cfg)}
    selection = manifest["run"]["chapters"]
    if selection != frozen["batch"]["selection"]:
        raise AuthorityError("RF-11 selection differs from the control operation selection")
    records = {item["chapter"]: item for item in authority.get("control_review", [])}
    if set(records) != set(selection):
        raise AuthorityError("H-F01 control review authority is partial or ambiguous")
    operation = {"id": PS.state_hash({"root": str(root), "run": manifest["run"],
        "batch": frozen["batch"]["operation"], "control": writer["receipt_hash"]}),
        "batch_sha256": PS.state_hash(frozen["batch"]["operation"]),
        "rf11_receipt_hash": frozen["receipt_hash"],
        "control_authority_receipt_hash": writer["receipt_hash"]}
    tasks = {}
    for number in selection:
        record, assignment = records[number], records[number]["assignment"]
        packets = {path: CP.require_member(root, tree / path, "product", manifest
            ).read_text(encoding="utf-8") for path in assignment["packets"]}
        try:
            evidence = GE.assigned_records(
                packets, assignment["authority"]["assigned_evidence"])
        except GE.EvidenceError as exc:
            raise AuthorityError(str(exc)) from exc
        draft = _draft(root, number, frozen)
        identity = {"operation": operation, "generation": manifest["accepted_generation"],
                    "config": config, "selection": selection, "chapter": number}
        context = record["plan_context"]
        tasks[number] = C.task(C.make_task(
            identity, reviewer, prompt, draft.decode("utf-8"), context["text"],
            assignment, evidence))
    common = {"operation": operation, "generation": manifest["accepted_generation"],
              "run_sha256": PS.state_hash(manifest["run"]), "config": config,
              "selection": selection, "reviewer": reviewer,
              "rf11_receipt_hash": frozen["receipt_hash"],
              "control_authority_receipt_hash": writer["receipt_hash"],
              "prompt_sha256": PS.sha(prompt.encode("utf-8")),
              "rules_sha256": PS.state_hash(C.RULES)}
    return tasks, common


def load(root, supplied_cfg=None):
    root = Path(root).absolute()
    try:
        frozen = FB.require_frozen_batch(root)
        manifest, tree = CP.load(root), CP.candidate_tree(root)
        writer = json.loads(WO.read(root, manifest["operation"]))
        if writer.get("authority") == HCA.AUTHORITY:
            return _control_load(root, supplied_cfg, frozen, manifest, tree, writer)
        base = _base(root, supplied_cfg)
        frozen, manifest, _, _, audit, prompt, reviewer, config, operation = base
        selection, assignments = manifest["run"]["chapters"], audit.get("assignments")
        if not isinstance(assignments, dict) or set(assignments) != {
                f"C-{number:02d}" for number in selection}:
            raise AuthorityError("RF-09 assignments do not match the frozen selection")
        if audit.get("bindings", {}).get("assignment_sha256") != PS.state_hash(assignments):
            raise AuthorityError("RF-09 assignment hash is invalid")
        tasks = {number: _task(root, number, base, assignments[f"C-{number:02d}"])
                 for number in selection}
        common = {"operation": operation, "generation": manifest["accepted_generation"],
                  "run_sha256": PS.state_hash(manifest["run"]), "config": config,
                  "selection": selection, "reviewer": reviewer,
                  "rf11_receipt_hash": frozen["receipt_hash"],
                  "rf09_receipt_hash": audit["receipt_hash"],
                  "prompt_sha256": PS.sha(prompt.encode("utf-8")),
                  "rules_sha256": PS.state_hash(C.RULES)}
        return tasks, common
    except AuthorityError:
        raise
    except (FB.BatchError, CP.PairError, HCA.ControlAuthorityError, PS.StoreError,
            WO.OperationError, OSError,
            UnicodeError, json.JSONDecodeError, KeyError, TypeError, C.ContractError) as exc:
        raise AuthorityError(f"cannot resolve grounded authority: {exc}") from exc
