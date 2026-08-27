#!/usr/bin/env python3
"""Review the candidate master plan via Muse Spark; DeepSeek is the config default but Cursor maps planning-family Muse for writer-adjacent work? No — HARNESS Cursor says judges are composer-2.5; plan-reviewer is DeepSeek in config. Cursor adapter: composer-2.5 for judges; plan-reviewer should be composer-2.5 here as the reachable independent reviewer (same as 001–011 judges)."""
from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path

REPO = Path(os.environ["BC_REPO"])
AGENT = Path.home() / ".local/bin/agent"
SLUG = "quit-sugar"


def main() -> None:
    traces = Path(os.environ["PLAN_TRACE_DIR"])
    traces.mkdir(parents=True, exist_ok=True)
    out = REPO / "production-books" / SLUG / "master-plan-review.md"
    contract = (REPO / "prompts" / "master-plan-reviewer-v2.md").read_text()
    plan = REPO / "production-books" / SLUG / "master-plan.md"
    style = REPO / "prompts" / "style-guide.md"
    brief = REPO / "production-books" / SLUG / "00-brief.md"
    lived = REPO / "production-books" / SLUG / "research" / "lived-experience.md"
    science = REPO / "production-books" / SLUG / "research" / "scientific-evidence.md"
    prompt = f"""You are the book factory plan-reviewer, a fresh isolated role call.

Follow this contract exactly:

{contract}

Read these five files and nothing else:
- {plan}
- {style}
- {brief}
- {lived}
- {science}

Your entire reply IS the review. End with exactly `fit to write from` or `needs changes first` as the contract requires. Do not write files.
"""
    round_name = os.environ.get("PLAN_ROUND", "review")
    (traces / f"plan-reviewer-{round_name}-prompt.md").write_text(prompt)
    t0 = time.time()
    r = subprocess.run(
        [
            str(AGENT),
            "--trust",
            "--model",
            "composer-2.5",
            "--mode",
            "ask",
            "-p",
            "--output-format",
            "text",
            prompt,
        ],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    text = r.stdout if r.stdout.strip() else (r.stderr or "")
    partial = out.with_suffix(".md.partial")
    partial.write_text(text)
    partial.rename(out)
    (traces / f"plan-reviewer-{round_name}-response.md").write_text(text)
    meta = {
        "model": "composer-2.5",
        "harness": "cursor-agent-cli",
        "latency_s": round(time.time() - t0, 3),
        "exit": r.returncode,
        "round": round_name,
        "chars": len(text),
    }
    (traces / f"plan-reviewer-{round_name}-metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
    tail = text.strip().splitlines()[-1] if text.strip() else ""
    print(f"OK review {round_name} {meta['latency_s']}s exit={r.returncode} last={tail!r}", flush=True)
    if r.returncode != 0:
        raise SystemExit(f"plan-reviewer failed: {r.stderr[:400]}")


if __name__ == "__main__":
    main()
