"""Regression evidence for Stage-A v2.1 comparative stability semantics."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
import judge_protocol as V2
import native_judge as N


ROOT = Path(__file__).parents[3]
IDENTICAL = ROOT / "calibration/runs/run-012/judgments/controls/identical"
FAILURE = "generic_self_help_voice"


def record(order, scores=None, ours_failures=(), ref_failures=(), verdict="tie"):
    dims = V2.ROLE_SPECS["craft"]["dims"]
    return {
        "model": "gpt-5.6-sol", "judge_identity": "replica",
        "role": "craft", "target": "chapter-01", "order": order,
        "mapped": {
            "dims": scores or {dim: {"ours": 7, "ref": 7} for dim in dims},
            "critical_ours": list(ours_failures), "critical_ref": list(ref_failures),
            "product_parity_verdict": verdict, "confidence": 1.0,
            "paraphrased_evidence": {"ours": "Same.", "ref": "Same."},
            "generic_mechanism": "Same comparative effect.",
        },
    }


class RecordedControlRegressionTests(unittest.TestCase):
    def test_new_configuration_invalidates_frozen_v2_control_reuse(self):
        frozen = json.loads((IDENTICAL / "judge-summary.json").read_text(encoding="utf-8"))
        prompts = {role: (ROOT / "calibration/judges" / spec["prompt"]).read_text(
            encoding="utf-8") for role, spec in V2.ROLE_SPECS.items()}
        schemas = {role: N.role_output_schema(spec)
                   for role, spec in V2.ROLE_SPECS.items()}
        config = N.instrument_configuration(
            prompts, schemas, [(1, 1), (2, 2), (3, 3)], N.DEFAULT_IDENTITIES)

        self.assertFalse(frozen["prompt_control"]["passed"])
        self.assertEqual(config["protocol_version"], "stage-a-v2.2-native-sol-ultra-1")
        self.assertNotEqual(config["role_prompt_sha256"],
                            frozen["instrument_configuration"]["role_prompt_sha256"])
        self.assertIn("role_output_schema_sha256", config)
        self.assertNotEqual(config, frozen["instrument_configuration"])
        self.assertNotEqual(config["implementation_sha256"],
                            frozen["instrument_configuration"]["implementation_sha256"])

    def test_run012_records_are_comparatively_stable_but_retain_absolute_drift(self):
        records = [json.loads(path.read_text(encoding="utf-8"))
                   for path in sorted(IDENTICAL.glob("**/o?.json"))]
        summary = V2.aggregate_v2(records)

        self.assertEqual(len(records), 20)
        self.assertEqual(summary["collapsed_observations"], 10)
        self.assertEqual(summary["order_instability"]["observations"], 0)
        self.assertEqual(summary["absolute_drift"], {
            "critical_label_observations": 4,
            "score_observations": 9,
            "max_same_text_score_shift": 3,
        })
        self.assertTrue(V2.evaluate_control(summary, "identical")["passed"])


class ComparativeSignatureTests(unittest.TestCase):
    def test_score_winner_or_relative_critical_flip_is_unstable(self):
        dims = V2.ROLE_SPECS["craft"]["dims"]
        winning = {dim: {"ours": 8, "ref": 7} for dim in dims}
        losing = {dim: {"ours": 7, "ref": 8} for dim in dims}
        cases = (
            [record(0, winning, verdict="ours"), record(1, losing, verdict="ours")],
            [record(0, ours_failures=(FAILURE,)),
             record(1, ref_failures=(FAILURE,))],
        )
        for records in cases:
            with self.subTest(records=records):
                summary = V2.aggregate_v2(records)
                self.assertEqual(summary["order_instability"]["observations"], 1)
                self.assertIsNone(
                    summary["product_parity"]["overall_preference_rate_incl_half_ties"])

    def test_within_call_critical_asymmetry_fails_identical_control(self):
        summary = V2.aggregate_v2([
            record(0, ours_failures=(FAILURE,)),
            record(1, ours_failures=(FAILURE,)),
        ])
        observation = summary["observations"][0]
        control_input = {"panel_complete": True, "observations": [observation]}

        self.assertFalse(observation["order_instability"]["unstable"])
        self.assertFalse(V2.evaluate_control(control_input, "identical")["passed"])

    def test_absolute_label_drift_preserves_unioned_safety_signal(self):
        summary = V2.aggregate_v2([
            record(0),
            record(1, ours_failures=(FAILURE,), ref_failures=(FAILURE,)),
        ])
        observation = summary["observations"][0]

        self.assertFalse(observation["order_instability"]["unstable"])
        self.assertTrue(observation["absolute_drift"]["critical_failures_changed"])
        self.assertEqual(observation["critical_ours"], [FAILURE])
        self.assertEqual(observation["critical_ref"], [FAILURE])


if __name__ == "__main__":
    unittest.main()
