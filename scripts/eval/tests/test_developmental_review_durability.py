"""RF-13 isolated transport and non-downgradable lifecycle regressions."""
import json
import os
import shutil
import stat
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
sys.path.insert(0, str(ROOT / "scripts/eval"))
sys.path.insert(0, str(ROOT / "scripts/eval/tests"))
import candidate_pair as PAIR  # noqa: E402
import developmental_review as DEV  # noqa: E402
import developmental_review_call as CALL  # noqa: E402
import developmental_review_lifecycle as LIFE  # noqa: E402
import developmental_review_runtime as RUNTIME  # noqa: E402
import judge_scope as SCOPE  # noqa: E402
import native_developmental_review as NATIVE  # noqa: E402
import pair_store as STORE  # noqa: E402
from developmental_review_fixture import (  # noqa: E402
    DevelopmentalFixture, pass_developmental, proven_runner, verdict)


class DevelopmentalDurabilityTests(DevelopmentalFixture, unittest.TestCase):
    def lifecycle(self, candidate):
        manifest = json.loads((candidate / PAIR.MANIFEST).read_text(encoding="utf-8"))
        return LIFE.path(candidate, manifest)

    def erase_local(self, candidate):
        target = CALL.folder(candidate)
        target.chmod(0o700)
        shutil.rmtree(target)

    def test_transport_crash_recovers_without_duplicate_callback(self):
        """OpenSpec requirement: Candidate isolation and atomic promotion."""
        candidate, calls = self.ready("transport-crash"), []

        def interrupt(step):
            if step == "transport-persisted":
                raise RuntimeError("crash after transport")

        with self.assertRaisesRegex(RuntimeError, "crash after transport"):
            DEV.advance(candidate, runner=proven_runner(calls=calls), interrupt=interrupt)
        self.assertEqual(1, len(calls))
        self.assertTrue(CALL.transport_path(candidate).is_file())
        self.assertFalse(CALL.raw_path(candidate).exists())
        replay = mock.Mock()
        receipt = DEV.advance(candidate, runner=replay)
        replay.assert_not_called()
        self.assertEqual("PASS", receipt["state"])
        self.assertTrue(CALL.raw_path(candidate).is_file())

    def test_marker_only_is_ambiguous_and_never_redispatches(self):
        """OpenSpec scenario: A manual agent is dispatched."""
        candidate, calls = self.ready("marker-only"), []

        def crash(dispatch):
            calls.append(dispatch["task_sha256"])
            raise RuntimeError("before native persistence")

        with self.assertRaisesRegex(RuntimeError, "before native persistence"):
            DEV.advance(candidate, runner=crash)
        replay = mock.Mock()
        with self.assertRaisesRegex(DEV.DevelopmentalReviewError, "ambiguous"):
            DEV.advance(candidate, runner=replay)
        replay.assert_not_called()
        self.assertEqual(1, len(calls))

    def test_cross_operation_runtime_result_replay_is_rejected(self):
        """OpenSpec requirement: Candidate isolation and atomic promotion."""
        first, second = self.ready("operation-a"), self.ready("operation-b")
        first_task, second_task = DEV.prepare(first), DEV.prepare(second)
        CALL.start(first, first_task)
        proven_runner()({"task": first_task})
        CALL.start(second, second_task)
        RUNTIME.persist_result(second_task, RUNTIME.result(first_task))
        with self.assertRaisesRegex(CALL.CallError, "identity|proof"):
            CALL.import_result(second, second_task)

    def test_native_runtime_is_external_exact_and_rejects_every_tool_event(self):
        """Infrastructure: native callback is stubbed; no model call occurs."""
        candidate, captured = self.ready("native-wrapper"), {}
        task = DEV.prepare(candidate)
        _, marker = CALL.start(candidate, task)

        def clean_run(command, **kwargs):
            captured.update(command=command, **kwargs)
            events = (json.dumps({"type": "thread.started", "thread_id": "thread"}),
                      json.dumps({"type": "turn.started"}),
                      json.dumps({"type": "item.completed", "item": {
                          "type": "agent_message", "text": verdict(task)}}),
                      json.dumps({"type": "turn.completed", "usage": {"input_tokens": 1}}))
            return mock.Mock(returncode=0, stdout="\n".join(events), stderr="")

        NATIVE.complete(task["task_sha256"], run=clean_run)
        runtime = RUNTIME.path(task["task_sha256"])
        self.assertEqual(runtime, Path(captured["cwd"]))
        self.assertTrue(str(runtime).startswith("/tmp/belief-changer-rf13-"))
        self.assertNotIn(str(candidate), json.dumps(marker))
        self.assertNotIn(str(candidate), captured["input"])
        self.assertEqual(task, json.loads(captured["input"]))
        self.assertEqual({"task.json", "schema.json", "result.json"},
                         {item.name for item in runtime.iterdir()})
        self.assertEqual(0o555, stat.S_IMODE(os.lstat(runtime).st_mode))
        for feature in RUNTIME.DISABLED:
            self.assertIn(feature, captured["command"])

        blocked = self.ready("tool-attempt")
        blocked_task = DEV.prepare(blocked)
        CALL.start(blocked, blocked_task)

        def tool_run(_command, **_kwargs):
            events = (json.dumps({"type": "thread.started", "thread_id": "thread"}),
                      json.dumps({"type": "item.completed", "item": {
                          "type": "command_execution", "command": "cat /etc/passwd"}}),
                      json.dumps({"type": "item.completed", "item": {
                          "type": "agent_message", "text": verdict(blocked_task)}}),
                      json.dumps({"type": "turn.completed", "usage": {}}))
            return mock.Mock(returncode=0, stdout="\n".join(events), stderr="")

        with self.assertRaisesRegex(NATIVE.NativeError, "forbidden tool event"):
            NATIVE.complete(blocked_task["task_sha256"], run=tool_run)
        self.assertIsNone(RUNTIME.result(blocked_task))
        self.assertFalse(CALL.transport_path(blocked).exists())

    def test_lifecycle_anchor_modes_tamper_and_downgrade_fail_closed(self):
        """OpenSpec requirement: Candidate isolation and atomic promotion."""
        never = self.candidate("never-started")
        anchor = self.lifecycle(never)
        self.assertEqual(("NEVER_STARTED", None), tuple(
            json.loads(anchor.read_text())[key] for key in ("state", "local_state")))
        self.assertEqual(0o444, stat.S_IMODE(os.lstat(anchor).st_mode))

        candidate = self.ready("committed-anchor")
        task = DEV.prepare(candidate)
        started = json.loads(self.lifecycle(candidate).read_text())
        self.assertEqual(("STARTED", "PENDING"),
                         (started["state"], started["local_state"]))
        self.assertEqual(CALL.binding(task), started["binding"])
        DEV.advance(candidate, runner=proven_runner())
        committed = json.loads(self.lifecycle(candidate).read_text())
        self.assertEqual("COMMITTED", committed["local_state"])
        self.assertEqual(0o444, stat.S_IMODE(os.lstat(self.lifecycle(candidate)).st_mode))
        with self.assertRaisesRegex(DEV.DevelopmentalReviewError, "committed"):
            DEV.advance(candidate, runner=mock.Mock())

        self.erase_local(candidate)
        path = candidate / PAIR.MANIFEST
        value = json.loads(path.read_text())
        value["developmental_review"] = None
        path.write_bytes(STORE.json_bytes(value))
        with self.assertRaisesRegex(PAIR.PairError, "committed|authority|missing"):
            PAIR.load(candidate)

        tampered = self.ready("tampered-anchor")
        DEV.prepare(tampered)
        anchor = self.lifecycle(tampered)
        anchor.chmod(0o644)
        value = json.loads(anchor.read_text())
        value["state"] = "NEVER_STARTED"
        anchor.write_text(json.dumps(value), encoding="utf-8")
        anchor.chmod(0o444)
        with self.assertRaisesRegex(PAIR.PairError, "tampered|malformed"):
            PAIR.load(tampered)

    def test_seal_binds_lifecycle_and_evidence_deletion_never_reopens(self):
        """OpenSpec requirement: Candidate isolation and atomic promotion."""
        candidate = self.ready("seal-delete")
        pass_developmental(candidate)
        identity = DEV.seal_identity(candidate)
        tested = PAIR.seal(candidate)
        manifest = PAIR.load(candidate)
        self.assertEqual(identity, manifest["sealed"]["developmental_review"])
        self.assertFalse(any(item["path"].startswith("evidence/")
                             for item in PAIR._members(manifest)))
        self.erase_local(candidate)
        callback = mock.Mock()
        with self.assertRaises(DEV.DevelopmentalReviewError):
            DEV.advance(candidate, runner=callback)
        with self.assertRaises(PAIR.PairError):
            PAIR.verify_sealed(candidate, tested)
        callback.assert_not_called()
        self.lifecycle(candidate).unlink()
        with self.assertRaisesRegex(PAIR.PairError, "anchor is missing"):
            PAIR.load(candidate)

    @unittest.skipUnless(hasattr(os, "fork"), "requires POSIX crash semantics")
    def test_lifecycle_commit_kill_windows_recover_without_callback_replay(self):
        """OpenSpec scenario: Promotion is killed at an atomic boundary."""
        cases = (("pending", "developmental-lifecycle-finishing", 1),
                 ("pair", "write-prepared:pair.json", 1),
                 ("local", "developmental-lifecycle-local-commit", 1),
                 ("anchor", "lifecycle-write", 3))
        for name, event, occurrence in cases:
            with self.subTest(window=name):
                candidate = self.ready(f"kill-{name}")
                anchor = self.lifecycle(candidate)
                wanted = f"write-prepared:{anchor.name}" if event == "lifecycle-write" else event
                log = Path(self.tmp.name) / f"{name}-calls"
                base = proven_runner()

                def logged(dispatch):
                    with log.open("a", encoding="utf-8") as handle:
                        handle.write("call\n")
                        handle.flush()
                        os.fsync(handle.fileno())
                    return base(dispatch)

                pid = os.fork()
                if pid == 0:
                    seen = 0

                    def kill(step):
                        nonlocal seen
                        if step == wanted:
                            seen += 1
                            if seen == occurrence:
                                os.kill(os.getpid(), 9)

                    DEV.advance(candidate, runner=logged, interrupt=kill)
                    os._exit(70)
                _, status = os.waitpid(pid, 0)
                self.assertTrue(os.WIFSIGNALED(status))
                PAIR.load(candidate)
                self.assertEqual("PASS", DEV.require_developmental_pass(candidate)["state"])
                replay = mock.Mock()
                with self.assertRaisesRegex(DEV.DevelopmentalReviewError, "committed"):
                    DEV.advance(candidate, runner=replay)
                replay.assert_not_called()
                self.assertEqual(["call"], log.read_text().splitlines())
                record = json.loads(anchor.read_text())
                self.assertEqual("COMMITTED", record["local_state"])
                self.assertFalse(anchor.with_name(f".{anchor.name}.rf02-tmp").exists())

    def test_receipt_tamper_and_direct_product_gate_fail_before_outputs(self):
        """OpenSpec requirement: Split chapter review."""
        candidate = self.ready("direct-product")
        pass_developmental(candidate)
        tested = PAIR.seal(candidate)
        manifest = PAIR.load(candidate)
        exact = SimpleNamespace(candidate_root=str(candidate), tested_pair_hash=tested,
            chapters="1-3", pairs="", control="", h_f04_root="",
            ours=str(PAIR.candidate_tree(candidate) / manifest["run"]["book"] / "chapters"),
            ref=str(PAIR.evaluation_tree(candidate) / "calibration/reference/book"),
            out=str(PAIR.evidence_tree(candidate) / "product-judge"))
        raw = CALL.raw_path(candidate)
        raw.chmod(0o644)
        raw.write_text(raw.read_text().replace('"PASS"', '"NEEDS_CHANGES"', 1))
        raw.chmod(0o444)
        with self.assertRaisesRegex(SCOPE.ScopeError, "developmental|transport|verdict"):
            SCOPE.guard(exact)
        self.assertFalse(Path(exact.out).exists())


if __name__ == "__main__":
    unittest.main()
