"""RF-10 replay-verifiable manual writer handoff regressions."""
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
sys.path.insert(0, str(ROOT / "scripts/eval/tests"))
import candidate_pair as PAIR  # noqa: E402
import commission_set as SET  # noqa: E402
import gate as GATE  # noqa: E402
import gate_decision as DECISION  # noqa: E402
import pair_store as STORE  # noqa: E402
import run_iteration as RUN  # noqa: E402
import writer_context as WC  # noqa: E402
from writer_context_fixture import WriterFixture  # noqa: E402


class WriterManualReceiptTests(WriterFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.ledger = Path(self.tmp.name) / "tasks.md"
        self.ledger.write_text(
            "### RF-23 — prose\n\n- Status: `READY`\n", encoding="utf-8")

    def handoff(self, name):
        candidate = self.candidate(name)
        self.generate(candidate)
        with mock.patch.object(SET.SC, "require_subject_contract"):
            authority = WC.capture(candidate, self.book(candidate), [1, 2])
        token = WC.persist_manual_receipt(candidate, authority)
        return candidate, token

    def argv(self, candidate, token):
        out = ["run_iteration.py", "--book", "production-books/test",
               "--chapters", "1-2", "--iter", "1", "--accepted-root",
               str(self.accepted), "--decision-timestamp", "2026-07-14T12:00:00+00:00",
               "--redesign-authorized", "--rf-stage", "RF-23",
               "--candidate-root", str(candidate), "--no-write"]
        return out + (["--writer-authority-receipt", token] if token else [])

    def assert_resume_blocked(self, candidate, token):
        with mock.patch.object(sys, "argv", self.argv(candidate, token)), \
                mock.patch.object(RUN.LG, "LEDGER", self.ledger), \
                mock.patch.object(RUN.CP, "seal") as seal:
            with self.assertRaisesRegex(SystemExit, "manual writer resume|resume rejected"):
                RUN.main()
        seal.assert_not_called()

    def test_clean_chapter_only_resume_really_seals_verifies_and_never_promotes_receipt(self):
        """OpenSpec scenario: A manual agent is dispatched."""
        candidate, token = self.handoff("clean-resume")
        value = json.loads(WC.manual_receipt_path(candidate).read_text(encoding="utf-8"))
        self.assertEqual(token, value["receipt_hash"])
        self.assertEqual("production-books/test", value["book"])
        self.assertEqual([1, 2], value["chapters"])
        self.assertEqual({1, 2}, {item["chapter"] for item in value["commissions"]})
        self.assertEqual(64, len(value["contract"]["sha256"]))
        self.assertEqual(64, len(value["audit"]["sha256"]))
        self.assertEqual(len(PAIR._members(PAIR.load(candidate))),
                         len(value["pair_inventory"]))
        self.assertEqual([
            "production-books/test/chapters/chapter-01.md",
            "production-books/test/chapters/chapter-02.md",
        ], value["selected_draft_paths"])
        for number in (1, 2):
            (self.book(candidate) / f"chapters/chapter-{number:02d}.md").write_text(
                f"# MANUAL CHAPTER {number}\n" + "word " * 801 + "\n", encoding="utf-8")
        with mock.patch.object(sys, "argv", self.argv(candidate, token)), \
                mock.patch.object(RUN.LG, "LEDGER", self.ledger), \
                mock.patch.object(RUN, "run_step", return_value=3):
            with self.assertRaises(SystemExit) as stopped:
                RUN.main()
        self.assertEqual(3, stopped.exception.code)
        tested = PAIR.load(candidate)["tested_hash"]
        PAIR.verify_sealed(candidate, tested)
        row = {key: "" for key in GATE.COLUMNS if key != "timestamp_utc"}
        row.update(iter=1, reward=0.5, hard_ok=True, verdict="KEEP",
                   notes="test", tested_pair_hash=tested)
        _, history = DECISION.ensure(
            candidate, PAIR.load(candidate), {"receipt_hash": "score-fixture"},
            PAIR.evaluation_tree(candidate) / "loop/results.tsv", row,
            GATE.COLUMNS, 0.03, 0.5, "0", "KEEP", True,
            "2026-07-14T12:00:00+00:00")
        PAIR.promote(candidate, self.accepted, tested, history)
        accepted, _, registry = STORE.current(self.accepted)
        self.assertNotIn(WC.MANUAL_RECEIPT, {item["path"] for item in registry["entries"]})
        self.assertFalse((accepted / "pair" / WC.MANUAL_RECEIPT).exists())

    def test_authority_and_handoff_receipt_drift_block_before_seal(self):
        """OpenSpec scenario: A manual agent is dispatched."""
        cases = ("contract", "commission", "audit", "missing", "tampered", "stale-token",
                 "omit-token", "delete-and-omit", "unselected", "config", "product",
                 "manifest-assignment", "undeclared-entry")
        for case in cases:
            with self.subTest(case=case):
                candidate, token = self.handoff(f"blocked-{case}")
                if case == "contract":
                    path = PAIR.candidate_tree(candidate) / "prompts/chapter-writer.md"
                    path.write_text(path.read_text() + "drift\n", encoding="utf-8")
                elif case == "commission":
                    path = self.book(candidate) / "commissions/chapter-02.md"
                    path.write_text(path.read_text() + "drift\n", encoding="utf-8")
                elif case == "audit":
                    path = PAIR.evidence_tree(candidate) / SET.RECEIPT
                    path.write_text(path.read_text() + "drift\n", encoding="utf-8")
                elif case == "missing":
                    WC.manual_receipt_path(candidate).unlink()
                elif case == "tampered":
                    path = WC.manual_receipt_path(candidate)
                    value = json.loads(path.read_text(encoding="utf-8"))
                    value["book"] = "production-books/tampered"
                    STORE.write_json(path, value)
                else:
                    if case == "stale-token":
                        token = "0" * 64
                    elif case == "omit-token":
                        token = None
                    elif case == "delete-and-omit":
                        WC.manual_receipt_path(candidate).unlink()
                        token = None
                    elif case == "unselected":
                        path = self.book(candidate) / "chapters/chapter-03.md"
                        path.write_text(path.read_text() + "drift\n", encoding="utf-8")
                    elif case == "config":
                        path = PAIR.candidate_tree(candidate) / "loop/config.yaml"
                        path.write_text(path.read_text() + "drift: true\n", encoding="utf-8")
                    elif case == "product":
                        path = self.book(candidate) / "00-brief.md"
                        path.write_text(path.read_text() + "drift\n", encoding="utf-8")
                    elif case == "manifest-assignment":
                        path = candidate / PAIR.MANIFEST
                        value = json.loads(path.read_text(encoding="utf-8"))
                        value["outputs"].reverse()
                        STORE.write_json(path, value)
                    else:
                        path = self.book(candidate) / "undeclared.md"
                        path.write_text("undeclared\n", encoding="utf-8")
                self.assert_resume_blocked(candidate, token)

    def test_undeclared_receipt_cannot_reach_real_seal(self):
        candidate = self.candidate("undeclared-receipt")
        self.generate(candidate)
        STORE.write_json(WC.manual_receipt_path(candidate), {"receipt_hash": "0" * 64})
        with self.assertRaisesRegex(PAIR.PairError, "undeclared"):
            PAIR.seal(candidate)

    def test_pair_metadata_downgrade_cannot_hide_existing_handoff(self):
        candidate, _ = self.handoff("metadata-downgrade")
        path = candidate / PAIR.MANIFEST
        value = json.loads(path.read_text(encoding="utf-8"))
        value.update(state="CANDIDATE", operation=None)
        STORE.write_json(path, value)
        self.assert_resume_blocked(candidate, None)


if __name__ == "__main__":
    unittest.main()
