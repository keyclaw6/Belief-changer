"""ONE command -> ONE reward + hard checks + diagnostics (wraps scripts/eval).

  python3 scripts/loop/score.py --book production-books/quit-sugar --chapters 1-3 --iter 7
  python3 scripts/loop/score.py --control-ref --iter 0   # real GSBS as "ours"

HARD CHECKS (gate-blocking): originality tripwire, mantra/repetition law, loose
length sanity. REWARD: the reference-anchored rubric (PROGRAM §4.2) — fresh
native Sol subagents score distance from the matched real chapter; emits task
files and exits 3 (WAITING-FOR-VERDICTS) until every verdict JSON is saved,
then aggregates. DIAGNOSTICS (never gate): stylometrics. Writes
loop/scores/iter-NNN.json.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "eval"))
sys.path.insert(0, str(HERE.parent))
import evallib as E          # noqa: E402
import metrics as M          # noqa: E402
import repetition as R       # noqa: E402
import mantra_check as MC     # noqa: E402
import loopcfg               # noqa: E402
import judges                # noqa: E402

BUDGET_RE = re.compile(r"\*\*CH-(\d+)\*\*.*?\|\s*([\d,]+)\s*\|\s*$")


def parse_budgets(plan_text: str) -> dict:
    """Map chapter number -> planned word budget from the arc/budget table.

    Rows look like `| **CH-01** | ... | 2,400 |`. The budget is the last numeric
    cell on a CH row. Returns {} if none parse (caller degrades length to WARN).
    """
    budgets = {}
    for line in plan_text.splitlines():
        m = BUDGET_RE.search(line.strip())
        if m:
            budgets[int(m.group(1))] = int(m.group(2).replace(",", ""))
    return budgets


def length_check(ours, sel, budgets, band):
    """Loose sanity: each selected chapter within +/- band of its plan budget."""
    rows, fails = [], []
    for c in ours["chapters"]:
        if c["n"] not in sel:
            continue
        budget = budgets.get(c["n"])
        words = c["words"]
        if not budget:
            rows.append({"n": c["n"], "words": words, "budget": None, "ok": True})
            continue
        lo, hi = round(budget * (1 - band)), round(budget * (1 + band))
        ok = lo <= words <= hi
        rows.append({"n": c["n"], "words": words, "budget": budget,
                     "band": [lo, hi], "ok": ok})
        if not ok:
            side = "below" if words < lo else "above"
            fails.append(f"length: ch{c['n']} {words}w {side} band {lo}-{hi} "
                         f"(budget {budget}, +/-{int(band*100)}%)")
    return rows, fails


def load_reference(cfg):
    ref_dir = Path(cfg["reference_dir"])
    if not (ref_dir / "reference-metrics.json").is_file():
        raise SystemExit(
            f"score: reference metrics missing at {ref_dir}. Run:\n"
            f'  python3 scripts/eval/extract_reference.py --epub "{cfg["reference_epub"]}" '
            f"--out {ref_dir}")
    ref_chapters = E.load_chapters(ref_dir, exts=(".txt", ".md"))
    ref_metrics = json.loads((ref_dir / "reference-metrics.json").read_text(encoding="utf-8"))
    return ref_dir, ref_chapters, ref_metrics


def build_pairs(ours_chapters, ref_chapters, sel, offset):
    """(label, ours_text, ref_text) for each selected chapter -> matched real chapter."""
    pairs = []
    for n in sel:
        ref_pos = n + offset
        if ref_pos > len(ref_chapters):
            continue
        ours_text = E.strip_markdown(ours_chapters[n - 1][1])
        ref_text = ref_chapters[ref_pos - 1][1]
        pairs.append((f"ch{n:02d}", ours_text, ref_text))
    return pairs


def stylometrics(ours, ref_metrics, sel, offset):
    """Our stylometric aggregate beside the matched reference positions (diagnostic)."""
    ref_positions = {n + offset for n in sel}
    o = M.book_metrics_from_counts([c for c in ours["chapters"] if c["n"] in set(sel)])
    r = M.book_metrics_from_counts([c for c in ref_metrics["chapters"] if c["n"] in ref_positions])
    keys = ("mean_chapter_words", "mean_sentence_words", "pct_short_sentences",
            "questions_per_100_sents", "second_person_per_1000", "first_person_per_1000")
    return [{"metric": k, "ours": o.get(k), "ref": r.get(k)} for k in keys]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--book", help="book folder with chapters/ and master-plan.md")
    ap.add_argument("--chapters", default="1-3")
    ap.add_argument("--iter", type=int, help="iteration number for the artifact name")
    ap.add_argument("--config", default=None)
    ap.add_argument("--control-ref", action="store_true",
                    help="score real GSBS chapters AS ours (originality excludes the "
                         "matched reference chapter; sanity control, expect PASS)")
    a = ap.parse_args()

    cfg = loopcfg.load(a.config) if a.config else loopcfg.load(loopcfg.find_config())
    band = float(cfg["length_band"])
    offset = int(cfg["reference_chapter_offset"])
    ref_dir, ref_chapters, ref_metrics = load_reference(cfg)

    # Resolve the chapters under test.
    if a.control_ref:
        # Treat the real chapters (offset+1 .. offset+len(sel)) as "ours".
        sel = E.parse_range(a.chapters, len(ref_chapters) - offset)
        ours_chapters = [(f"chapter-{n:02d}.md", ref_chapters[n + offset - 1][1]) for n in sel]
        plan_text = ""
    else:
        if not a.book:
            ap.error("--book is required unless --control-ref")
        book = Path(a.book)
        ours_chapters = E.load_chapters(book / "chapters")
        sel = E.parse_range(a.chapters, len(ours_chapters))
        plan_path = book / "master-plan.md"
        plan_text = plan_path.read_text(encoding="utf-8", errors="replace") if plan_path.is_file() else ""

    ours = M.book_metrics(ours_chapters)
    selset = set(sel)
    scoped = [(name, raw if i in selset else "") for i, (name, raw) in enumerate(ours_chapters, 1)]
    hard_fails = []

    # --- HARD CHECK 1: originality vs reference (plagiarism tripwire). In
    # --control-ref, reference-vs-itself is degenerate -> N/A, never a fail.
    if a.control_ref:
        cross = {"mode": "N/A (control): reference-vs-self is degenerate, not a "
                 "plagiarism signal", "overlap_ratio": None, "tripwire": float(cfg["originality_tripwire"]),
                 "tripped": False}
    else:
        cross = R.cross_book(scoped, str(ref_dir), tripwire=float(cfg["originality_tripwire"]))
        if cross["tripped"]:
            hard_fails.append(f"originality: overlap {cross['overlap_ratio']*100:.3f}% > "
                              f"tripwire {cross['tripwire']*100:.1f}%")

    # --- HARD CHECK 2: mantra law + verbatim-repetition law ---
    mantra_res, within = None, None
    mantras = MC.parse_mantra_sheet(plan_text) if plan_text else []
    if mantras:
        mantra_res = MC.verify(mantras, ours_chapters, sel)
        for f in mantra_res["failures"]:
            hard_fails.append(f"mantra: {f}")
    elif not a.control_ref:
        hard_fails.append("mantra: no parseable mantra sheet in master-plan.md")
    wl = [m["wording"] for m in (mantra_res["mantras"] if mantra_res else [])]
    within = R.within_book(scoped, wl)
    # In control mode the real book's cross-chapter refrains are a DIAGNOSTIC of
    # Carr's actual repetition habit, not a repo-law violation — never gate them.
    if not a.control_ref:
        for s in within["hard_fails"][:5]:
            hard_fails.append(f"repetition: {s['len']}-gram x{s['count']} ch{s['chapters']}: {s['text'][:70]}")

    # --- HARD CHECK 3: loose length sanity ---
    budgets = parse_budgets(plan_text) if plan_text else {}
    length_rows, length_fails = length_check(ours, sel, budgets, band)
    hard_fails += length_fails

    hard_ok = not hard_fails

    # --- DIAGNOSTICS (never gate) ---
    style_rows = stylometrics(ours, ref_metrics, sel, offset)

    # --- REWARD (reference-anchored rubric; judges = native Sol subagents) ---
    pairs = build_pairs(ours_chapters, ref_chapters, sel, offset)
    labels = [lbl for lbl, _, _ in pairs]
    iter_name = f"{a.iter:03d}" if a.iter is not None else "adhoc"
    rubric = Path(cfg["judge_rubric"]).read_text(encoding="utf-8")
    missing = judges.missing_verdicts(cfg, labels, iter_name)
    if missing:
        judges.emit_tasks(cfg, pairs, iter_name, rubric)
        rub, reward, status = None, None, "WAITING-FOR-VERDICTS"
    else:
        rub = judges.aggregate(cfg, labels, iter_name)
        reward, status = rub["reward"], "SCORED"

    payload = {
        "campaign": cfg.get("campaign"), "instrument_version": cfg.get("instrument_version"),
        "book": a.book if not a.control_ref else "CONTROL:reference-as-ours",
        "chapters_checked": sel, "control_ref": a.control_ref,
        "reward": reward, "hard_ok": hard_ok, "hard_fails": hard_fails,
        "checks": {"originality": cross, "mantra": mantra_res, "repetition_within": within,
                   "length": length_rows},
        "diagnostics": {"stylometrics": style_rows},
        "judges": {"status": status, "rubric": rub, "missing": missing},
    }
    _report(payload)

    scores_dir = Path(cfg["scores_dir"])
    scores_dir.mkdir(parents=True, exist_ok=True)
    name = f"iter-{a.iter:03d}.json" if a.iter is not None else "iter-adhoc.json"
    (scores_dir / name).write_text(json.dumps(payload, indent=1), encoding="utf-8")
    print(f"[score] wrote {scores_dir / name}")
    # Exit 3 = verdicts pending (dispatch judges, re-run). Else 0: gate.py decides.
    sys.exit(3 if status == "WAITING-FOR-VERDICTS" else 0)


def _report(p):
    print(f"[score] campaign={p['campaign']} instrument={p['instrument_version']} "
          f"chapters={p['chapters_checked']}")
    c = p["checks"]["originality"]
    if c.get("overlap_ratio") is None:
        print(f"[hard] originality: {c.get('mode', 'N/A')}")
    else:
        print(f"[hard] originality overlap {c['overlap_ratio']*100:.3f}% "
              f"(tripwire {c['tripwire']*100:.1f}%) -> {'TRIPPED' if c['tripped'] else 'ok'}")
    mr = p["checks"]["mantra"]
    if mr is not None:
        print(f"[hard] mantra: {len(mr['mantras'])} parsed, {len(mr['failures'])} failures; "
              f"no-mantra chapters {mr['chapters_without_mantra']}")
    nrep = len(p["checks"]["repetition_within"]["hard_fails"])
    tag = "diagnostic (control)" if p.get("control_ref") else "hard"
    print(f"[{'diag' if p.get('control_ref') else 'hard'}] repetition: {nrep} "
          f">=12-gram non-mantra repeats ({tag})")
    print("[hard] length: " + " | ".join(
        f"ch{r['n']} {r['words']}w/{r.get('budget') or '-'} "
        f"{'ok' if r['ok'] else 'FAIL'}" for r in p["checks"]["length"]))
    print("[diag] stylometrics (ours vs matched reference positions):")
    for r in p["diagnostics"]["stylometrics"]:
        print(f"        {r['metric']:<26}{str(r['ours']):>10}{str(r['ref']):>10}")
    j = p["judges"]
    if j["status"] == "WAITING-FOR-VERDICTS":
        print(f"[reward] WAITING-FOR-VERDICTS — {len(j['missing'])} verdicts missing; "
              "task files emitted (see [judges] lines above).")
    else:
        r = j["rubric"]
        print(f"[reward] carr-likeness composite = {r['reward']}  "
              f"({r['n_verdicts']} verdicts, k={r['judge_k']}, judge={r['judge_model']})")
        for c in r["per_chapter"]:
            dims = "  ".join(f"{d.split('_')[0]}={c['dims'][d]}" for d in judges.DIMS)
            print(f"         {c['chapter']} composite={c['composite']}  {dims}")
        if r["worst_dimensions"]:
            print("[gap]    worst-dimension votes: " + ", ".join(
                f"{x['dimension']} x{x['votes']}" for x in r["worst_dimensions"]))
        for s in r["suggestions"]:
            print(f"[sugg]   ({s['asset']}, x{s['count']}) {s['suggestion'][:140]}")
    print(f"[verdict] HARD CHECKS: {'PASS' if p['hard_ok'] else 'FAIL'} "
          f"({len(p['hard_fails'])} failures)")
    for f in p["hard_fails"]:
        print(f"          - {f}")


if __name__ == "__main__":
    main()
