"""RF-17/RF-18 semantic decision-table regressions."""
import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
import product_decision as DECISION  # noqa: E402

TESTED, PROMPT = "a" * 64, "b" * 64


def core(**changes):
    checks = {
        "originality": {"tripped": False},
        "near_copy": [{"ratio": 0.1, "tripwire": 0.5}],
        "mantra": {"failures": []}, "length": [{"ok": True}],
        "repetition_within": {"hard_fails": []},
    }
    checks.update(changes)
    return {"checks": checks}


def verdict(prefix, index, vote="PASS", family="openai", kind="model",
            actor=None, base=None, input_hash=None):
    row = {
        "raw_verdict_id": f"raw-{prefix}-{index}",
        "actor": actor or f"judge-{prefix}-{index}", "kind": kind,
        "family": family if kind == "model" else None, "verdict": vote,
        "scope": "ordinary_product", "promotion_eligible": True,
        "base_task_sha256": base or DECISION.PS.state_hash(prefix),
        "tested_pair_hash": TESTED, "prompt_sha256": PROMPT,
        "input_sha256": input_hash or DECISION.PS.state_hash(f"input-{prefix}"),
    }
    row["task_id"] = DECISION.bound_task_id(row)
    return row


def pair(prefix, votes=("PASS", "PASS")):
    return [verdict(prefix, 1, votes[0], "openai"),
            verdict(prefix, 2, votes[1], "anthropic")]


def decide(**changes):
    values = {
        "core": core(), "grounded_review": {"state": "PASSED"},
        "developmental_review": {"state": "PASS"},
        "chapter_effect": pair("effect"),
        "whole_opening_sequence": pair("sequence"),
        "carr_craft": {"reward": 10, "diagnosis": "craft evidence only"},
        "tested_pair_hash": TESTED, "prompt_sha256": PROMPT,
    }
    values.update(changes)
    return DECISION.decide(**values)


class ProductDecisionTests(unittest.TestCase):
    def test_four_layers_stay_separate_without_a_master_reward(self):
        """OpenSpec scenario: Likeness improves without reader effect."""
        result = decide(chapter_effect=pair("effect", ("FAIL", "FAIL")),
                        carr_craft={"reward": 10, "verdict": "excellent"})
        self.assertEqual("REJECT", result["decision"])
        self.assertEqual({"integrity_hard_gate", "blind_chapter_effect",
                          "blind_whole_opening_sequence", "carr_craft_diagnostic"},
                         set(result["layers"]))
        self.assertEqual("DIAGNOSTIC_ONLY",
                         result["layers"]["carr_craft_diagnostic"]["role"])
        self.assertNotIn("reward", result)

    def test_recomputed_integrity_failures_are_non_overridable(self):
        """OpenSpec scenario: A candidate is too close to the matched reference."""
        failures = {
            "originality_pass": {"originality": {"tripped": True}},
            "near_copy_pass": {"near_copy": [{"ratio": 0.8, "tripwire": 0.5}]},
            "exact_mantra_pass": {"mantra": {"failures": ["missing"]}},
            "loose_length_pass": {"length": [{"ok": False}]},
        }
        for field, changes in failures.items():
            with self.subTest(field=field):
                result = decide(core=core(**changes))
                self.assertEqual("REJECT", result["decision"])
                self.assertIn(field, result["layers"]["integrity_hard_gate"]["failures"])
        with self.assertRaisesRegex(DECISION.ProductDecisionError, "receipts required"):
            decide(grounded_review={"state": "BLOCKED"})

    def test_repetition_is_repair_only_and_old_reward_cannot_override_effect(self):
        """OpenSpec requirement: Separated product evidence."""
        repeated = core(repetition_within={"hard_fails": [{"text": "echo"}]})
        result = decide(core=repeated)
        self.assertEqual("PROMOTE", result["decision"])
        self.assertEqual(["non_mantra_repetition"],
                         result["layers"]["integrity_hard_gate"]["repair_signals"])
        rejected = decide(chapter_effect=pair("effect", ("FAIL", "FAIL")),
                          carr_craft={"reward": 999})
        self.assertEqual("REJECT", rejected["decision"])

    def test_material_disagreement_is_inconclusive(self):
        """OpenSpec scenario: Evaluator disagreement is too large."""
        result = decide(chapter_effect=pair("effect", ("PASS", "FAIL")))
        self.assertEqual("INCONCLUSIVE", result["decision"])

    def test_two_families_or_one_model_plus_named_human_are_valid(self):
        """OpenSpec requirement: Blind and independent judgment."""
        self.assertEqual("two_model_families",
                         DECISION.aggregate_pair(pair("models"))["panel"])
        human = [verdict("mixed", 1), verdict(
            "mixed", 2, kind="human", actor="Founder Kristian")]
        self.assertEqual("model_plus_named_human",
                         DECISION.aggregate_pair(human)["panel"])

    def test_independence_and_task_pair_binding_fail_closed(self):
        """OpenSpec requirement: Blind and independent judgment."""
        cases = []
        for field in ("task_id", "raw_verdict_id"):
            rows = pair(field)
            rows[1][field] = rows[0][field]
            cases.append(rows)
        same_family = pair("family")
        same_family[1]["family"] = same_family[0]["family"]
        unrelated = pair("unrelated")
        unrelated[1]["base_task_sha256"] = "c" * 64
        unrelated[1]["task_id"] = DECISION.bound_task_id(unrelated[1])
        cases.extend((same_family, unrelated))
        for rows in cases:
            with self.subTest(rows=rows), self.assertRaises(
                    DECISION.ProductDecisionError):
                DECISION.aggregate_pair(rows)
        reused = pair("effect")
        with self.assertRaisesRegex(DECISION.ProductDecisionError, "reuse"):
            decide(whole_opening_sequence=reused)

    def test_calibration_rows_and_stale_rubric_are_rejected(self):
        row = verdict("scope", 1)
        row.update(scope="h_f04_calibration", promotion_eligible=False,
                   tested_pair_hash=None)
        with self.assertRaisesRegex(DECISION.ProductDecisionError, "calibration"):
            DECISION.aggregate_pair([row, copy.deepcopy(row)])
        with self.assertRaisesRegex(DECISION.ProductDecisionError, "stale"):
            DECISION.aggregate_pair(pair("stale"), prompt_sha256="c" * 64)

    def test_owner_vocabulary_covers_the_complete_factory(self):
        self.assertEqual(("brief", "research/synthesis", "framing", "plan",
                          "commission/context", "prose", "revision", "evaluation"),
                         DECISION.OWNERS)


if __name__ == "__main__":
    unittest.main()
