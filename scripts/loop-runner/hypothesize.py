#!/usr/bin/env python3
"""Hypothesizer: GPT-6 Astra (Experiential), then Claude Fable 5.1."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from muse_client import http_json  # noqa: E402

REPO = Path(os.environ.get("BC_REPO", Path(__file__).resolve().parents[2]))
AGENT = Path.home() / ".local/bin/agent"
ASTRA_MODEL = "gpt-6-astra"
ASTRA_URL = "https://api.experientiallabs.ai/v1/chat/completions"
FABLE_MODEL = "claude-fable-5-1-thinking-high"
FACTORY = [
    "prompts/chapter-writer.md",
    "prompts/chapter-reviewer.md",
    "prompts/style-guide.md",
    "prompts/factory-orchestrator.md",
    "prompts/master-plan-skill-v2.md",
    "prompts/master-plan-reviewer-v2.md",
]
QUOTA_HINT = re.compile(
    r"quota|rate.?limit|insufficient|token.?cap|usage.?limit|too many tokens",
    re.I,
)


def redacted(text: str) -> str:
    return re.sub(r"xpl_[0-9a-f]+", "xpl_[redacted]", text, flags=re.I)


def read_repo(*parts: str) -> str:
    path = REPO.joinpath(*parts)
    return path.read_text() if path.is_file() else ""


def census(it: str, slug: str) -> str:
    root = REPO / "loop/iterations" / it / slug / "replicate-a" / "judgments"
    if not root.is_dir():
        return f"{slug}: no judgments\n"
    r = subprocess.run(
        [sys.executable, str(HERE / "census_judgments.py"), str(root)],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    return f"## census {slug}\n{(r.stdout or r.stderr).strip()}\n"


def pack(it: str) -> tuple[str, str]:
    prev = f"{int(it) - 1:03d}"
    chunks = [
        f"Iteration to propose: {it}. Previous: {prev}.",
        "Propose 1–4 bound changes, exactly one PRIMARY.",
        "The orchestrator will apply every listed Change N, not only PRIMARY.",
        census(prev, "quit-sugar"),
        census(prev, "quit-smoking"),
        "## learnings.md\n" + read_repo("loop", "learnings.md"),
        "## previous decision.md\n" + read_repo("loop", "iterations", prev, "decision.md"),
        "## previous hypothesis.md\n" + read_repo("loop", "iterations", prev, "hypothesis.md"),
        "## previous trace-analysis.md\n"
        + read_repo("loop", "iterations", prev, "trace-analysis.md"),
        "## results.tsv (tail)\n" + "\n".join(read_repo("loop", "results.tsv").splitlines()[-20:]),
    ]
    for rel in FACTORY:
        chunks.append(f"## {rel}\n{read_repo(*rel.split('/'))}")
    return read_repo("loop", "prompts", "hypothesizer.md"), "\n\n".join(chunks)


def extract_chat(data: dict) -> str:
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict):
                parts.append(part.get("text") or part.get("content") or "")
            elif isinstance(part, str):
                parts.append(part)
        return "".join(parts)
    return str(content or "")


def quota_fail(code: int, data: dict | str) -> bool:
    if code == 429:
        return True
    blob = data if isinstance(data, str) else json.dumps(data)
    return bool(QUOTA_HINT.search(blob))


def write_out(it: str, text: str, meta: dict) -> None:
    dest = REPO / "loop" / "iterations" / it
    dest.mkdir(parents=True, exist_ok=True)
    hyp = dest / "hypothesis.md"
    meta_path = dest / "hypothesis-metadata.json"
    partial = hyp.with_suffix(".md.partial")
    partial.write_text(text.strip() + "\n")
    partial.rename(hyp)
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")
    print(f"wrote {hyp.relative_to(REPO)} model={meta.get('model')}", flush=True)
    print("Apply every Change N in hypothesis.md, not PRIMARY only.", flush=True)


def astra(system: str, user: str) -> tuple[str, dict, str]:
    key = (os.environ.get("EXPERIENTIAL_API_KEY") or "").strip()
    if not key:
        return "", {}, "no_key"
    payload = {
        "model": ASTRA_MODEL,
        "reasoning_effort": "low",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    t0 = time.time()
    last_reason = "empty"
    for attempt in (1, 2):
        code, data = http_json(ASTRA_URL, payload, headers)
        blob = data if isinstance(data, str) else json.dumps(data)
        if quota_fail(code, data):
            return "", {}, "quota"
        if code == 200 and isinstance(data, dict):
            text = extract_chat(data).strip()
            if text:
                usage = data.get("usage") or {}
                meta = {
                    "model": data.get("model") or ASTRA_MODEL,
                    "harness": "experiential",
                    "spawn": "scripts/loop-runner/hypothesize.py",
                    "fallback_from": None,
                    "fallback_reason": None,
                    "reasoning_effort": "low",
                    "latency_s": round(time.time() - t0, 3),
                    "usage": usage,
                    "attempt": attempt,
                }
                return text, meta, ""
            last_reason = "empty"
        else:
            last_reason = f"http_{code}"
            print(f"astra fail attempt {attempt} {last_reason} {redacted(blob)[:400]}", flush=True)
        if code not in {429, 500, 502, 503, 504, 599} and attempt == 1:
            break
        time.sleep(8)
    return "", {}, last_reason


def fable(system: str, user: str, reason: str) -> tuple[str, dict]:
    prompt = system + "\n\n" + user
    cmd = [
        str(AGENT),
        "--trust",
        "--model",
        FABLE_MODEL,
        "--mode",
        "ask",
        "-p",
        "--output-format",
        "text",
        prompt,
    ]
    t0 = time.time()
    r = subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=600)
    text = (r.stdout or "").strip()
    if r.returncode != 0 and not text:
        text = (r.stderr or "").strip()
    meta = {
        "model": FABLE_MODEL,
        "harness": "cursor",
        "spawn": "agent --trust --model claude-fable-5-1-thinking-high --mode ask -p",
        "fallback_from": ASTRA_MODEL,
        "fallback_reason": reason,
        "latency_s": round(time.time() - t0, 3),
        "exit": r.returncode,
    }
    if r.returncode != 0 and not text.lstrip().startswith("## Failure evidence"):
        raise SystemExit(f"fable fail exit={r.returncode} {redacted(text)[:400]}")
    return text, meta


def ping() -> int:
    key = (os.environ.get("EXPERIENTIAL_API_KEY") or "").strip()
    if not key:
        print("ping missing EXPERIENTIAL_API_KEY", flush=True)
        return 2
    payload = {
        "model": ASTRA_MODEL,
        "reasoning_effort": "low",
        "messages": [{"role": "user", "content": "Hello"}],
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    code, data = http_json(ASTRA_URL, payload, headers)
    text = extract_chat(data) if isinstance(data, dict) else ""
    usage = (data.get("usage") if isinstance(data, dict) else {}) or {}
    print(
        f"ping http={code} model={ASTRA_MODEL} "
        f"chars={len(text)} cost={usage.get('cost')} "
        f"in={usage.get('prompt_tokens')} out={usage.get('completion_tokens')}",
        flush=True,
    )
    return 0 if code == 200 and text.strip() else 2


def main() -> None:
    if "--ping" in sys.argv:
        raise SystemExit(ping())
    it = os.environ.get("ITER") or (sys.argv[1] if len(sys.argv) > 1 else "")
    if not it:
        raise SystemExit("set ITER")
    dest = REPO / "loop" / "iterations" / it / "hypothesis.md"
    if dest.is_file() and "--force" not in sys.argv:
        print(f"exists {dest.relative_to(REPO)}; pass --force to replace", flush=True)
        return
    system, user = pack(it)
    text, meta, reason = astra(system, user)
    if not text:
        print(f"astra fallback → fable reason={reason}", flush=True)
        text, meta = fable(system, user, reason or "empty")
    write_out(it, text, meta)


if __name__ == "__main__":
    main()
