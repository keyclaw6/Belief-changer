"""Focused RF-16 blind product-effect contract tests."""
import inspect
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
import product_effect as EFFECT  # noqa: E402


def valid_verdict(task):
    observation = {
        "entering_belief": "The urge promises useful relief.",
        "leaving_belief": "The urge creates the discomfort it claims to solve.",
        "enacted_discovery": "A concrete before-and-after comparison exposes the loop.",
        "subject_specificity": "CLEAR", "mechanism_credibility": "CLEAR",
        "emotion_relief": "PARTIAL", "escalation": "CLEAR",
        "continuity_handoff": "PARTIAL",
    }
    return {"schema": 1, "task_sha256": task["task_sha256"], "mode": task["mode"],
            "observations": {"A": observation, "B": deepcopy(observation)},
            "preferred": "A", "confidence": "MEDIUM",
            "decisive_reason": "A makes the causal discovery more concrete."}


class ProductEffectTests(unittest.TestCase):
    def test_rubric_has_both_modes_all_measures_and_no_reference_slot(self):
        """OpenSpec requirement: Blind and independent judgment."""
        text = (ROOT / "calibration/judges/product-effect-rubric.md").read_text()
        for phrase in ("`chapter`", "`whole_opening`", *EFFECT.TEXT_FIELDS,
                       *EFFECT.RATING_FIELDS, "condition", "provenance", "scores", "history"):
            self.assertIn(phrase, text)
        self.assertIn("{{TASK}}", text)
        self.assertNotIn("{{REFERENCE}}", text)
        for boundary in ("reader-perceived causal legibility", "source grounding",
                         "safety", "medical truth", "integrity hard gate"):
            self.assertIn(boundary, text)

    def test_builds_strict_chapter_and_whole_opening_tasks(self):
        """OpenSpec requirement: Blind and independent judgment."""
        chapter = EFFECT.chapter_pair("compulsive checking", "A concrete phone scene.",
                                      "A generic instruction.")
        opening = EFFECT.whole_opening("compulsive checking",
            ["The promise is met.", "The loop is discovered.", "Relief follows."],
            ["The topic is named.", "Advice is listed.", "The reader is told to stop."])
        self.assertEqual(([1, 1], [3, 3]), ([len(item["chapters"])
            for item in chapter["candidates"].values()], [len(item["chapters"])
            for item in opening["candidates"].values()]))
        self.assertEqual(("chapter", "whole_opening"), (chapter["mode"], opening["mode"]))
        self.assertEqual(("A", "B"), tuple(chapter["candidates"]))
        self.assertEqual(chapter, EFFECT.validate_task(chapter))

    def test_task_rejects_identity_metadata_and_nonanonymous_labels(self):
        """OpenSpec scenario: H-F04 calibrates on a reference-as-candidate."""
        task = EFFECT.chapter_pair("checking", "Candidate one.", "Candidate two.")
        for key in ("condition", "provenance", "scores", "history", "reference_identity"):
            with self.subTest(key=key):
                changed = deepcopy(task)
                changed[key] = "leak"
                with self.assertRaises(EFFECT.ContractError):
                    EFFECT.validate_task(changed)
        changed = deepcopy(task)
        changed["candidates"] = {"control": changed["candidates"]["A"],
                                 "treatment": changed["candidates"]["B"]}
        with self.assertRaises(EFFECT.ContractError):
            EFFECT.validate_task(changed)

    def test_h_f04_identity_stays_outside_isolated_judge_payload(self):
        """OpenSpec scenario: H-F04 calibrates on a reference-as-candidate."""
        task = EFFECT.whole_opening("checking", ["First A.", "Second A."],
                                    ["First B.", "Second B."])
        envelope = EFFECT.h_f04_envelope(task, "B")
        payload = EFFECT.h_f04_judge_task(envelope)
        self.assertEqual(task, payload)
        self.assertEqual((True, False, False), (envelope["isolated"],
            envelope["generation_eligible"], envelope["promotion_eligible"]))
        serialized = json.dumps(payload)
        for leak in ("h_f04", "reference_candidate", "provenance", "promotion_eligible"):
            self.assertNotIn(leak, serialized)
        self.assertNotIn("reference", inspect.signature(EFFECT.chapter_pair).parameters)

    def test_verdict_is_exact_bound_and_categorical(self):
        """OpenSpec requirement: Separated product evidence."""
        task = EFFECT.chapter_pair("checking", "Candidate one.", "Candidate two.")
        value = valid_verdict(task)
        self.assertEqual(value, EFFECT.verdict(json.dumps(value), task))
        schema = EFFECT.output_schema()
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["properties"]["observations"]["properties"]), {"A", "B"})
        mutations = []
        unknown = deepcopy(value); unknown["score"] = 9; mutations.append(unknown)
        stale = deepcopy(value); stale["task_sha256"] = "stale"; mutations.append(stale)
        numeric = deepcopy(value); numeric["observations"]["A"]["escalation"] = 9
        mutations.append(numeric)
        verbose = deepcopy(value); verbose["decisive_reason"] = "x" * 401; mutations.append(verbose)
        for changed in mutations:
            with self.subTest(change=changed), self.assertRaises(EFFECT.ContractError):
                EFFECT.verdict(json.dumps(changed), task)

    def test_duplicate_verdict_keys_fail_closed(self):
        """Infra: strict JSON parsing rejects ambiguous judge output."""
        task = EFFECT.chapter_pair("checking", "Candidate one.", "Candidate two.")
        raw = json.dumps(valid_verdict(task)).replace('"schema": 1', '"schema": 1, "schema": 1')
        with self.assertRaises(EFFECT.ContractError):
            EFFECT.verdict(raw, task)


if __name__ == "__main__":
    unittest.main()
