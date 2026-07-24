"""Offline H-F01 blind, chronology, and coordinator-to-gate regressions."""
import json, os, shlex, sys, tempfile, unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock
ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "scripts/loop"), str(ROOT / "scripts/eval")]
import experiment_record as ER  # noqa: E402
import hf01_blind as BLIND  # noqa: E402
import hf01_preflight as HF  # noqa: E402
import hf01_stage_a as STAGE  # noqa: E402
import pair_store as PS  # noqa: E402
import product_decision as PD  # noqa: E402
import product_effect as PE  # noqa: E402
CONTROL, TREATMENT, GSBS, PROMPT = "c" * 64, "d" * 64, "e" * 64, "f" * 64
def preregistration():
    seal = "9" * 64
    return {"schema": 2, "surface": "writing",
            "hypothesis": "linked handoff improves enacted belief change",
            "causal_chain": ["plan fixes belief job", "commission carries evidence"],
            "changed_bundle": ["planning:plan", "commission:commission"],
            "frozen_variables": {"route": "fixed",
                                 "accepted_research_seal_sha256": seal},
            "inputs": {"git_commit": "a" * 64},
            "research": {"control_seal_sha256": seal,
                         "treatment_seal_sha256": seal},
            "falsifier": "blind effect or integrity fails"}
def panel(name, votes, panel_hash, prompt_hash=PROMPT):
    experiment = PS.state_hash({"control_pair_hash": CONTROL,
        "treatment_pair_hash": TREATMENT, "gsbs_sha256": GSBS})
    rows = []
    for index, (actor, position, vote) in enumerate(zip(
            PD.HF01_READERS, ("B", "A"), votes), 1):
        row = {"raw_verdict_id": f"raw-{name}-{index}", "actor": actor,
            "kind": "model", "family": "openai", "verdict": vote,
            "scope": "ordinary_product", "promotion_eligible": True,
            "base_task_sha256": PS.state_hash(f"{name}-task-{index}"),
            "tested_pair_hash": experiment, "prompt_sha256": prompt_hash,
            "input_sha256": PS.state_hash(f"{name}-input-{index}")}
        row["task_id"] = PD.bound_task_id(row)
        row.update(reader_identity=actor, treatment_candidate=position,
            gsbs_sha256=panel_hash, envelope_sha256=PS.state_hash(f"{name}-envelope-{index}"),
            raw_record_sha256=PS.state_hash(f"{name}-record-{index}"), authority_sha256="4" * 64,
            native_call_sha256=PS.state_hash(f"{name}-call-{index}"),
            model="gpt-5.6-sol", route="codex-native", reasoning="xhigh",
            command=PD.HF01_COMMAND)
        rows.append(row)
    return rows

def evidence_fixture(root):
    base = STAGE.folder(root); base.mkdir(parents=True)
    rubric = root / "rubric.md"; rubric.write_text("blind rubric\n")
    prompt_hash = PS.sha(rubric.read_bytes())
    panel_hashes = [PS.state_hash(f"panel-{index}") for index in range(4)]
    integrity = {"status": "PASS", "unsupported_claim_comparison": {
        "control": 1, "treatment": 0, "increased": False,
        "grounded_receipt_hashes": {"control": "1" * 64, "treatment": "2" * 64}}}
    diagnostic = {"role": "DIAGNOSTIC_ONLY", "status": "PASS",
                  "task_ids": [PS.state_hash(f"absolute-{n}") for n in range(6)]}
    bundle = {"schema": 2, "authority_sha256": "4" * 64, "control_pair_hash": CONTROL,
        "treatment_pair_hash": TREATMENT, "gsbs_sha256": GSBS,
        "gsbs_panel_sha256": panel_hashes}
    bundle["task_bundle_sha256"] = PS.state_hash(bundle)
    blind_body = {"schema": 2, "frozen_at_utc": "2026-07-19T11:00:00+00:00",
        "authority_sha256": "4" * 64, "upstream_receipt_sha256": "5" * 64,
        "task_bundle_sha256": bundle["task_bundle_sha256"],
        "control_pair_hash": CONTROL, "treatment_pair_hash": TREATMENT,
        "experiment_sha256": PS.state_hash({"control_pair_hash": CONTROL,
            "treatment_pair_hash": TREATMENT, "gsbs_sha256": GSBS}),
        "gsbs_matches": [], "gsbs_sha256": GSBS, "gsbs_panel_sha256": panel_hashes,
        "integrity": integrity, "control_treatment_causal_diagnostic": diagnostic,
        "gsbs_chapter_panels": [panel("chapter-1", ("PASS", "PASS"), panel_hashes[0], prompt_hash),
            panel("chapter-2", ("PASS", "PASS"), panel_hashes[1], prompt_hash),
            panel("chapter-3", ("PASS", "FAIL"), panel_hashes[2], prompt_hash)],
        "gsbs_whole_opening_panel": panel("opening", ("PASS", "PASS"), panel_hashes[3], prompt_hash)}
    blind = {**blind_body, "receipt_hash": PS.state_hash(blind_body)}
    carr = {"schema": 3, "iteration": "007", "completed_at_utc": "2026-07-19T11:30:00+00:00",
        "blind_receipt_sha256": PS.sha(PS.json_bytes(blind)),
        "native_receipt_sha256": "9" * 64,
        "aggregate": {"reward": 7}, "score_receipt": {"receipt": "fixture"}}
    context, reference = STAGE._decision_context(bundle, blind, carr, prompt_hash)
    human = {"schema": 2, "reviewer": "Founder Kristian", "verdict": "APPROVE",
        "reviewed_at_utc": "2026-07-19T12:00:00+00:00", "control_pair_hash": CONTROL,
        "treatment_pair_hash": TREATMENT, "gsbs_sha256": GSBS,
        "blind_receipt_sha256": PS.sha(PS.json_bytes(blind)),
        "reference_sighted_diagnostic_sha256": reference,
        "decision_context_sha256": context}
    authority = {"preregistration": preregistration(), "next_command": "resume-hf01"}
    for name, value in ((STAGE.TASKS, bundle), (STAGE.RECEIPT, blind),
                        (STAGE.CARR, carr), (STAGE.HUMAN, human), ("authority.json", authority)):
        (base / name).write_bytes(PS.json_bytes(value))
    view = {"manifest": {"run": {"iteration_id": 7}},
            "config": {"product_effect_rubric": str(rubric)}, "pair": root / "pair"}
    return bundle, blind, carr, human, authority, integrity, view


class Hf01StageTests(unittest.TestCase):
    @staticmethod
    def _replace(source, target):
        target = Path(target)
        if target.exists() and not target.is_symlink(): target.chmod(0o644)
        os.replace(source, target)
    def setUp(self):
        self.root_guard = mock.patch.object(HF, "require_authorized_root",
            side_effect=lambda root: Path(root).absolute())
        self.root_guard.start(); self.addCleanup(self.root_guard.stop)
        self.sync_patch = mock.patch.object(PS, "_sync", return_value=None)
        self.sync_patch.start(); self.addCleanup(self.sync_patch.stop)
        self.replace_patch = mock.patch.object(PS, "_replace_file", side_effect=self._replace)
        self.replace_patch.start(); self.addCleanup(self.replace_patch.stop)
    def test_final_record_cannot_post_author_preregistered_fields(self):
        frozen = preregistration(); decision = {"decision": "REJECT", "layers": {
            "integrity_hard_gate": {"status": "PASS"}, "blind_chapter_effect": {"status": "FAIL"},
            "blind_whole_opening_sequence": {"status": "FAIL"},
            "carr_craft_diagnostic": {"role": "DIAGNOSTIC_ONLY"}}}
        digest, tested = PS.state_hash(decision), "b" * 64
        record = {**{key: frozen[key] for key in ER.PREREG_FIELDS_V2 - {"inputs"}},
            "inputs": {**frozen["inputs"], "tested_pair_hash": tested,
                       "product_decision_sha256": digest},
            "evidence": ER.decision_evidence(decision), "decision": "REFUTED"}
        self.assertEqual(record, ER.bind(record, decision, tested, digest, frozen))
        changed = deepcopy(record); changed["hypothesis"] = "post-hoc story"
        with self.assertRaisesRegex(ER.RecordError, "post-authored preregistered hypothesis"):
            ER.bind(changed, decision, tested, digest, frozen)

    def test_bundle_uses_exact_offset_gsbs_and_opposite_reader_positions(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); root = Path(tmp.name)
        for arm in ("control", "treatment"):
            book = HF.arm_paths(root)[arm]["book"]
            for number in HF.CHAPTERS:
                path = book / f"chapters/chapter-{number:02d}.md"; path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"{arm} treatment content {number}\n")
        matches = []
        evaluation = HF.arm_paths(root)["treatment"]["experiment"] / "evaluation"
        for number, position in zip(HF.CHAPTERS, (3, 4, 5)):
            relative = f"calibration/reference/gsbs/chapter-{position}.txt"
            path = evaluation / relative; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"GSBS exact offset {position}\n")
            matches.append({"treatment_chapter": number, "reference_position": position,
                            "path": relative, "sha256": PS.sha(path.read_bytes())})
        authority = {"identity": {"gsbs_matches": matches, "gsbs_sha256": PS.state_hash(matches)},
            "route": {"judge_model": "gpt-5.6-sol", "judge_route": "codex-native",
                      "judge_reasoning": "xhigh"}}
        task_bundle = BLIND.bundle(root, {"control": CONTROL, "treatment": TREATMENT},
            {"status": "PASS"}, authority, "a" * 64)
        self.assertEqual(matches, task_bundle["gsbs_matches"])
        self.assertEqual(4, len(task_bundle["gsbs_panels"]))
        for index, group in enumerate(task_bundle["gsbs_panels"]):
            first, second = group["readers"]; self.assertEqual(PD.HF01_READERS,
                (first["identity"], second["identity"]))
            self.assertEqual(("B", "A"), (first["envelope"]["treatment_support"]["PASS"],
                                           second["envelope"]["treatment_support"]["PASS"]))
            a, b = (row["envelope"]["judge_task"]["candidates"] for row in (first, second))
            self.assertEqual(a["A"], b["B"]); self.assertEqual(a["B"], b["A"])
            expected_files = ({matches[index]["path"]: matches[index]["sha256"]}
                              if index < 3 else {row["path"]: row["sha256"] for row in matches})
            self.assertEqual(expected_files, first["envelope"]["gsbs_files"])
            self.assertEqual(PS.state_hash(expected_files), task_bundle["gsbs_panel_sha256"][index])
        (evaluation / matches[0]["path"]).write_text("tampered\n")
        with self.assertRaisesRegex(BLIND.BlindError, "hash changed"):
            BLIND._gsbs(root, authority)

    def test_absolute_receipt_requires_exact_native_route_identity_and_command(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); root = Path(tmp.name)
        task = BLIND.ABS.chapter("sugar", "treatment chapter")
        row = {"key": "treatment-chapter-01", "identity": "hf01-absolute-treatment-01",
            "route": {"model": "gpt-5.6-sol", "route": "codex-native", "reasoning": "xhigh"},
            "envelope": BLIND.ABS.envelope(task, "treatment-chapter-01", TREATMENT)}
        observation = {field: "CLEAR" for field in BLIND.ABS.RATING_FIELDS}
        observation.update(entering_belief="old belief", leaving_belief="new belief",
            enacted_discovery="felt discovery", construct_sufficiency="MEETS",
            construct_reason="the chapter enacts the change", opening_sequence={
                field: BLIND.ABS.NOT_APPLICABLE for field in BLIND.ABS.SEQUENCE_FIELDS})
        raw = json.dumps({"schema": 1, "task_sha256": task["task_sha256"], "mode": "chapter",
                          "observation": observation, "confidence": "HIGH"})
        prompt = b"exact anonymous absolute prompt"
        def complete(_content, _actor, _schema, model, reasoning):
            return raw, {"thread_id": "fresh-native-thread", "model": model,
                "reasoning_effort": reasoning, "command": BLIND.NATIVE.command("<isolated-tmp>",
                    "<isolated-tmp>/judge-output-schema.json", model, reasoning)}, None
        value = BLIND._absolute_record(BLIND.folder(root), row, prompt, "4" * 64, True, complete)
        self.assertEqual("4" * 64, value["authority_sha256"])
        path = BLIND.folder(root) / "absolute/verdicts/treatment-chapter-01.json"
        self.assertEqual(value, BLIND._absolute_record(BLIND.folder(root), row, prompt, "4" * 64, False))
        path.chmod(0o644)
        value["command"] = ["wrong"]; path.write_bytes(PS.json_bytes(value))
        with self.assertRaisesRegex(BLIND.BlindError, "route, identity, command"):
            BLIND._absolute_record(BLIND.folder(root), row, prompt, "4" * 64, False)

    def test_unsupported_claims_come_from_both_grounded_receipts(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); root = Path(tmp.name)
        paths = {arm: {"experiment": root / arm} for arm in ("control", "treatment")}
        receipts = {"control": {"receipt_hash": "1" * 64, "chapters": [{"verdict": {
            "findings": [{"classification": "invention"}, {"classification": "inference broadening"}]}}]},
            "treatment": {"receipt_hash": "2" * 64, "chapters": [{"verdict": {
                "findings": [{"classification": "invention"}, {"classification": "supported"}]}}]}}
        tested = {"control": CONTROL, "treatment": TREATMENT}
        def arm(path): return Path(path).name
        core = {"hard_ok": True, "hard_fails": [], "checks": {}}
        patches = (mock.patch.object(STAGE.HF, "arm_paths", return_value=paths),
            mock.patch.object(STAGE.GR, "require_complete", side_effect=lambda path: receipts[arm(path)]),
            mock.patch.object(STAGE.CP, "load", side_effect=lambda path: {
                "state": "SEALED", "tested_hash": tested[arm(path)]}),
            mock.patch.object(STAGE.CP, "open_sealed", side_effect=lambda path, _tested: {
                "config": {}, "pair": Path(path) / "candidate"}),
            mock.patch.object(STAGE.score_core, "evaluate", return_value=core))
        with patches[0], patches[1], patches[2], patches[3], patches[4]:
            hashes, integrity = STAGE._sealed(root)
            self.assertEqual(tested, hashes)
            self.assertEqual({"control": 2, "treatment": 1, "increased": False,
                "grounded_receipt_hashes": {"control": "1" * 64, "treatment": "2" * 64}},
                integrity["unsupported_claim_comparison"])
            receipts["treatment"]["chapters"][0]["verdict"]["findings"].extend(
                [{"classification": "invention"}, {"classification": "invention"}])
            with self.assertRaisesRegex(STAGE.StageError, "unsupported-claim"):
                STAGE._sealed(root)

    def test_named_human_binds_all_hashes_and_follows_carr(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); root = Path(tmp.name)
        bundle, blind, carr, human, *_rest = evidence_fixture(root)
        prompt_hash = PS.sha((root / "rubric.md").read_bytes())
        self.assertEqual(human["reviewer"], STAGE._human(root, bundle, blind, carr, prompt_hash)["reviewer"])
        path = STAGE.folder(root) / STAGE.HUMAN
        for field in ("control_pair_hash", "treatment_pair_hash", "gsbs_sha256",
                      "blind_receipt_sha256", "reference_sighted_diagnostic_sha256",
                      "decision_context_sha256"):
            changed = dict(human); changed[field] = "0" * 64; path.write_bytes(PS.json_bytes(changed))
            with self.subTest(field=field), self.assertRaisesRegex(STAGE.StageError, "hashes or chronology"):
                STAGE._human(root, bundle, blind, carr, prompt_hash)
        path.write_bytes(PS.json_bytes(human))
        with self.assertRaisesRegex(STAGE.StageError, "hashes or chronology"):
            STAGE._human(root, bundle, blind, carr, "0" * 64)
        changed = dict(human); changed["reviewed_at_utc"] = carr["completed_at_utc"]
        path.write_bytes(PS.json_bytes(changed))
        with self.assertRaisesRegex(STAGE.StageError, "hashes or chronology"):
            STAGE._human(root, bundle, blind, carr, prompt_hash)

    def test_coordinator_emits_and_gate_adapter_consumes_one_atomic_command(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup); root = Path(tmp.name)
        bundle, _blind, carr, _human, authority, integrity, view = evidence_fixture(root)
        product_path = HF.arm_paths(root)["treatment"]["experiment"] / "evidence" / PD.PATH
        record_path = HF.arm_paths(root)["treatment"]["experiment"] / "evidence" / ER.PATH
        with mock.patch.object(STAGE, "_review"), \
                mock.patch.object(STAGE, "_sealed", return_value=(
                    {"control": CONTROL, "treatment": TREATMENT}, integrity)), \
                mock.patch.object(STAGE.BLIND, "bundle", return_value=bundle), \
                mock.patch.object(STAGE.BLIND, "emit", return_value=view), \
                mock.patch.object(STAGE, "_carr", return_value=carr), \
                mock.patch.object(STAGE.CARR_NATIVE, "verify",
                    return_value={"receipt_hash": carr["native_receipt_sha256"],
                        "calls": [{"completed_at_utc": "2026-07-19T11:20:00+00:00"}]}), \
                mock.patch.object(STAGE.score_core, "evaluate", return_value={"pairs": []}), \
                mock.patch.object(STAGE.CP, "open_sealed", return_value=view):
            result = STAGE.advance(root, authority, "5" * 64,
                decision_timestamp="2026-07-19T13:00:00+00:00", promote_pair=True)
            product, record = STAGE.gate_product(root, carr["aggregate"], product_path, record_path)
        self.assertEqual(("ATOMIC_GATE_COMMAND_EMITTED", "PROMOTE"),
                         (result["state"], product["decision"]))
        self.assertEqual("SUPPORTED", record["decision"])
        command = shlex.split(result["gate_command"])
        self.assertEqual((sys.executable, "scripts/loop/gate.py", "7"),
                         (command[0], command[1], command[command.index("--iter") + 1]))
        self.assertEqual((TREATMENT, "2026-07-19T13:00:00+00:00"),
            (command[command.index("--tested-pair-hash") + 1],
             command[command.index("--decision-timestamp") + 1]))
        self.assertTrue(os.path.samefile(
            command[command.index("--accepted-root") + 1], root))
        self.assertIn("--promote-pair", command); self.assertEqual("007", STAGE.carr_iteration(view["manifest"]))

    def test_offline_contract_checks_leave_repo_fixtures_unchanged(self):
        paths = (ROOT / "loop/config.yaml", ROOT / "calibration/runs/LEDGER.md",
                 ROOT / "production-books/quit-sugar/00-brief.md")
        before = {path: PS.sha(path.read_bytes()) for path in paths}
        ER.validate_preregistration(preregistration())
        PE.validate_h_f01(PE.h_f01_envelope(PE.chapter_pair(
            "sugar", "GSBS", "treatment"), TREATMENT, {"gsbs.txt": GSBS},
            "B", "sol-xhigh-r1"))
        self.assertEqual(before, {path: PS.sha(path.read_bytes()) for path in paths})
if __name__ == "__main__": unittest.main()
