#!/usr/bin/env python3
"""Resume authority-bound H-F01 through the accepted first-draft lifecycle."""
import argparse, json, os, sys, urllib.request
from pathlib import Path
HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import candidate_pair as CP  # noqa: E402
import first_draft_batch as FB  # noqa: E402
import hf01_control_authority as HCA  # noqa: E402
import hf01_preflight as HF  # noqa: E402
import hf01_stage_a as STAGE  # noqa: E402
import hf01_upstream as UP  # noqa: E402
import legacy_guard as LG  # noqa: E402
import pair_store as PS  # noqa: E402
import path_guard as PG  # noqa: E402
import writer_context as WC  # noqa: E402
import immutable_file as IF  # noqa: E402
FOLDER = STAGE.FOLDER
NO_PREVIOUS = "ABSENT — Chapter 1 has no previous chapter."
class RunError(RuntimeError): pass
def _read(path, boundary):
    try: return PG.safe_file(path, boundary).read_bytes()
    except (PG.PathError, OSError) as exc: raise RunError(str(exc)) from exc
def _write_once(path, data, root, authority):
    HF.validate_execution_authority(root, authority)
    try:
        IF.write_once(path, data, lambda item: _read(item, item.parent), "H-F01 evidence")
    except IF.ImmutableFileError as exc: raise RunError(str(exc)) from exc
def _authority(root, timestamp):
    folder, path = root / FOLDER, root / FOLDER / "authority.json"
    if os.path.lexists(folder):
        try: PG.safe_dir(folder, root)
        except PG.PathError as exc: raise RunError(str(exc)) from exc
        if os.path.lexists(path):
            try: stored = json.loads(_read(path, folder))
            except (UnicodeError, json.JSONDecodeError) as exc:
                raise RunError(f"H-F01 authority evidence is malformed: {exc}") from exc
            HF.validate_execution_authority(root, stored)
            if timestamp and stored["frozen_at_utc"] != timestamp:
                raise RunError("resume authority timestamp differs")
            return folder, stored, PS.sha(_read(path, folder))
    else:
        manifest = HF.require_ready(root, authority_timestamp=timestamp)
        HF.validate_execution_authority(root, manifest)
        try:
            if not os.path.lexists(folder.parent): PG.safe_dir(folder.parent.parent, root); folder.parent.mkdir()
            else: PG.safe_dir(folder.parent, root)
            folder.mkdir(); PS._sync(folder.parent)
        except (PG.PathError, OSError) as exc: raise RunError(str(exc)) from exc
    manifest = HF.require_ready(root, authority_timestamp=timestamp)
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
WRITER_SETTINGS = {"model": HF.MODEL, "reasoning": {"effort": "high"},
                   "temperature": 0.7, "max_tokens": 16000,
                   "provider": {"allow_fallbacks": False}}
def _payload(prompt):
    return {"model": HF.MODEL, "messages": [{"role": "user", "content": prompt}],
            "reasoning": {"effort": "high"}, "temperature": 0.7,
            "max_tokens": 16000, "provider": {"allow_fallbacks": False}}
def _post(payload):
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key: raise RunError("OPENROUTER_API_KEY is missing")
    request = urllib.request.Request(
        HF.URL, data=json.dumps(payload, separators=(",", ":")).encode(), method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "X-OpenRouter-Metadata": "enabled"})
    with urllib.request.urlopen(request, timeout=600) as response: return response.read()
def _credit_check(open_url=urllib.request.urlopen):
    try:
        return HF.authenticated_preflight(open_url=open_url)
    except HF.PreflightError as exc: raise RunError(str(exc)) from exc
def _authenticated_preflight(root, authority, authority_sha, check, location_check=None):
    path = Path(root) / FOLDER / "openrouter-preflight.json"
    expected_location = {"source": HF.LOCATION_URL, "country_code": "US"}
    if os.path.lexists(path):
        try: value = json.loads(_read(path, path.parent))
        except (UnicodeError, json.JSONDecodeError) as exc: raise RunError(f"invalid frozen OpenRouter preflight: {exc}") from exc
        if value.get("schema") != 1 or value.get("authority_sha256") != authority_sha \
                or value.get("model") != HF.MODEL or value.get("canonical_model") != HF.CANONICAL_MODEL \
                or value.get("current_request_location") != expected_location:
            raise RunError("frozen OpenRouter preflight binding is stale")
        try: current = (location_check or HF.current_location)()
        except HF.PreflightError as exc: raise RunError(str(exc)) from exc
        if current != value["current_request_location"]:
            raise RunError("current OpenRouter edge location differs from frozen US proof")
        return value
    result = check()
    if not isinstance(result, dict) or result.get("model") != HF.MODEL \
            or result.get("canonical_model") != HF.CANONICAL_MODEL \
            or result.get("current_request_location") != expected_location:
        raise RunError("authenticated OpenRouter preflight returned no valid route proof")
    value = {"schema": 1, "authority_sha256": authority_sha, **result}
    _write_once(path, PS.json_bytes(value), root, authority)
    return value
def _upstream(root, authority, authority_sha, native, dispatch_stage=None):
    try:
        if dispatch_stage in ("RF-21", "RF-22"):
            HF.require_stage(authority, dispatch_stage)
            return UP.dispatch_stage(root, authority, authority_sha, dispatch_stage), dispatch_stage
        return UP.verify(root, authority, authority_sha), None
    except UP.UpstreamPending as exc:
        missing = "RF-21" if exc.path.name == UP.RF21_PATH else "RF-22"
        command = HF.resume_command(authority, stage=missing, native=True)
        raise STAGE.StagePending(f"{missing.lower()}-authority-bound-native-tasks",
            [command], HF.resume_command(authority, stage=missing)) from exc
    except UP.UpstreamError as exc: raise RunError(str(exc)) from exc
def _proof_folder(root):
    return HF.arm_paths(root)["treatment"]["experiment"] / "evidence/hf01/writer-route"
def _route_proof(root, authority, authority_sha, arm, number, payload, response, text):
    metadata, response_model = response.get("openrouter_metadata"), response.get("model")
    if not isinstance(metadata, dict): raise RunError("H-F01 response lacks OpenRouter route metadata")
    endpoints, attempts = metadata.get("endpoints"), metadata.get("attempts")
    attempts_present = "attempts" in metadata
    available = endpoints.get("available") if isinstance(endpoints, dict) else None
    selected = [item for item in available or () if isinstance(item, dict) and item.get("selected") is True]
    attempts_valid = not attempts_present or (
        isinstance(attempts, list) and len(attempts) == 1
        and isinstance(attempts[0], dict)
        and attempts[0].get("provider") == "Meta"
        and attempts[0].get("model") == HF.CANONICAL_MODEL
        and attempts[0].get("status") == 200)
    if metadata.get("requested") != HF.MODEL or metadata.get("strategy") != "direct" \
            or metadata.get("attempt") != 1 or not isinstance(endpoints, dict) \
            or endpoints.get("total") != 1 or not isinstance(available, list) or len(available) != 1 \
            or len(selected) != 1 or selected[0].get("provider") != "Meta" \
            or selected[0].get("model") != HF.CANONICAL_MODEL \
            or not attempts_valid \
            or response_model != HF.CANONICAL_MODEL:
        raise RunError("H-F01 response proves fallback, retry, or noncanonical routing")
    if "models" in payload or "fallbacks" in payload or any(payload.get(key) != value for key, value in WRITER_SETTINGS.items()):
        raise RunError("H-F01 writer request settings are not exact")
    folder = _proof_folder(root)
    if os.path.lexists(folder):
        try: existing = list(PG.files(folder, HF.arm_paths(root)["treatment"]["experiment"]))
        except PG.PathError as exc: raise RunError(str(exc)) from exc
        if len(existing) >= 6: raise RunError("H-F01 seventh writer call is forbidden")
    else:
        PG.ensure_dir(folder)
    chapter = FB.S.clean_response(text.encode("utf-8"))
    route_metadata = {key: metadata[key] for key in
        ("requested", "strategy", "attempt", "endpoints")}
    if attempts_present: route_metadata["attempts"] = attempts
    body = {"schema": 1, "authority_sha256": authority_sha, "arm": arm,
        "chapter": number, "request_sha256": PS.state_hash(payload),
        "requested_model": HF.MODEL, "response_model": response_model,
        "provider": selected[0]["provider"], "chapter_sha256": PS.sha(chapter),
        "openrouter_metadata": route_metadata}
    path = folder / f"{arm}-chapter-{number:02d}.json"
    _write_once(path, PS.json_bytes(body), root, authority)
    return text
def _reply(payload, arm, number, root, authority, authority_sha):
    try:
        value = json.loads(_post(payload))
        text = value["choices"][0]["message"]["content"]
        if not isinstance(text, str): raise TypeError("content is not text")
        return _route_proof(root, authority, authority_sha, arm, number, payload, value, text)
    except (UnicodeError, json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
        raise RunError(f"H-F01 response for chapter {number} is invalid: {exc}") from exc
def _require_arm_authority(root, arm, manifest):
    experiment, book = HF.arm_paths(root)[arm]["experiment"], HF.arm_paths(root)[arm]["book"]
    expected = manifest["operation"]["receipt_hash"]
    if arm == "control":
        HCA.require_resume(experiment, book, HF.CHAPTERS, expected)
    else: WC.require_manual_resume(experiment, book, HF.CHAPTERS, expected)
def _prepare_arm(root, authority_sha, arm):
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
        return FB.begin(experiment, authority_sha, "api")
    except (HCA.ControlAuthorityError, WC.WriterContextError, FB.BatchError,
            CP.PairError, PS.StoreError, OSError) as exc:
        raise RunError(f"H-F01 {arm} writer authority failed: {exc}") from exc
def _generate_arm(root, authority, authority_sha, arm, ensure_credit):
    experiment, book = HF.arm_paths(root)[arm]["experiment"], HF.arm_paths(root)[arm]["book"]
    manifest = CP.load(experiment)
    if manifest["state"] in ("BATCH_FROZEN", "SEALED"):
        _prepare_arm(root, authority_sha, arm); FB.require_frozen_batch(experiment); return
    if manifest.get("draft_batch") is None: ensure_credit()
    batch = _prepare_arm(root, authority_sha, arm)
    try: remaining = FB.prepare(experiment)
    except FB.BatchError as exc: raise RunError(f"H-F01 {arm} draft resume failed: {exc}") from exc
    if remaining: ensure_credit()
    for number in remaining:
        HF.validate_execution_authority(root, authority)
        previous = NO_PREVIOUS if number == 1 else _text(
            book / f"chapters/chapter-{number-1:02d}.md", root)
        payload = _payload(_prompt(root, arm, number, previous))
        request = {"method": "POST", "url": HF.URL,
            "h_f01_authority_sha256": authority_sha,
            "draft_batch_start_sha256": batch["start_sha256"], "payload": payload}
        try:
            FB.durable_call(experiment, number, request,
                            lambda p=payload, a=arm, n=number: _reply(
                                p, a, n, root, authority, authority_sha))
            HF.validate_execution_authority(root, authority)
            FB.accept_response(experiment, number)
        except FB.BatchError as exc:
            raise RunError(f"H-F01 {arm} chapter {number} failed closed: {exc}") from exc


def verify_frozen(root, authority=None):
    root = HF.require_authorized_root(root); folder = root / FOLDER
    if authority is None: authority = json.loads(_read(folder / "authority.json", folder))
    HF.validate_execution_authority(root, authority, key_present=True)
    authority_sha = PS.sha(_read(folder / "authority.json", folder))
    arms = {}
    proof_folder = _proof_folder(root)
    try: proof_paths = list(PG.files(proof_folder, HF.arm_paths(root)["treatment"]["experiment"]))
    except PG.PathError as exc: raise RunError(str(exc)) from exc
    if len(proof_paths) != 6: raise RunError("H-F01 requires exactly six writer route proofs")
    for arm, paths in HF.arm_paths(root).items():
        try: receipt = FB.require_frozen_batch(paths["experiment"])
        except FB.BatchError as exc: raise RunError(f"H-F01 {arm} batch is not frozen: {exc}") from exc
        batch, responses = receipt["batch"], receipt["batch"]["responses"]
        expected = []
        for number in HF.CHAPTERS:
            previous = NO_PREVIOUS if number == 1 else _text(
                paths["book"] / f"chapters/chapter-{number-1:02d}.md", root)
            request = {"method": "POST", "url": HF.URL,
                "h_f01_authority_sha256": authority_sha,
                "draft_batch_start_sha256": batch["start_sha256"],
                "payload": _payload(_prompt(root, arm, number, previous))}
            expected.append(PS.state_hash(request))
            proof_path = proof_folder / f"{arm}-chapter-{number:02d}.json"
            try: proof = json.loads(_read(proof_path, proof_folder))
            except (UnicodeError, json.JSONDecodeError) as exc: raise RunError(f"invalid writer route proof: {exc}") from exc
            chapter = _read(paths["book"] / f"chapters/chapter-{number:02d}.md", root)
            if proof.get("authority_sha256") != authority_sha or proof.get("arm") != arm \
                    or proof.get("chapter") != number \
                    or proof.get("request_sha256") != PS.state_hash(request["payload"]) \
                    or proof.get("requested_model") != HF.MODEL \
                    or proof.get("response_model") != HF.CANONICAL_MODEL \
                    or proof.get("provider") != "Meta" or proof.get("chapter_sha256") != PS.sha(chapter):
                raise RunError(f"H-F01 {arm} chapter {number} route proof is stale")
        if batch.get("authority_sha256") != authority_sha \
                or any(item["authority_sha256"] != batch["start_sha256"] for item in responses) \
                or [item["request_sha256"] for item in responses] != expected:
            raise RunError(f"H-F01 {arm} writer calls do not bind the frozen authority")
        arms[arm] = {"manifest_state": CP.load(paths["experiment"])["state"],
                     "receipt_hash": receipt["receipt_hash"],
                     "request_sha256": [item["request_sha256"] for item in responses]}
    return {"schema": 1, "experiment": "H-F01", "state": "BATCH_FROZEN",
            "authority_sha256": authority_sha,
            "arms": arms, "automatic_stop": "freeze_all_six",
            "ordered_review_boundaries": list(HF.BOUNDARIES[1:])}


def run(snapshot_root, credit_check=_credit_check, native=False,
        authority_timestamp=None, decision_timestamp=None, promote_pair=False,
        upstream_stage=None, location_check=None):
    root = HF.require_authorized_root(snapshot_root)
    _, authority, authority_sha = _authority(root, authority_timestamp)
    upstream_sha, completed_stage = _upstream(
        root, authority, authority_sha, native, upstream_stage)
    if completed_stage is not None:
        return {"schema": 1, "experiment": "H-F01",
            "state": f"{completed_stage.replace('-', '')}_COMPLETE_PAUSED",
            "authority_sha256": authority_sha, "upstream_receipt_sha256": upstream_sha,
            "automatic_stop": completed_stage,
            "next_command": HF.resume_command(authority,
                stage="RF-22" if completed_stage == "RF-21" else "RF-23")}
    HF.require_stage(authority, "RF-23")
    checked = all(CP.load(paths["experiment"])["state"] in ("BATCH_FROZEN", "SEALED")
                  for paths in HF.arm_paths(root).values())
    preflight_path = root / FOLDER / "openrouter-preflight.json"
    if os.path.lexists(preflight_path) or not checked:
        _authenticated_preflight(root, authority, authority_sha, credit_check,
                                 location_check)
        checked = True
    def ensure_credit():
        nonlocal checked
        if not checked: credit_check(); checked = True
    for arm in ("control", "treatment"):
        _generate_arm(root, authority, authority_sha, arm, ensure_credit)
    for paths in HF.arm_paths(root).values():
        if CP.load(paths["experiment"])["state"] not in ("BATCH_FROZEN", "SEALED"):
            try: FB.freeze(paths["experiment"])
            except FB.BatchError as exc: raise RunError(f"H-F01 batch freeze failed: {exc}") from exc
    verify_frozen(root, authority)
    return STAGE.advance(root, authority, upstream_sha, native=native,
                         decision_timestamp=decision_timestamp, promote_pair=promote_pair)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot-root", required=True)
    parser.add_argument("--authority-timestamp")
    parser.add_argument("--decision-timestamp")
    parser.add_argument("--promote-pair", action="store_true")
    parser.add_argument("--native", action="store_true",
                        help="dispatch pending native RF21/RF22 and review calls")
    LG.add_arguments(parser)
    args = parser.parse_args()
    pre_stage = args.rf_stage if args.rf_stage in ("RF-21", "RF-22") else None
    candidate = LG.require_authorized(args, entrypoint="hf01_run", pre_rf23_stage=pre_stage,
        exact_candidate=HF.AUTHORIZED_ROOT / "loop/experiments",
        require_in_progress=pre_stage is not None)
    if candidate != Path(args.snapshot_root).absolute() / "loop/experiments":
        raise SystemExit("RF-00 legacy guard: --candidate-root must equal "
                         "<snapshot-root>/loop/experiments")
    if LG.dry_run(args, "hf01_run"): return
    try: result = run(args.snapshot_root, native=args.native,
        authority_timestamp=args.authority_timestamp,
        decision_timestamp=args.decision_timestamp, promote_pair=args.promote_pair,
        upstream_stage=args.rf_stage if args.native and args.rf_stage in ("RF-21", "RF-22") else None)
    except STAGE.StagePending as exc:
        for command in exc.commands: print(f"[H-F01] dispatch: {command}")
        print(f"[H-F01] resume: {exc.resume}")
        raise SystemExit(4) from exc
    except (RunError, HF.PreflightError, STAGE.StageError) as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__": main()
