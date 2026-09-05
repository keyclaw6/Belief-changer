#!/usr/bin/env python3
"""Split the US Easyway smoking PDF into GSBS-style chapter files.

Source: Allen Carr's Easyway to Stop Smoking, Clarity Marketing US edition
(2011, ISBN 978-0-6154-8215-6). Not the illustrated Aisbett edition.

Spine kept as judging material:
  00-introduction.md  Preface + Warning + Introduction (Foreword omitted)
  chapter-01.md … chapter-45.md  literal numbered chapters
  chapter-46.md  Final Instructions (GSBS Ch20 analogue)

Omitted: copyright, dedication, TOC, Foreword (not Carr), Tell Easyway,
About the Author, Testimonials, Centers.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/kab/Belief-changer")
PDF_NAME = "Allen Carr's Easyway to Stop Smoking (Clarity 2011 US).pdf"
PDF = REPO / "analysis/reference-books" / PDF_NAME
OUT = REPO / "calibration/reference/easyway-smoking"
PAGES = Path("/tmp/easyway-us/pages")

UPLOAD = Path(
    "/home/kab/.cursor/projects/home-kab/uploads/"
    "Allen_Carr_s_Easyway_to_Stop_Smoking_--_Carr__Allen_--_0_"
    "--_Clarity_Marteting_USA_--_5ac0c37b85d703b93441d0fc812811ae_"
    "--_Anna_s_Archive_2ef0.pdf"
)

TITLES = {
    1: "THE WORST NICOTINE ADDICT I EVER MET",
    2: "THE EASYWAY",
    3: "WHY IS IT DIFFICULT TO STOP?",
    4: "THE SINISTER TRAP",
    5: "WHY WE SMOKE",
    6: "NICOTINE ADDICTION",
    7: "BRAINWASHING AND THE SLEEPING PARTNER",
    8: "RELIEVING WITHDRAWAL PANGS",
    9: "STRESS",
    10: "BOREDOM",
    11: "CONCENTRATION",
    12: "RELAXATION",
    13: "COMBINATION CIGARETTES",
    14: "WHAT AM I GIVING UP?",
    15: "SELF-IMPOSED SLAVERY",
    16: "I'LL SAVE $X EVERY WEEK",
    17: "HEALTH",
    18: "ENERGY",
    19: "IT RELAXES ME AND GIVES ME CONFIDENCE",
    20: "THOSE SINISTER BLACK SHADOWS",
    21: "THE ADVANTAGES OF BEING A SMOKER",
    22: "THE WILLPOWER METHOD OF STOPPING",
    23: "BEWARE OF CUTTING DOWN",
    24: "JUST ONE CIGARETTE",
    25: "CASUAL SMOKERS, TEENAGERS, NON-SMOKERS",
    26: "THE SECRET SMOKER",
    27: "A SOCIAL HABIT?",
    28: "TIMING",
    29: "WILL I MISS THE CIGARETTE?",
    30: "WILL I PUT ON WEIGHT?",
    31: "AVOID FALSE INCENTIVES",
    32: "THE EASY WAY TO STOP SMOKING",
    33: "THE WITHDRAWAL PERIOD",
    34: "JUST ONE DRAG",
    35: "WILL IT BE HARDER FOR ME?",
    36: "THE MAIN REASONS FOR FAILURE",
    37: "SUBSTITUTES",
    38: "SHOULD I AVOID TEMPTATION?",
    39: "THE MOMENT OF REVELATION",
    40: "THE FINAL CIGARETTE",
    41: "A FINAL WARNING",
    42: "OVER TWENTY YEARS OF FEEDBACK",
    43: "HELP THE SMOKER LEFT ON THE SINKING SHIP",
    44: "ADVICE TO NON-SMOKERS",
    45: "FINALE: HELP END THIS SCANDAL",
}

CHAPTER_RE = re.compile(r"^\s*CHAPTER\s*(\d+)\s*$", re.I)
FRONT_RE = re.compile(r"^\s*(PREFACE|WARNING|INTRODUCTION)\s*$", re.I)
FOREWORD_RE = re.compile(r"^\s*FOREWORD TO THE US EDITION\s*$", re.I)
FINAL_RE = re.compile(r"^\s*FINAL INSTRUCTIONS\s*$", re.I)
BACK_RE = re.compile(
    r"^\s*TELL ALLEN CARR|^\s*ABOUT THE AUTHOR\s*$|^\s*TESTIMONIALS\s*$"
    r"|^\s*ALLEN CARR'S EASYWAY CENTERS",
    re.I,
)
PAGE_NUM = re.compile(r"^\d{1,3}$")


def ensure_pdf() -> Path:
    PDF.parent.mkdir(parents=True, exist_ok=True)
    if not PDF.exists():
        if not UPLOAD.exists():
            raise SystemExit(f"missing source PDF: {UPLOAD}")
        shutil.copy2(UPLOAD, PDF)
        print(f"copied PDF → {PDF}")
    return PDF


def dump_pages(pdf: Path) -> None:
    PAGES.mkdir(parents=True, exist_ok=True)
    info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
    pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    for n in range(1, pages + 1):
        dest = PAGES / f"p{n:03d}.txt"
        subprocess.check_call(
            ["pdftotext", "-layout", "-f", str(n), "-l", str(n), str(pdf), str(dest)]
        )


def page_lines(n: int) -> list[str]:
    raw = (PAGES / f"p{n:03d}.txt").read_text(errors="replace")
    raw = raw.replace("\f", "")
    return [ln.rstrip() for ln in raw.splitlines()]


def is_title_line(s: str) -> bool:
    t = s.strip()
    if not t:
        return False
    letters = "".join(c for c in t if c.isalpha())
    if len(letters) < 3:
        return False
    return letters.isupper()


def marker_at(s: str) -> tuple[str, int | None] | None:
    m = CHAPTER_RE.match(s)
    if m:
        return ("chapter", int(m.group(1)))
    m = FRONT_RE.match(s)
    if m:
        return (m.group(1).lower(), None)
    if FOREWORD_RE.match(s):
        return ("foreword", None)
    if FINAL_RE.match(s):
        return ("final", 46)
    if BACK_RE.search(s):
        return ("back", None)
    return None


def collect_markers() -> list[tuple[int, int, str, int | None]]:
    """(page, line_index, kind, chapter_num_or_none) in reading order."""
    found: list[tuple[int, int, str, int | None]] = []
    for n in range(1, 200):
        p = PAGES / f"p{n:03d}.txt"
        if not p.exists():
            break
        for i, ln in enumerate(page_lines(n)):
            mark = marker_at(ln)
            if mark:
                found.append((n, i, mark[0], mark[1]))
    return found


def slice_lines(start: tuple[int, int], end: tuple[int, int] | None) -> list[str]:
    """Lines after start marker until end marker (exclusive)."""
    sp, si = start
    if end is None:
        ep, ei = 999, 0
    else:
        ep, ei = end
    out: list[str] = []
    n = sp
    while n <= 199:
        p = PAGES / f"p{n:03d}.txt"
        if not p.exists():
            break
        lines = page_lines(n)
        for i, ln in enumerate(lines):
            if n == sp and i <= si:
                continue
            if n == ep and i >= ei:
                return out
            out.append(ln)
        n += 1
    return out


KEEP_HYPHEN_PREFIX = {"ex", "non", "pre", "re", "co", "un", "self"}
SOFT_SUFFIX = {
    "ly", "ing", "ed", "tion", "sion", "ness", "ment", "ers", "ies", "est",
    "ful", "ous", "ive", "ize", "ised", "ized", "ally", "ence", "ance",
}


def drop_title(lines: list[str], expected: str | None) -> tuple[str, list[str]]:
    """Peel ALL-CAPS title lines; return (canonical title, remaining)."""
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    while i < len(lines) and is_title_line(lines[i]):
        i += 1
        while i < len(lines) and not lines[i].strip():
            i += 1
    return (expected or ""), lines[i:]


def join_wrapped(a: str, b: str) -> str:
    if not (a.endswith("-") and b and b[0].islower()):
        return a + " " + b
    left_m = re.search(r"([A-Za-z]+)-$", a)
    right_m = re.match(r"([a-z]+)", b)
    if not left_m or not right_m:
        return a[:-1] + b
    left, right = left_m.group(1), right_m.group(1)
    if left.lower() in KEEP_HYPHEN_PREFIX:
        return a + b
    if len(left) <= 3 or right.lower() in SOFT_SUFFIX or len(right) <= 2:
        return a[:-1] + b
    return a + b


def indent_of(ln: str) -> int:
    return len(ln) - len(ln.lstrip(" "))


def is_all_caps_block(s: str) -> bool:
    letters = "".join(c for c in s if c.isalpha())
    return bool(letters) and letters.isupper() and len(s.strip()) <= 80


def paragraphize(lines: list[str]) -> str:
    cleaned: list[str] = []
    for ln in lines:
        s = ln.replace("\f", "")
        if PAGE_NUM.match(s.strip()):
            continue
        cleaned.append(s)

    paras: list[str] = []
    buf: list[str] = []

    def flush() -> None:
        if not buf:
            return
        text = buf[0]
        for nxt in buf[1:]:
            text = join_wrapped(text, nxt)
        text = re.sub(r"[ \t]+", " ", text).strip()
        if text:
            paras.append(text)
        buf.clear()

    prev_blank = True
    for ln in cleaned:
        if not ln.strip():
            if buf:
                flush()
            prev_blank = True
            continue
        raw = ln
        s = ln.strip()
        ind = indent_of(raw)
        new_para = False
        if not buf:
            new_para = True
        elif re.match(r"^\d+\.\s", s):
            new_para = True
        elif ind >= 5 and not (s[:1].islower() and buf and not buf[-1].endswith((".", "!", "?"))):
            new_para = True
        elif ind == 4 and buf:
            last = buf[-1]
            if last.endswith((".", "!", "?", ":", ".”", ".’", '"', "'")) or prev_blank:
                new_para = True
        if new_para and buf:
            flush()
        buf.append(s)
        prev_blank = False
    flush()

    # Collapse consecutive short ALL-CAPS shout lines into one block.
    merged: list[str] = []
    cap_buf: list[str] = []

    def flush_caps() -> None:
        if cap_buf:
            merged.append("\n".join(cap_buf))
            cap_buf.clear()

    for p in paras:
        if is_all_caps_block(p) and "\n" not in p:
            cap_buf.append(p)
            continue
        flush_caps()
        merged.append(p)
    flush_caps()
    return "\n\n".join(merged)


def chapter_md(num: int, title: str, body: str) -> str:
    body = body.rstrip()
    if body:
        return f"# Chapter {num}\n\n# {title}\n\n{body}\n"
    return f"# Chapter {num}\n\n# {title}\n"


def intro_md(preface: str, warning: str, introduction: str) -> str:
    return (
        "# INTRODUCTION\n\n"
        "## PREFACE\n\n"
        f"{preface.rstrip()}\n\n"
        "## WARNING\n\n"
        f"{warning.rstrip()}\n\n"
        "## INTRODUCTION\n\n"
        f"{introduction.rstrip()}\n"
    )


def main() -> None:
    pdf = ensure_pdf()
    dump_pages(pdf)
    markers = collect_markers()
    by_kind: dict[str, list[tuple[int, int, str, int | None]]] = {}
    chapters: dict[int, tuple[int, int]] = {}
    for page, idx, kind, num in markers:
        by_kind.setdefault(kind, []).append((page, idx, kind, num))
        if kind == "chapter" and num is not None:
            if num in chapters:
                continue  # first occurrence is the header
            chapters[num] = (page, idx)
        if kind == "final":
            chapters[46] = (page, idx)

    missing = [n for n in range(1, 46) if n not in chapters]
    if missing:
        raise SystemExit(f"missing chapter headers: {missing}")
    if 46 not in chapters:
        raise SystemExit("missing FINAL INSTRUCTIONS")
    for name in ("preface", "warning", "introduction"):
        if name not in by_kind:
            raise SystemExit(f"missing {name} header")

    # Ordered starts for slicing: only first TOC-free body markers.
    starts: list[tuple[int, int, str, int | None]] = []
    seen_ch: set[int] = set()
    for page, idx, kind, num in markers:
        if kind == "foreword":
            continue
        if kind == "back":
            # TOC echoes "Tell Allen Carr…" on page 6; real back matter is after
            # Final Instructions (~p174).
            if page < 170:
                continue
            starts.append((page, idx, kind, num))
            break
        if kind == "chapter":
            if num in seen_ch:
                continue
            seen_ch.add(num)
            starts.append((page, idx, kind, num))
            continue
        if kind in {"preface", "warning", "introduction", "final"}:
            # Skip TOC echoes: real headers are the later ones (page >= 10).
            if page < 10:
                continue
            starts.append((page, idx, kind, num))

    def next_start(i: int) -> tuple[int, int] | None:
        if i + 1 >= len(starts):
            return None
        return starts[i + 1][0], starts[i + 1][1]

    bodies: dict[str, str] = {}
    titles_out: dict[int, str] = {}
    for i, (page, idx, kind, num) in enumerate(starts):
        if kind == "back":
            break
        raw = slice_lines((page, idx), next_start(i))
        if kind == "chapter" and num is not None:
            title, rest = drop_title(raw, TITLES[num])
            titles_out[num] = title or TITLES[num]
            bodies[f"ch{num}"] = paragraphize(rest)
        elif kind == "final":
            title, rest = drop_title(raw, "FINAL INSTRUCTIONS")
            titles_out[46] = "FINAL INSTRUCTIONS"
            bodies["ch46"] = paragraphize(rest)
        elif kind in {"preface", "warning", "introduction"}:
            bodies[kind] = paragraphize(raw)

    # Wipe previous (illustrated) extract so no leftover chapter files remain.
    if OUT.exists():
        for p in OUT.glob("*.md"):
            p.unlink()
    OUT.mkdir(parents=True, exist_ok=True)

    intro = intro_md(bodies["preface"], bodies["warning"], bodies["introduction"])
    (OUT / "00-introduction.md").write_text(intro)

    rows: list[tuple[str, str, int]] = []
    intro_words = len(intro.split())
    rows.append(("00-introduction.md", "Preface + Warning + Introduction", intro_words))
    total = intro_words
    for n in range(1, 47):
        title = titles_out.get(n, TITLES.get(n, "FINAL INSTRUCTIONS"))
        if n == 46:
            title = "FINAL INSTRUCTIONS"
        md = chapter_md(n, title, bodies.get(f"ch{n}", ""))
        name = f"chapter-{n:02d}.md"
        (OUT / name).write_text(md)
        words = len(md.split())
        total += words
        rows.append((name, title, words))
        print(f"{name:22} {words:5}w  {title}")

    print(f"TOTAL {total}w")
    if not (50_000 <= total <= 70_000):
        raise SystemExit(f"judged-body word count {total} outside 50k–70k")
    # Ch21 is a one-line gag; allow empty-ish body.
    if len(bodies.get("ch21", "").split()) > 80:
        print("note: chapter 21 longer than the expected gag", file=sys.stderr)
    if "FOREWORD" in intro.upper() and "Allen Carr saved my life" in intro:
        raise SystemExit("foreword leaked into introduction")

    readme = f"""# Easyway Smoking Reference — *Allen Carr’s Easyway to Stop Smoking*

Chapter-level extraction of the real US book, from
`analysis/reference-books/{PDF_NAME}`.

**Edition:** Allen Carr, Clarity Marketing US edition (2011),
ISBN 978-0-6154-8215-6, LCCN 2011933692. Letter, 199 pages.
This is the long Easyway smoking book the judges compare against —
not the illustrated Aisbett/Arcturus edition.

~{total:,} judged-body words. Foreword (Damian O’Hara, not Carr’s voice)
and back matter are omitted.

- `00-introduction.md` — Preface, Warning, Introduction (three `##` sections)
- `chapter-01.md` … `chapter-45.md` — the 45 numbered chapters, unmerged
- `chapter-46.md` — Final Instructions (GSBS chapter-20 analogue)

Our produced smoking book stays ~13 chapters. Alignment is many-to-one
via `loop/reference-alignment-quit-smoking.md` — never mechanical offset.

| File | Title | Words |
|---|---|---|
"""
    for filename, title, words in rows:
        readme += f"| `{filename}` | {title} | {words} |\n"
    readme += """
Read-only. Never edited by the loop.
"""
    (OUT / "README.md").write_text(readme)


if __name__ == "__main__":
    main()
