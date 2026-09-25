"""Fail-closed outer factory-learning cycle: reviewed intervention -> frozen change -> blind holdout -> transfer experiment."""
from __future__ import annotations

import subprocess
from pathlib import Path

from .common import confined, digest, exact_keys, file_hash, identifier, lock, nonempty, now, read_json, require, seal, unseal
from .schema import DIMENSIONS, validate_config, validate_metadata

PLAN_AFFECTING_PATHS = {
    "prompts/evidence-reviewer.md",
    "prompts/master-plan-skill-v2.md",
    "prompts/master-plan-reviewer-v2.md",
    "prompts/style-guide.md",
}

SELF_OPTIMIZABLE_PRODUCTION_PATHS = {
    "prompts/evidence-reviewer.md",
    "prompts/master-plan-skill-v2.md",
    "prompts/master-plan-reviewer-v2.md",
    "prompts/chapter-writer.md",
    "prompts/chapter-reviewer.md",
    "prompts/reader-state.md",
    "prompts/book-editor.md",
    "prompts/final-auditor.md",
    "prompts/style-guide.md",
}

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
    exact_keys(data, {"schema_version", "evidence_sha256", "decision", "observations", "candidate_root_causes",
                      "subject_specific_lessons", "transferable_factory_lessons", "protected_strengths",
                      "proposed_factory_change", "falsification_test", "confidence", "reasoning_summary"},
               label="factory learner")
    require(isinstance(data["evidence_sha256"], str) and len(data["evidence_sha256"]) == 64,
            "Factory learner must bind the frozen training evidence hash")
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
    exact_keys(test, {"training_subjects", "holdout_requirements", "acceptance_policy",
                      "success_criteria", "failure_signals", "leakage_rule"},
               label="falsification test")
    require(test["acceptance_policy"] == "strict_transfer_v1",
            "Factory-learning acceptance policy is fixed to strict_transfer_v1")
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
    exact_keys(data, {"schema_version", "evidence_sha256", "learner_sha256", "verdict", "checks", "findings",
                      "approved_change_surface", "held_out_test", "reasoning_summary"}, label="factory-learning reviewer")
    for key in ("evidence_sha256", "learner_sha256"):
        require(isinstance(data[key], str) and len(data[key]) == 64, f"{key} must be a SHA-256")
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
    exact_keys(holdout, {"holdout_requirements", "acceptance_policy", "success_criteria", "failure_signals"},
               label="reviewed holdout test")
    require(holdout["acceptance_policy"] == "strict_transfer_v1",
            "Reviewer must preserve strict_transfer_v1 acceptance policy")
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


def _holdout_record_path(repo: Path, cycle_id: str) -> Path:
    return confined(repo, f"loop/holdout-registry/{identifier(cycle_id)}.json")


def _history_record_path(repo: Path, cycle_id: str) -> Path:
    return confined(repo, f"loop/factory-learning-history/{identifier(cycle_id)}.json")


def _post_freeze_paths(repo: Path, change_head: str) -> list[str]:
    current = _git(repo, "rev-parse", "HEAD")
    if current == change_head:
        return []
    return [x for x in _git(repo, "diff", "--name-only", change_head, current).splitlines() if x]


def _require_only_holdout_history_after_freeze(repo: Path, change: dict) -> None:
    changed = _post_freeze_paths(repo, change["head_commit"])
    allowed = ("loop/holdout-registry/", "loop/factory-learning-history/")
    require(all(p.startswith(allowed) for p in changed),
            f"Only committed learning-history records may follow intervention freeze: {changed}")


def _factory_snapshot(repo: Path) -> dict[str, str]:
    from .runs import active_files
    files = {}
    for rel in active_files(repo):
        path = confined(repo, rel)
        require(path.is_file(), f"Active factory file missing: {rel}")
        files[rel] = file_hash(path)
    return files


def _eligible_change_surface(repo: Path) -> list[str]:
    from .runs import active_files
    active = set(active_files(repo))
    require(SELF_OPTIMIZABLE_PRODUCTION_PATHS <= active,
            f"Configured self-optimizable production files are missing: {sorted(SELF_OPTIMIZABLE_PRODUCTION_PATHS-active)}")
    return sorted(SELF_OPTIMIZABLE_PRODUCTION_PATHS)


def evidence(repo: Path, cycle_id: str) -> tuple[Path, dict]:
    root = _cycle(repo, cycle_id)
    return root, unseal(root / "evidence.json")


def _validate_frozen_evidence(repo: Path, doc: dict) -> None:
    from .runs import Run
    require(doc.get("schema_version") == 2, "Factory-learning evidence schema must be v2")
    for item in doc["runs"]:
        run = Run(repo, item["run_id"])
        complete = run.complete()
        require(run.brief["subject"] == item["subject"]
                and run.manifest["fixture"] == item["fixture"]
                and digest(run.manifest) == item["manifest_sha256"]
                and complete["book_sha256"] == item["book_sha256"]
                and file_hash(run.accepted_audit_file()) == item["audit_sha256"],
                f"Frozen training evidence changed: {item['run_id']}")
    for item in doc["artifacts"]:
        path = confined(repo, item["path"])
        require(path.is_file() and file_hash(path) == item["sha256"],
                f"Frozen training evidence artifact changed: {item['path']}")


def freeze_evidence(repo: Path, cycle_id: str, run_ids: list[str], artifact_paths: list[str] | None = None) -> dict:
    from .runs import Run
    repo = repo.resolve(); identifier(cycle_id)
    root = _cycle(repo, cycle_id)
    require(not (root / "registration.json").exists(), "Training evidence must be frozen before learner/reviewer registration")
    if (root / "evidence.json").exists():
        existing = unseal(root / "evidence.json")
        require(set(run_ids) == {x["run_id"] for x in existing["runs"]},
                "Factory-learning evidence is already frozen with different run IDs")
        require(set(artifact_paths or []) == {x["path"] for x in existing["artifacts"]},
                "Factory-learning evidence is already frozen with different artifact paths")
        require(existing["base_commit"] == _git(repo, "rev-parse", "HEAD")
                and existing["experimental_branch"] == _git(repo, "branch", "--show-current"),
                "Frozen training evidence belongs to another branch/source state")
        _validate_frozen_evidence(repo, existing)
        require(_factory_snapshot(repo) == existing["base_factory_files"],
                "Active factory changed after training evidence was frozen")
        require(_eligible_change_surface(repo) == existing["eligible_change_surface"],
                "Eligible factory-learning change surface changed after evidence freeze")
        return existing
    require(not _git(repo, "status", "--porcelain"), "Freeze training evidence from a clean source tree")
    branch_name = _git(repo, "branch", "--show-current")
    require(bool(branch_name) and branch_name != "main",
            "Factory-learning evidence must be frozen on an isolated experimental branch")
    require(isinstance(run_ids, list) and len(set(run_ids)) == len(run_ids) and len(run_ids) >= 2,
            "Training evidence needs at least two distinct completed run IDs")
    runs = []
    subjects = set()
    for rid in run_ids:
        run = Run(repo, identifier(rid))
        complete = run.complete()
        subjects.add(run.brief["subject"])
        runs.append({"run_id": rid, "subject": run.brief["subject"], "fixture": run.manifest["fixture"],
                     "manifest_sha256": digest(run.manifest), "book_sha256": complete["book_sha256"],
                     "audit_sha256": file_hash(run.accepted_audit_file())})
    require(len(subjects) >= 2, "Transferable factory learning needs evidence from at least two distinct training subjects")
    artifacts = []
    for rel in artifact_paths or []:
        path = confined(repo, rel)
        require(path.is_file(), f"Training evidence artifact missing: {rel}")
        artifacts.append({"path": rel, "sha256": file_hash(path)})
    base_factory_files = _factory_snapshot(repo)
    doc = {"schema_version": 2, "cycle_id": cycle_id, "frozen_at": now(),
           "base_commit": _git(repo, "rev-parse", "HEAD"), "experimental_branch": branch_name,
           "training_subjects": sorted(subjects), "runs": runs, "artifacts": artifacts,
           "eligible_change_surface": _eligible_change_surface(repo),
           "base_factory_files": base_factory_files, "base_factory_digest": digest(base_factory_files)}
    with lock(root):
        seal(root / "evidence.json", doc)
    return doc


def registration(repo: Path, cycle_id: str) -> tuple[Path, dict]:
    root = _cycle(repo, cycle_id)
    record = unseal(root / "registration.json")
    return root, record


def register(repo: Path, cycle_id: str, learner: dict, learner_meta: dict, reviewer: dict, reviewer_meta: dict) -> Path:
    repo = repo.resolve(); identifier(cycle_id)
    validate_learner(learner); validate_reviewer(reviewer)
    root, frozen_evidence = evidence(repo, cycle_id)
    _validate_frozen_evidence(repo, frozen_evidence)
    require(frozen_evidence["base_commit"] == _git(repo, "rev-parse", "HEAD")
            and frozen_evidence["experimental_branch"] == _git(repo, "branch", "--show-current"),
            "Factory-learning evidence belongs to another source state")
    require(learner["evidence_sha256"] == digest(frozen_evidence),
            "Factory learner output is not bound to the frozen training evidence")
    require(reviewer["evidence_sha256"] == digest(frozen_evidence)
            and reviewer["learner_sha256"] == digest(learner),
            "Factory-learning review is not bound to the frozen evidence and learner proposal")
    require(set(learner["falsification_test"]["training_subjects"]) == set(frozen_evidence["training_subjects"]),
            "Learner training subjects differ from the frozen evidence manifest")
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
    eligible = set(frozen_evidence["eligible_change_surface"])
    require(approved <= eligible,
            f"Factory intervention paths are outside the frozen eligible production surface: {sorted(approved-eligible)}")
    test = learner["falsification_test"]; reviewed = reviewer["held_out_test"]
    for key in ("holdout_requirements", "acceptance_policy", "success_criteria", "failure_signals"):
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
    require(base_factory_files == frozen_evidence["base_factory_files"]
            and digest(base_factory_files) == frozen_evidence["base_factory_digest"],
            "Factory changed after training evidence was frozen")
    record = {"schema_version": 2, "cycle_id": cycle_id, "registered_at": now(), "base_commit": base_commit,
              "experimental_branch": branch_name,
              "evidence_sha256": digest(frozen_evidence),
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
        require(_git(repo, "branch", "--show-current") == reg["experimental_branch"],
                "Existing frozen intervention belongs to another branch")
        _require_only_holdout_history_after_freeze(repo, existing)
        require(_factory_snapshot(repo) == existing["factory_files"],
                "Active factory no longer matches the frozen intervention")
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
    require(digest(factory_files) != reg["base_factory_digest"],
            "Committed intervention did not change the active factory snapshot")
    doc = {"schema_version": 2, "cycle_id": cycle_id, "base_commit": reg["base_commit"],
           "head_commit": head, "changed_paths": sorted(changed), "path_hashes": hashes,
           "factory_files": factory_files, "factory_digest": digest(factory_files), "frozen_at": now()}
    with lock(root):
        seal(root / "change.json", doc)
    return doc


def submit_holdout(repo: Path, cycle_id: str, selection: dict, metadata: dict) -> dict:
    root, reg = registration(repo, cycle_id)
    change = unseal(root / "change.json")
    training = set(reg["learner"]["falsification_test"]["training_subjects"])
    if (root / "holdout.json").exists():
        existing = unseal(root / "holdout.json")
        require(existing["selection"] == selection and existing["selector_metadata"] == metadata
                and existing["change_sha256"] == digest(change),
                "Held-out selection is already frozen with different inputs")
        require(_git(repo, "branch", "--show-current") == reg["experimental_branch"],
                "Frozen held-out selection belongs to another branch")
        _require_only_holdout_history_after_freeze(repo, change)
        require(_factory_snapshot(repo) == change["factory_files"],
                "Active factory changed after held-out selection was frozen")
        retirement_path = _holdout_record_path(repo, cycle_id)
        if retirement_path.exists():
            retirement = unseal(retirement_path)
        else:
            # Crash-safe replay: holdout.json is authoritative once sealed; recreate only its missing ledger mirror.
            retirement = {"schema_version": 2, "cycle_id": cycle_id, "subjects": list(selection["subjects"]),
                          "training_subjects": sorted(training),
                          "selection_sha256": digest(selection), "change_sha256": digest(change),
                          "selector_family": metadata["family"], "selected_at": existing["selected_at"]}
            seal(retirement_path, retirement)
        require(set(retirement["subjects"]) == set(selection["subjects"])
                and set(retirement.get("training_subjects", [])) == training
                and retirement["selection_sha256"] == digest(selection)
                and retirement["change_sha256"] == digest(change),
                "Tracked holdout-retirement record differs from frozen selection")
        return {**existing, "retirement_record": retirement_path.relative_to(repo).as_posix(),
                "retirement_sha256": digest(retirement), "requires_commit": bool(_git(repo, "status", "--porcelain"))}
    require(_git(repo, "branch", "--show-current") == reg["experimental_branch"],
            "Held-out selection must occur on the frozen experimental branch")
    require(not _git(repo, "status", "--porcelain"), "Held-out selection requires the frozen intervention tree to be clean")
    require(change["head_commit"] == _git(repo, "rev-parse", "HEAD"), "Factory changed after intervention freeze")
    exact_keys(selection, {"schema_version", "subjects", "rationale"}, label="held-out selection")
    require(selection["schema_version"] == 2, "Held-out selection schema must be v2")
    subjects = _strings(selection["subjects"], "held-out subjects", 2)
    require(len(subjects) == len(set(subjects)), "Duplicate held-out subject")
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
    registry_root = repo / "loop/holdout-registry"
    if registry_root.is_dir():
        for path in registry_root.glob("*.json"):
            prior = unseal(path)
            previously_revealed.update(prior["subjects"])
            previously_revealed.update(prior.get("training_subjects", []))
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
    retirement = {"schema_version": 2, "cycle_id": cycle_id, "subjects": list(subjects),
                  "training_subjects": sorted(training),
                  "selection_sha256": digest(selection), "change_sha256": digest(change),
                  "selector_family": metadata["family"], "selected_at": doc["selected_at"]}
    with lock(root):
        seal(root / "holdout.json", doc)
        seal(_holdout_record_path(repo, cycle_id), retirement)
    return {**doc, "retirement_record": _holdout_record_path(repo, cycle_id).relative_to(repo).as_posix(),
            "retirement_sha256": digest(retirement), "requires_commit": True}


def prepare_arm(repo: Path, cycle_id: str, arm: str, run_id: str, brief: dict, research: dict,
                parent: str | None = None, fixture: bool = False, research_preflight: dict | None = None) -> dict:
    """Prepare one held-out generation arm from exactly the cycle's frozen parent/candidate factory."""
    from .runs import Run, prepare
    require(arm in ("parent", "candidate"), "Factory-learning arm must be parent or candidate")
    root, reg = registration(repo, cycle_id)
    require(_git(repo, "branch", "--show-current") == reg["experimental_branch"],
            "Factory-learning arm preparation belongs on the experimental branch")
    require(not _git(repo, "status", "--porcelain"),
            "Commit the holdout-retirement record before preparing transfer arms")
    change = unseal(root / "change.json")
    holdout = unseal(root / "holdout.json")
    _require_only_holdout_history_after_freeze(repo, change)
    require(_factory_snapshot(repo) == change["factory_files"],
            "Active factory changed after intervention freeze")
    retirement = unseal(_holdout_record_path(repo, cycle_id))
    require(set(retirement["subjects"]) == set(holdout["selection"]["subjects"]),
            "Tracked holdout retirement differs from frozen selection")
    subject = brief.get("subject")
    require(subject in set(holdout["selection"]["subjects"]),
            "Transfer arm subject is not in the frozen held-out set")
    require(research.get("subject") == subject, "Transfer arm research/brief subject mismatch")
    factory_ref = reg["base_commit"] if arm == "parent" else change["head_commit"]
    expected_files = reg["base_factory_files"] if arm == "parent" else change["factory_files"]
    expected_digest = reg["base_factory_digest"] if arm == "parent" else change["factory_digest"]
    run_root = prepare(repo, run_id, brief, research, parent, fixture, research_preflight,
                       factory_ref=factory_ref)
    run = Run(repo, run_id)
    require(run.manifest["factory_files"] == expected_files
            and run.manifest["factory_digest"] == expected_digest,
            f"Prepared {arm} arm does not match its frozen factory snapshot")
    require(run.manifest["origin_commit"] == factory_ref,
            f"Prepared {arm} arm origin commit is not the cycle's frozen factory commit")
    return {"status": "ARM_FROZEN", "cycle_id": cycle_id, "arm": arm, "run_id": run_id,
            "subject": subject, "factory_ref": factory_ref, "factory_digest": expected_digest,
            "run": str(run_root)}


def bind_experiment(repo: Path, cycle_id: str, experiment_id: str) -> dict:
    from . import experiments
    from .runs import Run
    root, reg = registration(repo, cycle_id)
    if (root / "experiment.json").exists():
        existing = unseal(root / "experiment.json")
        require(existing["experiment_id"] == experiment_id,
                "Factory-learning cycle already binds a different transfer experiment")
        require(_git(repo, "branch", "--show-current") == reg["experimental_branch"],
                "Stored transfer binding belongs to another branch")
        require(not _git(repo, "status", "--porcelain"),
                "Stored transfer binding requires a clean frozen intervention tree")
        change = unseal(root / "change.json")
        _require_only_holdout_history_after_freeze(repo, change)
        require(_factory_snapshot(repo) == change["factory_files"],
                "Active factory changed after transfer binding")
        retirement = unseal(_holdout_record_path(repo, cycle_id))
        require(existing["holdout_retirement_sha256"] == digest(retirement),
                "Stored transfer binding's holdout-retirement record changed")
        _, current_exp = experiments.registration(repo, experiment_id)
        require(existing["registration_sha256"] == digest(current_exp),
                "Stored transfer binding's experiment registration changed")
        return existing
    require(_git(repo, "branch", "--show-current") == reg["experimental_branch"],
            "Transfer binding must occur on the frozen experimental branch")
    require(not _git(repo, "status", "--porcelain"),
            "Commit the holdout-retirement record before binding the transfer experiment")
    change = unseal(root / "change.json"); holdout = unseal(root / "holdout.json")
    _require_only_holdout_history_after_freeze(repo, change)
    require(_factory_snapshot(repo) == change["factory_files"],
            "Active factory changed after intervention freeze")
    retirement_path = _holdout_record_path(repo, cycle_id)
    retirement = unseal(retirement_path)
    require(set(retirement["subjects"]) == set(holdout["selection"]["subjects"])
            and set(retirement.get("training_subjects", [])) == set(reg["learner"]["falsification_test"]["training_subjects"])
            and retirement["selection_sha256"] == digest(holdout["selection"]),
            "Committed holdout-retirement record is not bound to this selection")
    exp_root, exp = experiments.registration(repo, experiment_id)
    require(set(exp["spec"]["subjects"]) == set(holdout["selection"]["subjects"]),
            "Transfer experiment subjects must equal the independently selected held-out set")
    require(exp["spec"]["primary_dimension"] == reg["learner"]["proposed_factory_change"]["primary_dimension"],
            "Transfer experiment changed the predeclared primary quality dimension")
    require(exp["spec"]["confirmatory"] is True,
            "Factory-learning transfer must be preregistered confirmatory")
    require(exp["spec"].get("freeze_research", True) is True,
            "Factory-learning safe surface does not alter research generation; research must be byte-frozen between arms")
    changed_paths = set(change["changed_paths"])
    expected_freeze_plan = not bool(changed_paths.intersection(PLAN_AFFECTING_PATHS))
    require(exp["spec"]["freeze_plan"] is expected_freeze_plan,
            "Transfer experiment freeze_plan does not match whether the frozen intervention can affect planning")
    require(experiments.wilson_lower(exp["spec"]["samples_per_subject"], exp["spec"]["samples_per_subject"]) > 0.5,
            "Transfer sample allocation cannot possibly satisfy strict_transfer_v1 even with all candidate wins")
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
    retirement_rel = retirement_path.relative_to(repo).as_posix()
    retirement_commit = _git(repo, "log", "-1", "--format=%H", "--", retirement_rel)
    require(bool(retirement_commit), "Holdout-retirement record must be committed before transfer binding")
    doc = {"schema_version": 2, "cycle_id": cycle_id, "experiment_id": experiment_id,
           "registration_sha256": digest(exp), "holdout_sha256": digest(holdout),
           "holdout_retirement_sha256": digest(retirement), "holdout_retirement_commit": retirement_commit,
           "change_sha256": digest(change), "bound_at": now()}
    with lock(root):
        seal(root / "experiment.json", doc)
    return doc


def _terminal_history(reg: dict, change: dict, holdout: dict, binding: dict, decision: dict) -> dict:
    return {
        "schema_version": 2,
        "cycle_id": reg["cycle_id"],
        "decision": decision["decision"],
        "evidence_sha256": reg["evidence_sha256"],
        "learner_sha256": digest(reg["learner"]),
        "review_sha256": digest(reg["review"]),
        "base_commit": reg["base_commit"],
        "intervention_commit": change["head_commit"],
        "approved_change_surface": list(reg["approved_change_surface"]),
        "training_subjects": list(reg["learner"]["falsification_test"]["training_subjects"]),
        "holdout_subjects": list(holdout["selection"]["subjects"]),
        "holdout_retirement_sha256": binding["holdout_retirement_sha256"],
        "holdout_retirement_commit": binding["holdout_retirement_commit"],
        "experiment_id": binding["experiment_id"],
        "experiment_registration_sha256": binding["registration_sha256"],
        "binding_sha256": digest(binding),
        "experiment_decision": decision["experiment_decision"],
        "decided_at": decision["decided_at"],
    }


def decide(repo: Path, cycle_id: str) -> dict:
    from . import experiments
    root, reg = registration(repo, cycle_id)
    if (root / "decision.json").exists():
        existing = unseal(root / "decision.json")
        require(_git(repo, "branch", "--show-current") == reg["experimental_branch"],
                "Stored factory-learning decision belongs to another branch")
        require(not _git(repo, "status", "--porcelain"),
                "Stored factory-learning decision requires a clean frozen intervention tree")
        change = unseal(root / "change.json")
        _require_only_holdout_history_after_freeze(repo, change)
        require(_factory_snapshot(repo) == change["factory_files"],
                "Active factory changed after the factory-learning decision")
        binding = unseal(root / "experiment.json")
        require(existing["binding_sha256"] == digest(binding),
                "Stored factory-learning decision is bound to another experiment state")
        retirement = unseal(_holdout_record_path(repo, cycle_id))
        require(binding["holdout_retirement_sha256"] == digest(retirement),
                "Stored factory-learning decision's holdout-retirement record changed")
        _, current_exp = experiments.registration(repo, binding["experiment_id"])
        require(digest(current_exp) == binding["registration_sha256"],
                "Stored factory-learning decision's experiment registration changed")
        holdout = unseal(root / "holdout.json")
        history_path = _history_record_path(repo, cycle_id)
        expected_history = _terminal_history(reg, change, holdout, binding, existing)
        if history_path.exists():
            history = unseal(history_path)
            require(history == expected_history, "Tracked factory-learning history differs from terminal decision")
        else:
            history = expected_history
            seal(history_path, history)
        return {**existing, "history_record": history_path.relative_to(repo).as_posix(),
                "history_sha256": digest(history), "requires_commit": bool(_git(repo, "status", "--porcelain"))}
    require(_git(repo, "branch", "--show-current") == reg["experimental_branch"],
            "Factory-learning decision must occur on its frozen experimental branch")
    require(not _git(repo, "status", "--porcelain"), "Factory-learning decision requires a clean frozen intervention tree")
    change = unseal(root / "change.json")
    _require_only_holdout_history_after_freeze(repo, change)
    require(_factory_snapshot(repo) == change["factory_files"],
            "Active factory changed after the intervention was frozen")
    binding = unseal(root / "experiment.json")
    result = experiments.transfer_decide(repo, binding["experiment_id"])
    if result["decision"] == "TRANSFER_ELIGIBLE_NONPROMOTIONAL":
        require(len(result["judge_models"]) == 1, "Transfer retention requires one stable judge model/family")
        holdout = unseal(root / "holdout.json")
        config = read_json(repo / "factory/config.json"); validate_config(config)
        judge_family = result["judge_models"][0]["family"]
        forbidden = {reg["learner_metadata"]["family"], config["profiles"]["factory"]["family"]}
        if judge_family in forbidden:
            result["decision"] = "REJECT_TRANSFER"
            result["reasons"].append("Transfer judge family is not independent of the generator/learner family")
    verdict = ("KEEP_FACTORY_CHANGE" if result["decision"] == "TRANSFER_ELIGIBLE_NONPROMOTIONAL"
               else "REJECT_FACTORY_CHANGE" if result["decision"] == "REJECT_TRANSFER"
               else "INCONCLUSIVE")
    doc = {"schema_version": 2, "cycle_id": cycle_id, "decision": verdict,
           "experiment_decision": result, "binding_sha256": digest(binding),
           "holdout_retirement_commit": binding["holdout_retirement_commit"], "decided_at": now()}
    # Missing judgments are an unfinished panel, not an immutable experimental conclusion.
    # Once the preregistered panel is complete, KEEP/REJECT or a measured INCONCLUSIVE is terminal.
    if result.get("missing"):
        doc["terminal"] = False
        return doc
    doc["terminal"] = True
    holdout = unseal(root / "holdout.json")
    history_path = _history_record_path(repo, cycle_id)
    history = _terminal_history(reg, change, holdout, binding, doc)
    with lock(root):
        seal(root / "decision.json", doc)
        seal(history_path, history)
    return {**doc, "history_record": history_path.relative_to(repo).as_posix(),
            "history_sha256": digest(history), "requires_commit": True}
