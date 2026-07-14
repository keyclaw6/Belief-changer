"""RF-03 regressions for the book-pipeline Brief artifact contract."""
import tempfile
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_subject_contract as SC  # noqa: E402


VALID = """# Brief — Stop compulsive phone checking

## Target behavior
Compulsively checking a smartphone without a chosen purpose.

## Intended reader
Adults who repeatedly interrupt work and rest to check their phones.

## Fork decisions
- **Outcome (Fork 2):** Intentional phone use without automatic checking.
- **Void (Fork 5):** Restore the natural baseline without a replacement ritual.
- **Science weight (Fork 3):** Use bounded evidence to clarify mechanisms.
- **Villain (Fork 4):** Name attention-capture product incentives where sourced.
- **Inner state (Fork 1):** Externalize the learned belief without blaming the reader.

## Destination
The reader uses the phone by deliberate choice and feels no pull to keep checking.

## Exclusions
This edition does not address required on-call monitoring or device accessibility use.

## Safety perimeter
Preserve emergency access and route clinically significant anxiety to qualified care.

## Primary false belief
- "Checking my phone keeps me informed and in control."

## Subordinate beliefs
- "A quick check will help me settle and focus."
- "I might miss something important if I wait."
- "Checking is the easiest way to fill an empty moment."
"""


def without_section(text, name):
    marker = f"## {name}\n"
    start = text.index(marker)
    next_heading = text.find("\n## ", start + len(marker))
    return text[:start] + (text[next_heading + 1:] if next_heading >= 0 else "")


def replace_section(text, name, body):
    marker = f"## {name}\n"
    start = text.index(marker) + len(marker)
    end = text.find("\n## ", start)
    if end < 0:
        end = len(text)
    return text[:start] + body.rstrip() + "\n" + text[end:]


class SubjectContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.book = Path(self.tmp.name) / "production-books/stop-phone-checking"
        self.book.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, text=VALID):
        (self.book / "00-brief.md").write_text(text, encoding="utf-8")

    def test_complete_non_sugar_contract_passes_every_gate(self):
        """OpenSpec scenario: Downstream work starts from an incomplete subject contract."""
        self.write()
        for stage in SC.STAGES:
            with self.subTest(stage=stage):
                self.assertEqual(self.book / "00-brief.md",
                                 SC.require_subject_contract(self.book, stage))

    def test_missing_or_empty_brief_fails_closed(self):
        """OpenSpec scenario: Planning begins without a brief."""
        for stage in SC.STAGES:
            with self.subTest(stage=stage, state="missing"):
                with self.assertRaises(SC.ContractError):
                    SC.require_subject_contract(self.book, stage)
        self.write("")
        for stage in SC.STAGES:
            with self.subTest(stage=stage, state="empty"):
                with self.assertRaises(SC.ContractError):
                    SC.require_subject_contract(self.book, stage)

    def test_each_required_field_is_mandatory(self):
        """OpenSpec scenario: Downstream work starts from an incomplete subject contract."""
        required = (*SC.SCALAR_FIELDS, "Fork decisions", *SC.BELIEF_FIELDS)
        for name in required:
            with self.subTest(field=name):
                self.write(without_section(VALID, name))
                with self.assertRaisesRegex(SC.ContractError, "missing section"):
                    SC.require_subject_contract(self.book, "planning")

    def test_each_fork_decision_is_mandatory(self):
        """OpenSpec scenario: Downstream work starts from an incomplete subject contract."""
        for name in SC.FORKS:
            line = next(line for line in VALID.splitlines() if f"**{name}:**" in line)
            with self.subTest(fork=name):
                self.write(VALID.replace(line + "\n", ""))
                with self.assertRaisesRegex(SC.ContractError, "missing fork decision"):
                    SC.require_subject_contract(self.book, "framing")

    def test_empty_placeholder_and_unresolved_values_fail(self):
        """OpenSpec scenario: Downstream work starts from an incomplete subject contract."""
        cases = {
            "empty": "",
            "placeholder": "<reader to be filled>",
            "unresolved": "TBD after research",
            "pending research": "Pending research.",
            "pending research bang": "Pending research!",
            "to be determined": "To be determined.",
            "to be determined question": "To be determined?",
            "tbc": "TBC",
            "tbc bang": "TBC!",
            "question marks": "???",
            "question marks period": "???.",
            "punctuation only": "!!!",
            "alternatives": "Adults | teens",
        }
        for label, value in cases.items():
            with self.subTest(case=label):
                self.write(replace_section(VALID, "Intended reader", value))
                with self.assertRaisesRegex(SC.ContractError, "unresolved section"):
                    SC.require_subject_contract(self.book, "research-synthesis")
        substantive = (
            '- "One quick check cannot really hurt, can it?"',
            '- "Surely one quick check cannot hurt???"',
            '- "I need to check now!"',
        )
        for reader_belief in substantive:
            self.write(replace_section(VALID, "Primary false belief", reader_belief))
            SC.require_subject_contract(self.book, "research-synthesis")

    def test_primary_belief_requires_one_reader_language_bullet(self):
        """OpenSpec scenario: Downstream work starts from an incomplete subject contract."""
        cases = (
            '- "One belief."\n- "Another belief."',
            "The reader believes checking helps.",
            '- "<belief to decide>"',
        )
        for value in cases:
            with self.subTest(value=value):
                self.write(replace_section(VALID, "Primary false belief", value))
                with self.assertRaises(SC.ContractError):
                    SC.require_subject_contract(self.book, "planning")

    def test_subordinate_belief_count_is_three_to_five(self):
        """OpenSpec scenario: Downstream work starts from an incomplete subject contract."""
        for count in (0, 1, 2, 6):
            beliefs = "\n".join(f'- "Reader belief {n}."' for n in range(count))
            with self.subTest(count=count):
                self.write(replace_section(VALID, "Subordinate beliefs", beliefs))
                with self.assertRaises(SC.ContractError):
                    SC.require_subject_contract(self.book, "planning")
        for count in (3, 4, 5):
            beliefs = "\n".join(f'- "Reader belief {n}."' for n in range(count))
            with self.subTest(count=count):
                self.write(replace_section(VALID, "Subordinate beliefs", beliefs))
                SC.require_subject_contract(self.book, "planning")

    def test_template_remains_generic_and_fails_until_completed(self):
        """OpenSpec scenario: Downstream work starts from an incomplete subject contract."""
        template = ROOT / "production-books/_template/00-brief.md"
        text = template.read_text(encoding="utf-8").lower()
        for topic_word in ("sugar", "food", "eating", "diet", "addiction"):
            self.assertNotIn(topic_word, text)
        with self.assertRaises(SC.ContractError):
            SC.validate_text(template.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
