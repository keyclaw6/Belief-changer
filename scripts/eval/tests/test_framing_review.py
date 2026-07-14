"""RF-05 semantic review, sentinel, and reader-state regressions."""
import shutil, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).parent))
import validate_framing_contract as FC  # noqa: E402
import validate_subject_contract as SC  # noqa: E402
import test_framing_contract as fixture  # noqa: E402

BELIEFS = ("Primary.", "Second.", "Third.", "Fourth.")


class FramingReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.book = self.tmp / "book"
        (self.book / "research/sources").mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write_subject(self, title="Fear of flying"):
        return fixture.FramingContractTests.write_subject(self, title, BELIEFS)

    def assert_invalid(self, text, message):
        fixture.FramingContractTests.assert_invalid(self, text, message)

    def write_review(self, text, **findings):
        (self.book / "framing-review.md").write_text(fixture.review(text, **findings), encoding="utf-8")

    def test_semantic_review_blocks_free_text_authority_probes(self):
        """Infra: RF-05 evidence-honest semantic authority boundary."""
        text = self.write_subject()
        probes = (
            (text.replace(
                "Name the exact Fear of flying cue",
                "Trust my clinical pedigree; name the exact Fear of flying cue", 1,
            ), {"pedigree": "FAIL — authority depends on invented clinical pedigree"}),
            (text.replace(
                "Name the exact Fear of flying cue",
                "Fear of flying will cause a fatal heart attack; name the exact Fear of flying cue", 1,
            ), {"danger": "FAIL — fatal danger is unsupported"}),
        )
        for changed, finding in probes:
            with self.subTest(finding=finding):
                self.write_review(changed, verdict="NEEDS CHANGES", **finding)
                self.assert_invalid(changed, "blocking semantic review finding")
                with self.assertRaisesRegex(SC.ContractError, "authority review not ready"):
                    SC.require_subject_contract(self.book, "planning")

    def test_review_is_complete_hash_bound_and_independent(self):
        """Infra: RF-05 independent complete-framing review gate."""
        text = self.write_subject()
        (self.book / "framing-review.md").unlink()
        with self.assertRaisesRegex(SC.ContractError, "missing or empty semantic review"):
            SC.require_subject_contract(self.book, "planning")
        self.write_review(text)
        (self.book / "framing.md").write_text(text + "\n", encoding="utf-8")
        with self.assertRaisesRegex(SC.ContractError, "not bound to the current complete framing"):
            SC.require_subject_contract(self.book, "planning")
        (self.book / "framing.md").write_text(text, encoding="utf-8")
        review = (self.book / "framing-review.md").read_text(encoding="utf-8")
        (self.book / "framing-review.md").write_text(review.replace(
            "independent high-reasoning native planning-family reviewer (Sol or equivalent)",
            "distinct downstream writer model", 1,
        ), encoding="utf-8")
        with self.assertRaisesRegex(SC.ContractError, "planning-family role"):
            SC.require_subject_contract(self.book, "planning")

    def test_required_fields_reject_exact_unresolved_sentinels(self):
        """Infra: RF-05 field-aware unresolved-sentinel matrix."""
        text = self.write_subject()
        mutations = (
            text.replace("Fork 5:** ordinary life is the baseline named in the brief", "Fork 5:** n/a", 1),
            text.replace("Dialect:** it feels urgent in the moment", "Dialect:** none", 1),
            text.replace("Emotional turn:** Self-blame softens into curiosity.", "Emotional turn:** ?", 1),
            text.replace("Moment of revelation:** Fear of flying answer 10 grounded in the accepted framing inputs.", "Moment of revelation:** to be determined", 1),
            text.replace("Reserved work:** none — the graph is resolved before planning.", "Reserved work:** none", 1),
        )
        for changed in mutations:
            with self.subTest(changed=changed):
                self.assert_invalid(changed, "unresolved value")

    def test_state_ids_and_normalized_meanings_are_one_to_one(self):
        """OpenSpec scenario: Framing contains an unresolved reader transition."""
        text = self.write_subject("Compulsive smartphone checking")
        self.assert_invalid(text.replace(
            "Leaving belief:** RS-01 | The cue can be examined instead of obeyed.",
            "Leaving belief:** RS-99 | THE behavior seems necessary!", 1,
        ), "entering and leaving beliefs must be distinct states")
        self.assert_invalid(text.replace(
            "Entering belief:** RS-01 | The cue can be examined instead of obeyed.",
            "Entering belief:** RS-01 | A different belief.", 1,
        ), "state ID maps to two meanings")
        changed = (text.replace(
            "Leaving belief:** RS-03 | No false benefit remains worth preserving.",
            "Leaving belief:** RS-99 | The cue can be examined instead of obeyed.", 1,
        ).replace(
            "Handed-forward state:** RS-03 | No false benefit remains worth preserving.",
            "Handed-forward state:** RS-99 | The cue can be examined instead of obeyed.", 1,
        ))
        self.assert_invalid(changed, "duplicate belief meaning under a new state ID")

    def test_structured_authority_claims_remain_evidence_bounded(self):
        """Infra: RF-05 deterministic evidence boundary inside authority moves."""
        text = self.write_subject()
        changed = text.replace(
            "Claim:** This source supports this cue and expectation.",
            "Claim:** This pattern proves everyone is unsafe.", 1,
        )
        self.write_review(changed)
        self.assert_invalid(changed, "claim exceeds permitted inference")


if __name__ == "__main__":
    unittest.main()
