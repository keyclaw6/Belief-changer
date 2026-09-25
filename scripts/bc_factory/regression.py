"""Blinded AB/BA no-regression gate for cross-iteration optimization."""
from __future__ import annotations

from pathlib import Path

from .common import digest, exact_keys, file_hash, identifier, lock, nonempty, now, require, seal, unseal
from .learning import validate_packet_binding
from .schema import DIMENSIONS, FINDINGS, validate_metadata


def _instrument(run) -> dict:
    contract = run.snapshot("loop/judges/pairwise.md")
    return {"schema_version": 2, "contract": contract, "dimensions": list(DIMENSIONS),
            "policy": "cross-iteration-no-regression-v1"}


def _round(run) -> int:
    return run.accepted_assembly()["assembly"]["assembly_round"]


def task_path(run, round_no: int, order: str) -> Path:
    return run.root / "regression" / "tasks" / f"r{round_no:02d}-{order}.json"


def judgment_path(run, round_no: int, order: str) -> Path:
    return run.root / "regression" / "judgments" / f"r{round_no:02d}-{order}.json"


def decision_path(run, round_no: int) -> Path:
    return run.root / "regression" / f"decision-r{round_no:02d}.json"


def task(repo: Path, run_id: str, order: str) -> dict:
    from .runs import Run
    require(order in ("AB", "BA"), "Order is AB or BA")
    candidate = Run(repo, identifier(run_id))
    candidate.complete()
    require(candidate.learning is not None, "No-regression gate requires a frozen cross-iteration baseline")
    baseline = validate_packet_binding(repo, candidate.learning, candidate.brief["subject"], candidate.manifest["fixture"])
    require(baseline.manifest["run_id"] != candidate.manifest["run_id"], "Candidate cannot compare to itself")
    ba, ca = baseline.accepted_assembly()["assembly"], candidate.accepted_assembly()["assembly"]
    round_no = ca["assembly_round"]
    instrument = _instrument(candidate)
    a, b = (ba["text"], ca["text"]) if order == "AB" else (ca["text"], ba["text"])
    judge_task = {
        "schema_version": 2,
        "role": "pair-judge",
        "contract": instrument["contract"],
        "style": "",
        "inputs": {
            "A": a, "B": b,
            "reader_goal": candidate.brief["reader_goal"],
            "audience": candidate.brief["audience"],
            "evaluation_goal": "Detect any material regression versus the inherited baseline; ties are acceptable.",
        },
    }
    record = {
        "schema_version": 2, "task": judge_task, "order": order, "assembly_round": round_no,
        "instrument_hash": digest(instrument),
        "candidate_manifest_sha256": digest(candidate.manifest),
        "baseline_manifest_sha256": digest(baseline.manifest),
        "candidate_book_sha256": ca["text_sha256"], "baseline_book_sha256": ba["text_sha256"],
        "candidate_audit_sha256": file_hash(candidate.accepted_audit_file()),
        "baseline_audit_sha256": file_hash(baseline.accepted_audit_file()),
        "learning_sha256": digest(candidate.learning),
    }
    with lock(candidate.root / "regression"):
        seal(task_path(candidate, round_no, order), record)
    return judge_task


def _validate_judgment(judge_task: dict, output: dict) -> None:
    exact_keys(output, {"schema_version", "preferences", "critical"}, label="no-regression judgment")
    require(output["schema_version"] == 2, "Invalid judgment schema")
    exact_keys(output["preferences"], set(DIMENSIONS), label="judgment preferences")
    for preference in output["preferences"].values():
        exact_keys(preference, {"winner", "a_quote", "b_quote", "reason"}, label="dimension judgment")
        require(preference["winner"] in ("A", "B", "tie"), "Invalid preference winner")
        nonempty(preference["reason"], "Preference explanation")
        for label, key in (("A", "a_quote"), ("B", "b_quote")):
            nonempty(preference[key], "Preference evidence")
            require(preference[key] in judge_task["inputs"][label], "Judgment quote not present in labeled book")
    exact_keys(output["critical"], {"A", "B"}, label="critical findings")
    for label, findings in output["critical"].items():
        require(isinstance(findings, list), "Critical findings must be a list")
        for finding in findings:
            exact_keys(finding, {"kind", "quote", "explanation"}, label="critical finding")
            require(finding["kind"] in FINDINGS, "Unknown critical finding")
            require(bool(finding["quote"]) and finding["quote"] in judge_task["inputs"][label], "Invalid critical quote")
            nonempty(finding["explanation"], "Critical explanation")


def submit(repo: Path, run_id: str, order: str, output: dict, metadata: dict) -> dict:
    from .runs import Run
    candidate = Run(repo, identifier(run_id))
    judge_task = task(repo, run_id, order)
    round_no = _round(candidate)
    record = unseal(task_path(candidate, round_no, order))
    _validate_judgment(judge_task, output)
    validate_metadata(metadata)
    baseline = validate_packet_binding(repo, candidate.learning, candidate.brief["subject"], candidate.manifest["fixture"])
    require(metadata["family"] not in candidate.generating_families() | baseline.generating_families(),
            "No-regression judge must be independent of both generators")
    if not candidate.manifest["fixture"]:
        require(metadata["harness"] != "fixture", "Fixture judging cannot validate a live baseline gate")
    result = {"schema_version": 2, "task_hash": digest(record), "output": output,
              "metadata": metadata, "created_at": now()}
    with lock(candidate.root / "regression"):
        seal(judgment_path(candidate, round_no, order), result)
    return result


def _candidate_label(order: str) -> str:
    return "B" if order == "AB" else "A"


def decide(repo: Path, run_id: str) -> dict:
    from .runs import Run
    candidate = Run(repo, identifier(run_id))
    candidate.complete()
    require(candidate.learning is not None, "No-regression gate requires a frozen baseline")
    round_no = _round(candidate)
    dpath = decision_path(candidate, round_no)
    if dpath.exists():
        stored = unseal(dpath)
        require(stored["candidate_book_sha256"] == candidate.accepted_assembly()["assembly"]["text_sha256"],
                "Stored no-regression decision is stale")
        return stored
    missing, results, judge_profiles = [], {}, set()
    for order in ("AB", "BA"):
        task(repo, run_id, order)
        path = judgment_path(candidate, round_no, order)
        if not path.exists():
            missing.append(order)
            continue
        task_record = unseal(task_path(candidate, round_no, order))
        result = unseal(path)
        require(result["task_hash"] == digest(task_record), "No-regression judgment has stale task inputs")
        meta = result["metadata"]
        judge_profiles.add((meta["model"], meta["family"], meta["route"], meta["harness"]))
        results[order] = result
    if missing:
        return {"decision": "INCONCLUSIVE", "run_id": run_id, "assembly_round": round_no,
                "missing": missing, "reason": "Both blinded label orders are required; no baseline advancement"}
    outcomes, instability, losses, critical = {}, [], [], []
    for dimension in DIMENSIONS:
        observations = []
        for order in ("AB", "BA"):
            pref = results[order]["output"]["preferences"][dimension]
            label = _candidate_label(order)
            observations.append(0 if pref["winner"] == "tie" else 1 if pref["winner"] == label else -1)
        if observations[0] != observations[1]:
            status = "order_sensitive"; instability.append(dimension)
        elif observations[0] == -1:
            status = "baseline_win"; losses.append(dimension)
        elif observations[0] == 1:
            status = "candidate_win"
        else:
            status = "tie"
        outcomes[dimension] = {"outcome": status,
                               "AB": results["AB"]["output"]["preferences"][dimension],
                               "BA": results["BA"]["output"]["preferences"][dimension]}
    for order in ("AB", "BA"):
        findings = results[order]["output"]["critical"][_candidate_label(order)]
        if findings:
            critical.append({"order": order, "findings": findings})
    has_improvement = any(x["outcome"] == "candidate_win" for x in outcomes.values())
    mixed_judges = len(judge_profiles) != 1
    gate = ("INCONCLUSIVE" if mixed_judges else
            "REPAIR_REQUIRED" if critical or losses else
            "INCONCLUSIVE" if instability else
            "ADVANCE" if has_improvement else
            "PRESERVE_BASELINE")
    ca = candidate.accepted_assembly()["assembly"]
    baseline = validate_packet_binding(repo, candidate.learning, candidate.brief["subject"], candidate.manifest["fixture"])
    decision = {
        "schema_version": 2, "decision": gate, "run_id": run_id,
        "baseline_run": baseline.manifest["run_id"], "assembly_round": round_no,
        "candidate_book_sha256": ca["text_sha256"],
        "baseline_book_sha256": baseline.accepted_assembly()["assembly"]["text_sha256"],
        "candidate_audit_sha256": file_hash(candidate.accepted_audit_file()),
        "baseline_audit_sha256": file_hash(baseline.accepted_audit_file()),
        "dimension_outcomes": outcomes, "losses": losses, "critical": critical,
        "order_instability": instability,
        "judge_profiles": [{"model": m, "family": f, "route": r, "harness": h}
                           for m, f, r, h in sorted(judge_profiles)],
        "judge_instrument_mixed": mixed_judges,
        "judgment_sha256": {o: file_hash(judgment_path(candidate, round_no, o)) for o in ("AB", "BA")},
        "created_at": now(),
    }
    with lock(candidate.root / "regression"):
        seal(dpath, decision)
    return decision


def repair_feedback(run, assembly_round: int) -> dict:
    path = decision_path(run, assembly_round)
    require(path.is_file(), "Accepted assembly needs a sealed no-regression decision before post-audit repair")
    decision = unseal(path)
    require(decision["decision"] == "REPAIR_REQUIRED",
            "Accepted assembly can only reopen for a material no-regression failure")
    assembly = run.assembly_version(assembly_round)["assembly"]
    require(decision["candidate_book_sha256"] == assembly["text_sha256"], "No-regression feedback is stale")
    au, _ = run.accepted_audit()
    require(au == assembly_round and decision["candidate_audit_sha256"] == file_hash(run.accepted_audit_file()),
            "No-regression feedback is not bound to the accepted audit")
    rel = path.relative_to(run.root).as_posix()
    return {"rel": rel, "sha256": file_hash(path), "decision": decision}
