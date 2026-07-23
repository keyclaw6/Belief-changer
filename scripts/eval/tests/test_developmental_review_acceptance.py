"""RF-13 exact scope -> trap -> inventory acceptance regression."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
sys.path.insert(0, str(ROOT / "scripts/eval/tests"))
import developmental_review as DEV  # noqa: E402
import developmental_review_contract as CONTRACT  # noqa: E402
from developmental_deferred_fixture import (  # noqa: E402
    DeferredSequenceFixture, DRAFTS, REQUIRED, SPANS, STATES, TOKENS,
    finding, validate_task)
from developmental_review_fixture import proven_runner, verdict  # noqa: E402


class DevelopmentalReviewAcceptanceTests(DeferredSequenceFixture, unittest.TestCase):
    def assert_locally_complete(self, task):
        chapters = task["context"]["chapters"]
        self.assertEqual(3, len({item["commission"] for item in chapters}))
        seen = set()
        markers = {
            1: ("survey chapter has mapped scope", "local transition is complete",
                "handed the recurring pattern to the next chapter"),
            2: ("checking trap", "transition is locally complete",
                "scope map and trap name to Lena"),
            3: ("five cards", "each completed their local job",
                "Read alone, each chapter reaches its authority"),
        }
        for chapter in chapters:
            number, draft = chapter["number"], chapter["frozen_draft"]
            paragraphs = [item.strip() for item in draft.split("\n\n") if item.strip()][1:]
            with self.subTest(chapter=number):
                self.assertGreaterEqual(len(draft.split()), 800)
                self.assertGreaterEqual(len(paragraphs), 10)
                self.assertEqual(len(paragraphs), len(set(paragraphs)))
                self.assertFalse(seen & set(paragraphs))
                seen.update(paragraphs)
                self.assertEqual(STATES[number][0], chapter["entering_state"])
                self.assertEqual(STATES[number][1], chapter["leaving_state"])
                self.assertIn(chapter["entering_state"], chapter["commission"])
                self.assertIn(chapter["leaving_state"], chapter["commission"])
                self.assertIn(REQUIRED[number]["situation"], chapter["commission"])
                self.assertIn(REQUIRED[number]["handoff"], chapter["commission"])
                self.assertEqual(1, chapter["commission"].count(TOKENS[number]))
                self.assertEqual(1, draft.count(TOKENS[number]))
                for other in set(TOKENS.values()) - {TOKENS[number]}:
                    self.assertNotIn(other, draft)
                for marker in markers[number]:
                    self.assertIn(marker, draft)
        self.assertEqual(STATES[1][1], STATES[2][0])
        self.assertEqual(STATES[2][1], STATES[3][0])

    def test_scope_trap_inventory_fails_only_as_a_cumulative_plan_sequence(self):
        """OpenSpec requirement: Split chapter review."""
        candidate, captured = self.ready("scope-trap-inventory"), {}
        task = DEV.prepare(candidate)
        self.assertEqual(task, validate_task(task))
        self.assert_locally_complete(task)
        failure = finding(task)
        for number, evidence in enumerate(failure["evidence"], 1):
            self.assertEqual({"chapter_id": f"C-{number:02d}",
                              "span": SPANS[number]}, evidence)
            self.assertEqual(1, task["context"]["chapters"][number - 1]
                             ["frozen_draft"].count(SPANS[number]))
            for other in set(DRAFTS) - {number}:
                self.assertNotIn(SPANS[number], DRAFTS[other])
        self.assertEqual("deferred_transformation_repetition", failure["category"])
        self.assertEqual("catalogue_replaces_discovery", failure["symptom_code"])
        self.assertEqual("card_sequence_defect", failure["ownership_basis"])
        self.assertEqual("plan", failure["owner"])
        self.assertEqual("repair_sequence_cards", failure["action_code"])
        self.assertEqual(["C-01", "C-02", "C-03"], failure["chapters"])
        CONTRACT.verdict(verdict(task, "NEEDS_CHANGES", [failure]), task)

        def response(exact):
            validate_task(exact)
            return verdict(exact, "NEEDS_CHANGES", [failure])

        with self.assertRaisesRegex(DEV.DevelopmentalReviewError, "NEEDS_CHANGES"):
            DEV.advance(candidate, runner=proven_runner(response, captured=captured))
        body = captured["kwargs"]["input"]
        self.assertEqual(task, captured["task"])
        self.assertEqual(task, json.loads(body))
        self.assertEqual(3, body.count("frozen_draft"))
        self.assertNotIn(str(candidate), body)
        self.assertEqual(Path(tempfile.gettempdir()).resolve(),
                         Path(captured["kwargs"]["cwd"]).resolve().parents[1])
        decoded = json.dumps(task, ensure_ascii=False)
        for allowed in ("RS-11", "RS-14", "scope", "checking trap",
                        "claimed benefits", "AUTHORITATIVE SEMANTIC COMMISSION — C-03"):
            self.assertIn(allowed, decoded)
        for forbidden in ("FORBIDDEN-FULL-PLAN", "FORBIDDEN-FULL-STYLE",
                          "FORBIDDEN-RAW-ASSIGNED", "FORBIDDEN-REFERENCE-TEXT",
                          "FORBIDDEN-JUDGE-FEEDBACK", "FORBIDDEN-UNASSIGNED",
                          "FORBIDDEN-EXTRA-CHAPTER"):
            self.assertNotIn(forbidden, decoded)
        for feature in ("shell_tool", "unified_exec", "browser_use", "plugins"):
            self.assertIn(feature, captured["command"])


if __name__ == "__main__":
    unittest.main()
