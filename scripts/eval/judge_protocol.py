"""Response schemas and aggregation for the calibration judge instrument."""
from collections import defaultdict
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
def _collapse_orders(key, records):
    judge_identity, role, target = key
    models = {record["model"] for record in records}
    valid = sorted((record for record in records if record.get("mapped")),
                   key=lambda record: record["order"])
    base = {"judge_identity": judge_identity,
            "model": next(iter(models)) if len(models) == 1 else "inconsistent",
            "role": role, "target": target, "complete": False}
    if len(models) != 1:
        base["validation_error"] = "one judge identity used inconsistent models"
        return base
    if len(valid) != 2 or [record["order"] for record in valid] != [0, 1]:
        base["missing_or_invalid_orders"] = sorted({0, 1} - {record["order"] for record in valid})
        return base
    mapped = [record["mapped"] for record in valid]
    verdicts = [item["product_parity_verdict"] for item in mapped]
    dims, flips, score_signs = {}, [], [{}, {}]
    max_gap = max_within = 0
    for dim in ROLE_SPECS[role]["dims"]:
        pairs = [item["dims"][dim] for item in mapped]
        signs = [(pair["ours"] > pair["ref"]) - (pair["ours"] < pair["ref"]) for pair in pairs]
        for index, sign in enumerate(signs):
            score_signs[index][dim] = sign
        if signs[0] != signs[1]:
            flips.append(dim)
        max_gap = max(max_gap, *(abs(pairs[0][side] - pairs[1][side]) for side in ("ours", "ref")))
        max_within = max(max_within, *(abs(pair["ours"] - pair["ref"]) for pair in pairs))
        dims[dim] = {"ours_mean": round(sum(pair["ours"] for pair in pairs) / 2, 2),
                     "ref_mean": round(sum(pair["ref"] for pair in pairs) / 2, 2)}
    critical_relative = [{
        "ours_only": sorted(set(item["critical_ours"]) - set(item["critical_ref"])),
        "ref_only": sorted(set(item["critical_ref"]) - set(item["critical_ours"])),
    } for item in mapped]
    signatures = [{"verdict": verdicts[index], "score_signs": score_signs[index],
                   **critical_relative[index]} for index in range(2)]
    absolute_critical_changed = any(set(mapped[0][field]) != set(mapped[1][field])
                                    for field in ("critical_ours", "critical_ref"))
    unstable = signatures[0] != signatures[1]
    base.update({
        "complete": True, "dims": dims,
        "product_parity_verdict": verdicts[0] if verdicts[0] == verdicts[1] else "unstable",
        "confidence_mean": round(sum(item["confidence"] for item in mapped) / 2, 3),
        "critical_ours": sorted({item for result in mapped for item in result["critical_ours"]}),
        "critical_ref": sorted({item for result in mapped for item in result["critical_ref"]}),
        "paraphrased_evidence_by_order": [item["paraphrased_evidence"] for item in mapped],
        "generic_mechanism_by_order": [item["generic_mechanism"] for item in mapped],
        "order_instability": {"unstable": unstable,
                              "comparative_signatures": signatures, "verdicts": verdicts,
                              "score_winner_flips": flips,
                              "relative_critical_failures_changed":
                                  critical_relative[0] != critical_relative[1],
                              "max_within_order_candidate_gap": max_within},
        "absolute_drift": {"critical_failures_changed": absolute_critical_changed,
                           "max_same_text_score_shift": max_gap},
    })
    return base
def _rate(observations):
    stable = [item for item in observations
              if item.get("complete") and not item["order_instability"]["unstable"]]
    if not stable:
        return None
    ours = sum(item["product_parity_verdict"] == "ours" for item in stable)
    ties = sum(item["product_parity_verdict"] == "tie" for item in stable)
    return round((ours + 0.5 * ties) / len(stable), 3)
def aggregate_v2(records):
    grouped = defaultdict(list)
    for record in records:
        identity = record.get("judge_identity", record["model"])
        grouped[(identity, record["role"], record["target"])].append(record)
    observations = [_collapse_orders(key, grouped[key]) for key in sorted(grouped)]
    identities = sorted({item[0] for item in grouped})
    models = sorted({record["model"] for record in records})
    role_identities = {
        role: sorted({record.get("judge_identity", record["model"]) for record in records
                      if record["role"] == role}) for role in ROLE_SPECS}
    role_targets = {role: sorted({record["target"] for record in records
                                  if record["role"] == role}) for role in ROLE_SPECS}
    role_target_matrix = {
        role: {identity: sorted({record["target"] for record in records
                                if record["role"] == role and
                                record.get("judge_identity", record["model"]) == identity})
               for identity in identities}
        for role in ROLE_SPECS
    }
    roles = {}
    for role in ROLE_SPECS:
        subset = [item for item in observations if item["role"] == role]
        roles[role] = {"scope": ROLE_SPECS[role]["scope"], "observations": len(subset),
                       "preference_rate_incl_half_ties": _rate(subset),
                       "order_unstable": sum(item.get("order_instability", {}).get("unstable", False)
                                             for item in subset)}
    complete = [item for item in observations if item.get("complete")]
    unstable = [item for item in complete if item["order_instability"]["unstable"]]
    label_drift = [item for item in complete if item["absolute_drift"]["critical_failures_changed"]]
    score_drift = [item for item in complete if item["absolute_drift"]["max_same_text_score_shift"] > 0]
    role_rates = [value["preference_rate_incl_half_ties"] for value in roles.values()
                  if value["preference_rate_incl_half_ties"] is not None]
    invalid = len(records) - sum(bool(record.get("mapped")) for record in records)
    matrix_complete = bool(identities) and all(
        role_identities[role] == identities and role_targets[role] and
        all(role_target_matrix[role][identity] == role_targets[role]
            for identity in identities)
        for role in ROLE_SPECS)
    model_by_identity = {identity: sorted({record["model"] for record in records
                                          if record.get("judge_identity", record["model"])
                                          == identity}) for identity in identities}
    same_model_replicated = len(models) == 1 and len(identities) > 1
    return {
        "protocol": "stage-a-v2.2", "raw_judgments": len(records),
        "collapsed_observations": len(observations), "invalid_judgments": invalid,
        "panel_complete": invalid == 0 and all(item.get("complete") for item in observations)
                          and matrix_complete,
        "judge_replications": {
            "design": ("independent fresh-context same-model replications"
                       if same_model_replicated else "distinct judge identities"),
            "identities": identities, "model_by_identity": model_by_identity,
            "cross_family_evidence": False if same_model_replicated else None,
            "interpretation": ("independent replications, not cross-family evidence"
                               if same_model_replicated else "no cross-family claim")},
        "role_judge_identity_matrix": role_identities,
        "role_target_matrix": role_target_matrix,
        "role_judge_identity_matrix_complete": matrix_complete,
        "order_instability": {"observations": len(unstable),
                              "rate": round(len(unstable) / len(complete), 3) if complete else None,
                              "ids": [f'{item["judge_identity"]}|{item["role"]}|{item["target"]}'
                                      for item in unstable]},
        "absolute_drift": {
            "critical_label_observations": len(label_drift),
            "score_observations": len(score_drift),
            "max_same_text_score_shift": max((item["absolute_drift"]["max_same_text_score_shift"]
                                               for item in complete),
                default=0)},
        "product_parity": {"unit": "collapsed judge-identity-role-target observation",
                           "overall_preference_rate_incl_half_ties": _rate(complete),
                           "equal_role_macro_preference_rate": (
                               round(sum(role_rates) / len(role_rates), 3)
                               if len(role_rates) == len(ROLE_SPECS) else None),
                           "stable_observations": len(complete) - len(unstable),
                           "unstable_observations": len(unstable),
                           "roles": roles, "threshold_verdict": "not applied by instrument"},
        "causal_movement": {"status": "not measured",
                            "reason": "Requires a preregistered candidate-to-candidate experiment."},
        "observations": observations,
    }
def evaluate_control(summary, mode):
    observations = [item for item in summary["observations"] if item.get("complete")]
    first_response_valid = summary.get("raw_judgments") == 20 and summary.get("invalid_judgments") == 0
    label_drift = sum(item["order_instability"]["relative_critical_failures_changed"] for item in observations)
    taxonomy_scorable = first_response_valid and summary["panel_complete"]
    core = {"efficacy": "incoherent_block_arc", "craft": "broken_chapter_flow", "integrity": "broken_continuity"}
    core_retained = None if mode == "identical" else bool(observations) and all(
        len(item["order_instability"]["comparative_signatures"]) == 2 and all(
            core[item["role"]] in signature["ours_only"] and
            core[item["role"]] not in signature["ref_only"]
            for signature in item["order_instability"]["comparative_signatures"])
        for item in observations)
    taxonomy_passed = taxonomy_scorable and label_drift == 0 and core_retained is not False
    if mode == "identical":
        passed = (summary["panel_complete"] and observations and
                  all(item["product_parity_verdict"] == "tie" for item in observations) and
                  all(item["critical_ours"] == item["critical_ref"] and
                      not item["order_instability"]["unstable"] and
                      item["order_instability"]["max_within_order_candidate_gap"] <= 1
                      for item in observations))
        expectation = "identical texts tie without order or critical-failure asymmetry"
    else:
        passed = (summary["panel_complete"] and observations and
                  all(item["product_parity_verdict"] == "ref" and
                      not item["order_instability"]["unstable"] for item in observations) and
                  core_retained)
        expectation = "the intact reference beats its locally degraded copy in every observation"
    repairs = {"structured_output": {"passed": first_response_valid,
        "valid_first_responses": (summary.get("raw_judgments", 0) -
                                  summary.get("invalid_judgments", 0)),
        "expected_first_responses": 20},
        "critical_taxonomy": {"passed": taxonomy_passed,
                              "scorable": taxonomy_scorable,
                              "candidate_relative_label_drift_observations": label_drift,
                              "core_degraded_labels_retained": core_retained}}
    return {"mode": mode, "expectation": expectation, "repair_predictions": repairs,
            "passed": bool(passed and all(value["passed"] for value in repairs.values()))}
