"""Endpoint-reported model limits for calibration model calls."""
import json
import time
import urllib.error
import urllib.request


def chat(base_url, api_key, model, content, reasoning_effort, max_tokens,
         temperature=0.2, retries=3):
    """Historical OpenAI-compatible transport used only by legacy judging."""
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
