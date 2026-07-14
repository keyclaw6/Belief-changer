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
import legacy_guard as LG

DIMS = ("voice_certainty", "method_execution", "structure_anatomy",
        "repetition_mantra", "emotional_register", "rhythm_texture")
ASSETS = {"style-guide", "chapter-writer", "chapter-reviewer", "master-plan",
          "research"}
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


def emit_tasks(cfg, pairs, iter_name: str, rubric_text: str, candidate: Path) -> list:
    """pairs: (label, ours_text, ref_text, ctx). Writes tasks/, creates verdicts/."""
    for ph in ("{{REFERENCE}}", "{{CANDIDATE}}", "{{CONTEXT}}"):
        if ph not in rubric_text:
            raise SystemExit(f"judges: rubric missing {ph} placeholder")
    base = judging_dir(cfg, iter_name)
    tdir, vdir = base / "tasks", base / "verdicts"
    LG.require_output(candidate, tdir)
    tdir.mkdir(parents=True, exist_ok=True)
    LG.require_output(candidate, vdir)
    vdir.mkdir(parents=True, exist_ok=True)
    k = int(cfg.get("judge_k", 2))
    out = []
    for lbl, ours, ref, ctx in pairs:
        body = (rubric_text.replace("{{REFERENCE}}", _norm(ref))
                .replace("{{CANDIDATE}}", _norm(ours))
                .replace("{{CONTEXT}}", _norm(ctx)))
        for j in range(1, k + 1):
            p = tdir / f"{lbl}-j{j}.md"
            LG.require_output(candidate, p)
            p.write_text(body, encoding="utf-8")
            out.append(p)
    print(f"[judges] wrote {len(out)} task files. DISPATCH each as a FRESH native Codex "
          f"subagent — model {cfg.get('judge_model')}, reasoning={cfg.get('judge_reasoning')} "
          "— NEVER via OpenRouter. Save each raw JSON reply EXACTLY here:")
    for p in out:
        print(f"[judges]   {p}  ->  {vdir / (p.stem + '.json')}")
    print("[judges] Task files embed reference text and are gitignored — NEVER commit them.")
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
    sugg = obj.get("suggestions")
    if not isinstance(sugg, list) or not 3 <= len(sugg) <= 5:
        raise SystemExit(f"judges: {path.name}: suggestions must be a list of 3-5 items "
                         f"(got {len(sugg) if isinstance(sugg, list) else type(sugg).__name__}) "
                         "— re-dispatch this one judge task")
    for i, s in enumerate(sugg):
        if not isinstance(s, dict) or not str(s.get("suggestion", "")).strip():
            raise SystemExit(f"judges: {path.name}: suggestions[{i}] missing text")
        if s.get("asset") not in ASSETS:
            raise SystemExit(f"judges: {path.name}: suggestions[{i}].asset {s.get('asset')!r} "
                             f"not in {sorted(ASSETS)} — re-dispatch this one judge task")
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
            for i, s in enumerate(v.get("suggestions", [])):
                all_sugg.append((str(s["asset"]), " ".join(str(s["suggestion"]).split()),
                                 5 - min(i, 4), lbl))
    reward = round(sum(c["composite"] for c in per_chapter) / len(per_chapter), 4)
    # Rank-weighted consensus: judge priority (rank 1 -> weight 5 ... rank 5 -> 1),
    # ties broken by chapter spread, then first-seen (review finding H-C3).
    counts, order = {}, []
    for asset, txt, wt, lbl in all_sugg:
        key = txt.lower()
        if key not in counts:
            counts[key] = {"suggestion": txt, "asset": asset, "weight": 0,
                           "count": 0, "chapters": set(), "_ord": len(order)}
            order.append(key)
        counts[key]["weight"] += wt
        counts[key]["count"] += 1
        counts[key]["chapters"].add(lbl)
    top = sorted(counts.values(),
                 key=lambda x: (-x["weight"], -len(x["chapters"]), x["_ord"]))[:5]
    for s in top:
        s["chapters"] = sorted(s["chapters"])
        del s["_ord"]
    worst = sorted(worst_votes.items(), key=lambda kv: -kv[1])
    return {"reward": reward, "per_chapter": per_chapter, "suggestions": top,
            "worst_dimensions": [{"dimension": d, "votes": n} for d, n in worst],
            "n_verdicts": len(labels) * k, "judge_model": cfg.get("judge_model"),
            "judge_k": k}
