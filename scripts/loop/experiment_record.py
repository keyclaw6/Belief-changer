"""Validate the minimal RF-19 causal-bundle results lineage."""
import json
from pathlib import Path

import pair_store as PS


FIELDS = {
    "hypothesis", "causal_chain", "changed_bundle", "frozen_variables",
    "inputs", "evidence", "decision", "falsifier",
}
FIELDS_V2 = FIELDS | {"schema", "surface", "research"}
EVIDENCE = {
    "integrity", "reader_effect", "whole_opening_sequence",
    "carr_craft_diagnostic",
}
DECISIONS = {"DRY_RUN", "SUPPORTED", "REFUTED", "INCONCLUSIVE", "BLOCKED"}
PATH = "causal-record.json"
PREREG_FIELDS = {
    "hypothesis", "causal_chain", "changed_bundle", "frozen_variables",
    "inputs", "falsifier",
}
PREREG_FIELDS_V2 = PREREG_FIELDS | {"schema", "surface", "research"}
TREATMENT_FIELDS = PREREG_FIELDS | {
    "schema", "surface", "research_bundle", "downstream_effect",
}
SURFACES = {"research", "writing"}
RESEARCH_HARD_GATES = {
    "source_eligibility", "privacy", "safety", "originality", "traceability",
    "scientific_lineage", "inference_bounds", "deduplication", "coverage",
    "independent_evidence_judgment",
}
FROZEN_FOR_RESEARCH = {
    "subject", "input", "model", "planning", "commission", "writing",
    "safety", "evaluation",
}
SHA256 = __import__("re").compile(r"[0-9a-f]{64}")
RESEARCH_JUDGE_MODEL = "gpt-5.6-sol"
RESEARCH_JUDGE_REASONING = "ultra"


class RecordError(ValueError):
    pass


def research_comparison_schema():
    return {"type": "object", "additionalProperties": False,
        "properties": {"schema": {"type": "integer", "enum": [1]},
            "task_sha256": {"type": "string"},
            "preferred": {"type": "string", "enum": ["A", "B", "TIE"]},
            "decisive_reason": {"type": "string"}},
        "required": ["schema", "task_sha256", "preferred", "decisive_reason"]}


def research_comparison_prompt(task):
    return json.dumps(task, sort_keys=True, ensure_ascii=False)


def research_comparison_schema_bytes():
    return json.dumps(research_comparison_schema(), sort_keys=True,
                      separators=(",", ":")).encode()


def research_candidate(book):
    book = Path(book)
    paths = [book / "research/lived-experience.md",
             book / "research/scientific-evidence.md",
             book / "research/research-coverage.json"]
    paths.extend(sorted((book / "research/sources").glob("*.md")))
    try:
        return {path.relative_to(book).as_posix(): path.read_text(encoding="utf-8")
                for path in paths}
    except (OSError, UnicodeError) as exc:
        raise RecordError("research comparison candidate is missing or unreadable") from exc


def research_comparison_task(declaration, seals, candidates):
    validate_research_treatment(declaration)
    declaration_sha256 = PS.state_hash(declaration)
    if set(seals) != {"A", "B"} or set(candidates) != {"A", "B"}:
        raise RecordError("research comparison must contain exactly candidates A and B")
    for label in ("A", "B"):
        _seal(f"candidate {label} seal", seals[label])
        if not isinstance(candidates[label], dict) or not candidates[label]:
            raise RecordError(f"research comparison candidate {label} is empty")
    body = {"schema": 1, "instrument": "blind-research-quality",
        "fresh_context": True, "experiment_sha256": declaration_sha256,
        "candidate_seals": dict(seals),
        "instruction": "Compare evidence integrity, belief and reader coverage, and intervention utility. Prefer a side only for a material research-quality difference.",
        "causal_question": {"hypothesis": declaration["hypothesis"],
            "causal_chain": declaration["causal_chain"],
            "falsifier": declaration["falsifier"],
            "downstream_effect_required": declaration["downstream_effect"]["required"],
            "downstream_effect_task_sha256": declaration["downstream_effect"]["task_sha256"]},
        "candidates": candidates}
    return {**body, "task_sha256": PS.state_hash(body)}


def validate_research_comparison_verdict(task, verdict):
    if not isinstance(verdict, dict) or set(verdict) != {
            "schema", "task_sha256", "preferred", "decisive_reason"} \
            or verdict.get("schema") != 1 \
            or verdict.get("task_sha256") != task.get("task_sha256") \
            or verdict.get("preferred") not in {"A", "B", "TIE"} \
            or not isinstance(verdict.get("decisive_reason"), str) \
            or not verdict["decisive_reason"].strip():
        raise RecordError("research comparison verdict is malformed or stale")
    return verdict


def research_hypothesis_outcome(preferred, treatment_candidate="B"):
    """Map a blind preference to the hidden treatment only after judging."""
    if preferred not in {"A", "B", "TIE"} or treatment_candidate not in {"A", "B"}:
        raise RecordError("research comparison mapping is invalid")
    if preferred == "TIE":
        return "INCONCLUSIVE"
    return "SUPPORTED" if preferred == treatment_candidate else "REFUTED"


def research_downstream_contract(chapters):
    """Hash the preregistrable blind downstream instrument, before outputs exist."""
    values = list(chapters)
    if not values or any(not isinstance(value, int) or value < 1 for value in values) \
            or values != sorted(set(values)):
        raise RecordError("downstream chapter scope is invalid")
    body = {"schema": 1, "instrument": "blind-research-downstream-effect-v1",
        "chapters": values,
        "instruction": "Compare belief-change reader effect and source-bounded Carr-method execution. Prefer a side only for a material downstream difference."}
    return {**body, "contract_sha256": PS.state_hash(body)}


def research_downstream_candidate(book, chapters):
    """Load only the paired planning/writing outcomes exposed to the blind judge."""
    book = Path(book)
    paths = [book / "framing.md", book / "master-plan.md"]
    paths.extend(book / "chapters" / f"chapter-{number:02d}.md"
                 for number in chapters)
    try:
        values = {path.relative_to(book).as_posix(): path.read_text(encoding="utf-8")
                  for path in paths}
    except (OSError, UnicodeError) as exc:
        raise RecordError("downstream comparison candidate is missing or unreadable") from exc
    if any(not value.strip() for value in values.values()):
        raise RecordError("downstream comparison candidate contains an empty outcome")
    return values


def research_downstream_task(declaration, contract, pair_hashes, research_seals,
                             hard_gates, candidates):
    """Build an anonymous exact A/B downstream task from preregistered inputs."""
    validate_research_treatment(declaration)
    if contract.get("contract_sha256") != declaration["downstream_effect"][
            "task_sha256"]:
        raise RecordError("downstream instrument differs from preregistration")
    for values, label in ((pair_hashes, "pair hashes"),
                          (research_seals, "research seals"),
                          (hard_gates, "hard gates"), (candidates, "candidates")):
        if not isinstance(values, dict) or set(values) != {"A", "B"}:
            raise RecordError(f"downstream {label} must contain exactly A and B")
    for label in ("A", "B"):
        _seal(f"downstream {label} pair", pair_hashes[label])
        _seal(f"downstream {label} research seal", research_seals[label])
        _seal(f"downstream {label} hard gate", hard_gates[label])
        if not isinstance(candidates[label], dict) or not candidates[label]:
            raise RecordError(f"downstream candidate {label} is empty")
    body = {"schema": 1, "instrument": contract["instrument"],
        "fresh_context": True, "contract_sha256": contract["contract_sha256"],
        "instruction": contract["instruction"], "chapters": contract["chapters"],
        "candidate_pair_hashes": dict(pair_hashes),
        "research_seals": dict(research_seals),
        "hard_gate_sha256": dict(hard_gates), "candidates": candidates}
    return {**body, "task_sha256": PS.state_hash(body)}


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


def _seal(label, value):
    if not isinstance(value, str) or SHA256.fullmatch(value) is None:
        raise RecordError(f"{label} must be one lowercase sha256")


def _surface(record):
    """Validate the RF-32 surface extension without changing RF-19 history."""
    if record["schema"] != 2 or record["surface"] not in SURFACES:
        raise RecordError("schema 2 must declare a research or writing surface")
    research = record["research"]
    if not isinstance(research, dict):
        raise RecordError("research authority must be an object")
    changed = record["changed_bundle"]
    owners = [item.partition(":")[0] for item in changed]
    if any(not owner or ":" not in item for owner, item in zip(owners, changed)):
        raise RecordError("changed bundle items must use owner:change form")
    if record["surface"] == "research":
        expected = {
            "control_seal_sha256", "treatment_seal_sha256",
            "hard_gate_receipt_sha256", "comparison_task_sha256",
            "comparison_receipt_sha256", "downstream_effect_required",
            "downstream_effect_receipt_sha256",
        }
        if set(research) != expected:
            raise RecordError("research surface authority fields are missing or unknown")
        if set(owners) != {"research"}:
            raise RecordError("research treatment mixes research and writing variables")
        _seal("inputs.research_declaration_sha256",
              record["inputs"].get("research_declaration_sha256"))
        missing = FROZEN_FOR_RESEARCH - record["frozen_variables"].keys()
        if missing:
            raise RecordError(f"research treatment does not freeze {sorted(missing)[0]}")
        for name in ("hard_gate_receipt_sha256", "comparison_task_sha256",
                     "comparison_receipt_sha256"):
            _seal(f"research.{name}", research[name])
        required = research["downstream_effect_required"]
        receipt = research["downstream_effect_receipt_sha256"]
        if not isinstance(required, bool) or (required and receipt is None) \
                or (not required and receipt is not None):
            raise RecordError("research downstream-effect receipt contradicts preregistration")
        if receipt is not None:
            _seal("research.downstream_effect_receipt_sha256", receipt)
    else:
        expected = {"control_seal_sha256", "treatment_seal_sha256"}
        if set(research) != expected:
            raise RecordError("writing surface research authority fields are missing or unknown")
        if any(owner not in {"planning", "commission", "writing", "revision"}
               for owner in owners):
            raise RecordError("writing treatment mixes research or frozen variables")
        if research["control_seal_sha256"] != research["treatment_seal_sha256"]:
            raise RecordError("writing treatment must freeze the same accepted research seal")
        if record["frozen_variables"].get("accepted_research_seal_sha256") \
                != research["control_seal_sha256"]:
            raise RecordError("writing treatment frozen variables do not bind its research seal")
    _seal("research.control_seal_sha256", research["control_seal_sha256"])
    _seal("research.treatment_seal_sha256", research["treatment_seal_sha256"])


def validate(record):
    """Return record after enforcing the exact decision-evidence schema."""
    if not isinstance(record, dict) or set(record) not in (FIELDS, FIELDS_V2):
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
    if set(record) == FIELDS_V2:
        _surface(record)
    return record


def validate_preregistration(value):
    """Validate the immutable pre-call subset of the existing record schema."""
    if not isinstance(value, dict) or set(value) not in (
            PREREG_FIELDS, PREREG_FIELDS_V2):
        raise RecordError("preregistration fields must match the causal record subset")
    _text("hypothesis", value["hypothesis"])
    _text_list("causal_chain", value["causal_chain"])
    _text_list("changed_bundle", value["changed_bundle"])
    _text_map("frozen_variables", value["frozen_variables"])
    _text_map("inputs", value["inputs"])
    _text("falsifier", value["falsifier"])
    if set(value) == PREREG_FIELDS_V2:
        provisional = {**value, "evidence": {key: "PENDING" for key in EVIDENCE},
                       "decision": "DRY_RUN"}
        _surface(provisional)
    return value


def validate_research_treatment(value):
    """Validate the pre-dispatch research-only causal branch declaration."""
    if not isinstance(value, dict) or set(value) != TREATMENT_FIELDS \
            or value.get("schema") != 2 or value.get("surface") != "research":
        raise RecordError("research treatment must use the exact schema-2 declaration")
    _text("hypothesis", value["hypothesis"])
    _text_list("causal_chain", value["causal_chain"])
    _text_list("changed_bundle", value["changed_bundle"])
    _text_map("frozen_variables", value["frozen_variables"])
    _text_map("inputs", value["inputs"])
    _text("falsifier", value["falsifier"])
    if any(not item.startswith("research:") for item in value["changed_bundle"]):
        raise RecordError("research treatment mixes research and writing variables")
    missing = FROZEN_FOR_RESEARCH - value["frozen_variables"].keys()
    if missing:
        raise RecordError(f"research treatment does not freeze {sorted(missing)[0]}")
    for name in FROZEN_FOR_RESEARCH:
        _seal(f"frozen_variables.{name}", value["frozen_variables"][name])
    if set(value["inputs"]) != {"control_candidate_root", "treatment_candidate_root"}:
        raise RecordError("research treatment must name exactly two isolated candidate roots")
    if value["inputs"]["control_candidate_root"] == value["inputs"]["treatment_candidate_root"]:
        raise RecordError("research treatment candidate roots must be distinct")
    if any(not Path(item).is_absolute() for item in value["inputs"].values()):
        raise RecordError("research treatment candidate roots must be absolute")
    bundle = value["research_bundle"]
    if not isinstance(bundle, dict) or not bundle:
        raise RecordError("research treatment bundle must contain exact changed text")
    paths = []
    for path, text in bundle.items():
        _text("research_bundle path", path)
        if Path(path).is_absolute() or ".." in Path(path).parts \
                or path != "prompts/research-agent.md":
            raise RecordError("research treatment bundle path is not an allowed research component")
        if not isinstance(text, str) or not text:
            raise RecordError("research treatment bundle value must be exact non-empty text")
        paths.append(path)
    if set(value["changed_bundle"]) != {f"research:{path}" for path in paths}:
        raise RecordError("changed bundle does not name the exact research component paths")
    downstream = value["downstream_effect"]
    if not isinstance(downstream, dict) or set(downstream) != {
            "required", "task_sha256", "receipt_path"} \
            or not isinstance(downstream["required"], bool):
        raise RecordError("downstream-effect preregistration is malformed")
    if downstream["required"]:
        _seal("downstream_effect.task_sha256", downstream["task_sha256"])
        if not isinstance(downstream["receipt_path"], str) \
                or not Path(downstream["receipt_path"]).is_absolute():
            raise RecordError("required downstream effect must name an absolute receipt path")
    elif downstream["task_sha256"] is not None or downstream["receipt_path"] is not None:
        raise RecordError("unrequired downstream effect must not name task or receipt")
    return value


def bind_research_evidence(record, evidence):
    """Bind schema-2 research outcomes to actual compact evidence receipts."""
    validate(record)
    if record.get("surface") != "research" or not isinstance(evidence, dict) \
            or set(evidence) != {"hard_gates", "comparison", "downstream_effect"}:
        raise RecordError("research causal evidence fields are missing or unknown")
    authority = record["research"]
    hard, comparison, downstream = (evidence[name] for name in
                                    ("hard_gates", "comparison", "downstream_effect"))
    if not isinstance(hard, dict) or set(hard) != {
            "schema", "control_seal_sha256", "treatment_seal_sha256", "gates"} \
            or hard.get("schema") != 1 or set(hard.get("gates", {})) != RESEARCH_HARD_GATES \
            or any(SHA256.fullmatch(value or "") is None
                   for value in hard.get("gates", {}).values()):
        raise RecordError("research hard-gate receipt is malformed")
    if (hard["control_seal_sha256"], hard["treatment_seal_sha256"]) != (
            authority["control_seal_sha256"], authority["treatment_seal_sha256"]):
        raise RecordError("research hard-gate receipt binds different seals")
    if PS.state_hash(hard) != authority["hard_gate_receipt_sha256"]:
        raise RecordError("research hard-gate receipt hash is stale")
    if not isinstance(comparison, dict) or set(comparison) != {
            "schema", "task_sha256", "preferred", "treatment_candidate",
            "hypothesis_outcome", "verdict_sha256", "native_record_sha256",
            "native_binding"} \
            or comparison.get("schema") != 1 \
            or comparison.get("preferred") not in {"A", "B", "TIE"} \
            or comparison.get("treatment_candidate") not in {"A", "B"} \
            or not isinstance(comparison.get("native_binding"), dict) \
            or set(comparison["native_binding"]) != {
                "kind", "judge_identity", "fresh_ephemeral_context",
                "input_sha256", "output_schema_sha256"} \
            or comparison["native_binding"].get("kind") != "native-codex-subscription" \
            or comparison["native_binding"].get("judge_identity") \
                != "research-quality-independent" \
            or comparison["native_binding"].get("fresh_ephemeral_context") is not True \
            or any(SHA256.fullmatch(comparison["native_binding"].get(key, "")) is None
                   for key in ("input_sha256", "output_schema_sha256")):
        raise RecordError("research comparison receipt is malformed")
    if comparison["task_sha256"] != authority["comparison_task_sha256"] \
            or PS.state_hash(comparison) != authority["comparison_receipt_sha256"]:
        raise RecordError("research comparison receipt binding is stale")
    expected = research_hypothesis_outcome(
        comparison["preferred"], comparison["treatment_candidate"])
    if comparison["hypothesis_outcome"] != expected:
        raise RecordError("research hypothesis outcome contradicts the blind preference")
    if record["decision"] != expected:
        raise RecordError("research decision differs from the blind comparison")
    required = authority["downstream_effect_required"]
    if required:
        if not isinstance(downstream, dict) or PS.state_hash(downstream) != \
                authority["downstream_effect_receipt_sha256"] \
                or downstream.get("task_sha256") != record["inputs"].get(
                    "downstream_effect_task_sha256") or downstream.get("status") != "PASS":
            raise RecordError("required downstream-effect evidence is missing or stale")
    elif downstream is not None:
        raise RecordError("unrequired downstream-effect evidence must be absent")
    return record


def require_writing_surface(record, accepted_research_seal_sha256):
    """Reject a new writing decision unless it freezes one current research seal."""
    validate(record)
    if record.get("schema") != 2 or record.get("surface") != "writing":
        raise RecordError("new writing outcomes must use the schema-2 writing surface")
    _seal("accepted research seal", accepted_research_seal_sha256)
    research = record["research"]
    if research["control_seal_sha256"] != accepted_research_seal_sha256 \
            or research["treatment_seal_sha256"] != accepted_research_seal_sha256:
        raise RecordError("writing outcome does not bind the current accepted research seal")
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


def bind(record, product_decision, tested_pair_hash, product_decision_sha256,
         preregistration=None, research_evidence=None):
    """Fail closed unless one record exactly represents the gate's product decision."""
    validate(record)
    if record.get("surface") == "research":
        if research_evidence is None:
            raise RecordError("research outcome lacks bound causal evidence receipts")
        bind_research_evidence(record, research_evidence)
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
    if preregistration is not None:
        frozen = validate_preregistration(preregistration)
        for field in set(frozen) - {"inputs"}:
            if record[field] != frozen[field]:
                raise RecordError(f"causal record post-authored preregistered {field}")
        if any(inputs.get(key) != value for key, value in frozen["inputs"].items()):
            raise RecordError("causal record post-authored preregistered inputs")
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
