"""Frozen cross-iteration editorial learning packets."""
from __future__ import annotations

from pathlib import Path

from .common import digest, exact_keys, file_hash, identifier, lock, nonempty, require, seal
from .schema import DIMENSIONS, FINDINGS, validate_learning_packet


def _dimension_items(items: object, label: str) -> list[dict]:
    require(isinstance(items, list), f"{label} must be a list")
    out, seen = [], set()
    for item in items:
        exact_keys(item, {"dimension", "instruction", "evidence"}, label=label)
        require(item["dimension"] in DIMENSIONS, f"Unknown learning dimension: {item['dimension']}")
        require(item["dimension"] not in seen, f"Duplicate {label} dimension: {item['dimension']}")
        seen.add(item["dimension"])
        nonempty(item["instruction"], f"{label} instruction")
        nonempty(item["evidence"], f"{label} evidence")
        out.append(item)
    return out


def _repair_items(items: object) -> list[dict]:
    require(isinstance(items, list), "recurring_repairs must be a list")
    out = []
    for item in items:
        exact_keys(item, {"kind", "instruction", "evidence"}, label="recurring repair")
        require(item["kind"] in FINDINGS, f"Unknown recurring repair kind: {item['kind']}")
        nonempty(item["instruction"], "Recurring repair instruction")
        nonempty(item["evidence"], "Recurring repair evidence")
        out.append(item)
    return out


def validate_lessons(data: dict) -> None:
    exact_keys(data, {"schema_version", "subject", "preserve", "improve", "recurring_repairs",
                      "research_gaps", "note"}, label="cross-iteration seed lessons")
    require(data["schema_version"] == 2, "Learning schema must be v2")
    identifier(data["subject"])
    preserve = _dimension_items(data["preserve"], "preserve")
    improve = _dimension_items(data["improve"], "improve")
    require({x["dimension"] for x in preserve}.isdisjoint({x["dimension"] for x in improve}),
            "A dimension cannot be both preserve and improve in one learning packet")
    _repair_items(data["recurring_repairs"])
    require(isinstance(data["research_gaps"], list) and
            all(isinstance(x, str) and x.strip() for x in data["research_gaps"]),
            "research_gaps must be nonempty strings")
    nonempty(data["note"], "Learning note")


def _packet_for(run, preserve: list[dict], improve: list[dict], recurring: list[dict],
                research_gaps: list[str], provenance: dict) -> dict:
    complete = run.complete()
    packet = {
        "schema_version": 2,
        "subject": run.brief["subject"],
        "baseline_run": run.manifest["run_id"],
        "baseline_manifest_sha256": digest(run.manifest),
        "baseline_book_sha256": complete["book_sha256"],
        "baseline_audit_sha256": file_hash(run.accepted_audit_file()),
        "preserve": preserve,
        "improve": improve,
        "recurring_repairs": recurring,
        "research_gaps": research_gaps,
        "provenance": provenance,
    }
    validate_learning_packet(packet)
    return packet


def learning_path(run) -> Path:
    return run.root / "regression" / "learning-next.json"


def load_next(run) -> dict:
    from .runs import load_learning_packet
    return load_learning_packet(run)


def validate_packet_binding(repo: Path, packet: dict, expected_subject: str, fixture: bool):
    from .runs import validate_learning_binding
    return validate_learning_binding(repo, packet, expected_subject, fixture)


def seed(repo: Path, run_id: str, lessons: dict) -> dict:
    from .runs import Run
    validate_lessons(lessons)
    run = Run(repo, identifier(run_id))
    run.complete()
    require(run.brief["subject"] == lessons["subject"], "Seed lessons subject mismatch")
    packet = _packet_for(
        run, lessons["preserve"], lessons["improve"], lessons["recurring_repairs"], lessons["research_gaps"],
        {"mode": "bootstrap", "source_sha256": digest(lessons), "note": lessons["note"]},
    )
    path = learning_path(run)
    with lock(run.root / "regression"):
        seal(path, packet)
    return {"status": "LEARNING_SEEDED", "run_id": run_id,
            "path": path.relative_to(repo).as_posix(), "learning_sha256": digest(packet)}


def advance(repo: Path, run_id: str) -> dict:
    from .regression import decide, decision_path
    from .runs import Run
    candidate = Run(repo, identifier(run_id))
    candidate.complete()
    require(candidate.learning is not None, "Baseline advancement requires inherited learning")
    decision = decide(repo, run_id)
    if decision["decision"] == "PRESERVE_BASELINE":
        return {"status": "BASELINE_PRESERVED", "run_id": run_id,
                "baseline_run": candidate.learning["baseline_run"]}
    require(decision["decision"] == "ADVANCE", f"Baseline advancement blocked: {decision['decision']}")
    old = candidate.learning
    preserve = {x["dimension"]: dict(x) for x in old["preserve"]}
    improve = {x["dimension"]: dict(x) for x in old["improve"]}
    for dimension, outcome in decision["dimension_outcomes"].items():
        if outcome["outcome"] != "candidate_win":
            continue
        evidence = ("Independent AB/BA no-regression gate consistently preferred the candidate. "
                    "AB: " + outcome["AB"]["reason"] + " BA: " + outcome["BA"]["reason"])
        if dimension in improve:
            prior = improve.pop(dimension)
            preserve[dimension] = {"dimension": dimension,
                "instruction": "Preserve the achieved improvement: " + prior["instruction"], "evidence": evidence}
        elif dimension not in preserve:
            preserve[dimension] = {"dimension": dimension,
                "instruction": f"Preserve the demonstrated {dimension} advantage without weakening other protected dimensions.",
                "evidence": evidence}
    dpath = decision_path(candidate, candidate.accepted_assembly()["assembly"]["assembly_round"])
    packet = _packet_for(
        candidate, list(preserve.values()), list(improve.values()),
        [dict(x) for x in old["recurring_repairs"]], list(old["research_gaps"]),
        {"mode": "no_regression_pass", "source_sha256": file_hash(dpath),
         "note": "Advanced only after a stable blinded AB/BA candidate improvement with no regression."},
    )
    path = learning_path(candidate)
    with lock(candidate.root / "regression"):
        seal(path, packet)
    return {"status": "BASELINE_ADVANCED", "run_id": run_id,
            "path": path.relative_to(repo).as_posix(), "learning_sha256": digest(packet)}
