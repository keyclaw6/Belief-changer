"""Additional RF-02 causal-gate binding and complete-view scenarios."""
import json
import unittest

from scripts.eval.tests import test_pair_binding as binding

PAIR, PRODUCT, STORE = binding.PAIR, binding.PRODUCT, binding.STORE
score_receipt = binding.score_receipt


class PairBindingMoreTests(unittest.TestCase):
    setUp = binding.PairBindingTests.setUp
    tearDown = binding.PairBindingTests.tearDown
    product_row = staticmethod(binding.PairBindingTests.product_row)
    write_causal = binding.PairBindingTests.write_causal
    fixture = binding.PairBindingTests.fixture
    run_gate = binding.PairBindingTests.run_gate

    def test_inconclusive_product_decision_never_promotes(self):
        accepted, experiment, tested, view, core, score_path, _ = self.fixture("inconclusive")
        carr = json.loads(score_path.read_text())["judges"]["rubric"]
        self.write_causal(view, tested, core, carr, disagree=True)
        with self.assertRaises(SystemExit) as decided:
            self.run_gate(accepted, experiment, tested, core)
        self.assertEqual(0, decided.exception.code)
        self.assertEqual("REJECTED", PAIR.status(experiment))
        self.assertEqual("INCONCLUSIVE", json.loads(
            (experiment / PAIR.DECISION).read_text())["gate_receipt"]["verdict"])

    def test_failed_gate_writes_rejection_evidence_only(self):
        accepted, experiment, tested, view, core, score_path, _ = self.fixture("reject")
        old_tree, old_id, _ = STORE.current(accepted)
        old_history = (old_tree / "evaluation/loop/causal-bundle-results.jsonl").read_bytes()
        core["hard_ok"], core["hard_fails"] = False, ["fixture failure"]
        core["checks"]["originality"]["tripped"] = True
        score = json.loads(score_path.read_text(encoding="utf-8"))
        aggregate = score["judges"]["rubric"]
        artifacts = score_receipt.judge_artifacts(
            view["config"], ["ch01"], "001", tested, experiment)
        score.update(hard_ok=False, hard_fails=core["hard_fails"],
                     receipt=score_receipt.build(view["manifest"], core,
                                                 aggregate, artifacts))
        score_path.write_text(json.dumps(score), encoding="utf-8")
        self.write_causal(view, tested, core, aggregate)
        with self.assertRaises(SystemExit) as decided:
            self.run_gate(accepted, experiment, tested, core)
        self.assertEqual(0, decided.exception.code)
        self.assertEqual("REJECTED", PAIR.status(experiment))
        current, current_id, _ = STORE.current(accepted)
        self.assertEqual(old_id, current_id)
        current_history = current / "evaluation/loop/causal-bundle-results.jsonl"
        self.assertEqual(old_history, current_history.read_bytes())
        evidence = (experiment / "evidence/loop/causal-bundle-results.jsonl").read_text()
        self.assertIn(tested, evidence)
        self.assertIn("REFUTED", evidence)

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
        required = ("prompts/master-plan.md", "production-books/test/00-brief.md",
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
                    "production-books/second/chapters/chapter-01.md")
        for path in required:
            self.assertIn(path, paths)
        self.assertFalse(any(path.startswith("calibration/") for path in paths))
        old_generation = STORE.current(accepted)[1]
        files = {"00-brief.md": "brief\n", "framing.md": "framing\n",
                 "master-plan.md": "### CH-01 — New\n", "master-plan-review.md": "review\n",
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
