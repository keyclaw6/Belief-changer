"""Blind judge panel runner; no --prompt selects the Stage-A v2 protocol."""
import argparse, json, os, re, sys, time, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import evallib as E
import model_endpoint as M
from judge_legacy import DIMS, aggregate, map_verdict, validate_pairwise
import judge_protocol as V2


JUDGE_DIR = Path(__file__).resolve().parents[2] / "calibration" / "judges"
ROLE_SPECS = V2.ROLE_SPECS

def chat(base_url, api_key, model, content, reasoning_effort, max_tokens,
         temperature=0.2, retries=3):
    url = base_url.rstrip("/") + "/chat/completions"
    body = {"model": model, "messages": [{"role": "user", "content": content}],
            "reasoning": {"effort": reasoning_effort}, "max_tokens": max_tokens}
    if temperature is not None:
        body["temperature"] = temperature
    for attempt in range(retries):
        try:
            request = urllib.request.Request(
                url, data=json.dumps(body).encode(),
                headers={"Authorization": f"Bearer {api_key}",
                         "Content-Type": "application/json"})
            with urllib.request.urlopen(request, timeout=600) as response:
                data = json.loads(response.read().decode())
            return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as exc:
            if exc.code == 400 and temperature is not None:
                body.pop("temperature", None)
                temperature = None
                continue
            if exc.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(10 * (attempt + 1))
                continue
            raise
    raise RuntimeError(f"chat: exhausted retries for {model}")

def extract_json(text):
    start = text.find("{")
    while start != -1:
        depth = 0
        for index in range(start, len(text)):
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:index + 1])
                    except json.JSONDecodeError:
                        break
        start = text.find("{", start + 1)
    return None

def _completion(cfg, model, prompt, ours_text, ref_text, order):
    a_text, b_text = (ours_text, ref_text) if order == 0 else (ref_text, ours_text)
    content = f"{prompt}\n\n=== TEXT A ===\n{a_text}\n\n=== TEXT B ===\n{b_text}"
    allowance = cfg["max_output_allowances"][model]
    raw = chat(cfg["base_url"], cfg["api_key"], model, content,
               cfg["reasoning_efforts"][model], allowance)
    return raw, extract_json(raw), allowance

def judge_pair(cfg, model, ch_n, ours_text, ref_text, order):
    raw, parsed, allowance = _completion(
        cfg, model, cfg["prompt"], ours_text, ref_text, order)
    record = {"chapter": ch_n, "model": model, "order": order,
              "max_output_allowance": allowance, "raw": raw, "parsed": parsed}
    if parsed is None:
        record["validation_error"] = "no complete JSON object found"
    else:
        ours_key, ref_key = ("A", "B") if order == 0 else ("B", "A")
        try:
            record["mapped"] = map_verdict(parsed, ours_key, ref_key)
        except ValueError as exc:
            record["validation_error"] = str(exc)
    return record

def judge_role(cfg, model, role, cell, order):
    raw, parsed, allowance = _completion(
        cfg, model, cfg["prompts"][role], cell["ours"], cell["ref"], order)
    record = {"protocol": "stage-a-v2", "role": role, "scope": ROLE_SPECS[role]["scope"],
              "target": cell["target"], "ours_chapters": cell["ours_chapters"],
              "ref_chapters": cell["ref_chapters"], "model": model, "order": order,
              "max_output_allowance": allowance, "raw": raw, "parsed": parsed}
    if parsed is None:
        record["validation_error"] = "no complete JSON object found"
    else:
        ours_key, ref_key = ("A", "B") if order == 0 else ("B", "A")
        try:
            record["mapped"] = V2.map_role_response(parsed, role, ours_key, ref_key)
        except ValueError as exc:
            record["validation_error"] = str(exc)
    return record

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


def degrade_text(text):
    """Make a local, deterministic incoherent control while retaining topic vocabulary."""
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]
    if len(sentences) >= 4:
        return " ".join(reversed(sentences[::3]))
    words = text.split()
    return " ".join(reversed(words[::3]))


def stage_a_materials(ours, ref, pairing, control=""):
    craft, ours_block, ref_block = [], [], []
    ours_numbers, ref_numbers = [], []
    for position, (ours_n, ref_n) in enumerate(pairing, 1):
        ours_text = E.strip_markdown(ours[ours_n - 1][1])
        ref_text = ref[ref_n - 1][1]
        if control == "identical":
            ours_text = ref_text
        elif control == "degraded-reference":
            ours_text = degrade_text(ref_text)
        target = (f"chapter-{ours_n:02d}" if ours_n == ref_n else
                  f"chapter-{ours_n:02d}-vs-{ref_n:02d}")
        craft.append({"target": target, "ours": ours_text, "ref": ref_text,
                      "ours_chapters": [ours_n], "ref_chapters": [ref_n]})
        ours_block.append(f"## Sample chapter {position}\n{ours_text}")
        ref_block.append(f"## Sample chapter {position}\n{ref_text}")
        ours_numbers.append(ours_n)
        ref_numbers.append(ref_n)
    block = {"target": "block", "ours": "\n\n".join(ours_block),
             "ref": "\n\n".join(ref_block), "ours_chapters": ours_numbers,
             "ref_chapters": ref_numbers}
    return {"efficacy": [block], "craft": craft, "integrity": [block]}


def _endpoint(args):
    if args.base_url:
        return (args.base_url, os.environ.get(args.api_key_env or "LITELLM_API_KEY") or
                os.environ.get("OPENROUTER_API_KEY"))
    if os.environ.get("LITELLM_BASE_URL"):
        return os.environ["LITELLM_BASE_URL"], os.environ.get("LITELLM_API_KEY")
    return "https://openrouter.ai/api/v1", os.environ.get("OPENROUTER_API_KEY")


def _write_record(outdir, record, legacy=False):
    safe_model = re.sub(r"[^a-zA-Z0-9.-]+", "_", record["model"])
    if legacy:
        path = outdir / f'ch{record["chapter"]:02d}-{safe_model}-o{record["order"]}.json'
    else:
        path = (outdir / record["role"] / record["target"] / safe_model /
                f'o{record["order"]}.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=1), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ours", required=True)
    parser.add_argument("--ref", required=True)
    parser.add_argument("--chapters", default="1-3")
    parser.add_argument("--pairs", default="", help="override pairing, e.g. 1:2,2:3")
    parser.add_argument("--models", required=True, help="comma-separated exact model ids")
    parser.add_argument("--reasoning-efforts", required=True,
                        help="comma-separated exact model=effort mappings")
    parser.add_argument("--max-output-allowances", default="")
    parser.add_argument("--prompt", default="", help="explicit legacy single-role prompt")
    parser.add_argument("--control", choices=("identical", "degraded-reference"), default="",
                        help="Stage-A v2 prompt-control run")
    parser.add_argument("--out", required=True)
    parser.add_argument("--base-url", default="")
    parser.add_argument("--api-key-env", default="")
    args = parser.parse_args()
    models = [model.strip() for model in args.models.split(",") if model.strip()]
    if not models:
        parser.error("--models must select at least one model")
    legacy = bool(args.prompt)
    if args.control and legacy:
        parser.error("--control is available only in the Stage-A v2 no--prompt protocol")
    if not legacy and (len(models) < 2 or len({model.split("/", 1)[0] for model in models}) < 2):
        parser.error("Stage-A v2 requires at least two configured model families")
    try:
        efforts = parse_reasoning_efforts(args.reasoning_efforts, models)
    except ValueError as exc:
        parser.error(str(exc))
    ours = E.load_chapters(args.ours)
    ref = E.load_chapters(args.ref, exts=(".txt", ".md"))
    pairing = (parse_pairs(args.pairs, len(ours), len(ref)) if args.pairs else
               [(n, n) for n in E.parse_range(args.chapters, min(len(ours), len(ref)))])
    base_url, api_key = _endpoint(args)
    if not base_url or not api_key:
        raise SystemExit("judge_panel: provide OPENROUTER_API_KEY, or LITELLM_BASE_URL"
                         " + LITELLM_API_KEY, or --base-url/--api-key-env")
    try:
        allowances = (M.parse_output_allowances(args.max_output_allowances, models)
                      if args.max_output_allowances else
                      M.resolve_output_allowances(base_url, api_key, models))
    except (ValueError, urllib.error.URLError, json.JSONDecodeError) as exc:
        raise SystemExit(f"judge_panel: cannot resolve endpoint output allowance: {exc}")
    cfg = {"base_url": base_url, "api_key": api_key, "reasoning_efforts": efforts,
           "max_output_allowances": allowances}
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    records = []
    if legacy:
        cfg["prompt"] = Path(args.prompt).read_text(encoding="utf-8")
        for ours_n, ref_n in pairing:
            for model in models:
                for order in (0, 1):
                    record = judge_pair(cfg, model, ours_n, E.strip_markdown(ours[ours_n - 1][1]),
                                        ref[ref_n - 1][1], order)
                    _write_record(outdir, record, legacy=True)
                    records.append(record)
        summary = aggregate(records)
    else:
        cfg["prompts"] = {role: (JUDGE_DIR / spec["prompt"]).read_text(encoding="utf-8")
                          for role, spec in ROLE_SPECS.items()}
        for role, cells in stage_a_materials(ours, ref, pairing, args.control).items():
            for cell in cells:
                for model in models:
                    for order in (0, 1):
                        record = judge_role(cfg, model, role, cell, order)
                        _write_record(outdir, record)
                        records.append(record)
        summary = V2.aggregate_v2(records)
        if args.control:
            summary["prompt_control"] = V2.evaluate_control(summary, args.control)
    (outdir / "judge-summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(json.dumps(summary.get("product_parity", summary), indent=1))
    if not summary["panel_complete"]:
        raise SystemExit("judge_panel: incomplete panel; inspect judge-summary.json")
    if args.control and not summary["prompt_control"]["passed"]:
        raise SystemExit("judge_panel: prompt control failed; inspect judge-summary.json")


if __name__ == "__main__":
    main()
