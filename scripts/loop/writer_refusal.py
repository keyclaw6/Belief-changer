"""Durable RF-14 writer refusal routed to its earliest owning stage."""
import json
import os
from pathlib import Path

import candidate_pair as CP
import defect_routing as ROUTING
import draft_call as DC
import draft_batch_state as S
from draft_batch_contract import BatchError
import pair_store as PS

SCHEMA = 1
ACTION = "repair_owner_and_regenerate_downstream"
PREFIX = "ROUTE REFUSAL: "
FOLDER = "writer-refusal"
RECEIPT = "receipt.json"
SOURCE = "manual-chapter-{number:02d}.txt"
ANCHOR = "writer-refusal-anchor.json"


class RefusalError(BatchError):
    pass


class RoutedRefusal(RefusalError):
    pass


def folder(root):
    return CP.evidence_tree(root) / FOLDER


def receipt_path(root):
    return folder(root) / RECEIPT


def manual_path(root, number):
    return folder(root) / SOURCE.format(number=number)


def anchor_path(root):
    return Path(root).absolute() / ANCHOR


def prepare_manual(root):
    evidence, target = CP.evidence_tree(root), folder(root)
    operation = Path(root).absolute()
    PS.safe_dir(operation)
    if not os.path.lexists(evidence):
        evidence.mkdir()
    PS.safe_dir(evidence, operation)
    if not os.path.lexists(target):
        target.mkdir()
    PS.safe_dir(target, evidence)
    return target


def parse(text):
    if not isinstance(text, str) or not text.startswith(PREFIX) or "\n" in text:
        raise RefusalError("writer route refusal must be exactly one canonical line")
    def exact_object(pairs):
        keys = [key for key, _value in pairs]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate key")
        return dict(pairs)
    try:
        finding = json.loads(text[len(PREFIX):], object_pairs_hook=exact_object)
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        raise RefusalError(f"writer route refusal JSON is malformed: {exc}") from exc
    if not isinstance(finding, dict) or set(finding) != {
            "action_code", "finding", "owner"}:
        raise RefusalError("writer route refusal fields are not exact")
    if finding.get("owner") not in ROUTING.OWNERS:
        raise RefusalError("writer route refusal owner is not canonical")
    note = finding.get("finding")
    if finding.get("action_code") != ACTION \
            or not isinstance(note, str) or not note or note != note.strip() \
            or len(note) > 500:
        raise RefusalError("writer route refusal action or finding is invalid")
    canonical = PREFIX + json.dumps(finding, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":"))
    if text != canonical:
        raise RefusalError("writer route refusal bytes are not canonical")
    return finding


def is_refusal(text):
    return isinstance(text, str) and text.strip().startswith(PREFIX)


def _source(root, batch, number, supplied=None):
    if batch["mode"] == "api":
        call = batch.get("call")
        if not call or call.get("chapter") != number:
            raise RefusalError("API refusal lost its durable model call")
        raw, descriptor = DC.read(root, call)
        try:
            text = raw.decode("utf-8")
        except UnicodeError as exc:
            raise RefusalError("writer refusal is not UTF-8") from exc
        source = {"path": f"evidence/{S.FOLDER}/{descriptor['path']}",
                  "file_sha256": descriptor["sha256"],
                  "response_sha256": descriptor["response_sha256"]}
    else:
        path = manual_path(root, number)
        try:
            data = PS._safe_file(path, folder(root)).read_bytes()
            text = data.decode("utf-8")
        except (PS.StoreError, OSError, UnicodeError) as exc:
            raise RefusalError(f"manual writer refusal is unreadable: {exc}") from exc
        source = {"path": f"evidence/{FOLDER}/{path.name}",
                  "file_sha256": PS.sha(data), "response_sha256": PS.sha(data)}
    if supplied is not None and text != supplied:
        raise RefusalError("writer refusal differs from its durable response")
    return text, source


def _receipt(batch, number, text, source):
    finding = parse(text)
    routing = ROUTING.plan("chapter-writer", [finding], ACTION)
    body = {"schema": SCHEMA, "state": "ROUTED", "chapter": number,
            "mode": batch["mode"], "batch_start_sha256": batch["start_sha256"],
            "operation_sha256": PS.state_hash(batch["operation"]),
            "source": source, "routing": routing}
    body["receipt_hash"] = PS.state_hash(body)
    data = PS.json_bytes(body)
    descriptor = {"chapter": number, "path": f"evidence/{FOLDER}/{RECEIPT}",
                  "sha256": PS.sha(data), "receipt_hash": body["receipt_hash"],
                  "routing_sha256": routing["routing_sha256"], "source": source}
    return body, data, descriptor


def _write_receipt(root, data, interrupt=None):
    target = receipt_path(root)
    prepare_manual(root)
    if os.path.lexists(target):
        if PS._safe_file(target, folder(root)).read_bytes() != data:
            raise RefusalError("writer route receipt identity changed")
    else:
        PS.write(target, data, interrupt)
    target.chmod(0o444)


def _write_anchor(root, data, interrupt=None):
    target = anchor_path(root)
    if os.path.lexists(target):
        if PS._safe_file(target, Path(root).absolute()).read_bytes() != data:
            raise RefusalError("writer refusal monotonic anchor changed")
    else:
        PS.write(target, data, interrupt)
    target.chmod(0o444)


def _record(root, batch, number, text, source, interrupt=None):
    if batch.get("refusal") is not None:
        return require(root, batch)
    remaining = batch["selection"][len(batch["drafts"]):]
    if batch["state"] != "DRAFTING" or batch.get("pending") is not None \
            or not remaining or number != remaining[0]:
        raise RefusalError("writer refusal is outside the next draft assignment")
    body, data, descriptor = _receipt(batch, number, text, source)
    manifest = CP.load(root)
    S.save(root, manifest, {**batch, "refusal": descriptor}, interrupt)
    (interrupt or (lambda _step: None))("refusal-recorded")
    _write_anchor(root, data, interrupt)
    (interrupt or (lambda _step: None))("refusal-anchored")
    _write_receipt(root, data, interrupt)
    source_path = Path(root).absolute() / source["path"]
    source_path.chmod(0o444)
    (interrupt or (lambda _step: None))("refusal-receipt-written")
    return body["routing"]


def require(root, batch=None):
    batch = batch or CP.load(root).get("draft_batch") or {}
    descriptor = batch.get("refusal")
    if descriptor is None:
        raise RefusalError("operation has no durable writer route refusal")
    number = descriptor.get("chapter") if isinstance(descriptor, dict) else None
    text, source = _source(root, batch, number)
    body, data, expected = _receipt(batch, number, text, source)
    if descriptor != expected:
        raise RefusalError("writer route refusal descriptor changed")
    ROUTING.require_plan(body["routing"])
    _write_anchor(root, data)
    _write_receipt(root, data)
    source_path = Path(root).absolute() / source["path"]
    source_path.chmod(0o444)
    expected_tree = [{"group": "evidence", "path": RECEIPT}]
    if batch["mode"] == "manual":
        expected_tree.append({"group": "evidence", "path": source_path.name})
    PS.exact_tree(folder(root), expected_tree)
    return body["routing"]


def _message(plan):
    return (f"writer routed refusal to {plan['next_owner']}; repair "
            f"{','.join(plan['repair_artifacts'])}, then regenerate exactly "
            f"{','.join(plan['regenerate_owners'])}; route={plan['routing_sha256']}")


def require_clear(root, batch=None):
    batch = batch or CP.load(root).get("draft_batch") or {}
    if batch.get("refusal") is not None:
        raise RoutedRefusal(_message(require(root, batch)))


def capture_api(root, number, text, interrupt=None):
    if not is_refusal(text):
        return None
    batch = CP.load(root).get("draft_batch") or {}
    _, source = _source(root, batch, number, text)
    plan = _record(root, batch, number, text, source, interrupt)
    raise RoutedRefusal(_message(plan))


def capture_manual(root, interrupt=None):
    batch = CP.load(root).get("draft_batch") or {}
    require_clear(root, batch)
    remaining = batch.get("selection", [])[len(batch.get("drafts", [])):]
    if not remaining:
        return None
    existing = [number for number in remaining if os.path.lexists(manual_path(root, number))]
    if not existing:
        return None
    if existing != [remaining[0]]:
        raise RefusalError("manual writer refusal is out of order or duplicated")
    number = existing[0]
    text, source = _source(root, batch, number)
    if not is_refusal(text):
        raise RefusalError("manual writer refusal sidecar lacks canonical prefix")
    plan = _record(root, batch, number, text, source, interrupt)
    raise RoutedRefusal(_message(plan))
