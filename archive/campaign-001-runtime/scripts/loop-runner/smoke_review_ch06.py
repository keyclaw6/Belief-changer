#!/usr/bin/env python3
"""Scratch smoke: review 019 CH-06 (1064w / 4800) and one rewrite if REVISE."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from muse_client import call_muse
from write_replicate import parse_budget, review_prompt, rewrite_prompt, word_count

REPO = Path(os.environ.get("BC_REPO", "/home/kab/Belief-changer"))
OUT = REPO / "loop/preflight/runs-2026-09-04-reviewer-ch06-smoke"
SRC = REPO / "loop/iterations/019/replicate-a"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    reviewer = (REPO / "prompts/chapter-reviewer.md").read_text()
    writer = (REPO / "prompts/chapter-writer.md").read_text()
    plan = (REPO / "production-books/quit-sugar/master-plan.md").read_text()
    style = (REPO / "prompts/style-guide.md").read_text()
    card = (SRC / "traces/chapter-06/chapter-card.md").read_text()
    draft = (SRC / "chapters/chapter-06.md").read_text()
    prev = (SRC / "chapters/chapter-05.md").read_text()
    budget = parse_budget(card, plan, 6)
    words_draft = word_count(draft)
    rprompt = review_prompt(reviewer, plan, card, draft, words_draft, budget)
    (OUT / "review-prompt.md").write_text(rprompt)
    leaked = re.findall(r"calibration/reference|chapter-\d{2}\.md", rprompt)
    if leaked:
        raise SystemExit(f"reviewer prompt leaked reference: {leaked}")
    review, rroute, rmeta = call_muse(rprompt, reasoning="high")
    (OUT / "review.md").write_text(review)
    verdict = review.strip().splitlines()[0].strip().upper() if review.strip() else "REVISE"
    print(f"REVIEW {verdict.split()[0]} draft={words_draft}w budget={budget} {rroute}", flush=True)
    text = draft
    if not verdict.startswith("ACCEPT"):
        wprompt = rewrite_prompt(writer, plan, style, card, prev, 6, draft, review)
        (OUT / "rewrite-prompt.md").write_text(wprompt)
        text, wroute, wmeta = call_muse(wprompt)
        (OUT / "rewrite.md").write_text(text)
        print(f"REWRITE {word_count(text)}w {wroute} {wmeta.get('latency_s')}s", flush=True)
    else:
        wroute = None
        wmeta = {}
    words_final = word_count(text)
    lo, hi = int(budget * 0.85), int(budget * 1.15)
    meta = {
        "words_draft": words_draft,
        "words_final": words_final,
        "budget": budget,
        "band": [lo, hi],
        "in_band": lo <= words_final <= hi,
        "review_verdict": verdict.split()[0],
        "review_route": rroute,
        "rewrite_route": wroute,
        "review_latency_s": rmeta.get("latency_s"),
        "rewrite_latency_s": wmeta.get("latency_s"),
        "review_prompt_has_gsbs": False,
    }
    (OUT / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"SMOKE {'OK' if meta['in_band'] else 'OUT-OF-BAND'} {words_final}w band={lo}-{hi}", flush=True)
    if not meta["in_band"]:
        raise SystemExit("final word count outside ±15% of budget")


if __name__ == "__main__":
    main()
