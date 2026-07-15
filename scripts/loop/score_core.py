"""Pure RF-02 score inputs; score.py and gate.py both recompute these."""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "eval"))
import evallib as E  # noqa: E402
import metrics as M  # noqa: E402
import repetition as R  # noqa: E402
import mantra_check as MC  # noqa: E402
import planctx  # noqa: E402

BUDGET_RE = re.compile(r"\*\*CH-(\d+)\*\*.*?\|\s*([\d,]+)\s*\|\s*$")


def _budgets(text):
    out = {}
    for line in text.splitlines():
        match = BUDGET_RE.search(line.strip())
        if match:
            out[int(match.group(1))] = int(match.group(2).replace(",", ""))
    return out


def _length(ours, sel, budgets, band):
    rows, fails = [], []
    for chapter in ours["chapters"]:
        if chapter["n"] not in sel:
            continue
        budget, words = budgets.get(chapter["n"]), chapter["words"]
        if not budget:
            rows.append({"n": chapter["n"], "words": words, "budget": None, "ok": True})
            continue
        lo, hi = round(budget * (1 - band)), round(budget * (1 + band))
        ok = lo <= words <= hi
        rows.append({"n": chapter["n"], "words": words, "budget": budget,
                     "band": [lo, hi], "ok": ok})
        if not ok:
            side = "below" if words < lo else "above"
            fails.append(f"length: ch{chapter['n']} {words}w {side} band {lo}-{hi} "
                         f"(budget {budget}, +/-{int(band*100)}%)")
    return rows, fails


def _reference(cfg):
    root = Path(cfg["reference_dir"])
    metrics = root / "reference-metrics.json"
    if not metrics.is_file():
        raise SystemExit(f"score: reference metrics missing at {root}")
    return root, E.load_chapters(root, exts=(".txt", ".md")), json.loads(
        metrics.read_text(encoding="utf-8"))


def _style(ours, reference, sel, offset):
    positions = {n + offset for n in sel}
    ours_metrics = M.book_metrics_from_counts(
        [chapter for chapter in ours["chapters"] if chapter["n"] in set(sel)])
    ref_metrics = M.book_metrics_from_counts(
        [chapter for chapter in reference["chapters"] if chapter["n"] in positions])
    keys = ("mean_chapter_words", "mean_sentence_words", "pct_short_sentences",
            "questions_per_100_sents", "second_person_per_1000", "first_person_per_1000")
    return [{"metric": key, "ours": ours_metrics.get(key), "ref": ref_metrics.get(key)}
            for key in keys]


def evaluate(cfg, book, chapters, control_ref=False):
    """Return every deterministic hard/diagnostic value and the judge task inputs."""
    offset = int(cfg["reference_chapter_offset"])
    ref_dir, ref_chapters, ref_metrics = _reference(cfg)
    if control_ref:
        sel = E.parse_range(chapters, len(ref_chapters) - offset)
        ours_chapters = [(f"chapter-{n:02d}.md", ref_chapters[n + offset - 1][1])
                         for n in sel]
        plan_text = ""
    else:
        book = Path(book)
        ours_chapters = E.load_chapters(book / "chapters")
        sel = E.parse_range(chapters, len(ours_chapters))
        plan = book / "master-plan.md"
        plan_text = plan.read_text(encoding="utf-8", errors="replace")
    ours = M.book_metrics(ours_chapters)
    selected = set(sel)
    scoped = [(name, raw if index in selected else "")
              for index, (name, raw) in enumerate(ours_chapters, 1)]
    fails = []
    if control_ref:
        cross = {"mode": "N/A control", "overlap_ratio": None,
                 "tripwire": float(cfg["originality_tripwire"]), "tripped": False}
    else:
        cross = R.cross_book(scoped, str(ref_dir),
                             tripwire=float(cfg["originality_tripwire"]))
        if cross["tripped"]:
            fails.append(f"originality: overlap {cross['overlap_ratio']*100:.3f}% > "
                         f"tripwire {cross['tripwire']*100:.1f}%")
    mantra = None
    mantras = MC.parse_mantra_sheet(plan_text) if plan_text else []
    if mantras:
        mantra = MC.verify(mantras, ours_chapters, sel)
        fails.extend(f"mantra: {failure}" for failure in mantra["failures"])
    elif not control_ref:
        fails.append("mantra: no parseable mantra sheet in master-plan.md")
    wording = [item["wording"] for item in (mantra["mantras"] if mantra else [])]
    within = R.within_book(scoped, wording)
    lengths, length_fails = _length(ours, sel, _budgets(plan_text),
                                    float(cfg["length_band"]))
    fails.extend(length_fails)
    pairs = planctx.build_pairs(ours_chapters, ref_chapters, sel, offset,
                                plan_text, control_ref)
    near = []
    if not control_ref:
        tripwire = float(cfg.get("near_copy_tripwire", 0.5))
        for label, ours_text, ref_text, _ in pairs:
            ratio = planctx.near_copy_ratio(ours_text, ref_text)
            near.append({"chapter": label, "ratio": ratio, "tripwire": tripwire})
            if ratio > tripwire:
                fails.append(f"near-copy: {label} word-sequence similarity "
                             f"{ratio} > {tripwire}")
    return {
        "chapters_checked": sel, "hard_ok": not fails, "hard_fails": fails,
        "checks": {"originality": cross, "mantra": mantra,
                   "repetition_within": within, "length": lengths, "near_copy": near},
        "diagnostics": {"stylometrics": _style(ours, ref_metrics, sel, offset)},
        "pairs": pairs,
    }
