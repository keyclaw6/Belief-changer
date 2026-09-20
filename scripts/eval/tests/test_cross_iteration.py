"""Offline cross-iteration learning tests. No network/model calls."""
from __future__ import annotations
import json
from pathlib import Path
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SOURCE / "scripts"))

from bc_factory.common import FactoryError, unseal
from bc_factory.demo import finish, inputs, metadata, scaffold
from bc_factory.learning import advance, seed, validate_lessons
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
        return {"schema_version": 2, "subject": self.brief["subject"],
                "preserve": [{"dimension": "argument",
                              "instruction": "Preserve explicit evidentiary boundaries.",
                              "evidence": "Prior blinded comparison preferred the bounded argument."}],
                "improve": [{"dimension": "voice",
                             "instruction": "Recover direct natural voice without weakening evidence discipline.",
                             "evidence": "Prior comparison found the earlier baseline more natural."}],
                "recurring_repairs": [{"kind": "OVERCLAIM",
                                       "instruction": "Do not turn an anecdote into a prevalence claim.",
                                       "evidence": "A prior lineage regenerated an unsupported generalization."}],
                "research_gaps": ["Reader effects remain unmeasured."],
                "note": "Explicit bootstrap from the completed prior iteration."}

    def seed_baseline(self):
        run = self.completed("baseline")
        self.assertEqual(seed(self.repo, "baseline", self.lessons())["status"], "LEARNING_SEEDED")
        return run

    @staticmethod
    def judgment(judge_task, voice_winner="tie"):
        quote = "One unsuccessful attempt is one observation."
        prefs = {d: {"winner": voice_winner if d == "voice" else "tie",
                     "a_quote": quote, "b_quote": quote,
                     "reason": "Synthetic fixture comparison for gate behavior only."}
                 for d in DIMENSIONS}
        return {"schema_version": 2, "preferences": prefs, "critical": {"A": [], "B": []}}

    def test_learning_is_frozen_into_role_tasks(self):
        self.seed_baseline()
        prepare(self.repo, "candidate", self.brief, self.research, fixture=True, learning_from="baseline")
        run = Run(self.repo, "candidate")
        self.assertEqual(run.learning["baseline_run"], "baseline")
        frozen = run.task("evidence-reviewer")
        self.assertEqual(frozen["inputs"]["cross_iteration_learning"], run.learning)
        self.assertIn("NOT empirical evidence", frozen["contract"])
        (run.root / "inputs/cross-iteration-learning.json").write_text("{}")
        with self.assertRaises(FactoryError):
            Run(self.repo, "candidate")

    def test_seed_rejects_wrong_subject_and_conflicting_dimension(self):
        self.completed("baseline")
        bad = self.lessons()
        bad["subject"] = "other-subject"
        with self.assertRaises(FactoryError):
            seed(self.repo, "baseline", bad)
        bad = self.lessons()
        bad["improve"][0]["dimension"] = "argument"
        with self.assertRaises(FactoryError):
            validate_lessons(bad)

    def test_tied_candidate_passes_and_becomes_next_baseline(self):
        self.seed_baseline()
        candidate = self.completed("candidate", learning_from="baseline")
        for order in ("AB", "BA"):
            frozen = task(self.repo, "candidate", order)
            blob = json.dumps(frozen)
            self.assertNotIn('"run_id"', blob)
            self.assertNotIn('"baseline_run"', blob)
            submit(self.repo, "candidate", order, self.judgment(frozen), metadata(True))
        gate = decide(self.repo, "candidate")
        self.assertEqual(gate["decision"], "PASS")
        self.assertEqual(advance(self.repo, "candidate")["status"], "BASELINE_ADVANCED")
        packet = unseal(candidate.root / "regression/learning-next.json")
        self.assertEqual(packet["baseline_run"], "candidate")
        self.assertTrue(any(x["dimension"] == "voice" for x in packet["improve"]))
        prepare(self.repo, "next", self.brief, self.research, fixture=True, learning_from="candidate")
        self.assertEqual(Run(self.repo, "next").learning["baseline_run"], "candidate")

    def test_accepted_candidate_cannot_reopen_without_regression_failure(self):
        self.seed_baseline()
        candidate = self.completed("candidate", learning_from="baseline")
        with self.assertRaises(FactoryError):
            candidate.task("book-editor", round_no=2)


if __name__ == "__main__":
    unittest.main()
