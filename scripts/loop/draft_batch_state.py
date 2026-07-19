"""RF-11 first-draft batch identity and atomic manifest state."""
import json
import os
import re
from pathlib import Path

import candidate_pair as CP
import draft_batch_lifecycle as L
from draft_batch_contract import (BatchError, FOLDER, RECEIPT, SCHEMA, folder,
                                  relative, start_marker, validate_pair, validate_shape)
import loopcfg
import pair_store as PS
import writer_operation as WO

WORD_RE = re.compile(r"[A-Za-z0-9']+")
START = L.START


def entry(manifest, number, data):
    return {"chapter": number, "path": relative(manifest, number),
            "sha256": PS.sha(data)}


def validate_draft(data, number):
    try:
        text = data.decode("utf-8").strip()
    except UnicodeError as exc:
        raise BatchError(f"chapter {number} is not UTF-8") from exc
    if text.startswith("ROUTE REFUSAL:"):
        raise BatchError(f"chapter {number} is a routed refusal, not a draft")
    count = len(WORD_RE.findall(text.lower()))
    if count < 800:
        raise BatchError(f"chapter {number} has {count} words; expected a complete draft")
    return count


def clean_response(raw):
    try:
        text = raw.decode("utf-8").strip()
    except UnicodeError as exc:
        raise BatchError("model response is not UTF-8") from exc
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return (text + "\n").encode("utf-8")


def save(root, manifest, batch, interrupt=None, state=None, start=None):
    updated = {**manifest, "draft_batch": batch}
    if state is not None:
        updated["state"] = state
    if start is not None:
        updated["draft_batch_start"] = start
    try:
        PS.exact_layout(root, manifest, {".pair.json.rf02-tmp": PS.json_bytes(updated)})
        PS.write_json(CP._manifest_path(root), updated, interrupt)
        return CP.load(root)
    except (CP.PairError, PS.StoreError, OSError) as exc:
        raise BatchError(f"draft batch state write failed: {exc}") from exc


def receipt_value(root, manifest):
    try:
        raw = WO.read(root, manifest.get("operation"))
        value = json.loads(raw)
        receipt_hash = value["receipt_hash"]
        inventory = value["pair_inventory"]
    except (WO.OperationError, TypeError, KeyError, json.JSONDecodeError) as exc:
        raise BatchError(f"writer authority identity is invalid: {exc}") from exc
    return value, receipt_hash, inventory


def operation(manifest, receipt_hash, inventory):
    run = manifest["run"]
    return {"experiment_id": run["experiment_id"],
            "iteration_id": run["iteration_id"],
            "accepted_generation": manifest["accepted_generation"],
            "accepted_pair_hash": manifest["accepted_pair_hash"],
            "accepted_evaluation_hash": manifest["accepted_evaluation_hash"],
            "run_sha256": PS.state_hash(run),
            "writer_receipt_hash": receipt_hash,
            "writer_inventory_sha256": PS.state_hash(inventory)}


def config(root, manifest):
    tree, relative_path = CP.candidate_tree(root), manifest["run"]["config"]
    try:
        data = CP.require_member(root, tree / relative_path, "config", manifest).read_bytes()
        values = loopcfg.load(tree / relative_path)
    except (CP.PairError, OSError) as exc:
        raise BatchError(f"draft batch configuration is invalid: {exc}") from exc
    return {"path": relative_path, "sha256": PS.sha(data),
            "values_sha256": PS.state_hash(values)}


def identity(root, manifest, batch):
    validate_shape(batch, manifest)
    value, receipt_hash, inventory = receipt_value(root, manifest)
    try:
        if value.get("authority") == "hf01-control":
            import hf01_control_authority as HCA
            HCA.require_resume(root, CP.candidate_tree(root) / manifest["run"]["book"],
                               batch["selection"], receipt_hash)
        else:
            import writer_context as WC
            WC.require_manual_resume(root, CP.candidate_tree(root) / manifest["run"]["book"],
                                     batch["selection"], receipt_hash)
    except (RuntimeError, CP.PairError, PS.StoreError, OSError) as exc:
        raise BatchError(f"writer authority drifted during draft batch: {exc}") from exc
    selected = {relative(manifest, number) for number in batch["selection"]}
    expected = {item["path"]: item["sha256"] for item in inventory
                if item.get("path") in selected}
    if batch["operation"] != operation(manifest, receipt_hash, inventory) \
            or batch["config"] != config(root, manifest) \
            or {item["path"]: item["sha256"] for item in batch["baseline"]} != expected:
        raise BatchError("authority, configuration, or product baseline drifted")
    return value


def begin(root, mode, authority_sha256, interrupt=None):
    manifest = CP.load(root)
    if manifest.get("draft_batch") is not None:
        batch = manifest["draft_batch"]
        identity(root, manifest, batch)
        if batch["mode"] != mode:
            raise BatchError("draft generation mode changed mid-batch")
        if batch["authority_sha256"] != authority_sha256:
            raise BatchError("draft generation authority changed mid-batch")
        return batch
    _, receipt_hash, inventory = receipt_value(root, manifest)
    hashes = {item["path"]: item["sha256"] for item in inventory}
    baseline = [{"chapter": number, "path": relative(manifest, number),
                 "sha256": hashes[relative(manifest, number)]}
                for number in manifest["run"]["chapters"]]
    batch = {"schema": SCHEMA, "state": "DRAFTING", "mode": mode,
             "operation": operation(manifest, receipt_hash, inventory),
             "selection": manifest["run"]["chapters"], "config": config(root, manifest),
             "baseline": baseline, "drafts": [], "pending": None,
             "receipt": None, "pair_sha256": None, "responses": [], "call": None,
             "refusal": None, "authority_sha256": authority_sha256}
    start = start_marker(batch)
    batch["start_sha256"] = start["start_sha256"]
    try:
        L.start(root, manifest, batch, start, interrupt)
        return CP.load(root)["draft_batch"]
    except L.LifecycleError as exc:
        raise BatchError(f"draft batch lifecycle start failed: {exc}") from exc


def safe_pending(path, root, wanted):
    tmp = path.with_name(f".{path.name}.rf02-tmp")
    if not os.path.lexists(tmp):
        return None
    try:
        data = PS._safe_file(tmp, root).read_bytes()
    except PS.StoreError as exc:
        raise BatchError(str(exc)) from exc
    if os.lstat(tmp).st_uid != os.lstat(root).st_uid or PS.sha(data) != wanted:
        raise BatchError(f"draft staging bytes do not belong to this batch: {tmp}")
    return data


def write_snapshot(root, path, data, interrupt=None):
    batch_folder = folder(root)
    if not os.path.lexists(batch_folder):
        evidence = CP.evidence_tree(root)
        PS.safe_dir(evidence, root)
        batch_folder.mkdir()
        PS.safe_dir(batch_folder, evidence)
    else:
        PS.safe_dir(batch_folder, CP.evidence_tree(root))
    if os.path.lexists(path):
        actual = PS._safe_file(path, batch_folder).read_bytes()
        if actual != data:
            raise BatchError(f"draft evidence already differs: {path.name}")
        return
    staged = safe_pending(path, batch_folder, PS.sha(data))
    if staged is not None and staged != data:
        raise BatchError(f"draft evidence staging differs: {path.name}")
    PS.write(path, data, interrupt)
