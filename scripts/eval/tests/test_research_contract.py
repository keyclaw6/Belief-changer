"""Focused OpenSpec regressions for intervention-ready research synthesis."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_research_contract as RC  # noqa: E402
FORKS = """- **Outcome (Fork 2):** freedom from the behavior
- **Void (Fork 5):** ordinary life is the clean baseline
- **Science weight (Fork 3):** use bounded evidence
- **Villain (Fork 4):** name the external trap
- **Inner state (Fork 1):** treat discomfort without shame"""
def brief(title, beliefs):
    subordinate = "\n".join(f'- "{belief}"' for belief in beliefs[1:])
    return f"""# Brief — {title}

## Target behavior
{title}

## Intended reader
An adult who wants freedom from {title.lower()}.

## Fork decisions
{FORKS}

## Destination
Calm freedom without avoidance or white-knuckling.

## Exclusions
Diagnosis, treatment, and unrelated behaviors.

## Safety perimeter
Medical or acute psychological concerns go to a qualified professional.

## Primary false belief
- "{beliefs[0]}"

## Subordinate beliefs
{subordinate}
"""
def packet(source_id, grades, disposition="ACCEPTED"):
    evidence = []
    for number, grade in enumerate(grades, 1):
        evidence.append(f"""### E-{number:03d}

- **Kind:** EXACT_QUOTE
- **Text:** I need this right now.
- **Excerpt ID:** C-001
- **Locator:** paragraph {number}
- **Persona tags:** P-01
- **Bank slots:** Bank 2; Bank 3
- **Evidence grade:** {grade}
- **Use / limits:** At a specific cue, the reader reaches for the behavior. The reported emotion is unease before the behavior and disappointment after it. This source supports this cue and expectation. It does not establish prevalence or diagnosis.
""")
    return f"""# {source_id} — Accepted fixture source

- **Source ID:** {source_id}
- **URL:** https://example.test/{source_id.lower()}
- **Title:** Rights-clean fixture
- **Source type:** community
- **Retrieved (UTC):** 2026-07-14T00:00:00Z
- **Access / license basis:** public page accessed normally under fixture license
- **Excerpt / redistribution basis:** minimum excerpt may be retained for verification
- **Required attribution:** Example author
- **Retention / deletion sensitivity:** durable, non-deletion-sensitive source
- **Privacy / personal-data basis:** no identifying personal details retained
- **Disposition:** {disposition}

## Minimum retained excerpt

### C-001

- **Locator:** paragraphs 1–4
- **Capture method:** page text

```text
I need this right now.
```

## Evidence items

{"".join(evidence)}"""
def unit(unit_id, belief, locator, grade="n/a", omit=None):
    fields = (
        ("Situation", "At a specific cue, the reader reaches for the behavior."),
        ("Reader wording", '"I need this right now."'),
        ("Implicated belief", f'"{belief}"'),
        ("Emotion", "unease before the behavior and disappointment after it"),
        ("Permitted inference", "This source supports this cue and expectation."),
        ("Prohibited inference", "It does not establish prevalence or diagnosis."),
        ("Source locator", locator),
        ("Evidence grade", grade),
    )
    body = "\n".join(
        f"- **{name}:** {value}" for name, value in fields if name != omit
    )
    return f"### {unit_id}\n\n{body}\n"
def gap(belief, owner="research/synthesis"):
    return f"""### GAP-001

- **Implicated belief:** "{belief}"
- **Missing support:** No accepted source yet supplies concrete reader wording.
- **Owner:** {owner}
"""
class ResearchContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.book = self.tmp / "book"
        self.research = self.book / "research"
        (self.research / "sources").mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmp)
    def write_fixture(self, title, beliefs, grades, science_first=False):
        (self.book / "00-brief.md").write_text(brief(title, beliefs), encoding="utf-8")
        source = self.research / "sources/s-001-fixture.md"
        source.write_text(packet("S-001", grades), encoding="utf-8")
        lived_units = []
        science_units = []
        for number, belief in enumerate(beliefs, 1):
            locator = f"S-001#E-{number:03d}"
            if science_first and number == 1:
                science_units.append(unit("SEU-001", belief, locator, grades[0]))
            else:
                lived_units.append(unit(f"LEU-{number:03d}", belief, locator, grades[number - 1]))
        (self.research / "lived-experience.md").write_text(
            "# Lived\n\n" + "\n".join(lived_units), encoding="utf-8"
        )
        (self.research / "scientific-evidence.md").write_text(
            "# Science\n\n" + "\n".join(science_units), encoding="utf-8"
        )
    def test_smartphone_units_cover_the_completed_brief(self):
        """OpenSpec: Synthesized research — Synthesis cites an unsourced claim."""
        beliefs = (
            "Checking now helps me stay in control.",
            "A quick look will only take a moment.",
            "The phone settles my unease.",
            "I might miss something important.",
        )
        self.write_fixture("Compulsive smartphone checking", beliefs, ["n/a"] * 4)
        self.assertEqual(4, len(RC.require_research_contract(self.book)))
        self.assertEqual(47, len(RC._packet_index(ROOT / "production-books/quit-sugar/research/sources")))
        self.assertEqual(self.book / "00-brief.md", RC.subject.require_subject_contract(self.book, "framing"))
    def test_fear_of_flying_transfers_and_keeps_scientific_grade(self):
        """OpenSpec: Synthesized research — Synthesis cites an unsourced claim."""
        beliefs = (
            "My fear is the warning that keeps me safe.",
            "Turbulence means the aircraft is in danger.",
            "If I relax, I will lose control.",
            "Avoiding flights protects me from panic.",
        )
        self.write_fixture("Fear of flying", beliefs, ["SUPPORTED", "n/a", "n/a", "n/a"], True)
        source = self.research / "sources/s-001-fixture.md"
        source.write_text(source.read_text(encoding="utf-8").replace(
            "- **Evidence grade:** SUPPORTED",
            "- **Evidence grade:** SUPPORTED for this claim; CONTESTED if broadened",
        ), encoding="utf-8")
        self.assertEqual(4, len(RC.require_research_contract(self.book)))
        science = self.research / "scientific-evidence.md"
        science.write_text(science.read_text(encoding="utf-8").replace(
            "- **Evidence grade:** SUPPORTED", "- **Evidence grade:** MIXED"
        ), encoding="utf-8")
        with self.assertRaisesRegex(RC.ContractError, "grade is not grounded"):
            RC.require_research_contract(self.book)
        self.write_fixture("Fear of flying", beliefs, ["SUPPORTED", "n/a", "n/a", "n/a"], True)
        source.write_text(source.read_text(encoding="utf-8").replace(
            "- **Evidence grade:** SUPPORTED", "- **Evidence grade:** n/a", 1
        ), encoding="utf-8")
        with self.assertRaisesRegex(RC.ContractError, "grade is not grounded"):
            RC.require_research_contract(self.book)

    def test_partial_or_untraceable_unit_fails(self):
        """OpenSpec: Synthesized research — Synthesis cites an unsourced claim."""
        beliefs = ("Belief one.", "Belief two.", "Belief three.", "Belief four.")
        self.write_fixture("Generic checking", beliefs, ["n/a"] * 4)
        lived = self.research / "lived-experience.md"
        text = lived.read_text(encoding="utf-8")
        lived.write_text(text.replace("- **Prohibited inference:** It does not establish prevalence or diagnosis.\n", "", 1), encoding="utf-8")
        with self.assertRaisesRegex(RC.ContractError, "missing field Prohibited inference"):
            RC.require_research_contract(self.book)
        self.write_fixture("Generic checking", beliefs, ["n/a"] * 4)
        text = lived.read_text(encoding="utf-8")
        lived.write_text(text.replace("S-001#E-001", "S-001#E-999", 1), encoding="utf-8")
        with self.assertRaisesRegex(RC.ContractError, "unknown source locator"):
            RC.require_research_contract(self.book)
        for old, new, error in (
            ('"I need this right now."', '"Invented reader wording."', "reader wording"),
            ("This source supports this cue and expectation.", "Invented mechanism.", "not permitted"),
        ):
            self.write_fixture("Generic checking", beliefs, ["n/a"] * 4)
            lived.write_text(lived.read_text(encoding="utf-8").replace(old, new, 1), encoding="utf-8")
            with self.assertRaisesRegex(RC.ContractError, error):
                RC.require_research_contract(self.book)

    def test_missing_support_routes_to_research_and_stops(self):
        """OpenSpec: Synthesized research — A planned belief lacks usable evidence."""
        beliefs = ("Belief one.", "Belief two.", "Belief three.", "Belief four.")
        self.write_fixture("Generic checking", beliefs, ["n/a"] * 4)
        lived = self.research / "lived-experience.md"
        text = lived.read_text(encoding="utf-8")
        start = text.index("### LEU-004")
        lived.write_text(text[:start] + gap(beliefs[3]), encoding="utf-8")
        with self.assertRaisesRegex(RC.ResearchGap, "GAP-001"):
            RC.require_research_contract(self.book)
        sentinel = self.tmp / "downstream-ran"
        gate = ROOT / "scripts/validate_subject_contract.py"
        command = '"$1" "$2" --book "$3" --stage framing && touch "$4"'
        result = subprocess.run(
            ["bash", "-c", command, "stage-gate", sys.executable, str(gate),
             str(self.book), str(sentinel)], check=False,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(sentinel.exists())

    def test_rejected_rights_material_is_neither_tracked_nor_counted(self):
        """OpenSpec: Synthesized research — Research material fails rights or privacy review."""
        beliefs = ("Belief one.", "Belief two.", "Belief three.", "Belief four.")
        self.write_fixture("Generic checking", beliefs, ["n/a"] * 4)
        rejected = self.research / "sources/s-001-fixture.md"
        rejected.write_text(packet("S-001", ["n/a"] * 4, "REJECTED"), encoding="utf-8")
        with self.assertRaisesRegex(RC.ContractError, "rejected material must stay out of Git"):
            RC.require_research_contract(self.book)
    def test_rights_and_excerpt_placeholders_fail_closed(self):
        """OpenSpec: Synthesized research — Research material fails rights or privacy review."""
        beliefs = ("Belief one.", "Belief two.", "Belief three.", "Belief four.")
        cases = (
            ("https://example.test/s-001", "unknown"),
            ("public page accessed normally under fixture license", "<TBD rights basis>"),
            ("public page accessed normally under fixture license", "n/a"),
            ("- **Excerpt / redistribution basis:** minimum excerpt may be retained for verification\n", ""),
            ("minimum excerpt may be retained for verification", "none"),
            ("Example author", "<TBD attribution>"),
            ("Example author", "unknown"),
            ("durable, non-deletion-sensitive source", "<TBD retention>"),
            ("durable, non-deletion-sensitive source", "not available"),
            ("no identifying personal details retained", "<TBD privacy basis>"),
            ("no identifying personal details retained", "unknown"),
            ("I need this right now.\n```", "<TBD excerpt>\n```"),
        )
        for old, new in cases:
            self.write_fixture("Generic checking", beliefs, ["n/a"] * 4)
            source = self.research / "sources/s-001-fixture.md"
            source.write_text(source.read_text(encoding="utf-8").replace(old, new, 1), encoding="utf-8")
            with self.assertRaises(RC.ContractError):
                RC.require_research_contract(self.book)
        self.write_fixture("Generic checking", beliefs, ["n/a"] * 4)
        source.write_text(source.read_text(encoding="utf-8")
                          .replace("Example author", "n/a", 1)
                          .replace("public page accessed normally under fixture license",
                                   "n/a appears in this substantive licensed-access explanation", 1),
                          encoding="utf-8")
        RC.require_research_contract(self.book)


if __name__ == "__main__":
    unittest.main()
