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

    def test_autoresearch_supervisor_skill_has_circuit_breakers(self):
        skill = (ROOT / "skills" / "running-auto-research-loop" / "SKILL.md").read_text(encoding="utf-8")
        required = (
            "OpenCode Go only",
            "Do not arm the heartbeat until startup is proven",
            "A heartbeat is a watchdog, not a retry engine",
            "no successful model response since campaign startup",
            "two consecutive heartbeat checks with no durable progress",
            "disable the recurring schedule",
        )
        for phrase in required:
            self.assertIn(phrase, skill)


if __name__ == "__main__":
    unittest.main()
