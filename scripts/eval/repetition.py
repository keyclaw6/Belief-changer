"""THE LAW, mechanized: mantras repeat verbatim; everything else never does.

Two checks:
  within — n-gram shingles repeated inside the generated book, excluding
           mantra wordings (whitelist from the master plan). 8-gram repeats are
           reported; 12-gram repeats are HARD FAILURES.
  cross  — n-gram overlap between the generated book and the reference book
           (mimicry/plagiarism tripwire; default hard threshold 0.3%).

Usage:
  python3 scripts/eval/repetition.py --book production-books/quit-sugar/chapters \
      [--plan production-books/quit-sugar/master-plan.md] \
      [--ref-dir calibration/reference/gsbs] [--json OUT.json]
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import evallib as E

N_SOFT, N_HARD = 8, 12
CROSS_TRIPWIRE = 0.003


def _mantra_whitelist(plan_path):
    if not plan_path or not Path(plan_path).is_file():
        return []
    import mantra_check as MC
    return [m["wording"] for m in MC.parse_mantra_sheet(Path(plan_path).read_text(encoding="utf-8"))]


def _is_whitelisted(shingle: str, wl_tokenized: list) -> bool:
    toks = shingle.split()
    for wl in wl_tokenized:
        for i in range(len(wl) - len(toks) + 1):
            if wl[i:i + len(toks)] == toks:
                return True
    return False


def within_book(chapters, whitelist, n_soft=N_SOFT, n_hard=N_HARD):
    wl_tok = [E.words(w) for w in whitelist]
    occurrences = defaultdict(list)  # shingle -> [(ch_idx, pos)]
    tokens_per_ch = []
    for idx, (_, raw) in enumerate(chapters, 1):
        toks = E.words(E.strip_markdown(raw))
        tokens_per_ch.append(toks)
        for pos, sh in enumerate(E.shingles(toks, n_soft)):
            occurrences[sh].append((idx, pos))
    repeated = {sh: locs for sh, locs in occurrences.items()
                if len(locs) > 1 and not _is_whitelisted(sh, wl_tok)}
    # merge chains of consecutive repeated shingles for readable reporting
    spans, seen = [], set()
    for sh, locs in repeated.items():
        if sh in seen:
            continue
        chain, cur = [sh], sh
        while True:
            nxt = [s for s in repeated if s not in seen and s != cur
                   and s.split()[:-1] == cur.split()[1:]]
            if not nxt:
                break
            cur = nxt[0]
            chain.append(cur)
            seen.add(cur)
        seen.add(sh)
        first, full = chain[0].split(), chain[0].split()
        for link in chain[1:]:
            full.append(link.split()[-1])
        spans.append({"text": " ".join(full), "len": len(full),
                      "count": len(repeated[chain[0]]),
                      "chapters": sorted({c for c, _ in repeated[chain[0]]})})
    spans.sort(key=lambda s: (-s["len"], -s["count"]))
    hard = [s for s in spans if s["len"] >= n_hard]
    return {"repeated_ngrams": len(repeated), "spans_top": spans[:20],
            "hard_fails": hard, "whitelist_size": len(whitelist)}


def cross_book(chapters, ref_dir, n=N_SOFT, tripwire=CROSS_TRIPWIRE):
    ours = set()
    for _, raw in chapters:
        ours.update(E.shingles(E.words(E.strip_markdown(raw)), n))
    ref = set()
    for _, raw in E.load_chapters(ref_dir, exts=(".txt", ".md")):
        ref.update(E.shingles(E.words(raw), n))
    overlap = ours & ref
    ratio = len(overlap) / (len(ours) or 1)
    return {"ours_ngrams": len(ours), "overlap_ngrams": len(overlap),
            "overlap_ratio": round(ratio, 5), "tripwire": tripwire,
            "tripped": ratio > tripwire,
            "samples": sorted(overlap)[:15]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--book", required=True)
    ap.add_argument("--plan", help="master-plan.md carrying the mantra sheet whitelist")
    ap.add_argument("--ref-dir", help="reference text dir for cross-book overlap")
    ap.add_argument("--tripwire", type=float, default=CROSS_TRIPWIRE)
    ap.add_argument("--json", dest="json_out")
    a = ap.parse_args()

    chapters = E.load_chapters(a.book)
    wl = _mantra_whitelist(a.plan)
    result = {"within": within_book(chapters, wl)}
    w = result["within"]
    print(f"[repetition] whitelist mantras: {w['whitelist_size']} | repeated "
          f"{N_SOFT}-grams (non-mantra): {w['repeated_ngrams']} | hard fails "
          f"(>={N_HARD}-gram): {len(w['hard_fails'])}")
    for s in w["spans_top"][:5]:
        print(f"  repeat x{s['count']} ({s['len']}w, ch {s['chapters']}): {s['text'][:90]}")
    ok = not w["hard_fails"]
    if a.ref_dir:
        result["cross"] = cross_book(chapters, a.ref_dir, tripwire=a.tripwire)
        c = result["cross"]
        print(f"[repetition] cross-overlap vs reference: {c['overlap_ratio']*100:.3f}% "
              f"({c['overlap_ngrams']}/{c['ours_ngrams']}) tripwire {c['tripwire']*100:.1f}% "
              f"-> {'TRIPPED' if c['tripped'] else 'ok'}")
        ok = ok and not c["tripped"]
    if a.json_out:
        Path(a.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json_out).write_text(json.dumps(result, indent=1), encoding="utf-8")
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
