"""Regression tests for subscription-backed canonical judge transport."""
import hashlib
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

sys.path.insert(0, str(Path(__file__).parents[1]))
import judge_panel as J
import native_judge as N

TRANSPORT_SCHEMA = {
    "type": "object", "properties": {"answer": {"type": "number"}},
    "required": ["answer"], "additionalProperties": False,
}

def event_stream(message="{}"):
    events = [
        {"type": "thread.started", "thread_id": "thread-1"},
        {"type": "turn.started"},
        {"type": "item.completed",
         "item": {"type": "agent_message", "text": message}},
        {"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 5}},
    ]
    return "\n".join(json.dumps(event) for event in events)

class NativeTransportTests(unittest.TestCase):
    def test_command_is_pinned_fresh_read_only_and_has_no_output_cap(self):
        """Infra: every native observation uses the exact fixed Sol-ultra boundary."""
        calls = []

        def run(cmd, **kwargs):
            schema_path = Path(cmd[cmd.index("--output-schema") + 1])
            calls.append((cmd, kwargs,
                          stat.S_IMODE(os.stat(kwargs["cwd"]).st_mode),
                          stat.S_IMODE(schema_path.stat().st_mode),
                          json.loads(schema_path.read_text(encoding="utf-8"))))
            return SimpleNamespace(returncode=0, stdout=event_stream('{"answer": 1}'),
                                   stderr="")

        secrets = {"OPENROUTER_API_KEY": "secret", "MINIMAX_API_KEY": "secret",
                   "LINEAR_API_KEY": "secret", "OPENAI_BASE_URL": "secret"}
        with mock.patch.dict(os.environ, secrets):
            raw, transport, error = N.complete(
                "frozen input", "replica-1", TRANSPORT_SCHEMA, run=run)

        cmd, kwargs, mode, schema_mode, written_schema = calls[0]
        self.assertEqual(cmd[:11], [
            "codex", "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
            "--disable", "multi_agent", "--model", "gpt-5.6-sol",
            "-c", "model_reasoning_effort=ultra"])
        self.assertIn(["--sandbox", "read-only"], [cmd[i:i + 2] for i in range(len(cmd) - 1)])
        self.assertIn("--skip-git-repo-check", cmd)
        self.assertIn("--output-schema", cmd)
        self.assertNotIn("max_output_tokens", " ".join(cmd))
        self.assertEqual(kwargs["input"], "frozen input")
        self.assertTrue(kwargs["cwd"].startswith("/tmp/belief-changer-judge-"))
        self.assertEqual(mode & 0o222, 0)
        self.assertEqual(schema_mode & 0o222, 0)
        self.assertEqual(written_schema, TRANSPORT_SCHEMA)
        self.assertTrue(all(name not in kwargs["env"] for name in secrets))
        self.assertTrue(set(kwargs["env"]).issubset(N.NATIVE_ENV_ALLOWLIST))
        self.assertEqual(raw, '{"answer": 1}')
        self.assertIsNone(error)
        self.assertEqual(transport["output_limit"], "none set by harness")
        self.assertIn("no provider API keys", transport["environment_policy"])
        self.assertIn("<isolated-tmp>/judge-output-schema.json", transport["command"])
        self.assertEqual(transport["event_stream"], event_stream('{"answer": 1}'))
        canonical = json.dumps(TRANSPORT_SCHEMA, sort_keys=True,
                               separators=(",", ":")).encode()
        self.assertEqual(transport["output_schema_sha256"],
                         hashlib.sha256(canonical).hexdigest())
    def test_each_completion_gets_a_distinct_ephemeral_context(self):
        """Infra: judge identities are independent calls, not one resumed context."""
        workdirs = []

        def run(_cmd, **kwargs):
            workdirs.append(kwargs["cwd"])
            return SimpleNamespace(returncode=0, stdout=event_stream(), stderr="")

        N.complete("same", "r1", TRANSPORT_SCHEMA, run=run)
        N.complete("same", "r2", TRANSPORT_SCHEMA, run=run)

        self.assertEqual(len(set(workdirs)), 2)
    def test_nonzero_process_and_invalid_event_stream_are_observable(self):
        """Infra: native transport defects become invalid records, never judgments."""
        cases = [
            (SimpleNamespace(returncode=9, stdout="partial", stderr="failure"),
             "native Codex exited 9"),
            (SimpleNamespace(returncode=0, stdout="not-json", stderr=""),
             "invalid native Codex JSONL event"),
            (SimpleNamespace(returncode=0, stdout=json.dumps({"type": "turn.started"}),
                             stderr=""), "no final agent message"),
            (SimpleNamespace(returncode=0, stdout="\n".join([
                json.dumps({"type": "item.completed", "item": {
                    "type": "agent_message", "text": "{}"}}),
                json.dumps({"type": "turn.completed", "usage": {}})]), stderr=""),
             "no thread identity"),
        ]
        for result, expected in cases:
            with self.subTest(expected=expected):
                raw, transport, error = N.complete(
                    "input", "r1", TRANSPORT_SCHEMA,
                    run=lambda *_args, **_kwargs: result)
                self.assertEqual(raw, "")
                self.assertIn(expected, error)
                self.assertIn("event_stream", transport)
    def test_process_launch_error_is_an_invalid_transport_result(self):
        """Infra: a missing native runner fails closed without losing diagnostics."""
        raw, transport, error = N.complete(
            "input", "r1", TRANSPORT_SCHEMA,
            run=lambda *_args, **_kwargs: (_ for _ in ()).throw(
                FileNotFoundError("codex missing")))

        self.assertEqual(raw, "")
        self.assertIn("launch failed", error)
        self.assertIn("codex missing", transport["stderr"])
class NativeRoleRecordTests(unittest.TestCase):
    def test_role_call_preserves_frozen_prompt_material_and_swapped_order(self):
        """Infra: native transport changes no judge prompt, material, order, or schema."""
        seen = []
        schema = N.role_output_schema(J.ROLE_SPECS["craft"])
        cfg = {"prompts": {"craft": "FROZEN ROLE PROMPT"},
               "schemas": {"craft": schema}}
        cell = {"target": "chapter-01", "ours": "OURS", "ref": "REFERENCE",
                "ours_chapters": [1], "ref_chapters": [1]}

        def complete(content, identity, output_schema):
            seen.append((content, identity, output_schema))
            response = {
                "scores": {dim: {"A": 7, "B": 7}
                           for dim in J.ROLE_SPECS["craft"]["dims"]},
                "critical_failures": {"A": [], "B": []},
                "product_parity_verdict": "tie", "confidence": 0.8,
                "paraphrased_evidence": {"A": "Controlled prose.",
                                           "B": "Controlled prose."},
                "generic_mechanism": "Controlled progression supports reader attention.",
            }
            return json.dumps(response), {"kind": "test"}, None

        with mock.patch.object(J.N, "complete", side_effect=complete):
            first = J.judge_role(cfg, "r1", "craft", cell, 0)
            second = J.judge_role(cfg, "r1", "craft", cell, 1)

        self.assertEqual([(content, identity) for content, identity, _schema in seen], [
            ("FROZEN ROLE PROMPT\n\n=== TEXT A ===\nOURS\n\n=== TEXT B ===\nREFERENCE", "r1"),
            ("FROZEN ROLE PROMPT\n\n=== TEXT A ===\nREFERENCE\n\n=== TEXT B ===\nOURS", "r1"),
        ])
        self.assertTrue(all(output_schema is schema for _, _, output_schema in seen))
        self.assertEqual(first["model"], "gpt-5.6-sol")
        self.assertEqual(first["protocol"], "stage-a-v2.3")
        self.assertEqual(first["judge_identity"], "r1")
        self.assertEqual(first["mapped"]["product_parity_verdict"], "tie")
        self.assertEqual(second["mapped"]["product_parity_verdict"], "tie")

    def test_invalid_native_schema_stays_unmapped(self):
        """Infra: a final agent message is not evidence until v2 validation passes."""
        cfg = {"prompts": {"craft": "prompt"},
               "schemas": {"craft": N.role_output_schema(J.ROLE_SPECS["craft"])}}
        cell = {"target": "chapter-01", "ours": "ours", "ref": "ref",
                "ours_chapters": [1], "ref_chapters": [1]}
        with mock.patch.object(J.N, "complete", return_value=("{}", {}, None)):
            record = J.judge_role(cfg, "r1", "craft", cell, 0)

        self.assertNotIn("mapped", record)
        self.assertIn("schema", record["validation_error"])

    def test_canonical_response_must_be_only_the_json_object(self):
        """Infra: forbidden prose around valid JSON cannot bypass the v2 schema."""
        cfg = {"prompts": {"craft": "prompt"},
               "schemas": {"craft": N.role_output_schema(J.ROLE_SPECS["craft"])}}
        cell = {"target": "chapter-01", "ours": "ours", "ref": "ref",
                "ours_chapters": [1], "ref_chapters": [1]}
        wrapped = 'authorship guess\n{"scores": {}}'
        with mock.patch.object(J.N, "complete", return_value=(wrapped, {}, None)):
            record = J.judge_role(cfg, "r1", "craft", cell, 0)

        self.assertNotIn("mapped", record)
        self.assertEqual(record["validation_error"],
                         "response is not one strict JSON object")


class CanonicalPreflightTests(unittest.TestCase):
    def test_exact_two_safe_identity_labels(self):
        """Infra: the frozen native baseline cannot silently change replica count."""
        self.assertEqual(N.parse_identities("r1,r2"), ["r1", "r2"])
        for raw in ("r1", "r1,r1", "r1,r2,r3", "r/1,r2"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                N.parse_identities(raw)

    def test_product_rejects_caller_supplied_synthetic_controls(self):
        """Infra: self-described summaries outside H-F04 never become authority."""
        prompts = {role: "prompt " + role for role in J.ROLE_SPECS}
        schemas = {role: N.role_output_schema(spec)
                   for role, spec in J.ROLE_SPECS.items()}
        config = N.instrument_configuration(
            prompts, schemas, [(1, 1), (2, 2), (3, 3)], N.DEFAULT_IDENTITIES)
        with tempfile.TemporaryDirectory() as tmp:
            paths = []
            for mode in ("identical", "degraded-reference"):
                path = Path(tmp) / f"{mode}.json"
                path.write_text(json.dumps({
                    "protocol": "stage-a-v2.3",
                    "canonical": True, "panel_complete": True,
                    "raw_judgments": 20, "invalid_judgments": 0,
                    "collapsed_observations": 5, "matrix": {"passed": True},
                    "instrument_configuration": config,
                    "prompt_control": {"mode": mode, "passed": True,
                                       "matrix_transport_valid": True,
                                       "semantic_expectation_met": True,
                                       "instrument_configuration": config},
                }), encoding="utf-8")
                paths.append(path)
            with self.assertRaisesRegex(ValueError, "exact canonical ordered"):
                N.validate_controls(",".join(map(str, paths)), config)
    def test_product_cli_without_controls_fails_before_native_call(self):
        """Infra: missing control evidence fails before any product judgment."""
        chapters = [(Path(f"chapter-{number}.md"), "text") for number in range(1, 4)]
        argv = ["judge_panel.py", "--ours", "ours", "--ref", "ref", "--out", "out"]
        with (mock.patch.object(sys, "argv", argv),
              mock.patch.object(J.E, "load_chapters", side_effect=[chapters, chapters]),
              mock.patch.object(J.N, "complete") as complete,
              mock.patch("sys.stderr")):
            with self.assertRaises(SystemExit):
                J.main()
        complete.assert_not_called()

    def test_canonical_cli_rejects_non_three_chapter_matrix(self):
        """Infra: canonical Stage A cannot shrink below its 20-cell design."""
        chapters = [(Path(f"chapter-{number}.md"), "text") for number in range(1, 4)]
        argv = ["judge_panel.py", "--ours", "ours", "--ref", "ref",
                "--chapters", "1-2", "--control", "identical", "--out", "out"]
        with (mock.patch.object(sys, "argv", argv),
              mock.patch.object(J.E, "load_chapters", side_effect=[chapters, chapters]),
              mock.patch.object(J.N, "complete") as complete,
              mock.patch("sys.stderr")):
            with self.assertRaises(SystemExit):
                J.main()
        complete.assert_not_called()
if __name__ == "__main__":
    unittest.main()
