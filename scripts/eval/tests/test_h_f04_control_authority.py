"""RF-12 regressions for receipt-bound canonical H-F04 controls."""
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parents[1]))
import h_f04_controls as H  # noqa: E402
import judge_panel as J  # noqa: E402
import native_judge as N  # noqa: E402


def configuration():
    prompts = {role: f"fixed {role}" for role in J.ROLE_SPECS}
    schemas = {role: N.role_output_schema(spec) for role, spec in J.ROLE_SPECS.items()}
    return N.instrument_configuration(
        prompts, schemas, [(1, 1), (2, 2), (3, 3)], N.DEFAULT_IDENTITIES)


def summary(config, mode):
    return {
        "protocol": "stage-a-v2.3", "canonical": True, "panel_complete": True,
        "raw_judgments": 20, "invalid_judgments": 0,
        "collapsed_observations": 5, "matrix": {"passed": True},
        "instrument_configuration": config,
        "prompt_control": {
            "mode": mode, "passed": True, "matrix_transport_valid": True,
            "semantic_expectation_met": True, "instrument_configuration": config,
        },
    }


def base_layout(base):
    for name in ("anonymous-a", "anonymous-b", "outputs"):
        (base / name).mkdir(parents=True, exist_ok=True)


def write_control(base, config, mode):
    output = base / "outputs" / mode
    output.mkdir()
    N.write_summary(output / "judge-summary.json", summary(config, mode))


class CanonicalControlAuthorityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        self.base = self.repo / "calibration" / "h-f04"
        self.patch = mock.patch.object(H, "ROOT", self.repo)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.config = configuration()
        base_layout(self.base)

    def complete(self):
        for mode in H.MODES:
            write_control(self.base, self.config, mode)
        return H.finalize(self.config)

    def test_finalizer_waits_for_both_then_atomically_binds_exact_authority(self):
        """OpenSpec scenario: H-F04 calibrates on a reference-as-candidate."""
        write_control(self.base, self.config, "identical")
        self.assertIsNone(H.finalize(self.config))
        self.assertFalse((self.base / H.RECEIPT).exists())
        write_control(self.base, self.config, "degraded-reference")
        evidence = H.finalize(self.config)

        receipt_path = self.base / H.RECEIPT
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        self.assertEqual(receipt["schema"], 2)
        self.assertEqual(list(evidence), list(H.MODES))
        self.assertEqual(stat.S_IMODE(receipt_path.stat().st_mode), 0o444)
        self.assertEqual(receipt["instrument_configuration"], self.config)
        self.assertEqual(receipt["replica_identities"], list(N.DEFAULT_IDENTITIES))
        self.assertEqual([item["mode"] for item in receipt["controls"]], list(H.MODES))
        self.assertEqual([item["path"] for item in receipt["controls"]], [
            f"outputs/{mode}/judge-summary.json" for mode in H.MODES])
        for item, path in zip(receipt["controls"], H.summaries()):
            info = path.stat()
            self.assertEqual((item["st_dev"], item["st_ino"], item["st_nlink"]),
                             (info.st_dev, info.st_ino, info.st_nlink))
        self.assertFalse(any(path.name.endswith("rf02-tmp")
                             for path in self.base.iterdir()))
        self.assertEqual(N.validate_controls("", self.config), evidence)
        self.assertEqual(N.validate_controls(H.canonical_argument(), self.config), evidence)

    def test_external_swapped_extra_and_synthetic_cli_pairs_fail_before_reads(self):
        """Infra: product callers cannot nominate or reorder control evidence."""
        bad = (
            "/etc/passwd,/etc/hosts", "/tmp/identical.json,/tmp/degraded.json",
            ",".join(reversed(H.canonical_argument().split(","))),
            H.canonical_argument() + ",/tmp/extra.json",
            H.canonical_argument().replace(str(self.repo), str(self.repo / "escape/..")),
        )
        with mock.patch.object(H, "_preflight") as preflight:
            for raw in bad:
                with self.subTest(raw=raw), self.assertRaisesRegex(
                        ValueError, "exact canonical ordered"):
                    H.require(self.config, raw)
        preflight.assert_not_called()

    def test_missing_extra_wrong_mode_alias_stale_and_tamper_fail_closed(self):
        """Infra: only the immutable receipt-bound pair is product authority."""
        mutations = {
            "missing": lambda: (self.base / H.RECEIPT).unlink(),
            "extra": lambda: (self.base / "outputs" / "extra").mkdir(),
            "wrong-mode": lambda: (self.base / H.RECEIPT).chmod(0o644),
            "symlink": self._symlink_summary,
            "hardlink": self._hardlink_summary,
            "swapped": self._swap_summaries,
            "tampered": self._tamper_summary,
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                self._reset()
                mutate()
                with self.assertRaises(ValueError):
                    N.validate_controls("", self.config)
        self._reset()
        changed = dict(self.config)
        changed["reasoning_effort"] = "high"
        with self.assertRaisesRegex(ValueError, "stale"):
            N.validate_controls("", changed)

    def test_descriptor_read_rejects_a_post_inspection_inode_swap(self):
        """Infra: path validation cannot be raced into reading replacement bytes."""
        self.complete()
        path = H.summaries()[0]
        expected = H._inspect(path, self.base)
        replacement = self.base / "replacement.json"
        replacement.write_bytes(path.read_bytes())
        replacement.chmod(0o444)
        os.replace(replacement, path)
        with self.assertRaisesRegex(ValueError, "changed during read"):
            H._read_stable(path, expected)

    def test_receipt_rejects_byte_identical_atomic_summary_replacement(self):
        """Infra: unchanged bytes cannot replace the finalized control identity."""
        self.complete()
        path = H.summaries()[0]
        old_identity = (path.stat().st_dev, path.stat().st_ino)
        replacement = path.with_name("replacement.json")
        replacement.write_bytes(path.read_bytes())
        replacement.chmod(0o444)
        os.replace(replacement, path)
        self.assertNotEqual(old_identity, (path.stat().st_dev, path.stat().st_ino))
        with self.assertRaisesRegex(ValueError, "identity does not match"):
            N.validate_controls("", self.config)

    def test_second_control_preflight_validates_existing_authority(self):
        """Infra: an unsafe first control blocks the second before dispatch."""
        write_control(self.base, self.config, "identical")
        H.control_layout("degraded-reference", self.config)
        existing = H.summaries()[0]
        existing.chmod(0o644)
        with self.assertRaisesRegex(ValueError, "wrong mode"):
            H.control_layout("degraded-reference", self.config)

    def _reset(self):
        for path in sorted(self.base.rglob("*"), reverse=True):
            path.chmod(0o755 if path.is_dir() else 0o644) if not path.is_symlink() else None
            path.unlink() if path.is_file() or path.is_symlink() else path.rmdir()
        base_layout(self.base)
        self.complete()

    def _symlink_summary(self):
        path = H.summaries()[0]
        outside = self.repo / "outside.json"
        outside.write_bytes(path.read_bytes())
        path.unlink()
        path.symlink_to(outside)

    def _hardlink_summary(self):
        path = H.summaries()[0]
        outside = self.repo / "outside.json"
        outside.write_bytes(path.read_bytes())
        path.unlink()
        os.link(outside, path)

    def _swap_summaries(self):
        first, second = H.summaries()
        temporary = self.base / "swap.json"
        os.replace(first, temporary)
        os.replace(second, first)
        os.replace(temporary, second)

    def _tamper_summary(self):
        path = H.summaries()[0]
        value = json.loads(path.read_text(encoding="utf-8"))
        value["canonical"] = False
        path.chmod(0o644)
        path.write_bytes(H.PS.json_bytes(value))
        path.chmod(0o444)


if __name__ == "__main__":
    unittest.main()
