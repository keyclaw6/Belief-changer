#!/usr/bin/env python3
"""Web primitives for research sub-agents (search + fetch).
Usage:
  python3 web_tools.py search "<query>"      -> JSON list of up to 10 results
  python3 web_tools.py fetch "<url>"          -> readable page text (trimmed)
Shared by the research orchestrator and every spawned research sub-agent.
Research depth is sacred and unlimited: there is no search or fetch ceiling
here — these are filters on size, never on count.
"""
import base64
import html
import http.cookiejar as cookiejar
import json
import random
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


def http(url, headers=None, timeout=120):
    req = urllib.request.Request(url, headers=headers or {})
    return urllib.request.urlopen(req, timeout=timeout)


def strip_html(page):
    page = re.sub(r"(?is)<(script|style|noscript|svg|nav|footer|header)[^>]*>.*?</\1>", " ", page)
    page = re.sub(r"(?s)<[^>]+>", " ", page)
    page = html.unescape(page)
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n\n", page)).strip()


_UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
       "Chrome/120.0 Safari/537.36")


def _clean_url(url):
    url = url.replace("&amp;", "&")
    url = re.sub(r"[?&](rut|uddg)[^&]*", "", url)
    if url.endswith("&"):
        url = url[:-1]
    return url


def _ddg_parse(text):
    results = []
    for url_match, title_match in re.findall(
            r'<a rel="nofollow" href="([^"]+)"[^>]*>(.*?)</a>', text, re.S):
        if "uddg=" in url_match:
            target = urllib.parse.unquote(url_match.split("uddg=", 1)[1])
            target = _clean_url(target)
            title = strip_html(title_match).strip()
            if title and target.startswith("http"):
                results.append({"title": title[:300], "url": target})
    return results


def _ddg_lite(query, post=True):
    headers = {"User-Agent": _UA}
    try:
        if post:
            data = urllib.parse.urlencode({"q": query}).encode()
            req = urllib.request.Request("https://lite.duckduckgo.com/lite/",
                                         data=data, headers=headers)
        else:
            req = urllib.request.Request(
                "https://lite.duckduckgo.com/lite/?q=" + urllib.parse.quote(query),
                headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            text = r.read().decode("utf-8", "replace")
    except Exception:
        return []
    if "anomaly" in text.lower() or "challenge" in text.lower() or len(text) < 500:
        return []
    return _ddg_parse(text)


def web_search(query):
    # Backend fix 2026-08-14: Bing RSS became locale-contaminated and returned
    # unrelated pages, making search unusable for research depth. DuckDuckGo
    # Lite + Bing HTML (real URL recovered from its base64 `u=` param) were the
    # deterministic backends then.
    # Backend fix 2026-08-15: DDG lite/html are unreachable from the harness IP
    # (all requests time out) and Bing HTML serves degraded SERPs for
    # conversational queries unless they carry a strong brand anchor (e.g.
    # "mumsnet <topic>"). Marginalia (old interface, indexes personal blogs/
    # forums — a premium vein for lived experience) is the primary backend;
    # Bing (cookie-warmed) is the fallback for brand-anchored discovery.
    # Search stays keyless and unlimited; pacing only avoids challenge walls.
    results = marginalia_search(query)
    if not isinstance(results, list) or not results:
        time.sleep(2)
        results = bing_fallback(query)
    if isinstance(results, list) and results:
        return results[:10]
    return results if isinstance(results, dict) else {"error": "[no results]"}


def marginalia_search(query):
    """Marginalia Search (old interface) — clean HTML, indexes personal blogs
    and niche web, ideal for lived-experience material."""
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0",
               "Accept-Language": "en-US,en;q=0.9"}
    url = "https://old-search.marginalia.nu/search?query=" + urllib.parse.quote(query)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as r:
            text = r.read(800000).decode("utf-8", "replace")
    except Exception as e:
        return {"error": f"[search error] {e}"}
    if 'id="results"' not in text:
        return {"error": "[no results]"}
    results = []
    for sec in re.findall(r'<section[^>]*class="card search-result"[^>]*>(.*?)</section>', text, re.S):
        h2m = re.search(r'<h2>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', sec, re.S)
        if not h2m:
            continue
        url_t = h2m.group(1).replace("&amp;", "&")
        title = strip_html(h2m.group(2)).strip()
        desc_m = re.search(r'<p class="description">(.*?)</p>', sec, re.S)
        desc = strip_html(desc_m.group(1)).strip() if desc_m else ""
        if not url_t.startswith("http"):
            continue
        results.append({"title": title[:300], "url": url_t, "description": desc[:400]})
        if len(results) >= 10:
            break
    return results if results else {"error": "[no results]"}


def bing_fallback(query):
    # Bing HTML as a deterministic fallback. The result href is a /ck/a
    # redirect carrying the real URL in a base64url `u=` parameter. A cookie
    # warm-up request is required: without session cookies Bing serves a
    # degraded SERP that ignores multi-token queries.
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0",
               "Accept-Language": "en-US,en;q=0.9"}
    cj = cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = list(headers.items())
    try:
        with opener.open("https://www.bing.com/", timeout=10) as r:
            r.read()
    except Exception:
        pass
    try:
        req = urllib.request.Request(
            "https://www.bing.com/search?q=" + urllib.parse.quote(query) + "&cc=US&setlang=en&count=20",
            headers=headers)
        with opener.open(req, timeout=20) as r:
            text = r.read().decode("utf-8", "replace")
    except Exception as e:
        return {"error": f"[search error] {e}"}
    results = []
    for h2 in re.findall(r'<h2[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', text, re.S):
        href, title_markup = h2
        href = href.replace("&amp;", "&")
        title = strip_html(title_markup).strip()
        m = re.search(r"[?&]u=([A-Za-z0-9+/=_-]+)", href) or re.search(r"[?&]u=([^&]+)", href)
        target = None
        if m:
            b64 = re.sub(r"^a1", "", m.group(1))
            pad = "=" * (-len(b64) % 4)
            try:
                target = base64.urlsafe_b64decode(b64 + pad).decode("utf-8", "replace")
            except Exception:
                target = None
        if not target:
            plain = href.replace("&amp;", "&")
            if plain.startswith("http") and "bing.com" not in plain:
                target = plain
        if title and target and target.startswith("http") and "bing.com" not in target:
            target = _clean_url(target)
            results.append({"title": title[:300], "url": target})
        if len(results) >= 10:
            break
    return results if results else {"error": "[no results]"}


def web_fetch(url):
    try:
        with http(url, headers={"User-Agent": "Mozilla/5.0 (research)"}, timeout=120) as r:
            raw = r.read(1500000).decode("utf-8", "replace")
    except Exception as e:
        return {"error": f"[fetch error] {e}"}
    text = strip_html(raw)
    if len(text) > 30000:
        text = text[:30000] + "\n[TRIMMED — page continues]"
    return text


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    command, arg = sys.argv[1], " ".join(sys.argv[2:])
    if command == "search":
        print(json.dumps(web_search(arg), ensure_ascii=False))
    elif command == "fetch":
        print(json.dumps(web_fetch(arg), ensure_ascii=False))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
