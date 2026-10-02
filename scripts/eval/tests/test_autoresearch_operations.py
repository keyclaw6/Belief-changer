"""Offline regressions for the outer handoff and native Pi launch boundary."""
from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from bc_autoresearch import operations as ops
from bc_autoresearch.cli import parser
from bc_factory.common import FactoryError, digest, file_hash


class OperationsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        self.iteration = self.repo / "loop/iterations/901"
        self.iteration.mkdir(parents=True)
        (self.iteration / "hypothesis.md").write_text("OFFLINE TEST: two sugar books, no intervention.\n")
        self.progress = {
            "schema_version": 1, "iteration": "901", "execution_status": "ACTIVE",
            "preregistration_sha256": file_hash(self.iteration / "hypothesis.md"),
            "allocation": {"quit-sugar": 2}, "excluded_runs": [],
            "authorization": {"status": "APPROVED", "reference": "offline-test-fixture",
                              "quote": "Synthetic test approval, not a real campaign authorization."},
        }
        self.progress["authorization"]["scope_sha256"] = ops.scope_digest(self.progress)
        self.save()
        self.config = json.loads((ROOT / "factory/config.json").read_text())
        self.agent = self.repo / "private-pi"
        self.agent.mkdir()
        self.provider = {"providers": {"opencode-go": {
            "baseUrl": "https://opencode.ai/zen/go/v1", "api": "openai-responses",
            "models": [{"id": self.config["profiles"]["factory"]["routes"][0]["model"]}],
        }}}
        self.save_provider()
        self.extension = self.repo / "subagent.ts"
        self.runs = {}
        self.addCleanup(patch.stopall)
        patch.object(ops, "Run", side_effect=lambda repo, run_id: self.runs[run_id]).start()
        self.worker = patch.object(ops, "_pty_run", return_value=0).start()
        self.a = self.add_run("iter901-sugar-a")

    def save(self):
        (self.iteration / "progress.json").write_text(json.dumps(self.progress))

    def save_provider(self):
        (self.agent / "models.json").write_text(json.dumps(self.provider))

    def commissioning(self, status="ACTIVE", iterations=None, completed=None):
        data = {"id": "offline-commissioning", "execution_status": status,
                "iterations": iterations or ["901", "902"],
                "completed": completed or [], "plan": {"subject": "quit-sugar", "books_per_cycle": 1},
                "authorization": {"reference": "offline-test-fixture",
                                  "quote": "Synthetic commissioning boundary, no model execution."}}
        data["authorization"]["scope_sha256"] = digest({"iterations": data["iterations"], "plan": data["plan"]})
        (self.repo / "loop/commissioning.json").write_text(json.dumps(data))
        return data

    def add_run(self, name, subject="quit-sugar", complete=False):
        root = self.repo / "runs" / name
        (root / "snapshot/.pi/agents").mkdir(parents=True)
        (root / "snapshot/.pi/agents/factory-orchestrator.md").write_text("Frozen factory role")
        (root / "snapshot/AGENTS.md").write_text("Frozen factory contract")
        run = Mock(root=root, config=copy.deepcopy(self.config), manifest={"subject": subject})
        run.status.return_value = {"status": "COMPLETE_UNRELEASED" if complete else "INCOMPLETE", "run_id": name}
        run.accepted_audit.return_value = (1, {})
        run.complete.return_value = run.status.return_value
        self.runs[name] = run
        return run

    def plan(self, name="iter901-sugar-a", **kwargs):
        return ops.launch_book(self.repo, "901", name, self.agent, self.extension, sys.executable, **kwargs)

    def test_inspection_has_no_worker_or_session_side_effect(self):
        self.assertEqual(self.plan()["status"], "READY_TO_LAUNCH")
        self.worker.assert_not_called()
        self.assertFalse((self.repo / ".loop-work").exists())

    def test_relative_executable_is_pinned_before_snapshot_chdir(self):
        relative = os.path.relpath(sys.executable)
        for requested in (relative, Path(sys.executable).name):
            with self.subTest(requested=requested), patch.dict(os.environ, {"PATH": str(Path(relative).parent)}):
                plan = ops.launch_plan(self.repo, "901", "iter901-sugar-a", self.agent,
                                       self.extension, requested)
                self.assertTrue(os.path.isabs(plan["argv"][0]))
                self.assertTrue(os.path.samefile(plan["argv"][0], sys.executable))
                self.assertEqual(plan["cwd"], str(self.a.root / "snapshot"))
        self.worker.assert_not_called()

    @unittest.skipUnless(os.name == "posix", "Native executable symlink check")
    def test_pinning_executable_preserves_selected_symlink(self):
        runtime = self.repo / "runtime"
        (runtime / "nested").mkdir(parents=True)
        executable = runtime / "selected-pi"
        executable.symlink_to(sys.executable)
        via = self.repo / "via"
        via.symlink_to(runtime / "nested", target_is_directory=True)
        # Do not resolve the interpreter link or lexically collapse a symlink/.. path.
        for requested in (str(executable), str(via / ".." / "selected-pi")):
            with self.subTest(requested=requested):
                plan = ops.launch_plan(self.repo, "901", "iter901-sugar-a", self.agent,
                                       self.extension, requested)
                self.assertEqual(plan["argv"][0], requested)
                self.assertTrue(os.path.samefile(plan["argv"][0], sys.executable))
        self.worker.assert_not_called()

    def test_same_book_resume_preserves_native_session(self):
        first = self.plan()
        session_dir = Path(first["session_dir"])
        session_dir.mkdir(parents=True)
        session = session_dir / "saved.jsonl"
        content = json.dumps({"type": "session", "id": first["session_id"]}) + "\n"
        session.write_text(content)
        again = self.plan()
        self.assertEqual(again["session_id"], first["session_id"])
        self.assertIn(str(session), again["argv"])
        self.assertEqual(session.read_text(), content)

    def test_damaged_session_records_cannot_be_silently_resumed(self):
        first = self.plan()
        root = Path(first["session_dir"])
        root.mkdir(parents=True)
        session = root / "saved.jsonl"
        header = json.dumps({"type": "session", "id": first["session_id"]}).encode() + b"\n"
        for body in (b'{"type":"message","message":', b'null\n', b'{}\n',
                     b'{"type":"session","id":"another-book"}\n',
                     b'{"type":"message","type":"custom"}\n', b'\xff\n'):
            with self.subTest(body=body):
                original = header + body
                session.write_bytes(original)
                for allow_paid in (False, True):
                    with patch.dict(os.environ, {"OPENCODE_GO_API_KEY": "offline-test-only"}):
                        with self.assertRaisesRegex(FactoryError, "Repair damaged native session"):
                            self.plan(allow_paid=allow_paid)
                    self.assertEqual(session.read_bytes(), original)
        self.worker.assert_not_called()

    def test_valid_session_extensions_and_missing_final_newline_are_preserved(self):
        first = self.plan()
        root = Path(first["session_dir"])
        root.mkdir(parents=True)
        session = root / "saved.jsonl"
        content = (json.dumps({"type": "session", "id": first["session_id"]}) + "\n\n" +
                   json.dumps({"type": "custom-extension-record", "data": {"future_field": True}}))
        session.write_text(content)
        again = self.plan()
        self.assertEqual(again["session_id"], first["session_id"])
        self.assertIn(str(session), again["argv"])
        self.assertEqual(session.read_text(), content)
        self.worker.assert_not_called()

    def test_repaired_session_can_resume_without_changing_scope_or_identity(self):
        first = self.plan()
        root = Path(first["session_dir"])
        root.mkdir(parents=True)
        session = root / "saved.jsonl"
        intact = json.dumps({"type": "session", "id": first["session_id"]}) + "\n"
        progress = (self.iteration / "progress.json").read_bytes()
        session.write_text(intact + '{"type":"message",')
        with self.assertRaisesRegex(FactoryError, "Repair damaged native session"):
            self.plan()
        # Explicit fixture repair from known original bytes, not automatic salvage.
        session.write_text(intact)
        repaired = self.plan()
        self.assertEqual(repaired["status"], "READY_TO_LAUNCH")
        self.assertEqual(repaired["session_id"], first["session_id"])
        self.assertEqual((self.iteration / "progress.json").read_bytes(), progress)
        self.worker.assert_not_called()

    def test_completed_book_history_does_not_block_new_book(self):
        first = self.plan()
        session_dir = Path(first["session_dir"])
        session_dir.mkdir(parents=True)
        session = session_dir / "saved.jsonl"
        session.write_text(json.dumps({"type": "session", "id": first["session_id"]})+"\n")
        original = session.read_bytes()
        self.a.status.return_value["status"] = "COMPLETE_UNRELEASED"
        self.add_run("iter901-sugar-b")
        second = self.plan("iter901-sugar-b")
        self.assertNotEqual(first["session_id"], second["session_id"])
        self.assertEqual(session.read_bytes(), original)
        self.assertEqual(self.plan()["status"], "ALREADY_COMPLETE")

    def test_completed_book_does_not_require_live_runtime_to_verify(self):
        self.a.status.return_value["status"] = "COMPLETE_UNRELEASED"
        (self.agent / "models.json").unlink()
        self.assertEqual(self.plan()["status"], "ALREADY_COMPLETE")
        self.worker.assert_not_called()

    def test_two_prepared_books_do_not_circularly_block_recovery(self):
        self.add_run("iter901-sugar-b")
        self.assertEqual(self.plan()["status"], "READY_TO_LAUNCH")
        self.assertEqual(self.plan("iter901-sugar-b")["status"], "READY_TO_LAUNCH")
        with ops.worker_lock(self.repo, "901"):
            for name in ("iter901-sugar-a", "iter901-sugar-b"):
                with self.assertRaisesRegex(FactoryError, "still owns"):
                    self.plan(name, allow_paid=True)
        self.worker.assert_not_called()

    def test_noop_worker_cannot_claim_pending_caller_repair_complete(self):
        self.a.status.return_value["status"] = "COMPLETE_UNRELEASED"
        root = self.a.root / "caller-feedback"
        root.mkdir()
        (root / "repair-r01.json").write_text("{}")
        with patch.object(ops, "load_caller_repair", return_value={}), patch.dict(os.environ, {"OPENCODE_GO_API_KEY": "offline-test-only"}):
            result = self.plan(allow_paid=True)
        self.assertEqual(result["status"], "NEEDS_INSPECTION")

    def test_bound_caller_repair_can_reopen_same_book(self):
        self.a.status.return_value["status"] = "COMPLETE_UNRELEASED"
        root = self.a.root / "caller-feedback"
        root.mkdir()
        (root / "repair-r01.json").write_text("{}")
        with patch.object(ops, "load_caller_repair", return_value={}) as validate:
            self.assertEqual(self.plan()["status"], "READY_TO_LAUNCH")
            validate.assert_called_once_with(self.a, 1)
        with patch.object(ops, "load_caller_repair", side_effect=FactoryError("stale repair")):
            with self.assertRaisesRegex(FactoryError, "stale repair"):
                self.plan()

    def test_stopped_owner_cannot_be_overridden_by_worker_metadata(self):
        self.progress.update(execution_status="STOPPED", worker={"state": "running", "unit": "missing.service"})
        self.save()
        self.assertEqual(ops.iteration_status(self.repo, "901")["next_action"], "AWAIT_OWNER_RESUME")
        with self.assertRaisesRegex(FactoryError, "Owner stop"):
            self.plan(allow_paid=True)
        self.worker.assert_not_called()

    def test_campaign_stop_and_completion_refuse_direct_book_launch(self):
        original = (self.iteration / "progress.json").read_bytes()
        for state in ("STOPPED", "COMPLETE"):
            with self.subTest(state=state):
                self.commissioning(status=state)
                with self.assertRaisesRegex(FactoryError, "Commissioning stop/completion"):
                    self.plan(allow_paid=True)
                self.assertEqual((self.iteration / "progress.json").read_bytes(), original)
        self.worker.assert_not_called()

    def test_direct_launch_cannot_reopen_checkpointed_or_future_cycle(self):
        self.commissioning(completed=[{"iteration": "901"}])
        with self.assertRaisesRegex(FactoryError, "next authorized commissioning"):
            self.plan(allow_paid=True)
        self.commissioning(iterations=["900", "901"])
        with self.assertRaisesRegex(FactoryError, "next authorized commissioning"):
            self.plan(allow_paid=True)
        self.worker.assert_not_called()

    def test_active_current_cycle_can_launch_but_other_campaign_does_not_govern_it(self):
        self.commissioning()
        self.assertEqual(self.plan()["status"], "READY_TO_LAUNCH")
        self.commissioning(status="STOPPED", iterations=["902", "903"])
        self.assertEqual(self.plan()["status"], "READY_TO_LAUNCH")
        self.worker.assert_not_called()

    def test_direct_launch_validates_the_commissioning_scope(self):
        data = self.commissioning()
        data["plan"]["books_per_cycle"] = 3
        (self.repo / "loop/commissioning.json").write_text(json.dumps(data))
        with self.assertRaisesRegex(FactoryError, "Campaign scope changed"):
            self.plan(allow_paid=True)
        self.worker.assert_not_called()

    def test_next_cycle_requires_the_prior_checkpoint_evidence(self):
        self.commissioning(iterations=["900", "901"],
                           completed=[{"iteration": "900", "run_id": "missing-prior-book"}])
        with self.assertRaisesRegex(FactoryError, "Missing or symlinked file"):
            self.plan(allow_paid=True)
        self.worker.assert_not_called()

    def test_unconfirmed_scope_cannot_launch(self):
        self.progress["authorization"] = {"status": "UNCONFIRMED"}
        self.save()
        with self.assertRaisesRegex(FactoryError, "Confirm the material"):
            self.plan()
        self.worker.assert_not_called()

    def test_approval_needs_actual_source_fields(self):
        for field in ("reference", "quote"):
            with self.subTest(field=field):
                original = self.progress["authorization"].pop(field)
                self.save()
                with self.assertRaises(FactoryError):
                    self.plan()
                self.progress["authorization"][field] = original

    def test_more_books_invalidate_approval(self):
        self.progress["allocation"]["quit-sugar"] = 3
        self.save()
        with self.assertRaisesRegex(FactoryError, "approved scope"):
            self.plan()

    def test_changed_hypothesis_cannot_reuse_approval(self):
        (self.iteration / "hypothesis.md").write_text("Changed subjects or success criteria")
        with self.assertRaisesRegex(FactoryError, "Hypothesis changed"):
            self.plan()
        self.progress["preregistration_sha256"] = file_hash(self.iteration / "hypothesis.md")
        self.save()
        with self.assertRaisesRegex(FactoryError, "approved scope"):
            self.plan()

    def test_oversampling_and_unknown_subject_fail_closed(self):
        self.add_run("iter901-sugar-b", complete=True)
        self.add_run("iter901-sugar-c", complete=True)
        with self.assertRaisesRegex(FactoryError, "exceed"):
            self.plan()
        self.runs["iter901-sugar-c"].manifest["subject"] = "quit-smoking"
        with self.assertRaisesRegex(FactoryError, "subject outside"):
            self.plan()

    def test_explicit_diagnostic_exclusion_does_not_consume_extra_slot(self):
        self.add_run("iter901-sugar-diagnostic")
        self.progress["excluded_runs"] = [{"run_id": "iter901-sugar-diagnostic", "reason": "Offline deterministic failure fixture"}]
        self.save()
        self.assertEqual(self.plan()["status"], "READY_TO_LAUNCH")

    def test_snapshot_and_model_are_pinned_without_outer_context(self):
        p = self.plan()
        self.assertEqual(p["cwd"], str(self.a.root / "snapshot"))
        self.assertIn("--no-context-files", p["argv"])
        self.assertIn("--no-extensions", p["argv"])
        self.assertIn(str(self.a.root / "snapshot/AGENTS.md"), p["argv"])
        self.assertIn("--models", p["argv"])
        self.assertNotIn("loop/state.md", p["argv"][-1])
        self.assertNotIn("running-auto-research-loop", p["argv"][-1])

    def test_wrong_go_routing_and_same_family_fail_closed(self):
        for change in ("endpoint", "family", "absent"):
            with self.subTest(change=change):
                self.a.config = copy.deepcopy(self.config)
                if change == "endpoint":
                    self.a.config["profiles"]["factory"]["routes"][0]["endpoint"] = "https://example.invalid/responses"
                elif change == "family":
                    self.a.config["profiles"]["external"]["family"] = "meta"
                else:
                    self.a.config["profiles"]["external"] = None
                with self.assertRaises(FactoryError):
                    self.plan()

    def test_native_launch_needs_no_extension_and_broken_mapping_is_repairable(self):
        self.assertFalse(self.extension.exists())
        self.assertNotIn("--extension", self.plan()["argv"])
        self.provider["providers"]["opencode-go"]["baseUrl"] = "https://example.invalid"
        self.save_provider()
        with self.assertRaisesRegex(FactoryError, "Repair the Pi"):
            self.plan()
        self.provider["providers"]["opencode-go"]["baseUrl"] = "https://opencode.ai/zen/go/v1"
        self.save_provider()
        self.assertEqual(self.plan()["status"], "READY_TO_LAUNCH")

    def test_dead_service_and_failed_launch_do_not_make_permanent_block(self):
        self.progress["worker"] = {"unit": "missing-obsolete.service", "pid": 99999999}
        self.save()
        original = (self.iteration / "progress.json").read_bytes()
        self.worker.return_value = 127
        with patch.dict(os.environ, {"OPENCODE_GO_API_KEY": "offline-test-only"}):
            result = self.plan(allow_paid=True)
        self.assertEqual(result["status"], "NEEDS_INSPECTION")
        self.assertEqual((self.iteration / "progress.json").read_bytes(), original)
        self.assertEqual(self.plan()["status"], "READY_TO_LAUNCH")

    def test_model_specific_overrides_cannot_change_provider_or_api(self):
        for where in ("model", "modelOverrides"):
            for field, value in (("baseUrl", "https://other-provider.invalid/v1"),
                                 ("api", "anthropic-messages")):
                with self.subTest(where=where, field=field):
                    original = copy.deepcopy(self.provider)
                    provider = self.provider["providers"]["opencode-go"]
                    model = provider["models"][0]
                    target = model if where == "model" else provider.setdefault("modelOverrides", {}).setdefault(model["id"], {})
                    target[field] = value
                    self.save_provider()
                    with self.assertRaisesRegex(FactoryError, "model-specific route"):
                        self.plan()
                    self.provider = original
                    self.save_provider()
        self.worker.assert_not_called()

    def test_stage_dispatch_has_no_generated_child_extension(self):
        plan = self.plan()
        self.assertNotIn("--extension", plan["argv"])
        self.assertNotIn("subagent", plan)
        self.assertIn("frozen task/execute", plan["argv"][-1])
        with patch.dict(os.environ, {"OPENCODE_GO_API_KEY": "offline-test-only"}):
            self.plan(allow_paid=True)
        self.assertFalse((Path(plan["session_dir"]) / "subagent.ts").exists())

    def test_existing_execution_lock_refuses_a_second_controller(self):
        lock = self.a.root / "inflight/writer-ch01-r01/.factory.lock"
        lock.parent.mkdir(parents=True)
        lock.write_text(json.dumps({"pid": os.getpid()}))
        with self.assertRaisesRegex(FactoryError, "role execution lock"):
            self.plan(allow_paid=True)
        self.worker.assert_not_called()

    def test_cli_defaults_to_inspection(self):
        args = parser().parse_args(["launch-book", "--iteration", "901", "--run", "iter901-sugar-a", "--agent-dir", "/tmp/test", "--extension", "/tmp/test.ts"])
        self.assertFalse(args.allow_paid)


class PreparedLineageTests(unittest.TestCase):
    """Real frozen-run fixtures, not mocked lineage/acceptance labels."""
    def setUp(self):
        from bc_factory.demo import inputs, scaffold
        from bc_factory.runs import Run, prepare
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "repo"
        scaffold(ROOT, self.repo)
        self.brief, self.research, self.chapter_plan = inputs()
        self.source_id = "iter901-topic-a"
        prepare(self.repo, self.source_id, self.brief, self.research, fixture=True)
        self.source = Run(self.repo, self.source_id)
        iteration = self.repo / "loop/iterations/901"
        iteration.mkdir(parents=True)
        (iteration / "hypothesis.md").write_text("One synthetic book; no live execution.")
        progress = {"schema_version": 1, "iteration": "901", "execution_status": "ACTIVE",
                    "preregistration_sha256": file_hash(iteration / "hypothesis.md"),
                    "allocation": {self.brief["subject"]: 1},
                    "authorization": {"status": "APPROVED", "reference": "fixture-only",
                                      "quote": "Synthetic infrastructure testing only."}}
        progress["authorization"]["scope_sha256"] = ops.scope_digest(progress)
        (iteration / "progress.json").write_text(json.dumps(progress))
        self.agent = self.repo / "private-pi"
        self.agent.mkdir()
        route = self.source.config["profiles"]["factory"]["routes"][0]
        (self.agent / "models.json").write_text(json.dumps({"providers": {"opencode-go": {
            "baseUrl": "https://opencode.ai/zen/go/v1", "api": "openai-responses",
            "models": [{"id": route["model"]}]}}}))
        self.extension = self.agent / "subagent.ts"

    def plan(self, run_id=None, **kwargs):
        return ops.launch_book(self.repo, "901", run_id or self.source_id,
                               self.agent, self.extension, sys.executable, **kwargs)

    def reject_evidence(self):
        from bc_factory.demo import accepted, metadata
        review = accepted()
        review.update(verdict="REVISE", findings=[{
            "kind": "EVIDENCE", "severity": "material", "quote": self.brief["reader_goal"],
            "explanation": "Synthetic missing research.", "repair": "Revise the fixture dossier."}])
        review["checks"]["truth"] = False
        self.source.submit(self.source.task("evidence-reviewer"), review, metadata(True))

    def successor(self, name="iter901-topic-a-r1", **kwargs):
        from bc_factory.runs import prepare
        return prepare(self.repo, name, kwargs.pop("brief", self.brief), self.research,
                       fixture=True, research_revision_of=self.source_id, **kwargs)

    def test_research_successor_is_one_book_and_resumes_its_session(self):
        first = self.plan()
        history = Path(first["session_dir"]) / "saved.jsonl"
        history.parent.mkdir(parents=True)
        original = json.dumps({"type": "session", "id": first["session_id"]}) + "\n"
        history.write_text(original)
        self.reject_evidence()
        source_hash = file_hash(self.source.root / "manifest.json")
        child = self.successor()
        later = self.plan(child.name)
        self.assertEqual(later["session_id"], first["session_id"])
        self.assertEqual(later["cwd"], str(child / "snapshot"))
        self.assertEqual(later["book_id"], self.source_id)
        self.assertEqual(history.read_text(), original)
        self.assertEqual(file_hash(self.source.root / "manifest.json"), source_hash)
        resumed = self.plan()
        self.assertEqual(resumed["run_id"], child.name)
        self.assertEqual(resumed["session_id"], first["session_id"])
        duplicate = self.repo / ".loop-work/pi" / child.name / "other.jsonl"
        duplicate.parent.mkdir(parents=True)
        duplicate.write_text(original)
        with self.assertRaisesRegex(FactoryError, "multiple native sessions"):
            self.plan(child.name)

    def test_research_handoff_automatically_resumes_the_exact_successor(self):
        from bc_factory.demo import finish
        from bc_factory.runs import Run
        self.reject_evidence()
        plans = []
        def worker(plan):
            plans.append(plan)
            if len(plans) == 1:
                self.successor()
            else:
                finish(Run(self.repo, "iter901-topic-a-r1"), self.chapter_plan)
            return 0
        with patch.object(ops, "_pty_run", side_effect=worker):
            with patch.dict(os.environ, {"OPENCODE_GO_API_KEY": "offline-only"}):
                result = self.plan(allow_paid=True)
        self.assertEqual(len(plans), 2)
        self.assertEqual(plans[0]["session_id"], plans[1]["session_id"])
        self.assertEqual(result["status"], "COMPLETE_UNRELEASED")
        self.assertEqual(result["next_run"], "iter901-topic-a-r1")

    def test_campaign_stop_at_research_boundary_prevents_automatic_handoff(self):
        self.reject_evidence()
        boundary = {"id": "offline-commissioning", "execution_status": "ACTIVE",
                    "iterations": ["901", "902"], "completed": [],
                    "plan": {"subject": self.brief["subject"], "books_per_cycle": 1},
                    "authorization": {"reference": "offline-test-only", "quote": "Synthetic boundary fault."}}
        boundary["authorization"]["scope_sha256"] = digest({"iterations": boundary["iterations"], "plan": boundary["plan"]})
        path = self.repo / "loop/commissioning.json"
        path.write_text(json.dumps(boundary))
        original = (self.repo / "loop/iterations/901/progress.json").read_bytes()
        def worker(plan):
            self.successor()
            boundary["execution_status"] = "STOPPED"
            path.write_text(json.dumps(boundary))
            return 0
        with patch.object(ops, "_pty_run", side_effect=worker) as launch, patch.dict(os.environ, {"OPENCODE_GO_API_KEY": "offline-only"}):
            with self.assertRaisesRegex(FactoryError, "Commissioning stop/completion"):
                self.plan(allow_paid=True)
        launch.assert_called_once()
        self.assertEqual((self.repo / "loop/iterations/901/progress.json").read_bytes(), original)

    def test_one_slot_cannot_hide_branching_research_successors(self):
        self.reject_evidence()
        self.successor()
        self.successor("iter901-topic-a-r2")
        with self.assertRaisesRegex(FactoryError, "branch"):
            self.plan("iter901-topic-a-r1")

    def test_linked_successor_cannot_change_frozen_brief(self):
        self.reject_evidence()
        changed = {**self.brief, "reader_goal": "A different experimental goal"}
        self.successor(brief=changed)
        with self.assertRaisesRegex(FactoryError, "scope|brief"):
            self.plan("iter901-topic-a-r1")

    def test_linked_successor_requires_original_source_evidence(self):
        from bc_factory.common import atomic_json, digest, read_json
        self.reject_evidence()
        self.successor()
        path = self.source.root / "results/evidence-reviewer-r01.json"
        record = read_json(path)
        record["payload"]["created_at"] = "different-source-receipt"
        record["sha256"] = digest(record["payload"])
        atomic_json(path, record)
        with self.assertRaisesRegex(FactoryError, "source|lineage"):
            self.plan("iter901-topic-a-r1")

    def test_remediation_successor_uses_the_same_book_slot(self):
        from bc_factory.demo import finish
        from bc_factory.runs import prepare
        first = self.plan()
        real_submit = self.source.submit
        def final_revise(task, output, meta):
            if task["role"] == "final-auditor":
                output = copy.deepcopy(output)
                output["verdict"] = "REVISE"
                output["checks"]["truth"] = False
                output["findings"] = [{"kind": "EVIDENCE", "severity": "material",
                    "quote": "One unsuccessful attempt is one observation.",
                    "explanation": "Synthetic fixable audit.", "repair": "Bounded whole-book repair."}]
            return real_submit(task, output, meta)
        with patch.object(self.source, "submit", side_effect=final_revise):
            with self.assertRaises(FactoryError):
                finish(self.source, self.chapter_plan)
        child = prepare(self.repo, "iter901-topic-a-rem", self.brief, self.research,
                        fixture=True, remediation_of=self.source_id)
        later = self.plan(child.name)
        self.assertEqual(later["book_id"], self.source_id)
        self.assertEqual(later["session_id"], first["session_id"])

    def test_remediation_can_repair_runtime_and_preserve_initial_preparation_and_stages(self):
        from bc_factory.demo import finish
        from bc_factory.runs import Run, prepare
        preparation = {"root": str(self.repo / ".loop-work/pi" / self.source_id / "preparation"),
                       "record": {"schema_version": 1, "run_id": self.source_id,
                                  "factory_files": self.source.manifest["factory_files"]},
                       "brief": self.brief, "caller_context": None, "frozen": False}
        ops._freeze_preparation(self.repo, preparation)
        first = self.plan()
        saved = Path(first["session_dir"]) / "saved.jsonl"
        history = json.dumps({"type": "session", "id": first["session_id"],
                              "cwd": str(self.source.root / "snapshot")}) + "\n"
        saved.write_text(history)
        real_submit = self.source.submit
        def final_revise(task, output, meta):
            if task["role"] == "final-auditor":
                output = copy.deepcopy(output)
                output["verdict"] = "REVISE"
                output["checks"]["truth"] = False
                output["findings"] = [{"kind": "EVIDENCE", "severity": "material",
                    "quote": "One unsuccessful attempt is one observation.",
                    "explanation": "Synthetic fixable audit.", "repair": "Bounded whole-book repair."}]
            return real_submit(task, output, meta)
        with patch.object(self.source, "submit", side_effect=final_revise):
            with self.assertRaises(FactoryError):
                finish(self.source, self.chapter_plan)
        original = {p.relative_to(self.source.root): p.read_bytes()
                    for p in self.source.root.rglob("*") if p.is_file()}
        contract = self.repo / "prompts/book-editor.md"
        contract.write_text(contract.read_text() + "\nSynthetic runtime repair: use supplied source-note identities.\n")
        child = prepare(self.repo, "iter901-topic-a-rem", self.brief, self.research,
                        fixture=True, remediation_of=self.source_id)
        repaired = Run(self.repo, child.name)
        self.assertNotEqual(repaired.manifest["factory_files"]["prompts/book-editor.md"],
                            self.source.manifest["factory_files"]["prompts/book-editor.md"])
        later = self.plan()  # A stale root pointer resolves the validated successor.
        self.assertEqual(later["run_id"], child.name)
        self.assertEqual(later["book_id"], self.source_id)
        self.assertEqual(later["session_id"], first["session_id"])
        self.assertEqual(later["cwd"], str(child / "snapshot"))
        self.assertEqual(saved.read_text(), history)
        self.assertEqual(original, {p.relative_to(self.source.root): p.read_bytes()
                                    for p in self.source.root.rglob("*") if p.is_file()})
        for rel, contents in original.items():
            if rel.parts[0] in ("tasks", "results", "assembly") or rel.as_posix() == "book.md":
                self.assertEqual((child / rel).read_bytes(), contents, str(rel))

    def next_brief(self):
        path = self.repo / "next-brief.json"
        path.write_text(json.dumps(self.brief))
        progress_path = self.repo / "loop/iterations/901/progress.json"
        progress = json.loads(progress_path.read_text())
        progress["allocation"][self.brief["subject"]] = 2
        progress["authorization"]["scope_sha256"] = ops.scope_digest(progress)
        progress_path.write_text(json.dumps(progress))
        return path

    def test_bootstrap_inspection_is_read_only_and_requires_frozen_science(self):
        with self.assertRaisesRegex(FactoryError, "Supply --brief"):
            self.plan("iter901-topic-b")
        plan = self.plan("iter901-topic-b", brief=self.next_brief())
        self.assertIn("/preparation", plan["cwd"])
        self.assertFalse(Path(plan["cwd"]).exists())
        self.assertIn("prompts/research-agent.md", plan["argv"][-1])
        self.assertNotIn("--extension", plan["argv"])

    def test_bootstrap_freezes_inputs_and_resumes_same_session_through_completion(self):
        from bc_factory.demo import finish
        from bc_factory.runs import Run
        from bc_autoresearch.learning import context_path, seed
        from bc_factory.common import unseal
        plans = []
        finish(self.source, self.chapter_plan)
        seed(self.repo, self.source_id, {
            "schema_version": 2, "subject": self.brief["subject"], "preserve": [], "improve": [],
            "recurring_repairs": [], "research_gaps": ["Retain the bounded valid countercase"],
            "note": "Synthetic baseline learning for the actual sealed-context handoff.",
        })
        guidance = context_path(self.source)
        context_payload = unseal(guidance)
        self.assertEqual(set(json.loads(guidance.read_text())), {"payload", "sha256"})
        def worker(plan):
            plans.append(plan)
            if len(plans) == 1:
                preparation = Path(plan["cwd"])
                self.assertTrue((preparation / "preparation.json").is_file())
                saved = Path(plan["session_dir"]) / "saved.jsonl"
                saved.write_text(json.dumps({"type": "session", "id": plan["session_id"],
                                             "cwd": str(preparation)}) + "\n")
                context = json.loads((preparation / "inputs/caller-context.json").read_text())
                self.assertEqual(context, context_payload)
                self.assertNotIn("payload", context)
                resumed = self.plan("iter901-topic-b", caller_context=guidance)
                self.assertEqual(resumed["preparation"]["caller_context"], context_payload)
                self.assertEqual(resumed["session_id"], plan["session_id"])
                dossier = preparation / "inputs/research.json"
                dossier.write_text(json.dumps(self.research))
                command = [sys.executable, str(preparation / "scripts/factory.py"),
                           "--repo", str(self.repo), "prepare", "--run", "iter901-topic-b",
                           "--brief", str(preparation / "inputs/brief.json"), "--research", str(dossier),
                           "--fixture", "--caller-context", str(preparation / "inputs/caller-context.json")]
                receipt = subprocess.run(command, capture_output=True, text=True, timeout=10)
                self.assertEqual(receipt.returncode, 0, receipt.stderr)
            else:
                self.assertIn("--session", plan["argv"])
                finish(Run(self.repo, "iter901-topic-b"), self.chapter_plan)
            return 0
        with patch.object(ops, "_pty_run", side_effect=worker), patch.dict(os.environ, {"OPENCODE_GO_API_KEY": "offline-only"}):
            result = self.plan("iter901-topic-b", brief=self.next_brief(), caller_context=guidance, allow_paid=True)
        self.assertEqual(len(plans), 2)
        self.assertEqual(plans[0]["session_id"], plans[1]["session_id"])
        self.assertEqual(plans[1]["cwd"], str(self.repo / "runs/iter901-topic-b/snapshot"))
        self.assertEqual(result["status"], "COMPLETE_UNRELEASED")
        candidate = Run(self.repo, "iter901-topic-b")
        self.assertEqual(candidate.caller_context, context_payload)
        frozen = Path(plans[0]["cwd"]) / "inputs/caller-context.json"
        self.assertEqual(candidate.manifest["caller_context_sha256"], file_hash(frozen))
        # The canonical sealed artifact is accepted identically when resuming
        # preparation and when checking a completed prepared book.
        self.assertEqual(self.plan("iter901-topic-b", caller_context=guidance)["status"], "ALREADY_COMPLETE")

    def test_sealed_caller_context_rejects_a_bad_checksum_before_inference(self):
        from bc_factory.common import seal
        guidance = self.repo / "sealed-context.json"
        seal(guidance, {"research_priorities": ["A valid control"]})
        record = json.loads(guidance.read_text())
        record["payload"]["research_priorities"] = ["Unsealed tampering"]
        guidance.write_text(json.dumps(record))
        with patch.object(ops, "_pty_run") as worker:
            with self.assertRaisesRegex(FactoryError, "Checksum mismatch"):
                self.plan("iter901-topic-b", brief=self.next_brief(), caller_context=guidance)
        worker.assert_not_called()

    def test_preparation_cannot_be_rebound_to_changed_science_or_extra_sample(self):
        brief = self.next_brief()
        with patch.object(ops, "_pty_run", return_value=0), patch.dict(os.environ, {"OPENCODE_GO_API_KEY": "offline-only"}):
            result = self.plan("iter901-topic-b", brief=brief, allow_paid=True)
        self.assertEqual(result["factory"]["status"], "UNPREPARED")
        changed = {**self.brief, "reader_goal": "An unregistered new goal"}
        brief.write_text(json.dumps(changed))
        with self.assertRaisesRegex(FactoryError, "Requested brief differs"):
            self.plan("iter901-topic-b", brief=brief)
        brief.write_text(json.dumps(self.brief))
        with self.assertRaisesRegex(FactoryError, "exceed"):
            self.plan("iter901-topic-c", brief=brief)

    def test_code_change_during_research_blocks_the_automatic_stage_handoff(self):
        from bc_factory.runs import prepare
        def worker(plan):
            prompt = self.repo / "prompts/research-agent.md"
            prompt.write_text(prompt.read_text() + "\nSynthetic concurrent code change.\n")
            prepare(self.repo, "iter901-topic-b", self.brief, self.research, fixture=True)
            return 0
        with patch.object(ops, "_pty_run", side_effect=worker) as launch, patch.dict(os.environ, {"OPENCODE_GO_API_KEY": "offline-only"}):
            with self.assertRaisesRegex(FactoryError, "source changed during research"):
                self.plan("iter901-topic-b", brief=self.next_brief(), allow_paid=True)
        launch.assert_called_once()

    def test_owner_stop_at_preparation_boundary_prevents_stage_execution(self):
        from bc_factory.runs import prepare
        def worker(plan):
            prepare(self.repo, "iter901-topic-b", self.brief, self.research, fixture=True)
            path = self.repo / "loop/iterations/901/progress.json"
            progress = json.loads(path.read_text())
            progress["execution_status"] = "STOPPED"
            path.write_text(json.dumps(progress))
            return 0
        with patch.object(ops, "_pty_run", side_effect=worker) as launch, patch.dict(os.environ, {"OPENCODE_GO_API_KEY": "offline-only"}):
            result = self.plan("iter901-topic-b", brief=self.next_brief(), allow_paid=True)
        self.assertEqual(result["status"], "STOPPED")
        launch.assert_called_once()


@unittest.skipUnless(os.name == "posix", "PTY/kernel launch locks are POSIX host facilities")
class NativeMechanicsTests(unittest.TestCase):
    def test_duplicate_owner_refused_but_stale_file_does_not_block(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            with ops.worker_lock(repo, "901"):
                with self.assertRaisesRegex(FactoryError, "still owns"):
                    with ops.worker_lock(repo, "901"):
                        self.fail("Duplicate worker admitted")
            # File remains; there is no PID-based stale-lock deletion ritual.
            self.assertTrue((repo / ".loop-work/pi/iteration-901.lock").exists())
            with ops.worker_lock(repo, "901"):
                pass

    def test_live_child_retains_lock_after_parent_releases_descriptor(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            child = None
            try:
                with ops.worker_lock(repo, "901"):
                    child = subprocess.Popen([sys.executable, "-c", "import sys; print('ready', flush=True); sys.stdin.readline()"],
                                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, close_fds=False)
                    self.assertEqual(child.stdout.readline().strip(), "ready")
                with self.assertRaises(FactoryError):
                    with ops.worker_lock(repo, "901"):
                        self.fail("Live orphan owner lost its lock")
                child.communicate("finish\n", timeout=5)
                with ops.worker_lock(repo, "901"):
                    pass
            finally:
                if child is not None and child.poll() is None:
                    child.kill()
                    child.communicate(timeout=5)

    def test_resume_binds_workspace_without_rewriting_history(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "snapshot"
            target.mkdir()
            session = root / "saved.jsonl"
            # Deliberate formatting and no final newline must survive unchanged.
            history = b'\n{"type": "custom", "data": {"preserve": true}}'
            for old_cwd in (str(root), str(target)):
                with self.subTest(old_cwd=old_cwd):
                    header = {"type": "session", "version": 3, "id": "same-book",
                              "cwd": old_cwd, "extra": {"keep": True}}
                    original_header = json.dumps(header).encode()
                    original = original_header + b"\n" + history
                    session.write_bytes(original)
                    log = root / ("changed.log" if old_cwd != str(target) else "same.log")
                    plan = {"cwd": str(target), "agent_dir": directory, "log": str(log),
                            "argv": [sys.executable, "-c", "pass", "--session", str(session)]}
                    with ops.worker_lock(root, "901"):
                        self.assertEqual(ops._pty_run(plan), 0)
                    current_header, _, current_history = session.read_bytes().partition(b"\n")
                    self.assertEqual(json.loads(current_header), {**header, "cwd": str(target)})
                    self.assertEqual(current_history, history)
                    if old_cwd != str(target):
                        self.assertIn(original_header, log.read_bytes())
                    else:
                        self.assertEqual(session.read_bytes(), original)
                        self.assertEqual(log.read_bytes(), b"")

    def test_startup_failure_reports_phase_without_disclosing_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            private_marker = "SYNTHETIC_PRIVATE_PATH"
            executable = root / private_marker
            executable.write_text("#!" + str(root / "missing-interpreter") + "\n")
            executable.chmod(0o700)
            cases = (("chdir", str(root / "missing" / private_marker), [sys.executable]),
                     ("exec", directory, [str(executable)]))
            for phase, cwd, argv in cases:
                with self.subTest(phase=phase):
                    log = root / (phase + ".log")
                    plan = {"cwd": cwd, "agent_dir": directory, "log": str(log), "argv": argv}
                    self.assertEqual(ops._pty_run(plan), 127)
                    diagnostic = log.read_text()
                    self.assertIn("Pi launch failed during " + phase, diagnostic)
                    self.assertIn("FileNotFoundError (errno=2)", diagnostic)
                    self.assertNotIn(private_marker, diagnostic)
                    self.assertNotIn(directory, diagnostic)

    def test_launcher_provides_real_pty_and_preserves_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = {"cwd": directory, "agent_dir": directory, "log": str(root / "console.log"),
                    "argv": [sys.executable, "-c", "import os; print('PTY_OK' if all(os.isatty(i) for i in (0,1,2)) else 'NO_PTY'); raise SystemExit(7)"]}
            self.assertEqual(ops._pty_run(plan), 7)
            self.assertIn("PTY_OK", (root / "console.log").read_text())
            self.assertEqual((root / "console.log").stat().st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()
