"""Focused H-F01 readiness and durable execution regressions."""
import json, os, shutil, sys, tempfile, unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "scripts/loop"), str(ROOT / "scripts/eval/tests")]
import candidate_pair as PAIR  # noqa: E402
import commission_set as SET  # noqa: E402
import hf01_preflight as HF  # noqa: E402
import hf01_run as RUN  # noqa: E402
from commission_packet_fixture import packet  # noqa: E402
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
        for relative in ("prompts/style-guide.md", "prompts/chapter-writer.md"):
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
            "production-books/quit-sugar/master-plan.md": "# Plan\n" + "".join(
                f"### C-{n:02d} — Chapter {n}\n- **Entering belief:** RS-{n-1:02d} | state\n"
                for n in (1, 2, 3)),
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
        self.assignments = {f"C-{n:02d}": assignment(f"C-{n:02d}", f"S-{100+n}")
                            for n in (1, 2, 3)}
        with mock.patch.object(SET.SC, "require_subject_contract"):
            SET.generate(self.arms["treatment"]["experiment"], self.assignments,
                         lambda request: commission(
                             self.assignments[request["target"]]["authority"]),
                         lambda _request: SET.AUDIT_PASS)
        self.baseline = {f"{arm}-{n}": (paths["book"] /
            f"chapters/chapter-{n:02d}.md").read_bytes()
            for arm, paths in self.arms.items() for n in HF.CHAPTERS}

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
        self.assertEqual(("DONE", "READY"),
                         (manifest["authority"]["rf20_status"],
                          manifest["authority"]["rf23_status"]))
        self.assertTrue(any("research/sources/" in path
                            for path in manifest["shared_research_and_safety"]))

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

    def test_run_persists_all_raw_responses_then_writes_freezes_and_resumes(self):
        calls = []
        def post(payload):
            calls.append(payload)
            for arm, paths in self.arms.items():
                for number in HF.CHAPTERS:
                    self.assertEqual(self.baseline[f"{arm}-{number}"],
                                     (paths["book"] / f"chapters/chapter-{number:02d}.md").read_bytes())
            text = f"# Chapter {len(calls)}\n" + "earned discovery relief " * 280
            return json.dumps({"choices": [{"message": {"content": text}}]}).encode()
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
                mock.patch.object(HF, "LEDGER", self.ledger), \
                mock.patch.object(SET.SC, "require_subject_contract"):
            with mock.patch.object(RUN, "_post", side_effect=post), \
                    mock.patch.object(RUN, "_write_chapters",
                                      side_effect=RUN.RunError("stop after responses")):
                with self.assertRaisesRegex(RUN.RunError, "stop after responses"):
                    RUN.run(self.root)
            with mock.patch.object(RUN, "_post",
                                   side_effect=AssertionError("duplicate dispatch")):
                frozen = RUN.run(self.root)
                again = RUN.run(self.root)
        self.assertEqual(6, len(calls))
        self.assertEqual(frozen, again)
        self.assertEqual("FROZEN", frozen["state"])
        self.assertEqual(list(HF.BOUNDARIES[1:]), frozen["ordered_review_boundaries"])
        folder = self.root / RUN.FOLDER
        self.assertEqual(6, len(list(folder.glob("*.response.json"))))
        control, treatment = (calls[index]["messages"][0]["content"] for index in (1, 4))
        self.assertIn("frozen_full_style_guide", control)
        self.assertNotIn("audited_chapter_commission", control)
        self.assertIn("compact_writer_contract", treatment)
        self.assertNotIn("[N]", treatment)
        self.assertNotIn("[SLUG]", treatment)
        self.assertFalse(any(folder.glob("*review*")))

    def test_orphan_marker_blocks_duplicate_dispatch_with_resume_command(self):
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}), \
                mock.patch.object(HF, "LEDGER", self.ledger), \
                mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN, "_post", side_effect=RuntimeError("network lost")):
            with self.assertRaisesRegex(RuntimeError, "network lost"): RUN.run(self.root)
            with self.assertRaisesRegex(RUN.RunError, r"orphan call marker.*--snapshot-root"):
                RUN.run(self.root)


if __name__ == "__main__": unittest.main()
