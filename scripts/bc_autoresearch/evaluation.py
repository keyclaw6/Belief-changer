"""Normal outer model calls, using the same bound receipts as factory stages."""
from __future__ import annotations

from pathlib import Path

from bc_factory.adapters import execute, validate_identity
from bc_factory.common import digest, exact_keys, file_hash, identifier, lock, nonempty, require, seal, unseal
from bc_factory.runs import Run
from . import regression


def validate_learning(role: str, output: dict) -> None:
    reviewer = role == "factory-learning-reviewer"
    fields = ({"verdict", "checks", "findings", "approved_change_surface", "held_out_test"} if reviewer else
              {"decision", "observations", "candidate_root_causes", "subject_specific_lessons",
               "transferable_factory_lessons", "protected_strengths", "proposed_factory_change",
               "falsification_test", "confidence"})
    exact_keys(output, {"schema_version", "reasoning_summary", *fields}, label=role)
    require(output["schema_version"] == 2, "Learning output must use schema v2")
    nonempty(output["reasoning_summary"], "Learning reasoning")
    if reviewer:
        require(output["verdict"] in ("ACCEPT", "REVISE", "REJECT", "MEASURE_MORE"), "Invalid learning review")
        checks = output["checks"]
        expected = {"transferable", "not_subject_overfit", "causal_honesty", "minimal_change",
                    "protected_strengths", "held_out_integrity", "judge_overfit_control", "falsifiable"}
        exact_keys(checks, expected, label="learning review checks")
        require(all(type(v) is bool for v in checks.values()), "Review checks must be booleans")
        require(isinstance(output["findings"], list) and isinstance(output["approved_change_surface"], list)
                and isinstance(output["held_out_test"], dict), "Incomplete learning review")
        if output["verdict"] == "ACCEPT":
            require(all(checks.values()) and not output["findings"], "ACCEPT needs all checks and no findings")
    else:
        require(output["decision"] in ("CHANGE_FACTORY", "KEEP_FACTORY", "MEASURE_MORE"), "Invalid learner decision")
        require(output["confidence"] in ("low", "medium", "high"), "Invalid learning confidence")
        require(all(isinstance(output[k], list) for k in ("observations", "candidate_root_causes",
                    "subject_specific_lessons", "transferable_factory_lessons", "protected_strengths")) and
                isinstance(output["proposed_factory_change"], dict) and isinstance(output["falsification_test"], dict),
                "Incomplete learner output")


def compare(repo: Path, run_id: str, baseline: str, order: str,
            allow_paid: bool = False, new_attempt: bool = False) -> dict:
    run = Run(repo, run_id)
    with lock(run.root / "regression/inflight" / order):
        judge_task = regression.task(repo, run_id, baseline, order)
        round_no = run.accepted_assembly()["assembly"]["assembly_round"]
        record = unseal(regression.task_path(run, round_no, order))
        path = regression.judgment_path(run, round_no, order)
        if path.exists():
            saved = unseal(path)
            require(saved["task_hash"] == digest(record), "Saved comparison is stale")
            validate_identity(saved["metadata"], run.config, "external")
            require(run.manifest["fixture"] or saved["metadata"]["harness"] != "fixture",
                    "Synthetic comparison cannot enter a live cycle")
            # Submission rechecks quotation support and independence as well.
            regression.submit(repo, run_id, baseline, order, saved["output"], saved["metadata"])
        else:
            output, metadata = execute(judge_task, run.config, allow_paid, "external",
                                       run.root / "regression/requests", new_attempt)
            validate_identity(metadata, run.config, "external")
            require(run.manifest["fixture"] or metadata["harness"] != "fixture",
                    "Synthetic comparison cannot enter a live cycle")
            saved = regression.submit(repo, run_id, baseline, order, output, metadata)
        return {"status": "RECORDED", "task_hash": saved["task_hash"]}


def learn(repo: Path, iteration: str, run_id: str, baseline: str,
          allow_paid: bool = False, new_attempt: bool = False) -> dict:
    """Retain a real learner and independent reviewer; never apply their edits."""
    run, prior = Run(repo, run_id), Run(repo, baseline)
    complete, prior_complete = run.complete(), prior.complete()
    decision = regression.decide(repo, run_id, baseline)
    require(not decision.get("missing"), "Learning needs both real label-order judgments")
    root = repo / "loop/iterations" / identifier(iteration) / "learning"
    inputs = {"candidate": {"complete": complete, "brief": run.brief, "research": run.research,
                             "book": run.accepted_assembly()["assembly"]["text"],
                             "audit": run.accepted_audit()[1]},
              "baseline": {"complete": prior_complete, "book": prior.accepted_assembly()["assembly"]["text"]},
              "decision": decision,
              "judgments": {o: unseal(regression.judgment_path(run, decision["assembly_round"], o))
                            for o in ("AB", "BA")},
              "boundary": "Exploratory commissioning. Retain honest learning; no factory edits, release or efficacy claim."}
    with lock(root):
        for role, profile in (("factory-learner", "factory"), ("factory-learning-reviewer", "external")):
            task = {"schema_version": 2, "role": role, "style": "",
                    "contract": (repo / "loop/prompts" / (role + ".md")).read_text(), "inputs": inputs}
            path = root / (role + ".json")
            seal(root / (role + "-task.json"), task)
            if path.exists():
                saved = unseal(path)
                require(saved["task_sha256"] == digest(task), "Learning evidence is stale")
            else:
                output, metadata = execute(task, run.config, allow_paid, profile, root / "requests", new_attempt)
                validate_identity(metadata, run.config, profile)
                validate_learning(role, output)
                saved = {"task_sha256": digest(task), "output": output, "metadata": metadata}
                seal(path, saved)
            validate_identity(saved["metadata"], run.config, profile)
            require(run.manifest["fixture"] or saved["metadata"]["harness"] != "fixture",
                    "Synthetic learning cannot enter a live cycle")
            validate_learning(role, saved["output"])
            if role == "factory-learner":
                inputs = {**inputs, "learner_proposal": saved["output"]}
        return {"status": "LEARNING_RETAINED", "iteration": iteration,
                "review": saved["output"]["verdict"], "path": str(root),
                "review_sha256": file_hash(path)}
