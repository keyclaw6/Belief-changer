"""Outer autoresearch learning packets and generic factory caller context."""
from __future__ import annotations

from pathlib import Path

from bc_factory.common import digest, exact_keys, file_hash, identifier, lock, nonempty, require, seal, unseal
from bc_factory.schema import DIMENSIONS, FINDINGS


def _sha256(value: object, label: str) -> str:
    require(isinstance(value, str) and len(value) == 64
            and all(c in "0123456789abcdef" for c in value),
            f"{label} must be a lowercase SHA-256")
    return value


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
    require(isinstance(data["research_gaps"], list)
            and all(isinstance(x, str) and x.strip() for x in data["research_gaps"]),
            "research_gaps must be nonempty strings")
    nonempty(data["note"], "Learning note")


def validate_packet(data: dict) -> None:
    exact_keys(data, {"schema_version", "subject", "baseline_run", "baseline_manifest_sha256",
                      "baseline_book_sha256", "baseline_audit_sha256", "preserve", "improve",
                      "recurring_repairs", "research_gaps", "provenance"},
               label="cross-iteration learning packet")
    require(data["schema_version"] == 2, "Learning packet schema must be v2")
    identifier(data["subject"])
    identifier(data["baseline_run"])
    _sha256(data["baseline_manifest_sha256"], "baseline_manifest_sha256")
    _sha256(data["baseline_book_sha256"], "baseline_book_sha256")
    _sha256(data["baseline_audit_sha256"], "baseline_audit_sha256")
    preserve = _dimension_items(data["preserve"], "preserve")
    improve = _dimension_items(data["improve"], "improve")
    require({x["dimension"] for x in preserve}.isdisjoint({x["dimension"] for x in improve}),
            "A dimension cannot be both preserve and improve")
    _repair_items(data["recurring_repairs"])
    require(isinstance(data["research_gaps"], list)
            and all(isinstance(x, str) and x.strip() for x in data["research_gaps"]),
            "research_gaps must be nonempty strings")
    exact_keys(data["provenance"], {"mode", "source_sha256", "note"}, label="learning provenance")
    require(data["provenance"]["mode"] in ("bootstrap", "no_regression_pass"),
            "Unknown learning provenance")
    _sha256(data["provenance"]["source_sha256"], "Learning provenance source_sha256")
    nonempty(data["provenance"]["note"], "Learning provenance note")


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
    validate_packet(packet)
    return packet


def factory_context(packet: dict) -> dict:
    """Strip autoresearch lineage/evidence into generic caller-owned guidance."""
    validate_packet(packet)
    constraints = [
        {"intent": "preserve", "area": x["dimension"], "instruction": x["instruction"]}
        for x in packet["preserve"]
    ]
    constraints += [
        {"intent": "improve", "area": x["dimension"], "instruction": x["instruction"]}
        for x in packet["improve"]
    ]
    constraints += [
        {"intent": "repair", "area": x["kind"], "instruction": x["instruction"]}
        for x in packet["recurring_repairs"]
    ]
    return {
        "schema_version": 2,
        "research_priorities": list(packet["research_gaps"]),
        "editorial_constraints": constraints,
    }


def learning_path(run) -> Path:
    return run.root / "caller-feedback" / "learning-next.json"


def context_path(run) -> Path:
    return run.root / "caller-feedback" / "factory-context.json"


def load_next(run) -> dict:
    packet = unseal(learning_path(run))
    validate_packet(packet)
    require(packet["baseline_run"] == run.manifest["run_id"],
            "Learning packet is bound to another run")
    return packet


def validate_packet_binding(repo: Path, packet: dict, expected_subject: str, fixture: bool):
    from bc_factory.runs import Run
    validate_packet(packet)
    baseline = Run(repo, packet["baseline_run"])
    complete = baseline.complete()
    require(baseline.brief["subject"] == expected_subject == packet["subject"],
            "Learning baseline subject mismatch")
    require(baseline.manifest["fixture"] == fixture, "Learning baseline fixture/live trust mismatch")
    require(digest(baseline.manifest) == packet["baseline_manifest_sha256"],
            "Learning baseline manifest changed")
    require(complete["book_sha256"] == packet["baseline_book_sha256"],
            "Learning baseline book changed")
    require(file_hash(baseline.accepted_audit_file()) == packet["baseline_audit_sha256"],
            "Learning baseline audit changed")
    return baseline


def baseline_for_candidate(repo: Path, candidate, baseline_run_id: str):
    from bc_factory.runs import Run
    baseline = Run(repo, identifier(baseline_run_id))
    packet = load_next(baseline)
    validate_packet_binding(repo, packet, candidate.brief["subject"], candidate.manifest["fixture"])
    require(baseline.manifest["run_id"] != candidate.manifest["run_id"],
            "Candidate cannot compare to itself")
    expected = factory_context(packet)
    require(candidate.caller_context is not None and digest(candidate.caller_context) == digest(expected),
            "Candidate caller context is not bound to the selected learning baseline")
    return baseline, packet


def _write_artifacts(run, packet: dict) -> tuple[Path, Path]:
    lp, cp = learning_path(run), context_path(run)
    with lock(lp.parent):
        seal(lp, packet)
        seal(cp, factory_context(packet))
    return lp, cp


def seed(repo: Path, run_id: str, lessons: dict) -> dict:
    from bc_factory.runs import Run
    validate_lessons(lessons)
    run = Run(repo, identifier(run_id))
    run.complete()
    require(run.brief["subject"] == lessons["subject"], "Seed lessons subject mismatch")
    packet = _packet_for(
        run, lessons["preserve"], lessons["improve"], lessons["recurring_repairs"], lessons["research_gaps"],
        {"mode": "bootstrap", "source_sha256": digest(lessons), "note": lessons["note"]},
    )
    lp, cp = _write_artifacts(run, packet)
    return {"status": "LEARNING_SEEDED", "run_id": run_id,
            "path": lp.relative_to(repo).as_posix(),
            "factory_context": cp.relative_to(repo).as_posix(),
            "learning_sha256": digest(packet)}


def advance(repo: Path, run_id: str, baseline_run_id: str) -> dict:
    from .regression import decide, decision_path
    from bc_factory.runs import Run
    candidate = Run(repo, identifier(run_id))
    candidate.complete()
    baseline, old = baseline_for_candidate(repo, candidate, baseline_run_id)
    decision = decide(repo, run_id, baseline_run_id)
    if decision["decision"] == "PRESERVE_BASELINE":
        return {"status": "BASELINE_PRESERVED", "run_id": run_id,
                "baseline_run": baseline.manifest["run_id"]}
    require(decision["decision"] == "ADVANCE",
            f"Baseline advancement blocked: {decision['decision']}")
    preserve = {x["dimension"]: dict(x) for x in old["preserve"]}
    improve = {x["dimension"]: dict(x) for x in old["improve"]}
    for dimension, outcome in decision["dimension_outcomes"].items():
        if outcome["outcome"] != "candidate_win":
            continue
        evidence = ("Independent AB/BA no-regression gate consistently preferred the candidate. "
                    "AB: " + outcome["AB"]["reason"] + " BA: " + outcome["BA"]["reason"])
        if dimension in improve:
            prior = improve.pop(dimension)
            preserve[dimension] = {
                "dimension": dimension,
                "instruction": "Preserve the achieved improvement: " + prior["instruction"],
                "evidence": evidence,
            }
        elif dimension not in preserve:
            preserve[dimension] = {
                "dimension": dimension,
                "instruction": f"Preserve the demonstrated {dimension} advantage without weakening other protected dimensions.",
                "evidence": evidence,
            }
    dpath = decision_path(candidate, candidate.accepted_assembly()["assembly"]["assembly_round"])
    packet = _packet_for(
        candidate, list(preserve.values()), list(improve.values()),
        [dict(x) for x in old["recurring_repairs"]], list(old["research_gaps"]),
        {"mode": "no_regression_pass", "source_sha256": file_hash(dpath),
         "note": "Advanced only after a stable blinded AB/BA candidate improvement with no regression."},
    )
    lp, cp = _write_artifacts(candidate, packet)
    return {"status": "BASELINE_ADVANCED", "run_id": run_id,
            "path": lp.relative_to(repo).as_posix(),
            "factory_context": cp.relative_to(repo).as_posix(),
            "learning_sha256": digest(packet)}
