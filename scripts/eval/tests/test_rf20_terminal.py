"""Focused RF-20 terminal-state truth test."""
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class RF20TerminalTests(unittest.TestCase):
    def test_failed_calibration_lineage_remains_terminal_and_product_blocking(self):
        """OpenSpec scenario: A failed calibration lineage remains terminal."""
        ledger = (ROOT / "calibration/runs/LEDGER.md").read_text()
        rows = [line for line in ledger.splitlines()
                if line.startswith("| rf20-attempt-5 |")]
        self.assertEqual(1, len(rows))
        self.assertIn("newly founder/root-approved hypothesis and control lineage required",
                      rows[0])

        program = (ROOT / "PROGRAM.md").read_text()
        self.assertIn("RF-20 is `BLOCKED` by a terminal failed lineage", program)
        self.assertIn("`rf20-attempt-5` row", program)

        tasks = (ROOT / "openspec/changes/redesign-book-factory/tasks.md").read_text()
        rf20 = tasks.split("### RF-20", 1)[1].split("### RF-21", 1)[0]
        rf21 = tasks.split("### RF-21", 1)[1].split("### RF-22", 1)[0]
        self.assertIn("- Status: `BLOCKED`", rf20)
        self.assertIn("- Acceptance: unmet.", rf20)
        self.assertIn("`rf20-attempt-5` row", rf20)
        self.assertIn("- Status: `BLOCKED`", rf21)


if __name__ == "__main__": unittest.main()
