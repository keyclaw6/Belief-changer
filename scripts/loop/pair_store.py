"""RF-02 immutable accepted generations behind one atomic pointer."""
import hashlib
import json
import os
from pathlib import Path
import experiment_recovery as ER
import path_guard as PG


class StoreError(RuntimeError):
    pass
def sha(data):
    return hashlib.sha256(data).hexdigest()
def state_hash(value):
    body = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha(body)
def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
def state_dir(root):
    return Path(root).absolute() / "loop/accepted"


def _sync(path):
    if os.name != "nt":
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
        return

    import ctypes
    from ctypes import wintypes

    target = safe_dir(path)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateFileW.argtypes = (wintypes.LPCWSTR, wintypes.DWORD,
                                    wintypes.DWORD, ctypes.c_void_p,
                                    wintypes.DWORD, wintypes.DWORD,
                                    wintypes.HANDLE)
    kernel.CreateFileW.restype = wintypes.HANDLE
    kernel.FlushFileBuffers.argtypes = (wintypes.HANDLE,)
    kernel.FlushFileBuffers.restype = wintypes.BOOL
    kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
    handle = kernel.CreateFileW(str(target), 0x40000000, 0x00000007, None,
                                3, 0x02000000 | 0x00200000, None)
    if handle == wintypes.HANDLE(-1).value:
        raise OSError(ctypes.get_last_error(), f"cannot open directory for flush: {path}")
    try:
        if not kernel.FlushFileBuffers(handle):
            raise OSError(ctypes.get_last_error(), f"cannot flush directory: {path}")
    finally:
        kernel.CloseHandle(handle)


def _replace_file(source, target):
    if os.name != "nt" or not os.path.lexists(target):
        os.replace(source, target)
        return

    import ctypes
    from ctypes import wintypes

    class FILE_RENAME_INFO_EX(ctypes.Structure):
        _fields_ = (("Flags", wintypes.DWORD), ("RootDirectory", wintypes.HANDLE),
                    ("FileNameLength", wintypes.DWORD), ("FileName", wintypes.WCHAR * 1))

    _safe_file(source, Path(source).parent)
    _safe_file(target, Path(target).parent)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateFileW.argtypes = (wintypes.LPCWSTR, wintypes.DWORD,
                                    wintypes.DWORD, ctypes.c_void_p,
                                    wintypes.DWORD, wintypes.DWORD,
                                    wintypes.HANDLE)
    kernel.CreateFileW.restype = wintypes.HANDLE
    kernel.SetFileInformationByHandle.argtypes = (
        wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD)
    kernel.SetFileInformationByHandle.restype = wintypes.BOOL
    kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
    handle = kernel.CreateFileW(str(Path(source)), 0x00010000, 0x00000007,
                                None, 3, 0, None)
    if handle == wintypes.HANDLE(-1).value:
        raise OSError(ctypes.get_last_error(), f"cannot open replacement: {source}")
    try:
        name = str(Path(target)).encode("utf-16-le")
        size = FILE_RENAME_INFO_EX.FileName.offset + len(name) + 2
        buffer = ctypes.create_string_buffer(size)
        info = FILE_RENAME_INFO_EX.from_buffer(buffer)
        info.Flags = 0x00000001 | 0x00000002 | 0x00000040
        info.RootDirectory = None
        info.FileNameLength = len(name)
        ctypes.memmove(ctypes.addressof(buffer) + FILE_RENAME_INFO_EX.FileName.offset,
                       name, len(name))
        if not kernel.SetFileInformationByHandle(handle, 22, buffer, size):
            raise OSError(ctypes.get_last_error(),
                          f"cannot atomically replace read-only file: {target}")
    finally:
        kernel.CloseHandle(handle)

def write(path, data, interrupt=None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.rf02-tmp")
    try:
        PG.discard_file(tmp)
    except PG.PathError as exc:
        raise StoreError(str(exc)) from exc
    try:
        with tmp.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        (interrupt or (lambda _step: None))(f"write-prepared:{path.name}")
        _replace_file(tmp, path)
        _sync(path.parent)
    finally:
        if tmp.exists() or tmp.is_symlink():
            tmp.unlink()
def write_json(path, value, interrupt=None):
    write(path, json_bytes(value), interrupt)
def _safe_file(path, root):
    try:
        return PG.safe_file(path, root)
    except PG.PathError as exc:
        raise StoreError(str(exc)) from exc
def safe_dir(path, boundary=None):
    try:
        return PG.safe_dir(path, boundary)
    except PG.PathError as exc:
        raise StoreError(str(exc)) from exc
def ensure_dir(path, boundary=None):
    try:
        return PG.ensure_dir(path, boundary)
    except PG.PathError as exc:
        raise StoreError(str(exc)) from exc
def tree_files(root, boundary=None):
    try:
        return PG.files(root, boundary)
    except PG.PathError as exc:
        raise StoreError(str(exc)) from exc

def discard_stage(path, boundary):
    try:
        PG.discard_tree(path, boundary)
    except PG.PathError as exc:
        raise StoreError(str(exc)) from exc

def states(root, entries):
    return [{"group": item["group"], "path": item["path"],
             "sha256": sha(_safe_file(Path(root) / item["path"], root).read_bytes())}
            for item in entries]

def exact_tree(root, entries):
    root = Path(root).absolute()
    declared = {item["path"] for item in entries}
    found = {path.relative_to(root).as_posix() for path in tree_files(root)}
    if found != declared:
        raise StoreError(f"tree membership mismatch; missing={sorted(declared-found)}, "
                         f"extra={sorted(found-declared)}")
    return states(root, entries)

def generation_hash(pair_hash, evaluation_hash):
    return state_hash([
        {"group": "pair", "path": "pair", "sha256": pair_hash},
        {"group": "evaluation", "path": "evaluation", "sha256": evaluation_hash},
    ])

def _registry(root, generation):
    return state_dir(root) / "manifests" / f"{generation}.json"

def _valid_entries(entries, groups):
    if not isinstance(entries, list) or not entries:
        return False
    paths = [item.get("path") for item in entries if isinstance(item, dict)]
    return len(paths) == len(entries) == len(set(paths)) and all(
        isinstance(path, str) and path and not Path(path).is_absolute()
        and ".." not in Path(path).parts and item.get("group") in groups
        for path, item in zip(paths, entries))

def load_registry(root, generation):
    if len(generation) != 64 or set(generation) - set("0123456789abcdef"):
        raise StoreError(f"invalid accepted generation id: {generation}")
    path = _registry(root, generation)
    safe_dir(state_dir(root), root)
    try:
        value = json.loads(_safe_file(path, root).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, StoreError) as exc:
        raise StoreError(f"malformed accepted generation metadata: {path}") from exc
    pair, evaluation = value.get("entries"), value.get("evaluation")
    if value.get("schema") != 2 or value.get("generation") != generation \
            or not _valid_entries(pair, {"config", "product"}) \
            or not _valid_entries(evaluation, {"evaluation"}):
        raise StoreError(f"stale accepted generation metadata: {path}")
    tree = state_dir(root) / "generations" / generation
    pair_hash = state_hash(exact_tree(tree / "pair", pair))
    eval_hash = state_hash(exact_tree(tree / "evaluation", evaluation))
    actual = generation_hash(pair_hash, eval_hash)
    if (pair_hash, eval_hash, actual) != (value.get("pair_hash"),
                                         value.get("evaluation_hash"), generation):
        raise StoreError(f"accepted generation hash mismatch: {generation}")
    return tree, value

def current(root, required=True):
    """Resolve and fully validate the current immutable generation exactly once."""
    root, store = Path(root).absolute(), state_dir(root)
    safe_dir(root)
    safe_dir(root / "loop", root)
    if not os.path.lexists(store):
        if required:
            raise StoreError(f"accepted generation pointer missing or malformed: {store / 'current'}")
        return None, None, None
    safe_dir(store, root)
    pointer = store / "current"
    if os.name == "nt":
        if not os.path.lexists(pointer):
            if required:
                raise StoreError(f"accepted generation pointer missing or malformed: {pointer}")
            return None, None, None
        try:
            data = _safe_file(pointer, store).read_bytes()
            generation = data.decode("ascii").removesuffix("\n")
        except (OSError, UnicodeError, StoreError) as exc:
            raise StoreError(f"accepted generation pointer missing or malformed: {pointer}") from exc
        if data != (generation + "\n").encode("ascii"):
            raise StoreError(f"accepted generation pointer missing or malformed: {pointer}")
    else:
        if not pointer.is_symlink():
            if required or os.path.lexists(pointer):
                raise StoreError(f"accepted generation pointer missing or malformed: {pointer}")
            return None, None, None
        raw = Path(os.readlink(pointer))
        if raw.is_absolute() or len(raw.parts) != 2 or raw.parts[0] != "generations":
            raise StoreError(f"accepted generation pointer escapes its store: {raw}")
        generation = raw.parts[1]
    tree, registry = load_registry(root, generation)
    return tree, generation, registry

def _copy_tree(target, source, entries):
    for item in entries:
        write(Path(target) / item["path"], _safe_file(
            Path(source) / item["path"], source).read_bytes())

def _write_registry(root, generation, pair_hash, eval_hash, entries, evaluation):
    write_json(_registry(root, generation), {
        "schema": 2, "generation": generation, "pair_hash": pair_hash,
        "evaluation_hash": eval_hash, "entries": entries, "evaluation": evaluation})
    _registry(root, generation).chmod(0o444)

def materialize(root, generation, entries, evaluation, pair_source, eval_source):
    """Create a complete hidden generation; never changes current visibility."""
    root, store = Path(root).absolute(), state_dir(root)
    safe_dir(root)
    safe_dir(root / "loop", root)
    store = ensure_dir(store, root)
    children = (store / "generations", store / "manifests")
    for child in children:
        if os.path.lexists(child):
            safe_dir(child, store)
    generations, _manifests = (ensure_dir(child, store) for child in children)
    target = generations / generation
    if target.exists():
        if target.is_symlink():
            raise StoreError(f"accepted generation is aliased: {target}")
        if _registry(root, generation).is_symlink():
            raise StoreError("accepted generation metadata is aliased")
        if not _registry(root, generation).exists():
            pair_hash = state_hash(exact_tree(target / "pair", entries))
            eval_hash = state_hash(exact_tree(target / "evaluation", evaluation))
            if generation != generation_hash(pair_hash, eval_hash):
                raise StoreError("incomplete generation cannot be recovered")
            _write_registry(root, generation, pair_hash, eval_hash, entries, evaluation)
        load_registry(root, generation)
        return target
    tmp = target.with_name(f".{generation}.rf02-tmp")
    discard_stage(tmp, store)
    try:
        _copy_tree(tmp / "pair", pair_source, entries)
        _copy_tree(tmp / "evaluation", eval_source, evaluation)
        pair_hash = state_hash(exact_tree(tmp / "pair", entries))
        eval_hash = state_hash(exact_tree(tmp / "evaluation", evaluation))
        if generation != generation_hash(pair_hash, eval_hash):
            raise StoreError("generation id does not match its complete inputs")
        for path in tree_files(tmp):
            path.chmod(0o444)
        os.replace(tmp, target)
        _sync(target.parent)
        _write_registry(root, generation, pair_hash, eval_hash, entries, evaluation)
        return target
    finally:
        discard_stage(tmp, store)

def switch(root, generation, interrupt=None):
    """Expose a complete generation with one same-directory os.replace."""
    store = state_dir(root)
    load_registry(root, generation)
    pointer, tmp = store / "current", store / ".current.rf02-tmp"
    expected = Path("generations") / generation
    if os.path.lexists(tmp):
        if os.name == "nt":
            try:
                valid = (_safe_file(tmp, store).read_bytes()
                         == (generation + "\n").encode("ascii"))
            except (OSError, StoreError):
                valid = False
        else:
            valid = tmp.is_symlink() and Path(os.readlink(tmp)) == expected
        if not valid:
            raise StoreError(f"stale pointer staging path is invalid: {tmp}")
        tmp.unlink()
    boundary = interrupt or (lambda _step: None)
    if os.name == "nt":
        with tmp.open("xb") as handle:
            handle.write((generation + "\n").encode("ascii"))
            handle.flush()
            os.fsync(handle.fileno())
        _safe_file(tmp, store)
    else:
        tmp.symlink_to(expected)
    try:
        _sync(store)
        boundary("pointer-prepared")
        os.replace(tmp, pointer)
        _sync(store)
        boundary("pointer-switched")
    finally:
        if tmp.exists() or tmp.is_symlink():
            tmp.unlink()

def same_filesystem(*paths):
    if len({Path(path).stat().st_dev for path in paths}) != 1:
        raise StoreError("candidate and accepted generations cross filesystems")

def freeze_files(root):
    for path in tree_files(root):
        path.chmod(0o444)

def exact_layout(root, manifest, expected=None):
    try:
        ER.recover(root, manifest, expected)
    except PG.PathError as exc:
        raise StoreError(str(exc)) from exc
    safe_dir(root)
    for name in ("candidate", "evaluation", "evidence"):
        if os.path.lexists(Path(root) / name):
            safe_dir(Path(root) / name, root)
    allowed = {"pair.json", "decision.json", "gate-decision.json",
               "candidate", "evaluation", "evidence", "writer-refusal-anchor.json"}
    operation = manifest.get("operation")
    if isinstance(operation, dict) and operation.get("path"):
        allowed.add(operation["path"])
    extra = {path.name for path in Path(root).iterdir()} - allowed
    if extra:
        raise StoreError(f"experiment contains undeclared entries: {sorted(extra)}")

def recovery_preflight(root):
    try:
        ER.preflight(root)
    except PG.PathError as exc:
        raise StoreError(str(exc)) from exc
