"""Fail-closed outer factory-learning cycle: reviewed intervention -> frozen change -> blind holdout -> transfer experiment."""
from __future__ import annotations

import subprocess
from pathlib import Path

from .common import confined, digest, exact_keys, file_hash, identifier, lock, nonempty, now, read_json, require, seal, unseal
from .schema import DIMENSIONS, validate_config, validate_metadata

PROTECTED_EVALUATION_PATHS = {
    "AGENTS.md",
    "docs/CROSS-ITERATION-LEARNING.md",
    "factory/config.json",
    "loop/PROGRAM.md",
    "loop/judges/pairwise.md",
    "loop/prompts/factory-holdout-selector.md",
    "loop/prompts/factory-learner.md",
    "loop/prompts/factory-learning-reviewer.md",
    "loop/prompts/hypothesizer.md",
    "loop/prompts/trace-analyzer.md",
    "prompts/factory-orchestrator.md",
    ".opencode/agent/factory.md",
    ".opencode/agents/factory-holdout-selector.md",
    ".opencode/agents/factory-learner.md",
    ".opencode/agents/factory-learning-reviewer.md",
    ".pi/agents/factory-holdout-selector.md",
    ".pi/agents/factory-learner.md",
    ".pi/agents/factory-learning-reviewer.md",
    ".pi/agents/factory-orchestrator.md",
    ".pi/agents/hypothesizer.md",
    ".pi/agents/judge.md",
    ".pi/agents/trace-analyzer.md",
    "scripts/factory.py",
    "scripts/bc_factory/adapters.py",
    "scripts/bc_factory/cli.py",
    "scripts/bc_factory/common.py",
    "scripts/bc_factory/experiments.py",
    "scripts/bc_factory/factory_learning.py",
    "scripts/bc_factory/learning.py",
    "scripts/bc_factory/regression.py",
    "scripts/bc_factory/runs.py",
    "scripts/bc_factory/schema.py",
}


def _strings(value, label: str, minimum: int = 0) -> list[str]:
    require(isinstance(value, list) and len(value) >= minimum and all(isinstance(x, str) and x.strip() for x in value),
            f"{label} must be a list of nonempty strings")
    return value


def validate_learner(data: dict) -> None:
    exact_keys(data, {"schema_version", "decision", "observations", "candidate_root_causes",
                      "subject_specific_lessons", "transferable_factory_lessons", "protected_strengths",
                      "proposed_factory_change", "falsification_test", "confidence", "reasoning_summary"},
               label="factory learner")
    require(data["schema_version"] == 2, "Factory learner schema must be v2")
    require(data["decision"] in ("CHANGE_FACTORY", "KEEP_FACTORY", "MEASURE_MORE"), "Invalid factory learner decision")
    _strings(data["observations"], "observations")
    require(isinstance(data["candidate_root_causes"], list), "candidate_root_causes must be a list")
    for item in data["candidate_root_causes"]:
        exact_keys(item, {"mechanism", "support", "alternatives"}, label="root cause")
        nonempty(item["mechanism"], "root cause mechanism"); _strings(item["support"], "root cause support", 1)
        _strings(item["alternatives"], "root cause alternatives")
    require(isinstance(data["subject_specific_lessons"], list), "subject_specific_lessons must be a list")
    for item in data["subject_specific_lessons"]:
        exact_keys(item, {"subject", "lesson", "reason"}, label="subject-specific lesson")
        identifier(item["subject"]); nonempty(item["lesson"], "lesson"); nonempty(item["reason"], "lesson reason")
    require(isinstance(data["transferable_factory_lessons"], list), "transferable_factory_lessons must be a list")
    for item in data["transferable_factory_lessons"]:
        exact_keys(item, {"lesson", "evidence", "scope"}, label="transferable lesson")
        nonempty(item["lesson"], "transferable lesson"); _strings(item["evidence"], "transferable evidence", 1)
        nonempty(item["scope"], "transferable lesson scope")
    require(isinstance(data["protected_strengths"], list), "protected_strengths must be a list")
    for item in data["protected_strengths"]:
        exact_keys(item, {"dimension", "constraint", "evidence"}, label="protected strength")
        require(item["dimension"] in DIMENSIONS, "Unknown protected dimension")
        nonempty(item["constraint"], "protected constraint"); nonempty(item["evidence"], "protected evidence")
    change = data["proposed_factory_change"]
    exact_keys(change, {"hypothesis", "primary_dimension", "change_surface", "smallest_change", "expected_transfer", "possible_regressions"},
               label="proposed factory change")
    nonempty(change["hypothesis"], "factory hypothesis")
    require(change["primary_dimension"] in DIMENSIONS, "Unknown factory-change primary dimension")
    _strings(change["change_surface"], "change surface")
    nonempty(change["smallest_change"], "smallest change"); nonempty(change["expected_transfer"], "expected transfer")
    _strings(change["possible_regressions"], "possible regressions")
    test = data["falsification_test"]
    exact_keys(test, {"training_subjects", "holdout_requirements", "success_criteria", "failure_signals", "leakage_rule"},
               label="falsification test")
    subjects = _strings(test["training_subjects"], "training subjects", 1)
    require(len(subjects) == len(set(subjects)), "Duplicate training subject")
    _strings(test["holdout_requirements"], "holdout requirements", 1)
    _strings(test["success_criteria"], "success criteria", 1); _strings(test["failure_signals"], "failure signals", 1)
    nonempty(test["leakage_rule"], "leakage rule")
    require(data["confidence"] in ("low", "medium", "high"), "Invalid learner confidence")
    nonempty(data["reasoning_summary"], "learner reasoning")
    if data["decision"] == "CHANGE_FACTORY":
        require(bool(change["change_surface"]), "Factory change requires an explicit change surface")


def validate_reviewer(data: dict) -> None:
    exact_keys(data, {"schema_version", "verdict", "checks", "findings", "approved_change_surface",
                      "held_out_test", "reasoning_summary"}, label="factory-learning reviewer")
    require(data["schema_version"] == 2, "Factory-learning reviewer schema must be v2")
    require(data["verdict"] in ("ACCEPT", "REVISE", "REJECT", "MEASURE_MORE"), "Invalid reviewer verdict")
    check_names = {"transferable", "not_subject_overfit", "causal_honesty", "minimal_change",
                   "protected_strengths", "held_out_integrity", "judge_overfit_control", "falsifiable"}
    exact_keys(data["checks"], check_names, label="factory-learning checks")
    require(all(type(v) is bool for v in data["checks"].values()), "Factory-learning checks must be explicit booleans")
    require(isinstance(data["findings"], list), "Factory-learning findings must be a list")
    for item in data["findings"]:
        exact_keys(item, {"kind", "severity", "explanation", "repair"}, label="factory-learning finding")
        require(item["kind"] in ("TRANSFER", "OVERFIT", "CAUSALITY", "SCOPE", "REGRESSION_RISK",
                                 "HELD_OUT_LEAKAGE", "JUDGE_OVERFIT", "MEASUREMENT"), "Unknown factory-learning finding")
        require(item["severity"] in ("material", "critical"), "Invalid factory-learning finding severity")
        nonempty(item["explanation"], "finding explanation"); nonempty(item["repair"], "finding repair")
    _strings(data["approved_change_surface"], "approved change surface")
    holdout = data["held_out_test"]
    exact_keys(holdout, {"holdout_requirements", "success_criteria", "failure_signals"}, label="reviewed holdout test")
    _strings(holdout["holdout_requirements"], "reviewed holdout requirements", 1)
    _strings(holdout["success_criteria"], "reviewed success criteria", 1)
    _strings(holdout["failure_signals"], "reviewed failure signals", 1)
    nonempty(data["reasoning_summary"], "reviewer reasoning")
    if data["verdict"] == "ACCEPT":
        require(all(data["checks"].values()) and not data["findings"], "ACCEPT requires all checks and no findings")
        require(bool(data["approved_change_surface"]), "ACCEPT needs an approved change surface")


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    require(proc.returncode == 0, f"Git command failed: {' '.join(args)}")
    return proc.stdout.strip()


def _cycle(repo: Path, cycle_id: str) -> Path:
    return confined(repo, f"factory-learning/{identifier(cycle_id)}")


def _factory_snapshot(repo: Path) -> dict[str, str]:
    from .runs import active_files
    files = {}
    for rel in active_files(repo):
        path = confined(repo, rel)
        require(path.is_file(), f"Active factory file missing: {rel}")
        files[rel] = file_hash(path)
    return files


def registration(repo: Path, cycle_id: str) -> tuple[Path, dict]:
    root = _cycle(repo, cycle_id)
    record = unseal(root / "registration.json")
    return root, record


def register(repo: Path, cycle_id: str, learner: dict, learner_meta: dict, reviewer: dict, reviewer_meta: dict) -> Path:
    repo = repo.resolve(); identifier(cycle_id)
    validate_learner(learner); validate_reviewer(reviewer)
    root = _cycle(repo, cycle_id)
    if (root / "registration.json").exists():
        existing = unseal(root / "registration.json")
        require(existing["learner"] == learner and existing["learner_metadata"] == learner_meta
                and existing["review"] == reviewer and existing["reviewer_metadata"] == reviewer_meta,
                "Factory-learning cycle already exists with different frozen inputs")
        require(existing["base_commit"] == _git(repo, "rev-parse", "HEAD")
                and existing["experimental_branch"] == _git(repo, "branch", "--show-current"),
                "Existing factory-learning registration belongs to another source state")
        return root
    validate_metadata(learner_meta); validate_metadata(reviewer_meta)
    require(learner_meta["harness"] != "fixture" and reviewer_meta["harness"] != "fixture",
            "Fixture outer-learning agents cannot authorize a real factory intervention")
    require(learner["decision"] == "CHANGE_FACTORY", "Only CHANGE_FACTORY can register an intervention")
    require(reviewer["verdict"] == "ACCEPT", "Factory intervention requires an ACCEPTed independent review")
    config = read_json(repo / "factory/config.json"); validate_config(config)
    forbidden = {learner_meta["family"], config["profiles"]["factory"]["family"]}
    require(reviewer_meta["family"] not in forbidden, "Factory-learning reviewer must be independent of learner and generator family")
    proposed = set(learner["proposed_factory_change"]["change_surface"])
    approved = set(reviewer["approved_change_surface"])
    require(approved <= proposed, "Reviewer approved paths outside the learner proposal")
    require(not approved.intersection(PROTECTED_EVALUATION_PATHS),
            "Factory self-optimization cannot edit its own evaluator, routing, or learning control plane")
    test = learner["falsification_test"]; reviewed = reviewer["held_out_test"]
    for key in ("holdout_requirements", "success_criteria", "failure_signals"):
        require(reviewed[key] == test[key], f"Reviewer changed frozen {key}; revise learner proposal instead")
    require(not _git(repo, "status", "--porcelain"), "Register factory learning from a clean working tree before intervention edits")
    branch_name = _git(repo, "branch", "--show-current")
    require(bool(branch_name) and branch_name != "main",
            "Factory-learning interventions must run on an isolated experimental branch; merge to main only after KEEP_FACTORY_CHANGE")
    base_commit = _git(repo, "rev-parse", "HEAD")
    base_hashes = {}
    for rel in sorted(approved):
        path = confined(repo, rel)
        base_hashes[rel] = file_hash(path) if path.is_file() else None
    base_factory_files = _factory_snapshot(repo)
    record = {"schema_version": 2, "cycle_id": cycle_id, "registered_at": now(), "base_commit": base_commit,
              "experimental_branch": branch_name,
              "learner": learner, "learner_metadata": learner_meta, "review": reviewer,
              "reviewer_metadata": reviewer_meta, "approved_change_surface": sorted(approved),
              "base_path_hashes": base_hashes, "base_factory_files": base_factory_files,
              "base_factory_digest": digest(base_factory_files)}
    with lock(root):
        seal(root / "registration.json", record)
    return root


def freeze_change(repo: Path, cycle_id: str) -> dict:
    repo = repo.resolve(); root, reg = registration(repo, cycle_id)
    if (root / "change.json").exists():
        existing = unseal(root / "change.json")
        require(_git(repo, "branch", "--show-current") == reg["experimental_branch"]
                and existing["head_commit"] == _git(repo, "rev-parse", "HEAD"),
                "Existing frozen intervention does not match current branch/HEAD")
        return existing
    require(_git(repo, "branch", "--show-current") == reg["experimental_branch"],
            "Factory-learning cycle moved to another branch")
    require(not _git(repo, "status", "--porcelain"), "Freeze only a committed, clean intervention")
    head = _git(repo, "rev-parse", "HEAD")
    require(head != reg["base_commit"], "No factory change exists to freeze")
    changed = [x for x in _git(repo, "diff", "--name-only", reg["base_commit"], head).splitlines() if x]
    require(bool(changed), "No changed paths")
    approved = set(reg["approved_change_surface"])
    require(set(changed) <= approved, f"Factory intervention escaped approved change surface: {sorted(set(changed)-approved)}")
    hashes = {}
    for rel in sorted(changed):
        path = confined(repo, rel)
        hashes[rel] = file_hash(path) if path.is_file() else None
    factory_files = _factory_snapshot(repo)
    doc = {"schema_version": 2, "cycle_id": cycle_id, "base_commit": reg["base_commit"],
           "head_commit": head, "changed_paths": sorted(changed), "path_hashes": hashes,
           "factory_files": factory_files, "factory_digest": digest(factory_files), "frozen_at": now()}
    with lock(root):
        seal(root / "change.json", doc)
    return doc


def submit_holdout(repo: Path, cycle_id: str, selection: dict, metadata: dict) -> dict:
    root, reg = registration(repo, cycle_id)
    change = unseal(root / "change.json")
    if (root / "holdout.json").exists():
        existing = unseal(root / "holdout.json")
        require(existing["selection"] == selection and existing["selector_metadata"] == metadata
                and existing["change_sha256"] == digest(change),
                "Held-out selection is already frozen with different inputs")
        return existing
    require(_git(repo, "branch", "--show-current") == reg["experimental_branch"],
            "Held-out selection must occur on the frozen experimental branch")
    require(not _git(repo, "status", "--porcelain"), "Held-out selection requires the frozen intervention tree to be clean")
    require(change["head_commit"] == _git(repo, "rev-parse", "HEAD"), "Factory changed after intervention freeze")
    exact_keys(selection, {"schema_version", "subjects", "rationale"}, label="held-out selection")
    require(selection["schema_version"] == 2, "Held-out selection schema must be v2")
    subjects = _strings(selection["subjects"], "held-out subjects", 2)
    require(len(subjects) == len(set(subjects)), "Duplicate held-out subject")
    training = set(reg["learner"]["falsification_test"]["training_subjects"])
    require(not training.intersection(subjects), "A training subject cannot also be held out in the same cycle")
    prior_run_subjects = set()
    runs_root = repo / "runs"
    if runs_root.is_dir():
        for manifest in runs_root.glob("*/manifest.json"):
            prior = unseal(manifest)
            require(isinstance(prior.get("subject"), str) and prior["subject"].strip(),
                    f"Historical run manifest lacks a valid subject: {manifest.parent.name}")
            prior_run_subjects.add(prior["subject"])
    require(not prior_run_subjects.intersection(subjects),
            "Held-out topics must be unseen: a selected subject already has run history")
    previously_revealed = set()
    state_root = repo / "factory-learning"
    if state_root.is_dir():
        for path in state_root.glob("*/holdout.json"):
            if path == root / "holdout.json":
                continue
            prior = unseal(path)
            previously_revealed.update(prior["selection"]["subjects"])
    require(not previously_revealed.intersection(subjects),
            "A previously revealed held-out topic cannot count as unseen transfer evidence again")
    nonempty(selection["rationale"], "held-out selection rationale")
    validate_metadata(metadata)
    require(metadata["harness"] != "fixture", "Fixture holdout selection cannot authorize a real transfer test")
    config = read_json(repo / "factory/config.json"); validate_config(config)
    forbidden = {reg["learner_metadata"]["family"], reg["reviewer_metadata"]["family"],
                 config["profiles"]["factory"]["family"]}
    require(metadata["family"] not in forbidden,
            "Held-out selector must be independent of learner, reviewer, and generator families")
    doc = {"schema_version": 2, "cycle_id": cycle_id, "change_sha256": digest(change),
           "selection": selection, "selector_metadata": metadata, "selected_at": now()}
    with lock(root):
        seal(root / "holdout.json", doc)
    return doc


def bind_experiment(repo: Path, cycle_id: str, experiment_id: str) -> dict:
    from . import experiments
    from .runs import Run
    root, reg = registration(repo, cycle_id)
    if (root / "experiment.json").exists():
        existing = unseal(root / "experiment.json")
        require(existing["experiment_id"] == experiment_id,
                "Factory-learning cycle already binds a different transfer experiment")
        experiments.registration(repo, experiment_id)
        return existing
    require(_git(repo, "branch", "--show-current") == reg["experimental_branch"],
            "Transfer binding must occur on the frozen experimental branch")
    require(not _git(repo, "status", "--porcelain"), "Transfer binding requires the frozen intervention tree to be clean")
    change = unseal(root / "change.json"); holdout = unseal(root / "holdout.json")
    exp_root, exp = experiments.registration(repo, experiment_id)
    require(set(exp["spec"]["subjects"]) == set(holdout["selection"]["subjects"]),
            "Transfer experiment subjects must equal the independently selected held-out set")
    require(exp["spec"]["primary_dimension"] == reg["learner"]["proposed_factory_change"]["primary_dimension"],
            "Transfer experiment changed the predeclared primary quality dimension")
    require(set(exp["spec"]["allowed_change_paths"]) <= set(reg["approved_change_surface"]),
            "Transfer experiment declares paths outside approved factory change surface")
    for pair in exp["spec"]["pairs"]:
        parent, candidate = Run(repo, pair["parent_run"]), Run(repo, pair["candidate_run"])
        require(parent.manifest["factory_files"] == reg["base_factory_files"]
                and parent.manifest["factory_digest"] == reg["base_factory_digest"],
                "Transfer parent is not the exact pre-intervention factory snapshot")
        require(candidate.manifest["factory_files"] == change["factory_files"]
                and candidate.manifest["factory_digest"] == change["factory_digest"],
                "Transfer candidate is not the exact frozen intervention factory snapshot")
    doc = {"schema_version": 2, "cycle_id": cycle_id, "experiment_id": experiment_id,
           "registration_sha256": digest(exp), "holdout_sha256": digest(holdout),
           "change_sha256": digest(change), "bound_at": now()}
    with lock(root):
        seal(root / "experiment.json", doc)
    return doc


def decide(repo: Path, cycle_id: str) -> dict:
    from . import experiments
    root, reg = registration(repo, cycle_id)
    if (root / "decision.json").exists():
        existing = unseal(root / "decision.json")
        binding = unseal(root / "experiment.json")
        require(existing["binding_sha256"] == digest(binding),
                "Stored factory-learning decision is bound to another experiment state")
        return existing
    require(_git(repo, "branch", "--show-current") == reg["experimental_branch"],
            "Factory-learning decision must occur on its frozen experimental branch")
    require(not _git(repo, "status", "--porcelain"), "Factory-learning decision requires a clean frozen intervention tree")
    change = unseal(root / "change.json")
    require(change["head_commit"] == _git(repo, "rev-parse", "HEAD"),
            "Factory changed after the intervention was frozen")
    binding = unseal(root / "experiment.json")
    result = experiments.transfer_decide(repo, binding["experiment_id"])
    if result["decision"] == "TRANSFER_ELIGIBLE_NONPROMOTIONAL":
        require(len(result["judge_models"]) == 1, "Transfer retention requires one stable judge model/family")
        holdout = unseal(root / "holdout.json")
        config = read_json(repo / "factory/config.json"); validate_config(config)
        judge_family = result["judge_models"][0]["family"]
        forbidden = {reg["learner_metadata"]["family"], reg["reviewer_metadata"]["family"],
                     holdout["selector_metadata"]["family"], config["profiles"]["factory"]["family"]}
        if judge_family in forbidden:
            result["decision"] = "REJECT_TRANSFER"
            result["reasons"].append("Transfer judge family is not independent of the generator/learner/reviewer/selector roles")
        prior_kept = []
        state_root = repo / "factory-learning"
        if state_root.is_dir():
            for path in state_root.glob("*/decision.json"):
                if path == root / "decision.json":
                    continue
                prior = unseal(path)
                if prior.get("decision") == "KEEP_FACTORY_CHANGE":
                    models = prior.get("experiment_decision", {}).get("judge_models", [])
                    if len(models) == 1:
                        prior_kept.append((prior.get("decided_at", ""), models[0]["family"]))
        if prior_kept and max(prior_kept)[1] == judge_family:
            result["decision"] = "INCONCLUSIVE"
            result["reasons"].append("Rotate the transfer judge family after a retained factory change to reduce judge overfitting")
    verdict = ("KEEP_FACTORY_CHANGE" if result["decision"] == "TRANSFER_ELIGIBLE_NONPROMOTIONAL"
               else "REJECT_FACTORY_CHANGE" if result["decision"] == "REJECT_TRANSFER"
               else "INCONCLUSIVE")
    doc = {"schema_version": 2, "cycle_id": cycle_id, "decision": verdict,
           "experiment_decision": result, "binding_sha256": digest(binding), "decided_at": now()}
    with lock(root):
        seal(root / "decision.json", doc)
    return doc
