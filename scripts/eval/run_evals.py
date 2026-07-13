"""Objective eval orchestrator (retired-instrument tool — the live loop uses
scripts/loop/score.py; this remains for the archived calibration/runs/ records).

Runs metrics comparison, the mantra law check, the within-book repetition law,
and the cross-book originality tripwire; writes {run-dir}/metrics.json and
prints a gate summary. Exit 0 = objective gates green (length deltas are
WARN-level; the live hard checks + gate now live in PROGRAM.md §4).

Usage:
  python3 scripts/eval/run_evals.py \
      --book production-books/quit-sugar \
      --ref-dir calibration/reference/gsbs \
      --run-dir calibration/runs/run-001 [--chapters 1-3]
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import evallib as E
import metrics as M
import repetition as R
import mantra_check as MC


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--book", required=True, help="book folder (with chapters/, master-plan.md)")
    ap.add_argument("--ref-dir", required=True, help="extracted reference dir")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--chapters", default=None, help="e.g. 1-3 for Stage A")
    ap.add_argument("--cross-tripwire", type=float, default=R.CROSS_TRIPWIRE)
    a = ap.parse_args()

    book = Path(a.book)
    plan = book / "master-plan.md"
    ref_metrics_path = Path(a.ref_dir) / "reference-metrics.json"
    if not ref_metrics_path.is_file():
        raise SystemExit(f"run_evals: {ref_metrics_path} missing — run extract_reference.py first")
    run_dir = Path(a.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    chapters = E.load_chapters(book / "chapters")
    sel = E.parse_range(a.chapters, len(chapters))
    selected = set(sel)
    # Empty placeholders keep repetition findings numbered as source chapters.
    scoped_chapters = [(name, raw if i in selected else "")
                       for i, (name, raw) in enumerate(chapters, 1)]
    hard_fails, warnings = [], []

    # 1. metrics vs reference
    ours = M.book_metrics(chapters)
    ref = json.loads(ref_metrics_path.read_text(encoding="utf-8"))
    cmpres = M.compare(ours, ref, sel if a.chapters is not None else None)
    warnings += cmpres["warnings"]
    print(M.fmt_table(cmpres["rows"]))

    # 2. mantra law
    mantra_res = None
    if plan.is_file():
        mantras = MC.parse_mantra_sheet(plan.read_text(encoding="utf-8", errors="replace"))
        if mantras:
            mantra_res = MC.verify(mantras, chapters, sel)
            for f in mantra_res["failures"]:
                hard_fails.append(f"mantra: {f}")
        else:
            hard_fails.append("mantra: mantra sheet not parseable/unfilled")
    else:
        hard_fails.append("mantra: no master-plan.md")

    # 3. repetition law within the book
    wl = [m["wording"] for m in (mantra_res and mantra_res.get("mantras") or [])]
    within = R.within_book(scoped_chapters, wl)
    if within["hard_fails"]:
        hard_fails += [f"repetition: {s['len']}-gram x{s['count']} ch{s['chapters']}: "
                       f"{s['text'][:70]}" for s in within["hard_fails"][:5]]

    # 4. originality vs reference
    cross = R.cross_book(scoped_chapters, a.ref_dir, tripwire=a.cross_tripwire)
    if cross["tripped"]:
        hard_fails.append(f"originality: cross-overlap {cross['overlap_ratio']*100:.3f}% "
                          f"> tripwire {a.cross_tripwire*100:.1f}%")

    payload = {"chapters_checked": sel, "metrics": {"ours": ours, "compare": cmpres},
               "mantra": mantra_res, "repetition_within": within,
               "originality_cross": cross,
               "hard_fails": hard_fails, "warnings": warnings}
    out = run_dir / "metrics.json"
    out.write_text(json.dumps(payload, indent=1), encoding="utf-8")

    print(f"\n[run_evals] wrote {out}")
    for w in warnings:
        print(f"  WARN: {w}")
    for f in hard_fails:
        print(f"  HARD FAIL: {f}")
    print(f"[run_evals] objective verdict: {'FAIL' if hard_fails else 'PASS'} "
          f"({len(hard_fails)} hard, {len(warnings)} warns)")
    sys.exit(2 if hard_fails else 0)


if __name__ == "__main__":
    main()
