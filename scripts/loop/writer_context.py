"""Capture and render the exact RF-10 writer authority boundary."""
import json
import os
from pathlib import Path

import candidate_pair as CP
import commission_set as CS
import pair_store as PS
import writer_operation as WO

INPUT_KEYS = ("compact_writer_contract", "authoritative_commission",
              "previous_chapter")
NO_PREVIOUS_CHAPTER = "ABSENT — Chapter 1 has no previous chapter."
API_OUTPUT_CONTRACT = (
    "\n\n===== API OUTPUT CONTRACT (supersedes any save/report instructions above) =====\n"
    "You are running over a raw API with no filesystem. Return ONE thing: the complete final "
    "chapter text in book prose, starting with the chapter heading line. No preamble, no "
    "completion report, no word counts, no code fences. Your entire reply is saved verbatim "
    "as the chapter file."
)
MANUAL_RECEIPT = WO.RECEIPT


class WriterContextError(RuntimeError):
    pass


def _commission_paths(manifest):
    book = manifest["run"]["book"]
    return {number: f"{book}/commissions/chapter-{number:02d}.md"
            for number in manifest["run"]["chapters"]}


def capture(candidate, book, selected):
    """Capture authority bytes and prove they are the exact RF-09-audited pair."""
    receipt_hash = CS.require_writer_eligible(candidate)
    manifest = CP.load(candidate)
    tree = CP.candidate_tree(candidate)
    if Path(book).absolute() != tree / manifest["run"]["book"] \
            or list(selected) != manifest["run"]["chapters"]:
        raise WriterContextError("writer target differs from the audited commission set")
    receipt_file = PS._safe_file(CP.evidence_tree(candidate) / CS.RECEIPT,
                                 Path(candidate).absolute())
    receipt_bytes = receipt_file.read_bytes()
    try:
        receipt = json.loads(receipt_bytes)
    except json.JSONDecodeError as exc:
        raise WriterContextError("commission audit identity became invalid") from exc
    if receipt.get("receipt_hash") != receipt_hash:
        raise WriterContextError("commission audit identity changed during capture")
    paths = ["prompts/chapter-writer.md", *_commission_paths(manifest).values()]
    files = {relative: CP.require_member(
        candidate, tree / relative, manifest=manifest).read_bytes() for relative in paths}
    pair_inventory = PS.exact_tree(tree, CP._members(manifest))
    pair_hash = PS.state_hash(pair_inventory)
    if receipt.get("bindings", {}).get("candidate_pair_sha256") != pair_hash:
        raise WriterContextError("writer authority changed during eligibility capture")
    try:
        contract = files[paths[0]].decode("utf-8")
        commissions = {number: files[path].decode("utf-8")
                       for number, path in _commission_paths(manifest).items()}
    except UnicodeError as exc:
        raise WriterContextError("writer authority is not UTF-8") from exc
    return {"manifest": manifest, "files": files, "receipt_bytes": receipt_bytes,
            "pair_inventory": pair_inventory, "contract": contract,
            "commissions": commissions}


def require_fresh(candidate, authority):
    """Compare only writer authority, allowing expected candidate chapter writes."""
    root, tree = Path(candidate).absolute(), CP.candidate_tree(candidate)
    try:
        receipt = PS._safe_file(CP.evidence_tree(candidate) / CS.RECEIPT, root).read_bytes()
        if receipt != authority["receipt_bytes"]:
            raise WriterContextError("commission audit identity changed after eligibility")
        for relative, expected in authority["files"].items():
            actual = CP.require_member(
                candidate, tree / relative, manifest=authority["manifest"]).read_bytes()
            if actual != expected:
                raise WriterContextError(f"writer authority changed after eligibility: {relative}")
    except (CP.PairError, PS.StoreError, OSError) as exc:
        raise WriterContextError(f"writer authority freshness failed: {exc}") from exc


def manual_receipt_path(candidate):
    return Path(candidate).absolute() / MANUAL_RECEIPT


def _assignment(manifest):
    keys = ("schema", "accepted_generation", "accepted_pair_hash",
            "accepted_evaluation_hash", "entries", "outputs", "evaluation", "run")
    return {key: manifest[key] for key in keys}


def _draft_paths(manifest):
    book = manifest["run"]["book"]
    return [f"{book}/chapters/chapter-{number:02d}.md"
            for number in manifest["run"]["chapters"]]


def _manual_body(candidate, authority):
    manifest, files = authority["manifest"], authority["files"]
    receipt_bytes = authority["receipt_bytes"]
    root, run = Path(candidate).absolute(), manifest["run"]
    try:
        audit_hash = json.loads(receipt_bytes)["receipt_hash"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise WriterContextError("commission audit identity is invalid") from exc
    commissions = [{"chapter": number, "path": path,
                    "sha256": PS.sha(files[path])}
                   for number, path in _commission_paths(manifest).items()]
    return {
        "schema": 1,
        "operation": {"root": str(root), "experiment_id": run["experiment_id"],
                      "iteration_id": run["iteration_id"],
                      "accepted_generation": manifest["accepted_generation"]},
        "book": run["book"], "chapters": run["chapters"],
        "manifest_assignment_sha256": PS.state_hash(_assignment(manifest)),
        "pair_inventory": authority["pair_inventory"],
        "selected_draft_paths": _draft_paths(manifest),
        "contract": {"path": "prompts/chapter-writer.md",
                     "sha256": PS.sha(files["prompts/chapter-writer.md"])},
        "commissions": commissions,
        "audit": {"path": f"evidence/{CS.RECEIPT}",
                  "receipt_hash": audit_hash, "sha256": PS.sha(receipt_bytes)},
    }


def persist_manual_receipt(candidate, authority):
    """Transition the pair to a declared, hash-pinned manual handoff."""
    root, path = Path(candidate).absolute(), manual_receipt_path(candidate)
    try:
        manifest = CP.load(candidate)
        if manifest["state"] not in ("CANDIDATE", "WRITER_HANDOFF") \
                or _assignment(manifest) != _assignment(authority["manifest"]):
            raise WriterContextError("manual writer handoff operation identity changed")
        current = PS.exact_tree(CP.candidate_tree(candidate), CP._members(manifest))
        if current != authority["pair_inventory"]:
            raise WriterContextError("declared pair changed before manual handoff")
        body = _manual_body(candidate, authority)
        body["receipt_hash"] = PS.state_hash(body)
        data = PS.json_bytes(body)
        operation = {"group": "operation", "path": MANUAL_RECEIPT,
                     "sha256": PS.sha(data), "receipt_hash": body["receipt_hash"]}
        if manifest["state"] == "CANDIDATE":
            updated = {**manifest, "state": "WRITER_HANDOFF", "operation": operation}
            PS.exact_layout(root, manifest, {
                ".pair.json.rf02-tmp": PS.json_bytes(updated)})
            PS.write_json(CP._manifest_path(root), updated)
        elif manifest.get("operation") != operation:
            raise WriterContextError("manual writer handoff identity changed")
        if os.path.lexists(path):
            if PS._safe_file(path, root).read_bytes() != data:
                raise WriterContextError("manual writer authority receipt already differs")
        else:
            PS.write(path, data)
    except (CP.PairError, PS.StoreError, OSError) as exc:
        raise WriterContextError(f"manual writer authority receipt failed: {exc}") from exc
    return body["receipt_hash"]


def manual_receipt_hash(candidate):
    try:
        manifest = CP.load(candidate)
        data = WO.read(candidate, manifest.get("operation"))
        value = json.loads(data)
        recorded = value["receipt_hash"]
    except (CP.PairError, WO.OperationError, OSError, UnicodeError, json.JSONDecodeError,
            KeyError, TypeError) as exc:
        raise WriterContextError("manual writer authority receipt is missing or invalid") from exc
    return recorded


def require_manual_resume(candidate, book, selected, expected_hash):
    """Verify the pinned handoff while deliberately excluding selected chapter bytes."""
    manifest, root, tree = CP.load(candidate), Path(candidate).absolute(), CP.candidate_tree(candidate)
    operation = manifest.get("operation")
    if manifest["state"] not in ("WRITER_HANDOFF", "SEALED") or not operation:
        raise WriterContextError("operation has no durable manual writer handoff")
    recorded = manual_receipt_hash(candidate)
    if recorded != expected_hash or operation["receipt_hash"] != expected_hash:
        raise WriterContextError("manual writer authority receipt identity mismatch")
    if Path(book).absolute() != tree / manifest["run"]["book"] \
            or list(selected) != manifest["run"]["chapters"]:
        raise WriterContextError("manual writer resume target differs from its receipt")
    try:
        current = PS.exact_tree(tree, CP._members(manifest))
        audit = PS._safe_file(CP.evidence_tree(candidate) / CS.RECEIPT, root).read_bytes()
        value = json.loads(WO.read(candidate, manifest.get("operation")))
    except (CP.PairError, PS.StoreError, WO.OperationError, OSError,
            json.JSONDecodeError) as exc:
        raise WriterContextError(f"manual writer resume authority failed: {exc}") from exc
    value.pop("receipt_hash", None)
    drafts = _draft_paths(manifest)
    expected_inventory = value.get("pair_inventory")
    stable = {item["path"]: item["sha256"] for item in expected_inventory or ()
              if isinstance(item, dict) and item.get("path") not in drafts}
    current_stable = {item["path"]: item["sha256"] for item in current
                      if item["path"] not in drafts}
    identity = value.get("operation") == {
        "root": str(root), "experiment_id": manifest["run"]["experiment_id"],
        "iteration_id": manifest["run"]["iteration_id"],
        "accepted_generation": manifest["accepted_generation"]}
    inventory = [(item.get("group"), item.get("path"))
                 for item in expected_inventory or () if isinstance(item, dict)]
    if not identity or value.get("book") != manifest["run"]["book"] \
            or value.get("chapters") != manifest["run"]["chapters"] \
            or value.get("manifest_assignment_sha256") != PS.state_hash(_assignment(manifest)) \
            or value.get("selected_draft_paths") != drafts \
            or inventory != [(item["group"], item["path"]) for item in current] \
            or stable != current_stable \
            or value.get("audit", {}).get("sha256") != PS.sha(audit):
        raise WriterContextError("manual writer authority drifted after handoff")


def inputs(candidate, book, authority, number):
    """Assemble exactly contract, captured commission, and immediate previous chapter."""
    manifest = authority["manifest"]
    if number not in manifest["run"]["chapters"]:
        raise WriterContextError("chapter is outside the audited selection")
    if number == 1:
        previous = NO_PREVIOUS_CHAPTER
    else:
        previous = CP.require_member(
            candidate, Path(book) / f"chapters/chapter-{number-1:02d}.md",
            "product", manifest).read_text(encoding="utf-8")
    contract = authority["contract"].replace("[N]", str(number)).replace(
        "[SLUG]", Path(book).name) + API_OUTPUT_CONTRACT
    values = contract, authority["commissions"][number], previous
    return dict(zip(INPUT_KEYS, values))


def build(values):
    if tuple(values) != INPUT_KEYS or not all(isinstance(value, str)
                                              for value in values.values()):
        raise WriterContextError("writer inputs must be the exact ordered three-key contract")
    return "".join(f"===== {key} =====\n{values[key]}\n\n" for key in INPUT_KEYS)
