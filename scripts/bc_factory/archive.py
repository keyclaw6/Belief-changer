"""Reproducible full working-tree ZIP, without VCS internals or credentials."""
from __future__ import annotations
import os
import hashlib
import subprocess
import zipfile
from pathlib import Path
from .common import FactoryError, atomic_json, canonical, confined, file_hash, require

OMIT_DIRS = {".git", "__pycache__", ".venv", "node_modules", ".codebase-memory-mcp", ".codex", "dist"}

def excluded(rel: str) -> bool:
    p = Path(rel)
    return (bool(set(p.parts) & OMIT_DIRS) or (p.name.startswith(".env") and p.name != ".env.example")
            or p.name.endswith((".pem", ".key", ".pyc", ".partial")) or p.name in ("id_rsa", "id_ed25519", ".factory.lock"))


def build(repo: Path, output: Path) -> dict:
    repo, output = repo.resolve(), output.resolve()
    require(not output.is_relative_to(repo) or "dist" in output.relative_to(repo).parts, "Archive output must be outside the repo or inside dist/")
    proc = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=repo, capture_output=True)
    if proc.returncode == 0:
        paths = sorted(set(proc.stdout.decode().split("\0")) - {""})
    else:
        # rglob does not descend into symlinked directories. Validate file links below.
        paths = sorted(p.relative_to(repo).as_posix() for p in repo.rglob("*") if (p.is_file() or p.is_symlink()) and not excluded(p.relative_to(repo).as_posix()))
    paths = [p for p in paths if not excluded(p)]
    require(bool(paths) and "scripts/factory.py" in paths, "No v2 source tree to archive")
    files = {}
    dereferenced_symlinks = {}
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_suffix(output.suffix + ".partial")
    try:
        with zipfile.ZipFile(temp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for rel in paths:
                path = Path(rel)
                require(not path.is_absolute() and ".." not in path.parts, "Unsafe archive path")
                src = repo / path
                # Legacy reference aliases are safe to materialize as regular files,
                # but links to credentials, directories or outside the tree must fail.
                if src.is_symlink():
                    confined(repo, path.parent.as_posix())
                    try:
                        target = src.resolve(strict=True)
                    except (OSError, RuntimeError) as exc:
                        raise FactoryError(f"Broken/cyclic archive symlink: {rel}") from exc
                    require(target.is_relative_to(repo), f"External archive symlink: {rel}")
                    target_rel = target.relative_to(repo).as_posix()
                    require(not excluded(target_rel), f"Symlink targets an excluded file: {rel}")
                    src = confined(repo, target_rel)
                    require(src.is_file(), f"Symlink does not target a regular file: {rel}")
                    dereferenced_symlinks[rel] = target_rel
                else:
                    src = confined(repo, rel)
                require(src.is_file(), f"Missing/non-regular archive input: {rel}")
                data = src.read_bytes()
                files[rel] = hashlib.sha256(data).hexdigest()
                info = zipfile.ZipInfo("Belief-changer/" + rel, date_time=(2026, 9, 11, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (0o100755 if os.access(src, os.X_OK) else 0o100644) << 16
                z.writestr(info, data)
            manifest = {"schema_version": 2, "files": files, "dereferenced_symlinks": dereferenced_symlinks, "omissions": "VCS internals, private/environment credentials, caches and archive output; historical research retained under its existing rights."}
            info = zipfile.ZipInfo("Belief-changer/ARCHIVE-MANIFEST.json", date_time=(2026, 9, 11, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, canonical(manifest) + b"\n")
        with zipfile.ZipFile(temp) as z:
            require(z.testzip() is None, "ZIP CRC check failed")
            require(not any(excluded(n.split("/", 1)[-1]) for n in z.namelist()), "Credential/cache file entered archive")
        os.replace(temp, output)
    finally:
        temp.unlink(missing_ok=True)
    summary = {"file": str(output), "sha256": file_hash(output), "files": len(files), "bytes": output.stat().st_size}
    atomic_json(output.with_suffix(output.suffix + ".json"), summary)
    return summary
