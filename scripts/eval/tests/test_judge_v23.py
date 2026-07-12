"""Preregistered synthetic tests for the Stage-A v2.3 aggregation freeze."""
import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
import judge_protocol as V2
import judge_v23 as V23
CONFIG = {
    "protocol_version": "stage-a-v2.3-native-sol-ultra-1",
    "transport": "native-codex-subscription", "model": "gpt-5.6-sol",
    "reasoning_effort": "ultra", "replica_identities": ["replica-1", "replica-2"],
    "chapter_pairs": [[1, 1], [2, 2], [3, 3]],
    "role_output_schema_sha256": {role: f"schema-{role}" for role in V2.ROLE_SPECS},
}
TARGETS = {"efficacy": ["block"],
           "craft": ["chapter-01", "chapter-02", "chapter-03"],
           "integrity": ["block"]}
def response(role, order, ours=8, ref=7, verdict="ours", ours_critical=(), ref_critical=(),
             dim_scores=None):
    ours_key, ref_key = (("A", "B") if order == 0 else ("B", "A"))
    raw_verdict = ours_key if verdict == "ours" else ref_key if verdict == "ref" else "tie"
    scores = {dim: {ours_key: ours, ref_key: ref} for dim in V2.ROLE_SPECS[role]["dims"]}
    for dim, pair in (dim_scores or {}).items():
        scores[dim] = {ours_key: pair[0], ref_key: pair[1]}
    return {
        "scores": scores,
        "critical_failures": {ours_key: list(ours_critical), ref_key: list(ref_critical)},
        "product_parity_verdict": raw_verdict, "confidence": 1,
        "paraphrased_evidence": {"A": "Candidate A advances its argument clearly.",
                                  "B": "Candidate B advances its argument clearly."},
        "generic_mechanism": "Clear causal progression makes a belief shift easier to follow.",
    }
def make_records(spec=None):
    records = []
    for role, targets in TARGETS.items():
        for target in targets:
            for identity in CONFIG["replica_identities"]:
                for order in (0, 1):
                    values = spec(role, target, identity, order) if spec else {}
                    parsed = response(role, order, **values)
                    ours_key, ref_key = (("A", "B") if order == 0 else ("B", "A"))
                    mapped = V2.map_role_response(parsed, role, ours_key, ref_key)
                    records.append({
                        "protocol": "stage-a-v2.3", "role": role, "target": target,
                        "order": order, "model": CONFIG["model"], "judge_identity": identity,
                        "raw": json.dumps(parsed), "parsed": parsed, "mapped": mapped,
                        "transport": {"kind": CONFIG["transport"], "model": CONFIG["model"],
                            "reasoning_effort": CONFIG["reasoning_effort"],
                            "judge_identity": identity, "fresh_ephemeral_context": True,
                            "returncode": 0, "thread_id": f"{role}-{target}-{identity}-{order}",
                            "input_sha256": f"input-{role}-{target}-{order}",
                            "output_schema_sha256": CONFIG["role_output_schema_sha256"][role]},
                    })
    return records
def aggregate(records):
    return V23.aggregate(records, CONFIG, V2.map_role_response)
def observation(summary, role, target):
    return next(item for item in summary["observations"]
                if item["role"] == role and item["target"] == target)
class PooledAggregationTests(unittest.TestCase):
    def test_replica_permutation_and_record_order_are_decision_invariant(self):
        """HARNESS §9: replica labels are trace-only within each order stratum."""
        varied = lambda _r, _t, identity, order: {"ours": 7, "ref": 7,
            "verdict": "ours" if (identity == "replica-1") == (order == 0) else "tie"}
        base, original = make_records(varied), aggregate(make_records(varied))
        swap = {"replica-1": "replica-2", "replica-2": "replica-1"}
        strata = sorted({(r["role"], r["target"], r["order"]) for r in base})
        for mask in range(1 << len(strata)):
            permuted = copy.deepcopy(base)
            selected = {key for bit, key in enumerate(strata) if mask & (1 << bit)}
            for record in permuted:
                if (record["role"], record["target"], record["order"]) in selected:
                    record["judge_identity"] = swap[record["judge_identity"]]
                    record["transport"]["judge_identity"] = record["judge_identity"]
            self.assertEqual(original, aggregate(list(reversed(permuted))))
        self.assertTrue(original["matrix"]["passed"])
        self.assertEqual([r["mapped"]["product_parity_verdict"] for r in base[:4]],
                         ["ours", "tie", "tie", "ours"])
    def test_order_reversal_stays_in_means_but_fails_target_guard(self):
        """HARNESS §9: a polarized target cannot average into apparent parity."""
        def split(role, target, identity, order):
            if role == "craft" and target == "chapter-01":
                return {"ours": 7, "ref": 7, "verdict": "ours" if order == 0 else "ref"}
            return {}
        summary = aggregate(make_records(split))
        target = observation(summary, "craft", "chapter-01")
        self.assertEqual(target["preference_rate_incl_half_ties"], .5)
        self.assertEqual(target["order_mean_gap"], 1)
        self.assertFalse(target["target_noninferiority_passed"])
        self.assertAlmostEqual(summary["product_parity"]["roles"]["craft"]
                               ["preference_rate_incl_half_ties"], 5 / 6)

    def test_symmetric_dominance_and_unique_critical_exception(self):
        """HARNESS §9: dominance is symmetric after order remapping."""
        cases = [
            ({"ours": 8, "ref": 7, "verdict": "tie"}, "ours"),
            ({"ours": 7, "ref": 8, "verdict": "ours"}, "ref"),
        ]
        for order in (0, 1):
            for values, dominant in cases:
                with self.subTest(order=order, dominant=dominant):
                    def contradiction(role, target, identity, cell_order, values=values):
                        return values if (role, target, identity, cell_order) == (
                            "craft", "chapter-01", "replica-1", order) else {}
                    found = aggregate(make_records(contradiction))[
                        "strict_dominance_contradictions"]
                    self.assertEqual(len(found), 1)
                    self.assertEqual(found[0]["dominant"], dominant)
                    self.assertEqual(found[0]["order"], order)
        def exception(role, target, identity, order):
            if (role, target, identity, order) == ("craft", "chapter-01", "replica-1", 1):
                return {"ours": 8, "ref": 7, "verdict": "ref",
                        "ours_critical": ("repetitive_sag",)}
            return {}
        self.assertEqual(aggregate(make_records(exception))[
            "strict_dominance_contradictions"], [])

    def test_critical_union_includes_single_and_shared_raw_labels(self):
        """HARNESS §9: every raw critical label survives conservative unioning."""
        def critical(role, target, identity, order):
            if role == "craft" and target == "chapter-02" and identity == "replica-1":
                return ({"ours_critical": ("repetitive_sag",),
                         "ref_critical": ("repetitive_sag",)} if order == 0 else
                        {"ours_critical": ("weak_ending_handoff",)})
            return {}
        target = observation(aggregate(make_records(critical)), "craft", "chapter-02")
        self.assertEqual(target["critical_ours"], ["repetitive_sag", "weak_ending_handoff"])
        self.assertEqual(target["critical_ref"], ["repetitive_sag"])
class ValidationMutationTests(unittest.TestCase):
    def test_matrix_hash_thread_raw_and_remap_mutations_fail_closed(self):
        """HARNESS §9: every matrix, transport, hash, raw parse, and remap miss is fatal."""
        mutations = {
            "matrix": lambda rows: rows.pop(),
            "duplicate_coordinate": lambda rows: rows.__setitem__(-1, copy.deepcopy(rows[0])),
            "identity": lambda rows: (rows[0].__setitem__("judge_identity", "rogue"),
                                      rows[0]["transport"].__setitem__("judge_identity", "rogue")),
            "thread": lambda rows: rows[1]["transport"].__setitem__(
                "thread_id", rows[0]["transport"]["thread_id"]),
            "input_hash": lambda rows: rows[1]["transport"].__setitem__("input_sha256", "changed"),
            "schema_hash": lambda rows: rows[0]["transport"].__setitem__(
                "output_schema_sha256", "changed"),
            "transport": lambda rows: rows[0]["transport"].__setitem__(
                "fresh_ephemeral_context", False),
            "cached_parse": lambda rows: rows[0]["parsed"].__setitem__("confidence", .5),
            "malformed_raw": lambda rows: rows[0].__setitem__("raw", "{"),
            "remap": lambda rows: rows[0]["mapped"].__setitem__("product_parity_verdict", "tie"),
            "protocol": lambda rows: rows[0].__setitem__("protocol", "stage-a-v2.2"),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                rows = make_records()
                mutate(rows)
                summary = aggregate(rows)
                self.assertFalse(summary["panel_complete"])
                self.assertFalse(summary["matrix"]["passed"])
                self.assertTrue(summary["matrix"]["violations"])

    def test_frozen_configuration_mutations_fail_closed(self):
        """HARNESS §9: records cannot validate under a changed frozen configuration."""
        mutations = [
            lambda cfg: cfg.__setitem__("protocol_version", "stage-a-v2.2"),
            lambda cfg: cfg.__setitem__("protocol_version", "stage-a-v2.3-other"),
            lambda cfg: cfg.__setitem__("model", "changed"),
            lambda cfg: cfg["chapter_pairs"].__setitem__(0, [1, 2]),
            lambda cfg: cfg["role_output_schema_sha256"].__setitem__("craft", "changed"),
        ]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                config = copy.deepcopy(CONFIG)
                mutate(config)
                summary = V23.aggregate(make_records(), config, V2.map_role_response)
                self.assertFalse(summary["panel_complete"])
                self.assertTrue(summary["matrix"]["violations"])
class ControlAndProductTests(unittest.TestCase):
    @staticmethod
    def identical(spec=None):
        def values(role, target, identity, order):
            base = {"ours": 7, "ref": 7, "verdict": "tie"}
            base.update(spec(role, target, identity, order) if spec else {})
            return base
        return aggregate(make_records(values))

    @staticmethod
    def degraded(spec=None):
        def values(role, target, identity, order):
            base = {"ours": 3, "ref": 8, "verdict": "ref",
                    "ours_critical": (V23.CORE_FAILURE[role],)}
            base.update(spec(role, target, identity, order) if spec else {})
            return base
        return aggregate(make_records(values))

    def test_controls_pass_and_raw_semantic_mutations_fail(self):
        """HARNESS §9: identical and gross-degraded controls enforce every raw anchor."""
        self.assertTrue(V23.evaluate_control(self.identical(), "identical")["passed"])
        self.assertTrue(V23.evaluate_control(self.degraded(), "degraded-reference")["passed"])
        mutations = [
            (self.identical, lambda r, t, i, o: {"verdict": "ours"} if i == "replica-1" and o == 0 else {}),
            (self.identical, lambda r, t, i, o: {"ours": 8} if i == "replica-1" and o == 0 else {}),
            (self.identical, lambda r, t, i, o: {"ours_critical": (next(iter(
                V2.ROLE_SPECS[r]["failures"])),)} if i == "replica-1" and o == 0 else {}),
            (self.degraded, lambda r, t, i, o: {"ours_critical": ()} if i == "replica-1" and o == 0 else {}),
            (self.degraded, lambda r, t, i, o: {"ours_critical": (),
                "ref_critical": (V23.CORE_FAILURE[r],)} if i == "replica-1" and o == 0 else {}),
            (self.degraded, lambda r, t, i, o: {"ours": 8, "ref": 8} if i == "replica-1" and o == 0 else {}),
        ]
        for builder, mutate in mutations:
            mode = "identical" if builder == self.identical else "degraded-reference"
            with self.subTest(mode=mode):
                self.assertFalse(V23.evaluate_control(builder(mutate), mode)["passed"])

    def test_degraded_allows_secondary_label_and_unnamed_dimension_variation(self):
        """HARNESS §9: non-core labels and non-transform dimensions remain diagnostic."""
        def variation(role, target, identity, order):
            if identity != "replica-1" or order != 0:
                return {}
            secondary = next(label for label in V2.ROLE_SPECS[role]["failures"]
                             if label != V23.CORE_FAILURE[role])
            unnamed = next(dim for dim in V2.ROLE_SPECS[role]["dims"]
                           if dim not in V23.TRANSFORM_DIMS[role])
            return {"ours_critical": (V23.CORE_FAILURE[role], secondary),
                    "dim_scores": {unnamed: (8, 2)}}
        result = V23.evaluate_control(self.degraded(variation), "degraded-reference")
        self.assertTrue(result["passed"])

    def test_product_threshold_safety_coherence_guard_and_controls(self):
        """HARNESS §5/§9: product applies controls, thresholds, safety, and guards."""
        controls = {
            "identical": V23.evaluate_control(self.identical(), "identical"),
            "degraded-reference": V23.evaluate_control(
                self.degraded(), "degraded-reference"),
        }
        product = aggregate(make_records())
        self.assertTrue(V23.evaluate_product(product, controls)["passed"])
        mutations = [
            lambda value: value.__setitem__("critical_ours", ["publication_blocker"]),
            lambda value: value.__setitem__("target_noninferiority_passed", False),
            lambda value: value.__setitem__("strict_dominance_contradictions", [{}]),
            lambda value: value["product_parity"].__setitem__(
                "equal_role_macro_preference_rate", .449),
            lambda value: value["product_parity"]["roles"]["craft"].__setitem__(
                "preference_rate_incl_half_ties", .349),
            lambda value: value.__setitem__("panel_complete", False),
        ]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                changed = copy.deepcopy(product)
                mutate(changed)
                self.assertFalse(V23.evaluate_product(changed, controls)["passed"])
        wrong = copy.deepcopy(controls)
        wrong["identical"]["instrument_configuration"]["model"] = "changed"
        self.assertFalse(V23.evaluate_product(product, wrong)["passed"])
        for invalid in ({}, [], {"identical": controls["identical"]},
                        {**controls, "identical": {**controls["identical"], "mode": "wrong"}},
                        {**controls, "identical": {**controls["identical"], "passed": False}}):
            with self.subTest(invalid_controls=invalid):
                self.assertFalse(V23.evaluate_product(product, invalid)["passed"])
if __name__ == "__main__":
    unittest.main()
