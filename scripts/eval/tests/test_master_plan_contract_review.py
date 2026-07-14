"""RF-06 regressions for independent review attempt 1."""
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).parent))
import validate_framing_contract as FC  # noqa: E402
import validate_master_plan_contract as MPC  # noqa: E402
import validate_research_contract as RC  # noqa: E402
import validate_subject_contract as SC  # noqa: E402
from test_master_plan_contract import TRANSITIONS, framing, plan  # noqa: E402
from test_subject_contract import VALID as VALID_BRIEF  # noqa: E402


class MasterPlanReviewRepairTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.book = self.tmp / "production-books/stop-phone-checking"
        self.book.mkdir(parents=True)
        (self.book / "00-brief.md").write_text(VALID_BRIEF, encoding="utf-8")
        (self.book / "framing.md").write_text(framing(), encoding="utf-8")
        self.write(plan())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write(self, text):
        (self.book / "master-plan.md").write_text(text, encoding="utf-8")

    def assert_invalid(self, text, message):
        self.write(text)
        with self.assertRaisesRegex(MPC.ContractError, message):
            MPC.require_master_plan_contract(self.book)

    def test_total_budget_is_positive_present_and_equal_to_cards(self):
        """Infra: RF-06 total budget binds every positive chapter budget."""
        total = "**Total planned word budget:** 3000\n"
        cases = (
            (plan().replace(total, ""), "Total planned word budget"),
            (plan().replace("3000", "6000", 1), "do not equal Total planned"),
            (plan().replace("3000", "0", 1), "invalid positive integer"),
        )
        for text, message in cases:
            with self.subTest(message=message):
                self.assert_invalid(text, message)

    def test_arc_and_card_budgets_are_exactly_once_and_positive(self):
        """Infra: RF-06 each chapter has one matching validated budget."""
        row1 = "| C-01 | 1 — Move | correction 1 | movement 1 | slot 1 | 1000 |\n"
        row3 = "| C-03 | 3 — Move | correction 3 | movement 3 | slot 3 | 1000 |\n"
        cases = (
            (plan().replace(row3, ""), "exactly one budget"),
            (plan().replace(row1, row1 + row1), "exactly one budget"),
            (plan().replace("- **Word budget:** 1000\n", "", 1), "missing field Word budget"),
            (plan().replace("| slot 1 | 1000 |", "| slot 1 | 0 |", 1), "invalid positive integer"),
        )
        for text, message in cases:
            with self.subTest(message=message):
                self.assert_invalid(text, message)

    def test_cards_reject_prose_anatomy_and_copied_arc_rows(self):
        """Infra: RF-06 cards contain semantic fields, never prose anatomy or tables."""
        anatomy = """#### IN THIS CHAPTER
Preview the claims that later chapters will address.

#### SUMMARY
This chapter prepared the reader to continue.

"""
        self.assert_invalid(
            plan().replace("- **Word budget:** 1000\n", anatomy + "- **Word budget:** 1000\n", 1),
            "only permitted semantic fields",
        )
        copied_arc = "| C-01 | 1 — Move | correction 1 | movement 1 | slot 1 | 1000 |\n"
        self.assert_invalid(
            plan().replace("- **Word budget:** 1000\n", "- **Word budget:** 1000\n" + copied_arc, 1),
            "arc-map rows may appear only",
        )

    def test_commissioning_rejects_a_coherent_replacement_journey(self):
        """OpenSpec scenario: The cumulative reader walk is unresolved."""
        alternate = (
            ("The signal is trustworthy.", TRANSITIONS[0][1], TRANSITIONS[0][2], "The signal can be questioned."),
            ("The signal can be questioned.", TRANSITIONS[1][1], TRANSITIONS[1][2], "The ritual has no proof."),
            ("The ritual has no proof.", TRANSITIONS[2][1], TRANSITIONS[2][2], "The ritual is unnecessary."),
        )
        replacements = (
            (plan(alternate), "normalized meanings"),
            (re.sub(r"RS-(0[0-3])", lambda match: f"RS-{int(match.group(1)) + 10:02d}", plan()), "state IDs"),
        )
        with patch.object(RC, "require_research_contract", return_value=()), patch.object(
            FC, "require_framing_contract", return_value=self.book / "framing.md"
        ):
            for text, kind in replacements:
                with self.subTest(kind=kind):
                    self.write(text)
                    with self.assertRaisesRegex(SC.ContractError, "accepted framing journey"):
                        SC.require_subject_contract(self.book, "commissioning")


if __name__ == "__main__":
    unittest.main()
