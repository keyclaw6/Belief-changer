"""Regressions for the calibration-ready research and planning contracts."""
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class ResearchContractTests(unittest.TestCase):
    def test_roles_receive_only_blind_bounded_inputs(self):
        """OpenSpec: research begins; unbounded and forbidden work is rejected."""
        prompt = read("prompts/research-agent.md")

        for required in (
            "fresh-context **research lead**",
            "same filled brief",
            "one bounded assignment record",
            "community/source scope",
            "persona scope",
            "bank slots",
            "caller rejects an exact-input brief containing calibration/reference metadata",
            "Every matrix row must be independently reconstructable",
            "exactly one integer from `1` through `10`",
            "Do not hide alternate, supplemental, fallback",
            "Never use `same`, `as above`",
            "brief's non-goals as research-scope exclusions",
            "CANDIDATE — VALIDATION REQUIRED",
            "retrieval-capable lead pass validates",
            "reject it and every dependent finding",
        ):
            self.assertIn(required, prompt)
        self.assertNotIn("harvested (from the communities, the reference analyses", prompt)

    def test_source_packets_and_coverage_are_measurable(self):
        """OpenSpec: quotes remain verifiable and weak numeric coverage stays open."""
        prompt = read("prompts/research-agent.md")

        for required in (
            "## Visit history",
            "## Captured raw source text",
            "Worker ID:",
            "Search settings:",
            "Research-log event IDs:",
            "Capture ID:",
            "EXACT_QUOTE | INTERPRETATION",
            "character-for-character verification",
            "qualitative verdict is `PASS`",
            "≥5 moments/persona from ≥2 sources",
            "≥8 terms/persona",
        ):
            self.assertIn(required, prompt)

    def test_caller_owns_invisible_runtime_metadata_and_persistence(self):
        """OpenSpec: a bare model call returns artifacts instead of false-blocking."""
        prompt = read("prompts/research-agent.md")

        for required in (
            "The **caller**, not the language model inside the call",
            "MUST NOT try to inspect invisible request metadata",
            "returns complete artifact-ready Markdown blocks",
            "Lack of direct filesystem access is not a blocker",
            "first call returns provisional personas",
        ):
            self.assertIn(required, prompt)

    def test_templates_preserve_handoff_and_arm_measurement(self):
        """OpenSpec: syntheses trace to packets and equal-arm yields are reconstructable."""
        log = read("production-books/_template/research/research-log.md")
        packets = read("production-books/_template/research/sources/README.md")
        lived = read("production-books/_template/research/lived-experience.md")
        science = read("production-books/_template/research/scientific-evidence.md")

        for required in ("Assignment / coverage matrix", "Research-arm summary",
                         "Runtime model ID", "Reasoning config", "Cost (USD)"):
            self.assertIn(required, log)
        for required in ("Captured raw source text", "Evidence ID:", "Capture ID:",
                         "Persona tags:", "Bank slots:"):
            self.assertIn(required, packets)
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
            "master-plan-reviewer.md`",
            "Opus sub-agent",
            "Commit both directly to `main`",
        ):
            self.assertNotIn(forbidden, prompt)

    def test_plan_and_review_gate_explicit_budgets_and_allowed_models(self):
        """OpenSpec: only a fit reviewed plan can reach chapter writing."""
        plan_prompt = read("prompts/master-plan-skill-v2.md")
        review_prompt = read("prompts/master-plan-reviewer-v2.md")
        plan_template = read("production-books/_template/master-plan.md")
        review_template = read("production-books/_template/master-plan-review.md")

        for text in (plan_prompt, review_prompt, plan_template):
            self.assertIn("54,000–66,000", text)
            self.assertRegex(text, r"(?:single-integer|single integer|explicit integer)")
        for model in ("Gemini 3.1 Pro", "GPT-5.6 Sol", "Grok 4.5"):
            self.assertIn(model, review_prompt)
            self.assertIn(model, review_template)
        self.assertEqual("needs changes first", review_template.rstrip().splitlines()[-1])


class HarnessBoundaryTests(unittest.TestCase):
    def test_brief_and_research_roles_are_manifested(self):
        """OpenSpec: downstream stages stop when the brief or role record is missing."""
        harness = read("calibration/HARNESS.md")
        manifest = json.loads(read("calibration/runs/_template/manifest.json"))

        framing_row = next(line for line in harness.splitlines()
                           if line.startswith("| Framing |"))
        self.assertIn("`00-brief.md`", framing_row)
        self.assertIn("baseline_boundary", manifest)
        self.assertIn("research_orchestration", manifest)
        self.assertIn("research_lead", manifest["models"])
        self.assertIn("research_workers", manifest["models"])

    def test_subrole_brief_contains_no_calibration_or_reference_metadata(self):
        """HARNESS §4: the style guide alone carries reference-derived patterns."""
        brief = read("production-books/quit-sugar/00-brief.md")

        for forbidden in ("Good Sugar Bad Sugar", "calibration/", "analysis/",
                          "reference metrics", "factory-calibration"):
            self.assertNotIn(forbidden, brief)


if __name__ == "__main__":
    unittest.main()
