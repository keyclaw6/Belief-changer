"""Integration tests for the canonical role-separated v2.3 judge protocol."""
import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
from collections import defaultdict
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parents[1]))
import judge_panel as J
import judge_protocol as V2


def role_response(role, order, mapped_verdict="tie"):
    ours_key, ref_key = (("A", "B") if order == 0 else ("B", "A"))
    verdict = (ours_key if mapped_verdict == "ours" else
               ref_key if mapped_verdict == "ref" else "tie")
    return {
        "scores": {dim: {"A": 7, "B": 7} for dim in V2.ROLE_SPECS[role]["dims"]},
        "critical_failures": {"A": [], "B": []},
        "product_parity_verdict": verdict,
        "confidence": 0.8,
        "paraphrased_evidence": {
            "A": "The candidate advances its argument clearly.",
            "B": "The candidate advances its argument clearly.",
        },
        "generic_mechanism": "Clear causal progression makes belief movement easier to follow.",
    }


def native_answers(mapped_verdict="tie", events=None):
    calls = []
    schemas = {role: J.N.role_output_schema(spec) for role, spec in V2.ROLE_SPECS.items()}
    def answer(content, identity, schema):
        index = len(calls)
        order = index % 2
        role = next(role for role, expected in schemas.items() if schema == expected)
        parsed = role_response(role, order, mapped_verdict)
        raw = json.dumps(parsed)
        calls.append((content, identity, schema))
        if events is not None:
            events.append("complete")
        return raw, {
            "kind": "native-codex-subscription", "model": J.N.MODEL,
            "reasoning_effort": J.N.REASONING_EFFORT, "judge_identity": identity,
            "fresh_ephemeral_context": True, "returncode": 0,
            "thread_id": f"thread-{index:02d}",
            "input_sha256": hashlib.sha256(content.encode()).hexdigest(),
            "output_schema_sha256": hashlib.sha256(J.N._schema_bytes(schema)).hexdigest(),
        }, None
    return calls, answer


def chapters():
    return [(Path(f"chapter-{number}.md"), f"Chapter {number}. More text.")
            for number in range(1, 4)]


class RoleSchemaTests(unittest.TestCase):
    def test_roles_and_mapping_remain_authoritative(self):
        self.assertEqual({role: spec["scope"] for role, spec in V2.ROLE_SPECS.items()},
                         {"efficacy": "block", "craft": "chapter",
                          "integrity": "block"})
        parsed = role_response("craft", 1, "ours")
        mapped = V2.map_role_response(parsed, "craft", "B", "A")
        self.assertEqual(mapped["product_parity_verdict"], "ours")
        self.assertEqual(set(mapped["dims"]), set(V2.ROLE_SPECS["craft"]["dims"]))

    def test_schema_rejects_detection_probe_quotes_and_extra_fields(self):
        mutations = [
            lambda value: value.__setitem__("which_is_real_carr", "B"),
            lambda value: value["paraphrased_evidence"].__setitem__("A", 'It says "words".'),
            lambda value: value.__setitem__("confidence", True),
            lambda value: value.__setitem__("generic_mechanism", "word " * 41),
        ]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                parsed = role_response("efficacy", 0)
                mutate(parsed)
                with self.assertRaises(ValueError):
                    V2.validate_role_response(parsed, "efficacy")

    def test_prompts_keep_role_schema_and_no_authorship_probe(self):
        for role, spec in V2.ROLE_SPECS.items():
            with self.subTest(role=role):
                text = (J.JUDGE_DIR / spec["prompt"]).read_text(encoding="utf-8")
                self.assertIn("product_parity_verdict", text)
                self.assertIn("generic_mechanism", text)
                self.assertNotIn("which_is_real_carr", text)
                for dim in spec["dims"]:
                    self.assertIn(dim, text)


class CanonicalRunnerTests(unittest.TestCase):
    def test_identical_control_writes_exact_valid_twenty_call_matrix(self):
        calls, answer = native_answers()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            argv = ["judge_panel.py", "--ours", "ours", "--ref", "ref",
                    "--control", "identical", "--out", str(out)]
            with (mock.patch.object(sys, "argv", argv),
                  mock.patch.object(J.SCOPE, "guard"),
                  mock.patch.object(J.E, "load_chapters", side_effect=[chapters(), chapters()]),
                  mock.patch.object(J.N, "complete", side_effect=answer),
                  mock.patch.object(J.N, "finalize_controls"),
                  contextlib.redirect_stdout(io.StringIO())):
                J.main()
            summary = json.loads((out / "judge-summary.json").read_text(encoding="utf-8"))
            records = [json.loads(path.read_text(encoding="utf-8"))
                       for path in out.glob("*/*/*/o*.json")]

        self.assertEqual(len(calls), 20)
        self.assertEqual(summary["protocol"], "stage-a-v2.3")
        self.assertEqual(summary["collapsed_observations"], 5)
        self.assertTrue(summary["canonical"] and summary["matrix"]["passed"])
        self.assertTrue(summary["prompt_control"]["passed"])
        self.assertEqual(len(records), 20)
        self.assertEqual(len({r["transport"]["thread_id"] for r in records}), 20)
        strata = defaultdict(list)
        for record in records:
            self.assertEqual(json.loads(record["raw"]), record["parsed"])
            ours, ref = (("A", "B") if record["order"] == 0 else ("B", "A"))
            self.assertEqual(V2.map_role_response(
                record["parsed"], record["role"], ours, ref), record["mapped"])
            self.assertEqual(record["transport"]["output_schema_sha256"], summary[
                "instrument_configuration"]["role_output_schema_sha256"][record["role"]])
            strata[(record["role"], record["target"], record["order"])].append(record)
        self.assertEqual(len(strata), 10)
        for group in strata.values():
            self.assertEqual(len({r["transport"]["input_sha256"] for r in group}), 1)
            self.assertEqual(len({r["transport"]["output_schema_sha256"] for r in group}), 1)

    def test_product_gate_failure_is_written_and_does_not_fail_process(self):
        events = []
        calls, answer = native_answers("ref", events)
        def validate(_paths, configuration):
            events.append("validate")
            return {mode: {"mode": mode, "passed": True,
                    "instrument_configuration": configuration,
                    "summary": f"{mode}.json", "sha256": mode}
                    for mode in ("identical", "degraded-reference")}
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            argv = ["judge_panel.py", "--ours", "ours", "--ref", "ref",
                    "--validated-controls", J.SCOPE.HF.canonical_argument(),
                    "--out", str(out)]
            stdout = io.StringIO()
            with (mock.patch.object(sys, "argv", argv),
                  mock.patch.object(J.SCOPE, "guard"),
                  mock.patch.object(J.E, "load_chapters", side_effect=[chapters(), chapters()]),
                  mock.patch.object(J.N, "validate_controls", side_effect=validate),
                  mock.patch.object(J.N, "complete", side_effect=answer),
                  contextlib.redirect_stdout(stdout)):
                J.main()
            summary = json.loads((out / "judge-summary.json").read_text(encoding="utf-8"))
        self.assertEqual(events[0], "validate")
        self.assertEqual(len(calls), 20)
        self.assertTrue(summary["panel_complete"])
        gate = summary["product_parity"]["stage_a_judge_gate"]
        self.assertFalse(gate["passed"])
        self.assertFalse(json.loads(stdout.getvalue())["stage_a_judge_gate"]["passed"])

    def test_failed_control_exits_after_writing_diagnostic_summary(self):
        _calls, answer = native_answers("tie")
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            argv = ["judge_panel.py", "--ours", "ours", "--ref", "ref",
                    "--control", "degraded-reference", "--out", str(out)]
            with (mock.patch.object(sys, "argv", argv),
                  mock.patch.object(J.SCOPE, "guard"),
                  mock.patch.object(J.E, "load_chapters", side_effect=[chapters(), chapters()]),
                  mock.patch.object(J.N, "complete", side_effect=answer),
                  contextlib.redirect_stdout(io.StringIO())):
                with self.assertRaises(SystemExit):
                    J.main()
            summary = json.loads((out / "judge-summary.json").read_text(encoding="utf-8"))
        self.assertTrue(summary["panel_complete"])
        self.assertFalse(summary["prompt_control"]["passed"])

    def test_canonical_rejects_api_flags_before_loading_or_calling(self):
        argv = ["judge_panel.py", "--ours", "ours", "--ref", "ref",
                "--models", "openai/gpt-5.6-sol", "--out", "out"]
        with (mock.patch.object(sys, "argv", argv),
              mock.patch.object(J.E, "load_chapters") as load,
              mock.patch.object(J.N, "complete") as complete,
              contextlib.redirect_stderr(io.StringIO())):
            with self.assertRaises(SystemExit):
                J.main()
        load.assert_not_called()
        complete.assert_not_called()


class MaterialTests(unittest.TestCase):
    def test_controls_use_identical_and_degraded_reference_materials(self):
        sample = [(Path("chapter.md"), "One. Two. Three. Four. Five. Six.")]
        identical = J.stage_a_materials(sample, sample, [(1, 1)], "identical")
        degraded = J.stage_a_materials(sample, sample, [(1, 1)], "degraded-reference")
        self.assertEqual(identical["craft"][0]["ours"], identical["craft"][0]["ref"])
        self.assertNotEqual(degraded["craft"][0]["ours"], degraded["craft"][0]["ref"])


if __name__ == "__main__":
    unittest.main()
