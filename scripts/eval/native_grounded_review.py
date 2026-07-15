"""Run one RF-12 task in its isolated workdir and persist native proof."""
import argparse
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

import native_judge as N

ROOT = Path(__file__).resolve().parents[2]
LOOP = ROOT / "scripts" / "loop"
sys.path.insert(0, str(LOOP))
import grounded_review_call as GC  # noqa: E402
import grounded_review_contract as C  # noqa: E402
import pair_store as PS  # noqa: E402


class NativeError(RuntimeError):
    pass


def _load(workdir, marker_path, transport_path, raw_path):
    workdir = Path(workdir).absolute()
    match = re.fullmatch(r"chapter-(\d{2})", workdir.name)
    if not match or workdir.parent.name != "work" \
            or workdir.parent.parent.name != C.FOLDER \
            or workdir.parent.parent.parent.name != "evidence":
        raise NativeError("native grounded workdir is outside the exact task layout")
    number, root = int(match.group(1)), workdir.parents[3]
    expected_paths = (GC.marker_path(root, number), GC.transport_path(root, number),
                      GC.raw_path(root, number))
    supplied = tuple(Path(value).absolute() for value in
                     (marker_path, transport_path, raw_path))
    if supplied != expected_paths:
        raise NativeError("native grounded output path differs from its task layout")
    try:
        PS.safe_dir(workdir, GC.work_root(root))
        PS.exact_tree(workdir, [{"group": "evidence", "path": "task.json"},
                                {"group": "evidence", "path": "schema.json"}])
        task_data = PS._safe_file(GC.task_path(root, number), workdir).read_bytes()
        task = C.task(C.loads(task_data.decode("utf-8"), "grounded task"))
        schema_data = PS._safe_file(GC.schema_path(root, number), workdir).read_bytes()
        marker_data = PS._safe_file(expected_paths[0], GC.folder(root)).read_bytes()
        marker = C.loads(marker_data.decode("utf-8"), "grounded call marker")
    except (PS.StoreError, OSError, UnicodeError, C.ContractError) as exc:
        raise NativeError(f"native grounded task evidence is invalid: {exc}") from exc
    if task["chapter"] != number or task_data != PS.json_bytes(task) \
            or schema_data != PS.json_bytes(C.output_schema()) \
            or marker != GC.expected_marker(root, task) \
            or marker_data != PS.json_bytes(marker):
        raise NativeError("native grounded task, schema, or marker identity differs")
    for path, mode in ((workdir, 0o555), (GC.task_path(root, number), 0o444),
                       (GC.schema_path(root, number), 0o444),
                       (expected_paths[0], 0o444)):
        if stat.S_IMODE(os.lstat(path).st_mode) != mode:
            raise NativeError("native grounded task layout mode differs")
    if os.path.lexists(expected_paths[1]) or os.path.lexists(expected_paths[2]):
        raise NativeError("native grounded call already has durable output")
    return root, task, marker


def complete(workdir, marker_path, transport_path, raw_path, run=subprocess.run,
             interrupt=None):
    root, task, marker = _load(workdir, marker_path, transport_path, raw_path)
    command, content = marker["command"], GC.input_text(task)
    env = {name: os.environ[name] for name in N.NATIVE_ENV_ALLOWLIST if name in os.environ}
    try:
        result = run(command, input=content, text=True, capture_output=True,
                     cwd=workdir, env=env, check=False)
    except OSError as exc:
        raise NativeError(f"native grounded-review launch failed: {exc}") from exc
    if result.returncode:
        raise NativeError(f"native grounded-review exited {result.returncode}")
    try:
        raw, thread_id, usage = N._events(result.stdout)
    except ValueError as exc:
        raise NativeError(str(exc)) from exc
    runtime = {"exit_code": result.returncode, "thread_id": thread_id,
               "usage": usage, "command": command}
    try:
        return GC.persist(root, task, marker, raw, runtime, interrupt)
    except (GC.CallError, C.ContractError, PS.StoreError, OSError) as exc:
        raise NativeError(str(exc)) from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--marker", required=True)
    parser.add_argument("--transport", required=True)
    parser.add_argument("--raw", required=True)
    args = parser.parse_args()
    try:
        envelope = complete(args.workdir, args.marker, args.transport, args.raw)
    except NativeError as exc:
        raise SystemExit(f"native-grounded-review: {exc}") from exc
    print(f"native-grounded-review: persisted {envelope['call_id']}")


if __name__ == "__main__":
    main()
