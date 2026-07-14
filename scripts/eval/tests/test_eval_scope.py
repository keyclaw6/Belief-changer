"""Infra regressions for the one accepted deterministic scoring core."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVAL_DIR = ROOT / "scripts/eval"
sys.path[:0] = [str(EVAL_DIR), str(ROOT / "scripts/loop")]
import evallib as E  # noqa: E402
import metrics as M  # noqa: E402
import score_core as SCORE  # noqa: E402


class EvalScopeTest(unittest.TestCase):
    def test_explicit_ranges_reject_empty_malformed_and_unavailable(self):
        for spec in ("", " ", ",", "1,,2", "3-1", "nope", "0", "1-3"):
            with self.subTest(spec=spec), self.assertRaises(SystemExit):
                E.parse_range(spec, 2)
        self.assertEqual([1, 2], E.parse_range("1-2", 2))
        self.assertEqual([1, 2], E.parse_range(None, 2))

    def test_core_scopes_repetition_and_originality(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book, ref, cfg = self._fixture(root, chapter_count=3)
            copied = "one two three four five six seven eight nine ten eleven twelve thirteen"
            (book / "chapters/chapter-03.md").write_text(
                f"{copied}.\n\n{copied}.\n", encoding="utf-8")
            (ref / "003-reference.txt").write_text(copied, encoding="utf-8")
            self._write_ref_metrics(ref)

            scoped = SCORE.evaluate(cfg, book, "1-2")
            self.assertEqual([1, 2], scoped["chapters_checked"])
            self.assertEqual([], scoped["checks"]["repetition_within"]["hard_fails"])
            self.assertEqual(0, scoped["checks"]["originality"]["overlap_ngrams"])

            full = SCORE.evaluate(cfg, book, None)
            self.assertTrue(full["checks"]["repetition_within"]["hard_fails"])
            self.assertTrue(full["checks"]["originality"]["tripped"])

    def test_core_fails_closed_on_unavailable_chapter_or_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book, _, cfg = self._fixture(root)
            with self.assertRaises(SystemExit):
                SCORE.evaluate(cfg, book, "1-3")
            (book / "master-plan.md").unlink()
            with self.assertRaises(FileNotFoundError):
                SCORE.evaluate(cfg, book, "1-2")

    def _fixture(self, root, chapter_count=2):
        book, ref = root / "book", root / "reference"
        (book / "chapters").mkdir(parents=True)
        ref.mkdir()
        plan = (
            '- **promise — FROZEN WORDING:** "Freedom is already yours." '
            '| debut: ch. 1 | schedule: every chapter | hand-over: direct\n'
        )
        (book / "master-plan.md").write_text(plan, encoding="utf-8")
        for chapter in range(1, chapter_count + 1):
            text = ("Freedom is already yours. "
                    f"Generated chapter {chapter} carries distinct words token{chapter}.\n")
            (book / f"chapters/chapter-{chapter:02d}.md").write_text(
                text, encoding="utf-8")
            (ref / f"{chapter:03d}-reference.txt").write_text(
                f"Reference passage {chapter} uses wholly separate language.\n",
                encoding="utf-8")
        self._write_ref_metrics(ref)
        return book, ref, {
            "reference_dir": str(ref), "reference_chapter_offset": 0,
            "originality_tripwire": 0.1, "near_copy_tripwire": 0.5,
            "length_band": 0.4,
        }

    @staticmethod
    def _write_ref_metrics(ref):
        chapters = E.load_chapters(ref, exts=(".txt", ".md"))
        (ref / "reference-metrics.json").write_text(
            json.dumps(M.book_metrics(chapters)), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
