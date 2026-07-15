"""Task-hash-only isolated runtime for the RF-13 native reviewer."""
import json
import os
import stat
from pathlib import Path

import developmental_review_contract as C
import pair_store as PS

SCHEMA = 1
BASE = Path("/tmp") / f"belief-changer-rf13-{os.getuid()}"
TASK = "task.json"
OUTPUT_SCHEMA = "schema.json"
RESULT = "result.json"
HEX = set("0123456789abcdef")
DISABLED = ("multi_agent", "shell_tool", "unified_exec", "browser_use",
            "computer_use", "apps", "plugins", "image_generation",
            "in_app_browser", "standalone_web_search")


class RuntimeError(RuntimeError):
    pass


def _hash(value):
    if not isinstance(value, str) or len(value) != 64 or set(value) - HEX:
        raise RuntimeError("developmental runtime task identity is invalid")
    return value


def path(task_sha256):
    return BASE / _hash(task_sha256)


def task_path(task_sha256):
    return path(task_sha256) / TASK


def schema_path(task_sha256):
    return path(task_sha256) / OUTPUT_SCHEMA


def result_path(task_sha256):
    return path(task_sha256) / RESULT


def _mode(value, wanted, label):
    if stat.S_IMODE(os.lstat(value).st_mode) != wanted:
        raise RuntimeError(f"{label} mode is not canonical {wanted:04o}")


def _ancestry(root):
    current = root
    while True:
        for name in (".git", "AGENTS.md"):
            if os.path.lexists(current / name):
                raise RuntimeError("developmental runtime has git or AGENTS ancestry")
        if current == current.parent:
            return
        current = current.parent


def _base():
    try:
        if not os.path.lexists(BASE):
            BASE.mkdir(mode=0o700)
        PS.safe_dir(BASE, "/tmp")
        info = os.lstat(BASE)
        if info.st_uid != os.getuid():
            raise RuntimeError("developmental runtime base has the wrong owner")
        _mode(BASE, 0o700, "developmental runtime base")
        _ancestry(BASE)
        for child in BASE.iterdir():
            _hash(child.name)
            PS.safe_dir(child, BASE)
    except (PS.StoreError, OSError) as exc:
        raise RuntimeError(f"developmental runtime base is unsafe: {exc}") from exc
    return BASE


def _inventory(root):
    """Describe every descendant without following aliases."""
    found = {}

    def visit(folder):
        with os.scandir(folder) as entries:
            items = sorted(entries, key=lambda item: item.name)
        for item in items:
            target, info = Path(item.path), item.stat(follow_symlinks=False)
            relative = target.relative_to(root).as_posix()
            if stat.S_ISLNK(info.st_mode):
                raise RuntimeError(f"developmental runtime entry is aliased: {relative}")
            if stat.S_ISDIR(info.st_mode):
                found[relative] = ("directory", stat.S_IMODE(info.st_mode), info.st_uid)
                visit(target)
            elif stat.S_ISREG(info.st_mode) and info.st_nlink == 1:
                found[relative] = ("file", stat.S_IMODE(info.st_mode), info.st_uid)
            elif stat.S_ISREG(info.st_mode):
                raise RuntimeError(f"developmental runtime entry is multiply linked: {relative}")
            else:
                raise RuntimeError(f"developmental runtime entry is special: {relative}")

    try:
        PS.safe_dir(root, BASE)
        visit(root)
        return found
    except (PS.StoreError, OSError) as exc:
        raise RuntimeError(f"developmental runtime inventory is unsafe: {exc}") from exc


def _structure(root, allowed, required=None):
    found = _inventory(root)
    expected = {name: ("file", 0o444, os.getuid()) for name in allowed}
    required = set(allowed) if required is None else set(required)
    if not required <= set(found) <= set(expected) \
            or any(found[name] != expected[name] for name in found):
        raise RuntimeError("developmental task runtime structure differs")
    return set(found)


def _write_once(target, data, label):
    if os.path.lexists(target):
        try:
            if PS._safe_file(target, target.parent).read_bytes() != data:
                raise RuntimeError(f"{label} already differs")
            _mode(target, 0o444, label)
            return
        except PS.StoreError as exc:
            raise RuntimeError(f"{label} is unsafe: {exc}") from exc
    PS.write(target, data)
    target.chmod(0o444)


def prepare(task):
    C.task(task)
    task_sha = task["task_sha256"]
    base, root = _base(), path(task_sha)
    try:
        if not os.path.lexists(root):
            root.mkdir(mode=0o700)
        PS.safe_dir(root, base)
        info = os.lstat(root)
        if info.st_uid != os.getuid():
            raise RuntimeError("developmental task runtime has the wrong owner")
        if stat.S_IMODE(info.st_mode) not in (0o700, 0o555):
            raise RuntimeError("developmental task runtime mode is invalid")
        root.chmod(0o700)
        _structure(root, {TASK, OUTPUT_SCHEMA, RESULT}, set())
        _write_once(task_path(task_sha), PS.json_bytes(task), "runtime task")
        _write_once(schema_path(task_sha), PS.json_bytes(C.output_schema()), "runtime schema")
        root.chmod(0o555)
        validate(task, allow_result=True)
        return root
    except (PS.StoreError, OSError) as exc:
        raise RuntimeError(f"developmental task runtime cannot be prepared: {exc}") from exc


def validate(task, allow_result=False):
    C.task(task)
    task_sha, root = task["task_sha256"], path(task["task_sha256"])
    _base()
    try:
        if root.absolute() != path(task_sha) or root.resolve() != root:
            raise RuntimeError("developmental runtime path is aliased")
        PS.safe_dir(root, BASE)
        _mode(root, 0o555, "developmental task runtime")
        allowed = {TASK, OUTPUT_SCHEMA, RESULT} if allow_result else {TASK, OUTPUT_SCHEMA}
        found = _structure(root, allowed, {TASK, OUTPUT_SCHEMA})
        task_data = PS._safe_file(task_path(task_sha), root).read_bytes()
        schema_data = PS._safe_file(schema_path(task_sha), root).read_bytes()
        if task_data != PS.json_bytes(task) or schema_data != PS.json_bytes(C.output_schema()):
            raise RuntimeError("developmental runtime task or schema differs")
        _mode(task_path(task_sha), 0o444, "runtime task")
        _mode(schema_path(task_sha), 0o444, "runtime schema")
        if RESULT in found:
            _mode(result_path(task_sha), 0o444, "runtime result")
        return root
    except (PS.StoreError, OSError) as exc:
        raise RuntimeError(f"developmental task runtime is unsafe: {exc}") from exc


def _command(task, root, schema):
    reviewer = task["reviewer"]
    disabled = [item for feature in DISABLED for item in ("--disable", feature)]
    return ["codex", "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
            *disabled, "--model", reviewer["model"], "-c",
            f"model_reasoning_effort={reviewer['reasoning']}", "--sandbox", "read-only",
            "--skip-git-repo-check", "--cd", str(root), "--output-schema", str(schema),
            "--json", "-"]


def command(task):
    root = validate(task)
    return _command(task, root, schema_path(task["task_sha256"]))


def command_spec(task):
    C.task(task)
    return _command(task, "<isolated-rf13-task>", "<isolated-rf13-task>/schema.json")


def input_bytes(task):
    C.task(task)
    return PS.json_bytes(task)


def load(task_sha256, allow_result=False):
    root = path(task_sha256)
    _base()
    try:
        data = PS._safe_file(task_path(task_sha256), root).read_bytes()
        task = C.task(C.loads(data.decode("utf-8"), "runtime developmental task"))
    except (PS.StoreError, OSError, UnicodeError, C.ContractError) as exc:
        raise RuntimeError(f"developmental runtime task is invalid: {exc}") from exc
    if task["task_sha256"] != task_sha256 or data != PS.json_bytes(task):
        raise RuntimeError("developmental runtime task identity differs")
    validate(task, allow_result=allow_result)
    return task


def persist_result(task, value):
    root = validate(task)
    data = PS.json_bytes(value)
    try:
        root.chmod(0o700)
        _write_once(result_path(task["task_sha256"]), data, "runtime result")
    finally:
        root.chmod(0o555)
    validate(task, allow_result=True)


def result(task):
    validate(task, allow_result=True)
    target = result_path(task["task_sha256"])
    if not os.path.lexists(target):
        return None
    try:
        return json.loads(PS._safe_file(target, target.parent).read_text(encoding="utf-8"))
    except (PS.StoreError, OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"developmental runtime result is invalid: {exc}") from exc
