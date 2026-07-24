"""RF-02 gate receipt binds every decision input and judge artifact."""
import json, sys, tempfile, unittest
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
import product_decision as PRODUCT  # noqa: E402
import experiment_record as RECORD  # noqa: E402

RUBRIC = "{{REFERENCE}}\n{{CANDIDATE}}\n{{CONTEXT}}\n"
TIMESTAMP = "2026-07-14T12:00:00+00:00"
RESEARCH_SEAL = "9" * 64


def verdict(pair_hash, task_hash):
    return {"pair_hash": pair_hash, "task_hash": task_hash,
            "scores": {dimension: 5 for dimension in judges.DIMS},
            "worst_dimension": judges.DIMS[0], "gap_summary": "fixture",
            "suggestions": [
                {"owner": "framing", "suggestion": "first"},
                {"owner": "prose", "suggestion": "second"},
                {"owner": "plan", "suggestion": "third"}]}


class PairBindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    @staticmethod
    def research_report(book, require_seal=True):
        del require_seal
        experiment = Path(book).parents[2]
        seal = "8" * 64 if experiment.name.endswith("-control") else RESEARCH_SEAL
        return {"ok": True, "seal_identity": seal}

    @staticmethod
    def research_preflight(root):
        control = Path(root).name.endswith("-control")
        return {"frozen_variables": {name: STORE.state_hash(name)
                    for name in RECORD.FROZEN_FOR_RESEARCH},
                "research_bundle": {"components": {
                    "prompts/research-agent.md": STORE.sha(
                        ("control prompt\n" if control else
                         "treatment prompt\n").encode()),
                    "prompts/research-evidence-editor.md": STORE.sha(
                        b"frozen editor\n"),
                    "loop/config.yaml#research": STORE.state_hash("config")}}}

    @staticmethod
    def product_row(tested, prefix, index, family):
        row = {"raw_verdict_id": f"raw-{prefix}-{index}",
               "actor": f"judge-{prefix}-{index}", "kind": "model",
               "family": family, "verdict": "PASS", "scope": "ordinary_product",
               "promotion_eligible": True,
               "base_task_sha256": STORE.state_hash(prefix),
               "tested_pair_hash": tested, "prompt_sha256": None,
               "input_sha256": STORE.state_hash(f"input-{prefix}")}
        row["task_id"] = PRODUCT.bound_task_id(row)
        return row

    def write_causal(self, view, tested, core, carr, disagree=False):
        prompt_hash = STORE.sha(Path(view["config"]["product_effect_rubric"]).read_bytes())
        evidence = {"schema": 1, "tested_pair_hash": tested,
                    "blind_chapter_effect": [self.product_row(
                        tested, "effect", 1, "openai"), self.product_row(
                        tested, "effect", 2, "anthropic")],
                    "blind_whole_opening_sequence": [self.product_row(
                        tested, "sequence", 1, "openai"), self.product_row(
                        tested, "sequence", 2, "anthropic")]}
        for rows in (evidence["blind_chapter_effect"],
                     evidence["blind_whole_opening_sequence"]):
            for row in rows:
                row["prompt_sha256"] = prompt_hash
                row["task_id"] = PRODUCT.bound_task_id(row)
        if disagree:
            evidence["blind_chapter_effect"][1]["verdict"] = "FAIL"
        product = PRODUCT.decide(
            core=core, grounded_review={"state": "PASSED"},
            developmental_review={"state": "PASS"},
            chapter_effect=evidence["blind_chapter_effect"],
            whole_opening_sequence=evidence["blind_whole_opening_sequence"],
            carr_craft=carr, tested_pair_hash=tested, prompt_sha256=prompt_hash)
        product_hash = STORE.state_hash(product)
        record = {"schema": 2, "surface": "writing",
                  "hypothesis": "linked bundle improves the opening",
                  "causal_chain": ["reader state focuses commission", "draft enacts discovery"],
                  "changed_bundle": ["planning:reader-state card", "commission:handoff"],
                  "frozen_variables": {
                      "accepted_research_seal_sha256": RESEARCH_SEAL},
                  "inputs": {"tested_pair_hash": tested,
                             "product_decision_sha256": product_hash},
                  "evidence": RECORD.decision_evidence(product),
                  "research": {"control_seal_sha256": RESEARCH_SEAL,
                               "treatment_seal_sha256": RESEARCH_SEAL},
                  "decision": {"PROMOTE": "SUPPORTED", "REJECT": "REFUTED",
                               "INCONCLUSIVE": "INCONCLUSIVE"}[product["decision"]],
                  "falsifier": "Reject if integrity, effect, or sequence fails."}
        evidence_root = view["evidence"]
        (evidence_root / PRODUCT.EVIDENCE_PATH).write_text(
            json.dumps(evidence), encoding="utf-8")
        (evidence_root / RECORD.PATH).write_text(json.dumps(record), encoding="utf-8")

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
                "product_effect_rubric: calibration/judges/product.md\n"
                "product_effect_absolute_rubric: calibration/judges/absolute.md\n"
                "causal_results_jsonl: loop/causal-bundle-results.jsonl\n"
                "reference_dir: calibration/reference/book\nresults_tsv: loop/results.tsv\n"
                "scores_dir: loop/scores\ntasks_dir: loop/iterations\nweights:\n" + weights + "\n"),
            "loop/results.tsv": "iter\treward\tverdict\n0\t0.5\tBASELINE\n",
            "loop/causal-bundle-results.jsonl": (ROOT / "loop/causal-bundle-results.jsonl").read_text(),
            "prompts/style-guide.md": "style\n", "prompts/chapter-writer.md": "writer\n",
            "prompts/chapter-reviewer.md": "reviewer\n",
            "prompts/master-plan.md": "planner\n",
            "production-books/test/00-brief.md": "brief\n",
            "production-books/test/research/sources/source.txt": "source\n",
            "production-books/test/research/lived-experience.md": "lived\n",
            "production-books/test/research/scientific-evidence.md": "science\n",
            "production-books/test/research/research-coverage.json": "{}\n",
            "production-books/test/research/research-review.json": "{}\n",
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
            "calibration/judges/product.md": "Blind product effect\n{{TASK}}\n",
            "calibration/judges/absolute.md": "Blind absolute effect\n{{TASK}}\n",
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
        # Infra: both product-effect contracts are sealed evaluation inputs.
        self.assertEqual("Blind product effect\n{{TASK}}\n", Path(
            view["config"]["product_effect_rubric"]).read_text())
        self.assertEqual("Blind absolute effect\n{{TASK}}\n", Path(
            view["config"]["product_effect_absolute_rubric"]).read_text())
        cfg, label = view["config"], "ch01"
        with mock.patch.object(judges.FB, "require_frozen_batch"), \
                mock.patch.object(judges.GR, "require_complete"), \
                mock.patch.object(judges.DR, "require_developmental_pass"):
            task = judges.emit_tasks(cfg, [(label, "ours", "reference", "context")],
                                      "001", RUBRIC, experiment, tested)[0]
        task_hash = judges._task_binding(task, tested, experiment)
        vpath = task.parents[1] / "verdicts" / f"{label}-j1.json"
        vpath.write_text(json.dumps(verdict(tested, task_hash)), encoding="utf-8")
        aggregate = judges.aggregate(cfg, [label], "001", tested, experiment)
        artifacts = score_receipt.judge_artifacts(cfg, [label], "001", tested, experiment)
        core = {"chapters_checked": [1], "hard_ok": True, "hard_fails": [],
                "checks": {"originality": {"tripped": False},
                           "near_copy": [{"ratio": 0.1, "tripwire": 0.5}],
                           "mantra": {"failures": []}, "length": [{"ok": True}],
                           "repetition_within": {"hard_fails": []}},
                "pairs": [(label, "ours", "reference", "context")],
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
        self.write_causal(view, tested, core, aggregate)
        return accepted, experiment, tested, view, core, score_path, vpath

    def run_gate(self, accepted, experiment, tested, core, approve=True):
        ledger = self.root / "tasks.md"
        ledger.write_text("### RF-23 — prose\n\n- Status: `READY`\n", encoding="utf-8")
        argv = ["gate.py", "--iter", "1", "--config",
                str(PAIR.candidate_tree(experiment) / "loop/config.yaml"),
                "--tested-pair-hash", tested, "--accepted-root", str(accepted),
                "--redesign-authorized", "--rf-stage", "RF-23",
                "--candidate-root", str(experiment),
                "--decision-timestamp", TIMESTAMP]
        if approve:
            argv.append("--promote-pair")
        with mock.patch.object(sys, "argv", argv), mock.patch.object(GUARD, "LEDGER", ledger), \
                mock.patch.object(GATE.RC, "research_seal_identity",
                                  return_value=RESEARCH_SEAL), \
                mock.patch.object(GATE.score_core, "evaluate", return_value=dict(core)), \
                mock.patch.object(GATE.FB, "require_frozen_batch"), \
                mock.patch.object(GATE.GR, "require_complete",
                                  return_value={"state": "PASSED"}), \
                mock.patch.object(GATE.DR, "require_developmental_pass",
                                  return_value={"state": "PASS"}):
            GATE.main()

    def write_research_causal(self, view, decision="SUPPORTED"):
        treatment = view["pair"].parent
        accepted = treatment.parents[2]
        control = treatment.parent / (treatment.name + "-control")
        control.mkdir()
        PAIR.snapshot(control, accepted, "production-books/test", "1", iteration=1)
        control_seal = "8" * 64
        frozen = {name: STORE.state_hash(name)
                  for name in RECORD.FROZEN_FOR_RESEARCH}
        declaration = {"schema": 2, "surface": "research",
            "hypothesis": "A research-only prompt improves the accepted corpus.",
            "causal_chain": ["prompt changes discovery", "discovery changes coverage"],
            "changed_bundle": ["research:prompts/research-agent.md"],
            "frozen_variables": frozen,
            "inputs": {"control_candidate_root": str(control),
                       "treatment_candidate_root": str(treatment)},
            "falsifier": "A hard gate or blinded comparison fails.",
            "research_bundle": {"prompts/research-agent.md": "treatment prompt\n"},
            "downstream_effect": {"required": False, "task_sha256": None,
                                  "receipt_path": None}}
        declaration_sha = STORE.state_hash(declaration)
        anchors = {}
        for name, root, seal in (("control", control, control_seal),
                                 ("treatment", treatment, RESEARCH_SEAL)):
            book = PAIR.candidate_tree(root) / "production-books/test"
            anchors[name] = {"seal_sha256": seal,
                "coverage_sha256": STORE.sha(
                    (book / "research/research-coverage.json").read_bytes()),
                "review_sha256": STORE.sha(
                    (book / "research/research-review.json").read_bytes())}
        hard = {"schema": 1, "control_seal_sha256": control_seal,
                "treatment_seal_sha256": RESEARCH_SEAL,
                "gates": {name: STORE.state_hash({"gate": name, "arms": anchors})
                          for name in sorted(RECORD.RESEARCH_HARD_GATES)}}
        preferred = "B" if decision == "SUPPORTED" else (
            "A" if decision == "REFUTED" else "TIE")
        task = RECORD.research_comparison_task(declaration,
            {"A": control_seal, "B": RESEARCH_SEAL},
            {"A": RECORD.research_candidate(
                PAIR.candidate_tree(control) / "production-books/test"),
             "B": RECORD.research_candidate(
                PAIR.candidate_tree(treatment) / "production-books/test")})
        verdict = {"schema": 1, "task_sha256": task["task_sha256"],
                   "preferred": preferred,
                   "decisive_reason": "fixture hypothesis-specific difference"}
        native = {"task_sha256": task["task_sha256"], "verdict": verdict,
            "model": RECORD.RESEARCH_JUDGE_MODEL,
            "reasoning": RECORD.RESEARCH_JUDGE_REASONING,
            "thread_id": "fresh-fixture-thread", "command": ["codex", "exec"],
            "kind": "native-codex-subscription",
            "judge_identity": "research-quality-independent",
            "fresh_ephemeral_context": True,
            "input_sha256": STORE.sha(
                RECORD.research_comparison_prompt(task).encode()),
            "output_schema_sha256": STORE.sha(
                RECORD.research_comparison_schema_bytes())}
        comparison = {"schema": 1, "task_sha256": task["task_sha256"],
            "preferred": preferred, "treatment_candidate": "B",
            "hypothesis_outcome": decision,
            "verdict_sha256": STORE.state_hash(verdict),
            "native_record_sha256": STORE.state_hash(native),
            "native_binding": {"kind": "native-codex-subscription",
                "judge_identity": "research-quality-independent",
                "fresh_ephemeral_context": True,
                "input_sha256": native["input_sha256"],
                "output_schema_sha256": native["output_schema_sha256"]}}
        authority = {"control_seal_sha256": control_seal,
            "treatment_seal_sha256": RESEARCH_SEAL,
            "hard_gate_receipt_sha256": STORE.state_hash(hard),
            "comparison_task_sha256": comparison["task_sha256"],
            "comparison_receipt_sha256": STORE.state_hash(comparison),
            "downstream_effect_required": False,
            "downstream_effect_receipt_sha256": None}
        record = {"schema": 2, "surface": "research",
            "hypothesis": declaration["hypothesis"],
            "causal_chain": declaration["causal_chain"],
            "changed_bundle": declaration["changed_bundle"],
            "frozen_variables": frozen,
            "inputs": {"control_candidate_root": str(control),
                       "treatment_candidate_root": str(treatment),
                       "research_declaration_sha256": declaration_sha},
            "evidence": {"integrity": authority["hard_gate_receipt_sha256"],
                "reader_effect": authority["comparison_receipt_sha256"],
                "whole_opening_sequence": "NOT_REQUIRED",
                "carr_craft_diagnostic": "NOT_APPLICABLE: research surface"},
            "research": authority, "decision": decision,
            "falsifier": declaration["falsifier"]}
        RECORD.bind_research_evidence(record, {"hard_gates": hard,
            "comparison": comparison, "downstream_effect": None})
        base = view["evidence"] / "research-causal"
        base.mkdir(parents=True, exist_ok=True)
        for name, value in (("declaration.json", declaration),
                            ("hard-gates.json", hard),
                            ("comparison-receipt.json", comparison),
                            ("comparison.marker.json", {"schema": 1,
                                "task_sha256": task["task_sha256"],
                                "treatment_candidate": "B", "task": task}),
                            ("comparison.result.json", {"schema": 1,
                                "task_sha256": task["task_sha256"], "native": native,
                                "native_record_sha256": STORE.state_hash(native)}),
                            ("causal-record.json", record)):
            (base / name).write_text(json.dumps(value), encoding="utf-8")
        return base

    def test_valid_receipt_promotes_exact_pair(self):
        accepted, experiment, tested, _, core, _, _ = self.fixture("valid")
        with self.assertRaises(SystemExit) as decided:
            self.run_gate(accepted, experiment, tested, core)
        self.assertEqual(0, decided.exception.code)
        self.assertEqual("PROMOTED", PAIR.status(experiment))
        decision = json.loads((experiment / PAIR.DECISION).read_text(encoding="utf-8"))
        self.assertEqual("PROMOTE", decision["gate_receipt"]["verdict"])
        self.assertTrue(decision["gate_receipt"]["human_promotion_approved"])
        accepted_tree = STORE.current(accepted)[0]
        accepted_history = (accepted_tree / "evaluation/loop/causal-bundle-results.jsonl").read_text()
        self.assertIn(tested, accepted_history)
        self.assertIn("SUPPORTED", accepted_history)
        next_experiment = accepted / "loop/experiments/iter-002"
        next_experiment.mkdir()
        PAIR.snapshot(next_experiment, accepted, "production-books/test", "1", iteration=2)
        next_tested = PAIR.seal(next_experiment)
        next_view = PAIR.open_sealed(next_experiment, next_tested)
        next_history = Path(next_view["config"]["history_causal_results_jsonl"])
        self.assertIn(tested, next_history.read_text())
        self.assertEqual("SUPPORTED", RECORD.load(next_history)[-1]["decision"])

    def test_gate_retry_reuses_exact_canonical_timestamp_and_row(self):
        accepted, experiment, tested, _, core, _, _ = self.fixture("retry")
        with mock.patch.object(GATE.CP, "promote",
                               side_effect=PAIR.PairError("interrupted")):
            with self.assertRaisesRegex(SystemExit, "interrupted"):
                self.run_gate(accepted, experiment, tested, core)
        canonical = (experiment / "gate-decision.json").read_bytes()
        evidence = (experiment / "evidence/loop/causal-bundle-results.jsonl").read_bytes()
        self.assertEqual("SEALED", PAIR.status(experiment))
        with self.assertRaises(SystemExit) as decided:
            self.run_gate(accepted, experiment, tested, core)
        self.assertEqual(0, decided.exception.code)
        self.assertEqual(canonical, (experiment / "gate-decision.json").read_bytes())
        self.assertEqual(evidence, (experiment / "evidence/loop/causal-bundle-results.jsonl").read_bytes())
        self.assertEqual("PROMOTED", PAIR.status(experiment))

    def test_edited_hard_ok_or_reward_cannot_promote(self):
        for field, value in (("hard_ok", False), ("reward", 0.0)):
            with self.subTest(field=field):
                accepted, experiment, tested, _, core, score_path, _ = self.fixture(field)
                score = json.loads(score_path.read_text(encoding="utf-8"))
                score[field] = value
                score_path.write_text(json.dumps(score), encoding="utf-8")
                with self.assertRaisesRegex(SystemExit, "Carr diagnostic fields"):
                    self.run_gate(accepted, experiment, tested, core)
                self.assertEqual("SEALED", PAIR.status(experiment))

    def test_product_record_and_atomic_approval_are_all_required(self):
        for mode in ("missing", "stale-record", "unapproved"):
            with self.subTest(mode=mode):
                accepted, experiment, tested, view, core, _, _ = self.fixture(mode)
                if mode == "missing":
                    (view["evidence"] / PRODUCT.EVIDENCE_PATH).unlink()
                elif mode == "stale-record":
                    path = view["evidence"] / RECORD.PATH
                    value = json.loads(path.read_text())
                    value["inputs"]["product_decision_sha256"] = "0" * 64
                    path.write_text(json.dumps(value), encoding="utf-8")
                with self.assertRaises(SystemExit):
                    self.run_gate(accepted, experiment, tested, core,
                                  approve=mode != "unapproved")
                self.assertEqual("SEALED", PAIR.status(experiment))

    def test_new_writing_gate_rejects_legacy_record_without_research_freeze(self):
        accepted, experiment, tested, view, core, _, _ = self.fixture("legacy-writing")
        path = view["evidence"] / RECORD.PATH
        value = json.loads(path.read_text(encoding="utf-8"))
        for key in ("schema", "surface", "research"):
            value.pop(key)
        value["changed_bundle"] = ["research:prompt", "writing:prompt"]
        value["frozen_variables"] = {"route": "fixed"}
        path.write_text(json.dumps(value), encoding="utf-8")
        with self.assertRaisesRegex(SystemExit, "schema-2 writing surface"):
            self.run_gate(accepted, experiment, tested, core)
        self.assertEqual("SEALED", PAIR.status(experiment))

    def test_research_result_uses_existing_atomic_human_gate(self):
        accepted, experiment, tested, view, _core, _, _ = self.fixture("research-gate")
        self.write_research_causal(view)
        with mock.patch.object(GATE.RC, "inspect_research",
                               side_effect=self.research_report), \
                mock.patch.object(GATE.RF, "preflight",
                                  side_effect=self.research_preflight), \
                mock.patch.object(GATE.RF, "require_control_baseline",
                                  side_effect=self.research_preflight), \
                self.assertRaisesRegex(SystemExit, "explicit named-human"):
            GATE._research_gate(experiment, view, tested, accepted, False, TIMESTAMP)
        self.assertEqual("SEALED", PAIR.status(experiment))
        self.assertFalse((experiment / "gate-decision.json").exists())
        record = json.loads((view["evidence"] /
            "research-causal/causal-record.json").read_text())
        evidence = {"hard_gates": json.loads((view["evidence"] /
                "research-causal/hard-gates.json").read_text()),
            "comparison": json.loads((view["evidence"] /
                "research-causal/comparison-receipt.json").read_text()),
            "downstream_effect": None}
        approval = {"schema": 1, "reviewer_name": "Kristian Bilstrup",
            "reviewer_role": "named-human", "decision": "PROMOTE",
            "approved_at_utc": TIMESTAMP, "tested_pair_hash": tested,
            "causal_record_sha256": STORE.sha(RECORD.record_bytes(record)),
            "research_evidence_sha256": STORE.state_hash(evidence),
            "control_seal_sha256": record["research"]["control_seal_sha256"],
            "treatment_seal_sha256": record["research"]["treatment_seal_sha256"]}
        approval_path = experiment / GATE.GD.RESEARCH_APPROVAL
        approval_path.parent.mkdir(parents=True, exist_ok=True)
        approval_path.write_text(json.dumps(approval), encoding="utf-8")
        with mock.patch.object(GATE.RC, "inspect_research",
                               side_effect=self.research_report), \
                mock.patch.object(GATE.RF, "preflight",
                                  side_effect=self.research_preflight), \
                mock.patch.object(GATE.RF, "require_control_baseline",
                                  side_effect=self.research_preflight):
            GATE._research_gate(experiment, view, tested, accepted, True, TIMESTAMP)
        self.assertEqual("PROMOTED", PAIR.status(experiment))
        receipt = json.loads((experiment / "gate-decision.json").read_text())
        self.assertEqual((3, "PROMOTE", True),
                         (receipt["schema"], receipt["verdict"],
                          receipt["human_promotion_approved"]))
        accepted_history = (STORE.current(accepted)[0] /
            "evaluation/loop/causal-bundle-results.jsonl").read_text()
        self.assertEqual("research", RECORD.load(
            STORE.current(accepted)[0] /
            "evaluation/loop/causal-bundle-results.jsonl")[-1]["surface"])
        self.assertIn("SUPPORTED", accepted_history)

    def test_research_gate_rejects_tampered_evidence_and_stale_seal(self):
        for mode in ("evidence", "seal"):
            with self.subTest(mode=mode):
                accepted, experiment, tested, view, _core, _, _ = self.fixture(
                    "research-" + mode)
                base = self.write_research_causal(view)
                seal = RESEARCH_SEAL
                if mode == "evidence":
                    hard = json.loads((base / "hard-gates.json").read_text())
                    hard["gates"]["privacy"] = "0" * 64
                    (base / "hard-gates.json").write_text(json.dumps(hard))
                else:
                    seal = "0" * 64
                def report(book, require_seal=True):
                    value = self.research_report(book, require_seal)
                    if mode == "seal" and not Path(book).parents[2].name.endswith("-control"):
                        value["seal_identity"] = seal
                    return value
                with mock.patch.object(GATE.RC, "inspect_research",
                                       side_effect=report), \
                        mock.patch.object(GATE.RF, "preflight",
                                          side_effect=self.research_preflight), \
                        mock.patch.object(GATE.RF, "require_control_baseline",
                                          side_effect=self.research_preflight), \
                        self.assertRaises(SystemExit):
                    GATE._research_gate(
                        experiment, view, tested, accepted, True, TIMESTAMP)
                self.assertEqual("SEALED", PAIR.status(experiment))
                self.assertFalse((experiment / "gate-decision.json").exists())

    def test_research_gate_rejects_control_baseline_drift(self):
        """OpenSpec scenario: Research promotion rechecks the accepted control bytes."""
        accepted, experiment, tested, view, _core, _, _ = self.fixture(
            "research-control-drift")
        self.write_research_causal(view)
        with mock.patch.object(GATE.RC, "inspect_research",
                               side_effect=self.research_report), \
                mock.patch.object(GATE.RF, "preflight",
                                  side_effect=self.research_preflight), \
                mock.patch.object(GATE.RF, "require_control_baseline",
                                  side_effect=GATE.RF.ResearchBlocked(
                                      "control research component differs from accepted baseline")), \
                self.assertRaisesRegex(SystemExit, "differs from accepted baseline"):
            GATE._research_gate(
                experiment, view, tested, accepted, False, TIMESTAMP)
        self.assertEqual("SEALED", PAIR.status(experiment))
        self.assertFalse((experiment / "gate-decision.json").exists())

if __name__ == "__main__":
    unittest.main()
