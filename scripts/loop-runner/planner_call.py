#!/usr/bin/env python3
"""Planner call — chat completions through the founder's Command Code proxy
loopback (sole provider route; no fallbacks — on failure the operator
escalates to the founder), per loop/config.yaml. Key: the env var named by
`planner_auth_env`, or the founder's Command Code CLI login
(~/.commandcode/auth.json) when that env var is absent.
Saves request (Authorization REDACTED), raw response, text, metadata.
Retries 3x. No time limits (founder rule)."""
import argparse, json, os, re, sys, time
import urllib.request

def getcfg(cfg, key, default=None):
    for line in open(cfg):
        m = re.match(rf'^{re.escape(key)}:\s*([^#]+)', line)
        if m:
            return m.group(1).strip()
    if default is not None:
        return default
    raise SystemExit(f"config key missing: {key}")

def resolve_key(cfg):
    env_name = getcfg(cfg, "planner_auth_env", "COMMANDCODE_API_KEY")
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
    ap.add_argument("--system-file", required=True)
    ap.add_argument("--user-file", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()

    url = getcfg(a.config, "planner_endpoint")
    model = getcfg(a.config, "planner_model")
    key = resolve_key(a.config)
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json",
               "User-Agent": "loop-runner/1.0"}
    body = {"model": model,
            "messages": [{"role": "system", "content": open(a.system_file).read()},
                         {"role": "user", "content": open(a.user_file).read()}],
            "reasoning_effort": getcfg(a.config, "planner_reasoning")}

    os.makedirs(a.out_dir, exist_ok=True)
    red = dict(headers); red["Authorization"] = "Bearer [REDACTED]"
    json.dump({"endpoint": url, "headers": red, "body": body},
              open(os.path.join(a.out_dir, "request.json"), "w"), indent=2)

    backoffs = [30, 60, 120]
    attempt = 0
    fw_waits = 0
    while attempt < 4:
        t0 = time.time()
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
            with urllib.request.urlopen(req) as r:  # no timeout — founder rule
                code, raw = r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            code, raw = e.code, e.read().decode("utf-8", "replace")
        except Exception as e:
            code, raw = 0, f"[transport error] {e}"
        latency = round(time.time() - t0, 1)
        if (code == 403 and "blocked by network policy" in raw) or \
           (code == 0 and latency < 5):
            fw_waits += 1
            if fw_waits <= 120:
                print(f"egress firewall block (window {fw_waits}/120) — waiting 60s",
                      file=sys.stderr)
                time.sleep(60)
                continue
        text, ok, meta = "", False, {}
        if code == 200:
            try:
                d = json.loads(raw)
                ch = d["choices"][0]
                text = ch["message"].get("content") or ""
                meta = {"finish_reason": ch.get("finish_reason"),
                        "usage": d.get("usage"), "model": d.get("model")}
                ok = bool(text.strip())
            except Exception as e:
                meta = {"parse_error": str(e)}
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
            print(f"FAILED after 4 attempts: {a.out_dir}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
