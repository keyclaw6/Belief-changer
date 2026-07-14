"""Compute hard checks and judge reward; RF-02 scores carry a gate receipt."""
import argparse
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "eval"))
sys.path.insert(0, str(HERE.parent))
import loopcfg  # noqa: E402
import judges  # noqa: E402
import legacy_guard as LG  # noqa: E402
import candidate_pair as CP  # noqa: E402
import score_core  # noqa: E402
import score_receipt  # noqa: E402
import pair_store as PS  # noqa: E402
import score_report  # noqa: E402

_report = score_report.report


def _payload(cfg, a, core, aggregate, missing, pair_hash):
    status = "WAITING-FOR-VERDICTS" if missing else "SCORED"
    return {
        "campaign": cfg.get("campaign"), "instrument_version": cfg.get("instrument_version"),
        "tested_pair_hash": pair_hash,
        "book": a.book if not a.control_ref else "CONTROL:reference-as-ours",
        "chapters_checked": core["chapters_checked"], "control_ref": a.control_ref,
        "reward": aggregate["reward"] if aggregate else None,
        "hard_ok": core["hard_ok"], "hard_fails": core["hard_fails"],
        "checks": core["checks"], "diagnostics": core["diagnostics"],
        "judges": {"status": status, "rubric": aggregate, "missing": missing},
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--book")
    ap.add_argument("--chapters", default="1-3")
    ap.add_argument("--iter", type=int)
    ap.add_argument("--config", default=None)
    ap.add_argument("--tested-pair-hash")
    ap.add_argument("--control-ref", action="store_true")
    LG.add_arguments(ap)
    a = ap.parse_args()
    candidate = LG.require_authorized(a, entrypoint="score.py")
    pair_mode = os.path.lexists(candidate / CP.MANIFEST)
    if pair_mode:
        if not a.tested_pair_hash:
            ap.error("sealed pair scoring requires --tested-pair-hash")
        try:
            view = CP.open_sealed(candidate, a.tested_pair_hash)
            manifest, cfg = view["manifest"], view["config"]
            config_path = Path(a.config) if a.config else view["pair"] / manifest["run"]["config"]
            LG.require_targets(candidate, config_path)
            CP.require_member(candidate, config_path, "config", manifest)
            CP.assert_run(candidate, manifest, a.book, a.chapters, a.iter, config_path)
            if CP._chapters(a.chapters) != manifest["run"]["chapters"]:
                raise CP.PairError("chapter selection differs from sealed run contract")
            expected_book = view["pair"] / manifest["run"]["book"]
            if not a.control_ref and Path(a.book).absolute() != expected_book:
                raise CP.PairError("--book is not the sealed product root")
        except CP.PairError as exc:
            raise SystemExit(f"score: sealed pair rejected: {exc}") from exc
    else:
        if a.tested_pair_hash:
            ap.error("--tested-pair-hash requires an RF-02 manifest")
        config_path = Path(a.config) if a.config else loopcfg.find_config()
        LG.require_targets(candidate, config_path)
        manifest, view, cfg = None, None, loopcfg.load(config_path)
    LG.require_config_targets(candidate, cfg, "scores_dir", "tasks_dir")
    if not a.control_ref:
        LG.require_targets(candidate, Path(a.book), Path(a.book) / "chapters",
                           Path(a.book) / "master-plan.md")
    if LG.dry_run(a, "score.py"):
        return
    core = score_core.evaluate(cfg, a.book, a.chapters, a.control_ref)
    labels = [pair[0] for pair in core["pairs"]]
    iter_name = f"{a.iter:03d}" if a.iter is not None else "adhoc"
    rubric_path = Path(cfg["judge_rubric"])
    if pair_mode:
        rubric_path = PS._safe_file(rubric_path, view["evaluation"])
    rubric = rubric_path.read_text(encoding="utf-8")
    missing = judges.missing_verdicts(cfg, labels, iter_name, a.tested_pair_hash,
                                      candidate if pair_mode else None)
    if missing:
        judges.emit_tasks(cfg, core["pairs"], iter_name, rubric, candidate,
                          a.tested_pair_hash)
        aggregate = None
    else:
        aggregate = judges.aggregate(cfg, labels, iter_name, a.tested_pair_hash,
                                     candidate if pair_mode else None)
    payload = _payload(cfg, a, core, aggregate, missing, a.tested_pair_hash)
    if pair_mode and aggregate:
        artifacts = score_receipt.judge_artifacts(
            cfg, labels, iter_name, a.tested_pair_hash, candidate)
        core.update(pair_root=view["pair"], evaluation_root=view["evaluation"],
                    rubric_sha256=PS.sha(rubric_path.read_bytes()))
        payload["receipt"] = score_receipt.build(manifest, core, aggregate, artifacts)
    _report(payload)
    scores = Path(cfg["scores_dir"])
    LG.require_output(candidate, scores)
    scores.mkdir(parents=True, exist_ok=True)
    name = f"iter-{a.iter:03d}.json" if a.iter is not None else "iter-adhoc.json"
    output = LG.require_output(candidate, scores / name)
    output.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    print(f"[score] wrote {output}")
    sys.exit(3 if missing else 0)


if __name__ == "__main__":
    main()
