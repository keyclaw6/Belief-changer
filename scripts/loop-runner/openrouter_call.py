#!/usr/bin/env python3
"""OpenRouter role call — writer (chat completions) or research (Responses API
with web_search + web_fetch). Routes/models/params read from loop/config.yaml.
Saves exact request (Authorization REDACTED), raw response, extracted text,
metadata. Retries 3x (30/60/120s). Founder rule: no time limits on role calls.
Research continuation on finish_reason/status "length"/"incomplete" is handled
by the caller re-invoking with --continue-from.
"""
import argparse, json, os, re, sys, time
import urllib.request

def getcfg(cfg, key):
    for line in open(cfg):
        m = re.match(rf'^{re.escape(key)}:\s*([^#]+)', line)
        if m:
            return m.group(1).strip()
    raise SystemExit(f"config key missing: {key}")

def post_stream(url, body, headers):
    """Stream SSE; returns (status, full_raw_text). Heartbeats arrive as events,
    so the proxy's idle/again cutoffs on long synchronous bodies don't apply."""
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
    try:
        with urllib.request.urlopen(req) as r:  # no timeout — founder rule
            chunks = []
            while True:
                b = r.read(65536)
                if not b:
                    break
                chunks.append(b)
            return r.status, b"".join(chunks).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:
        return 0, f"[transport error] {e}"

def parse_sse(raw):
    """Yield parsed JSON events from an SSE body."""
    for line in raw.splitlines():
        if line.startswith("data:"):
            data = line[5:].strip()
            if data and data != "[DONE]":
                try:
                    yield json.loads(data)
                except Exception:
                    pass

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--role", required=True, choices=["writer", "research"])
    ap.add_argument("--system-file")          # writer: system prompt file
    ap.add_argument("--user-file", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--previous-response-id") # research continuation
    a = ap.parse_args()

    key = os.environ["OPENROUTER_API_KEY"]
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json",
               "User-Agent": "loop-runner/1.0"}
    user_text = open(a.user_file).read()

    if a.role == "writer":
        url = getcfg(a.config, "writer_endpoint")
        model = getcfg(a.config, "writer_model")
        msgs = []
        if a.system_file:
            msgs.append({"role": "system", "content": open(a.system_file).read()})
        msgs.append({"role": "user", "content": user_text})
        body = {"model": model, "messages": msgs, "stream": True,
                "temperature": float(getcfg(a.config, "writer_temperature")),
                "reasoning": {"effort": getcfg(a.config, "writer_reasoning")}}
        # no max_tokens, no fallbacks — per config comments
    else:
        url = getcfg(a.config, "researcher_endpoint")
        model = getcfg(a.config, "researcher_model")
        body = {"model": model,
                "input": user_text if not a.system_file else None,
                "reasoning": {"effort": getcfg(a.config, "researcher_reasoning")},
                "tools": [{"type": "web_search"}, {"type": "web_fetch"}],
                "stream": True, "store": False}
        if a.system_file:
            body["instructions"] = open(a.system_file).read()
            body["input"] = user_text
        if a.previous_response_id:
            body["previous_response_id"] = a.previous_response_id

    os.makedirs(a.out_dir, exist_ok=True)
    red = dict(headers); red["Authorization"] = "Bearer [REDACTED]"
    json.dump({"endpoint": url, "headers": red, "body": body},
              open(os.path.join(a.out_dir, "request.json"), "w"), indent=2)

    backoffs = [30, 60, 120]
    attempt = 0
    fw_waits = 0
    while attempt < 4:
        t0 = time.time()
        code, raw = post_stream(url, body, headers)
        latency = round(time.time() - t0, 1)
        if (code == 403 and "blocked by network policy" in raw) or \
           (code == 0 and latency < 5):
            fw_waits += 1
            if fw_waits <= 120:
                print(f"egress firewall block (window {fw_waits}/120) — waiting 60s",
                      file=sys.stderr)
                time.sleep(60)
                continue
        ok, text, meta = False, "", {}
        if code == 200:
            if a.role == "writer":
                parts, finish, usage, mdl = [], None, None, None
                for ev in parse_sse(raw):
                    for ch in ev.get("choices", []) or []:
                        delta = ch.get("delta") or {}
                        if delta.get("content"):
                            parts.append(delta["content"])
                        if ch.get("finish_reason"):
                            finish = ch["finish_reason"]
                    usage = ev.get("usage") or usage
                    mdl = ev.get("model") or mdl
                text = "".join(parts)
                meta = {"finish_reason": finish, "usage": usage, "model": mdl}
                ok = bool(text.strip()) and finish is not None
            else:
                parts, status, rid, usage, incomplete = [], None, None, None, None
                for ev in parse_sse(raw):
                    et = ev.get("type", "")
                    if et == "response.output_text.delta":
                        parts.append(ev.get("delta", ""))
                    elif et in ("response.completed", "response.incomplete"):
                        resp = ev.get("response", {})
                        status = resp.get("status")
                        rid = resp.get("id")
                        usage = resp.get("usage")
                        incomplete = resp.get("incomplete_details")
                        if not parts:
                            for item in resp.get("output", []):
                                for c in item.get("content", []) or []:
                                    if c.get("type") in ("output_text", "text"):
                                        parts.append(c.get("text", ""))
                text = "".join(parts)
                meta = {"status": status, "response_id": rid,
                        "incomplete": incomplete, "usage": usage}
                ok = status in ("completed", "incomplete") and bool(text.strip())
        if ok:
            open(os.path.join(a.out_dir, "response.raw.json"), "w").write(raw)
            open(os.path.join(a.out_dir, "response.md"), "w").write(text)
            meta.update({"http": code, "latency_s": latency, "attempt": attempt + 1})
            json.dump(meta, open(os.path.join(a.out_dir, "metadata.json"), "w"), indent=2)
            print(f"OK {a.out_dir} ({latency}s)")
            return
        if attempt < 3:
            print(f"attempt {attempt+1} failed (http={code}) — retrying in {backoffs[attempt]}s",
                  file=sys.stderr)
            time.sleep(backoffs[attempt])
            attempt += 1
        else:
            open(os.path.join(a.out_dir, "response.raw.json"), "w").write(raw[:50000])
            json.dump({"http": code, "latency_s": latency, "attempt": attempt + 1,
                       "failed": True}, open(os.path.join(a.out_dir, "metadata.json"), "w"), indent=2)
            print(f"FAILED after 4 attempts: {a.out_dir}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
