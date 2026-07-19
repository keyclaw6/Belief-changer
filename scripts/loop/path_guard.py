"""No-follow validation for every component before RF-02 reads or traversal."""
import os
import shutil
import stat
from pathlib import Path


class PathError(RuntimeError):
    pass


def absolute(path):
    return Path(os.path.abspath(path))


def _inside(path, boundary):
    try:
        path.relative_to(boundary)
        return True
    except ValueError:
        return False


def safe_dir(path, boundary=None):
    path = absolute(path)
    boundary = absolute(boundary) if boundary is not None else Path(path.anchor)
    if not _inside(path, boundary):
        raise PathError(f"path escapes boundary: {path}")
    current = Path(path.anchor)
    for part in path.relative_to(current).parts:
        current /= part
        try:
            info = os.lstat(current)
        except OSError as exc:
            raise PathError(f"directory is missing: {current}") from exc
        if stat.S_ISLNK(info.st_mode):
            raise PathError(f"directory component is aliased: {current}")
        if not stat.S_ISDIR(info.st_mode):
            raise PathError(f"path component is not a directory: {current}")
    return path


def ensure_dir(path, boundary=None):
    """Create missing directories only below a validated, non-aliased ancestor."""
    path = absolute(path)
    boundary = absolute(boundary) if boundary is not None else Path(path.anchor)
    if not _inside(path, boundary):
        raise PathError(f"path escapes boundary: {path}")
    missing, current = [], path
    while not os.path.lexists(current):
        if current == boundary:
            raise PathError(f"boundary is missing: {boundary}")
        missing.append(current)
        current = current.parent
    safe_dir(current, boundary)
    for folder in reversed(missing):
        folder.mkdir()
        safe_dir(folder, boundary)
    return safe_dir(path, boundary)


def safe_file(path, boundary):
    path, boundary = absolute(path), absolute(boundary)
    if not _inside(path, boundary) or path == boundary:
        raise PathError(f"file escapes boundary: {path}")
    safe_dir(path.parent, boundary)
    try:
        info = os.lstat(path)
    except OSError as exc:
        raise PathError(f"declared file is missing: {path}") from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise PathError(f"declared file is aliased or special: {path}")
    if info.st_nlink != 1:
        raise PathError(f"declared file is multiply linked: {path}")
    return path


def files(root, boundary=None):
    root = safe_dir(root, boundary)
    out = []

    def visit(folder):
        with os.scandir(folder) as entries:
            items = sorted(entries, key=lambda item: item.name)
        for item in items:
            info = item.stat(follow_symlinks=False)
            path = Path(item.path)
            if stat.S_ISLNK(info.st_mode):
                raise PathError(f"tree entry is aliased: {path}")
            if stat.S_ISDIR(info.st_mode):
                visit(path)
            elif stat.S_ISREG(info.st_mode) and info.st_nlink == 1:
                out.append(path)
            elif stat.S_ISREG(info.st_mode):
                raise PathError(f"tree file is multiply linked: {path}")
            else:
                raise PathError(f"tree entry is special: {path}")

    visit(root)
    return out


def discard_tree(path, boundary):
    """Remove only a validated, non-aliased private staging tree."""
    path = absolute(path)
    if not os.path.lexists(path):
        return
    if path.is_symlink():
        raise PathError(f"staging path is aliased: {path}")
    safe_dir(path, boundary)
    files(path, boundary)
    shutil.rmtree(path)


def discard_file(path):
    """Remove a private single-link regular file left by interrupted writing."""
    path = absolute(path)
    if not os.path.lexists(path):
        return
    info = os.lstat(path)
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise PathError(f"atomic-write staging path is unsafe: {path}")
    path.unlink()
