from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class AutoResearchRuntimeInvariantTests(unittest.TestCase):
    def test_factory_uses_opencode_go_only(self):
        config = json.loads((ROOT / "factory" / "config.json").read_text(encoding="utf-8"))
        routes = config["profiles"]["factory"]["routes"]
        self.assertEqual([route["name"] for route in routes], ["opencode-go"])
        self.assertEqual(routes[0]["auth_env"], "OPENCODE_GO_API_KEY")
        self.assertTrue(routes[0]["endpoint"].startswith("https://opencode.ai/zen/go/"))
        serialized = json.dumps(config).lower()
        for forbidden in ("vercel", "ai_gateway", "opencode-zen", "chatgpt", "opencodex"):
            self.assertNotIn(forbidden, serialized)

    def test_no_pi_provider_fallback_layer(self):
        settings = json.loads((ROOT / ".pi" / "settings.json").read_text(encoding="utf-8"))
        self.assertNotIn("npm:pi-provider-fallback", settings.get("packages", []))
        self.assertFalse((ROOT / ".pi" / "provider-fallback.json").exists())
        self.assertFalse((ROOT / ".opencode" / "agent" / "factory.md").exists())

    def test_env_example_exposes_only_opencode_go_for_models(self):
        env = (ROOT / ".env.example").read_text(encoding="utf-8")
        self.assertIn("OPENCODE_GO_API_KEY=", env)
        self.assertNotIn("OPENCODE_API_KEY=", env)
        self.assertNotIn("AI_GATEWAY_API_KEY=", env)

    def test_autoresearch_supervisor_skill_repairs_before_stopping(self):
        skill = (ROOT / "skills" / "running-auto-research-loop" / "SKILL.md").read_text(encoding="utf-8")
        required = (
            "OpenCode Go only",
            "real pseudo-terminal (PTY)",
            "Do not arm the heartbeat until startup is proven",
            "A heartbeat is a watchdog, not a retry engine",
            "attempt to restore forward progress",
            "A blocker is not grounds to stop until",
            "Repair before stop",
            "same failure fingerprint recurs after a real repair",
            "disable the recurring schedule",
        )
        for phrase in required:
            self.assertIn(phrase, skill)

    def test_upgrade_skill_governs_repository_changes(self):
        upgrade = (ROOT / "skills" / "upgrade" / "SKILL.md").read_text(encoding="utf-8")
        running = (ROOT / "skills" / "running-auto-research-loop" / "SKILL.md").read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        catalog = (ROOT / "skills" / "README.md").read_text(encoding="utf-8")
        self.assertIn("before changing the belief-changer system itself", upgrade.lower())
        self.assertIn("skills/upgrade/SKILL.md", agents)
        for name, skill in (("upgrade", upgrade), ("running-auto-research-loop", running)):
            description = next(line.removeprefix("description: ").strip()
                               for line in skill.splitlines() if line.startswith("description: "))
            self.assertIn(f"**{name}** — {description}", catalog)

    def test_external_evaluator_is_deepseek_v41_flash_via_opencode_go(self):
        config = json.loads((ROOT / "factory" / "config.json").read_text(encoding="utf-8"))
        external = config["profiles"]["external"]
        self.assertEqual(external["family"], "deepseek")
        self.assertEqual(len(external["routes"]), 1)
        route = external["routes"][0]
        self.assertEqual(route["model"], "deepseek-v4.1-flash")
        self.assertEqual(route["auth_env"], "OPENCODE_GO_API_KEY")
        self.assertEqual(route["api"], "chat")
        self.assertEqual(route["endpoint"], "https://opencode.ai/zen/go/v1/chat/completions")

    def test_host_controller_owns_hypothesis_formation(self):
        program = (ROOT / "loop" / "PROGRAM.md").read_text(encoding="utf-8")
        hypothesis = (ROOT / "loop" / "prompts" / "hypothesizer.md").read_text(encoding="utf-8")
        backlog = (ROOT / "loop" / "FUTURE-HYPOTHESES.md").read_text(encoding="utf-8")
        self.assertIn("human-facing host autoresearch controller itself is the hypothesizer", program)
        self.assertIn("executed directly by the human-facing host autoresearch controller", hypothesis)
        self.assertIn("unfrozen, untested hypotheses", backlog)


if __name__ == "__main__":
    unittest.main()
