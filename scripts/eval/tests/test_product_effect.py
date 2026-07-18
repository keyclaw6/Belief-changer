"""Focused paired product-effect comparison contract tests."""
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
import product_effect as EFFECT  # noqa: E402


def valid_verdict(task, preferred="A"):
    return {"schema": 1, "task_sha256": task["task_sha256"],
            "mode": task["mode"], "preferred": preferred,
            "confidence": "MEDIUM",
            "decisive_reason": "The selected prose enacts the causal path more clearly."}


class ProductEffectTests(unittest.TestCase):
    def test_rubric_is_blind_comparison_only(self):
        """OpenSpec scenario: Paired comparison stays comparison-only."""
        text = (ROOT / "calibration/judges/product-effect-rubric.md").read_text()
        for phrase in ("anonymous candidates `A` and `B`", "materially stronger",
                       "Choose `TIE`", "similarly strong or similarly weak",
                       "named trap or thesis", "benefit catalogue",
                       "promised later", "analogy with an assumed mapping",
                       "intended-outcome summary", "instructed emotion",
                       "dependent prior insight -> weakened felt benefit ->",
                       "Do not make independent pass/fail claims"):
            self.assertIn(phrase, text)
        self.assertEqual(1, text.count("{{TASK}}"))
        self.assertNotIn("{{REFERENCE}}", text)
        for field in ("observations", "construct_sufficiency", "opening_sequence"):
            self.assertNotIn(field, text)

    def test_builds_strict_chapter_and_opening_pairs(self):
        """OpenSpec scenario: Paired comparison stays comparison-only."""
        chapter = EFFECT.chapter_pair("checking", "One.", "Two.")
        opening = EFFECT.whole_opening("checking", ["A1.", "A2."], ["B1.", "B2."])
        self.assertEqual(([1, 1], [2, 2]), ([len(item["chapters"])
            for item in chapter["candidates"].values()], [len(item["chapters"])
            for item in opening["candidates"].values()]))
        self.assertEqual(chapter, EFFECT.validate_task(chapter))
        self.assertEqual(opening, EFFECT.validate_task(opening))

    def test_task_rejects_identity_metadata_and_nonanonymous_labels(self):
        """OpenSpec scenario: H-F04 calibrates on a reference-as-candidate."""
        task = EFFECT.chapter_pair("checking", "One.", "Two.")
        for key in ("condition", "provenance", "scores", "history", "reference_identity"):
            changed = deepcopy(task); changed[key] = "leak"
            with self.subTest(key=key), self.assertRaises(EFFECT.ContractError):
                EFFECT.validate_task(changed)
        changed = deepcopy(task)
        changed["candidates"] = {"control": changed["candidates"]["A"],
                                 "treatment": changed["candidates"]["B"]}
        with self.assertRaises(EFFECT.ContractError):
            EFFECT.validate_task(changed)

    def test_h_f04_identity_stays_outside_judge_payload(self):
        """OpenSpec scenario: H-F04 calibrates on a reference-as-candidate."""
        task = EFFECT.whole_opening("checking", ["A1.", "A2."], ["B1.", "B2."])
        envelope = EFFECT.h_f04_envelope(task, "B")
        self.assertEqual(task, EFFECT.h_f04_judge_task(envelope))
        payload = json.dumps(EFFECT.h_f04_judge_task(envelope))
        for leak in ("reference_candidate", "promotion_eligible", "h_f04"):
            self.assertNotIn(leak, payload)

    def test_verdict_and_schema_are_exactly_comparison_only(self):
        """OpenSpec scenario: Paired comparison stays comparison-only."""
        task = EFFECT.chapter_pair("checking", "One.", "Two.")
        value = valid_verdict(task)
        self.assertEqual(value, EFFECT.verdict(json.dumps(value), task))
        schema = EFFECT.output_schema()
        self.assertEqual(set(value), set(schema["properties"]))
        self.assertFalse(schema["additionalProperties"])
        mutations = []
        for preferred in ("CONTROL", "MEETS"):
            changed = deepcopy(value); changed["preferred"] = preferred; mutations.append(changed)
        stale = deepcopy(value); stale["task_sha256"] = "stale"; mutations.append(stale)
        verbose = deepcopy(value); verbose["decisive_reason"] = "x" * 401; mutations.append(verbose)
        for changed in mutations:
            with self.subTest(changed=changed), self.assertRaises(EFFECT.ContractError):
                EFFECT.verdict(json.dumps(changed), task)

    def test_absolute_verdict_does_not_cross_validate(self):
        """OpenSpec scenario: Split verdicts do not cross-validate."""
        task = EFFECT.chapter_pair("checking", "One.", "Two.")
        absolute = {"schema": 1, "task_sha256": task["task_sha256"],
                    "mode": task["mode"], "observation": {},
                    "confidence": "MEDIUM"}
        with self.assertRaises(EFFECT.ContractError):
            EFFECT.verdict(json.dumps(absolute), task)

    def test_duplicate_keys_fail_closed(self):
        """Infra: strict JSON parsing rejects ambiguous judge output."""
        task = EFFECT.chapter_pair("checking", "One.", "Two.")
        raw = json.dumps(valid_verdict(task)).replace(
            '"schema": 1', '"schema": 1, "schema": 1')
        with self.assertRaises(EFFECT.ContractError):
            EFFECT.verdict(raw, task)


if __name__ == "__main__":
    unittest.main()
