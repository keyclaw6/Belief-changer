"""RF-11 external lifecycle anchoring and cross-root recovery scenarios."""
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
sys.path.insert(0, str(ROOT / "scripts/eval/tests"))
import candidate_pair as PAIR  # noqa: E402
import commission_set as SET  # noqa: E402
import draft_batch_lifecycle as LIFE  # noqa: E402
import first_draft_batch as BATCH  # noqa: E402
import run_iteration as RUN  # noqa: E402
from writer_context_fixture import WriterFixture  # noqa: E402


def draft(number):
    return f"# Chapter {number}\n" + "word " * 801 + "\n"


class DraftBatchLifecycleTests(WriterFixture, unittest.TestCase):
    def prepared(self, name):
        candidate = self.candidate(name)
        self.generate(candidate)
        return candidate

    def run_api(self, candidate, output, interrupt=None):
        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", return_value=("api", "key")), \
                mock.patch.object(RUN.ME, "chat", side_effect=output):
            return RUN.write_chapters(
                {"writer_model": "writer/model", "writer_reasoning": "none"},
                self.book(candidate), [1, 2], candidate, interrupt)

    def lifecycle_path(self, candidate):
        value = json.loads((candidate / PAIR.MANIFEST).read_text(encoding="utf-8"))
        return LIFE.path(candidate, value)

    def assert_generic_paths_blocked(self, candidate):
        operations = (lambda: PAIR.load(candidate), lambda: PAIR.seal(candidate),
                      lambda: PAIR.verify_sealed(candidate, "0" * 64),
                      lambda: PAIR.pending_sealed(candidate, "0" * 64),
                      lambda: BATCH.prepare(candidate))
        for operation in operations:
            with self.assertRaises((PAIR.PairError, BATCH.BatchError)):
                operation()

    def assert_anchor_mode_blocks(self, candidate):
        manifest = json.loads((candidate / PAIR.MANIFEST).read_text())
        operations = (lambda: PAIR.load(candidate), lambda: PAIR.seal(candidate),
                      lambda: PAIR.verify_sealed(candidate, "0" * 64),
                      lambda: PAIR.pending_sealed(candidate, "0" * 64),
                      lambda: LIFE.recover(candidate, manifest))
        for operation in operations:
            with self.assertRaisesRegex(
                    (PAIR.PairError, LIFE.LifecycleError),
                    "not a canonical read-only file|mode is not canonical 0444"):
                operation()

    def erase_local_batch(self, candidate, state, remove_operation=False):
        folder = BATCH.S.folder(candidate)
        for member in folder.rglob("*"):
            member.chmod(0o755 if member.is_dir() else 0o644)
        folder.chmod(0o755)
        shutil.rmtree(folder)
        path = candidate / PAIR.MANIFEST
        value = json.loads(path.read_text(encoding="utf-8"))
        value.update(state=state, draft_batch=None, draft_batch_start=None)
        if remove_operation:
            operation = value.pop("operation", None)
            if operation:
                operation_path = candidate / operation["path"]
                operation_path.chmod(0o644)
                operation_path.unlink()
            value["operation"] = None
        path.write_text(json.dumps(value), encoding="utf-8")

    def test_never_started_operation_has_explicit_external_lifecycle(self):
        """OpenSpec requirement: Candidate isolation and atomic promotion."""
        candidate = self.candidate("never-started")
        lifecycle = self.lifecycle_path(candidate)
        self.assertEqual("NEVER_STARTED", json.loads(lifecycle.read_text())["state"])
        self.assertEqual(0o444, stat.S_IMODE(os.lstat(lifecycle).st_mode))
        manifest = PAIR.load(candidate)
        tested = PAIR.seal(candidate)
        self.assertEqual(manifest["accepted_generation"],
                         PAIR.verify_sealed(candidate, tested)["accepted_generation"])

    def test_all_local_batch_deletion_cannot_restore_generic_semantics(self):
        """OpenSpec requirement: Candidate isolation and atomic promotion."""
        manual = self.prepared("manual-downgrade")
        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", return_value=("api", "")):
            self.assertFalse(RUN.write_chapters(
                {"writer_model": "writer/model"}, self.book(manual), [1, 2], manual))
        (self.book(manual) / "chapters/chapter-01.md").write_text(draft(1))
        self.assertEqual([2], BATCH.accept_manual(manual))
        self.erase_local_batch(manual, "WRITER_HANDOFF")
        self.assert_generic_paths_blocked(manual)

        api = self.prepared("api-downgrade")
        def stop(step):
            if step == "progress-recorded":
                raise RuntimeError(step)
        with self.assertRaisesRegex(RuntimeError, "progress-recorded"):
            self.run_api(api, lambda *args, **kwargs: draft(1), stop)
        self.erase_local_batch(api, "CANDIDATE", True)
        self.assert_generic_paths_blocked(api)

    def test_missing_or_tampered_external_lifecycle_fails_closed(self):
        """OpenSpec requirement: Candidate isolation and atomic promotion."""
        missing = self.candidate("missing-lifecycle")
        missing_anchor = self.lifecycle_path(missing)
        missing_anchor.chmod(0o644)
        missing_anchor.unlink()
        with self.assertRaisesRegex(PAIR.PairError, "lifecycle anchor is missing"):
            PAIR.load(missing)

        tampered = self.prepared("tampered-lifecycle")
        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", return_value=("api", "")):
            self.assertFalse(RUN.write_chapters(
                {"writer_model": "writer/model"}, self.book(tampered), [1, 2], tampered))
        lifecycle = self.lifecycle_path(tampered)
        lifecycle.chmod(0o644)
        value = json.loads(lifecycle.read_text())
        value["local_state"] = "PENDING"
        lifecycle.write_text(json.dumps(value))
        lifecycle.chmod(0o444)
        with self.assertRaisesRegex(PAIR.PairError, "tampered"):
            PAIR.load(tampered)

    def test_final_lifecycle_anchor_requires_canonical_read_only_mode(self):
        """OpenSpec scenario: Promotion is killed at an atomic boundary."""
        modes = (0o666,) if os.name == "nt" else (0o644, 0o400, 0o440)
        for mode in modes:
            with self.subTest(state="NEVER_STARTED", mode=oct(mode)):
                never = self.candidate(f"never-mode-{mode:o}")
                anchor = self.lifecycle_path(never)
                anchor.chmod(mode)
                self.assert_anchor_mode_blocks(never)
            with self.subTest(state="STARTED/COMMITTED", mode=oct(mode)):
                started = self.prepared(f"started-mode-{mode:o}")
                self.assertTrue(self.run_api(
                    started, lambda *args, **kwargs: draft(1)))
                anchor = self.lifecycle_path(started)
                self.assertEqual(0o444, stat.S_IMODE(os.lstat(anchor).st_mode))
                anchor.chmod(mode)
                self.assert_anchor_mode_blocks(started)

    @unittest.skipUnless(hasattr(os, "fork"), "requires POSIX process crash semantics")
    def test_lifecycle_start_kill_windows_restart_exactly(self):
        """OpenSpec scenario: Promotion is killed at an atomic boundary."""
        cases = (("external-pending", "lifecycle-write", 1),
                 ("started-before-local", "lifecycle-started", 1),
                 ("local-pair", "write-prepared:pair.json", 1),
                 ("evidence-before-commit", "lifecycle-evidence", 1),
                 ("external-commit", "lifecycle-write", 2))
        for name, event, occurrence in cases:
            with self.subTest(window=name):
                candidate = self.prepared(f"lifecycle-{name}")
                lifecycle = self.lifecycle_path(candidate)
                wanted = f"write-prepared:{lifecycle.name}" \
                    if event == "lifecycle-write" else event
                log = Path(self.tmp.name) / f"lifecycle-{name}-calls"

                def response(*_args, **_kwargs):
                    with log.open("a", encoding="utf-8") as handle:
                        handle.write("call\n")
                        handle.flush()
                        os.fsync(handle.fileno())
                    return draft(1)

                pid = os.fork()
                if pid == 0:
                    seen = 0
                    def kill(step):
                        nonlocal seen
                        if step == wanted:
                            seen += 1
                            if seen == occurrence:
                                os.kill(os.getpid(), 9)
                    self.run_api(candidate, response, kill)
                    os._exit(70)
                _, status = os.waitpid(pid, 0)
                self.assertTrue(os.WIFSIGNALED(status))
                self.assertTrue(self.run_api(candidate, response))
                self.assertEqual(2, len(log.read_text().splitlines()))
                state = json.loads(lifecycle.read_text())
                self.assertEqual(("STARTED", "COMMITTED"),
                                 (state["state"], state["local_state"]))
                self.assertEqual(0o444, stat.S_IMODE(os.lstat(lifecycle).st_mode))
                self.assertFalse(os.path.lexists(
                    lifecycle.with_name(f".{lifecycle.name}.rf02-tmp")))


if __name__ == "__main__":
    unittest.main()
