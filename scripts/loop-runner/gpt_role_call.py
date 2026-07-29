#!/usr/bin/env python3
"""Fresh clean GPT role call via the Codex backend Responses endpoint.

Reads endpoint from loop/config.yaml (sole authority). Saves exact request
(Authorization REDACTED), raw SSE response, extracted text, and metadata.
Retries 3x (30/60/120s) on transient failures. Exits 2 on 401 (STOP signal).
"""
import argparse, base64, json, os, re, sys, time
import urllib.request

def getcfg(cfg_path, key):
    with open(cfg_path) as f:
        for line in f:
            m = re.match(rf'^{re.escape(key)}:\s*([^#]+)', line)
            if m:
                return m.group(1).strip()
    raise SystemExit(f"config key missing: {key}")

def account_id(tok):
    p = tok.split('.')[1]
    p += '=' * (-len(p) % 4)
    d = json.loads(base64.urlsafe_b64decode(p))
    return d.get("https://api.openai.com/auth", {}).get("chatgpt_account_id", "")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--reasoning", required=True)
    ap.add_argument("--instructions-file", required=True)
    ap.add_argument("--input-file", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()

    ep = getcfg(a.config, "openai_endpoint")
    tok = os.environ["OPENAI_OAUTH_TOKEN"]
    acct = account_id(tok)
    instructions = open(a.instructions_file).read()
    user_text = open(a.input_file).read()

    body = {
        "model": a.model,
        "instructions": instructions,
        "input": [{"role": "user", "content": [{"type": "input_text", "text": user_text}]}],
        "reasoning": {"effort": a.reasoning},
        "stream": True,
        "store": False,
    }
    headers = {
        "Authorization": f"Bearer {tok}",
        "chatgpt-account-id": acct,
        "OpenAI-Beta": "responses=experimental",
        "originator": "codex_cli_rs",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }
    os.makedirs(a.out_dir, exist_ok=True)
    red = dict(headers)
    red["Authorization"] = "Bearer [REDACTED]"
    red["chatgpt-account-id"] = "[REDACTED]"
    with open(os.path.join(a.out_dir, "request.json"), "w") as f:
        json.dump({"endpoint": ep, "headers": red, "body": body}, f, indent=2)

    backoffs = [30, 60, 120]
    attempt = 0
    fw_waits = 0   # sandbox egress-firewall block windows: wait them out
    while attempt < 4:
        t0 = time.time()
        try:
            req = urllib.request.Request(ep, data=json.dumps(body).encode(), headers=headers)
            # Founder rule 2026-07-28: role calls are never time-limited.
            with urllib.request.urlopen(req) as resp:
                raw = resp.read().decode("utf-8", "replace")
                code = resp.status
        except urllib.error.HTTPError as e:
            code = e.code
            raw = e.read().decode("utf-8", "replace")
        except Exception as e:
            code = 0
            raw = f"[transport error] {e}"
        latency = round(time.time() - t0, 1)

        if (code == 403 and "blocked by network policy" in raw) or \
           (code == 0 and latency < 5):
            fw_waits += 1
            if fw_waits <= 120:
                # Operator-side network outage, not an API failure: waiting it
                # out does not consume a PROGRAM retry attempt.
                print(f"egress firewall block (window {fw_waits}/120) — waiting 60s",
                      file=sys.stderr)
                time.sleep(60)
                continue

        if code == 401:
            with open(os.path.join(a.out_dir, "response.sse"), "w") as f:
                f.write(raw[:5000])
            print("HTTP 401 — OAuth token rejected. STOP: founder must refresh token.", file=sys.stderr)
            sys.exit(2)

        text_parts, usage, completed = [], None, False
        if code == 200:
            for line in raw.splitlines():
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if not data or data == "[DONE]":
                    continue
                try:
                    ev = json.loads(data)
                except Exception:
                    continue
                et = ev.get("type", "")
                if et == "response.output_text.delta":
                    text_parts.append(ev.get("delta", ""))
                elif et == "response.completed":
                    completed = True
                    usage = ev.get("response", {}).get("usage")
                    if not text_parts:
                        for item in ev.get("response", {}).get("output", []):
                            for c in item.get("content", []) or []:
                                if c.get("type") in ("output_text", "text"):
                                    text_parts.append(c.get("text", ""))
        text = "".join(text_parts)

        if code == 200 and completed and text.strip():
            with open(os.path.join(a.out_dir, "response.sse"), "w") as f:
                f.write(raw)
            with open(os.path.join(a.out_dir, "response.md"), "w") as f:
                f.write(text)
            with open(os.path.join(a.out_dir, "metadata.json"), "w") as f:
                json.dump({"model": a.model, "reasoning": a.reasoning, "http": code,
                           "latency_s": latency, "usage": usage, "attempt": attempt + 1,
                           "completed": True}, f, indent=2)
            print(f"OK {a.out_dir} ({latency}s)")
            return

        if attempt < 3:
            wait = backoffs[attempt]
            print(f"attempt {attempt+1} failed (http={code}, completed={completed}, "
                  f"text={len(text)} chars) — retrying in {wait}s", file=sys.stderr)
            time.sleep(wait)
            attempt += 1
        else:
            with open(os.path.join(a.out_dir, "response.sse"), "w") as f:
                f.write(raw[:20000])
            with open(os.path.join(a.out_dir, "metadata.json"), "w") as f:
                json.dump({"model": a.model, "http": code, "latency_s": latency,
                           "attempt": attempt + 1, "completed": False}, f, indent=2)
            print(f"FAILED after 4 attempts: {a.out_dir}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
