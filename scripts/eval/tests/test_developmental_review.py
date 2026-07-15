"""RF-13 whole-sequence contract, scope, routing, and gate regressions."""
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
sys.path.insert(0, str(ROOT / "scripts/eval/tests"))
import candidate_pair as PAIR  # noqa: E402
import developmental_review as DEV  # noqa: E402
import developmental_review_contract as CONTRACT  # noqa: E402
import judges  # noqa: E402
import manual_dispatch as MANUAL  # noqa: E402
import pair_store as STORE  # noqa: E402
from developmental_review_fixture import (  # noqa: E402
    DevelopmentalFixture, finding, pass_developmental, proven_runner, verdict)
from developmental_commission_fixture import REQUIRED, STATES, TOKENS  # noqa: E402


class DevelopmentalReviewTests(DevelopmentalFixture, unittest.TestCase):
    def assert_cumulative_authority(self, task):
        chapters = task["context"]["chapters"]
        commissions = [item["commission"] for item in chapters]
        self.assertEqual(3, len(set(commissions)))
        for number, chapter in enumerate(chapters, 1):
            with self.subTest(chapter=number):
                self.assertEqual(STATES[number][0], chapter["entering_state"])
                self.assertEqual(STATES[number][1], chapter["leaving_state"])
                self.assertIn(chapter["entering_state"], chapter["commission"])
                self.assertIn(chapter["leaving_state"], chapter["commission"])
                self.assertIn(f"S-{100 + number}#E-001", chapter["commission"])
                self.assertIn(REQUIRED[number]["situation"], chapter["commission"])
                self.assertIn(REQUIRED[number]["handoff"], chapter["commission"])
                self.assertEqual(1, chapter["commission"].count(TOKENS[number]))
                self.assertEqual(1, chapter["frozen_draft"].count(TOKENS[number]))
                for other in set(TOKENS.values()) - {TOKENS[number]}:
                    self.assertNotIn(other, chapter["frozen_draft"])
        self.assertEqual(STATES[1][1], STATES[2][0])
        self.assertEqual(STATES[2][1], STATES[3][0])
        self.assertIn("No prior correction", commissions[0])
        for commission in commissions[1:]:
            self.assertNotIn("No prior correction", commission)
            self.assertNotIn(REQUIRED[1]["entering belief"], commission)
            self.assertNotIn(REQUIRED[1]["handoff"], commission)

    def assert_locally_adequate_sequence(self, task, expected):
        seen = set()
        for chapter, markers in zip(task["context"]["chapters"], expected):
            draft = chapter["frozen_draft"]
            paragraphs = [item.strip() for item in draft.split("\n\n") if item.strip()][1:]
            self.assertGreaterEqual(len(draft.split()), 800)
            self.assertGreaterEqual(len(paragraphs), 10)
            self.assertEqual(len(paragraphs), len(set(paragraphs)))
            self.assertFalse(seen & set(paragraphs))
            seen.update(paragraphs)
            for marker in markers:
                self.assertIn(marker, draft)

    def test_one_exact_whole_sequence_task_excludes_every_forbidden_input(self):
        """OpenSpec requirement: Split chapter review."""
        candidate, captured = self.ready("clean-exact-input"), {}
        task = DEV.prepare(candidate)
        self.assert_cumulative_authority(task)
        body = json.dumps(task, ensure_ascii=False)
        self.assertEqual([1, 2, 3], [item["number"] for item in
                                  task["context"]["chapters"]])
        self.assert_locally_adequate_sequence(task, (
            ("hand on the cupboard", "urge no longer proves", "portable test"),
            ("archive clock", "interest replace apprehension", "promised cure"),
            ("loyalty card", "hopeful bargaining to quiet ownership",
             "cumulative leaving state")))
        for allowed in ("At 7:10 Mara", "During the next afternoon pause",
                        "In the grocery queue", "RS-01", "RS-04",
                        "AUTHORITATIVE SEMANTIC COMMISSION — C-03"):
            self.assertIn(allowed, body)
        for forbidden in ("FORBIDDEN-FULL-PLAN", "FORBIDDEN-FULL-STYLE",
                          "FORBIDDEN-RAW-ASSIGNED", "FORBIDDEN-REFERENCE-TEXT",
                          "FORBIDDEN-JUDGE-FEEDBACK", "FORBIDDEN-UNASSIGNED",
                          "FORBIDDEN-EXTRA-CHAPTER"):
            self.assertNotIn(forbidden, body)
        self.assertEqual(body.count("frozen_draft"), 3)
        receipt = DEV.advance(candidate, runner=proven_runner(captured=captured))
        self.assertEqual("PASS", receipt["state"])
        self.assertEqual(task["task_sha256"], receipt["task_sha256"])
        self.assertEqual([1, 2, 3], receipt["selection"])
        self.assertEqual(task, captured["task"])
        self.assertEqual(json.loads(captured["kwargs"]["input"]), task)
        self.assertNotIn(str(candidate), captured["kwargs"]["input"])
        self.assertTrue(str(captured["kwargs"]["cwd"]).startswith("/tmp/"))
        for feature in ("shell_tool", "unified_exec", "browser_use", "plugins"):
            self.assertIn(feature, captured["command"])

    def test_locally_complete_repetitive_opening_is_a_writing_failure(self):
        """OpenSpec requirement: Split chapter review."""
        candidate, captured = self.ready("repetitive-opening"), {}
        task = DEV.prepare(candidate)
        self.assert_cumulative_authority(task)
        self.assert_locally_adequate_sequence(task, (
            ("five boxes", "an urge can be examined before it is followed",
             "question test as settled prior work"),
            ("copies Mara's five boxes", "Mara's correction",
             "anticipated checking can create the tension it claims to relieve"),
            ("repeats the same five boxes", "Mara taught her", "Ivo showed her",
             "old bargain is unnecessary rather than forbidden")))
        failure = finding(task, symptom="scene_argument_pattern_repeats")
        with self.assertRaisesRegex(DEV.DevelopmentalReviewError, "NEEDS_CHANGES"):
            DEV.advance(candidate, runner=proven_runner(
                lambda exact: verdict(exact, "NEEDS_CHANGES", [failure]),
                captured=captured))
        self.assertEqual(task, captured["task"])
        self.assertEqual("mode_scene_argument_variation", failure["category"])
        self.assertEqual("draft_execution_defect", failure["ownership_basis"])
        self.assertEqual("writing", failure["owner"])
        self.assertEqual(["C-01", "C-02", "C-03"], failure["chapters"])
        self.assertEqual(failure["chapters"],
                         [item["chapter_id"] for item in failure["evidence"]])

    def test_clean_sequence_passes_and_source_reaudit_is_not_an_output_path(self):
        """OpenSpec requirement: Split chapter review."""
        candidate = self.ready("clean")
        task = DEV.prepare(candidate)
        self.assertEqual("PASS", CONTRACT.verdict(verdict(task), task)["verdict"])
        self.assertEqual("PASS", pass_developmental(candidate)["state"])
        grounded = finding(task, "newly_detected_grounded_need",
                           "new_truth_safety_need", chapters=["C-01"])
        self.assertEqual("grounded-review", grounded["owner"])
        self.assertNotIn("source", json.dumps(grounded).casefold())
        invented = deepcopy(grounded)
        invented["source_locators"] = ["S-101#E-001"]
        with self.assertRaises(CONTRACT.ContractError):
            CONTRACT.verdict(verdict(task, "NEEDS_CHANGES", [invented]), task)

    def test_closed_owner_basis_prevents_inappropriate_writer_routing(self):
        """OpenSpec requirement: Owner-routed repair."""
        task = DEV.prepare(self.ready("owners"))
        for basis, owner in (("journey_definition_conflict", "framing"),
                             ("card_sequence_defect", "planning"),
                             ("commission_transport_defect", "commissioning"),
                             ("draft_execution_defect", "writing")):
            row = finding(task, basis=basis)
            self.assertEqual(owner, row["owner"])
            CONTRACT.verdict(verdict(task, "NEEDS_CHANGES", [row]), task)
            wrong = deepcopy(row)
            wrong.update(owner="writing", action_code="repair_sequence_execution")
            if basis != "draft_execution_defect":
                with self.assertRaises(CONTRACT.ContractError):
                    CONTRACT.verdict(verdict(task, "NEEDS_CHANGES", [wrong]), task)

    def test_finding_evidence_is_exact_complete_unique_and_meaningful(self):
        """OpenSpec requirement: Split chapter review."""
        task = DEV.prepare(self.ready("evidence-contract"))
        valid = finding(task)
        CONTRACT.verdict(verdict(task, "NEEDS_CHANGES", [valid]), task)
        cases = {}
        missing = deepcopy(valid); missing["evidence"] = missing["evidence"][:-1]
        cases["missing chapter evidence"] = [missing]
        duplicate = deepcopy(valid); duplicate["evidence"][1] = duplicate["evidence"][0]
        cases["duplicate chapter evidence"] = [duplicate]
        outside = deepcopy(valid); outside["chapters"] = ["C-01"]
        outside["expected_transitions"] = outside["expected_transitions"][:1]
        cases["unlisted chapter evidence"] = [outside]
        for label, span in (("blank", " "), ("punctuation", "."), ("one char", "a")):
            bad = deepcopy(valid); bad["evidence"][0]["span"] = span
            cases[label] = [bad]
        duplicate_chapter = deepcopy(valid); duplicate_chapter["chapters"].append("C-03")
        cases["duplicate chapters"] = [duplicate_chapter]
        duplicate_transition = deepcopy(valid)
        duplicate_transition["expected_transitions"][1] = deepcopy(
            duplicate_transition["expected_transitions"][0])
        cases["duplicate transitions"] = [duplicate_transition]
        semantic_copy = deepcopy(valid)
        alternate = "The scene stays with the immediate choice"
        for item in semantic_copy["evidence"]:
            item["span"] = alternate
        cases["semantic duplicate"] = [valid, semantic_copy]
        for label, findings in cases.items():
            with self.subTest(label=label), self.assertRaises(CONTRACT.ContractError):
                CONTRACT.verdict(verdict(task, "NEEDS_CHANGES", findings), task)

    def test_needs_changes_stops_every_existing_next_boundary_without_outputs(self):
        """OpenSpec scenario: A grounded blocker remains."""
        candidate = self.ready("blocked")
        def response(task):
            return verdict(task, "NEEDS_CHANGES", [finding(task)])
        with self.assertRaisesRegex(DEV.DevelopmentalReviewError, "NEEDS_CHANGES"):
            DEV.advance(candidate, runner=proven_runner(response))
        with self.assertRaises(DEV.DevelopmentalReviewError):
            MANUAL.reviewer(candidate)
        with self.assertRaisesRegex(PAIR.PairError, "NEEDS_CHANGES"):
            PAIR.seal(candidate)
        cfg = {"tasks_dir": str(candidate / "judge-tasks"), "judge_k": 1}
        with self.assertRaisesRegex(SystemExit, "developmental PASS"):
            judges.emit_tasks(cfg, [], "001", "", candidate)
        self.assertFalse((candidate / "judge-tasks").exists())

    def test_model_family_and_complete_task_identity_fail_closed(self):
        """Infrastructure: distinct native high-reasoning reviewer provenance."""
        valid = {"writer_model": "anthropic/writer", "writer_family": "anthropic",
                 "grounded_reviewer_model": "openai/sol", "grounded_reviewer_family": "sol",
                 "developmental_reviewer_model": "openai/luna",
                 "developmental_reviewer_family": "luna",
                 "developmental_reviewer_route": "codex-native",
                 "developmental_reviewer_reasoning": "max"}
        self.assertEqual("luna", CONTRACT.model(valid)["family"])
        for key, value in (("developmental_reviewer_route", "openrouter"),
                           ("developmental_reviewer_reasoning", "none"),
                           ("developmental_reviewer_family", "sol"),
                           ("developmental_reviewer_model", "anthropic/writer")):
            with self.subTest(key=key), self.assertRaises(CONTRACT.ContractError):
                CONTRACT.model({**valid, key: value})
        task = DEV.prepare(self.ready("task-hash"))
        for path, replacement in ((["operation", "id"], "changed"),
                                  (["selection"], [1]),
                                  (["context", "chapters", 0, "frozen_draft"], "changed")):
            bad, target = deepcopy(task), None
            target = bad
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = replacement
            with self.subTest(path=path), self.assertRaises(CONTRACT.ContractError):
                CONTRACT.task(bad)


if __name__ == "__main__":
    unittest.main()
