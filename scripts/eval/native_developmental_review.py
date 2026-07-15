"""Run one task-hash-pinned RF-13 review with zero tool events."""
import argparse
import base64
import json
import os
import subprocess
import sys
from pathlib import Path

import native_judge as N

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "loop"))
import developmental_review_call as DC  # noqa: E402
import developmental_review_contract as C  # noqa: E402
import developmental_review_runtime as R  # noqa: E402
import pair_store as PS  # noqa: E402


class NativeError(RuntimeError):
    pass


def _events(stdout):
    parsed = []
    for line in stdout.splitlines():
        if not line.strip():
            continue
        try:
            parsed.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise NativeError(f"invalid native Codex JSONL event: {exc}") from exc
    messages, threads, usage = [], [], None
    for event in parsed:
        kind = event.get("type")
        if kind == "thread.started" and event.get("thread_id"):
            threads.append(event["thread_id"])
        elif kind == "turn.completed":
            usage = event.get("usage")
        elif kind == "turn.started":
            continue
        elif kind == "item.completed":
            item = event.get("item", {})
            if item.get("type") == "agent_message" and isinstance(item.get("text"), str):
                messages.append(item["text"])
            elif item.get("type") != "reasoning":
                raise NativeError("developmental reviewer emitted a forbidden tool event")
        else:
            raise NativeError("developmental reviewer emitted an unknown or tool event")
    if not messages or not threads or not isinstance(usage, dict):
        raise NativeError("developmental reviewer lacks final zero-tool native proof")
    return messages[-1], threads[-1], usage


def _result(task, raw, thread_id, usage):
    marker = DC.expected_marker(task)
    encoded = raw.encode("utf-8")
    value = {"schema": DC.SCHEMA, "call_id": marker["call_id"],
             "task_sha256": task["task_sha256"], "provider": marker["provider"],
             "route": marker["route"], "model": marker["model"],
             "family": marker["family"], "reasoning": marker["reasoning"],
             "command_sha256": marker["command_sha256"], "exit_code": 0,
             "thread_id": thread_id, "usage": usage, "tool_event_count": 0,
             "raw_sha256": PS.sha(encoded),
             "raw_b64": base64.b64encode(encoded).decode("ascii")}
    DC._proven(task, value)
    return value


def complete(task_sha256, run=subprocess.run):
    try:
        task = R.load(task_sha256)
        command = R.command(task)
        env = {name: os.environ[name] for name in N.NATIVE_ENV_ALLOWLIST
               if name in os.environ}
        result = run(command, input=R.input_bytes(task).decode("utf-8"), text=True,
                     capture_output=True, cwd=R.path(task_sha256), env=env, check=False)
        if result.returncode:
            raise NativeError(f"native developmental-review exited {result.returncode}")
        raw, thread_id, usage = _events(result.stdout)
        C.verdict(raw, task)
        value = _result(task, raw, thread_id, usage)
        R.persist_result(task, value)
        return value
    except NativeError:
        raise
    except (OSError, R.RuntimeError, DC.CallError, C.ContractError) as exc:
        raise NativeError(str(exc)) from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-sha256", required=True)
    args = parser.parse_args()
    try:
        value = complete(args.task_sha256)
    except NativeError as exc:
        raise SystemExit(f"native-developmental-review: {exc}") from exc
    print(f"native-developmental-review: persisted {value['call_id']}")


if __name__ == "__main__":
    main()
