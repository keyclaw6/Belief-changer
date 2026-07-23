"""Immutable verdict and byte-hash checks for historical judge controls."""
import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[3]
CASES = (
    ("controls/identical", "0d408215378f40dd9f0bc95e1a2e78dd76423f4b8ace5cfdeea4745f544f4c94", False),
    ("controls-v2.1/identical", "7623699f69fe00130e2266f93815262961044bfbc6ac1d60ece092cc73c194f1", True),
    ("controls-v2.1/degraded-reference", "ebfa0e571b5968f3ef30ff453297b964b552cf864719928e8fef35ec515bab8e", False),
    ("controls-v2.2/identical", "f9077e5fb8b26f3125c484bb64c5426f011ecc4f1d68a48f6601dece2c269348", True),
    ("controls-v2.2/degraded-reference", "ca77838c3907a356f13cbcb7304a2dd5852dc2b7bde5233e555c7d2c0dc02d9f", False),
)


class HistoricalControlRecordTests(unittest.TestCase):
    def test_recorded_summaries_keep_exact_bytes_and_verdicts(self):
        """Infra: prospective protocols cannot rewrite historical control evidence."""
        base = ROOT / "calibration/runs/run-012/judgments"
        for relative, expected_hash, expected_passed in CASES:
            with self.subTest(summary=relative):
                payload = (base / relative / "judge-summary.json").read_text(
                    encoding="utf-8").encode("utf-8")
                self.assertEqual(hashlib.sha256(payload).hexdigest(), expected_hash)
                self.assertIs(json.loads(payload)["prompt_control"]["passed"], expected_passed)


if __name__ == "__main__":
    unittest.main()
