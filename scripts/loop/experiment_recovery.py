"""Exact recovery of RF-02 experiment-root atomic-write temps."""
import json
import os
from pathlib import Path

import path_guard as PG


TEMPS = {
    ".pair.json.rf02-tmp": ("pair.json", ("CANDIDATE", "WRITER_HANDOFF",
                                           "DRAFTING", "BATCH_FROZEN")),
    ".gate-decision.json.rf02-tmp": ("gate-decision.json", "SEALED"),
    ".decision.json.rf02-tmp": ("decision.json", "SEALED"),
}
STABLE = {"pair.json", "gate-decision.json", "decision.json",
          "candidate", "evaluation", "evidence", "writer-authority.json"}


def _bytes(path, root):
    path = PG.safe_file(path, root)
    if os.lstat(path).st_uid != os.lstat(root).st_uid:
        raise PG.PathError(f"atomic-write staging path has the wrong owner: {path}")
    return path.read_bytes()


def _manifest_bytes(manifest):
    return (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()


def preflight(root):
    """Validate root inventory and owned temp file types without deleting."""
    root = PG.safe_dir(root)
    extra = {path.name for path in root.iterdir()} - STABLE - set(TEMPS)
    if extra:
        raise PG.PathError(f"experiment contains undeclared entries: {sorted(extra)}")
    return root, {name: _bytes(root / name, root) for name in TEMPS
                  if os.path.lexists(root / name)}


def recover(root, manifest, expected=None):
    """Discard only temps equal to caller-recomputed bytes for this operation."""
    root, actual = preflight(root)
    expected = expected or {}
    if set(expected) - set(TEMPS):
        raise PG.PathError("atomic-write recovery context contains an unknown staging name")
    pending = []
    for name, found in actual.items():
        target_name, state = TEMPS[name]
        temp = root / name
        if name not in expected:
            raise PG.PathError(f"exact recovery context is unavailable for: {temp}")
        wanted = expected[name]
        states = state if isinstance(state, tuple) else (state,)
        if not isinstance(wanted, bytes) or manifest.get("state") not in states \
                or found != wanted:
            raise PG.PathError(f"atomic-write staging bytes do not belong to this operation: {temp}")
        target = root / target_name
        if target_name == "pair.json":
            if _bytes(target, root) != _manifest_bytes(manifest):
                raise PG.PathError(f"pair staging target changed before recovery: {target}")
        elif os.path.lexists(target) and _bytes(target, root) != wanted:
            raise PG.PathError(f"atomic-write target differs from its staging bytes: {target}")
        pending.append(temp)
    for temp in pending:
        PG.discard_file(temp)
