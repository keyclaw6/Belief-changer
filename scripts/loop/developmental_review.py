"""Pinned, isolated, monotonic RF-13 whole-opening review."""
import argparse
import os
import shlex
import stat
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "eval"))
import candidate_pair as CP  # noqa: E402
import developmental_review_authority as A  # noqa: E402
import developmental_review_call as DC  # noqa: E402
import developmental_review_contract as C  # noqa: E402
import developmental_review_lifecycle as L  # noqa: E402
import developmental_review_runtime as R  # noqa: E402
import legacy_guard as LG  # noqa: E402
import pair_store as PS  # noqa: E402


class DevelopmentalReviewError(RuntimeError):
    pass


class DevelopmentalReviewPending(DevelopmentalReviewError):
    pass


folder = DC.folder
task_path = DC.task_path
raw_path = DC.raw_path
transport_path = DC.transport_path


def receipt_path(root):
    return folder(root) / C.RECEIPT


def _authority(root, cfg=None):
    try:
        return A.load(root, cfg)
    except A.AuthorityError as exc:
        raise DevelopmentalReviewError(str(exc)) from exc


def _manifest(root):
    try:
        manifest = CP.load(root)
        state = L.status(root, manifest)
        return manifest, state
    except (CP.PairError, L.LifecycleError) as exc:
        raise DevelopmentalReviewError(str(exc)) from exc


def _result(root, task):
    try:
        raw, transport, hashes = DC.read(root, task)
        return raw, transport, hashes, C.verdict(raw, task)
    except (DC.CallError, C.ContractError, PS.StoreError, OSError) as exc:
        raise DevelopmentalReviewError(
            f"invalid developmental native result: {exc}") from exc


def prepare(root, cfg=None, interrupt=None):
    task, _ = _authority(root, cfg)
    manifest, state = _manifest(root)
    if manifest["state"] == "SEALED":
        raise DevelopmentalReviewError("SEALED operation cannot start developmental review")
    if state[1] == "COMMITTED":
        raise DevelopmentalReviewError("committed developmental review cannot be reissued")
    try:
        L.start(root, manifest, DC.binding(task),
                lambda: DC.prepare_local(root, task), interrupt)
        R.prepare(task)
        return task
    except (L.LifecycleError, DC.CallError, R.RuntimeError, PS.StoreError,
            OSError) as exc:
        raise DevelopmentalReviewError(
            f"developmental task preparation failed: {exc}") from exc


def _receipt(root, task, common):
    raw, transport, hashes, verdict = _result(root, task)
    del raw, transport
    evidence = {
        "task": {"path": "task.json", "sha256": hashes["task_file_sha256"],
                 "mode": "0444"},
        "schema": {"path": "schema.json", "sha256": hashes["schema_sha256"],
                   "mode": "0444"},
        "call": {"path": "call.json", "sha256": hashes["call_sha256"],
                 "mode": "0444"},
        "transport": {"path": "transport.json", "sha256": hashes["transport_sha256"],
                      "mode": "0444"},
        "raw": {"path": "verdict.raw.json", "sha256": hashes["raw_sha256"],
                "mode": "0444"}}
    body = {"schema": C.SCHEMA, "state": verdict["verdict"], **common,
            "task_sha256": task["task_sha256"], "evidence": evidence,
            "verdict": verdict}
    return {**body, "receipt_hash": PS.state_hash(body)}


def _descriptor(root, task, receipt):
    evidence = receipt["evidence"]
    call_data = PS._safe_file(DC.marker_path(root), folder(root)).read_bytes()
    marker = C.loads(call_data.decode("utf-8"), "developmental call marker")
    return {"task_sha256": task["task_sha256"],
            "task_file_sha256": evidence["task"]["sha256"],
            "schema_sha256": evidence["schema"]["sha256"],
            "call_id": marker["call_id"], "call_sha256": evidence["call"]["sha256"],
            "transport_sha256": evidence["transport"]["sha256"],
            "raw_sha256": evidence["raw"]["sha256"],
            "receipt_hash": receipt["receipt_hash"],
            "receipt_sha256": PS.sha(PS.json_bytes(receipt))}


def finalize(root, cfg=None, interrupt=None):
    task, common = _authority(root, cfg)
    manifest, state = _manifest(root)
    if state[1] == "COMMITTED":
        raise DevelopmentalReviewError("committed developmental review cannot be finalized again")
    value, target = _receipt(root, task, common), receipt_path(root)
    data = PS.json_bytes(value)
    try:
        if os.path.lexists(target):
            actual = PS._safe_file(target, folder(root)).read_bytes()
            if C.loads(actual.decode("utf-8"), "developmental receipt") != value \
                    or actual != data:
                raise DevelopmentalReviewError("developmental receipt already differs")
        else:
            PS.write(target, data, interrupt)
            target.chmod(0o444)
        descriptor = _descriptor(root, task, value)
        folder(root).chmod(0o555)
        L.commit(root, manifest, descriptor, interrupt)
        return require_complete(root, cfg, require_pass=False)
    except DevelopmentalReviewError:
        raise
    except (L.LifecycleError, PS.StoreError, OSError, UnicodeError,
            C.ContractError) as exc:
        raise DevelopmentalReviewError(
            f"developmental receipt commit failed: {exc}") from exc


def require_complete(root, cfg=None, require_pass=True):
    task, common = _authority(root, cfg)
    if not os.path.lexists(receipt_path(root)):
        raise DevelopmentalReviewError("developmental receipt is missing")
    try:
        expected = _receipt(root, task, common)
        data = PS._safe_file(receipt_path(root), folder(root)).read_bytes()
        actual = C.loads(data.decode("utf-8"), "developmental receipt")
        descriptor = _descriptor(root, task, expected)
        lifecycle = L.committed(root, CP.load(root))
        if actual != expected or data != PS.json_bytes(expected) \
                or descriptor != {key: lifecycle[key] for key in descriptor}:
            raise DevelopmentalReviewError("developmental receipt or lifecycle is stale")
        DC.validate_local(root, task, {"task.json", "schema.json", "call.json",
            "transport.json", "verdict.raw.json", C.RECEIPT})
        if stat.S_IMODE(os.lstat(folder(root)).st_mode) != 0o555:
            raise DevelopmentalReviewError("developmental folder mode is not canonical 0555")
    except DevelopmentalReviewError:
        raise
    except (DC.CallError, L.LifecycleError, PS.StoreError, OSError, UnicodeError,
            C.ContractError, CP.PairError) as exc:
        raise DevelopmentalReviewError(
            f"developmental evidence verification failed: {exc}") from exc
    if require_pass and actual["state"] != "PASS":
        raise DevelopmentalReviewError(
            "developmental NEEDS_CHANGES stops review, revision, and evaluation")
    return actual


def require_developmental_pass(root, cfg=None):
    return require_complete(root, cfg, require_pass=True)


def seal_identity(root, cfg=None):
    require_developmental_pass(root, cfg)
    try:
        return L.committed(root, CP.load(root))
    except (L.LifecycleError, CP.PairError) as exc:
        raise DevelopmentalReviewError(str(exc)) from exc


def advance(root, cfg=None, runner=None, interrupt=None):
    manifest, state = _manifest(root)
    if manifest["state"] == "SEALED":
        raise DevelopmentalReviewError("SEALED operation cannot advance developmental review")
    if state[1] == "COMMITTED":
        raise DevelopmentalReviewError("committed developmental review cannot be reissued")
    if os.path.lexists(receipt_path(root)):
        result = finalize(root, cfg, interrupt)
        if result["state"] != "PASS":
            raise DevelopmentalReviewError(
                "developmental NEEDS_CHANGES stops review, revision, and evaluation")
        return result
    task = prepare(root, cfg, interrupt)
    try:
        if os.path.lexists(DC.transport_path(root)):
            _result(root, task)
        elif R.result(task) is not None:
            DC.import_result(root, task, interrupt)
        else:
            created, _ = DC.start(root, task)
            if not created:
                raise DevelopmentalReviewError(
                    "marked developmental review has no result; replay is ambiguous")
            if runner is None:
                raise DevelopmentalReviewPending("developmental native dispatch is pending")
            result = runner({"task": task, "task_sha256": task["task_sha256"],
                             "command": DC.wrapper_command(task)})
            if isinstance(result, str):
                raise DevelopmentalReviewError("bare reviewer JSON lacks native proof")
            DC.import_result(root, task, interrupt)
        result = finalize(root, cfg, interrupt)
        if result["state"] != "PASS":
            raise DevelopmentalReviewError(
                "developmental NEEDS_CHANGES stops review, revision, and evaluation")
        return result
    except (DevelopmentalReviewPending, DevelopmentalReviewError):
        raise
    except (DC.CallError, R.RuntimeError, C.ContractError, PS.StoreError,
            OSError) as exc:
        raise DevelopmentalReviewError(f"developmental dispatch failed: {exc}") from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    LG.add_arguments(parser)
    parser.add_argument("--native", action="store_true")
    args = parser.parse_args()
    candidate = LG.require_authorized(
        args, entrypoint="developmental_review", pre_rf23_stage="RF-13")
    if LG.dry_run(args, "developmental_review"):
        return
    try:
        try:
            receipt = require_developmental_pass(candidate)
        except DevelopmentalReviewError:
            runner = None
            if args.native:
                import native_developmental_review as native
                runner = lambda dispatch: native.complete(dispatch["task_sha256"])
            receipt = advance(candidate, runner=runner)
        print(f"[developmental] complete PASS {receipt['receipt_hash']}")
    except DevelopmentalReviewPending as exc:
        task, _ = _authority(candidate)
        print(f"[developmental] dispatch once: {shlex.join(DC.wrapper_command(task))}")
        raise SystemExit(4) from exc
    except DevelopmentalReviewError as exc:
        raise SystemExit(f"[developmental] blocked: {exc}") from exc


if __name__ == "__main__":
    main()
