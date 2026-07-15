"""Strict RF-12 task, verdict, and structural routing contracts."""
import json
import re

import pair_store as PS

SCHEMA = 2
PROMPT = "prompts/grounded-reviewer.md"
FOLDER = "grounded-review"
RECEIPT = "receipt.json"
LOCATOR = re.compile(r"^S-\d{3}#E-\d{3}$")
RULES = (
    "assigned evidence records and provenance bounds are hard authority",
    "safety limits are hard and medical specifics stay with qualified professionals",
    "reference prose is forbidden; assigned-excerpt near-copy signals are hard",
    "warm to the reader and never shame or moralize",
    "belief change must not use willpower, deprivation, resistance, or day-counting",
    "unassigned evidence and work reserved elsewhere are forbidden",
)
CLASS_RULES = {
    "invention": {
        "conditions": {"unsupported_by_assigned_authority"},
        "routes": {"research": "repair_assigned_evidence",
                   "commissioning": "repair_commission_authority",
                   "writing": "remove_unsupported_span"}},
    "inference broadening": {
        "conditions": {"exceeds_permitted_inference"},
        "routes": {"research": "repair_assigned_evidence",
                   "commissioning": "repair_commission_authority",
                   "writing": "narrow_claim_to_assigned_authority"}},
    "packet conflict": {
        "conditions": {"assigned_authority_conflict"},
        "routes": {"research": "resolve_assigned_conflict",
                   "commissioning": "repair_commission_authority"}},
    "safety breach": {
        "conditions": {"omits_required_safety_limit",
                       "violates_required_safety_limit"},
        "routes": {"research": "repair_assigned_evidence",
                   "framing": "repair_framing_authority",
                   "planning": "repair_plan_authority",
                   "commissioning": "repair_commission_authority",
                   "writing": "restore_required_safeguard"}},
    "originality/near-copy": {
        "conditions": {"near_copy_of_assigned_excerpt"},
        "routes": {"writing": "replace_near_copy_span"}},
    "ownership leakage": {
        "conditions": {"uses_unassigned_authority", "performs_reserved_work",
                       "omits_required_commission_condition"},
        "routes": {"framing": "repair_framing_authority",
                   "planning": "repair_plan_authority",
                   "commissioning": "repair_commission_authority",
                   "writing": "remove_reserved_or_unassigned_work"}},
}


class ContractError(RuntimeError):
    pass


def _unique(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ContractError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def loads(raw, label="JSON"):
    try:
        return json.loads(raw, object_pairs_hook=_unique)
    except ContractError:
        raise
    except (json.JSONDecodeError, TypeError, UnicodeError) as exc:
        raise ContractError(f"{label} is not one strict JSON object: {exc}") from exc


def model(cfg):
    keys = ("model", "family", "route", "reasoning")
    values = {key: cfg.get(f"grounded_reviewer_{key}") for key in keys}
    if not all(isinstance(value, str) and value.strip() for value in values.values()):
        raise ContractError("grounded reviewer model metadata is incomplete")
    if values["route"].casefold() != "codex-native":
        raise ContractError("grounded reviewer must use the native Codex route")
    if values["reasoning"].casefold() != "xhigh":
        raise ContractError("grounded reviewer reasoning must be xhigh")
    writer_model = str(cfg.get("writer_model", "")).strip()
    writer_family = str(cfg.get("writer_family") or writer_model.split("/", 1)[0]).strip()
    if not writer_model or not writer_family:
        raise ContractError("writer family provenance is missing")
    if values["model"].casefold() == writer_model.casefold() \
            or values["family"].casefold() == writer_family.casefold():
        raise ContractError("grounded reviewer family must differ from the writer")
    return values


def make_task(identity, reviewer, prompt, draft, commission, assignment, evidence):
    context = {"prompt": prompt, "rules": list(RULES), "frozen_draft": draft,
               "authoritative_commission": commission, "assignment": assignment,
               "assigned_evidence": evidence}
    body = {"schema": SCHEMA, **identity, "fresh_context": True,
            "reviewer": reviewer, "context": context}
    return {**body, "task_sha256": PS.state_hash(body)}


def task(value):
    keys = {"schema", "operation", "generation", "config", "selection", "chapter",
            "fresh_context", "reviewer", "context", "task_sha256"}
    if not isinstance(value, dict) or set(value) != keys or value.get("schema") != SCHEMA:
        raise ContractError("grounded task fields are missing or unknown")
    body = {key: item for key, item in value.items() if key != "task_sha256"}
    if value.get("task_sha256") != PS.state_hash(body):
        raise ContractError("grounded task identity is stale or tampered")
    if value.get("fresh_context") is not True or not isinstance(value.get("chapter"), int):
        raise ContractError("grounded task dispatch identity is malformed")
    records = value.get("context", {}).get("assigned_evidence")
    if not isinstance(records, list) or not records:
        raise ContractError("grounded task has no assigned evidence records")
    locators = [record.get("locator") for record in records if isinstance(record, dict)]
    if len(locators) != len(records) or len(locators) != len(set(locators)) \
            or any(not isinstance(item, str) or not LOCATOR.fullmatch(item)
                   for item in locators):
        raise ContractError("grounded task assigned evidence is malformed")
    return value


def _finding(value, draft, assigned):
    keys = {"classification", "draft_span", "source_locators", "condition_code",
            "owner", "action_code"}
    if not isinstance(value, dict) or set(value) != keys:
        raise ContractError("grounded finding fields are missing or unknown")
    rules = CLASS_RULES.get(value["classification"])
    if not rules or value["condition_code"] not in rules["conditions"] \
            or rules["routes"].get(value["owner"]) != value["action_code"]:
        raise ContractError("grounded finding route is invalid")
    span = value["draft_span"]
    if not isinstance(span, str) or not span.strip() \
            or span != "<missing>" and span not in draft:
        raise ContractError("grounded finding draft span is not exact")
    omitted = value["condition_code"].startswith("omits_")
    if (span == "<missing>") != omitted:
        raise ContractError("grounded finding missing condition does not match its span")
    locators = value["source_locators"]
    if not isinstance(locators, list) \
            or any(not isinstance(item, str) or item not in assigned for item in locators) \
            or len(locators) != len(set(locators)):
        raise ContractError("grounded finding locator is invalid or unassigned")
    source_required = value["classification"] in {
        "invention", "inference broadening", "packet conflict", "originality/near-copy"}
    if source_required and not locators:
        raise ContractError("grounded finding requires assigned source authority")


def verdict(raw, expected_task):
    value = loads(raw, "grounded verdict")
    keys = {"schema", "task_sha256", "verdict", "findings"}
    if not isinstance(value, dict) or set(value) != keys or value.get("schema") != SCHEMA:
        raise ContractError("grounded verdict fields are missing or unknown")
    if value["task_sha256"] != expected_task["task_sha256"]:
        raise ContractError("grounded verdict task identity is stale")
    findings = value["findings"]
    if value["verdict"] not in ("PASS", "BLOCK") or not isinstance(findings, list) \
            or value["verdict"] == "PASS" and findings \
            or value["verdict"] == "BLOCK" and not findings:
        raise ContractError("grounded verdict must be exact PASS or BLOCK")
    assigned = {record["locator"] for record in
                expected_task["context"]["assigned_evidence"]}
    for finding in findings:
        _finding(finding, expected_task["context"]["frozen_draft"], assigned)
    return value


def output_schema():
    string = {"type": "string"}
    finding = {"type": "object", "additionalProperties": False,
               "properties": {
                   "classification": {"type": "string", "enum": sorted(CLASS_RULES)},
                   "draft_span": string,
                   "source_locators": {"type": "array", "items": string,
                                       "uniqueItems": True},
                   "condition_code": {"type": "string", "enum": sorted({condition
                       for rule in CLASS_RULES.values() for condition in rule["conditions"]})},
                   "owner": {"type": "string", "enum": sorted({owner for rule in
                       CLASS_RULES.values() for owner in rule["routes"]})},
                   "action_code": {"type": "string", "enum": sorted({action for rule in
                       CLASS_RULES.values() for action in rule["routes"].values()})}},
               "required": ["classification", "draft_span", "source_locators",
                            "condition_code", "owner", "action_code"]}
    return {"type": "object", "additionalProperties": False,
            "properties": {"schema": {"type": "integer", "enum": [SCHEMA]},
                           "task_sha256": string,
                           "verdict": {"type": "string", "enum": ["PASS", "BLOCK"]},
                           "findings": {"type": "array", "items": finding}},
            "required": ["schema", "task_sha256", "verdict", "findings"]}
