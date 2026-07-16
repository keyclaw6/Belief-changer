#!/usr/bin/env python3
"""Run H-F01 once its ledger and sealed-input preflight is ready."""
import argparse, json, os, shlex, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import candidate_pair as CP  # noqa: E402
import draft_batch_state as DRAFT  # noqa: E402
import hf01_preflight as HF  # noqa: E402
import legacy_guard as LG  # noqa: E402
import pair_store as PS  # noqa: E402
import path_guard as PG  # noqa: E402

FOLDER = "loop/experiments/h-f01-execution"
NO_PREVIOUS = "ABSENT — Chapter 1 has no previous chapter."


class RunError(RuntimeError): pass


def _resume(root):
    return shlex.join([sys.executable, str(HERE), "--snapshot-root", str(root),
                       "--redesign-authorized", "--rf-stage", "RF-23",
                       "--candidate-root", str(Path(root) / "loop/experiments")])


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


def _content(raw, number):
    try:
        value = json.loads(raw)
        text = value["choices"][0]["message"]["content"]
        if not isinstance(text, str): raise TypeError("content is not text")
        clean = DRAFT.clean_response(text.encode("utf-8"))
        DRAFT.validate_draft(clean, number)
        return clean
    except (UnicodeError, json.JSONDecodeError, KeyError, IndexError, TypeError,
            DRAFT.BatchError) as exc:
        raise RunError(f"H-F01 response for chapter {number} is invalid: {exc}") from exc


def _response(folder, root, authority, authority_sha, arm, number, prompt):
    call_id = f"write-{arm}-{number:02d}"
    marker, response = folder / f"{call_id}.call.json", folder / f"{call_id}.response.json"
    payload = _payload(prompt)
    expected = {"schema": 1, "call_id": call_id, "authority_sha256": authority_sha,
                "request_sha256": PS.state_hash(payload), "method": "POST", "url": HF.URL}
    if os.path.lexists(response):
        if not os.path.lexists(marker): raise RunError(f"{call_id}: response has no call marker")
        try: actual = json.loads(_read(marker, folder))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise RunError(f"{call_id}: call marker is malformed: {exc}") from exc
        if actual != expected: raise RunError(f"{call_id}: resumed request identity differs")
        return _content(_read(response, folder), number)
    if os.path.lexists(marker):
        raise RunError(f"{call_id}: orphan call marker blocks duplicate dispatch; resume: "
                       f"{_resume(root)}")
    _write_once(marker, PS.json_bytes(expected), root, authority)
    raw = _post(payload)
    _write_once(response, raw, root, authority)
    return _content(raw, number)


def _write_chapters(root, authority, drafts):
    arms = HF.arm_paths(root)
    for arm in ("control", "treatment"):
        experiment = arms[arm]["experiment"]
        for number in HF.CHAPTERS:
            HF.validate_execution_authority(root, authority)
            manifest = CP.inspect(experiment)
            path = arms[arm]["book"] / f"chapters/chapter-{number:02d}.md"
            try: current = CP.require_member(experiment, path, "product", manifest).read_bytes()
            except (CP.PairError, OSError) as exc: raise RunError(str(exc)) from exc
            wanted = drafts[(arm, number)]
            if current == wanted: continue
            baseline = authority["arms"][arm]["chapter_baseline_sha256"][str(number)]
            if PS.sha(current) != baseline:
                raise RunError(f"write-{arm}-{number:02d}: chapter differs from baseline and response")
            PS.write(path, wanted)


def _freeze(folder, root, authority, authority_sha, drafts):
    outputs, responses = [], []
    for arm in ("control", "treatment"):
        for number in HF.CHAPTERS:
            call_id = f"write-{arm}-{number:02d}"
            output = HF.arm_paths(root)[arm]["book"] / f"chapters/chapter-{number:02d}.md"
            response = folder / f"{call_id}.response.json"
            data = _read(output, root)
            if data != drafts[(arm, number)]:
                raise RunError(f"{call_id}: candidate output differs from durable response")
            outputs.append({"id": call_id, "path": str(output), "sha256": PS.sha(data)})
            responses.append({"id": call_id, "path": response.name,
                              "sha256": PS.sha(_read(response, folder))})
    receipt = {"schema": 1, "state": "FROZEN", "authority_sha256": authority_sha,
               "outputs": outputs, "raw_responses": responses,
               "automatic_stop": "freeze_all_six",
               "ordered_review_boundaries": list(HF.BOUNDARIES[1:])}
    receipt["receipt_sha256"] = PS.state_hash(receipt)
    path = folder / "frozen.json"
    if not os.path.lexists(path): _write_once(path, PS.json_bytes(receipt), root, authority)
    return verify_frozen(root, authority)


def verify_frozen(root, authority=None):
    root, folder = Path(root).absolute(), Path(root).absolute() / FOLDER
    if authority is None:
        authority = json.loads(_read(folder / "authority.json", folder))
    HF.validate_execution_authority(root, authority, key_present=True)
    try: receipt = json.loads(_read(folder / "frozen.json", folder))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise RunError(f"H-F01 freeze receipt is malformed: {exc}") from exc
    recorded = dict(receipt); receipt_hash = recorded.pop("receipt_sha256", None)
    if receipt_hash != PS.state_hash(recorded) or receipt.get("state") != "FROZEN":
        raise RunError("H-F01 freeze receipt identity is invalid")
    for item in receipt["outputs"]:
        if PS.sha(_read(item["path"], root)) != item["sha256"]:
            raise RunError(f"frozen H-F01 output changed: {item['id']}")
    for item in receipt["raw_responses"]:
        if PS.sha(_read(folder / item["path"], folder)) != item["sha256"]:
            raise RunError(f"frozen H-F01 response changed: {item['id']}")
    return receipt


def run(snapshot_root):
    root = Path(snapshot_root).absolute()
    folder, authority, authority_sha = _authority(root)
    if os.path.lexists(folder / "frozen.json"): return verify_frozen(root, authority)
    drafts = {}
    for arm in ("control", "treatment"):
        previous = NO_PREVIOUS
        for number in HF.CHAPTERS:
            draft = _response(folder, root, authority, authority_sha, arm, number,
                              _prompt(root, arm, number, previous))
            drafts[(arm, number)], previous = draft, draft.decode("utf-8")
    _write_chapters(root, authority, drafts)
    return _freeze(folder, root, authority, authority_sha, drafts)


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
