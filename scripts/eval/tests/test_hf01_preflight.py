"""Focused H-F01 readiness and durable execution regressions."""
import json, os, shutil, sys, tempfile, unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "scripts/loop"), str(ROOT / "scripts/eval/tests")]
import candidate_pair as PAIR  # noqa: E402
import commission_set as SET  # noqa: E402
import developmental_review as DEV  # noqa: E402
import first_draft_batch as BATCH  # noqa: E402
import grounded_review as GR  # noqa: E402
import hf01_preflight as HF  # noqa: E402
import hf01_run as RUN  # noqa: E402
from commission_packet_fixture import packet  # noqa: E402
from developmental_review_fixture import proven_runner as developmental_runner  # noqa: E402
from grounded_review_fixture import proven_runner as grounded_runner  # noqa: E402
from test_commission_contract import authority, commission  # noqa: E402
def assignment(chapter, source):
    auth = deepcopy(authority())
    old = next(iter(auth["assigned_evidence"]))
    locator = f"{source}#E-001"
    auth["target"] = chapter
    auth["resolved_ids"] = {chapter: auth["required"]["entering belief"]}
    binding = auth["assigned_evidence"].pop(old)
    binding["provenance"] = binding["provenance"].replace(old, locator)
    auth["assigned_evidence"][locator] = binding
    return {"packets": [f"production-books/quit-sugar/research/sources/"
                        f"{source.lower()}-fixture.md"], "authority": auth}

class Hf01Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.ledger = self.root / "tasks.md"
        self.ledger.write_text("### RF-20 — calibration\n- Status: `DONE`\n"
                               "### RF-21 — generation\n- Status: `BLOCKED`\n"
                               "### RF-23 — readiness\n- Status: `READY`\n")
        for relative in ("prompts/style-guide.md", "prompts/chapter-writer.md",
                         "prompts/grounded-reviewer.md", "prompts/developmental-reviewer.md"):
            target = self.root / relative; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, target)
        for relative, text in {
            "prompts/chapter-commissioner.md": "commissioner contract\n",
            "prompts/commission-set-auditor.md": "grounding continuity leakage\n",
            "production-books/quit-sugar/00-brief.md": "Safety perimeter is fixed.\n",
            "production-books/quit-sugar/research/lived-experience.md": "shared lived\n",
            "production-books/quit-sugar/research/scientific-evidence.md": "shared science\n",
            "production-books/quit-sugar/research/sources/s-101-fixture.md":
                packet("S-101", "E-001", "ONLY-ONE"),
            "production-books/quit-sugar/research/sources/s-102-fixture.md":
                packet("S-102", "E-001", "ONLY-TWO"),
            "production-books/quit-sugar/research/sources/s-103-fixture.md":
                packet("S-103", "E-001", "ONLY-THREE"),
            "production-books/quit-sugar/framing.md": "# Framing\n" + "".join(
                f"### CH-{n:02d} — State {n}\n- **Entering belief:** RS-{n-1:02d} | state\n"
                for n in (1, 2, 3)),
            "production-books/quit-sugar/master-plan.md": "# Plan\n\n" + "\n".join(
                f"| EV-L{n:02d} | bounded finding {n} | S-{100+n}#E-001. | "
                f"bounded use {n} | forbidden broadening {n} |" for n in (1, 2, 3)) +
                "\n\n" + "\n\n".join(
                f"### C-{n:02d} — Chapter {n}\n"
                f"- **Belief job:** correct belief {n}.\n"
                f"- **Entering belief:** RS-{n-1:02d} | received state {n}.\n"
                f"- **Leaving belief:** RS-{n:02d} | handed state {n}.\n"
                f"- **Evidence:** EV-L{n:02d}.\n"
                f"- **Guardrails:** safety limit {n}; no diagnosis or willpower.\n"
                f"- **Continuity:** receives received state {n}; hands C-{n+1:02d} "
                f"handed state {n}." for n in (1, 2, 3)),
            "production-books/quit-sugar/master-plan-review.md": "fit to write from\n",
            "production-books/quit-sugar/chapters/chapter-01.md": "baseline one\n",
            "production-books/quit-sugar/chapters/chapter-02.md": "baseline two\n",
            "production-books/quit-sugar/chapters/chapter-03.md": "baseline three\n",
            "calibration/reference/gsbs/reference-metrics.json": '{"chapters": []}\n',
            "calibration/reference/gsbs/chapter-1.txt": "reference\n",
            "loop/results.tsv": "iter\treward\tverdict\n",
            "loop/causal-bundle-results.jsonl": "",
        }.items():
            path = self.root / relative; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        shutil.copy2(ROOT / "loop/config.yaml", self.root / "loop/config.yaml")
        for relative in ("calibration/judges/carr-likeness-rubric.md", *HF.RUBRICS):
            target = self.root / relative; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, target)
        PAIR.initialize(self.root, HF.BOOK)
        self.arms = HF.arm_paths(self.root)
        for paths in self.arms.values():
            paths["experiment"].mkdir(parents=True)
            PAIR.snapshot(paths["experiment"], self.root, HF.BOOK, "1-3")
        (self.arms["treatment"]["book"] / "00-brief.md").write_text(
            "Safety perimeter is fixed. Treatment reader journey is accepted.\n")
        self.assignments = {f"C-{n:02d}": assignment(f"C-{n:02d}", f"S-{100+n}")
                            for n in (1, 2, 3)}
        with mock.patch.object(SET.SC, "require_subject_contract"):
            SET.generate(self.arms["treatment"]["experiment"], self.assignments,
                         lambda request: commission(
                             self.assignments[request["target"]]["authority"]),
                         lambda _request: SET.AUDIT_PASS)

    def tearDown(self): self.tmp.cleanup()

    def manifest(self, **kwargs):
        with mock.patch.object(SET.SC, "require_subject_contract"):
            return HF.build_manifest(self.root, key_present=True, ledger=self.ledger, **kwargs)

    def snapshot(self):
        return {path.relative_to(self.root).as_posix(): PAIR.PS.sha(path.read_bytes())
                for path in self.root.rglob("*") if path.is_file()}

    def test_real_rf02_preflight_is_pure_exact_and_secret_free(self):
        before, secret = self.snapshot(), "do-not-serialize"
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": secret}), \
                mock.patch.object(SET.SC, "require_subject_contract"):
            manifest = HF.build_manifest(self.root, ledger=self.ledger)
        self.assertEqual(before, self.snapshot())
        self.assertTrue(manifest["ready_to_send"])
        self.assertNotIn(secret, json.dumps(manifest))
        self.assertEqual({"method": "POST", "url": HF.URL, "model": HF.MODEL,
                          "reasoning": {"effort": "none"}, "temperature": 0.7,
                          "max_tokens": 16000, "attempts": 1, "fallbacks": []},
                         manifest["route"])
        self.assertTrue(any("research/sources/" in path
                            for path in manifest["shared_research_and_safety"]))

    def test_treatment_brief_may_differ_but_both_briefs_remain_hash_bound(self):
        control = self.arms["control"]["book"] / "00-brief.md"
        treatment = self.arms["treatment"]["book"] / "00-brief.md"
        self.assertNotEqual(control.read_bytes(), treatment.read_bytes())
        manifest = self.manifest()
        self.assertTrue(manifest["ready_to_send"])
        keys = set(manifest["static_input_sha256"])
        self.assertTrue(any(key.endswith("h-f01-control/candidate/" + HF.BOOK +
                                         "/00-brief.md") for key in keys))
        self.assertTrue(any(key.endswith("h-f01-treatment/candidate/" + HF.BOOK +
                                         "/00-brief.md") for key in keys))
        self.assertNotIn(HF.BOOK + "/00-brief.md",
                         manifest["shared_research_and_safety"])

    def test_mutable_manifest_state_is_excluded_but_assignment_is_bound(self):
        authority_manifest = self.manifest()
        pair = self.arms["treatment"]["experiment"] / "pair.json"
        value = json.loads(pair.read_text())
        value["outputs"].reverse()
        pair.write_bytes(PAIR.PS.json_bytes(value))
        with self.assertRaisesRegex(HF.PreflightError, "manifest assignment changed"):
            HF.validate_execution_authority(self.root, authority_manifest, key_present=True)

    def test_fake_manifest_audit_and_high_risk_drift_never_become_ready(self):
        control_pair = self.arms["control"]["experiment"] / "pair.json"
        audit = self.arms["treatment"]["experiment"] / "evidence" / SET.RECEIPT
        for path, fake, code in (
                (control_pair, {"accepted_generation": "a", "accepted_pair_hash": "b",
                                "run": {}}, "RF02_CONTROL_INVALID"),
                (audit, {"schema": 1, "state": "PASSED",
                         "audit": {"result": SET.AUDIT_PASS}}, "COMMISSION_SET_INELIGIBLE")):
            original = path.read_bytes(); path.write_text(json.dumps(fake))
            self.assertIn(code, {item["code"] for item in self.manifest()["blockers"]})
            path.write_bytes(original)
        mutations = (
            (self.arms["control"]["book"] / "research/sources/s-101-fixture.md",
             "\nchanged shared research", "SHARED_RESEARCH_DIFFERS"),
            (self.arms["control"]["candidate"] / "loop/config.yaml",
             "\nwriter_max_tokens: 1", "CONTROL_ROUTE_CONFIG_MISMATCH"),
            (self.arms["treatment"]["book"] / "master-plan.md",
             "\nchanged plan", "COMMISSION_SET_INELIGIBLE"),
            (self.arms["control"]["experiment"] / "evaluation" / HF.RUBRICS[0],
             "\nchanged rubric", "RF02_CONTROL_INVALID"),
        )
        for path, suffix, code in mutations:
            original = path.read_text(); path.write_text(original + suffix)
            with self.subTest(code=code):
                self.assertIn(code, {item["code"] for item in self.manifest()["blockers"]})
            path.write_text(original)

    def test_rf20_rf23_and_key_are_authoritative_but_manifest_still_emits(self):
        self.ledger.write_text("### RF-20 — calibration\n- Status: `DONE`\n"
                               "### RF-23 — readiness\n- Status: `BLOCKED`\n")
        with mock.patch.object(SET.SC, "require_subject_contract"):
            manifest = HF.build_manifest(self.root, key_present=False, ledger=self.ledger)
        self.assertFalse(manifest["ready_to_send"])
        self.assertEqual("NO_SEND_PREFLIGHT", manifest["mode"])
        codes = {item["code"] for item in manifest["blockers"]}
        self.assertTrue({"RF23_NOT_READY", "OPENROUTER_API_KEY_MISSING"} <= codes)

    def test_run_uses_rf11_freezes_both_arms_and_stops_before_review(self):
        calls = []
        def post(payload):
            calls.append(payload)
            self.assertFalse(any(self.root.rglob("grounded-review/receipt.json")))
            self.assertFalse(any(self.root.rglob("developmental-review/receipt.json")))
            if len(calls) == 1:
                receipt = json.loads((self.arms["control"]["experiment"] /
                                      "writer-authority.json").read_text())
                self.assertEqual([1, 2, 3],
                                 [item["chapter"] for item in receipt["control_review"]])
                self.assertNotIn("AUTHORITATIVE SEMANTIC COMMISSION", json.dumps(receipt))
            text = f"# Chapter {len(calls)}\n" + "earned discovery relief " * 280
            return json.dumps({"choices": [{"message": {"content": text}}]}).encode()
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
                mock.patch.object(HF, "LEDGER", self.ledger), \
                mock.patch.object(SET.SC, "require_subject_contract"):
            with mock.patch.object(RUN, "_post", side_effect=post):
                frozen = RUN.run(self.root)
            with mock.patch.object(RUN, "_post", side_effect=AssertionError("duplicate dispatch")):
                frozen = RUN.run(self.root)
                again = RUN.run(self.root)
        self.assertEqual((6, frozen), (len(calls), again))
        self.assertEqual("BATCH_FROZEN", frozen["state"])
        self.assertEqual(list(HF.BOUNDARIES[1:]), frozen["ordered_review_boundaries"])
        self.assertEqual(["authority.json"], sorted(
            path.name for path in (self.root / RUN.FOLDER).iterdir()))
        control, treatment = (calls[index]["messages"][0]["content"] for index in (0, 3))
        self.assertIn("frozen_full_style_guide", control)
        self.assertNotIn("audited_chapter_commission", control)
        self.assertNotIn("AUTHORITATIVE SEMANTIC COMMISSION", control)
        self.assertIn("compact_writer_contract", treatment)
        self.assertNotIn("[N]", treatment)
        self.assertNotIn("[SLUG]", treatment)
        for arm, paths in self.arms.items():
            receipt = BATCH.require_frozen_batch(paths["experiment"])
            self.assertEqual("BATCH_FROZEN", PAIR.load(paths["experiment"])["state"])
            self.assertEqual(3, len(receipt["batch"]["responses"]))
            self.assertEqual(3, len(frozen["arms"][arm]["request_sha256"]))
            with self.assertRaisesRegex(
                PAIR.PairError, "grounded authority|grounded receipt|commission-set-audit"):
                PAIR.seal(paths["experiment"])
        control_root = self.arms["control"]["experiment"]
        treatment_root = self.arms["treatment"]["experiment"]
        control_ground, treatment_ground = GR.prepare(control_root), GR.prepare(treatment_root)
        control_authority = json.dumps(control_ground)
        self.assertNotIn("AUTHORITATIVE SEMANTIC COMMISSION", control_authority)
        self.assertNotIn("/commissions/", control_authority)
        self.assertIn("AUTHORITATIVE SEMANTIC COMMISSION", json.dumps(treatment_ground))
        GR.advance(control_root, runner=grounded_runner())
        GR.advance(treatment_root, runner=grounded_runner())
        control_dev, treatment_dev = DEV.prepare(control_root), DEV.prepare(treatment_root)
        self.assertNotIn("AUTHORITATIVE SEMANTIC COMMISSION", json.dumps(control_dev))
        self.assertNotIn("/commissions/", json.dumps(control_dev))
        self.assertIn("AUTHORITATIVE SEMANTIC COMMISSION", json.dumps(treatment_dev))
        DEV.advance(control_root, runner=developmental_runner())
        DEV.advance(treatment_root, runner=developmental_runner())
        for root in (control_root, treatment_root):
            tested_hash = PAIR.seal(root)
            self.assertEqual(tested_hash, PAIR.verify_sealed(root, tested_hash)["tested_hash"])

    def test_ambiguous_inflight_call_stops_without_fake_resume(self):
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
                mock.patch.object(HF, "LEDGER", self.ledger), \
                mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN, "_post", side_effect=RuntimeError("network lost")):
            with self.assertRaisesRegex(RuntimeError, "network lost"): RUN.run(self.root)
            with self.assertRaisesRegex(RUN.RunError, "replay is ambiguous"):
                RUN.run(self.root)
