"""RF-02 immutable generation, pinning, and rejection scenarios."""
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
import candidate_pair as PAIR  # noqa: E402
import gate as GATE  # noqa: E402
import gate_decision as DECISION  # noqa: E402
import pair_store as STORE  # noqa: E402
import legacy_guard as GUARD  # noqa: E402
import run_iteration as RUN  # noqa: E402
TIMESTAMP = "2026-07-14T12:00:00+00:00"
class Interrupted(RuntimeError):
    pass
class CandidatePairTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def fixture(self, name, initialize=True, snapshot=True):
        accepted = self.base / name / "repo"
        experiment = accepted / "loop/experiments" / name
        experiment.mkdir(parents=True)
        files = {
            "loop/config.yaml": (
                "epsilon: 0.03\nlength_band: 0.4\nreference_chapter_offset: 0\n"
                "originality_tripwire: 0.1\njudge_k: 1\n"
                "judge_rubric: calibration/judges/rubric.md\n"
                "reference_dir: calibration/reference/book\n"
                "writer_model: writer\nwriter_reasoning: none\njudge_model: judge\n"
                "results_tsv: loop/results.tsv\nscores_dir: loop/scores\n"
                "tasks_dir: loop/iterations\nweights:\n"
                "  - 'voice_certainty: 0.1666666667'\n"
                "  - 'method_execution: 0.1666666667'\n"
                "  - 'structure_anatomy: 0.1666666667'\n"
                "  - 'repetition_mantra: 0.1666666667'\n"
                "  - 'emotional_register: 0.1666666667'\n"
                "  - 'rhythm_texture: 0.1666666665'\n"),
            "loop/results.tsv": "iter\treward\tverdict\n0\t0.5\tBASELINE\n",
            "prompts/style-guide.md": "old style\n",
            "prompts/chapter-writer.md": "old writer\n",
            "prompts/chapter-reviewer.md": "old reviewer\n",
            "prompts/master-plan.md": "planner\n",
            "production-books/test/00-brief.md": "brief\n",
            "production-books/test/research/sources/source.txt": "source\n",
            "production-books/test/research/lived-experience.md": "lived\n",
            "production-books/test/research/scientific-evidence.md": "science\n",
            "production-books/test/framing.md": "framing\n",
            "production-books/test/master-plan.md": "### CH-01 — One\n### CH-02 — Two\n",
            "production-books/test/master-plan-review.md": "fit\n",
            "production-books/test/commissions/chapter-01.md": "commission\n",
            "production-books/test/chapters/chapter-01.md": "old chapter one\n",
            "production-books/test/chapters/chapter-02.md": "old chapter two\n",
            "production-books/second/00-brief.md": "second brief\n",
            "production-books/second/master-plan.md": "### CH-01 — Second\n",
            "production-books/second/chapters/chapter-01.md": "second chapter\n",
            "calibration/judges/rubric.md": "{{REFERENCE}}{{CANDIDATE}}{{CONTEXT}}\n",
            "calibration/reference/book/001.txt": "reference chapter\n",
            "calibration/reference/book/reference-metrics.json": '{"chapters": []}\n',
        }
        for relative, text in files.items():
            path = accepted / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        evidence = accepted / "loop/iterations/old/verdict.json"
        evidence.parent.mkdir(parents=True)
        evidence.write_text('{"old": true}\n', encoding="utf-8")
        if initialize:
            PAIR.initialize(accepted, "production-books/test")
        manifest = (PAIR.snapshot(experiment, accepted, "production-books/test", "1-2", iteration=1)
                    if snapshot else None)
        return accepted, experiment, manifest, evidence

    def logical_bytes(self, accepted, manifest):
        root = STORE.current(accepted)[0] / "pair"
        return tuple((root / item["path"]).read_bytes() for item in manifest["entries"])

    def public_state(self, accepted, manifest):
        out = []
        for item in manifest["entries"]:
            path = accepted / item["path"]
            info = path.lstat()
            out.append((item["path"], stat.S_IFMT(info.st_mode),
                        os.readlink(path) if path.is_symlink() else None,
                        STORE.sha(path.read_bytes())))
        return tuple(out)

    def bootstrap_state(self, accepted):
        paths = ["loop/config.yaml"] + [
            path.relative_to(accepted).as_posix() for root in (accepted / "prompts",
                                                               accepted / "production-books")
            for path in sorted(root.rglob("*")) if path.is_file()]
        out = []
        for relative in paths:
            path, info = accepted / relative, (accepted / relative).lstat()
            out.append((relative, stat.S_IFMT(info.st_mode),
                        os.readlink(path) if path.is_symlink() else None,
                        STORE.sha(path.read_bytes())))
        return tuple(out)

    def amend(self, experiment):
        tree = PAIR.candidate_tree(experiment)
        (tree / "prompts/style-guide.md").write_text("new style\n", encoding="utf-8")
        (tree / "production-books/test/chapters/chapter-01.md").write_text(
            "new chapter one\n", encoding="utf-8")

    def decide(self, experiment, tested, verdict="KEEP"):
        row = {key: "" for key in GATE.COLUMNS if key != "timestamp_utc"}
        row.update(iter=1, reward=0.5, hard_ok=verdict != "FAIL-HARD",
                   verdict=verdict, notes="test", tested_pair_hash=tested)
        _, history = DECISION.ensure(
            experiment, PAIR.load(experiment), {"receipt_hash": "fixture"},
            PAIR.evaluation_tree(experiment) / "loop/results.tsv", row,
            GATE.COLUMNS, 0.03, 0.5, "0", verdict, verdict == "KEEP", TIMESTAMP)
        return history

    def test_reject_preserves_public_bytes_types_links_and_old_evidence(self):
        """OpenSpec scenario: A treatment is rejected."""
        accepted, experiment, manifest, evidence = self.fixture("reject")
        public, logical = self.public_state(accepted, manifest), self.logical_bytes(accepted, manifest)
        self.amend(experiment)
        tested = PAIR.seal(experiment)
        self.decide(experiment, tested, "REVERT")
        PAIR.reject(experiment, tested)
        self.assertEqual(public, self.public_state(accepted, manifest))
        self.assertEqual(logical, self.logical_bytes(accepted, manifest))
        self.assertEqual('{"old": true}\n', evidence.read_text(encoding="utf-8"))
        self.assertEqual("REJECTED", PAIR.status(experiment))

    def test_accept_switches_exact_complete_logical_generation(self):
        """OpenSpec scenario: A treatment is promoted."""
        accepted, experiment, manifest, _ = self.fixture("accept")
        public = self.public_state(accepted, manifest)
        self.amend(experiment)
        new = tuple((PAIR.candidate_tree(experiment) / item["path"]).read_bytes()
                    for item in manifest["entries"])
        tested = PAIR.seal(experiment)
        PAIR.promote(experiment, accepted, tested,
                     self.decide(experiment, tested))
        self.assertEqual(new, self.logical_bytes(accepted, manifest))
        self.assertEqual(public, self.public_state(accepted, manifest))
        self.assertEqual("PROMOTED", PAIR.status(experiment))

    def test_setup_interruption_exposes_none_old_or_new(self):
        for index, stop in enumerate(("generation-ready", "pointer-prepared", "pointer-switched")):
            with self.subTest(setup=stop):
                accepted, _, _, _ = self.fixture(f"setup-{index}", False, False)
                before = self.bootstrap_state(accepted)
                with self.assertRaises(Interrupted):
                    PAIR.initialize(accepted, "production-books/test",
                                    interrupt=lambda step: (_ for _ in ()).throw(Interrupted())
                                    if step == stop else None)
                self.assertEqual(before, self.bootstrap_state(accepted))
                if stop == "pointer-switched":
                    self.assertIsNotNone(STORE.current(accepted)[0])
                else:
                    self.assertEqual((None, None, None), STORE.current(accepted, required=False))
                    if stop == "generation-ready":
                        registry = next((STORE.state_dir(accepted) / "manifests").iterdir())
                        registry.chmod(0o666)
                        registry.unlink()
                    PAIR.initialize(accepted, "production-books/test")
                    self.assertIsNotNone(STORE.current(accepted)[0])
                    self.assertEqual(before, self.bootstrap_state(accepted))

    def test_current_pointer_is_native_atomic_and_directory_flush_succeeds(self):
        """OpenSpec scenario: The accepted-generation store is initialized."""
        accepted, _, _, _ = self.fixture("native-pointer", True, False)
        store = STORE.state_dir(accepted)
        generation = STORE.current(accepted)[1]
        pointer = store / "current"
        STORE._sync(store)
        if os.name == "nt":
            self.assertTrue(pointer.is_file())
            self.assertFalse(pointer.is_symlink())
            self.assertEqual((generation + "\n").encode("ascii"), pointer.read_bytes())
        else:
            self.assertTrue(pointer.is_symlink())
            self.assertEqual(Path("generations") / generation,
                             Path(os.readlink(pointer)))

    def test_snapshot_pins_one_generation_and_corrupt_metadata_fails(self):
        accepted, first, manifest, _ = self.fixture("pin")
        old_id = STORE.current(accepted)[1]
        self.amend(first)
        tested = PAIR.seal(first)
        PAIR.promote(first, accepted, tested, self.decide(first, tested))
        new_tree, new_id, _ = STORE.current(accepted)
        second = accepted / "loop/experiments/second"
        second.mkdir()
        real_current, calls = STORE.current, []

        def switch_after_pin(root, required=True):
            calls.append(1)
            pinned = real_current(root, required)
            STORE.switch(accepted, old_id)
            return pinned

        with mock.patch.object(STORE, "current", side_effect=switch_after_pin):
            snap = PAIR.snapshot(second, accepted, "production-books/test", "1-2")
        self.assertEqual(1, len(calls))
        self.assertEqual(new_id, snap["accepted_generation"])
        self.assertEqual((new_tree / "pair/prompts/style-guide.md").read_bytes(),
                         (PAIR.candidate_tree(second) / "prompts/style-guide.md").read_bytes())

        metadata = STORE.state_dir(accepted) / "manifests" / f"{old_id}.json"
        metadata.chmod(0o644)
        metadata.write_text("{malformed", encoding="utf-8")
        third = accepted / "loop/experiments/third"
        third.mkdir()
        with self.assertRaisesRegex(PAIR.PairError, "malformed"):
            PAIR.snapshot(third, accepted, "production-books/test")

    def test_sealed_metadata_and_tree_drift_fail_closed(self):
        _, experiment, manifest, _ = self.fixture("sealed")
        tested = PAIR.seal(experiment)
        with self.assertRaisesRegex(PAIR.PairError, "terminal"):
            PAIR.seal(experiment)
        pair_json = experiment / PAIR.MANIFEST
        pair_json.chmod(0o644)
        value = json.loads(pair_json.read_text(encoding="utf-8"))
        value["run"]["chapters"] = [2]
        pair_json.write_text(json.dumps(value), encoding="utf-8")
        with self.assertRaisesRegex(PAIR.PairError, "lifecycle"):
            PAIR.verify_sealed(experiment, tested)

        value["run"]["chapters"] = manifest["run"]["chapters"]
        pair_json.write_text(json.dumps(value), encoding="utf-8")
        eval_file = PAIR.evaluation_tree(experiment) / manifest["evaluation"][0]["path"]
        eval_file.chmod(0o644)
        eval_file.write_text("drift\n", encoding="utf-8")
        with self.assertRaisesRegex(PAIR.PairError, "drifted"):
            PAIR.verify_sealed(experiment, tested)

    def test_run_requires_explicit_setup_then_derives_canonical_identity(self):
        accepted, experiment, _, _ = self.fixture("run", True, False)
        ledger = self.base / "run-ledger.md"
        ledger.write_text("### RF-23 — prose\n\n- Status: `READY`\n", encoding="utf-8")
        argv = ["run_iteration.py", "--book", "production-books/test", "--chapters", "1",
                "--iter", "1", "--accepted-root", str(accepted), "--redesign-authorized",
                "--rf-stage", "RF-23", "--candidate-root", str(experiment),
                "--decision-timestamp", TIMESTAMP]
        authority = {"manifest": {"run": {"book": "production-books/test",
                                             "chapters": [1]}},
                     "contract": "writer\n", "commissions": {1: "commission\n"}}
        with mock.patch.object(sys, "argv", argv), mock.patch.object(GUARD, "LEDGER", ledger), \
                mock.patch.object(RUN.WC, "capture", return_value=authority), \
                mock.patch.object(RUN.WC, "require_fresh"), \
                mock.patch.object(RUN.WC, "persist_manual_receipt", return_value="a" * 64), \
                mock.patch.object(RUN.WC, "manual_receipt_hash", return_value="a" * 64), \
                mock.patch.object(RUN.FB, "begin", return_value={
                    "state": "DRAFTING", "mode": "manual",
                    "drafts": [], "selection": [1]}), \
                mock.patch.object(RUN.judges, "endpoint", return_value=("", "")):
            with self.assertRaises(SystemExit) as stopped:
                RUN.main()
        self.assertEqual(2, stopped.exception.code)
        run = PAIR.load(experiment)["run"]
        self.assertEqual({"experiment_id": "run", "iteration_id": 1,
                          "book": "production-books/test", "chapters": [1],
                          "config": "loop/config.yaml"}, run)
        with self.assertRaisesRegex(PAIR.PairError, "resume CLI"):
            PAIR.assert_run(experiment, PAIR.load(experiment),
                            "production-books/test", "2", 1, "loop/config.yaml")


if __name__ == "__main__":
    unittest.main()
