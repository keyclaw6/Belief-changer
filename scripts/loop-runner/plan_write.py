#!/usr/bin/env python3
"""Write or revise the quit-sugar master plan via Muse Spark (PROGRAM planning stage)."""
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
    out = REPO / "production-books" / SLUG / "master-plan.md"
    skill = (REPO / "prompts" / "master-plan-skill-v2.md").read_text()
    style = (REPO / "prompts" / "style-guide.md").read_text()
    brief = (REPO / "production-books" / SLUG / "00-brief.md").read_text()
    lived = (REPO / "production-books" / SLUG / "research" / "lived-experience.md").read_text()
    science = (REPO / "production-books" / SLUG / "research" / "scientific-evidence.md").read_text()
    banks_dir = REPO / "production-books" / SLUG / "research" / "banks"
    bank_files = sorted(banks_dir.glob("bank-*.md")) if banks_dir.is_dir() else []
    total = sum(p.stat().st_size for p in bank_files)
    bank_parts = []
    for p in bank_files:
        text = p.read_text()
        if total > 100_000 and "lived" not in p.name:
            text = text[:2000] + "\n…[truncated for plan context; full file on disk]\n"
        bank_parts.append(f"#### {p.name}\n{text}")
    banks = "\n\n".join(bank_parts) if bank_parts else "(no research/banks/)"
    revision_plan = os.environ.get("PLAN_CANDIDATE")
    revision_review = os.environ.get("PLAN_REVIEW")
    if revision_plan and revision_review:
        assignment = (
            "Revise the candidate master plan using only the reviewer's findings. "
            "Your entire reply is the complete replacement master plan and nothing else."
        )
        extra = (
            f"\n### Current candidate plan\n```\n{Path(revision_plan).read_text().rstrip()}\n```\n\n"
            f"### Reviewer findings\n```\n{Path(revision_review).read_text().rstrip()}\n```\n"
        )
        round_name = os.environ.get("PLAN_ROUND", "revision")
    else:
        assignment = (
            f"Write the complete master plan for `production-books/{SLUG}` "
            "(chapter cards + plan-wide inventories). Your entire reply is that plan and nothing else."
        )
        extra = ""
        round_name = "initial"
    prompt = (
        f"{skill.rstrip()}\n\n\n{assignment}\n\n"
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
        f"{extra}"
    )
    (traces / f"plan-writer-{round_name}-prompt.md").write_text(prompt)
    text, route, meta = call_muse(prompt, reasoning="xhigh")
    partial = out.with_suffix(".md.partial")
    partial.write_text(text)
    partial.rename(out)
    (traces / f"plan-writer-{round_name}-response.md").write_text(text)
    meta.update({"role": "plan-writer", "round": round_name, "chars": len(text)})
    (traces / f"plan-writer-{round_name}-metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"OK plan {round_name} {meta['latency_s']}s {route} {len(text)}c", flush=True)


if __name__ == "__main__":
    main()
