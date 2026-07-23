"""External monotonic lifecycle for one RF-02 candidate operation."""
import json
import os
import stat
from pathlib import Path

import draft_batch_contract as D
import pair_store as PS

SCHEMA = 1
START = "start.json"
KEYS = {"schema", "operation", "operation_sha256", "state", "local_state",
        "start", "batch", "before_sha256", "after_sha256", "evidence",
        "record_hash"}
IMMUTABLE_BATCH = ("schema", "mode", "operation", "selection", "config",
                   "baseline", "authority_sha256", "start_sha256")


class LifecycleError(RuntimeError):
    pass
def _accepted(root):
    root = Path(root).absolute()
    if root.parent.name != "experiments" or root.parent.parent.name != "loop":
        raise LifecycleError("candidate operation is outside the accepted operation root")
    accepted = root.parents[2]
    try:
        PS.safe_dir(accepted)
        PS.safe_dir(root, accepted)
    except PS.StoreError as exc:
        raise LifecycleError(str(exc)) from exc
    return accepted
def identity(root, manifest):
    accepted = _accepted(root)
    try:
        _, registry = PS.load_registry(accepted, manifest["accepted_generation"])
        if (registry["pair_hash"], registry["evaluation_hash"]) != (
                manifest["accepted_pair_hash"], manifest["accepted_evaluation_hash"]):
            raise LifecycleError("candidate lifecycle generation identity mismatch")
        return {"candidate_root": str(Path(root).absolute()),
                "accepted_root": str(accepted), "run": manifest["run"],
                "accepted_generation": manifest["accepted_generation"],
                "accepted_pair_hash": manifest["accepted_pair_hash"],
                "accepted_evaluation_hash": manifest["accepted_evaluation_hash"]}
    except (KeyError, PS.StoreError) as exc:
        raise LifecycleError(f"candidate lifecycle cannot resolve its generation: {exc}") from exc
def path(root, manifest):
    operation = identity(root, manifest)
    return PS.state_dir(_accepted(root)) / "operations" / f"{PS.state_hash(operation)}.json"
def _pack(body):
    return {**body, "record_hash": PS.state_hash(body)}
def _never(operation):
    return _pack({"schema": SCHEMA, "operation": operation,
                  "operation_sha256": PS.state_hash(operation),
                  "state": "NEVER_STARTED", "local_state": None,
                  "start": None, "batch": None, "before_sha256": None,
                  "after_sha256": None, "evidence": None})
def _start_evidence(operation_sha, start):
    return PS.json_bytes({"schema": SCHEMA, "operation_sha256": operation_sha,
                          "start": start})
def _started(operation, manifest, batch, start, local_state):
    after = {**manifest, "state": "DRAFTING", "draft_batch": batch,
             "draft_batch_start": start}
    evidence_data = _start_evidence(PS.state_hash(operation), start)
    return _pack({"schema": SCHEMA, "operation": operation,
                  "operation_sha256": PS.state_hash(operation), "state": "STARTED",
                  "local_state": local_state, "start": start, "batch": batch,
                  "before_sha256": PS.state_hash(manifest),
                  "after_sha256": PS.state_hash(after),
                  "evidence": {"path": f"evidence/{D.FOLDER}/{START}",
                               "sha256": PS.sha(evidence_data)}})
def _read_bytes(value, boundary, final_anchor=False):
    try:
        data = PS._safe_file(value, boundary).read_bytes()
        info = os.lstat(value)
        if info.st_uid != os.lstat(boundary).st_uid:
            raise LifecycleError("candidate lifecycle record has the wrong owner")
        if final_anchor:
            if os.name == "nt":
                attributes = getattr(info, "st_file_attributes", 0)
                if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 \
                        or attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0) \
                        or not attributes & getattr(stat, "FILE_ATTRIBUTE_READONLY", 0):
                    raise LifecycleError(
                        "candidate lifecycle anchor is not a canonical read-only file")
            elif stat.S_IMODE(info.st_mode) != 0o444:
                raise LifecycleError("candidate lifecycle anchor mode is not canonical 0444")
        return data
    except (PS.StoreError, OSError) as exc:
        raise LifecycleError(f"candidate lifecycle record is unsafe: {exc}") from exc


def _parse(data, operation):
    try:
        value = json.loads(data)
        body = {key: item for key, item in value.items() if key != "record_hash"}
    except (json.JSONDecodeError, TypeError) as exc:
        raise LifecycleError(f"candidate lifecycle record is malformed: {exc}") from exc
    if set(value) != KEYS or value.get("schema") != SCHEMA \
            or value.get("operation") != operation \
            or value.get("operation_sha256") != PS.state_hash(operation) \
            or value.get("record_hash") != PS.state_hash(body) \
            or value.get("state") not in ("NEVER_STARTED", "STARTED"):
        raise LifecycleError("candidate lifecycle identity is missing or tampered")
    if value["state"] == "NEVER_STARTED":
        if any(value[key] is not None for key in
               ("local_state", "start", "batch", "before_sha256",
                "after_sha256", "evidence")):
            raise LifecycleError("never-started lifecycle contains batch state")
    elif value.get("local_state") not in ("PENDING", "COMMITTED") \
            or not isinstance(value.get("batch"), dict) \
            or value.get("start") != D.start_marker(value["batch"]) \
            or value["batch"].get("start_sha256") != value["start"].get("start_sha256") \
            or not all(_valid_hash(value.get(key)) for key in
                       ("before_sha256", "after_sha256")):
        raise LifecycleError("started lifecycle metadata is malformed")
    return value


def _valid_hash(value):
    return isinstance(value, str) and len(value) == 64 \
        and not set(value) - set("0123456789abcdef")


def _write(target, value, interrupt=None):
    data, boundary = PS.json_bytes(value), target.parent
    temp = target.with_name(f".{target.name}.rf02-tmp")
    if os.path.lexists(temp) and _read_bytes(temp, boundary) != data:
        raise LifecycleError("candidate lifecycle staging bytes are not replayable")
    if os.path.lexists(target) and not os.path.lexists(temp) \
            and _read_bytes(target, boundary, True) == data:
        return
    try:
        PS.write(target, data, interrupt)
        target.chmod(0o444)
    except (PS.StoreError, OSError) as exc:
        raise LifecycleError(f"candidate lifecycle write failed: {exc}") from exc


def initialize(root, manifest):
    operation = identity(root, manifest)
    target = path(root, manifest)
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        PS.safe_dir(target.parent, PS.state_dir(_accepted(root)))
    except (PS.StoreError, OSError) as exc:
        raise LifecycleError(f"candidate lifecycle registry is invalid: {exc}") from exc
    wanted = _never(operation)
    if os.path.lexists(target) \
            and _parse(_read_bytes(target, target.parent, True), operation) != wanted:
        raise LifecycleError("candidate lifecycle operation identity is reused")
    _write(target, wanted)


def _record(root, manifest):
    operation, target = identity(root, manifest), path(root, manifest)
    if not os.path.lexists(target):
        raise LifecycleError("candidate lifecycle anchor is missing")
    current = _parse(_read_bytes(target, target.parent, True), operation)
    temp = target.with_name(f".{target.name}.rf02-tmp")
    return operation, target, current, temp


def _after(manifest, record):
    return {**manifest, "state": "DRAFTING", "draft_batch": record["batch"],
            "draft_batch_start": record["start"]}


def _ensure_evidence(root, record, interrupt=None):
    folder = D.folder(root)
    try:
        if not os.path.lexists(folder):
            evidence = Path(root).absolute() / "evidence"
            PS.safe_dir(evidence, root)
            folder.mkdir()
        PS.safe_dir(folder, Path(root).absolute() / "evidence")
        target = folder / START
        data = _start_evidence(record["operation_sha256"], record["start"])
        temp = target.with_name(f".{target.name}.rf02-tmp")
        if os.path.lexists(target) and _read_bytes(target, folder) != data:
            raise LifecycleError("draft lifecycle evidence differs from its registry")
        if os.path.lexists(temp) and _read_bytes(temp, folder) != data:
            raise LifecycleError("draft lifecycle evidence staging differs")
        if not os.path.lexists(target) or os.path.lexists(temp):
            PS.write(target, data, interrupt)
    except (PS.StoreError, OSError) as exc:
        raise LifecycleError(f"draft lifecycle evidence write failed: {exc}") from exc


def recover(root, manifest):
    operation, target, record, temp = _record(root, manifest)
    if os.path.lexists(temp):
        staged = _parse(_read_bytes(temp, target.parent), operation)
        if record["state"] == "NEVER_STARTED" and staged.get("local_state") == "PENDING":
            if PS.state_hash(manifest) != staged["before_sha256"]:
                raise LifecycleError("pending lifecycle start no longer matches its candidate")
        elif record.get("local_state") == "PENDING" \
                and staged == _pack({**{k: v for k, v in record.items()
                                       if k != "record_hash"}, "local_state": "COMMITTED"}):
            pass
        else:
            raise LifecycleError("candidate lifecycle staging transition is invalid")
        _write(target, staged)
        record = staged
    if record.get("local_state") != "PENDING":
        return
    after = _after(manifest, record)
    if PS.state_hash(manifest) == record["before_sha256"]:
        D.validate_shape(record["batch"], after)
        try:
            PS.exact_layout(root, manifest, {".pair.json.rf02-tmp": PS.json_bytes(after)})
            PS.write_json(Path(root).absolute() / "pair.json", after)
        except (PS.StoreError, OSError) as exc:
            raise LifecycleError(f"pending local draft start cannot recover: {exc}") from exc
    elif PS.state_hash(manifest) != record["after_sha256"]:
        raise LifecycleError("pending local draft start was overwritten")
    _ensure_evidence(root, record)
    committed = _pack({**{k: v for k, v in record.items() if k != "record_hash"},
                       "local_state": "COMMITTED"})
    _write(target, committed)


def start(root, manifest, batch, marker, interrupt=None):
    operation, target, current, temp = _record(root, manifest)
    if os.path.lexists(temp) or current["state"] != "NEVER_STARTED":
        raise LifecycleError("candidate lifecycle cannot start from its current state")
    pending = _started(operation, manifest, batch, marker, "PENDING")
    after = _after(manifest, pending)
    D.validate_shape(batch, after)
    boundary = interrupt or (lambda _step: None)
    _write(target, pending, boundary)
    boundary("lifecycle-started")
    try:
        PS.exact_layout(root, manifest, {".pair.json.rf02-tmp": PS.json_bytes(after)})
        PS.write_json(Path(root).absolute() / "pair.json", after, boundary)
    except (PS.StoreError, OSError) as exc:
        raise LifecycleError(f"local draft start failed: {exc}") from exc
    boundary("lifecycle-local")
    _ensure_evidence(root, pending, boundary)
    boundary("lifecycle-evidence")
    committed = _pack({**{k: v for k, v in pending.items() if k != "record_hash"},
                       "local_state": "COMMITTED"})
    _write(target, committed, boundary)
    boundary("lifecycle-committed")


def validate(root, manifest):
    _, _, record, temp = _record(root, manifest)
    if os.path.lexists(temp) or record.get("local_state") == "PENDING":
        raise LifecycleError("candidate lifecycle transition requires recovery")
    batch, marker = manifest.get("draft_batch"), manifest.get("draft_batch_start")
    if record["state"] == "NEVER_STARTED":
        if batch is not None or marker is not None \
                or manifest.get("state") in ("DRAFTING", "BATCH_FROZEN"):
            raise LifecycleError("never-started lifecycle contradicts local batch state")
        return
    if not isinstance(batch, dict) or marker != record["start"] \
            or manifest.get("state") not in ("DRAFTING", "BATCH_FROZEN", "SEALED") \
            or any(batch.get(key) != record["batch"].get(key) for key in IMMUTABLE_BATCH):
        raise LifecycleError("started lifecycle lost or downgraded its local batch state")
    evidence = D.folder(root) / START
    data = _start_evidence(record["operation_sha256"], record["start"])
    if not os.path.lexists(evidence) or _read_bytes(evidence, D.folder(root)) != data \
            or record["evidence"] != {"path": f"evidence/{D.FOLDER}/{START}",
                                      "sha256": PS.sha(data)}:
        raise LifecycleError("started lifecycle evidence is missing or tampered")
