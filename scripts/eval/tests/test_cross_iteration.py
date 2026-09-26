"""Small offline tests for caller-owned cross-iteration learning and no-regression."""
from __future__ import annotations

from pathlib import Path
import shutil
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SOURCE / "scripts"))

from bc_factory.common import FactoryError, unseal
from bc_factory.demo import finish, inputs, metadata, scaffold
from bc_autoresearch.learning import advance, context_path, seed
from bc_autoresearch.regression import decide, submit, task
from bc_factory.runs import Run, prepare
from bc_factory.schema import DIMENSIONS


class CrossIterationLearningTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        scaffold(SOURCE, self.repo)
        judge = self.repo / "loop/judges/pairwise.md"
        judge.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE / "loop/judges/pairwise.md", judge)
        self.brief, self.research, self.plan = inputs()

    def tearDown(self):
        self.tmp.cleanup()

    def completed(self, name, baseline=None):
        caller_context = unseal(context_path(Run(self.repo, baseline))) if baseline else None
        prepare(self.repo, name, self.brief, self.research, fixture=True, caller_context=caller_context)
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

    def test_learning_becomes_generic_frozen_caller_context(self):
        baseline = self.seed_baseline()
        context = unseal(context_path(baseline))
        prepare(self.repo, "candidate", self.brief, self.research, fixture=True, caller_context=context)
        run = Run(self.repo, "candidate")
        frozen = run.task("evidence-reviewer")
        self.assertEqual(frozen["inputs"]["caller_context"], context)
        self.assertNotIn("baseline_run", context)
        self.assertNotIn("provenance", context)
        self.assertIn("NOT empirical evidence", frozen["contract"])
        (run.root / "inputs/caller-context.json").write_text("{}")
        with self.assertRaises(FactoryError):
            Run(self.repo, "candidate")

    def test_all_ties_preserve_existing_book_baseline(self):
        baseline = self.seed_baseline()
        self.completed("candidate", baseline="baseline")
        for order in ("AB", "BA"):
            t = task(self.repo, "candidate", "baseline", order)
            submit(self.repo, "candidate", "baseline", order, self.judgment(t), metadata(True))
        self.assertEqual(decide(self.repo, "candidate", "baseline")["decision"], "PRESERVE_BASELINE")
        result = advance(self.repo, "candidate", "baseline")
        self.assertEqual(result["status"], "BASELINE_PRESERVED")
        self.assertEqual(result["baseline_run"], "baseline")
        self.assertFalse((self.repo / "runs/candidate/caller-feedback/learning-next.json").exists())
        self.assertTrue((baseline.root / "caller-feedback/learning-next.json").exists())

    def test_stable_improvement_advances_baseline(self):
        self.seed_baseline()
        candidate = self.completed("candidate", baseline="baseline")
        for order, winner in (("AB", "B"), ("BA", "A")):
            t = task(self.repo, "candidate", "baseline", order)
            submit(self.repo, "candidate", "baseline", order, self.judgment(t, winner), metadata(True))
        self.assertEqual(decide(self.repo, "candidate", "baseline")["decision"], "ADVANCE")
        self.assertEqual(advance(self.repo, "candidate", "baseline")["status"], "BASELINE_ADVANCED")
        packet = unseal(candidate.root / "caller-feedback/learning-next.json")
        self.assertEqual(packet["baseline_run"], "candidate")
        self.assertTrue(any(x["dimension"] == "voice" for x in packet["preserve"]))
        context = unseal(candidate.root / "caller-feedback/factory-context.json")
        self.assertNotIn("baseline_run", context)
        self.assertTrue(any(x["area"] == "voice" for x in context["editorial_constraints"]))

    def test_mixed_ab_ba_judges_are_inconclusive(self):
        self.seed_baseline()
        self.completed("candidate", baseline="baseline")
        t = task(self.repo, "candidate", "baseline", "AB")
        submit(self.repo, "candidate", "baseline", "AB", self.judgment(t, "B"), metadata(True))
        t = task(self.repo, "candidate", "baseline", "BA")
        other = metadata(True)
        other["model"] = "other-judge"
        other["route"] = "other-route"
        submit(self.repo, "candidate", "baseline", "BA", self.judgment(t, "A"), other)
        gate = decide(self.repo, "candidate", "baseline")
        self.assertEqual(gate["decision"], "INCONCLUSIVE")
        self.assertTrue(gate["judge_instrument_mixed"])
        with self.assertRaises(FactoryError):
            advance(self.repo, "candidate", "baseline")


if __name__ == "__main__":
    unittest.main()
