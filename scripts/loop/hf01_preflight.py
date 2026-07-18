#!/usr/bin/env python3
"""Pure H-F01 readiness manifest. It never sends, creates, or mutates files."""
import argparse, hashlib, json, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import candidate_pair as CP  # noqa: E402
import commission_set as CS  # noqa: E402
import hf01_control_authority as HCA  # noqa: E402
import loopcfg  # noqa: E402
import pair_store as PS  # noqa: E402
import path_guard as PG  # noqa: E402

REPO = HERE.parents[2]
CONFIG = REPO / "loop/config.yaml"
LEDGER = REPO / "openspec/changes/redesign-book-factory/tasks.md"
BOOK = "production-books/quit-sugar"
CHAPTERS = (1, 2, 3)
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "anthropic/claude-opus-4.6"
ROUTE_CONFIG = {"writer_model": MODEL, "writer_provider": "openrouter",
                "writer_reasoning": "none", "writer_endpoint": URL,
                "writer_temperature": 0.7, "writer_max_tokens": 16000,
                "writer_attempts": 1}
RUBRICS = ("calibration/judges/product-effect-rubric.md",
           "calibration/judges/product-effect-absolute-rubric.md")
INSTRUMENTS = ("scripts/loop/product_effect.py",
               "scripts/loop/product_effect_absolute.py")
BOUNDARIES = ("freeze_all_six", "grounded_integrity_and_near_copy_all_six",
              "developmental_reader_state_and_sequence", "absolute_observations",
              "paired_blind_comparisons", "carr_craft_diagnostic_after_blind",
              "named_human_comparison", "rf02_atomic_promotion_after_full_pass")


class PreflightError(RuntimeError): pass


def _sha(data): return hashlib.sha256(data).hexdigest()


def _safe_bytes(path, boundary):
    try: return PG.safe_file(path, boundary).read_bytes()
    except (PG.PathError, OSError) as exc: raise PreflightError(str(exc)) from exc


def _status(ledger, task):
    try: text = _safe_bytes(ledger, Path(ledger).absolute().parent).decode()
    except (PreflightError, UnicodeError): return "MISSING"
    match = re.search(rf"^### {re.escape(task)}\b(?P<body>.*?)(?=^### RF-|\Z)",
                      text, re.MULTILINE | re.DOTALL)
    status = re.search(r"^- Status: `([A-Z_]+)`$", match.group("body"), re.MULTILINE) \
        if match else None
    return status.group(1) if status else "MISSING"


def arm_paths(root):
    root = Path(root).absolute()
    return {arm: {"experiment": root / f"loop/experiments/h-f01-{arm}",
                  "candidate": root / f"loop/experiments/h-f01-{arm}/candidate",
                  "book": root / f"loop/experiments/h-f01-{arm}/candidate/{BOOK}"}
            for arm in ("control", "treatment")}


def _block(blockers, code, detail=None, path=None, kind="static_input"):
    item = {"class": kind, "code": code}
    if detail: item["detail"] = detail
    if path: item["path"] = str(path)
    blockers.append(item)


def _route(path, blockers, code):
    try: cfg = loopcfg.load(PG.safe_file(path, path.parent.parent))
    except (PG.PathError, SystemExit, OSError) as exc:
        _block(blockers, code, str(exc), path); return
    if any(cfg.get(key) != value for key, value in ROUTE_CONFIG.items()):
        _block(blockers, code, "fixed writer route or budget differs", path)


def _inspect_arm(arm, paths, blockers):
    try:
        manifest = CP.inspect(paths["experiment"])
        pair_hash, evaluation_hash = CP._actual(paths["experiment"], manifest)
    except (CP.PairError, PS.StoreError, OSError) as exc:
        _block(blockers, f"RF02_{arm.upper()}_INVALID", str(exc), paths["experiment"])
        return None, None, None
    run = manifest["run"]
    if run["book"] != BOOK or tuple(run["chapters"]) != CHAPTERS:
        _block(blockers, f"RF02_{arm.upper()}_RUN_MISMATCH", path=paths["experiment"])
    return manifest, pair_hash, evaluation_hash


def _shared_paths(manifest):
    prefix = f"{BOOK}/research/sources/"
    paths = {item["path"] for item in manifest["entries"]
             if item["path"].startswith(prefix) and item["path"].endswith(".md")}
    paths |= {f"{BOOK}/{name}" for name in
              ("research/lived-experience.md", "research/scientific-evidence.md")}
    return sorted(paths)


def _record(hashes, key, path, boundary):
    hashes[key] = _sha(_safe_bytes(path, boundary))


def _stable_hashes(root, arms, manifests, ledger, blockers):
    hashes = {}
    targets = {f"{BOOK}/chapters/chapter-{number:02d}.md" for number in CHAPTERS}
    try:
        for arm, manifest in manifests.items():
            if manifest is None: continue
            paths, candidate = arms[arm], arms[arm]["candidate"]
            for item in manifest["entries"] + manifest["outputs"]:
                if item["path"] not in targets:
                    _record(hashes, f"snapshot:{(candidate / item['path']).relative_to(root)}",
                            candidate / item["path"], root)
            for item in manifest["evaluation"]:
                path = paths["experiment"] / "evaluation" / item["path"]
                _record(hashes, f"snapshot:{path.relative_to(root)}", path, root)
        receipt = arms["treatment"]["experiment"] / "evidence" / CS.RECEIPT
        _record(hashes, f"snapshot:{receipt.relative_to(root)}", receipt, root)
        for rel in (*INSTRUMENTS, *RUBRICS, "prompts/style-guide.md",
                    "prompts/chapter-writer.md", "loop/config.yaml"):
            _record(hashes, f"repo:{rel}", REPO / rel, REPO)
        ledger_hash = _sha(_safe_bytes(ledger, Path(ledger).absolute().parent))
    except (PreflightError, ValueError) as exc:
        _block(blockers, "STATIC_AUTHORITY_INVALID", str(exc)); ledger_hash = None
    return hashes, ledger_hash


def _compare_shared(root, arms, manifests, blockers):
    if not all(manifests.values()): return []
    left, right = (_shared_paths(manifests[arm]) for arm in ("control", "treatment"))
    if left != right or not any("/research/sources/" in path for path in left):
        _block(blockers, "SHARED_RESEARCH_MEMBERSHIP_DIFFERS"); return left
    for rel in left:
        try:
            values = [_safe_bytes(arms[arm]["candidate"] / rel, root)
                      for arm in ("control", "treatment")]
        except PreflightError as exc:
            _block(blockers, "SHARED_RESEARCH_INVALID", str(exc), rel); continue
        if values[0] != values[1]: _block(blockers, "SHARED_RESEARCH_DIFFERS", path=rel)
    return left


def _current_assets(root, arms, blockers):
    comparisons = [(arms["control"]["candidate"] / "prompts/style-guide.md",
                    REPO / "prompts/style-guide.md", "CONTROL_STYLE_NOT_CURRENT"),
                   (arms["treatment"]["candidate"] / "prompts/chapter-writer.md",
                    REPO / "prompts/chapter-writer.md", "WRITER_CONTRACT_NOT_CURRENT")]
    for rel in RUBRICS:
        comparisons += [(arms[arm]["experiment"] / "evaluation" / rel,
                         REPO / rel, "SEALED_RUBRIC_NOT_CURRENT")
                        for arm in ("control", "treatment")]
    for actual, current, code in comparisons:
        try: equal = _safe_bytes(actual, root) == _safe_bytes(current, REPO)
        except PreflightError as exc:
            _block(blockers, code, str(exc), actual); continue
        if not equal: _block(blockers, code, path=actual)


def build_manifest(snapshot_root, key_present=None, ledger=None, config=CONFIG):
    root, ledger = Path(snapshot_root).absolute(), Path(ledger or LEDGER).absolute()
    arms, blockers = arm_paths(root), []
    _route(Path(config).absolute(), blockers, "WRITER_ROUTE_CONFIG_MISMATCH")
    manifests, arm_state = {}, {}
    for arm, paths in arms.items():
        manifest, pair_hash, evaluation_hash = _inspect_arm(arm, paths, blockers)
        manifests[arm] = manifest
        arm_state[arm] = {"pair_sha256": pair_hash, "evaluation_sha256": evaluation_hash}
        if manifest:
            arm_state[arm]["manifest_assignment_sha256"] = \
                PS.state_hash(HCA.assignment(manifest))
            arm_state[arm]["chapter_baseline_sha256"] = {
                str(number): _sha(_safe_bytes(paths["book"] /
                    f"chapters/chapter-{number:02d}.md", root)) for number in CHAPTERS}
        _route(paths["candidate"] / "loop/config.yaml", blockers,
               f"{arm.upper()}_ROUTE_CONFIG_MISMATCH")
    if all(manifests.values()):
        identity = {(m["accepted_generation"], m["accepted_pair_hash"],
                     m["accepted_evaluation_hash"]) for m in manifests.values()}
        if len(identity) != 1: _block(blockers, "RF02_ARMS_NOT_MATCHED")
    try: arm_state["treatment"]["commission_receipt_sha256"] = \
            CS.inspect_writer_eligible(arms["treatment"]["experiment"])
    except CS.CommissionSetError as exc:
        _block(blockers, "COMMISSION_SET_INELIGIBLE", str(exc),
               arms["treatment"]["experiment"])
    shared = _compare_shared(root, arms, manifests, blockers)
    _current_assets(root, arms, blockers)
    hashes, ledger_hash = _stable_hashes(root, arms, manifests, ledger, blockers)
    rf20, rf23 = _status(ledger, "RF-20"), _status(ledger, "RF-23")
    if rf20 != "DONE": _block(blockers, "RF20_NOT_DONE", rf20, kind="product_authority")
    if rf23 not in ("READY", "DONE"):
        _block(blockers, "RF23_NOT_READY", rf23, kind="product_authority")
    present = bool(os.environ.get("OPENROUTER_API_KEY", "").strip()) \
        if key_present is None else bool(key_present)
    if not present: _block(blockers, "OPENROUTER_API_KEY_MISSING", kind="credential_machine")
    blockers.sort(key=lambda item: (item["class"], item["code"], item.get("path", "")))
    return {"schema": 2, "experiment": "H-F01", "mode": "NO_SEND_PREFLIGHT",
            "snapshot_root": str(root), "chapters": list(CHAPTERS),
            "route": {"method": "POST", "url": URL, "model": MODEL,
                      "reasoning": {"effort": "none"}, "temperature": 0.7,
                      "max_tokens": 16000, "attempts": 1, "fallbacks": []},
            "credential": {"name": "OPENROUTER_API_KEY", "present": present},
            "authority": {"rf20_status": rf20, "rf23_status": rf23,
                          "ledger_path": str(ledger), "ledger_sha256": ledger_hash},
            "arms": arm_state, "static_input_sha256": hashes,
            "shared_research_and_safety": shared,
            "post_write_boundaries": [{"order": index + 1, "name": name,
                                        "automatic": index == 0}
                                       for index, name in enumerate(BOUNDARIES)],
            "automatic_stop": "freeze_all_six", "ready_to_send": not blockers,
            "blockers": blockers}


def require_ready(root, **kwargs):
    manifest = build_manifest(root, **kwargs)
    if not manifest["ready_to_send"]:
        raise PreflightError("H-F01 blocked: " + ", ".join(
            item["code"] for item in manifest["blockers"]))
    return manifest


def validate_execution_authority(root, manifest, key_present=None):
    authority = manifest["authority"]
    if (_status(authority["ledger_path"], "RF-20"),
            _status(authority["ledger_path"], "RF-23")) != ("DONE", authority["rf23_status"]):
        raise PreflightError("H-F01 ledger authority changed")
    present = bool(os.environ.get("OPENROUTER_API_KEY", "").strip()) \
        if key_present is None else bool(key_present)
    if not present: raise PreflightError("OPENROUTER_API_KEY is missing")
    for arm, paths in arm_paths(root).items():
        try: current = CP.load(paths["experiment"])
        except (CP.PairError, PS.StoreError, OSError) as exc:
            raise PreflightError(f"H-F01 {arm} manifest is invalid: {exc}") from exc
        if PS.state_hash(HCA.assignment(current)) != \
                manifest["arms"][arm]["manifest_assignment_sha256"]:
            raise PreflightError(f"H-F01 {arm} manifest assignment changed")
    for key, expected in manifest["static_input_sha256"].items():
        namespace, relative = key.split(":", 1)
        base = Path(root).absolute() if namespace == "snapshot" else REPO
        if _sha(_safe_bytes(base / relative, base)) != expected:
            raise PreflightError(f"H-F01 static authority changed: {key}")
    if _sha(_safe_bytes(authority["ledger_path"], Path(authority["ledger_path"]).parent)) \
            != authority["ledger_sha256"]:
        raise PreflightError("H-F01 ledger authority changed")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot-root", required=True)
    print(json.dumps(build_manifest(parser.parse_args().snapshot_root), indent=2, sort_keys=True))


if __name__ == "__main__": main()
