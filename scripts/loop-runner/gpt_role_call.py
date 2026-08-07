#!/usr/bin/env python3
"""Fresh clean role call — chat completions through the founder's Command
Code proxy loopback (sole provider route; no fallbacks — on failure the
operator escalates to the founder).

Reads endpoint from loop/config.yaml (sole authority). Key: the env var
named by `gpt_auth_env`, or the founder's Command Code CLI login
(~/.commandcode/auth.json) when that env var is absent. Saves exact request
(Authorization REDACTED), raw SSE response, extracted text, and metadata.
Retries 3x (30/60/120s) on transient failures. Exits 2 on 401 (STOP signal:
credential rejected or model not in the founder's plan).
"""
import argparse, json, os, re, sys, time
import urllib.request

def getcfg(cfg_path, key, default=None):
    with open(cfg_path) as f:
        for line in f:
            m = re.match(rf'^{re.escape(key)}:\s*([^#]+)', line)
            if m:
                return m.group(1).strip()
    if default is not None:
        return default
    raise SystemExit(f"config key missing: {key}")

def resolve_key(cfg_path):
    env_name = getcfg(cfg_path, "gpt_auth_env", "COMMANDCODE_API_KEY")
    key = os.environ.get(env_name, "").strip()
    if not key:  # founder's Command Code CLI login (auto-refreshed OAuth)
        try:
            key = json.load(open(os.path.expanduser(
                "~/.commandcode/auth.json")))["apiKey"].strip()
        except (OSError, ValueError, KeyError):
            key = ""
    if not key:
        sys.exit(f"{env_name} missing and no ~/.commandcode/auth.json — "
                 "escalate to the founder; there is no fallback route")
    return key

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--reasoning", required=True)
    ap.add_argument("--instructions-file", required=True)
    ap.add_argument("--input-file", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()

    ep = getcfg(a.config, "gpt_endpoint")
    key = resolve_key(a.config)
    instructions = open(a.instructions_file).read()
    user_text = open(a.input_file).read()

    body = {
        "model": a.model,
        "messages": [{"role": "system", "content": instructions},
                     {"role": "user", "content": user_text}],
        "reasoning_effort": a.reasoning,
        "stream": True,
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "User-Agent": "loop-runner/1.0",
    }
    os.makedirs(a.out_dir, exist_ok=True)
    red = dict(headers)
    red["Authorization"] = "Bearer [REDACTED]"
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
            print("HTTP 401 — Command Code credential rejected or model not in "
                  "plan. STOP: escalate to the founder.", file=sys.stderr)
            sys.exit(2)

        text_parts, usage, finish = [], None, None
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
                for ch in ev.get("choices", []) or []:
                    delta = ch.get("delta") or {}
                    if delta.get("content"):
                        text_parts.append(delta["content"])
                    if ch.get("finish_reason"):
                        finish = ch["finish_reason"]
                usage = ev.get("usage") or usage
        text = "".join(text_parts)

        if code == 200 and finish is not None and text.strip():
            with open(os.path.join(a.out_dir, "response.sse"), "w") as f:
                f.write(raw)
            with open(os.path.join(a.out_dir, "response.md"), "w") as f:
                f.write(text)
            with open(os.path.join(a.out_dir, "metadata.json"), "w") as f:
                json.dump({"model": a.model, "reasoning": a.reasoning, "http": code,
                           "latency_s": latency, "usage": usage, "attempt": attempt + 1,
                           "finish_reason": finish, "completed": True}, f, indent=2)
            print(f"OK {a.out_dir} ({latency}s)")
            return

        if attempt < 3:
            wait = backoffs[attempt]
            print(f"attempt {attempt+1} failed (http={code}, finish={finish}, "
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
