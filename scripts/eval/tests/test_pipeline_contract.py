"""Regressions for the calibration-ready research and planning contracts."""
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class ResearchContractTests(unittest.TestCase):
    def test_lead_owns_decomposition_and_remains_blind(self):
        """OpenSpec: research begins under model-owned delegation and blindness."""
        prompt = read("prompts/research-agent.md")

        for required in (
            "Choose your own research plan",
            "Use multiple fresh subagents",
            "prescribes a role graph, a sequence, or a stopping number; the lead owns",
            "Do not ask the operator to design the research",
            "Never use reference books",
            "Never invent a source, quote, persona, or finding",
            "Generic volume is not depth",
            "DeepSeek V4 Pro",
            "independent high-reasoning evidence editor from another model",
            "never through OpenRouter",
            "This prompt defines role contracts; it does not dispatch models",
        ):
            self.assertIn(required, prompt)
        for obsolete in (
            "Assignment / coverage matrix",
            "at least four separate fresh-context scout/specialist tracks",
            "Every matrix row must be independently reconstructable",
            "one focused assignment record",
        ):
            self.assertNotIn(obsolete, prompt)

    def test_evidence_is_minimal_rights_safe_and_verifiable(self):
        """OpenSpec: accepted evidence is durable, private enough, and exact."""
        prompt = read("prompts/research-agent.md")
        packets = read("production-books/_template/research/sources/README.md")

        for required in (
            "minimum permitted excerpt",
            "deletion-sensitive/nonredistributable material",
            "Reddit is excluded",
            "character-for-character",
            "CONTESTED",
        ):
            self.assertIn(required, prompt)
        for required in (
            "Access / license basis:",
            "Excerpt / redistribution basis:",
            "Required attribution:",
            "Retention / deletion sensitivity:",
            "Privacy / personal-data basis:",
            "## Minimum retained excerpt",
            "EXACT_QUOTE | INTERPRETATION",
            "Persona tags:",
            "Bank slots:",
        ):
            self.assertIn(required, packets)

    def test_execution_is_quality_first_without_theoretical_ceiling_block(self):
        """OpenSpec: the greatest live allowance is used without shrinking work.

        The quality-only law's surviving home is the research prompt
        (HARNESS retired to PROGRAM.md; stale change specs deleted 2026-07-13)."""
        prompt = read("prompts/research-agent.md")

        self.assertIn("Quality is the only optimizer", prompt)
        self.assertIn("quality-only law", prompt)
        self.assertIn("never stop conditions", prompt)

    def test_templates_record_results_without_planning_reasoning(self):
        """OpenSpec: files preserve evidence and arm records, not a workflow graph."""
        log = read("production-books/_template/research/research-log.md")
        lived = read("production-books/_template/research/lived-experience.md")
        science = read("production-books/_template/research/scientific-evidence.md")

        for required in (
            "Model and subagent calls",
            "Objective and model-chosen strategy",
            "Requested → actual model",
            "Requested / authorized output",
            "Source decisions",
            "Final bank audit",
            "Research-arm summary",
        ):
            self.assertIn(required, log)
        self.assertNotIn("Assignment / coverage matrix", log)
        for bank in (1, 2, 3, 4, 5, 6, 9, 10):
            self.assertIn(f"## Bank {bank}", lived)
        for bank in (7, 8):
            self.assertIn(f"## Bank {bank}", science)
        self.assertIn("SUPPORTED | MIXED | CONTESTED", science)
        for required in (
            "Intervention-ready evidence units", "Situation:", "Reader wording:",
            "Implicated belief:", "Emotion:", "Permitted inference:",
            "Prohibited inference:", "Source locator:", "Evidence grade:",
            "Brief-belief evidence gaps", "Missing support:", "Owner:",
        ):
            self.assertIn(required, lived)
            self.assertIn(required, science)
        prompt = read("prompts/research-agent.md")
        self.assertIn("source count never establishes", prompt)
        self.assertIn("primary and subordinate brief belief", prompt)


class PlanningContractTests(unittest.TestCase):
    def test_planner_is_blind_and_uses_exact_pipeline_inputs(self):
        """OpenSpec: a planner given forbidden reference context must stop."""
        prompt = read("prompts/master-plan-skill-v2.md")

        for required in (
            "prompts/style-guide.md",
            "production-books/<slug>/00-brief.md",
            "production-books/<slug>/framing.md",
            "production-books/<slug>/research/lived-experience.md",
            "production-books/<slug>/research/scientific-evidence.md",
            "exact-input contract",
        ):
            self.assertIn(required, prompt)
        for forbidden in (
            "analysis/easyway-prose-patterns.md",
            "analysis/sugar-prose-patterns.md",
            "Opus sub-agent",
        ):
            self.assertNotIn(forbidden, prompt)

    def test_live_and_generic_plans_have_review_and_budget_gates(self):
        """OpenSpec: only a fit, budgeted, non-Opus-reviewed plan reaches writing."""
        plan = read("production-books/_template/master-plan.md")
        self.assertIn("54,000–66,000", plan)
        self.assertIn("Planned chapter count", plan)
        self.assertIn("single integer", plan)
        self.assertNotIn("Reviewed by an Opus sub-agent", plan)

        template_review = read("production-books/_template/master-plan-review.md")
        self.assertIn("GPT-5.6 Sol", template_review)
        self.assertIn("gpt-5.6-sol", template_review)
        self.assertIn("fresh native Codex subagent", template_review)
        self.assertNotIn("Gemini", template_review)
        self.assertNotIn("Grok", template_review)

        for review_path in (
            "production-books/_template/master-plan-review.md",
            "production-books/quit-sugar/master-plan-review.md",
        ):
            review = read(review_path)
            self.assertIn(
                review.rstrip().splitlines()[-1],
                ("needs changes first", "fit to write from"),
            )

    def test_master_plan_is_single_source_and_reviewed_by_outcome(self):
        """OpenSpec H-039: semantic context lives once; prose is reviewed as prose."""
        planner = read("prompts/master-plan-skill-v2.md")
        reviewer = read("prompts/master-plan-reviewer-v2.md")
        template = read("production-books/_template/master-plan.md")

        for required in (
            "Define every shared book decision once",
            "Compact evidence ledger",
            "Compact chapter cards",
            "Mantras are routed by chapter, not by occurrence arithmetic",
            "The writer derives `IN THIS CHAPTER`",
        ):
            self.assertIn(required, planner)
        for required in (
            "## Blocking dimensions",
            "## Explicit non-blockers",
            "If no blocking dimension fails",
            "prose-density or sentence metrics before a chapter exists",
        ):
            self.assertIn(required, reviewer)
        for required in (
            "## Evidence ledger", "## Mantra sheet", "## Instruction spine",
            "## Arc and length map", "## Compact chapter cards",
        ):
            self.assertIn(required, template)
        for obsolete in (
            "Mantra assignment — DEBUTS", "Chapter anatomy:",
            "mantra-state (already debuted)",
        ):
            self.assertNotIn(obsolete, template)

    def test_role_models_and_writer_arms_are_explicit(self):
        """PROGRAM §1 (founder 2026-07-13): model matrix + routing law explicit."""
        program = read("PROGRAM.md")
        cfg = read("loop/config.yaml")

        self.assertIn("meta/muse-spark-1.1", program)
        self.assertIn("reasoning `{effort: high}`", program)
        self.assertIn("provider: {allow_fallbacks: false}", program)
        self.assertIn("DeepSeek V4 Pro", program)
        self.assertIn("GPT‑5.6 Sol", program)
        self.assertIn("NEVER route through OpenRouter", program)
        self.assertIn("RESCINDED", program)
        self.assertIn("writer_model: meta/muse-spark-1.1", cfg)
        self.assertIn("writer_provider: openrouter", cfg)
        self.assertIn("writer_reasoning: high", cfg)
        self.assertIn("writer_temperature: 0.7", cfg)
        self.assertNotIn("writer_max_tokens:", cfg)
        self.assertIn("writer_attempts: 1", cfg)
        self.assertIn("writer_allow_fallbacks: false", cfg)
        self.assertIn("researcher_model: deepseek/deepseek-v4-pro", cfg)
        self.assertIn("judge_model: gpt-5.6-sol", cfg)
        self.assertIn("judge_route: codex-native", cfg)
        self.assertIn("planner_route: codex-native", cfg)


class HarnessBoundaryTests(unittest.TestCase):
    def test_manifest_records_simple_model_led_research(self):
        """OpenSpec: the run records calls without prescribing an org chart."""
        manifest = json.loads(read("calibration/runs/_template/manifest.json"))

        self.assertTrue(
            manifest["research_orchestration"]["lead_chooses_subagents_and_workflow"]
        )
        models = manifest["models"]
        for key in ("research_lead", "research_calls", "research_reviewer",
                    "writer", "later_writer_arm"):
            self.assertIn(key, models)
        for obsolete in ("research_architects", "research_retrieval_agents",
                         "research_workers"):
            self.assertNotIn(obsolete, models)

    def test_subrole_brief_contains_no_calibration_metadata(self):
        """PROGRAM §7: only the style guide carries reference-derived patterns."""
        brief = read("production-books/quit-sugar/00-brief.md")

        for forbidden in (
            "Good Sugar Bad Sugar", "calibration/", "analysis/",
            "reference metrics", "factory-calibration",
        ):
            self.assertNotIn(forbidden, brief)

    def test_invalid_reddit_pilot_artifacts_are_removed(self):
        """OpenSpec: unauthorized source packets remain absent."""
        forbidden = (
            "calibration/pilots/council/persona-architect-annotations.json",
            "calibration/pilots/council/persona-architect-output.md",
            "calibration/pilots/council/persona-architect-review.md",
            "calibration/pilots/council/a1-q3-f01",
            "calibration/pilots/council/retrieval-a1-q3-web.md",
            "calibration/pilots/council/retrieval-a1-q3-deepseek-validation.md",
            "calibration/pilots/council/retrieval-a1-q3-minimax-review.md",
            "calibration/pilots/council/retrieval-a1-q3-luna-review.md",
        )
        for path in forbidden:
            self.assertFalse((ROOT / path).exists(), path)


if __name__ == "__main__":
    unittest.main()
