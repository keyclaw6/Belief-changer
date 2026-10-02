"""Provider identities and the discoverable durable outer-owner contract."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from bc_factory.adapters import execute
from bc_factory.common import FactoryError
from bc_factory.schema import EXTERNAL_ROLES, ROLES, validate_config


class AutoResearchRuntimeInvariantTests(unittest.TestCase):
    def text(self, rel):
        return (ROOT / rel).read_text(encoding="utf-8")

    def config(self):
        return json.loads(self.text("factory/config.json"))

    def test_all_live_profiles_use_configured_opencode_go_identities(self):
        config = self.config()
        validate_config(config)
        expected = {"factory": ("meta", "muse-spark-1.3-contributor", "responses"),
                    "external": ("deepseek", "deepseek-v4.1-flash", "chat")}
        for name, (family, model, api) in expected.items():
            with self.subTest(profile=name):
                profile = config["profiles"][name]
                self.assertEqual(profile["adapter"], "http")
                self.assertEqual(profile["family"], family)
                self.assertEqual(len(profile["routes"]), 1)
                route = profile["routes"][0]
                self.assertEqual(route["model"], model)
                self.assertEqual(route["api"], api)
                self.assertEqual(route["auth_env"], "OPENCODE_GO_API_KEY")
                self.assertEqual(route["endpoint"], f"https://opencode.ai/zen/go/v1/{'responses' if api == 'responses' else 'chat/completions'}")
        bad = copy.deepcopy(config)
        bad["profiles"]["external"]["family"] = config["profiles"]["factory"]["family"]
        with self.assertRaises(FactoryError):
            validate_config(bad)

    def test_semantic_stage_execution_selects_independent_review_profile(self):
        config = self.config()
        for role in ROLES:
            profile = "external" if role in EXTERNAL_ROLES else "factory"
            route = config["profiles"][profile]["routes"][0]
            body = {"model": route["model"], "usage": None}
            output = json.dumps({"synthetic": True})
            if route["api"] == "responses":
                body.update(status="completed", output_text=output)
            else:
                body["choices"] = [{"finish_reason": "stop", "message": {"content": output}}]
            response = {"kind": "http", "route": route["name"], "body": json.dumps(body), "latency_s": 0}
            with self.subTest(role=role), patch("bc_factory.adapters._request", return_value=response) as request:
                result, metadata = execute({"role": role}, config, allow_paid=True)
                self.assertEqual(result, {"synthetic": True})
                self.assertEqual(request.call_args.args[1], config["profiles"][profile])
                self.assertEqual(metadata["family"], config["profiles"][profile]["family"])
                self.assertEqual(metadata["model"], route["model"])

    def test_model_credentials_and_pi_settings_have_no_fallback(self):
        env = self.text(".env.example")
        self.assertIn("OPENCODE_GO_API_KEY=", env)
        for name in ("OPENCODE_API_KEY=", "AI_GATEWAY_API_KEY="):
            self.assertNotIn(name, env)
        settings = json.loads(self.text(".pi/settings.json"))
        self.assertNotIn("npm:pi-provider-fallback", settings.get("packages", []))
        self.assertFalse((ROOT / ".pi/provider-fallback.json").exists())
        self.assertFalse((ROOT / ".opencode/agent/factory.md").exists())

    def test_canonical_skill_exposes_the_actual_lifecycle_commands(self):
        from bc_autoresearch.cli import parser
        command_parser = parser()
        available = next(a.choices for a in command_parser._actions
                         if isinstance(a, argparse._SubParsersAction))
        skill = self.text("skills/running-auto-research-loop/SKILL.md")
        for command in ("start", "status", "stop", "resume"):
            with self.subTest(command=command):
                self.assertIn(command, available)
                self.assertEqual(command_parser.parse_args([command]).command, command)
                self.assertRegex(skill, rf"scripts/autoresearch\.py\s+{command}\b")
        for command in ("start", "resume"):
            self.assertFalse(command_parser.parse_args([command]).allow_paid)
        self.assertIn("loop/PROGRAM.md", skill)
        self.assertIn("loop/HARNESS.md", skill)
        self.assertIn("skills/upgrade/SKILL.md", skill)

    def test_upgrade_and_runner_skills_are_discoverable(self):
        agents, catalog = self.text("AGENTS.md"), self.text("skills/README.md")
        self.assertIn("skills/upgrade/SKILL.md", agents)
        for name in ("upgrade", "running-auto-research-loop"):
            skill = self.text(f"skills/{name}/SKILL.md")
            description = next(line.removeprefix("description: ").strip()
                               for line in skill.splitlines() if line.startswith("description: "))
            self.assertIn(f"**{name}** — {description}", catalog)

    def test_outer_hypothesis_ownership_and_scientific_scope_remain_explicit(self):
        program = self.text("loop/PROGRAM.md").lower()
        hypothesis = self.text("loop/prompts/hypothesizer.md").lower()
        skill = self.text("skills/running-auto-research-loop/SKILL.md").lower()
        self.assertRegex(program, r"outer[^.\n]*controller[^.\n]*hypothesizer")
        self.assertRegex(hypothesis, r"executed directly[^.\n]*outer[^.\n]*controller")
        self.assertRegex(hypothesis, r"pi[^.\n]*evaluator[^.\n]*never[^.\n]*next intervention")
        self.assertIn("authorization source", skill)
        self.assertIn("iteration 054", skill)
        self.assertIn("negative", skill)
        self.assertIn("holdout", skill)
        self.assertIn("unfrozen, untested hypotheses", self.text("loop/FUTURE-HYPOTHESES.md"))


if __name__ == "__main__":
    unittest.main()
