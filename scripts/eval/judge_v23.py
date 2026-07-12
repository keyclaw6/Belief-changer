"""Pooled, order-balanced aggregation for the Stage-A v2.3 judge panel."""
import json
from collections import Counter, defaultdict
from copy import deepcopy
from judge_protocol import ROLE_SPECS
VERDICT_VALUE = {"ours": 1.0, "tie": 0.5, "ref": 0.0}
CORE_FAILURE = {"efficacy": "incoherent_block_arc", "craft": "broken_chapter_flow", "integrity": "broken_continuity"}
TRANSFORM_DIMS = {"efficacy": ("cumulative_progression",),
                  "craft": ("flow_and_momentum", "ending_handoff"),
                  "integrity": ("cross_chapter_consistency",)}
def _expected(configuration):
    errors = []
    if configuration.get("protocol_version") != "stage-a-v2.3-native-sol-ultra-1":
        errors.append("configuration is not Stage-A v2.3")
    fixed = {"transport": "native-codex-subscription", "model": "gpt-5.6-sol",
             "reasoning_effort": "ultra"}
    if any(configuration.get(key) != value for key, value in fixed.items()):
        errors.append("configuration violates the frozen native Sol-ultra transport")
    identities = configuration.get("replica_identities", [])
    if (not isinstance(identities, list) or len(identities) != 2 or
            any(not isinstance(identity, str) for identity in identities) or
            len(set(identities)) != 2):
        errors.append("configuration requires exactly two replica labels")
        identities = []
    pairs = configuration.get("chapter_pairs", [])
    if (not isinstance(pairs, list) or len(pairs) != 3 or
            any(not isinstance(pair, (list, tuple)) or len(pair) != 2 or
                any(isinstance(n, bool) or not isinstance(n, int) or n < 1 for n in pair)
                for pair in pairs) or
            len({tuple(pair) for pair in pairs}) != 3):
        errors.append("configuration requires three unique chapter pairs")
        pairs = []
    schemas = configuration.get("role_output_schema_sha256", {})
    if (not isinstance(schemas, dict) or set(schemas) != set(ROLE_SPECS) or
            not all(isinstance(v, str) and v for v in schemas.values())):
        errors.append("configuration lacks the three role schema hashes")
    craft = [f"chapter-{ours:02d}" if ours == ref else
             f"chapter-{ours:02d}-vs-{ref:02d}" for ours, ref in pairs]
    targets = {"efficacy": ["block"], "craft": craft, "integrity": ["block"]}
    cells = {(role, target, identity, order) for role, values in targets.items()
             for target in values for identity in identities for order in (0, 1)}
    return identities, targets, cells, errors
def _mapped_valid(mapped, role):
    if not isinstance(mapped, dict) or mapped.get("product_parity_verdict") not in VERDICT_VALUE:
        return False
    dims = mapped.get("dims")
    if not isinstance(dims, dict) or set(dims) != set(ROLE_SPECS[role]["dims"]):
        return False
    if any(not isinstance(pair, dict) or set(pair) != {"ours", "ref"} or
           any(isinstance(value, bool) or not isinstance(value, (int, float)) or not 1 <= value <= 9
               for value in pair.values()) for pair in dims.values()):
        return False
    return all(isinstance(mapped.get(key), list) and
               all(isinstance(label, str) for label in mapped[key]) and
               set(mapped[key]) <= ROLE_SPECS[role]["failures"]
               for key in ("critical_ours", "critical_ref"))
def _record(record, configuration, identities, targets, map_response):
    errors = []
    role, target, order = record.get("role"), record.get("target"), record.get("order")
    identity, transport = record.get("judge_identity"), record.get("transport")
    if role not in targets or target not in targets.get(role, []):
        errors.append("unexpected role target")
    if order not in (0, 1) or isinstance(order, bool):
        errors.append("order must be 0 or 1")
    if identity not in identities:
        errors.append("unexpected replica label")
    if (record.get("protocol") != "stage-a-v2.3" or
            record.get("model") != configuration.get("model")):
        errors.append("record protocol or model mismatch")
    if not isinstance(transport, dict):
        transport = {}
        errors.append("missing transport")
    expected = {"kind": configuration.get("transport"), "model": configuration.get("model"),
                "reasoning_effort": configuration.get("reasoning_effort"),
                "judge_identity": identity, "fresh_ephemeral_context": True, "returncode": 0}
    if any(transport.get(key) != value for key, value in expected.items()):
        errors.append("transport configuration mismatch")
    for key in ("thread_id", "input_sha256", "output_schema_sha256"):
        if not isinstance(transport.get(key), str) or not transport[key]:
            errors.append(f"transport lacks {key}")
    if role in ROLE_SPECS and transport.get("output_schema_sha256") != configuration.get(
            "role_output_schema_sha256", {}).get(role):
        errors.append("output schema hash mismatch")
    forbidden = ("retry", "retried", "repair", "repaired", "extraction", "extracted",
                 "tolerant_parse")
    if any(record.get(key) or transport.get(key) for key in forbidden):
        errors.append("response used retry, repair, extraction, or tolerant parsing")
    if (record.get("attempts", 1) != 1 or record.get("validation_error") or
            record.get("parse_mode", "strict") != "strict"):
        errors.append("response was not one strict-valid first response")
    parsed = None
    try:
        if not isinstance(record.get("raw"), str):
            raise ValueError("raw response is not text")
        parsed = json.loads(record["raw"])
        if not isinstance(parsed, dict) or record.get("parsed") != parsed:
            raise ValueError("raw response and cached parse differ")
    except (json.JSONDecodeError, ValueError) as exc:
        errors.append(f"strict raw parsing failed: {exc}")
    rebuilt = None
    if parsed is not None and role in ROLE_SPECS and order in (0, 1):
        ours_key, ref_key = (("A", "B") if order == 0 else ("B", "A"))
        try:
            rebuilt = map_response(parsed, role, ours_key, ref_key)
        except (AttributeError, KeyError, TypeError, ValueError) as exc:
            errors.append(f"parsed response failed remapping: {exc}")
    if rebuilt is not None and (not _mapped_valid(rebuilt, role) or record.get("mapped") != rebuilt):
        errors.append("stored mapping does not match raw A/B plus order")
    return {"role": role, "target": target, "order": order, "identity": identity,
            "transport": transport, "mapped": rebuilt}, errors
def _diagnostic(rows):
    verdicts = Counter(row["mapped"]["product_parity_verdict"] for row in rows)
    dims = {}
    for dim in ROLE_SPECS[rows[0]["role"]]["dims"]:
        pairs = sorted([row["mapped"]["dims"][dim]["ours"],
                        row["mapped"]["dims"][dim]["ref"]] for row in rows)
        dims[dim] = {"pairs": pairs, "ours_values": sorted(pair[0] for pair in pairs),
                     "ref_values": sorted(pair[1] for pair in pairs),
                     "winner_signs": sorted((a > b) - (a < b) for a, b in pairs)}
    critical_pairs = sorted([[sorted(set(row["mapped"]["critical_ours"])),
                              sorted(set(row["mapped"]["critical_ref"]))] for row in rows])
    return {"verdict_counts": {key: verdicts[key] for key in VERDICT_VALUE},
            "verdict_mean": sum(VERDICT_VALUE[key] * count
                                for key, count in verdicts.items()) / len(rows),
            "scores": dims, "critical_pairs": critical_pairs}
def _contradiction(row):
    mapped = row["mapped"]
    ours = (all(pair["ours"] > pair["ref"] for pair in mapped["dims"].values()) and
            set(mapped["critical_ours"]) <= set(mapped["critical_ref"]))
    ref = (all(pair["ref"] > pair["ours"] for pair in mapped["dims"].values()) and
           set(mapped["critical_ref"]) <= set(mapped["critical_ours"]))
    dominant = "ours" if ours else "ref" if ref else None
    if dominant and mapped["product_parity_verdict"] != dominant:
        return {"role": row["role"], "target": row["target"], "order": row["order"],
                "judge_identity": row["identity"], "thread_id": row["transport"]["thread_id"],
                "dominant": dominant, "verdict": mapped["product_parity_verdict"]}
    return None
def aggregate(records, configuration, map_response):
    """Validate and pool the exact twenty-cell, five-target v2.3 matrix."""
    configuration = deepcopy(configuration)
    identities, targets, expected_cells, errors = _expected(configuration)
    rows, seen, invalid = [], Counter(), 0
    for index, record in enumerate(records):
        row, row_errors = _record(record, configuration, identities, targets, map_response)
        seen[(row["role"], row["target"], row["identity"], row["order"])] += 1
        if row_errors:
            invalid += 1
            errors.extend(f"record {index}: {error}" for error in row_errors)
        else:
            rows.append(row)
    if len(records) != 20:
        errors.append("matrix requires exactly 20 raw cells")
    if set(seen) != expected_cells or any(count != 1 for count in seen.values()):
        errors.append("matrix role-target-replica-order cells are incomplete or duplicated")
    threads = [row["transport"].get("thread_id") for row in rows]
    if len(threads) != 20 or len(set(threads)) != 20:
        errors.append("matrix requires 20 unique fresh thread IDs")
    strata = defaultdict(list)
    for row in rows:
        strata[(row["role"], row["target"], row["order"])].append(row)
    for key, group in strata.items():
        if (len(group) != 2 or len({row["transport"]["input_sha256"] for row in group}) != 1 or
                len({row["transport"]["output_schema_sha256"] for row in group}) != 1):
            errors.append(f"stratum {key} lacks two matching input/schema hashes")
    observations, contradictions = [], []
    for role in ROLE_SPECS:
        for target in targets.get(role, []):
            group = [row for row in rows if row["role"] == role and row["target"] == target]
            by_order = {order: [row for row in group if row["order"] == order] for order in (0, 1)}
            diagnostics = {str(order): _diagnostic(items) for order, items in by_order.items()
                           if len(items) == 2}
            mean = (sum(item["verdict_mean"] for item in diagnostics.values()) / 2
                    if len(diagnostics) == 2 else None)
            verdicts = Counter(row["mapped"]["product_parity_verdict"] for row in group)
            found = sorted((item for row in group if (item := _contradiction(row))),
                           key=lambda item: (item["order"], item["judge_identity"], item["thread_id"]))
            contradictions.extend(found)
            critical = {side: sorted({label for row in group
                                      for label in row["mapped"][f"critical_{side}"]})
                        for side in ("ours", "ref")}
            observations.append({"role": role, "target": target, "raw_judgments": len(group),
                "preference_rate_incl_half_ties": mean,
                "verdict_counts": {key: verdicts[key] for key in VERDICT_VALUE},
                "target_noninferiority_passed": len(group) == 4 and verdicts["ref"] <= 1,
                "critical_ours": critical["ours"], "critical_ref": critical["ref"],
                "order_diagnostics": diagnostics,
                "order_mean_gap": (abs(diagnostics["0"]["verdict_mean"] -
                                       diagnostics["1"]["verdict_mean"])
                                   if len(diagnostics) == 2 else None),
                "strict_dominance_contradictions": found})
    roles = {}
    for role in ROLE_SPECS:
        values = [item["preference_rate_incl_half_ties"] for item in observations
                  if item["role"] == role]
        roles[role] = {"targets": len(values), "preference_rate_incl_half_ties":
                       sum(values) / len(values) if values and None not in values else None}
    role_values = [item["preference_rate_incl_half_ties"] for item in roles.values()]
    critical = {side: sorted({label for item in observations for label in item[f"critical_{side}"]})
                for side in ("ours", "ref")}
    matrix = {"passed": not errors, "violations": errors, "expected_raw_cells": 20,
              "raw_cells": len(records), "expected_strata": 10, "strata": len(strata),
              "expected_unique_thread_ids": 20, "unique_thread_ids": len(set(threads))}
    return {"protocol": "stage-a-v2.3", "instrument_configuration": configuration,
            "raw_judgments": len(records), "invalid_judgments": invalid,
            "strict_valid_first_responses": len(rows), "collapsed_observations": len(observations),
            "panel_complete": matrix["passed"], "matrix": matrix, "observations": observations,
            "replica_aggregation": "pooled within order; replica labels are trace metadata only",
            "strict_dominance_contradictions": contradictions,
            "critical_ours": critical["ours"], "critical_ref": critical["ref"],
            "target_noninferiority_passed": bool(observations) and all(
                item["target_noninferiority_passed"] for item in observations),
            "product_parity": {"roles": roles, "equal_role_macro_preference_rate":
                sum(role_values) / 3 if None not in role_values else None}}
def evaluate_control(summary, mode):
    if mode not in ("identical", "degraded-reference"):
        raise ValueError("control mode must be identical or degraded-reference")
    observations = summary.get("observations", [])
    valid = (summary.get("panel_complete") and summary.get("raw_judgments") == 20 and
             summary.get("invalid_judgments") == 0 and len(observations) == 5)
    if mode == "identical":
        semantic = all(item["verdict_counts"] == {"ours": 0, "tie": 4, "ref": 0} and
            all(all(a == b for dim in order["scores"].values() for a, b in dim["pairs"]) and
                all(ours == ref for ours, ref in order["critical_pairs"])
                for order in item["order_diagnostics"].values()) for item in observations)
    else:
        semantic = all(item["verdict_counts"] == {"ours": 0, "tie": 0, "ref": 4} and
            all(CORE_FAILURE[item["role"]] in ours and CORE_FAILURE[item["role"]] not in ref
                for order in item["order_diagnostics"].values()
                for ours, ref in order["critical_pairs"]) and
            all(all(a < b for a, b in order["scores"][dim]["pairs"])
                for order in item["order_diagnostics"].values()
                for dim in TRANSFORM_DIMS[item["role"]]) for item in observations)
    passed = bool(valid and semantic and not summary.get("strict_dominance_contradictions"))
    return {"mode": mode, "passed": passed, "matrix_transport_valid": bool(valid),
            "semantic_expectation_met": bool(semantic),
            "instrument_configuration": deepcopy(summary.get("instrument_configuration"))}
def evaluate_product(summary, validated_controls):
    controls = (list(validated_controls.values()) if isinstance(validated_controls, dict)
                else list(validated_controls or []))
    by_mode = {item.get("mode"): item for item in controls if isinstance(item, dict)}
    if isinstance(validated_controls, dict):
        by_mode = {mode: value for mode, value in validated_controls.items()
                   if mode in ("identical", "degraded-reference") and isinstance(value, dict)}
    config = summary.get("instrument_configuration")
    controls_pass = (set(by_mode) == {"identical", "degraded-reference"} and len(controls) == 2 and
                     all(item.get("mode") == mode and item.get("passed") is True and
                         item.get("instrument_configuration") == config
                         for mode, item in by_mode.items()))
    roles = summary.get("product_parity", {}).get("roles", {})
    role_pass = set(roles) == set(ROLE_SPECS) and all(
        item.get("preference_rate_incl_half_ties") is not None and
        item["preference_rate_incl_half_ties"] >= .35 for item in roles.values())
    macro = summary.get("product_parity", {}).get("equal_role_macro_preference_rate")
    checks = {"validated_controls": controls_pass, "panel_complete": bool(summary.get("panel_complete")),
              "target_noninferiority": bool(summary.get("target_noninferiority_passed")),
              "verdict_rubric_coherence": not summary.get("strict_dominance_contradictions"),
              "critical_safety": not summary.get("critical_ours"),
              "role_thresholds": role_pass, "macro_threshold": macro is not None and macro >= .45}
    return {"passed": all(checks.values()), "checks": checks,
            "thresholds": {"equal_role_macro": .45, "each_role": .35}}
