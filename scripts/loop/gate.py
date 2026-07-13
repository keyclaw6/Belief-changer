"""The keep/revert gate (PROGRAM §4.3). Reads loop/scores/iter-NNN.json and the
results ledger, then decides:

  FAIL-HARD  hard checks failed — reward not consulted; revert the amendment.
  NO-DECISION  reward is null (verdicts still missing) — dispatch judges first.
  BASELINE   first scored iteration — accepted as the starting point.
  NEW-BEST   reward > best accepted so far.
  KEEP       reward >= best - epsilon (within judge noise; amendment stays).
  REVERT     reward < best - epsilon — prints the exact commands to undo the
             iteration's tunable-asset changes; the operator runs them.

Every decided verdict appends one row to loop/results.tsv and exits 0 —
the exit code means "decision made", never pass/fail; the verdict lives in
the row and stdout. Exit 2 = NO-DECISION (verdicts missing). The amendment
under test must be UNCOMMITTED (PROGRAM §4: amend -> run -> score -> gate ->
commit), so the printed `git checkout` genuinely restores the accepted state.

  python3 scripts/loop/gate.py --iter 7 --hypothesis "H-001 word budgets"
  python3 scripts/loop/gate.py            # newest iter-*.json
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import loopcfg  # noqa: E402

# Tunable assets (PROGRAM §3) — the files a REVERT may need to undo.
TUNABLE = [
    "prompts/style-guide.md",
    "prompts/chapter-writer.md",
    "prompts/chapter-reviewer.md",
    "prompts/master-plan-skill-v2.md",
    "prompts/master-plan-reviewer-v2.md",
    "prompts/research-agent.md",
    "production-books/_template/",
]

COLUMNS = ["iter", "timestamp_utc", "campaign", "instrument", "hypothesis",
           "reward", "hard_ok", "verdict", "worst_dimension", "top_suggestion",
           "notes"]
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


def append_row(tsv: Path, row: dict):
    exists = tsv.is_file() and tsv.read_text(encoding="utf-8").strip()
    with tsv.open("a", encoding="utf-8") as fh:
        if not exists:
            fh.write("\t".join(COLUMNS) + "\n")
        fh.write("\t".join(_clean(row.get(c, ""), 400) for c in COLUMNS) + "\n")


def find_latest_score(scores_dir: Path):
    cands = sorted(scores_dir.glob("iter-[0-9]*.json"))
    if not cands:
        raise SystemExit(f"gate: no iter-*.json in {scores_dir}; run score.py first")
    return cands[-1]


def _print_revert(iter_no, assets=None, book=""):
    print("[gate] The amendment was UNCOMMITTED (PROGRAM §4) — restore the accepted state:")
    for path in (assets or TUNABLE):
        print(f"        git checkout -- {path}")
    if book and not str(book).startswith("CONTROL"):
        print(f"        git checkout -- {book}/master-plan.md   # only if this "
              "iteration re-ran the plan")
    print(f"        rm loop/scores/iter-{str(iter_no).zfill(3)}.json")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--iter", type=int, help="iteration number (else newest iter-*.json)")
    ap.add_argument("--hypothesis", default="", help="the ONE hypothesis this iteration tested")
    ap.add_argument("--asset", default="", help="comma-separated path(s) this iteration amended "
                    "(sharpens the printed revert commands)")
    ap.add_argument("--config", default=None)
    a = ap.parse_args()

    cfg = loopcfg.load(a.config) if a.config else loopcfg.load(loopcfg.find_config())
    scores_dir = Path(cfg["scores_dir"])
    tsv = Path(cfg["results_tsv"])
    epsilon = float(cfg["epsilon"])

    score_path = (scores_dir / f"iter-{a.iter:03d}.json") if a.iter is not None \
        else find_latest_score(scores_dir)
    if not score_path.is_file():
        raise SystemExit(f"gate: score file not found: {score_path}")
    score = json.loads(score_path.read_text(encoding="utf-8"))
    iter_no = a.iter if a.iter is not None else score_path.stem.split("-")[-1]

    assets = [s.strip() for s in a.asset.split(",") if s.strip()] or None
    book = score.get("book") or ""
    hard_ok = bool(score.get("hard_ok"))
    reward = score.get("reward")
    judges_blk = score.get("judges") or {}
    rub = judges_blk.get("rubric") or {}
    worst = (rub.get("worst_dimensions") or [{}])[0].get("dimension", "")
    top_sugg = (rub.get("suggestions") or [{}])[0].get("suggestion", "")

    rows = read_rows(tsv)
    best, best_iter = best_accepted(rows)

    print(f"[gate] iter={iter_no} campaign={score.get('campaign')} "
          f"instrument={score.get('instrument_version')}")
    print(f"[gate] hard_checks={'PASS' if hard_ok else 'FAIL'} "
          f"({len(score.get('hard_fails', []))} failures)")
    for f in score.get("hard_fails", []):
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
        print("[gate] FAIL-HARD — hard checks failed; reward not consulted. Revert the amendment.")
        _print_revert(iter_no, assets, book)
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
        _print_revert(iter_no, assets, book)

    row = {"iter": iter_no,
           "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "campaign": score.get("campaign", ""),
           "instrument": score.get("instrument_version", ""),
           "hypothesis": a.hypothesis, "reward": reward, "hard_ok": hard_ok,
           "verdict": verdict, "worst_dimension": worst,
           "top_suggestion": _clean(top_sugg),
           "notes": Path(book).name or book}
    append_row(tsv, row)
    print(f"[gate] appended {verdict} row to {tsv}")
    sys.exit(0)  # decided = 0, always; the verdict is the row, not the exit code


if __name__ == "__main__":
    main()
