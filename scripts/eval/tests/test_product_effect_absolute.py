"""Focused one-content product-effect contract tests."""
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
import product_effect_absolute as EFFECT  # noqa: E402


def observation(task, sufficiency="MEETS", links=None):
    if links is None:
        links = ({field: "NOT_APPLICABLE" for field in EFFECT.SEQUENCE_FIELDS}
                 if task["mode"] == "chapter" else
                 {field: "CLEAR" for field in EFFECT.SEQUENCE_FIELDS})
    return {
        "entering_belief": "The behavior promises relief.",
        "leaving_belief": "The behavior creates the discomfort.",
        "enacted_discovery": "A concrete encounter exposes the causal loop.",
        "subject_specificity": "CLEAR", "mechanism_credibility": "CLEAR",
        "emotion_relief": "PARTIAL", "escalation": "CLEAR",
        "continuity_handoff": "PARTIAL", "construct_sufficiency": sufficiency,
        "construct_reason": "The discovery earns the belief change now.",
        "opening_sequence": links,
    }


def verdict(task, sufficiency="MEETS", links=None, confidence="MEDIUM"):
    return {"schema": 1, "task_sha256": task["task_sha256"],
            "mode": task["mode"],
            "observation": observation(task, sufficiency, links),
            "confidence": confidence}


class AbsoluteProductEffectTests(unittest.TestCase):
    def test_rubric_is_one_content_absolute_and_has_no_comparator_terms(self):
        """OpenSpec scenario: One-content absolute assessment is strict."""
        text = (ROOT / "calibration/judges/product-effect-absolute-rubric.md").read_text()
        self.assertEqual(1, text.count("{{TASK}}"))
        for phrase in ("entering_belief", "leaving_belief", "enacted_discovery",
                       *EFFECT.RATING_FIELDS, *EFFECT.SEQUENCE_FIELDS,
                       "dependent prior", "weakened felt benefit -> reduced sacrifice",
                       "enacted after and from a non-`ABSENT` prerequisite"):
            self.assertIn(phrase, text)
        folded = text.casefold()
        for forbidden in ("{{reference}}", "comparison", "preference", "candidate `a`",
                          "candidate `b`", "anonymous a", "anonymous b"):
            self.assertNotIn(forbidden, folded)

    def test_tasks_contain_exactly_one_content(self):
        """OpenSpec scenario: One-content absolute assessment is strict."""
        chapter = EFFECT.chapter("checking", "One chapter.")
        opening = EFFECT.whole_opening("checking", ["First.", "Second."])
        self.assertEqual((1, 2), (len(chapter["chapters"]), len(opening["chapters"])))
        self.assertEqual(EFFECT.INSTRUMENT, chapter["instrument"])
        self.assertEqual(chapter, EFFECT.validate_task(chapter))
        for bad in ([], ["One.", "Two."]):
            body = deepcopy(chapter); body["chapters"] = bad
            body["task_sha256"] = EFFECT._hash({key: item for key, item in body.items()
                                                 if key != "task_sha256"})
            with self.assertRaises(EFFECT.ContractError):
                EFFECT.validate_task(body)
        with self.assertRaises(EFFECT.ContractError):
            EFFECT.whole_opening("checking", ["Only one."])

    def test_envelope_keeps_identity_and_scope_outside_payload(self):
        """OpenSpec scenario: H-F04 calibrates on a reference-as-candidate."""
        task = EFFECT.whole_opening("checking", ["First.", "Second."])
        calibration = EFFECT.envelope(task, "complete-opening", calibration=True)
        ordinary = EFFECT.envelope(task, "chapter-set-1", "a" * 64)
        self.assertEqual((False, None), (calibration["promotion_eligible"],
                                        calibration["tested_pair_hash"]))
        self.assertEqual((True, "a" * 64), (ordinary["promotion_eligible"],
                                           ordinary["tested_pair_hash"]))
        self.assertEqual(task, EFFECT.judge_task(calibration))
        payload = json.dumps(EFFECT.judge_task(calibration))
        for leak in ("complete-opening", "content_sha256", "scope", "tested_pair_hash"):
            self.assertNotIn(leak, payload)
        changed = deepcopy(calibration); changed["content_sha256"] = "0" * 64
        with self.assertRaises(EFFECT.ContractError):
            EFFECT.validate_envelope(changed)
        with self.assertRaises(EFFECT.ContractError):
            EFFECT.envelope(task, "ordinary-without-pair")

    def test_chapter_sequence_is_not_applicable_and_verdict_fields_are_exact(self):
        """OpenSpec scenario: One-content absolute assessment is strict."""
        task = EFFECT.chapter("checking", "One chapter.")
        value = verdict(task)
        self.assertEqual(value, EFFECT.verdict(json.dumps(value), task))
        schema = EFFECT.output_schema()
        self.assertEqual(set(value), set(schema["properties"]))
        changed = deepcopy(value)
        changed["observation"]["opening_sequence"]["prior_insight"] = "CLEAR"
        with self.assertRaises(EFFECT.ContractError):
            EFFECT.verdict(json.dumps(changed), task)

    def test_whole_sufficiency_is_iff_all_clear_and_clear_links_require_prerequisites(self):
        """OpenSpec scenario: One-content absolute assessment is strict."""
        task = EFFECT.whole_opening("checking", ["First.", "Second."])
        self.assertEqual(verdict(task), EFFECT.verdict(json.dumps(verdict(task)), task))
        cases = [
            verdict(task, "DOES_NOT_MEET"),
            verdict(task, "MEETS", {"prior_insight": "CLEAR", "felt_benefit": "PARTIAL",
                                     "reduced_sacrifice": "PARTIAL"}),
            verdict(task, "DOES_NOT_MEET", {"prior_insight": "ABSENT",
                "felt_benefit": "CLEAR", "reduced_sacrifice": "PARTIAL"}),
            verdict(task, "DOES_NOT_MEET", {"prior_insight": "CLEAR",
                "felt_benefit": "ABSENT", "reduced_sacrifice": "CLEAR"}),
        ]
        for changed in cases:
            with self.subTest(changed=changed), self.assertRaises(EFFECT.ContractError):
                EFFECT.verdict(json.dumps(changed), task)
        for field, marker in (("entering_belief", "UNRESOLVED"),
                              ("leaving_belief", "UNRESOLVED"),
                              ("enacted_discovery", "NOT_ENACTED")):
            changed = verdict(task)
            changed["observation"][field] = marker
            with self.subTest(field=field), self.assertRaises(EFFECT.ContractError):
                EFFECT.verdict(json.dumps(changed), task)

    def test_malformed_fields_ratings_and_duplicate_keys_fail_closed(self):
        """OpenSpec scenario: One-content absolute assessment is strict."""
        task = EFFECT.whole_opening("checking", ["First.", "Second."])
        value = verdict(task)
        mutations = []
        missing = deepcopy(value); del missing["observation"]["construct_reason"]
        mutations.append(missing)
        extra = deepcopy(value); extra["observation"]["score"] = 9; mutations.append(extra)
        numeric = deepcopy(value); numeric["observation"]["escalation"] = 3
        mutations.append(numeric)
        low = deepcopy(value); low["confidence"] = "CERTAIN"; mutations.append(low)
        stale = deepcopy(value); stale["task_sha256"] = "stale"; mutations.append(stale)
        for changed in mutations:
            with self.subTest(changed=changed), self.assertRaises(EFFECT.ContractError):
                EFFECT.verdict(json.dumps(changed), task)
        raw = json.dumps(value).replace('"schema": 1', '"schema": 1, "schema": 1')
        with self.assertRaises(EFFECT.ContractError):
            EFFECT.verdict(raw, task)

    def test_paired_verdict_does_not_cross_validate(self):
        """OpenSpec scenario: Split verdicts do not cross-validate."""
        task = EFFECT.chapter("checking", "One chapter.")
        paired = {"schema": 1, "task_sha256": task["task_sha256"],
                  "mode": task["mode"], "preferred": "A",
                  "confidence": "MEDIUM", "decisive_reason": "A is stronger."}
        with self.assertRaises(EFFECT.ContractError):
            EFFECT.verdict(json.dumps(paired), task)


if __name__ == "__main__":
    unittest.main()
