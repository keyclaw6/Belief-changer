"""Verify the master plan's mantra sheet is executed in the chapters.

Checks, per mantra parsed from the plan's mantra sheet:
  - frozen wording appears VERBATIM (whitespace-normalized, case-sensitive)
    in its debut chapter;
  - it appears in every scheduled chapter within the checked range;
  - every chapter in range contains at least one mantra (debut or echo).

Parses mantra-sheet lines of the form:
  - **[archetype] — FROZEN WORDING:** "exact words" | ... debut: ch. N | schedule: ...

Usage:
  python3 scripts/eval/mantra_check.py --plan production-books/quit-sugar/master-plan.md \
      --book production-books/quit-sugar/chapters [--chapters 1-3] [--json OUT.json]
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import evallib as E

DEBUT_RE = re.compile(r"debut:?\**\s*ch\.?\s*(\d+)", re.I)
SCHED_RE = re.compile(r"schedule:?\**\s*([^|]*)", re.I)
ALL_WORDS = ("every chapter", "all chapters", "each chapter")


def parse_mantra_sheet(plan_text: str) -> list:
    mantras = []
    for line in plan_text.splitlines():
        if "frozen wording" not in line.lower():
            continue
        wording = E.first_quoted(line)
        if not wording or "<" in wording:  # unfilled template placeholder
            continue
        if not DEBUT_RE.search(line):  # a filled sheet entry always carries a debut
            continue
        head = re.split(r"frozen wording", line, flags=re.I)[0]
        archetype = re.sub(r"[*\[\]—:\-]+", " ", head).strip() or "unnamed"
        debut_m = DEBUT_RE.search(line)
        sched_m = SCHED_RE.search(line)
        sched_txt = sched_m.group(1).strip() if sched_m else ""
        schedule = ("all" if any(k in sched_txt.lower() for k in ALL_WORDS)
                    else [int(x) for x in re.findall(r"\d+", sched_txt)])
        mantras.append({"archetype": archetype, "wording": E.collapse_ws(wording),
                        "debut": int(debut_m.group(1)) if debut_m else None,
                        "schedule": schedule, "schedule_raw": sched_txt})
    return mantras


def _normalize_for_match(raw: str) -> str:
    text = E.strip_markdown(raw)
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    return E.collapse_ws(text)


def verify(mantras, chapters, chapter_sel) -> dict:
    norm = {i: _normalize_for_match(raw) for i, (_, raw) in enumerate(chapters, 1)}
    in_range = [i for i in norm if i in chapter_sel]
    results, failures = [], []
    for m in mantras:
        wording = m["wording"].replace("’", "'")
        present = sorted(i for i in in_range if wording in norm[i])
        counts = {i: norm[i].count(wording) for i in present}
        r = {"archetype": m["archetype"], "wording": wording,
             "debut": m["debut"], "schedule": m["schedule"],
             "found_in": present, "counts": counts}
        if m["debut"] and m["debut"] in chapter_sel and m["debut"] not in present:
            failures.append(f"debut missing: '{wording[:50]}' not verbatim in ch {m['debut']}")
        sched = (in_range if m["schedule"] == "all"
                 else [c for c in (m["schedule"] or []) if c in chapter_sel])
        missing = [c for c in sched if c not in present]
        if missing:
            failures.append(f"schedule missing: '{wording[:50]}' absent from ch {missing}")
        results.append(r)
    bare = [i for i in in_range
            if not any(i in r["found_in"] for r in results)]
    if mantras and bare:
        failures.append(f"chapters with NO mantra (law: every chapter debuts or echoes one): {bare}")
    return {"mantras": results, "chapters_checked": in_range,
            "chapters_without_mantra": bare, "failures": failures}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--book", required=True)
    ap.add_argument("--chapters", default=None)
    ap.add_argument("--json", dest="json_out")
    a = ap.parse_args()

    plan_path = Path(a.plan)
    if not plan_path.is_file():
        print(f"[mantra] FAIL: plan not found: {plan_path}")
        sys.exit(2)
    plan_text = plan_path.read_text(encoding="utf-8", errors="replace")
    mantras = parse_mantra_sheet(plan_text)
    chapters = E.load_chapters(a.book)
    sel = E.parse_range(a.chapters, len(chapters))
    if not mantras:
        print("[mantra] FAIL: no filled mantra-sheet lines parsed from plan "
              "(template unfilled, or format drifted — fix the plan or the parser)")
        sys.exit(2)
    res = verify(mantras, chapters, sel)
    print(f"[mantra] {len(mantras)} mantras parsed | chapters checked: {res['chapters_checked']}")
    for r in res["mantras"]:
        print(f"  '{r['wording'][:55]}' debut ch{r['debut']} -> found in {r['found_in']}")
    for f in res["failures"]:
        print(f"  FAIL: {f}")
    if a.json_out:
        Path(a.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json_out).write_text(json.dumps({"parsed": mantras, **res}, indent=1),
                                    encoding="utf-8")
    sys.exit(2 if res["failures"] else 0)


if __name__ == "__main__":
    main()
