"""RF-11 ordered, recoverable, immutable first-draft batch scenarios."""
import json
import os
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
import gate as GATE  # noqa: E402
import gate_decision as DECISION  # noqa: E402
import grounded_review as GR  # noqa: E402
import judges  # noqa: E402
import manual_dispatch as MANUAL  # noqa: E402
import pair_store as STORE  # noqa: E402
import run_iteration as RUN  # noqa: E402
import writer_context as WC  # noqa: E402
from writer_context_fixture import WriterFixture  # noqa: E402
from grounded_review_fixture import pass_review  # noqa: E402

TIMESTAMP = "2026-07-14T12:00:00+00:00"


def draft(number, marker=""):
    return f"# Chapter {number}\n{marker}\n" + "word " * 801 + "\n"


class FirstDraftBatchTests(WriterFixture, unittest.TestCase):
    def write_api(self, candidate, outputs, capture=None, interrupt=None):
        side_effect = outputs if isinstance(outputs, list) else None

        def chat(*args, **kwargs):
            if capture is not None:
                capture.append(args[3])
            value = side_effect.pop(0) if side_effect is not None else outputs
            if isinstance(value, BaseException):
                raise value
            return value

        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", return_value=("api", "key")), \
                mock.patch.object(RUN.ME, "chat", side_effect=chat) as callback:
            result = RUN.write_chapters(
                {"writer_model": "writer/model", "writer_reasoning": "none"},
                self.book(candidate), [1, 2], candidate, interrupt)
        return result, callback

    def prepared(self, name):
        candidate = self.candidate(name)
        self.generate(candidate)
        return candidate

    def partial(self, name):
        candidate = self.prepared(name)
        def stop(step):
            if step == "progress-recorded":
                raise RuntimeError("interrupted")
        with self.assertRaises(RuntimeError):
            self.write_api(candidate, [draft(1, "FIRST")], interrupt=stop)
        self.assertEqual([1], [item["chapter"] for item in
                              PAIR.load(candidate)["draft_batch"]["drafts"]])
        return candidate

    def test_full_api_batch_is_ordered_and_frozen_before_review(self):
        """OpenSpec scenarios: extra context; review before batch freeze."""
        candidate = self.prepared("full-api")
        prompts = []
        self.assertTrue(self.write_api(
            candidate, [draft(1, "FIRST-GENERATED"), draft(2, "SECOND-GENERATED")],
            prompts)[0])
        self.assertIn("FIRST-GENERATED", prompts[1])
        self.assertNotIn("ORIGINAL-PREVIOUS-ONE", prompts[1])
        receipt = BATCH.freeze(candidate)
        batch = receipt["batch"]
        self.assertEqual([1, 2], [item["chapter"] for item in batch["drafts"]])
        self.assertEqual("FROZEN", batch["state"])
        with self.assertRaisesRegex(GR.GroundedReviewError, "receipt"):
            MANUAL.reviewer(candidate)
        GR.prepare(candidate)
        self.assertIn("evidence/grounded-review/work/chapter-01",
                      MANUAL.grounded(candidate, [1]))
        pass_review(candidate)
        self.assertIn("prompts/chapter-reviewer.md", MANUAL.reviewer(candidate))
        for item in batch["drafts"]:
            frozen = BATCH.S.folder(candidate) / f"chapter-{item['chapter']:02d}.md"
            self.assertEqual(item["sha256"], STORE.sha(frozen.read_bytes()))

    def test_manual_completion_uses_rf10_receipt_and_rejects_gaps(self):
        """OpenSpec scenario: A manual agent is dispatched."""
        candidate = self.prepared("manual")
        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", return_value=("api", "")):
            self.assertFalse(RUN.write_chapters(
                {"writer_model": "writer/model"}, self.book(candidate), [1, 2], candidate))
        token = WC.manual_receipt_hash(candidate)
        self.assertEqual(token, PAIR.load(candidate)["draft_batch"]
                         ["operation"]["writer_receipt_hash"])
        (self.book(candidate) / "chapters/chapter-02.md").write_text(draft(2, "GAP"))
        with self.assertRaisesRegex(BATCH.BatchError, "gap"):
            BATCH.accept_manual(candidate)
        (self.book(candidate) / "chapters/chapter-01.md").write_text(draft(1, "MANUAL-ONE"))
        self.assertEqual([], BATCH.accept_manual(candidate))
        BATCH.freeze(candidate)
        self.assertEqual(token, PAIR.load(candidate)["draft_batch"]
                         ["operation"]["writer_receipt_hash"])

    def test_early_review_and_judge_dispatch_fail_before_outputs(self):
        """OpenSpec scenario: Review begins before the draft batch is frozen."""
        candidate = self.prepared("early")
        with self.assertRaisesRegex(BATCH.BatchError, "not frozen"):
            MANUAL.reviewer(candidate)
        cfg = {"tasks_dir": str(candidate / "tasks"), "judge_k": 1,
               "judge_model": "judge", "judge_reasoning": "xhigh"}
        with self.assertRaisesRegex(SystemExit, "frozen first-draft batch"):
            judges.emit_tasks(cfg, [("ch1", "ours", "ref", "ctx")], "001",
                                "{{REFERENCE}}{{CANDIDATE}}{{CONTEXT}}", candidate)
        self.assertFalse((candidate / "tasks").exists())
        partial = self.partial("early-partial")
        with self.assertRaisesRegex(SystemExit, "frozen first-draft batch"):
            judges.emit_tasks(cfg, [("ch1", "ours", "ref", "ctx")], "001",
                                "{{REFERENCE}}{{CANDIDATE}}{{CONTEXT}}", partial)

    def test_interruption_resumes_only_remaining_with_same_authority(self):
        """OpenSpec requirement: Chapter writing loop."""
        candidate = self.partial("resume")
        prompts = []
        self.assertTrue(self.write_api(candidate, draft(2, "SECOND"), prompts)[0])
        self.assertEqual(1, len(prompts))
        self.assertIn("FIRST", prompts[0])
        BATCH.freeze(candidate)
        self.assertEqual([1, 2], [item["chapter"] for item in
                                  PAIR.load(candidate)["draft_batch"]["drafts"]])

    def test_drift_overwrite_mixed_and_extra_state_fail_before_callback(self):
        """OpenSpec requirement: Candidate isolation and atomic promotion."""
        def config(candidate):
            path = PAIR.candidate_tree(candidate) / "loop/config.yaml"
            path.write_text(path.read_text() + "drift: true\n")

        def overwrite(candidate):
            (self.book(candidate) / "chapters/chapter-01.md").write_text(
                draft(1, "OVERWRITTEN"))

        def mixed(candidate):
            (self.book(candidate) / "chapters/chapter-02.md").write_text(
                draft(2, "UNRECORDED"))

        def extra(candidate):
            (BATCH.S.folder(candidate) / "extra.md").write_text("extra\n")

        for name, mutate in (("config", config), ("overwrite", overwrite),
                             ("mixed", mixed), ("extra", extra)):
            with self.subTest(case=name):
                candidate = self.partial(name)
                mutate(candidate)
                callback = mock.Mock(return_value=draft(2))
                with mock.patch.object(SET.SC, "require_subject_contract"), \
                        mock.patch.object(RUN.judges, "endpoint", return_value=("api", "key")), \
                        mock.patch.object(RUN.ME, "chat", callback):
                    with self.assertRaises(SystemExit):
                        RUN.write_chapters({"writer_model": "writer/model"},
                                           self.book(candidate), [1, 2], candidate)
                callback.assert_not_called()

    def test_frozen_originals_survive_repair_and_promote_without_evidence(self):
        """OpenSpec scenarios: treatment promoted; immutable first drafts."""
        candidate = self.prepared("promote")
        self.write_api(candidate, [draft(1, "ORIGINAL-ONE"), draft(2, "ORIGINAL-TWO")])
        BATCH.freeze(candidate)
        frozen = BATCH.S.folder(candidate) / "chapter-01.md"
        before = frozen.read_bytes()
        working = self.book(candidate) / "chapters/chapter-01.md"
        working.write_text(draft(1, "REPAIRED"))
        self.assertEqual(before, frozen.read_bytes())
        BATCH.require_frozen_batch(candidate)
        pass_review(candidate)
        tested = PAIR.seal(candidate)
        PAIR.verify_sealed(candidate, tested)
        row = {key: "" for key in GATE.COLUMNS if key != "timestamp_utc"}
        row.update(iter=1, reward=0.5, hard_ok=True, verdict="KEEP",
                   notes="test", tested_pair_hash=tested)
        _, history = DECISION.ensure(
            candidate, PAIR.load(candidate), {"receipt_hash": "score-fixture"},
            PAIR.evaluation_tree(candidate) / "loop/results.tsv", row,
            GATE.COLUMNS, 0.03, 0.5, "0", "KEEP", True, TIMESTAMP)
        PAIR.promote(candidate, self.accepted, tested, history)
        accepted, _, registry = STORE.current(self.accepted)
        self.assertEqual(working.read_bytes(), (accepted / "pair" /
                         "production-books/test/chapters/chapter-01.md").read_bytes())
        self.assertFalse(any("first-draft-batch" in item["path"]
                             for item in registry["entries"]))
        self.assertFalse((accepted / "pair/evidence").exists())

    @unittest.skipUnless(hasattr(os, "fork"), "requires POSIX process crash semantics")
    def test_freeze_sigkill_recovery_replays_exact_receipt(self):
        """OpenSpec scenario: Promotion is killed at an atomic boundary."""
        candidate = self.prepared("freeze-recovery")
        self.write_api(candidate, [draft(1), draft(2)])
        pid = os.fork()
        if pid == 0:
            BATCH.freeze(candidate, interrupt=lambda step: os.kill(os.getpid(), 9)
                         if step == "write-prepared:pair.json" else None)
            os._exit(70)
        _, status = os.waitpid(pid, 0)
        self.assertTrue(os.WIFSIGNALED(status))
        temp = candidate / ".pair.json.rf02-tmp"
        self.assertTrue(temp.is_file())
        expected = temp.read_bytes()
        resumed, callback = self.write_api(candidate, [])
        self.assertTrue(resumed)
        callback.assert_not_called()
        receipt = BATCH.freeze(candidate)
        self.assertFalse(os.path.lexists(temp))
        self.assertEqual("FROZEN", receipt["batch"]["state"])
        self.assertEqual(json.loads(expected)["draft_batch"],
                         PAIR.load(candidate)["draft_batch"])


if __name__ == "__main__":
    unittest.main()
