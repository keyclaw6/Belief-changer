"""Strict serialization, immutable records, confined paths and atomic writes."""
from __future__ import annotations
import contextlib
import datetime as dt
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any, Iterator

class FactoryError(ValueError):
    """An input or integrity failure. Never convert this into a successful marker."""

def require(condition: bool, message: str) -> None:
    if not condition:
        raise FactoryError(message)

def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()

def identifier(value: str) -> str:
    require(isinstance(value, str) and re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_.-]{0,95}", value) is not None,
            f"Invalid identifier: {value!r}")
    require(value not in (".", ".."), "Unsafe identifier")
    return value

def canonical(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")

def digest(data: Any) -> str:
    return hashlib.sha256(canonical(data)).hexdigest()

def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def _pairs(pairs: list[tuple[str, Any]]) -> dict:
    out: dict = {}
    for k, v in pairs:
        require(k not in out, f"Duplicate JSON key: {k}")
        out[k] = v
    return out

def parse_json(text: str) -> Any:
    def bad_constant(value: str) -> None:
        raise FactoryError(f"Non-finite JSON value: {value}")
    try:
        return json.loads(text, object_pairs_hook=_pairs, parse_constant=bad_constant)
    except (json.JSONDecodeError, TypeError) as exc:
        raise FactoryError(f"Invalid JSON: {exc}") from exc

def read_json(path: Path) -> Any:
    require(path.is_file() and not path.is_symlink(), f"Missing or symlinked file: {path}")
    return parse_json(path.read_text(encoding="utf-8"))

def reply_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```json\n") and text.endswith("\n```"):
        text = text[8:-4]
    data = parse_json(text)
    require(isinstance(data, dict), "Role output must be one JSON object; console logs are not a response")
    return data

def confined(root: Path, relative: str) -> Path:
    require(isinstance(relative, str) and bool(relative) and "\\" not in relative, "Invalid relative path")
    rel = Path(relative)
    require(not rel.is_absolute() and all(p not in (".", "..") for p in rel.parts), "Path traversal is forbidden")
    root = root.resolve()
    target = root / rel
    for parent in [target, *target.parents]:
        if parent == root:
            break
        require(not parent.is_symlink(), f"Symlink is forbidden: {parent}")
    require(target.resolve().is_relative_to(root), "Path escapes workspace")
    return target

def atomic_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    require(not path.is_symlink(), f"Cannot replace symlink: {path}")
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".partial", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
        # Persist directory entry on platforms that support directory fsync.
        if hasattr(os, "O_DIRECTORY"):
            dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(dfd)
            finally:
                os.close(dfd)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

def atomic_json(path: Path, data: Any) -> None:
    atomic_bytes(path, canonical(data) + b"\n")

def seal(path: Path, data: dict) -> dict:
    """Single-file checksummed record; the checksum is integrity, NOT authentication."""
    record = {"payload": data, "sha256": digest(data)}
    if path.exists():
        existing = unseal(path)
        require(existing == data, f"Immutable record already exists with other content: {path}")
        return existing
    atomic_json(path, record)
    return data

def unseal(path: Path) -> dict:
    record = read_json(path)
    require(isinstance(record, dict) and set(record) == {"payload", "sha256"}, f"Not a sealed record: {path}")
    require(isinstance(record["payload"], dict), "Sealed payload must be an object")
    require(digest(record["payload"]) == record["sha256"], f"Checksum mismatch: {path}")
    return record["payload"]

@contextlib.contextmanager
def lock(root: Path) -> Iterator[None]:
    root.mkdir(parents=True, exist_ok=True)
    path = root / ".factory.lock"
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise FactoryError(f"Workspace locked: {path}. Inspect the owning process; never auto-steal a lock.") from exc
    try:
        with os.fdopen(fd, "w") as f:
            json.dump({"pid": os.getpid(), "created_at": now()}, f)
        yield
    finally:
        path.unlink(missing_ok=True)

def nonempty(value: Any, label: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{label} must be a nonempty string")
    return value

def exact_keys(data: Any, required: set[str], optional: set[str] | None = None, label: str = "object") -> None:
    require(isinstance(data, dict), f"{label} must be an object")
    missing = required - set(data)
    unknown = set(data) - required - (optional or set())
    require(not missing and not unknown, f"{label}: missing={sorted(missing)}, unknown={sorted(unknown)}")

def version(data: dict) -> None:
    require(type(data.get("schema_version")) is int and data["schema_version"] == 2, "schema_version must be 2")
