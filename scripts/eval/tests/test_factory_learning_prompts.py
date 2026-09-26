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
        # Pi subprocesses auto-load the repository context file even when a
        # project agent wrapper never names it, so the root contract itself
        # must not contain host/autoresearch execution mechanics.
        agents = self.text("AGENTS.md")
        self.assertNotIn("Read `docs/FACTORY-V2.md`, `docs/BOOK-FACTORY-VISION.md` and `loop/PROGRAM.md`", agents)
        self.assertIn("Pi factory agents must not load that outer-loop contract", agents)
        self.assertNotIn("The supervisor becomes substantively active", agents)
        self.assertNotIn("OpenCode-host recovery", agents)
        self.assertNotIn("provider-state-portability", agents)

    def test_factory_orchestrator_stops_at_completed_book(self):
        p = self.text("prompts/factory-orchestrator.md")
        self.assertIn("COMPLETE_UNRELEASED", p)
        self.assertIn("hand the completed run back to the caller", p)
        self.assertIn("caller-feedback/repair-rNN.json", p)
        self.assertIn("opaque editorial constraints", p)
        self.assertIn("--caller-context FILE", p)
        self.assertNotIn("--learning-from", p)
        self.assertNotIn("REPAIR_REQUIRED", p)
        self.assertNotIn("OUTER FACTORY LOOP", p)
        self.assertNotIn("factory-learner.md", p)
        self.assertNotIn("factory-learning-reviewer.md", p)

    def test_autoresearch_owns_outer_learning(self):
        program = self.text("loop/PROGRAM.md")
        self.assertIn("Autoresearch is the OUTER controller", program)
        self.assertIn("persistent Pi `factory-orchestrator`", program)
        self.assertNotIn("factory/OpenCode executor", program)
        self.assertIn("never as Pi factory agents", program)
        self.assertIn("factory-learner.md", program)
        self.assertIn("factory-learning-reviewer.md", program)
        self.assertIn("exact unseen held-out subjects", program)

    def test_pi_orchestrator_is_the_portable_factory_controller(self):
        readme = self.text(".pi/agents/_README.md")
        agents = self.text("AGENTS.md")
        wrapper = self.text(".pi/agents/factory-orchestrator.md")
        prompt = self.text("prompts/factory-orchestrator.md")
        host = self.text(".opencode/agent/factory.md")
        self.assertIn("Pi `factory-orchestrator` is the reusable factory controller", readme)
        self.assertIn("saved top-level Pi session", readme)
        self.assertIn("`subagent` extension", readme)
        self.assertIn("Pi `factory-orchestrator` owns those stages", agents)
        self.assertNotIn("OpenCode is the persistent factory controller", agents)
        self.assertIn("tools: read, bash, subagent", wrapper)
        self.assertIn('agentScope: "project"', wrapper)
        self.assertIn('agentScope: "project"', prompt)
        self.assertIn("host harness only", host)
        self.assertIn("Do not execute factory roles", host)

    def test_independent_pi_wrappers_do_not_self_review_by_inheritance(self):
        for rel in (".pi/agents/evidence-reviewer.md", ".pi/agents/final-auditor.md"):
            text = self.text(rel)
            self.assertIn("inherited Pi model is controller-only", text)
            self.assertIn("configured independent family", text)

    def test_factory_cli_has_no_outer_autoresearch_commands(self):
        factory_cli = self.text("scripts/bc_factory/cli.py")
        outer_cli = self.text("scripts/bc_autoresearch/cli.py")
        commands = ("register-experiment", "pair-task", "pair-submit", "pair-execute", "decide", "promote",
                    "learning-seed", "regression-task", "regression-submit",
                    "regression-decide", "advance-baseline")
        for command in commands:
            self.assertNotIn(f'"{command}"', factory_cli)
            self.assertIn(f'"{command}"', outer_cli)
        self.assertTrue((ROOT / "scripts/autoresearch.py").is_file())
        self.assertIn("from . import experiments, learning, regression", outer_cli)
        self.assertNotIn("from bc_factory import experiments", outer_cli)

    def test_factory_run_core_does_not_depend_on_outer_autoresearch(self):
        runs = self.text("scripts/bc_factory/runs.py")
        self.assertNotIn("from .learning", runs)
        self.assertNotIn("from .regression", runs)
        self.assertNotIn("loop/judges", runs)
        self.assertNotIn('"regression" /', runs)
        self.assertNotIn("REPAIR_REQUIRED", runs)
        self.assertNotIn("regression_feedback", runs)
        self.assertNotIn("learning_from", runs)
        self.assertNotIn("cross_iteration_learning", runs)
        self.assertNotIn("validate_learning", runs)
        self.assertIn("caller_context", runs)
        self.assertIn("caller_repair_feedback", runs)
        factory_cli = self.text("scripts/bc_factory/cli.py")
        self.assertNotIn("REPAIR_REQUIRED", factory_cli)
        self.assertNotIn('result.get("decision")', factory_cli)
        self.assertNotIn("--learning-from", factory_cli)
        self.assertIn("--caller-context", factory_cli)
        schema = self.text("scripts/bc_factory/schema.py")
        self.assertNotIn('"pair-judge"', schema)
        self.assertNotIn("no_regression_pass", schema)
        self.assertNotIn("validate_learning_packet", schema)
        from bc_factory.runs import active_files
        frozen = set(active_files(ROOT))
        for name in ("experiments.py", "learning.py", "regression.py"):
            outer = self.text(f"scripts/bc_autoresearch/{name}")
            legacy = self.text(f"scripts/bc_factory/{name}")
            self.assertIn("def ", outer)
            self.assertNotIn("def ", legacy)
        self.assertFalse({"scripts/bc_factory/experiments.py", "scripts/bc_factory/learning.py",
                          "scripts/bc_factory/regression.py"} & frozen)
        self.assertFalse(any(path.startswith("scripts/bc_autoresearch/") for path in frozen))
        self.assertFalse(any(path.startswith("loop/") for path in frozen))

    def test_frozen_run_binds_pi_runtime_contracts(self):
        from bc_factory.runs import active_files
        frozen = set(active_files(ROOT))
        self.assertIn("AGENTS.md", frozen)
        self.assertIn("docs/FACTORY-V2.md", frozen)
        self.assertIn("docs/RESEARCH-ACCESS.md", frozen)
        self.assertIn("prompts/factory-orchestrator.md", frozen)
        wrappers = {p.relative_to(ROOT).as_posix() for p in (ROOT / ".pi/agents").glob("*.md")}
        self.assertTrue(wrappers <= frozen)
        for rel in (".pi/settings.json", ".pi/provider-fallback.json", ".pi/pi-goal-x-settings.json"):
            self.assertIn(rel, frozen)
        self.assertFalse(any(path.startswith(".opencode/") for path in frozen))

    def test_factory_docs_define_extractable_boundary(self):
        docs = self.text("docs/FACTORY-V2.md")
        self.assertIn("Factory output boundary", docs)
        self.assertIn("outside the Pi factory runtime", docs)
        self.assertIn("extractable without carrying the autoresearch loop", docs)

    def test_learning_is_constraint_not_evidence_or_template(self):
        expected = {
            "prompts/research-agent.md": "SEARCH PRIORITY",
            "prompts/evidence-reviewer.md": "NOT empirical evidence",
            "prompts/master-plan-skill-v2.md": "not empirical evidence",
            "prompts/master-plan-reviewer-v2.md": "never as empirical evidence",
            "prompts/chapter-writer.md": "not empirical evidence",
            "prompts/chapter-reviewer.md": "not empirical evidence",
            "prompts/reader-state.md": "caller-owned editorial guidance rather than evidence",
            "prompts/book-editor.md": "never factual evidence",
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
        wrapper = self.text(".pi/agents/book-editor.md")
        judge = self.text("loop/judges/pairwise.md")
        self.assertIn("If `caller_repair_feedback` is present", editor)
        self.assertNotIn("no-regression", editor.lower())
        self.assertNotIn("no-regression", wrapper.lower())
        self.assertIn("smallest whole-book operations", editor)
        self.assertIn("a tie is a successful preservation result", judge)
        self.assertIn("do not manufacture a winner", judge)


if __name__ == "__main__":
    unittest.main()
