"""Pure RF-16 blind paired product-effect comparison contract."""
import hashlib
import json

SCHEMA = 1
INSTRUMENT = "blind-product-effect"
MODES = ("chapter", "whole_opening")
LABELS = ("A", "B")


class ContractError(RuntimeError):
    pass


def _unique(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ContractError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def _loads(raw):
    try:
        return json.loads(raw, object_pairs_hook=_unique)
    except ContractError:
        raise
    except (json.JSONDecodeError, TypeError, UnicodeError) as exc:
        raise ContractError(f"verdict is not one strict JSON object: {exc}") from exc


def _hash(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(raw.encode()).hexdigest()


def _text(value, label, limit=None):
    if not isinstance(value, str) or not value.strip() or "\x00" in value \
            or limit is not None and len(value) > limit:
        raise ContractError(f"{label} must be non-empty text" +
                            (f" of at most {limit} characters" if limit else ""))
    return value


def _make(mode, subject, candidate_a, candidate_b):
    if mode not in MODES:
        raise ContractError("unknown product-effect mode")
    candidates = {"A": {"chapters": list(candidate_a)},
                  "B": {"chapters": list(candidate_b)}}
    body = {"schema": SCHEMA, "instrument": INSTRUMENT, "mode": mode,
            "subject": subject, "fresh_context": True, "candidates": candidates}
    return validate_task({**body, "task_sha256": _hash(body)})


def chapter_pair(subject, candidate_a, candidate_b):
    """Build an ordinary anonymous A/B chapter task; no reference input exists."""
    return _make("chapter", subject, (candidate_a,), (candidate_b,))


def whole_opening(subject, candidate_a, candidate_b):
    """Build an ordinary anonymous A/B task from two ordered chapter sequences."""
    if not isinstance(candidate_a, (list, tuple)) or not isinstance(candidate_b, (list, tuple)):
        raise ContractError("whole openings must be ordered chapter sequences")
    return _make("whole_opening", subject, candidate_a, candidate_b)


def validate_task(value):
    keys = {"schema", "instrument", "mode", "subject", "fresh_context",
            "candidates", "task_sha256"}
    if not isinstance(value, dict) or set(value) != keys \
            or value.get("schema") != SCHEMA or value.get("instrument") != INSTRUMENT \
            or value.get("mode") not in MODES or value.get("fresh_context") is not True:
        raise ContractError("product-effect task fields are missing, unknown, or stale")
    _text(value["subject"], "subject", 120)
    candidates = value["candidates"]
    if not isinstance(candidates, dict) or tuple(candidates) != LABELS:
        raise ContractError("candidates must be anonymous A and B in fixed order")
    lengths = []
    for label in LABELS:
        candidate = candidates[label]
        if not isinstance(candidate, dict) or set(candidate) != {"chapters"} \
                or not isinstance(candidate["chapters"], list):
            raise ContractError(f"candidate {label} must contain only ordered chapters")
        for index, chapter in enumerate(candidate["chapters"], 1):
            _text(chapter, f"candidate {label} chapter {index}")
        lengths.append(len(candidate["chapters"]))
    if value["mode"] == "chapter" and lengths != [1, 1] \
            or value["mode"] == "whole_opening" and (lengths[0] < 2 or lengths[0] != lengths[1]):
        raise ContractError("candidate chapter counts do not match the declared mode")
    body = {key: item for key, item in value.items() if key != "task_sha256"}
    if value["task_sha256"] != _hash(body):
        raise ContractError("product-effect task identity is stale")
    return value


def h_f04_envelope(task, reference_candidate):
    """Keep reference identity outside the judge payload and disable downstream use."""
    envelope = {"schema": SCHEMA, "purpose": "h_f04_calibration", "isolated": True,
                "generation_eligible": False, "promotion_eligible": False,
                "reference_candidate": reference_candidate, "judge_task": validate_task(task)}
    return validate_h_f04(envelope)


def validate_h_f04(value):
    keys = {"schema", "purpose", "isolated", "generation_eligible",
            "promotion_eligible", "reference_candidate", "judge_task"}
    if not isinstance(value, dict) or set(value) != keys or value.get("schema") != SCHEMA \
            or value.get("purpose") != "h_f04_calibration" or value.get("isolated") is not True \
            or value.get("generation_eligible") is not False \
            or value.get("promotion_eligible") is not False \
            or value.get("reference_candidate") not in LABELS:
        raise ContractError("H-F04 envelope is not isolated and non-promotable")
    validate_task(value["judge_task"])
    return value


def h_f04_judge_task(envelope):
    """Return only the anonymous payload that a calibration evaluator may see."""
    return validate_h_f04(envelope)["judge_task"]


def verdict(raw, expected_task):
    task = validate_task(expected_task)
    value = _loads(raw)
    keys = {"schema", "task_sha256", "mode", "preferred", "confidence",
            "decisive_reason"}
    if not isinstance(value, dict) or set(value) != keys or value.get("schema") != SCHEMA \
            or value.get("task_sha256") != task["task_sha256"] \
            or value.get("mode") != task["mode"]:
        raise ContractError("product-effect verdict identity is missing or stale")
    if value["preferred"] not in ("A", "B", "TIE") \
            or value["confidence"] not in ("LOW", "MEDIUM", "HIGH"):
        raise ContractError("preference or confidence is invalid")
    _text(value["decisive_reason"], "decisive_reason", 400)
    return value


def output_schema():
    string = {"type": "string"}
    root = {"schema": {"type": "integer", "enum": [SCHEMA]},
            "task_sha256": string, "mode": {"type": "string", "enum": list(MODES)},
            "preferred": {"type": "string", "enum": ["A", "B", "TIE"]},
            "confidence": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH"]},
            "decisive_reason": string}
    return {"type": "object", "additionalProperties": False,
            "properties": root, "required": list(root)}
