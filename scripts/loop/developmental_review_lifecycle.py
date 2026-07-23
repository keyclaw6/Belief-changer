"""Accepted-root monotonic lifecycle for one RF-13 review operation."""
import json
import os
import stat
from pathlib import Path
import draft_batch_lifecycle as DL
import pair_store as PS
SCHEMA = 1
KEYS = {"schema", "operation", "operation_sha256", "state", "local_state",
        "binding", "result", "before_sha256", "after_sha256", "record_hash"}
BINDING = {"task_sha256", "task_file_sha256", "schema_sha256", "call_id",
           "call_sha256"}
RESULT = BINDING | {"transport_sha256", "raw_sha256", "receipt_hash",
                    "receipt_sha256"}
HEX = set("0123456789abcdef")
class LifecycleError(RuntimeError):
    pass
def identity(root, manifest):
    return {"stage": "RF-13", **DL.identity(root, manifest)}
def path(root, manifest):
    operation = identity(root, manifest)
    accepted = Path(operation["accepted_root"])
    return (PS.state_dir(accepted) / "operations" / "developmental" /
            f"{PS.state_hash(operation)}.json")
def _pack(body):
    return {**body, "record_hash": PS.state_hash(body)}
def _never(operation):
    return _pack({"schema": SCHEMA, "operation": operation,
                  "operation_sha256": PS.state_hash(operation),
                  "state": "NEVER_STARTED", "local_state": None,
                  "binding": None, "result": None, "before_sha256": None,
                  "after_sha256": None})
def _valid_hash(value):
    return isinstance(value, str) and len(value) == 64 and not set(value) - HEX
def _descriptor(value, keys):
    return isinstance(value, dict) and set(value) == keys \
        and all(_valid_hash(item) for item in value.values())
def _read(path, boundary, final=True):
    try:
        data = PS._safe_file(path, boundary).read_bytes()
        info = os.lstat(path)
        if info.st_uid != os.lstat(boundary).st_uid:
            raise LifecycleError("developmental lifecycle record has the wrong owner")
        if final:
            if os.name == "nt":
                attributes = getattr(info, "st_file_attributes", 0)
                if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 \
                        or attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0) \
                        or not attributes & getattr(stat, "FILE_ATTRIBUTE_READONLY", 0):
                    raise LifecycleError(
                        "developmental lifecycle anchor is not a canonical read-only file")
            elif stat.S_IMODE(info.st_mode) != 0o444:
                raise LifecycleError(
                    "developmental lifecycle anchor mode is not canonical 0444")
        return data
    except (PS.StoreError, OSError) as exc:
        raise LifecycleError(f"developmental lifecycle record is unsafe: {exc}") from exc
def _parse(data, operation):
    try:
        value = json.loads(data)
        body = {key: item for key, item in value.items() if key != "record_hash"}
    except (json.JSONDecodeError, TypeError) as exc:
        raise LifecycleError(f"developmental lifecycle record is malformed: {exc}") from exc
    if set(value) != KEYS or value.get("schema") != SCHEMA \
            or value.get("operation") != operation \
            or value.get("operation_sha256") != PS.state_hash(operation) \
            or value.get("record_hash") != PS.state_hash(body) \
            or value.get("state") not in ("NEVER_STARTED", "STARTED"):
        raise LifecycleError("developmental lifecycle identity is missing or tampered")
    if value["state"] == "NEVER_STARTED":
        if any(value[key] is not None for key in
               ("local_state", "binding", "result", "before_sha256", "after_sha256")):
            raise LifecycleError("never-started developmental lifecycle contains review state")
    elif value.get("local_state") not in ("PENDING", "COMMITTED") \
            or not _descriptor(value.get("binding"), BINDING) \
            or not _valid_hash(value.get("before_sha256")):
        raise LifecycleError("started developmental lifecycle metadata is malformed")
    elif value["result"] is None:
        if value["local_state"] != "PENDING" or value["after_sha256"] is not None:
            raise LifecycleError("unfinished developmental lifecycle metadata is malformed")
    elif not _descriptor(value["result"], RESULT) \
            or any(value["result"][key] != value["binding"][key] for key in BINDING) \
            or not _valid_hash(value.get("after_sha256")):
        raise LifecycleError("completed developmental lifecycle metadata is malformed")
    return value
def _write(target, value, interrupt=None):
    data, temp = PS.json_bytes(value), target.with_name(f".{target.name}.rf02-tmp")
    if os.path.lexists(temp) and _read(temp, target.parent, False) != data:
        raise LifecycleError("developmental lifecycle staging bytes are not replayable")
    if os.path.lexists(target) and not os.path.lexists(temp) \
            and _read(target, target.parent) == data:
        return
    try:
        PS.write(target, data, interrupt)
        target.chmod(0o444)
    except (PS.StoreError, OSError) as exc:
        raise LifecycleError(f"developmental lifecycle write failed: {exc}") from exc
def initialize(root, manifest):
    operation, target = identity(root, manifest), path(root, manifest)
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        PS.safe_dir(target.parent, PS.state_dir(operation["accepted_root"]))
    except (PS.StoreError, OSError) as exc:
        raise LifecycleError(f"developmental lifecycle registry is unsafe: {exc}") from exc
    wanted = _never(operation)
    if os.path.lexists(target) and _parse(_read(target, target.parent), operation) != wanted:
        raise LifecycleError("developmental lifecycle operation identity is reused")
    _write(target, wanted)
def _record(root, manifest):
    operation, target = identity(root, manifest), path(root, manifest)
    if not os.path.lexists(target):
        raise LifecycleError("developmental lifecycle anchor is missing")
    current = _parse(_read(target, target.parent), operation)
    return operation, target, current, target.with_name(f".{target.name}.rf02-tmp")
def _started(operation, manifest, binding):
    return _pack({"schema": SCHEMA, "operation": operation,
                  "operation_sha256": PS.state_hash(operation), "state": "STARTED",
                  "local_state": "PENDING", "binding": binding, "result": None,
                  "before_sha256": PS.state_hash(manifest), "after_sha256": None})
def _transition(old, new, manifest):
    if old["state"] == "NEVER_STARTED":
        return new == _started(old["operation"], manifest, new.get("binding"))
    common = {key: old[key] for key in
              ("schema", "operation", "operation_sha256", "state", "binding",
               "before_sha256")}
    if old["result"] is None:
        return new.get("local_state") == "PENDING" and new.get("result") is not None \
            and all(new.get(key) == item for key, item in common.items())
    expected = _pack({**{key: value for key, value in old.items()
                         if key != "record_hash"}, "local_state": "COMMITTED"})
    return new == expected
def _write_manifest(root, manifest, updated, interrupt=None):
    target, temp = Path(root).absolute() / "pair.json", Path(root).absolute() / ".pair.json.rf02-tmp"
    data = PS.json_bytes(updated)
    if os.path.lexists(temp) and _read(temp, Path(root).absolute(), False) != data:
        raise LifecycleError("developmental local manifest staging differs")
    try:
        PS.write_json(target, updated, interrupt)
    except (PS.StoreError, OSError) as exc:
        raise LifecycleError(f"developmental local manifest write failed: {exc}") from exc
def recover(root, manifest):
    _, target, record, temp = _record(root, manifest)
    if os.path.lexists(temp):
        staged = _parse(_read(temp, target.parent, False), record["operation"])
        if not _transition(record, staged, manifest):
            raise LifecycleError("developmental lifecycle staging transition is invalid")
        _write(target, staged)
        record = staged
    if record.get("local_state") != "PENDING" or record.get("result") is None:
        return
    updated = {**manifest, "developmental_review": record["result"]}
    if manifest.get("developmental_review") is None:
        if PS.state_hash(manifest) != record["before_sha256"]:
            raise LifecycleError("pending developmental commit no longer matches its candidate")
        _write_manifest(root, manifest, updated)
        manifest = updated
    if manifest.get("developmental_review") != record["result"] \
            or PS.state_hash(manifest) != record["after_sha256"]:
        raise LifecycleError("pending developmental local commit was overwritten")
    committed = _pack({**{key: value for key, value in record.items()
                          if key != "record_hash"}, "local_state": "COMMITTED"})
    _write(target, committed)
def start(root, manifest, binding, local_writer, interrupt=None):
    if not _descriptor(binding, BINDING):
        raise LifecycleError("developmental lifecycle binding is invalid")
    operation, target, record, temp = _record(root, manifest)
    boundary = interrupt or (lambda _step: None)
    if os.path.lexists(temp):
        raise LifecycleError("developmental lifecycle start requires recovery")
    if record["state"] == "NEVER_STARTED":
        record = _started(operation, manifest, binding)
        _write(target, record, boundary)
        boundary("developmental-lifecycle-started")
    elif record.get("local_state") != "PENDING" or record.get("result") is not None \
            or record.get("binding") != binding:
        raise LifecycleError("developmental lifecycle cannot restart or change task")
    local_writer()
    boundary("developmental-lifecycle-local")
    return record
def commit(root, manifest, descriptor, interrupt=None):
    if not _descriptor(descriptor, RESULT):
        raise LifecycleError("developmental lifecycle result descriptor is invalid")
    _, target, record, temp = _record(root, manifest)
    if os.path.lexists(temp) or record.get("local_state") != "PENDING" \
            or record.get("result") is not None or descriptor.get("task_sha256") \
            != record["binding"]["task_sha256"]:
        raise LifecycleError("developmental lifecycle cannot commit from its current state")
    updated = {**manifest, "developmental_review": descriptor}
    pending = _pack({**{key: value for key, value in record.items()
                        if key != "record_hash"}, "result": descriptor,
                     "after_sha256": PS.state_hash(updated)})
    boundary = interrupt or (lambda _step: None)
    _write(target, pending, boundary)
    boundary("developmental-lifecycle-finishing")
    _write_manifest(root, manifest, updated, boundary)
    boundary("developmental-lifecycle-local-commit")
    committed = _pack({**{key: value for key, value in pending.items()
                          if key != "record_hash"}, "local_state": "COMMITTED"})
    _write(target, committed, boundary)
    boundary("developmental-lifecycle-committed")
    return committed
def _local(root, record, committed):
    folder = Path(root).absolute() / "evidence" / "developmental-review"
    if not os.path.lexists(folder):
        if committed:
            raise LifecycleError("committed developmental local folder is missing")
        return
    try:
        PS.safe_dir(folder, Path(root).absolute() / "evidence")
        files = {path.name: path for path in PS.tree_files(folder)}
        order = ("task.json", "schema.json", "call.json", "transport.json",
                 "verdict.raw.json", "receipt.json")
        found = tuple(name for name in order if name in files)
        if set(files) != set(found) or found != order[:len(found)]:
            raise LifecycleError("developmental local evidence inventory differs")
        if committed and found != order:
            raise LifecycleError("committed developmental local evidence is incomplete")
        for item in files.values():
            if stat.S_IMODE(os.lstat(item).st_mode) != 0o444:
                raise LifecycleError("developmental local evidence mode is not canonical 0444")
        expected = record["result"] if committed else record["binding"]
        mapping = {"task.json": "task_file_sha256", "schema.json": "schema_sha256",
                   "call.json": "call_sha256", "transport.json": "transport_sha256",
                   "verdict.raw.json": "raw_sha256", "receipt.json": "receipt_sha256"}
        for name, key in mapping.items():
            if name in files and key in expected and PS.sha(files[name].read_bytes()) != expected[key]:
                raise LifecycleError("developmental local evidence hash differs")
        if committed and stat.S_IMODE(os.lstat(folder).st_mode) != 0o555:
            raise LifecycleError("committed developmental local folder mode is not 0555")
    except (PS.StoreError, OSError) as exc:
        raise LifecycleError(f"developmental local evidence is unsafe: {exc}") from exc
def validate(root, manifest):
    _, _, record, temp = _record(root, manifest)
    if os.path.lexists(temp):
        raise LifecycleError("developmental lifecycle transition requires recovery")
    local = manifest.get("developmental_review")
    if record["state"] == "NEVER_STARTED":
        if local is not None or manifest.get("draft_batch") is not None \
                and manifest.get("state") == "SEALED":
            raise LifecycleError("never-started developmental lifecycle was downgraded")
        if os.path.lexists(Path(root).absolute() / "evidence" / "developmental-review"):
            raise LifecycleError("never-started developmental lifecycle has local evidence")
        _local(root, record, False)
        return
    if record["local_state"] == "PENDING":
        if local is not None or manifest.get("state") != "BATCH_FROZEN":
            raise LifecycleError("pending developmental lifecycle conflicts with candidate")
        _local(root, record, False)
        return
    if local != record["result"] or manifest.get("state") not in ("BATCH_FROZEN", "SEALED"):
        raise LifecycleError("committed developmental lifecycle lost local authority")
    _local(root, record, True)
def committed(root, manifest):
    _, _, record, temp = _record(root, manifest)
    if os.path.lexists(temp) or record.get("local_state") != "COMMITTED" \
            or record.get("result") != manifest.get("developmental_review"):
        raise LifecycleError("developmental lifecycle is not committed")
    _local(root, record, True)
    return {**record["result"], "lifecycle_record_hash": record["record_hash"]}
def status(root, manifest):
    _, _, record, temp = _record(root, manifest)
    if os.path.lexists(temp):
        raise LifecycleError("developmental lifecycle transition requires recovery")
    return record["state"], record["local_state"], record["result"]
