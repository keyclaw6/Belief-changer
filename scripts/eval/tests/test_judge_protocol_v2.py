"""Regression tests for the Stage-A role-separated judge protocol."""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parents[1]))
import judge_panel as J
import judge_protocol as V2


def role_response(role, a=7, b=8, verdict="B"):
    return {
        "scores": {dim: {"A": a, "B": b} for dim in V2.ROLE_SPECS[role]["dims"]},
        "critical_failures": {"A": [], "B": []},
        "product_parity_verdict": verdict,
        "confidence": 0.8,
        "paraphrased_evidence": {
            "A": "The argument advances but leaves part of the benefit intact.",
            "B": "The argument converts its premise into a more complete shift.",
        },
        "generic_mechanism": "Demonstrated causal steps move belief more reliably than asserted conclusions.",
    }


def mapped_record(model, role, target, order, response, judge_identity=None):
    ours, ref = ("A", "B") if order == 0 else ("B", "A")
    return {"model": model, "role": role, "target": target, "order": order,
            "judge_identity": judge_identity or model,
            "mapped": V2.map_role_response(response, role, ours, ref)}


class RoleSchemaTests(unittest.TestCase):
    def test_each_role_has_distinct_scope_dimensions_and_failures(self):
        """Infra: Stage-A roles remain separate measurement instruments."""
        self.assertEqual(V2.ROLE_SPECS["craft"]["scope"], "chapter")
        self.assertEqual(V2.ROLE_SPECS["efficacy"]["scope"], "block")
        self.assertEqual(V2.ROLE_SPECS["integrity"]["scope"], "block")
        self.assertEqual(len({tuple(spec["dims"]) for spec in V2.ROLE_SPECS.values()}), 3)

    def test_schema_rejects_detection_probe_quotes_and_extra_fields(self):
        """Infra: v2 cannot silently restore authorship detection or quoted evidence."""
        mutations = [
            lambda value: value.__setitem__("which_is_real_carr", "B"),
            lambda value: value["paraphrased_evidence"].__setitem__("A", 'It says "copied words".'),
            lambda value: value.__setitem__("confidence", True),
            lambda value: value.__setitem__("generic_mechanism", "word " * 41),
        ]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                response = role_response("efficacy")
                mutate(response)
                with self.assertRaises(ValueError):
                    V2.validate_role_response(response, "efficacy")

    def test_prompts_use_role_schema_without_carr_detection(self):
        """Infra: shipped prompts expose the validated blind schema."""
        for role, spec in V2.ROLE_SPECS.items():
            with self.subTest(role=role):
                text = (J.JUDGE_DIR / spec["prompt"]).read_text(encoding="utf-8")
                self.assertIn("product_parity_verdict", text)
                self.assertIn("generic_mechanism", text)
                self.assertNotIn("which_is_real_carr", text)
                for dim in spec["dims"]:
                    self.assertIn(dim, text)


class RepeatedOrderAggregationTests(unittest.TestCase):
    def test_two_orders_collapse_to_one_model_role_target_observation(self):
        """Infra: position swaps are repeated measures, never independent votes."""
        records = [
            mapped_record("google/model", "craft", "chapter-01", 0,
                          role_response("craft", 7, 8, "B")),
            mapped_record("google/model", "craft", "chapter-01", 1,
                          role_response("craft", 8, 7, "A")),
        ]
        summary = V2.aggregate_v2(records)
        observation = summary["observations"][0]

        self.assertEqual(summary["raw_judgments"], 2)
        self.assertEqual(summary["collapsed_observations"], 1)
        self.assertEqual(observation["product_parity_verdict"], "ref")
        self.assertEqual(observation["dims"]["prose_control"],
                         {"ours_mean": 7.0, "ref_mean": 8.0})
        self.assertFalse(observation["order_instability"]["unstable"])

    def test_order_disagreement_is_reported_not_turned_into_a_tie_vote(self):
        """Infra: presentation sensitivity remains visible in the product signal."""
        records = [
            mapped_record("google/model", "efficacy", "block", 0,
                          role_response("efficacy", 7, 8, "B")),
            mapped_record("google/model", "efficacy", "block", 1,
                          role_response("efficacy", 8, 7, "B")),
        ]
        summary = V2.aggregate_v2(records)

        self.assertEqual(summary["observations"][0]["product_parity_verdict"], "unstable")
        self.assertEqual(summary["order_instability"]["observations"], 1)
        self.assertIsNone(summary["product_parity"]["overall_preference_rate_incl_half_ties"])

    def test_product_comparison_is_separate_from_causal_movement(self):
        """Infra: a reference comparison cannot certify an experiment's cause."""
        records = [
            mapped_record("google/model", "integrity", "block", 0,
                          role_response("integrity", 7, 8, "B")),
            mapped_record("google/model", "integrity", "block", 1,
                          role_response("integrity", 8, 7, "A")),
        ]
        summary = V2.aggregate_v2(records)

        self.assertIn("product_parity", summary)
        self.assertNotIn("real_detection_accuracy", summary)
        self.assertEqual(summary["causal_movement"]["status"], "not measured")
        self.assertEqual(summary["product_parity"]["threshold_verdict"],
                         "not applied by instrument")

    def test_incomplete_role_identity_target_matrix_fails_closed(self):
        """Infra: every judge identity must judge the same targets in every role."""
        records = []
        for role in V2.ROLE_SPECS:
            for model in ("google/a", "openai/b"):
                for order in (0, 1):
                    records.append(mapped_record(
                        model, role, "block" if role != "craft" else "chapter-01",
                        order, role_response(role, 7, 7, "tie")))
        for order in (0, 1):
            records.append(mapped_record(
                "google/a", "craft", "chapter-02", order,
                role_response("craft", 7, 7, "tie")))

        summary = V2.aggregate_v2(records)

        self.assertFalse(summary["role_judge_identity_matrix_complete"])
        self.assertFalse(summary["panel_complete"])

    def test_empty_panel_is_incomplete(self):
        """Infra: absence of observations can never pass a panel."""
        self.assertFalse(V2.aggregate_v2([])["panel_complete"])


class StageAMatrixTests(unittest.TestCase):
    def test_canonical_v2_rejects_api_model_flags_before_loading(self):
        """Infra: canonical judging cannot route GPT through a provider API."""
        argv = ["judge_panel.py", "--ours", "ours", "--ref", "ref",
                "--models", "openai/gpt-5.6-sol",
                "--reasoning-efforts", "openai/gpt-5.6-sol=max", "--out", "out"]
        with (mock.patch.object(sys, "argv", argv),
              mock.patch.object(J.E, "load_chapters") as load,
              mock.patch.object(J.N, "complete") as complete,
              contextlib.redirect_stderr(io.StringIO())):
            with self.assertRaises(SystemExit):
                J.main()
        load.assert_not_called()
        complete.assert_not_called()

    def test_default_cli_runs_two_fresh_identities_across_balanced_matrix(self):
        """Infra: two same-model replications cover every role, target, and order."""
        chapters = [(Path(f"chapter-{number}.md"), f"Chapter {number}. More text.")
                    for number in range(1, 4)]

        def answer(content, identity):
            for role, spec in V2.ROLE_SPECS.items():
                if f'`{spec["dims"][0]}`' in content:
                    return json.dumps(role_response(role, 7, 7, "tie")), {
                        "judge_identity": identity}, None
            raise AssertionError("unknown role prompt")

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            argv = ["judge_panel.py", "--ours", "ours", "--ref", "ref",
                    "--chapters", "1-3", "--control", "identical", "--out", str(out)]
            with (mock.patch.object(sys, "argv", argv),
                  mock.patch.object(J.E, "load_chapters", side_effect=[chapters, chapters]),
                  mock.patch.object(J.N, "complete", side_effect=answer) as complete,
                  contextlib.redirect_stdout(io.StringIO())):
                J.main()

            summary = json.loads((out / "judge-summary.json").read_text(encoding="utf-8"))
            self.assertEqual(complete.call_count, 20)
            self.assertTrue(summary["panel_complete"])
            self.assertEqual(summary["collapsed_observations"], 10)
            self.assertTrue(summary["role_judge_identity_matrix_complete"])
            self.assertEqual(summary["product_parity"]["equal_role_macro_preference_rate"],
                             0.5)
            replications = summary["judge_replications"]
            self.assertEqual(replications["design"],
                             "independent fresh-context same-model replications")
            self.assertFalse(replications["cross_family_evidence"])
            self.assertEqual(replications["identities"], list(J.N.DEFAULT_IDENTITIES))
            self.assertTrue((out / "craft" / "chapter-01" / "sol-ultra-r1" /
                             "o0.json").is_file())
            self.assertTrue((out / "efficacy" / "block" / "sol-ultra-r2" /
                             "o1.json").is_file())


class PromptControlTests(unittest.TestCase):
    def test_control_materials_use_identical_and_degraded_reference_pairs(self):
        """Infra: prompt controls never require a second orchestration system."""
        chapters = [(Path("chapter.md"), "One. Two. Three. Four. Five. Six.")]
        identical = J.stage_a_materials(chapters, chapters, [(1, 1)], "identical")
        degraded = J.stage_a_materials(chapters, chapters, [(1, 1)], "degraded-reference")

        self.assertEqual(identical["craft"][0]["ours"], identical["craft"][0]["ref"])
        self.assertNotEqual(degraded["craft"][0]["ours"], degraded["craft"][0]["ref"])
        self.assertEqual(degraded["craft"][0]["ref"], chapters[0][1])
        formatted = [(Path("chapter.md"), "# Heading\n\n*Emphasis*.")]
        product = J.stage_a_materials(formatted, formatted, [(1, 1)])
        self.assertEqual(product["craft"][0]["ours"], product["craft"][0]["ref"])

    def test_control_verdicts_fail_closed(self):
        """Infra: semantic prompt controls have explicit pass conditions."""
        observation = {"complete": True, "product_parity_verdict": "tie",
                       "critical_ours": [], "critical_ref": [],
                       "order_instability": {"unstable": False,
                                             "max_within_order_candidate_gap": 0}}
        summary = {"panel_complete": True, "observations": [observation]}
        self.assertTrue(V2.evaluate_control(summary, "identical")["passed"])

        observation["product_parity_verdict"] = "ref"
        self.assertTrue(V2.evaluate_control(summary, "degraded-reference")["passed"])
        observation["order_instability"]["unstable"] = True
        self.assertFalse(V2.evaluate_control(summary, "degraded-reference")["passed"])

    def test_cli_exits_nonzero_when_semantic_control_fails(self):
        """Infra: a written control failure cannot be mistaken for validation."""
        chapters = [(Path(f"chapter-{number}.md"), f"Chapter {number}. More text.")
                    for number in range(1, 4)]

        def tie(content, identity):
            for role, spec in V2.ROLE_SPECS.items():
                if f'`{spec["dims"][0]}`' in content:
                    return json.dumps(role_response(role, 7, 7, "tie")), {
                        "judge_identity": identity}, None
            raise AssertionError("unknown role prompt")

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            argv = ["judge_panel.py", "--ours", "ours", "--ref", "ref",
                    "--chapters", "1-3", "--control", "degraded-reference",
                    "--out", str(out)]
            with (mock.patch.object(sys, "argv", argv),
                  mock.patch.object(J.E, "load_chapters", side_effect=[chapters, chapters]),
                  mock.patch.object(J.N, "complete", side_effect=tie),
                  contextlib.redirect_stdout(io.StringIO())):
                with self.assertRaises(SystemExit):
                    J.main()

            summary = json.loads((out / "judge-summary.json").read_text(encoding="utf-8"))
            self.assertFalse(summary["prompt_control"]["passed"])


if __name__ == "__main__":
    unittest.main()
