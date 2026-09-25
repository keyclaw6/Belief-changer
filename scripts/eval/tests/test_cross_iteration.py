"""Small offline tests for cross-iteration learning and no-regression."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SOURCE / "scripts"))

from bc_factory.common import FactoryError, unseal
from bc_factory.demo import finish, inputs, metadata, scaffold
from bc_factory.learning import advance, seed
from bc_factory.regression import decide, submit, task
from bc_factory.runs import Run, prepare
from bc_factory.schema import DIMENSIONS


class CrossIterationLearningTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        scaffold(SOURCE, self.repo)
        self.brief, self.research, self.plan = inputs()

    def tearDown(self):
        self.tmp.cleanup()

    def completed(self, name, learning_from=None):
        prepare(self.repo, name, self.brief, self.research, fixture=True, learning_from=learning_from)
        run = Run(self.repo, name)
        finish(run, self.plan)
        return run

    def lessons(self):
        return {
            "schema_version": 2, "subject": self.brief["subject"],
            "preserve": [{"dimension": "argument", "instruction": "Preserve evidentiary boundaries.",
                          "evidence": "Prior blinded comparison."}],
            "improve": [{"dimension": "voice", "instruction": "Improve natural voice.",
                         "evidence": "Prior blinded comparison."}],
            "recurring_repairs": [{"kind": "OVERCLAIM",
                                   "instruction": "Do not turn anecdotes into prevalence claims.",
                                   "evidence": "Prior repaired defect."}],
            "research_gaps": ["Reader effects remain unmeasured."],
            "note": "Fixture learning packet.",
        }

    def seed_baseline(self):
        baseline = self.completed("baseline")
        seed(self.repo, "baseline", self.lessons())
        return baseline

    @staticmethod
    def judgment(judge_task, voice_winner="tie"):
        quote = "One unsuccessful attempt is one observation."
        return {
            "schema_version": 2,
            "preferences": {
                d: {"winner": voice_winner if d == "voice" else "tie",
                    "a_quote": quote, "b_quote": quote, "reason": "Synthetic fixture."}
                for d in DIMENSIONS
            },
            "critical": {"A": [], "B": []},
        }

    def test_learning_packet_is_frozen_into_book_roles(self):
        self.seed_baseline()
        prepare(self.repo, "candidate", self.brief, self.research, fixture=True, learning_from="baseline")
        run = Run(self.repo, "candidate")
        frozen = run.task("evidence-reviewer")
        self.assertEqual(frozen["inputs"]["cross_iteration_learning"], run.learning)
        self.assertIn("NOT empirical evidence", frozen["contract"])
        (run.root / "inputs/cross-iteration-learning.json").write_text("{}")
        with self.assertRaises(FactoryError):
            Run(self.repo, "candidate")

    def test_all_ties_preserve_existing_book_baseline(self):
        baseline = self.seed_baseline()
        self.completed("candidate", learning_from="baseline")
        for order in ("AB", "BA"):
            t = task(self.repo, "candidate", order)
            submit(self.repo, "candidate", order, self.judgment(t), metadata(True))
        self.assertEqual(decide(self.repo, "candidate")["decision"], "PRESERVE_BASELINE")
        result = advance(self.repo, "candidate")
        self.assertEqual(result["status"], "BASELINE_PRESERVED")
        self.assertEqual(result["baseline_run"], "baseline")
        self.assertFalse((self.repo / "runs/candidate/regression/learning-next.json").exists())
        self.assertTrue((baseline.root / "regression/learning-next.json").exists())

    def test_stable_improvement_advances_baseline(self):
        self.seed_baseline()
        candidate = self.completed("candidate", learning_from="baseline")
        for order, winner in (("AB", "B"), ("BA", "A")):
            t = task(self.repo, "candidate", order)
            submit(self.repo, "candidate", order, self.judgment(t, winner), metadata(True))
        self.assertEqual(decide(self.repo, "candidate")["decision"], "ADVANCE")
        self.assertEqual(advance(self.repo, "candidate")["status"], "BASELINE_ADVANCED")
        packet = unseal(candidate.root / "regression/learning-next.json")
        self.assertEqual(packet["baseline_run"], "candidate")
        self.assertTrue(any(x["dimension"] == "voice" for x in packet["preserve"]))

    def test_mixed_ab_ba_judges_are_inconclusive(self):
        self.seed_baseline()
        self.completed("candidate", learning_from="baseline")
        t = task(self.repo, "candidate", "AB")
        submit(self.repo, "candidate", "AB", self.judgment(t, "B"), metadata(True))
        t = task(self.repo, "candidate", "BA")
        other = metadata(True)
        other["model"] = "other-judge"
        other["route"] = "other-route"
        submit(self.repo, "candidate", "BA", self.judgment(t, "A"), other)
        gate = decide(self.repo, "candidate")
        self.assertEqual(gate["decision"], "INCONCLUSIVE")
        self.assertTrue(gate["judge_instrument_mixed"])
        with self.assertRaises(FactoryError):
            advance(self.repo, "candidate")


if __name__ == "__main__":
    unittest.main()
