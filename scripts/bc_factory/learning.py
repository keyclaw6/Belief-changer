"""Frozen cross-iteration editorial learning packets."""
from __future__ import annotations

from pathlib import Path

from .common import digest, exact_keys, file_hash, identifier, lock, nonempty, require, seal, unseal
from .schema import DIMENSIONS, FINDINGS

LEARNING_CONTRACT = """
CROSS-ITERATION LEARNING (inherited, frozen):
- cross_iteration_learning is editorial/evaluation feedback, NOT empirical evidence. Never cite it as support for a factual claim.
- Preserve every listed strength, address every listed improvement target, and do not reintroduce a recurring repair unless current verified research genuinely resolves the stated issue.
- These constraints are NOT a mandatory rhetorical template. Apply them only where relevant to the present subject; never force a learned mechanism, metaphor, addiction model, abstinence structure, chapter anatomy, or stylistic trick onto a domain that does not support it.
- Research gaps guide targeted retrieval or safe scope exclusions; they are not claims that the missing proposition is true.
- Later reviewers first verify these inherited constraints before widening critique. New concerns still need the normal material truth/safety/revision-caused justification.
""".strip()


def _sha(value: object, label: str) -> str:
    require(isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value),
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
    require(isinstance(data["research_gaps"], list) and
            all(isinstance(x, str) and x.strip() for x in data["research_gaps"]),
            "research_gaps must be nonempty strings")
    nonempty(data["note"], "Learning note")


def validate_packet(data: dict) -> None:
    exact_keys(data, {"schema_version", "subject", "baseline_run", "baseline_manifest_sha256",
                      "baseline_book_sha256", "baseline_audit_sha256", "preserve", "improve",
                      "recurring_repairs", "research_gaps", "provenance"}, label="cross-iteration learning packet")
    require(data["schema_version"] == 2, "Learning packet schema must be v2")
    identifier(data["subject"]); identifier(data["baseline_run"])
    _sha(data["baseline_manifest_sha256"], "baseline_manifest_sha256")
    _sha(data["baseline_book_sha256"], "baseline_book_sha256")
    _sha(data["baseline_audit_sha256"], "baseline_audit_sha256")
    preserve = _dimension_items(data["preserve"], "preserve")
    improve = _dimension_items(data["improve"], "improve")
    require({x["dimension"] for x in preserve}.isdisjoint({x["dimension"] for x in improve}),
            "A dimension cannot be both preserve and improve")
    _repair_items(data["recurring_repairs"])
    require(isinstance(data["research_gaps"], list) and
            all(isinstance(x, str) and x.strip() for x in data["research_gaps"]),
            "research_gaps must be nonempty strings")
    exact_keys(data["provenance"], {"mode", "source_sha256", "note"}, label="learning provenance")
    require(data["provenance"]["mode"] in ("bootstrap", "no_regression_pass", "no_regression_advance", "no_regression_preserve"),
            "Unknown learning provenance")
    _sha(data["provenance"]["source_sha256"], "Learning provenance source_sha256")
    nonempty(data["provenance"]["note"], "Learning provenance note")


def _packet_for(baseline, preserve: list[dict], improve: list[dict], recurring: list[dict],
                research_gaps: list[str], provenance: dict) -> dict:
    complete = baseline.complete()
    packet = {
        "schema_version": 2,
        "subject": baseline.brief["subject"],
        "baseline_run": baseline.manifest["run_id"],
        "baseline_manifest_sha256": digest(baseline.manifest),
        "baseline_book_sha256": complete["book_sha256"],
        "baseline_audit_sha256": file_hash(baseline.accepted_audit_file()),
        "preserve": preserve,
        "improve": improve,
        "recurring_repairs": recurring,
        "research_gaps": research_gaps,
        "provenance": provenance,
    }
    validate_packet(packet)
    return packet


def learning_path(run) -> Path:
    return run.root / "regression" / "learning-next.json"


def _revision_number(path: Path) -> int:
    stem = path.stem
    require(stem.startswith("learning-r") and stem[10:].isdigit(), f"Invalid learning revision filename: {path.name}")
    return int(stem[10:])


def _revision_paths(run) -> list[Path]:
    root = run.root / "regression" / "learning-revisions"
    return sorted(root.glob("learning-r*.json"), key=_revision_number) if root.is_dir() else []


def _next_revision_path(run) -> Path:
    paths = _revision_paths(run)
    next_no = (_revision_number(paths[-1]) + 1) if paths else 1
    return run.root / "regression" / "learning-revisions" / f"learning-r{next_no:02d}.json"


def load_next(run) -> dict:
    revisions = _revision_paths(run)
    path = revisions[-1] if revisions else learning_path(run)
    packet = unseal(path)
    validate_packet(packet)
    require(packet["baseline_run"] == run.manifest["run_id"], "Learning packet is bound to another run")
    return packet


def validate_packet_binding(repo: Path, packet: dict, expected_subject: str, fixture: bool):
    from .runs import Run
    validate_packet(packet)
    baseline = Run(repo, packet["baseline_run"])
    complete = baseline.complete()
    require(baseline.brief["subject"] == expected_subject == packet["subject"], "Learning baseline subject mismatch")
    require(baseline.manifest["fixture"] == fixture, "Learning baseline fixture/live trust mismatch")
    require(digest(baseline.manifest) == packet["baseline_manifest_sha256"], "Learning baseline manifest changed")
    require(complete["book_sha256"] == packet["baseline_book_sha256"], "Learning baseline book changed")
    require(file_hash(baseline.accepted_audit_file()) == packet["baseline_audit_sha256"],
            "Learning baseline audit changed")
    return baseline


def research_guidance(packet: dict, brief: dict) -> dict:
    validate_packet(packet)
    require(packet["subject"] == brief["subject"], "Research guidance subject mismatch")
    core = {
        "schema_version": 2,
        "subject": brief["subject"],
        "baseline_run": packet["baseline_run"],
        "learning_sha256": digest(packet),
        "research_gaps": list(packet["research_gaps"]),
        "instruction": "Treat these as search priorities only. Re-establish every question from fresh current-subject sources; prior learning is not evidence.",
    }
    return {**core, "guidance_sha256": digest(core)}


def guidance_for(repo: Path, baseline_run: str, brief: dict) -> dict:
    from .runs import Run
    source = Run(repo, identifier(baseline_run))
    packet = load_next(source)
    validate_packet_binding(repo, packet, brief["subject"], source.manifest["fixture"])
    return research_guidance(packet, brief)


def validate_research_learning(research: dict, packet: dict, brief: dict) -> None:
    guidance = research_guidance(packet, brief)
    context = research.get("learning_context")
    require(isinstance(context, dict), "A learning successor must bind the pre-research learning context")
    exact_keys(context, {"guidance_sha256", "baseline_run", "gap_resolutions"}, label="research learning context")
    require(context["guidance_sha256"] == guidance["guidance_sha256"], "Research used stale or different cross-iteration guidance")
    require(context["baseline_run"] == packet["baseline_run"], "Research learning baseline mismatch")
    resolutions = context["gap_resolutions"]
    require(isinstance(resolutions, list), "gap_resolutions must be a list")
    expected = list(packet["research_gaps"])
    require(len(resolutions) == len(expected), "Every inherited research gap needs one explicit resolution")
    seen = set(); source_ids = {x["id"] for x in research["sources"]}
    for item in resolutions:
        exact_keys(item, {"gap", "status", "evidence_ids", "note"}, label="research gap resolution")
        require(item["gap"] in expected and item["gap"] not in seen, "Unknown or duplicate inherited research gap")
        seen.add(item["gap"])
        require(item["status"] in ("addressed", "scoped_out", "unresolved"), "Unknown research gap status")
        require(isinstance(item["evidence_ids"], list) and set(item["evidence_ids"]) <= source_ids,
                "Research gap resolution cites unknown evidence")
        if item["status"] == "addressed":
            require(bool(item["evidence_ids"]), "Addressed research gap needs current-subject evidence IDs")
        nonempty(item["note"], "research gap resolution note")
    require(seen == set(expected), "Inherited research gap coverage is incomplete")


def seed(repo: Path, run_id: str, lessons: dict) -> dict:
    from .runs import Run
    validate_lessons(lessons)
    run = Run(repo, identifier(run_id)); run.complete()
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


def _accumulate(candidate, old: dict, decisions: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    preserve = {x["dimension"]: dict(x) for x in old["preserve"]}
    improve = {x["dimension"]: dict(x) for x in old["improve"]}
    repairs = [dict(x) for x in old["recurring_repairs"]]
    repair_keys = {(x["kind"], x["instruction"]) for x in repairs}

    for decision in decisions:
        for dimension in decision.get("losses", []):
            if dimension not in preserve and dimension not in improve:
                improve[dimension] = {
                    "dimension": dimension,
                    "instruction": f"Avoid the previously observed {dimension} regression while preserving protected strengths.",
                    "evidence": f"No-regression round {decision['assembly_round']} consistently preferred the prior baseline on {dimension} before repair.",
                }
        for block in decision.get("critical", []):
            for finding in block.get("findings", []):
                instruction = finding["explanation"]
                key = (finding["kind"], instruction)
                if key not in repair_keys:
                    repairs.append({"kind": finding["kind"], "instruction": instruction,
                                    "evidence": f"Independent no-regression judge flagged: {finding['quote']}"})
                    repair_keys.add(key)

    for path in sorted((candidate.root / "results").glob("final-auditor-r*.json")):
        record = unseal(path); output = record["output"]
        if output["verdict"] == "ACCEPT":
            continue
        for finding in output["findings"]:
            if finding["severity"] not in ("material", "critical"):
                continue
            instruction = finding["repair"]
            key = (finding["kind"], instruction)
            if key not in repair_keys:
                evidence = finding["explanation"] + (f" Quote: {finding['quote']}" if finding["quote"] else "")
                repairs.append({"kind": finding["kind"], "instruction": instruction, "evidence": evidence})
                repair_keys.add(key)
    return list(preserve.values()), list(improve.values()), repairs


def _next_research_gaps(candidate) -> list[str]:
    gaps = []
    for gap in candidate.research["open_questions"]:
        if gap not in gaps:
            gaps.append(gap)
    context = candidate.research.get("learning_context")
    if context:
        for item in context["gap_resolutions"]:
            if item["status"] == "unresolved" and item["gap"] not in gaps:
                gaps.append(item["gap"])
    return gaps


def advance(repo: Path, run_id: str) -> dict:
    from .regression import decide, decision_path
    from .runs import Run
    candidate = Run(repo, identifier(run_id)); candidate.complete()
    require(candidate.learning is not None, "Baseline update requires inherited learning")
    decision = decide(repo, run_id)
    require(decision["decision"] in ("ADVANCE", "PRESERVE_BASELINE"),
            f"Baseline update blocked: {decision['decision']}")
    old = candidate.learning
    decisions = [unseal(p) for p in sorted((candidate.root / "regression").glob("decision-r*.json"))]
    preserve_list, improve_list, repairs = _accumulate(candidate, old, decisions)
    preserve = {x["dimension"]: x for x in preserve_list}
    improve = {x["dimension"]: x for x in improve_list}
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
    if decision["decision"] == "ADVANCE":
        baseline = candidate; mode = "no_regression_advance"
        note = "Candidate became the new baseline only after a stable improvement and zero protected regressions."
        path = learning_path(candidate); status = "BASELINE_ADVANCED"
    else:
        baseline = Run(repo, old["baseline_run"]); mode = "no_regression_preserve"
        note = (f"Candidate {candidate.manifest['run_id']} did not demonstrate a stable improvement; "
                "the prior book baseline was preserved while newly observed lessons were appended.")
        decision_sha = file_hash(dpath)
        for existing_path in _revision_paths(baseline):
            existing = unseal(existing_path)
            if existing["provenance"]["source_sha256"] == decision_sha:
                return {"status": "BASELINE_PRESERVED_LEARNING_UPDATED", "run_id": run_id,
                        "baseline_run": baseline.manifest["run_id"],
                        "path": existing_path.relative_to(repo).as_posix(),
                        "learning_sha256": digest(existing)}
        path = _next_revision_path(baseline); status = "BASELINE_PRESERVED_LEARNING_UPDATED"

    packet = _packet_for(
        baseline, list(preserve.values()), list(improve.values()), repairs, _next_research_gaps(candidate),
        {"mode": mode, "source_sha256": file_hash(dpath), "note": note},
    )
    with lock(baseline.root / "regression"):
        seal(path, packet)
    return {"status": status, "run_id": run_id, "baseline_run": baseline.manifest["run_id"],
            "path": path.relative_to(repo).as_posix(), "learning_sha256": digest(packet)}
