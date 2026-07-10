"""Shared helpers for the calibration eval suite (scripts/eval/). stdlib only.

Both the generated book and the reference pass through the SAME functions, so
systematic tokenizer noise (abbreviation splits etc.) cancels out in comparisons.
"""
import re
from pathlib import Path

WORD_RE = re.compile(r"[A-Za-z0-9']+")
QUOTE_RE = re.compile(r'"([^"]+)"|“([^”]+)”')  # straight or curly

_MD_PATTERNS = [
    (re.compile(r"```.*?```", re.S), " "),          # code fences
    (re.compile(r"!\[[^\]]*\]\([^)]*\)"), " "),     # images
    (re.compile(r"\[([^\]]+)\]\([^)]*\)"), r"\1"),  # links -> text
    (re.compile(r"<[^>]+>"), " "),                  # html tags
    (re.compile(r"^\s{0,3}#{1,6}\s*", re.M), ""),   # heading markers (keep text)
    (re.compile(r"^\s{0,3}>\s?", re.M), ""),        # blockquote markers
    (re.compile(r"[*_]{1,3}([^*_]+)[*_]{1,3}"), r"\1"),  # emphasis -> text
    (re.compile(r"^\s*[-*+]\s+", re.M), ""),        # list bullets
    (re.compile(r"^\s*-{3,}\s*$", re.M), " "),      # hrules
]


def strip_markdown(text: str) -> str:
    for pat, rep in _MD_PATTERNS:
        text = pat.sub(rep, text)
    return text


def collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def words(text: str) -> list:
    return WORD_RE.findall(text.lower())


def sentences(text: str) -> list:
    """Crude sentence split; identical noise on both sides of any comparison."""
    flat = collapse_ws(text)
    parts = re.split(r"(?<=[.!?])\s+", flat)
    return [p for p in parts if WORD_RE.search(p)]


def paragraphs(text: str) -> list:
    parts = re.split(r"\n\s*\n", text)
    return [p for p in parts if WORD_RE.search(p)]


def shingles(tokens: list, n: int) -> list:
    return [" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def _sort_key(path: Path):
    m = re.search(r"(\d+)", path.stem)
    return (0, int(m.group(1)), path.stem) if m else (1, 0, path.stem)


def load_chapters(dirpath, exts=(".md", ".txt")) -> list:
    """Return [(name, raw_text)] for chapter files in dirpath, numeric order.

    Skips README* and hidden files. Raises SystemExit with a clear message if
    the directory is missing or empty (fail loud, per repo harness rules).
    """
    d = Path(dirpath)
    if not d.is_dir():
        raise SystemExit(f"evallib: chapter dir not found: {d}")
    files = [p for p in d.iterdir() if p.suffix.lower() in exts
             and not p.name.lower().startswith("readme") and not p.name.startswith(".")]
    files.sort(key=_sort_key)
    if not files:
        raise SystemExit(f"evallib: no chapter files in {d}")
    return [(p.name, p.read_text(encoding="utf-8", errors="replace")) for p in files]


def parse_range(spec: str, upper: int) -> list:
    """Parse a chapter selection; reject any invalid explicit selection."""
    if spec is None:
        return list(range(1, upper + 1))
    if not spec.strip():
        raise SystemExit("evallib: --chapters selection is empty")

    out = []
    for raw in spec.split(","):
        part = raw.strip()
        if not part:
            raise SystemExit(f"evallib: invalid --chapters selection: {spec!r}")
        match = re.fullmatch(r"(\d+)\s*-\s*(\d+)", part)
        if match:
            start, end = (int(value) for value in match.groups())
            if start > end:
                raise SystemExit(f"evallib: descending --chapters range: {part!r}")
            out.extend(range(start, end + 1))
        elif part.isdigit():
            out.append(int(part))
        else:
            raise SystemExit(f"evallib: invalid --chapters selection: {part!r}")

    unavailable = sorted({chapter for chapter in out if not 1 <= chapter <= upper})
    if unavailable:
        raise SystemExit(
            f"evallib: requested chapter(s) unavailable (have 1-{upper}): {unavailable}"
        )
    return out


def first_quoted(line: str):
    m = QUOTE_RE.search(line)
    if not m:
        return None
    return m.group(1) if m.group(1) is not None else m.group(2)
