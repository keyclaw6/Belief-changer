"""RF-10 post-eligibility tampering and tokenless-commission regressions."""
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
import run_iteration as RUN  # noqa: E402
from test_commission_contract import commission  # noqa: E402
from writer_context_fixture import WriterFixture  # noqa: E402


class WriterFreshnessTests(WriterFixture, unittest.TestCase):
    def test_endpoint_mutation_blocks_api_and_manual_dispatch(self):
        """Infra: eligibility capture cannot be invalidated during endpoint lookup."""
        candidate = self.candidate("endpoint-mutation")
        self.generate(candidate)
        contract = PAIR.candidate_tree(candidate) / "prompts/chapter-writer.md"

        def endpoint():
            contract.write_text("TAMPERED-ENDPOINT-CONTRACT\n", encoding="utf-8")
            return "api", "key"

        api, manual = mock.Mock(), mock.Mock()
        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", side_effect=endpoint), \
                mock.patch.object(RUN.ME, "chat", api), \
                mock.patch.object(RUN.MD, "writer", manual):
            with self.assertRaisesRegex(SystemExit, "after endpoint resolution"):
                RUN.write_chapters({"writer_model": "writer"},
                                   self.book(candidate), [1, 2], candidate)
        api.assert_not_called()
        manual.assert_not_called()

    def test_first_writer_mutation_blocks_second_dispatch_and_uses_clean_capture(self):
        """Infra: each API dispatch rechecks authority captured at eligibility."""
        candidate = self.candidate("first-writer-mutation")
        self.generate(candidate)
        chapter = self.book(candidate) / "chapters/chapter-01.md"
        before = chapter.read_bytes()
        commission_path = self.book(candidate) / "commissions/chapter-02.md"
        prompts = []

        def chat(*args, **kwargs):
            prompts.append(args[3])
            commission_path.write_text("TAMPERED-FIRST-WRITER\n", encoding="utf-8")
            return "# Chapter 1\n" + "word " * 801

        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", return_value=("api", "key")), \
                mock.patch.object(RUN.ME, "chat", side_effect=chat) as api:
            with self.assertRaisesRegex(SystemExit, "writer output failed closed"):
                RUN.write_chapters({"writer_model": "writer"},
                                   self.book(candidate), [1, 2], candidate)
        api.assert_called_once()
        self.assertNotIn("TAMPERED-FIRST-WRITER", prompts[0])
        self.assertEqual(before, chapter.read_bytes())

    def test_final_callback_audit_mutation_writes_no_affected_chapter_or_seal(self):
        """OpenSpec scenario: A later chapter follows an earlier chapter in one audited batch."""
        candidate = self.candidate("final-callback")
        self.generate(candidate)
        chapter = self.book(candidate) / "chapters/chapter-02.md"
        before = chapter.read_bytes()
        audit = PAIR.evidence_tree(candidate) / SET.RECEIPT
        ledger = Path(self.tmp.name) / "tasks.md"
        ledger.write_text("### RF-23 — prose\n\n- Status: `READY`\n", encoding="utf-8")
        argv = ["run_iteration.py", "--book", "production-books/test",
                "--chapters", "1-2", "--iter", "1", "--accepted-root",
                str(self.accepted), "--decision-timestamp", "2026-07-14T12:00:00+00:00",
                "--redesign-authorized", "--rf-stage", "RF-23",
                "--candidate-root", str(candidate), "--score-now"]
        calls = []

        def chat(*args, **kwargs):
            calls.append(args[3])
            if len(calls) == 2:
                audit.write_text(audit.read_text() + "tampered\n", encoding="utf-8")
            return f"# Chapter {len(calls)}\n" + "word " * 801

        with mock.patch.object(sys, "argv", argv), \
                mock.patch.object(RUN.LG, "LEDGER", ledger), \
                mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", return_value=("api", "key")), \
                mock.patch.object(RUN.ME, "chat", side_effect=chat), \
                mock.patch.object(RUN.CP, "seal") as seal:
            with self.assertRaisesRegex(SystemExit, "writer output failed closed"):
                RUN.main()
        self.assertEqual(2, len(calls))
        self.assertEqual(before, chapter.read_bytes())
        seal.assert_not_called()

    def test_manual_dispatch_receives_captured_bytes_despite_callback_mutation(self):
        """Infra: manual instructions carry captured authority instead of mutable paths."""
        candidate = self.candidate("manual-mutation")
        self.generate(candidate)
        contract_path = PAIR.candidate_tree(candidate) / "prompts/chapter-writer.md"
        seen = []

        def manual(cfg, operation, book, selected, authority):
            seen.append(deepcopy(authority))
            contract_path.write_text("TAMPERED-MANUAL-CALLBACK\n", encoding="utf-8")

        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", return_value=("api", "")), \
                mock.patch.object(RUN.MD, "writer", side_effect=manual) as dispatched, \
                mock.patch.object(RUN.ME, "chat") as api:
            self.assertFalse(RUN.write_chapters(
                {"writer_model": "writer"}, self.book(candidate), [1, 2], candidate))
        dispatched.assert_called_once()
        api.assert_not_called()
        self.assertEqual("COMPACT-CONTRACT chapter=[N] slug=[SLUG]\n",
                         seen[0]["contract"])
        self.assertEqual({1, 2}, set(seen[0]["commissions"]))
        self.assertNotIn("TAMPERED-MANUAL-CALLBACK", repr(seen[0]))

    def test_valid_tokenless_commission_routes_to_commission_owner(self):
        """OpenSpec requirement: one commission-assigned mantra per chapter."""
        candidate = self.candidate("tokenless")
        (PAIR.candidate_tree(candidate) / "prompts/chapter-writer.md").write_text(
            (ROOT / "prompts/chapter-writer.md").read_text(encoding="utf-8"), encoding="utf-8")
        tokenless = deepcopy(self.assignments)
        for assignment in tokenless.values():
            assignment["authority"]["frozen_tokens"] = ()

        def runner(request):
            authority = self.assignments[request["target"]]["authority"]
            token = authority["frozen_tokens"][0]
            return commission(authority).replace(
                f" Preserve the frozen words `{token}`.", "")

        self.generate(candidate, assignments=tokenless, runner=runner)
        chapter = self.book(candidate) / "chapters/chapter-01.md"
        before, prompts = chapter.read_bytes(), []

        def chat(*args, **kwargs):
            prompts.append(args[3])
            return ('ROUTE REFUSAL: {"action_code":'
                    '"repair_owner_and_regenerate_downstream","finding":'
                    '"No commission-assigned mantra or frozen token.",'
                    '"owner":"commission/context"}')

        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", return_value=("api", "key")), \
                mock.patch.object(RUN.ME, "chat", side_effect=chat):
            with self.assertRaisesRegex(SystemExit,
                                        "writer routed refusal to commission/context"):
                RUN.write_chapters({"writer_model": "writer"},
                                   self.book(candidate), [1, 2], candidate)
        self.assertIn("Every chapter debuts or reinforces at least one", prompts[0])
        self.assertIn("ROUTE REFUSAL:", prompts[0])
        route = PAIR.load(candidate)["draft_batch"]["refusal"]
        self.assertEqual(1, route["chapter"])
        self.assertEqual(before, chapter.read_bytes())


if __name__ == "__main__":
    unittest.main()
