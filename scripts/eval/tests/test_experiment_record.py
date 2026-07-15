"""RF-19 minimal causal-bundle record regressions."""
import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
import experiment_record as RECORD  # noqa: E402


class ExperimentRecordTests(unittest.TestCase):
    def setUp(self):
        self.records = RECORD.load(ROOT / "loop/causal-bundle-results.jsonl")

    def test_dry_run_is_one_minimal_causal_bundle(self):
        """OpenSpec requirement: Minimal experiment record."""
        self.assertEqual(1, len(self.records))
        record = self.records[0]
        self.assertEqual(RECORD.FIELDS, set(record))
        self.assertEqual(RECORD.EVIDENCE, set(record["evidence"]))
        self.assertEqual("DRY_RUN", record["decision"])
        self.assertTrue(record["causal_chain"])
        self.assertTrue(record["changed_bundle"])

    def test_old_reward_or_missing_layer_cannot_enter_lineage(self):
        """OpenSpec scenario: The experiment record grows beyond decision evidence."""
        reward = copy.deepcopy(self.records[0])
        reward["reward"] = 0.99
        with self.assertRaisesRegex(RECORD.RecordError, "minimal RF-19 schema"):
            RECORD.validate(reward)
        missing = copy.deepcopy(self.records[0])
        del missing["evidence"]["whole_opening_sequence"]
        with self.assertRaisesRegex(RECORD.RecordError, "four product layers"):
            RECORD.validate(missing)

    def test_record_requires_one_linked_hypothesis_and_falsifier(self):
        """OpenSpec requirement: Causal-bundle experiment."""
        for key in ("hypothesis", "falsifier"):
            with self.subTest(field=key):
                invalid = copy.deepcopy(self.records[0])
                invalid[key] = " "
                with self.assertRaises(RECORD.RecordError):
                    RECORD.validate(invalid)
        duplicate = copy.deepcopy(self.records[0])
        duplicate["changed_bundle"].append(duplicate["changed_bundle"][0])
        with self.assertRaisesRegex(RECORD.RecordError, "duplicates"):
            RECORD.validate(duplicate)

    def test_runbook_orders_reused_factory_stages(self):
        """OpenSpec requirement: Causal-bundle experiment."""
        runbook = (ROOT / "PROGRAM.md").read_text(encoding="utf-8")
        stages = (
            "Candidate isolation", "Generation", "Frozen batch",
            "Grounded review", "Developmental review", "Blind evaluation",
            "Owner routing", "Decision", "Atomic promotion",
        )
        positions = [runbook.index(f"**{stage}**") for stage in stages]
        self.assertEqual(sorted(positions), positions)
        self.assertIn("Never\ncompare their rewards numerically", runbook)


if __name__ == "__main__":
    unittest.main()
