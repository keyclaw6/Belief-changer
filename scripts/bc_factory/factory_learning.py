"""Fail-closed outer factory-learning cycle: reviewed intervention -> frozen change -> blind holdout -> transfer experiment."""
from __future__ import annotations

import subprocess
from pathlib import Path

from .common import confined, digest, exact_keys, file_hash, identifier, lock, nonempty, now, read_json, require, seal, unseal
from .schema import DIMENSIONS, validate_config, validate_metadata


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
    exact_keys(change, {"hypothesis", "change_surface", "smallest_change", "expected_transfer", "possible_regressions"},
               label="proposed factory change")
    nonempty(change["hypothesis"], "factory hypothesis"); _strings(change["change_surface"], "change surface")
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


def registration(repo: Path, cycle_id: str) -> tuple[Path, dict]:
    root = _cycle(repo, cycle_id)
    record = unseal(root / "registration.json")
    return root, record


def register(repo: Path, cycle_id: str, learner: dict, learner_meta: dict, reviewer: dict, reviewer_meta: dict) -> Path:
    repo = repo.resolve(); identifier(cycle_id)
    validate_learner(learner); validate_reviewer(reviewer)
    validate_metadata(learner_meta); validate_metadata(reviewer_meta)
    require(learner["decision"] == "CHANGE_FACTORY", "Only CHANGE_FACTORY can register an intervention")
    require(reviewer["verdict"] == "ACCEPT", "Factory intervention requires an ACCEPTed independent review")
    config = read_json(repo / "factory/config.json"); validate_config(config)
    forbidden = {learner_meta["family"], config["profiles"]["factory"]["family"]}
    require(reviewer_meta["family"] not in forbidden, "Factory-learning reviewer must be independent of learner and generator family")
    proposed = set(learner["proposed_factory_change"]["change_surface"])
    approved = set(reviewer["approved_change_surface"])
    require(approved <= proposed, "Reviewer approved paths outside the learner proposal")
    test = learner["falsification_test"]; reviewed = reviewer["held_out_test"]
    for key in ("holdout_requirements", "success_criteria", "failure_signals"):
        require(reviewed[key] == test[key], f"Reviewer changed frozen {key}; revise learner proposal instead")
    require(not _git(repo, "status", "--porcelain"), "Register factory learning from a clean working tree before intervention edits")
    base_commit = _git(repo, "rev-parse", "HEAD")
    base_hashes = {}
    for rel in sorted(approved):
        path = confined(repo, rel)
        base_hashes[rel] = file_hash(path) if path.is_file() else None
    record = {"schema_version": 2, "cycle_id": cycle_id, "registered_at": now(), "base_commit": base_commit,
              "learner": learner, "learner_metadata": learner_meta, "review": reviewer,
              "reviewer_metadata": reviewer_meta, "approved_change_surface": sorted(approved),
              "base_path_hashes": base_hashes}
    root = _cycle(repo, cycle_id)
    require(not (root / "registration.json").exists(), "Factory-learning cycle already registered")
    with lock(root):
        seal(root / "registration.json", record)
    return root


def freeze_change(repo: Path, cycle_id: str) -> dict:
    repo = repo.resolve(); root, reg = registration(repo, cycle_id)
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
    doc = {"schema_version": 2, "cycle_id": cycle_id, "base_commit": reg["base_commit"],
           "head_commit": head, "changed_paths": sorted(changed), "path_hashes": hashes, "frozen_at": now()}
    with lock(root):
        seal(root / "change.json", doc)
    return doc


def submit_holdout(repo: Path, cycle_id: str, selection: dict, metadata: dict) -> dict:
    root, reg = registration(repo, cycle_id)
    change = unseal(root / "change.json")
    require(change["head_commit"] == _git(repo, "rev-parse", "HEAD"), "Factory changed after intervention freeze")
    exact_keys(selection, {"schema_version", "subjects", "rationale"}, label="held-out selection")
    require(selection["schema_version"] == 2, "Held-out selection schema must be v2")
    subjects = _strings(selection["subjects"], "held-out subjects", 1)
    require(len(subjects) == len(set(subjects)), "Duplicate held-out subject")
    training = set(reg["learner"]["falsification_test"]["training_subjects"])
    require(not training.intersection(subjects), "A training subject cannot also be held out in the same cycle")
    nonempty(selection["rationale"], "held-out selection rationale")
    validate_metadata(metadata)
    require(metadata["family"] not in {reg["learner_metadata"]["family"], reg["reviewer_metadata"]["family"]},
            "Held-out selector must be independent of learner and reviewer families")
    doc = {"schema_version": 2, "cycle_id": cycle_id, "change_sha256": digest(change),
           "selection": selection, "selector_metadata": metadata, "selected_at": now()}
    with lock(root):
        seal(root / "holdout.json", doc)
    return doc


def bind_experiment(repo: Path, cycle_id: str, experiment_id: str) -> dict:
    from . import experiments
    from .runs import Run
    root, reg = registration(repo, cycle_id)
    change = unseal(root / "change.json"); holdout = unseal(root / "holdout.json")
    exp_root, exp = experiments.registration(repo, experiment_id)
    require(set(exp["spec"]["subjects"]) == set(holdout["selection"]["subjects"]),
            "Transfer experiment subjects must equal the independently selected held-out set")
    require(set(exp["spec"]["allowed_change_paths"]) <= set(reg["approved_change_surface"]),
            "Transfer experiment declares paths outside approved factory change surface")
    for pair in exp["spec"]["pairs"]:
        parent, candidate = Run(repo, pair["parent_run"]), Run(repo, pair["candidate_run"])
        for rel, expected in reg["base_path_hashes"].items():
            require(parent.manifest["factory_files"].get(rel) == expected,
                    f"Transfer parent does not match pre-intervention factory at {rel}")
        for rel, expected in change["path_hashes"].items():
            require(candidate.manifest["factory_files"].get(rel) == expected,
                    f"Transfer candidate does not match frozen intervention at {rel}")
    doc = {"schema_version": 2, "cycle_id": cycle_id, "experiment_id": experiment_id,
           "registration_sha256": digest(exp), "holdout_sha256": digest(holdout),
           "change_sha256": digest(change), "bound_at": now()}
    with lock(root):
        seal(root / "experiment.json", doc)
    return doc


def decide(repo: Path, cycle_id: str, calibration: dict | None = None) -> dict:
    from . import experiments
    root, _ = registration(repo, cycle_id)
    binding = unseal(root / "experiment.json")
    result = experiments.decide(repo, binding["experiment_id"], calibration)
    verdict = ("KEEP_FACTORY_CHANGE" if result["decision"] == "KEEP_ELIGIBLE"
               else "REJECT_FACTORY_CHANGE" if result["decision"] == "REJECT"
               else "INCONCLUSIVE")
    doc = {"schema_version": 2, "cycle_id": cycle_id, "decision": verdict,
           "experiment_decision": result, "binding_sha256": digest(binding), "decided_at": now()}
    with lock(root):
        seal(root / "decision.json", doc)
    return doc
