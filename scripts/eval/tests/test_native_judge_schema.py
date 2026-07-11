"""Regression tests for the Stage-A v2.2 native structured-output schema."""
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).parents[1]))
import judge_protocol as V2
import native_judge as N


class NativeOutputSchemaTests(unittest.TestCase):
    def assert_closed_objects(self, node):
        if isinstance(node, dict):
            if node.get("type") == "object":
                self.assertEqual(set(node), {
                    "type", "properties", "required", "additionalProperties"})
                self.assertEqual(node["required"], list(node["properties"]))
                self.assertFalse(node["additionalProperties"])
            for value in node.values():
                self.assert_closed_objects(value)
        elif isinstance(node, list):
            for value in node:
                self.assert_closed_objects(value)

    def test_every_role_schema_is_exact_closed_and_bounded(self):
        expected_fields = [
            "scores", "critical_failures", "product_parity_verdict", "confidence",
            "paraphrased_evidence", "generic_mechanism",
        ]
        for role, spec in V2.ROLE_SPECS.items():
            with self.subTest(role=role):
                schema = N.role_output_schema(spec)
                fields = schema["properties"]
                self.assertEqual(schema["required"], expected_fields)
                self.assertEqual(list(fields), expected_fields)
                self.assert_closed_objects(schema)
                scores = fields["scores"]
                self.assertEqual(list(scores["properties"]), list(spec["dims"]))
                for pair in scores["properties"].values():
                    self.assertEqual(list(pair["properties"]), ["A", "B"])
                    for value in pair["properties"].values():
                        self.assertEqual(value, {
                            "type": "number", "minimum": 1, "maximum": 9})
                failures = fields["critical_failures"]["properties"]
                self.assertEqual(list(failures), ["A", "B"])
                for value in failures.values():
                    self.assertEqual(value, {"type": "array", "items": {
                        "type": "string", "enum": sorted(spec["failures"])}})
                self.assertEqual(fields["product_parity_verdict"], {
                    "type": "string", "enum": ["A", "B", "tie"]})
                self.assertEqual(fields["confidence"], {
                    "type": "number", "minimum": 0, "maximum": 1})
                evidence = fields["paraphrased_evidence"]["properties"]
                self.assertEqual(evidence, {
                    "A": {"type": "string"}, "B": {"type": "string"}})
                self.assertEqual(fields["generic_mechanism"], {"type": "string"})

    def test_canonical_schema_serialization_is_deterministic(self):
        schema = N.role_output_schema(V2.ROLE_SPECS["craft"])
        reversed_root = dict(reversed(list(schema.items())))

        self.assertEqual(N._schema_bytes(schema), N._schema_bytes(reversed_root))
        self.assertEqual(N._schema_bytes(schema), json.dumps(
            schema, sort_keys=True, separators=(",", ":")).encode())

    def test_malformed_final_message_is_never_repaired_or_retried(self):
        """Infra: wrapper validation remains fail-closed and single-attempt."""
        calls = []
        malformed = '{"answer": 1,}'
        events = "\n".join(json.dumps(event) for event in (
            {"type": "thread.started", "thread_id": "thread-1"},
            {"type": "item.completed", "item": {
                "type": "agent_message", "text": malformed}},
            {"type": "turn.completed", "usage": {}},
        ))

        def run(*_args, **_kwargs):
            calls.append(True)
            return SimpleNamespace(returncode=0, stdout=events, stderr="")

        raw, transport, error = N.complete(
            "input", "r1", N.role_output_schema(V2.ROLE_SPECS["craft"]), run=run)
        self.assertEqual((calls, raw, error), ([True], malformed, None))
        self.assertEqual(transport["event_stream"], events)

    def test_schema_hash_is_part_of_control_configuration_identity(self):
        prompts = {role: "prompt " + role for role in V2.ROLE_SPECS}
        schemas = {role: N.role_output_schema(spec)
                   for role, spec in V2.ROLE_SPECS.items()}
        changed = copy.deepcopy(schemas)
        changed["craft"]["properties"]["confidence"]["maximum"] = 0.9
        args = ([(1, 1), (2, 2), (3, 3)], N.DEFAULT_IDENTITIES)

        baseline = N.instrument_configuration(prompts, schemas, *args)
        mutation = N.instrument_configuration(prompts, changed, *args)

        self.assertEqual(baseline["protocol_version"],
                         "stage-a-v2.2-native-sol-ultra-1")
        self.assertEqual(baseline["role_prompt_sha256"],
                         mutation["role_prompt_sha256"])
        self.assertNotEqual(baseline["role_output_schema_sha256"],
                            mutation["role_output_schema_sha256"])
        expected = hashlib.sha256(N._schema_bytes(schemas["craft"])).hexdigest()
        self.assertEqual(baseline["role_output_schema_sha256"]["craft"], expected)
        self.assertNotEqual(baseline, mutation)


class ControlRepairPredictionTests(unittest.TestCase):
    def test_degraded_control_requires_every_core_label_in_both_orders(self):
        """Infra: v2.2 cannot pass on verdict direction while losing taxonomy anchors."""
        core = {"efficacy": "incoherent_block_arc", "craft": "broken_chapter_flow",
                "integrity": "broken_continuity"}
        roles = ["efficacy"] * 2 + ["craft"] * 6 + ["integrity"] * 2
        observations = []
        for role in roles:
            signatures = [{"ours_only": [core[role]], "ref_only": []} for _ in range(2)]
            observations.append({"complete": True, "role": role,
                "product_parity_verdict": "ref", "order_instability": {
                    "unstable": False, "comparative_signatures": signatures,
                    "relative_critical_failures_changed": False}})
        summary = {"panel_complete": True, "raw_judgments": 20,
                   "invalid_judgments": 0, "observations": observations}
        result = V2.evaluate_control(summary, "degraded-reference")
        self.assertTrue(result["passed"])
        self.assertTrue(result["repair_predictions"]["structured_output"]["passed"])
        self.assertTrue(result["repair_predictions"]["critical_taxonomy"]["passed"])
        observations[0]["order_instability"]["relative_critical_failures_changed"] = True
        repairs = V2.evaluate_control(summary, "degraded-reference")["repair_predictions"]
        self.assertTrue(repairs["structured_output"]["passed"])
        self.assertFalse(repairs["critical_taxonomy"]["passed"])
        observations[0]["order_instability"]["relative_critical_failures_changed"] = False
        for observation in observations:
            with self.subTest(role=observation["role"]):
                signature = observation["order_instability"]["comparative_signatures"][0]
                label = signature["ours_only"].pop()
                self.assertFalse(V2.evaluate_control(
                    summary, "degraded-reference")["passed"])
                signature["ours_only"].append(label)

    def test_repair_outcomes_remain_independently_visible(self):
        summary = {"panel_complete": False, "raw_judgments": 20,
                   "invalid_judgments": 1, "observations": []}
        repairs = V2.evaluate_control(summary, "identical")["repair_predictions"]
        self.assertFalse(repairs["structured_output"]["passed"])
        self.assertFalse(repairs["critical_taxonomy"]["scorable"])


if __name__ == "__main__":
    unittest.main()
