"""Role schemas and response mapping for the calibration judge instrument."""
ROLE_SPECS = {
    "efficacy": {"scope": "block", "prompt": "belief-change-efficacy.md",
        "dims": ("benefit_dismantling", "belief_movement", "escape_conviction",
                 "cumulative_progression"),
        "failures": {"no_belief_shift", "assertion_without_demonstration",
                     "sacrifice_or_deprivation", "incoherent_block_arc"}},
    "craft": {"scope": "chapter", "prompt": "literary-craft.md",
        "dims": ("prose_control", "rhythm_and_variety", "specificity",
                 "flow_and_momentum", "ending_handoff"),
        "failures": {"generic_self_help_voice", "mechanical_or_listicle_prose",
                     "repetitive_sag", "broken_chapter_flow", "weak_ending_handoff"}},
    "integrity": {"scope": "block", "prompt": "method-integrity-epistemic-safety.md",
        "dims": ("non_shaming_regard", "willpower_free_logic",
                 "epistemic_honesty", "originality", "cross_chapter_consistency"),
        "failures": {"shame_moralizing", "willpower_framing", "fear_as_motivator",
                     "medical_overreach", "unsupported_authority_or_testimony",
                     "copyright_expression_risk", "broken_continuity"}},
}
def _score_pairs(response, dims):
    scores = response.get("scores")
    if not isinstance(scores, dict) or set(scores) != set(dims):
        raise ValueError("scores must contain exactly the role dimensions")
    for dim in dims:
        pair = scores[dim]
        if not isinstance(pair, dict) or set(pair) != {"A", "B"}:
            raise ValueError(f"scores.{dim} must contain exactly A and B")
        for label in ("A", "B"):
            value = pair[label]
            if (isinstance(value, bool) or not isinstance(value, (int, float)) or
                    not 1 <= value <= 9):
                raise ValueError(f"scores.{dim}.{label} must be a number from 1 to 9")
def validate_role_response(response, role):
    spec = ROLE_SPECS[role]
    expected = {"scores", "critical_failures", "product_parity_verdict", "confidence",
                "paraphrased_evidence", "generic_mechanism"}
    if not isinstance(response, dict) or set(response) != expected:
        raise ValueError("response must contain exactly the role schema fields")
    _score_pairs(response, spec["dims"])
    failures = response["critical_failures"]
    if not isinstance(failures, dict) or set(failures) != {"A", "B"}:
        raise ValueError("critical_failures must contain exactly A and B")
    for label, items in failures.items():
        if not isinstance(items, list) or any(item not in spec["failures"] for item in items):
            raise ValueError(f"critical_failures.{label} contains an unknown role failure")
    if response["product_parity_verdict"] not in ("A", "B", "tie"):
        raise ValueError("product_parity_verdict must be A, B, or tie")
    confidence = response["confidence"]
    if (isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or
            not 0 <= confidence <= 1):
        raise ValueError("confidence must be a number from 0 to 1")
    evidence = response["paraphrased_evidence"]
    if not isinstance(evidence, dict) or set(evidence) != {"A", "B"}:
        raise ValueError("paraphrased_evidence must contain exactly A and B")
    for label, text in evidence.items():
        if (not isinstance(text, str) or not text.strip() or len(text.split()) > 45 or
                any(mark in text for mark in ('"', "“", "”"))):
            raise ValueError(f"paraphrased_evidence.{label} must be unquoted and at most 45 words")
    mechanism = response["generic_mechanism"]
    if (not isinstance(mechanism, str) or not mechanism.strip() or
            len(mechanism.split()) > 40 or any(mark in mechanism for mark in ('"', "“", "”"))):
        raise ValueError("generic_mechanism must be one non-empty string of at most 40 words")
def map_role_response(response, role, ours_key, ref_key):
    validate_role_response(response, role)
    verdict = response["product_parity_verdict"]
    return {
        "dims": {dim: {"ours": response["scores"][dim][ours_key],
                       "ref": response["scores"][dim][ref_key]}
                 for dim in ROLE_SPECS[role]["dims"]},
        "critical_ours": response["critical_failures"][ours_key],
        "critical_ref": response["critical_failures"][ref_key],
        "product_parity_verdict": (
            "ours" if verdict == ours_key else "ref" if verdict == ref_key else "tie"),
        "confidence": response["confidence"],
        "paraphrased_evidence": {"ours": response["paraphrased_evidence"][ours_key],
                                 "ref": response["paraphrased_evidence"][ref_key]},
        "generic_mechanism": response["generic_mechanism"],
    }
