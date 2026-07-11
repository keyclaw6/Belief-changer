"""Infra regressions for accepted mantra-sheet representations."""
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mantra_check as M


FIRST = "Freedom belongs to you, exactly as you are."
SECOND = "The old debate has no job left."


class MantraSheetTests(unittest.TestCase):
    def test_normalized_table_parses_wording_debut_and_echoes(self):
        plan = f"""
| ID | Frozen wording | Job and installed belief | Debut | Echo chapters | Hand-over form |
|---|---|---|---|---|---|
| M-01 | `{FIRST}` | Portable promise. | C-01 | C-02, C-04 | Recall it. |
| M-02 | `{SECOND}` | Portable conclusion. | C-03 | C-04 | Recall it. |
"""

        parsed = M.parse_mantra_sheet(plan)

        self.assertEqual(
            [
                {"archetype": "M-01", "wording": FIRST, "debut": 1,
                 "schedule": [2, 4], "schedule_raw": "C-02, C-04"},
                {"archetype": "M-02", "wording": SECOND, "debut": 3,
                 "schedule": [4], "schedule_raw": "C-04"},
            ],
            parsed,
        )
        chapters = [
            ("chapter-01.md", FIRST),
            ("chapter-02.md", FIRST),
            ("chapter-03.md", SECOND),
            ("chapter-04.md", f"{FIRST} {SECOND}"),
        ]
        self.assertEqual([], M.verify(parsed, chapters, [1, 2, 3, 4])["failures"])

    def test_legacy_bullet_format_remains_supported(self):
        plan = (
            f'- **promise — FROZEN WORDING:** "{FIRST}" '
            "| debut: ch. 1 | schedule: ch. 2, ch. 4 | hand-over: direct\n"
        )

        parsed = M.parse_mantra_sheet(plan)

        self.assertEqual(FIRST, parsed[0]["wording"])
        self.assertEqual(1, parsed[0]["debut"])
        self.assertEqual([2, 4], parsed[0]["schedule"])


if __name__ == "__main__":
    unittest.main()
