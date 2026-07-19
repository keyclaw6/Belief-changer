#!/usr/bin/env python3
"""Pure pre-RF21 H-F01 authority preflight; never writes, dispatches, or connects."""
import argparse, datetime as dt, hashlib, json, os, re, shlex, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve(); sys.path.insert(0, str(HERE.parent))
import candidate_pair as CP  # noqa: E402
import loopcfg  # noqa: E402
import pair_store as PS  # noqa: E402
import path_guard as PG  # noqa: E402
REPO, CONFIG = HERE.parents[2], HERE.parents[2] / "loop/config.yaml"; LEDGER = REPO / "openspec/changes/redesign-book-factory/tasks.md"
BOOK, SUBJECT, CHAPTERS = "production-books/quit-sugar", "sugar", (1, 2, 3)
URL, KEY_URL = "https://openrouter.ai/api/v1/chat/completions", "https://openrouter.ai/api/v1/key"; MODEL = "anthropic/claude-opus-4.6"
ROUTE_LAW = {
    "writer_model": MODEL, "writer_provider": "openrouter", "writer_reasoning": "none",
    "writer_endpoint": URL, "writer_temperature": .7, "writer_max_tokens": 16000,
    "writer_attempts": 1, "researcher_model": "deepseek/deepseek-v4-pro",
    "researcher_provider": "openrouter", "researcher_reasoning": "xhigh",
    "planner_model": "gpt-5.6-sol", "planner_route": "codex-native", "planner_reasoning": "xhigh",
    "grounded_reviewer_model": "gpt-5.6-sol", "grounded_reviewer_family": "openai",
    "grounded_reviewer_route": "codex-native", "grounded_reviewer_reasoning": "xhigh",
    "developmental_reviewer_model": "gpt-5.6-luna",
    "developmental_reviewer_family": "luna", "developmental_reviewer_route": "codex-native",
    "developmental_reviewer_reasoning": "max", "judge_model": "gpt-5.6-sol",
    "judge_route": "codex-native", "judge_reasoning": "xhigh", "judge_k": 2,
    "reference_dir": "calibration/reference/gsbs", "reference_chapter_offset": 2}
ROUTE_CONFIG = {key: ROUTE_LAW[key] for key in tuple(ROUTE_LAW)[:7]}; RUBRICS = ("calibration/judges/product-effect-rubric.md", "calibration/judges/product-effect-absolute-rubric.md")
EXECUTABLES = ("scripts/loop/product_effect.py", "scripts/loop/product_effect_absolute.py", "scripts/loop/hf01_preflight.py", "scripts/loop/hf01_run.py",
    "scripts/loop/hf01_stage_a.py", "scripts/loop/hf01_blind.py", "scripts/loop/hf01_carr.py", "scripts/loop/hf01_upstream.py", "scripts/loop/hf01_upstream_contract.py",
    "scripts/loop/candidate_pair.py", "scripts/loop/commission_set.py", "scripts/loop/first_draft_batch.py", "scripts/loop/draft_call.py", "scripts/loop/draft_batch_state.py",
    "scripts/loop/grounded_review.py", "scripts/loop/developmental_review.py", "scripts/eval/native_grounded_review.py", "scripts/eval/native_developmental_review.py",
    "scripts/loop/hf01_control_authority.py", "scripts/loop/writer_context.py", "scripts/loop/score_core.py", "scripts/loop/score_receipt.py", "scripts/loop/judges.py",
    "scripts/loop/product_decision.py", "scripts/loop/experiment_record.py", "scripts/loop/gate.py", "scripts/eval/product_effect_panel.py", "scripts/eval/native_judge.py")
TREATMENT_PATHS = frozenset((f"{BOOK}/00-brief.md", f"{BOOK}/framing.md",
    f"{BOOK}/framing-review.md", f"{BOOK}/master-plan.md", f"{BOOK}/master-plan-review.md",
    *(f"{BOOK}/commissions/chapter-{n:02d}.md" for n in CHAPTERS)))
CALLS = {"rf21_plan_and_review": 2, "rf22_commissions_and_audit": 4, "writers": 6,
         "grounded_reviews": 6, "developmental_reviews": 2,
         "absolute_causal_diagnostic": 6, "gsbs_blind_votes": 8,
         "carr_diagnostics": 6}
BOUNDARIES = ("rf21_rf22_authority_bound_receipts", "rf23_writer_authorization", "freeze_all_six",
    "grounded_integrity_and_near_copy_all_six", "developmental_reader_state_and_sequence",
    "control_treatment_causal_diagnostic", "position_swapped_gsbs_comparisons", "blind_evidence_receipt",
    "carr_craft_diagnostic_after_blind", "named_human_comparison", "explicit_atomic_gate")
AUTHORITY_FIELDS = ("schema", "experiment", "lineage", "mode", "frozen_at_utc", "snapshot_root", "identity", "route", "call_budget", "allowed_treatment_paths",
    "subject_reference_isolation", "validation_ladder", "rf21_rf22_native_calls",
    "static_input_sha256", "output_isolation", "next_command", "post_authority_boundaries")
class PreflightError(RuntimeError): pass
def _sha(data): return hashlib.sha256(data).hexdigest()
def _safe(path, boundary):
    try: return PG.safe_file(path, boundary).read_bytes()
    except (PG.PathError, OSError) as exc: raise PreflightError(str(exc)) from exc
def _block(rows, code, detail=None, path=None, kind="static_input"):
    row = {"class": kind, "code": code, **({"detail": detail} if detail else {}), **({"path": str(path)} if path else {})}; rows.append(row)
def _task_text(path, task):
    try: text = _safe(path, Path(path).parent).decode()
    except (PreflightError, UnicodeError): return ""
    match = re.search(rf"^### {task}\b(?P<body>.*?)(?=^### RF-|\Z)", text, re.M | re.S)
    return match.group(0) if match else ""
def _status(path, task): return match.group(1) if (match := re.search(r"^- Status: `([A-Z_]+)`$", _task_text(path, task), re.M)) else "MISSING"
def _utc(value):
    try: parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError): return None
    return value if parsed.utcoffset() == dt.timedelta(0) else None
def _git(*args):
    try: return subprocess.check_output(["git", "-C", str(REPO), *args], text=True)
    except (OSError, subprocess.SubprocessError) as exc: raise PreflightError(str(exc)) from exc
def _commit(): return _git("rev-parse", "HEAD").strip()
def _clean(): return not _git("status", "--porcelain", "--untracked-files=all").strip()
def arm_paths(root):
    root = Path(root).absolute()
    return {arm: {"experiment": root / f"loop/experiments/h-f01-{arm}", "candidate": root / f"loop/experiments/h-f01-{arm}/candidate",
                  "book": root / f"loop/experiments/h-f01-{arm}/candidate/{BOOK}"}
            for arm in ("control", "treatment")}
def _route(path, blockers, code):
    try: cfg = loopcfg.load(PG.safe_file(path, path.parent.parent))
    except (PG.PathError, SystemExit, OSError) as exc:
        _block(blockers, code, str(exc), path); return
    if any(cfg.get(key) != value for key, value in ROUTE_LAW.items()):
        _block(blockers, code, "full fixed route law differs", path)
def _pair_map(root, paths, manifest):
    drafts = {f"{BOOK}/chapters/chapter-{n:02d}.md" for n in CHAPTERS}
    return {item["path"]: _sha(_safe(paths["candidate"] / item["path"], root))
            for item in manifest["entries"] + manifest["outputs"] if item["path"] not in drafts}
def _execution_contract(paths, maps): import hf01_upstream as upstream; return upstream.authority_contract(paths, maps)
def _arms(root, paths, blockers):
    manifests, states, maps = {}, {}, {}
    for arm, item in paths.items():
        try:
            manifest = CP.inspect(item["experiment"]); pair, evaluation = CP._actual(item["experiment"], manifest)
            if manifest["state"] != "CANDIDATE" or manifest.get("operation") is not None \
                    or manifest.get("outputs") or pair != manifest["accepted_pair_hash"]:
                _block(blockers, f"{arm.upper()}_NOT_PRERF21_SNAPSHOT")
            if manifest["run"]["book"] != BOOK or tuple(manifest["run"]["chapters"]) != CHAPTERS:
                _block(blockers, f"{arm.upper()}_RUN_MISMATCH")
            manifests[arm], maps[arm] = manifest, _pair_map(root, item, manifest)
            states[arm] = {"accepted_generation": manifest["accepted_generation"],
                "accepted_pair_hash": manifest["accepted_pair_hash"],
                "accepted_evaluation_hash": manifest["accepted_evaluation_hash"],
                "pre_rf21_pair_sha256": pair, "evaluation_sha256": evaluation,
                "run": manifest["run"]}
        except (CP.PairError, PS.StoreError, OSError, PreflightError) as exc:
            _block(blockers, f"RF02_{arm.upper()}_INVALID", str(exc), item["experiment"])
        _route(item["candidate"] / "loop/config.yaml", blockers,
               f"{arm.upper()}_ROUTE_CONFIG_MISMATCH")
    if len(states) == 2:
        identities = {(s["accepted_generation"], s["accepted_pair_hash"],
                       s["accepted_evaluation_hash"]) for s in states.values()}
        iterations = {s["run"]["iteration_id"] for s in states.values()}
        if len(identities) != 1: _block(blockers, "RF02_ARMS_NOT_MATCHED")
        if len(iterations) != 1 or not isinstance(next(iter(iterations)), int):
            _block(blockers, "HF01_ITERATION_ID_INVALID")
    return manifests, states, maps
def _reference(root, paths, manifest, blockers):
    if not manifest: return [], []
    prefix, rows = "calibration/reference/gsbs/", []
    for item in manifest["evaluation"]:
        if item["path"].startswith(prefix):
            path = paths["experiment"] / "evaluation" / item["path"]
            rows.append({"path": item["path"], "sha256": _sha(_safe(path, root))})
    chapters = [row for row in rows if Path(row["path"]).suffix.lower() in {".md", ".txt"}
                and re.search(r"\d+", Path(row["path"]).stem)]
    chapters.sort(key=lambda row: int(re.search(r"\d+", Path(row["path"]).stem).group()))
    offset, matched = ROUTE_LAW["reference_chapter_offset"], []
    if len(chapters) < max(CHAPTERS) + offset:
        _block(blockers, "GSBS_OFFSET_MATCHES_MISSING")
    else:
        matched = [{"treatment_chapter": n, "reference_position": n + offset,
                    **chapters[n + offset - 1]} for n in CHAPTERS]
    if not any(row["path"].endswith("reference-metrics.json") for row in rows):
        _block(blockers, "GSBS_EVALUATION_REFERENCE_MISSING")
    return rows, matched
def _static(root, paths, manifests, maps, blockers):
    hashes = {}
    try:
        for arm, values in maps.items():
            for rel, digest in values.items():
                if arm == "treatment" and rel in TREATMENT_PATHS: continue
                path = paths[arm]["candidate"] / rel
                hashes[f"snapshot:{path.relative_to(root)}"] = digest
        for arm, manifest in manifests.items():
            for item in manifest["evaluation"]:
                path = paths[arm]["experiment"] / "evaluation" / item["path"]
                hashes[f"snapshot:{path.relative_to(root)}"] = _sha(_safe(path, root))
        for rel in (*EXECUTABLES, *RUBRICS, "prompts/style-guide.md", "prompts/chapter-writer.md", "prompts/master-plan-skill-v2.md",
                    "prompts/master-plan-reviewer-v2.md", "production-books/_template/00-brief.md",
                    "production-books/_template/framing.md", "production-books/_template/framing-review.md",
                    "prompts/chapter-commissioner.md", "prompts/commission-set-auditor.md", "loop/config.yaml"):
            hashes[f"repo:{rel}"] = _sha(_safe(REPO / rel, REPO))
    except (PreflightError, ValueError) as exc: _block(blockers, "STATIC_AUTHORITY_INVALID", str(exc))
    return hashes
def _prereg(state, matched, commit):
    return {"hypothesis": "The linked reader-state and source-grounded handoff makes the "
            "quit-sugar opening achieve stronger belief change against offset-matched GSBS.",
        "causal_chain": ["reader-state plan fixes each chapter's belief job", "assigned evidence becomes a source-grounded commission",
                         "compact handoff lets the writer enact the planned discovery"],
        "changed_bundle": sorted(TREATMENT_PATHS),
        "frozen_variables": {"route_sha256": PS.state_hash(ROUTE_LAW),
            "gsbs_sha256": PS.state_hash(matched), "call_ceiling": "40", "writer_calls": "6"},
        "inputs": {"git_commit": commit,
            "control_pre_generation_pair_sha256": state.get("control", {}).get("pre_rf21_pair_sha256", "missing"),
            "treatment_pre_generation_pair_sha256": state.get("treatment", {}).get("pre_rf21_pair_sha256", "missing"),
            "subject": SUBJECT, "book": BOOK, "config": "loop/config.yaml"},
        "falsifier": "Refuted by integrity failure, at most three of six GSBS chapter votes, "
                     "zero of two GSBS opening votes, or named-human rejection."}
def build_manifest(snapshot_root, key_present=None, ledger=None, config=CONFIG,
                   authority_timestamp=None):
    root, ledger = Path(snapshot_root).absolute(), Path(ledger or LEDGER).absolute()
    paths, blockers, downstream = arm_paths(root), [], []
    _route(Path(config).absolute(), blockers, "WRITER_ROUTE_CONFIG_MISMATCH")
    manifests, states, maps = _arms(root, paths, blockers)
    if len(maps) == 2:
        changed = sorted(path for path in set(maps["control"]) | set(maps["treatment"])
                         if maps["control"].get(path) != maps["treatment"].get(path))
        if changed: _block(blockers, "RF21_ALREADY_STARTED_BEFORE_AUTHORITY", ", ".join(changed))
    references, matched = _reference(root, paths["control"], manifests.get("control"), blockers)
    hashes = _static(root, paths, manifests, maps, blockers)
    try: commit, clean = _commit(), _clean()
    except PreflightError as exc: _block(blockers, "PINNED_COMMIT_UNAVAILABLE", str(exc)); commit, clean = "missing", False
    if not clean: _block(blockers, "GIT_WORKTREE_DIRTY", kind="source_authority")
    rf20, rf21, rf22, rf23 = (_status(ledger, task) for task in ("RF-20", "RF-21", "RF-22", "RF-23"))
    if rf20 != "BLOCKED": _block(blockers, "RF20_TERMINAL_STATE_CHANGED", rf20, kind="product_authority")
    if rf21 not in ("READY", "DONE"): _block(blockers, "RF21_NOT_AUTHORIZED", rf21, kind="product_authority")
    if rf22 not in ("READY", "DONE"): _block(downstream, "RF22_NOT_READY", rf22, kind="product_authority")
    if rf23 not in ("READY", "DONE"): _block(downstream, "RF23_NOT_READY", rf23, kind="product_authority")
    present = bool(os.environ.get("OPENROUTER_API_KEY", "").strip()) if key_present is None else bool(key_present)
    if not present: _block(downstream, "OPENROUTER_API_KEY_MISSING", kind="credential_machine")
    if not _utc(authority_timestamp): _block(blockers, "AUTHORITY_TIMESTAMP_REQUIRED", kind="product_authority")
    stamp = authority_timestamp or "REQUIRED_UTC_ISO_8601"
    command = shlex.join(["python3", "scripts/loop/hf01_run.py", "--snapshot-root", str(root),
        "--authority-timestamp", stamp, "--redesign-authorized", "--rf-stage", "RF-21",
        "--candidate-root", str(root / "loop/experiments")])
    blockers.sort(key=lambda row: (row["class"], row["code"])); downstream.sort(key=lambda row: (row["class"], row["code"]))
    return {"schema": 5, "experiment": "H-F01", "lineage": "direct-gsbs-stage-a",
        "mode": "NO_SEND_PREFLIGHT", "frozen_at_utc": authority_timestamp,
        "snapshot_root": str(root), "identity": {"subject": SUBJECT, "book": BOOK,
            "config": "loop/config.yaml", "reference": "calibration/reference/gsbs",
            "reference_inputs": references, "gsbs_matches": matched,
            "gsbs_sha256": PS.state_hash(matched)}, "route": dict(ROUTE_LAW),
        "call_budget": {"ceiling": 40, "writer_calls": 6, "breakdown": CALLS,
            "planned_total": sum(CALLS.values()), "counted_before_authority": 0},
        "credential": {"name": "OPENROUTER_API_KEY", "present": present,
            "credit_check": {"method": "GET", "url": KEY_URL, "runtime_before_write": True}},
        "authority": {"rf20_status": rf20, "rf21_status": rf21,
            "ledger_path": str(ledger), "rf20_sha256": _sha(_task_text(ledger, "RF-20").encode()),
            "git_commit": commit}, "preregistration": _prereg(states, matched, commit),
        "arms": states, "allowed_treatment_paths": sorted(TREATMENT_PATHS),
        **_execution_contract(paths, maps),
        "static_input_sha256": hashes, "output_isolation": {"root": str(root / "loop/experiments"),
            **{arm: str(item["experiment"]) for arm, item in paths.items()}},
        "next_command": command, "post_authority_boundaries": list(BOUNDARIES),
        "ready_to_freeze_authority": not blockers,
        "ready_to_send": not blockers and not downstream,
        "blockers": blockers, "downstream_blockers": downstream}
def require_ready(root, **kwargs):
    value = build_manifest(root, **kwargs)
    if not value["ready_to_freeze_authority"]:
        raise PreflightError("H-F01 blocked: " + ", ".join(row["code"] for row in value["blockers"]))
    return value
def validate_execution_authority(root, value, key_present=None):
    root, authority = Path(root).absolute(), value.get("authority", {})
    if value.get("schema") != 5 or value.get("lineage") != "direct-gsbs-stage-a" \
            or not _utc(value.get("frozen_at_utc")):
        raise PreflightError("H-F01 pre-RF21 authority is invalid")
    if not _clean(): raise PreflightError("H-F01 source worktree changed")
    if _commit() != authority.get("git_commit"): raise PreflightError("H-F01 pinned commit changed")
    ledger = Path(authority["ledger_path"])
    if _status(ledger, "RF-20") != "BLOCKED" or _sha(_task_text(ledger, "RF-20").encode()) != authority.get("rf20_sha256"):
        raise PreflightError("RF-20 terminal authority changed")
    paths = arm_paths(root); maps = {arm: _pair_map(root, item, CP.inspect(item["experiment"])) for arm, item in paths.items()}
    changed = {path for path in set(maps["control"]) | set(maps["treatment"]) if maps["control"].get(path) != maps["treatment"].get(path)}
    if not changed <= TREATMENT_PATHS: raise PreflightError("H-F01 treatment escaped its allowlist")
    expected = build_manifest(root, key_present=key_present, ledger=ledger, authority_timestamp=value["frozen_at_utc"])
    if any(value.get(key) != expected.get(key) for key in AUTHORITY_FIELDS):
        raise PreflightError("H-F01 stable authority core changed")
    arms = value.get("arms", {})
    identities = {(item.get("accepted_generation"), item.get("accepted_pair_hash"), item.get("accepted_evaluation_hash"),
                   item.get("pre_rf21_pair_sha256")) for item in arms.values() if isinstance(item, dict)}
    if set(arms) != {"control", "treatment"} or len(identities) != 1 or any(item.get("pre_rf21_pair_sha256") != item.get("accepted_pair_hash") for item in arms.values()):
        raise PreflightError("H-F01 pre-RF21 arm authority changed")
    for arm, frozen in arms.items():
        current = CP.inspect(paths[arm]["experiment"])
        if any(current.get(key) != frozen.get(key) for key in ("accepted_generation", "accepted_pair_hash", "accepted_evaluation_hash", "run")):
            raise PreflightError(f"H-F01 {arm} accepted/run identity changed")
    if value.get("preregistration") != _prereg(value.get("arms", {}), expected["identity"]["gsbs_matches"], authority["git_commit"]):
        raise PreflightError("H-F01 preregistration authority changed")
    return value
def require_stage(value, task):
    status = _status(value["authority"]["ledger_path"], task)
    if status not in ("READY", "DONE"): raise PreflightError(f"{task} is {status}, not READY")
    return status
def treatment_artifacts(root):
    paths = arm_paths(root); manifests = {arm: CP.inspect(item["experiment"]) for arm, item in paths.items()}
    maps = {arm: _pair_map(Path(root).absolute(), paths[arm], manifests[arm]) for arm in paths}
    changed = {path for path in set(maps["control"]) | set(maps["treatment"])
               if maps["control"].get(path) != maps["treatment"].get(path)}
    if changed != TREATMENT_PATHS: raise PreflightError("RF21/RF22 treatment bundle is not exact")
    return {path: maps["treatment"][path] for path in sorted(TREATMENT_PATHS)}
def main():
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--snapshot-root", required=True); parser.add_argument("--authority-timestamp"); args = parser.parse_args(); print(json.dumps(build_manifest(args.snapshot_root, authority_timestamp=args.authority_timestamp), indent=2, sort_keys=True))
if __name__ == "__main__": main()
