"""Offline tests for the sealed outer factory-learning state machine."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SOURCE / "scripts"))

from bc_factory.common import FactoryError
from bc_factory.demo import scaffold
from bc_factory.factory_learning import freeze_change, register, submit_holdout
from bc_factory.runs import active_files


class FactoryLearningRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        scaffold(SOURCE, self.repo)
        shutil.copyfile(SOURCE / ".gitignore", self.repo / ".gitignore")
        self.git("init")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Fixture")
        self.git("add", "-A")
        self.git("commit", "-m", "baseline")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        p = subprocess.run(["git", *args], cwd=self.repo, capture_output=True, text=True)
        if p.returncode:
            raise AssertionError(p.stderr)
        return p.stdout.strip()

    @staticmethod
    def meta(family):
        return {"model": family + "-model", "family": family, "route": "offline-fixture",
                "harness": "fixture", "usage": None, "latency_s": 0.0}

    @staticmethod
    def learner():
        return {
            "schema_version": 2, "decision": "CHANGE_FACTORY",
            "observations": ["Training books show a repeatable voice/evidence tradeoff."],
            "candidate_root_causes": [{"mechanism": "One prompt mixes two jobs.",
                                       "support": ["Observed across two training subjects."],
                                       "alternatives": ["Judge variance remains possible."]}],
            "subject_specific_lessons": [],
            "transferable_factory_lessons": [{"lesson": "Separate the jobs.", "evidence": ["Two training subjects."],
                                               "scope": "Planning prompt only."}],
            "protected_strengths": [{"dimension": "argument", "constraint": "Preserve evidence discipline.",
                                      "evidence": "Stable prior advantage."}],
            "proposed_factory_change": {
                "hypothesis": "Separating jobs should recover voice without weakening argument.",
                "change_surface": ["prompts/chapter-writer.md"],
                "smallest_change": "Clarify one prompt boundary.",
                "expected_transfer": "The conflict is role-level rather than topic-level.",
                "possible_regressions": ["argument"],
            },
            "falsification_test": {
                "training_subjects": ["train-a", "train-b"],
                "holdout_requirements": ["One unseen habit topic and one unseen non-habit belief topic."],
                "success_criteria": ["No protected regression and a stable gain on the target dimension."],
                "failure_signals": ["Any held-out protected regression."],
                "leakage_rule": "Exact held-out topics are selected only after the intervention is frozen.",
            },
            "confidence": "medium", "reasoning_summary": "A bounded transferable hypothesis.",
        }

    @classmethod
    def reviewer(cls):
        l = cls.learner()
        return {
            "schema_version": 2, "verdict": "ACCEPT",
            "checks": {"transferable": True, "not_subject_overfit": True, "causal_honesty": True,
                       "minimal_change": True, "protected_strengths": True, "held_out_integrity": True,
                       "judge_overfit_control": True, "falsifiable": True},
            "findings": [], "approved_change_surface": ["prompts/chapter-writer.md"],
            "held_out_test": {
                "holdout_requirements": l["falsification_test"]["holdout_requirements"],
                "success_criteria": l["falsification_test"]["success_criteria"],
                "failure_signals": l["falsification_test"]["failure_signals"],
            },
            "reasoning_summary": "The change is narrow enough to test.",
        }

    def test_new_runs_freeze_outer_orchestration_contracts(self):
        files = set(active_files(SOURCE))
        for rel in ("AGENTS.md", "loop/PROGRAM.md", "loop/prompts/factory-learner.md",
                    "loop/prompts/factory-learning-reviewer.md", ".opencode/agents/factory-learner.md"):
            self.assertIn(rel, files)

    def test_reviewed_change_freezes_before_independent_holdout_selection(self):
        register(self.repo, "cycle-1", self.learner(), self.meta("learner"),
                 self.reviewer(), self.meta("reviewer"))
        with self.assertRaises(FactoryError):
            submit_holdout(self.repo, "cycle-1",
                           {"schema_version": 2, "subjects": ["held-a"], "rationale": "unseen"},
                           self.meta("selector"))
        p = self.repo / "prompts/chapter-writer.md"
        p.write_text(p.read_text() + "\n<!-- fixture intervention -->\n")
        self.git("add", "prompts/chapter-writer.md"); self.git("commit", "-m", "intervention")
        change = freeze_change(self.repo, "cycle-1")
        self.assertEqual(change["changed_paths"], ["prompts/chapter-writer.md"])
        with self.assertRaises(FactoryError):
            submit_holdout(self.repo, "cycle-1",
                           {"schema_version": 2, "subjects": ["train-a"], "rationale": "bad overlap"},
                           self.meta("selector"))
        result = submit_holdout(self.repo, "cycle-1",
                                {"schema_version": 2, "subjects": ["held-a", "held-b"],
                                 "rationale": "Selected after freeze to satisfy the generic transfer criteria."},
                                self.meta("selector"))
        self.assertEqual(result["selection"]["subjects"], ["held-a", "held-b"])

    def test_reviewer_and_selector_must_be_independent(self):
        with self.assertRaises(FactoryError):
            register(self.repo, "cycle-bad", self.learner(), self.meta("same"),
                     self.reviewer(), self.meta("same"))
        register(self.repo, "cycle-2", self.learner(), self.meta("learner"),
                 self.reviewer(), self.meta("reviewer"))
        p = self.repo / "prompts/chapter-writer.md"
        p.write_text(p.read_text() + "\n<!-- fixture intervention -->\n")
        self.git("add", "prompts/chapter-writer.md"); self.git("commit", "-m", "intervention")
        freeze_change(self.repo, "cycle-2")
        with self.assertRaises(FactoryError):
            submit_holdout(self.repo, "cycle-2",
                           {"schema_version": 2, "subjects": ["held-a", "held-b"], "rationale": "unseen"},
                           self.meta("learner"))

    def test_change_surface_is_enforced_from_git_diff(self):
        register(self.repo, "cycle-3", self.learner(), self.meta("learner"),
                 self.reviewer(), self.meta("reviewer"))
        p = self.repo / "prompts/chapter-reviewer.md"
        p.write_text(p.read_text() + "\n<!-- undeclared change -->\n")
        self.git("add", "prompts/chapter-reviewer.md"); self.git("commit", "-m", "bad intervention")
        with self.assertRaises(FactoryError):
            freeze_change(self.repo, "cycle-3")


if __name__ == "__main__":
    unittest.main()
