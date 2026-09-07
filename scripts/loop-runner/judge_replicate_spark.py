#!/usr/bin/env python3
"""Muse Spark judge runner (OpenCode harness adapter).

Same panel/inputs/outputs as judge_replicate.py (Cursor composer-2.5),
but each judge call is a fresh `opencode run --model
opencode-go/muse-spark-1.3-contributor` session. Skips existing reports,
so re-invoke fills gaps. One runner at a time (PROGRAM §4 Step 3).

Env: BC_REPO, ITER, SLUG, REPLICATE=a, REF_DIR, ALIGNMENT, MOVES, ONLY.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import judge_replicate as J  # noqa: E402

MODEL = "opencode-go/muse-spark-1.3-contributor"
JUDGE_PARALLEL = int(os.environ.get("JUDGE_PARALLEL", "4"))
CHAPTER_TIMEOUT = int(os.environ.get("JUDGE_CHAPTER_TIMEOUT", "1200"))
BOOK_TIMEOUT = int(os.environ.get("JUDGE_BOOK_TIMEOUT", "2400"))


def clean(text: str) -> str:
    lines = [l for l in text.splitlines() if not l.startswith("⟐")]
    return "\n".join(lines).strip()


def accepted(text: str) -> bool:
    t = clean(text)
    if len(t) < 200:
        return False
    head = t[:60]
    return (
        head.startswith(("PASS", "FAIL"))
        or "CLUSTER CENSUS" in t
        or "CARR DISTANCE" in t
    )


def run_agent(prompt: str, out: Path, tag: str) -> bool:
    out.parent.mkdir(parents=True, exist_ok=True)
    (out.parent / "prompt.md").write_text(prompt)
    partial = out.with_suffix(out.suffix + ".partial")
    timeout = BOOK_TIMEOUT if tag in ("book-arc", "carr-distance") else CHAPTER_TIMEOUT
    cmd = [
        "dotenvx", "run", "-f", str(J.REPO / ".env"), "--",
        "opencode", "run", "--dir", str(J.REPO),
        "--model", MODEL, "--variant", "high", "--auto",
        "--title", f"judge-{os.environ.get('ITER', '?')}-{tag}",
        prompt,
    ]
    for attempt in (1, 2):
        t0 = time.time()
        try:
            r = subprocess.run(
                cmd, cwd=str(J.REPO), capture_output=True, text=True,
                timeout=timeout,
            )
            text = r.stdout or ""
            err = ""
        except subprocess.TimeoutExpired:
            text, err = "", f"timeout>{timeout}s"
            r = None
        ok = accepted(text)
        (out.parent / "metadata.json").write_text(json.dumps({
            "model": "muse-spark-1.3-contributor",
            "harness": "opencode-run",
            "spawn": f"opencode run --model {MODEL} --variant high --auto",
            "latency_s": round(time.time() - t0, 3),
            "attempt": attempt,
            "accepted": ok,
            "error": err,
            "chars": len(text),
        }) + "\n")
        if ok:
            partial.write_text(text)
            partial.rename(out)
            print(f"OK {out.relative_to(J.REPO)} {round(time.time() - t0, 1)}s", flush=True)
            return True
        print(f"FAIL {tag} attempt {attempt} chars={len(text)} {err}", flush=True)
        time.sleep(10)
    return False


J.run_agent = run_agent
J.JUDGE_PARALLEL = JUDGE_PARALLEL

if __name__ == "__main__":
    J.main()
