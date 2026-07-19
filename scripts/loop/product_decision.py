"""Pure RF-17/RF-18 integrity, blind-panel, and product decision rules."""
import json, re; from collections.abc import Mapping; from pathlib import Path
import defect_routing as ROUTING
import pair_store as PS
PATH, OWNERS = "product-decision.json", ROUTING.OWNERS
VERDICT_FIELDS = {"task_id", "raw_verdict_id", "actor", "kind", "family", "verdict",
    "scope", "promotion_eligible", "base_task_sha256", "tested_pair_hash", "prompt_sha256", "input_sha256"}
VERDICTS, HF01_READERS = {"PASS", "FAIL", "INCONCLUSIVE"}, ("sol-xhigh-r1", "sol-xhigh-r2")
HF01_EXTRA = {"reader_identity", "treatment_candidate", "gsbs_sha256", "envelope_sha256", "raw_record_sha256", "authority_sha256", "native_call_sha256", "model", "route", "reasoning", "command"}
HF01_COMMAND = ["codex", "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules", "--disable", "multi_agent", "--model", "gpt-5.6-sol", "-c", "model_reasoning_effort=xhigh", "--sandbox", "read-only", "--skip-git-repo-check", "--cd", "<isolated-tmp>", "--output-schema", "<isolated-tmp>/judge-output-schema.json", "--json", "-"]
HEX = re.compile(r"^[0-9a-f]{64}$")
class ProductDecisionError(ValueError): pass
def _text(value, field, layer):
    if not isinstance(value, str) or not value.strip(): raise ProductDecisionError(f"{layer}: {field} must be non-empty text")
    return value
def _hash(value, field, layer):
    if not isinstance(value, str) or not HEX.fullmatch(value): raise ProductDecisionError(f"{layer}: {field} must be a sha256")
def bound_task_id(row):
    return PS.state_hash({key: row[key] for key in ("base_task_sha256", "tested_pair_hash",
        "prompt_sha256", "input_sha256", "actor")})
def _row(verdict, layer):
    if not isinstance(verdict, Mapping) or set(verdict) != VERDICT_FIELDS:
        raise ProductDecisionError(f"{layer}: verdict fields must be exact")
    row = dict(verdict)
    for field in ("raw_verdict_id", "actor"): _text(row[field], field, layer)
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
    return {"status": rows[0]["verdict"] if len(votes) == 1 else "INCONCLUSIVE",
        "panel": panel, "task_ids": [row["task_id"] for row in rows],
        "raw_verdict_ids": [row["raw_verdict_id"] for row in rows], "verdicts": rows}
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
    values = {"source_grounding_pass": review_pass, "safety_pass": review_pass,
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
    if not isinstance(carr_craft, Mapping): raise ProductDecisionError("Carr craft diagnostic must be a mapping")
    return {"decision": decision, "reason": reason, "tested_pair_hash": tested_pair_hash,
        "layers": {"integrity_hard_gate": integrity, "blind_chapter_effect": chapter,
            "blind_whole_opening_sequence": sequence, "carr_craft_diagnostic": {
                "role": "DIAGNOSTIC_ONLY", "evidence": dict(carr_craft)}},
        "owner_vocabulary": list(OWNERS)}
def _hf01_panel(verdicts, layer, experiment_hash, prompt_sha256, gsbs_sha256):
    if not isinstance(verdicts, (list, tuple)) or len(verdicts) != 2:
        raise ProductDecisionError(f"{layer}: exactly two independent readers required")
    if any(not isinstance(value, Mapping) or set(value) != VERDICT_FIELDS | HF01_EXTRA
           for value in verdicts):
        raise ProductDecisionError(f"{layer}: GSBS verdict fields must be exact")
    rows = []
    for value in verdicts:
        row = _row({key: value[key] for key in VERDICT_FIELDS}, layer)
        for field in ("gsbs_sha256", "envelope_sha256", "raw_record_sha256",
                      "authority_sha256", "native_call_sha256"):
            _hash(value[field], field, layer)
        if value["reader_identity"] != row["actor"] or value["treatment_candidate"] not in {"A", "B"}:
            raise ProductDecisionError(f"{layer}: reader position or treatment support is stale")
        if (value["model"], value["route"], value["reasoning"], value["command"]) != \
                ("gpt-5.6-sol", "codex-native", "xhigh", HF01_COMMAND):
            raise ProductDecisionError(f"{layer}: decisive native route binding is stale")
        rows.append({**row, **{key: value[key] for key in HF01_EXTRA}})
    for field in ("task_id", "raw_verdict_id", "actor"):
        if len({row[field] for row in rows}) != 2:
            raise ProductDecisionError(f"{layer}: {field}s must identify fresh contexts")
    if tuple(row["reader_identity"] for row in rows) != HF01_READERS \
            or {row["treatment_candidate"] for row in rows} != {"A", "B"} \
            or len({row["base_task_sha256"] for row in rows}) != 2 \
            or len({row["input_sha256"] for row in rows}) != 2 \
            or len({row["envelope_sha256"] for row in rows}) != 2:
        raise ProductDecisionError(f"{layer}: opposite A/B order and two fresh readers are required")
    if rows[0]["tested_pair_hash"] != experiment_hash \
            or {row["tested_pair_hash"] for row in rows} != {experiment_hash} \
            or {row["prompt_sha256"] for row in rows} != {prompt_sha256} \
            or {row["gsbs_sha256"] for row in rows} != {gsbs_sha256}:
        raise ProductDecisionError(f"{layer}: treatment/GSBS or rubric binding is stale")
    kinds = {row["kind"] for row in rows}
    if kinds not in ({"model"}, {"model", "human"}):
        raise ProductDecisionError(f"{layer}: readers must be independent models or model/human")
    return rows
def decide_hf01(*, integrity, causal_diagnostic, chapter_panels, whole_opening_panel, carr_craft,
                 human_approval, control_pair_hash, treatment_pair_hash, gsbs_sha256, gsbs_panel_sha256,
                 prompt_sha256, blind_receipt_sha256,
                 reference_sighted_diagnostic_sha256, decision_context_sha256):
    for field, value in (("control_pair_hash", control_pair_hash), ("treatment_pair_hash", treatment_pair_hash),
                         ("gsbs_sha256", gsbs_sha256), ("prompt_sha256", prompt_sha256),
                         ("blind_receipt_sha256", blind_receipt_sha256),
                         ("reference_sighted_diagnostic_sha256", reference_sighted_diagnostic_sha256),
                         ("decision_context_sha256", decision_context_sha256)):
        _hash(value, field, "H-F01")
    if not isinstance(integrity, Mapping) or integrity.get("status") != "PASS" \
            or integrity.get("unsupported_claim_comparison", {}).get("increased") is not False:
        raise ProductDecisionError("H-F01 all-six integrity PASS is required")
    if not isinstance(causal_diagnostic, Mapping) or causal_diagnostic.get("role") != "DIAGNOSTIC_ONLY" \
            or causal_diagnostic.get("status") != "PASS" \
            or len(causal_diagnostic.get("task_ids", ())) != 6:
        raise ProductDecisionError("H-F01 control/treatment causal diagnostic is incomplete")
    if not isinstance(chapter_panels, (list, tuple)) or len(chapter_panels) != 3:
        raise ProductDecisionError("H-F01 requires three matched chapter panels")
    if not isinstance(gsbs_panel_sha256, (list, tuple)) or len(gsbs_panel_sha256) != 4:
        raise ProductDecisionError("H-F01 GSBS panel hashes are incomplete")
    for digest in gsbs_panel_sha256: _hash(digest, "gsbs_panel_sha256", "H-F01")
    experiment_hash = PS.state_hash({"control_pair_hash": control_pair_hash,
                                     "treatment_pair_hash": treatment_pair_hash,
                                     "gsbs_sha256": gsbs_sha256})
    chapters = [_hf01_panel(panel, f"H-F01 chapter {index}", experiment_hash,
                            prompt_sha256, gsbs_panel_sha256[index - 1])
                for index, panel in enumerate(chapter_panels, 1)]
    opening = _hf01_panel(whole_opening_panel, "H-F01 whole opening",
                          experiment_hash, prompt_sha256, gsbs_panel_sha256[3])
    all_rows = [row for panel in (*chapters, opening) for row in panel]
    for field in ("task_id", "raw_verdict_id"):
        if len({row[field] for row in all_rows}) != 8:
            raise ProductDecisionError(f"H-F01 reuses a blind {field}")
    chapter_votes = [row["verdict"] for panel in chapters for row in panel]
    opening_votes = [row["verdict"] for row in opening]
    passes = chapter_votes.count("PASS")
    if "INCONCLUSIVE" in chapter_votes + opening_votes:
        decision, reason = "INCONCLUSIVE", "a blind reader returned no material preference"
    elif passes >= 5 and opening_votes == ["PASS", "PASS"]:
        decision, reason = "PROMOTE", "at least 5/6 chapter and 2/2 opening votes passed"
    elif passes <= 3 or opening_votes == ["FAIL", "FAIL"]:
        decision, reason = "REJECT", "chapter or opening falsifier fired"
    else:
        decision, reason = "INCONCLUSIVE", "blind effect is between decisive thresholds"
    fields = {"schema", "reviewer", "verdict", "reviewed_at_utc", "control_pair_hash", "treatment_pair_hash", "gsbs_sha256",
              "blind_receipt_sha256", "reference_sighted_diagnostic_sha256",
              "decision_context_sha256", "receipt_sha256"}
    if not isinstance(human_approval, Mapping) or set(human_approval) != fields \
            or human_approval.get("schema") != 2 or len(str(human_approval.get("reviewer", "")).split()) < 2 \
            or human_approval.get("verdict") not in {"APPROVE", "REJECT"} \
            or human_approval.get("control_pair_hash") != control_pair_hash or human_approval.get("treatment_pair_hash") != treatment_pair_hash \
            or human_approval.get("gsbs_sha256") != gsbs_sha256 or human_approval.get("blind_receipt_sha256") != blind_receipt_sha256 \
            or human_approval.get("reference_sighted_diagnostic_sha256") != reference_sighted_diagnostic_sha256 \
            or human_approval.get("decision_context_sha256") != decision_context_sha256:
        raise ProductDecisionError("H-F01 requires an exact named-human reading receipt")
    for field in ("reference_sighted_diagnostic_sha256", "decision_context_sha256", "receipt_sha256"): _hash(human_approval[field], field, "H-F01 human")
    body = {key: value for key, value in human_approval.items() if key != "receipt_sha256"}
    if human_approval["receipt_sha256"] != PS.sha(PS.json_bytes(body)): raise ProductDecisionError("H-F01 named-human receipt hash is stale")
    if human_approval["verdict"] == "REJECT": decision, reason = "REJECT", "named human rejected the direct reading comparison"
    if not isinstance(carr_craft, Mapping):
        raise ProductDecisionError("Carr craft diagnostic must be a mapping")
    return {"decision": decision, "reason": reason,
        "tested_pair_hash": treatment_pair_hash, "control_pair_hash": control_pair_hash,
        "experiment_sha256": experiment_hash, "gsbs_sha256": gsbs_sha256,
        "gsbs_panel_sha256": list(gsbs_panel_sha256), "blind_receipt_sha256": blind_receipt_sha256,
        "reference_sighted_diagnostic_sha256": reference_sighted_diagnostic_sha256, "decision_context_sha256": decision_context_sha256,
        "human_approval": dict(human_approval),
        "layers": {"integrity_hard_gate": dict(integrity),
            "control_treatment_causal_diagnostic": dict(causal_diagnostic),
            "blind_chapter_effect": {"status": "PASS" if passes >= 5 else
                "FAIL" if passes <= 3 else "INCONCLUSIVE", "pass_votes": passes,
                "required": 5, "panels": chapters},
            "blind_whole_opening_sequence": {"status": "PASS" if opening_votes ==
                ["PASS", "PASS"] else "FAIL" if opening_votes == ["FAIL", "FAIL"]
                else "INCONCLUSIVE", "pass_votes": opening_votes.count("PASS"),
                "required": 2, "verdicts": opening},
            "carr_craft_diagnostic": {"role": "DIAGNOSTIC_ONLY",
                                      "evidence": dict(carr_craft)}},
        "owner_vocabulary": list(OWNERS)}
