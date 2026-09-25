"""Static contract tests for the factory-learning prompt layer."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]


class FactoryLearningPromptTests(unittest.TestCase):
    def text(self, rel):
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_factory_learner_targets_transfer_not_one_book(self):
        p = self.text("loop/prompts/factory-learner.md")
        for token in (
            "transferable_factory_lessons",
            "subject_specific_lessons",
            "held_out_subjects",
            "MEASURE_MORE",
            "smallest_change",
            "possible_regressions",
            "Held-out subjects are evaluation only",
        ):
            self.assertIn(token, p)
        self.assertIn("what general factory mechanism", p)

    def test_independent_factory_learning_reviewer_is_anti_overfit(self):
        p = self.text("loop/prompts/factory-learning-reviewer.md")
        for token in (
            "not_subject_overfit",
            "causal_honesty",
            "held_out_integrity",
            "judge_overfit_control",
            "falsifiable",
            "MEASURE_MORE",
        ):
            self.assertIn(token, p)
        self.assertIn("Do not write book prose", p)

    def test_inner_roles_do_not_treat_learning_as_template_or_evidence(self):
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

    def test_runtime_learning_contract_forbids_cross_topic_template_transfer(self):
        p = self.text("scripts/bc_factory/learning.py")
        self.assertIn("NOT a mandatory rhetorical template", p)
        self.assertIn("never force a learned mechanism", p)

    def test_no_regression_repair_is_minimal_and_preserves_other_dimensions(self):
        p = self.text("prompts/book-editor.md")
        self.assertIn("If `regression_feedback` is present", p)
        self.assertIn("Repair only the dimensions or critical defects", p)
        self.assertIn("Preserve every dimension where the candidate tied or beat the baseline", p)
        self.assertIn("smallest whole-book operations", p)

    def test_pairwise_no_regression_mode_allows_ties(self):
        p = self.text("loop/judges/pairwise.md")
        self.assertIn("a tie is a successful preservation result", p)
        self.assertIn("do not manufacture a winner", p)

    def test_factory_learning_roles_are_registered(self):
        learner = self.text(".pi/agents/factory-learner.md")
        reviewer = self.text(".pi/agents/factory-learning-reviewer.md")
        oc_learner = self.text(".opencode/agents/factory-learner.md")
        oc_reviewer = self.text(".opencode/agents/factory-learning-reviewer.md")
        self.assertIn("loop/prompts/factory-learner.md", learner)
        self.assertIn("never writes book prose", learner)
        self.assertIn("tools: read", learner)
        self.assertNotIn("bash", learner.split("---", 2)[1])
        self.assertIn("loop/prompts/factory-learning-reviewer.md", reviewer)
        self.assertIn("independent evaluator family", reviewer)
        self.assertIn("sealed held-out results", reviewer)
        self.assertIn("tools: read", reviewer)
        self.assertNotIn("bash", reviewer.split("---", 2)[1])
        self.assertIn("mode: subagent", oc_learner)
        self.assertIn("factory-learner.md", oc_learner)
        self.assertIn("edit: deny", oc_learner)
        self.assertIn("bash: deny", oc_learner)
        self.assertIn("task: deny", oc_learner)
        self.assertIn("mode: subagent", oc_reviewer)
        self.assertIn("independent", oc_reviewer.lower())
        self.assertIn("do not ACCEPT", oc_reviewer)
        self.assertIn("edit: deny", oc_reviewer)
        self.assertIn("bash: deny", oc_reviewer)
        self.assertIn("task: deny", oc_reviewer)

    def test_orchestrator_and_program_require_held_out_transfer(self):
        orchestrator = self.text("prompts/factory-orchestrator.md")
        program = self.text("loop/PROGRAM.md")
        agents = self.text("AGENTS.md")
        for p in (orchestrator, program, agents):
            self.assertIn("factory-learner.md", p)
            self.assertIn("factory-learning-reviewer.md", p)
            self.assertIn("held-out", p.lower())
        self.assertIn("A training-only improvement is evidence of possible overfit", orchestrator)
        self.assertIn("Held-out subjects are a sealed test set", program)


if __name__ == "__main__":
    unittest.main()
