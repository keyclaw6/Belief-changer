#!/usr/bin/env python3
"""OpenCode Zen Muse Spark client with one Vercel contributor fallback (PROGRAM §1)."""
from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.request

ZEN_URL = "https://opencode.ai/zen/v1/responses"
ZEN_MODEL = "muse-spark-1.2-contributor-free"
VERCEL_URL = "https://ai-gateway.vercel.sh/v1/chat/completions"
VERCEL_MODEL = "meta/muse-spark-1.2-contributor"
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


def call_muse(prompt: str, *, reasoning: str | None = None) -> tuple[str, str, dict]:
    oc = os.environ["OPENCODE_API_KEY"]
    zen_headers = {
        "Authorization": f"Bearer {oc}",
        "Content-Type": "application/json",
        "User-Agent": UA,
    }
    zen_payload: dict = {"model": ZEN_MODEL, "input": prompt}
    if reasoning:
        zen_payload["reasoning"] = {"effort": reasoning}
    t0 = time.time()
    code, data = http_json(ZEN_URL, zen_payload, zen_headers)
    for _ in range(2):
        if code == 200 and isinstance(data, dict) and extract_zen(data).strip():
            break
        if not (isinstance(code, int) and code >= 500):
            break
        time.sleep(15)
        code, data = http_json(ZEN_URL, zen_payload, zen_headers)
    if code == 200 and isinstance(data, dict):
        text = extract_zen(data)
        if text.strip():
            return text, "opencode", {
                "model": ZEN_MODEL,
                "route": "opencode",
                "latency_s": round(time.time() - t0, 3),
                "usage": data.get("usage") or {},
            }
    vg = os.environ["AI_GATEWAY_API_KEY"]
    v_headers = {
        "Authorization": f"Bearer {vg}",
        "Content-Type": "application/json",
        "User-Agent": UA,
    }
    v_payload = {
        "model": VERCEL_MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }
    t1 = time.time()
    code2, data2 = http_json(VERCEL_URL, v_payload, v_headers)
    if code2 == 200 and isinstance(data2, dict):
        text = extract_vercel(data2)
        if text.strip():
            return text, "vercel", {
                "model": VERCEL_MODEL,
                "route": "vercel",
                "latency_s": round(time.time() - t1, 3),
                "zen_failed_status": code,
                "usage": data2.get("usage") or {},
            }
    raise SystemExit(
        f"muse failed zen={code} vercel={code2} zen_body={str(data)[:400]}"
    )
