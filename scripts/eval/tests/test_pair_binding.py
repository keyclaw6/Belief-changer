"""RF-02 gate receipt binds every decision input and judge artifact."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
import candidate_pair as PAIR  # noqa: E402
import gate as GATE  # noqa: E402
import judges  # noqa: E402
import legacy_guard as GUARD  # noqa: E402
import score_receipt  # noqa: E402
import pair_store as STORE  # noqa: E402

RUBRIC = "{{REFERENCE}}\n{{CANDIDATE}}\n{{CONTEXT}}\n"
TIMESTAMP = "2026-07-14T12:00:00+00:00"


def verdict(pair_hash, task_hash):
    return {"pair_hash": pair_hash, "task_hash": task_hash,
            "scores": {dimension: 5 for dimension in judges.DIMS},
            "worst_dimension": judges.DIMS[0], "gap_summary": "fixture",
            "suggestions": [
                {"asset": "style-guide", "suggestion": "first"},
                {"asset": "chapter-writer", "suggestion": "second"},
                {"asset": "master-plan", "suggestion": "third"}]}


class PairBindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def fixture(self, name):
        accepted = self.root / name / "repo"
        experiment = accepted / "loop/experiments/iter-001"
        experiment.mkdir(parents=True)
        weights = "\n".join(f"  - '{dimension}: {1 / len(judges.DIMS)}'"
                            for dimension in judges.DIMS)
        files = {
            "loop/config.yaml": (
                "epsilon: 0.03\njudge_k: 1\njudge_model: judge\njudge_reasoning: xhigh\n"
                "judge_rubric: calibration/judges/rubric.md\n"
                "reference_dir: calibration/reference/book\nresults_tsv: loop/results.tsv\n"
                "scores_dir: loop/scores\ntasks_dir: loop/iterations\nweights:\n" + weights + "\n"),
            "loop/results.tsv": "iter\treward\tverdict\n0\t0.5\tBASELINE\n",
            "prompts/style-guide.md": "style\n", "prompts/chapter-writer.md": "writer\n",
            "prompts/chapter-reviewer.md": "reviewer\n",
            "prompts/master-plan.md": "planner\n",
            "production-books/test/00-brief.md": "brief\n",
            "production-books/test/research/sources/source.txt": "source\n",
            "production-books/test/research/lived-experience.md": "lived\n",
            "production-books/test/research/scientific-evidence.md": "science\n",
            "production-books/test/framing.md": "framing\n",
            "production-books/test/master-plan.md": "### CH-01 — One\n",
            "production-books/test/master-plan-review.md": "review\n",
            "production-books/test/commissions/chapter-01.md": "commission\n",
            "production-books/test/chapters/chapter-01.md": "chapter\n",
            "production-books/second/00-brief.md": "second brief\n",
            "production-books/second/research/sources/source.txt": "second source\n",
            "production-books/second/research/lived-experience.md": "second lived\n",
            "production-books/second/research/scientific-evidence.md": "second science\n",
            "production-books/second/framing.md": "second framing\n",
            "production-books/second/master-plan.md": "### CH-01 — Second\n",
            "production-books/second/master-plan-review.md": "second review\n",
            "production-books/second/commissions/chapter-01.md": "second commission\n",
            "production-books/second/chapters/chapter-01.md": "second chapter\n",
            "calibration/judges/rubric.md": RUBRIC,
            "calibration/reference/book/001.txt": "reference\n",
            "calibration/reference/book/reference-metrics.json": '{"chapters": []}\n'}
        for relative, text in files.items():
            path = accepted / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        PAIR.initialize(accepted, "production-books/test")
        PAIR.snapshot(experiment, accepted, "production-books/test", "1", iteration=1)
        tested = PAIR.seal(experiment)
        view = PAIR.open_sealed(experiment, tested)
        cfg, label = view["config"], "ch01"
        task = judges.emit_tasks(cfg, [(label, "ours", "reference", "context")],
                                  "001", RUBRIC, experiment, tested)[0]
        task_hash = judges._task_binding(task, tested, experiment)
        vpath = task.parents[1] / "verdicts" / f"{label}-j1.json"
        vpath.write_text(json.dumps(verdict(tested, task_hash)), encoding="utf-8")
        aggregate = judges.aggregate(cfg, [label], "001", tested, experiment)
        artifacts = score_receipt.judge_artifacts(cfg, [label], "001", tested, experiment)
        core = {"chapters_checked": [1], "hard_ok": True, "hard_fails": [],
                "checks": {"fixture": True}, "pairs": [(label, "ours", "reference", "context")],
                "pair_root": view["pair"], "evaluation_root": view["evaluation"],
                "rubric_sha256": STORE.sha(Path(cfg["judge_rubric"]).read_bytes())}
        receipt = score_receipt.build(view["manifest"], core, aggregate, artifacts)
        scores = Path(cfg["scores_dir"])
        scores.mkdir(parents=True)
        score = {"tested_pair_hash": tested, "book": str(view["pair"] / "production-books/test"),
                 "hard_ok": True, "hard_fails": [], "reward": aggregate["reward"],
                 "campaign": None, "instrument_version": None,
                 "judges": {"rubric": aggregate}, "receipt": receipt}
        score_path = scores / "iter-001.json"
        score_path.write_text(json.dumps(score), encoding="utf-8")
        return accepted, experiment, tested, view, core, score_path, vpath

    def run_gate(self, accepted, experiment, tested, core):
        ledger = self.root / "tasks.md"
        ledger.write_text("### RF-23 — prose\n\n- Status: `READY`\n", encoding="utf-8")
        argv = ["gate.py", "--iter", "1", "--config",
                str(PAIR.candidate_tree(experiment) / "loop/config.yaml"),
                "--tested-pair-hash", tested, "--accepted-root", str(accepted),
                "--promote-pair", "--redesign-authorized", "--rf-stage", "RF-23",
                "--candidate-root", str(experiment),
                "--decision-timestamp", TIMESTAMP]
        with mock.patch.object(sys, "argv", argv), mock.patch.object(GUARD, "LEDGER", ledger), \
                mock.patch.object(GATE.score_core, "evaluate", return_value=dict(core)):
            GATE.main()

    def test_valid_receipt_promotes_exact_pair(self):
        accepted, experiment, tested, _, core, _, _ = self.fixture("valid")
        with self.assertRaises(SystemExit) as decided:
            self.run_gate(accepted, experiment, tested, core)
        self.assertEqual(0, decided.exception.code)
        self.assertEqual("PROMOTED", PAIR.status(experiment))
        decision = json.loads((experiment / PAIR.DECISION).read_text(encoding="utf-8"))
        self.assertEqual("KEEP", decision["gate_receipt"]["verdict"])
        self.assertTrue(decision["gate_receipt"]["human_promotion_approved"])
        accepted_tree = STORE.current(accepted)[0]
        accepted_history = (accepted_tree / "evaluation/loop/results.tsv").read_text()
        self.assertIn(tested, accepted_history)
        self.assertIn("KEEP", accepted_history)
        next_experiment = accepted / "loop/experiments/iter-002"
        next_experiment.mkdir()
        PAIR.snapshot(next_experiment, accepted, "production-books/test", "1", iteration=2)
        next_tested = PAIR.seal(next_experiment)
        next_view = PAIR.open_sealed(next_experiment, next_tested)
        next_history = Path(next_view["config"]["history_results_tsv"])
        self.assertIn(tested, next_history.read_text())
        self.assertEqual("KEEP", GATE.read_rows(next_history)[-1]["verdict"])

    def test_gate_retry_reuses_exact_canonical_timestamp_and_row(self):
        accepted, experiment, tested, _, core, _, _ = self.fixture("retry")
        with mock.patch.object(GATE.CP, "promote",
                               side_effect=PAIR.PairError("interrupted")):
            with self.assertRaisesRegex(SystemExit, "interrupted"):
                self.run_gate(accepted, experiment, tested, core)
        canonical = (experiment / "gate-decision.json").read_bytes()
        evidence = (experiment / "evidence/results.tsv").read_bytes()
        self.assertEqual("SEALED", PAIR.status(experiment))
        with self.assertRaises(SystemExit) as decided:
            self.run_gate(accepted, experiment, tested, core)
        self.assertEqual(0, decided.exception.code)
        self.assertEqual(canonical, (experiment / "gate-decision.json").read_bytes())
        self.assertEqual(evidence, (experiment / "evidence/results.tsv").read_bytes())
        self.assertEqual("PROMOTED", PAIR.status(experiment))

    def test_edited_hard_ok_or_reward_cannot_promote(self):
        for field, value in (("hard_ok", False), ("reward", 1.0)):
            with self.subTest(field=field):
                accepted, experiment, tested, _, core, score_path, _ = self.fixture(field)
                score = json.loads(score_path.read_text(encoding="utf-8"))
                score[field] = value
                score_path.write_text(json.dumps(score), encoding="utf-8")
                with self.assertRaisesRegex(SystemExit, "decision fields"):
                    self.run_gate(accepted, experiment, tested, core)
                self.assertEqual("SEALED", PAIR.status(experiment))

    def test_failed_gate_writes_rejection_evidence_only(self):
        accepted, experiment, tested, view, core, score_path, _ = self.fixture("reject")
        old_tree, old_id, _ = STORE.current(accepted)
        old_history = (old_tree / "evaluation/loop/results.tsv").read_bytes()
        core["hard_ok"], core["hard_fails"] = False, ["fixture failure"]
        score = json.loads(score_path.read_text(encoding="utf-8"))
        aggregate = score["judges"]["rubric"]
        artifacts = score_receipt.judge_artifacts(
            view["config"], ["ch01"], "001", tested, experiment)
        score.update(hard_ok=False, hard_fails=core["hard_fails"],
                     receipt=score_receipt.build(view["manifest"], core,
                                                 aggregate, artifacts))
        score_path.write_text(json.dumps(score), encoding="utf-8")
        with self.assertRaises(SystemExit) as decided:
            self.run_gate(accepted, experiment, tested, core)
        self.assertEqual(0, decided.exception.code)
        self.assertEqual("REJECTED", PAIR.status(experiment))
        current, current_id, _ = STORE.current(accepted)
        self.assertEqual(old_id, current_id)
        self.assertEqual(old_history, (current / "evaluation/loop/results.tsv").read_bytes())
        evidence = (experiment / "evidence/results.tsv").read_text(encoding="utf-8")
        self.assertIn(tested, evidence)
        self.assertIn("FAIL-HARD", evidence)

    def test_missing_extra_or_stale_verdict_fails_closed(self):
        for mode in ("missing", "extra", "stale"):
            with self.subTest(mode=mode):
                accepted, experiment, tested, _, core, _, vpath = self.fixture(mode)
                if mode == "missing":
                    vpath.unlink()
                elif mode == "extra":
                    (vpath.parent / "extra.json").write_text("{}", encoding="utf-8")
                else:
                    value = json.loads(vpath.read_text(encoding="utf-8"))
                    value["pair_hash"] = "0" * 64
                    vpath.write_text(json.dumps(value), encoding="utf-8")
                with self.assertRaises(SystemExit):
                    self.run_gate(accepted, experiment, tested, core)
                self.assertEqual("SEALED", PAIR.status(experiment))

    def test_complete_view_keeps_second_book_and_adds_new_book_without_reinit(self):
        accepted, _, _, view, _, _, _ = self.fixture("complete")
        paths = {item["path"] for item in view["manifest"]["entries"]}
        self.assertEqual({"prompts/style-guide.md", "prompts/chapter-writer.md",
                          "prompts/chapter-reviewer.md", "prompts/master-plan.md"},
                         {path for path in paths if path.startswith("prompts/")})
        for required in ("prompts/master-plan.md", "production-books/test/00-brief.md",
                         "production-books/test/research/sources/source.txt",
                         "production-books/test/research/lived-experience.md",
                         "production-books/test/research/scientific-evidence.md",
                         "production-books/test/framing.md",
                         "production-books/test/master-plan-review.md",
                         "production-books/test/commissions/chapter-01.md",
                         "production-books/test/chapters/chapter-01.md",
                         "production-books/second/research/sources/source.txt",
                         "production-books/second/master-plan-review.md",
                         "production-books/second/commissions/chapter-01.md",
                         "production-books/second/chapters/chapter-01.md"):
            self.assertIn(required, paths)
        self.assertFalse(any(path.startswith("calibration/") for path in paths))
        old_generation = STORE.current(accepted)[1]
        files = {"00-brief.md": "brief\n", "framing.md": "framing\n",
                 "master-plan.md": "### CH-01 — New\n",
                 "master-plan-review.md": "review\n",
                 "research/sources/source.txt": "source\n",
                 "research/lived-experience.md": "lived\n",
                 "research/scientific-evidence.md": "science\n",
                 "commissions/chapter-01.md": "commission\n",
                 "chapters/chapter-01.md": "chapter\n"}
        for relative, text in files.items():
            path = accepted / "production-books/new-book" / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        PAIR.add_book(accepted, "production-books/new-book")
        self.assertTrue((STORE.state_dir(accepted) / "generations" / old_generation).is_dir())
        experiment = accepted / "loop/experiments/new-book"
        experiment.mkdir()
        manifest = PAIR.snapshot(experiment, accepted, "production-books/new-book", "1")
        new_paths = {item["path"] for item in manifest["entries"]}
        self.assertIn("production-books/new-book/research/sources/source.txt", new_paths)
        self.assertIn("production-books/new-book/commissions/chapter-01.md", new_paths)
        self.assertIn("production-books/second/chapters/chapter-01.md", new_paths)


if __name__ == "__main__":
    unittest.main()
