#!/usr/bin/env python3
"""Resume the factory conversation while loop/state.md is IN PROGRESS.

Cursor analog of pi-goal-x autoContinue on agent_settled. PROGRAM.md stays
the sequencer. This hook only re-enters the same conversation.

stdin: Cursor stop / subagentStop JSON.
stdout: {} or {"followup_message": "..."}.

User abort (status=aborted) is a halt — do not fight it.
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


def main() -> None:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        print("{}")
        return
    if payload.get("status") == "aborted":
        print("{}")
        return
    active = next((s for s in collect_states(payload) if s.get("status") == "IN PROGRESS"), None)
    if not active:
        print("{}")
        return
    event = payload.get("hook_event_name") or ""
    if event == "subagentStop":
        msg = (
            f"The factory orchestrator subagent stopped while loop/state.md is "
            f"IN PROGRESS (iteration {active['iter']}; last: {active['last']}; "
            f"next: {active['next']}). Resume from the furthest on-disk marker "
            f"(PROGRAM §0). Do not restart completed units. Do not wait for a "
            f"human continue. A multi-chapter runner is one unit: wait for "
            f"process exit, not the first OK line. Do not background "
            f"write_replicate.py or judge_replicate.py."
        )
    else:
        msg = (
            f"loop/state.md is IN PROGRESS (iteration {active['iter']}). "
            f"You ended a turn between factory units. Last completed: "
            f"{active['last']}. Next: {active['next']}. Read PROGRAM.md §0, "
            f"confirm markers, continue from the furthest unit. Do not rewrite "
            f"completed units. Do not wait for a human continue. Wait for each "
            f"runner process to exit (last chapter marker), not the first OK "
            f"line. Finish through decision.md + results.tsv + campaign records."
        )
    print(json.dumps({"followup_message": msg}))


if __name__ == "__main__":
    main()
