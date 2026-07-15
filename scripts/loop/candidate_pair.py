"""RF-02 sealed candidate pairs and atomic accepted-generation promotion."""
import json
from pathlib import Path
import loopcfg, draft_batch_contract as DB, draft_batch_lifecycle as DL
import pair_contract as PC, pair_store as PS, writer_operation as WO
from pair_transition import add_book, assert_run, initialize, promote, reject, status
SCHEMA = 6
MANIFEST = "pair.json"
DECISION = "decision.json"
class PairError(RuntimeError):
    pass
def _fail(exc):
    if isinstance(exc, PairError):
        raise exc
    raise PairError(str(exc)) from exc
def _grounded(root):
    import first_draft_batch as FB, grounded_review as GR
    try: FB.require_frozen_batch(root); GR.require_complete(root)
    except (FB.BatchError, GR.GroundedReviewError) as exc: raise PairError(str(exc)) from exc
def candidate_tree(root): return Path(root).absolute() / "candidate"
def evaluation_tree(root): return Path(root).absolute() / "evaluation"
def evidence_tree(root): return Path(root).absolute() / "evidence"
def _manifest_path(root): return Path(root).absolute() / MANIFEST
def _chapters(value):
    out = []
    for token in str(value).split(","):
        token = token.strip()
        if not token:
            raise PairError("chapter selection is empty")
        if "-" in token:
            lo, hi = token.split("-", 1)
            if not lo.isdigit() or not hi.isdigit() or int(lo) > int(hi):
                raise PairError(f"invalid chapter selection: {value}")
            out.extend(range(int(lo), int(hi) + 1))
        elif token.isdigit():
            out.append(int(token))
        else:
            raise PairError(f"invalid chapter selection: {value}")
    if not out or len(out) != len(set(out)) or out != sorted(out):
        raise PairError(f"invalid chapter selection: {value}")
    return out
def _recorded_hash(entries, key):
    try:
        states = [{"group": item["group"], "path": item["path"],
                   "sha256": item[key]} for item in entries]
    except (KeyError, TypeError) as exc:
        raise PairError("candidate pair metadata is malformed") from exc
    return PS.state_hash(states)
def _validate_entries(entries, groups):
    if not isinstance(entries, list) or not entries:
        return False
    paths = [item.get("path") for item in entries if isinstance(item, dict)]
    return len(paths) == len(entries) == len(set(paths)) and all(
        item.get("group") in groups and isinstance(path, str) and path
        and not Path(path).is_absolute() and ".." not in Path(path).parts
        for path, item in zip(paths, entries))
def load(root):
    path = _manifest_path(root)
    try:
        value = json.loads(PS._safe_file(path, Path(root).absolute()).read_text(encoding="utf-8"))
        DL.recover(root, value)
        value = json.loads(PS._safe_file(path, Path(root).absolute()).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, PS.StoreError, DL.LifecycleError) as exc:
        raise PairError(f"invalid candidate pair manifest: {exc}") from exc
    run = value.get("run")
    state = value.get("state")
    if value.get("schema") != SCHEMA \
            or state not in ("CANDIDATE", "WRITER_HANDOFF", "DRAFTING",
                             "BATCH_FROZEN", "SEALED") \
            or not _validate_entries(value.get("entries"), {"config", "product"}) \
            or not _validate_entries(value.get("evaluation"), {"evaluation"}) \
            or not PC.valid_run(run, Path(root).name) \
            or not WO.valid(value.get("operation"), state):
        raise PairError("invalid candidate pair manifest schema")
    try:
        DL.validate(root, value)
        DB.validate_pair(value, root)
    except (DL.LifecycleError, DB.BatchError) as exc:
        raise PairError(str(exc)) from exc
    outputs = value.get("outputs")
    allowed = {f"{run['book']}/commissions/chapter-{number:02}.md"
               for number in run["chapters"]}
    output_paths = {item.get("path") for item in outputs or () if isinstance(item, dict)}
    entry_paths = {item["path"] for item in value["entries"]}
    if not isinstance(outputs, list) or outputs and not _validate_entries(outputs, {"product"}) \
            or not output_paths <= allowed or output_paths & entry_paths:
        raise PairError("invalid candidate commission outputs")
    if _recorded_hash(value["entries"], "accepted_sha256") != value.get("accepted_pair_hash") \
            or _recorded_hash(value["evaluation"], "accepted_sha256") != value.get("accepted_evaluation_hash"):
        raise PairError("accepted pair manifest hash is invalid")
    return value
def _bare(entries):
    return [{"group": item["group"], "path": item["path"]} for item in entries]
def _members(manifest):
    return manifest["entries"] + manifest["outputs"]
def _copy(target, source, entries):
    for item in entries:
        data = PS._safe_file(Path(source) / item["path"], source).read_bytes()
        PS.write(Path(target) / item["path"], data)
def snapshot(root, accepted_root, book, chapters="1-3", config="loop/config.yaml",
             iteration=None):
    """Copy one already-pinned accepted generation into an unused experiment."""
    experiment, accepted = Path(root).absolute(), Path(accepted_root).absolute()
    try:
        if experiment.parent != accepted / "loop/experiments":
            raise PairError("candidate snapshots must be loop/experiments/<id>")
        PS.safe_dir(accepted)
        PS.safe_dir(experiment, accepted)
        if any(experiment.iterdir()):
            raise PairError(f"experiment id is reused or nonempty: {experiment}")
        PS.same_filesystem(experiment, accepted, PS.state_dir(accepted))
        tree, generation, registry = PS.current(accepted)
        pair_root, eval_root = tree / "pair", tree / "evaluation"
        contract = PC.derive(pair_root, book, config, registry["entries"], eval_root)
        entries = [{**item, "accepted_sha256": PS.sha(
            PS._safe_file(pair_root / item["path"], pair_root).read_bytes())}
            for item in contract["pair"]]
        evaluation = [{"group": "evaluation", "path": path, "accepted_sha256": PS.sha(
            PS._safe_file(eval_root / path, eval_root).read_bytes())}
            for path in contract["evaluation"]]
        if _bare(entries) != registry["entries"] or _bare(evaluation) != registry["evaluation"]:
            raise PairError("requested run contract is not the initialized generation contract")
        _copy(candidate_tree(experiment), pair_root, entries)
        _copy(evaluation_tree(experiment), eval_root, evaluation)
        value = {
            "schema": SCHEMA, "state": "CANDIDATE", "tested_hash": None,
            "accepted_generation": generation,
            "accepted_pair_hash": registry["pair_hash"],
            "accepted_evaluation_hash": registry["evaluation_hash"],
            "entries": entries, "outputs": [], "evaluation": evaluation,
            "operation": None, "draft_batch": None, "draft_batch_start": None,
            "run": {"experiment_id": experiment.name,
                    "iteration_id": iteration if iteration is not None else experiment.name,
                    "book": contract["book"], "chapters": _chapters(chapters),
                    "config": contract["config"]},
        }
        DL.initialize(experiment, value)
        PS.write_json(_manifest_path(experiment), value)
        return value
    except (PS.StoreError, PC.ContractError, DL.LifecycleError, OSError) as exc:
        _fail(exc)
def candidate_path(root, relative):
    if Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise PairError(f"invalid candidate path: {relative}")
    return candidate_tree(root) / relative
def require_member(root, path, group=None, manifest=None):
    manifest = manifest or load(root)
    tree = candidate_tree(root)
    try:
        relative = Path(path).absolute().relative_to(tree).as_posix()
    except ValueError as exc:
        raise PairError(f"path escapes candidate generation: {path}") from exc
    matches = [item for item in _members(manifest) if item["path"] == relative]
    if len(matches) != 1 or group and matches[0]["group"] != group:
        raise PairError(f"path is not a declared {group or 'pair'} member: {path}")
    try:
        return PS._safe_file(Path(path).absolute(), tree)
    except PS.StoreError as exc:
        _fail(exc)
def _check_eval_contract(root, manifest):
    tree = candidate_tree(root)
    cfg = loopcfg.load(PS._safe_file(tree / manifest["run"]["config"], tree))
    expected = set(PC.evaluation_paths(cfg, evaluation_tree(root)))
    declared = {item["path"] for item in manifest["evaluation"]}
    if expected != declared:
        raise PairError(f"candidate config changed evaluation membership: "
                        f"missing={sorted(expected-declared)}, extra={sorted(declared-expected)}")
    return cfg
def _actual(root, manifest):
    pair = PS.exact_tree(candidate_tree(root), _members(manifest))
    evaluation = PS.exact_tree(evaluation_tree(root), manifest["evaluation"])
    pair_hash, eval_hash = PS.state_hash(pair), PS.state_hash(evaluation)
    if eval_hash != manifest["accepted_evaluation_hash"]:
        raise PairError("sealed evaluation inputs drifted from the accepted contract")
    return pair_hash, eval_hash
def _model_identity(cfg):
    keys = ("model", "provider", "reasoning", "route", "judge_k", "campaign",
            "instrument_version", "epsilon", "tripwire", "threshold", "weights")
    return {key: cfg[key] for key in sorted(cfg) if any(part in key for part in keys)}
def _identity(manifest):
    return PS.state_hash({key: value for key, value in manifest.items()
                          if key != "tested_hash"})
def seal(root, interrupt=None):
    manifest = load(root)
    if manifest["state"] not in ("CANDIDATE", "WRITER_HANDOFF", "BATCH_FROZEN"):
        raise PairError("SEALED is terminal")
    try:
        if manifest.get("draft_batch") is not None:
            _grounded(root)
        WO.read(root, manifest.get("operation"))
        cfg = _check_eval_contract(root, manifest)
        pair_hash, eval_hash = _actual(root, manifest)
        config_data = PS._safe_file(candidate_tree(root) / manifest["run"]["config"],
                                    candidate_tree(root)).read_bytes()
        sealed = dict(manifest)
        sealed["state"] = "SEALED"
        sealed["sealed"] = {
            "pair_hash": pair_hash, "evaluation_hash": eval_hash,
            "config_sha256": PS.sha(config_data),
            "config_values_sha256": PS.state_hash(cfg),
            "model_identity": _model_identity(cfg),
        }
        sealed["tested_hash"] = _identity(sealed)
        PS.exact_layout(root, manifest, {".pair.json.rf02-tmp": PS.json_bytes(sealed)})
        PS.freeze_files(candidate_tree(root))
        PS.freeze_files(evaluation_tree(root))
        WO.freeze(root, manifest.get("operation"))
        PS.write_json(_manifest_path(root), sealed, interrupt)
        _manifest_path(root).chmod(0o444)
        return sealed["tested_hash"]
    except (PS.StoreError, PC.ContractError, WO.OperationError, DB.BatchError) as exc:
        _fail(exc)
def verify_sealed(root, tested_hash, expected=None):
    manifest = load(root)
    if manifest["state"] != "SEALED" or manifest.get("tested_hash") != tested_hash:
        raise PairError("tested pair hash does not match sealed identity")
    try:
        if manifest.get("draft_batch") is not None:
            _grounded(root)
        WO.read(root, manifest.get("operation"))
        cfg = _check_eval_contract(root, manifest)
        PS.exact_layout(root, manifest, expected)
        pair_hash, eval_hash = _actual(root, manifest)
        sealed = manifest.get("sealed") or {}
        config_data = PS._safe_file(candidate_tree(root) / manifest["run"]["config"],
                                    candidate_tree(root)).read_bytes()
        expected = (pair_hash, eval_hash, PS.sha(config_data), PS.state_hash(cfg),
                    _model_identity(cfg), _identity(manifest))
        actual = (sealed.get("pair_hash"), sealed.get("evaluation_hash"),
                  sealed.get("config_sha256"), sealed.get("config_values_sha256"),
                  sealed.get("model_identity"), tested_hash)
        if expected != actual:
            raise PairError("sealed metadata, configuration, product, or inputs drifted")
        return manifest
    except (PS.StoreError, PC.ContractError, WO.OperationError, DB.BatchError) as exc:
        _fail(exc)
def _view(root, manifest):
    tree = candidate_tree(root)
    cfg = dict(loopcfg.load(PS._safe_file(tree / manifest["run"]["config"], tree)))
    evaluation, evidence = evaluation_tree(root), evidence_tree(root)
    cfg.update(judge_rubric=str(evaluation / cfg["judge_rubric"]),
               reference_dir=str(evaluation / cfg["reference_dir"]),
               reference_epub="SEALED-EVALUATION-DOES-NOT-READ-EPUB",
               history_results_tsv=str(evaluation / cfg.get("results_tsv", "loop/results.tsv")),
               scores_dir=str(evidence / "scores"), tasks_dir=str(evidence / "iterations"),
               results_tsv=str(evidence / "results.tsv"))
    return {"manifest": manifest, "pair": tree,
            "evaluation": evaluation, "evidence": evidence, "config": cfg}
def pending_sealed(root, tested_hash):
    """Load guarded paths needed to recompute recovery bytes; not a verified pair."""
    manifest = load(root)
    if manifest["state"] != "SEALED" or manifest.get("tested_hash") != tested_hash:
        raise PairError("tested pair hash does not match sealed identity")
    try:
        PS.recovery_preflight(root)
        return _view(root, manifest)
    except PS.StoreError as exc:
        _fail(exc)
def open_sealed(root, tested_hash, expected=None):
    return _view(root, verify_sealed(root, tested_hash, expected))
