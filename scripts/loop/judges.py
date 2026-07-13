"""Reference-anchored rubric judging (PROGRAM §4.2).

Instrument: calibration/judges/carr-likeness-rubric.md — one judge context sees
the REAL reference chapter (ground truth) beside our candidate and returns six
0-10 distance-from-reference scores, a worst dimension, and improvement
suggestions tagged with the owning factory asset.

Judges are GPT-5.6 Sol (xhigh) run ONLY as fresh native Codex subagents on the
founder's subscription. There is deliberately NO judge API transport in this
module and judge traffic NEVER touches OpenRouter. This module only:

  emit_tasks()       write one self-contained task file per (chapter, judge j)
  missing_verdicts() which verdict files are still absent
  aggregate()        strict-parse saved verdict JSONs into one reward

The operator dispatches each task file as a fresh subagent and saves the raw
JSON reply to the matching verdicts/ path. Judge output is never fabricated.

endpoint()/have_key() remain here for the WRITER transport only
(run_iteration.py: Opus 4.6 via OpenRouter/LiteLLM).
"""
import json
import os
import re
from pathlib import Path

DIMS = ("voice_certainty", "method_execution", "structure_anatomy",
        "repetition_mantra", "emotional_register", "rhythm_texture")
_FENCE_RE = re.compile(r"```(?:json)?\s*(\{.*\})\s*```", re.S)
_BLANKS_RE = re.compile(r"\n{3,}")


def endpoint():
    """(base_url, api_key) for the WRITER only: LiteLLM else OpenRouter."""
    if os.environ.get("LITELLM_BASE_URL"):
        return os.environ["LITELLM_BASE_URL"], os.environ.get("LITELLM_API_KEY")
    return "https://openrouter.ai/api/v1", os.environ.get("OPENROUTER_API_KEY")


def have_key() -> bool:
    return bool(endpoint()[1])


def weights(cfg) -> dict:
    """Parse config's weights list ('name: 0.20' strings) into {dim: float}."""
    w = {}
    for item in cfg.get("weights") or []:
        if ":" not in str(item):
            raise SystemExit(f"judges: bad weights item {item!r}")
        k, _, v = str(item).partition(":")
        w[k.strip()] = float(v)
    if set(w) != set(DIMS):
        raise SystemExit(f"judges: weights keys {sorted(w)} != rubric dimensions {sorted(DIMS)}")
    if abs(sum(w.values()) - 1.0) > 1e-3:
        raise SystemExit(f"judges: weights sum {sum(w.values())} != 1.0")
    return w


def _norm(text: str) -> str:
    return _BLANKS_RE.sub("\n\n", (text or "").strip())


def judging_dir(cfg, iter_name: str) -> Path:
    return Path(cfg.get("tasks_dir", "loop/iterations")) / f"iter-{iter_name}" / "judging"


def _stems(labels, k):
    return [f"{lbl}-j{j}" for lbl in labels for j in range(1, k + 1)]


def missing_verdicts(cfg, labels, iter_name: str) -> list:
    vdir = judging_dir(cfg, iter_name) / "verdicts"
    k = int(cfg.get("judge_k", 2))
    return [s for s in _stems(labels, k) if not (vdir / f"{s}.json").is_file()]


def emit_tasks(cfg, pairs, iter_name: str, rubric_text: str) -> list:
    """pairs: (label, ours_text, ref_text). Writes tasks/, creates verdicts/."""
    if "{{REFERENCE}}" not in rubric_text or "{{CANDIDATE}}" not in rubric_text:
        raise SystemExit("judges: rubric missing {{REFERENCE}}/{{CANDIDATE}} placeholders")
    base = judging_dir(cfg, iter_name)
    tdir, vdir = base / "tasks", base / "verdicts"
    tdir.mkdir(parents=True, exist_ok=True)
    vdir.mkdir(parents=True, exist_ok=True)
    k = int(cfg.get("judge_k", 2))
    out = []
    for lbl, ours, ref in pairs:
        body = (rubric_text.replace("{{REFERENCE}}", _norm(ref))
                .replace("{{CANDIDATE}}", _norm(ours)))
        for j in range(1, k + 1):
            p = tdir / f"{lbl}-j{j}.md"
            p.write_text(body, encoding="utf-8")
            out.append(p)
    print(f"[judges] wrote {len(out)} task files -> {tdir}")
    print(f"[judges] DISPATCH each task file as a FRESH native Codex subagent — model "
          f"{cfg.get('judge_model')}, reasoning={cfg.get('judge_reasoning')} — NEVER via OpenRouter.")
    print(f"[judges] Save each subagent's raw reply (the JSON object) as {vdir}/<taskname>.json")
    print("[judges] Then re-run score.py with the same --iter to aggregate.")
    return out


def _parse_verdict(path: Path) -> dict:
    """Strict: bare JSON object or one ```json fenced``` block. No repair."""
    text = path.read_text(encoding="utf-8").strip()
    m = _FENCE_RE.search(text)
    raw = m.group(1) if m else text
    try:
        obj = json.loads(raw)
    except Exception as e:
        raise SystemExit(f"judges: malformed JSON in {path.name}: {e}")
    scores = obj.get("scores") or {}
    for d in DIMS:
        v = scores.get(d)
        if not isinstance(v, (int, float)) or not 0 <= v <= 10:
            raise SystemExit(f"judges: {path.name}: scores.{d} missing/out of range: {v!r}")
    if not isinstance(obj.get("suggestions", []), list):
        raise SystemExit(f"judges: {path.name}: suggestions must be a list")
    return obj


def aggregate(cfg, labels, iter_name: str) -> dict:
    vdir = judging_dir(cfg, iter_name) / "verdicts"
    k = int(cfg.get("judge_k", 2))
    missing = missing_verdicts(cfg, labels, iter_name)
    if missing:
        raise SystemExit(f"judges: missing verdicts for: {', '.join(missing)}")
    w = weights(cfg)
    per_chapter, all_sugg, worst_votes = [], [], {}
    for lbl in labels:
        verdicts = [_parse_verdict(vdir / f"{lbl}-j{j}.json") for j in range(1, k + 1)]
        dims = {d: round(sum(v["scores"][d] for v in verdicts) / k, 3) for d in DIMS}
        composite = round(sum(w[d] * dims[d] for d in DIMS) / 10.0, 4)
        per_chapter.append({"chapter": lbl, "composite": composite, "dims": dims,
                            "gap_summaries": [str(v.get("gap_summary", "")) for v in verdicts]})
        for v in verdicts:
            wd = v.get("worst_dimension")
            if wd in DIMS:
                worst_votes[wd] = worst_votes.get(wd, 0) + 1
            for s in v.get("suggestions", []):
                if isinstance(s, dict) and s.get("suggestion"):
                    all_sugg.append((str(s.get("asset", "?")),
                                     " ".join(str(s["suggestion"]).split())))
    reward = round(sum(c["composite"] for c in per_chapter) / len(per_chapter), 4)
    counts, order = {}, []
    for asset, txt in all_sugg:
        key = txt.lower()
        if key not in counts:
            counts[key] = {"suggestion": txt, "asset": asset, "count": 0}
            order.append(key)
        counts[key]["count"] += 1
    top = sorted((counts[k2] for k2 in order), key=lambda x: -x["count"])[:5]
    worst = sorted(worst_votes.items(), key=lambda kv: -kv[1])
    return {"reward": reward, "per_chapter": per_chapter, "suggestions": top,
            "worst_dimensions": [{"dimension": d, "votes": n} for d, n in worst],
            "n_verdicts": len(labels) * k, "judge_model": cfg.get("judge_model"),
            "judge_k": k}
