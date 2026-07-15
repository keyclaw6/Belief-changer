"""Pure RF-17/RF-18 integrity, blind-panel, and product decision rules."""
import json
import re
from collections.abc import Mapping
from pathlib import Path

import defect_routing as ROUTING
import pair_store as PS


PATH = "product-decision.json"
OWNERS = ROUTING.OWNERS
VERDICT_FIELDS = {
    "task_id", "raw_verdict_id", "actor", "kind", "family", "verdict",
    "scope", "promotion_eligible", "base_task_sha256", "tested_pair_hash",
    "prompt_sha256", "input_sha256",
}
VERDICTS = {"PASS", "FAIL", "INCONCLUSIVE"}
HEX = re.compile(r"^[0-9a-f]{64}$")


class ProductDecisionError(ValueError):
    pass


def _text(value, field, layer):
    if not isinstance(value, str) or not value.strip():
        raise ProductDecisionError(f"{layer}: {field} must be non-empty text")
    return value


def _hash(value, field, layer):
    if not isinstance(value, str) or not HEX.fullmatch(value):
        raise ProductDecisionError(f"{layer}: {field} must be a sha256")


def bound_task_id(row):
    """Bind one context identity to the anonymous task, pair, and exact prompt."""
    return PS.state_hash({key: row[key] for key in (
        "base_task_sha256", "tested_pair_hash", "prompt_sha256",
        "input_sha256", "actor")})


def _row(verdict, layer):
    if not isinstance(verdict, Mapping) or set(verdict) != VERDICT_FIELDS:
        raise ProductDecisionError(f"{layer}: verdict fields must be exact")
    row = dict(verdict)
    for field in ("raw_verdict_id", "actor"):
        _text(row[field], field, layer)
    if row["scope"] != "ordinary_product" or row["promotion_eligible"] is not True:
        raise ProductDecisionError(f"{layer}: calibration/nonpromotable verdict is forbidden")
    for field in ("base_task_sha256", "tested_pair_hash",
                  "prompt_sha256", "input_sha256"):
        _hash(row[field], field, layer)
    if row["task_id"] != bound_task_id(row):
        raise ProductDecisionError(f"{layer}: task identity is stale or unbound")
    if row["kind"] not in {"model", "human"} or row["verdict"] not in VERDICTS:
        raise ProductDecisionError(f"{layer}: kind or verdict is unsupported")
    if row["kind"] == "model":
        _text(row["family"], "family", layer)
    elif row["family"] is not None or len(row["actor"].split()) < 2:
        raise ProductDecisionError(f"{layer}: human verdict must name a real reviewer")
    return row


def aggregate_pair(verdicts, *, layer="panel", tested_pair_hash=None,
                   prompt_sha256=None):
    """Validate two independent verdict identities and return their consensus."""
    if not isinstance(verdicts, (list, tuple)) or len(verdicts) != 2:
        raise ProductDecisionError(f"{layer}: exactly two fresh verdicts are required")
    rows = [_row(value, layer) for value in verdicts]
    for field in ("task_id", "raw_verdict_id", "actor"):
        if len({row[field] for row in rows}) != 2:
            raise ProductDecisionError(f"{layer}: {field}s must identify fresh contexts")
    for field in ("base_task_sha256", "tested_pair_hash",
                  "prompt_sha256", "input_sha256"):
        if len({row[field] for row in rows}) != 1:
            raise ProductDecisionError(f"{layer}: verdicts bind unrelated tasks or pairs")
    if tested_pair_hash and rows[0]["tested_pair_hash"] != tested_pair_hash:
        raise ProductDecisionError(f"{layer}: verdicts bind another sealed pair")
    if prompt_sha256 and rows[0]["prompt_sha256"] != prompt_sha256:
        raise ProductDecisionError(f"{layer}: verdicts use a stale product rubric")

    kinds = {row["kind"] for row in rows}
    if kinds == {"model"} and len({row["family"] for row in rows}) == 2:
        panel = "two_model_families"
    elif kinds == {"model", "human"}:
        panel = "model_plus_named_human"
    else:
        raise ProductDecisionError(
            f"{layer}: use two model families or one model plus a named human")
    votes = {row["verdict"] for row in rows}
    return {
        "status": rows[0]["verdict"] if len(votes) == 1 else "INCONCLUSIVE",
        "panel": panel, "task_ids": [row["task_id"] for row in rows],
        "raw_verdict_ids": [row["raw_verdict_id"] for row in rows],
        "verdicts": rows,
    }


def _integrity_layer(core, grounded, developmental):
    if not isinstance(grounded, Mapping) or grounded.get("state") != "PASSED" \
            or not isinstance(developmental, Mapping) \
            or developmental.get("state") != "PASS":
        raise ProductDecisionError("canonical grounded/developmental PASS receipts required")
    checks = core.get("checks") if isinstance(core, Mapping) else None
    if not isinstance(checks, Mapping):
        raise ProductDecisionError("integrity: recomputed hard checks are missing")
    cross, mantra = checks.get("originality"), checks.get("mantra")
    near, lengths = checks.get("near_copy"), checks.get("length")
    repetition = checks.get("repetition_within")
    review_pass = grounded["state"] == "PASSED"
    values = {
        "source_grounding_pass": review_pass,
        "safety_pass": review_pass,
        "originality_pass": isinstance(cross, Mapping) and cross.get("tripped") is False,
        "near_copy_pass": isinstance(near, list) and bool(near) and all(
            row.get("ratio", 1) <= row.get("tripwire", 0) for row in near),
        "method_integrity_pass": review_pass,
        "exact_mantra_pass": isinstance(mantra, Mapping) and not mantra.get("failures"),
        "loose_length_pass": isinstance(lengths, list) and bool(lengths)
        and all(row.get("ok") is True for row in lengths),
    }
    failures = [field for field, passed in values.items() if not passed]
    repair = isinstance(repetition, Mapping) and bool(repetition.get("hard_fails"))
    return {"status": "FAIL" if failures else "PASS", "checks": values,
            "failures": failures,
            "repair_signals": ["non_mantra_repetition"] if repair else []}


def _require_fresh_layers(chapter, sequence, tested_pair_hash):
    for field in ("task_ids", "raw_verdict_ids"):
        if set(chapter[field]) & set(sequence[field]):
            raise ProductDecisionError(f"blind layers reuse {field[:-1]} identity")
    pairs = {row["tested_pair_hash"] for layer in (chapter, sequence)
             for row in layer["verdicts"]}
    if pairs != {tested_pair_hash}:
        raise ProductDecisionError("blind layers do not bind the sealed tested pair")


def load_evidence(path, tested_pair_hash):
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProductDecisionError(f"product evidence is missing or malformed: {path}") from exc
    fields = {"schema", "tested_pair_hash", "blind_chapter_effect",
              "blind_whole_opening_sequence"}
    if not isinstance(value, dict) or set(value) != fields or value.get("schema") != 1 \
            or value.get("tested_pair_hash") != tested_pair_hash:
        raise ProductDecisionError("product evidence fields or tested-pair binding are invalid")
    return value


def decide(*, core, grounded_review, developmental_review, chapter_effect=None,
           whole_opening_sequence=None, carr_craft=None,
           tested_pair_hash=None, prompt_sha256=None):
    """Return four separate evidence layers and one non-numeric product decision."""
    _hash(tested_pair_hash, "tested_pair_hash", "decision")
    _hash(prompt_sha256, "prompt_sha256", "decision")
    integrity = _integrity_layer(core, grounded_review, developmental_review)
    if integrity["status"] == "FAIL":
        chapter = sequence = {"status": "NOT_RUN"}
        decision, reason = "REJECT", "integrity hard gate failed"
    else:
        chapter = aggregate_pair(chapter_effect, layer="blind chapter effect",
                                 tested_pair_hash=tested_pair_hash,
                                 prompt_sha256=prompt_sha256)
        sequence = aggregate_pair(
            whole_opening_sequence, layer="blind whole-opening sequence",
            tested_pair_hash=tested_pair_hash, prompt_sha256=prompt_sha256)
        _require_fresh_layers(chapter, sequence, tested_pair_hash)
        if "INCONCLUSIVE" in {chapter["status"], sequence["status"]}:
            decision, reason = "INCONCLUSIVE", "blind judges materially disagreed"
        elif chapter["status"] == sequence["status"] == "PASS":
            decision, reason = "PROMOTE", "blind effect and sequence both passed"
        else:
            decision, reason = "REJECT", "blind effect or sequence failed"
    if not isinstance(carr_craft, Mapping):
        raise ProductDecisionError("Carr craft diagnostic must be a mapping")
    return {
        "decision": decision, "reason": reason, "tested_pair_hash": tested_pair_hash,
        "layers": {"integrity_hard_gate": integrity,
                   "blind_chapter_effect": chapter,
                   "blind_whole_opening_sequence": sequence,
                   "carr_craft_diagnostic": {
                       "role": "DIAGNOSTIC_ONLY", "evidence": dict(carr_craft)}},
        "owner_vocabulary": list(OWNERS),
    }
