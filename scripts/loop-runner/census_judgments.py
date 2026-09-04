#!/usr/bin/env python3
"""Summarize CLUSTER CENSUS from one replicate's judgments/."""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

LANES = {
    "belief-mechanic": "belief",
    "voice-emotion": "voice",
    "reader-journey": "journey",
    "chapter-comparison": "comparison",
    "book-arc": "book-arc",
}


def parse_census(text: str) -> dict:
    m = re.search(r"CLUSTER CENSUS\n(.*?)(?:\n\n|\Z)", text, re.S)
    if not m:
        return {}
    block = m.group(1)
    out = {"verdict": None, "blocking": {}, "noted": {}}
    vm = re.search(r"^verdict:\s*(PASS|FAIL)", block, re.M)
    if vm:
        out["verdict"] = vm.group(1)
    section = None
    for line in block.splitlines():
        if line.strip() == "blocking:":
            section = "blocking"
            continue
        if line.strip() == "noted:":
            section = "noted"
            continue
        if section and line.strip() and not line.startswith(("lane:", "scope:", "verdict:")):
            mm = re.match(r"(\S+)\s+(\d+)\s*$", line.strip())
            if mm:
                out[section][mm.group(1)] = int(mm.group(2))
    return out


def main() -> None:
    root = Path(sys.argv[1])
    pass_fail = defaultdict(lambda: [0, 0])
    block_sum = defaultdict(lambda: defaultdict(int))
    noted_sum = defaultdict(lambda: defaultdict(int))
    missing = []
    files = sorted(root.glob("*/response.md"))
    for f in files:
        tag = f.parent.name
        text = f.read_text()
        c = parse_census(text)
        if not c or not c.get("verdict"):
            head = text.lstrip()[:8]
            verdict = "PASS" if head.startswith("PASS") else ("FAIL" if head.startswith("FAIL") else "?")
            c = {"verdict": verdict, "blocking": {}, "noted": {}}
        lane = "book-arc" if tag == "book-arc" else next((LANES[k] for k in LANES if tag.startswith(k)), tag)
        if c["verdict"] == "PASS":
            pass_fail[lane][0] += 1
        elif c["verdict"] == "FAIL":
            pass_fail[lane][1] += 1
        else:
            missing.append(tag)
        for k, v in c.get("blocking", {}).items():
            block_sum[lane][k] += v
        for k, v in c.get("noted", {}).items():
            noted_sum[lane][k] += v
    print(f"reports {len(files)}")
    for lane, (p, f) in sorted(pass_fail.items()):
        print(f"  {lane}: PASS {p} FAIL {f}")
        b = {k: v for k, v in block_sum[lane].items() if v}
        n = {k: v for k, v in noted_sum[lane].items() if v}
        if b:
            print(f"    blocking {b}")
        if n:
            print(f"    noted    {n}")
    if missing:
        print("unparsed", missing)


if __name__ == "__main__":
    main()
