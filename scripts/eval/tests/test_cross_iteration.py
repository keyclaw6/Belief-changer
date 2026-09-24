"""Offline cross-iteration learning tests. No network/model calls."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SOURCE / "scripts"))

from bc_factory.common import FactoryError, canonical, file_hash, seal, unseal
from bc_factory.demo import finish, inputs, metadata, scaffold
from bc_factory.learning import advance, load_next, research_guidance, seed, validate_lessons
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

    def research_for(self, learning_from=None):
        research = copy.deepcopy(self.research)
        if learning_from is None:
            return research
        source = Run(self.repo, learning_from)
        packet = load_next(source)
        guidance = research_guidance(packet, self.brief)
        for gap in packet["research_gaps"]:
            if gap not in research["open_questions"]:
                research["open_questions"].append(gap)
        research["learning_context"] = {
            "guidance_sha256": guidance["guidance_sha256"],
            "baseline_run": packet["baseline_run"],
            "gap_resolutions": [{
                "gap": gap, "status": "unresolved", "evidence_ids": [],
                "note": "Synthetic fixture explicitly carried this inherited gap into the fresh research pass."
            } for gap in packet["research_gaps"]],
        }
        return research

    def completed(self, name, learning_from=None):
        prepare(self.repo, name, self.brief, self.research_for(learning_from),
                fixture=True, learning_from=learning_from)
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

    def test_learning_is_bound_before_research_and_frozen_into_role_tasks(self):
        self.seed_baseline()
        with self.assertRaises(FactoryError):
            prepare(self.repo, "missing-guidance", self.brief, self.research,
                    fixture=True, learning_from="baseline")
        research = self.research_for("baseline")
        bad = copy.deepcopy(research)
        bad["learning_context"]["guidance_sha256"] = "0" * 64
        with self.assertRaises(FactoryError):
            prepare(self.repo, "stale-guidance", self.brief, bad,
                    fixture=True, learning_from="baseline")
        prepare(self.repo, "candidate", self.brief, research, fixture=True, learning_from="baseline")
        run = Run(self.repo, "candidate")
        self.assertEqual(run.learning["baseline_run"], "baseline")
        frozen = run.task("evidence-reviewer")
        self.assertEqual(frozen["inputs"]["cross_iteration_learning"], run.learning)
        self.assertIn("NOT empirical evidence", frozen["contract"])
        (run.root / "inputs/cross-iteration-learning.json").write_text("{}")
        with self.assertRaises(FactoryError):
            Run(self.repo, "candidate")

    def test_legacy_learning_run_without_research_receipt_remains_readable(self):
        self.seed_baseline()
        root = prepare(self.repo, "legacy-candidate", self.brief, self.research_for("baseline"),
                       fixture=True, learning_from="baseline")
        manifest = unseal(root / "manifest.json")
        legacy_research = copy.deepcopy(self.research)
        (root / "inputs/research.json").write_bytes(canonical(legacy_research) + b"\n")
        manifest["research_sha256"] = file_hash(root / "inputs/research.json")
        manifest.pop("research_guidance_sha256", None)
        (root / "manifest.json").unlink()
        seal(root / "manifest.json", manifest)
        run = Run(self.repo, "legacy-candidate")
        self.assertEqual(run.learning["baseline_run"], "baseline")
        self.assertNotIn("learning_context", run.research)

    def test_scoped_out_inherited_gap_cannot_resurrect_through_open_questions(self):
        self.seed_baseline()
        research = self.research_for("baseline")
        gap = self.lessons()["research_gaps"][0]
        research["learning_context"]["gap_resolutions"][0]["status"] = "scoped_out"
        research["open_questions"] = [q for q in research["open_questions"] if q != gap]
        prepare(self.repo, "scoped", self.brief, research, fixture=True, learning_from="baseline")
        bad = self.research_for("baseline")
        bad["learning_context"]["gap_resolutions"][0]["status"] = "scoped_out"
        with self.assertRaises(FactoryError):
            prepare(self.repo, "scoped-bad", self.brief, bad, fixture=True, learning_from="baseline")

    def test_seed_rejects_wrong_subject_and_conflicting_dimension(self):
        self.completed("baseline")
        bad = self.lessons(); bad["subject"] = "other-subject"
        with self.assertRaises(FactoryError):
            seed(self.repo, "baseline", bad)
        bad = self.lessons(); bad["improve"][0]["dimension"] = "argument"
        with self.assertRaises(FactoryError):
            validate_lessons(bad)

    def test_all_ties_preserve_book_baseline_but_append_learning_revision(self):
        baseline = self.seed_baseline()
        candidate = self.completed("candidate", learning_from="baseline")
        for order in ("AB", "BA"):
            frozen = task(self.repo, "candidate", order)
            blob = json.dumps(frozen)
            self.assertNotIn('"run_id"', blob)
            self.assertNotIn('"baseline_run"', blob)
            submit(self.repo, "candidate", order, self.judgment(frozen), metadata(True))
        gate = decide(self.repo, "candidate")
        self.assertEqual(gate["decision"], "PRESERVE_BASELINE")
        result = advance(self.repo, "candidate")
        self.assertEqual(result["status"], "BASELINE_PRESERVED_LEARNING_UPDATED")
        self.assertEqual(result["baseline_run"], "baseline")
        packet = load_next(baseline)
        self.assertEqual(packet["baseline_run"], "baseline")
        self.assertEqual(packet["provenance"]["mode"], "no_regression_preserve")
        self.assertIn("Reader effects remain unmeasured.", packet["research_gaps"])
        prepare(self.repo, "next", self.brief, self.research_for("baseline"),
                fixture=True, learning_from="baseline")
        self.assertEqual(Run(self.repo, "next").learning["baseline_run"], "baseline")

    def test_stable_candidate_win_advances_baseline(self):
        self.seed_baseline()
        candidate = self.completed("candidate", learning_from="baseline")
        for order, winner in (("AB", "B"), ("BA", "A")):
            frozen = task(self.repo, "candidate", order)
            submit(self.repo, "candidate", order, self.judgment(frozen, winner), metadata(True))
        gate = decide(self.repo, "candidate")
        self.assertEqual(gate["decision"], "ADVANCE")
        result = advance(self.repo, "candidate")
        self.assertEqual(result["status"], "BASELINE_ADVANCED")
        packet = load_next(candidate)
        self.assertEqual(packet["baseline_run"], "candidate")
        self.assertTrue(any(x["dimension"] == "voice" for x in packet["preserve"]))

    def test_stale_candidate_cannot_overwrite_newer_learning_revision(self):
        baseline = self.seed_baseline()
        candidate_a = self.completed("candidate-a", learning_from="baseline")
        candidate_b = self.completed("candidate-b", learning_from="baseline")
        for order in ("AB", "BA"):
            frozen = task(self.repo, "candidate-a", order)
            submit(self.repo, "candidate-a", order, self.judgment(frozen), metadata(True))
        self.assertEqual(decide(self.repo, "candidate-a")["decision"], "PRESERVE_BASELINE")
        advance(self.repo, "candidate-a")
        self.assertNotEqual(load_next(baseline), candidate_b.learning)
        for order, winner in (("AB", "B"), ("BA", "A")):
            frozen = task(self.repo, "candidate-b", order)
            submit(self.repo, "candidate-b", order, self.judgment(frozen, winner), metadata(True))
        self.assertEqual(decide(self.repo, "candidate-b")["decision"], "ADVANCE")
        with self.assertRaises(FactoryError):
            advance(self.repo, "candidate-b")

    def test_accepted_candidate_cannot_reopen_without_regression_failure(self):
        self.seed_baseline()
        candidate = self.completed("candidate", learning_from="baseline")
        with self.assertRaises(FactoryError):
            candidate.task("book-editor", round_no=2)


if __name__ == "__main__":
    unittest.main()
