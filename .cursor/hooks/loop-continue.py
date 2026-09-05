#!/usr/bin/env python3
"""Resume auto-research while loop/state.md is IN PROGRESS.

Does not tell this conversation to run plan/chapter loops. The factory is a
Muse Spark 1.3 session (prompts/factory-orchestrator.md).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CAMPAIGN_STATE = Path("/home/kab/Belief-changer/loop/state.md")


def field(text: str, name: str) -> str:
    m = re.search(rf"^- \*\*{re.escape(name)}:\*\*\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def load_state(path: Path) -> dict | None:
    if not path.is_file():
        return None
    text = path.read_text()
    return {
        "status": field(text, "Status"),
        "next": field(text, "Next unit"),
        "last": field(text, "Last completed unit"),
        "worktree": field(text, "Worktree"),
        "iter": field(text, "Iteration"),
        "path": str(path),
    }


def worktree_state_path(worktree_field: str) -> Path | None:
    m = re.search(r"(/[^\s`]+)", worktree_field)
    if not m:
        return None
    return Path(m.group(1)) / "loop" / "state.md"


def collect_states(payload: dict) -> list[dict]:
    paths: list[Path] = [CAMPAIGN_STATE]
    for root in payload.get("workspace_roots") or []:
        paths.append(Path(root) / "loop" / "state.md")
    out: list[dict] = []
    seen: set[str] = set()
    for path in paths:
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        st = load_state(path)
        if not st:
            continue
        out.append(st)
        wt = worktree_state_path(st.get("worktree") or "")
        if wt and str(wt) not in seen:
            seen.add(str(wt))
            wst = load_state(wt)
            if wst:
                out.append(wst)
    return out


def run(raw: str) -> str:
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return "{}"
    if payload.get("status") == "aborted":
        return "{}"
    active = next((s for s in collect_states(payload) if s.get("status") == "IN PROGRESS"), None)
    if not active:
        return "{}"
    msg = (
        f"loop/state.md is IN PROGRESS (iteration {active['iter']}). "
        f"Last: {active['last']}. Next: {active['next']}. "
        "Simple check only. If the current unit is unfinished and not stuck, "
        "sleep; do not chapter-journal. This conversation is auto-research, "
        "not the book factory. When FACTORY DONE, start that subject's judge "
        "(one at a time) then sleep. When both PANEL DONE: KEEP/QUANTIFY, "
        "hypothesize.py (Astra then Fable), apply every listed change, start "
        "both writes, sleep. Do not start a second factory orchestrator."
    )
    return json.dumps({"followup_message": msg})


def main() -> None:
    print(run(sys.stdin.read()))


if __name__ == "__main__":
    if sys.argv[1:] == ["self-check"]:
        assert run('{"status":"aborted"}') == "{}"
        assert run("{") == "{}"
        assert "book factory" in run("{}") or run("{}") == "{}"
        print("ok")
    else:
        main()
