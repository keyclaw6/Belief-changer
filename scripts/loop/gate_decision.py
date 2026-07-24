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
RESEARCH_APPROVAL = "evidence/research-causal/human-approval.json"
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


def research_material(root):
    """Load the exact compact research evidence consumed by the RF-02 gate."""
    base = Path(root).absolute() / "evidence" / "research-causal"
    try:
        record = json.loads(PS._safe_file(
            base / "causal-record.json", Path(root).absolute()).read_text(encoding="utf-8"))
        declaration = json.loads(PS._safe_file(
            base / "declaration.json", Path(root).absolute()).read_text(encoding="utf-8"))
        hard = json.loads(PS._safe_file(
            base / "hard-gates.json", Path(root).absolute()).read_text(encoding="utf-8"))
        comparison = json.loads(PS._safe_file(
            base / "comparison-receipt.json", Path(root).absolute()).read_text(encoding="utf-8"))
        marker = json.loads(PS._safe_file(
            base / "comparison.marker.json", Path(root).absolute()).read_text(encoding="utf-8"))
        result = json.loads(PS._safe_file(
            base / "comparison.result.json", Path(root).absolute()).read_text(encoding="utf-8"))
        downstream_path = base / "downstream-effect-bound.json"
        downstream = (json.loads(PS._safe_file(
            downstream_path, Path(root).absolute()).read_text(encoding="utf-8"))
            if os.path.lexists(downstream_path) else None)
    except (OSError, json.JSONDecodeError, PS.StoreError) as exc:
        raise DecisionError("research causal evidence is missing or malformed") from exc
    evidence = {"hard_gates": hard, "comparison": comparison,
                "downstream_effect": downstream}
    try:
        ER.validate_research_treatment(declaration)
        ER.bind_research_evidence(record, evidence)
    except ER.RecordError as exc:
        raise DecisionError(str(exc)) from exc
    if PS.state_hash(declaration) != record.get("inputs", {}).get(
            "research_declaration_sha256") \
            or any(record.get(key) != declaration.get(key) for key in (
                "schema", "surface", "hypothesis", "causal_chain", "changed_bundle",
                "frozen_variables", "falsifier")) \
            or any(record.get("inputs", {}).get(key) != value
                   for key, value in declaration.get("inputs", {}).items()):
        raise DecisionError("research causal record differs from its declaration")
    task = marker.get("task") if isinstance(marker, dict) else None
    native = result.get("native") if isinstance(result, dict) else None
    verdict = native.get("verdict") if isinstance(native, dict) else None
    try:
        expected_task = ER.research_comparison_task(
            declaration, task.get("candidate_seals", {}), task.get("candidates", {}))
        ER.validate_research_comparison_verdict(task, verdict)
    except (ER.RecordError, AttributeError) as exc:
        raise DecisionError("durable research comparison task is invalid") from exc
    if not isinstance(task, dict) or task != expected_task \
            or marker != {"schema": 1, "task_sha256": task["task_sha256"],
                          "treatment_candidate": "B", "task": task} \
            or not isinstance(native, dict) or not isinstance(verdict, dict) \
            or result != {"schema": 1, "task_sha256": task["task_sha256"],
                          "native": native,
                          "native_record_sha256": PS.state_hash(native)} \
            or native.get("model") != ER.RESEARCH_JUDGE_MODEL \
            or native.get("reasoning") != ER.RESEARCH_JUDGE_REASONING \
            or not native.get("thread_id") or not native.get("command"):
        raise DecisionError("durable native research comparison is missing or stale")
    binding_keys = {"kind", "judge_identity", "fresh_ephemeral_context",
                    "input_sha256", "output_schema_sha256"}
    binding = {key: native.get(key) for key in binding_keys}
    prompt = ER.research_comparison_prompt(task)
    if binding.get("input_sha256") != PS.sha(prompt.encode()) \
            or binding.get("output_schema_sha256") != PS.sha(
                ER.research_comparison_schema_bytes()):
        raise DecisionError("native research comparison binds a different task contract")
    expected_comparison = {"schema": 1, "task_sha256": task["task_sha256"],
        "preferred": verdict["preferred"], "treatment_candidate": "B",
        "hypothesis_outcome": ER.research_hypothesis_outcome(
            verdict["preferred"], "B"),
        "verdict_sha256": PS.state_hash(verdict),
        "native_record_sha256": result["native_record_sha256"],
        "native_binding": binding}
    if comparison != expected_comparison:
        raise DecisionError("research comparison receipt differs from its durable native result")
    return record, evidence, declaration


def research_approval(root, tested_hash, record, evidence):
    """Load one named-human receipt bound to the exact research decision inputs."""
    path = Path(root).absolute() / RESEARCH_APPROVAL
    try:
        value = json.loads(PS._safe_file(
            path, Path(root).absolute()).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, PS.StoreError) as exc:
        raise DecisionError("named-human research approval is missing or malformed") from exc
    fields = {"schema", "reviewer_name", "reviewer_role", "decision",
              "approved_at_utc", "tested_pair_hash", "causal_record_sha256",
              "research_evidence_sha256", "control_seal_sha256",
              "treatment_seal_sha256"}
    if not isinstance(value, dict):
        raise DecisionError("named-human research approval is missing or malformed")
    try:
        parsed = dt.datetime.fromisoformat(
            str(value.get("approved_at_utc", "")).replace("Z", "+00:00"))
    except ValueError as exc:
        raise DecisionError("named-human research approval timestamp is invalid") from exc
    if not isinstance(value, dict) or set(value) != fields or value.get("schema") != 1 \
            or not isinstance(value.get("reviewer_name"), str) \
            or not value["reviewer_name"].strip() \
            or value.get("reviewer_role") != "named-human" \
            or value.get("decision") != "PROMOTE" \
            or parsed.utcoffset() != dt.timedelta(0) \
            or value.get("tested_pair_hash") != tested_hash \
            or value.get("causal_record_sha256") != PS.sha(ER.record_bytes(record)) \
            or value.get("research_evidence_sha256") != PS.state_hash(evidence) \
            or value.get("control_seal_sha256") != record["research"][
                "control_seal_sha256"] \
            or value.get("treatment_seal_sha256") != record["research"][
                "treatment_seal_sha256"]:
        raise DecisionError("named-human research approval binds different evidence")
    return {"reviewer_name": value["reviewer_name"],
            "reviewer_role": value["reviewer_role"],
            "receipt_sha256": PS.state_hash(value)}


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
                        else ER.record_bytes(row) if schema in (2, 3) and isinstance(row, dict)
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
    research_ok = True
    if schema == 3:
        try:
            stored_record, evidence, _declaration = research_material(root)
        except DecisionError:
            research_ok = False
        else:
            research_ok = (
                stored_record == row and row.get("surface") == "research"
                and value.get("causal_record_sha256") == PS.sha(expected_row or b"")
                and value.get("research_evidence_sha256") == PS.state_hash(evidence)
                and {"SUPPORTED": "PROMOTE", "REFUTED": "REJECT",
                     "INCONCLUSIVE": "INCONCLUSIVE"}.get(row.get("decision"))
                == value.get("verdict")
                and ((value.get("verdict") == "PROMOTE"
                      and value.get("human_promotion_approved") is True
                      and isinstance(value.get("human_approval"), dict)
                      and set(value["human_approval"]) == {
                          "reviewer_name", "reviewer_role", "receipt_sha256"}
                      and value["human_approval"].get("reviewer_role") == "named-human"
                      and isinstance(value["human_approval"].get("reviewer_name"), str)
                      and bool(value["human_approval"]["reviewer_name"].strip())
                      and len(value["human_approval"].get("receipt_sha256", "")) == 64)
                     or (value.get("verdict") != "PROMOTE"
                         and value.get("human_promotion_approved") is False
                         and value.get("human_approval") is None)))
    if schema not in (1, 2, 3) or value.get("tested_pair_hash") != tested_hash \
            or value.get("decision_hash") != PS.state_hash(body) or expected_row is None \
            or _decode(value.get("row_bytes_b64", "")) != expected_row \
            or not causal_ok or not legacy_ok or not research_ok:
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


def expected_research(manifest, history, record, evidence, verdict, approval,
                      timestamp):
    try:
        parsed = dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise DecisionError("gate decision timestamp must be UTC ISO-8601") from exc
    if parsed.utcoffset() != dt.timedelta(0):
        raise DecisionError("gate decision timestamp must be UTC ISO-8601")
    history = Path(history)
    original = history.read_bytes() if history.is_file() else b""
    try:
        ER.bind_research_evidence(record, evidence)
        history_bytes = ER.result_history(history, record)
        row_bytes = ER.record_bytes(record)
    except ER.RecordError as exc:
        raise DecisionError(str(exc)) from exc
    expected_verdict = {"SUPPORTED": "PROMOTE", "REFUTED": "REJECT",
                        "INCONCLUSIVE": "INCONCLUSIVE"}.get(record.get("decision"))
    if record.get("surface") != "research" or verdict != expected_verdict:
        raise DecisionError("research outcome does not map to the RF-02 verdict")
    if (verdict == "PROMOTE") != (approval is not None):
        raise DecisionError("research promotion requires one named-human approval")
    base = {"schema": 3, "tested_pair_hash": manifest["tested_hash"],
            "research_evidence_sha256": PS.state_hash(evidence),
            "causal_record_sha256": PS.sha(row_bytes),
            "history_sha256": PS.sha(original), "verdict": verdict,
            "decision_timestamp_utc": timestamp,
            "human_promotion_approved": approval is not None,
            "human_approval": approval}
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


def ensure_research(root, manifest, history, verdict, approval, timestamp,
                    interrupt=None):
    record, evidence, _declaration = research_material(root)
    value, history_bytes = expected_research(
        manifest, history, record, evidence, verdict, approval, timestamp)
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
