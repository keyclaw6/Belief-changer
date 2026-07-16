"""Strict one-content product-effect task and observation contract."""
import re

import product_effect as COMMON

SCHEMA = 1
INSTRUMENT = "blind-product-effect-absolute"
MODES = COMMON.MODES
TEXT_FIELDS = ("entering_belief", "leaving_belief", "enacted_discovery")
RATING_FIELDS = ("subject_specificity", "mechanism_credibility", "emotion_relief",
                 "escalation", "continuity_handoff")
RATINGS = ("ABSENT", "PARTIAL", "CLEAR")
SEQUENCE_FIELDS = ("prior_insight", "felt_benefit", "reduced_sacrifice")
SUFFICIENCIES = ("MEETS", "DOES_NOT_MEET")
NOT_APPLICABLE = "NOT_APPLICABLE"
CONFIDENCES = ("LOW", "MEDIUM", "HIGH")
SCOPES = ("h_f04_absolute_calibration", "ordinary_product_absolute")
SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
HEX = re.compile(r"[0-9a-f]{64}")
ContractError = COMMON.ContractError
_hash = COMMON._hash
_loads = COMMON._loads


def _make(mode, subject, chapters):
    body = {"schema": SCHEMA, "instrument": INSTRUMENT, "mode": mode,
            "subject": subject, "fresh_context": True, "chapters": list(chapters)}
    return validate_task({**body, "task_sha256": _hash(body)})


def chapter(subject, content):
    return _make("chapter", subject, (content,))


def whole_opening(subject, chapters):
    if not isinstance(chapters, (list, tuple)):
        raise ContractError("whole opening must be an ordered chapter sequence")
    return _make("whole_opening", subject, chapters)


def validate_task(value):
    keys = {"schema", "instrument", "mode", "subject", "fresh_context",
            "chapters", "task_sha256"}
    if not isinstance(value, dict) or set(value) != keys \
            or value.get("schema") != SCHEMA or value.get("instrument") != INSTRUMENT \
            or value.get("mode") not in MODES or value.get("fresh_context") is not True:
        raise ContractError("absolute product-effect task fields are missing, unknown, or stale")
    COMMON._text(value["subject"], "subject", 120)
    chapters = value["chapters"]
    if not isinstance(chapters, list):
        raise ContractError("absolute task chapters must be an ordered list")
    for index, content in enumerate(chapters, 1):
        COMMON._text(content, f"chapter {index}")
    if value["mode"] == "chapter" and len(chapters) != 1 \
            or value["mode"] == "whole_opening" and len(chapters) < 2:
        raise ContractError("absolute task chapter count does not match its mode")
    body = {key: item for key, item in value.items() if key != "task_sha256"}
    if value["task_sha256"] != _hash(body):
        raise ContractError("absolute product-effect task identity is stale")
    return value


def envelope(task, content_id, tested_pair_hash=None, *, calibration=False):
    """Bind stable identity outside the one-content judge payload."""
    task = validate_task(task)
    if not isinstance(content_id, str) or not SAFE_ID.fullmatch(content_id):
        raise ContractError("content ID must be safe and stable")
    if calibration:
        scope, eligible, tested_pair_hash = SCOPES[0], False, None
    elif not isinstance(tested_pair_hash, str) or not HEX.fullmatch(tested_pair_hash):
        raise ContractError("ordinary absolute task requires a sealed tested-pair hash")
    else:
        scope, eligible = SCOPES[1], True
    body = {"schema": SCHEMA, "scope": scope, "promotion_eligible": eligible,
            "content_id": content_id, "content_sha256": _hash(task["chapters"]),
            "tested_pair_hash": tested_pair_hash, "judge_task": task}
    return validate_envelope({**body, "envelope_sha256": _hash(body)})


def validate_envelope(value):
    keys = {"schema", "scope", "promotion_eligible", "content_id",
            "content_sha256", "tested_pair_hash", "judge_task", "envelope_sha256"}
    if not isinstance(value, dict) or set(value) != keys or value.get("schema") != SCHEMA \
            or value.get("scope") not in SCOPES \
            or not isinstance(value.get("content_id"), str) \
            or not SAFE_ID.fullmatch(value["content_id"]):
        raise ContractError("absolute envelope fields are missing, unknown, or stale")
    task = validate_task(value["judge_task"])
    calibration = value["scope"] == SCOPES[0]
    if calibration and (value.get("promotion_eligible") is not False
                        or value.get("tested_pair_hash") is not None) \
            or not calibration and (value.get("promotion_eligible") is not True
                                    or not isinstance(value.get("tested_pair_hash"), str)
                                    or not HEX.fullmatch(value["tested_pair_hash"])):
        raise ContractError("absolute envelope scope binding is invalid")
    if value.get("content_sha256") != _hash(task["chapters"]):
        raise ContractError("absolute content hash is stale")
    body = {key: item for key, item in value.items() if key != "envelope_sha256"}
    if value.get("envelope_sha256") != _hash(body):
        raise ContractError("absolute envelope identity is stale")
    return value


def judge_task(value):
    return validate_envelope(value)["judge_task"]


def _observation(value, mode):
    fields = set(TEXT_FIELDS + RATING_FIELDS + (
        "construct_sufficiency", "construct_reason", "opening_sequence"))
    if not isinstance(value, dict) or set(value) != fields:
        raise ContractError("absolute observation fields are not exact")
    for field in TEXT_FIELDS:
        COMMON._text(value[field], field, 200)
    COMMON._text(value["construct_reason"], "construct_reason", 200)
    if any(value[field] not in RATINGS for field in RATING_FIELDS):
        raise ContractError("absolute categorical rating is invalid")
    if value["construct_sufficiency"] not in SUFFICIENCIES:
        raise ContractError("absolute construct sufficiency is invalid")
    sequence = value["opening_sequence"]
    if not isinstance(sequence, dict) or set(sequence) != set(SEQUENCE_FIELDS):
        raise ContractError("absolute opening-sequence fields are not exact")
    links = tuple(sequence[field] for field in SEQUENCE_FIELDS)
    unresolved = (value["entering_belief"].strip() == "UNRESOLVED"
                  or value["leaving_belief"].strip() == "UNRESOLVED"
                  or value["enacted_discovery"].strip() == "NOT_ENACTED")
    if value["construct_sufficiency"] == "MEETS" and unresolved:
        raise ContractError("content cannot meet with unresolved belief work")
    if mode == "chapter":
        if any(link != NOT_APPLICABLE for link in links):
            raise ContractError("chapter opening sequence must be not applicable")
    else:
        if any(link not in RATINGS for link in links):
            raise ContractError("whole-opening sequence rating is invalid")
        if links[1] == "CLEAR" and links[0] == "ABSENT" \
                or links[2] == "CLEAR" and "ABSENT" in links[:2]:
            raise ContractError("downstream sequence links require clear prerequisites")
        if (value["construct_sufficiency"] == "MEETS") != all(
                link == "CLEAR" for link in links):
            raise ContractError("whole-opening sufficiency contradicts its sequence")
    return value


def verdict(raw, expected_task):
    task = validate_task(expected_task)
    value = _loads(raw)
    keys = {"schema", "task_sha256", "mode", "observation", "confidence"}
    if not isinstance(value, dict) or set(value) != keys or value.get("schema") != SCHEMA \
            or value.get("task_sha256") != task["task_sha256"] \
            or value.get("mode") != task["mode"]:
        raise ContractError("absolute product-effect verdict identity is missing or stale")
    _observation(value["observation"], task["mode"])
    if value["confidence"] not in CONFIDENCES:
        raise ContractError("absolute confidence is invalid")
    return value


def output_schema():
    bounded = {"type": "string", "minLength": 1, "maxLength": 200}
    fields = {field: bounded for field in TEXT_FIELDS}
    fields.update({field: {"type": "string", "enum": list(RATINGS)}
                   for field in RATING_FIELDS})
    fields.update({
        "construct_sufficiency": {"type": "string", "enum": list(SUFFICIENCIES)},
        "construct_reason": bounded,
        "opening_sequence": {"type": "object", "additionalProperties": False,
            "properties": {field: {"type": "string",
                "enum": list(RATINGS) + [NOT_APPLICABLE]}
                for field in SEQUENCE_FIELDS}, "required": list(SEQUENCE_FIELDS)},
    })
    root = {
        "schema": {"type": "integer", "enum": [SCHEMA]},
        "task_sha256": {"type": "string"},
        "mode": {"type": "string", "enum": list(MODES)},
        "observation": {"type": "object", "additionalProperties": False,
                        "properties": fields, "required": list(fields)},
        "confidence": {"type": "string", "enum": list(CONFIDENCES)},
    }
    return {"type": "object", "additionalProperties": False,
            "properties": root, "required": list(root)}
