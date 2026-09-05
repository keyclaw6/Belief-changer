#!/usr/bin/env python3
"""Write one subject's chapters via Muse Spark (Go → Zen → Vercel).

A1 loop: draft → review → rewrite until ACCEPT or K=3 rewrites.
After the third rewrite no further review runs; that rewrite is the chapter.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from muse_client import call_muse

REPO = Path(os.environ.get("BC_REPO", "/home/kab/Belief-changer"))
ITER = os.environ.get("ITER", "")
REPLICATE = os.environ.get("REPLICATE", "")  # a | b
SLUG = os.environ.get("SLUG", "quit-sugar")
MAX_REWRITES = 3

CARD_SPLIT = re.compile(r"\n(?=(?:#{1,3}\s+|\*\*)(?:CH-|C-)\d{1,2}\s+—)")
CARD_HEAD = re.compile(r"(?:#{1,3}\s+|\*\*)(?:CH-|C-)(\d{1,2})\s+—")
FINDING_HEAD = re.compile(
    r"^(JOB|MANTRA|INSTRUCTION|ID|LENGTHEN|SHORTEN|HEADER|STOPPED-SHORT|"
    r"UNASSIGNED-REFRAIN|RESERVED-REACH|RE-ARGUMENT|OVERCLAIM)\b",
    re.I | re.M,
)


def parse_cards(plan: str) -> dict[int, str]:
    m = re.search(r"## 7\. COMPACT CHAPTER CARDS\n(.*?)(?:\n## |\Z)", plan, re.S | re.I)
    block = m.group(1) if m else plan
    cards: dict[int, str] = {}
    for part in CARD_SPLIT.split("\n" + block):
        part = part.strip()
        nm = CARD_HEAD.match(part)
        if not nm:
            continue
        cards[int(nm.group(1))] = part + "\n"
    if not cards:
        raise SystemExit("no chapter cards parsed")
    return cards


def book_core(plan: str) -> str:
    m = re.search(r"(## 1\. BOOK CORE\n.*?)(?=\n## 2\. )", plan, re.S | re.I)
    if not m:
        raise SystemExit("no book core")
    return m.group(1).rstrip() + "\n"


def word_count(text: str) -> int:
    return len(text.split())


def parse_budget(card: str, plan: str, n: int) -> int:
    m = re.search(r"(?im)^(?:[-*]\s*)?budget:\s*(\d+)\s*$", card)
    if m:
        return int(m.group(1))
    m = re.search(rf"CH-{n:02d}\s+(\d+)", plan)
    if m:
        return int(m.group(1))
    m = re.search(rf"\bC{n:02d}\s+(\d+)", plan)
    if m:
        return int(m.group(1))
    raise SystemExit(f"no word budget for chapter {n}")


def finding_types(review: str) -> list[str]:
    return [m.group(1).upper() for m in FINDING_HEAD.finditer(review)]


def review_prompt(contract: str, plan: str, card: str, draft: str, n_words: int, budget: int) -> str:
    return (
        "You are the book factory chapter-reviewer, a fresh isolated role call.\n\n"
        "Follow this contract exactly:\n\n"
        f"{contract.rstrip()}\n\n"
        f"Delivered {n_words} words. Budget {budget}.\n\n"
        "### The accepted master plan\n"
        f"```\n{plan.rstrip()}\n```\n\n"
        "### This chapter's card\n"
        f"```\n{card.rstrip()}\n```\n\n"
        "### The draft chapter\n"
        f"```\n{draft.rstrip()}\n```\n"
    )


def rewrite_prompt(writer: str, plan: str, style: str, card: str, prev: str, n: int, draft: str, review: str) -> str:
    base = assemble(writer, plan, style, card, prev, n)
    return (
        f"{base.rstrip()}\n\n"
        "### Draft to revise\n"
        f"```\n{draft.rstrip()}\n```\n\n"
        "### Chapter-reviewer findings\n"
        "Findings are instructions to you, never text to print. "
        "Never surface finding names, ledger IDs, or grades in the chapter. "
        "Obey LENGTHEN/SHORTEN and listed gaps; do not add new jobs; "
        "do not continue into a reserved-later job.\n"
        f"```\n{review.rstrip()}\n```\n"
    )


def assemble(writer: str, plan: str, style: str, card: str, prev: str, n: int) -> str:
    title = re.search(r"(?:CH-|C-)\d{1,2}\s+—\s+.+", card.splitlines()[0] if card else "")
    title_s = title.group(0).strip(" *#") if title else f"C{n:02d}"
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


def replicate_root() -> Path:
    return REPO / "loop" / "iterations" / ITER / SLUG / f"replicate-{REPLICATE}"


def main() -> None:
    if not ITER or REPLICATE not in ("a", "b"):
        raise SystemExit("ITER and REPLICATE=a|b required")
    if not SLUG:
        raise SystemExit("SLUG required (quit-sugar | quit-smoking)")
    root = replicate_root()
    traces_root = root / "traces"
    chapters_dir = root / "chapters"
    chapters_dir.mkdir(parents=True, exist_ok=True)
    writer = (REPO / "prompts" / "chapter-writer.md").read_text()
    reviewer = (REPO / "prompts" / "chapter-reviewer.md").read_text()
    plan = (REPO / "production-books" / SLUG / "master-plan.md").read_text()
    style = (REPO / "prompts" / "style-guide.md").read_text()
    cards = parse_cards(plan)
    core = book_core(plan)
    traces_root.mkdir(parents=True, exist_ok=True)
    if not (traces_root / "plan.md").exists():
        (traces_root / "plan.md").write_text(plan)

    for n in sorted(cards):
        tdir = traces_root / f"chapter-{n:02d}"
        tdir.mkdir(parents=True, exist_ok=True)
        resp_path = tdir / "response.md"
        live_path = chapters_dir / f"chapter-{n:02d}.md"
        if resp_path.exists():
            if not live_path.exists():
                live_path.write_text(resp_path.read_text())
            print(f"SKIP chapter-{n:02d} already written")
            continue
        prev = core if n == 1 else (chapters_dir / f"chapter-{n-1:02d}.md").read_text()
        prompt = assemble(writer, plan, style, cards[n], prev, n)
        (tdir / "prompt.md").write_text(prompt)
        (tdir / "chapter-card.md").write_text(cards[n])
        draft, route, meta = call_muse(prompt)
        if draft.strip().startswith("ROUTE REFUSAL:"):
            (tdir / "refusal.md").write_text(draft)
            raise SystemExit(f"refusal chapter-{n:02d}: {draft[:200]}")
        (tdir / "draft.md").write_text(draft)
        budget = parse_budget(cards[n], plan, n)
        text = draft
        words_by_round = [word_count(draft)]
        review_verdicts: list[str] = []
        findings_by_round: list[list[str]] = []
        rewrite_routes: list[str | None] = []
        rewrite_latencies: list[float | None] = []
        review_routes: list[str | None] = []
        review_latencies: list[float | None] = []
        final_status = "ACCEPT"
        last_verdict = "ACCEPT"

        for rnd in range(1, MAX_REWRITES + 1):
            n_words = word_count(text)
            rprompt = review_prompt(reviewer, plan, cards[n], text, n_words, budget)
            (tdir / f"review-prompt-{rnd:02d}.md").write_text(rprompt)
            if rnd == 1:
                (tdir / "review-prompt.md").write_text(rprompt)
            review, rroute, rmeta = call_muse(rprompt, reasoning="high")
            (tdir / f"review-{rnd:02d}.md").write_text(review)
            (tdir / "review.md").write_text(review)
            review_routes.append(rroute)
            review_latencies.append(rmeta.get("latency_s"))
            verdict = review.strip().splitlines()[0].strip().upper() if review.strip() else "REVISE"
            last_verdict = verdict.split()[0]
            review_verdicts.append(last_verdict)
            findings_by_round.append(finding_types(review))
            if last_verdict.startswith("ACCEPT"):
                final_status = "ACCEPT"
                break
            wprompt = rewrite_prompt(writer, plan, style, cards[n], prev, n, text, review)
            (tdir / f"rewrite-prompt-{rnd:02d}.md").write_text(wprompt)
            if rnd == 1:
                (tdir / "rewrite-prompt.md").write_text(wprompt)
            text, rewrite_route, rewrite_meta = call_muse(wprompt)
            if text.strip().startswith("ROUTE REFUSAL:"):
                (tdir / "refusal.md").write_text(text)
                raise SystemExit(f"refusal rewrite chapter-{n:02d} r{rnd}: {text[:200]}")
            (tdir / f"rewrite-{rnd:02d}.md").write_text(text)
            rewrite_routes.append(rewrite_route)
            rewrite_latencies.append(rewrite_meta.get("latency_s"))
            words_by_round.append(word_count(text))
            if rnd == MAX_REWRITES:
                final_status = "CAP"
                last_verdict = "CAP"

        partial = live_path.with_suffix(".md.partial")
        partial.write_text(text)
        partial.rename(live_path)
        resp_path.write_text(text)
        meta.update(
            {
                "chapter": n,
                "replicate": REPLICATE,
                "slug": SLUG,
                "iteration": ITER,
                "chars": len(text),
                "words_draft": words_by_round[0],
                "words_final": word_count(text),
                "words_by_round": words_by_round,
                "budget": budget,
                "review_rounds": len(review_verdicts),
                "review_verdicts": review_verdicts,
                "review_verdict": last_verdict,
                "final_status": final_status,
                "findings_by_round": findings_by_round,
                "review_routes": review_routes,
                "review_latencies_s": review_latencies,
                "rewritten": bool(rewrite_routes),
                "rewrite_routes": rewrite_routes,
                "rewrite_latencies_s": rewrite_latencies,
                "draft_route": route,
            }
        )
        (tdir / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
        print(
            f"OK chapter-{n:02d} draft={words_by_round[0]}w final={meta['words_final']}w "
            f"budget={budget} {final_status} rounds={len(review_verdicts)} {route}",
            flush=True,
        )


if __name__ == "__main__":
    main()
