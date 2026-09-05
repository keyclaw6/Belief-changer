#!/usr/bin/env python3
"""Split the illustrated Easyway smoking PDF extract into GSBS-style chapters."""
from __future__ import annotations

import re
from pathlib import Path

PAGES = Path("/tmp/easyway-smoking/pages")
OUT = Path("/home/kab/Belief-changer/calibration/reference/easyway-smoking")

# PDF page (1-indexed pdftotext) → chapter. Front/back matter omitted.
CHAPTERS = [
    ("00-introduction.md", "ABOUT EASYWAY", 7, 7),
    ("chapter-01.md", "SO YOU WANT TO QUIT SMOKING?", 9, 27),
    ("chapter-02.md", "THE TRAP", 28, 41),
    ("chapter-03.md", "THE TWO-HEADED MONSTER", 42, 61),
    ("chapter-04.md", "NO BUTTS", 62, 93),
    ("chapter-05.md", "THE VOID", 94, 107),
    ("chapter-06.md", "THOSE TERRIBLE CRAVINGS", 108, 125),
    ("chapter-07.md", "FINAL INSTRUCTIONS", 126, 132),
    ("chapter-08.md", "THE RITUAL", 133, 141),
]

HEADER = re.compile(r"^THE ILLUSTRATED\s*$", re.I)
PAGE_NUM = re.compile(r"^\d{1,3}$")
URL = re.compile(r"https?\s*://|archive\.org|allencarr\.com|easywaypublishing", re.I)
JUNK = re.compile(
    r"^(ch|ccc|kin|ec“|aaa,|ig \.|ae|one|a|=|88|ccc 911|39876|AD000036EN|"
    r"Printed in the UK|ARCTURUS|BRENT LIBRARIES)\s*$",
    re.I,
)


def letter_ratio(s: str) -> float:
    letters = sum(c.isalpha() for c in s)
    return letters / len(s) if s else 0


def keep_line(raw: str) -> bool:
    s = raw.strip()
    if not s:
        return False
    if HEADER.match(s) or PAGE_NUM.match(s) or JUNK.match(s):
        return False
    if URL.search(s) and letter_ratio(s) < 0.55:
        return False
    if s.startswith("https"):
        return False
    if letter_ratio(s) < 0.35 and not re.search(r"[A-Za-z]{3,}", s):
        return False
    if len(s) <= 3 and not s.isalpha():
        return False
    if re.fullmatch(r"[\W\d_]+", s):
        return False
    # Illustration leftovers: almost no vowels, or a couple of letters beside junk
    letters = "".join(c for c in s if c.isalpha())
    if len(letters) <= 4 and re.search(r"[|_/\\=]{2,}|[0-9]{3,}", s):
        return False
    vowels = sum(c.lower() in "aeiou" for c in letters)
    if letters and vowels / len(letters) < 0.15 and len(s) < 20:
        return False
    return True


def pages_text(start: int, end: int) -> str:
    lines: list[str] = []
    for n in range(start, end + 1):
        p = PAGES / f"p{n:03d}.txt"
        if not p.exists():
            continue
        for raw in p.read_text(errors="replace").splitlines():
            if keep_line(raw):
                lines.append(re.sub(r"[ \t]+", " ", raw).strip())
    return "\n".join(lines)


def paragraphize(text: str) -> str:
    raw_lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    # Join consecutive short ALL-CAPS bursts into one speech line
    merged: list[str] = []
    cap_buf: list[str] = []

    def flush_caps() -> None:
        if cap_buf:
            merged.append(" ".join(cap_buf))
            cap_buf.clear()

    for ln in raw_lines:
        letters = "".join(c for c in ln if c.isalpha())
        is_caps = bool(letters) and letters.isupper() and len(ln) <= 40
        if is_caps:
            cap_buf.append(ln)
            continue
        flush_caps()
        merged.append(ln)
    flush_caps()
    raw_lines = merged
    paras: list[str] = []
    buf: list[str] = []

    def flush() -> None:
        if not buf:
            return
        paras.append(" ".join(buf))
        buf.clear()

    for ln in raw_lines:
        short_shout = len(ln) <= 80 and (ln.isupper() or ln.endswith("!") or ln.endswith("?"))
        if short_shout and not buf:
            paras.append(ln)
            continue
        if short_shout and buf:
            flush()
            paras.append(ln)
            continue
        if buf and (buf[-1].endswith((".", "!", "?", "…", "—")) or ln[:1].isupper() and len(buf[-1]) > 40):
            # start new paragraph on a clear sentence boundary + new capital
            if buf[-1].endswith((".", "!", "?")) and ln[:1].isupper():
                flush()
        buf.append(ln)
    flush()
    return "\n\n".join(paras)


def chapter_md(filename: str, title: str, start: int, end: int) -> str:
    body = paragraphize(pages_text(start, end))
    # Drop a leading title echo if the first paragraph is the chapter name
    first = body.split("\n\n", 1)
    if first and re.sub(r"[‘’']", "", first[0]).upper().replace(" ", "") in re.sub(r"\s+", "", title.upper()):
        body = first[1] if len(first) > 1 else body
    if filename.startswith("00-"):
        return f"# {title}\n\n{body.rstrip()}\n"
    num = int(re.search(r"(\d+)", filename).group(1))
    return f"# Chapter {num}\n\n# {title}\n\n{body.rstrip()}\n"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    rows = []
    for filename, title, start, end in CHAPTERS:
        md = chapter_md(filename, title, start, end)
        (OUT / filename).write_text(md)
        words = len(md.split())
        total += words
        rows.append((filename, title, words))
        print(f"{filename:22} {words:5}w  {title}")
    print(f"TOTAL {total}w")
    readme = f"""# Easyway Smoking Reference — *The Illustrated Easy Way to Stop Smoking*

Chapter-level extraction of the real book, from
`analysis/reference-books/The Illustrated Easy Way to Stop Smoking (Arcturus 2011).pdf`.

**Edition:** Allen Carr / Bev Aisbett illustrated edition (copyright 2006;
this scan: Arcturus 2013 reprint, ISBN 978-1-84837-930-5). This is the
short illustrated smoker's guide, not the original long *Easy Way to Stop
Smoking*. ~{total:,} extractable words. Illustration OCR noise was stripped;
speech-bubble lines were kept when they were readable English.

- `00-introduction.md` — About Easyway
- `chapter-01.md` … `chapter-08.md` — spine order from the printed contents
- Front matter (cover, title, dedication, copyright, TOC) and back matter
  (clinics list, other publications) are omitted — they are not judging material.

| File | Title | Words |
|---|---|---|
"""
    for filename, title, words in rows:
        readme += f"| `{filename}` | {title} | {words} |\n"
    readme += """
Read-only. Never edited by the loop. Chapter mapping to our book is
content-based via `loop/reference-alignment-quit-smoking.md` — never
mechanical offset.
"""
    (OUT / "README.md").write_text(readme)


if __name__ == "__main__":
    main()
