#!/usr/bin/env python3
"""Run H-F01 through the accepted RF-11 first-draft batch lifecycle."""
import argparse, json, os, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import candidate_pair as CP  # noqa: E402
import first_draft_batch as FB  # noqa: E402
import hf01_control_authority as HCA  # noqa: E402
import hf01_preflight as HF  # noqa: E402
import legacy_guard as LG  # noqa: E402
import pair_store as PS  # noqa: E402
import path_guard as PG  # noqa: E402
import writer_context as WC  # noqa: E402

FOLDER = "loop/experiments/h-f01-execution"
NO_PREVIOUS = "ABSENT — Chapter 1 has no previous chapter."


class RunError(RuntimeError): pass


def _read(path, boundary):
    try: return PG.safe_file(path, boundary).read_bytes()
    except (PG.PathError, OSError) as exc: raise RunError(str(exc)) from exc


def _write_once(path, data, root, authority):
    HF.validate_execution_authority(root, authority)
    if os.path.lexists(path): raise RunError(f"immutable H-F01 evidence already exists: {path}")
    try:
        with path.open("xb") as handle:
            handle.write(data); handle.flush(); os.fchmod(handle.fileno(), 0o444)
            os.fsync(handle.fileno())
        PS._sync(path.parent)
    except OSError as exc: raise RunError(f"H-F01 evidence write failed: {exc}") from exc


def _authority(root):
    folder, path = root / FOLDER, root / FOLDER / "authority.json"
    if os.path.lexists(folder):
        try: PG.safe_dir(folder, root)
        except PG.PathError as exc: raise RunError(str(exc)) from exc
        if os.path.lexists(path):
            try: stored = json.loads(_read(path, folder))
            except (UnicodeError, json.JSONDecodeError) as exc:
                raise RunError(f"H-F01 authority evidence is malformed: {exc}") from exc
            HF.validate_execution_authority(root, stored)
            return folder, stored, PS.sha(_read(path, folder))
    else:
        manifest = HF.require_ready(root)
        HF.validate_execution_authority(root, manifest)
        try: PG.safe_dir(folder.parent, root); folder.mkdir(); PS._sync(folder.parent)
        except (PG.PathError, OSError) as exc: raise RunError(str(exc)) from exc
    manifest = HF.require_ready(root)
    if any(folder.iterdir()): raise RunError("H-F01 execution evidence lacks its authority")
    data = PS.json_bytes(manifest)
    _write_once(path, data, root, manifest)
    return folder, manifest, PS.sha(data)


def _text(path, boundary):
    try: return _read(path, boundary).decode("utf-8")
    except UnicodeError as exc: raise RunError(f"writer input is not UTF-8: {path}") from exc


def _target(number):
    return (f"Write Chapter {number} for quit-sugar now. Return only the complete final "
            "chapter prose, beginning with its chapter heading. No preamble, report, word "
            "count, or code fence.")


def _prompt(root, arm, number, previous):
    paths, book = HF.arm_paths(root)[arm], HF.arm_paths(root)[arm]["book"]
    if arm == "control":
        sections = (("frozen_full_style_guide", _text(paths["candidate"] /
                     "prompts/style-guide.md", root)),
                    ("current_full_master_plan", _text(book / "master-plan.md", root)))
    else:
        contract = _text(paths["candidate"] / "prompts/chapter-writer.md", root)
        contract = contract.replace("[N]", str(number)).replace("[SLUG]", "quit-sugar")
        sections = (("compact_writer_contract", contract),
                    ("audited_chapter_commission", _text(
                        book / f"commissions/chapter-{number:02d}.md", root)))
    sections += (("target_and_output_instruction", _target(number)),
                 ("immediately_previous_arm_chapter", previous))
    return "".join(f"===== {name} =====\n{value.rstrip()}\n\n" for name, value in sections)


def _payload(prompt):
    return {"model": HF.MODEL, "messages": [{"role": "user", "content": prompt}],
            "reasoning": {"effort": "none"}, "temperature": 0.7,
            "max_tokens": 16000}


def _post(payload):
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key: raise RunError("OPENROUTER_API_KEY is missing")
    request = urllib.request.Request(
        HF.URL, data=json.dumps(payload, separators=(",", ":")).encode(), method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=600) as response:
        return response.read()


def _reply(payload, number):
    try:
        value = json.loads(_post(payload))
        text = value["choices"][0]["message"]["content"]
        if not isinstance(text, str): raise TypeError("content is not text")
        return text
    except (UnicodeError, json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
        raise RunError(f"H-F01 response for chapter {number} is invalid: {exc}") from exc


def _require_arm_authority(root, arm, manifest):
    experiment, book = HF.arm_paths(root)[arm]["experiment"], HF.arm_paths(root)[arm]["book"]
    expected = manifest["operation"]["receipt_hash"]
    if arm == "control":
        HCA.require_resume(experiment, book, HF.CHAPTERS, expected)
    else:
        WC.require_manual_resume(experiment, book, HF.CHAPTERS, expected)


def _prepare_arm(root, arm):
    experiment, book = HF.arm_paths(root)[arm]["experiment"], HF.arm_paths(root)[arm]["book"]
    manifest = CP.load(experiment)
    try:
        if manifest.get("operation") is None:
            if arm == "control":
                captured = HCA.capture(experiment, book, HF.CHAPTERS)
                HCA.persist(experiment, captured)
            else:
                captured = WC.capture(experiment, book, HF.CHAPTERS)
                WC.persist_manual_receipt(experiment, captured)
            manifest = CP.load(experiment)
        _require_arm_authority(root, arm, manifest)
        return FB.begin(experiment, None, "api")
    except (HCA.ControlAuthorityError, WC.WriterContextError, FB.BatchError,
            CP.PairError, PS.StoreError, OSError) as exc:
        raise RunError(f"H-F01 {arm} writer authority failed: {exc}") from exc


def _generate_arm(root, authority, arm):
    experiment, book = HF.arm_paths(root)[arm]["experiment"], HF.arm_paths(root)[arm]["book"]
    if CP.load(experiment)["state"] == "BATCH_FROZEN":
        FB.require_frozen_batch(experiment); return
    _prepare_arm(root, arm)
    try: remaining = FB.prepare(experiment)
    except FB.BatchError as exc: raise RunError(f"H-F01 {arm} draft resume failed: {exc}") from exc
    for number in remaining:
        HF.validate_execution_authority(root, authority)
        previous = NO_PREVIOUS if number == 1 else _text(
            book / f"chapters/chapter-{number-1:02d}.md", root)
        payload = _payload(_prompt(root, arm, number, previous))
        request = {"method": "POST", "url": HF.URL, "payload": payload}
        try:
            FB.durable_call(experiment, number, request,
                            lambda p=payload, n=number: _reply(p, n))
            HF.validate_execution_authority(root, authority)
            FB.accept_response(experiment, number)
        except FB.BatchError as exc:
            raise RunError(f"H-F01 {arm} chapter {number} failed closed: {exc}") from exc


def verify_frozen(root, authority=None):
    root, folder = Path(root).absolute(), Path(root).absolute() / FOLDER
    if authority is None: authority = json.loads(_read(folder / "authority.json", folder))
    HF.validate_execution_authority(root, authority, key_present=True)
    arms = {}
    for arm, paths in HF.arm_paths(root).items():
        try: receipt = FB.require_frozen_batch(paths["experiment"])
        except FB.BatchError as exc: raise RunError(f"H-F01 {arm} batch is not frozen: {exc}") from exc
        responses = receipt["batch"]["responses"]
        arms[arm] = {"manifest_state": CP.load(paths["experiment"])["state"],
                     "receipt_hash": receipt["receipt_hash"],
                     "request_sha256": [item["request_sha256"] for item in responses]}
    return {"schema": 1, "experiment": "H-F01", "state": "BATCH_FROZEN",
            "authority_sha256": PS.sha(_read(folder / "authority.json", folder)),
            "arms": arms, "automatic_stop": "freeze_all_six",
            "ordered_review_boundaries": list(HF.BOUNDARIES[1:])}


def run(snapshot_root):
    root = Path(snapshot_root).absolute()
    _, authority, _ = _authority(root)
    for arm in ("control", "treatment"): _generate_arm(root, authority, arm)
    for paths in HF.arm_paths(root).values():
        if CP.load(paths["experiment"])["state"] != "BATCH_FROZEN":
            try: FB.freeze(paths["experiment"])
            except FB.BatchError as exc: raise RunError(f"H-F01 batch freeze failed: {exc}") from exc
    return verify_frozen(root, authority)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot-root", required=True)
    LG.add_arguments(parser)
    args = parser.parse_args()
    candidate = LG.require_authorized(args, entrypoint="hf01_run")
    if candidate != Path(args.snapshot_root).absolute() / "loop/experiments":
        raise SystemExit("RF-00 legacy guard: --candidate-root must equal "
                         "<snapshot-root>/loop/experiments")
    if LG.dry_run(args, "hf01_run"): return
    try: result = run(args.snapshot_root)
    except (RunError, HF.PreflightError) as exc: raise SystemExit(str(exc)) from exc
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__": main()
