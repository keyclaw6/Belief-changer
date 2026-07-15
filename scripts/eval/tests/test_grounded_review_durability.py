"""RF-12 durable native-call and recovery regressions."""
import json
import os
import shutil
import stat
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
sys.path.insert(0, str(ROOT / "scripts/eval"))
sys.path.insert(0, str(ROOT / "scripts/eval/tests"))
import grounded_review as GR  # noqa: E402
import grounded_review_call as CALL  # noqa: E402
import grounded_review_contract as CONTRACT  # noqa: E402
import native_grounded_review as NATIVE  # noqa: E402
from grounded_review_fixture import (  # noqa: E402
    GroundedFixture, pass_review, proven_runner, verdict)


class GroundedReviewDurabilityTests(GroundedFixture, unittest.TestCase):
    def test_crash_after_transport_is_recovered_without_redispatch(self):
        """OpenSpec requirement: Candidate isolation and atomic promotion."""
        candidate = self.frozen("transport-crash")
        calls = []

        def interrupt(step):
            if step == "transport-persisted":
                raise RuntimeError("crash after transport")

        with self.assertRaisesRegex(RuntimeError, "crash after transport"):
            GR.advance(candidate, runner=proven_runner(calls=calls, interrupt=interrupt))
        self.assertEqual([1], calls)
        self.assertTrue(CALL.transport_path(candidate, 1).is_file())
        self.assertFalse(CALL.raw_path(candidate, 1).exists())
        receipt = GR.advance(candidate, runner=proven_runner(calls=calls))
        self.assertEqual([1, 2], calls)
        self.assertEqual("PASSED", receipt["state"])
        self.assertTrue(CALL.raw_path(candidate, 1).is_file())

    def test_marker_only_replay_is_ambiguous_and_never_calls_again(self):
        """OpenSpec scenario: A manual agent is dispatched."""
        candidate = self.frozen("marker-only")
        calls = []

        def crash(dispatch):
            calls.append(dispatch["task"]["chapter"])
            raise RuntimeError("before native persistence")

        with self.assertRaisesRegex(RuntimeError, "before native persistence"):
            GR.advance(candidate, runner=crash)
        self.assertEqual([1], calls)
        replay = mock.Mock()
        with self.assertRaisesRegex(GR.GroundedReviewError, "ambiguous"):
            GR.advance(candidate, runner=replay)
        replay.assert_not_called()

    def test_cross_operation_transport_replay_is_rejected(self):
        """OpenSpec requirement: Candidate isolation and atomic promotion."""
        first, second = self.frozen("operation-a"), self.frozen("operation-b")
        first_task, second_task = GR.prepare(first)[1], GR.prepare(second)[1]
        _, first_marker = CALL.start(first, first_task)
        CALL.persist(first, first_task, first_marker, verdict(first_task), {
            "exit_code": 0, "thread_id": "thread-a", "usage": {"input_tokens": 1},
            "command": first_marker["command"]})
        CALL.start(second, second_task)
        shutil.copyfile(CALL.transport_path(first, 1), CALL.transport_path(second, 1))
        shutil.copyfile(CALL.raw_path(first, 1), CALL.raw_path(second, 1))
        CALL.transport_path(second, 1).chmod(0o444)
        CALL.raw_path(second, 1).chmod(0o444)
        with self.assertRaisesRegex(CALL.CallError, "identity"):
            CALL.read(second, second_task)

    def test_native_wrapper_uses_only_readonly_task_workdir_and_persists_proof(self):
        """Infrastructure: native callback is stubbed; no model call occurs."""
        candidate = self.frozen("native-wrapper")
        task = GR.prepare(candidate)[1]
        _, marker = CALL.start(candidate, task)
        captured = {}

        def run(command, **kwargs):
            captured.update(command=command, **kwargs)
            events = (
                json.dumps({"type": "thread.started", "thread_id": "fresh-thread"}),
                json.dumps({"type": "item.completed",
                            "item": {"type": "agent_message", "text": verdict(task)}}),
                json.dumps({"type": "turn.completed", "usage": {"input_tokens": 1}}),
            )
            return mock.Mock(returncode=0, stdout="\n".join(events), stderr="")

        envelope = NATIVE.complete(CALL.workdir(candidate, 1), CALL.marker_path(candidate, 1),
                                   CALL.transport_path(candidate, 1),
                                   CALL.raw_path(candidate, 1), run=run)
        self.assertEqual(marker["call_id"], envelope["call_id"])
        self.assertEqual(CALL.workdir(candidate, 1), Path(captured["cwd"]))
        self.assertEqual({"task.json", "schema.json"},
                         {path.name for path in Path(captured["cwd"]).iterdir()})
        self.assertEqual(marker["command"], captured["command"])
        self.assertNotIn("FORBIDDEN-RAW-UNASSIGNED-SAME-PACKET", captured["input"])
        self.assertNotIn("OPENROUTER_API_KEY", captured["env"])
        self.assertTrue(CALL.transport_path(candidate, 1).is_file())
        self.assertTrue(CALL.raw_path(candidate, 1).is_file())

    def test_bare_json_manual_result_and_raw_file_are_not_accepted(self):
        """OpenSpec scenario: A manual agent is dispatched."""
        candidate = self.frozen("bare-json")
        with self.assertRaisesRegex(GR.GroundedReviewError, "bare reviewer JSON"):
            GR.advance(candidate, runner=lambda dispatch: verdict(dispatch["task"]))
        self.assertFalse(CALL.raw_path(candidate, 1).exists())

        manual = self.frozen("bare-file")
        task = GR.prepare(manual)[1]
        CALL.raw_path(manual, 1).write_text(verdict(task))
        with self.assertRaisesRegex(GR.GroundedReviewError, "order"):
            GR.advance(manual)

    def test_receipt_and_every_stored_byte_are_reread_fail_closed(self):
        """OpenSpec requirement: Candidate isolation and atomic promotion."""
        candidate = self.frozen("reread")
        pass_review(candidate)
        task = CALL.task_path(candidate, 1)
        task.chmod(0o644)
        with self.assertRaises(GR.GroundedReviewError):
            GR.require_complete(candidate)

        duplicate = self.frozen("duplicate-receipt")
        pass_review(duplicate)
        path = GR.receipt_path(duplicate)
        raw = path.read_text().replace('"state": "PASSED"',
                                       '"state": "PASSED", "state": "PASSED"', 1)
        path.chmod(0o644)
        path.write_text(raw)
        path.chmod(0o444)
        with self.assertRaisesRegex(GR.GroundedReviewError, "duplicate"):
            GR.require_complete(duplicate)

        modes = self.frozen("transport-mode")
        pass_review(modes)
        CALL.transport_path(modes, 1).chmod(0o644)
        with self.assertRaises(GR.GroundedReviewError):
            GR.require_complete(modes)


if __name__ == "__main__":
    unittest.main()
