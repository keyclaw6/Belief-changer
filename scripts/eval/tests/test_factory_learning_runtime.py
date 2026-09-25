"""Offline tests for the sealed outer factory-learning state machine."""
from __future__ import annotations

import copy
import shutil
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SOURCE / "scripts"))

from bc_factory.common import FactoryError, digest, now, seal, unseal
from bc_factory.demo import finish, inputs, scaffold
from bc_factory.factory_learning import (bind_experiment, decide as learning_decide, freeze_change,
                                         freeze_evidence, prepare_arm, register, submit_holdout)
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

    def commit_holdout_registry(self):
        self.git("add", "loop/holdout-registry")
        self.git("commit", "-m", "retire held-out topics")

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
        for rel in ("AGENTS.md", "loop/PROGRAM.md", "docs/FACTORY-V2.md",
                    "loop/prompts/factory-learner.md", "loop/prompts/factory-learning-reviewer.md",
                    ".opencode/agents/factory-learner.md", "scripts/bc_factory/learning.py",
                    "scripts/bc_factory/factory_learning.py"):
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
        self.assertNotIn("prompts/research-agent.md", evidence["eligible_change_surface"])
        self.assertNotIn("scripts/bc_factory/quality.py", evidence["eligible_change_surface"])
        self.assertTrue(all(path.startswith("prompts/") for path in evidence["eligible_change_surface"]))
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
        selection = {"schema_version": 2, "subjects": ["held-a", "held-b"],
                     "rationale": "Selected after freeze to satisfy the generic transfer criteria."}
        result = submit_holdout(self.repo, "cycle-1", selection, self.meta("selector"))
        self.assertEqual(result["selection"]["subjects"], ["held-a", "held-b"])
        self.commit_holdout_registry()

        p.write_text(p.read_text() + "\n<!-- untested post-holdout mutation -->\n")
        self.git("add", "prompts/chapter-writer.md"); self.git("commit", "-m", "untested post-holdout mutation")
        with self.assertRaises(FactoryError):
            submit_holdout(self.repo, "cycle-1", selection, self.meta("selector"))

    def test_holdout_replay_recovers_missing_tracked_ledger_mirror(self):
        self.register_cycle("cycle-holdout-replay")
        p = self.repo / "prompts/chapter-writer.md"
        p.write_text(p.read_text() + "\n<!-- fixture intervention -->\n")
        self.git("add", "prompts/chapter-writer.md"); self.git("commit", "-m", "intervention")
        freeze_change(self.repo, "cycle-holdout-replay")
        selection = {"schema_version": 2, "subjects": ["replay-a", "replay-b"],
                     "rationale": "Selected after intervention freeze."}
        first = submit_holdout(self.repo, "cycle-holdout-replay", selection, self.meta("selector"))
        ledger = self.repo / first["retirement_record"]
        original = unseal(ledger)
        self.assertEqual(set(original["training_subjects"]), {"train-a", "train-b"})
        ledger.unlink()
        replay = submit_holdout(self.repo, "cycle-holdout-replay", selection, self.meta("selector"))
        self.assertEqual(unseal(ledger), original)
        self.assertEqual(replay["retirement_sha256"], digest(original))
        self.assertTrue(replay["requires_commit"])

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
        with self.assertRaises(FactoryError):
            submit_holdout(self.repo, "cycle-2",
                           {"schema_version": 2, "subjects": ["held-c", "held-d"], "rationale": "unseen"},
                           self.meta("reviewer"))

    def test_heldout_parent_and_candidate_arms_prepare_from_the_two_frozen_factories(self):
        evidence, _, _ = self.register_cycle("cycle-arms")
        prompt = self.repo / "prompts/chapter-writer.md"
        original = prompt.read_text()
        marker = "\n<!-- candidate factory marker -->\n"
        prompt.write_text(original + marker)
        self.git("add", "prompts/chapter-writer.md"); self.git("commit", "-m", "intervention")
        change = freeze_change(self.repo, "cycle-arms")
        submit_holdout(
            self.repo, "cycle-arms",
            {"schema_version": 2, "subjects": ["held-a", "held-b"],
             "rationale": "Selected after the intervention was frozen."},
            self.meta("selector"))
        self.commit_holdout_registry()

        brief, research, plan = inputs("held-a")
        parent_info = prepare_arm(self.repo, "cycle-arms", "parent", "held-a-parent",
                                  brief, research, fixture=True)
        candidate_info = prepare_arm(self.repo, "cycle-arms", "candidate", "held-a-candidate",
                                     brief, research, fixture=True)
        parent = Run(self.repo, "held-a-parent")
        candidate = Run(self.repo, "held-a-candidate")
        self.assertEqual(parent.manifest["brief_sha256"], candidate.manifest["brief_sha256"])
        self.assertEqual(parent.manifest["research_sha256"], candidate.manifest["research_sha256"])
        self.assertEqual(parent.manifest["factory_files"], evidence["base_factory_files"])
        self.assertEqual(candidate.manifest["factory_files"], change["factory_files"])
        self.assertEqual(parent_info["factory_ref"], evidence["base_commit"])
        self.assertEqual(candidate_info["factory_ref"], change["head_commit"])
        self.assertNotIn("candidate factory marker", parent.snapshot("prompts/chapter-writer.md"))
        self.assertIn("candidate factory marker", candidate.snapshot("prompts/chapter-writer.md"))
        # Both frozen arms remain executable because self-optimization cannot alter runtime code.
        finish(parent, plan)
        finish(candidate, plan)
        self.assertEqual(parent.complete()["status"], "COMPLETE_UNRELEASED")
        self.assertEqual(candidate.complete()["status"], "COMPLETE_UNRELEASED")

    def test_transfer_binding_rejects_confounded_or_impossible_designs(self):
        _, learner, _ = self.register_cycle("cycle-bind")
        p = self.repo / "prompts/chapter-writer.md"
        p.write_text(p.read_text() + "\n<!-- fixture intervention -->\n")
        self.git("add", "prompts/chapter-writer.md"); self.git("commit", "-m", "intervention")
        change = freeze_change(self.repo, "cycle-bind")
        submit_holdout(self.repo, "cycle-bind",
                       {"schema_version": 2, "subjects": ["held-a", "held-b"],
                        "rationale": "Selected only after intervention freeze."},
                       self.meta("selector"))
        self.assertTrue(self.git("status", "--porcelain"))
        self.commit_holdout_registry()

        from bc_factory.factory_learning import registration as cycle_registration
        _, cycle = cycle_registration(self.repo, "cycle-bind")

        class FakeRun:
            def __init__(self, *args):
                rid = args[-1]
                candidate = rid.startswith("candidate-")
                files = change["factory_files"] if candidate else cycle["base_factory_files"]
                fdigest = change["factory_digest"] if candidate else cycle["base_factory_digest"]
                self.manifest = {"factory_files": files, "factory_digest": fdigest}

        def spec(*, freeze_research=True, freeze_plan=True, samples=4):
            return {"spec": {
                "subjects": ["held-a", "held-b"],
                "primary_dimension": learner["proposed_factory_change"]["primary_dimension"],
                "allowed_change_paths": ["prompts/chapter-writer.md"],
                "confirmatory": True,
                "freeze_research": freeze_research,
                "freeze_plan": freeze_plan,
                "samples_per_subject": samples,
                "pairs": [
                    {"id": "a", "subject": "held-a", "parent_run": "parent-a", "candidate_run": "candidate-a"},
                    {"id": "b", "subject": "held-b", "parent_run": "parent-b", "candidate_run": "candidate-b"},
                ],
            }}

        with patch("bc_factory.experiments.registration", return_value=(self.repo / "experiments/fake", spec(freeze_research=False))), \
             patch("bc_factory.runs.Run", side_effect=FakeRun):
            with self.assertRaises(FactoryError):
                bind_experiment(self.repo, "cycle-bind", "exp-research")

        with patch("bc_factory.experiments.registration", return_value=(self.repo / "experiments/fake", spec(freeze_plan=False))), \
             patch("bc_factory.runs.Run", side_effect=FakeRun):
            with self.assertRaises(FactoryError):
                bind_experiment(self.repo, "cycle-bind", "exp-plan")

        with patch("bc_factory.experiments.registration", return_value=(self.repo / "experiments/fake", spec(samples=3))), \
             patch("bc_factory.runs.Run", side_effect=FakeRun):
            with self.assertRaises(FactoryError):
                bind_experiment(self.repo, "cycle-bind", "exp-small")

        valid = spec()
        with patch("bc_factory.experiments.registration", return_value=(self.repo / "experiments/fake", valid)), \
             patch("bc_factory.runs.Run", side_effect=FakeRun):
            bound = bind_experiment(self.repo, "cycle-bind", "exp-valid")
        self.assertEqual(bound["experiment_id"], "exp-valid")

        # A cached binding must not bless later untested source changes.
        p.write_text(p.read_text() + "\n<!-- untested post-bind mutation -->\n")
        self.git("add", "prompts/chapter-writer.md"); self.git("commit", "-m", "untested post-bind mutation")
        with patch("bc_factory.experiments.registration", return_value=(self.repo / "experiments/fake", valid)):
            with self.assertRaises(FactoryError):
                bind_experiment(self.repo, "cycle-bind", "exp-valid")

    def test_missing_transfer_panel_is_not_sealed_as_terminal(self):
        self.register_cycle("cycle-decision")
        p = self.repo / "prompts/chapter-writer.md"
        p.write_text(p.read_text() + "\n<!-- fixture intervention -->\n")
        self.git("add", "prompts/chapter-writer.md"); self.git("commit", "-m", "intervention")
        change = freeze_change(self.repo, "cycle-decision")
        holdout = submit_holdout(
            self.repo, "cycle-decision",
            {"schema_version": 2, "subjects": ["held-a", "held-b"],
             "rationale": "Selected after freeze."},
            self.meta("selector"))
        self.commit_holdout_registry()
        fake_exp = {"spec": {"subjects": ["held-a", "held-b"]}}
        root = self.repo / "factory-learning/cycle-decision"
        retirement_path = self.repo / "loop/holdout-registry/cycle-decision.json"
        retirement = unseal(retirement_path)
        retirement_commit = self.git("log", "-1", "--format=%H", "--", "loop/holdout-registry/cycle-decision.json")
        binding = {"schema_version": 2, "cycle_id": "cycle-decision", "experiment_id": "exp",
                   "registration_sha256": digest(fake_exp), "holdout_sha256": digest({k: v for k, v in holdout.items()
                       if k not in ("retirement_record", "retirement_sha256", "requires_commit")}),
                   "holdout_retirement_sha256": digest(retirement),
                   "holdout_retirement_commit": retirement_commit,
                   "change_sha256": digest(change), "bound_at": now()}
        seal(root / "experiment.json", binding)

        incomplete = {"decision": "INCONCLUSIVE", "missing": ["pair-a-AB"],
                      "judge_models": [], "reasons": ["missing"], "subjects": {},
                      "critical": [], "order_instability": [], "fixture": False,
                      "efficacy": "NOT_MEASURED", "release_eligible": False}
        with patch("bc_factory.experiments.transfer_decide", return_value=incomplete):
            first = learning_decide(self.repo, "cycle-decision")
        self.assertFalse(first["terminal"])
        self.assertFalse((root / "decision.json").exists())

        rejected = dict(incomplete)
        rejected.update({"decision": "REJECT_TRANSFER", "missing": [], "reasons": ["measured regression"]})
        with patch("bc_factory.experiments.transfer_decide", return_value=rejected):
            second = learning_decide(self.repo, "cycle-decision")
        self.assertTrue(second["terminal"])
        self.assertTrue((root / "decision.json").exists())
        history_path = self.repo / second["history_record"]
        history = unseal(history_path)
        self.assertEqual(history["decision"], "REJECT_FACTORY_CHANGE")
        self.assertEqual(set(history["holdout_subjects"]), {"held-a", "held-b"})
        self.git("add", "loop/factory-learning-history")
        self.git("commit", "-m", "record terminal factory-learning decision")

        with patch("bc_factory.experiments.registration", return_value=(self.repo / "experiments/exp", fake_exp)):
            cached = learning_decide(self.repo, "cycle-decision")
        self.assertEqual(cached["decision"], "REJECT_FACTORY_CHANGE")
        self.assertFalse(cached["requires_commit"])
        history_path.unlink()
        self.assertIn("loop/factory-learning-history/cycle-decision.json",
                      [line[2:].strip() for line in self.git("status", "--porcelain").splitlines()])
        with patch("bc_factory.experiments.registration", return_value=(self.repo / "experiments/exp", fake_exp)):
            recovered = learning_decide(self.repo, "cycle-decision")
        self.assertTrue(history_path.is_file())
        self.assertEqual(unseal(history_path), history)
        self.assertTrue(recovered["requires_commit"])
        self.git("add", "loop/factory-learning-history")
        self.git("commit", "-m", "restore terminal history mirror")

        # A cached terminal decision must never authorize a later source mutation.
        p.write_text(p.read_text() + "\n<!-- untested post-decision mutation -->\n")
        self.git("add", "prompts/chapter-writer.md"); self.git("commit", "-m", "untested post-decision mutation")
        with patch("bc_factory.experiments.registration", return_value=(self.repo / "experiments/exp", fake_exp)):
            with self.assertRaises(FactoryError):
                learning_decide(self.repo, "cycle-decision")

    def test_committed_holdout_registry_survives_loss_of_local_cycle_state(self):
        self.register_cycle("cycle-retire")
        p = self.repo / "prompts/chapter-writer.md"
        original = p.read_text()
        p.write_text(original + "\n<!-- fixture intervention -->\n")
        self.git("add", "prompts/chapter-writer.md"); self.git("commit", "-m", "intervention")
        freeze_change(self.repo, "cycle-retire")
        submit_holdout(
            self.repo, "cycle-retire",
            {"schema_version": 2, "subjects": ["retired-a", "retired-b"],
             "rationale": "Selected after intervention freeze."},
            self.meta("selector"))
        self.commit_holdout_registry()
        self.assertTrue((self.repo / "loop/holdout-registry/cycle-retire.json").is_file())

        # Simulate loss of ignored local runtime state and restore the production prompt.
        shutil.rmtree(self.repo / "factory-learning/cycle-retire")
        p.write_text(original)
        self.git("add", "prompts/chapter-writer.md"); self.git("commit", "-m", "restore production prompt")

        self.register_cycle("cycle-next")
        p.write_text(original + "\n<!-- next fixture intervention -->\n")
        self.git("add", "prompts/chapter-writer.md"); self.git("commit", "-m", "next intervention")
        freeze_change(self.repo, "cycle-next")
        with self.assertRaises(FactoryError):
            submit_holdout(
                self.repo, "cycle-next",
                {"schema_version": 2, "subjects": ["retired-a", "fresh-b"],
                 "rationale": "Attempted reuse after local state loss."},
                self.meta("selector"))

    def test_change_surface_is_enforced_from_git_diff(self):
        self.register_cycle("cycle-3")
        p = self.repo / "prompts/chapter-reviewer.md"
        p.write_text(p.read_text() + "\n<!-- undeclared change -->\n")
        self.git("add", "prompts/chapter-reviewer.md"); self.git("commit", "-m", "bad intervention")
        with self.assertRaises(FactoryError):
            freeze_change(self.repo, "cycle-3")


if __name__ == "__main__":
    unittest.main()
