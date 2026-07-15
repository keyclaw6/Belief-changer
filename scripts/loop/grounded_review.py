"""Pinned, restartable RF-12 grounded review for one frozen draft batch."""
import argparse
import os
import shlex
import stat
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "eval"))
import grounded_review_authority as A  # noqa: E402
import grounded_review_call as GC  # noqa: E402
import grounded_review_contract as C  # noqa: E402
import legacy_guard as LG  # noqa: E402
import pair_store as PS  # noqa: E402


class GroundedReviewError(RuntimeError):
    pass


class GroundedReviewPending(GroundedReviewError):
    def __init__(self, missing):
        self.missing = missing
        super().__init__("grounded review native dispatch is pending")


folder = GC.folder
task_path = GC.task_path
raw_path = GC.raw_path
transport_path = GC.transport_path


def receipt_path(root):
    return folder(root) / C.RECEIPT


def _authority(root, cfg=None):
    try:
        return A.load(root, cfg)
    except A.AuthorityError as exc:
        raise GroundedReviewError(str(exc)) from exc


def _entries(root, tasks, receipt=False):
    entries = []
    for number in tasks:
        entries.extend((
            {"group": "evidence", "path": f"work/chapter-{number:02d}/task.json"},
            {"group": "evidence", "path": f"work/chapter-{number:02d}/schema.json"},
        ))
        for path in (GC.marker_path(root, number), GC.transport_path(root, number),
                     GC.raw_path(root, number)):
            if os.path.lexists(path):
                entries.append({"group": "evidence", "path": path.name})
    if receipt:
        entries.append({"group": "evidence", "path": C.RECEIPT})
    return entries


def _layout(root, tasks, receipt=False):
    try:
        GC.validate_workdirs(root, tasks)
        for number in tasks:
            marker = os.path.lexists(GC.marker_path(root, number))
            transport = os.path.lexists(GC.transport_path(root, number))
            raw = os.path.lexists(GC.raw_path(root, number))
            if transport and not marker or raw and not transport:
                raise GroundedReviewError("grounded call evidence order is invalid")
            if receipt and not (marker and transport and raw):
                raise GroundedReviewError("grounded receipt has partial call evidence")
        PS.exact_tree(folder(root), _entries(root, tasks, receipt))
    except (GC.CallError, PS.StoreError, OSError) as exc:
        raise GroundedReviewError(f"grounded evidence layout is invalid: {exc}") from exc


def prepare(root, cfg=None):
    tasks, _ = _authority(root, cfg)
    try:
        GC.prepare_workdirs(root, tasks)
        _layout(root, tasks, os.path.lexists(receipt_path(root)))
        return tasks
    except (GC.CallError, PS.StoreError, OSError) as exc:
        raise GroundedReviewError(f"grounded task preparation failed: {exc}") from exc


def _dispatch(root, task, marker):
    number = task["chapter"]
    return {"workdir": GC.workdir(root, number),
            "marker_path": GC.marker_path(root, number),
            "transport_path": GC.transport_path(root, number),
            "raw_path": GC.raw_path(root, number), "task": task, "marker": marker,
            "command": GC.wrapper_command(root, number)}


def _result(root, task):
    try:
        raw, transport, hashes = GC.read(root, task)
        return raw, transport, hashes, C.verdict(raw, task)
    except (GC.CallError, C.ContractError, PS.StoreError, OSError) as exc:
        raise GroundedReviewError(
            f"chapter {task['chapter']}: invalid grounded native result: {exc}") from exc


def _chapter(root, task):
    number = task["chapter"]
    raw, transport, hashes, verdict = _result(root, task)
    del raw, transport
    return {"chapter": number, "task_sha256": task["task_sha256"],
            "task": {"path": f"work/chapter-{number:02d}/task.json",
                     "sha256": hashes["task_file_sha256"], "mode": "0444"},
            "schema": {"path": f"work/chapter-{number:02d}/schema.json",
                       "sha256": hashes["schema_sha256"], "mode": "0444"},
            "call": {"path": f"call-{number:02d}.json",
                     "sha256": hashes["call_sha256"], "mode": "0444"},
            "transport": {"path": f"transport-{number:02d}.json",
                          "sha256": hashes["transport_sha256"], "mode": "0444"},
            "raw": {"path": f"verdict-{number:02d}.raw.json",
                    "sha256": hashes["raw_sha256"], "mode": "0444"},
            "verdict": verdict}


def _receipt(root, tasks, common):
    chapters = [_chapter(root, task) for task in tasks.values()]
    state = "PASSED" if all(item["verdict"]["verdict"] == "PASS"
                            for item in chapters) else "BLOCKED"
    body = {"schema": C.SCHEMA, "state": state, **common, "chapters": chapters}
    return {**body, "receipt_hash": PS.state_hash(body)}


def finalize(root, cfg=None):
    tasks, common = _authority(root, cfg)
    _layout(root, tasks, os.path.lexists(receipt_path(root)))
    missing = [number for number in tasks
               if not os.path.lexists(GC.transport_path(root, number))]
    if missing:
        raise GroundedReviewPending(missing)
    value = _receipt(root, tasks, common)
    path, data = receipt_path(root), PS.json_bytes(value)
    try:
        if os.path.lexists(path):
            actual = PS._safe_file(path, folder(root)).read_bytes()
            parsed = C.loads(actual.decode("utf-8"), "grounded receipt")
            if parsed != value or actual != data:
                raise GroundedReviewError("grounded receipt already differs")
        else:
            PS.write(path, data)
            path.chmod(0o444)
        return require_complete(root, cfg, require_pass=False)
    except (PS.StoreError, OSError, UnicodeError, C.ContractError) as exc:
        raise GroundedReviewError(f"grounded receipt write failed: {exc}") from exc


def require_complete(root, cfg=None, require_pass=True):
    tasks, common = _authority(root, cfg)
    if not os.path.lexists(receipt_path(root)):
        raise GroundedReviewError("grounded receipt is missing")
    try:
        GC.validate_workdirs(root, tasks)
        expected = _receipt(root, tasks, common)
        data = PS._safe_file(receipt_path(root), folder(root)).read_bytes()
        actual = C.loads(data.decode("utf-8"), "grounded receipt")
        if actual != expected or data != PS.json_bytes(expected):
            raise GroundedReviewError("grounded receipt is stale or tampered")
        _layout(root, tasks, True)
        for path in PS.tree_files(folder(root)):
            if stat.S_IMODE(os.lstat(path).st_mode) != 0o444:
                raise GroundedReviewError("grounded evidence mode is not canonical 0444")
    except (GC.CallError, PS.StoreError, OSError, UnicodeError, C.ContractError) as exc:
        raise GroundedReviewError(f"grounded evidence verification failed: {exc}") from exc
    if require_pass and actual["state"] != "PASSED":
        raise GroundedReviewError("unresolved grounded BLOCK stops downstream work")
    return actual


def advance(root, cfg=None, runner=None):
    tasks = prepare(root, cfg)
    pending = []
    for number, task in tasks.items():
        if os.path.lexists(GC.transport_path(root, number)):
            _result(root, task)
            continue
        try:
            created, marker = GC.start(root, task)
            if not created:
                _result(root, task)
            elif runner is None:
                pending.append(number)
            else:
                result = runner(_dispatch(root, task, marker))
                if isinstance(result, str):
                    raise GroundedReviewError("bare reviewer JSON lacks native transport proof")
                _result(root, task)
        except (GC.CallError, C.ContractError, PS.StoreError, OSError) as exc:
            raise GroundedReviewError(f"chapter {number}: grounded dispatch failed: {exc}") from exc
    if pending:
        raise GroundedReviewPending(pending)
    result = finalize(root, cfg)
    if result["state"] != "PASSED":
        raise GroundedReviewError("unresolved grounded BLOCK stops downstream work")
    return require_complete(root, cfg)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    LG.add_arguments(parser)
    parser.add_argument("--native", action="store_true")
    args = parser.parse_args()
    candidate = LG.require_authorized(
        args, entrypoint="grounded_review", pre_rf23_stage="RF-12")
    if LG.dry_run(args, "grounded_review"):
        return
    runner = None
    if args.native:
        import native_grounded_review as native
        runner = lambda dispatch: native.complete(
            dispatch["workdir"], dispatch["marker_path"],
            dispatch["transport_path"], dispatch["raw_path"])
    try:
        receipt = advance(candidate, runner=runner)
        print(f"[grounded] complete PASS {receipt['receipt_hash']}")
    except GroundedReviewPending as exc:
        for number in exc.missing:
            print(f"[grounded] dispatch once: {shlex.join(GC.wrapper_command(candidate, number))}")
        raise SystemExit(4) from exc
    except GroundedReviewError as exc:
        raise SystemExit(f"[grounded] blocked: {exc}") from exc


if __name__ == "__main__":
    main()
