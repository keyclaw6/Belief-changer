"""Bound RF-13 operation evidence and isolated-runtime result import."""
import base64
import os
import stat
import sys
from pathlib import Path

import developmental_review_contract as C
import developmental_review_runtime as R
import pair_store as PS

SCHEMA = 2
PROVIDER = "openai-codex-subscription"


class CallError(RuntimeError):
    pass


def folder(root):
    return Path(root).absolute() / "evidence" / C.FOLDER


def task_path(root):
    return folder(root) / "task.json"


def schema_path(root):
    return folder(root) / "schema.json"


def marker_path(root):
    return folder(root) / "call.json"


def transport_path(root):
    return folder(root) / "transport.json"


def raw_path(root):
    return folder(root) / "verdict.raw.json"


def _mode(path, wanted, label):
    info = os.lstat(path)
    if os.name == "nt":
        if wanted == 0o444 and not (getattr(info, "st_file_attributes", 0)
                                    & getattr(stat, "FILE_ATTRIBUTE_READONLY", 0)):
            raise CallError(f"{label} is writable")
        return
    if stat.S_IMODE(info.st_mode) != wanted:
        raise CallError(f"{label} mode is not canonical {wanted:04o}")


def _write_once(path, data, label, interrupt=None):
    if os.path.lexists(path):
        try:
            if PS._safe_file(path, path.parent).read_bytes() != data:
                raise CallError(f"{label} already differs")
            _mode(path, 0o444, label)
            return
        except PS.StoreError as exc:
            raise CallError(f"{label} is unsafe: {exc}") from exc
    PS.write(path, data, interrupt)
    path.chmod(0o444)


def _ensure_folder(root):
    target, evidence = folder(root), Path(root).absolute() / "evidence"
    try:
        PS.safe_dir(evidence, root)
        if not os.path.lexists(target):
            target.mkdir(mode=0o700)
        PS.safe_dir(target, evidence)
        if os.name != "nt" and stat.S_IMODE(os.lstat(target).st_mode) not in (0o700, 0o555):
            raise CallError("developmental operation folder mode is invalid")
        return target
    except (PS.StoreError, OSError) as exc:
        raise CallError(f"developmental operation folder is unsafe: {exc}") from exc


def expected_marker(task):
    spec = R.command_spec(task)
    body = {"schema": SCHEMA, "task_sha256": task["task_sha256"],
            "task_file_sha256": PS.sha(PS.json_bytes(task)),
            "output_schema_sha256": PS.sha(PS.json_bytes(C.output_schema())),
            "input_sha256": PS.sha(R.input_bytes(task)), "provider": PROVIDER,
            "route": task["reviewer"]["route"], "model": task["reviewer"]["model"],
            "family": task["reviewer"]["family"],
            "reasoning": task["reviewer"]["reasoning"],
            "runtime_id": task["task_sha256"], "command": spec,
            "command_sha256": PS.state_hash(spec)}
    return {**body, "call_id": PS.state_hash(body)}


def binding(task):
    marker = expected_marker(task)
    return {"task_sha256": task["task_sha256"],
            "task_file_sha256": marker["task_file_sha256"],
            "schema_sha256": marker["output_schema_sha256"],
            "call_id": marker["call_id"],
            "call_sha256": PS.sha(PS.json_bytes(marker))}


def prepare_local(root, task):
    target = _ensure_folder(root)
    if os.name != "nt" and stat.S_IMODE(os.lstat(target).st_mode) == 0o555:
        raise CallError("committed developmental operation cannot be rewritten")
    _write_once(task_path(root), PS.json_bytes(task), "developmental task")
    _write_once(schema_path(root), PS.json_bytes(C.output_schema()),
                "developmental schema")
    validate_local(root, task, {"task.json", "schema.json"}, allow_more=True)


def validate_local(root, task, required, allow_more=False):
    target = _ensure_folder(root)
    allowed = {"task.json", "schema.json", "call.json", "transport.json",
               "verdict.raw.json", C.RECEIPT}
    try:
        found = {path.name for path in PS.tree_files(target, Path(root).absolute() / "evidence")}
        if not required <= found or found - allowed or not allow_more and found != required:
            raise CallError("developmental operation evidence inventory differs")
        task_data = PS._safe_file(task_path(root), target).read_bytes()
        schema_data = PS._safe_file(schema_path(root), target).read_bytes()
        if task_data != PS.json_bytes(task) or schema_data != PS.json_bytes(C.output_schema()):
            raise CallError("developmental task or schema differs")
        for name in found:
            _mode(target / name, 0o444, f"developmental {name}")
        return found
    except (PS.StoreError, OSError) as exc:
        raise CallError(f"developmental operation evidence is unsafe: {exc}") from exc


def _read_json(path, root, label):
    try:
        data = PS._safe_file(path, folder(root)).read_bytes()
        value = C.loads(data.decode("utf-8"), label)
        _mode(path, 0o444, label)
        return data, value
    except (PS.StoreError, OSError, UnicodeError, C.ContractError) as exc:
        raise CallError(f"{label} is invalid: {exc}") from exc


def start(root, task):
    prepare_local(root, task)
    try:
        R.prepare(task)
    except R.RuntimeError as exc:
        raise CallError(str(exc)) from exc
    wanted, path = expected_marker(task), marker_path(root)
    data = PS.json_bytes(wanted)
    if os.path.lexists(path):
        actual_data, actual = _read_json(path, root, "developmental call marker")
        if actual != wanted or actual_data != data:
            raise CallError("developmental call marker identity differs")
        return False, wanted
    _write_once(path, data, "developmental call marker")
    validate_local(root, task, {"task.json", "schema.json", "call.json"}, True)
    return True, wanted


def wrapper_command(task):
    script = Path(__file__).resolve().parents[1] / "eval" / "native_developmental_review.py"
    return [sys.executable or "python3", str(script),
            "--task-sha256", task["task_sha256"]]


def _proven(task, value):
    marker = expected_marker(task)
    keys = {"schema", "call_id", "task_sha256", "provider", "route", "model",
            "family", "reasoning", "command_sha256", "exit_code", "thread_id",
            "usage", "tool_event_count", "raw_sha256", "raw_b64"}
    if not isinstance(value, dict) or set(value) != keys or value.get("schema") != SCHEMA:
        raise CallError("developmental runtime result fields differ")
    identity = {key: marker[key] for key in
                ("call_id", "task_sha256", "provider", "route", "model", "family",
                 "reasoning", "command_sha256")}
    if any(value.get(key) != item for key, item in identity.items()) \
            or value.get("exit_code") != 0 or value.get("tool_event_count") != 0 \
            or not isinstance(value.get("thread_id"), str) or not value["thread_id"].strip() \
            or not isinstance(value.get("usage"), dict):
        raise CallError("developmental runtime result lacks zero-tool native proof")
    try:
        raw = base64.b64decode(value["raw_b64"], validate=True).decode("utf-8")
    except (ValueError, TypeError, UnicodeError) as exc:
        raise CallError(f"developmental runtime raw result is malformed: {exc}") from exc
    if value["raw_sha256"] != PS.sha(raw.encode("utf-8")):
        raise CallError("developmental runtime raw hash differs")
    C.verdict(raw, task)
    return raw


def import_result(root, task, interrupt=None):
    try:
        value = R.result(task)
    except R.RuntimeError as exc:
        raise CallError(str(exc)) from exc
    if value is None:
        raise CallError("developmental native result is pending")
    raw = _proven(task, value)
    boundary = interrupt or (lambda _step: None)
    _write_once(transport_path(root), PS.json_bytes(value), "developmental transport", boundary)
    boundary("transport-persisted")
    _write_once(raw_path(root), raw.encode("utf-8"), "developmental raw verdict", boundary)
    boundary("raw-persisted")
    return value


def read(root, task):
    marker_data, marker = _read_json(marker_path(root), root, "developmental call marker")
    if marker != expected_marker(task) or marker_data != PS.json_bytes(marker):
        raise CallError("developmental call marker identity differs")
    if not os.path.lexists(transport_path(root)):
        if os.path.lexists(raw_path(root)):
            raise CallError("raw verdict exists without proven native transport")
        raise CallError("marked developmental review has no durable transport; replay is ambiguous")
    transport_data, transport = _read_json(
        transport_path(root), root, "developmental transport")
    raw = _proven(task, transport)
    if not os.path.lexists(raw_path(root)):
        _write_once(raw_path(root), raw.encode("utf-8"), "developmental raw verdict")
    elif PS._safe_file(raw_path(root), folder(root)).read_text(encoding="utf-8") != raw:
        raise CallError("developmental raw verdict differs from proven transport")
    _mode(raw_path(root), 0o444, "developmental raw verdict")
    return raw, transport, {"task_file_sha256": marker["task_file_sha256"],
        "schema_sha256": marker["output_schema_sha256"], "call_sha256": PS.sha(marker_data),
        "transport_sha256": PS.sha(transport_data), "raw_sha256": PS.sha(raw.encode("utf-8"))}
