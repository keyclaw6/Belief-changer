"""Command line: explicit stage operations; no hidden continuous optimization."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from . import __version__
from .common import FactoryError, atomic_json, read_json, reply_json, require, unseal, lock, seal, digest, now
from .runs import Run, prepare
from .adapters import execute
from . import archive, experiments


def document(path: str) -> dict:
    p = Path(path)
    data = read_json(p)
    return unseal(p) if isinstance(data, dict) and set(data) == {"payload", "sha256"} else data


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Belief-Changer v2, one inspectable role/stage at a time")
    p.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="command", required=True)
    s = sub.add_parser("prepare", help="Freeze brief, research, code, prompts and config")
    s.add_argument("--run", required=True); s.add_argument("--brief", required=True); s.add_argument("--research", required=True)
    s.add_argument("--parent"); s.add_argument("--fixture", action="store_true"); s.add_argument("--research-preflight")
    s = sub.add_parser("task", help="Construct and freeze the next role's input without model calls")
    s.add_argument("--run", required=True); s.add_argument("--role", required=True)
    s.add_argument("--chapter", type=int); s.add_argument("--round", type=int, default=1); s.add_argument("--out")
    for name in ("submit", "execute"):
        s = sub.add_parser(name)
        s.add_argument("--run", required=True); s.add_argument("--task", required=True)
        if name == "submit":
            s.add_argument("--response", required=True); s.add_argument("--metadata", required=True)
        else:
            s.add_argument("--allow-paid", action="store_true")
    for name in ("status", "verify", "assemble"):
        sub.add_parser(name).add_argument("--run", required=True)
    sub.add_parser("register-experiment").add_argument("--spec", required=True)
    for name in ("pair-task", "pair-submit", "pair-execute"):
        s = sub.add_parser(name)
        s.add_argument("--experiment", required=True); s.add_argument("--pair", required=True)
        s.add_argument("--order", choices=("AB", "BA"), required=True)
        if name == "pair-task": s.add_argument("--out")
        elif name == "pair-submit":
            s.add_argument("--response", required=True); s.add_argument("--metadata", required=True)
        else: s.add_argument("--allow-paid", action="store_true")
    s = sub.add_parser("decide")
    s.add_argument("--experiment", required=True); s.add_argument("--calibration")
    s = sub.add_parser("promote")
    s.add_argument("--experiment", required=True); s.add_argument("--release", required=True)
    s.add_argument("--calibration", required=True); s.add_argument("--approval", required=True)
    sub.add_parser("archive").add_argument("--output", type=Path, required=True)
    s = sub.add_parser("demo", help="Offline two-chapter fixture pipeline, never publication evidence")
    s.add_argument("--output", type=Path, required=True)
    s = sub.add_parser("research-bootstrap", help="Plan or explicitly install pinned research tools outside the repository")
    s.add_argument("--apply", action="store_true")
    s = sub.add_parser("research-login", help="Interactive authorized login in dedicated CloakBrowser")
    s.add_argument("--allow-captcha", action="store_true")
    s = sub.add_parser("research-preflight", help="Verify tools, logins, search, threads and CAPTCHA before a campaign")
    s.add_argument("--subject", required=True); s.add_argument("--live", action="store_true")
    s.add_argument("--allow-captcha", action="store_true"); s.add_argument("--out"); s.add_argument("--probe-query")
    s = sub.add_parser("research-query", help="Read-only web/Reddit/X search or thread reading in CloakBrowser")
    s.add_argument("--subject", required=True); s.add_argument("--lane", choices=("web","reddit","x"), required=True)
    s.add_argument("--action", choices=("search","read"), required=True); s.add_argument("--value", required=True)
    s.add_argument("--limit", type=int, default=10); s.add_argument("--preflight", required=True)
    s.add_argument("--allow-captcha", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    repo = args.repo.resolve()
    try:
        cmd = args.command
        if cmd == "prepare":
            root = prepare(repo, args.run, document(args.brief), document(args.research), args.parent, args.fixture, document(args.research_preflight) if args.research_preflight else None)
            result = {"status": "FROZEN", "run": str(root)}
        elif cmd == "task":
            result = Run(repo, args.run).task(args.role, args.chapter, args.round)
        elif cmd in ("submit", "execute"):
            run, task = Run(repo, args.run), document(args.task)
            if cmd == "execute":
                # Check dependencies BEFORE spending, as well as when accepting the response.
                require(run.task(task["role"], task["chapter"], task["round"]) == task, "Stale task")
                # One provider invocation owns this unit at a time. Stale claims are never auto-stolen.
                with lock(run.root / "inflight" / task["key"]):
                    try:
                        output, meta = execute(task, run.config, args.allow_paid)
                        record = run.submit(task, output, meta)
                    except FactoryError as exc:
                        failure = {"task_digest": digest(task), "role": task["role"], "error": str(exc), "created_at": now(), "usage": None}
                        seal(run.root / "failures" / (digest(failure) + ".json"), failure)
                        raise
            else:
                output, meta = document(args.response), document(args.metadata)
                record = run.submit(task, output, meta)
            result = {"status": "RECORDED", "key": record["key"], "output_sha256": record["output_sha256"]}
        elif cmd == "status": result = Run(repo, args.run).status()
        elif cmd == "verify": result = Run(repo, args.run).complete()
        elif cmd == "assemble":
            r = Run(repo, args.run); a = r.assemble()
            result = {"status": "ASSEMBLED_UNAUDITED", "path": str(r.root / "book.md"), "sha256": a["text_sha256"]}
        elif cmd == "register-experiment": result = {"registered": str(experiments.register(repo, document(args.spec)))}
        elif cmd == "pair-task": result = experiments.pair_task(repo, args.experiment, args.pair, args.order)
        elif cmd in ("pair-submit", "pair-execute"):
            if cmd == "pair-execute":
                task = experiments.pair_task(repo, args.experiment, args.pair, args.order)
                _, reg = experiments.registration(repo, args.experiment)
                first = reg["spec"]["pairs"][0]["parent_run"]
                exp_root, _ = experiments.registration(repo, args.experiment)
                unit = f"{args.pair}-{args.order}"
                with lock(exp_root / "inflight" / unit):
                    require(not (exp_root / "judgments" / (unit + ".json")).exists(), "Judgment already recorded; no duplicate paid execution")
                    try:
                        output, meta = execute(task, Run(repo, first).config, args.allow_paid)
                        record = experiments.submit_pair(repo, args.experiment, args.pair, args.order, output, meta)
                    except FactoryError as exc:
                        failure = {"task_digest": digest(task), "role": "pairwise", "error": str(exc), "created_at": now(), "usage": None}
                        seal(exp_root / "failures" / (digest(failure) + ".json"), failure)
                        raise
            else:
                output, meta = document(args.response), document(args.metadata)
                record = experiments.submit_pair(repo, args.experiment, args.pair, args.order, output, meta)
            result = {"status": "RECORDED", "task_hash": record["task_hash"]}
        elif cmd == "decide": result = experiments.decide(repo, args.experiment, document(args.calibration) if args.calibration else None)
        elif cmd == "promote": result = {"release": str(experiments.promote(repo, args.experiment, args.release, document(args.calibration), document(args.approval)))}
        elif cmd == "research-bootstrap":
            from .research_setup import bootstrap
            result = bootstrap(repo, args.apply)
        elif cmd == "research-login":
            from .research_access import login
            result = login(repo, args.allow_captcha)
        elif cmd == "research-preflight":
            from .research_access import preflight
            result = preflight(repo, args.subject, args.live, args.allow_captcha, args.probe_query)
        elif cmd == "research-query":
            from .research_access import query
            result = query(repo,args.subject,args.lane,args.action,args.value,args.limit,document(args.preflight),args.allow_captcha)
        elif cmd == "archive": result = archive.build(repo, args.output)
        elif cmd == "demo":
            from .demo import run_demo
            result = run_demo(repo, args.output)
        else: raise FactoryError("Unknown command")
        if getattr(args, "out", None):
            atomic_json(Path(args.out), result)
            print(json.dumps({"written": str(Path(args.out).resolve())}))
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        if result.get("status") in ("INCOMPLETE", "BLOCKED") or result.get("decision") in ("INCONCLUSIVE", "REJECT"):
            return 2
        return 0
    except Exception as exc:
        from .research_access import safe_error
        print(json.dumps({"status": "ERROR", "error": safe_error(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
