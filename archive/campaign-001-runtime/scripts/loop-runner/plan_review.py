#!/usr/bin/env python3
"""Review the candidate master plan via Muse Spark (PROGRAM planning stage)."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from muse_client import call_muse

REPO = Path(os.environ["BC_REPO"])
SLUG = os.environ.get("SLUG", "quit-sugar")


def main() -> None:
    traces = Path(os.environ["PLAN_TRACE_DIR"])
    traces.mkdir(parents=True, exist_ok=True)
    out = REPO / "production-books" / SLUG / "master-plan-review.md"
    contract = (REPO / "prompts" / "master-plan-reviewer-v2.md").read_text()
    plan = (REPO / "production-books" / SLUG / "master-plan.md").read_text()
    style = (REPO / "prompts" / "style-guide.md").read_text()
    brief = (REPO / "production-books" / SLUG / "00-brief.md").read_text()
    lived = (REPO / "production-books" / SLUG / "research" / "lived-experience.md").read_text()
    science = (REPO / "production-books" / SLUG / "research" / "scientific-evidence.md").read_text()
    banks_dir = REPO / "production-books" / SLUG / "research" / "banks"
    bank_files = sorted(banks_dir.glob("bank-*.md")) if banks_dir.is_dir() else []
    bank_parts = [
        f"#### {p.name}\n{p.read_text()}" for p in bank_files
    ]
    banks = "\n\n".join(bank_parts) if bank_parts else "(no research/banks/)"
    prompt = (
        "You are the book factory plan-reviewer, a fresh isolated role call.\n\n"
        "Follow this contract exactly:\n\n"
        f"{contract.rstrip()}\n\n"
        "Your entire reply IS the review. End with exactly `fit to write from` or "
        "`needs changes first` as the contract requires.\n\n"
        "### Master plan\n"
        f"```\n{plan.rstrip()}\n```\n\n"
        "### Style guide\n"
        f"```\n{style.rstrip()}\n```\n\n"
        "### Brief\n"
        f"```\n{brief.rstrip()}\n```\n\n"
        "### Lived-experience synthesis\n"
        f"```\n{lived.rstrip()}\n```\n\n"
        "### Scientific-evidence synthesis\n"
        f"```\n{science.rstrip()}\n```\n\n"
        "### Research banks (verbatim packets)\n"
        f"```\n{banks.rstrip()}\n```\n"
    )
    round_name = os.environ.get("PLAN_ROUND", "review")
    (traces / f"plan-reviewer-{round_name}-prompt.md").write_text(prompt)
    text, route, meta = call_muse(prompt, reasoning="xhigh")
    partial = out.with_suffix(".md.partial")
    partial.write_text(text)
    partial.rename(out)
    (traces / f"plan-reviewer-{round_name}-response.md").write_text(text)
    meta.update({"role": "plan-reviewer", "round": round_name, "chars": len(text)})
    (traces / f"plan-reviewer-{round_name}-metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
    tail = text.strip().splitlines()[-1] if text.strip() else ""
    print(f"OK review {round_name} {meta['latency_s']}s {route} {len(text)}c last={tail!r}", flush=True)


if __name__ == "__main__":
    main()
