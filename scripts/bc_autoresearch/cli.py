"""Outer autoresearch command line."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

from . import experiments, learning, regression, operations
from bc_factory.adapters import execute
from bc_factory.common import FactoryError, atomic_json, digest, lock, now, read_json, require, seal, unseal
from bc_factory.runs import Run


def document(path: str) -> dict:
    p = Path(path)
    data = read_json(p)
    if isinstance(data, dict) and set(data) == {"payload", "sha256"}:
        return unseal(p)
    return data

def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Belief-Changer outer autoresearch controls")
    p.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("iteration-status", help="Inspect scope and owner stop; no model calls").add_argument("--iteration", required=True)
    s = sub.add_parser("launch-book", help="Inspect or explicitly launch one prepared book in a persistent Pi PTY")
    s.add_argument("--iteration", required=True)
    s.add_argument("--run", required=True)
    s.add_argument("--agent-dir", type=Path, required=True)
    s.add_argument("--extension", type=Path, required=True)
    s.add_argument("--pi", default="pi")
    s.add_argument("--allow-paid", action="store_true")

    sub.add_parser("register-experiment").add_argument("--spec", required=True)
    for name in ("pair-task", "pair-submit", "pair-execute"):
        s = sub.add_parser(name)
        s.add_argument("--experiment", required=True)
        s.add_argument("--pair", required=True)
        s.add_argument("--order", choices=("AB", "BA"), required=True)
        if name == "pair-task":
            s.add_argument("--out")
        elif name == "pair-submit":
            s.add_argument("--response", required=True)
            s.add_argument("--metadata", required=True)
        else:
            s.add_argument("--allow-paid", action="store_true")

    s = sub.add_parser("decide")
    s.add_argument("--experiment", required=True)
    s.add_argument("--calibration")
    s = sub.add_parser("promote")
    s.add_argument("--experiment", required=True)
    s.add_argument("--release", required=True)
    s.add_argument("--calibration", required=True)
    s.add_argument("--approval", required=True)

    s = sub.add_parser("learning-seed")
    s.add_argument("--run", required=True)
    s.add_argument("--lessons", required=True)
    s = sub.add_parser("regression-task")
    s.add_argument("--run", required=True)
    s.add_argument("--baseline", required=True)
    s.add_argument("--order", choices=("AB", "BA"), required=True)
    s.add_argument("--out")

    s = sub.add_parser("regression-submit")
    s.add_argument("--run", required=True)
    s.add_argument("--baseline", required=True)
    s.add_argument("--order", choices=("AB", "BA"), required=True)
    s.add_argument("--response", required=True)
    s.add_argument("--metadata", required=True)
    s = sub.add_parser("regression-decide")
    s.add_argument("--run", required=True)
    s.add_argument("--baseline", required=True)
    s = sub.add_parser("advance-baseline")
    s.add_argument("--run", required=True)
    s.add_argument("--baseline", required=True)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    repo = args.repo.resolve()
    try:
        cmd = args.command
        if cmd == "iteration-status":
            result = operations.iteration_status(repo, args.iteration)
        elif cmd == "launch-book":
            result = operations.launch_book(repo, args.iteration, args.run,
                                           args.agent_dir, args.extension, args.pi, args.allow_paid)
        elif cmd == "register-experiment":
            result = {"registered": str(experiments.register(repo, document(args.spec)))}

        elif cmd == "pair-task":
            result = experiments.pair_task(repo, args.experiment, args.pair, args.order)
        elif cmd in ("pair-submit", "pair-execute"):
            exp_root, reg = experiments.registration(repo, args.experiment)
            pair = next((p for p in reg["spec"]["pairs"] if p["id"] == args.pair), None)
            require(pair is not None, "Unknown pair")
            unit = f"{pair['id']}-{args.order}"
            if cmd == "pair-submit":
                output, meta = document(args.response), document(args.metadata)
            # Transport recovery does not alter the registered evaluator instrument.
            # Both entry points fence the same work and recheck evidence before replay.
            with lock(exp_root / "inflight" / unit):
                task = experiments.pair_task(repo, args.experiment, args.pair, args.order)
                path = exp_root / "judgments" / (unit + ".json")
                if path.exists():
                    record = unseal(path)
                    task_record = unseal(exp_root / "tasks" / (unit + ".json"))
                    require(record["task_hash"] == digest(task_record), "Judgment has stale task inputs")
                    if cmd == "pair-submit":
                        require(digest(record["output"]) == digest(output) and
                                digest(record["metadata"]) == digest(meta),
                                "Recorded judgment differs from supplied response/metadata; it is immutable")
                elif cmd == "pair-execute":
                    try:
                        output, meta = execute(task, Run(repo, pair["parent_run"]).config,
                                               args.allow_paid, profile_name="external")
                        record = experiments.submit_pair(repo, args.experiment, args.pair, args.order, output, meta)
                    except FactoryError as exc:
                        failure = {"task_digest": digest(task), "role": "pairwise", "error": str(exc),
                                   "created_at": now(), "usage": None}
                        seal(exp_root / "failures" / (digest(failure) + ".json"), failure)
                        raise
                else:
                    record = experiments.submit_pair(repo, args.experiment, args.pair, args.order, output, meta)
            result = {"status": "RECORDED", "task_hash": record["task_hash"]}
        elif cmd == "decide":
            result = experiments.decide(
                repo, args.experiment,
                document(args.calibration) if args.calibration else None,
            )
        elif cmd == "promote":
            result = {"release": str(experiments.promote(
                repo, args.experiment, args.release,
                document(args.calibration), document(args.approval),
            ))}

        elif cmd == "learning-seed":
            result = learning.seed(repo, args.run, document(args.lessons))
        elif cmd == "regression-task":
            result = regression.task(repo, args.run, args.baseline, args.order)
        elif cmd == "regression-submit":
            record = regression.submit(
                repo, args.run, args.baseline, args.order,
                document(args.response), document(args.metadata),
            )
            result = {"status": "RECORDED", "task_hash": record["task_hash"]}
        elif cmd == "regression-decide":
            result = regression.decide(repo, args.run, args.baseline)
        elif cmd == "advance-baseline":
            result = learning.advance(repo, args.run, args.baseline)
        else:
            raise FactoryError("Unknown autoresearch command")

        if getattr(args, "out", None):
            atomic_json(Path(args.out), result)
            print(json.dumps({"written": str(Path(args.out).resolve())}))
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        if result.get("status") == "NEEDS_INSPECTION" or result.get("decision") in ("INCONCLUSIVE", "REJECT", "REPAIR_REQUIRED"):
            return 2
        return 0
    except Exception as exc:
        from bc_factory.research_access import safe_error
        print(json.dumps({"status": "ERROR", "error": safe_error(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
