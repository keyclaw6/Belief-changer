"""The keep/revert gate. Reads the last ACCEPTED reward from loop/results.tsv
and the new loop/scores/iter-NNN.json, then decides:

  ACCEPT iff all hard checks pass AND (reward >= last_accepted + epsilon OR
         this is the first iteration).
  REVERT otherwise — prints the EXACT `git checkout` commands to undo this
         iteration's tunable-asset changes; the operator runs them.

Either way, appends one verdict row to results.tsv so the ledger is complete.

  python3 scripts/loop/gate.py --iter 7 --hypothesis "H-001 word budgets"
  python3 scripts/loop/gate.py            # newest iter-*.json

DRY-RUN scores (reward=null, no judge key) CANNOT be accepted on reward: the
gate reports NO-DECISION (exit 2). Hard-check blockers still print.
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import loopcfg  # noqa: E402

# Tunable assets the loop may edit between iterations (PROGRAM.md "tunable
# surface"); on REVERT these are the files the iteration could own.
TUNABLE = [
    "prompts/style-guide.md",
    "prompts/chapter-writer.md",
    "prompts/chapter-reviewer.md",
]

COLUMNS = ["iter", "timestamp_utc", "campaign", "instrument", "hypothesis",
           "reward", "detection_acc", "hard_ok", "verdict", "notes"]


def read_rows(tsv: Path):
    lines = tsv.read_text(encoding="utf-8").splitlines() if tsv.is_file() else []
    if not lines:
        return []
    header = lines[0].split("\t")
    return [dict(zip(header, ln.split("\t"))) for ln in lines[1:] if ln.strip()]


def last_accepted_reward(rows):
    for row in reversed(rows):
        if row.get("verdict") == "ACCEPT":
            try:
                return float(row["reward"]), row["iter"]
            except (KeyError, ValueError):
                continue
    return None, None


def append_row(tsv: Path, row: dict):
    exists = tsv.is_file() and tsv.read_text(encoding="utf-8").strip()
    with tsv.open("a", encoding="utf-8") as fh:
        if not exists:
            fh.write("\t".join(COLUMNS) + "\n")
        fh.write("\t".join(str(row.get(c, "")) for c in COLUMNS) + "\n")


def find_latest_score(scores_dir: Path):
    cands = sorted(scores_dir.glob("iter-[0-9]*.json"))
    if not cands:
        raise SystemExit(f"gate: no iter-*.json in {scores_dir}; run score.py first")
    return cands[-1]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--iter", type=int, help="iteration number (else newest iter-*.json)")
    ap.add_argument("--hypothesis", default="", help="the ONE hypothesis this iteration tested")
    ap.add_argument("--config", default=None)
    a = ap.parse_args()

    cfg = loopcfg.load(a.config) if a.config else loopcfg.load(loopcfg.find_config())
    scores_dir = Path(cfg["scores_dir"])
    tsv = Path(cfg["results_tsv"])
    epsilon = float(cfg["epsilon"])

    score_path = (scores_dir / f"iter-{a.iter:03d}.json") if a.iter is not None else find_latest_score(scores_dir)
    if not score_path.is_file():
        raise SystemExit(f"gate: score file not found: {score_path}")
    score = json.loads(score_path.read_text(encoding="utf-8"))
    iter_no = a.iter if a.iter is not None else score_path.stem.split("-")[-1]

    rows = read_rows(tsv)
    last_reward, last_iter = last_accepted_reward(rows)
    first_iter = last_reward is None
    hard_ok = bool(score.get("hard_ok"))
    reward = score.get("reward")
    dry_run = score.get("judges", {}).get("pairwise", {}).get("dry_run", reward is None)
    probe = score.get("judges", {}).get("detection_probe", {})
    det = probe.get("detection_accuracy")

    print(f"[gate] iter={iter_no} campaign={score.get('campaign')} "
          f"instrument={score.get('instrument_version')}")
    print(f"[gate] hard_checks={'PASS' if hard_ok else 'FAIL'} "
          f"({len(score.get('hard_fails', []))} failures)")
    for f in score.get("hard_fails", []):
        print(f"        - {f}")
    print(f"[gate] reward={reward}  last_accepted={last_reward}"
          + (f" (iter {last_iter})" if last_iter else "")
          + f"  epsilon={epsilon}  first_iteration={first_iter}")

    # Decide.
    if dry_run or reward is None:
        verdict = "NO-DECISION"
        print("[gate] NO-DECISION — reward is null (judges DRY-RUN / no key). Re-run "
              "score.py with OPENROUTER_API_KEY set, then re-gate. Hard blockers still apply.")
    elif not hard_ok:
        verdict = "REVERT"
        print("[gate] REVERT — hard checks FAILED; reward is not consulted.")
        _print_revert(iter_no)
    elif first_iter or reward >= last_reward + epsilon:
        verdict = "ACCEPT"
        why = "first iteration (baseline)" if first_iter else \
            f"reward {reward} >= {last_reward} + {epsilon}"
        print(f"[gate] ACCEPT — {why}. Keep the changes; record the hypothesis outcome.")
    else:
        verdict = "REVERT"
        print(f"[gate] REVERT — reward {reward} < {last_reward} + epsilon {epsilon} (no improvement).")
        _print_revert(iter_no)

    book = score.get("book") or ""
    notes = Path(book).name if book and not book.startswith("CONTROL") else book
    row = {"iter": iter_no, "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "campaign": score.get("campaign", ""), "instrument": score.get("instrument_version", ""),
           "hypothesis": a.hypothesis, "reward": "" if reward is None else reward,
           "detection_acc": "" if det is None else det, "hard_ok": hard_ok,
           "verdict": verdict, "notes": notes}
    append_row(tsv, row)
    print(f"[gate] appended verdict row to {tsv}")
    sys.exit({"ACCEPT": 0, "REVERT": 1, "NO-DECISION": 2}[verdict])  # 0/1/2 for wrappers


def _print_revert(iter_no):
    print("[gate] To undo this iteration's tunable-asset changes, run:")
    for path in TUNABLE:
        print(f"        git checkout -- {path}")
    print("        # if THIS iteration edited it: git checkout -- production-books/<slug>/master-plan.md")
    print(f"        rm loop/scores/iter-{str(iter_no).zfill(3)}.json")


if __name__ == "__main__":
    main()
