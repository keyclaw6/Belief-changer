"""Regression tests for the within-book repetition law. Infra coverage."""
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import repetition as R


PHRASE = "alpha bravo charlie delta echo foxtrot golf hotel india juliet kilo lima"


class WithinBookTests(unittest.TestCase):
    def test_detects_a_real_repeated_twelve_word_span(self):
        chapters = [
            ("chapter-1.md", f"beforeone {PHRASE} afterone"),
            ("chapter-2.md", f"beforetwo {PHRASE} aftertwo"),
        ]

        result = R.within_book(chapters, [])

        self.assertTrue(any(span["text"] == PHRASE for span in result["hard_fails"]))

    def test_does_not_stitch_overlapping_shingles_from_unrelated_locations(self):
        words = PHRASE.split()
        snippets = [" ".join(words[i:i + R.N_SOFT]) for i in range(5)]
        parts = []
        for copy in range(2):
            for index, snippet in enumerate(snippets):
                parts.append(f"unique{copy}{index}start {snippet} unique{copy}{index}end")
        chapters = [("chapter-1.md", " ".join(parts))]

        result = R.within_book(chapters, [])

        self.assertEqual([], result["hard_fails"])
        self.assertTrue(result["repeated_ngrams"])

    def test_hard_gate_catches_repeat_hidden_behind_a_more_frequent_short_branch(self):
        prefix = "alpha bravo charlie delta echo foxtrot golf hotel"
        long_repeat = f"{prefix} india juliet kilo lima"
        chapters = [
            (f"short-{index}.md", f"before{index} {prefix} short after{index}")
            for index in range(3)
        ] + [
            ("long-1.md", f"beforelongone {long_repeat} afterlongone"),
            ("long-2.md", f"beforelongtwo {long_repeat} afterlongtwo"),
        ]

        result = R.within_book(chapters, [])

        self.assertTrue(any(span["text"] == long_repeat for span in result["hard_fails"]))

    def test_whitelisted_mantra_is_not_reported(self):
        chapters = [
            ("chapter-1.md", f"beforeone {PHRASE} afterone"),
            ("chapter-2.md", f"beforetwo {PHRASE} aftertwo"),
        ]

        result = R.within_book(chapters, [PHRASE])

        self.assertEqual(0, result["repeated_ngrams"])
        self.assertEqual([], result["hard_fails"])

    def test_normalized_plan_whitelists_licensed_mantra_wording(self):
        plan_text = f"""
| ID | Frozen wording | Job | Debut | Echo chapters | Hand-over form |
|---|---|---|---|---|---|
| M-01 | `{PHRASE}` | Portable thought. | C-01 | C-02 | Recall it. |
"""
        chapters = [
            ("chapter-1.md", f"beforeone {PHRASE} afterone"),
            ("chapter-2.md", f"beforetwo {PHRASE} aftertwo"),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp, "master-plan.md")
            plan.write_text(plan_text, encoding="utf-8")
            whitelist = R._mantra_whitelist(plan)

        result = R.within_book(chapters, whitelist)

        self.assertEqual([PHRASE], whitelist)
        self.assertEqual(1, result["whitelist_size"])
        self.assertEqual(0, result["repeated_ngrams"])
        self.assertEqual([], result["hard_fails"])

    def test_preview_and_summary_are_excluded_only_from_within_book_check(self):
        chapter = (
            "chapter-1.md",
            f"## IN THIS CHAPTER\n\n- {PHRASE}\n\n"
            f"## Body\n\n{PHRASE}\n\n"
            f"## SUMMARY\n\n- {PHRASE}\n",
        )

        within = R.within_book([chapter], [])
        self.assertEqual([], within["hard_fails"])

        recap_only = [("chapter-1.md", f"## SUMMARY\n\n- {PHRASE}\n")]
        with tempfile.TemporaryDirectory() as ref_dir:
            Path(ref_dir, "chapter-1.txt").write_text(PHRASE, encoding="utf-8")
            cross = R.cross_book(recap_only, ref_dir, tripwire=0)
        self.assertTrue(cross["tripped"])
        self.assertGreater(cross["overlap_ngrams"], 0)

    def test_bold_preview_and_summary_labels_are_licensed(self):
        chapter = (
            "chapter-1.md",
            f"**IN THIS CHAPTER**\n\n- {PHRASE}\n\n"
            f"## Body\n\n{PHRASE}\n\n"
            f"**SUMMARY**\n\n- {PHRASE}\n",
        )

        result = R.within_book([chapter], [])

        self.assertEqual([], result["hard_fails"])

    def test_other_bold_or_inline_summary_text_does_not_open_a_recap(self):
        openings = (
            "**AN ORDINARY BOLD PHRASE**",
            "Ordinary body text containing **SUMMARY** inline.",
        )
        for opening in openings:
            with self.subTest(opening=opening):
                chapter = ("chapter-1.md", f"{opening}\n\n{PHRASE}\n\n{PHRASE}\n")

                result = R.within_book([chapter], [])

                self.assertTrue(result["hard_fails"])


if __name__ == "__main__":
    unittest.main()
