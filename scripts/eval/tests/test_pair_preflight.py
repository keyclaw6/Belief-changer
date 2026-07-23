"""RF-02 rejects aliases and hardlinks before parsers or outside reads."""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
import candidate_pair as PAIR  # noqa: E402
import pair_store as STORE  # noqa: E402


class PairPreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def fixture(self, name):
        root = self.root / name
        files = {
            "loop/config.yaml": (
                "judge_rubric: calibration/rubric.md\n"
                "reference_dir: calibration/reference\nresults_tsv: loop/results.tsv\n"),
            "loop/results.tsv": "iter\treward\tverdict\n",
            "prompts/style-guide.md": "style\n",
            "production-books/test/master-plan.md": "### CH-01 — One\n",
            "production-books/test/chapters/chapter-01.md": "chapter\n",
            "production-books/test/research/source.txt": "source\n",
            "calibration/rubric.md": "rubric\n",
            "calibration/reference/001.txt": "reference\n",
            "calibration/reference/reference-metrics.json": "{}\n"}
        for relative, text in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        return root

    def test_intermediate_alias_never_opens_outside_file(self):
        accepted = self.fixture("alias")
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "secret.txt").write_text("secret\n", encoding="utf-8")
        research = accepted / "production-books/test/research"
        for path in research.iterdir():
            path.unlink()
        research.rmdir()
        try:
            research.symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            if os.name == "nt" and getattr(exc, "winerror", None) in (50, 1314):
                self.skipTest(f"directory symlinks unavailable: {exc}")
            raise
        original, outside_reads = Path.open, []

        def spy(path, *args, **kwargs):
            if path in (outside, research) or outside in path.parents or research in path.parents:
                outside_reads.append(path)
                raise AssertionError("outside file opened")
            return original(path, *args, **kwargs)

        with mock.patch.object(Path, "open", spy), \
                mock.patch.object(PAIR.PC.loopcfg, "load", side_effect=AssertionError("parsed")):
            with self.assertRaisesRegex(PAIR.PairError, "aliased"):
                PAIR.initialize(accepted, "production-books/test")
        self.assertEqual([], outside_reads)

    def test_hardlinked_config_fails_before_parser(self):
        accepted = self.fixture("hardlink")
        config = accepted / "loop/config.yaml"
        outside = self.root / "outside-config.yaml"
        outside.write_text(config.read_text(), encoding="utf-8")
        config.unlink()
        config.hardlink_to(outside)
        with mock.patch.object(PAIR.PC.loopcfg, "load", side_effect=AssertionError("parsed")):
            with self.assertRaisesRegex(PAIR.PairError, "multiply linked"):
                PAIR.initialize(accepted, "production-books/test")

    @unittest.skipUnless(hasattr(os, "mkfifo"), "os.mkfifo unavailable on this platform")
    def test_special_prompt_fails_before_parser(self):
        accepted = self.fixture("special")
        special = accepted / "prompts/device"
        os.mkfifo(special)
        with mock.patch.object(PAIR.PC.loopcfg, "load", side_effect=AssertionError("parsed")):
            with self.assertRaisesRegex(PAIR.PairError, "special"):
                PAIR.initialize(accepted, "production-books/test")

    def test_store_child_directories_fail_closed_before_sibling_creation(self):
        accepted = self.fixture("store-child")
        store = STORE.state_dir(accepted)
        store.mkdir()
        manifests = store / "manifests"
        manifests.write_text("not a directory\n", encoding="utf-8")
        with self.assertRaisesRegex(STORE.StoreError, "not a directory"):
            STORE.materialize(accepted, "0" * 64, [], [], self.root, self.root)
        self.assertFalse((store / "generations").exists())

    def test_aliased_store_child_fails_before_other_child_creation(self):
        accepted = self.fixture("store-child-alias")
        store = STORE.state_dir(accepted)
        store.mkdir()
        outside = self.root / "outside-generations"
        outside.mkdir()
        try:
            (store / "generations").symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"directory symlinks unavailable: {exc}")
        with self.assertRaisesRegex(STORE.StoreError, "aliased"):
            STORE.materialize(accepted, "0" * 64, [], [], self.root, self.root)
        self.assertFalse((store / "manifests").exists())


if __name__ == "__main__":
    unittest.main()
