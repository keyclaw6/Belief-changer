"""Regression tests for the blind pairwise judge measurement instrument."""
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


def valid_response():
    return {
        "scores": {dim: {"A": 7, "B": 8} for dim in J.DIMS},
        "critical_failures": {"A": [], "B": ["broken_continuity"]},
        "which_is_real_carr": "B",
        "detection_confidence": 0.8,
        "verdict_better": "B",
        "notes": "B is more convincing.",
    }


class PairwiseSchemaTests(unittest.TestCase):
    def test_complete_response_maps_every_dimension(self):
        """Infra: valid frozen judge schema maps completely."""
        mapped = J.map_verdict(valid_response(), "A", "B")

        self.assertEqual(set(mapped["dims"]), set(J.DIMS))
        self.assertEqual(mapped["verdict"], "ref")
        self.assertTrue(mapped["real_guess_correct"])

    def test_missing_verdict_cannot_fall_through_to_tie(self):
        """Infra: incomplete judge schema cannot become a tie."""
        response = valid_response()
        del response["verdict_better"]

        with self.assertRaisesRegex(ValueError, "verdict_better"):
            J.map_verdict(response, "A", "B")

    def test_every_dimension_requires_numeric_a_and_b_scores(self):
        """Infra: all frozen dimension score cells are required."""
        mutations = [
            lambda p: p["scores"].pop("pacing"),
            lambda p: p["scores"]["click"].pop("B"),
            lambda p: p["scores"]["flow"].__setitem__("A", True),
            lambda p: p["scores"]["warmth"].__setitem__("B", 10),
        ]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                response = valid_response()
                mutate(response)
                with self.assertRaises(ValueError):
                    J.validate_pairwise(response)

    def test_probe_verdict_and_failure_lists_use_frozen_values(self):
        """Infra: judge categorical values stay inside their schema."""
        mutations = [
            ("probe", lambda p: p.__setitem__("which_is_real_carr", "maybe")),
            ("verdict", lambda p: p.__setitem__("verdict_better", "unsure")),
            ("list", lambda p: p["critical_failures"].__setitem__("A", "none")),
            ("item", lambda p: p["critical_failures"]["A"].append("generic_prose")),
            ("confidence-bool", lambda p: p.__setitem__("detection_confidence", True)),
            ("confidence-range", lambda p: p.__setitem__("detection_confidence", 1.1)),
            ("notes-type", lambda p: p.__setitem__("notes", [])),
            ("notes-length", lambda p: p.__setitem__("notes", "word " * 61)),
        ]
        for name, mutate in mutations:
            with self.subTest(name=name):
                response = valid_response()
                mutate(response)
                with self.assertRaises(ValueError):
                    J.validate_pairwise(response)

    @mock.patch.object(J, "chat", return_value='{"scores":')
    def test_malformed_json_is_recorded_without_mapping(self, _chat):
        """Infra: malformed responses remain observable and unmapped."""
        rec = J.judge_pair(
            {"base_url": "x", "api_key": "x", "prompt": "judge",
             "reasoning_efforts": {"model": "high"},
             "max_output_allowances": {"model": 32768}},
            "model", 1, "ours", "ref", 0)

        self.assertNotIn("mapped", rec)
        self.assertIn("validation_error", rec)
        _chat.assert_called_once_with("x", "x", "model", mock.ANY, "high", 32768)


class PanelCompletenessTests(unittest.TestCase):
    def test_invalid_record_marks_panel_incomplete(self):
        """Infra: an invalid call invalidates the panel aggregate."""
        summary = J.aggregate([{"parsed": None}])

        self.assertEqual(summary["invalid_judgments"], 1)
        self.assertFalse(summary["panel_complete"])
        self.assertIsNone(summary["overall_win_rate_incl_half_ties"])

    def test_summary_exposes_overall_and_dimension_rates_per_exact_model(self):
        """Infra: cross-family enforcement has exact-model aggregates."""
        response = valid_response()
        records = [
            {"model": "provider/model-a", "mapped": J.map_verdict(response, "A", "B")},
            {"model": "provider/model-b", "mapped": J.map_verdict(response, "B", "A")},
        ]

        summary = J.aggregate(records)

        self.assertEqual(summary["by_model"]["provider/model-a"]
                         ["overall_win_rate_incl_half_ties"], 0.0)
        self.assertEqual(summary["by_model"]["provider/model-b"]
                         ["dims"]["click"]["win_rate_incl_half_ties"], 1.0)

    def test_all_unsure_probes_produce_neutral_detection_signal(self):
        """Infra: unsure Carr probes contribute the documented neutral score."""
        response = valid_response()
        response["which_is_real_carr"] = "unsure"
        records = [{"model": "provider/model",
                    "mapped": J.map_verdict(response, "A", "B")}]

        self.assertEqual(J.aggregate(records)["real_detection_accuracy"], 0.5)

    def test_main_exits_nonzero_after_writing_incomplete_summary(self):
        """Infra: the CLI cannot silently accept an incomplete panel."""
        good = json.dumps(valid_response())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prompt = root / "prompt.md"
            prompt.write_text("judge", encoding="utf-8")
            out = root / "out"
            argv = ["judge_panel.py", "--ours", "ours", "--ref", "ref",
                    "--chapters", "1", "--models", "judge-model",
                    "--reasoning-efforts", "judge-model=high",
                    "--max-output-allowances", "judge-model=32768",
                    "--prompt", str(prompt), "--out", str(out)]
            chapters = [(Path("chapter.md"), "chapter text")]
            with (mock.patch.object(sys, "argv", argv),
                  mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test"}, clear=True),
                  mock.patch.object(J.E, "load_chapters", return_value=chapters),
                  mock.patch.object(J, "chat", side_effect=[good, '{"scores":']),
                  contextlib.redirect_stdout(io.StringIO())):
                with self.assertRaises(SystemExit):
                    J.main()

            summary = json.loads((out / "judge-summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["invalid_judgments"], 1)
            self.assertFalse(summary["panel_complete"])
            self.assertEqual(summary["protocol"], "legacy-noncanonical-api")
            self.assertFalse(summary["canonical"])


class ReasoningEffortTests(unittest.TestCase):
    def test_chat_sends_explicit_reasoning_effort(self):
        """Infra: every judge request carries its configured reasoning effort."""
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({
            "choices": [{"message": {"content": "ok"}}]}).encode()
        with mock.patch.object(J.urllib.request, "urlopen", return_value=response) as urlopen:
            J.chat("https://example.test", "key", "provider/model", "judge", "max", 65536)

        request = urlopen.call_args.args[0]
        body = json.loads(request.data)
        self.assertEqual(body["reasoning"], {"effort": "max"})
        self.assertEqual(body["max_tokens"], 65536)

    def test_models_metadata_supplies_full_completion_allowance(self):
        """Infra: judge allowance comes from endpoint metadata, not a local cap."""
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({
            "data": [{"id": "provider/model",
                      "top_provider": {"max_completion_tokens": 131072}}]
        }).encode()
        with mock.patch.object(J.M.urllib.request, "urlopen", return_value=response):
            values = J.M.resolve_output_allowances(
                "https://example.test/v1", "key", ["provider/model"])

        self.assertEqual(values, {"provider/model": 131072})

    def test_explicit_endpoint_allowances_are_complete_and_positive(self):
        """Infra: proxy metadata fallback cannot omit or zero a judge ceiling."""
        self.assertEqual(J.M.parse_output_allowances("a=10,b=20", ["a", "b"]),
                         {"a": 10, "b": 20})
        for raw in ("a=10", "a=0,b=20", "a=many,b=20"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                J.M.parse_output_allowances(raw, ["a", "b"])

    def test_main_rejects_missing_model_mapping_before_any_call(self):
        """Infra: reasoning preflight prevents partially configured panels."""
        argv = ["judge_panel.py", "--ours", "ours", "--ref", "ref",
                "--models", "provider/a,provider/b", "--reasoning-efforts", "provider/a=high",
                "--max-output-allowances", "provider/a=100,provider/b=100",
                "--prompt", "prompt", "--out", "out"]
        with (mock.patch.object(sys, "argv", argv),
              mock.patch.object(J, "chat") as chat,
              mock.patch.object(J.E, "load_chapters") as load_chapters,
              contextlib.redirect_stderr(io.StringIO())):
            with self.assertRaises(SystemExit):
                J.main()

        chat.assert_not_called()
        load_chapters.assert_not_called()


class ScopeValidationTests(unittest.TestCase):
    def test_pairs_are_exact_positive_and_in_bounds(self):
        """Infra: explicit chapter pairs cannot wrap or exceed either book."""
        self.assertEqual(J.parse_pairs("1:2,2:1", 2, 2), [(1, 2), (2, 1)])
        for raw in ("0:1", "1:0", "1", "1:2:3", "3:1", "1:3", "1:1,"):
            with self.subTest(raw=raw), self.assertRaises(SystemExit):
                J.parse_pairs(raw, 2, 2)

    def test_main_rejects_empty_model_selection_before_loading(self):
        """Infra: a panel must select at least one judge model."""
        argv = ["judge_panel.py", "--ours", "ours", "--ref", "ref", "--models", ",,",
                "--reasoning-efforts", "provider/a=high", "--prompt", "prompt", "--out", "out"]
        with (mock.patch.object(sys, "argv", argv),
              mock.patch.object(J.E, "load_chapters") as load_chapters,
              mock.patch.object(J, "chat") as chat,
              contextlib.redirect_stderr(io.StringIO())):
            with self.assertRaises(SystemExit):
                J.main()

        load_chapters.assert_not_called()
        chat.assert_not_called()

    def test_main_rejects_zero_pair_before_network_call(self):
        """Infra: zero cannot index the last chapter through the CLI."""
        argv = ["judge_panel.py", "--ours", "ours", "--ref", "ref", "--pairs", "0:1",
                "--models", "provider/a", "--reasoning-efforts", "provider/a=high",
                "--max-output-allowances", "provider/a=100",
                "--prompt", "prompt", "--out", "out"]
        chapters = [(Path("chapter.md"), "chapter text")]
        with (mock.patch.object(sys, "argv", argv),
              mock.patch.object(J.E, "load_chapters", return_value=chapters),
              mock.patch.object(J, "chat") as chat):
            with self.assertRaises(SystemExit):
                J.main()

        chat.assert_not_called()


if __name__ == "__main__":
    unittest.main()
