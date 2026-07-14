"""RF-00 permits only explicit RF-02 non-prose store maintenance pre-RF-23."""
import contextlib
import io
import os
import shlex
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
import candidate_pair as PAIR  # noqa: E402
import gate as GATE  # noqa: E402
import legacy_guard as GUARD  # noqa: E402
import manual_dispatch as MANUAL  # noqa: E402
import run_iteration as RUN  # noqa: E402
import score as SCORE  # noqa: E402
import pair_store as STORE  # noqa: E402

TIMESTAMP = "2026-07-14T12:00:00+00:00"


class RF02StoreCliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "isolated"
        self.root.mkdir()
        self._write("loop/config.yaml",
                    "judge_rubric: calibration/rubric.md\n"
                    "reference_dir: calibration/reference\nresults_tsv: loop/results.tsv\n"
                    "writer_model: writer\nwriter_reasoning: none\n")
        self._write("loop/results.tsv", "iter\treward\tverdict\n")
        self._write("prompts/style-guide.md", "style\n")
        self._write("prompts/chapter-writer.md", "writer\n")
        self._write("prompts/chapter-reviewer.md", "reviewer\n")
        self._book("test")
        self._write("calibration/rubric.md", "rubric\n")
        self._write("calibration/reference/001.txt", "reference\n")
        self._write("calibration/reference/reference-metrics.json", "{}\n")
        self.ledger = Path(self.tmp.name) / "tasks.md"
        self.ledger.write_text(
            "### RF-02 — store\n\n- Status: `READY`\n\n"
            "### RF-23 — prose\n\n- Status: `TODO`\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _book(self, slug):
        self._write(f"production-books/{slug}/master-plan.md", "### CH-01 — One\n")
        self._write(f"production-books/{slug}/chapters/chapter-01.md", "chapter\n")

    def _run_store(self, flag, book="production-books/test", target=None):
        argv = ["run_iteration.py", "--book", book, "--iter", "1",
                "--accepted-root", str(target or self.root),
                "--candidate-root", str(self.root), "--redesign-authorized",
                "--rf-stage", "RF-02", flag]
        with mock.patch.object(sys, "argv", argv), \
                mock.patch.object(GUARD, "LEDGER", self.ledger):
            RUN.main()

    def test_rf02_ready_initializes_and_extends_store_before_rf23(self):
        self._run_store("--initialize-accepted-store")
        first = STORE.current(self.root)[1]
        self._book("new")
        self._run_store("--add-book-to-accepted-store", "production-books/new")
        current, second, registry = STORE.current(self.root)
        self.assertNotEqual(first, second)
        self.assertIn("production-books/new/chapters/chapter-01.md",
                      {item["path"] for item in registry["entries"]})
        self.assertEqual(b"chapter\n",
                         (current / "pair/production-books/new/chapters/chapter-01.md").read_bytes())

    def test_rf02_does_not_authorize_run_score_or_gate(self):
        common = ["--redesign-authorized", "--rf-stage", "RF-02",
                  "--candidate-root", str(self.root)]
        cases = (
            (RUN, ["run_iteration.py", "--book", str(self.root / "production-books/test"),
                   "--iter", "1"]),
            (SCORE, ["score.py", "--book", str(self.root / "production-books/test"),
                     "--iter", "1"]),
            (GATE, ["gate.py", "--iter", "1"]),
        )
        with mock.patch.object(GUARD, "LEDGER", self.ledger):
            for module, prefix in cases:
                with self.subTest(entrypoint=prefix[0]), \
                        mock.patch.object(sys, "argv", prefix + common), \
                        mock.patch.object(module.loopcfg, "load", side_effect=AssertionError):
                    with self.assertRaises(SystemExit) as stopped:
                        module.main()
                    self.assertIn("legacy execution requires RF-23 READY",
                                  str(stopped.exception))

    def test_rf02_store_target_cannot_escape_isolated_root(self):
        outside = Path(self.tmp.name) / "other"
        outside.mkdir()
        with mock.patch.object(PAIR, "initialize", side_effect=AssertionError):
            with self.assertRaises(SystemExit) as stopped:
                self._run_store("--initialize-accepted-store", target=outside)
        self.assertIn("must equal the isolated", str(stopped.exception))

    def test_manual_dispatch_pins_cwd_and_uses_only_relative_inputs(self):
        operation = self.root / "loop/experiments/iter-001/candidate"
        book = operation / "production-books/test"
        book.mkdir(parents=True)
        authority = {"contract": "CAPTURED-CONTRACT\n",
                     "commissions": {1: "CAPTURED-ONE\n", 2: "CAPTURED-TWO\n"}}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            MANUAL.writer({"writer_model": "writer", "writer_reasoning": "none"},
                          operation, book, [1, 2], authority)
        text = output.getvalue()
        self.assertIn(f"cd -- {operation}", text)
        self.assertIn("CAPTURED-CONTRACT", text)
        self.assertIn("CAPTURED-ONE", text)
        self.assertIn("CAPTURED-TWO", text)
        self.assertNotIn("master-plan.md", text)
        self.assertNotIn("style-guide.md", text)
        self.assertNotIn(str(ROOT), text)
        review = MANUAL.reviewer(operation)
        self.assertIn(f"cd -- {operation}", review)
        self.assertIn("prompts/chapter-reviewer.md", review)
        self.assertNotIn(str(ROOT), review)

    def test_resume_command_replays_exact_pinned_invocation_shell_safely(self):
        """OpenSpec scenario: A manual agent is dispatched."""
        PAIR.initialize(self.root, "production-books/test")
        candidate = self.root / "loop/experiments/iter 007; $quoted'"
        candidate.mkdir(parents=True)
        self.ledger.write_text(
            "### RF-02 — store\n\n- Status: `READY`\n\n"
            "### RF-23 — prose\n\n- Status: `READY`\n", encoding="utf-8")
        hypothesis = "quote ' and $HOME; no shell execution"
        argv = ["run_iteration.py", "--book", "production-books/test",
                "--chapters", "1", "--iter", "7", "--hypothesis", hypothesis,
                "--config", "loop/config.yaml", "--accepted-root", str(self.root),
                "--promote-pair", "--redesign-authorized", "--rf-stage", "RF-23",
                "--candidate-root", str(candidate),
                "--decision-timestamp", TIMESTAMP]
        output = io.StringIO()
        with mock.patch.object(sys, "argv", argv), \
                mock.patch.object(GUARD, "LEDGER", self.ledger), \
                mock.patch.object(RUN, "write_chapters", return_value=True), \
                mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "do-not-render"}), \
                contextlib.redirect_stdout(output):
            with self.assertRaises(SystemExit) as paused:
                RUN.main()
        self.assertEqual(0, paused.exception.code)
        line = next(item for item in output.getvalue().splitlines()
                    if item.startswith("[run]   "))
        command = line.removeprefix("[run]   ")
        tokens = shlex.split(command)
        self.assertEqual(str(Path(RUN.__file__).absolute()), tokens[1])
        for flag, value in (("--book", "production-books/test"), ("--chapters", "1"),
                            ("--iter", "7"), ("--hypothesis", hypothesis),
                            ("--config", "loop/config.yaml"),
                            ("--accepted-root", str(self.root)),
                            ("--decision-timestamp", TIMESTAMP),
                            ("--rf-stage", "RF-23"),
                            ("--candidate-root", str(candidate))):
            self.assertEqual(value, tokens[tokens.index(flag) + 1])
        for flag in ("--promote-pair", "--redesign-authorized", "--no-write"):
            self.assertIn(flag, tokens)
        self.assertEqual(1, tokens.count("--no-write"))
        self.assertNotIn("do-not-render", command)

        with mock.patch.object(sys, "argv", tokens[1:]), \
                mock.patch.object(GUARD, "LEDGER", self.ledger), \
                mock.patch.object(RUN, "write_chapters", side_effect=AssertionError), \
                mock.patch.object(RUN, "run_step", return_value=3) as dispatched:
            with self.assertRaises(SystemExit) as replayed:
                RUN.main()
        self.assertEqual(3, replayed.exception.code)
        dispatched.assert_called_once()

    def test_no_endpoint_prints_exact_safe_resume(self):
        """OpenSpec scenario: A manual agent is dispatched."""
        PAIR.initialize(self.root, "production-books/test")
        candidate = self.root / "loop/experiments/no key; $quoted'"
        candidate.mkdir(parents=True)
        self.ledger.write_text(
            "### RF-02 — store\n\n- Status: `READY`\n\n"
            "### RF-23 — prose\n\n- Status: `READY`\n", encoding="utf-8")
        hypothesis = "quote ' and $HOME; no shell execution"
        argv = ["run_iteration.py", "--book", "production-books/test",
                "--chapters", "1", "--iter", "7", "--hypothesis", hypothesis,
                "--config", "loop/config.yaml", "--accepted-root", str(self.root),
                "--decision-timestamp", TIMESTAMP, "--promote-pair",
                "--redesign-authorized", "--rf-stage", "RF-23",
                "--candidate-root", str(candidate)]
        authority = {"manifest": {"run": {"book": "production-books/test",
                                             "chapters": [1]}},
                     "contract": "writer\n", "commissions": {1: "commission\n"}}
        output = io.StringIO()
        with mock.patch.object(sys, "argv", argv), \
                mock.patch.object(GUARD, "LEDGER", self.ledger), \
                mock.patch.object(RUN.WC, "capture", return_value=authority), \
                mock.patch.object(RUN.WC, "require_fresh"), \
                mock.patch.object(RUN.WC, "persist_manual_receipt", return_value="a" * 64), \
                mock.patch.object(RUN.WC, "manual_receipt_hash", return_value="a" * 64), \
                mock.patch.object(RUN.judges, "endpoint", return_value=("", "")), \
                mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "do-not-render"}), \
                contextlib.redirect_stdout(output):
            with self.assertRaises(SystemExit) as stopped:
                RUN.main()
        self.assertEqual(2, stopped.exception.code)
        command = next(line.removeprefix("[run]   ") for line in output.getvalue().splitlines()
                       if line.startswith("[run]   "))
        tokens = shlex.split(command)
        for flag, value in (("--book", "production-books/test"), ("--chapters", "1"),
                            ("--iter", "7"), ("--hypothesis", hypothesis),
                            ("--config", "loop/config.yaml"),
                            ("--accepted-root", str(self.root)),
                            ("--decision-timestamp", TIMESTAMP), ("--rf-stage", "RF-23"),
                            ("--candidate-root", str(candidate))):
            self.assertEqual(value, tokens[tokens.index(flag) + 1])
        for flag in ("--promote-pair", "--redesign-authorized", "--no-write"):
            self.assertIn(flag, tokens)
        self.assertEqual("a" * 64, tokens[tokens.index("--writer-authority-receipt") + 1])
        self.assertEqual(1, tokens.count("--no-write"))
        self.assertNotIn("do-not-render", command)


if __name__ == "__main__":
    unittest.main()
