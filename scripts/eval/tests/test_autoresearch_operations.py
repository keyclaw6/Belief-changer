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

UPSTREAM_STUB = '\n'.join([
    'import { discoverAgents } from "./agents.ts";',
    'const args: string[] = ["--mode", "json", "-p", "--no-session"];',
    'resolve(code ?? 0);',
])

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from bc_autoresearch import operations as ops
from bc_autoresearch.cli import parser
from bc_factory.common import FactoryError, file_hash


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
        self.extension.write_text(UPSTREAM_STUB)
        (self.extension.parent / "agents.ts").write_text("// Offline discovery fixture")
        self.runs = {}
        self.addCleanup(patch.stopall)
        patch.object(ops, "Run", side_effect=lambda repo, run_id: self.runs[run_id]).start()
        self.worker = patch.object(ops, "_pty_run", return_value=0).start()
        self.a = self.add_run("iter901-sugar-a")

    def save(self):
        (self.iteration / "progress.json").write_text(json.dumps(self.progress))

    def save_provider(self):
        (self.agent / "models.json").write_text(json.dumps(self.provider))

    def add_run(self, name, subject="quit-sugar", complete=False):
        root = self.repo / "runs" / name
        (root / "snapshot/.pi/agents").mkdir(parents=True)
        (root / "snapshot/.pi/agents/factory-orchestrator.md").write_text("Frozen factory role")
        (root / "snapshot/AGENTS.md").write_text("Frozen factory contract")
        run = Mock(root=root, config=copy.deepcopy(self.config), manifest={"subject": subject})
        run.status.return_value = {"status": "COMPLETE_UNRELEASED" if complete else "INCOMPLETE", "run_id": name}
        run.accepted_audit.return_value = (1, {})
        self.runs[name] = run
        return run

    def plan(self, name="iter901-sugar-a", **kwargs):
        return ops.launch_book(self.repo, "901", name, self.agent, self.extension, sys.executable, **kwargs)

    def test_inspection_has_no_worker_or_session_side_effect(self):
        self.assertEqual(self.plan()["status"], "READY_TO_LAUNCH")
        self.worker.assert_not_called()
        self.assertFalse((self.repo / ".loop-work").exists())

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
        self.extension.unlink()
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

    def test_missing_extension_and_broken_pi_mapping_are_repairable(self):
        self.extension.unlink()
        with self.assertRaisesRegex(FactoryError, "Repair/install"):
            self.plan()
        self.extension.write_text(UPSTREAM_STUB)
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

    def test_child_startup_isolated_without_copying_orchestrator_prompt(self):
        plan = self.plan()
        text = ops.isolated_subagent_source(self.extension, Path(plan["cwd"]))
        for flag in ("--no-context-files", "--no-extensions", "--no-skills", "--no-prompt-templates", "--approve"):
            self.assertIn(flag, text)
        self.assertIn(str(self.a.root / "snapshot/AGENTS.md"), text)
        self.assertNotIn("factory-orchestrator.md", text)
        self.assertIn(str(self.extension.parent / "agents.ts"), text)
        self.assertEqual(self.extension.read_text(), UPSTREAM_STUB)
        self.assertFalse(Path(plan["subagent"]["path"]).exists())
        with patch.dict(os.environ, {"OPENCODE_GO_API_KEY": "offline-test-only"}):
            self.plan(allow_paid=True)
        self.assertEqual(Path(plan["subagent"]["path"]).read_text(), text)

    def test_changed_upstream_subagent_needs_compatibility_repair(self):
        self.extension.write_text("// incompatible upstream revision")
        with self.assertRaisesRegex(FactoryError, "startup compatibility"):
            self.plan()
        self.worker.assert_not_called()

    def test_cli_defaults_to_inspection(self):
        args = parser().parse_args(["launch-book", "--iteration", "901", "--run", "iter901-sugar-a", "--agent-dir", "/tmp/test", "--extension", "/tmp/test.ts"])
        self.assertFalse(args.allow_paid)


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
