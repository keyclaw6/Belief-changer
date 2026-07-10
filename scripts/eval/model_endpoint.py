"""Endpoint-reported model limits for calibration model calls."""
import json
import urllib.request


def parse_output_allowances(raw, models):
    """Parse trusted proxy metadata when its /models response omits limits."""
    try:
        values = dict(item.rsplit("=", 1) for item in raw.split(","))
        values = {model.strip(): int(value.strip()) for model, value in values.items()}
    except (ValueError, TypeError) as exc:
        raise ValueError("output allowances must use model=positive-integer entries") from exc
    missing = [model for model in models if model not in values]
    if missing:
        raise ValueError("missing output allowance for: " + ", ".join(missing))
    if "" in values or any(value <= 0 for value in values.values()):
        raise ValueError("output allowances must be positive integers")
    return values


def resolve_output_allowances(base_url, api_key, models):
    """Return exact completion maxima exposed by an OpenAI-compatible endpoint."""
    req = urllib.request.Request(
        base_url.rstrip("/") + "/models",
        headers={"Authorization": f"Bearer {api_key}"})
    with urllib.request.urlopen(req, timeout=60) as response:
        records = json.loads(response.read().decode()).get("data", [])
    by_id = {record.get("id"): record for record in records}
    values = {}
    for model in models:
        record = by_id.get(model)
        if not record:
            raise ValueError(f"model metadata not found for {model}")
        candidates = (record.get("top_provider", {}).get("max_completion_tokens"),
                      record.get("max_completion_tokens"),
                      record.get("max_output_tokens"),
                      record.get("model_info", {}).get("max_output_tokens"),
                      record.get("model_info", {}).get("max_completion_tokens"))
        values[model] = next((value for value in candidates
                              if isinstance(value, int) and value > 0), None)
        if values[model] is None:
            raise ValueError(f"endpoint metadata has no completion maximum for {model}")
    return values
