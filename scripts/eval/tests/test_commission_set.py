"""Focused RF-09 commission generation, isolation, and audit regressions."""
import json
import os
import shutil
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
sys.path.insert(0, str(ROOT / "scripts/eval/tests"))
import candidate_pair as PAIR  # noqa: E402
import commission_set as SET  # noqa: E402
import pair_store as STORE  # noqa: E402
from test_commission_contract import authority, commission  # noqa: E402
from test_master_plan_review import review_text  # noqa: E402
from research_contract_fixture import (chapter_binding, evidence_row,
                                       write_sealed_research)  # noqa: E402

def assigned(chapter, source, research=None):
    auth = deepcopy(authority())
    old_locator = next(iter(auth["assigned_evidence"]))
    locator = f"{source}#E-001"
    auth["target"] = chapter
    auth["resolved_ids"] = {chapter: auth["required"]["entering belief"]}
    binding = auth["assigned_evidence"].pop(old_locator)
    binding["provenance"] = binding["provenance"].replace(old_locator, locator)
    auth["assigned_evidence"][locator] = binding
    if research is not None:
        auth["research"] = research
    path = f"production-books/test/research/sources/{source}-sealed-fixture.md"
    return {"packets": [path], "authority": auth}

class CommissionSetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.accepted = Path(self.tmp.name) / "repo"
        self.experiment = self.accepted / "loop/experiments/commission-set"
        self.experiment.mkdir(parents=True)
        files = {
            "loop/config.yaml": (
                "judge_rubric: calibration/judges/rubric.md\n"
                "reference_dir: calibration/reference/book\nresults_tsv: loop/results.tsv\n"),
            "loop/results.tsv": "iter\treward\tverdict\n",
            "prompts/chapter-commissioner.md": "commissioner contract\n",
            "prompts/commission-set-auditor.md": "grounding ownership continuity leakage\n",
            "production-books/test/framing.md": (
                "## Cumulative reader-state journey\n"
                "### CH-01 — First\n- **Entering belief:** RS-00 | start\n"
                "### CH-02 — Second\n- **Entering belief:** RS-01 | changed\n"),
            "production-books/test/master-plan.md": (
                "# Plan\n### C-01 — First\n- **Entering belief:** RS-00 | start\n"
                "### C-02 — Second\n- **Entering belief:** RS-01 | changed\n"),
            "production-books/test/master-plan-review.md": "fit to write from\n",
            "production-books/test/chapters/chapter-01.md": "accepted chapter one\n",
            "production-books/test/chapters/chapter-02.md": "accepted chapter two\n",
            "calibration/judges/rubric.md": "rubric\n",
            "calibration/reference/book/reference-metrics.json": '{"chapters": []}\n',
        }
        for relative, text in files.items():
            path = self.accepted / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        report = write_sealed_research(self.accepted / "production-books/test")
        self.research_report = report
        for relative in (
            "calibration/judges/carr-likeness-rubric.md",
            "calibration/judges/product-effect-rubric.md",
            "calibration/judges/product-effect-absolute-rubric.md",
        ):
            target = self.accepted / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, target)
        metrics = self.accepted / "calibration/reference/gsbs/reference-metrics.json"
        metrics.parent.mkdir(parents=True, exist_ok=True)
        metrics.write_text('{"chapters": []}\n', encoding="utf-8")
        units = report["inventory"]["units"]
        plan = ("# Plan\n\n## Evidence ledger\n\n"
                "| ID | Finding / lived material | Research unit IDs | Source ID | Grade or outcome tier | Scope and limit | Permitted inference | Prohibited inference |\n"
                "|---|---|---|---|---|---|---|---|\n" +
                evidence_row(report, "E-01", "LEU-001") + "\n" +
                evidence_row(report, "E-02", "LEU-002") + "\n\n"
                "### C-01 â€” First\n- **Entering belief:** RS-00 | start\n"
                "- **Evidence IDs and required limits:** E-01\n"
                f"- **Guardrails:** {units['LEU-001']['safety']}\n"
                "### C-02 â€” Second\n- **Entering belief:** RS-01 | changed\n"
                "- **Evidence IDs and required limits:** E-02\n"
                f"- **Guardrails:** {units['LEU-002']['safety']}\n")
        (self.accepted / "production-books/test/master-plan.md").write_text(
            plan, encoding="utf-8")
        PAIR.initialize(self.accepted, "production-books/test")
        PAIR.snapshot(self.experiment, self.accepted, "production-books/test", "1-2")
        self.assignments = {
            "C-01": assigned("C-01", "S-001", chapter_binding(report, "E-01", "LEU-001")),
            "C-02": assigned("C-02", "S-002", chapter_binding(report, "E-02", "LEU-002")),
        }

    def tearDown(self):
        self.tmp.cleanup()
    def generate(self, audit=SET.AUDIT_PASS, assignments=None):
        calls, audits = [], []

        def commissioner(request):
            calls.append(request)
            return commission((assignments or self.assignments)[request["target"]]["authority"])

        def auditor(request):
            audits.append(request)
            return audit

        with mock.patch.object(SET.SC, "require_subject_contract"):
            result = SET.generate(self.experiment, assignments or self.assignments,
                                  commissioner, auditor)
        return result, calls, audits

    def current_state(self):
        tree, generation, registry = STORE.current(self.accepted)
        del tree
        workshop = self.accepted / "production-books/test"
        public = tuple((path.relative_to(workshop).as_posix(), path.read_bytes())
                       for path in sorted(workshop.rglob("*")) if path.is_file())
        return generation, registry["pair_hash"], public

    def test_exact_packet_context_and_one_fresh_whole_set_audit(self):
        """OpenSpec requirement: Chapter commission artifact."""
        before = self.current_state()
        with self.assertRaisesRegex(SET.CommissionSetError, "receipt"):
            SET.require_writer_eligible(self.experiment)
        receipt, calls, audits = self.generate()
        self.assertEqual(2, len(calls))
        self.assertEqual(1, len(audits))
        for call, own, other in ((calls[0], "example 1", "example 2"),
                                 (calls[1], "example 2", "example 1")):
            body = json.dumps(call)
            self.assertIn(own, body)
            self.assertNotIn(other, body)
            self.assertNotIn("example 10", body)
            self.assertTrue(call["fresh_context"] and call["reference_blind"])
        audit_body = json.dumps(audits[0])
        self.assertIn("example 1", audit_body)
        self.assertIn("example 2", audit_body)
        self.assertNotIn("example 10", audit_body)
        with mock.patch.object(SET.SC, "require_subject_contract"):
            self.assertEqual(receipt, SET.require_writer_eligible(self.experiment))
        manifest = PAIR.load(self.experiment)
        expected = {f"production-books/test/commissions/chapter-{n:02}.md" for n in (1, 2)}
        self.assertEqual(expected, {item["path"] for item in manifest["outputs"]})
        for path in expected:
            self.assertTrue((PAIR.candidate_tree(self.experiment) / path).is_file())
        tested = PAIR.seal(self.experiment)
        self.assertEqual(tested, PAIR.verify_sealed(self.experiment, tested)["tested_hash"])
        self.assertEqual(before, self.current_state())

    def test_blocked_or_partial_set_never_becomes_writer_eligible(self):
        """OpenSpec scenario: A commission cannot ground its assignment."""
        before = self.current_state()
        blocked = deepcopy(self.assignments)
        blocked["C-02"]["authority"]["blocker"] = {
            "owner": "research/synthesis", "gap": "Assigned evidence cannot support the inference."}
        audit = mock.Mock(return_value=SET.AUDIT_PASS)

        def commissioner(request):
            auth = blocked[request["target"]]["authority"]
            if request["target"] == "C-02":
                gap = auth["blocker"]
                return f"COMMISSION BLOCKED\nOwner: {gap['owner']}\nGap: {gap['gap']}"
            return commission(auth)

        with mock.patch.object(SET.SC, "require_subject_contract"):
            with self.assertRaisesRegex(SET.CommissionSetError, "COMMISSION BLOCKED"):
                SET.generate(self.experiment, blocked, commissioner, audit)
        audit.assert_not_called()
        blocked_path = PAIR.candidate_tree(self.experiment) / \
            "production-books/test/commissions/chapter-02.md"
        self.assertTrue(blocked_path.read_text().startswith("COMMISSION BLOCKED\n"))
        with self.assertRaises(SET.CommissionSetError):
            SET.require_writer_eligible(self.experiment)
        self.assertEqual(before, self.current_state())

    def test_inference_widening_blocks_before_commission_callbacks(self):
        """OpenSpec scenario: A chapter's assigned research is inadequate."""
        plan_path = (PAIR.candidate_tree(self.experiment) /
                     "production-books/test/master-plan.md")
        permitted = self.research_report["inventory"]["units"]["LEU-001"][
            "permitted_inference"]
        plan = plan_path.read_text(encoding="utf-8")
        plan_path.write_text(
            plan.replace(f"| {permitted} |",
                         f"| {permitted}; invented permission |", 1),
            encoding="utf-8",
        )
        commissioner, auditor = mock.Mock(), mock.Mock()
        with mock.patch.object(SET.SC, "require_subject_contract"):
            with self.assertRaisesRegex(SET.ResearchDispatchGap,
                                        "inference_mismatch"):
                SET.generate(self.experiment, self.assignments,
                             commissioner, auditor)
        commissioner.assert_not_called()
        auditor.assert_not_called()

    def test_proven_chapter_gap_yields_read_only_targeted_request(self):
        """OpenSpec scenario: Targeted research resumes only from a proven gap."""
        book = PAIR.candidate_tree(self.experiment) / "production-books/test"
        plan_path = book / "master-plan.md"
        framing_path = book / "framing.md"
        review_path = book / "master-plan-review.md"
        plan = plan_path.read_text(encoding="utf-8")
        plan_path.write_text(
            plan.replace("LEU-001", "LEU-999", 1),
            encoding="utf-8",
        )
        review_path.write_text(
            review_text(plan_path, framing_path), encoding="utf-8")
        before = {path.relative_to(self.experiment).as_posix(): path.read_bytes()
                  for path in self.experiment.rglob("*") if path.is_file()}
        request = SET.chapter_gap_request(self.experiment, 1)
        after = {path.relative_to(self.experiment).as_posix(): path.read_bytes()
                 for path in self.experiment.rglob("*") if path.is_file()}
        self.assertEqual(before, after)
        self.assertEqual({"schema", "research_seal_sha256", "chapter_id",
                          "plan", "card", "gaps"}, set(request))
        self.assertEqual("C-01", request["chapter_id"])
        self.assertEqual("unit_missing", request["gaps"][0]["code"])
        self.assertEqual(
            "Accepted chapter need names an intervention-ready unit absent from "
            "the current sealed corpus.",
            request["gaps"][0]["detail"],
        )
        self.assertEqual(
            "production-books/test/master-plan.md#C-01",
            request["card"]["path"],
        )
        with self.assertRaisesRegex(SET.CommissionSetError, "adequate"):
            plan_path.write_text(plan, encoding="utf-8")
            review_path.write_text(
                review_text(plan_path, framing_path), encoding="utf-8")
            SET.chapter_gap_request(self.experiment, 1)

    def test_tampered_audited_plan_cannot_authorize_targeted_research(self):
        """OpenSpec scenario: Targeted research resumes only from a proven gap."""
        self.generate()
        plan_path = (PAIR.candidate_tree(self.experiment) /
                     "production-books/test/master-plan.md")
        plan_path.write_text(
            plan_path.read_text(encoding="utf-8").replace("LEU-001", "LEU-999", 1),
            encoding="utf-8")
        with self.assertRaisesRegex(SET.CommissionSetError, "owning stage"):
            SET.chapter_gap_request(self.experiment, 1)

    def test_audit_receipt_fails_closed_when_missing_blocked_stale_or_tampered(self):
        """OpenSpec requirement: Candidate isolation and atomic promotion."""
        self.generate()
        commission_path = PAIR.candidate_tree(self.experiment) / \
            "production-books/test/commissions/chapter-01.md"
        original = commission_path.read_text()
        commission_path.write_text("invalid commission\n")
        with mock.patch.object(SET.SC, "require_subject_contract"):
            with self.assertRaisesRegex(SET.CommissionSetError, "invalid commission"):
                SET.require_writer_eligible(self.experiment)
        commission_path.write_text(original)
        for relative in ("production-books/test/chapters/chapter-02.md", "loop/config.yaml"):
            member = PAIR.candidate_tree(self.experiment) / relative
            member_original = member.read_text()
            member.write_text(member_original + "mutated after pass\n")
            with mock.patch.object(SET.SC, "require_subject_contract"):
                with self.assertRaisesRegex(SET.CommissionSetError,
                                            r"stale|hash-mismatched"):
                    SET.require_writer_eligible(self.experiment)
            member.write_text(member_original)
        commission_path.unlink()
        with self.assertRaisesRegex(SET.CommissionSetError, "missing"):
            SET.require_writer_eligible(self.experiment)
        commission_path.write_text(original)
        receipt_path = PAIR.evidence_tree(self.experiment) / SET.RECEIPT
        receipt = json.loads(receipt_path.read_text())
        receipt["bindings"]["plan_sha256"] = "0" * 64
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        with self.assertRaisesRegex(SET.CommissionSetError, "receipt hash mismatch"):
            SET.require_writer_eligible(self.experiment)

    def test_undeclared_or_escaping_outputs_are_rejected(self):
        """OpenSpec scenario: An operation root contains an unsafe path."""
        manifest_path = self.experiment / PAIR.MANIFEST
        manifest = json.loads(manifest_path.read_text())
        manifest["outputs"] = [{"group": "product", "path": "production-books/test/evil.md"}]
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(PAIR.PairError, "commission outputs"):
            PAIR.load(self.experiment)

        other = self.accepted / "loop/experiments/path-escape"
        other.mkdir()
        PAIR.snapshot(other, self.accepted, "production-books/test", "1-2")
        escaped = deepcopy(self.assignments)
        escaped["C-01"]["packets"] = ["../outside.md"]
        with mock.patch.object(SET.SC, "require_subject_contract"):
            with self.assertRaisesRegex(SET.CommissionSetError, "outside its accepted source bank"):
                SET.generate(other, escaped, mock.Mock(), mock.Mock())

        aliased = self.accepted / "loop/experiments/aliased-output"
        aliased.mkdir()
        PAIR.snapshot(aliased, self.accepted, "production-books/test", "1-2")
        target = PAIR.candidate_tree(aliased) / "production-books/test/commissions/chapter-01.md"
        target.parent.mkdir()
        try:
            target.symlink_to(self.accepted / "production-books/test/00-brief.md")
        except OSError as exc:
            if os.name == "nt" and getattr(exc, "winerror", None) in {50, 1314}:
                self.skipTest("Windows symlink creation is unavailable")
            raise
        with self.assertRaisesRegex(SET.CommissionSetError, "aliased"):
            SET.generate(aliased, self.assignments, mock.Mock(), mock.Mock())

    def test_blocked_whole_set_audit_persists_no_eligibility(self):
        """OpenSpec requirement: Chapter commission artifact."""
        verdict = "COMMISSION SET BLOCKED\nOwner: commission/context\nGap: C-02 breaks the handoff."
        with self.assertRaisesRegex(SET.CommissionSetError, "audit blocked"):
            self.generate(verdict)
        receipt = json.loads((PAIR.evidence_tree(self.experiment) / SET.RECEIPT).read_text())
        self.assertEqual("BLOCKED", receipt["state"])
        with self.assertRaisesRegex(SET.CommissionSetError, "no passing"):
            SET.require_writer_eligible(self.experiment)

    def test_invalid_selection_or_book_fails_before_validation_and_callbacks(self):
        """OpenSpec requirement: Chapter commission artifact."""
        manifest_path = self.experiment / PAIR.MANIFEST
        original = json.loads(manifest_path.read_text())
        actual, validator, commissioner, auditor = (mock.Mock() for _ in range(4))
        invalid_runs = [
            {**original["run"], "chapters": chapters}
            for chapters in ([], [1, 1], [0], ["1"], [2, 1])
        ] + [{**original["run"], "book": book}
             for book in ("../outside", "production-books/Bad", "production-books/a/b")]
        with mock.patch.object(SET.CP, "_actual", actual), \
                mock.patch.object(SET.SC, "require_subject_contract", validator):
            for run in invalid_runs:
                invalid = {**original, "run": run}
                manifest_path.write_text(json.dumps(invalid), encoding="utf-8")
                with self.assertRaises(SET.CommissionSetError):
                    SET.generate(self.experiment, self.assignments, commissioner, auditor)
                with self.assertRaises(SET.CommissionSetError):
                    SET.require_writer_eligible(self.experiment)
        actual.assert_not_called()
        validator.assert_not_called()
        commissioner.assert_not_called()
        auditor.assert_not_called()


if __name__ == "__main__":
    unittest.main()
