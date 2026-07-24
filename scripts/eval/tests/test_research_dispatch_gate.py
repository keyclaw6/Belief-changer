"""Focused RF-32 immediate chapter-research dispatch regressions."""
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
sys.path.insert(0, str(ROOT / "scripts/eval"))
import draft_batch_runtime as RUNTIME  # noqa: E402
import writer_context as CONTEXT  # noqa: E402


class ResearchDispatchGateTests(unittest.TestCase):
    def _batch(self):
        return {"state": "DRAFTING", "drafts": [], "selection": [1], "mode": "api"}

    def _base(self):
        authority = {"manifest": {"run": {"chapters": [1]}}}
        patches = (
            mock.patch.object(RUNTIME, "_capture", return_value=(authority, self._batch())),
            mock.patch.object(RUNTIME.judges, "endpoint", return_value=("api", "secret")),
            mock.patch.object(RUNTIME.WC, "require_fresh"),
            mock.patch.object(RUNTIME.FB, "begin", return_value=self._batch()),
            mock.patch.object(RUNTIME.FB, "prepare", return_value=[1]),
            mock.patch.object(RUNTIME.LG, "require_output"),
        )
        return authority, patches

    def test_structured_gap_blocks_before_durable_writer_callback(self):
        """OpenSpec scenario: A chapter's assigned research is inadequate."""
        _authority, patches = self._base()
        durable, callback = mock.Mock(), mock.Mock()
        gap = ("RESEARCH GAP\nOwner: research/synthesis\nChapter: C-01\n"
               "Code: unit_missing\nGap: LEU-001 is absent")
        with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], \
                mock.patch.object(RUNTIME.WC, "require_chapter_research",
                                  side_effect=CONTEXT.WriterContextError(gap)), \
                mock.patch.object(RUNTIME.FB, "durable_call", durable), \
                mock.patch.object(RUNTIME.ME, "chat", callback):
            with self.assertRaisesRegex(SystemExit, "RESEARCH GAP"):
                RUNTIME.write_chapters({"writer_model": "writer"}, Path("book"),
                                       [1], Path("candidate"))
        durable.assert_not_called()
        callback.assert_not_called()

    def test_current_binding_reaches_only_the_existing_writer_callback(self):
        """OpenSpec scenario: A chapter's assigned research is adequate."""
        authority, patches = self._base()
        binding = {"seal_sha256": "a" * 64,
                   "needs": {"E-01": {"unit_ids": ["LEU-001"]}}}
        seen = []

        def durable(_candidate, _number, request, callback, _interrupt):
            seen.append(request)
            return callback()

        with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], \
                mock.patch.object(RUNTIME.WC, "require_chapter_research",
                                  return_value=binding) as research, \
                mock.patch.object(RUNTIME.WC, "inputs", return_value={
                    "compact_writer_contract": "contract",
                    "authoritative_commission": "commission",
                    "previous_chapter": "previous"}), \
                mock.patch.object(RUNTIME.WC, "build", return_value="compact input"), \
                mock.patch.object(RUNTIME.FB, "durable_call", side_effect=durable), \
                mock.patch.object(RUNTIME.ME, "chat", return_value="chapter") as callback, \
                mock.patch.object(RUNTIME.WR, "capture_api"), \
                mock.patch.object(RUNTIME.FB, "accept_response", return_value=801):
            self.assertTrue(RUNTIME.write_chapters(
                {"writer_model": "writer", "writer_reasoning": "none"},
                Path("book"), [1], Path("candidate")))
        research.assert_called_once_with(Path("candidate"), 1, authority)
        callback.assert_called_once()
        self.assertEqual("a" * 64, seen[0]["research_seal_sha256"])
        self.assertIn("research_needs_sha256", seen[0])


if __name__ == "__main__":
    unittest.main()
