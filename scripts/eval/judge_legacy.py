"""Frozen schema and aggregation for explicit legacy judge-panel runs."""

DIMS = ["click", "flow", "warmth", "mantra_discipline", "voice", "pacing"]
CRITICAL_FAILURES = {
    "shame_moralizing", "willpower_framing", "fear_as_motivator",
    "medical_overreach", "plagiarism_suspect", "broken_continuity",
}


def validate_pairwise(response):
    if not isinstance(response, dict):
        raise ValueError("response must be a JSON object")
    scores = response.get("scores")
    if not isinstance(scores, dict):
        raise ValueError("scores must be an object")
    for dim in DIMS:
        pair = scores.get(dim)
        if not isinstance(pair, dict):
            raise ValueError(f"scores.{dim} must be an object")
        for label in ("A", "B"):
            value = pair.get(label)
            if (isinstance(value, bool) or not isinstance(value, (int, float)) or
                    not 1 <= value <= 9):
                raise ValueError(f"scores.{dim}.{label} must be a number from 1 to 9")
    failures = response.get("critical_failures")
    if not isinstance(failures, dict):
        raise ValueError("critical_failures must be an object")
    for label in ("A", "B"):
        items = failures.get(label)
        if not isinstance(items, list) or any(
                not isinstance(item, str) or item not in CRITICAL_FAILURES for item in items):
            raise ValueError(f"critical_failures.{label} must be a list of known failures")
    if response.get("which_is_real_carr") not in ("A", "B", "unsure"):
        raise ValueError("which_is_real_carr must be A, B, or unsure")
    if response.get("verdict_better") not in ("A", "B", "tie"):
        raise ValueError("verdict_better must be A, B, or tie")
    confidence = response.get("detection_confidence")
    if (isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or
            not 0 <= confidence <= 1):
        raise ValueError("detection_confidence must be a number from 0 to 1")
    notes = response.get("notes")
    if not isinstance(notes, str) or len(notes.split()) > 60:
        raise ValueError("notes must be a string of at most 60 words")


def map_verdict(response, ours_key, ref_key):
    validate_pairwise(response)
    mapped = {"dims": {}, "critical_ours": response["critical_failures"][ours_key]}
    for dim in DIMS:
        scores = response["scores"][dim]
        mapped["dims"][dim] = {"ours": scores[ours_key], "ref": scores[ref_key]}
    verdict = response["verdict_better"]
    mapped["verdict"] = "ours" if verdict == ours_key else "ref" if verdict == ref_key else "tie"
    guess = response["which_is_real_carr"]
    mapped["real_guess_correct"] = (guess == ref_key) if guess in ("A", "B") else 0.5
    return mapped


def _summarize_dims(records):
    summary = {}
    for dim in DIMS:
        pairs = [record["mapped"]["dims"][dim] for record in records]
        if pairs:
            wins = sum(pair["ours"] > pair["ref"] for pair in pairs)
            ties = sum(pair["ours"] == pair["ref"] for pair in pairs)
            summary[dim] = {
                "ours_mean": round(sum(pair["ours"] for pair in pairs) / len(pairs), 2),
                "ref_mean": round(sum(pair["ref"] for pair in pairs) / len(pairs), 2),
                "win_rate_incl_half_ties": round((wins + 0.5 * ties) / len(pairs), 3),
            }
    return summary


def aggregate(records):
    valid = [record for record in records if record.get("mapped")]
    summary = {"judgments": len(records), "parsed": len(valid),
               "invalid_judgments": len(records) - len(valid),
               "panel_complete": len(records) == len(valid),
               "dims": _summarize_dims(valid), "by_model": {}}
    wins = ties = 0
    guesses = [record["mapped"]["real_guess_correct"] for record in valid]
    for record in valid:
        verdict = record["mapped"]["verdict"]
        wins += verdict == "ours"
        ties += verdict == "tie"
        model = summary["by_model"].setdefault(record["model"], {"ours": 0, "ref": 0, "tie": 0})
        model[verdict] += 1
    for name, model in summary["by_model"].items():
        subset = [record for record in valid if record["model"] == name]
        model["overall_win_rate_incl_half_ties"] = round(
            (model["ours"] + 0.5 * model["tie"]) / len(subset), 3)
        model["dims"] = _summarize_dims(subset)
    summary["overall_win_rate_incl_half_ties"] = (
        round((wins + 0.5 * ties) / len(valid), 3) if valid else None)
    summary["real_detection_accuracy"] = round(sum(guesses) / len(guesses), 3) if guesses else None
    summary["critical_failures_ours"] = sorted({failure for record in valid
                                                for failure in record["mapped"]["critical_ours"]})
    return summary
