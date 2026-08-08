#!/usr/bin/env python3
"""Web primitives for research sub-agents (search + fetch).
Usage:
  python3 web_tools.py search "<query>"      -> JSON list of up to 10 results
  python3 web_tools.py fetch "<url>"          -> readable page text (trimmed)
Shared by the research orchestrator and every spawned research sub-agent.
Research depth is sacred and unlimited: there is no search or fetch ceiling
here — these are filters on size, never on count.
"""
import html
import json
import re
import sys
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


def web_search(query):
    # Bing RSS is keyless and returns parseable results; DuckDuckGo's HTML
    # endpoint serves a bot-challenge page to scripted clients (verified
    # 2026-08-08), so it is not a usable backend.
    url = ("https://www.bing.com/search?q=" + urllib.parse.quote(query)
           + "&format=rss&count=10")
    try:
        with http(url, headers={"User-Agent": "Mozilla/5.0 (research)"}, timeout=60) as r:
            xml_text = r.read().decode("utf-8", "replace")
    except Exception as e:
        return {"error": f"[search error] {e}"}
    results = []
    try:
        root = ET.fromstring(xml_text)
        for item in root.iter("item"):
            title = item.findtext("title") or ""
            link = item.findtext("link") or ""
            desc = item.findtext("description") or ""
            if title and link and title not in (f"Bing: {query}",):
                results.append({"title": title, "url": link,
                                "snippet": strip_html(desc)[:300]})
    except ET.ParseError as e:
        return {"error": f"[search parse error] {e}"}
    if not results:
        return {"error": "[no results]"}
    return results[:10]


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
