#!/usr/bin/env python3
"""Muse Spark: Go contributor → Zen contributor-free → Vercel contributor."""
from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.request

# PROGRAM §1 chain, founder-only order. Vercel stays last resort (402 on 2026-09-04).
ROUTES = [
    (
        "opencode-go",
        "https://opencode.ai/zen/go/v1/responses",
        "muse-spark-1.3-contributor",
        "OPENCODE_GO_API_KEY",
        "responses",
    ),
    (
        "opencode",
        "https://opencode.ai/zen/v1/responses",
        "muse-spark-1.3-contributor-free",
        "OPENCODE_API_KEY",
        "responses",
    ),
    (
        "vercel",
        "https://ai-gateway.vercel.sh/v1/chat/completions",
        "meta/muse-spark-1.3-contributor",
        "AI_GATEWAY_API_KEY",
        "chat",
    ),
]
TRANSIENT = {429, 599} | set(range(500, 600))
TRIES = 4
UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
TIMEOUT = 600


def http_json(url: str, payload: dict, headers: dict) -> tuple[int, dict | str]:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
            raw = resp.read().decode()
            return resp.status, json.loads(raw)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            return e.code, json.loads(body)
        except json.JSONDecodeError:
            return e.code, body
    except (TimeoutError, urllib.error.URLError, ConnectionError) as e:
        return 599, str(e)


def extract_zen(data: dict) -> str:
    if isinstance(data.get("output_text"), str) and data["output_text"].strip():
        return data["output_text"]
    parts: list[str] = []
    for item in data.get("output") or []:
        if not isinstance(item, dict):
            continue
        for c in item.get("content") or []:
            if not isinstance(c, dict):
                continue
            text = c.get("text") or c.get("output_text") or ""
            if text:
                parts.append(text)
    return "".join(parts)


def extract_vercel(data: dict) -> str:
    try:
        return data["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError):
        return ""


def _headers(key: str) -> dict:
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "User-Agent": UA,
    }


def call_muse(prompt: str, *, reasoning: str | None = None) -> tuple[str, str, dict]:
    failed: dict[str, int | str] = {}
    for name, url, model, env, kind in ROUTES:
        key = (os.environ.get(env) or "").strip()
        if not key:
            failed[name] = "no key"
            continue
        payload: dict
        if kind == "responses":
            payload = {"model": model, "input": prompt}
            if reasoning:
                payload["reasoning"] = {"effort": reasoning}
        else:
            payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
        t0 = time.time()
        code: int = 0
        data: dict | str = {}
        for _ in range(TRIES):
            code, data = http_json(url, payload, _headers(key))
            text = (
                (extract_zen if kind == "responses" else extract_vercel)(data)
                if code == 200 and isinstance(data, dict)
                else ""
            )
            if text.strip():
                return text, name, {
                    "model": (data.get("model") or model) if isinstance(data, dict) else model,
                    "route": name,
                    "latency_s": round(time.time() - t0, 3),
                    "usage": (data.get("usage") or {}) if isinstance(data, dict) else {},
                    "failed_routes": failed,
                }
            if code not in TRANSIENT:
                break
            time.sleep(90 if code == 429 else 15)
        failed[name] = code
    raise SystemExit(f"muse failed {failed}")
