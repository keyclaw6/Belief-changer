"""RF-11 call durability, irreversible start, and canonical freeze scenarios."""
import json
import os
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
import first_draft_batch as BATCH  # noqa: E402
import pair_store as STORE  # noqa: E402
import run_iteration as RUN  # noqa: E402
from writer_context_fixture import WriterFixture  # noqa: E402


def draft(number, marker=""):
    return f"# Chapter {number}\n{marker}\n" + "word " * 801 + "\n"


class DraftBatchDurabilityTests(WriterFixture, unittest.TestCase):
    def prepared(self, name):
        candidate = self.candidate(name)
        self.generate(candidate)
        return candidate

    def run_api(self, candidate, output, calls, interrupt=None):
        def chat(*args, **kwargs):
            calls.append(args[3])
            value = output(len(calls)) if callable(output) else output
            if isinstance(value, BaseException):
                raise value
            return value

        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", return_value=("api", "key")), \
                mock.patch.object(RUN.ME, "chat", side_effect=chat):
            return RUN.write_chapters(
                {"writer_model": "writer/model", "writer_reasoning": "none"},
                self.book(candidate), [1, 2], candidate, interrupt)

    def interrupt_at(self, wanted):
        def stop(step):
            if step == wanted:
                raise RuntimeError(wanted)
        return stop

    def test_each_accepted_response_window_resumes_without_duplicate_callback(self):
        """OpenSpec requirement: Chapter writing loop."""
        stages = ("response-staged", "response-returning", "pending-recorded",
                  "snapshot-preparing", "progress-committing", "progress-recorded")
        for stage in stages:
            with self.subTest(stage=stage):
                candidate, calls = self.prepared(stage), []
                with self.assertRaisesRegex(RuntimeError, stage):
                    self.run_api(candidate, draft(1, "ACCEPTED-ONE"), calls,
                                 self.interrupt_at(stage))
                self.assertEqual(1, len(calls))
                self.assertTrue(self.run_api(candidate, draft(2, "SECOND"), calls))
                self.assertEqual(2, len(calls))
                batch = PAIR.load(candidate)["draft_batch"]
                self.assertEqual([1, 2], [item["chapter"] for item in batch["drafts"]])
                self.assertEqual([1, 2], [item["chapter"] for item in batch["responses"]])
                frozen = BATCH.S.folder(candidate) / "chapter-01.md"
                self.assertIn(b"ACCEPTED-ONE", frozen.read_bytes())

    def test_pre_return_ambiguity_fails_closed_without_another_callback(self):
        """OpenSpec scenario: Review begins before the draft batch is frozen."""
        cases = (("before-call", self.interrupt_at("call-marked"), draft(1)),
                 ("received-unpersisted", self.interrupt_at("response-received"), draft(1)),
                 ("remote-ambiguous", None, RuntimeError("remote ambiguous")))
        for name, interrupt, output in cases:
            with self.subTest(case=name):
                candidate, calls = self.prepared(name), []
                with self.assertRaises(RuntimeError):
                    self.run_api(candidate, output, calls, interrupt)
                accepted = len(calls)
                with self.assertRaisesRegex(SystemExit, "replay is ambiguous"):
                    self.run_api(candidate, draft(1, "MUST-NOT-RUN"), calls)
                self.assertEqual(accepted, len(calls))

    def test_response_mismatch_after_call_marker_fails_closed(self):
        """OpenSpec requirement: Chapter writing loop."""
        candidate, calls = self.prepared("response-mismatch"), []
        with self.assertRaisesRegex(RuntimeError, "response-staged"):
            self.run_api(candidate, draft(1), calls,
                         self.interrupt_at("response-staged"))
        response = BATCH.S.folder(candidate) / "response-01.json"
        value = json.loads(response.read_text(encoding="utf-8"))
        value["response_sha256"] = "0" * 64
        response.write_text(json.dumps(value), encoding="utf-8")
        with self.assertRaisesRegex(SystemExit, "identity mismatch"):
            self.run_api(candidate, draft(1, "MUST-NOT-RUN"), calls)
        self.assertEqual(1, len(calls))

    @unittest.skipUnless(hasattr(os, "fork"), "requires POSIX process crash semantics")
    def test_sigkill_at_each_atomic_window_recovers_without_duplicate_callback(self):
        """OpenSpec scenario: Promotion is killed at an atomic boundary."""
        cases = (("call-marker", "write-prepared:pair.json", 2),
                 ("response", "write-prepared:response-01.json", 1),
                 ("pending", "write-prepared:pair.json", 3),
                 ("snapshot", "write-prepared:chapter-01.md", 1),
                 ("progress", "write-prepared:pair.json", 4))
        for name, wanted, occurrence in cases:
            with self.subTest(window=name):
                candidate = self.prepared(f"sigkill-{name}")
                call_log = Path(self.tmp.name) / f"{name}-calls"

                def response(_number):
                    count = len(call_log.read_text().splitlines()) \
                        if call_log.exists() else 0
                    with call_log.open("a", encoding="utf-8") as handle:
                        handle.write(f"{count + 1}\n")
                        handle.flush()
                        os.fsync(handle.fileno())
                    return draft(count + 1, f"CALL-{count + 1}")

                pid = os.fork()
                if pid == 0:
                    seen = 0

                    def stop(step):
                        nonlocal seen
                        if step == wanted:
                            seen += 1
                            if seen == occurrence:
                                os.kill(os.getpid(), 9)

                    self.run_api(candidate, response, [], stop)
                    os._exit(70)
                _, status = os.waitpid(pid, 0)
                self.assertTrue(os.WIFSIGNALED(status))
                self.assertTrue(self.run_api(candidate, response, []))
                self.assertEqual(2, len(call_log.read_text().splitlines()))
                self.assertEqual([1, 2], [item["chapter"] for item in
                                 PAIR.load(candidate)["draft_batch"]["drafts"]])
                temps = [path for path in candidate.rglob("*")
                         if "rf02-tmp" in path.name]
                self.assertEqual([], temps)

    def test_batch_start_cannot_be_downgraded_into_generic_rf02(self):
        """OpenSpec requirement: Candidate isolation and atomic promotion."""
        def null_batch(value):
            value["draft_batch"] = None

        def delete_batch(value):
            del value["draft_batch"]

        def delete_marker(value):
            del value["draft_batch_start"]

        def downgrade_state(value):
            value["state"] = "WRITER_HANDOFF"

        def delete_all_metadata(value):
            value.pop("draft_batch", None)
            value.pop("draft_batch_start", None)
            value["state"] = "WRITER_HANDOFF"

        for name, mutate in (("null", null_batch), ("deleted", delete_batch),
                             ("marker", delete_marker), ("state", downgrade_state),
                             ("evidence-retained", delete_all_metadata)):
            with self.subTest(case=name):
                candidate, calls = self.prepared(f"downgrade-{name}"), []
                with self.assertRaises(RuntimeError):
                    self.run_api(candidate, draft(1), calls,
                                 self.interrupt_at("response-staged"))
                path = candidate / PAIR.MANIFEST
                value = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual("DRAFTING", value["state"])
                self.assertEqual(value["draft_batch"]["start_sha256"],
                                 value["draft_batch_start"]["start_sha256"])
                mutate(value)
                path.write_text(json.dumps(value), encoding="utf-8")
                for operation in (lambda: PAIR.load(candidate),
                                  lambda: PAIR.seal(candidate),
                                  lambda: PAIR.verify_sealed(candidate, "0" * 64),
                                  lambda: BATCH.prepare(candidate)):
                    with self.assertRaises((PAIR.PairError, BATCH.BatchError)):
                        operation()

    def test_every_frozen_evidence_file_requires_platform_read_only_state(self):
        """OpenSpec scenario: Review begins before the draft batch is frozen."""
        candidate, calls = self.prepared("modes"), []
        self.assertTrue(self.run_api(candidate, lambda n: draft(n), calls))
        BATCH.freeze(candidate)
        folder = BATCH.S.folder(candidate)
        if os.name == "nt":
            BATCH.require_frozen_batch(candidate)
            targets = ((folder / "chapter-01.md", 0o666),)
            error = "single-link read-only file"
        else:
            targets = ((folder / "chapter-01.md", 0o400),
                       (folder / BATCH.S.RECEIPT, 0o440),
                       (folder / "response-01.json", 0o400))
            error = "canonical 0444"
        for path, mode in targets:
            with self.subTest(path=path.name, mode=oct(mode)):
                path.chmod(mode)
                with self.assertRaisesRegex(BATCH.BatchError, error):
                    BATCH.require_frozen_batch(candidate)
                path.chmod(0o444)
        BATCH.require_frozen_batch(candidate)
        if os.name == "nt":
            self.assertTrue(all(
                getattr(os.lstat(path), "st_file_attributes", 0)
                & getattr(stat, "FILE_ATTRIBUTE_READONLY", 0)
                for path in STORE.tree_files(folder)))
        else:
            self.assertTrue(all(stat.S_IMODE(os.lstat(path).st_mode) == 0o444
                                for path in STORE.tree_files(folder)))


if __name__ == "__main__":
    unittest.main()
