"""Canonical, resumable RF-02 gate decision receipt."""
import base64
import datetime as dt
import json
import os
from pathlib import Path

import pair_store as PS
import score_receipt as SR
import experiment_record as ER

PATH = "gate-decision.json"
ACCEPTED = {"BASELINE", "NEW-BEST", "KEEP", "PROMOTE"}


class DecisionError(RuntimeError):
    pass


def _path(root):
    return Path(root).absolute() / PATH


def _decode(value):
    try:
        return base64.b64decode(value, validate=True)
    except Exception as exc:
        raise DecisionError("gate decision row bytes are malformed") from exc


def load(root, tested_hash):
    path = _path(root)
    try:
        value = json.loads(PS._safe_file(path, Path(root).absolute()).read_text(
            encoding="utf-8"))
    except (OSError, json.JSONDecodeError, PS.StoreError) as exc:
        raise DecisionError(f"canonical gate decision is missing or malformed: {path}") from exc
    body = {key: item for key, item in value.items() if key != "decision_hash"}
    row, columns, schema = value.get("row"), value.get("columns"), value.get("schema")
    try:
        expected_row = (SR.row_bytes(row, columns) if schema == 1
                        and isinstance(row, dict) and isinstance(columns, list)
                        else ER.record_bytes(row) if schema == 2 and isinstance(row, dict)
                        else None)
    except ER.RecordError as exc:
        raise DecisionError("canonical causal record is invalid") from exc
    causal_ok = schema != 2 or (
        value.get("causal_record_sha256") == PS.sha(expected_row or b"")
        and isinstance(value.get("product_decision_sha256"), str)
        and len(value["product_decision_sha256"]) == 64
        and row.get("inputs", {}).get("tested_pair_hash") == tested_hash
        and {"SUPPORTED": "PROMOTE", "REFUTED": "REJECT",
             "INCONCLUSIVE": "INCONCLUSIVE"}.get(row.get("decision"))
        == value.get("verdict"))
    legacy_ok = schema != 1 or (row.get("tested_pair_hash") == tested_hash
                                and row.get("verdict") == value.get("verdict"))
    if schema not in (1, 2) or value.get("tested_pair_hash") != tested_hash \
            or value.get("decision_hash") != PS.state_hash(body) or expected_row is None \
            or _decode(value.get("row_bytes_b64", "")) != expected_row \
            or not causal_ok or not legacy_ok:
        raise DecisionError("canonical gate decision receipt is invalid")
    return value


def verify_history(decision, history_bytes):
    row = _decode(decision["row_bytes_b64"])
    if PS.sha(history_bytes) != decision.get("accepted_history_sha256") \
            or not history_bytes.endswith(row):
        raise DecisionError("accepted history bytes differ from the canonical gate decision")


def expected(manifest, score, history, row, columns, epsilon, best, best_iter,
             verdict, approved, timestamp):
    try:
        parsed = dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise DecisionError("gate decision timestamp must be UTC ISO-8601") from exc
    if parsed.utcoffset() != dt.timedelta(0):
        raise DecisionError("gate decision timestamp must be UTC ISO-8601")
    history = Path(history)
    original = history.read_bytes() if history.is_file() else b""
    base = {"schema": 1, "tested_pair_hash": manifest["tested_hash"],
            "score_receipt_hash": score["receipt_hash"],
            "history_sha256": PS.sha(original),
            "epsilon": epsilon, "best_accepted": best,
            "best_iteration": best_iter, "verdict": verdict,
            "human_promotion_approved": bool(approved)}
    full_row = dict(row)
    full_row["timestamp_utc"] = timestamp
    history_bytes = SR.result_history(history, full_row, columns)
    body = {**base, "row": full_row, "columns": list(columns),
            "row_bytes_b64": base64.b64encode(
                SR.row_bytes(full_row, columns)).decode("ascii"),
            "accepted_history_sha256": PS.sha(history_bytes)}
    return {**body, "decision_hash": PS.state_hash(body)}, history_bytes


def expected_causal(manifest, score, history, record, product_hash, verdict,
                    approved, timestamp):
    try:
        parsed = dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise DecisionError("gate decision timestamp must be UTC ISO-8601") from exc
    if parsed.utcoffset() != dt.timedelta(0):
        raise DecisionError("gate decision timestamp must be UTC ISO-8601")
    history = Path(history)
    original = history.read_bytes() if history.is_file() else b""
    try:
        history_bytes = ER.result_history(history, record)
        row_bytes = ER.record_bytes(record)
    except ER.RecordError as exc:
        raise DecisionError(str(exc)) from exc
    base = {"schema": 2, "tested_pair_hash": manifest["tested_hash"],
            "score_receipt_hash": score["receipt_hash"],
            "product_decision_sha256": product_hash,
            "causal_record_sha256": PS.sha(row_bytes),
            "history_sha256": PS.sha(original), "verdict": verdict,
            "decision_timestamp_utc": timestamp,
            "human_promotion_approved": bool(approved)}
    body = {**base, "row": dict(record),
            "row_bytes_b64": base64.b64encode(row_bytes).decode("ascii"),
            "accepted_history_sha256": PS.sha(history_bytes)}
    return {**body, "decision_hash": PS.state_hash(body)}, history_bytes


def terminal(value):
    """Return the exact terminal pair receipt bound to a canonical decision."""
    decision = "PROMOTED" if value["verdict"] in ACCEPTED else "REJECTED"
    return {"schema": 1, "tested_hash": value["tested_pair_hash"],
            "decision": decision, "gate_receipt": value}


def terminal_bytes(value):
    return PS.json_bytes(terminal(value))


def ensure(root, manifest, score, history, row, columns, epsilon, best, best_iter,
           verdict, approved, timestamp, interrupt=None):
    value, history_bytes = expected(
        manifest, score, history, row, columns, epsilon, best, best_iter,
        verdict, approved, timestamp)
    path = _path(root)
    try:
        PS.exact_layout(root, manifest, {
            ".gate-decision.json.rf02-tmp": PS.json_bytes(value),
            ".decision.json.rf02-tmp": terminal_bytes(value)})
    except PS.StoreError as exc:
        raise DecisionError(str(exc)) from exc
    if os.path.lexists(path):
        if load(root, manifest["tested_hash"]) != value:
            raise DecisionError("gate resume inputs differ from the canonical decision")
    else:
        PS.write_json(path, value, interrupt)
        path.chmod(0o444)
    verify_history(value, history_bytes)
    return value, history_bytes


def ensure_causal(root, manifest, score, history, record, product_hash, verdict,
                  approved, timestamp, interrupt=None):
    value, history_bytes = expected_causal(
        manifest, score, history, record, product_hash, verdict, approved, timestamp)
    path = _path(root)
    try:
        PS.exact_layout(root, manifest, {
            ".gate-decision.json.rf02-tmp": PS.json_bytes(value),
            ".decision.json.rf02-tmp": terminal_bytes(value)})
    except PS.StoreError as exc:
        raise DecisionError(str(exc)) from exc
    if os.path.lexists(path):
        if load(root, manifest["tested_hash"]) != value:
            raise DecisionError("gate resume inputs differ from the canonical decision")
    else:
        PS.write_json(path, value, interrupt)
        path.chmod(0o444)
    verify_history(value, history_bytes)
    return value, history_bytes


def for_promotion(root, tested_hash, history_bytes):
    value = load(root, tested_hash)
    verify_history(value, history_bytes)
    if value["verdict"] not in ACCEPTED or not value["human_promotion_approved"]:
        raise DecisionError("canonical gate decision does not authorize promotion")
    return value
