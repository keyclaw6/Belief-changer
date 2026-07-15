"""Validate the minimal RF-19 causal-bundle results lineage."""
import json
from pathlib import Path

import pair_store as PS


FIELDS = {
    "hypothesis", "causal_chain", "changed_bundle", "frozen_variables",
    "inputs", "evidence", "decision", "falsifier",
}
EVIDENCE = {
    "integrity", "reader_effect", "whole_opening_sequence",
    "carr_craft_diagnostic",
}
DECISIONS = {"DRY_RUN", "SUPPORTED", "REFUTED", "INCONCLUSIVE", "BLOCKED"}
PATH = "causal-record.json"


class RecordError(ValueError):
    pass


def _text(label, value):
    if not isinstance(value, str) or not value.strip():
        raise RecordError(f"{label} must be non-empty text")


def _text_list(label, value):
    if not isinstance(value, list) or not value:
        raise RecordError(f"{label} must be a non-empty list")
    for item in value:
        _text(label, item)
    if len(value) != len(set(value)):
        raise RecordError(f"{label} contains duplicates")


def _text_map(label, value):
    if not isinstance(value, dict) or not value:
        raise RecordError(f"{label} must be a non-empty object")
    for key, item in value.items():
        _text(f"{label} key", key)
        _text(f"{label}.{key}", item)


def validate(record):
    """Return record after enforcing the exact decision-evidence schema."""
    if not isinstance(record, dict) or set(record) != FIELDS:
        raise RecordError("record fields must match the minimal RF-19 schema")
    _text("hypothesis", record["hypothesis"])
    _text_list("causal_chain", record["causal_chain"])
    _text_list("changed_bundle", record["changed_bundle"])
    _text_map("frozen_variables", record["frozen_variables"])
    _text_map("inputs", record["inputs"])
    if not isinstance(record["evidence"], dict) \
            or set(record["evidence"]) != EVIDENCE:
        raise RecordError("evidence must contain exactly the four product layers")
    for layer, outcome in record["evidence"].items():
        _text(f"evidence.{layer}", outcome)
    if record["decision"] not in DECISIONS:
        raise RecordError("decision is not a causal-bundle outcome")
    _text("falsifier", record["falsifier"])
    return record


def load(path):
    """Read and validate every non-blank JSONL record without mutating it."""
    records = []
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RecordError(f"line {number} is not JSON") from exc
        try:
            records.append(validate(record))
        except RecordError as exc:
            raise RecordError(f"line {number}: {exc}") from exc
    if not records:
        raise RecordError("results lineage is empty")
    return records


def load_one(path):
    """Load one pending causal record from the fixed gate evidence path."""
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RecordError(f"pending causal record is missing or malformed: {path}") from exc
    return validate(value)


def decision_evidence(product_decision):
    try:
        layers = product_decision["layers"]
        return {
            "integrity": layers["integrity_hard_gate"]["status"],
            "reader_effect": layers["blind_chapter_effect"]["status"],
            "whole_opening_sequence": layers["blind_whole_opening_sequence"]["status"],
            "carr_craft_diagnostic": layers["carr_craft_diagnostic"]["role"],
        }
    except (KeyError, TypeError) as exc:
        raise RecordError("product decision does not contain four evidence layers") from exc


def bind(record, product_decision, tested_pair_hash, product_decision_sha256):
    """Fail closed unless one record exactly represents the gate's product decision."""
    validate(record)
    inputs = record["inputs"]
    if inputs.get("tested_pair_hash") != tested_pair_hash \
            or inputs.get("product_decision_sha256") != product_decision_sha256 \
            or product_decision_sha256 != PS.state_hash(product_decision):
        raise RecordError("causal record does not bind the tested pair and product decision")
    expected = {"PROMOTE": "SUPPORTED", "REJECT": "REFUTED",
                "INCONCLUSIVE": "INCONCLUSIVE"}.get(product_decision.get("decision"))
    if record["decision"] != expected or record["evidence"] != decision_evidence(
            product_decision):
        raise RecordError("causal outcome or four evidence layers differ from the decision")
    return record


def record_bytes(record):
    validate(record)
    return (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()


def result_history(path, record):
    """Append one validated JSON line without rewriting accepted lineage bytes."""
    old = Path(path).read_bytes() if Path(path).is_file() else b""
    if old.strip():
        load(path)
        if not old.endswith(b"\n"):
            raise RecordError("accepted causal lineage must end with a newline")
    return old + record_bytes(record)
