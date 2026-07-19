"""Focused pre-RF21 authority and durable H-F01 execution regressions."""
import json, os, shlex, shutil, sys, tempfile, unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock
ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "scripts/loop"), str(ROOT / "scripts/eval/tests")]
import candidate_pair as PAIR  # noqa: E402
import commission_set as SET  # noqa: E402
import first_draft_batch as BATCH  # noqa: E402
import hf01_preflight as HF  # noqa: E402
import hf01_run as RUN  # noqa: E402
import hf01_upstream as UP  # noqa: E402
from commission_packet_fixture import packet  # noqa: E402
from test_commission_contract import authority, commission  # noqa: E402
AUTH = "2026-07-19T10:00:00+00:00"
def assignment(chapter, source):
    auth = deepcopy(authority()); old = next(iter(auth["assigned_evidence"]))
    locator = f"{source}#E-001"; auth["target"] = chapter
    auth["resolved_ids"] = {chapter: auth["required"]["entering belief"]}
    binding = auth["assigned_evidence"].pop(old)
    binding["provenance"] = binding["provenance"].replace(old, locator)
    auth["assigned_evidence"][locator] = binding
    return {"packets": [f"production-books/quit-sugar/research/sources/{source.lower()}-fixture.md"], "authority": auth}
class Hf01Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name).resolve(); self.clean = mock.patch.object(HF, "_clean", return_value=True); self.clean.start(); self.addCleanup(self.clean.stop)
        self.ledger = self.root / "tasks.md"; self._ledger("BLOCKED", "BLOCKED")
        for relative in ("prompts/style-guide.md", "prompts/chapter-writer.md", "prompts/grounded-reviewer.md",
                         "prompts/developmental-reviewer.md", "prompts/master-plan-skill-v2.md", "prompts/master-plan-reviewer-v2.md"):
            target = self.root / relative; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, target)
        files = {
            "prompts/chapter-commissioner.md": "commissioner contract\n",
            "prompts/commission-set-auditor.md": "grounding continuity leakage\n",
            "production-books/quit-sugar/00-brief.md": "Safety perimeter is fixed.\n",
            "production-books/quit-sugar/research/lived-experience.md": "shared lived\n",
            "production-books/quit-sugar/research/scientific-evidence.md": "shared science\n",
            **{f"production-books/quit-sugar/research/sources/s-{100+n}-fixture.md": packet(
                f"S-{100+n}", "E-001", f"ONLY-{n}") for n in (1, 2, 3)},
            "production-books/quit-sugar/framing.md": "# Framing\n" + "".join(
                f"### CH-{n:02d} — State {n}\n- **Entering belief:** RS-{n-1:02d} | state\n"
                for n in (1, 2, 3)),
            "production-books/quit-sugar/master-plan.md": "# Plan\n\n" + "\n".join(
                f"| EV-L{n:02d} | bounded finding {n} | S-{100+n}#E-001. | "
                f"bounded use {n} | forbidden broadening {n} |" for n in (1, 2, 3)) +
                "\n\n" + "\n\n".join(
                f"### C-{n:02d} — Chapter {n}\n- **Belief job:** correct belief {n}.\n"
                f"- **Entering belief:** RS-{n-1:02d} | received state {n}.\n"
                f"- **Leaving belief:** RS-{n:02d} | handed state {n}.\n"
                f"- **Evidence:** EV-L{n:02d}.\n- **Guardrails:** safety limit {n}; no diagnosis.\n"
                f"- **Continuity:** receives received state {n}; hands C-{n+1:02d} handed state {n}."
                for n in (1, 2, 3)),
            "production-books/quit-sugar/master-plan-review.md": "fit to write from\n",
            **{f"production-books/quit-sugar/chapters/chapter-{n:02d}.md": f"baseline {n}\n" for n in (1, 2, 3)},
            "calibration/reference/gsbs/reference-metrics.json": '{"chapters": []}\n',
            **{f"calibration/reference/gsbs/chapter-{n}.txt": f"GSBS offset {n}\n" for n in range(1, 6)},
            "loop/results.tsv": "iter\treward\tverdict\n", "loop/causal-bundle-results.jsonl": ""}
        for relative, text in files.items():
            path = self.root / relative; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        shutil.copy2(ROOT / "loop/config.yaml", self.root / "loop/config.yaml")
        for relative in ("calibration/judges/carr-likeness-rubric.md", *HF.RUBRICS):
            target = self.root / relative; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, target)
        PAIR.initialize(self.root, HF.BOOK); self.arms = HF.arm_paths(self.root)
        for paths in self.arms.values(): paths["experiment"].mkdir(parents=True); PAIR.snapshot(paths["experiment"], self.root, HF.BOOK, "1-3", iteration=1)
        self.assignments = {f"C-{n:02d}": assignment(f"C-{n:02d}", f"S-{100+n}") for n in (1, 2, 3)}
    def tearDown(self): self.tmp.cleanup()
    def _ledger(self, rf22, rf23):
        self.ledger.write_text("### RF-20 — calibration\n- Status: `BLOCKED`\n"
            "### RF-21 — generation\n- Status: `READY`\n"
            f"### RF-22 — commissions\n- Status: `{rf22}`\n"
            f"### RF-23 — readiness\n- Status: `{rf23}`\n")
    def manifest(self, **changes):
        return HF.build_manifest(self.root, key_present=True, ledger=self.ledger, authority_timestamp=AUTH, **changes)
    def snapshot(self):
        return {path.relative_to(self.root).as_posix(): PAIR.PS.sha(path.read_bytes()) for path in self.root.rglob("*") if path.is_file()}
    def freeze(self):
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), mock.patch.object(HF, "LEDGER", self.ledger):
            return RUN._authority(self.root, AUTH)
    def prepare_treatment(self):
        book = self.arms["treatment"]["book"]
        for relative, suffix in (("00-brief.md", "Treatment reader journey.\n"),
                ("framing.md", "\nTreatment linked reader state.\n"),
                ("master-plan.md", "\nTreatment source-grounded handoff.\n"),
                ("master-plan-review.md", "Treatment plan review.\n")):
            path = book / relative; path.write_text(path.read_text() + suffix)
        UP._declare_review(self.arms["treatment"]["experiment"])
        (book / "framing-review.md").write_text("Treatment framing review.\n")
        with mock.patch.object(SET.SC, "require_subject_contract"):
            SET.generate(self.arms["treatment"]["experiment"], self.assignments, lambda request: commission(self.assignments[request["target"]]["authority"]), lambda _request: SET.AUDIT_PASS)
    def assignment_rows(self):
        rows = []
        for chapter, record in self.assignments.items():
            authority = record["authority"]
            rows.append({"chapter": chapter, "required": authority["required"],
                "resolved_ids": [{"id": key, "value": value}
                                 for key, value in authority["resolved_ids"].items()],
                "assigned_evidence": [{"locator": key, **value}
                    for key, value in authority["assigned_evidence"].items()],
                "frozen_tokens": list(authority["frozen_tokens"]),
                "forbidden": list(authority["forbidden"])})
        return rows
    def native(self, content, actor, _schema, model, reasoning):
        task = json.loads(content); call_id = task["id"]
        book = self.arms["control"]["book"]
        if call_id == "rf21-plan":
            value = {"brief": (book / "00-brief.md").read_text() + "Treatment reader journey.\n",
                "framing": (book / "framing.md").read_text() + "\nTreatment linked reader state.\n",
                "master_plan": (book / "master-plan.md").read_text() + "\nTreatment source-grounded handoff.\n",
                "assignments": self.assignment_rows()}
        elif call_id == "rf21-plan-review":
            value = {"framing_review": "Treatment framing review.",
                     "master_plan_review": "Treatment plan review."}
        elif call_id.startswith("rf22-commission"):
            target = f"C-{int(call_id[-2:]):02d}"
            value = {"commission": commission(self.assignments[target]["authority"])}
        else: value = {"verdict": SET.AUDIT_PASS}
        transport = {"thread_id": f"thread-{call_id}", "model": model,
            "reasoning_effort": reasoning, "command": UP.NATIVE.command(
                "<isolated-tmp>", "<isolated-tmp>/judge-output-schema.json", model, reasoning)}
        return json.dumps(value), transport, None
    def write_upstream(self, authority, authority_sha):
        with mock.patch.object(SET.SC, "require_subject_contract"):
            UP.dispatch(self.root, authority, authority_sha, complete=self.native)
        return self.root / UP.FOLDER / UP.PATH
    def authorize_run(self):
        _folder, authority, authority_sha = self.freeze()
        path = self.write_upstream(authority, authority_sha); self._ledger("DONE", "READY")
        return authority, authority_sha, path
    def test_preflight_is_pure_and_freezes_offset_gsbs_before_rf21(self):
        before, secret = self.snapshot(), "do-not-serialize"
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": secret}): manifest = self.manifest()
        self.assertEqual(before, self.snapshot()); self.assertTrue(manifest["ready_to_freeze_authority"])
        self.assertFalse(manifest["ready_to_send"])
        self.assertNotIn(secret, json.dumps(manifest)); self.assertEqual(HF.ROUTE_LAW, manifest["route"])
        self.assertEqual([3, 4, 5], [row["reference_position"] for row in manifest["identity"]["gsbs_matches"]])
        self.assertEqual(40, manifest["call_budget"]["planned_total"])
        self.assertEqual(0, manifest["call_budget"]["counted_before_authority"])
        self.assertEqual(["RF-25", "RF-30", "RF-31"], manifest["validation_ladder"]["order"])
        self.assertEqual(("evaluation-only", False), (manifest["subject_reference_isolation"]["reference_mode"], manifest["subject_reference_isolation"]["reference_in_rf21_rf22_inputs"]))
        self.assertEqual(list(UP.IDS), [row["id"] for row in manifest["rf21_rf22_native_calls"]])
        self.assertEqual(("gpt-5.6-luna", "gpt-5.6-sol"), tuple(row["model"] for row in manifest["rf21_rf22_native_calls"][:2]))
        self.assertNotIn("null", json.dumps(manifest["rf21_rf22_native_calls"]))
        self.assertTrue(all(row["reference_blind"] and "read-only" in row["command"]
                            for row in manifest["rf21_rf22_native_calls"]))
        self.assertNotIn("calibration/reference", json.dumps(
            manifest["rf21_rf22_native_calls"][0]["input_contract"]))
        self.assertEqual({"RF22_NOT_READY", "RF23_NOT_READY"},
                         {row["code"] for row in manifest["downstream_blockers"]})
        command = shlex.split(manifest["next_command"])
        self.assertEqual(("python3", "scripts/loop/hf01_run.py"), tuple(command[:2]))
        self.assertEqual((AUTH, "RF-21"), (command[command.index("--authority-timestamp") + 1], command[command.index("--rf-stage") + 1]))
    def test_authority_precedes_treatment_and_rejects_drift_outside_allowlist(self):
        brief = self.arms["treatment"]["book"] / "00-brief.md"; original = brief.read_text()
        brief.write_text(original + "premature treatment\n")
        self.assertIn("RF21_ALREADY_STARTED_BEFORE_AUTHORITY",
                      {row["code"] for row in self.manifest()["blockers"]})
        brief.write_text(original); _folder, authority, _sha = self.freeze(); self.prepare_treatment()
        self.assertEqual(set(HF.TREATMENT_PATHS), set(HF.treatment_artifacts(self.root)))
        HF.validate_execution_authority(self.root, authority, key_present=True)
        source = self.arms["treatment"]["book"] / "research/lived-experience.md"
        source.write_text(source.read_text() + "escaped change\n")
        with self.assertRaisesRegex(HF.PreflightError, "allowlist"):
            HF.validate_execution_authority(self.root, authority, key_present=True)
    def test_missing_writer_key_does_not_block_pre_rf21_authority(self):
        manifest = HF.build_manifest(self.root, key_present=False, ledger=self.ledger, authority_timestamp=AUTH)
        self.assertTrue(manifest["ready_to_freeze_authority"])
        self.assertFalse(manifest["ready_to_send"])
        self.assertNotIn("OPENROUTER_API_KEY_MISSING",
                         {row["code"] for row in manifest["blockers"]})
        self.assertIn("OPENROUTER_API_KEY_MISSING",
                      {row["code"] for row in manifest["downstream_blockers"]})
        with mock.patch.object(HF, "_clean", return_value=False): self.assertIn("GIT_WORKTREE_DIRTY", {row["code"] for row in self.manifest()["blockers"]})
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(HF, "LEDGER", self.ledger):
            _folder, authority, _digest = RUN._authority(self.root, AUTH)
        HF.validate_execution_authority(self.root, authority, key_present=False)
    def test_missing_and_tampered_upstream_receipts_fail_at_exact_boundary(self):
        _folder, authority, authority_sha = self.freeze()
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
                self.assertRaises(RUN.STAGE.StagePending) as stopped:
            RUN.run(self.root, credit_check=lambda: {"remaining_credit": 1}, authority_timestamp=AUTH)
        self.assertEqual("rf21-rf22-authority-bound-native-tasks", stopped.exception.boundary)
        self.assertEqual(authority["next_command"], stopped.exception.resume)
        self.assertEqual([authority["next_command"] + " --native"], stopped.exception.commands)
        path = self.write_upstream(authority, authority_sha)
        with mock.patch.object(SET.SC, "require_subject_contract"):
            self.assertEqual(64, len(UP.verify(self.root, authority, authority_sha)))
        task_path = self.root / UP.FOLDER / "upstream/tasks/rf21-plan.json"
        call_path = self.root / UP.FOLDER / "upstream/calls/rf21-plan.json"
        task = json.loads(task_path.read_text()); task["instruction"] = "validly rehashed substitution"
        task["task_sha256"] = PAIR.PS.state_hash({key: item for key, item in task.items()
                                                  if key != "task_sha256"})
        task_path.chmod(0o644); task_path.write_bytes(PAIR.PS.json_bytes(task))
        call = json.loads(call_path.read_text()); call["task_sha256"] = task["task_sha256"]
        call["input_sha256"] = PAIR.PS.sha(PAIR.PS.json_bytes(task))
        call_path.chmod(0o644); call_path.write_bytes(PAIR.PS.json_bytes(call))
        value = json.loads(path.read_text()); value["calls"][0].update(
            task_sha256=call["task_sha256"], input_sha256=call["input_sha256"])
        value["receipt_hash"] = PAIR.PS.state_hash({key: item for key, item in value.items()
                                                    if key != "receipt_hash"})
        path.chmod(0o644); path.write_bytes(PAIR.PS.json_bytes(value))
        with mock.patch.object(SET.SC, "require_subject_contract"), \
                self.assertRaisesRegex(UP.UpstreamError, "native record binding is stale"):
            UP.verify(self.root, authority, authority_sha)
    def test_run_resumes_one_authority_and_freezes_exactly_six_drafts(self):
        authority, authority_sha, _path = self.authorize_run(); calls = []; credit = mock.Mock(side_effect=AssertionError("credit check on frozen resume"))
        def post(payload):
            calls.append(payload); text = f"# Chapter {len(calls)}\n" + "earned discovery relief " * 280
            return json.dumps({"choices": [{"message": {"content": text}}]}).encode()
        with mock.patch.dict(os.environ, {}, clear=True), \
                mock.patch.object(HF, "LEDGER", self.ledger), \
                mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.STAGE, "advance",
                    side_effect=lambda root, auth, upstream, **_kw: RUN.verify_frozen(root, auth)), \
                mock.patch.object(RUN, "_post", side_effect=post):
            frozen = RUN.run(self.root, credit_check=lambda: {"remaining_credit": 1}, authority_timestamp=AUTH)
        with mock.patch.dict(os.environ, {}, clear=True), \
                mock.patch.object(HF, "LEDGER", self.ledger), \
                mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.STAGE, "advance",
                    side_effect=lambda root, auth, upstream, **_kw: RUN.verify_frozen(root, auth)), \
                mock.patch.object(RUN, "_post", side_effect=AssertionError("duplicate dispatch")):
            again = RUN.run(self.root, credit_check=credit, authority_timestamp=AUTH)
        credit.assert_not_called(); self.assertEqual((6, "BATCH_FROZEN", frozen), (len(calls), again["state"], again))
        self.assertEqual(authority["frozen_at_utc"], AUTH)
        self.assertEqual({"authority.json", UP.PATH, "upstream"}, {
            path.name for path in (self.root / RUN.FOLDER).iterdir()})
        control, treatment = (calls[index]["messages"][0]["content"] for index in (0, 3))
        self.assertIn("frozen_full_style_guide", control); self.assertNotIn("audited_chapter_commission", control)
        self.assertIn("compact_writer_contract", treatment)
        for arm, paths in self.arms.items():
            self.assertEqual("BATCH_FROZEN", PAIR.load(paths["experiment"])["state"])
            batch = BATCH.require_frozen_batch(paths["experiment"])["batch"]; self.assertEqual((3, authority_sha), (len(batch["responses"]), batch["authority_sha256"]))
    def test_ambiguous_call_and_credit_boundary_fail_closed(self):
        self.authorize_run()
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
                mock.patch.object(HF, "LEDGER", self.ledger), \
                mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN, "_post", side_effect=RuntimeError("network lost")):
            with self.assertRaisesRegex(RuntimeError, "network lost"):
                RUN.run(self.root, credit_check=lambda: {"remaining_credit": 1}, authority_timestamp=AUTH)
            with self.assertRaisesRegex(RUN.RunError, "replay is ambiguous"):
                RUN.run(self.root, credit_check=lambda: {"remaining_credit": 1}, authority_timestamp=AUTH)
        response = mock.MagicMock(); response.__enter__.return_value.read.return_value = \
            b'{"data":{"limit_remaining":null}}'
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            self.assertEqual("unlimited", RUN._credit_check(
                open_url=lambda _request, timeout: response)["remaining_credit"])
    def test_zero_credit_stops_before_chapter_generation(self):
        self.authorize_run(); before = self.snapshot(); response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = b'{"data":{"limit_remaining":0}}'
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
                mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN, "_post") as post, self.assertRaisesRegex(RUN.RunError, "remaining credit"):
            RUN.run(self.root, credit_check=lambda: RUN._credit_check(
                open_url=lambda _request, timeout: response), authority_timestamp=AUTH)
        post.assert_not_called(); self.assertEqual(before, self.snapshot())
if __name__ == "__main__": unittest.main()
