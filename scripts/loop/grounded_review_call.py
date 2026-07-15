"""Durable RF-12 native-call markers, task-only workdirs, and transport proof."""
import base64
import os
import stat
import sys
from pathlib import Path

import grounded_review_contract as C
import pair_store as PS

SCHEMA = 1
PROVIDER = "openai-codex-subscription"


class CallError(RuntimeError):
    pass


def folder(root):
    return Path(root).absolute() / "evidence" / C.FOLDER


def work_root(root):
    return folder(root) / "work"


def workdir(root, number):
    return work_root(root) / f"chapter-{number:02d}"


def task_path(root, number):
    return workdir(root, number) / "task.json"


def schema_path(root, number):
    return workdir(root, number) / "schema.json"


def marker_path(root, number):
    return folder(root) / f"call-{number:02d}.json"


def transport_path(root, number):
    return folder(root) / f"transport-{number:02d}.json"


def raw_path(root, number):
    return folder(root) / f"verdict-{number:02d}.raw.json"


def input_text(task):
    visible = {key: value for key, value in task.items() if key != "context"}
    visible["context"] = {key: value for key, value in task["context"].items()
                          if key != "prompt"}
    return (task["context"]["prompt"] + "\n\n===== CAPTURED REVIEW INPUT =====\n" +
            PS.json_bytes(visible).decode("utf-8"))


def codex_command(task, target_workdir, target_schema):
    reviewer = task["reviewer"]
    return ["codex", "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
            "--disable", "multi_agent", "--model", reviewer["model"], "-c",
            f"model_reasoning_effort={reviewer['reasoning']}", "--sandbox", "read-only",
            "--skip-git-repo-check", "--cd", str(target_workdir), "--output-schema",
            str(target_schema), "--json", "-"]


def _mode(path, wanted, label):
    if stat.S_IMODE(os.lstat(path).st_mode) != wanted:
        raise CallError(f"{label} mode is not canonical {wanted:04o}")


def _write_once(path, data, boundary, label):
    if os.path.lexists(path):
        if PS._safe_file(path, path.parent).read_bytes() != data:
            raise CallError(f"{label} already differs")
        _mode(path, 0o444, label)
        return
    PS.write(path, data, boundary)
    path.chmod(0o444)


def prepare_workdirs(root, tasks):
    target, workspace = folder(root), work_root(root)
    try:
        if not os.path.lexists(target):
            evidence = Path(root).absolute() / "evidence"
            PS.safe_dir(evidence, root)
            target.mkdir()
        PS.safe_dir(target, Path(root).absolute() / "evidence")
        if not os.path.lexists(workspace):
            workspace.mkdir()
        PS.safe_dir(workspace, target)
        expected_dirs = {f"chapter-{number:02d}" for number in tasks}
        if {path.name for path in workspace.iterdir()} - expected_dirs:
            raise CallError("grounded work root contains an extra entry")
        for number, task in tasks.items():
            current = workdir(root, number)
            if not os.path.lexists(current):
                current.mkdir()
            PS.safe_dir(current, workspace)
            if {path.name for path in current.iterdir()} - {"task.json", "schema.json"}:
                raise CallError(f"chapter {number}: task workdir contains an extra entry")
            _write_once(task_path(root, number), PS.json_bytes(task), None, "task file")
            _write_once(schema_path(root, number), PS.json_bytes(C.output_schema()), None,
                        "schema file")
            current.chmod(0o555)
        workspace.chmod(0o555)
        validate_workdirs(root, tasks)
    except (PS.StoreError, OSError, C.ContractError) as exc:
        raise CallError(f"grounded task workdir is invalid: {exc}") from exc


def validate_workdirs(root, tasks):
    workspace = PS.safe_dir(work_root(root), folder(root))
    _mode(workspace, 0o555, "work root")
    expected = {f"chapter-{number:02d}" for number in tasks}
    if {path.name for path in workspace.iterdir()} != expected:
        raise CallError("grounded work root layout differs")
    for number, expected_task in tasks.items():
        current = PS.safe_dir(workdir(root, number), workspace)
        _mode(current, 0o555, "chapter workdir")
        files = PS.exact_tree(current, [
            {"group": "evidence", "path": "task.json"},
            {"group": "evidence", "path": "schema.json"}])
        task_data = PS._safe_file(task_path(root, number), current).read_bytes()
        task = C.task(C.loads(task_data.decode("utf-8"), "grounded task"))
        schema_data = PS._safe_file(schema_path(root, number), current).read_bytes()
        if task != expected_task or task_data != PS.json_bytes(expected_task) \
                or schema_data != PS.json_bytes(C.output_schema()):
            raise CallError(f"chapter {number}: stored task or schema differs")
        if any(item["sha256"] != PS.sha((task_data if item["path"] == "task.json"
                                         else schema_data)) for item in files):
            raise CallError(f"chapter {number}: task workdir hash differs")
        _mode(task_path(root, number), 0o444, "task file")
        _mode(schema_path(root, number), 0o444, "schema file")


def expected_marker(root, task):
    number = task["chapter"]
    command = codex_command(task, workdir(root, number), schema_path(root, number))
    body = {"schema": SCHEMA, "chapter": number,
            "task_sha256": task["task_sha256"],
            "task_file_sha256": PS.sha(PS.json_bytes(task)),
            "output_schema_sha256": PS.sha(PS.json_bytes(C.output_schema())),
            "input_sha256": PS.sha(input_text(task).encode("utf-8")),
            "provider": PROVIDER, "route": task["reviewer"]["route"],
            "model": task["reviewer"]["model"],
            "reasoning": task["reviewer"]["reasoning"],
            "cwd": str(workdir(root, number)), "command": command,
            "command_sha256": PS.state_hash(command)}
    return {**body, "call_id": PS.state_hash(body)}


def _read_json(path, boundary, label):
    try:
        data = PS._safe_file(path, boundary).read_bytes()
        value = C.loads(data.decode("utf-8"), label)
        return data, value
    except (PS.StoreError, OSError, UnicodeError, C.ContractError) as exc:
        raise CallError(f"{label} is invalid: {exc}") from exc


def start(root, task):
    wanted, path = expected_marker(root, task), marker_path(root, task["chapter"])
    data = PS.json_bytes(wanted)
    if os.path.lexists(path):
        actual_data, actual = _read_json(path, folder(root), "grounded call marker")
        _mode(path, 0o444, "grounded call marker")
        if actual != wanted or actual_data != data:
            raise CallError("grounded call marker identity differs")
        return False, wanted
    _write_once(path, data, None, "grounded call marker")
    return True, wanted


def wrapper_command(root, number):
    script = Path(__file__).resolve().parents[1] / "eval" / "native_grounded_review.py"
    return [sys.executable or "python3", str(script), "--workdir", str(workdir(root, number)),
            "--marker", str(marker_path(root, number)),
            "--transport", str(transport_path(root, number)),
            "--raw", str(raw_path(root, number))]


def _envelope(marker, raw, runtime):
    encoded = raw.encode("utf-8")
    body = {key: marker[key] for key in (
        "chapter", "call_id", "task_sha256", "task_file_sha256",
        "output_schema_sha256", "input_sha256", "provider", "route", "model",
        "reasoning", "cwd", "command", "command_sha256")}
    body.update(schema=SCHEMA, exit_code=runtime["exit_code"],
                thread_id=runtime["thread_id"],
                session_id=f"codex:{runtime['thread_id']}", usage=runtime["usage"],
                raw_sha256=PS.sha(encoded), raw_b64=base64.b64encode(encoded).decode("ascii"))
    return body


def persist(root, task, marker, raw, runtime, interrupt=None):
    if marker != expected_marker(root, task):
        raise CallError("native transport marker differs from its task")
    if runtime.get("exit_code") != 0 or not isinstance(runtime.get("thread_id"), str) \
            or not runtime["thread_id"].strip() or not isinstance(runtime.get("usage"), dict):
        raise CallError("native transport lacks successful thread/session proof")
    if runtime.get("command") != marker["command"]:
        raise CallError("native transport command differs from its marker")
    C.verdict(raw, task)
    envelope = _envelope(marker, raw, runtime)
    boundary = interrupt or (lambda _step: None)
    _write_once(transport_path(root, task["chapter"]), PS.json_bytes(envelope), boundary,
                "grounded transport")
    boundary("transport-persisted")
    _write_once(raw_path(root, task["chapter"]), raw.encode("utf-8"), boundary,
                "grounded raw verdict")
    boundary("raw-persisted")
    return envelope


def read(root, task):
    number, marker = task["chapter"], expected_marker(root, task)
    marker_data, actual_marker = _read_json(
        marker_path(root, number), folder(root), "grounded call marker")
    _mode(marker_path(root, number), 0o444, "grounded call marker")
    if actual_marker != marker or marker_data != PS.json_bytes(marker):
        raise CallError("grounded call marker identity differs")
    transport = transport_path(root, number)
    if not os.path.lexists(transport):
        if os.path.lexists(raw_path(root, number)):
            raise CallError("raw verdict exists without proven native transport")
        raise CallError("marked native review has no durable transport; replay is ambiguous")
    transport_data, envelope = _read_json(transport, folder(root), "grounded transport")
    try:
        raw = base64.b64decode(envelope["raw_b64"], validate=True)
    except (KeyError, TypeError, ValueError) as exc:
        raise CallError(f"grounded transport raw response is malformed: {exc}") from exc
    if envelope.get("exit_code") != 0 or not isinstance(envelope.get("thread_id"), str) \
            or not envelope["thread_id"].strip() or not isinstance(envelope.get("usage"), dict):
        raise CallError("grounded transport lacks successful thread/session proof")
    expected = _envelope(marker, raw.decode("utf-8"), {
        "exit_code": envelope.get("exit_code"), "thread_id": envelope.get("thread_id"),
        "usage": envelope.get("usage")})
    if envelope != expected or envelope.get("session_id") != f"codex:{envelope.get('thread_id')}":
        raise CallError("grounded transport identity differs")
    C.verdict(raw.decode("utf-8"), task)
    _mode(transport, 0o444, "grounded transport")
    verdict_path = raw_path(root, number)
    if not os.path.lexists(verdict_path):
        _write_once(verdict_path, raw, None, "grounded raw verdict")
    elif PS._safe_file(verdict_path, folder(root)).read_bytes() != raw:
        raise CallError("grounded raw verdict differs from proven transport")
    _mode(verdict_path, 0o444, "grounded raw verdict")
    return raw.decode("utf-8"), envelope, {
        "task_file_sha256": marker["task_file_sha256"],
        "schema_sha256": marker["output_schema_sha256"],
        "call_sha256": PS.sha(marker_data), "transport_sha256": PS.sha(transport_data),
        "raw_sha256": PS.sha(raw)}
