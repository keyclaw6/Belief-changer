"""Infra regressions for the objective-gate scope (PROGRAM §4 hard checks)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EVAL_DIR))
import evallib as E
import metrics as M


class EvalScopeTest(unittest.TestCase):
    def test_explicit_ranges_reject_empty_malformed_and_unavailable(self):
        for spec in ("", " ", ",", "1,,2", "3-1", "nope", "0", "1-3"):
            with self.subTest(spec=spec), self.assertRaises(SystemExit):
                E.parse_range(spec, 2)
        self.assertEqual([1, 2], E.parse_range("1-2", 2))
        self.assertEqual([1, 2], E.parse_range(None, 2))

    def test_run_evals_rejects_partially_available_stage_a_range(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book, ref, run = self._fixture(root, chapter_count=2)
            result = self._run_evals(book, ref, run, "1-3")
            self.assertNotEqual(0, result.returncode)
            self.assertIn("requested chapter(s) unavailable", result.stderr)

    def test_run_evals_scopes_repetition_and_originality(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book, ref, run = self._fixture(root, chapter_count=3)
            copied = "one two three four five six seven eight nine ten eleven twelve thirteen"
            (book / "chapters/chapter-03.md").write_text(
                f"{copied}.\n\n{copied}.\n", encoding="utf-8"
            )
            (ref / "003-reference.txt").write_text(copied, encoding="utf-8")
            self._write_ref_metrics(ref)

            scoped = self._run_evals(book, ref, run, "1-2")
            self.assertEqual(0, scoped.returncode, scoped.stdout + scoped.stderr)
            payload = json.loads((run / "metrics.json").read_text(encoding="utf-8"))
            self.assertEqual([1, 2], payload["chapters_checked"])
            self.assertEqual([], payload["repetition_within"]["hard_fails"])
            self.assertEqual(0, payload["originality_cross"]["overlap_ngrams"])

            full = self._run_evals(book, ref, root / "full-run")
            self.assertEqual(2, full.returncode)
            full_payload = json.loads(
                (root / "full-run/metrics.json").read_text(encoding="utf-8")
            )
            self.assertTrue(full_payload["repetition_within"]["hard_fails"])
            self.assertTrue(full_payload["originality_cross"]["tripped"])

    def test_missing_or_unparseable_mantra_sheet_is_hard_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book, ref, run = self._fixture(root)
            plan = book / "master-plan.md"
            plan.unlink()
            missing = self._run_evals(book, ref, run, "1-2")
            self.assertEqual(2, missing.returncode)
            payload = json.loads((run / "metrics.json").read_text(encoding="utf-8"))
            self.assertIn("mantra: no master-plan.md", payload["hard_fails"])

            plan.write_text("# Plan\n\nNo mantra sheet here.\n", encoding="utf-8")
            unparseable = self._run_evals(book, ref, root / "unparseable", "1-2")
            self.assertEqual(2, unparseable.returncode)
            payload = json.loads(
                (root / "unparseable/metrics.json").read_text(encoding="utf-8")
            )
            self.assertIn(
                "mantra: mantra sheet not parseable/unfilled", payload["hard_fails"]
            )

            standalone = subprocess.run(
                [sys.executable, str(EVAL_DIR / "mantra_check.py"),
                 "--plan", str(plan), "--book", str(book / "chapters"),
                 "--chapters", "1-2"],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(2, standalone.returncode)
            self.assertIn("FAIL: no filled mantra-sheet", standalone.stdout)

            missing_plan = subprocess.run(
                [sys.executable, str(EVAL_DIR / "mantra_check.py"),
                 "--plan", str(root / "missing-plan.md"),
                 "--book", str(book / "chapters")],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(2, missing_plan.returncode)
            self.assertIn("FAIL: plan not found", missing_plan.stdout)

    def _fixture(self, root, chapter_count=2):
        book, ref, run = root / "book", root / "reference", root / "run"
        (book / "chapters").mkdir(parents=True)
        ref.mkdir()
        plan = (
            '- **promise — FROZEN WORDING:** "Freedom is already yours." '
            '| debut: ch. 1 | schedule: every chapter | hand-over: direct\n'
        )
        (book / "master-plan.md").write_text(plan, encoding="utf-8")
        for chapter in range(1, chapter_count + 1):
            text = (
                "Freedom is already yours. "
                f"Generated chapter {chapter} carries distinct words token{chapter}.\n"
            )
            (book / f"chapters/chapter-{chapter:02d}.md").write_text(
                text, encoding="utf-8"
            )
            (ref / f"{chapter:03d}-reference.txt").write_text(
                f"Reference passage {chapter} uses wholly separate language.\n",
                encoding="utf-8",
            )
        self._write_ref_metrics(ref)
        return book, ref, run

    @staticmethod
    def _write_ref_metrics(ref):
        chapters = E.load_chapters(ref, exts=(".txt", ".md"))
        (ref / "reference-metrics.json").write_text(
            json.dumps(M.book_metrics(chapters)), encoding="utf-8"
        )

    @staticmethod
    def _run_evals(book, ref, run, chapters=None):
        command = [
            sys.executable, str(EVAL_DIR / "run_evals.py"),
            "--book", str(book), "--ref-dir", str(ref), "--run-dir", str(run),
        ]
        if chapters is not None:
            command.extend(("--chapters", chapters))
        return subprocess.run(command, capture_output=True, text=True, check=False)


if __name__ == "__main__":
    unittest.main()
