"""Frozen factory boundaries, independent of retired intermediate Pi wrappers.

The offline fixtures check task context and contracts, never reviewer competence.
"""
import argparse
import ast
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from bc_factory.common import file_hash, seal, unseal
from bc_factory.demo import finish, inputs, scaffold
from bc_factory.runs import PROMPTS, Run, active_files, prepare
from bc_factory.schema import EXTERNAL_ROLES, ROLES


def commands(parser):
    return next(action.choices for action in parser._actions
                if isinstance(action, argparse._SubParsersAction))


class FactoryBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.repo = Path(cls.tmp.name) / "factory"
        scaffold(ROOT, cls.repo)
        brief, research, plan = inputs()
        cls.context = {"research_priorities": ["Preserve uncertainty"],
                       "editorial_constraints": ["Keep the reader's choice explicit"]}
        prepare(cls.repo, "boundary-fixture", brief, research, fixture=True,
                caller_context=cls.context)
        cls.book = Run(cls.repo, "boundary-fixture")
        finish(cls.book, plan)
        cls.tasks = [unseal(path) for path in (cls.book.root / "tasks").glob("*.json")]

    def text(self, rel):
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_every_role_uses_its_frozen_contract_and_generic_context(self):
        self.assertEqual(set(PROMPTS), set(ROLES))
        self.assertEqual({task["role"] for task in self.tasks}, set(ROLES))
        for task in self.tasks:
            with self.subTest(role=task["role"], chapter=task["chapter"]):
                contract = self.book.root / "snapshot/prompts" / PROMPTS[task["role"]]
                self.assertTrue(contract.read_text(encoding="utf-8").strip())
                self.assertEqual(task["contract"], contract.read_text(encoding="utf-8"))
                self.assertEqual(task["inputs"]["caller_context"], self.context)

    def test_chapter_roles_receive_actual_preceding_manuscript(self):
        first = self.book.result("writer", 1)["output"]
        state = self.book.result("state-editor", 1)["output"]
        for task in self.tasks:
            if task["chapter"] != 2:
                continue
            with self.subTest(role=task["role"]):
                previous = task["inputs"]["delivered_previous_chapters"]
                self.assertEqual(len(previous), 1)
                self.assertEqual(previous[0]["text"], first["text"])
                self.assertEqual(previous[0]["state"], state)

    def test_final_review_receives_the_exact_assembled_book(self):
        task = next(t for t in self.tasks if t["role"] == "final-auditor")
        self.assertEqual(task["inputs"]["assembled_book"],
                         (self.book.root / "book.md").read_text(encoding="utf-8"))
        self.assertEqual(EXTERNAL_ROLES, {"evidence-reviewer", "final-auditor"})

    def test_sealed_caller_repair_is_generic_and_bound_to_accepted_artifacts(self):
        feedback = {"caller_constraint": "Preserve the bounded conclusion"}
        assembly = self.book.assembly_version(1)["assembly"]
        seal(self.book.root / "caller-feedback/repair-r01.json", {
            "schema_version": 2, "assembly_round": 1,
            "book_sha256": assembly["text_sha256"],
            "audit_sha256": file_hash(self.book.accepted_audit_file()),
            "feedback": feedback,
        })
        task = self.book.task("book-editor", round_no=2)
        self.assertEqual(task["inputs"]["caller_repair_feedback"], feedback)
        self.assertEqual(task["inputs"]["previous_assembly"]["text"], assembly["text"])
        self.assertIn("caller-feedback/repair-r01.json", task["dependency_hashes"])

    def test_factory_cli_excludes_outer_decisions(self):
        from bc_factory.cli import parser as factory_parser
        from bc_autoresearch.cli import parser as outer_parser
        factory, outer = commands(factory_parser()), commands(outer_parser())
        outer_commands = {"register-experiment", "pair-task", "pair-submit", "pair-execute",
                          "decide", "promote", "learning-seed", "regression-task",
                          "regression-submit", "regression-decide", "advance-baseline"}
        self.assertFalse(outer_commands & set(factory))
        self.assertTrue(outer_commands <= set(outer))
        prepared = factory["prepare"].parse_args([
            "--run", "r1", "--brief", "brief.json", "--research", "research.json",
            "--caller-context", "guidance.json"])
        self.assertEqual(prepared.caller_context, "guidance.json")

    def test_frozen_factory_is_extractable_without_outer_runtime(self):
        frozen = set(active_files(ROOT))
        required = {"AGENTS.md", "factory/config.json", "docs/FACTORY-V2.md",
                    "docs/RESEARCH-ACCESS.md", "prompts/research-agent.md",
                    "prompts/factory-orchestrator.md", ".pi/agents/factory-orchestrator.md",
                    ".pi/settings.json", ".pi/pi-goal-x-settings.json"}
        required.update("prompts/" + prompt for prompt in PROMPTS.values())
        self.assertTrue(required <= frozen)
        self.assertFalse(any(path.startswith(("loop/", "scripts/bc_autoresearch/", ".opencode/"))
                             for path in frozen))
        for rel in frozen:
            if not rel.endswith(".py"):
                continue
            for node in ast.walk(ast.parse(self.text(rel), filename=rel)):
                imports = ([node.module or ""] if isinstance(node, ast.ImportFrom)
                           else [alias.name for alias in node.names] if isinstance(node, ast.Import)
                           else [])
                self.assertFalse(any(name.startswith("bc_autoresearch") for name in imports), rel)

    def test_pi_factory_does_not_load_outer_instructions(self):
        role = self.text(".pi/agents/factory-orchestrator.md")
        prompt = self.text("prompts/factory-orchestrator.md")
        self.assertIn("prompts/factory-orchestrator.md", role)
        self.assertIn("prompts/research-agent.md", prompt)
        self.assertIn("COMPLETE_UNRELEASED", prompt)
        for text in (role, prompt):
            self.assertNotIn("loop/PROGRAM.md", text)
            self.assertNotIn("loop/prompts/", text)
        outer_names = {"hypothesizer", "judge", "factory-learner", "factory-learning-reviewer"}
        self.assertFalse(outer_names & {p.stem for p in (ROOT / ".pi/agents").glob("*.md")})

    def test_role_guidance_cannot_replace_subject_evidence(self):
        for prompt in {"research-agent.md", *PROMPTS.values()}:
            with self.subTest(prompt=prompt):
                text = self.text("prompts/" + prompt).lower()
                self.assertIn("caller_context", text)
                self.assertRegex(text, r"(?:not|never|rather than)[^.!\n]*evidence")

    def test_learning_protocol_preserves_negatives_and_holdout_integrity(self):
        def protocol(path):
            text = self.text(path)
            return json.loads(text[text.index("{"):text.rindex("}") + 1])
        learner = protocol("loop/prompts/factory-learner.md")
        reviewer = protocol("loop/prompts/factory-learning-reviewer.md")
        self.assertEqual(set(learner["decision"].split(" | ")),
                         {"CHANGE_FACTORY", "KEEP_FACTORY", "MEASURE_MORE"})
        self.assertEqual(set(reviewer["verdict"].split(" | ")),
                         {"ACCEPT", "REVISE", "REJECT", "MEASURE_MORE"})
        self.assertTrue({"subject_specific_lessons", "protected_strengths", "candidate_root_causes"}
                        <= learner.keys())
        self.assertTrue({"change_surface", "smallest_change", "expected_transfer", "possible_regressions"}
                        <= learner["proposed_factory_change"].keys())
        self.assertTrue({"holdout_requirements", "success_criteria", "failure_signals", "leakage_rule"}
                        <= learner["falsification_test"].keys())
        self.assertTrue({"held_out_integrity", "judge_overfit_control", "causal_honesty",
                         "minimal_change", "not_subject_overfit", "protected_strengths"}
                        <= reviewer["checks"].keys())
        self.assertTrue({"holdout_requirements", "success_criteria", "failure_signals"}
                        <= reviewer["held_out_test"].keys())


if __name__ == "__main__":
    unittest.main()
