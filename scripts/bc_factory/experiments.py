"""Preregistered, blinded, order-reversed comparisons and atomic champion promotion."""
from __future__ import annotations
import math
import shutil
import tempfile
from pathlib import Path
from .common import (FactoryError, atomic_bytes, atomic_json, canonical, confined, digest, exact_keys,
                     file_hash, identifier, lock, nonempty, now, read_json, require, seal, unseal)
from .runs import Run
from .schema import DIMENSIONS, FINDINGS, validate_metadata

CALIBRATION_CATEGORIES = {
    "invented_authority", "unsupported_guarantee", "missing_objection", "misordered_dependency",
    "empty_scene", "excessive_repetition", "necessary_qualification", "strong_original",
    "order_reversal", "repeatability", "subject_transfer", "honest_counterevidence",
}


def instrument(repo: Path) -> dict:
    contract = (repo / "loop/judges/pairwise.md").read_text(encoding="utf-8")
    return {"schema_version": 2, "contract": contract, "dimensions": list(DIMENSIONS),
            "primary_scale": "candidate-win versus parent/tie; order reversals are not independent samples",
            "evaluation_code": {name: file_hash(repo / name) for name in ("scripts/bc_factory/experiments.py", "scripts/bc_factory/schema.py")},
            "confidence": 0.95, "guardrail": "any observed secondary-dimension loss blocks promotion"}


def register(repo: Path, spec: dict) -> Path:
    exact_keys(spec, {"schema_version", "id", "parent_release", "hypothesis", "primary_dimension", "allowed_change_paths",
                      "subjects", "samples_per_subject", "pairs", "freeze_plan", "confirmatory"}, label="experiment specification")
    require(spec["schema_version"] == 2, "Experiment schema must be v2")
    identifier(spec["id"])
    require(spec["parent_release"] is None or isinstance(spec["parent_release"], str), "Invalid parent release")
    require(spec["primary_dimension"] in DIMENSIONS, "Unknown primary dimension")
    nonempty(spec["hypothesis"], "Hypothesis")
    require(type(spec["samples_per_subject"]) is int and spec["samples_per_subject"] >= 3, "At least three independent generation pairs per subject for screening")
    require(type(spec["freeze_plan"]) is bool and type(spec["confirmatory"]) is bool, "Invalid design switches")
    require(isinstance(spec["subjects"], list) and len(set(spec["subjects"])) == len(spec["subjects"]) >= 2, "At least two distinct subjects required")
    require(isinstance(spec["allowed_change_paths"], list) and bool(spec["allowed_change_paths"]), "Preregister the intervention files")
    require(isinstance(spec["pairs"], list), "Pairs must be a list")
    runs = {}
    arm_hashes: dict[str, set] = {"parent_run": set(), "candidate_run": set()}
    seen_runs: set[str] = set()
    counts = {subject: 0 for subject in spec["subjects"]}
    seen_ids: set[str] = set()
    for pair in spec["pairs"]:
        exact_keys(pair, {"id", "subject", "parent_run", "candidate_run"}, label="generation pair")
        identifier(pair["id"])
        require(pair["id"] not in seen_ids, "Duplicate generation pair")
        seen_ids.add(pair["id"])
        require(pair["subject"] in counts, "Undeclared subject")
        counts[pair["subject"]] += 1
        sides = []
        for arm in ("parent_run", "candidate_run"):
            rid = pair[arm]
            require(rid not in seen_runs, "A generated book cannot count as multiple independent samples")
            seen_runs.add(rid)
            run = Run(repo, rid)
            require(run.manifest["subject"] == pair["subject"], "Pair subject mismatch")
            require(run.manifest["parent"] == spec["parent_release"], "Run has wrong declared parent release")
            if spec["confirmatory"]:
                require(not (run.root / "results").exists() or not list((run.root / "results").glob("writer-*.json")), "Confirmatory specification must be registered before generation")
            runs[rid] = digest(run.manifest)
            arm_hashes[arm].add(run.manifest["factory_digest"])
            sides.append(run)
        parent, candidate = sides
        for k in ("brief_sha256", "research_sha256"):
            require(parent.manifest[k] == candidate.manifest[k], f"Confounded pair: {k} differs")
        a, b = parent.manifest["factory_files"], candidate.manifest["factory_files"]
        changes = {p for p in set(a) | set(b) if a.get(p) != b.get(p)}
        require(changes <= set(spec["allowed_change_paths"]), f"Undeclared intervention files: {sorted(changes-set(spec['allowed_change_paths']))}")
    require(all(n == spec["samples_per_subject"] for n in counts.values()), "Incomplete/mismatched preregistered sample allocation")
    require(all(len(h) == 1 for h in arm_hashes.values()), "Each arm must be one factory across subjects/replicates")
    dest = confined(repo, f"experiments/{spec['id']}")
    require(not (dest / "registration.json").exists(), "Experiment already registered; do not edit after seeing results")
    doc = {"schema_version": 2, "registered_at": now(), "spec": spec, "run_manifests": runs,
           "instrument": instrument(repo), "instrument_hash": digest(instrument(repo))}
    with lock(dest):
        seal(dest / "registration.json", doc)
    return dest


def registration(repo: Path, experiment_id: str) -> tuple[Path, dict]:
    root = confined(repo, f"experiments/{identifier(experiment_id)}")
    reg = unseal(root / "registration.json")
    require(reg["instrument_hash"] == digest(reg["instrument"]), "Instrument changed")
    require(digest(instrument(repo)) == reg["instrument_hash"], "Evaluator contract/code changed after registration; a new experiment and calibration are required")
    for rid, expected in reg["run_manifests"].items():
        require(digest(Run(repo, rid).manifest) == expected, "Experiment run changed")
    return root, reg


def pair_task(repo: Path, eid: str, pair_id: str, order: str) -> dict:
    root, reg = registration(repo, eid)
    require(order in ("AB", "BA"), "Order is AB or BA")
    pairs = [p for p in reg["spec"]["pairs"] if p["id"] == pair_id]
    require(len(pairs) == 1, "Unknown pair")
    pair = pairs[0]
    parent, candidate = Run(repo, pair["parent_run"]), Run(repo, pair["candidate_run"])
    parent.complete()
    candidate.complete()
    if reg["spec"]["freeze_plan"]:
        require(digest(parent.accepted_plan()[1]) == digest(candidate.accepted_plan()[1]), "Plan changed in a fixed-plan experiment")
    # Model/route changes are only intentional when config was declared part of the intervention.
    if "factory/config.json" not in reg["spec"]["allowed_change_paths"]:
        def generators(run: Run) -> set:
            return {(x["metadata"]["model"], x["metadata"]["family"], x["metadata"]["route"])
                    for p in (run.root / "results").glob("*.json") for x in [unseal(p)]
                    if x["role"] in ("planner", "writer", "book-editor")}
        require(generators(parent) == generators(candidate), "Undeclared generation model/route confound")
    pa, ca = parent.assemble(), candidate.assemble()
    a, b = (pa["text"], ca["text"]) if order == "AB" else (ca["text"], pa["text"])
    # Crucially no run names, ages, scores, author identities or label mapping in model inputs.
    task = {"schema_version": 2, "role": "pair-judge", "contract": reg["instrument"]["contract"], "style": "",
            "inputs": {"A": a, "B": b, "reader_goal": parent.brief["reader_goal"],
                       "audience": parent.brief["audience"], "primary_dimension": reg["spec"]["primary_dimension"]}}
    record = {"task": task, "pair_id": pair_id, "order": order, "instrument_hash": reg["instrument_hash"],
              "parent_book_sha256": pa["text_sha256"], "candidate_book_sha256": ca["text_sha256"],
              "parent_audit_sha256": file_hash(parent.root / "results/final-auditor-r01.json"),
              "candidate_audit_sha256": file_hash(candidate.root / "results/final-auditor-r01.json")}
    with lock(root):
        seal(root / "tasks" / f"{identifier(pair_id)}-{order}.json", record)
    return task


def submit_pair(repo: Path, eid: str, pair_id: str, order: str, output: dict, metadata: dict) -> dict:
    root, reg = registration(repo, eid)
    task = pair_task(repo, eid, pair_id, order)
    record = unseal(root / "tasks" / f"{pair_id}-{order}.json")
    exact_keys(output, {"schema_version", "preferences", "critical"}, label="pair judgment")
    require(output["schema_version"] == 2, "Invalid judgment schema")
    exact_keys(output["preferences"], set(DIMENSIONS))
    for preference in output["preferences"].values():
        exact_keys(preference, {"winner", "a_quote", "b_quote", "reason"})
        require(preference["winner"] in ("A", "B", "tie"), "Invalid preference")
        nonempty(preference["reason"], "Preference explanation")
        for label, key in (("A", "a_quote"), ("B", "b_quote")):
            nonempty(preference[key], "Preference evidence")
            require(preference[key] in task["inputs"][label], "Judgment quote not present in labeled book")
    exact_keys(output["critical"], {"A", "B"})
    for label, findings in output["critical"].items():
        require(isinstance(findings, list), "Critical findings must be a list")
        for f in findings:
            exact_keys(f, {"kind", "quote", "explanation"})
            require(f["kind"] in FINDINGS, "Unknown critical finding")
            require(bool(f["quote"]) and f["quote"] in task["inputs"][label], "Invalid critical quote")
            nonempty(f["explanation"], "Critical explanation")
    validate_metadata(metadata)
    pair = next(p for p in reg["spec"]["pairs"] if p["id"] == pair_id)
    both = [Run(repo, pair[k]) for k in ("parent_run", "candidate_run")]
    require(all(metadata["family"] not in r.generating_families() for r in both), "Judge is not independent of the generators")
    if any(not r.manifest["fixture"] for r in both):
        require(metadata["harness"] != "fixture", "Fixture judging cannot validate a live experiment")
    result = {"schema_version": 2, "task_hash": digest(record), "output": output, "metadata": metadata, "created_at": now()}
    with lock(root):
        seal(root / "judgments" / f"{pair_id}-{order}.json", result)
    return result


def wilson_lower(wins: int, n: int) -> float:
    require(n > 0 and 0 <= wins <= n, "Invalid sample count")
    # Two-sided 95% Wilson interval lower endpoint; ties count against a win.
    z = 1.959963984540054
    p = wins / n
    return (p + z*z/(2*n) - z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))) / (1+z*z/n)


def validate_calibration(data: dict, instrument_hash: str, model: str, family: str) -> dict:
    exact_keys(data, {"schema_version", "instrument_hash", "model", "family", "human_raters", "cases", "provenance_note"})
    require(data["schema_version"] == 2 and data["instrument_hash"] == instrument_hash, "Calibration belongs to another instrument")
    require(data["model"] == model and data["family"] == family, "Calibration model differs from actual judge")
    require(isinstance(data["human_raters"], list) and len(set(data["human_raters"])) >= 2, "Need supplied ratings from at least two identified human raters")
    nonempty(data["provenance_note"], "Calibration provenance")
    require(isinstance(data["cases"], list) and len(data["cases"]) >= 12, "Calibration needs at least 12 supplied cases")
    categories, case_ids, matches = set(), set(), 0
    for c in data["cases"]:
        exact_keys(c, {"id", "category", "human_consensus", "judge_preference", "critical_failure_detected", "evidence_sha256"})
        identifier(c["id"])
        require(c["id"] not in case_ids, "Duplicate calibration case")
        case_ids.add(c["id"])
        categories.add(c["category"])
        require(c["human_consensus"] in ("A", "B", "tie") and c["judge_preference"] in ("A", "B", "tie"), "Invalid calibration preference")
        require(type(c["critical_failure_detected"]) is bool, "Critical control requires explicit result")
        require(isinstance(c["evidence_sha256"], str) and len(c["evidence_sha256"]) == 64 and all(x in "0123456789abcdef" for x in c["evidence_sha256"]), "Calibration must cite a retained case artifact hash")
        matches += c["human_consensus"] == c["judge_preference"]
        if c["category"] in ("invented_authority", "unsupported_guarantee"):
            require(c["critical_failure_detected"], "Critical calibration false negative")
        if c["category"] in ("order_reversal", "repeatability"):
            require(c["human_consensus"] == c["judge_preference"], "Order/repeatability calibration failed")
    require(CALIBRATION_CATEGORIES <= categories, "Calibration omitted required positive/negative controls")
    require(matches / len(data["cases"]) >= 0.8, "Insufficient agreement with supplied human ratings")
    return {"status": "VALIDATED_AGAINST_SUPPLIED_RATINGS", "agreement": matches/len(data["cases"]), "cases": len(data["cases"])}


def decide(repo: Path, eid: str, calibration: dict | None = None) -> dict:
    root, reg = registration(repo, eid)
    spec = reg["spec"]
    reasons, critical, unstable = [], [], []
    scores = {s: {d: [] for d in DIMENSIONS} for s in spec["subjects"]}
    judge_models = set()
    incomplete = []
    for pair in spec["pairs"]:
        observations = []
        for order in ("AB", "BA"):
            path = root / "judgments" / f"{pair['id']}-{order}.json"
            if not path.exists():
                incomplete.append(f"{pair['id']}-{order}")
                continue
            pair_task(repo, eid, pair["id"], order)  # Revalidates books/audits and exact frozen design.
            task_record = unseal(root / "tasks" / f"{pair['id']}-{order}.json")
            result = unseal(path)
            require(result["task_hash"] == digest(task_record), "Judgment has stale task inputs")
            judge_models.add((result["metadata"]["model"], result["metadata"]["family"]))
            candidate_label = "B" if order == "AB" else "A"
            if result["output"]["critical"][candidate_label]:
                critical.append(f"{pair['id']}-{order}")
            observations.append({d: (0 if p["winner"] == "tie" else 1 if p["winner"] == candidate_label else -1)
                                 for d, p in result["output"]["preferences"].items()})
        if len(observations) == 2:
            if observations[0] != observations[1]:
                unstable.append(pair["id"])
            for d in DIMENSIONS:
                # Reversed labels are repeated measurement, never an extra generation replicate.
                scores[pair["subject"]][d].append(observations[0][d] if observations[0][d] == observations[1][d] else 0)
    if incomplete:
        return {"decision": "INCONCLUSIVE", "missing": incomplete, "reason": "No complete panel; no promotion"}
    if critical:
        reasons.append("Critical failure in at least one candidate book")
    if unstable:
        reasons.append("Order-sensitive judgment; recalibration/repeated measurement required")
    if len(judge_models) != 1:
        reasons.append("Mixed judge model/family invalidates the instrument")
    cal = None
    if calibration is None:
        reasons.append("Real human calibration not supplied")
    elif len(judge_models) == 1:
        model, family = next(iter(judge_models))
        try:
            cal = validate_calibration(calibration, reg["instrument_hash"], model, family)
        except FactoryError as exc:
            reasons.append(str(exc))
    subjects = {}
    regressions = []
    for subject, dims in scores.items():
        primary = dims[spec["primary_dimension"]]
        lower = wilson_lower(primary.count(1), len(primary))
        subjects[subject] = {"n_generation_pairs": len(primary), "primary_wins": primary.count(1),
                             "primary_losses": primary.count(-1), "primary_ties": primary.count(0),
                             "win_rate_lower_95": lower, "dimension_outcomes": dims}
        if lower <= 0.5:
            reasons.append(f"{subject}: insufficient evidence of primary improvement beyond sampling variation")
        for dimension, values in dims.items():
            if dimension != spec["primary_dimension"] and -1 in values:
                regressions.append(f"{subject}/{dimension}")
    if regressions:
        reasons.append("Observed secondary-dimension regression in at least one subject")
    if not spec["confirmatory"]:
        reasons.append("Exploratory experiment cannot directly promote; preregister a confirmatory replication")
    fixture = any(Run(repo, rid).manifest["fixture"] for rid in reg["run_manifests"])
    if fixture:
        reasons.append("Fixture experiment is software testing, never production evidence")
    verdict = "REJECT" if critical or regressions else "INCONCLUSIVE" if reasons else "KEEP_ELIGIBLE"
    return {"decision": verdict, "reasons": reasons, "subjects": subjects, "critical": critical,
            "order_instability": unstable, "calibration": cal, "registration_hash": digest(reg),
            "fixture": fixture, "efficacy": "NOT_MEASURED"}


def promote(repo: Path, eid: str, release_id: str, calibration: dict, approval: dict) -> Path:
    repo = repo.resolve()
    identifier(release_id)
    root, reg = registration(repo, eid)
    decision = decide(repo, eid, calibration)
    require(decision["decision"] == "KEEP_ELIGIBLE", f"Promotion blocked: {decision}")
    exact_keys(approval, {"reviewer", "qualification", "book_hashes", "checks", "note"}, label="human release approval")
    nonempty(approval["reviewer"], "Human reviewer")
    nonempty(approval["note"], "Human review note")
    checks = {"final_book_read", "rights_reviewed", "truth_and_scope_reviewed", "no_unmeasured_efficacy_claims"}
    exact_keys(approval["checks"], checks)
    require(all(v is True for v in approval["checks"].values()), "Human release checks incomplete")
    selected = {}
    for pair in reg["spec"]["pairs"]:
        # Selection rule is deterministic and predeclared: first registered candidate per subject.
        selected.setdefault(pair["subject"], pair["candidate_run"])
    require(set(approval["book_hashes"]) == set(selected), "Approval must cover every selected subject")
    for subject, rid in selected.items():
        run = Run(repo, rid)
        require(run.complete()["book_sha256"] == approval["book_hashes"][subject], "Human approval refers to another book")
        require(not run.manifest["fixture"], "Cannot release fixtures")
        if run.brief["risk_level"] != "low":
            nonempty(approval["qualification"], "Qualified health/high-risk reviewer and review scope")
    release = confined(repo, f"releases/{release_id}")
    require(not release.exists(), "Release is immutable; choose a new ID")
    with lock(repo / "factory"):
        champion = read_json(repo / "factory/champion.json")
        require(champion["release"] == reg["spec"]["parent_release"], "Champion changed since registration; compare against the actual current parent")
        staging = Path(tempfile.mkdtemp(prefix=".release-", dir=repo))
        try:
            manifests = {}
            for subject, rid in selected.items():
                run = Run(repo, rid)
                dest = staging / "books" / subject
                dest.mkdir(parents=True)
                for name in ("book.md", "assembly.json", "manifest.json"):
                    shutil.copyfile(run.root / name, dest / name)
                shutil.copyfile(run.root / "results/final-auditor-r01.json", dest / "final-auditor.json")
                manifests[subject] = run.complete()
            first = Run(repo, next(iter(selected.values())))
            shutil.copytree(first.root / "snapshot", staging / "factory-snapshot")
            seal(staging / "release.json", {"schema_version": 2, "release_id": release_id, "experiment": eid,
                                           "registration": reg, "decision": decision, "calibration": calibration,
                                           "human_approval": approval, "books": manifests, "created_at": now()})
            release.parent.mkdir(parents=True, exist_ok=True)
            staging.rename(release)
            # One final atomic pointer update. Failed copying can never advance a champion.
            atomic_json(repo / "factory/champion.json", {"schema_version": 2, "release": release_id,
                        "release_sha256": file_hash(release / "release.json"), "status": "VALIDATED_FACTORY_CHAMPION", "efficacy": "NOT_MEASURED"})
        finally:
            if staging.exists():
                shutil.rmtree(staging)
    return release
