"""Small static tests for the factory/autoresearch boundary."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from bc_factory.schema import ROLES


class FactoryBoundaryTests(unittest.TestCase):
    def text(self, rel):
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_every_live_factory_role_has_one_pi_wrapper(self):
        role_map = {
            "evidence-reviewer": ("evidence-reviewer", "prompts/evidence-reviewer.md"),
            "planner": ("plan-writer", "prompts/master-plan-skill-v2.md"),
            "plan-reviewer": ("plan-reviewer", "prompts/master-plan-reviewer-v2.md"),
            "writer": ("chapter-writer", "prompts/chapter-writer.md"),
            "chapter-reviewer": ("chapter-reviewer", "prompts/chapter-reviewer.md"),
            "state-editor": ("state-editor", "prompts/reader-state.md"),
            "book-editor": ("book-editor", "prompts/book-editor.md"),
            "final-auditor": ("final-auditor", "prompts/final-auditor.md"),
        }
        self.assertEqual(set(role_map), set(ROLES))
        for role, (wrapper, prompt) in role_map.items():
            with self.subTest(role=role):
                p = ROOT / f".pi/agents/{wrapper}.md"
                self.assertTrue(p.is_file())
                self.assertIn(prompt, p.read_text(encoding="utf-8"))

    def test_pi_contains_factory_not_autoresearch_agents(self):
        expected_factory = {
            "_README.md", "factory-orchestrator.md", "researcher.md",
            "evidence-reviewer.md", "plan-writer.md", "plan-reviewer.md",
            "chapter-writer.md", "chapter-reviewer.md", "state-editor.md",
            "book-editor.md", "final-auditor.md",
        }
        actual = {p.name for p in (ROOT / ".pi/agents").glob("*.md")}
        self.assertEqual(actual, expected_factory)
        for name in ("factory-learner", "factory-learning-reviewer", "hypothesizer",
                     "trace-analyzer", "judge"):
            self.assertFalse((ROOT / f".pi/agents/{name}.md").exists())

    def test_pi_factory_agents_do_not_read_autoresearch_contracts(self):
        for p in (ROOT / ".pi/agents").glob("*.md"):
            if p.name == "_README.md":
                continue
            text = p.read_text(encoding="utf-8")
            self.assertNotIn("AGENTS.md", text, p.name)
            self.assertNotIn("loop/PROGRAM.md", text, p.name)
        orchestrator = self.text("prompts/factory-orchestrator.md")
        self.assertIn(".pi/agents/_README.md", orchestrator)
        self.assertNotIn("AGENTS.md", orchestrator)
        self.assertNotIn("loop/PROGRAM.md", orchestrator)

    def test_factory_orchestrator_stops_at_completed_book(self):
        p = self.text("prompts/factory-orchestrator.md")
        self.assertIn("COMPLETE_UNRELEASED", p)
        self.assertIn("hand the completed run back to the caller", p)
        self.assertNotIn("OUTER FACTORY LOOP", p)
        self.assertNotIn("factory-learner.md", p)
        self.assertNotIn("factory-learning-reviewer.md", p)

    def test_autoresearch_owns_outer_learning(self):
        program = self.text("loop/PROGRAM.md")
        self.assertIn("Autoresearch is the OUTER controller", program)
        self.assertIn("never as Pi factory agents", program)
        self.assertIn("factory-learner.md", program)
        self.assertIn("factory-learning-reviewer.md", program)
        self.assertIn("exact unseen held-out subjects", program)

    def test_factory_docs_define_extractable_boundary(self):
        docs = self.text("docs/FACTORY-V2.md")
        self.assertIn("Factory output boundary", docs)
        self.assertIn("outside the Pi factory runtime", docs)
        self.assertIn("extractable without carrying the autoresearch loop", docs)

    def test_learning_is_constraint_not_evidence_or_template(self):
        expected = {
            "prompts/research-agent.md": "SEARCH PRIORITY",
            "prompts/master-plan-skill-v2.md": "not a mandatory argument template",
            "prompts/master-plan-reviewer-v2.md": "not a template to imitate",
            "prompts/chapter-writer.md": "does not prescribe prose anatomy",
            "prompts/chapter-reviewer.md": "not a universal style rubric",
            "prompts/final-auditor.md": "never factual evidence",
        }
        for path, token in expected.items():
            with self.subTest(path=path):
                self.assertIn(token, self.text(path))

    def test_factory_learning_defaults_to_prompt_skill_changes(self):
        learner = self.text("loop/prompts/factory-learner.md")
        reviewer = self.text("loop/prompts/factory-learning-reviewer.md")
        self.assertIn("Default to the smallest prompt or skill change", learner)
        self.assertIn("existing prompt/skill", reviewer)
        self.assertIn("require the simpler change", reviewer)

    def test_no_regression_contract_remains_small(self):
        editor = self.text("prompts/book-editor.md")
        judge = self.text("loop/judges/pairwise.md")
        self.assertIn("If `regression_feedback` is present", editor)
        self.assertIn("smallest whole-book operations", editor)
        self.assertIn("a tie is a successful preservation result", judge)
        self.assertIn("do not manufacture a winner", judge)


if __name__ == "__main__":
    unittest.main()
