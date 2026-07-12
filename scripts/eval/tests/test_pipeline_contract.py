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
            "License / quotation basis:",
            "Required attribution:",
            "Retention / deletion status:",
            "Privacy judgment:",
            "## Minimum retained excerpt",
            "EXACT_QUOTE | INTERPRETATION",
            "Persona tags:",
            "Bank slots:",
        ):
            self.assertIn(required, packets)

    def test_execution_is_quality_first_without_theoretical_ceiling_block(self):
        """OpenSpec: the greatest live allowance is used without shrinking work.

        The quality-only law's surviving home is the research prompt
        (calibration/HARNESS.md retired to PROGRAM.md, founder 2026-07-12)."""
        prompt = read("prompts/research-agent.md")
        spec = read(
            "openspec/changes/calibration-ready-research-pipeline/"
            "specs/deep-research/spec.md"
        )

        self.assertIn("Quality is the only optimizer", prompt)
        self.assertIn("quality-only law", prompt)
        self.assertIn("greatest completion allowance actually authorized", spec)
        self.assertIn("no caller, prompt, framework", spec)
        self.assertIn("MUST NOT be stopped, narrowed, ranked, or selected", spec)

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
        for model in ("Gemini 3.1 Pro", "GPT-5.6 Sol", "Grok 4.5"):
            self.assertIn(model, template_review)

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
        """OpenSpec: run-001 stays Opus; Muse is isolated after the baseline."""
        spec = read(
            "openspec/changes/calibration-ready-research-pipeline/"
            "specs/book-pipeline/spec.md"
        )

        for model in (
            "DeepSeek V4 Pro", "MiniMax M3", "GPT‑5.6 Luna",
            "Gemini 3.1 Pro", "GPT‑5.6 Sol", "Grok 4.5",
            "Claude Opus 4.6", "Muse Spark 1.1",
        ):
            self.assertIn(model, spec)
        self.assertIn("Gemini 3.1 Flash Lite is forbidden in every role", spec)
        self.assertIn("greatest output allowance actually authorized", spec)
        self.assertIn("MUST NOT replace the run-001 baseline", spec)


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
        """HARNESS §4: only the style guide carries reference-derived patterns."""
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
