"""RF-02 canonical decision and real-process crash recovery scenarios."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
import candidate_pair as PAIR  # noqa: E402
import gate as GATE  # noqa: E402
import gate_decision as DECISION  # noqa: E402
import pair_store as STORE  # noqa: E402

TIMESTAMP = "2026-07-14T12:00:00+00:00"


class PairRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def crash(self, action):
        pid = os.fork()
        if pid == 0:
            try:
                action()
            except BaseException:
                os._exit(72)
            os._exit(74)
        _, status = os.waitpid(pid, 0)
        self.assertTrue(os.WIFSIGNALED(status))
        self.assertEqual(9, os.WTERMSIG(status))

    def fixture(self, name, authorize=True):
        accepted = self.base / name / "repo"
        experiment = accepted / "loop/experiments/iter-001"
        experiment.mkdir(parents=True)
        files = {
            "loop/config.yaml": (
                "epsilon: 0.03\njudge_rubric: calibration/rubric.md\n"
                "reference_dir: calibration/reference\nresults_tsv: loop/results.tsv\n"),
            "loop/results.tsv": "iter\treward\tverdict\n0\t0.5\tBASELINE\n",
            "prompts/style-guide.md": "old style\n",
            "prompts/chapter-writer.md": "writer\n",
            "prompts/chapter-reviewer.md": "reviewer\n",
            "production-books/test/master-plan.md": "### CH-01 — One\n",
            "production-books/test/chapters/chapter-01.md": "old chapter\n",
            "production-books/test/research/source.txt": "source\n",
            "calibration/rubric.md": "rubric\n",
            "calibration/reference/001.txt": "reference\n",
            "calibration/reference/reference-metrics.json": "{}\n",
        }
        for relative, text in files.items():
            path = accepted / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        PAIR.initialize(accepted, "production-books/test")
        manifest = PAIR.snapshot(experiment, accepted, "production-books/test", "1", iteration=1)
        (PAIR.candidate_tree(experiment) / "prompts/style-guide.md").write_text(
            "new style\n", encoding="utf-8")
        tested = PAIR.seal(experiment)
        if not authorize:
            return accepted, experiment, manifest, tested, None
        row = {key: "" for key in GATE.COLUMNS if key != "timestamp_utc"}
        row.update(iter=1, reward=0.5, hard_ok=True, verdict="KEEP",
                   notes="test", tested_pair_hash=tested)
        receipt, history = DECISION.ensure(
            experiment, PAIR.load(experiment), {"receipt_hash": "score-fixture"},
            PAIR.evaluation_tree(experiment) / "loop/results.tsv", row,
            GATE.COLUMNS, 0.03, 0.5, "0", "KEEP", True, TIMESTAMP)
        return accepted, experiment, manifest, tested, (receipt, history)

    def test_promotion_requires_canonical_decision_and_exact_history(self):
        accepted, experiment, _, tested, _ = self.fixture("required", False)
        with self.assertRaises(TypeError):
            PAIR.promote(experiment, accepted, tested)
        with self.assertRaisesRegex(PAIR.PairError, "canonical gate decision"):
            PAIR.promote(experiment, accepted, tested, b"invented history\n")

        row = {key: "" for key in GATE.COLUMNS if key != "timestamp_utc"}
        row.update(iter=1, reward=0.5, hard_ok=True, verdict="KEEP",
                   notes="test", tested_pair_hash=tested)
        receipt, history = DECISION.ensure(
            experiment, PAIR.load(experiment), {"receipt_hash": "score-fixture"},
            PAIR.evaluation_tree(experiment) / "loop/results.tsv", row,
            GATE.COLUMNS, 0.03, 0.5, "0", "KEEP", True, TIMESTAMP)
        before = (experiment / DECISION.PATH).read_bytes()
        again, same_history = DECISION.ensure(
            experiment, PAIR.load(experiment), {"receipt_hash": "score-fixture"},
            PAIR.evaluation_tree(experiment) / "loop/results.tsv", row,
            GATE.COLUMNS, 0.03, 0.5, "0", "KEEP", True, TIMESTAMP)
        self.assertEqual(receipt, again)
        self.assertEqual(history, same_history)
        self.assertEqual(before, (experiment / DECISION.PATH).read_bytes())
        with self.assertRaisesRegex(PAIR.PairError, "history bytes"):
            PAIR.promote(experiment, accepted, tested, history + b"tamper")

    def test_atomic_write_retry_discards_only_safe_stale_temp(self):
        _, experiment, _, _, _ = self.fixture("atomic-write")
        target = experiment / "evidence/retry.json"
        target.parent.mkdir(exist_ok=True)
        stale = target.with_name(f".{target.name}.rf02-tmp")
        stale.write_bytes(b"partial")
        STORE.write(target, b"complete")
        self.assertEqual(b"complete", target.read_bytes())
        target.unlink()
        stale.symlink_to(experiment / "pair.json")
        with self.assertRaisesRegex(STORE.StoreError, "unsafe"):
            STORE.write(target, b"must not follow")

    def test_layout_recovery_rejects_unknown_or_unowned_temps(self):
        cases = ("unknown", "malformed", "self-hashed-malformed", "symlink", "hardlink")
        for case in cases:
            with self.subTest(case=case):
                _, experiment, _, tested, _ = self.fixture(case, False)
                name = ".unknown.rf02-tmp" if case == "unknown" \
                    else ".gate-decision.json.rf02-tmp"
                temp = experiment / name
                if case in ("unknown", "malformed"):
                    temp.write_text("not an owned receipt\n", encoding="utf-8")
                elif case == "self-hashed-malformed":
                    body = {"schema": 1, "tested_pair_hash": tested}
                    temp.write_text(json.dumps(
                        {**body, "decision_hash": STORE.state_hash(body)}), encoding="utf-8")
                elif case == "symlink":
                    temp.symlink_to(experiment / "pair.json")
                else:
                    source = experiment / "evidence/source"
                    source.parent.mkdir()
                    source.write_text("outside temp\n", encoding="utf-8")
                    temp.hardlink_to(source)
                with self.assertRaisesRegex(
                        PAIR.PairError, "undeclared|staging|aliased|linked|context"):
                    PAIR.verify_sealed(experiment, tested)
                self.assertTrue(os.path.lexists(temp))

    @unittest.skipUnless(hasattr(os, "fork"), "requires POSIX process crash semantics")
    def test_sigkill_inside_owned_atomic_writes_replays_to_terminal_state(self):
        accepted, experiment, _, _, _ = self.fixture("pair-write", False)
        manifest = PAIR.load(experiment)
        manifest["state"], manifest["tested_hash"] = "CANDIDATE", None
        manifest.pop("sealed", None)
        pair_json = experiment / PAIR.MANIFEST
        pair_json.chmod(0o644)
        STORE.write_json(pair_json, manifest)
        self.crash(lambda: PAIR.seal(
            experiment, interrupt=lambda step: os.kill(os.getpid(), 9)
            if step == "write-prepared:pair.json" else None))
        self.assertTrue((experiment / ".pair.json.rf02-tmp").is_file())
        tested = PAIR.seal(experiment)
        self.assertFalse(os.path.lexists(experiment / ".pair.json.rf02-tmp"))

        row = {key: "" for key in GATE.COLUMNS if key != "timestamp_utc"}
        row.update(iter=1, reward=0.5, hard_ok=True, verdict="KEEP",
                   notes="test", tested_pair_hash=tested)
        args = (experiment, PAIR.load(experiment), {"receipt_hash": "0" * 64},
                PAIR.evaluation_tree(experiment) / "loop/results.tsv", row,
                GATE.COLUMNS, 0.03, 0.5, "0", "KEEP", True, TIMESTAMP)
        self.crash(lambda: DECISION.ensure(
            *args, interrupt=lambda step: os.kill(os.getpid(), 9)
            if step == "write-prepared:gate-decision.json" else None))
        self.assertTrue((experiment / ".gate-decision.json.rf02-tmp").is_file())
        receipt, history = DECISION.ensure(*args)
        PAIR.verify_sealed(experiment, tested)

        self.crash(lambda: PAIR.promote(
            experiment, accepted, tested, history,
            interrupt=lambda step: os.kill(os.getpid(), 9)
            if step == "write-prepared:decision.json" else None))
        self.assertNotEqual(PAIR.load(experiment)["accepted_generation"],
                            STORE.current(accepted)[1])
        self.assertTrue((experiment / ".decision.json.rf02-tmp").is_file())
        self.assertFalse((experiment / PAIR.DECISION).exists())
        PAIR.promote(experiment, accepted, tested, history)
        self.assertEqual("PROMOTED", PAIR.status(experiment))
        self.assertFalse(os.path.lexists(experiment / ".decision.json.rf02-tmp"))
        terminal = json.loads((experiment / PAIR.DECISION).read_text())
        self.assertEqual(receipt, terminal["gate_receipt"])

    @unittest.skipUnless(hasattr(os, "fork"), "requires POSIX process crash semantics")
    def test_sigkill_boundary_retries_finish_without_stale_staging(self):
        for index, boundary in enumerate(("history-ready", "generation-ready",
                                          "pointer-prepared", "pointer-switched")):
            with self.subTest(boundary=boundary):
                accepted, experiment, manifest, tested, decision = self.fixture(
                    f"crash-{index}")
                receipt, history = decision
                canonical = (experiment / DECISION.PATH).read_bytes()
                pid = os.fork()
                if pid == 0:
                    try:
                        PAIR.promote(
                            experiment, accepted, tested, history,
                            interrupt=lambda step: os.kill(os.getpid(), 9)
                            if step == boundary else None)
                    except BaseException:
                        os._exit(72)
                    os._exit(74)
                _, status = os.waitpid(pid, 0)
                self.assertTrue(os.WIFSIGNALED(status))
                self.assertEqual(9, os.WTERMSIG(status))

                PAIR.promote(experiment, accepted, tested, history)
                self.assertEqual("PROMOTED", PAIR.status(experiment))
                current = STORE.current(accepted)[0]
                candidate = PAIR.candidate_tree(experiment)
                for item in manifest["entries"]:
                    self.assertEqual((candidate / item["path"]).read_bytes(),
                                     (current / "pair" / item["path"]).read_bytes())
                self.assertEqual(history,
                                 (current / "evaluation/loop/results.tsv").read_bytes())
                self.assertEqual(canonical, (experiment / DECISION.PATH).read_bytes())
                terminal = json.loads((experiment / PAIR.DECISION).read_text())
                self.assertEqual(receipt, terminal["gate_receipt"])
                store = STORE.state_dir(accepted)
                stale = [path for path in store.rglob("*")
                         if "rf02-tmp" in path.name or path.name.endswith("-tmp")]
                self.assertEqual([], stale)


if __name__ == "__main__":
    unittest.main()
