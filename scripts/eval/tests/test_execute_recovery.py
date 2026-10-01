"""No-network fixture checks at the factory execution/recovery boundary."""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from bc_factory import cli
from bc_factory.common import atomic_json, lock
from bc_factory.demo import accepted, inputs, metadata, scaffold
from bc_factory.runs import Run, prepare


class ExecuteRecoveryTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name) / "repo"
        scaffold(ROOT, self.repo)
        brief, research, _ = inputs()
        prepare(self.repo, "recovery-fixture", brief, research, fixture=True)
        self.run = Run(self.repo, "recovery-fixture")
        self.task = self.run.task("evidence-reviewer")
        self.path = self.repo / "supplied-task.json"
        atomic_json(self.path, self.task)
        self.output, self.meta = accepted(), metadata(external=True)

    def invoke(self):
        with contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(io.StringIO()) as err:
            code = cli.main(["--repo", str(self.repo), "execute", "--run", "recovery-fixture",
                             "--task", str(self.path), "--allow-paid"])
        return code, out.getvalue(), err.getvalue()

    def test_recorded_task_replay_never_calls_provider(self):
        self.run.submit(self.task, self.output, self.meta)
        before = (self.run.root / "results/evidence-reviewer-r01.json").read_bytes()
        with patch.object(cli, "execute") as provider:
            code, out, err = self.invoke()
        self.assertEqual(provider.call_count, 0, "Provider must not run for a recorded/conflicting task")
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["status"], "RECORDED")
        self.assertEqual((self.run.root / "results/evidence-reviewer-r01.json").read_bytes(), before)

    def test_completion_between_inspection_and_lock_never_spends_twice(self):
        @contextlib.contextmanager
        def completed_before_acquisition(root):
            # Simulate another invocation finishing before this one acquires its lock.
            self.run.submit(self.task, self.output, self.meta)
            with lock(root):
                yield
        with patch.object(cli, "lock", completed_before_acquisition), patch.object(cli, "execute") as provider:
            code, out, err = self.invoke()
        self.assertEqual(provider.call_count, 0, "Provider must not run for a recorded/conflicting task")
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["status"], "RECORDED")

    def test_changed_task_cannot_reuse_an_existing_receipt(self):
        self.run.submit(self.task, self.output, self.meta)
        self.task["inputs"]["brief"]["title"] = "Different task"
        atomic_json(self.path, self.task)
        with patch.object(cli, "execute") as provider:
            code, _, err = self.invoke()
        self.assertEqual(provider.call_count, 0, "Provider must not run for a recorded/conflicting task")
        self.assertEqual(code, 2)
        self.assertIn("task", err.lower())

    def test_corrupt_recorded_result_is_not_success_or_regenerated(self):
        self.run.submit(self.task, self.output, self.meta)
        path = self.run.root / "results/evidence-reviewer-r01.json"
        broken = json.loads(path.read_text())
        broken["payload"]["output"]["verdict"] = "BLOCKED"
        atomic_json(path, broken)
        with patch.object(cli, "execute") as provider:
            code, _, _ = self.invoke()
        self.assertEqual(provider.call_count, 0, "Provider must not run for a recorded/conflicting task")
        self.assertEqual(code, 2)

    def test_unfinished_task_calls_provider_once_and_stores_real_return(self):
        with patch.object(cli, "execute", return_value=(self.output, self.meta)) as provider:
            code, _, err = self.invoke()
        self.assertEqual(code, 0, err)
        provider.assert_called_once()
        self.assertEqual(self.run.result("evidence-reviewer")["output"], self.output)


if __name__ == "__main__":
    unittest.main()
