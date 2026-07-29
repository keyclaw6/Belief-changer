#!/usr/bin/env python3
"""Research role call via the opencode Go gateway (chat completions,
function calling) with ORCHESTRATOR-EXECUTED web tools.

The gateway has no native web tools, so this runner supplies them:
  web_search(query)  -> DuckDuckGo HTML results (title, url, snippet)
  web_fetch(url)     -> GET, HTML stripped to text

Doctrine: research depth is unlimited — no cap on the number of searches
or fetches (a high runaway guard exists only to catch infinite loops and
is logged loudly if ever reached). Per-result size is trimmed to keep the
model's context usable; that is filtering, not a search ceiling.

Streaming SSE throughout (long final syntheses would otherwise be cut by
the egress proxy at ~4 min). Saves: transcript.json (full message list),
tools.log (every tool execution), response.md (final text), metadata.json.
Auth header REDACTED in saved requests. Founder rule: no time limits.
"""
import argparse, html, json, os, re, sys, time
import urllib.parse, urllib.request

RUNAWAY_GUARD = 5000  # not a research ceiling; loud failure if ever hit

def getcfg(cfg, key, default=None):
    for line in open(cfg):
        m = re.match(rf'^{re.escape(key)}:\s*([^#]+)', line)
        if m:
            return m.group(1).strip()
    if default is not None:
        return default
    raise SystemExit(f"config key missing: {key}")

def http(url, data=None, headers=None, timeout=None):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    return urllib.request.urlopen(req, timeout=timeout)

def strip_html(page):
    page = re.sub(r"(?is)<(script|style|noscript|svg|nav|footer|header)[^>]*>.*?</\1>", " ", page)
    page = re.sub(r"(?s)<[^>]+>", " ", page)
    page = html.unescape(page)
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n\n", page)).strip()

def web_search(query):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    try:
        with http(url, headers={"User-Agent": "Mozilla/5.0 (research)"} , timeout=60) as r:
            page = r.read().decode("utf-8", "replace")
    except Exception as e:
        return f"[search error] {e}"
    results = []
    for m in re.finditer(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', page):
        href, title = m.group(1), strip_html(m.group(2))
        qm = re.search(r'uddg=([^&]+)', href)
        if qm:
            href = urllib.parse.unquote(qm.group(1))
        results.append({"title": title, "url": href})
    snips = [strip_html(s) for s in re.findall(r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>', page)]
    for i, sn in enumerate(snips[:len(results)]):
        results[i]["snippet"] = sn
    if not results:
        return "[no results]"
    return json.dumps(results[:10], ensure_ascii=False)

def web_fetch(url):
    try:
        with http(url, headers={"User-Agent": "Mozilla/5.0 (research)"}, timeout=120) as r:
            raw = r.read(1500000).decode("utf-8", "replace")
    except Exception as e:
        return f"[fetch error] {e}"
    text = strip_html(raw)
    return text[:30000] + ("\n[TRIMMED — page continues]" if len(text) > 30000 else "")

TOOLS = [
    {"type": "function", "function": {
        "name": "web_search",
        "description": "Search the web. Returns up to 10 results as JSON: title, url, snippet. Call as often as needed — no limit.",
        "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}},
    {"type": "function", "function": {
        "name": "web_fetch",
        "description": "Fetch a URL and return its readable text (up to 30000 chars). Call as often as needed — no limit.",
        "parameters": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}}},
]

def stream_chat(endpoint, headers, body):
    """POST streaming chat completion; assemble content + tool_calls.
    Returns (status_code, content, tool_calls, finish_reason, usage, raw_len)."""
    data = json.dumps(body).encode()
    try:
        with http(endpoint, data=data, headers=headers) as r:
            raw = b""
            while True:
                b = r.read(65536)
                if not b:
                    break
                raw += b
            code, text = r.status, raw.decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace"), None, None, None, 0
    except Exception as e:
        return 0, f"[transport error] {e}", None, None, None, 0

    content, finish, usage = [], None, None
    tcalls = {}
    for line in text.splitlines():
        if not line.startswith("data:"):
            continue
        d = line[5:].strip()
        if not d or d == "[DONE]":
            continue
        try:
            ev = json.loads(d)
        except Exception:
            continue
        usage = ev.get("usage") or usage
        for ch in ev.get("choices", []) or []:
            delta = ch.get("delta") or {}
            if delta.get("content"):
                content.append(delta["content"])
            for tc in delta.get("tool_calls") or []:
                i = tc.get("index", 0)
                slot = tcalls.setdefault(i, {"id": None, "name": "", "args": ""})
                if tc.get("id"):
                    slot["id"] = tc["id"]
                fn = tc.get("function") or {}
                if fn.get("name"):
                    slot["name"] += fn["name"] if not slot["name"] else ""
                if fn.get("arguments"):
                    slot["args"] += fn["arguments"]
            if ch.get("finish_reason"):
                finish = ch["finish_reason"]
    calls = [{"id": v["id"] or f"call_{i}", "type": "function",
              "function": {"name": v["name"], "arguments": v["args"]}}
             for i, v in sorted(tcalls.items())]
    return code, "".join(content), calls, finish, usage, len(text)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--system-file", required=True)
    ap.add_argument("--user-file", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()

    cfg = a.config
    endpoint = getcfg(cfg, "researcher_endpoint")
    model = getcfg(cfg, "researcher_model")
    auth_env = getcfg(cfg, "researcher_auth_env", "OPENCODE_GO_API_KEY")
    effort = getcfg(cfg, "researcher_reasoning")
    key = os.environ[auth_env]
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json",
               "Accept": "text/event-stream", "User-Agent": "loop-runner/1.0"}
    os.makedirs(a.out_dir, exist_ok=True)
    tools_log = open(os.path.join(a.out_dir, "tools.log"), "a")

    ckpt = os.path.join(a.out_dir, "checkpoint.json")
    if os.path.exists(ckpt):
        state = json.load(open(ckpt))
        messages = state["messages"]
        print(f"resumed from checkpoint: {len(messages)} messages, "
              f"{state.get('searches',0)} searches, {state.get('fetches',0)} fetches")
    else:
        state = {"searches": 0, "fetches": 0}
        messages = [
            {"role": "system", "content": open(a.system_file).read()},
            {"role": "user", "content": open(a.user_file).read()},
        ]
    json.dump({"endpoint": endpoint, "model": model, "auth": "[REDACTED]",
               "reasoning_effort": effort},
              open(os.path.join(a.out_dir, "request.json"), "w"), indent=2)

    t_start = time.time()
    rounds = 0
    searches = state.get("searches", 0)
    fetches = state.get("fetches", 0)
    total_usage = None
    fw_waits = 0
    api_fail = 0
    while rounds < RUNAWAY_GUARD:
        rounds += 1
        body = {"model": model, "messages": messages, "tools": TOOLS,
                "stream": True, "reasoning_effort": effort}
        code, content, calls, finish, usage, rawlen = stream_chat(endpoint, headers, body)

        if (code == 403 and "blocked by network policy" in (content or "")) or \
           (code == 0):
            fw_waits += 1
            if fw_waits <= 120:
                print(f"egress/transport wait ({fw_waits}/120) — 60s", file=sys.stderr)
                time.sleep(60)
                continue
            print("FAILED: network never recovered", file=sys.stderr)
            sys.exit(1)
        if code != 200 or (finish is None and not calls and not content.strip()):
            api_fail += 1
            if api_fail <= 3:
                wait = [30, 60, 120][api_fail - 1]
                print(f"api attempt failed (http={code}) — retrying in {wait}s: {str(content)[:200]}",
                      file=sys.stderr)
                time.sleep(wait)
                continue
            open(os.path.join(a.out_dir, "response.raw.json"), "w").write(str(content)[:50000])
            print(f"FAILED after retries: {a.out_dir}", file=sys.stderr)
            sys.exit(1)
        api_fail = 0
        total_usage = usage or total_usage

        if calls:
            messages.append({"role": "assistant", "content": content or None,
                             "tool_calls": calls})
            for c in calls:
                name = c["function"]["name"]
                try:
                    args = json.loads(c["function"]["arguments"] or "{}")
                except Exception:
                    args = {}
                if name == "web_search":
                    searches += 1
                    q = str(args.get("query", ""))
                    result = web_search(q)
                    tools_log.write(f"SEARCH {searches}: {q}\n")
                elif name == "web_fetch":
                    fetches += 1
                    u = str(args.get("url", ""))
                    result = web_fetch(u)
                    tools_log.write(f"FETCH {fetches}: {u}\n")
                else:
                    result = f"[unknown tool {name}]"
                tools_log.flush()
                messages.append({"role": "tool", "tool_call_id": c["id"],
                                 "content": result})
            tmp = ckpt + ".tmp"
            json.dump({"messages": messages, "searches": searches,
                       "fetches": fetches}, open(tmp, "w"), ensure_ascii=False)
            os.replace(tmp, ckpt)
            continue

        # no tool calls -> final answer
        text = content
        if finish == "length":
            messages.append({"role": "assistant", "content": text})
            messages.append({"role": "user", "content":
                             "Continue exactly where you left off. Do not repeat."})
            continue
        if text.strip():
            clean = re.sub(r"(?s)<think>.*?</think>\s*", "", text)
            open(os.path.join(a.out_dir, "response.md"), "w").write(clean or text)
            json.dump({"model": model, "http": 200, "rounds": rounds,
                       "searches": searches, "fetches": fetches,
                       "latency_s": round(time.time() - t_start, 1),
                       "usage": total_usage, "finish": finish, "completed": True},
                      open(os.path.join(a.out_dir, "metadata.json"), "w"), indent=2)
            json.dump(messages, open(os.path.join(a.out_dir, "transcript.json"), "w"),
                      ensure_ascii=False)
            if os.path.exists(ckpt):
                os.remove(ckpt)
            print(f"OK {a.out_dir} ({round(time.time()-t_start,1)}s, "
                  f"{searches} searches, {fetches} fetches)")
            return
        # empty non-tool answer: nudge once per occurrence
        messages.append({"role": "user", "content":
                         "Your last message was empty. Continue the commission."})

    print(f"RUNAWAY GUARD HIT ({RUNAWAY_GUARD} rounds) — inspect transcript",
          file=sys.stderr)
    json.dump(messages, open(os.path.join(a.out_dir, "transcript.json"), "w"),
              ensure_ascii=False)
    sys.exit(1)

if __name__ == "__main__":
    main()
