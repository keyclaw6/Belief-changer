"""Small static tests for the prompt-led factory-learning layer."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from bc_factory.schema import ROLES


class FactoryLearningPromptTests(unittest.TestCase):
    def text(self, rel):
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_factory_learner_targets_transfer_not_one_book(self):
        p = self.text("loop/prompts/factory-learner.md")
        for token in ("transferable_factory_lessons", "subject_specific_lessons",
                      "holdout_requirements", "MEASURE_MORE", "smallest_change"):
            self.assertIn(token, p)
        self.assertNotIn('"held_out_subjects"', p)
        self.assertIn("what general factory mechanism", p)

    def test_learning_reviewer_checks_overfit(self):
        p = self.text("loop/prompts/factory-learning-reviewer.md")
        for token in ("not_subject_overfit", "causal_honesty", "judge_overfit_control",
                      "falsifiable", "holdout_requirements"):
            self.assertIn(token, p)
        self.assertIn("Do not write book prose", p)

    def test_inner_roles_treat_learning_as_constraints_not_template_or_evidence(self):
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

    def test_no_regression_repair_stays_minimal(self):
        p = self.text("prompts/book-editor.md")
        self.assertIn("If `regression_feedback` is present", p)
        self.assertIn("Repair only the dimensions or critical defects", p)
        self.assertIn("smallest whole-book operations", p)

    def test_no_regression_judge_allows_ties(self):
        p = self.text("loop/judges/pairwise.md")
        self.assertIn("a tie is a successful preservation result", p)
        self.assertIn("do not manufacture a winner", p)

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

    def test_helper_wrappers_match_their_real_surfaces(self):
        orchestrator = self.text(".pi/agents/factory-orchestrator.md")
        researcher = self.text(".pi/agents/researcher.md")
        hypothesizer = self.text(".pi/agents/hypothesizer.md")
        trace = self.text(".pi/agents/trace-analyzer.md")
        judge = self.text(".pi/agents/judge.md")
        self.assertIn("not itself a factory task/result", orchestrator)
        self.assertIn("canonical Pi role wrappers", orchestrator)
        self.assertIn("not a factory task/result role", researcher)
        self.assertIn("Do not mutate runs", hypothesizer)
        self.assertIn("Do not mutate runs", trace)
        self.assertIn("pair-submit", judge)
        self.assertIn("regression-submit", judge)

    def test_factory_learning_defaults_to_prompt_skill_changes(self):
        learner = self.text("loop/prompts/factory-learner.md")
        reviewer = self.text("loop/prompts/factory-learning-reviewer.md")
        self.assertIn("Default to the smallest prompt or skill change", learner)
        self.assertIn("existing prompt/skill", reviewer)
        self.assertIn("require the simpler change", reviewer)

    def test_meta_agents_are_pi_only_and_read_only(self):
        for name in ("factory-learner", "factory-learning-reviewer"):
            p = self.text(f".pi/agents/{name}.md")
            self.assertIn("tools: read", p)
            self.assertNotIn("bash", p.split("---", 2)[1])
            self.assertFalse((ROOT / f".opencode/agents/{name}.md").exists())

    def test_outer_loop_is_prompt_led(self):
        orchestrator = self.text("prompts/factory-orchestrator.md")
        program = self.text("loop/PROGRAM.md")
        self.assertIn("factory-learner.md", orchestrator)
        self.assertIn("factory-learning-reviewer.md", orchestrator)
        self.assertIn("exact unseen held-out subjects", program)
        self.assertIn("research gaps", orchestrator)
        self.assertIn("training-only improvement is evidence of possible overfit", orchestrator.lower())


if __name__ == "__main__":
    unittest.main()
