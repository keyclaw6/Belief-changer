"""Iteration-evidence and promotion-gate regression tests. Offline, stdlib only."""
from __future__ import annotations
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SOURCE / "scripts"))
from bc_autoresearch.experiments import wilson_lower
from validate_repo import REQUIRED_FILES, source_files


class PromotionGateTest(unittest.TestCase):
    def test_small_samples_cannot_promote(self):
        # loop/PROGRAM.md: three samples are screening, never sufficient.
        self.assertLess(wilson_lower(3, 3), 0.5)
        self.assertLess(wilson_lower(2, 2), 0.5)
        self.assertLess(wilson_lower(0, 3), 0.5)

    def test_sufficient_allocation_can_pass(self):
        # A large confirmatory allocation is the specified way out (051).
        self.assertGreater(wilson_lower(9, 9), 0.5)


class IterationEvidenceTest(unittest.TestCase):
    def test_evidence_files_are_machine_readable(self):
        found = sorted((SOURCE / "loop" / "iterations").glob("*/evidence.json"))
        self.assertTrue(found, "no iteration evidence bundle present")
        for path in found:
            with self.subTest(iter=path.parent.name):
                data = json.loads(path.read_text())
                for key in ("probe", "verdict", "head", "files"):
                    self.assertIn(key, data)
                self.assertIn(data["verdict"], ("SUPPORT", "REFUTE"))

    def test_repo_gate_accepts_tree(self):
        proc = subprocess.run([sys.executable, str(SOURCE / "scripts" / "validate_repo.py"),
                               str(SOURCE)], capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stderr)


class RepositorySourceGateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "source"
        for name in REQUIRED_FILES:
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Synthetic source-gate fixture.\n", encoding="utf-8")
        shutil.copyfile(SOURCE / "factory/config.json", self.repo / "factory/config.json")
        shutil.copyfile(SOURCE / ".gitignore", self.repo / ".gitignore")

    def git(self, *args):
        if not shutil.which("git"):
            self.skipTest("Git is unavailable; filesystem fallback remains tested")
        subprocess.run(["git", "-C", str(self.repo), *args], check=True,
                       capture_output=True, timeout=10)

    def write(self, relative):
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n", encoding="utf-8")
        return path

    def gate(self):
        return subprocess.run([sys.executable, str(SOURCE / "scripts/validate_repo.py"),
                               str(self.repo)], capture_output=True, text=True, timeout=20)

    def test_git_gate_accepts_ignored_private_learning(self):
        self.git("init", "--quiet")
        self.write("loop/iterations/055/learning/evidence.json")
        result = self.gate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_git_gate_rejects_unignored_intermediate_artifact(self):
        self.git("init", "--quiet")
        self.write("loop/iterations/055/BLOCKED.md")
        result = self.gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("Intermediate campaign artifact re-entered source tree", result.stderr)
        self.assertIn("loop/iterations/055/BLOCKED.md", result.stderr)

    def test_git_gate_rejects_tracked_artifact_even_when_ignored(self):
        self.git("init", "--quiet")
        path = "loop/iterations/055/learning/evidence.json"
        self.write(path)
        self.git("add", "--force", "--", path)
        result = self.gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn(path, result.stderr)

    def test_compact_progress_is_still_validated(self):
        self.git("init", "--quiet")
        self.write("loop/iterations/055/progress.json")
        result = self.gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("Invalid iteration handoff", result.stderr)

    def test_export_without_git_uses_strict_filesystem_gate(self):
        self.write("loop/iterations/055/learning/evidence.json")
        result = self.gate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("loop/iterations/055/learning/evidence.json", result.stderr)

    def test_missing_git_executable_uses_strict_filesystem_inventory(self):
        path = self.write("loop/iterations/055/learning/evidence.json")
        with patch("validate_repo.subprocess.run", side_effect=FileNotFoundError):
            self.assertIn(path, source_files(self.repo, "loop/iterations"))


class OfflineCredentialIsolationTest(unittest.TestCase):
    def test_only_test_subprocess_loses_the_provider_key(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            log = root / "invocations.jsonl"
            runner = root / "synthetic-python"
            runner.write_text(
                f"#!{sys.executable}\n"
                "import json, os, sys\n"
                f"with open({str(log)!r}, 'a') as output:\n"
                "    output.write(json.dumps({'argv': sys.argv[1:], "
                "'provider_present': 'OPENCODE_GO_API_KEY' in os.environ, "
                "'control_present': 'BC_SOURCE_GATE_CONTROL' in os.environ}) + '\\n')\n",
                encoding="utf-8")
            runner.chmod(0o755)
            environment = {**os.environ, "PYTHON": str(runner),
                           "OPENCODE_GO_API_KEY": "synthetic-offline-isolation-value",
                           "BC_SOURCE_GATE_CONTROL": "synthetic-control"}
            result = subprocess.run(["bash", str(SOURCE / "scripts/check.sh"), str(SOURCE)],
                                    env=environment, capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            invocations = [json.loads(line) for line in log.read_text().splitlines()]
            tests = [entry for entry in invocations if entry["argv"][:2] == ["-m", "unittest"]]
            self.assertEqual(len(tests), 1)
            self.assertFalse(tests[0]["provider_present"])
            self.assertTrue(all(entry["control_present"] for entry in invocations))
            self.assertTrue(all(entry["provider_present"] for entry in invocations if entry not in tests))
            self.assertIn("OPENCODE_GO_API_KEY", environment)


if __name__ == "__main__":
    unittest.main()
