"""Independent QA regressions for the RF-00 legacy-loop guard."""
import contextlib
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/eval"))
sys.path.insert(0, str(ROOT / "scripts/loop"))
import judges  # noqa: E402
import gate as GATE  # noqa: E402
import legacy_guard as LG  # noqa: E402
import run_iteration as RUN  # noqa: E402
import score as SCORE  # noqa: E402


class GuardQATests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.candidate = self.root / "candidate"
        self.book = self.candidate / "book"
        (self.book / "chapters").mkdir(parents=True)
        (self.book / "master-plan.md").write_text("### CH-01 — Test\n", encoding="utf-8")
        self.ledger = self.root / "tasks.md"
        self.ledger.write_text("### RF-23 — prose\n\n- Status: `READY`\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def sentinel(self, name):
        path = self.root / name
        path.write_text("outside sentinel\n", encoding="utf-8")
        return path

    def writer_patches(self):
        inputs = dict(zip(RUN.WC.INPUT_KEYS, ("contract", "commission", "previous")))
        authority = {"manifest": {"run": {"book": "book", "chapters": [1]}},
                     "contract": "contract", "commissions": {1: "commission"}}
        return (
            mock.patch.object(RUN.BR, "_capture", return_value=(authority, None)),
            mock.patch.object(RUN.WC, "require_fresh"),
            mock.patch.object(RUN.WC, "inputs", return_value=inputs),
            mock.patch.object(RUN.WC, "build", return_value="prompt"),
            mock.patch.object(RUN.WC, "persist_manual_receipt"),
            mock.patch.object(RUN.FB, "begin", return_value={
                "state": "DRAFTING", "mode": "api", "drafts": [], "selection": [1]}),
            mock.patch.object(RUN.FB, "prepare", return_value=[1]),
            mock.patch.object(
                RUN.FB, "durable_call",
                return_value="# Chapter\n" + "word " * 801),
            mock.patch.object(
                RUN.FB, "accept_response",
                side_effect=lambda _root, number, interrupt=None: (
                    self.book / f"chapters/chapter-{number:02d}.md").write_text(
                        "# Chapter\n" + "word " * 801, encoding="utf-8") and 801),
        )

    def run_writer(self, patches):
        with contextlib.ExitStack() as stack:
            for patch in patches:
                stack.enter_context(patch)
            return RUN.write_chapters(
                {"writer_model": "writer"}, self.book, [1], self.candidate)

    def test_chapter_leaf_symlink_cannot_escape_candidate(self):
        """OpenSpec scenario: An authorized isolated redesign path is exercised."""
        outside = self.sentinel("outside-chapter.md")
        leaf = self.book / "chapters/chapter-01.md"
        leaf.symlink_to(outside)
        patches = (
            mock.patch.object(RUN.judges, "endpoint", return_value=("url", "key")),
            mock.patch.object(RUN.ME, "chat", return_value="# Chapter\n" + "word " * 801),
            *self.writer_patches(),
        )
        with self.assertRaises(SystemExit) as stopped:
            self.run_writer(patches)
        self.assertIn("target contains a symlink", str(stopped.exception))
        self.assertEqual("outside sentinel\n", outside.read_text(encoding="utf-8"))
        leaf.unlink()
        self.assertTrue(self.run_writer(patches))
        self.assertTrue(leaf.read_text(encoding="utf-8").startswith("# Chapter"))
    def test_chapter_leaf_hardlink_cannot_escape_candidate(self):
        """OpenSpec scenario: An authorized isolated redesign path is exercised."""
        outside = self.sentinel("outside-hardlinked-chapter.md")
        leaf = self.book / "chapters/chapter-01.md"
        leaf.hardlink_to(outside)
        patches = (
            mock.patch.object(RUN.judges, "endpoint", return_value=("url", "key")),
            mock.patch.object(RUN.ME, "chat", return_value="# Chapter\n" + "word " * 801),
            *self.writer_patches(),
        )
        with self.assertRaises(SystemExit) as stopped:
            self.run_writer(patches)
        self.assertIn("multiply linked file", str(stopped.exception))
        self.assertEqual("outside sentinel\n", outside.read_text(encoding="utf-8"))
        leaf.unlink()
        self.assertTrue(self.run_writer(patches))
        self.assertTrue(leaf.read_text(encoding="utf-8").startswith("# Chapter"))

    def test_judge_task_leaf_symlink_cannot_escape_candidate(self):
        """OpenSpec scenario: An authorized isolated redesign path is exercised."""
        outside = self.sentinel("outside-task.md")
        cfg = {"tasks_dir": str(self.candidate / "tasks"), "judge_k": 1,
               "judge_model": "judge", "judge_reasoning": "xhigh"}
        leaf = self.candidate / "tasks/iter-001/judging/tasks/ch1-j1.md"
        leaf.parent.mkdir(parents=True)
        leaf.symlink_to(outside)
        args = (cfg, [("ch1", "ours", "reference", "context")], "001",
                "{{REFERENCE}}{{CANDIDATE}}{{CONTEXT}}", self.candidate)
        with mock.patch.object(judges.FB, "require_frozen_batch"), \
                mock.patch.object(judges.GR, "require_complete"), \
                self.assertRaises(SystemExit) as stopped:
            judges.emit_tasks(*args)
        self.assertIn("target contains a symlink", str(stopped.exception))
        self.assertEqual("outside sentinel\n", outside.read_text(encoding="utf-8"))
        leaf.unlink()
        with mock.patch.object(judges.FB, "require_frozen_batch"), \
                mock.patch.object(judges.GR, "require_complete"):
            self.assertEqual([leaf], judges.emit_tasks(*args))
        self.assertTrue(leaf.read_text(encoding="utf-8"))
    def test_judge_task_leaf_hardlink_cannot_escape_candidate(self):
        """OpenSpec scenario: An authorized isolated redesign path is exercised."""
        outside = self.sentinel("outside-hardlinked-task.md")
        cfg = {"tasks_dir": str(self.candidate / "tasks"), "judge_k": 1,
               "judge_model": "judge", "judge_reasoning": "xhigh"}
        leaf = self.candidate / "tasks/iter-001/judging/tasks/ch1-j1.md"
        leaf.parent.mkdir(parents=True)
        leaf.hardlink_to(outside)
        args = (cfg, [("ch1", "ours", "reference", "context")], "001",
                "{{REFERENCE}}{{CANDIDATE}}{{CONTEXT}}", self.candidate)
        with mock.patch.object(judges.FB, "require_frozen_batch"), \
                mock.patch.object(judges.GR, "require_complete"), \
                self.assertRaises(SystemExit) as stopped:
            judges.emit_tasks(*args)
        self.assertIn("multiply linked file", str(stopped.exception))
        self.assertEqual("outside sentinel\n", outside.read_text(encoding="utf-8"))
        leaf.unlink()
        with mock.patch.object(judges.FB, "require_frozen_batch"), \
                mock.patch.object(judges.GR, "require_complete"):
            self.assertEqual([leaf], judges.emit_tasks(*args))
        self.assertTrue(leaf.read_text(encoding="utf-8"))
    def _run_score(self, argv):
        with mock.patch.object(sys, "argv", argv), \
                mock.patch.object(LG, "LEDGER", self.ledger), \
                mock.patch.object(SCORE.score_core, "evaluate", return_value={
                    "chapters_checked": [1], "hard_ok": True, "hard_fails": [],
                    "checks": {}, "diagnostics": {"stylometrics": []},
                    "pairs": [("ch1", "ours", "reference", "context")]}), \
                mock.patch.object(SCORE.judges, "missing_verdicts", return_value=[]), \
                mock.patch.object(SCORE.judges, "aggregate", return_value={
                    "reward": 1, "worst_dimensions": [], "suggestions": []}), \
                mock.patch.object(SCORE.FB, "require_frozen_batch"), \
                mock.patch.object(SCORE.GR, "require_complete"), \
                mock.patch.object(SCORE, "_report"):
            SCORE.main()

    def test_score_leaf_symlink_cannot_escape_candidate(self):
        """OpenSpec scenario: An authorized isolated redesign path is exercised."""
        scores = self.candidate / "scores"
        scores.mkdir()
        outside = self.sentinel("outside-score.json")
        leaf = scores / "iter-001.json"
        leaf.symlink_to(outside)
        rubric = self.candidate / "rubric.md"
        rubric.write_text("{{REFERENCE}}{{CANDIDATE}}{{CONTEXT}}", encoding="utf-8")
        config = self.candidate / "config.yaml"
        config.write_text(
            f"scores_dir: {scores}\ntasks_dir: {self.candidate / 'tasks'}\n"
            f"judge_rubric: {rubric}\nlength_band: 0.4\n"
            "reference_chapter_offset: 0\noriginality_tripwire: 0.1\n",
            encoding="utf-8",
        )
        argv = ["score.py", "--book", str(self.book), "--chapters", "1", "--iter", "1",
                "--config", str(config), "--redesign-authorized", "--rf-stage", "RF-23",
                "--candidate-root", str(self.candidate)]
        with self.assertRaises(SystemExit) as stopped:
            self._run_score(argv)
        self.assertIn("target contains a symlink", str(stopped.exception))
        self.assertEqual("outside sentinel\n", outside.read_text(encoding="utf-8"))
        leaf.unlink()
        with self.assertRaises(SystemExit) as complete:
            self._run_score(argv)
        self.assertEqual(0, complete.exception.code)
        self.assertTrue(leaf.read_text(encoding="utf-8").startswith("{"))

    def test_score_leaf_hardlink_cannot_escape_candidate(self):
        """OpenSpec scenario: An authorized isolated redesign path is exercised."""
        scores = self.candidate / "scores"
        scores.mkdir()
        outside = self.sentinel("outside-hardlinked-score.json")
        leaf = scores / "iter-001.json"
        leaf.hardlink_to(outside)
        rubric = self.candidate / "rubric.md"
        rubric.write_text("{{REFERENCE}}{{CANDIDATE}}{{CONTEXT}}", encoding="utf-8")
        config = self.candidate / "config.yaml"
        config.write_text(
            f"scores_dir: {scores}\ntasks_dir: {self.candidate / 'tasks'}\n"
            f"judge_rubric: {rubric}\nlength_band: 0.4\n"
            "reference_chapter_offset: 0\noriginality_tripwire: 0.1\n",
            encoding="utf-8",
        )
        argv = ["score.py", "--book", str(self.book), "--chapters", "1", "--iter", "1",
                "--config", str(config), "--redesign-authorized", "--rf-stage", "RF-23",
                "--candidate-root", str(self.candidate)]
        with self.assertRaises(SystemExit) as stopped:
            self._run_score(argv)
        self.assertIn("multiply linked file", str(stopped.exception))
        self.assertEqual("outside sentinel\n", outside.read_text(encoding="utf-8"))
        leaf.unlink()
        with self.assertRaises(SystemExit) as complete:
            self._run_score(argv)
        self.assertEqual(0, complete.exception.code)
        self.assertTrue(leaf.read_text(encoding="utf-8").startswith("{"))

    def test_gate_ledger_leaf_hardlink_cannot_escape_candidate(self):
        """OpenSpec scenario: An authorized isolated redesign path is exercised."""
        outside = self.sentinel("outside-hardlinked-results.tsv")
        leaf = self.candidate / "results.tsv"
        leaf.hardlink_to(outside)
        row = {"iter": "1", "verdict": "KEEP"}
        with self.assertRaises(SystemExit) as stopped:
            GATE.append_row(leaf, row, self.candidate)
        self.assertIn("multiply linked file", str(stopped.exception))
        self.assertEqual("outside sentinel\n", outside.read_text(encoding="utf-8"))
        leaf.unlink()
        GATE.append_row(leaf, row, self.candidate)
        text = leaf.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("iter\ttimestamp_utc"))
        self.assertIn("KEEP", text)

    def test_ledger_requires_unique_tasks_and_valid_statuses(self):
        """OpenSpec scenario: An authorized isolated redesign path is exercised."""
        args = SimpleNamespace(redesign_authorized=True, rf_stage="RF-23",
                               candidate_root=str(self.candidate))
        valid = "### RF-23 — prose\n\n- Status: `READY`\n"
        cases = {
            "duplicate": valid + "\n### RF-23 — again\n\n- Status: `READY`\n",
            "missing RF-23": "### RF-20 — calibration\n\n- Status: `READY`\n",
            "missing status": "### RF-23 — prose\n\nno status\n",
            "multiple statuses": valid + "- Status: `DONE`\n",
            "unknown status": "### RF-23 — prose\n\n- Status: `FROZEN`\n",
            "malformed boundary": "### RF-23\n\n- Status: `READY`\n",
        }
        for label, text in cases.items():
            self.ledger.write_text(text, encoding="utf-8")
            with self.subTest(label=label), mock.patch.object(LG, "LEDGER", self.ledger):
                with self.assertRaises(SystemExit):
                    LG.require_authorized(args, entrypoint="qa")
        self.ledger.write_text(valid, encoding="utf-8")
        with mock.patch.object(LG, "LEDGER", self.ledger):
            self.assertEqual(self.candidate, LG.require_authorized(args, entrypoint="qa"))


if __name__ == "__main__":
    unittest.main()
