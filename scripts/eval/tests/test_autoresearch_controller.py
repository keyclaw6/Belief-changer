"""Offline normal-entrypoint checks; mocked transport is not live commissioning proof."""
from __future__ import annotations

import contextlib
import copy
import io
import json
import os
from pathlib import Path
import shutil
from subprocess import CompletedProcess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from bc_autoresearch import cli, controller, evaluation, learning, operations, regression
from bc_factory.common import FactoryError, atomic_json, digest, file_hash, read_json, unseal
from bc_factory.demo import finish, inputs, scaffold
from bc_factory.runs import Run, prepare
from bc_factory.schema import DIMENSIONS


class AutoResearchControllerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name) / "repo"
        scaffold(ROOT, self.repo)
        for relative in ("loop/judges/pairwise.md", "loop/prompts/factory-learner.md",
                         "loop/prompts/factory-learning-reviewer.md"):
            path = self.repo / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, path)
        self.brief, self.research, self.plan = inputs()
        self.research["sources"][0]["verification"] = "retrieved"
        self.baseline = self.completed("baseline")
        learning.seed(self.repo, "baseline", {
            "schema_version": 2, "subject": self.brief["subject"],
            "preserve": [{"dimension": "argument", "instruction": "Preserve bounded inference.",
                          "evidence": "Synthetic fixture only."}],
            "improve": [], "recurring_repairs": [], "research_gaps": [],
            "note": "Offline software fixture; no reader-effectiveness claim."})
        self.candidate = self.completed("iter901-candidate", "baseline")
        self.progress("901")
        self.campaign_path = self.repo / "loop/commissioning.json"
        self.save_campaign(["901", "902"])
        atomic_json(self.repo / ".loop-work/deployment.json", {
            "controller": "/synthetic/controller", "outer_model": "gpt-6.1-sol",
            "pi": "/synthetic/pi", "agent_dir": "/synthetic/agents", "env_file": "/synthetic/credentials"})

    def completed(self, name, baseline=None, fixture=False):
        brief, plan = copy.deepcopy(self.brief), copy.deepcopy(self.plan)
        brief["title"] = plan["title"] = f"{name} (OFFLINE SOFTWARE FIXTURE)"
        context = unseal(learning.context_path(Run(self.repo, baseline))) if baseline else None
        # Temporary synthetic envelopes exercise production trust guards. These
        # mocked access checks and marked stage metadata are not live evidence.
        with patch("bc_factory.research_access.validate_preflight"), patch("bc_factory.research_access.validate_coverage"):
            prepare(self.repo, name, brief, self.research, fixture=fixture, caller_context=context)
        run = Run(self.repo, name)
        if fixture:
            finish(run, plan)
        else:
            def stage_metadata(external=False):
                profile = run.config["profiles"]["external" if external else "factory"]
                route = profile["routes"][0]
                return {"model": route["model"], "family": profile["family"], "route": route["name"],
                        "harness": "offline-test-envelope", "usage": None, "latency_s": 0}
            with patch("bc_factory.demo.metadata", side_effect=stage_metadata):
                finish(run, plan)
        return run

    def progress(self, iteration):
        root = self.repo / "loop/iterations" / iteration
        root.mkdir(parents=True, exist_ok=True)
        (root / "hypothesis.md").write_text("Offline lifecycle fixture; no real experimental inference.")
        data = {"schema_version": 1, "iteration": iteration, "execution_status": "ACTIVE",
                "preregistration_sha256": file_hash(root / "hypothesis.md"),
                "allocation": {self.brief["subject"]: 1}, "excluded_runs": [],
                "authorization": {"status": "APPROVED", "reference": "offline-test-fixture",
                                  "quote": "Synthetic software checks only; no paid calls."}}
        data["authorization"]["scope_sha256"] = operations.scope_digest(data)
        atomic_json(root / "progress.json", data)

    def save_campaign(self, iterations):
        plan = {"workload": "Offline synthetic controller tests", "models": "Configured routes only",
                "subject": self.brief["subject"], "books_per_cycle": 1}
        data = {"id": "offline-controller", "execution_status": "ACTIVE", "iterations": iterations,
                "plan": plan, "completed": [], "controller_started": False,
                "authorization": {"reference": "offline-test-fixture", "quote": "No real model calls.",
                                  "scope_sha256": digest({"iterations": iterations, "plan": plan})}}
        atomic_json(self.campaign_path, data)

    @staticmethod
    def judgment(voice="tie"):
        quote = "One unsuccessful attempt is one observation."
        return {"schema_version": 2, "preferences": {
            dimension: {"winner": voice if dimension == "voice" else "tie", "a_quote": quote,
                        "b_quote": quote, "reason": "Synthetic fixture comparison."}
            for dimension in DIMENSIONS}, "critical": {"A": [], "B": []}}

    @staticmethod
    def learner():
        return {"schema_version": 2, "decision": "MEASURE_MORE",
                "observations": ["Both blinded orders tied in this synthetic fixture."],
                "candidate_root_causes": [], "subject_specific_lessons": [],
                "transferable_factory_lessons": [], "protected_strengths": [],
                "proposed_factory_change": {"hypothesis": "No change justified.", "change_surface": [],
                    "smallest_change": "None", "expected_transfer": "Unmeasured", "possible_regressions": []},
                "falsification_test": {"training_subjects": ["practice-belief"], "holdout_requirements": [],
                    "success_criteria": [], "failure_signals": [], "leakage_rule": "No tuning or transfer claim."},
                "confidence": "low", "reasoning_summary": "Fixture data justify no factory intervention."}

    @staticmethod
    def review():
        checks = ("transferable", "not_subject_overfit", "causal_honesty", "minimal_change",
                  "protected_strengths", "held_out_integrity", "judge_overfit_control", "falsifiable")
        return {"schema_version": 2, "verdict": "MEASURE_MORE", "checks": {key: True for key in checks},
                "findings": [], "approved_change_surface": [], "held_out_test": {
                    "holdout_requirements": [], "success_criteria": [], "failure_signals": []},
                "reasoning_summary": "No change or transfer claim is warranted from a software fixture."}

    @contextlib.contextmanager
    def transport(self, outputs):
        pending, seen = iter(outputs), []
        def respond(request, timeout=None):
            payload = json.loads(request.data)
            seen.append({"url": request.full_url, "payload": payload})
            output = next(pending)
            body = {"model": payload["model"], "usage": {"total_tokens": 1}}
            if request.full_url.endswith("/responses"):
                body.update({"status": "completed", "output_text": json.dumps(output)})
            else:
                body["choices"] = [{"finish_reason": "stop", "message": {"content": json.dumps(output)}}]
            return io.BytesIO(json.dumps(body).encode())
        with patch.dict(os.environ, {"OPENCODE_GO_API_KEY": "synthetic-test-key"}):
            with patch("urllib.request.urlopen", side_effect=respond):
                yield seen

    def invoke(self, command, *args):
        with contextlib.redirect_stdout(io.StringIO()) as output, contextlib.redirect_stderr(io.StringIO()) as error:
            code = cli.main(["--repo", str(self.repo), command, *args])
        return code, json.loads(output.getvalue()) if output.getvalue() else None, error.getvalue()

    def comparisons(self, candidate=None, voices=("tie", "tie")):
        candidate = candidate or self.candidate
        with self.transport([self.judgment(voice) for voice in voices]) as calls:
            for order in ("AB", "BA"):
                code, result, error = self.invoke("regression-execute", "--run", candidate.root.name,
                    "--baseline", "baseline", "--order", order, "--allow-paid")
                self.assertEqual(code, 0, error)
                self.assertEqual(result["status"], "RECORDED")
        self.assertEqual(len(calls), 2)
        return calls

    def retain_learning(self, iteration="901", candidate=None):
        candidate = candidate or self.candidate
        with self.transport([self.learner(), self.review()]) as calls:
            code, result, error = self.invoke("learn", "--iteration", iteration, "--run", candidate.root.name,
                                            "--baseline", "baseline", "--allow-paid")
            self.assertEqual(code, 0, error)
        self.assertEqual(result["review"], "MEASURE_MORE")
        return calls

    def test_normal_comparisons_use_both_orders_and_replay_without_calls(self):
        calls = self.comparisons()
        self.assertEqual([row["payload"]["model"] for row in calls], ["deepseek-v4.1-flash"] * 2)
        self.assertEqual(regression.decide(self.repo, self.candidate.root.name, "baseline")["decision"],
                         "PRESERVE_BASELINE")
        saved = {p.name: p.read_bytes() for p in (self.candidate.root / "regression/judgments").glob("*.json")}
        with patch("urllib.request.urlopen") as provider:
            for order in ("AB", "BA"):
                code, _, error = self.invoke("regression-execute", "--run", self.candidate.root.name,
                                             "--baseline", "baseline", "--order", order)
                self.assertEqual(code, 0, error)
            provider.assert_not_called()
        for path in (self.candidate.root / "regression/judgments").glob("*.json"):
            self.assertEqual(path.read_bytes(), saved[path.name])

    def test_order_disagreement_remains_honestly_inconclusive(self):
        self.comparisons(voices=("B", "B"))
        code, result, error = self.invoke("regression-decide", "--run", self.candidate.root.name,
                                         "--baseline", "baseline")
        self.assertEqual(code, 2, error)
        self.assertEqual(result["decision"], "INCONCLUSIVE")
        self.assertIn("voice", result["order_instability"])
        self.assertFalse(learning.learning_path(self.candidate).exists())

    def test_missing_judgment_invalidates_cached_decision_and_learning(self):
        self.comparisons()
        regression.decide(self.repo, self.candidate.root.name, "baseline")
        regression.judgment_path(self.candidate, 1, "BA").unlink()
        with patch("urllib.request.urlopen") as provider:
            code, _, error = self.invoke("learn", "--iteration", "901", "--run", self.candidate.root.name,
                                         "--baseline", "baseline", "--allow-paid")
            self.assertEqual(code, 2)
            self.assertIn("missing its judgment evidence", error)
            provider.assert_not_called()

    def test_cached_comparison_rejects_wrong_model_identity(self):
        self.comparisons()
        path = regression.judgment_path(self.candidate, 1, "AB")
        changed = unseal(path)
        changed["metadata"]["model"] = "unconfigured-independent-model"
        atomic_json(path, {"payload": changed, "sha256": digest(changed)})
        with patch("urllib.request.urlopen") as provider:
            code, _, error = self.invoke("regression-execute", "--run", self.candidate.root.name,
                                         "--baseline", "baseline", "--order", "AB")
            self.assertEqual(code, 2)
            self.assertIn("frozen profile", error)
            provider.assert_not_called()

    def test_corrupt_comparison_cannot_be_replayed(self):
        self.comparisons()
        path = regression.judgment_path(self.candidate, 1, "AB")
        changed = read_json(path)
        changed["payload"]["output"]["preferences"]["voice"]["winner"] = "A"
        atomic_json(path, changed)
        with patch("urllib.request.urlopen") as provider:
            code, _, error = self.invoke("regression-execute", "--run", self.candidate.root.name,
                                         "--baseline", "baseline", "--order", "AB")
            self.assertEqual(code, 2)
            self.assertIn("Checksum mismatch", error)
            provider.assert_not_called()

    def test_learning_review_binds_exact_proposal_and_independent_routes(self):
        self.comparisons()
        calls = self.retain_learning()
        self.assertEqual([row["payload"]["model"] for row in calls],
                         ["muse-spark-1.3-contributor", "deepseek-v4.1-flash"])
        root = self.repo / "loop/iterations/901/learning"
        proposal = unseal(root / "factory-learner.json")
        review_task = unseal(root / "factory-learning-reviewer-task.json")
        self.assertEqual(review_task["inputs"]["learner_proposal"], proposal["output"])
        self.assertEqual(unseal(root / "factory-learning-reviewer.json")["task_sha256"], digest(review_task))
        before = {path.name: path.read_bytes() for path in root.glob("*.json")}
        with patch("urllib.request.urlopen") as provider:
            code, result, error = self.invoke("learn", "--iteration", "901", "--run", self.candidate.root.name,
                                             "--baseline", "baseline")
            self.assertEqual(code, 0, error)
            self.assertEqual(result["review"], "MEASURE_MORE")
            provider.assert_not_called()
        self.assertEqual(before, {path.name: path.read_bytes() for path in root.glob("*.json")})

    def test_learning_unknown_fields_and_invalid_boolean_fail_without_review(self):
        self.comparisons()
        output = self.learner()
        output["unexpected_control"] = "change the model"
        with self.transport([output]) as calls:
            code, _, error = self.invoke("learn", "--iteration", "901", "--run", self.candidate.root.name,
                                         "--baseline", "baseline", "--allow-paid")
            self.assertEqual(code, 2)
            self.assertIn("unexpected_control", error)
        self.assertEqual(len(calls), 1)
        self.assertFalse((self.repo / "loop/iterations/901/learning/factory-learning-reviewer.json").exists())
        reviewer = self.review()
        reviewer["checks"]["causal_honesty"] = "true"
        with self.assertRaisesRegex(FactoryError, "booleans"):
            evaluation.validate_learning("factory-learning-reviewer", reviewer)

    def test_changed_learning_prompt_cannot_reuse_saved_evidence(self):
        self.comparisons()
        self.retain_learning()
        path = self.repo / "loop/prompts/factory-learner.md"
        path.write_text(path.read_text() + "\nDifferent assigned task.\n")
        with patch("urllib.request.urlopen") as provider:
            code, _, error = self.invoke("learn", "--iteration", "901", "--run", self.candidate.root.name,
                                         "--baseline", "baseline", "--allow-paid")
            self.assertEqual(code, 2)
            self.assertIn("Immutable record", error)
            provider.assert_not_called()

    def test_two_synthetic_envelope_cycles_checkpoint_and_stop_at_boundary(self):
        self.comparisons()
        self.retain_learning()
        first = controller.checkpoint(self.repo, "901", self.candidate.root.name, "baseline")
        self.assertEqual(first["decision"], "PRESERVE_BASELINE")
        self.assertEqual(read_json(self.campaign_path)["execution_status"], "ACTIVE")
        following = self.completed("iter902-following", "baseline")
        self.progress("902")
        self.comparisons(following)
        self.retain_learning("902", following)
        second = controller.checkpoint(self.repo, "902", following.root.name, "baseline")
        self.assertNotEqual(first["book_sha256"], second["book_sha256"])
        data = read_json(self.campaign_path)
        self.assertEqual(data["execution_status"], "COMPLETE")
        self.assertEqual([record["iteration"] for record in data["completed"]], ["901", "902"])
        with patch.object(controller, "native") as native, patch("urllib.request.urlopen") as provider:
            self.assertEqual(controller.status(self.repo)["execution_status"], "COMPLETE")
            self.assertEqual(controller.lifecycle(self.repo, "stop")["execution_status"], "COMPLETE")
            self.assertEqual(read_json(self.campaign_path)["execution_status"], "COMPLETE")
            with self.assertRaisesRegex(FactoryError, "Campaign complete"):
                controller.lifecycle(self.repo, "resume")
            with self.assertRaisesRegex(FactoryError, "cannot advance"):
                controller.checkpoint(self.repo, "902", following.root.name, "baseline")
            native.assert_not_called()
            provider.assert_not_called()
            # Stop-label changes cannot renew an exhausted scientific allocation.
            data["execution_status"] = "STOPPED"
            atomic_json(self.campaign_path, data)
            with self.assertRaisesRegex(FactoryError, "Campaign complete"):
                controller.lifecycle(self.repo, "resume")
            native.assert_not_called()

    def test_negative_measurement_checkpoint_preserves_loss_and_baseline(self):
        baseline_files = {p.relative_to(self.baseline.root): p.read_bytes()
                          for p in self.baseline.root.rglob("*") if p.is_file()}
        self.comparisons(voices=("A", "B"))  # Baseline wins in both orders.
        decision = regression.decide(self.repo, self.candidate.root.name, "baseline")
        self.assertEqual(decision["decision"], "REPAIR_REQUIRED")
        self.retain_learning()
        with patch("urllib.request.urlopen") as provider:
            record = controller.checkpoint(self.repo, "901", self.candidate.root.name, "baseline")
            provider.assert_not_called()
        self.assertEqual(record["decision"], "REPAIR_REQUIRED")
        self.assertEqual(read_json(self.campaign_path)["completed"][0]["decision"], "REPAIR_REQUIRED")
        self.assertEqual(read_json(self.campaign_path)["execution_status"], "ACTIVE")
        for rel, content in baseline_files.items():
            self.assertEqual((self.baseline.root / rel).read_bytes(), content, str(rel))
        # A negative comparative result cannot excuse missing factory acceptance.
        (self.candidate.root / "results/final-auditor-r01.json").unlink()
        with self.assertRaises(FactoryError):
            controller.validate_checkpoints(self.repo, read_json(self.campaign_path))

    def test_fixture_book_cannot_count_toward_live_commissioning(self):
        data = read_json(self.campaign_path)
        data["iterations"] = ["903"]
        data["authorization"]["scope_sha256"] = digest({"iterations": data["iterations"], "plan": data["plan"]})
        atomic_json(self.campaign_path, data)
        self.progress("903")
        fixture = self.completed("iter903-fixture", fixture=True)
        with self.assertRaisesRegex(FactoryError, "synthetic fixture cycles"):
            controller.checkpoint(self.repo, "903", fixture.root.name, "baseline")
        self.assertEqual(read_json(self.campaign_path)["completed"], [])

    def test_owner_stop_persists_and_cancels_even_when_book_evidence_is_missing(self):
        self.comparisons()
        self.retain_learning()
        controller.checkpoint(self.repo, "901", self.candidate.root.name, "baseline")
        (self.candidate.root / "book.md").unlink()
        data = read_json(self.campaign_path)
        data["controller_started"] = True
        atomic_json(self.campaign_path, data)
        calls = []
        def native(settings, *args):
            calls.append(args)
            if args[0] == "kill":
                self.assertEqual(read_json(self.campaign_path)["execution_status"], "STOPPED")
                return {"state": "finished"}
            return {"state": "finished" if any(call[0] == "kill" for call in calls) else "running"}
        with patch.object(controller, "native", side_effect=native), patch("urllib.request.urlopen") as provider:
            result = controller.lifecycle(self.repo, "stop")
            self.assertEqual(result["execution_status"], "STOPPED")
            self.assertEqual([call[0] for call in calls], ["status", "kill", "status"])
            provider.assert_not_called()

    def test_start_duplicate_is_noop_and_owner_stop_requires_explicit_resume(self):
        data = read_json(self.campaign_path)
        data["controller_started"] = True
        atomic_json(self.campaign_path, data)
        active = {"state": "running", "survives_origin": True, "run": 1, "backend": "codex"}
        with patch.object(controller, "native", return_value=active) as native:
            self.assertEqual(controller.lifecycle(self.repo, "start")["execution_status"], "ACTIVE")
            self.assertTrue(all(call.args[1] == "status" for call in native.call_args_list))
        data["execution_status"] = "STOPPED"
        atomic_json(self.campaign_path, data)
        with patch.object(controller, "native", return_value={"state": "finished", "run": 1, "backend": "codex"}):
            with self.assertRaisesRegex(FactoryError, "Owner stop"):
                controller.lifecycle(self.repo, "start")
            calls = []
            def resumed(settings, *args):
                calls.append(args)
                return {"state": "finished", "run": 1, "backend": "codex"} if args[0] == "status" else {
                    "state": "running", "survives_origin": True, "run": 2, "backend": "codex"}
            with patch.object(controller, "native", side_effect=resumed):
                self.assertEqual(controller.lifecycle(self.repo, "resume")["execution_status"], "ACTIVE")
            self.assertEqual([call[0] for call in calls], ["status", "follow"])

    def test_non_codex_native_owner_cannot_clear_stop_or_be_resumed(self):
        data = read_json(self.campaign_path)
        data["controller_started"] = True
        data["execution_status"] = "STOPPED"
        atomic_json(self.campaign_path, data)
        before = self.campaign_path.read_bytes()
        for state in ("finished", "running"):
            with self.subTest(state=state):
                receipt = {"state": state, "run": 1, "backend": "command", "survives_origin": True}
                with patch.object(controller, "native", return_value=receipt) as native:
                    code, _, error = self.invoke("resume", "--allow-paid")
                    self.assertEqual(code, 2)
                    self.assertIn("Codex backend", error)
                    self.assertTrue(all(call.args[1] == "status" for call in native.call_args_list))
                self.assertEqual(self.campaign_path.read_bytes(), before)

    def test_failed_codex_follow_preserves_stop_and_same_owner_resume_point(self):
        data = read_json(self.campaign_path)
        data["controller_started"] = True
        data["execution_status"] = "STOPPED"
        atomic_json(self.campaign_path, data)
        calls = []
        def native(settings, *args):
            calls.append(args)
            if args[0] == "status":
                return {"state": "finished", "run": 1, "backend": "codex"}
            raise FactoryError("Synthetic follow dispatch failure")
        with patch.object(controller, "native", side_effect=native), patch("urllib.request.urlopen") as provider:
            code, _, error = self.invoke("resume", "--allow-paid")
            self.assertEqual(code, 2)
            self.assertIn("dispatch failure", error)
            self.assertEqual([call[0] for call in calls], ["status", "follow"])
            self.assertEqual(calls[0][1], calls[1][1])
            provider.assert_not_called()
        after = read_json(self.campaign_path)
        self.assertEqual(after["execution_status"], "STOPPED")
        self.assertIn("same job belief-changer-offline-controller", after["next_action"])
        self.assertTrue(after["controller_started"])

    def test_malformed_native_follow_receipt_preserves_stop_and_same_job(self):
        data = read_json(self.campaign_path)
        data["controller_started"] = True
        data["execution_status"] = "STOPPED"
        atomic_json(self.campaign_path, data)
        def subprocess_result(args, **kwargs):
            body = json.dumps({"state": "finished", "run": 1, "backend": "codex"}) if args[1] == "status" else '{"malformed"'
            return CompletedProcess(args, 0, stdout=body, stderr="")
        with patch.object(controller.subprocess, "run", side_effect=subprocess_result) as native_process:
            with patch("urllib.request.urlopen") as provider:
                code, _, error = self.invoke("resume", "--allow-paid")
                self.assertEqual(code, 2)
                self.assertIn("invalid receipt", error)
                provider.assert_not_called()
        commands = [call.args[0] for call in native_process.call_args_list]
        self.assertEqual([args[1] for args in commands], ["status", "follow"])
        self.assertEqual(commands[0][2], commands[1][2])
        after = read_json(self.campaign_path)
        self.assertEqual(after["execution_status"], "STOPPED")
        self.assertIn("same job belief-changer-offline-controller", after["next_action"])
        self.assertTrue(after["controller_started"])

    def test_stop_intent_survives_unavailable_native_receipt(self):
        data = read_json(self.campaign_path)
        data["controller_started"] = True
        atomic_json(self.campaign_path, data)
        with patch.object(controller, "native", side_effect=FactoryError("Synthetic native status failure")):
            code, _, _ = self.invoke("stop")
        self.assertEqual(code, 2, "Unavailable cancellation must not masquerade as a successful stop")
        self.assertEqual(read_json(self.campaign_path)["execution_status"], "STOPPED")

    def test_owner_stop_cancels_despite_stale_campaign_plan(self):
        data = read_json(self.campaign_path)
        data["controller_started"] = True
        data["plan"]["workload"] = "Stale changed plan with its original scope hash"
        atomic_json(self.campaign_path, data)
        calls = []
        def native(settings, *args):
            calls.append(args)
            self.assertEqual(read_json(self.campaign_path)["execution_status"], "STOPPED")
            return {"state": "finished" if len(calls) > 1 else "running"}
        with patch.object(controller, "native", side_effect=native), patch("urllib.request.urlopen") as provider:
            code, result, error = self.invoke("stop")
            self.assertEqual(code, 0, error)
            self.assertEqual(result["execution_status"], "STOPPED")
            self.assertEqual([call[0] for call in calls], ["status", "kill", "status"])
            provider.assert_not_called()
        stopped = read_json(self.campaign_path)
        self.assertEqual(stopped["plan"], data["plan"])
        self.assertEqual(stopped["authorization"], data["authorization"])

    def test_status_keeps_owner_visible_when_checkpoint_evidence_is_invalid(self):
        self.comparisons()
        self.retain_learning()
        controller.checkpoint(self.repo, "901", self.candidate.root.name, "baseline")
        (self.candidate.root / "book.md").unlink()
        data = read_json(self.campaign_path)
        data["controller_started"] = True
        atomic_json(self.campaign_path, data)
        before = self.campaign_path.read_bytes()
        owner = {"state": "running", "survives_origin": True, "session_id": "offline-owned-session"}
        with patch.object(controller, "native", return_value=owner) as native, patch("urllib.request.urlopen") as provider:
            code, result, error = self.invoke("status")
            self.assertEqual(code, 0, error)
            self.assertEqual(result["owner"], owner)
            self.assertEqual(result["evidence"]["status"], "INVALID")
            self.assertTrue(result["evidence"]["error"])
            native.assert_called_once()
            self.assertEqual(native.call_args.args[1:], ("status", "belief-changer-offline-controller"))
            provider.assert_not_called()
        self.assertEqual(self.campaign_path.read_bytes(), before)
        self.assertFalse((self.candidate.root / "book.md").exists())

    def test_changed_campaign_scope_is_rejected_before_native_execution(self):
        data = read_json(self.campaign_path)
        data["controller_started"] = True
        data["plan"]["workload"] = "Expanded workload without matching authority"
        atomic_json(self.campaign_path, data)
        before = self.campaign_path.read_bytes()
        owner = {"state": "running", "backend": "codex", "survives_origin": True}
        with patch.object(controller, "native", return_value=owner) as native, patch("urllib.request.urlopen") as provider:
            code, _, error = self.invoke("start", "--allow-paid")
            self.assertEqual(code, 2)
            self.assertIn("Campaign scope changed", error)
            native.assert_not_called()
            code, result, error = self.invoke("status")
            self.assertEqual(code, 0, error)
            self.assertEqual(result["owner"], owner)
            self.assertEqual(result["evidence"]["status"], "INVALID")
            self.assertIn("Campaign scope changed", result["evidence"]["error"])
            native.assert_called_once()
            provider.assert_not_called()
        self.assertEqual(self.campaign_path.read_bytes(), before)

    def test_freeze_iteration_persists_host_hypothesis_and_authorized_scope(self):
        shutil.rmtree(self.repo / "loop/iterations/901")
        supplied = self.repo / "declared-measurement.md"
        supplied.write_text("Host-declared measurement: retain an honest tie; make no change claim.")
        with patch.object(controller, "native") as native, patch("urllib.request.urlopen") as provider:
            code, result, error = self.invoke("freeze-iteration", "--iteration", "901", "--hypothesis", str(supplied))
            self.assertEqual(code, 0, error)
            self.assertEqual(result["allocation"], {self.brief["subject"]: 1})
            self.assertEqual(result["authorization"]["scope_sha256"], operations.scope_digest(result))
            self.assertEqual((self.repo / "loop/iterations/901/hypothesis.md").read_bytes(), supplied.read_bytes())
            code, repeated, error = self.invoke("freeze-iteration", "--iteration", "901", "--hypothesis", str(supplied))
            self.assertEqual(code, 0, error)
            self.assertEqual(repeated, result)
            supplied.write_text("Different hypothesis after the freeze.")
            code, _, error = self.invoke("freeze-iteration", "--iteration", "901", "--hypothesis", str(supplied))
            self.assertEqual(code, 2)
            self.assertIn("cannot be overwritten", error)
            code, _, error = self.invoke("freeze-iteration", "--iteration", "902", "--hypothesis", str(supplied))
            self.assertEqual(code, 2)
            self.assertIn("next authorized cycle", error)
            native.assert_not_called()
            provider.assert_not_called()

    def test_cached_fixture_learning_cannot_enter_live_envelope(self):
        self.comparisons()
        self.retain_learning()
        path = self.repo / "loop/iterations/901/learning/factory-learning-reviewer.json"
        saved = unseal(path)
        saved["metadata"]["harness"] = "fixture"
        atomic_json(path, {"payload": saved, "sha256": digest(saved)})
        with patch("urllib.request.urlopen") as provider:
            code, _, error = self.invoke("learn", "--iteration", "901", "--run", self.candidate.root.name,
                                         "--baseline", "baseline")
            self.assertEqual(code, 2)
            self.assertIn("Synthetic learning", error)
            provider.assert_not_called()


if __name__ == "__main__":
    unittest.main()
