"""Focused RF-10 writer-context authority and fail-closed regressions."""
import contextlib
import io
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
sys.path.insert(0, str(ROOT / "scripts/eval/tests"))
import candidate_pair as PAIR  # noqa: E402
import commission_set as SET  # noqa: E402
import manual_dispatch as MANUAL  # noqa: E402
import run_iteration as RUN  # noqa: E402
import writer_context as WC  # noqa: E402
from test_commission_contract import commission  # noqa: E402
from writer_context_fixture import WriterFixture  # noqa: E402


class WriterContextTests(WriterFixture, unittest.TestCase):

    def test_exact_three_inputs_use_only_candidate_commission_and_previous_chapter(self):
        """OpenSpec scenarios: Writer context inventory and extra chapter context."""
        candidate = self.candidate("exact")
        self.generate(candidate)
        accepted_before = (self.accepted / "production-books/test/chapters/chapter-01.md").read_bytes()
        contexts, calls = [], []
        original_build = WC.build
        outputs = ["```markdown\n# Chapter 1\nFIRST-GENERATED\n" + "word " * 801 + "\n```",
                   "# Chapter 2\nSECOND-GENERATED\n" + "word " * 801]

        def capture_build(inputs):
            contexts.append(dict(inputs))
            return original_build(inputs)

        def chat(*args, **kwargs):
            calls.append((args, kwargs))
            return outputs[len(calls) - 1]

        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.CS, "require_writer_eligible",
                                  wraps=SET.require_writer_eligible) as eligible, \
                mock.patch.object(RUN.judges, "endpoint", return_value=("api", "key")), \
                mock.patch.object(RUN.WC, "build", side_effect=capture_build), \
                mock.patch.object(RUN.ME, "chat", side_effect=chat):
            self.assertTrue(RUN.write_chapters(
                {"writer_model": "writer/model", "writer_reasoning": "none"},
                self.book(candidate), [1, 2], candidate))
        eligible.assert_called_once_with(candidate)
        self.assertEqual(2, len(contexts))
        self.assertTrue(all(tuple(value) == WC.INPUT_KEYS for value in contexts))
        contract = (PAIR.candidate_tree(candidate) /
                    "prompts/chapter-writer.md").read_text(encoding="utf-8")
        self.assertEqual(contract.replace("[N]", "1").replace("[SLUG]", "test") +
                         WC.API_OUTPUT_CONTRACT, contexts[0]["compact_writer_contract"])
        commission_path = self.book(candidate) / "commissions/chapter-01.md"
        self.assertEqual(commission_path.read_text(encoding="utf-8"),
                         contexts[0]["authoritative_commission"])
        self.assertEqual(WC.NO_PREVIOUS_CHAPTER, contexts[0]["previous_chapter"])
        first_saved = (self.book(candidate) /
                       "chapters/chapter-01.md").read_text(encoding="utf-8")
        self.assertEqual(first_saved, contexts[1]["previous_chapter"])
        self.assertNotIn("```", first_saved)
        captured = json.dumps(contexts)
        for forbidden in ("FORBIDDEN-FULL-STYLE", "FORBIDDEN-FULL-PLAN",
                          "FORBIDDEN-RAW-ASSIGNED", "FORBIDDEN-RAW-SECOND",
                          "FORBIDDEN-UNASSIGNED", "FORBIDDEN-JUDGE-FEEDBACK",
                          "FORBIDDEN-REFERENCE-TEXT", "FORBIDDEN-EXTRA-CHAPTER"):
            self.assertNotIn(forbidden, captured)
        for index, (args, kwargs) in enumerate(calls):
            self.assertEqual(("api", "key", "writer/model"), args[:3])
            self.assertEqual(original_build(contexts[index]), args[3])
            self.assertEqual("none", args[4])
            self.assertEqual({"max_tokens": 16000, "temperature": 0.7,
                              "retries": 1}, kwargs)
        self.assertEqual(accepted_before, (self.accepted /
                         "production-books/test/chapters/chapter-01.md").read_bytes())

    def test_ineligible_commission_states_fail_before_any_writer_boundary(self):
        """OpenSpec scenario: A commission cannot ground its assignment."""
        cases = []
        cases.append((self.candidate("missing"), "receipt"))
        blocked = self.candidate("blocked-commission")
        blocked_assignments = deepcopy(self.assignments)
        gap = {"owner": "research/synthesis", "gap": "Assigned support is missing."}
        blocked_assignments["C-02"]["authority"]["blocker"] = gap

        def blocked_runner(request):
            if request["target"] == "C-02":
                return f"COMMISSION BLOCKED\nOwner: {gap['owner']}\nGap: {gap['gap']}"
            return commission(blocked_assignments[request["target"]]["authority"])

        with self.assertRaises(SET.CommissionSetError):
            self.generate(blocked, assignments=blocked_assignments, runner=blocked_runner)
        cases.append((blocked, "receipt"))
        failed_audit = self.candidate("failed-audit")
        with self.assertRaises(SET.CommissionSetError):
            self.generate(failed_audit, "COMMISSION SET BLOCKED\nOwner: plan\nGap: broken")
        cases.append((failed_audit, "no passing"))
        stale = self.candidate("stale")
        self.generate(stale)
        plan = self.book(stale) / "master-plan.md"
        plan.write_text(plan.read_text() + "changed after audit\n")
        cases.append((stale, "stale or hash-mismatched"))
        tampered = self.candidate("tampered")
        self.generate(tampered)
        (self.book(tampered) / "commissions/chapter-01.md").write_text("tampered\n")
        cases.append((tampered, "invalid commission"))
        for candidate, error in cases:
            endpoint, api, manual = mock.Mock(), mock.Mock(), mock.Mock()
            with self.subTest(candidate=candidate.name), \
                    mock.patch.object(SET.SC, "require_subject_contract"), \
                    mock.patch.object(RUN.judges, "endpoint", endpoint), \
                    mock.patch.object(RUN.ME, "chat", api), \
                    mock.patch.object(RUN.MD, "writer", manual):
                with self.assertRaisesRegex(SystemExit, error):
                    RUN.write_chapters({"writer_model": "writer"},
                                       self.book(candidate), [1, 2], candidate)
            endpoint.assert_not_called()
            api.assert_not_called()
            manual.assert_not_called()

    def test_contract_and_manual_route_name_no_legacy_writer_context(self):
        """Infra: the authorized writer has one API/manual context contract."""
        prompt = (ROOT / "prompts/chapter-writer.md").read_text(encoding="utf-8")
        compact = " ".join(prompt.split())
        for required in ("authoritative semantic commission", "Do not resolve plan IDs",
                         "Scare", "ROUTE REFUSAL:",
                         "repair_owner_and_regenerate_downstream",
                         "25–33", "8–10%", "15–17"):
            self.assertIn(required.casefold(), compact.casefold())
        output = io.StringIO()
        authority = {"contract": "CAPTURED-CONTRACT\n",
                     "commissions": {1: "CAPTURED-COMMISSION\n"}}
        with contextlib.redirect_stdout(output):
            MANUAL.writer({"writer_model": "writer"}, ROOT,
                          ROOT / "production-books/test", [1], authority)
        instructions = output.getvalue()
        self.assertIn("CAPTURED-CONTRACT", instructions)
        self.assertIn("CAPTURED-COMMISSION", instructions)
        self.assertIn("never rereading", instructions)
        self.assertIn("manual-chapter-NN.txt", instructions)
        self.assertNotIn("style-guide.md", instructions)
        self.assertNotIn("master-plan.md", instructions)


if __name__ == "__main__":
    unittest.main()
