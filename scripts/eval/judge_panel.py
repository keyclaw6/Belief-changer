"""Blind pairwise judge panel runner (calibration HARNESS §9).

For each selected chapter pair (ours vs reference), each judge model scores the
pair BLIND in both A/B orders. Raw responses are saved; a summary aggregates
win-rates per dimension, overall verdicts, and real-Carr detection accuracy.

Endpoint (OpenAI-compatible), resolved in this order:
  --base-url/--api-key-env args > LITELLM_BASE_URL + LITELLM_API_KEY >
  OPENROUTER_API_KEY (base defaults to https://openrouter.ai/api/v1).

Usage:
  python3 scripts/eval/judge_panel.py \
      --ours production-books/quit-sugar/chapters --ref calibration/reference/gsbs \
      --chapters 1-3 --models claude-strong,gpt-5.6 \
      --prompt calibration/judges/pairwise-judge.md \
      --out calibration/runs/run-001/judgments
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import evallib as E

DIMS = ["click", "flow", "warmth", "mantra_discipline", "voice", "pacing"]


def chat(base_url, api_key, model, content, temperature=0.2, retries=3):
    url = base_url.rstrip("/") + "/chat/completions"
    body = {"model": model, "messages": [{"role": "user", "content": content}]}
    if temperature is not None:
        body["temperature"] = temperature
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url, data=json.dumps(body).encode(),
                headers={"Authorization": f"Bearer {api_key}",
                         "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=600) as r:
                data = json.loads(r.read().decode())
            return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            if e.code == 400 and temperature is not None:
                body.pop("temperature", None)
                temperature = None
                continue
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(10 * (attempt + 1))
                continue
            raise
    raise RuntimeError(f"chat: exhausted retries for {model}")


def extract_json(text: str):
    start = text.find("{")
    while start != -1:
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:i + 1])
                    except json.JSONDecodeError:
                        break
        start = text.find("{", start + 1)
    return None


def judge_pair(cfg, model, ch_n, ours_text, ref_text, order):
    a_text, b_text = (ours_text, ref_text) if order == 0 else (ref_text, ours_text)
    content = (cfg["prompt"] + "\n\n=== TEXT A ===\n" + a_text +
               "\n\n=== TEXT B ===\n" + b_text)
    raw = chat(cfg["base_url"], cfg["api_key"], model, content)
    parsed = extract_json(raw)
    rec = {"chapter": ch_n, "model": model, "order": order, "raw": raw, "parsed": parsed}
    if parsed:
        ours_key, ref_key = ("A", "B") if order == 0 else ("B", "A")
        rec["mapped"] = map_verdict(parsed, ours_key, ref_key)
    return rec


def map_verdict(p, ours_key, ref_key):
    out = {"dims": {}, "critical_ours": (p.get("critical_failures") or {}).get(ours_key, [])}
    for d in DIMS:
        s = (p.get("scores") or {}).get(d) or {}
        if ours_key in s and ref_key in s:
            out["dims"][d] = {"ours": s[ours_key], "ref": s[ref_key]}
    v = p.get("verdict_better")
    out["verdict"] = "ours" if v == ours_key else "ref" if v == ref_key else "tie"
    real = p.get("which_is_real_carr")
    out["real_guess_correct"] = (real == ref_key) if real in ("A", "B") else None
    return out


def aggregate(records):
    ok = [r for r in records if r.get("mapped")]
    summary = {"judgments": len(records), "parsed": len(ok), "dims": {}, "by_model": {}}
    wins = ties = 0
    guesses = [r["mapped"]["real_guess_correct"] for r in ok
               if r["mapped"]["real_guess_correct"] is not None]
    for d in DIMS:
        pairs = [r["mapped"]["dims"][d] for r in ok if d in r["mapped"]["dims"]]
        if pairs:
            w = sum(1 for p in pairs if p["ours"] > p["ref"])
            t = sum(1 for p in pairs if p["ours"] == p["ref"])
            summary["dims"][d] = {
                "ours_mean": round(sum(p["ours"] for p in pairs) / len(pairs), 2),
                "ref_mean": round(sum(p["ref"] for p in pairs) / len(pairs), 2),
                "win_rate_incl_half_ties": round((w + 0.5 * t) / len(pairs), 3)}
    for r in ok:
        wins += r["mapped"]["verdict"] == "ours"
        ties += r["mapped"]["verdict"] == "tie"
        bm = summary["by_model"].setdefault(r["model"], {"ours": 0, "ref": 0, "tie": 0})
        bm[r["mapped"]["verdict"]] += 1
    n = len(ok) or 1
    summary["overall_win_rate_incl_half_ties"] = round((wins + 0.5 * ties) / n, 3)
    summary["real_detection_accuracy"] = (round(sum(guesses) / len(guesses), 3)
                                          if guesses else None)
    summary["critical_failures_ours"] = sorted({c for r in ok
                                                for c in r["mapped"]["critical_ours"]})
    return summary


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ours", required=True)
    ap.add_argument("--ref", required=True)
    ap.add_argument("--chapters", default="1-3")
    ap.add_argument("--pairs", default="", help="override pairing, e.g. 1:2,2:3")
    ap.add_argument("--models", required=True, help="comma-separated model ids/aliases")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--base-url", default="", help="override endpoint base URL")
    ap.add_argument("--api-key-env", default="", help="env var holding the API key")
    a = ap.parse_args()

    if a.base_url:
        base_url = a.base_url
        api_key = os.environ.get(a.api_key_env or "LITELLM_API_KEY") or \
            os.environ.get("OPENROUTER_API_KEY")
    elif os.environ.get("LITELLM_BASE_URL"):
        base_url = os.environ["LITELLM_BASE_URL"]
        api_key = os.environ.get("LITELLM_API_KEY")
    else:
        base_url = "https://openrouter.ai/api/v1"
        api_key = os.environ.get("OPENROUTER_API_KEY")
    if not base_url or not api_key:
        raise SystemExit("judge_panel: provide OPENROUTER_API_KEY, or LITELLM_BASE_URL"
                         " + LITELLM_API_KEY, or --base-url/--api-key-env")
    cfg = {"base_url": base_url, "api_key": api_key,
           "prompt": Path(a.prompt).read_text(encoding="utf-8")}

    ours = E.load_chapters(a.ours)
    ref = E.load_chapters(a.ref, exts=(".txt", ".md"))
    if a.pairs:
        pairing = [tuple(int(x) for x in p.split(":")) for p in a.pairs.split(",")]
    else:
        pairing = [(n, n) for n in E.parse_range(a.chapters, min(len(ours), len(ref)))]

    outdir = Path(a.out)
    outdir.mkdir(parents=True, exist_ok=True)
    records = []
    for o_n, r_n in pairing:
        o_text = E.strip_markdown(ours[o_n - 1][1])
        r_text = ref[r_n - 1][1]
        for model in [m.strip() for m in a.models.split(",") if m.strip()]:
            for order in (0, 1):
                rec = judge_pair(cfg, model, o_n, o_text, r_text, order)
                safe = re.sub(r"[^a-zA-Z0-9.-]+", "_", model)
                (outdir / f"ch{o_n:02d}-{safe}-o{order}.json").write_text(
                    json.dumps(rec, indent=1), encoding="utf-8")
                records.append(rec)
                print(f"[judge] ch{o_n} {model} order{order}: "
                      f"{rec.get('mapped', {}).get('verdict', 'UNPARSED')}")
    summary = aggregate(records)
    (outdir / "judge-summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(json.dumps({k: summary[k] for k in
                      ("overall_win_rate_incl_half_ties", "real_detection_accuracy",
                       "critical_failures_ours")}, indent=1))


if __name__ == "__main__":
    main()
