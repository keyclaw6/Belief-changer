#!/usr/bin/env python3
"""No automatic continuation of the retired campaign. Explicit v2 stages only."""
import json
import sys

def run(raw: str) -> str:
    return "{}"

if __name__ == "__main__":
    if sys.argv[1:] == ["self-check"]:
        assert run('{"status":"aborted"}') == "{}"
        print("ok")
    else:
        sys.stdin.read()
        print("{}")
