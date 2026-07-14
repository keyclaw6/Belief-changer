"""Decide one sealed iteration and atomically preserve its accepted history."""
import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import loopcfg  # noqa: E402
import legacy_guard as LG  # noqa: E402
import candidate_pair as CP  # noqa: E402
import gate_decision as GD  # noqa: E402
import judges  # noqa: E402
import score_core  # noqa: E402
import score_receipt  # noqa: E402
import pair_store as PS  # noqa: E402

COLUMNS = ["iter", "timestamp_utc", "campaign", "instrument", "hypothesis",
           "reward", "hard_ok", "verdict", "worst_dimension", "top_suggestion",
           "notes", "tested_pair_hash"]
ACCEPTED = {"BASELINE", "NEW-BEST", "KEEP"}


def read_rows(tsv: Path):
    lines = tsv.read_text(encoding="utf-8").splitlines() if tsv.is_file() else []
    if not lines:
        return []
    header = lines[0].split("\t")
    return [dict(zip(header, ln.split("\t"))) for ln in lines[1:] if ln.strip()]


def best_accepted(rows):
    best, best_iter = None, None
    for row in rows:
        if row.get("verdict") in ACCEPTED:
            try:
                r = float(row["reward"])
            except (KeyError, ValueError):
                continue
            if best is None or r > best:
                best, best_iter = r, row.get("iter")
    return best, best_iter


def _clean(text, limit=110):
    s = " ".join(("" if text is None else str(text)).split())
    return s[:limit]


def append_row(tsv: Path, row: dict, candidate: Path):
    exists = tsv.is_file() and tsv.read_text(encoding="utf-8").strip()
    LG.require_output(candidate, tsv)
    with tsv.open("a", encoding="utf-8") as fh:
        if not exists:
            fh.write("\t".join(COLUMNS) + "\n")
        fh.write("\t".join(_clean(row.get(c, ""), 400) for c in COLUMNS) + "\n")


def find_latest_score(scores_dir: Path):
    cands = sorted(scores_dir.glob("iter-[0-9]*.json"))
    if not cands:
        raise SystemExit(f"gate: no iter-*.json in {scores_dir}; run score.py first")
    return cands[-1]


def _print_revert(iter_no, score_path, assets=None, book="", isolated=False):
    if isolated:
        print("[gate] Candidate rejected; its isolated snapshot remains as evidence.")
        return
    print("[gate] The amendment was UNCOMMITTED (PROGRAM §4) — restore the accepted state:")
    for path in (assets or []):
        print(f"        git checkout -- {path}")
    if book and not str(book).startswith("CONTROL"):
        print(f"        git checkout -- {book}/master-plan.md   # only if this "
              "iteration re-ran the plan")
    print(f"        rm {score_path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--iter", type=int, help="iteration number (else newest iter-*.json)")
    ap.add_argument("--hypothesis", default="", help="the ONE hypothesis this iteration tested")
    ap.add_argument("--asset", default="", help="comma-separated path(s) this iteration amended "
                    "(sharpens the printed revert commands)")
    ap.add_argument("--config", default=None)
    ap.add_argument("--tested-pair-hash", help="sealed config+product hash evaluated by gates")
    ap.add_argument("--promote-pair", action="store_true",
                    help="human-approved atomic promotion when the gate accepts")
    ap.add_argument("--accepted-root",
                    help="accepted tree root; required with --tested-pair-hash")
    ap.add_argument("--decision-timestamp",
                    help="pinned UTC timestamp; required for resumable sealed-pair gating")
    LG.add_arguments(ap)
    a = ap.parse_args()

    candidate = LG.require_authorized(a, entrypoint="gate.py")
    pair_mode = os.path.lexists(candidate / CP.MANIFEST)
    if pair_mode:
        if not a.tested_pair_hash:
            ap.error("sealed pair gating requires --tested-pair-hash")
        try:
            view = CP.pending_sealed(candidate, a.tested_pair_hash)
            manifest, cfg = view["manifest"], view["config"]
            config_path = Path(a.config) if a.config else view["pair"] / manifest["run"]["config"]
            LG.require_targets(candidate, config_path)
            CP.require_member(candidate, config_path, "config", manifest)
            if a.iter != manifest["run"]["iteration_id"] or config_path.absolute() != (
                    view["pair"] / manifest["run"]["config"]):
                raise CP.PairError("gate CLI differs from canonical sealed run identity")
        except CP.PairError as exc:
            raise SystemExit(f"gate: sealed pair rejected: {exc}") from exc
    else:
        if a.tested_pair_hash:
            ap.error("--tested-pair-hash requires an RF-02 manifest")
        config_path = Path(a.config) if a.config else loopcfg.find_config()
        LG.require_targets(candidate, config_path)
        cfg = loopcfg.load(config_path)
    LG.require_config_targets(candidate, cfg, "scores_dir", "results_tsv")
    scores_dir = Path(cfg["scores_dir"])
    tsv = Path(cfg["results_tsv"])
    epsilon = float(cfg["epsilon"])

    score_path = (scores_dir / f"iter-{a.iter:03d}.json") if a.iter is not None \
        else find_latest_score(scores_dir)
    LG.require_targets(candidate, score_path)
    if not score_path.is_file():
        raise SystemExit(f"gate: score file not found: {score_path}")
    score = json.loads(score_path.read_text(encoding="utf-8"))
    if pair_mode and score.get("tested_pair_hash") != a.tested_pair_hash:
        raise SystemExit("gate: score artifact belongs to a different sealed pair")
    iter_no = a.iter if a.iter is not None else score_path.stem.split("-")[-1]

    assets = [s.strip() for s in a.asset.split(",") if s.strip()] or None
    book = str(view["pair"] / manifest["run"]["book"]) if pair_mode \
        else score.get("book") or ""
    if assets:
        LG.require_targets(candidate, *assets)
    if book and not str(book).startswith("CONTROL"):
        book_target = Path(book)
        LG.require_targets(candidate, book_target, book_target / "chapters",
                           book_target / "master-plan.md")
    if LG.dry_run(a, "gate.py"):
        return
    if a.promote_pair and not a.tested_pair_hash:
        ap.error("--promote-pair requires --tested-pair-hash")
    if a.tested_pair_hash and not a.accepted_root:
        ap.error("--tested-pair-hash requires --accepted-root")
    if pair_mode and not a.decision_timestamp:
        ap.error("sealed pair gating requires --decision-timestamp")
    if pair_mode:
        chapters = ",".join(str(n) for n in manifest["run"]["chapters"])
        core = score_core.evaluate(cfg, book, chapters, False)
        labels = [pair[0] for pair in core["pairs"]]
        iter_name = f"{a.iter:03d}" if a.iter is not None else "adhoc"
        aggregate = judges.aggregate(cfg, labels, iter_name, a.tested_pair_hash, candidate)
        artifacts = score_receipt.judge_artifacts(
            cfg, labels, iter_name, a.tested_pair_hash, candidate)
        core.update(pair_root=view["pair"], evaluation_root=view["evaluation"],
                    rubric_sha256=PS.sha(PS._safe_file(
                        cfg["judge_rubric"], view["evaluation"]).read_bytes()))
        expected = score_receipt.build(manifest, core, aggregate, artifacts)
        score_receipt.verify(score.get("receipt"), expected)
        if (score.get("hard_ok"), score.get("hard_fails"), score.get("reward")) != (
                core["hard_ok"], core["hard_fails"], aggregate["reward"]):
            raise SystemExit("gate: score decision fields do not match recomputed inputs")
        hard_ok, reward = core["hard_ok"], aggregate["reward"]
        hard_fails, rub = core["hard_fails"], aggregate
    else:
        hard_ok, reward = bool(score.get("hard_ok")), score.get("reward")
        hard_fails = score.get("hard_fails", [])
        rub = ((score.get("judges") or {}).get("rubric") or {})
    worst = (rub.get("worst_dimensions") or [{}])[0].get("dimension", "")
    top_sugg = (rub.get("suggestions") or [{}])[0].get("suggestion", "")

    history = Path(cfg.get("history_results_tsv", tsv))
    rows = read_rows(history)
    best, best_iter = best_accepted(rows)

    campaign = cfg.get("campaign") if pair_mode else score.get("campaign")
    instrument = cfg.get("instrument_version") if pair_mode else score.get("instrument_version")
    print(f"[gate] iter={iter_no} campaign={campaign} instrument={instrument}")
    print(f"[gate] hard_checks={'PASS' if hard_ok else 'FAIL'} "
          f"({len(hard_fails)} failures)")
    for f in hard_fails:
        print(f"        - {f}")
    print(f"[gate] reward={reward}  best_accepted={best}"
          + (f" (iter {best_iter})" if best_iter else "") + f"  epsilon={epsilon}")

    if reward is None:
        print("[gate] NO-DECISION — reward is null (judge verdicts missing). Dispatch the "
              "task files as fresh native Sol subagents, save the verdicts, re-run "
              "score.py, then re-gate. No row appended.")
        sys.exit(2)
    if not hard_ok:
        verdict = "FAIL-HARD"
        action = "Reject the candidate." if a.tested_pair_hash else "Revert the amendment."
        print(f"[gate] FAIL-HARD — hard checks failed; reward not consulted. {action}")
        _print_revert(iter_no, score_path, assets, book, bool(a.tested_pair_hash))
    elif best is None:
        verdict = "BASELINE"
        print("[gate] BASELINE — first scored iteration; accepted as the starting point.")
    elif reward > best:
        verdict = "NEW-BEST"
        print(f"[gate] NEW-BEST — reward {reward} > best {best}. Keep the amendment.")
    elif reward >= best - epsilon:
        verdict = "KEEP"
        print(f"[gate] KEEP — reward {reward} within epsilon {epsilon} of best {best}. "
              "Amendment stays; best unchanged.")
    else:
        verdict = "REVERT"
        print(f"[gate] REVERT — reward {reward} < best {best} - epsilon {epsilon}.")
        _print_revert(iter_no, score_path, assets, book, bool(a.tested_pair_hash))

    row = {"iter": iter_no,
           "campaign": campaign or "",
           "instrument": instrument or "",
           "hypothesis": a.hypothesis, "reward": reward, "hard_ok": hard_ok,
           "verdict": verdict, "worst_dimension": worst,
           "top_suggestion": _clean(top_sugg),
           "notes": Path(book).name or book,
           "tested_pair_hash": a.tested_pair_hash or ""}
    if pair_mode:
        if verdict in ACCEPTED and not a.promote_pair:
            raise SystemExit("gate: accepted pair lacks explicit human promotion approval")
        try:
            gate_receipt, history_bytes = GD.ensure(
                candidate, manifest, expected, history, row, COLUMNS, epsilon,
                best, best_iter, verdict, a.promote_pair, a.decision_timestamp)
            CP.verify_sealed(candidate, a.tested_pair_hash)
        except (GD.DecisionError, CP.PairError) as exc:
            raise SystemExit(f"gate: canonical decision rejected: {exc}") from exc
        row = gate_receipt["row"]
        LG.require_output(candidate, tsv)
        if tsv.exists() and tsv.read_bytes() != history_bytes:
            raise SystemExit("gate: existing experiment history differs from recomputed row")
        if not tsv.exists():
            PS.write(tsv, history_bytes)
    else:
        row["timestamp_utc"] = dt.datetime.now(dt.timezone.utc).isoformat(
            timespec="seconds")
    if a.tested_pair_hash:
        try:
            if verdict in ACCEPTED:
                CP.promote(candidate, Path(a.accepted_root), a.tested_pair_hash,
                           history_bytes)
                print(f"[gate] promoted exact tested pair {a.tested_pair_hash}")
            else:
                CP.reject(candidate, a.tested_pair_hash)
        except CP.PairError as exc:
            raise SystemExit(f"gate: pair decision failed closed: {exc}") from exc
    if not pair_mode:
        append_row(tsv, row, candidate)
    print(f"[gate] appended {verdict} row to {tsv}")
    sys.exit(0)  # decided = 0, always; the verdict is the row, not the exit code


if __name__ == "__main__":
    main()
