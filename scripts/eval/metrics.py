"""Voice & length metrics for a book (generated or reference), plus comparison.

Usage:
  python3 scripts/eval/metrics.py --book production-books/quit-sugar/chapters \
      [--ref calibration/reference/gsbs/reference-metrics.json] [--chapters 1-3] \
      [--json OUT.json]

Metrics are the measurable half of style guide Part B voice targets. Length
comparison against the reference is a loop diagnostic (PROGRAM.md §4 SCORE).
"""
import argparse
import json
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import evallib as E

SECOND_PERSON = {"you", "your", "yours", "yourself", "you're", "you've", "you'll", "you'd"}
FIRST_PERSON = {"i", "i'm", "i've", "i'll", "i'd", "me", "my"}


def chapter_metrics(raw_text: str) -> dict:
    text = E.strip_markdown(raw_text)
    ws = E.words(text)
    sents = E.sentences(text)
    paras = E.paragraphs(text)
    slens = [len(E.words(s)) for s in sents] or [0]
    n_words = len(ws) or 1
    n_sents = len(sents) or 1
    return {
        "words": len(ws),
        "sentences": len(sents),
        "paragraphs": len(paras),
        "mean_sentence_words": round(sum(slens) / n_sents, 1),
        "median_sentence_words": st.median(slens),
        "pct_short_sentences": round(100 * sum(1 for L in slens if L <= 8) / n_sents, 1),
        "questions_per_100_sents": round(100 * text.count("?") / n_sents, 1),
        "exclaims_per_100_sents": round(100 * text.count("!") / n_sents, 1),
        "second_person_per_1000": round(1000 * sum(1 for w in ws if w in SECOND_PERSON) / n_words, 1),
        "first_person_per_1000": round(1000 * sum(1 for w in ws if w in FIRST_PERSON) / n_words, 1),
        "mean_paragraph_words": round(len(ws) / (len(paras) or 1), 1),
    }


def book_metrics(chapters: list) -> dict:
    """chapters: [(name, raw_text)] -> per-chapter + aggregate metrics."""
    per = []
    for i, (name, raw) in enumerate(chapters, 1):
        m = chapter_metrics(raw)
        m["n"] = i
        m["file"] = name
        per.append(m)
    counts = [c["words"] for c in per] or [0]
    agg = {
        "chapter_count": len(per),
        "total_words": sum(counts),
        "mean_chapter_words": round(st.mean(counts), 1),
        "median_chapter_words": st.median(counts),
        "stdev_chapter_words": round(st.stdev(counts), 1) if len(counts) > 1 else 0.0,
        "min_chapter_words": min(counts),
        "max_chapter_words": max(counts),
    }
    for key in ("mean_sentence_words", "pct_short_sentences", "questions_per_100_sents",
                "exclaims_per_100_sents", "second_person_per_1000", "first_person_per_1000"):
        agg[key] = round(st.mean([c[key] for c in per]), 1)
    return {"chapters": per, "aggregate": agg}


def compare(ours: dict, ref: dict, chapter_sel=None) -> dict:
    """Compare aggregates; if chapter_sel, compare only those positions of both."""
    def slice_agg(book):
        chs = book["chapters"]
        if chapter_sel:
            chs = [c for c in chs if c["n"] in chapter_sel]
        pairs = [(c["file"], c["words"]) for c in chs]
        return book_metrics_from_counts(chs), pairs

    o_agg, _ = slice_agg(ours)
    r_agg, _ = slice_agg(ref)
    rows, flags = [], []
    for key in sorted(set(o_agg) | set(r_agg)):
        ov, rv = o_agg.get(key), r_agg.get(key)
        ratio = round(ov / rv, 2) if isinstance(ov, (int, float)) and rv else None
        rows.append({"metric": key, "ours": ov, "ref": rv, "ratio": ratio})
        if key in ("total_words", "mean_chapter_words") and ratio is not None:
            if not 0.85 <= ratio <= 1.15:
                flags.append(f"LENGTH WARN: {key} ratio {ratio} outside ±15%")
    return {"rows": rows, "warnings": flags}


def book_metrics_from_counts(per_chapters: list) -> dict:
    counts = [c["words"] for c in per_chapters] or [0]
    agg = {
        "chapter_count": len(per_chapters),
        "total_words": sum(counts),
        "mean_chapter_words": round(st.mean(counts), 1) if counts else 0,
        "median_chapter_words": st.median(counts) if counts else 0,
    }
    for key in ("mean_sentence_words", "pct_short_sentences", "questions_per_100_sents",
                "exclaims_per_100_sents", "second_person_per_1000", "first_person_per_1000"):
        vals = [c[key] for c in per_chapters if key in c]
        if vals:
            agg[key] = round(st.mean(vals), 1)
    return agg


def fmt_table(rows: list) -> str:
    out = [f"{'metric':<28}{'ours':>12}{'ref':>12}{'ratio':>8}"]
    for r in rows:
        out.append(f"{r['metric']:<28}{str(r['ours']):>12}{str(r['ref']):>12}"
                   f"{str(r['ratio'] if r['ratio'] is not None else '-'):>8}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--book", required=True, help="chapters dir (ours)")
    ap.add_argument("--ref", help="reference-metrics.json to compare against")
    ap.add_argument("--chapters", default="", help="restrict comparison, e.g. 1-3")
    ap.add_argument("--json", dest="json_out", help="write full metrics JSON here")
    a = ap.parse_args()

    ours = book_metrics(E.load_chapters(a.book))
    result = {"ours": ours}
    print(f"[metrics] {a.book}: {ours['aggregate']['chapter_count']} chapters, "
          f"{ours['aggregate']['total_words']} words")
    if a.ref:
        ref = json.loads(Path(a.ref).read_text(encoding="utf-8"))
        sel = E.parse_range(a.chapters, max(ours["aggregate"]["chapter_count"],
                                            ref["aggregate"]["chapter_count"])) if a.chapters else None
        cmpres = compare(ours, ref, sel)
        result["compare"] = cmpres
        print(fmt_table(cmpres["rows"]))
        for w in cmpres["warnings"]:
            print(w)
    if a.json_out:
        Path(a.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json_out).write_text(json.dumps(result, indent=1), encoding="utf-8")
        print(f"[metrics] wrote {a.json_out}")


if __name__ == "__main__":
    main()
