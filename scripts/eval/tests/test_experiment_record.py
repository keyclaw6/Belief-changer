"""RF-19 minimal causal-bundle record regressions."""
import copy
import json
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
import experiment_record as RECORD  # noqa: E402


class ExperimentRecordTests(unittest.TestCase):
    def setUp(self):
        self.records = RECORD.load(ROOT / "loop/causal-bundle-results.jsonl")

    def test_dry_run_is_one_minimal_causal_bundle(self):
        """OpenSpec requirement: Minimal experiment record."""
        self.assertEqual(1, len(self.records))
        record = self.records[0]
        self.assertEqual(RECORD.FIELDS, set(record))
        self.assertEqual(RECORD.EVIDENCE, set(record["evidence"]))
        self.assertEqual("DRY_RUN", record["decision"])
        self.assertTrue(record["causal_chain"])
        self.assertTrue(record["changed_bundle"])

    def test_old_reward_or_missing_layer_cannot_enter_lineage(self):
        """OpenSpec scenario: The experiment record grows beyond decision evidence."""
        reward = copy.deepcopy(self.records[0])
        reward["reward"] = 0.99
        with self.assertRaisesRegex(RECORD.RecordError, "minimal RF-19 schema"):
            RECORD.validate(reward)
        missing = copy.deepcopy(self.records[0])
        del missing["evidence"]["whole_opening_sequence"]
        with self.assertRaisesRegex(RECORD.RecordError, "four product layers"):
            RECORD.validate(missing)

    def test_record_requires_one_linked_hypothesis_and_falsifier(self):
        """OpenSpec requirement: Causal-bundle experiment."""
        for key in ("hypothesis", "falsifier"):
            with self.subTest(field=key):
                invalid = copy.deepcopy(self.records[0])
                invalid[key] = " "
                with self.assertRaises(RECORD.RecordError):
                    RECORD.validate(invalid)
        duplicate = copy.deepcopy(self.records[0])
        duplicate["changed_bundle"].append(duplicate["changed_bundle"][0])
        with self.assertRaisesRegex(RECORD.RecordError, "duplicates"):
            RECORD.validate(duplicate)

    def test_runbook_orders_reused_factory_stages(self):
        """OpenSpec requirement: Causal-bundle experiment."""
        runbook = (ROOT / "PROGRAM.md").read_text(encoding="utf-8")
        stages = (
            "Candidate isolation", "Generation", "Frozen batch",
            "Grounded review", "Developmental review", "Blind evaluation",
            "Owner routing", "Decision", "Atomic promotion",
        )
        positions = [runbook.index(f"**{stage}**") for stage in stages]
        self.assertEqual(sorted(positions), positions)
        self.assertIn("Never\ncompare their rewards numerically", runbook)

    def _v2(self, surface):
        value = copy.deepcopy(self.records[0])
        seal = "a" * 64
        value.update(schema=2, surface=surface)
        if surface == "research":
            value["changed_bundle"] = ["research:query-and-coverage-plan"]
            value["frozen_variables"] = {
                name: f"frozen-{name}" for name in RECORD.FROZEN_FOR_RESEARCH
            }
            value["research"] = {
                "control_seal_sha256": seal,
                "treatment_seal_sha256": "b" * 64,
                "hard_gate_receipt_sha256": "c" * 64,
                "comparison_task_sha256": "d" * 64,
                "comparison_receipt_sha256": "e" * 64,
                "downstream_effect_required": False,
                "downstream_effect_receipt_sha256": None,
            }
            value["inputs"]["research_declaration_sha256"] = "9" * 64
        else:
            value["changed_bundle"] = ["writing:compact-authority"]
            value["frozen_variables"]["accepted_research_seal_sha256"] = seal
            value["research"] = {
                "control_seal_sha256": seal, "treatment_seal_sha256": seal,
            }
        return value

    def test_v2_declares_isolated_research_or_writing_surface(self):
        """OpenSpec scenarios: Research/writing treatment preparation."""
        for surface in ("research", "writing"):
            with self.subTest(surface=surface):
                value = self._v2(surface)
                self.assertIs(value, RECORD.validate(value))
        self.assertEqual(RECORD.FIELDS, set(self.records[0]))

    def test_surface_rejects_mixed_bundle_or_unfrozen_research(self):
        """OpenSpec scenario: A purported causal decision mixes changes."""
        mixed = self._v2("research")
        mixed["changed_bundle"].append("writing:prompt")
        with self.assertRaisesRegex(RECORD.RecordError, "mixes"):
            RECORD.validate(mixed)
        unfrozen = self._v2("research")
        del unfrozen["frozen_variables"]["evaluation"]
        with self.assertRaisesRegex(RECORD.RecordError, "does not freeze evaluation"):
            RECORD.validate(unfrozen)
        missing_receipt = self._v2("research")
        del missing_receipt["research"]["hard_gate_receipt_sha256"]
        with self.assertRaisesRegex(RECORD.RecordError, "authority fields"):
            RECORD.validate(missing_receipt)

    def test_writing_surface_requires_the_same_accepted_research_seal(self):
        """OpenSpec scenario: A writing treatment is prepared."""
        different = self._v2("writing")
        different["research"]["treatment_seal_sha256"] = "b" * 64
        with self.assertRaisesRegex(RECORD.RecordError, "same accepted research seal"):
            RECORD.validate(different)
        stale = self._v2("writing")
        stale["frozen_variables"]["accepted_research_seal_sha256"] = "c" * 64
        with self.assertRaisesRegex(RECORD.RecordError, "do not bind"):
            RECORD.validate(stale)

    def test_supported_research_record_requires_bound_receipts(self):
        """OpenSpec scenario: A research treatment is prepared for comparison."""
        record = self._v2("research")
        record["decision"] = "SUPPORTED"
        hard = {"schema": 1,
            "control_seal_sha256": record["research"]["control_seal_sha256"],
            "treatment_seal_sha256": record["research"]["treatment_seal_sha256"],
            "gates": {name: f"{index:064x}" for index, name in
                      enumerate(sorted(RECORD.RESEARCH_HARD_GATES), 1)}}
        comparison = {"schema": 1,
            "task_sha256": record["research"]["comparison_task_sha256"],
            "preferred": "B", "treatment_candidate": "B",
            "hypothesis_outcome": "SUPPORTED",
            "verdict_sha256": "f" * 64, "native_record_sha256": "1" * 64,
            "native_binding": {"kind": "native-codex-subscription",
                "judge_identity": "research-quality-independent",
                "fresh_ephemeral_context": True, "input_sha256": "2" * 64,
                "output_schema_sha256": "3" * 64}}
        record["research"]["hard_gate_receipt_sha256"] = RECORD.PS.state_hash(hard)
        record["research"]["comparison_receipt_sha256"] = RECORD.PS.state_hash(comparison)
        evidence = {"hard_gates": hard, "comparison": comparison,
                    "downstream_effect": None}
        self.assertIs(record, RECORD.bind_research_evidence(record, evidence))
        with self.assertRaisesRegex(RECORD.RecordError,
                                    "lacks bound causal evidence receipts"):
            RECORD.bind(record, {}, "2" * 64, "3" * 64)
        forged = copy.deepcopy(evidence)
        forged["hard_gates"]["gates"]["privacy"] = "0" * 64
        with self.assertRaisesRegex(RECORD.RecordError, "hard-gate receipt hash is stale"):
            RECORD.bind_research_evidence(record, forged)

    def test_existing_causal_path_calls_only_named_production_research_facade(self):
        """OpenSpec scenario: A research treatment is prepared for comparison."""
        sys.path.insert(0, str(ROOT / "scripts/eval"))
        import run_iteration as run  # noqa: E402
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).absolute()
            control, treatment = root / "control", root / "treatment"
            declaration = {
                "schema": 2, "surface": "research",
                "hypothesis": "A coverage-plan change improves accepted research.",
                "causal_chain": ["plan changes discovery", "discovery changes coverage"],
                "changed_bundle": ["research:prompts/research-agent.md"],
                "frozen_variables": {
                    name: f"{index:064x}" for index, name in
                    enumerate(sorted(RECORD.FROZEN_FOR_RESEARCH), 1)
                },
                "inputs": {"control_candidate_root": str(control),
                           "treatment_candidate_root": str(treatment)},
                "research_bundle": {"prompts/research-agent.md": "treatment prompt\n"},
                "downstream_effect": {"required": False, "task_sha256": None,
                                      "receipt_path": None},
                "falsifier": "The treatment fails a hard gate.",
            }
            path = root / "declaration.json"
            path.write_text(json.dumps(declaration), encoding="utf-8")
            fake = types.ModuleType("research_factory")
            fake.start_experiment = mock.Mock(side_effect=("a" * 64, "b" * 64))
            fake.completed_experiment = mock.Mock(return_value=None)
            fake.advance = mock.Mock()
            roots = {"control": control, "treatment": treatment}
            expected = declaration["frozen_variables"]
            identity = {"frozen_variables": expected,
                        "run": {"config": "loop/config.yaml"},
                        "research_bundle": {"components": {
                            "prompts/research-agent.md": "a" * 64}}}
            comparison = {"schema": 1, "task_sha256": "d" * 64,
                "preferred": "B", "treatment_candidate": "B",
                "hypothesis_outcome": "SUPPORTED",
                "verdict_sha256": "e" * 64, "native_record_sha256": "f" * 64,
                "native_binding": {"kind": "native-codex-subscription",
                    "judge_identity": "research-quality-independent",
                    "fresh_ephemeral_context": True, "input_sha256": "1" * 64,
                    "output_schema_sha256": "2" * 64}}
            hard = {"schema": 1, "control_seal_sha256": "a" * 64,
                    "treatment_seal_sha256": "b" * 64,
                    "gates": {name: f"{index:064x}" for index, name in
                              enumerate(sorted(RECORD.RESEARCH_HARD_GATES), 1)}}
            with mock.patch.dict(sys.modules, {"research_factory": fake}), \
                    mock.patch.dict("os.environ", {"OPENROUTER_API_KEY": "fixture"},
                                    clear=True), \
                    mock.patch.object(run, "_prepare_research_arms", return_value=roots), \
                    mock.patch.object(run, "_research_preflight_identity",
                                      return_value={"control": identity,
                                                    "treatment": identity}), \
                    mock.patch.object(run, "_research_hard_gates",
                                      return_value=(hard, {})), \
                    mock.patch.object(run, "_research_comparison",
                                      return_value=comparison), \
                    mock.patch.object(run, "_persist_research_causal"), \
                    mock.patch.object(run.CP, "load",
                                      return_value={"state": "CANDIDATE"}), \
                    mock.patch.object(run.CP, "seal", return_value="c" * 64):
                result = run._research_treatment(path, root, "book", "1-3", 1)
            self.assertEqual(("a" * 64, "b" * 64),
                             (result["control_seal_sha256"],
                              result["treatment_seal_sha256"]))
            self.assertEqual(RECORD.PS.state_hash(hard),
                             result["hard_gate_receipt_sha256"])
            self.assertEqual("c" * 64, result["tested_pair_hash"])
            self.assertIn("--research-causal", result["gate_continuation"])
            self.assertEqual([mock.call(str(control)), mock.call(str(treatment))],
                             fake.start_experiment.call_args_list)
            fake.advance.assert_not_called()

    def test_actual_frozen_mismatch_blocks_both_research_starts(self):
        """OpenSpec scenario: A research treatment is prepared for comparison."""
        sys.path.insert(0, str(ROOT / "scripts/eval"))
        import run_iteration as run  # noqa: E402
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).absolute()
            control, treatment = root / "control", root / "treatment"
            frozen = {name: "a" * 64 for name in RECORD.FROZEN_FOR_RESEARCH}
            declaration = {"schema": 2, "surface": "research",
                "hypothesis": "Prompt delta improves research.",
                "causal_chain": ["prompt changes discovery"],
                "changed_bundle": ["research:prompts/research-agent.md"],
                "frozen_variables": frozen,
                "inputs": {"control_candidate_root": str(control),
                           "treatment_candidate_root": str(treatment)},
                "research_bundle": {"prompts/research-agent.md": "changed\n"},
                "downstream_effect": {"required": False, "task_sha256": None,
                                      "receipt_path": None},
                "falsifier": "Actual frozen bytes differ."}
            path = root / "declaration.json"
            path.write_text(json.dumps(declaration), encoding="utf-8")
            fake = types.ModuleType("research_factory")
            actual = dict(frozen); actual["writing"] = "b" * 64
            fake.preflight = mock.Mock(return_value={"frozen_variables": actual,
                "research_bundle": {"components": {
                    "prompts/research-agent.md": "a" * 64}}})
            fake.require_control_baseline = fake.preflight
            fake.ResearchBlocked = RuntimeError
            fake.ResearchFactoryError = RuntimeError
            fake.start_experiment = mock.Mock()
            with mock.patch.dict(sys.modules, {"research_factory": fake}), \
                    mock.patch.dict("os.environ", {"OPENROUTER_API_KEY": "fixture"},
                                    clear=True), \
                    mock.patch.object(run, "_prepare_research_arms",
                                      return_value={"control": control,
                                                    "treatment": treatment}), \
                    self.assertRaisesRegex(SystemExit, "actual frozen writing"):
                run._research_treatment(path, root, "book", "1-3", 1)
            fake.start_experiment.assert_not_called()

    def test_research_treatment_accepts_only_explicit_prompt_components(self):
        """OpenSpec scenario: A purported causal decision mixes changes."""
        root = Path("C:/isolated")
        value = {"schema": 2, "surface": "research",
            "hypothesis": "Research config improves retrieval.",
            "causal_chain": ["configuration changes discovery"],
            "changed_bundle": ["research:loop/config.yaml#research"],
            "frozen_variables": {name: "a" * 64
                for name in RECORD.FROZEN_FOR_RESEARCH},
            "inputs": {"control_candidate_root": str(root / "control"),
                       "treatment_candidate_root": str(root / "treatment")},
            "research_bundle": {"loop/config.yaml": "research_call_ceiling: 2\n"},
            "downstream_effect": {"required": False, "task_sha256": None,
                                  "receipt_path": None},
            "falsifier": "Retrieval quality does not improve."}
        with self.assertRaisesRegex(RECORD.RecordError,
                                    "not an allowed research component"):
            RECORD.validate_research_treatment(value)
        value["changed_bundle"] = [
            "research:prompts/research-evidence-editor.md"]
        value["research_bundle"] = {
            "prompts/research-evidence-editor.md": "loosened judge\n"}
        with self.assertRaisesRegex(RECORD.RecordError,
                                    "not an allowed research component"):
            RECORD.validate_research_treatment(value)

    def test_causal_preparation_creates_two_real_rf02_snapshots_and_exact_delta(self):
        """OpenSpec scenario: A research treatment is prepared for comparison."""
        sys.path.insert(0, str(ROOT / "scripts/eval"))
        import run_iteration as run  # noqa: E402
        from scripts.eval.tests.test_candidate_pair import CandidatePairTests
        fixture = CandidatePairTests(methodName="test_reject_preserves_public_bytes_types_links_and_old_evidence")
        fixture.setUp()
        try:
            accepted, existing, _manifest, _evidence = fixture.fixture(
                "research-causal", initialize=False, snapshot=False)
            for relative, text in {
                    "prompts/research-agent.md": "control research prompt\n",
                    "prompts/research-evidence-editor.md": "frozen editor\n"}.items():
                target = accepted / relative; target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text, encoding="utf-8")
            run.CP.initialize(accepted, "production-books/test")
            treatment = existing.parent / "research-causal-treatment"
            declaration = {"inputs": {
                "control_candidate_root": str(existing),
                "treatment_candidate_root": str(treatment)},
                "research_bundle": {
                    "prompts/research-agent.md": "treatment research prompt\n"}}
            preflight = lambda _root: {
                "research_bundle": {"components": {
                    "prompts/research-agent.md": "a" * 64,
                    "prompts/research-evidence-editor.md": "b" * 64,
                    "loop/config.yaml#research": "c" * 64}}}
            fake = types.SimpleNamespace(preflight=preflight,
                require_control_baseline=preflight, ResearchBlocked=RuntimeError,
                ResearchFactoryError=RuntimeError)
            roots = run._prepare_research_arms(declaration, accepted,
                "production-books/test", "1-2", 9, fake)
            self.assertEqual({"control", "treatment"}, set(roots))
            for arm in roots.values():
                self.assertEqual(9, run.CP.load(arm)["run"]["iteration_id"])
            self.assertEqual("control research prompt\n",
                (run.CP.candidate_tree(existing) /
                 "prompts/research-agent.md").read_text(encoding="utf-8"))
            self.assertEqual("treatment research prompt\n",
                (run.CP.candidate_tree(treatment) /
                 "prompts/research-agent.md").read_text(encoding="utf-8"))
            # Resume reuses both manifests and leaves the exact bundle unchanged.
            again = run._prepare_research_arms(declaration, accepted,
                "production-books/test", "1-2", 9, fake)
            self.assertEqual(roots, again)
        finally:
            fixture.tearDown()

    def test_real_causal_route_missing_key_makes_no_arm_or_marker_write(self):
        """OpenSpec scenario: Research causal readiness is verified without a run."""
        sys.path.insert(0, str(ROOT / "scripts/eval"))
        import run_iteration as run  # noqa: E402
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).absolute()
            declaration = {"schema": 2, "surface": "research",
                "hypothesis": "Prompt delta improves research.",
                "causal_chain": ["prompt changes discovery"],
                "changed_bundle": ["research:prompts/research-agent.md"],
                "frozen_variables": {name: "a" * 64
                    for name in RECORD.FROZEN_FOR_RESEARCH},
                "inputs": {"control_candidate_root": str(root / "control"),
                           "treatment_candidate_root": str(root / "treatment")},
                "research_bundle": {"prompts/research-agent.md": "changed\n"},
                "downstream_effect": {"required": False, "task_sha256": None,
                                      "receipt_path": None},
                "falsifier": "Hard evidence fails."}
            path = root / "declaration.json"
            path.write_text(json.dumps(declaration), encoding="utf-8")
            before = {item.relative_to(root).as_posix(): item.read_bytes()
                      for item in root.rglob("*") if item.is_file()}
            fake = types.ModuleType("research_factory")
            fake.preflight = mock.Mock(); fake.start_experiment = mock.Mock()
            with mock.patch.dict(sys.modules, {"research_factory": fake}), \
                    mock.patch.dict("os.environ", {}, clear=True), \
                    mock.patch.object(run.CP, "snapshot") as snapshot, \
                    self.assertRaisesRegex(SystemExit, "made no writes"):
                run._research_treatment(path, root, "book", "1-3", 1)
            snapshot.assert_not_called(); fake.preflight.assert_not_called()
            fake.start_experiment.assert_not_called()
            after = {item.relative_to(root).as_posix(): item.read_bytes()
                     for item in root.rglob("*") if item.is_file()}
            self.assertEqual(before, after)

    def test_research_cli_uses_rf32_without_unlocking_ordinary_loop(self):
        """OpenSpec RF-32: the research-only route has its own explicit authority."""
        sys.path.insert(0, str(ROOT / "scripts/eval"))
        import run_iteration as run  # noqa: E402
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).absolute()
            statuses = {"RF-23": "BLOCKED", "RF-32": "READY"}
            ledger = root / "tasks.md"
            ledger.write_text(
                "### RF-23 â€” writing\n- Status: `BLOCKED`\n"
                "### RF-32 â€” research readiness\n- Status: `READY`\n",
                encoding="utf-8")
            declaration = root / "declaration.json"
            declaration.write_text("{}", encoding="utf-8")
            argv = ["run_iteration.py", "--book", "production-books/test",
                    "--iter", "1", "--research-treatment", str(declaration),
                    "--redesign-authorized", "--rf-stage", "RF-32",
                    "--candidate-root", str(root)]
            seals = {"control_seal_sha256": "a" * 64,
                     "treatment_seal_sha256": "b" * 64,
                     "gate_continuation": "py gate.py --research-causal"}
            with mock.patch.object(run.LG, "_statuses", return_value=statuses), \
                    mock.patch.object(sys, "argv", argv), \
                    mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "fixture"}), \
                    mock.patch.object(run, "_research_treatment",
                                      return_value=seals) as treatment:
                with mock.patch("builtins.print") as output:
                    run.main()
            self.assertTrue(any("--research-causal" in str(call)
                                for call in output.call_args_list))
            treatment.assert_called_once_with(
                str(declaration), root, "production-books/test", "1-3", 1)
            ordinary = ["run_iteration.py", "--book", "production-books/test",
                        "--iter", "1", "--redesign-authorized", "--rf-stage", "RF-32",
                        "--candidate-root", str(root)]
            with mock.patch.object(run.LG, "_statuses", return_value=statuses), \
                    mock.patch.object(sys, "argv", ordinary), \
                    self.assertRaisesRegex(SystemExit, "RF-23 READY"):
                run.main()

    def test_blind_research_comparison_is_task_bound_and_resumable(self):
        """OpenSpec scenario: A research treatment is prepared for comparison."""
        sys.path.insert(0, str(ROOT / "scripts/eval"))
        import native_judge as native  # noqa: E402
        import run_iteration as run  # noqa: E402
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).absolute()
            roots = {name: root / name for name in ("control", "treatment")}
            identity = {"run": {"book": "production-books/test"}}
            for label, (name, arm) in zip(("one", "two"), roots.items()):
                research = arm / "candidate/production-books/test/research"
                (research / "sources").mkdir(parents=True)
                (research / "lived-experience.md").write_text(
                    f"anonymous lived {label}\n", encoding="utf-8")
                (research / "scientific-evidence.md").write_text(
                    f"anonymous science {label}\n", encoding="utf-8")
                (research / "research-coverage.json").write_text(
                    '{"status":"PASS"}\n', encoding="utf-8")
                (research / "sources/source.md").write_text(
                    f"eligible source {label}\n", encoding="utf-8")
            calls = []
            def complete(content, actor, schema, model, reasoning):
                task = json.loads(content); calls.append(task)
                verdict = {"schema": 1, "task_sha256": task["task_sha256"],
                           "preferred": "B",
                           "decisive_reason": "the hypothesis-specific coverage improved"}
                return json.dumps(verdict), {"kind": "native-codex-subscription",
                    "judge_identity": actor, "fresh_ephemeral_context": True,
                    "input_sha256": RECORD.PS.sha(content.encode()),
                    "output_schema_sha256": RECORD.PS.sha(native._schema_bytes(schema)),
                    "model": model,
                    "reasoning_effort": reasoning, "thread_id": "fresh-thread",
                    "command": ["codex", "exec"]}, None
            declaration = {"schema": 2, "surface": "research",
                "hypothesis": "prompt improves coverage",
                "causal_chain": ["prompt changes discovery"],
                "changed_bundle": ["research:prompts/research-agent.md"],
                "frozen_variables": {name: f"{index:064x}" for index, name in
                    enumerate(sorted(RECORD.FROZEN_FOR_RESEARCH), 1)},
                "inputs": {"control_candidate_root": str(roots["control"]),
                           "treatment_candidate_root": str(roots["treatment"])},
                "falsifier": "The bounded research comparison does not improve.",
                "research_bundle": {"prompts/research-agent.md": "treatment\n"},
                "downstream_effect": {"required": False, "task_sha256": None,
                                      "receipt_path": None}}
            receipt = run._research_comparison(declaration, roots,
                {"control": identity, "treatment": identity},
                {"control": "a" * 64, "treatment": "b" * 64}, complete)
            self.assertEqual(("B", "B"),
                             (receipt["preferred"], receipt["treatment_candidate"]))
            self.assertEqual(1, len(calls))
            self.assertNotIn("control", json.dumps(calls[0]).casefold())
            self.assertNotIn("treatment", json.dumps(calls[0]).casefold())
            again = run._research_comparison(declaration, roots,
                {"control": identity, "treatment": identity},
                {"control": "a" * 64, "treatment": "b" * 64},
                mock.Mock(side_effect=AssertionError("duplicate native call")))
            self.assertEqual(receipt, again)
            changed = dict(declaration)
            changed["hypothesis"] = "a different post-crash hypothesis"
            with self.assertRaisesRegex(SystemExit, "comparison marker is stale"):
                run._research_comparison(changed, roots,
                    {"control": identity, "treatment": identity},
                    {"control": "a" * 64, "treatment": "b" * 64},
                    mock.Mock(side_effect=AssertionError("duplicate native call")))
            self.assertEqual(native.MODEL,
                json.loads((roots["treatment"] /
                    "evidence/research-causal/comparison.result.json").read_text())
                    ["native"]["model"])
            result_path = (roots["treatment"] /
                           "evidence/research-causal/comparison.result.json")
            original = json.loads(result_path.read_text(encoding="utf-8"))
            for key in ("input_sha256", "output_schema_sha256"):
                with self.subTest(stale_native_binding=key):
                    stale = copy.deepcopy(original)
                    stale["native"][key] = "0" * 64
                    stale["native_record_sha256"] = RECORD.PS.state_hash(stale["native"])
                    result_path.write_text(json.dumps(stale), encoding="utf-8")
                    with self.assertRaisesRegex(SystemExit, "durable research comparison result is stale"):
                        run._research_comparison(declaration, roots,
                            {"control": identity, "treatment": identity},
                            {"control": "a" * 64, "treatment": "b" * 64},
                            mock.Mock(side_effect=AssertionError("duplicate native call")))
            result_path.write_text(json.dumps(original), encoding="utf-8")

    def test_required_downstream_effect_binds_exact_paired_blind_receipt(self):
        """OpenSpec scenario: A research treatment is prepared for comparison."""
        sys.path.insert(0, str(ROOT / "scripts/eval"))
        import run_iteration as run  # noqa: E402
        with tempfile.TemporaryDirectory() as temporary:
            treatment = Path(temporary).absolute() / "treatment"
            evidence = treatment / "evidence"; evidence.mkdir(parents=True)
            task_sha = "d" * 64
            receipt = {"schema": 1, "task_sha256": task_sha, "status": "PASS",
                "comparison_task_sha256": "e" * 64, "preferred": "B",
                "treatment_candidate": "B", "hypothesis_outcome": "SUPPORTED"}
            receipt_path = evidence / "downstream-effect.json"
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            declaration = {"frozen_variables": {"writing": "a" * 64},
                "downstream_effect": {"required": True,
                    "task_sha256": task_sha, "receipt_path": str(receipt_path)}}
            roots = {"control": treatment.parent / "control",
                     "treatment": treatment}
            seals = {"control": "b" * 64, "treatment": "c" * 64}
            with mock.patch.object(run, "_downstream_comparison",
                                   return_value=receipt) as comparison:
                self.assertEqual(receipt,
                    run._downstream_effect_receipt(declaration, roots, seals))
            comparison.assert_called_once_with(
                declaration, roots, seals, complete=False)
            forged = dict(receipt); forged["preferred"] = "A"
            receipt_path.write_text(json.dumps(forged), encoding="utf-8")
            with mock.patch.object(run, "_downstream_comparison",
                                   return_value=receipt), \
                    self.assertRaisesRegex(SystemExit, "stale or blocking"):
                run._downstream_effect_receipt(declaration, roots, seals)

    def test_actual_paired_downstream_producer_and_tamper_gate(self):
        """OpenSpec scenario: Required downstream research effect is paired and blind."""
        sys.path.insert(0, str(ROOT / "scripts/eval"))
        import run_iteration as run  # noqa: E402
        import research_factory as factory  # noqa: E402
        from scripts.eval.tests.test_research_factory import (
            ResearchFactoryTests, FakeTransport, FakeEditor, policy)
        fixture = ResearchFactoryTests(
            methodName="test_parallel_filter_synthesis_review_seal_and_resume")
        fixture.setUp()
        try:
            accepted, control = fixture.repo, fixture.candidate
            treatment = control.parent / "paired-downstream-treatment"
            treatment.mkdir()
            run.CP.snapshot(treatment, accepted, "production-books/test", "1-2",
                            iteration=1)
            treatment_prompt = run.CP.candidate_tree(treatment) / \
                "prompts/research-agent.md"
            treatment_text = "treatment research contract\n"
            treatment_prompt.write_text(treatment_text, encoding="utf-8")
            seals = {
                "control": factory.advance(
                    control, FakeTransport(), FakeEditor(), policy()),
                "treatment": factory.advance(
                    treatment, FakeTransport(), FakeEditor(), policy()),
            }
            treatment_chapter = run.CP.candidate_tree(treatment) / \
                "production-books/test/chapters/chapter-01.md"
            treatment_chapter.write_text(
                "distinct treatment downstream candidate\n", encoding="utf-8")
            control_hash, treatment_hash = run.CP.seal(control), run.CP.seal(treatment)
            frozen = factory.require_control_baseline(control)["frozen_variables"]
            self.assertEqual(frozen, factory.preflight(treatment)["frozen_variables"])
            task_sha = RECORD.research_downstream_contract([1, 2])["contract_sha256"]
            receipt_path = treatment / "evidence/research-causal/downstream-effect.json"
            declaration = {"schema": 2, "surface": "research",
                "hypothesis": "Better research improves the frozen downstream process.",
                "causal_chain": ["research changes planning evidence", "evidence changes effect"],
                "changed_bundle": ["research:prompts/research-agent.md"],
                "frozen_variables": frozen,
                "inputs": {"control_candidate_root": str(control),
                           "treatment_candidate_root": str(treatment)},
                "falsifier": "The blind downstream comparison does not prefer treatment.",
                "research_bundle": {"prompts/research-agent.md": treatment_text},
                "downstream_effect": {"required": True, "task_sha256": task_sha,
                                      "receipt_path": str(receipt_path)}}

            def complete(content, _identity, _schema, **_kwargs):
                task = json.loads(content)
                verdict = {"schema": 1, "task_sha256": task["task_sha256"],
                           "preferred": "B", "decisive_reason": "material paired effect"}
                return json.dumps(verdict), {
                    "kind": "native-codex-subscription",
                    "judge_identity": "research-downstream-effect-independent",
                    "model": RECORD.RESEARCH_JUDGE_MODEL,
                    "reasoning_effort": RECORD.RESEARCH_JUDGE_REASONING,
                    "fresh_ephemeral_context": True, "thread_id": "fresh-paired-test",
                    "command": ["codex", "exec"],
                    "input_sha256": RECORD.PS.sha(content.encode()),
                    "output_schema_sha256": RECORD.PS.sha(
                        RECORD.research_comparison_schema_bytes())}, None

            with mock.patch.object(run.FB, "require_frozen_batch"), \
                    mock.patch.object(run.GR, "require_complete",
                                      return_value={"state": "PASSED"}), \
                    mock.patch.object(run.DR, "require_developmental_pass",
                                      return_value={"state": "PASS"}), \
                    mock.patch.object(run.score_core, "evaluate",
                                      return_value={"hard_ok": True, "hard_fails": []}):
                receipt = run._downstream_comparison(
                    declaration, {"control": control, "treatment": treatment},
                    seals, complete)
                self.assertEqual(("PASS", "B", control_hash, treatment_hash),
                    (receipt["status"], receipt["preferred"],
                     receipt["control_pair_hash"], receipt["treatment_pair_hash"]))
                again = run._downstream_comparison(
                    declaration, {"control": control, "treatment": treatment},
                    seals, complete=False)
                self.assertEqual(receipt, again)
                chapter = run.CP.candidate_tree(control) / \
                    "production-books/test/chapters/chapter-01.md"
                chapter.chmod(0o666)
                chapter.write_text("tampered downstream arm\n", encoding="utf-8")
                with self.assertRaisesRegex(SystemExit, "hard gates failed"):
                    run._downstream_comparison(
                        declaration, {"control": control, "treatment": treatment},
                        seals, complete=False)
        finally:
            fixture.tearDown()

    def test_blind_preference_maps_to_hypothesis_only_after_judgment(self):
        """OpenSpec scenario: A research treatment is prepared for comparison."""
        self.assertEqual("REFUTED", RECORD.research_hypothesis_outcome("A"))
        self.assertEqual("SUPPORTED", RECORD.research_hypothesis_outcome("B"))
        self.assertEqual("INCONCLUSIVE", RECORD.research_hypothesis_outcome("TIE"))
        task = {"task_sha256": "a" * 64}
        with self.assertRaisesRegex(RECORD.RecordError, "malformed"):
            RECORD.validate_research_comparison_verdict(task, {
                "schema": 1, "task_sha256": "a" * 64, "preferred": "B",
                "hypothesis_outcome": "SUPPORTED", "decisive_reason": "extra field"})


if __name__ == "__main__":
    unittest.main()
