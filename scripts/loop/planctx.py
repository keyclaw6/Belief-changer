"""Plan-context extraction + near-copy detection for the loop (stdlib only).

planctx feeds the judge tasks the candidate-side context they need to score
the repetition/mantra system and instruction slots (review finding C2-rubric),
and supplies the near-copy hard check that catches paraphrase-spaced copying
which defeats exact 12-gram shingles (review finding C4).
"""
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "eval"))
import evallib as E  # noqa: E402

_SHEET_HEAD = re.compile(r"^(#{2,4})[^\n]*mantra sheet[^\n]*$", re.I | re.M)
_ANY_HEAD = re.compile(r"^#{2,4}\s", re.M)
_CARD_NEXT = re.compile(r"^(?:###\s+CH-|##\s)", re.M)

CONTROL_CTX = ('none provided (control run) — score repetition_mantra on '
               'within-chapter refrain discipline and an evident fixed-phrase '
               'system; score the instruction slot only if one is evident.')


def _slice_from(text: str, start: int, stop_re, limit: int) -> str:
    tail = text[start:]
    nl = tail.find("\n")
    nxt = stop_re.search(tail, nl + 1 if nl >= 0 else 1)
    out = tail[: nxt.start()] if nxt else tail
    return out.strip()[:limit]


def extract_mantra_sheet(plan_text: str, limit: int = 5000) -> str:
    m = _SHEET_HEAD.search(plan_text or "")
    if not m:
        return ""
    return _slice_from(plan_text, m.start(), _ANY_HEAD, limit)


def extract_card(plan_text: str, n: int, limit: int = 2500) -> str:
    m = re.search(rf"^###\s+CH-0*{n}\b", plan_text or "", re.M)
    if not m:
        return ""
    return _slice_from(plan_text, m.start(), _CARD_NEXT, limit)


def build_ctx(plan_text: str, n: int, control: bool) -> str:
    if control or not plan_text:
        return CONTROL_CTX
    sheet = extract_mantra_sheet(plan_text)
    card = extract_card(plan_text, n)
    return ("MANTRA SHEET (frozen wordings + debut/echo schedule):\n"
            f"{sheet or '(mantra sheet not found in plan)'}\n\n"
            "THIS CHAPTER'S PLAN CARD (job, assignments, budget):\n"
            f"{card or '(chapter card not found in plan)'}")


def build_pairs(ours_chapters, ref_chapters, sel, offset, plan_text="",
                control=False):
    """(label, ours_text, ref_text, ctx) per selected chapter."""
    pairs = []
    for n in sel:
        ref_pos = n + offset
        if ref_pos > len(ref_chapters):
            continue
        ours_text = E.strip_markdown(ours_chapters[n - 1][1])
        ref_text = ref_chapters[ref_pos - 1][1]
        pairs.append((f"ch{n:02d}", ours_text, ref_text,
                      build_ctx(plan_text, n, control)))
    return pairs


def near_copy_ratio(ours_text: str, ref_text: str) -> float:
    """Word-sequence similarity (0..1). Original same-topic prose sits far
    below 0.5; a reference copy with one token edited every ~11 words stays
    high — exactly the evasion exact-12-gram shingles miss."""
    a, b = E.words(ours_text), E.words(ref_text)
    if not a or not b:
        return 0.0
    return round(difflib.SequenceMatcher(None, a, b, autojunk=False).ratio(), 4)
