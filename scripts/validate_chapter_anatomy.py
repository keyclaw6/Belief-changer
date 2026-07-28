#!/usr/bin/env python3
"""Chapter anatomy validity gate for the auto-tuning loop (loop/PROGRAM.md).

Checks the mechanical FACTS of the writer contract so judges never have to:
anatomy presence, assigned instruction/mantras verbatim, banned register,
and the verbatim-repetition law (within chapter and across the book).
Judges evaluate effect; this gate checks presence.

Usage:
  python3 scripts/validate_chapter_anatomy.py --manifest MANIFEST.json \
      --chapters-dir production-books/quit-sugar/chapters [--chapter NN]

Manifest (built by the orchestrator from the accepted master plan):
{
  "banned": ["give up", "resist", ...],
  "instructions": [{"chapter": 3, "wording": "EXACT FROZEN TEXT"}],
  "mantras": [{"wording": "exact frozen text", "debut": 2, "echoes": [5, 9]}]
}

Exit code 0 when no FAIL (WARNs allowed); 1 otherwise. JSON report to stdout.
"""
import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_BANNED = [
    "give up", "resist", "stay strong", "discipline", "abstain",
    "trying to stop", "one day at a time", "recovery journey",
]
MIN_DUP_WORDS = 8  # sentences shorter than this are not "striking prose"


def sentences(text):
    for s in re.split(r"(?<=[.!?])\s+|\n+", text):
        s = re.sub(r"\s+", " ", s).strip()
        if len(s.split()) >= MIN_DUP_WORDS:
            yield s.lower()


def body_text(text):
    """Chapter text minus licensed recap zones (preview + SUMMARY)."""
    text = re.sub(r"(?is)##?\s*\**IN THIS CHAPTER\**.*?(?=\n#|\n\n[A-Z*])", "", text)
    text = re.sub(r"(?is)##?\s*\**SUMMARY\**.*\Z", "", text)
    return text


def check_chapter(num, text, manifest, prior_bodies):
    checks = []

    def add(name, ok, detail="", warn=False):
        checks.append({
            "check": name,
            "status": "PASS" if ok else ("WARN" if warn else "FAIL"),
            "detail": detail if not ok else "",
        })

    add("preview", re.search(r"IN THIS CHAPTER", text) is not None,
        "no IN THIS CHAPTER preview")
    add("summary", re.search(r"(?i)^#{0,3}\s*\**SUMMARY\**", text, re.M) is not None,
        "no SUMMARY section")
    add("thesis", re.search(r"(?m)^\*[^*\n][^\n]*\*\s*$", text[:3000]) is not None,
        "no italic thesis line found near the top", warn=True)

    for inst in manifest.get("instructions", []):
        if inst.get("chapter") == num:
            add("assigned-instruction", inst["wording"] in text,
                f"assigned instruction missing verbatim: {inst['wording'][:60]}…")

    for m in manifest.get("mantras", []):
        slots = [m.get("debut")] + list(m.get("echoes", []))
        if num in slots:
            add("assigned-mantra", m["wording"] in text,
                f"assigned mantra missing verbatim: {m['wording'][:60]}…")

    banned = manifest.get("banned", DEFAULT_BANNED)
    hits = sorted({b for b in banned
                   if re.search(rf"(?i)\b{re.escape(b)}\b", text)})
    add("banned-register", not hits,
        f"banned-register hits (verify each exposes the illusion/wrong "
        f"method, else FAIL): {hits}", warn=True)

    protected = [m["wording"].lower() for m in manifest.get("mantras", [])]
    protected += [i["wording"].lower() for i in manifest.get("instructions", [])]
    body = body_text(text)
    seen, dups = set(), set()
    for s in sentences(body):
        if any(p in s for p in protected):
            continue
        (dups if s in seen else seen).add(s)
    add("verbatim-repetition-within", not dups,
        f"{len(dups)} non-mantra sentence(s) repeated verbatim within "
        f"chapter: {sorted(dups)[:2]}")

    cross = {s for s in sentences(body)
             if not any(p in s for p in protected)} & prior_bodies
    add("verbatim-repetition-across", not cross,
        f"{len(cross)} non-mantra sentence(s) repeated verbatim from an "
        f"earlier chapter: {sorted(cross)[:2]}")

    return checks, {s for s in sentences(body)
                    if not any(p in s for p in protected)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--chapters-dir", required=True)
    ap.add_argument("--chapter", type=int, default=None,
                    help="check one chapter (prior chapters still feed the "
                         "cross-repetition set)")
    args = ap.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    files = sorted(Path(args.chapters_dir).glob("chapter-*.md"))
    report, prior, failed = [], set(), False

    for f in files:
        num = int(re.search(r"(\d+)", f.stem).group(1))
        text = f.read_text(encoding="utf-8")
        if args.chapter is not None and num > args.chapter:
            break
        checks, own = check_chapter(num, text, manifest, prior)
        prior |= own
        if args.chapter is None or num == args.chapter:
            report.append({"chapter": num, "checks": checks})
            failed |= any(c["status"] == "FAIL" for c in checks)

    # Book-level mantra schedule coverage (full-book mode only)
    if args.chapter is None:
        texts = {int(re.search(r"(\d+)", f.stem).group(1)):
                 f.read_text(encoding="utf-8") for f in files}
        schedule = []
        for m in manifest.get("mantras", []):
            for ch in [m.get("debut")] + list(m.get("echoes", [])):
                if ch is not None and m["wording"] not in texts.get(ch, ""):
                    schedule.append(
                        {"check": "mantra-schedule", "status": "FAIL",
                         "detail": f"ch {ch} missing: {m['wording'][:60]}…"})
                    failed = True
        report.append({"chapter": "book", "checks": schedule or
                       [{"check": "mantra-schedule", "status": "PASS",
                         "detail": ""}]})

    print(json.dumps(report, indent=2))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
