"""Focused RF-08 regressions for the natural-language commission contract."""
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_commission_contract as CC  # noqa: E402


def authority(subject="phone"):
    if subject == "phone":
        values = {
            "assumptions received": "No prior correction is assumed.",
            "entering belief": "The reader enters believing each urge signals useful information.",
            "leaving belief": "The urge is a question rather than useful information.",
            "situation": "The phone is unlocked during a quiet work pause before any purpose is named.",
            "reader wording": "I unlock it before I even know why.",
            "permitted mechanism": "Compare the promised information with what the check actually changes.",
            "emotional turn": "Self-blame loosens into amused recognition.",
            "empirical limits": "This single report does not establish prevalence or a clinical effect.",
            "safety limits": "Do not diagnose anxiety or prescribe withdrawal from necessary contact.",
            "handoff": "The next chapter may test whether checking created the relief it claims.",
            "assumptions handed forward": "Carry forward that an urge can be examined without obeying it.",
            "reserved work": "Fear of missing out and intentional notification choices remain elsewhere.",
        }
        return {
            "target": "C-01", "required": values,
            "resolved_ids": {"C-01": values["entering belief"]},
            "assigned_evidence": {
                "S-101#E-001": {
                    "values": {name: values[name] for name in CC.SOURCE_OWNED},
                    "statuses": {
                        name: "EXACT_QUOTE" if name == "reader wording" else "INTERPRETATION"
                        for name in CC.SOURCE_OWNED
                    },
                    "provenance": (
                        "Assigned evidence S-101#E-001: situation, permitted mechanism, and "
                        "empirical limits are INTERPRETATION; reader wording is EXACT_QUOTE."
                    ),
                },
            },
            "frozen_tokens": ("The urge is not an instruction.",),
            "forbidden": (
                "notifications cause clinical anxiety", "LEU-099",
                "demolish fear of missing out in this chapter",
            ),
        }
    values = {
        "assumptions received": "No prior correction is assumed for the flight encounter.",
        "entering belief": "The reader enters believing bodily alarm predicts danger.",
        "leaving belief": "Bodily alarm is a feeling rather than a forecast.",
        "situation": "Turbulence begins after the seat-belt sign sounds on a routine flight.",
        "reader wording": "I know the plane is safe, but my body says run.",
        "permitted mechanism": "Contrast anticipatory arousal with the evidence used to judge the flight.",
        "emotional turn": "Embarrassment gives way to steady recognition.",
        "empirical limits": "The report does not establish the safety of a particular flight.",
        "safety limits": "Do not override crew instructions or give medical advice.",
        "handoff": "The next chapter may examine avoidance as borrowed relief.",
        "assumptions handed forward": "Carry forward that alarm and external danger are different claims.",
        "reserved work": "Exposure decisions and clinical treatment remain outside this chapter.",
    }
    return {
        "target": "C-01", "required": values,
        "resolved_ids": {"C-01": values["entering belief"]},
        "assigned_evidence": {
            "S-202#E-004": {
                "values": {name: values[name] for name in CC.SOURCE_OWNED},
                "statuses": {
                    name: "EXACT_QUOTE" if name == "reader wording" else "INTERPRETATION"
                    for name in CC.SOURCE_OWNED
                },
                "provenance": (
                    "Assigned evidence S-202#E-004: situation, permitted mechanism, and "
                    "empirical limits are INTERPRETATION; reader wording is EXACT_QUOTE."
                ),
            },
        },
        "frozen_tokens": ("A feeling is not a forecast.",), "forbidden": (),
    }


def commission(auth):
    r = auth["required"]
    binding = next(iter(auth["assigned_evidence"].values()))
    token = auth["frozen_tokens"][0]
    return f"""AUTHORITATIVE SEMANTIC COMMISSION — {auth['target']}

{r['assumptions received']} {r['entering belief']} {r['situation']} The assigned exact reader wording is "{r['reader wording']}". {binding['provenance']}

{r['permitted mechanism']} {r['emotional turn']} {r['leaving belief']} Preserve the frozen words `{token}`.

{r['empirical limits']} {r['safety limits']} {r['handoff']} {r['assumptions handed forward']} {r['reserved work']}"""


def blocked(base, owner, gap):
    auth = deepcopy(base)
    auth["blocker"] = {"owner": owner, "gap": gap}
    return auth, f"COMMISSION BLOCKED\nOwner: {owner}\nGap: {gap}"


class CommissionContractTests(unittest.TestCase):
    def test_smartphone_and_fear_commissions_use_one_generic_contract(self):
        """Infra: RF-08 transfers through contrasting subject fixtures."""
        for subject in ("phone", "fear"):
            with self.subTest(subject=subject):
                auth = authority(subject)
                self.assertEqual("commission", CC.validate_text(commission(auth), auth))
                self.assertNotIn("sugar", commission(auth).casefold())

    def test_every_assigned_semantic_value_is_carried(self):
        """OpenSpec requirement: Chapter commission artifact."""
        auth = authority()
        for name, value in auth["required"].items():
            with self.subTest(name=name):
                bad = commission(auth).replace(value, "", 1)
                with self.assertRaisesRegex(CC.ContractError, f"assigned {name}"):
                    CC.validate_text(bad, auth)

    def test_blocked_fixtures_name_each_owning_gap(self):
        """OpenSpec scenario: A commission cannot ground its assignment."""
        cases = (
            ("plan", "RS-09 has no accepted reader-language meaning."),
            ("research/synthesis", "The packet cannot support the intended clinical inference."),
            ("commission/context", "LEU-099 is not in the assigned packet set."),
            ("plan", "Fear-of-missing-out demolition is reserved for C-03."),
            ("plan", "The leaving belief conflicts with the accepted handed-forward state."),
        )
        for owner, gap in cases:
            with self.subTest(gap=gap):
                auth, text = blocked(authority(), owner, gap)
                self.assertEqual("blocked", CC.validate_text(text, auth))
                with self.assertRaisesRegex(CC.ContractError, "COMMISSION BLOCKED"):
                    CC.validate_text(commission(authority()), auth)
        auth, text = blocked(authority(), "writing", "Obsolete owner label.")
        with self.assertRaisesRegex(CC.ContractError, "canonical vocabulary"):
            CC.validate_text(text, auth)

    def test_only_assigned_ids_inferences_work_and_quotes_pass(self):
        """OpenSpec scenario: A commission cannot ground its assignment."""
        auth = authority()
        mutations = (
            (" RS-99", "unresolved or unassigned ID"),
            (" P-99", "unresolved or unassigned ID"),
            (" AU-99", "unresolved or unassigned ID"),
            (" GAP-001", "COMMISSION BLOCKED required for research gap"),
            (' "A fresh invented line."', "quote is not assigned"),
            (" Notifications cause clinical anxiety.", "prohibited material"),
            (" LEU-099", "unresolved or unassigned ID"),
            (" Demolish fear of missing out in this chapter.", "prohibited material"),
        )
        for addition, error in mutations:
            with self.subTest(addition=addition):
                with self.assertRaisesRegex(CC.ContractError, error):
                    CC.validate_text(commission(auth) + addition, auth)
        unresolved = deepcopy(auth)
        unresolved["resolved_ids"]["C-01"] = "A meaning absent from the commission."
        with self.assertRaisesRegex(CC.ContractError, "ID lacks its resolved meaning"):
            CC.validate_text(commission(auth), unresolved)
        unquoted = commission(auth).replace(
            '"I unlock it before I even know why."', '`I unlock it before I even know why.`'
        )
        with self.assertRaisesRegex(CC.ContractError, "exact quotation"):
            CC.validate_text(unquoted, auth)

    def test_source_owned_values_require_assigned_provenance(self):
        """OpenSpec scenario: A commission cannot ground its assignment."""
        auth = authority()
        binding = next(iter(auth["assigned_evidence"].values()))
        without_provenance = commission(auth).replace(binding["provenance"], "")
        with self.assertRaisesRegex(CC.ContractError, "lacks assigned evidence provenance"):
            CC.validate_text(without_provenance, auth)
        unsupported = deepcopy(auth)
        locator = next(iter(unsupported["assigned_evidence"]))
        del unsupported["assigned_evidence"][locator]["values"]["permitted mechanism"]
        with self.assertRaisesRegex(CC.ContractError, "COMMISSION BLOCKED.*source-owned field"):
            CC.validate_text(commission(auth), unsupported)

    def test_frozen_tokens_are_exact_and_outline_or_prose_is_rejected(self):
        """Infra: RF-08 preserves exact tokens without drafting chapter anatomy."""
        auth = authority()
        altered = commission(auth).replace("The urge is not an instruction.", "An urge is no instruction.")
        with self.assertRaisesRegex(CC.ContractError, "frozen token"):
            CC.validate_text(altered, auth)
        for addition in (
            "\n\n## Opening", "\n\nBegin the chapter with a dramatic question.",
            "\n\nSection 1 — Recognize the signal", "\n\nAsk the reader: What changed?",
        ):
            with self.subTest(addition=addition):
                with self.assertRaisesRegex(CC.ContractError, "outline anatomy or drafted prose"):
                    CC.validate_text(commission(auth) + addition, auth)

    def test_assigned_belief_and_frozen_text_may_be_quoted(self):
        """Infra: RF-08 permits only assigned semantic, source, and frozen quotes."""
        auth = authority()
        r = auth["required"]
        quoted_beliefs = commission(auth).replace(
            r["entering belief"], f'"{r["entering belief"]}"', 1
        ).replace(r["leaving belief"], f'“{r["leaving belief"]}”', 1)
        self.assertEqual("commission", CC.validate_text(quoted_beliefs, auth))
        token = auth["frozen_tokens"][0]
        quoted_token = commission(auth).replace(f"`{token}`", f'"{token}"')
        self.assertEqual("commission", CC.validate_text(quoted_token, auth))
        embedded = deepcopy(auth)
        embedded_value = "The reader enters believing “checking proves I am informed.”"
        embedded["required"]["entering belief"] = embedded_value
        embedded["resolved_ids"]["C-01"] = embedded_value
        self.assertEqual("commission", CC.validate_text(commission(embedded), embedded))
        with self.assertRaisesRegex(CC.ContractError, "quote is not assigned"):
            CC.validate_text(commission(auth) + '\n"An unassigned source-like report."', auth)

    def test_prompt_keeps_a_fresh_editorial_role_and_free_form_output(self):
        """Infra: RF-08 prompt transport remains a commission, not RF-09 runtime."""
        prompt = (ROOT / "prompts/chapter-commissioner.md").read_text(encoding="utf-8")
        for phrase in (
            "fresh high-reasoning commissioning editor", "only the assigned source packets",
            "assumptions received", "empirical and safety limits", "exact frozen token",
            "assigned locator and provenance status", "source-owned situation",
            "Do not force the material into a fixed schema or checklist", "COMMISSION BLOCKED",
        ):
            self.assertIn(phrase, prompt)


if __name__ == "__main__":
    unittest.main()
