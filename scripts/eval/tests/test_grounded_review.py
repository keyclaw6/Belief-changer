"""RF-12 assigned-evidence, verdict, and downstream-gate regressions."""
import json
import os
import re
import stat
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
sys.path.insert(0, str(ROOT / "scripts/eval/tests"))
import candidate_pair as PAIR  # noqa: E402
import grounded_evidence as EVIDENCE  # noqa: E402
import grounded_review as GR  # noqa: E402
import grounded_review_contract as CONTRACT  # noqa: E402
import judges  # noqa: E402
import manual_dispatch as MANUAL  # noqa: E402
from grounded_review_fixture import (  # noqa: E402
    GroundedFixture, finding, pass_review, proven_runner, verdict)


class GroundedReviewTests(GroundedFixture, unittest.TestCase):
    def test_exact_assigned_record_is_the_only_packet_content_dispatched(self):
        """OpenSpec requirement: Split chapter review."""
        candidate = self.frozen("exact-pass")
        tasks = GR.prepare(candidate)
        first = json.dumps(tasks[1])
        self.assertIn("FROZEN-ONE", first)
        self.assertIn("I need to check this now, example 1.", first)
        for forbidden in ("I need to check this now, example 2.",
                          "I need to check this now, example 10.",
                          "FORBIDDEN-FULL-PLAN",
                          "FORBIDDEN-FULL-STYLE", "FORBIDDEN-REFERENCE-TEXT",
                          "FORBIDDEN-JUDGE-FEEDBACK",
                          "FORBIDDEN-EXTRA-CHAPTER"):
            self.assertNotIn(forbidden, first)
        self.assertNotIn("I need to check this now, example 2.",
                         GR.GC.input_text(tasks[1]))
        receipt = pass_review(candidate)
        self.assertEqual("PASSED", receipt["state"])
        self.assertIn("native_grounded_review.py", MANUAL.grounded(candidate, [1]))
        tested = PAIR.seal(candidate)
        self.assertEqual(tested, PAIR.verify_sealed(candidate, tested)["tested_hash"])
        self.assertTrue(all(stat.S_IMODE(os.lstat(path).st_mode) == 0o444
                            for path in GR.PS.tree_files(GR.folder(candidate))))

    def test_each_blocker_class_persists_and_stops_downstream_work(self):
        """OpenSpec scenario: A grounded blocker remains."""
        for classification in sorted(CONTRACT.CLASS_RULES):
            with self.subTest(classification=classification):
                candidate = self.frozen("block-" + classification.split()[0].replace("/", "-"))

                def response(task):
                    return (verdict(task, "BLOCK", [finding(task, classification)])
                            if task["chapter"] == 1 else verdict(task))

                with self.assertRaisesRegex(GR.GroundedReviewError, "BLOCK"):
                    GR.advance(candidate, runner=proven_runner(response))
                receipt = json.loads(GR.receipt_path(candidate).read_text(
                    encoding="utf-8"))
                self.assertEqual("BLOCKED", receipt["state"])
                self.assertEqual(classification,
                                 receipt["chapters"][0]["verdict"]["findings"][0]
                                 ["classification"])
                with self.assertRaisesRegex(PAIR.PairError, "BLOCK"):
                    PAIR.seal(candidate)
                with self.assertRaisesRegex(SystemExit, "grounded PASS"):
                    judges.emit_tasks({"tasks_dir": str(candidate / "judge-tasks"),
                                       "judge_k": 1}, [], "001", "", candidate)

    def test_structural_owner_action_routes_and_recursive_json_are_strict(self):
        """OpenSpec requirement: Split chapter review."""
        candidate = self.frozen("strict")
        task = GR.prepare(candidate)[1]
        invalid = []
        packet = finding(task, "packet conflict")
        packet.update(owner="prose", action_code="remove_unsupported_span")
        invalid.append(verdict(task, "BLOCK", [packet]))
        originality = finding(task, "originality/near-copy")
        originality.update(owner="research/synthesis", action_code="repair_assigned_evidence")
        invalid.append(verdict(task, "BLOCK", [originality]))
        invented_action = finding(task, "ownership leakage")
        invented_action["required_action"] = "Create a testimonial"
        invalid.append(verdict(task, "BLOCK", [invented_action]))
        malformed = finding(task, "invention")
        malformed["source_locators"] = [{"locator": "S-001#E-001"}]
        invalid.append(verdict(task, "BLOCK", [malformed]))
        duplicate = (f'{{"schema":2,"task_sha256":"{task["task_sha256"]}",'
                     '"verdict":"BLOCK","findings":[{"classification":"invention",'
                     '"classification":"invention"}]}' )
        invalid.append(duplicate)
        for raw in invalid:
            with self.subTest(raw=raw):
                with self.assertRaises(CONTRACT.ContractError):
                    CONTRACT.verdict(raw, task)

    def test_assigned_locator_missing_ambiguous_or_malformed_fails_pre_dispatch(self):
        """OpenSpec requirement: Split chapter review."""
        packet_path = "production-books/test/research/sources/S-001-sealed-fixture.md"
        source = self.accepted / packet_path
        authority = self.assignments["C-01"]["authority"]["assigned_evidence"]
        source_text = source.read_text(encoding="utf-8")
        with self.assertRaisesRegex(EVIDENCE.EvidenceError, "missing or ambiguous"):
            EVIDENCE.assigned_records({packet_path: source_text},
                                      {"S-777#E-001": next(iter(authority.values()))})
        variants = {
            "ambiguous": source_text + "\n### E-001\n- **Kind:** INTERPRETATION\n",
            "malformed": re.sub(r"^- \*\*Evidence grade:\*\*.*\n", "",
                                source_text, count=1, flags=re.M),
        }
        for name, text in variants.items():
            with self.subTest(name=name), self.assertRaisesRegex(
                    EVIDENCE.EvidenceError, "ambiguous|malformed"):
                EVIDENCE.assigned_records({packet_path: text}, authority)
        unassigned_path = (
            "production-books/test/research/sources/S-002-sealed-fixture.md")
        unassigned = (self.accepted / unassigned_path).read_text(encoding="utf-8")
        with self.assertRaisesRegex(EVIDENCE.EvidenceError,
                                    "contains no exact assigned locator"):
            EVIDENCE.assigned_records(
                {packet_path: source_text, unassigned_path: unassigned}, authority)

    def test_model_route_is_distinct_native_xhigh_and_task_hash_is_complete(self):
        """Infrastructure: native high-reasoning reviewer provenance."""
        valid = {"writer_model": "anthropic/writer", "writer_family": "anthropic",
                 "grounded_reviewer_model": "openai/reviewer",
                 "grounded_reviewer_family": "openai",
                 "grounded_reviewer_route": "codex-native",
                 "grounded_reviewer_reasoning": "xhigh"}
        self.assertEqual("codex-native", CONTRACT.model(valid)["route"])
        for key, value in (("grounded_reviewer_route", "openrouter"),
                           ("grounded_reviewer_family", "anthropic"),
                           ("grounded_reviewer_reasoning", "none"),
                           ("grounded_reviewer_model", "anthropic/writer")):
            with self.subTest(key=key), self.assertRaises(CONTRACT.ContractError):
                CONTRACT.model({**valid, key: value})
        candidate = self.frozen("task-bindings")
        task = GR.prepare(candidate)[1]
        for path, replacement in ((["operation", "id"], "0" * 64),
                                  (["config", "values_sha256"], "1" * 64),
                                  (["selection"], [1]),
                                  (["context", "frozen_draft"], "changed")):
            bad = deepcopy(task)
            target = bad
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = replacement
            with self.subTest(path=path), self.assertRaises(CONTRACT.ContractError):
                CONTRACT.task(bad)


if __name__ == "__main__":
    unittest.main()
