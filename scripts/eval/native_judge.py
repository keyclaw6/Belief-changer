"""Fresh subscription-backed Codex transport for canonical Stage-A judges."""
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path


MODEL = "gpt-5.6-sol"
REASONING_EFFORT = "ultra"
DEFAULT_IDENTITIES = ("sol-ultra-r1", "sol-ultra-r2")
NATIVE_ENV_ALLOWLIST = (
    "PATH", "HOME", "CODEX_HOME", "LANG", "LC_ALL", "LC_CTYPE", "TERM",
    "TMPDIR", "TMP", "TEMP", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY",
    "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY",
)
IMPLEMENTATION_FILES = ("judge_panel.py", "judge_protocol.py", "native_judge.py")


def parse_identities(raw):
    identities = [value.strip() for value in raw.split(",") if value.strip()]
    if (len(identities) != 2 or len(set(identities)) != 2 or
            any(not re.fullmatch(r"[A-Za-z0-9.-]+", value) for value in identities)):
        raise ValueError("canonical Stage-A requires exactly two unique safe identity labels")
    return identities


def command(workdir):
    return [
        "codex", "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
        "--disable", "multi_agent", "--model", MODEL,
        "-c", f"model_reasoning_effort={REASONING_EFFORT}",
        "--sandbox", "read-only", "--skip-git-repo-check", "--cd", workdir,
        "--json", "-",
    ]


def _events(stdout):
    parsed = []
    for line in stdout.splitlines():
        if not line.strip():
            continue
        try:
            parsed.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid native Codex JSONL event: {exc}") from exc
    messages = [event["item"]["text"] for event in parsed
                if event.get("type") == "item.completed"
                and event.get("item", {}).get("type") == "agent_message"]
    if not messages:
        raise ValueError("native Codex emitted no final agent message")
    thread_ids = [event["thread_id"] for event in parsed
                  if event.get("type") == "thread.started" and event.get("thread_id")]
    if not thread_ids:
        raise ValueError("native Codex emitted no thread identity")
    usage = next((event.get("usage") for event in reversed(parsed)
                  if event.get("type") == "turn.completed"), None)
    return messages[-1], thread_ids[-1], usage


def instrument_configuration(prompts, pairing, identities):
    root = Path(__file__).parent
    digest = lambda data: hashlib.sha256(data).hexdigest()
    return {
        "protocol_version": "stage-a-v2.1-native-sol-ultra-1",
        "transport": "native-codex-subscription", "model": MODEL,
        "reasoning_effort": REASONING_EFFORT, "replica_identities": list(identities),
        "chapter_pairs": [list(pair) for pair in pairing],
        "role_prompt_sha256": {role: digest(text.encode()) for role, text in prompts.items()},
        "implementation_sha256": {
            name: digest((root / name).read_bytes()) for name in IMPLEMENTATION_FILES},
    }


def validate_controls(raw_paths, configuration):
    paths = [Path(value.strip()) for value in raw_paths.split(",") if value.strip()]
    if len(paths) != 2:
        raise ValueError("product judging requires exactly two control summary paths")
    evidence = {}
    for supplied in paths:
        path = supplied / "judge-summary.json" if supplied.is_dir() else supplied
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"cannot read control summary {path}: {exc}") from exc
        control = data.get("prompt_control", {})
        mode = control.get("mode")
        if mode not in ("identical", "degraded-reference") or mode in evidence:
            raise ValueError("controls must contain one unique summary for each required mode")
        if (not data.get("canonical") or not data.get("panel_complete") or
                data.get("raw_judgments") != 20 or
                data.get("collapsed_observations") != 10 or not control.get("passed")):
            raise ValueError(f"{mode} control did not pass canonically")
        if data.get("instrument_configuration") != configuration:
            raise ValueError(f"{mode} control configuration does not match product panel")
        evidence[mode] = {"summary": str(path), "sha256": hashlib.sha256(
            path.read_bytes()).hexdigest()}
    if set(evidence) != {"identical", "degraded-reference"}:
        raise ValueError("both identical and degraded-reference controls are required")
    return evidence


def complete(content, judge_identity, run=subprocess.run):
    """Run one fresh, uncapped-by-harness native judge context."""
    env = {name: os.environ[name] for name in NATIVE_ENV_ALLOWLIST if name in os.environ}
    with tempfile.TemporaryDirectory(prefix="belief-changer-judge-", dir="/tmp") as workdir:
        os.chmod(workdir, 0o555)
        cmd = command(workdir)
        launch_error = None
        try:
            try:
                result = run(cmd, input=content, text=True, capture_output=True,
                             cwd=workdir, env=env, check=False)
            except OSError as exc:
                result, launch_error = None, str(exc)
        finally:
            os.chmod(workdir, 0o755)
    invocation = ["<isolated-tmp>" if item == workdir else item for item in cmd]
    transport = {
        "kind": "native-codex-subscription", "judge_identity": judge_identity,
        "model": MODEL, "reasoning_effort": REASONING_EFFORT,
        "output_limit": "none set by harness", "fresh_ephemeral_context": True,
        "isolated_workdir": "/tmp read-only",
        "environment_policy": "native runtime allowlist; no provider API keys inherited",
        "command": invocation, "returncode": result.returncode if result else None,
        "stderr": result.stderr if result else launch_error,
        "input_sha256": hashlib.sha256(content.encode()).hexdigest(),
    }
    if launch_error:
        return "", transport, f"native Codex launch failed: {launch_error}"
    if result.returncode:
        transport["event_stream"] = result.stdout
        return "", transport, f"native Codex exited {result.returncode}"
    try:
        raw, thread_id, usage = _events(result.stdout)
    except ValueError as exc:
        transport["event_stream"] = result.stdout
        return "", transport, str(exc)
    transport.update({"thread_id": thread_id, "usage": usage})
    return raw, transport, None
