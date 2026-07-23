"""Durable native Carr diagnostics for the sealed H-F01 treatment opening."""
import datetime as dt, json, os, sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path[:0] = [str(HERE.parent), str(HERE.parents[1] / "eval")]
import judges  # noqa: E402
import native_judge as NATIVE  # noqa: E402
import pair_store as PS  # noqa: E402
import path_guard as PG  # noqa: E402
import hf01_preflight as HF  # noqa: E402
import immutable_file as IF  # noqa: E402

FOLDER = "loop/experiments/h-f01-treatment/evidence/hf01/carr-native"
OWNERS = sorted(judges.OWNERS)
FIELDS = {"schema", "id", "authority_sha256", "blind_receipt_sha256", "tested_pair_hash",
    "task_sha256", "input_sha256", "output_sha256", "actor", "model", "route",
    "reasoning", "command", "thread_id", "started_at_utc", "completed_at_utc", "raw"}

class CarrError(RuntimeError): pass
class CarrPending(CarrError):
    def __init__(self, path): self.path = path; super().__init__(f"native Carr evidence is missing: {path}")

def _object(properties):
    return {"type": "object", "properties": properties,
            "required": list(properties), "additionalProperties": False}
def output_schema():
    text, score = {"type": "string"}, {"type": "number", "minimum": 0, "maximum": 10}
    return _object({"pair_hash": text, "task_hash": text,
        "scores": _object({name: score for name in judges.DIMS}),
        "evidence": _object({name: text for name in judges.DIMS}),
        "worst_dimension": {"type": "string", "enum": list(judges.DIMS)},
        "gap_summary": text, "suggestions": {"type": "array", "minItems": 3,
            "maxItems": 5, "items": _object({"suggestion": text,
                "owner": {"type": "string", "enum": OWNERS}})}})
def _now(): return dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds")
def _time(value):
    try: parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc: raise CarrError("Carr timestamp is invalid") from exc
    if parsed.utcoffset() != dt.timedelta(0): raise CarrError("Carr timestamp is not UTC")
    return parsed
def _read(path):
    try: return PG.safe_file(path, path.parent).read_bytes()
    except (PG.PathError, OSError) as exc: raise CarrError(str(exc)) from exc
def _write(path, data):
    path = Path(path)
    try:
        PG.ensure_dir(path.parent)
        IF.write_once(path, data, _read, "Carr evidence")
    except (PG.PathError, IF.ImmutableFileError) as exc: raise CarrError(f"Carr evidence write failed: {exc}") from exc
def _raw(raw, pair_hash, task_hash):
    try: value = json.loads(raw)
    except (TypeError, json.JSONDecodeError) as exc: raise CarrError("Carr output is not strict JSON") from exc
    expected = {"pair_hash", "task_hash", "scores", "evidence", "worst_dimension",
                "gap_summary", "suggestions"}
    if not isinstance(value, dict) or set(value) != expected \
            or (value.get("pair_hash"), value.get("task_hash")) != (pair_hash, task_hash):
        raise CarrError("Carr output binding or fields are invalid")
    scores, evidence, suggestions = value["scores"], value["evidence"], value["suggestions"]
    if set(scores) != set(judges.DIMS) or set(evidence) != set(judges.DIMS) \
            or any(isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 10
                   for score in scores.values()) \
            or any(not isinstance(item, str) or not item.strip() for item in evidence.values()) \
            or value["worst_dimension"] not in judges.DIMS or not str(value["gap_summary"]).strip() \
            or not isinstance(suggestions, list) or not 3 <= len(suggestions) <= 5 \
            or any(not isinstance(item, dict) or set(item) != {"suggestion", "owner"}
                   or not str(item["suggestion"]).strip() or item["owner"] not in judges.OWNERS
                   for item in suggestions):
        raise CarrError("Carr output does not satisfy the frozen rubric schema")
    return value
def _expected(cfg, stem, pair_hash, authority_sha, blind_sha, task_path):
    try: task_hash = judges._task_binding(task_path, pair_hash)
    except SystemExit as exc: raise CarrError(str(exc)) from exc
    task_bytes = _read(task_path); model, reasoning = cfg["judge_model"], cfg["judge_reasoning"]
    return {"id": stem, "authority_sha256": authority_sha,
        "blind_receipt_sha256": blind_sha, "tested_pair_hash": pair_hash,
        "task_sha256": task_hash, "input_sha256": PS.sha(task_bytes),
        "actor": f"hf01-carr-{stem}", "model": model,
        "route": cfg["judge_route"], "reasoning": reasoning,
        "command": NATIVE.command("<isolated-tmp>", "<isolated-tmp>/judge-output-schema.json",
                                  model, reasoning)}, task_bytes
def _one(base, cfg, stem, pair_hash, authority_sha, blind_sha, task_path, verdict_path, complete, repair):
    expected, task_bytes = _expected(cfg, stem, pair_hash, authority_sha, blind_sha, task_path)
    marker, result = base / "tasks" / f"{stem}.json", base / "calls" / f"{stem}.json"
    marker_bytes = PS.json_bytes({"schema": 1, **expected})
    if result.is_file():
        if not marker.is_file() or _read(marker) != marker_bytes: raise CarrError(f"{stem}: Carr task marker is stale")
        try: value = json.loads(_read(result))
        except (json.JSONDecodeError, TypeError) as exc: raise CarrError(f"{stem}: Carr record is malformed") from exc
        if set(value) != FIELDS or value.get("schema") != 1 \
                or any(value.get(key) != item for key, item in expected.items()) \
                or value.get("output_sha256") != PS.sha(str(value.get("raw", "")).encode()) \
                or not value.get("thread_id"):
            raise CarrError(f"{stem}: Carr record binding is stale")
        _raw(value["raw"], pair_hash, expected["task_sha256"])
        if repair: _write(verdict_path, value["raw"].encode())
        elif not verdict_path.is_file() or _read(verdict_path) != value["raw"].encode():
            raise CarrError(f"{stem}: Carr verdict materialization is stale")
        return value
    if marker.exists(): raise CarrError(f"{stem}: Carr call outcome is ambiguous; do not replay")
    if verdict_path.exists(): raise CarrError(f"{stem}: Carr verdict lacks its durable native record; do not replay")
    if complete is None: raise CarrPending(result)
    _write(marker, marker_bytes); started = _now()
    try: content = task_bytes.decode()
    except UnicodeError as exc: raise CarrError(f"{stem}: Carr task is not UTF-8") from exc
    raw, transport, error = complete(content, expected["actor"], output_schema(),
        model=expected["model"], reasoning=expected["reasoning"])
    if error: raise CarrError(f"{stem}: {error}")
    if (transport.get("model"), transport.get("reasoning_effort"), transport.get("command")) != \
            (expected["model"], expected["reasoning"], expected["command"]) \
            or not transport.get("thread_id"):
        raise CarrError(f"{stem}: Carr native transport identity is stale")
    _raw(raw, pair_hash, expected["task_sha256"])
    value = {"schema": 1, **expected, "output_sha256": PS.sha(raw.encode()),
        "thread_id": transport["thread_id"], "started_at_utc": started,
        "completed_at_utc": _now(), "raw": raw}
    _write(result, PS.json_bytes(value)); _write(verdict_path, raw.encode()); return value
def _pipeline(root, cfg, labels, iteration, pair_hash, blind, complete, repair):
    if len(labels) != 3 or int(cfg.get("judge_k", 0)) != 2: raise CarrError("H-F01 requires three chapters and two Carr judges")
    base, task_root = Path(root).absolute() / FOLDER, judges.judging_dir(cfg, iteration)
    blind_sha, authority_sha, records = PS.sha(PS.json_bytes(blind)), blind.get("authority_sha256"), []
    if not isinstance(authority_sha, str) or len(authority_sha) != 64: raise CarrError("Carr authority binding is invalid")
    for stem in judges._stems(labels, 2):
        records.append(_one(base, cfg, stem, pair_hash, authority_sha, blind_sha,
            task_root / "tasks" / f"{stem}.md", task_root / "verdicts" / f"{stem}.json",
            complete, repair))
    if len({row["thread_id"] for row in records}) != 6: raise CarrError("Carr diagnostics require six fresh native contexts")
    previous = _time(blind["frozen_at_utc"])
    for row in records:
        started, completed = _time(row["started_at_utc"]), _time(row["completed_at_utc"])
        if not previous <= started <= completed: raise CarrError("Carr call chronology is stale")
        previous = completed
    calls = [{key: row[key] for key in FIELDS - {"schema", "raw"}} for row in records]
    body = {"schema": 1, "authority_sha256": authority_sha, "blind_receipt_sha256": blind_sha,
            "tested_pair_hash": pair_hash, "calls": calls}
    return {**body, "receipt_hash": PS.state_hash(body)}
def dispatch(root, cfg, labels, iteration, pair_hash, blind, complete=NATIVE.complete):
    HF.require_authorized_root(root)
    return _pipeline(root, cfg, labels, iteration, pair_hash, blind, complete, True)
def verify(root, cfg, labels, iteration, pair_hash, blind):
    HF.require_authorized_root(root)
    return _pipeline(root, cfg, labels, iteration, pair_hash, blind, None, False)
