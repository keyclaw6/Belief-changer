"""Iteration-evidence and promotion-gate regression tests. Offline, stdlib only."""
from __future__ import annotations
import json
import subprocess
import sys
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SOURCE / "scripts"))
from bc_autoresearch.experiments import wilson_lower


class PromotionGateTest(unittest.TestCase):
    def test_small_samples_cannot_promote(self):
        # loop/PROGRAM.md: three samples are screening, never sufficient.
        self.assertLess(wilson_lower(3, 3), 0.5)
        self.assertLess(wilson_lower(2, 2), 0.5)
        self.assertLess(wilson_lower(0, 3), 0.5)

    def test_sufficient_allocation_can_pass(self):
        # A large confirmatory allocation is the specified way out (051).
        self.assertGreater(wilson_lower(9, 9), 0.5)


class IterationEvidenceTest(unittest.TestCase):
    def test_evidence_files_are_machine_readable(self):
        found = sorted((SOURCE / "loop" / "iterations").glob("*/evidence.json"))
        self.assertTrue(found, "no iteration evidence bundle present")
        for path in found:
            with self.subTest(iter=path.parent.name):
                data = json.loads(path.read_text())
                for key in ("probe", "verdict", "head", "files"):
                    self.assertIn(key, data)
                self.assertIn(data["verdict"], ("SUPPORT", "REFUTE"))

    def test_repo_gate_accepts_tree(self):
        proc = subprocess.run([sys.executable, str(SOURCE / "scripts" / "validate_repo.py"),
                               str(SOURCE)], capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stderr)


if __name__ == "__main__":
    unittest.main()
