"""Blind pairwise judge panel runner (calibration HARNESS §9)."""
import argparse
import json
import os
import re
import sys
import time
import urllib.error, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import evallib as E
import model_endpoint as M
DIMS = ["click", "flow", "warmth", "mantra_discipline", "voice", "pacing"]
CRITICAL_FAILURES = {"shame_moralizing", "willpower_framing", "fear_as_motivator",
                     "medical_overreach", "plagiarism_suspect", "broken_continuity"}
def chat(base_url, api_key, model, content, reasoning_effort, max_tokens,
         temperature=0.2, retries=3):
    url = base_url.rstrip("/") + "/chat/completions"
    body = {"model": model, "messages": [{"role": "user", "content": content}],
            "reasoning": {"effort": reasoning_effort}, "max_tokens": max_tokens}
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
    allowance = cfg["max_output_allowances"][model]
    raw = chat(cfg["base_url"], cfg["api_key"], model, content,
               cfg["reasoning_efforts"][model], allowance)
    parsed = extract_json(raw)
    rec = {"chapter": ch_n, "model": model, "order": order,
           "max_output_allowance": allowance, "raw": raw, "parsed": parsed}
    if parsed is None:
        rec["validation_error"] = "no complete JSON object found"
    else:
        ours_key, ref_key = ("A", "B") if order == 0 else ("B", "A")
        try:
            rec["mapped"] = map_verdict(parsed, ours_key, ref_key)
        except ValueError as exc:
            rec["validation_error"] = str(exc)
    return rec
def validate_pairwise(p):
    if not isinstance(p, dict):
        raise ValueError("response must be a JSON object")
    scores = p.get("scores")
    if not isinstance(scores, dict):
        raise ValueError("scores must be an object")
    for dim in DIMS:
        pair = scores.get(dim)
        if not isinstance(pair, dict):
            raise ValueError(f"scores.{dim} must be an object")
        for text in ("A", "B"):
            score = pair.get(text)
            if (isinstance(score, bool) or not isinstance(score, (int, float)) or
                    not 1 <= score <= 9):
                raise ValueError(f"scores.{dim}.{text} must be a number from 1 to 9")

    failures = p.get("critical_failures")
    if not isinstance(failures, dict):
        raise ValueError("critical_failures must be an object")
    for text in ("A", "B"):
        items = failures.get(text)
        if not isinstance(items, list) or any(
                not isinstance(item, str) or item not in CRITICAL_FAILURES
                for item in items):
            raise ValueError(f"critical_failures.{text} must be a list of known failures")
    if p.get("which_is_real_carr") not in ("A", "B", "unsure"):
        raise ValueError("which_is_real_carr must be A, B, or unsure")
    if p.get("verdict_better") not in ("A", "B", "tie"):
        raise ValueError("verdict_better must be A, B, or tie")
    confidence = p.get("detection_confidence")
    if (isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or
            not 0 <= confidence <= 1):
        raise ValueError("detection_confidence must be a number from 0 to 1")
    notes = p.get("notes")
    if not isinstance(notes, str) or len(notes.split()) > 60:
        raise ValueError("notes must be a string of at most 60 words")
def map_verdict(p, ours_key, ref_key):
    validate_pairwise(p)
    out = {"dims": {}, "critical_ours": p["critical_failures"][ours_key]}
    for d in DIMS:
        s = p["scores"][d]
        out["dims"][d] = {"ours": s[ours_key], "ref": s[ref_key]}
    v = p["verdict_better"]
    out["verdict"] = "ours" if v == ours_key else "ref" if v == ref_key else "tie"
    real = p["which_is_real_carr"]
    out["real_guess_correct"] = (real == ref_key) if real in ("A", "B") else 0.5
    return out
def summarize_dims(records):
    out = {}
    for dim in DIMS:
        pairs = [r["mapped"]["dims"][dim] for r in records]
        if pairs:
            wins = sum(1 for pair in pairs if pair["ours"] > pair["ref"])
            ties = sum(1 for pair in pairs if pair["ours"] == pair["ref"])
            out[dim] = {
                "ours_mean": round(sum(p["ours"] for p in pairs) / len(pairs), 2),
                "ref_mean": round(sum(p["ref"] for p in pairs) / len(pairs), 2),
                "win_rate_incl_half_ties": round((wins + 0.5 * ties) / len(pairs), 3)}
    return out
def parse_reasoning_efforts(raw, models):
    try:
        efforts = dict(item.rsplit("=", 1) for item in raw.split(","))
    except ValueError as exc:
        raise ValueError("reasoning efforts must use model=effort entries") from exc
    efforts = {model.strip(): effort.strip() for model, effort in efforts.items()}
    if "" in efforts or any(not effort for effort in efforts.values()):
        raise ValueError("reasoning effort model and value must be non-empty")
    missing = [model for model in models if model not in efforts]
    if missing:
        raise ValueError("missing reasoning effort for: " + ", ".join(missing))
    return efforts
def parse_pairs(raw, ours_count, ref_count):
    pairs = []
    for item in raw.split(","):
        match = re.fullmatch(r"([1-9]\d*):([1-9]\d*)", item.strip())
        if not match:
            raise SystemExit(f"judge_panel: invalid --pairs entry: {item!r}")
        pair = tuple(int(value) for value in match.groups())
        if pair[0] > ours_count or pair[1] > ref_count:
            raise SystemExit(f"judge_panel: out-of-bounds --pairs entry: {item!r}")
        pairs.append(pair)
    return pairs
def aggregate(records):
    ok = [r for r in records if r.get("mapped")]
    invalid = len(records) - len(ok)
    summary = {"judgments": len(records), "parsed": len(ok),
               "invalid_judgments": invalid, "panel_complete": invalid == 0,
               "dims": summarize_dims(ok), "by_model": {}}
    wins = ties = 0
    guesses = [r["mapped"]["real_guess_correct"] for r in ok
               if r["mapped"]["real_guess_correct"] is not None]
    for r in ok:
        wins += r["mapped"]["verdict"] == "ours"
        ties += r["mapped"]["verdict"] == "tie"
        bm = summary["by_model"].setdefault(r["model"], {"ours": 0, "ref": 0, "tie": 0})
        bm[r["mapped"]["verdict"]] += 1
    for model, bm in summary["by_model"].items():
        model_records = [r for r in ok if r["model"] == model]
        bm["overall_win_rate_incl_half_ties"] = round(
            (bm["ours"] + 0.5 * bm["tie"]) / len(model_records), 3)
        bm["dims"] = summarize_dims(model_records)
    summary["overall_win_rate_incl_half_ties"] = (
        round((wins + 0.5 * ties) / len(ok), 3) if ok else None)
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
    ap.add_argument("--reasoning-efforts", required=True,
                    help="comma-separated exact model=effort mappings")
    ap.add_argument("--max-output-allowances", default="",
                    help="exact endpoint-reported model=integer mappings; omitted queries /models")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--base-url", default="", help="override endpoint base URL")
    ap.add_argument("--api-key-env", default="", help="env var holding the API key")
    a = ap.parse_args()
    models = [model.strip() for model in a.models.split(",") if model.strip()]
    if not models:
        ap.error("--models must select at least one model")
    try:
        reasoning_efforts = parse_reasoning_efforts(a.reasoning_efforts, models)
    except ValueError as exc:
        ap.error(str(exc))
    ours = E.load_chapters(a.ours)
    ref = E.load_chapters(a.ref, exts=(".txt", ".md"))
    pairing = (parse_pairs(a.pairs, len(ours), len(ref)) if a.pairs else
               [(n, n) for n in E.parse_range(a.chapters, min(len(ours), len(ref)))])
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
    try:
        max_output_allowances = (M.parse_output_allowances(a.max_output_allowances, models)
                                 if a.max_output_allowances else
                                 M.resolve_output_allowances(base_url, api_key, models))
    except (ValueError, urllib.error.URLError, json.JSONDecodeError) as exc:
        raise SystemExit(f"judge_panel: cannot resolve endpoint output allowance: {exc}")
    cfg = {"base_url": base_url, "api_key": api_key,
           "reasoning_efforts": reasoning_efforts,
           "max_output_allowances": max_output_allowances,
           "prompt": Path(a.prompt).read_text(encoding="utf-8")}
    outdir = Path(a.out)
    outdir.mkdir(parents=True, exist_ok=True)
    records = []
    for o_n, r_n in pairing:
        o_text = E.strip_markdown(ours[o_n - 1][1])
        r_text = ref[r_n - 1][1]
        for model in models:
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
                       "critical_failures_ours", "invalid_judgments")}, indent=1))
    if summary["invalid_judgments"]:
        raise SystemExit("judge_panel: incomplete panel; "
                         f"{summary['invalid_judgments']} judgment(s) failed validation")
if __name__ == "__main__":
    main()
