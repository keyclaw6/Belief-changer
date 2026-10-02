"""A thin lifecycle surface over the installed durable host controller.

The host agent reasons about experiments. This module owns only the declared
boundary, stop intent and native process receipt; verified artifacts own results.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

from bc_factory.common import FactoryError, atomic_bytes, atomic_json, digest, file_hash, identifier, read_json, require, lock
from bc_factory.runs import Run


def campaign(repo: Path, path: Path | None = None, *, validate: bool = True) -> tuple[Path, dict]:
    path = (path or repo / "loop/commissioning.json").resolve()
    require(path.is_relative_to(repo.resolve()), "Campaign record must be in this repository")
    data = read_json(path)
    identifier(data["id"])
    if not validate:
        # Stop needs the owned job identity, not valid scientific scope/evidence.
        return path, data
    require(data["execution_status"] in ("ACTIVE", "STOPPED", "COMPLETE"), "Invalid campaign state")
    require(data["authorization"]["reference"] and data["authorization"]["quote"],
            "Campaign needs its actual human authorization source")
    iterations = data["iterations"]
    require(isinstance(iterations, list) and iterations and len(iterations) == len(set(iterations)),
            "Campaign needs a fixed list of independent cycles")
    for iteration in iterations:
        identifier(iteration)
    require(data["authorization"]["scope_sha256"] == digest({"iterations": iterations, "plan": data["plan"]}),
            "Campaign scope changed; reconcile actual owner authority before execution")
    return path, data


def freeze_iteration(repo: Path, iteration: str, hypothesis: Path, path: Path | None = None) -> dict:
    """Freeze the host's reasoning in the existing handoff, without inventing it."""
    from .operations import progress_record, scope_digest
    _, data = campaign(repo, path)
    validate_checkpoints(repo, data)
    completed = data.get("completed", [])
    require(data["execution_status"] == "ACTIVE" and len(completed) < len(data["iterations"])
            and data["iterations"][len(completed)] == iteration, "Freeze only the next authorized cycle")
    content = hypothesis.read_bytes()
    require(bool(content.strip()), "Host hypothesis/declared measurement must be substantive")
    root = repo / "loop/iterations" / identifier(iteration)
    with lock(root):
        if (root / "progress.json").exists():
            require((root / "hypothesis.md").read_bytes() == content, "Frozen hypothesis cannot be overwritten")
            return progress_record(repo, iteration)
        atomic_bytes(root / "hypothesis.md", content)
        progress = {"schema_version": 1, "iteration": iteration, "status": "IN_PROGRESS",
                    "preregistration_sha256": file_hash(root / "hypothesis.md"), "execution_status": "ACTIVE",
                    "allocation": {data["plan"]["subject"]: data["plan"]["books_per_cycle"]},
                    "excluded_runs": [], "runs": [],
                    "authorization": {"status": "APPROVED", "reference": data["authorization"]["reference"],
                                      "quote": data["authorization"]["quote"]},
                    "next_action": "Launch the one declared new book through Pi"}
        progress["authorization"]["scope_sha256"] = scope_digest(progress)
        atomic_json(root / "progress.json", progress)
        return progress_record(repo, iteration)


def checkpoint(repo: Path, iteration: str, run_id: str, baseline: str, path: Path | None = None) -> dict:
    from . import regression, operations
    path, data = campaign(repo, path)
    require(data["execution_status"] == "ACTIVE", "Stopped/completed campaign cannot advance")
    completed = data.get("completed", [])
    require(len(completed) < len(data["iterations"]) and data["iterations"][len(completed)] == iteration,
            "Checkpoint must be the next authorized independent cycle")
    run = Run(repo, run_id)
    prior = Run(repo, baseline)
    require(not run.manifest["fixture"] and not prior.manifest["fixture"],
            "Commissioning requires real complete books, not synthetic fixture cycles")
    progress = operations.progress_record(repo, iteration, for_launch=True)
    books = operations._allocated_runs(repo, iteration, progress)
    require(run_id in books and len(books) == 1 and sum(progress["allocation"].values()) == 1,
            "Commissioning cycle must contain its one declared logical book")
    complete = run.complete()
    require(complete["book_sha256"] not in {c["book_sha256"] for c in completed},
            "A retained book cannot count as another independent cycle")
    decision = regression.decide(repo, run_id, baseline)
    require(not decision.get("missing"), "Both actual blinded comparisons must be retained")
    learning_root = repo / "loop/iterations" / iteration / "learning"
    from .evaluation import learn
    # Replay proves current books/judgments still bind both retained learning tasks.
    learn(repo, iteration, run_id, baseline)
    record = {"iteration": iteration, "run_id": run_id, "baseline_run": baseline,
              "book_sha256": complete["book_sha256"],
              "decision": decision["decision"], "decision_sha256": digest(decision),
              "learner_sha256": file_hash(learning_root / "factory-learner.json"),
              "review_sha256": file_hash(learning_root / "factory-learning-reviewer.json")}
    with lock(repo / ".loop-work/controller"):
        path, data = campaign(repo, path)
        require(data["execution_status"] == "ACTIVE" and data.get("completed", []) == completed,
                "Campaign changed during checkpoint; reconcile before proceeding")
        data["completed"] = [*completed, record]
        data["execution_status"] = "COMPLETE" if len(data["completed"]) == len(data["iterations"]) else "ACTIVE"
        data["next_action"] = ("Boundary reached; no further work authorized" if data["execution_status"] == "COMPLETE"
                               else "Read retained learning, freeze the next permitted hypothesis and run its new book")
        atomic_json(path, data)
    return record


def validate_checkpoints(repo: Path, data: dict) -> None:
    from . import regression, evaluation
    completed = data.get("completed", [])
    require(len(completed) <= len(data["iterations"]), "Completed cycles exceed the authorized boundary")
    for index, record in enumerate(completed):
        require(record["iteration"] == data["iterations"][index], "Campaign checkpoint order changed")
        run = Run(repo, record["run_id"])
        require(run.complete()["book_sha256"] == record["book_sha256"], "Checkpoint book evidence changed")
        decision = regression.decide(repo, record["run_id"], record["baseline_run"])
        require(digest(decision) == record["decision_sha256"], "Checkpoint decision evidence changed")
        evaluation.learn(repo, record["iteration"], record["run_id"], record["baseline_run"])
        root = repo / "loop/iterations" / record["iteration"] / "learning"
        require(file_hash(root / "factory-learner.json") == record["learner_sha256"] and
                file_hash(root / "factory-learning-reviewer.json") == record["review_sha256"],
                "Checkpoint learning evidence changed")
    require(data["execution_status"] != "COMPLETE" or len(completed) == len(data["iterations"]),
            "Completion label is missing its actual cycle evidence")


def deployment(repo: Path) -> dict:
    """Local paths are setup, never scientific authority or credential values."""
    path = repo / ".loop-work/deployment.json"
    if path.is_file():
        return read_json(path)
    pi = shutil.which("pi")
    # mise's concrete executable avoids the host shim's global-config mutation.
    mise = shutil.which("mise")
    if mise:
        result = subprocess.run([mise, "which", "pi"], capture_output=True, text=True, check=False)
        if result.returncode == 0:
            pi = result.stdout.strip()
    require(bool(pi), "Install/configure the provisioned Pi executable")
    data = {"pi": str(Path(pi).resolve()),
            "agent_dir": str(Path.home() / ".local/share/belief-changer/pi-runtime"),
            "env_file": str(Path.home() / ".config/belief-changer-go.env"),
            "controller": shutil.which("opencode-rdc"),
            "outer_model": os.environ.get("BC_OUTER_MODEL", "gpt-6.1-sol")}
    require(bool(data["controller"]), "Install/configure the existing durable host controller")
    atomic_json(path, data)
    return data


def native(settings: dict, *args: str) -> dict:
    result = subprocess.run([settings["controller"], *args], capture_output=True, text=True, check=False)
    require(result.returncode == 0, "Native controller command failed; inspect the same job receipt")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise FactoryError("Native controller returned an invalid receipt") from exc


def status(repo: Path, path: Path | None = None) -> dict:
    path, data = campaign(repo, path, validate=False)
    try:
        campaign(repo, path)
        validate_checkpoints(repo, data)
        evidence = {"status": "VALIDATED"}
    except (FactoryError, OSError) as exc:
        from bc_factory.research_access import safe_error
        evidence = {"status": "INVALID", "error": safe_error(exc)}
    job = "belief-changer-" + data["id"]
    settings = deployment(repo)
    receipt = native(settings, "status", job) if data.get("controller_started") else None
    return {"campaign": data["id"], "execution_status": data["execution_status"],
            "record": str(path), "iterations": data["iterations"],
            "completed": data.get("completed", []), "owner": receipt, "evidence": evidence,
            "next_action": data.get("next_action", "Start or resume the outer controller")}


def lifecycle(repo: Path, action: str, path: Path | None = None) -> dict:
    path, _ = campaign(repo, path, validate=action != "stop")
    with lock(repo / ".loop-work/controller"):
        path, data = campaign(repo, path, validate=action != "stop")
        job = "belief-changer-" + data["id"]
        if action == "stop":
            # Persist intent before cancellation; reconnection cannot restart it.
            if data["execution_status"] != "COMPLETE":
                data["execution_status"] = "STOPPED"
                data["next_action"] = "Explicit resume preserves accepted work"
            atomic_json(path, data)
            settings = deployment(repo)
            receipt = native(settings, "status", job) if data.get("controller_started") else None
            if receipt and (receipt.get("state") in ("running", "reserved") or
                            receipt.get("execution_state") == "unverified-active"):
                native(settings, "kill", job)
            return {"campaign": data["id"], "execution_status": data["execution_status"], "record": str(path),
                    "owner": native(settings, "status", job) if receipt else None,
                    "evidence_status": "Stop does not depend on scientific evidence validation"}
        require(action in ("start", "resume"), "Unknown lifecycle action")
        validate_checkpoints(repo, data)
        require(data["execution_status"] != "COMPLETE" and
                len(data.get("completed", [])) < len(data["iterations"]),
                "Campaign complete; no additional work authorized")
        require(action == "resume" or data["execution_status"] != "STOPPED",
                "Owner stop: use explicit resume")
        settings = deployment(repo)
        receipt = native(settings, "status", job) if data.get("controller_started") else None
        require(not receipt or receipt.get("backend") == "codex",
                "The outer owner must be the existing Codex backend, not a command or factory worker")
        if receipt and receipt.get("state") in ("running", "reserved"):
            return status(repo, path)
        require(not receipt or receipt.get("state") not in ("unknown", "conflict"),
                "Reconcile the existing native owner before resuming; do not duplicate it")
        previous_status = data["execution_status"]
        data["execution_status"] = "ACTIVE"
        data["next_action"] = "Outer owner runs the remaining authorized cycles and stops at the boundary"
        atomic_json(path, data)
        prompt = (f"Run authorized autoresearch from {path.relative_to(repo)} using "
                  "skills/running-auto-research-loop/SKILL.md. You are its single durable outer owner "
                  "and hypothesizer. Reconcile actual artifacts before acting; complete the remaining "
                  "cycles, retain independent evaluation and learning, then stop at the declared boundary. "
                  "Pi owns each complete book. Do not modify factory source/prompts/config during qualifying "
                  "work, author factory role results, change models, publish, buy anything, or resume 054. "
                  "Project-local operational diagnosis is authorized; record a concrete blocker and resume "
                  "point if the fixed path cannot continue honestly. No implementer coaching is needed.")
        try:
            if receipt:
                receipt = native(settings, "follow", job, "--request-id",
                                 f"{job}-resume-{receipt['run'] + 1}", prompt)
            else:
                receipt = native(settings, "start", job, "--backend", "codex", "--model",
                                 settings["outer_model"], "--reasoning-effort", "high", "--dir", str(repo),
                                 "--env-file", settings["env_file"], "--request-id", job + "-start", prompt)
        except (FactoryError, OSError):
            data["execution_status"] = previous_status
            data["next_action"] = f"Native dispatch failed; reconcile the same job {job} before retrying"
            atomic_json(path, data)
            raise
        require(receipt.get("survives_origin") is True,
                "Native owner is not durable on this host; reconcile its receipt before any factory work")
        data["controller_started"] = True
        atomic_json(path, data)
        return {"campaign": data["id"], "execution_status": "ACTIVE", "owner": receipt}
