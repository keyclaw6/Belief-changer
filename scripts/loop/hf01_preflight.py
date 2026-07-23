#!/usr/bin/env python3
"""Pure pre-RF21 H-F01 authority preflight; never writes, dispatches, or connects."""
import argparse, datetime as dt, hashlib, json, os, re, shlex, subprocess, sys, urllib.request
from pathlib import Path
HERE = Path(__file__).resolve(); sys.path.insert(0, str(HERE.parent))
import candidate_pair as CP  # noqa: E402
import loopcfg  # noqa: E402
import pair_store as PS  # noqa: E402
import path_guard as PG  # noqa: E402
REPO, CONFIG = HERE.parents[2], HERE.parents[2] / "loop/config.yaml"; LEDGER = REPO / "openspec/changes/redesign-book-factory/tasks.md"
AUTHORIZED_ROOT_TEXT = r"C:\Users\Kristian Bilstrup\Documents\Belief-changer"
AUTHORIZED_ROOT = Path(AUTHORIZED_ROOT_TEXT)
FORBIDDEN_ROOT = "/home/kab/Belief-changer-minimal-loop"
BOOK, SUBJECT, CHAPTERS = "production-books/quit-sugar", "sugar", (1, 2, 3)
URL, KEY_URL = "https://openrouter.ai/api/v1/chat/completions", "https://openrouter.ai/api/v1/key"
CREDITS_URL = "https://openrouter.ai/api/v1/credits"
LOCATION_URL = "https://openrouter.ai/cdn-cgi/trace"
MODEL_URL = "https://openrouter.ai/api/v1/model/meta/muse-spark-1.1"
USER_MODELS_URL = "https://openrouter.ai/api/v1/models/user"
ENDPOINTS_URL = "https://openrouter.ai/api/v1/models/meta/muse-spark-1.1/endpoints"
MODEL, CANONICAL_MODEL = "meta/muse-spark-1.1", "meta/muse-spark-1.1-20260709"
SUPPORTED_EFFORTS = ("xhigh", "high", "medium", "low", "minimal")
PRICING = {"prompt": "0.00000125", "completion": "0.00000425",
           "input_cache_read": "0.00000015"}
MINIMUM_CREDIT_USD = 6 * 1048576 * float(PRICING["completion"])
ROUTE_LAW = {
    "writer_model": MODEL, "writer_provider": "openrouter", "writer_reasoning": "high",
    "writer_endpoint": URL, "writer_temperature": .7,
    "writer_attempts": 1, "writer_allow_fallbacks": False,
    "researcher_model": "deepseek/deepseek-v4-pro",
    "researcher_provider": "openrouter", "researcher_reasoning": "xhigh",
    "planner_model": "gpt-5.6-sol", "planner_route": "codex-native", "planner_reasoning": "xhigh",
    "grounded_reviewer_model": "gpt-5.6-sol", "grounded_reviewer_family": "openai",
    "grounded_reviewer_route": "codex-native", "grounded_reviewer_reasoning": "xhigh",
    "developmental_reviewer_model": "gpt-5.6-luna",
    "developmental_reviewer_family": "luna", "developmental_reviewer_route": "codex-native",
    "developmental_reviewer_reasoning": "max", "judge_model": "gpt-5.6-sol",
    "judge_route": "codex-native", "judge_reasoning": "xhigh", "judge_k": 2,
    "reference_dir": "calibration/reference/gsbs", "reference_chapter_offset": 2}
ROUTE_CONFIG_KEYS = ("writer_model", "writer_provider", "writer_reasoning",
    "writer_endpoint", "writer_temperature", "writer_attempts",
    "writer_allow_fallbacks")
ROUTE_CONFIG = {key: ROUTE_LAW[key] for key in ROUTE_CONFIG_KEYS}; RUBRICS = ("calibration/judges/product-effect-rubric.md", "calibration/judges/product-effect-absolute-rubric.md")
EXECUTABLES = ("scripts/loop/product_effect.py", "scripts/loop/product_effect_absolute.py", "scripts/loop/hf01_preflight.py", "scripts/loop/hf01_prepare.py", "scripts/loop/immutable_file.py", "scripts/loop/hf01_run.py",
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
def _path_text(path): return os.path.normcase(os.path.abspath(os.fspath(path)))
def require_authorized_root(root):
    """Reject every non-authoritative persistent root before touching its contents."""
    raw = os.fspath(root)
    if raw.replace("\\", "/").rstrip("/") == FORBIDDEN_ROOT \
            or _path_text(raw) != _path_text(AUTHORIZED_ROOT):
        raise PreflightError(f"H-F01 persistent root must be exactly {AUTHORIZED_ROOT_TEXT}")
    return Path(os.path.abspath(raw))

def _http_json(url, key, open_url):
    request = urllib.request.Request(url, method="GET", headers={"Authorization": f"Bearer {key}"})
    try:
        with open_url(request, timeout=30) as response:
            status = getattr(response, "status", 200)
            if status != 200: raise PreflightError(f"authenticated OpenRouter preflight returned HTTP {status}")
            value = json.loads(response.read())
    except PreflightError:
        raise
    except Exception as exc:
        code = getattr(exc, "code", None)
        detail = f"HTTP {code}" if code is not None else type(exc).__name__
        raise PreflightError(f"authenticated OpenRouter preflight failed: {detail}") from exc
    if not isinstance(value, dict): raise PreflightError("authenticated OpenRouter response is not an object")
    return value

def current_location(open_url=urllib.request.urlopen):
    """Return only the current country proof from OpenRouter's own edge."""
    request = urllib.request.Request(LOCATION_URL, method="GET")
    try:
        with open_url(request, timeout=30) as response:
            status = getattr(response, "status", 200)
            if status != 200:
                raise PreflightError(f"OpenRouter edge location check returned HTTP {status}")
            text = response.read().decode("utf-8")
    except PreflightError:
        raise
    except Exception as exc:
        code = getattr(exc, "code", None)
        detail = f"HTTP {code}" if code is not None else type(exc).__name__
        raise PreflightError(f"OpenRouter edge location check failed: {detail}") from exc
    loc_lines = [line for line in text.splitlines() if line.startswith("loc")]
    if not loc_lines:
        raise PreflightError("OpenRouter edge location trace is missing loc")
    if len(loc_lines) != 1:
        raise PreflightError("OpenRouter edge location trace has duplicate loc")
    match = re.fullmatch(r"loc=([A-Z]{2})", loc_lines[0])
    if match is None:
        raise PreflightError("OpenRouter edge location trace has malformed loc")
    country = match.group(1)
    if country != "US":
        raise PreflightError(f"OpenRouter edge location is not eligible: {country}")
    return {"source": LOCATION_URL, "country_code": country}

def authenticated_preflight(open_url=urllib.request.urlopen, now=None):
    """Perform only authenticated metadata/account GETs; never sends model input."""
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key: raise PreflightError("OPENROUTER_API_KEY is missing")
    location = current_location(open_url)
    key_data = _http_json(KEY_URL, key, open_url).get("data")
    model = _http_json(MODEL_URL, key, open_url).get("data")
    user_models = _http_json(USER_MODELS_URL, key, open_url).get("data")
    endpoints_value = _http_json(ENDPOINTS_URL, key, open_url)
    if not all(isinstance(item, dict) for item in (model, key_data)):
        raise PreflightError("OpenRouter preflight metadata is incomplete")
    top = model.get("top_provider")
    pricing = model.get("pricing")
    reasoning = model.get("reasoning")
    supported = model.get("supported_parameters")
    endpoints_data = endpoints_value.get("data")
    endpoints = endpoints_data.get("endpoints") if isinstance(endpoints_data, dict) else None
    expected_params = {"reasoning", "temperature", "max_tokens"}
    if model.get("id") != MODEL or model.get("canonical_slug") != CANONICAL_MODEL \
            or not isinstance(top, dict) \
            or top.get("context_length") != 1048576 or top.get("max_completion_tokens") is not None \
            or not isinstance(pricing, dict) \
            or any(pricing.get(name) != value for name, value in PRICING.items()) \
            or not isinstance(supported, list) or not expected_params <= set(supported) \
            or not isinstance(reasoning, dict) or reasoning.get("mandatory") is not True \
            or tuple(reasoning.get("supported_efforts", ())) != SUPPORTED_EFFORTS:
        raise PreflightError("Muse capability metadata does not match frozen H-F01 authority")
    visible = [item for item in user_models or () if isinstance(item, dict)
               and item.get("id") == MODEL and item.get("canonical_slug") == CANONICAL_MODEL]
    if not isinstance(user_models, list) or len(visible) != 1:
        raise PreflightError("Muse is not exactly once in the account-visible model list")
    if not isinstance(endpoints, list) or len(endpoints) != 1:
        raise PreflightError("Muse must expose exactly one account-visible endpoint")
    endpoint = endpoints[0]
    if not isinstance(endpoint, dict) or endpoint.get("provider_name") != "Meta" \
            or endpoint.get("model_id") != MODEL or endpoint.get("status") != 0 \
            or endpoint.get("name") != f"Meta | {CANONICAL_MODEL}":
        raise PreflightError("Muse endpoint does not bind the exact Meta canonical route")
    stamp = now or dt.datetime.now(dt.timezone.utc)
    expires = key_data.get("expires_at")
    if expires is not None:
        try: expiry = dt.datetime.fromisoformat(expires.replace("Z", "+00:00"))
        except (AttributeError, ValueError) as exc: raise PreflightError("OpenRouter key expiry is invalid") from exc
        if expiry <= stamp: raise PreflightError("OPENROUTER_API_KEY is expired")
    remaining = key_data.get("limit_remaining")
    if remaining is not None and (isinstance(remaining, bool) or not isinstance(remaining, (int, float)) or remaining < MINIMUM_CREDIT_USD):
        raise PreflightError("OPENROUTER_API_KEY spend allowance is under the six-call bound")
    management_key = os.environ.get("OPENROUTER_MANAGEMENT_KEY", "").strip()
    if not management_key:
        raise PreflightError("OPENROUTER_MANAGEMENT_KEY is required for the authenticated credit check")
    credits = _http_json(CREDITS_URL, management_key, open_url).get("data")
    if not isinstance(credits, dict):
        raise PreflightError("OpenRouter preflight credit metadata is incomplete")
    total, usage = credits.get("total_credits"), credits.get("total_usage")
    if any(isinstance(item, bool) or not isinstance(item, (int, float)) for item in (total, usage)) \
            or total - usage < MINIMUM_CREDIT_USD:
        raise PreflightError("OpenRouter account credit is under the six-call bound")
    return {"model": MODEL, "canonical_model": CANONICAL_MODEL,
        "provider": "Meta", "calls": 6,
        "context_length": 1048576, "max_completion_tokens": None,
        "prompt_price_per_token": PRICING["prompt"],
        "completion_price_per_token": PRICING["completion"],
        "cache_read_price_per_token": PRICING["input_cache_read"],
        "reasoning_mandatory": True,
        "reasoning_supported_efforts": list(SUPPORTED_EFFORTS),
        "current_request_location": location,
        "current_request_account_visible_model": {
            "source": USER_MODELS_URL, "authenticated": True, "exact_matches": 1,
            "id": visible[0]["id"], "canonical_slug": visible[0]["canonical_slug"]},
        "supported_parameters": sorted(expected_params),
        "minimum_credit_usd": MINIMUM_CREDIT_USD,
        "account_credit_remaining": total - usage,
        "key_spend_allowance_remaining": remaining}
def resume_command(authority, stage=None, native=False):
    """Render a stable receipt template with this process's actual interpreter."""
    args = shlex.split(authority["next_command"])
    if not args or args[0] != "{python}":
        return shlex.join([*args, *( ["--native"] if native and "--native" not in args else [])])
    args[0] = sys.executable
    if stage is not None:
        args[args.index("--rf-stage") + 1] = stage
    if native and "--native" not in args: args.append("--native")
    return shlex.join(args)
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
def _status(path, task): return match.group(1) if (match := re.search(r"^- Status: `([A-Z_]+)`\r?$", _task_text(path, task), re.M)) else "MISSING"
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
    root = require_authorized_root(root)
    return {arm: {"experiment": root / f"loop/experiments/h-f01-{arm}", "candidate": root / f"loop/experiments/h-f01-{arm}/candidate",
                  "book": root / f"loop/experiments/h-f01-{arm}/candidate/{BOOK}"}
            for arm in ("control", "treatment")}
def _route(path, blockers, code):
    try: cfg = loopcfg.load(PG.safe_file(path, path.parent.parent))
    except (PG.PathError, SystemExit, OSError) as exc:
        _block(blockers, code, str(exc), path); return
    if any(cfg.get(key) != value for key, value in ROUTE_LAW.items()):
        _block(blockers, code, "full fixed route law differs", path)
def _pair_map(root, paths, manifest, allow_missing=frozenset()):
    drafts = {f"{BOOK}/chapters/chapter-{n:02d}.md" for n in CHAPTERS}
    result = {}
    for item in manifest["entries"] + manifest["outputs"]:
        relative = item["path"]
        if relative in drafts:
            continue
        path = paths["candidate"] / relative
        if relative in allow_missing and not os.path.lexists(path):
            continue
        result[relative] = _sha(_safe(path, root))
    return result
def _execution_contract(paths, maps): import hf01_upstream as upstream; return upstream.authority_contract(paths, maps)
def _arms(root, paths, blockers, execution_states=None):
    manifests, states, maps = {}, {}, {}
    for arm, item in paths.items():
        try:
            manifest = CP.inspect(item["experiment"])
            if execution_states is None:
                pair, evaluation = CP._actual(item["experiment"], manifest)
                if manifest["state"] != "CANDIDATE" or manifest.get("operation") is not None \
                        or manifest.get("outputs") or pair != manifest["accepted_pair_hash"]:
                    _block(blockers, f"{arm.upper()}_NOT_PRERF21_SNAPSHOT")
            if manifest["run"]["book"] != BOOK or tuple(manifest["run"]["chapters"]) != CHAPTERS:
                _block(blockers, f"{arm.upper()}_RUN_MISMATCH")
            manifests[arm] = manifest
            maps[arm] = _pair_map(
                root, item, manifest,
                TREATMENT_PATHS if arm == "treatment" else frozenset())
            if execution_states is None:
                states[arm] = {"accepted_generation": manifest["accepted_generation"],
                    "accepted_pair_hash": manifest["accepted_pair_hash"],
                    "accepted_evaluation_hash": manifest["accepted_evaluation_hash"],
                    "pre_rf21_pair_sha256": pair, "evaluation_sha256": evaluation,
                    "run": manifest["run"]}
            else:
                states[arm] = dict(execution_states[arm])
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
def build_manifest(snapshot_root, key_present=None, ledger=None, config=None,
                   authority_timestamp=None, execution_states=None):
    root, ledger = require_authorized_root(snapshot_root), Path(ledger or LEDGER).absolute()
    config = Path(config or CONFIG).absolute()
    if root not in ledger.parents or root not in config.parents:
        raise PreflightError("H-F01 ledger and configuration must stay inside the authorized root")
    paths, blockers, downstream = arm_paths(root), [], []
    _route(config, blockers, "WRITER_ROUTE_CONFIG_MISMATCH")
    manifests, states, maps = _arms(root, paths, blockers, execution_states)
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
    if rf21 == "READY": _block(blockers, "RF21_NOT_STARTED", rf21, kind="product_authority")
    elif rf21 not in ("IN_PROGRESS", "DONE"): _block(blockers, "RF21_NOT_AUTHORIZED", rf21, kind="product_authority")
    if rf22 == "READY": _block(downstream, "RF22_NOT_STARTED", rf22, kind="product_authority")
    elif rf22 not in ("IN_PROGRESS", "DONE"): _block(downstream, "RF22_NOT_READY", rf22, kind="product_authority")
    if rf23 not in ("READY", "DONE"): _block(downstream, "RF23_NOT_READY", rf23, kind="product_authority")
    present = bool(os.environ.get("OPENROUTER_API_KEY", "").strip()) if key_present is None else bool(key_present)
    if not present: _block(downstream, "OPENROUTER_API_KEY_MISSING", kind="credential_machine")
    if not _utc(authority_timestamp): _block(blockers, "AUTHORITY_TIMESTAMP_REQUIRED", kind="product_authority")
    stamp = authority_timestamp or "REQUIRED_UTC_ISO_8601"
    command = shlex.join(["{python}", "scripts/loop/hf01_run.py", "--snapshot-root", str(root),
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
    root, authority = require_authorized_root(root), value.get("authority", {})
    if value.get("schema") != 5 or value.get("lineage") != "direct-gsbs-stage-a" \
            or not _utc(value.get("frozen_at_utc")):
        raise PreflightError("H-F01 pre-RF21 authority is invalid")
    if not _clean(): raise PreflightError("H-F01 source worktree changed")
    if _commit() != authority.get("git_commit"): raise PreflightError("H-F01 pinned commit changed")
    ledger = Path(authority["ledger_path"])
    if _status(ledger, "RF-20") != "BLOCKED" or _sha(_task_text(ledger, "RF-20").encode()) != authority.get("rf20_sha256"):
        raise PreflightError("RF-20 terminal authority changed")
    paths = arm_paths(root)
    maps = {arm: _pair_map(
        root, item, CP.inspect(item["experiment"]),
        TREATMENT_PATHS if arm == "treatment" else frozenset())
        for arm, item in paths.items()}
    changed = {path for path in set(maps["control"]) | set(maps["treatment"]) if maps["control"].get(path) != maps["treatment"].get(path)}
    if not changed <= TREATMENT_PATHS: raise PreflightError("H-F01 treatment escaped its allowlist")
    arms = value.get("arms", {})
    identities = {(item.get("accepted_generation"), item.get("accepted_pair_hash"), item.get("accepted_evaluation_hash"),
                   item.get("pre_rf21_pair_sha256")) for item in arms.values() if isinstance(item, dict)}
    if set(arms) != {"control", "treatment"} or len(identities) != 1 or any(item.get("pre_rf21_pair_sha256") != item.get("accepted_pair_hash") for item in arms.values()):
        raise PreflightError("H-F01 pre-RF21 arm authority changed")
    expected = build_manifest(
        root, key_present=key_present, ledger=ledger,
        authority_timestamp=value["frozen_at_utc"], execution_states=arms)
    if any(value.get(key) != expected.get(key) for key in AUTHORITY_FIELDS):
        raise PreflightError("H-F01 stable authority core changed")
    for arm, frozen in arms.items():
        current = CP.inspect(paths[arm]["experiment"])
        if any(current.get(key) != frozen.get(key) for key in ("accepted_generation", "accepted_pair_hash", "accepted_evaluation_hash", "run")):
            raise PreflightError(f"H-F01 {arm} accepted/run identity changed")
    if value.get("preregistration") != _prereg(value.get("arms", {}), expected["identity"]["gsbs_matches"], authority["git_commit"]):
        raise PreflightError("H-F01 preregistration authority changed")
    return value
def require_stage(value, task):
    status = _status(value["authority"]["ledger_path"], task)
    if task in ("RF-21", "RF-22"):
        if status != "IN_PROGRESS": raise PreflightError(f"{task} is {status}, not IN_PROGRESS")
    elif status not in ("READY", "DONE"):
        raise PreflightError(f"{task} is {status}, not READY")
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
