"""Blind pairwise + detection judging over the existing OpenRouter plumbing.

Wraps scripts/eval/model_endpoint.chat (the OpenAI-compatible transport the
founder told us to reuse) and the endpoint/JSON-extraction discipline from
scripts/eval/judge_panel. NEW instrument, not the retired v2.3 role panel:
ONE question per prompt, strictly parseable line output.

Two metrics:
  pairwise authenticity -> reward in [0,1] = mean win-rate of ours vs the matched
    real chapter, k calls per pair, order-swapped, cross-family judges.
  detection probe -> secondary accuracy toward 0.5 = indistinguishable.

If no API key is present, callers get a DRY-RUN result (reward=None) — hard
checks and diagnostics still run for real; judge output is NEVER fabricated.
"""
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "eval"))
import model_endpoint as ME  # noqa: E402  (path set above)

VERDICT_RE = re.compile(r"^\s*VERDICT:\s*([AB])\b", re.I | re.M)
REAL_RE = re.compile(r"^\s*REAL:\s*([AB])\b", re.I | re.M)
CONF_RE = re.compile(r"^\s*CONFIDENCE:\s*([01](?:\.\d+)?)\b", re.I | re.M)


def endpoint():
    """(base_url, api_key) reusing judge_panel's precedence: LiteLLM else OpenRouter."""
    if os.environ.get("LITELLM_BASE_URL"):
        return os.environ["LITELLM_BASE_URL"], os.environ.get("LITELLM_API_KEY")
    return "https://openrouter.ai/api/v1", os.environ.get("OPENROUTER_API_KEY")


def have_key() -> bool:
    return bool(endpoint()[1])


def _ask(base_url, key, model, reasoning, prompt, a_text, b_text, max_tokens=1200):
    content = f"{prompt}\n\n=== TEXT A ===\n{a_text}\n\n=== TEXT B ===\n{b_text}"
    return ME.chat(base_url, key, model, content, reasoning, max_tokens, temperature=0.2)


def _pairwise_score(raw, ours_is):
    """Map one VERDICT to ours-win=1.0 / ref-win=0.0. None if unparseable."""
    m = VERDICT_RE.search(raw or "")
    if not m:
        return None
    return 1.0 if m.group(1).upper() == ours_is else 0.0


def _detection_correct(raw, ref_is):
    """1.0 if judge's REAL guess correctly names the reference (real) text, else 0.0."""
    m = REAL_RE.search(raw or "")
    if not m:
        return None
    return 1.0 if m.group(1).upper() == ref_is else 0.0


def _confidence(raw):
    m = CONF_RE.search(raw or "")
    return float(m.group(1)) if m else None


def run_pairwise(cfg, pairs, prompt_text, kind):
    """pairs: [(label, ours_text, ref_text)]. kind: 'pairwise' | 'detection'.

    Returns a dict with per-call records and the aggregate. On no-key, returns
    {"dry_run": True, ...} without contacting any endpoint.
    """
    base_url, key = endpoint()
    models = cfg["judge_models"]
    k = int(cfg["k"])
    if k % 2 or k < 2:
        raise SystemExit(f"judges: k must be a positive even number, got {k}")
    reasoning = cfg.get("judge_reasoning", "high")
    out = {"kind": kind, "models": models, "k": k, "pairs": len(pairs),
           "calls": [], "dry_run": not key}
    if not key:
        return out

    # k calls per pair, split evenly across the model list and across A/B order.
    # order 0 => ours is A; order 1 => ours is B.
    scores, confidences = [], []
    for label, ours_text, ref_text in pairs:
        for i in range(k):
            model = models[i % len(models)]
            order = i % 2
            a_text, b_text = (ours_text, ref_text) if order == 0 else (ref_text, ours_text)
            ours_is = "A" if order == 0 else "B"
            ref_is = "B" if order == 0 else "A"
            try:
                raw = _ask(base_url, key, model, reasoning, prompt_text, a_text, b_text)
                err = None
            except Exception as exc:  # transport/HTTP error — record, never fake
                raw, err = "", f"{type(exc).__name__}: {exc}"
            rec = {"pair": label, "model": model, "order": order, "raw": raw,
                   "error": err}
            if kind == "pairwise":
                s = _pairwise_score(raw, ours_is)
                rec["ours_win"] = s
                if s is not None:
                    scores.append(s)
            else:
                c = _detection_correct(raw, ref_is)
                rec["real_correct"] = c
                conf = _confidence(raw)
                rec["confidence"] = conf
                if c is not None:
                    scores.append(c)
                if conf is not None:
                    confidences.append(conf)
            out["calls"].append(rec)

    valid = len(scores)
    out["valid_calls"] = valid
    out["invalid_calls"] = len(out["calls"]) - valid
    if kind == "pairwise":
        out["reward"] = round(sum(scores) / valid, 4) if valid else None
    else:
        out["detection_accuracy"] = round(sum(scores) / valid, 4) if valid else None
        out["mean_confidence"] = round(sum(confidences) / len(confidences), 3) if confidences else None
        # |accuracy - 0.5| : distance from indistinguishable (0 = perfect blind)
        acc = out["detection_accuracy"]
        out["distinguishability"] = round(abs(acc - 0.5), 4) if acc is not None else None
    return out
