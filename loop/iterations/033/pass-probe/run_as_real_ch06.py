#!/usr/bin/env python3
"""Re-run reader-journey on Easyway Ch6 with Carr-native CHAPTER CONTEXT."""
from pathlib import Path
import sys

sys.path.insert(0, "/home/kab/Belief-changer/scripts/loop-runner")
from judge_replicate import lane_prompt, run_agent

REPO = Path("/home/kab/Belief-changer")
CH = REPO / "calibration/reference/easyway-smoking/chapter-06.md"
PREV = REPO / "calibration/reference/easyway-smoking/chapter-05.md"
OUT = (
    REPO
    / "loop/iterations/033/pass-probe/reader-journey-easyway-06-as-real/response.md"
)

CTX = """CHAPTER CONTEXT
Chapter 6 of 46 — NICOTINE ADDICTION
Primary job: enacted transition — relief stops reading as a genuine lift and starts reading as a brief return to the pre-smoking baseline; physical withdrawal shrinks to a trivial little monster so brainwashing becomes the remaining danger.
Entering belief: enters fearing nicotine withdrawal as a terrible trauma; leaves seeing the physical tug as slight and brainwashing as the dominant hold.
Leaving belief: enters fearing nicotine withdrawal as a terrible trauma; leaves seeing the physical tug as slight and brainwashing as the dominant hold.
Arc and curve position: arc: middle mechanism; demolition of physical-terror; curve: middle mechanism.
Continuity: receives the two-factor setup from Chapter 5; hands brainwashing as the remaining problem.
Assigned compliance:
- Instruction: NONE
- Mantras: "little monster"; "the nicotine trap"; "slightly empty, restless feeling"
"""

if __name__ == "__main__":
    prompt = lane_prompt("reader-journey", 6, CH, CH, CTX, PREV)
    ok = run_agent(prompt, OUT, "reader-journey-easyway-06-as-real")
    raise SystemExit(0 if ok else 1)
