"""Small cross-platform durable write-once primitive for H-F01 evidence."""
import os
from pathlib import Path

import pair_store as PS


class ImmutableFileError(RuntimeError):
    pass


def write_once(path, data, read_existing, label):
    path = Path(path)
    if os.path.lexists(path):
        if read_existing(path) != data:
            raise ImmutableFileError(f"immutable {label} differs: {path}")
        try:
            path.chmod(0o444)
            PS._sync(path.parent)
        except (OSError, PS.StoreError) as exc:
            raise ImmutableFileError(f"{label} write failed: {exc}") from exc
        return
    try:
        PS.write(path, data)
        path.chmod(0o444)
        PS._sync(path.parent)
    except (OSError, PS.StoreError) as exc:
        raise ImmutableFileError(f"{label} write failed: {exc}") from exc
