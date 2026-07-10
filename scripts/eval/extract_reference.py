"""Extract the calibration reference book from an EPUB into local text files.

Writes per-chapter .txt files + reference-metrics.json to --out. The output dir
(calibration/reference/) is GITIGNORED: extracted book text is regenerated
locally and never committed (same policy as the analysis 10-page windows).

Usage:
  python3 scripts/eval/extract_reference.py \
      --epub "analysis/reference-books/The easyway Good Sugar Bad Sugar.epub" \
      --out calibration/reference/gsbs

stdlib only (an EPUB is a zip of XHTML).
"""
import argparse
import html
import json
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import evallib as E
import metrics as M

CH_SENTINEL = "@@CH@@"
MIN_CHAPTER_WORDS = 100  # spine docs / segments below this = front/back matter
FRONTBACK_TITLES = ("contents", "copyright", "index", "dedication", "acknowledg",
                    "about the author", "also by", "publisher", "title page",
                    "other allen carr", "the illustrator", "clinic", "discount voucher")


def _opf_path(z: zipfile.ZipFile) -> str:
    container = z.read("META-INF/container.xml").decode("utf-8", "replace")
    m = re.search(r'full-path="([^"]+)"', container)
    if not m:
        raise SystemExit("extract_reference: no rootfile in container.xml")
    return m.group(1)


def _spine_hrefs(opf_text: str) -> list:
    items = {}
    for m in re.finditer(r"<item\b[^>]*>", opf_text):
        tag = m.group(0)
        mid = re.search(r'id="([^"]+)"', tag)
        href = re.search(r'href="([^"]+)"', tag)
        if mid and href:
            items[mid.group(1)] = html.unescape(href.group(1))
    order = []
    for m in re.finditer(r'<itemref\b[^>]*idref="([^"]+)"', opf_text):
        href = items.get(m.group(1))
        if href and re.search(r"\.x?html?$", href, re.I):
            order.append(href)
    if not order:
        raise SystemExit("extract_reference: empty spine")
    return order


def _xhtml_to_text(raw: str, split_level: int) -> str:
    raw = re.sub(r"<(head|style|script)\b.*?</\1>", " ", raw, flags=re.S | re.I)
    if split_level >= 1:
        raw = re.sub(rf"<h[1-{split_level}]\b[^>]*>", "\n" + CH_SENTINEL + " ", raw, flags=re.I)
    raw = re.sub(r"</(p|h[1-6]|li|div|blockquote|tr)>", "\n", raw, flags=re.I)
    raw = re.sub(r"<br\b[^>]*/?>", "\n", raw, flags=re.I)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in raw.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def _split_segments(text: str) -> list:
    """Split doc text on chapter sentinels -> [(title, body)]."""
    parts = re.split(rf"^{CH_SENTINEL} *(.*)$", text, flags=re.M)
    segs = []
    if parts[0].strip():
        segs.append(("", parts[0]))
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        segs.append((title, body))
    return segs


def _slug(s: str, fallback: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (s or fallback).lower()).strip("-")
    return (s or fallback)[:48]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--epub", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--min-words", type=int, default=MIN_CHAPTER_WORDS)
    ap.add_argument("--split-level", type=int, default=1,
                    help="split chapters at h1..hN headings; 0 = one chapter per spine doc")
    ap.add_argument("--drop", default="",
                    help="1-based positions in the kept list to drop (eyeball first run, "
                         "then re-run, e.g. --drop 1,2)")
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.txt"):
        old.unlink()

    with zipfile.ZipFile(a.epub) as z:
        opf_rel = _opf_path(z)
        opf_dir = str(Path(opf_rel).parent)
        opf_text = z.read(opf_rel).decode("utf-8", "replace")
        chapters, skipped = [], []
        for href in _spine_hrefs(opf_text):
            member = href if href in z.namelist() else str(Path(opf_dir) / href)
            member = member.replace("\\", "/").lstrip("./")
            if member not in z.namelist():
                skipped.append((href, "not in zip"))
                continue
            text = _xhtml_to_text(z.read(member).decode("utf-8", "replace"), a.split_level)
            for title, body in _split_segments(text):
                wc = len(E.words(body))
                first_line = next((ln for ln in body.splitlines() if ln.strip()), "")
                probe = (title + " " + first_line).lower()
                head300 = body[:300].lower()
                if any(k in probe for k in FRONTBACK_TITLES):
                    skipped.append((title or first_line[:40] or member, "front/back matter title"))
                    continue
                if any(k in head300 for k in ("copyright ©", "all rights reserved", "isbn")):
                    skipped.append((title or first_line[:40] or member, "copyright page"))
                    continue
                if wc < a.min_words:
                    skipped.append((title or first_line[:40] or member, f"{wc} words"))
                    continue
                chapters.append((title or first_line[:60], body))

    if a.drop:
        drop = {int(x) for x in a.drop.split(",") if x.strip()}
        dropped = [t or "untitled" for i, (t, _) in enumerate(chapters, 1) if i in drop]
        chapters = [c for i, c in enumerate(chapters, 1) if i not in drop]
        skipped += [(t, "--drop") for t in dropped]
    if not chapters:
        raise SystemExit("extract_reference: no chapters above min-words threshold")

    named = []
    for i, (title, body) in enumerate(chapters, 1):
        fname = f"{i:03d}-{_slug(title, 'chapter')}.txt"
        content = (title + "\n\n" + body.strip() + "\n") if title else body.strip() + "\n"
        (out / fname).write_text(content, encoding="utf-8")
        named.append((fname, content))

    book = M.book_metrics(named)
    for ch, (title, _) in zip(book["chapters"], chapters):
        ch["title"] = title
    meta = {"source_epub": a.epub, "extracted_chapters": len(named),
            "skipped_segments": [f"{t}: {r}" for t, r in skipped]}
    payload = {"meta": meta, **book}
    (out / "reference-metrics.json").write_text(json.dumps(payload, indent=1), encoding="utf-8")

    agg = book["aggregate"]
    print(f"[extract] {len(named)} chapters -> {out}")
    print(f"[extract] total {agg['total_words']} words | mean ch {agg['mean_chapter_words']} | "
          f"median {agg['median_chapter_words']} | min {agg['min_chapter_words']} | "
          f"max {agg['max_chapter_words']}")
    print(f"[extract] skipped {len(skipped)} sub-min segments (front/back matter)")
    print(f"[extract] wrote {out / 'reference-metrics.json'}")


if __name__ == "__main__":
    main()
