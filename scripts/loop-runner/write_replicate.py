#!/usr/bin/env python3
"""Write quit-sugar chapters 01–18 for one replicate via Muse Spark (Zen, Vercel fallback)."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from muse_client import call_muse

REPO = Path(os.environ["BC_REPO"])
ITER = os.environ["ITER"]
REPLICATE = os.environ["REPLICATE"]  # a | b
SLUG = "quit-sugar"


def parse_cards(plan: str) -> dict[int, str]:
    m = re.search(r"## 7\. COMPACT CHAPTER CARDS\n(.*?)(?:\n## |\Z)", plan, re.S)
    if not m:
        raise SystemExit("no compact chapter cards")
    block = m.group(1)
    cards: dict[int, str] = {}
    parts = re.split(r"\n(?=\*\*C\d{2} —)", "\n" + block)
    for part in parts:
        part = part.strip()
        if not part.startswith("**C"):
            continue
        nm = re.match(r"\*\*C(\d{2}) —", part)
        if not nm:
            continue
        cards[int(nm.group(1))] = part.strip() + "\n"
    if not cards:
        raise SystemExit("no chapter cards parsed")
    return cards


def book_core(plan: str) -> str:
    m = re.search(r"(## 1\. BOOK CORE\n.*?)(?=\n## 2\. )", plan, re.S)
    if not m:
        raise SystemExit("no book core")
    return m.group(1).rstrip() + "\n"


def assemble(writer: str, plan: str, style: str, card: str, prev: str, n: int) -> str:
    title = re.match(r"\*\*(C\d{2} — .+?)\*\*", card)
    title_s = title.group(1) if title else f"C{n:02d}"
    assignment = (
        f"Write {title_s} of `production-books/{SLUG}` as the complete chapter file. "
        "Your chapter's card is the authoritative semantic authority. Resolve every ID it cites "
        "against the plan-wide inventories in the master plan. Use the immediately previous chapter "
        "only for voice continuity and the handoff seam. Do not read or seek anything beyond these "
        "four inputs."
    )
    return (
        f"{writer.rstrip()}\n\n\n{assignment}\n\n"
        "### The accepted master plan (inventory authority — resolve every ID your card cites against it)\n"
        f"```\n{plan.rstrip()}\n```\n\n"
        "### Your chapter card (semantic authority for this chapter)\n"
        f"```\n{card.rstrip()}\n```\n\n"
        "### Style guide\n"
        f"```\n{style.rstrip()}\n```\n\n"
        "### Previous chapter\n"
        f"```\n{prev.rstrip()}\n```\n"
    )


def main() -> None:
    traces_root = REPO / "loop" / "iterations" / ITER / f"replicate-{REPLICATE}" / "traces"
    live_dir = REPO / "production-books" / SLUG / "chapters"
    live_dir.mkdir(parents=True, exist_ok=True)
    writer = (REPO / "prompts" / "chapter-writer.md").read_text()
    plan = (REPO / "production-books" / SLUG / "master-plan.md").read_text()
    style = (REPO / "prompts" / "style-guide.md").read_text()
    cards = parse_cards(plan)
    core = book_core(plan)
    (traces_root / "plan.md").parent.mkdir(parents=True, exist_ok=True)
    if not (traces_root / "plan.md").exists():
        (traces_root / "plan.md").write_text(plan)

    for n in sorted(cards):
        tdir = traces_root / f"chapter-{n:02d}"
        tdir.mkdir(parents=True, exist_ok=True)
        resp_path = tdir / "response.md"
        live_path = live_dir / f"chapter-{n:02d}.md"
        if resp_path.exists() and live_path.exists():
            print(f"SKIP chapter-{n:02d} already written")
            continue
        prev = core if n == 1 else (live_dir / f"chapter-{n-1:02d}.md").read_text()
        prompt = assemble(writer, plan, style, cards[n], prev, n)
        (tdir / "prompt.md").write_text(prompt)
        (tdir / "chapter-card.md").write_text(cards[n])
        text, route, meta = call_muse(prompt)
        if text.strip().startswith("ROUTE REFUSAL:"):
            (tdir / "refusal.md").write_text(text)
            raise SystemExit(f"refusal chapter-{n:02d}: {text[:200]}")
        partial = live_path.with_suffix(".md.partial")
        partial.write_text(text)
        partial.rename(live_path)
        resp_path.write_text(text)
        meta.update(
            {
                "chapter": n,
                "replicate": REPLICATE,
                "iteration": ITER,
                "chars": len(text),
            }
        )
        (tdir / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
        print(f"OK chapter-{n:02d} {meta['latency_s']}s {route} {len(text)}c", flush=True)


if __name__ == "__main__":
    main()
