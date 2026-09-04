#!/usr/bin/env python3
"""Run late-Carr PASS tests (journey + belief, ×2) into a fresh preflight dir."""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from judge_replicate import REPO, JUDGES, run_agent

RUNS = REPO / os.environ.get(
    "PREFLIGHT_RUNS_DIR", "loop/preflight/runs-2026-09-04-composer-2.5-late-journey"
)
CHECKS = (
    ("reader-journey", "pass-test-reader-journey-late.md", "pass-test-reader-journey-late"),
    ("belief-mechanic", "pass-test-belief-mechanic-late.md", "pass-test-belief-mechanic-late"),
    ("chapter-comparison", "pass-test-chapter-comparison.md", "pass-test-chapter-comparison"),
)


def prompt_for(lane: str, input_name: str) -> str:
    inp = REPO / "loop/preflight/inputs" / input_name
    return f"""You are a book factory judge, fresh and reference-sighted. This is a single isolated judge call. There is no host task except this call.

Read {JUDGES / "_shared.md"} first, then read and follow the rubric at {JUDGES / f"{lane}.md"} exactly. The shared file is law; the rubric adds class tests.

Then read the input at {inp}. That file contains CHAPTER CONTEXT, OUR CHAPTER, and THE REAL CHAPTER (and PREVIOUS CHAPTER if present). Judge that input against the rubric and shared law.

Return your verdict exactly as the rubric demands, including CLUSTER CENSUS with every closed class listed (zeros included). Start your report with PASS or FAIL as the rubric requires. Quote the evidence for each verdict line.

Never reference scores, history, or prior judgments. Do not write any files. Do not search the rest of the repository. Your entire reply IS the judge report.
"""


def main() -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    failed = []
    for lane, input_name, stem in CHECKS:
        for n in (1, 2):
            tag = f"{stem}-run{n}"
            out = RUNS / tag / "response.md"
            if out.exists():
                print(f"skip {tag} (exists)", flush=True)
                continue
            ok = run_agent(prompt_for(lane, input_name), out, tag)
            if not ok:
                failed.append(tag)
    if failed:
        raise SystemExit(f"failed: {failed}")
    print("LATE PASS TESTS DONE", flush=True)


if __name__ == "__main__":
    main()
