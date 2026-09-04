#!/usr/bin/env python3
"""Muse Spark: Go contributor → Zen contributor-free → Vercel contributor."""
from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.request

GO_URL = "https://opencode.ai/zen/go/v1/responses"
GO_MODEL = "muse-spark-1.3-contributor"
ZEN_URL = "https://opencode.ai/zen/v1/responses"
ZEN_MODEL = "muse-spark-1.3-contributor-free"
VERCEL_URL = "https://ai-gateway.vercel.sh/v1/chat/completions"
VERCEL_MODEL = "meta/muse-spark-1.3-contributor"
UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
TIMEOUT = 600
RETRY_SLEEPS = (15, 30)


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


def _retryable(code: int) -> bool:
    return code == 429 or code >= 500


def _post(url: str, payload: dict, key: str) -> tuple[int, dict | str]:
    code, data = http_json(url, payload, _headers(key))
    for delay in RETRY_SLEEPS:
        if code == 200 or not _retryable(code):
            break
        time.sleep(delay)
        code, data = http_json(url, payload, _headers(key))
    return code, data


def _zen_hit(code, data, model, route, t0):
    if code == 200 and isinstance(data, dict):
        text = extract_zen(data)
        if text.strip():
            return text, route, {
                "model": data.get("model") or model,
                "route": route,
                "latency_s": round(time.time() - t0, 3),
                "usage": data.get("usage") or {},
                "http": code,
            }
    return None


def call_muse(prompt: str, *, reasoning: str | None = None) -> tuple[str, str, dict]:
    go_key = (os.environ.get("OPENCODE_GO_API_KEY") or "").strip()
    zen_key = os.environ["OPENCODE_API_KEY"]
    zen_payload: dict = {"model": ZEN_MODEL, "input": prompt}
    go_payload: dict = {"model": GO_MODEL, "input": prompt}
    if reasoning:
        zen_payload["reasoning"] = {"effort": reasoning}
        go_payload["reasoning"] = {"effort": reasoning}

    statuses: list[str] = []

    def try_responses(url: str, payload: dict, key: str, model: str, route: str):
        t0 = time.time()
        code, data = _post(url, payload, key)
        statuses.append(f"{route}={code}")
        return _zen_hit(code, data, model, route, t0), code, data

    if go_key:
        hit, _, _ = try_responses(GO_URL, go_payload, go_key, GO_MODEL, "opencode-go")
        if hit:
            return hit
        hit, _, _ = try_responses(ZEN_URL, zen_payload, go_key, ZEN_MODEL, "opencode")
        if hit:
            return hit
    hit, zen_code, zen_data = try_responses(
        ZEN_URL, zen_payload, zen_key, ZEN_MODEL, "opencode"
    )
    if hit:
        return hit

    vg = os.environ["AI_GATEWAY_API_KEY"]
    v_payload = {
        "model": VERCEL_MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }
    t1 = time.time()
    code2, data2 = _post(VERCEL_URL, v_payload, vg)
    statuses.append(f"vercel={code2}")
    if code2 == 200 and isinstance(data2, dict):
        text = extract_vercel(data2)
        if text.strip():
            return text, "vercel", {
                "model": data2.get("model") or VERCEL_MODEL,
                "route": "vercel",
                "latency_s": round(time.time() - t1, 3),
                "zen_failed_status": zen_code,
                "usage": data2.get("usage") or {},
                "http": code2,
            }
    raise SystemExit(
        f"muse failed {' '.join(statuses)} last={str(zen_data)[:400]}"
    )
