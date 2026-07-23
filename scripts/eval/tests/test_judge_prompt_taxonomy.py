"""Infra checks for the frozen Stage-A v2.2 critical-failure taxonomy."""
import hashlib
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
import judge_protocol as V2


ROOT = Path(__file__).parents[3]
JUDGES = ROOT / "calibration/judges"
V21_HASHES = {
    "efficacy": "6d29f64553940b52e54df5acebdb4555b80b4a7d97cc55ea676901d1b086fae4",
    "craft": "925f236ce8136f9fd0323660ac031067e394b2103d34503f60b133c8a22e7fa5",
    "integrity": "1da78e468c4dcb769329f112912d84c267a2cbaac28a1c58ef4ce7137d16ad23",
}
V22_HASHES = {
    "efficacy": "11fdedde0018ebcf7b2d37ddf08a6080d64c0931eec02cffcb630cde2fa28f4c",
    "craft": "916cf4c6c2e5748f54b91979c0edd1123e1a29ce2791437c301f9e7459394948",
    "integrity": "195820f1e4140918333449bc3fda374d42f356637619bbd92f028945e2107b0a",
}
SHARED_RULE = (
    "Critical failures are publication-blocking conditions, not a second inventory\n"
    "of every weakness already reflected in scores. Apply a label only when its\n"
    "defined mechanism is directly observable and severe enough by itself to make\n"
    "the text unsafe or unfit for this role. One intrinsically serious instance may\n"
    "qualify. Use multiple labels only for distinct mechanisms, never adjacent\n"
    "descriptions of the same defect."
)
FORBIDDEN = (
    "allen carr", "good sugar", "bad sugar", "identical-text", "degraded-reference",
    "scrambled", "reversed order", "control run", "specimen", "which_is_real_carr",
    "chapter-01",
)


def prompt(role):
    path = JUDGES / V2.ROLE_SPECS[role]["prompt"]
    text = path.read_text(encoding="utf-8")
    return text, text.encode("utf-8")


class CriticalTaxonomyPromptTests(unittest.TestCase):
    def test_v22_hashes_change_and_freeze_all_role_prompts(self):
        for role in V2.ROLE_SPECS:
            with self.subTest(role=role):
                _, raw = prompt(role)
                digest = hashlib.sha256(raw).hexdigest()
                self.assertNotEqual(digest, V21_HASHES[role])
                self.assertEqual(digest, V22_HASHES[role])

    def test_every_allowed_failure_is_defined_exactly_once(self):
        for role, spec in V2.ROLE_SPECS.items():
            with self.subTest(role=role):
                text, _ = prompt(role)
                taxonomy = text.split("List only these critical failures", 1)[1].split(
                    "`product_parity_verdict`", 1)[0]
                definitions = re.findall(r"^- `([a-z_]+)`: ", taxonomy, re.MULTILINE)
                self.assertEqual(set(definitions), spec["failures"])
                self.assertEqual(len(definitions), len(set(definitions)))
                for label in spec["failures"]:
                    self.assertEqual(text.count(f"`{label}`"), 1)

    def test_shared_materiality_rule_is_exact_and_generic(self):
        for role in V2.ROLE_SPECS:
            with self.subTest(role=role):
                text, _ = prompt(role)
                lowered = text.lower()
                self.assertEqual(text.count(SHARED_RULE), 1)
                self.assertIn("provenance", lowered)
                self.assertIn("author", lowered)
                for phrase in FORBIDDEN:
                    self.assertNotIn(phrase, lowered)
                for score_anchor in ("1–2", "1-2", "3–4", "3-4", "6–7", "6-7"):
                    self.assertNotIn(score_anchor, text)


if __name__ == "__main__":
    unittest.main()
