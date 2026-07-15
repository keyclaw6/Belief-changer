"""Strict RF-13 whole-sequence task and verdict contract."""
import json
import re

import master_plan_contract_context as MPC
import pair_store as PS

SCHEMA = 1
PROMPT = "prompts/developmental-reviewer.md"
FOLDER = "developmental-review"
RECEIPT = "receipt.json"
MAX_FINDINGS = 6
RULES = (
    "judge the complete canonical sequence, never chapter-local checklist scores",
    "use only exact reader-state cards, commissions, and frozen first drafts",
    "review transitions, specificity, emotion, variation, continuity, and deferral",
    "do not re-audit truth, safety, originality, or reference likeness",
    "route a newly detected truth or safety need only to grounded review",
    "route every other defect to its earliest framing, plan, commission/context, or prose owner",
)
CATEGORIES = {
    "failed_planned_transition": {"transition_not_enacted", "leaving_state_not_earned"},
    "specificity_concreteness": {"sequence_remains_generic", "encounters_do_not_accumulate"},
    "emotional_movement_authority": {"emotional_curve_flat", "authority_does_not_build"},
    "mode_scene_argument_variation": {"adjacent_mode_repetition", "scene_argument_pattern_repeats"},
    "cumulative_continuity_handoff": {"handoff_not_used", "sequence_resets_reader_state"},
    "deferred_transformation_repetition": {
        "transformation_deferred", "catalogue_replaces_discovery",
        "sequence_repeats_without_progress"},
    "newly_detected_grounded_need": {"new_truth_need", "new_safety_need"},
}
ROUTES = {
    "journey_definition_conflict": ("framing", "repair_reader_journey"),
    "card_sequence_defect": ("plan", "repair_sequence_cards"),
    "commission_transport_defect": ("commission/context", "repair_sequence_transport"),
    "draft_execution_defect": ("prose", "repair_sequence_execution"),
    "new_truth_safety_need": ("evaluation", "escalate_new_truth_safety_need"),
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
    values = {key: cfg.get(f"developmental_reviewer_{key}") for key in keys}
    if not all(isinstance(value, str) and value.strip() for value in values.values()):
        raise ContractError("developmental reviewer model metadata is incomplete")
    if values["route"].casefold() != "codex-native" or values["reasoning"].casefold() != "max":
        raise ContractError("developmental reviewer must use native Codex at max reasoning")
    other = []
    for role in ("writer", "grounded_reviewer"):
        other_model = str(cfg.get(f"{role}_model", "")).strip()
        family = str(cfg.get(f"{role}_family") or other_model.split("/", 1)[0]).strip()
        if not other_model or not family:
            raise ContractError(f"{role} model/family provenance is missing")
        other.append((other_model.casefold(), family.casefold()))
    if any(values["model"].casefold() == item[0] or
           values["family"].casefold() == item[1] for item in other):
        raise ContractError("developmental reviewer must differ from writer and grounded families")
    return values


def card_transition(chapter_id, card):
    fields = {}
    for name, value in MPC.FIELD.findall(card):
        if name in fields:
            raise ContractError(f"{chapter_id}: duplicate reader-state field {name}")
        fields[name] = value.strip()
    try:
        entering = fields["Entering belief"]
        leaving = fields["Leaving belief"]
        enter_id = MPC.state(entering, f"{chapter_id}.Entering belief")[0]
        leave_id = MPC.state(leaving, f"{chapter_id}.Leaving belief")[0]
    except (KeyError, MPC.ContractError) as exc:
        raise ContractError(f"{chapter_id}: reader-state card is malformed: {exc}") from exc
    return {"chapter_id": chapter_id,
            "transition_id": f"{chapter_id}:{enter_id}->{leave_id}",
            "entering_state": entering, "leaving_state": leaving}


def make_task(identity, reviewer, prompt, chapters):
    context = {"prompt": prompt, "review_rules": list(RULES), "chapters": chapters}
    body = {"schema": SCHEMA, **identity, "fresh_context": True,
            "reviewer": reviewer, "context": context}
    return {**body, "task_sha256": PS.state_hash(body)}


def task(value):
    keys = {"schema", "operation", "generation", "config", "selection",
            "fresh_context", "reviewer", "context", "task_sha256"}
    if not isinstance(value, dict) or set(value) != keys or value.get("schema") != SCHEMA:
        raise ContractError("developmental task fields are missing or unknown")
    body = {key: item for key, item in value.items() if key != "task_sha256"}
    if value.get("task_sha256") != PS.state_hash(body) or value.get("fresh_context") is not True:
        raise ContractError("developmental task identity is stale or malformed")
    selection, context = value.get("selection"), value.get("context")
    if not isinstance(selection, list) or selection != sorted(set(selection)) or not selection \
            or not isinstance(context, dict) \
            or set(context) != {"prompt", "review_rules", "chapters"} \
            or context["review_rules"] != list(RULES):
        raise ContractError("developmental task selection or context is malformed")
    chapters = context["chapters"]
    if not isinstance(chapters, list) or [item.get("number") for item in chapters
                                          if isinstance(item, dict)] != selection:
        raise ContractError("developmental chapters are partial or out of order")
    expected_keys = {"number", "chapter_id", "transition_id", "entering_state",
                     "leaving_state", "reader_state_card", "commission", "frozen_draft"}
    for number, chapter in zip(selection, chapters):
        if set(chapter) != expected_keys or chapter["chapter_id"] != f"C-{number:02d}" \
                or not all(isinstance(chapter[key], str) and chapter[key]
                           for key in ("reader_state_card", "commission", "frozen_draft")):
            raise ContractError("developmental chapter input is malformed")
        transition = card_transition(chapter["chapter_id"], chapter["reader_state_card"])
        if any(chapter[key] != transition[key] for key in
               ("transition_id", "entering_state", "leaving_state")):
            raise ContractError("developmental reader-state binding differs")
    return value


def _finding(value, expected_task):
    keys = {"category", "symptom_code", "chapters", "expected_transitions",
            "evidence", "ownership_basis", "owner", "action_code"}
    if not isinstance(value, dict) or set(value) != keys:
        raise ContractError("developmental finding fields are missing or unknown")
    category, symptom = value["category"], value["symptom_code"]
    if category not in CATEGORIES or symptom not in CATEGORIES[category]:
        raise ContractError("developmental finding category or symptom is invalid")
    route = ROUTES.get(value["ownership_basis"])
    if route != (value["owner"], value["action_code"]):
        raise ContractError("developmental finding owner route is invalid")
    grounded = value["ownership_basis"] == "new_truth_safety_need"
    if grounded != (category == "newly_detected_grounded_need"):
        raise ContractError("grounded escalation is not limited to a new truth/safety need")
    chapter_map = {item["chapter_id"]: item for item in expected_task["context"]["chapters"]}
    chapters = value["chapters"]
    if not isinstance(chapters, list) or not chapters or len(chapters) > len(chapter_map) \
            or chapters != sorted(set(chapters)) or any(item not in chapter_map for item in chapters):
        raise ContractError("developmental finding chapters are invalid")
    wanted = [{key: chapter_map[chapter][key] for key in
               ("chapter_id", "transition_id", "entering_state", "leaving_state")}
              for chapter in chapters]
    if value["expected_transitions"] != wanted:
        raise ContractError("developmental expected transition is stale or invented")
    spans = value["evidence"]
    if not isinstance(spans, list) or [item.get("chapter_id") for item in spans
                                       if isinstance(item, dict)] != chapters:
        raise ContractError("developmental finding requires evidence for every chapter")
    for span in spans:
        if not isinstance(span, dict) or set(span) != {"chapter_id", "span"} \
                or span["chapter_id"] not in chapters or not isinstance(span["span"], str) \
                or not 8 <= len(span["span"]) <= 240 \
                or len([word for word in re.findall(r"\w+", span["span"])
                        if any(char.isalnum() for char in word)]) < 2 \
                or span["span"] != span["span"].strip() \
                or span["span"] not in chapter_map[span["chapter_id"]]["frozen_draft"]:
            raise ContractError("developmental observed span is not exact")


def verdict(raw, expected_task):
    value = loads(raw, "developmental verdict")
    keys = {"schema", "task_sha256", "verdict", "findings"}
    if not isinstance(value, dict) or set(value) != keys or value.get("schema") != SCHEMA \
            or value.get("task_sha256") != expected_task["task_sha256"]:
        raise ContractError("developmental verdict identity is missing or stale")
    findings = value["findings"]
    if value["verdict"] not in ("PASS", "NEEDS_CHANGES") or not isinstance(findings, list) \
            or value["verdict"] == "PASS" and findings \
            or value["verdict"] == "NEEDS_CHANGES" and not 1 <= len(findings) <= MAX_FINDINGS:
        raise ContractError("developmental verdict must be compact PASS or NEEDS_CHANGES")
    fingerprints = set()
    for finding in findings:
        _finding(finding, expected_task)
        fingerprint = PS.state_hash({key: finding[key] for key in
            ("category", "symptom_code", "chapters", "ownership_basis")})
        if fingerprint in fingerprints:
            raise ContractError("developmental findings contain a duplicate semantic defect")
        fingerprints.add(fingerprint)
    return value


def output_schema():
    string = {"type": "string"}
    transition = {"type": "object", "additionalProperties": False,
                  "properties": {key: string for key in
                                 ("chapter_id", "transition_id", "entering_state", "leaving_state")},
                  "required": ["chapter_id", "transition_id", "entering_state", "leaving_state"]}
    span = {"type": "object", "additionalProperties": False,
            "properties": {"chapter_id": string, "span": string},
            "required": ["chapter_id", "span"]}
    finding = {"type": "object", "additionalProperties": False,
               "properties": {
                   "category": {"type": "string", "enum": sorted(CATEGORIES)},
                   "symptom_code": {"type": "string", "enum": sorted(
                       {item for values in CATEGORIES.values() for item in values})},
                   "chapters": {"type": "array", "items": string, "uniqueItems": True},
                   "expected_transitions": {"type": "array", "items": transition},
                   "evidence": {"type": "array", "items": span, "minItems": 1,
                                "uniqueItems": True},
                   "ownership_basis": {"type": "string", "enum": sorted(ROUTES)},
                   "owner": {"type": "string", "enum": sorted({item[0] for item in ROUTES.values()})},
                   "action_code": {"type": "string", "enum": sorted({item[1] for item in ROUTES.values()})}},
               "required": ["category", "symptom_code", "chapters", "expected_transitions",
                            "evidence", "ownership_basis", "owner", "action_code"]}
    return {"type": "object", "additionalProperties": False,
            "properties": {"schema": {"type": "integer", "enum": [SCHEMA]},
                           "task_sha256": string,
                           "verdict": {"type": "string", "enum": ["PASS", "NEEDS_CHANGES"]},
                           "findings": {"type": "array", "items": finding,
                                        "maxItems": MAX_FINDINGS}},
            "required": ["schema", "task_sha256", "verdict", "findings"]}
