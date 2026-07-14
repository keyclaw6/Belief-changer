"""Deterministic RF-02 judge inventory and gate receipt."""
import json
from pathlib import Path

import judges
import pair_store as PS


def judge_artifacts(cfg, labels, iter_name, pair_hash, candidate):
    base = judges.judging_dir(cfg, iter_name)
    tasks, verdicts = base / "tasks", base / "verdicts"
    PS.safe_dir(tasks, candidate)
    PS.safe_dir(verdicts, candidate)
    stems = judges._stems(labels, int(cfg.get("judge_k", 2)))
    expected_tasks = {f"{stem}.md" for stem in stems}
    expected_verdicts = {f"{stem}.json" for stem in stems}
    actual_tasks = {path.name for path in tasks.iterdir()} if tasks.is_dir() else set()
    actual_verdicts = {path.name for path in verdicts.iterdir()} if verdicts.is_dir() else set()
    if actual_tasks != expected_tasks or actual_verdicts != expected_verdicts:
        raise SystemExit(
            "judges: exact artifact inventory mismatch; "
            f"tasks missing={sorted(expected_tasks-actual_tasks)} extra={sorted(actual_tasks-expected_tasks)}; "
            f"verdicts missing={sorted(expected_verdicts-actual_verdicts)} "
            f"extra={sorted(actual_verdicts-expected_verdicts)}")
    out = []
    for stem in stems:
        task, verdict = tasks / f"{stem}.md", verdicts / f"{stem}.json"
        task_hash = judges._task_binding(task, pair_hash, candidate)
        judges._parse_verdict(verdict, pair_hash, task_hash, candidate)
        out.append({"stem": stem, "task_body_sha256": task_hash,
                    "task_file_sha256": PS.sha(task.read_bytes()),
                    "verdict_sha256": PS.sha(verdict.read_bytes())})
    return out


def build(manifest, core, aggregate, artifacts):
    body = {
        "schema": 1, "tested_pair_hash": manifest["tested_hash"],
        "pair_hash": manifest["sealed"]["pair_hash"],
        "evaluation_hash": manifest["sealed"]["evaluation_hash"],
        "run": manifest["run"],
        "pair_inputs": [{"path": item["path"], "sha256": item.get("sha256")
                         or item.get("accepted_sha256")} for item in
                        PS.exact_tree(Path(core["pair_root"]), manifest["entries"])],
        "evaluation_inputs": [{"path": item["path"], "sha256": item.get("sha256")
                               or item.get("accepted_sha256")} for item in
                              PS.exact_tree(Path(core["evaluation_root"]),
                                            manifest["evaluation"])],
        "judge_artifacts": artifacts,
        "aggregate": {"chapters_checked": core["chapters_checked"],
                      "hard_ok": core["hard_ok"], "hard_fails": core["hard_fails"],
                      "checks_sha256": PS.state_hash(core["checks"]),
                      "reward": aggregate["reward"],
                      "rubric_sha256": core["rubric_sha256"],
                      "aggregate_sha256": PS.state_hash(aggregate),
                      "n_verdicts": aggregate["n_verdicts"]},
    }
    return {**body, "receipt_hash": PS.state_hash(body)}


def verify(stored, expected):
    if not isinstance(stored, dict) or stored != expected:
        raise SystemExit("gate: score receipt is missing, stale, or does not recompute")
    body = {key: value for key, value in stored.items() if key != "receipt_hash"}
    if stored.get("receipt_hash") != PS.state_hash(body):
        raise SystemExit("gate: score receipt hash is invalid")


def result_history(history, row, columns):
    lines = Path(history).read_text(encoding="utf-8").splitlines() \
        if Path(history).is_file() else []
    old_header = lines[0].split("\t") if lines else []
    rows = [dict(zip(old_header, line.split("\t"))) for line in lines[1:] if line.strip()]
    rows.append(row)
    clean = lambda value: " ".join(str(value if value is not None else "").split())[:400]
    text = ["\t".join(columns)]
    text.extend("\t".join(clean(item.get(column, "")) for column in columns)
                for item in rows)
    return ("\n".join(text) + "\n").encode()


def row_bytes(row, columns):
    clean = lambda value: " ".join(str(value if value is not None else "").split())[:400]
    return ("\t".join(clean(row.get(column, "")) for column in columns) + "\n").encode()
