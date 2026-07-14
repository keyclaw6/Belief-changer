"""Canonical, resumable RF-02 gate decision receipt."""
import base64
import datetime as dt
import json
import os
from pathlib import Path

import pair_store as PS
import score_receipt as SR

PATH = "gate-decision.json"
ACCEPTED = {"BASELINE", "NEW-BEST", "KEEP"}


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
    row, columns = value.get("row"), value.get("columns")
    if value.get("schema") != 1 or value.get("tested_pair_hash") != tested_hash \
            or value.get("decision_hash") != PS.state_hash(body) \
            or not isinstance(row, dict) or not isinstance(columns, list) \
            or _decode(value.get("row_bytes_b64", "")) != SR.row_bytes(row, columns) \
            or row.get("tested_pair_hash") != tested_hash \
            or row.get("verdict") != value.get("verdict"):
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


def for_promotion(root, tested_hash, history_bytes):
    value = load(root, tested_hash)
    verify_history(value, history_bytes)
    if value["verdict"] not in ACCEPTED or not value["human_promotion_approved"]:
        raise DecisionError("canonical gate decision does not authorize promotion")
    return value
