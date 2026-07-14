"""Focused OpenSpec regressions for the framing artifact."""
import hashlib, re, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).parent))
import validate_framing_contract as FC  # noqa: E402
import validate_subject_contract as SC  # noqa: E402
from test_research_contract import brief, packet, unit  # noqa: E402
PLAYBOOK = (
    "Load-bearing false belief", "Illusory benefit and inversion",
    "Justifications to demolish", "Engineered villain",
    "Physical or chemical reality and science weight",
    "Natural baseline or root and replacement", "Behavior-specific analogies",
    "Escape routes to foreclose", "Strongest seductive scene",
    "Moment of revelation",
)
def review(text, pedigree="PASS — no invented pedigree", danger="PASS — no unsupported danger", overreach="PASS — no evidence overreach", verdict="ACCEPTED FOR PLANNING"):
    return f"""# Framing Review
- **Reviewer role:** independent high-reasoning native planning-family reviewer (Sol or equivalent)
- **Independence:** independent of the framing planner and writer
- **Reviewed artifact:** complete framing.md
- **Framing SHA-256:** {hashlib.sha256(text.encode()).hexdigest()}
- **Invented pedigree:** {pedigree}
- **Unsupported danger:** {danger}
- **Evidence overreach:** {overreach}
- **Verdict:** {verdict}
"""
def framing(title, beliefs):
    graph = []
    for index, belief in enumerate(beliefs, 1):
        kind = "primary" if index == 1 else "subordinate"
        deps = ", ".join(f"BG-{n:02d}" for n in range(2, len(beliefs) + 1)) if index == 1 else "none"
        graph.append(f"""### BG-{index:02d}
- **Kind:** {kind}
- **Belief:** "{belief}"
- **Depends on:** {deps}
""")
    answers = "\n".join(
        f"{index}. **{name}:** {title} answer {index} grounded in the accepted framing inputs."
        for index, name in enumerate(PLAYBOOK, 1)
    )
    return f"""# Framing — {title}

## Contract metadata
- **Planner role:** high-reasoning native planner (Sol or equivalent)
- **Writer role:** distinct downstream writer model

## Format and scope decisions
- **Format:** full-length because the belief graph needs a cumulative journey
- **Redefinition decision:** not applicable — the brief defines a clean destination

### P-01
- **Function:** immediate relief
- **Load-bearing belief:** the cue means action is necessary
- **Dialect:** it feels urgent in the moment

### P-02
- **Function:** felt safety
- **Load-bearing belief:** vigilance prevents a feared outcome
- **Dialect:** relaxing feels irresponsible

### P-03
- **Function:** regained control
- **Load-bearing belief:** the ritual restores control
- **Dialect:** one small action will settle this

## Style-guide Section 10 adaptation playbook
{answers}

## Mantra seeds
- **Trap-namer:** the false-alarm trap
- **Illusion-namer:** promised control, manufactured unease
- **Mechanism characters:** the cue and the story that magnifies it
- **Sensory definition:** a tight, urgent pull
- **Named anti-method:** the vigilance method
- **Named conflict model:** the false-alarm loop
- **Named positive authority:** direct observation and the reality check
- **Terminal mantra:** I can see the trap and I am free
- **Claim block:** Understanding removes the need to struggle

## Personal-experience use
Use accepted recognition language without turning individual reports into prevalence claims.

## Fork positions
- **Fork 1:** externalize the small cue without inventing a mighty enemy
- **Fork 2:** follow the brief's concrete destination
- **Fork 3:** use bounded evidence only
- **Fork 4:** attack the trap and the vigilance method, never the reader
- **Fork 5:** ordinary life is the baseline named in the brief

## Belief graph
{"".join(graph)}
## Evidence-honest authority strategy

### AU-01
- **Basis:** recognition
- **Subject-specific move:** Name the exact {title} cue in the reader's own language.
- **Evidence units:** LEU-001
- **Claim:** This source supports this cue and expectation.
- **Danger claim:** none
- **Limits:** It does not establish prevalence or diagnosis.

### AU-02
- **Basis:** bounded lived pattern
- **Subject-specific move:** Compare the before-and-after pattern reported around {title}.
- **Evidence units:** LEU-002
- **Claim:** This source supports this cue and expectation.
- **Danger claim:** none
- **Limits:** It does not establish prevalence or diagnosis.

### AU-03
- **Basis:** logic
- **Subject-specific move:** Ask whether {title} can provide control if it repeatedly renews the need for control.
- **Evidence units:** none
- **Claim:** A claimed rescue cannot be credited for a need it renews.
- **Danger claim:** none
- **Limits:** Logic does not establish prevalence or medical outcomes.

## Cumulative reader-state journey

### CH-01 — Notice the cue
- **Belief nodes resolved:** BG-02
- **Entering belief:** RS-00 | The behavior seems necessary.
- **Subject-specific encounter:** At the first {title} cue, the reader notices the urge before acting.
- **Discovery mechanism:** Compare the promised settling with the unease already present.
- **Emotional turn:** Self-blame softens into curiosity.
- **Leaving belief:** RS-01 | The cue can be examined instead of obeyed.
- **Handed-forward state:** RS-01 | The cue can be examined instead of obeyed.
- **Reserved work:** BG-01, BG-03, BG-04 remain for later stages.

### CH-02 — Test the promise
- **Belief nodes resolved:** BG-03
- **Entering belief:** RS-01 | The cue can be examined instead of obeyed.
- **Subject-specific encounter:** During a second {title} moment, the reader compares promise with result.
- **Discovery mechanism:** Isolate what changed and what the ritual merely claimed credit for.
- **Emotional turn:** Suspicion becomes relief.
- **Leaving belief:** RS-02 | The promise is not evidence of a benefit.
- **Handed-forward state:** RS-02 | The promise is not evidence of a benefit.
- **Reserved work:** BG-01, BG-04 remain for the final stage.

### CH-03 — Resolve the graph
- **Belief nodes resolved:** BG-04, BG-01
- **Entering belief:** RS-02 | The promise is not evidence of a benefit.
- **Subject-specific encounter:** In the strongest {title} scene, the reader reassigns every real benefit.
- **Discovery mechanism:** Follow each claimed benefit to its actual source and resolve the dependency graph.
- **Emotional turn:** Relief opens into confident freedom.
- **Leaving belief:** RS-03 | No false benefit remains worth preserving.
- **Handed-forward state:** RS-03 | No false benefit remains worth preserving.
- **Reserved work:** none — the graph is resolved before planning.
"""
class FramingContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.book = self.tmp / "book"
        (self.book / "research/sources").mkdir(parents=True)
    def tearDown(self):
        shutil.rmtree(self.tmp)
    def write_subject(self, title, beliefs):
        (self.book / "00-brief.md").write_text(brief(title, beliefs), encoding="utf-8")
        (self.book / "research/sources/s-001-fixture.md").write_text(
            packet("S-001", ["n/a"] * len(beliefs)), encoding="utf-8",
        )
        units = "\n".join(
            unit(f"LEU-{index:03d}", belief, f"S-001#E-{index:03d}")
            for index, belief in enumerate(beliefs, 1)
        )
        (self.book / "research/lived-experience.md").write_text("# Lived\n\n" + units, encoding="utf-8")
        (self.book / "research/scientific-evidence.md").write_text("# Science\n", encoding="utf-8")
        text = framing(title, beliefs)
        (self.book / "framing.md").write_text(text, encoding="utf-8")
        (self.book / "framing-review.md").write_text(review(text), encoding="utf-8")
        return text
    def assert_invalid(self, text, message):
        (self.book / "framing.md").write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(FC.ContractError, message):
            FC.require_framing_contract(self.book)
    def test_contrasting_subjects_pass_one_generic_contract(self):
        """Infra: RF-05 contrasting-subject genericity control."""
        cases = (
            ("Compulsive smartphone checking", (
                "Checking now helps me stay in control.", "A quick look will only take a moment.",
                "The phone settles my unease.", "I might miss something important.",
            )),
            ("Fear of flying", (
                "My fear is the warning that keeps me safe.", "Turbulence means the aircraft is in danger.",
                "If I relax, I will lose control.", "Avoiding flights protects me from panic.",
            )),
        )
        for title, beliefs in cases:
            with self.subTest(title=title):
                text = self.write_subject(title, beliefs)
                self.assertEqual(self.book / "framing.md", FC.require_framing_contract(self.book))
                self.assertEqual(self.book / "00-brief.md", SC.require_subject_contract(self.book, "planning"))
                self.assertNotIn("sugar", text.casefold())
    def test_graph_and_journey_cover_every_brief_belief_once(self):
        """Infra: RF-05 belief-graph coverage and allocation contract."""
        beliefs = ("Primary.", "Second.", "Third.", "Fourth.")
        text = self.write_subject("Compulsive smartphone checking", beliefs)
        self.assert_invalid(text.replace('"Fourth."', '"Third."', 1), "belief graph must cover")
        changed = (text.replace("BG-01, BG-03, BG-04 remain", "BG-01, BG-03 remain")
                   .replace("BG-01, BG-04 remain", "BG-01 remains")
                   .replace("BG-04, BG-01", "BG-01"))
        self.assert_invalid(changed, "journey does not resolve")
    def test_every_transition_field_is_required(self):
        """OpenSpec scenario: Framing contains an unresolved reader transition."""
        text = self.write_subject("Fear of flying", ("Primary.", "Second.", "Third.", "Fourth."))
        for field in FC.JOURNEY_FIELDS:
            changed = re.sub(rf"^- \*\*{re.escape(field)}:\*\*.*\n", "", text, count=1, flags=re.M)
            with self.subTest(field=field):
                self.assert_invalid(changed, f"missing field {re.escape(field)}")
    def test_adjacency_is_causal_and_not_duplicate(self):
        """OpenSpec scenario: Framing contains an unresolved reader transition."""
        text = self.write_subject("Compulsive smartphone checking", ("Primary.", "Second.", "Third.", "Fourth."))
        self.assert_invalid(text.replace("Entering belief:** RS-01 | The cue can be examined instead of obeyed.", "Entering belief:** pending", 1), "unresolved value")
        self.assert_invalid(text.replace(
            "Entering belief:** RS-01 | The cue can be examined instead of obeyed.",
            "Entering belief:** RS-09 | An unrelated state.", 1,
        ), "does not follow the prior handoff")
        self.assert_invalid(text.replace(
            "Isolate what changed and what the ritual merely claimed credit for.",
            "Compare the promised settling with the unease already present.", 1,
        ), "duplicate discovery mechanism")
    def test_retained_framing_choices_and_role_metadata_are_blocking(self):
        """Infra: RF-05 retained framing choices and role metadata."""
        text = self.write_subject("Fear of flying", ("Primary.", "Second.", "Third.", "Fourth."))
        mutations = (
            re.sub(r"^- \*\*Format:\*\*.*\n", "", text, count=1, flags=re.M),
            re.sub(r"^10\. \*\*Moment of revelation:.*\n", "", text, count=1, flags=re.M),
            re.sub(r"^- \*\*Terminal mantra:\*\*.*\n", "", text, count=1, flags=re.M),
            re.sub(r"^- \*\*Fork 5:\*\*.*\n", "", text, count=1, flags=re.M),
            re.sub(r"### P-03.*?(?=## Style-guide)", "", text, count=1, flags=re.S),
            text.replace("distinct downstream writer model", "high-reasoning native planner (Sol or equivalent)", 1),
        )
        for index, changed in enumerate(mutations):
            with self.subTest(index=index):
                self.assert_invalid(changed, ".+")
    def test_planning_fails_closed_until_framing_resolves(self):
        """OpenSpec scenario: Framing contains an unresolved reader transition."""
        text = self.write_subject("Fear of flying", ("Primary.", "Second.", "Third.", "Fourth."))
        (self.book / "framing.md").unlink()
        self.assertEqual(self.book / "00-brief.md", SC.require_subject_contract(self.book, "framing"))
        with self.assertRaisesRegex(SC.ContractError, "framing not ready"):
            SC.require_subject_contract(self.book, "planning")
        (self.book / "framing.md").write_text(text.replace(
            "Entering belief:** RS-01 | The cue can be examined instead of obeyed.",
            "Entering belief:** RS-09 | An unrelated state.", 1,
        ), encoding="utf-8")
        sentinel = self.tmp / "planning-ran"
        result = subprocess.run([
            sys.executable, str(ROOT / "scripts/validate_subject_contract.py"),
            "--book", str(self.book), "--stage", "planning",
        ], check=False, capture_output=True, text=True)
        if result.returncode == 0:
            sentinel.touch()
        self.assertNotEqual(0, result.returncode)
        self.assertFalse(sentinel.exists())
if __name__ == "__main__":
    unittest.main()
