"""Offline tests for the sealed outer factory-learning state machine."""
from __future__ import annotations

import copy
import shutil
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SOURCE / "scripts"))

from bc_factory.common import FactoryError, digest
from bc_factory.demo import finish, inputs, scaffold
from bc_factory.factory_learning import freeze_change, freeze_evidence, register, submit_holdout
from bc_factory.runs import active_files, Run, prepare


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
        self.git("branch", "-M", "factory-learning-test")
        self.training_runs = []
        for subject in ("train-a", "train-b"):
            brief, research, plan = inputs(subject)
            rid = subject + "-run"
            prepare(self.repo, rid, brief, research, fixture=True)
            finish(Run(self.repo, rid), plan)
            self.training_runs.append(rid)

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
                "harness": "offline-test", "usage": None, "latency_s": 0.0}

    @staticmethod
    def learner():
        return {
            "schema_version": 2, "evidence_sha256": "0" * 64, "decision": "CHANGE_FACTORY",
            "observations": ["Training books show a repeatable voice/evidence tradeoff."],
            "candidate_root_causes": [{"mechanism": "One prompt mixes two jobs.",
                                       "support": ["Observed across two training subjects."],
                                       "alternatives": ["Judge variance remains possible."]}],
            "subject_specific_lessons": [],
            "transferable_factory_lessons": [{"lesson": "Separate the jobs.",
                                               "evidence": ["Two training subjects."],
                                               "scope": "Planning prompt only."}],
            "protected_strengths": [{"dimension": "argument",
                                      "constraint": "Preserve evidence discipline.",
                                      "evidence": "Stable prior advantage."}],
            "proposed_factory_change": {
                "hypothesis": "Separating jobs should recover voice without weakening argument.",
                "primary_dimension": "voice",
                "change_surface": ["prompts/chapter-writer.md"],
                "smallest_change": "Clarify one prompt boundary.",
                "expected_transfer": "The conflict is role-level rather than topic-level.",
                "possible_regressions": ["argument"],
            },
            "falsification_test": {
                "training_subjects": ["train-a", "train-b"],
                "holdout_requirements": ["One unseen habit topic and one unseen non-habit belief topic."],
                "acceptance_policy": "strict_transfer_v1",
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
            "schema_version": 2, "evidence_sha256": "0" * 64, "learner_sha256": "0" * 64,
            "verdict": "ACCEPT",
            "checks": {"transferable": True, "not_subject_overfit": True, "causal_honesty": True,
                       "minimal_change": True, "protected_strengths": True, "held_out_integrity": True,
                       "judge_overfit_control": True, "falsifiable": True},
            "findings": [], "approved_change_surface": ["prompts/chapter-writer.md"],
            "held_out_test": {
                "holdout_requirements": l["falsification_test"]["holdout_requirements"],
                "acceptance_policy": l["falsification_test"]["acceptance_policy"],
                "success_criteria": l["falsification_test"]["success_criteria"],
                "failure_signals": l["falsification_test"]["failure_signals"],
            },
            "reasoning_summary": "The change is narrow enough to test.",
        }

    def bound_docs(self, cycle, learner=None, reviewer=None):
        evidence = freeze_evidence(self.repo, cycle, self.training_runs)
        learner = copy.deepcopy(learner or self.learner())
        learner["evidence_sha256"] = digest(evidence)
        reviewer = copy.deepcopy(reviewer or self.reviewer())
        reviewer["evidence_sha256"] = digest(evidence)
        reviewer["learner_sha256"] = digest(learner)
        return evidence, learner, reviewer

    def register_cycle(self, cycle, learner=None, reviewer=None):
        evidence, learner, reviewer = self.bound_docs(cycle, learner, reviewer)
        register(self.repo, cycle, learner, self.meta("learner"),
                 reviewer, self.meta("reviewer"))
        return evidence, learner, reviewer

    def test_new_runs_freeze_outer_orchestration_contracts(self):
        files = set(active_files(SOURCE))
        for rel in ("AGENTS.md", "loop/PROGRAM.md", "loop/prompts/factory-learner.md",
                    "loop/prompts/factory-learning-reviewer.md", ".opencode/agents/factory-learner.md",
                    "scripts/bc_factory/learning.py", "scripts/bc_factory/factory_learning.py"):
            self.assertIn(rel, files)

    def test_frozen_training_evidence_is_idempotent_only_for_same_inputs_and_revalidated(self):
        evidence = freeze_evidence(self.repo, "cycle-idem", self.training_runs)
        self.assertEqual(freeze_evidence(self.repo, "cycle-idem", list(reversed(self.training_runs))), evidence)
        with self.assertRaises(FactoryError):
            freeze_evidence(self.repo, "cycle-idem", [self.training_runs[0]])
        # Tampering with a sealed run artifact invalidates the evidence receipt.
        run = Run(self.repo, self.training_runs[0])
        audit = run.accepted_audit_file()
        original = audit.read_bytes()
        audit.write_bytes(original + b"\n")
        with self.assertRaises(FactoryError):
            freeze_evidence(self.repo, "cycle-idem", self.training_runs)

    def test_training_evidence_binds_learner_and_reviewer(self):
        evidence = freeze_evidence(self.repo, "cycle-evidence", self.training_runs)
        learner = self.learner()
        reviewer = self.reviewer()
        with self.assertRaises(FactoryError):
            register(self.repo, "cycle-evidence", learner, self.meta("learner"),
                     reviewer, self.meta("reviewer"))
        learner["evidence_sha256"] = digest(evidence)
        reviewer["evidence_sha256"] = digest(evidence)
        reviewer["learner_sha256"] = "0" * 64
        with self.assertRaises(FactoryError):
            register(self.repo, "cycle-evidence", learner, self.meta("learner"),
                     reviewer, self.meta("reviewer"))
        reviewer["learner_sha256"] = digest(learner)
        register(self.repo, "cycle-evidence", learner, self.meta("learner"),
                 reviewer, self.meta("reviewer"))

    def test_cycle_cannot_freeze_training_evidence_on_main(self):
        self.git("branch", "-M", "main")
        with self.assertRaises(FactoryError):
            freeze_evidence(self.repo, "cycle-main", self.training_runs)

    def test_fixture_outer_agents_cannot_authorize_factory_change(self):
        _, learner, reviewer = self.bound_docs("cycle-fixture")
        bad = self.meta("reviewer"); bad["harness"] = "fixture"
        with self.assertRaises(FactoryError):
            register(self.repo, "cycle-fixture", learner, self.meta("learner"), reviewer, bad)

    def test_evidence_manifest_freezes_only_safe_active_change_surface(self):
        evidence = freeze_evidence(self.repo, "cycle-surface", self.training_runs)
        self.assertIn("prompts/chapter-writer.md", evidence["eligible_change_surface"])
        self.assertNotIn("scripts/bc_factory/learning.py", evidence["eligible_change_surface"])
        self.assertNotIn("loop/judges/pairwise.md", evidence["eligible_change_surface"])
        self.assertNotIn("README.md", evidence["eligible_change_surface"])

    def test_non_runtime_intervention_cannot_be_registered(self):
        learner = self.learner()
        learner["proposed_factory_change"]["change_surface"] = ["README.md"]
        review = self.reviewer()
        review["approved_change_surface"] = ["README.md"]
        _, learner, review = self.bound_docs("cycle-nonruntime", learner, review)
        with self.assertRaises(FactoryError):
            register(self.repo, "cycle-nonruntime", learner, self.meta("learner"),
                     review, self.meta("reviewer"))

    def test_self_optimizer_cannot_edit_learning_or_evaluation_control_plane(self):
        learner = self.learner()
        learner["proposed_factory_change"]["change_surface"] = ["scripts/bc_factory/learning.py"]
        review = self.reviewer()
        review["approved_change_surface"] = ["scripts/bc_factory/learning.py"]
        _, learner, review = self.bound_docs("cycle-score", learner, review)
        with self.assertRaises(FactoryError):
            register(self.repo, "cycle-score", learner, self.meta("learner"),
                     review, self.meta("reviewer"))

    def test_reviewed_change_freezes_before_independent_holdout_selection(self):
        evidence, _, _ = self.register_cycle("cycle-1")
        with self.assertRaises(FactoryError):
            submit_holdout(self.repo, "cycle-1",
                           {"schema_version": 2, "subjects": ["held-a", "held-b"], "rationale": "unseen"},
                           self.meta("selector"))
        p = self.repo / "prompts/chapter-writer.md"
        p.write_text(p.read_text() + "\n<!-- fixture intervention -->\n")
        self.git("add", "prompts/chapter-writer.md"); self.git("commit", "-m", "intervention")
        change = freeze_change(self.repo, "cycle-1")
        self.assertEqual(change["changed_paths"], ["prompts/chapter-writer.md"])
        self.assertNotEqual(change["factory_digest"], evidence["base_factory_digest"])
        with self.assertRaises(FactoryError):
            submit_holdout(self.repo, "cycle-1",
                           {"schema_version": 2, "subjects": ["train-a", "held-b"], "rationale": "bad overlap"},
                           self.meta("selector"))
        result = submit_holdout(self.repo, "cycle-1",
                                {"schema_version": 2, "subjects": ["held-a", "held-b"],
                                 "rationale": "Selected after freeze to satisfy the generic transfer criteria."},
                                self.meta("selector"))
        self.assertEqual(result["selection"]["subjects"], ["held-a", "held-b"])

    def test_reviewer_and_selector_must_be_independent(self):
        evidence, learner, reviewer = self.bound_docs("cycle-bad")
        with self.assertRaises(FactoryError):
            register(self.repo, "cycle-bad", learner, self.meta("same"),
                     reviewer, self.meta("same"))
        self.register_cycle("cycle-2")
        p = self.repo / "prompts/chapter-writer.md"
        p.write_text(p.read_text() + "\n<!-- fixture intervention -->\n")
        self.git("add", "prompts/chapter-writer.md"); self.git("commit", "-m", "intervention")
        freeze_change(self.repo, "cycle-2")
        with self.assertRaises(FactoryError):
            submit_holdout(self.repo, "cycle-2",
                           {"schema_version": 2, "subjects": ["held-c", "held-d"], "rationale": "unseen"},
                           self.meta("learner"))

    def test_change_surface_is_enforced_from_git_diff(self):
        self.register_cycle("cycle-3")
        p = self.repo / "prompts/chapter-reviewer.md"
        p.write_text(p.read_text() + "\n<!-- undeclared change -->\n")
        self.git("add", "prompts/chapter-reviewer.md"); self.git("commit", "-m", "bad intervention")
        with self.assertRaises(FactoryError):
            freeze_change(self.repo, "cycle-3")


if __name__ == "__main__":
    unittest.main()
