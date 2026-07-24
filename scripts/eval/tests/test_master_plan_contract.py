"""Focused RF-06 regressions for semantic master-plan chapter cards."""
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
from test_subject_contract import VALID as VALID_BRIEF  # noqa: E402

TARGET = "Compulsive smartphone checking"
TRANSITIONS = (
    (
        "The urge seems like useful information.",
        "Compare the promised relief with the unease already present.",
        "Relief replaces self-blame.",
        "The urge is a question, not useful information.",
    ),
    (
        "The urge is a question, not useful information.",
        "Run a before-and-after test of what the check actually changed.",
        "Suspicion becomes amused recognition.",
        "Checking claims credit for relief it did not create.",
    ),
    (
        "Checking claims credit for relief it did not create.",
        "Reassign each real benefit to its actual source in the hardest scene.",
        "Recognition opens into confident freedom.",
        "Nothing valuable depends on automatic checking.",
    ),
)


def _card(index, states=TRANSITIONS):
    entering, discovery, emotion, leaving = states[index - 1]
    card_id = f"C-{index:02d}"
    reserved = (
        f"{', '.join(f'C-{n:02d}' for n in range(index + 1, 4))} — distinct later transitions"
        if index < 3 else "none — the opening transition is complete"
    )
    return f"""### {card_id} — Chapter {index}: Distinct move {index}

- **Primary persuasive job:** enacted transition — complete correction {index} now
- **Objection / justification resolved:** the reader's current justification {index}
- **Entering belief:** RS-{index - 1:02d} | {entering}
- **Concrete subject-specific encounter:** During {TARGET}, encounter {index} makes the promise observable.
- **Enacted discovery:** {discovery}
- **Emotional turn:** {emotion}
- **Leaving belief:** RS-{index:02d} | {leaving}
- **Assumptions handed forward:** RS-{index:02d} | {leaving}
- **Work reserved elsewhere:** {reserved}
- **Arc and curve:** movement {index}; demolition rises and freedom becomes clearer
- **Target personas / reader voice:** P-01 — "This check matters right now."
- **Evidence IDs and required limits:** E-{index:02d}; preserve its prohibited inference
- **Mantras:** debut M-01; echo M-02
- **Instruction:** I-01
- **Concrete scene / original analogy:** S-{index:02d} — perform discovery mode {index}
- **Structural responsibility:** distinct movement {index}
- **Guardrails:** warm to the reader; attack the trap; preserve evidence limits
- **Continuity intent:** receive RS-{index - 1:02d} → hand forward RS-{index:02d}
- **Word budget:** 1000
"""


def plan(states=TRANSITIONS):
    evidence = "\n".join(
        f"| E-{index:02d} | finding {index} | LEU-{index:03d} | S-001#E-{index:03d} | lived tier | scope | allowed | forbidden |"
        for index in range(1, 4)
    )
    arc = "\n".join(
        f"| C-{index:02d} | {index} — Move | correction {index} | movement {index} | slot {index} | 1000 |"
        for index in range(1, 4)
    )
    return f"""# Master Plan — Phone Freedom

**Target behavior:** {TARGET}
**Primary reader / functional personas:** one reader, P-01 through P-03
**Format:** full-length
**Planned chapter count:** 3
**Total planned word budget:** 3000
**Load-bearing false belief:** Checking creates control.
**Destination:** Deliberate phone use without an automatic pull.

## Evidence ledger
| ID | Finding / lived material | Research unit IDs | Source ID | Grade or outcome tier | Scope and limit | Permitted inference | Prohibited inference |
|---|---|---|---|---|---|---|---|
{evidence}

## Mantra sheet
| ID | Frozen wording | Job | Debut | Echo | Hand-over |
|---|---|---|---|---|---|
| M-01 | The promise is not the result. | expose | C-01 | C-02 | reader-owned |
| M-02 | I choose when to look. | freedom | C-02 | C-03 | reader-owned |

## Instruction spine
| ID | Frozen instruction | Owner | Recap | Type |
|---|---|---|---|---|
| I-01 | Observe the promise and result. | C-01 | final | epistemic |

## Arc and length map
| Chapter ID | Title | Job | Arc | Responsibility | Word budget |
|---|---|---|---|---|---:|
{arc}

## Compact chapter cards

{''.join(_card(index, states) for index in range(1, 4))}"""


def research_report():
    return {"ok": True, "status": "PASS", "seal_identity": "a" * 64,
            "blockers": [], "inventory": {"units": {
        f"LEU-{index:03d}": {"locators": [f"S-001#E-{index:03d}"],
                              "permitted_inference": "allowed",
                              "prohibited_inference": "forbidden"}
        for index in range(1, 4)}}}


def framing(states=TRANSITIONS):
    cards = []
    for index, (entering, _, _, leaving) in enumerate(states, 1):
        cards.append(f"""### CH-{index:02d} — Accepted transition {index}
- **Entering belief:** RS-{index - 1:02d} | {entering}
- **Leaving belief:** RS-{index:02d} | {leaving}
- **Handed-forward state:** RS-{index:02d} | {leaving}
""")
    return "# Framing fixture\n\n## Cumulative reader-state journey\n\n" + "\n".join(cards)


def remove_field(text, field, occurrence=1):
    pattern = rf"^- \*\*{re.escape(field)}:\*\*.*\n"
    return re.sub(pattern, "", text, count=occurrence, flags=re.M)


class MasterPlanContractTests(unittest.TestCase):
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

    def test_three_distinct_cumulative_transition_modes_pass(self):
        """Infra: RF-06 generic three-mode acceptance control."""
        self.assertEqual(("C-01", "C-02", "C-03"), MPC.validate_text(plan()))
        self.assertNotIn("sugar", plan().casefold())

    def test_setup_catalogue_and_deferred_primary_jobs_fail(self):
        """OpenSpec scenario: The opening defers its persuasive work."""
        original = "enacted transition — complete correction 1 now"
        bad_jobs = (
            "setup — define terms for later",
            "topic coverage — introduce the subject",
            "enacted transition — catalogue benefits for later demolition",
            "enacted transition — define a future investigation",
            "enacted transition — publish a prospectus of claims",
        )
        for job in bad_jobs:
            with self.subTest(job=job):
                self.assert_invalid(plan().replace(original, job, 1), "cannot be the primary job|must be an enacted")

    def test_every_transition_field_is_complete(self):
        """OpenSpec requirement: Master plan artifact has seven semantic fields."""
        for field in MPC.TRANSITION_FIELDS:
            with self.subTest(field=field, state="missing"):
                self.assert_invalid(remove_field(plan(), field), f"missing field {re.escape(field)}")
            unresolved = re.sub(
                rf"^- \*\*{re.escape(field)}:\*\*.*$",
                f"- **{field}:** pending",
                plan(), count=1, flags=re.M,
            )
            with self.subTest(field=field, state="unresolved"):
                self.assert_invalid(unresolved, f"{re.escape(field)}: unresolved value")

    def test_retained_card_authority_and_budget_stay_blocking(self):
        """Infra: RF-06 retains evidence, repetition, variation, continuity, and budget."""
        retained = {
            "Evidence IDs and required limits", "Mantras", "Instruction",
            "Concrete scene / original analogy", "Continuity intent", "Word budget",
        }
        for field in retained:
            with self.subTest(field=field):
                self.assert_invalid(remove_field(plan(), field), f"missing field {re.escape(field)}")
        self.assert_invalid(plan().replace("| slot 1 | 1000 |", "| slot 1 | 900 |", 1), "budget does not match")

    def test_continuity_and_discovery_modes_are_cumulative(self):
        """OpenSpec scenario: The cumulative reader walk is unresolved."""
        self.assert_invalid(
            plan().replace(
                "- **Entering belief:** RS-01 | The urge is a question, not useful information.",
                "- **Entering belief:** RS-09 | An unrelated belief.",
                1,
            ),
            "breaks the prior handoff",
        )
        self.assert_invalid(
            plan().replace(TRANSITIONS[1][1], TRANSITIONS[0][1], 1),
            "duplicate the enacted discovery mode",
        )

    def test_plan_wide_inventory_cannot_be_duplicated_in_a_card(self):
        """Infra: RF-06 cards reference rather than duplicate shared inventories."""
        duplicate = "\n| E-01 | copied finding | S-001 | lived tier | scope | allowed | forbidden |\n"
        self.assert_invalid(plan().replace("- **Word budget:** 1000\n", "- **Word budget:** 1000\n" + duplicate, 1), "plan-wide inventory")

    def test_commissioning_stage_enforces_cards_and_rf07_verdict(self):
        """Infra: RF-06 card gate remains before the RF-07 independent verdict."""
        report = research_report()
        with patch.object(RC, "require_research_contract", return_value=()), patch.object(
            RC, "inspect_research", return_value=report, create=True), patch.object(
            FC, "require_framing_contract", return_value=self.book / "framing.md"
        ):
            with self.assertRaisesRegex(SC.ContractError, "master plan review not ready"):
                SC.require_subject_contract(self.book, "commissioning")
            self.write(plan().replace(TRANSITIONS[1][1], TRANSITIONS[0][1], 1))
            with self.assertRaisesRegex(SC.ContractError, "master plan not ready"):
                SC.require_subject_contract(self.book, "commissioning")

    def test_plan_evidence_rows_bind_current_sealed_units(self):
        """OpenSpec requirement: Accepted research and immediate chapter adequacy."""
        report = research_report()
        with patch.object(RC, "inspect_research", return_value=report, create=True):
            self.assertEqual(self.book / "master-plan.md",
                             MPC.require_master_plan_contract(self.book))
            for old, new, error in (
                ("LEU-001", "LEU-999", "absent from current seal"),
                ("S-001#E-001", "S-999#E-999", "locators differ"),
                ("| allowed | forbidden |", "| widened | forbidden |",
                 "inference limits differ"),
                ("| allowed | forbidden |", "| allowed plus invented permission | forbidden |",
                 "inference limits differ"),
            ):
                with self.subTest(error=error):
                    self.write(plan().replace(old, new, 1))
                    with self.assertRaisesRegex(MPC.ContractError, error):
                        MPC.require_master_plan_contract(self.book)

    def test_blocked_research_report_cannot_authorize_master_plan(self):
        """OpenSpec RF-32: planning requires a current accepted research seal."""
        report = research_report()
        report.update(ok=False, status="BLOCKED", seal_identity=None,
                      blockers=["seal missing"])
        with patch.object(RC, "inspect_research", return_value=report, create=True), \
                self.assertRaisesRegex(MPC.ContractError, "seal missing"):
            MPC.require_master_plan_contract(self.book)


if __name__ == "__main__":
    unittest.main()
