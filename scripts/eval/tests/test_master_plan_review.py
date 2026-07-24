"""Focused RF-07 regressions for blocking cumulative plan review."""
import hashlib
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts/loop"))
sys.path.insert(0, str(Path(__file__).parent))
import hf01_upstream as UP  # noqa: E402
import validate_framing_contract as FC  # noqa: E402
import validate_master_plan_review as MPR  # noqa: E402
import validate_research_contract as RC  # noqa: E402
import validate_subject_contract as SC  # noqa: E402
from test_master_plan_contract import framing, plan, research_report  # noqa: E402
from test_subject_contract import VALID as VALID_BRIEF  # noqa: E402

PASS_FINDINGS = {
    "First-three cumulative walk": "PASS — three distinct corrections change the reader now",
    "Whole-book cumulative walk": "PASS — every handoff reaches the declared destination",
    "Opening persuasive work": "PASS — each opening card completes persuasive work now",
    "Deferred catalogue or future investigation": "PASS — no primary work is deferred",
    "Adjacent discovery modes": "PASS — adjacent cards enact distinct discovery modes",
    "Leaving-belief handoffs": "PASS — every leaving belief is a changed belief and the next entry",
    "Writer-facing authority": "PASS — every card resolves its evidence limits and ownership",
    "Other material blocker": "PASS — none",
}
BLOCKING_FINDINGS = {
    "three setup chapters": (
        "First-three cumulative walk",
        "BLOCK — plan | C-01, C-02, C-03 | all three only establish setup; complete one correction in each card",
    ),
    "deferred catalogue": (
        "Deferred catalogue or future investigation",
        "BLOCK — plan | C-02 | benefit catalogue is saved for later demolition; enact the owned correction now",
    ),
    "adjacent duplicate modes": (
        "Adjacent discovery modes",
        "BLOCK — plan | C-01, C-02 | both cards use the same comparison mode; assign C-02 a distinct discovery",
    ),
    "keep-reading exit": (
        "Leaving-belief handoffs",
        "BLOCK — plan | C-01 | exit state only agrees to keep reading; name the corrected belief handed forward",
    ),
    "unresolved writer authority": (
        "Writer-facing authority",
        "BLOCK — plan | C-03 | evidence limit is unresolved; bind the card to an exact permitted inference",
    ),
}


def review_text(plan_path, framing_path, findings=None, verdict="fit to write from", role=MPR.ROLE,
                model="gpt-5.6-sol", reasoning="xhigh"):
    findings = findings or PASS_FINDINGS
    rows = "\n".join(f"- **{name}:** {findings[name]}" for name in MPR.CHECKS)
    return f"""# Master Plan Review — Phone Freedom

## Review identity and binding
- **Reviewer role:** {role}
- **Fresh-context independence:** {MPR.INDEPENDENCE}
- **Exact runtime model ID:** {model}
- **Reasoning configuration:** {reasoning}
- **Reference blindness:** {MPR.BLINDNESS}
- **Reviewed plan:** complete master-plan.md
- **Master-plan SHA-256:** {hashlib.sha256(plan_path.read_bytes()).hexdigest()}
- **Reviewed framing:** exact accepted framing.md
- **Framing SHA-256:** {hashlib.sha256(framing_path.read_bytes()).hexdigest()}

## Cumulative reader-walk findings
{rows}

{verdict}
"""


class MasterPlanReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.book = self.tmp / "production-books/stop-phone-checking"
        self.book.mkdir(parents=True)
        (self.book / "00-brief.md").write_text(VALID_BRIEF, encoding="utf-8")
        self.plan = self.book / "master-plan.md"
        self.framing = self.book / "framing.md"
        self.plan.write_text(plan(), encoding="utf-8")
        self.framing.write_text(framing(), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write_review(self, **kwargs):
        text = review_text(self.plan, self.framing, **kwargs)
        (self.book / "master-plan-review.md").write_text(text, encoding="utf-8")
        return text

    def test_only_clean_cumulative_review_fits(self):
        """OpenSpec scenario: A master plan is drafted."""
        text = self.write_review()
        self.assertEqual("fit to write from", MPR.validate_review(text, self.plan, self.framing))
        self.assertNotIn("sugar", text.casefold())

    def test_rf21_review_route_satisfies_the_unmocked_blocking_contract(self):
        """OpenSpec scenario: RF-21 and RF-22 dispatch is durable and authority-bound."""
        spec = UP._spec(1)
        self.assertEqual(("gpt-5.6-sol", "xhigh"), (spec["model"], spec["reasoning"]))
        self.assertEqual(
            ["framing-review-template", "master-plan-reviewer-prompt", "style-guide", "brief",
             "framing", "master-plan", "lived-synthesis", "scientific-synthesis"],
            spec["input_contract"]["members"],
        )
        text = review_text(self.plan, self.framing, model=spec["model"], reasoning=spec["reasoning"])
        self.assertEqual("fit to write from", MPR.validate_review(text, self.plan, self.framing))

    def test_every_cumulative_blocker_requires_changes(self):
        """OpenSpec scenarios: opening defers work; cumulative reader walk unresolved."""
        for label, (field, finding) in BLOCKING_FINDINGS.items():
            with self.subTest(label=label):
                findings = dict(PASS_FINDINGS)
                findings[field] = finding
                text = self.write_review(findings=findings, verdict="needs changes first")
                self.assertEqual("needs changes first", MPR.validate_review(text, self.plan, self.framing))
                with self.assertRaisesRegex(MPR.ContractError, "verdict is needs changes first"):
                    MPR.require_master_plan_review(self.book)

    def test_stale_hash_wrong_reviewer_and_malformed_verdict_fail(self):
        """Infra: exact artifacts, independent reviewer, and standalone verdict are fail-closed."""
        text = self.write_review()
        for changed, message in (
            (text.replace(hashlib.sha256(self.plan.read_bytes()).hexdigest(), "0" * 64), "stale for master-plan"),
            (text.replace(hashlib.sha256(self.framing.read_bytes()).hexdigest(), "0" * 64), "stale for accepted framing"),
            (text.replace(MPR.ROLE, "chapter writer"), "not a writer"),
            (text.replace("gpt-5.6-sol", "chapter-writer-solstice"), "exact native planning-review model"),
            (text.replace("fit to write from\n", "FIT TO WRITE FROM\n"), "exact standalone verdict"),
        ):
            with self.subTest(message=message), self.assertRaisesRegex(MPR.ContractError, message):
                MPR.validate_review(changed, self.plan, self.framing)
        findings = dict(PASS_FINDINGS)
        findings["Writer-facing authority"] = BLOCKING_FINDINGS["unresolved writer authority"][1]
        with self.assertRaisesRegex(MPR.ContractError, "verdict must be needs changes first"):
            MPR.validate_review(review_text(self.plan, self.framing, findings), self.plan, self.framing)

    def test_pass_cannot_hide_an_incomplete_scope(self):
        """Infra: RF-07 PASS findings reject unresolved scope markers anywhere."""
        for detail in (
            "pending whole-book review completion",
            "TODO: complete the whole-book review",
            "whole-book review is incomplete",
            "whole-book scope was not reviewed",
            "whole-book scope was not-reviewed",
            "whole-book scope was not-yet-reviewed",
        ):
            findings = dict(PASS_FINDINGS)
            findings["Whole-book cumulative walk"] = f"PASS — {detail}"
            with self.subTest(detail=detail), self.assertRaisesRegex(
                MPR.ContractError, "unresolved cumulative review finding"
            ):
                MPR.validate_review(review_text(self.plan, self.framing, findings), self.plan, self.framing)
        findings = dict(PASS_FINDINGS)
        findings["Whole-book cumulative walk"] = "PASS — no pending plan work remains; every card was reviewed"
        self.assertEqual(
            "fit to write from",
            MPR.validate_review(review_text(self.plan, self.framing, findings), self.plan, self.framing),
        )

    def test_commissioning_refuses_everything_except_exact_fit(self):
        """OpenSpec scenario: A chapter is commissioned before the plan is fit."""
        with patch.object(RC, "require_research_contract", return_value=()), patch.object(
            RC, "inspect_research", return_value=research_report(), create=True), patch.object(
            FC, "require_framing_contract", return_value=self.framing
        ):
            with self.assertRaisesRegex(SC.ContractError, "missing or empty master plan review"):
                SC.require_subject_contract(self.book, "commissioning")
            findings = dict(PASS_FINDINGS)
            findings["First-three cumulative walk"] = BLOCKING_FINDINGS["three setup chapters"][1]
            self.write_review(findings=findings, verdict="needs changes first")
            with self.assertRaisesRegex(SC.ContractError, "verdict is needs changes first"):
                SC.require_subject_contract(self.book, "commissioning")
            self.write_review(verdict="fit to write from now")
            with self.assertRaisesRegex(SC.ContractError, "exact standalone verdict"):
                SC.require_subject_contract(self.book, "commissioning")
            self.write_review()
            self.plan.write_text(plan() + "\n", encoding="utf-8")
            with self.assertRaisesRegex(SC.ContractError, "review is stale for master-plan"):
                SC.require_subject_contract(self.book, "commissioning")
            self.plan.write_text(plan(), encoding="utf-8")
            self.write_review()
            self.assertEqual(self.book / "00-brief.md", SC.require_subject_contract(self.book, "commissioning"))


if __name__ == "__main__":
    unittest.main()
