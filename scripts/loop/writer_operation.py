"""One declared RF-10 writer handoff metadata file."""
import json
from pathlib import Path

import pair_store as PS

RECEIPT = "writer-authority.json"


class OperationError(RuntimeError):
    pass


def valid(value, state):
    if value is None:
        return state not in ("WRITER_HANDOFF", "DRAFTING", "BATCH_FROZEN")
    return state in ("WRITER_HANDOFF", "DRAFTING", "BATCH_FROZEN", "SEALED") \
        and isinstance(value, dict) \
        and set(value) == {"group", "path", "sha256", "receipt_hash"} \
        and value.get("group") == "operation" and value.get("path") == RECEIPT \
        and all(isinstance(value.get(key), str) and len(value[key]) == 64
                and not set(value[key]) - set("0123456789abcdef")
                for key in ("sha256", "receipt_hash"))


def read(root, operation):
    if operation is None:
        return None
    root = Path(root).absolute()
    try:
        data = PS._safe_file(root / operation["path"], root).read_bytes()
        value = json.loads(data)
        receipt_hash = value.pop("receipt_hash")
    except (PS.StoreError, OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise OperationError(f"invalid writer operation metadata: {exc}") from exc
    if PS.sha(data) != operation["sha256"] or receipt_hash != operation["receipt_hash"] \
            or receipt_hash != PS.state_hash(value):
        raise OperationError("writer operation metadata hash mismatch")
    return data


def freeze(root, operation):
    if operation:
        (Path(root).absolute() / operation["path"]).chmod(0o444)
