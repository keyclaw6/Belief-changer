"""RF-12 product-judge and isolated H-F04 preflight regressions."""
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
sys.path.insert(0, str(ROOT / "scripts/eval"))
sys.path.insert(0, str(ROOT / "scripts/eval/tests"))
import candidate_pair as PAIR  # noqa: E402
import grounded_review_call as CALL  # noqa: E402
import judge_panel as PANEL  # noqa: E402
import judge_scope as SCOPE  # noqa: E402
from grounded_review_fixture import GroundedFixture, pass_review  # noqa: E402


def args(**updates):
    values = {"candidate_root": "", "tested_pair_hash": "", "h_f04_root": "",
              "control": "", "chapters": "1-3", "pairs": "", "ours": "",
              "ref": "", "out": ""}
    return SimpleNamespace(**{**values, **updates})


def control_summary(configuration, mode):
    return {
        "protocol": "stage-a-v2.3", "canonical": True, "panel_complete": True,
        "raw_judgments": 20, "invalid_judgments": 0,
        "collapsed_observations": 5, "matrix": {"passed": True},
        "instrument_configuration": configuration,
        "prompt_control": {
            "mode": mode, "passed": True, "matrix_transport_valid": True,
            "semantic_expectation_met": True,
            "instrument_configuration": configuration,
        },
    }


class GroundedJudgeScopeTests(GroundedFixture, unittest.TestCase):
    def test_product_scope_requires_exact_sealed_grounded_identity_and_paths(self):
        """OpenSpec scenario: A grounded blocker remains."""
        candidate = self.frozen("judge-product")
        pass_review(candidate)
        tested = PAIR.seal(candidate)
        manifest = PAIR.load(candidate)
        exact = args(
            candidate_root=str(candidate), tested_pair_hash=tested, chapters="1-2",
            ours=str(PAIR.candidate_tree(candidate) / manifest["run"]["book"] / "chapters"),
            ref=str(PAIR.evaluation_tree(candidate) / "calibration/reference/book"),
            out=str(PAIR.evidence_tree(candidate) / "product-judge"))
        self.assertEqual("product", SCOPE.guard(exact)["mode"])
        for key, value in (("tested_pair_hash", "0" * 64), ("chapters", "1"),
                           ("ours", str(candidate)), ("ref", str(candidate)),
                           ("out", str(candidate / "other"))):
            with self.subTest(key=key), self.assertRaises(SCOPE.ScopeError):
                SCOPE.guard(args(**{**vars(exact), key: value}))

        raw = CALL.raw_path(candidate, 1)
        raw.chmod(0o644)
        raw.write_text(raw.read_text().replace('"PASS"', '"BLOCK"'))
        raw.chmod(0o444)
        with self.assertRaisesRegex(SCOPE.ScopeError, "grounded|transport"):
            SCOPE.guard(exact)

    def test_unpinned_product_cli_fails_before_reads_writes_or_native_callback(self):
        """OpenSpec scenario: A grounded blocker remains."""
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "output"
            argv = ["judge_panel.py", "--ours", "ours", "--ref", "ref",
                    "--out", str(out)]
            with (mock.patch.object(sys, "argv", argv),
                  mock.patch.object(PANEL.E, "load_chapters") as load,
                  mock.patch.object(PANEL.N, "complete") as native,
                  mock.patch.object(PANEL.Path, "mkdir") as mkdir,
                  mock.patch("sys.stderr")):
                with self.assertRaises(SystemExit):
                    PANEL.main()
            load.assert_not_called()
            native.assert_not_called()
            mkdir.assert_not_called()
            self.assertFalse(out.exists())

    def test_external_and_synthetic_control_paths_have_zero_product_side_effects(self):
        """OpenSpec scenario: A grounded blocker remains."""
        with tempfile.TemporaryDirectory() as tmp:
            paths = [Path(tmp) / f"{mode}.json" for mode in ("identical", "degraded")]
            for path in paths:
                path.write_text('{"passed": true}', encoding="utf-8")
            for raw in ("/etc/passwd,/etc/hosts", ",".join(map(str, paths))):
                out = Path(tmp) / "output"
                argv = ["judge_panel.py", "--ours", "ours", "--ref", "ref",
                        "--validated-controls", raw, "--out", str(out)]
                with self.subTest(raw=raw), mock.patch.object(sys, "argv", argv), \
                        mock.patch.object(PANEL.SCOPE, "guard") as guard, \
                        mock.patch.object(PANEL.E, "load_chapters") as load, \
                        mock.patch.object(PANEL.N, "complete") as native, \
                        mock.patch.object(PANEL.Path, "mkdir") as mkdir, \
                        mock.patch("sys.stderr"):
                    with self.assertRaises(SystemExit):
                        PANEL.main()
                    guard.assert_not_called()
                    load.assert_not_called()
                    native.assert_not_called()
                    mkdir.assert_not_called()
                    self.assertFalse(out.exists())

    def test_receipt_bound_inode_replacement_has_zero_product_side_effects(self):
        """OpenSpec scenario: A grounded blocker remains."""
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(SCOPE.HF, "ROOT", Path(tmp)):
            base = Path(tmp) / "calibration/h-f04"
            for name in ("anonymous-a", "anonymous-b", "outputs"):
                (base / name).mkdir(parents=True, exist_ok=True)
            prompts = {role: (PANEL.JUDGE_DIR / spec["prompt"]).read_text(encoding="utf-8")
                       for role, spec in PANEL.ROLE_SPECS.items()}
            schemas = {role: PANEL.N.role_output_schema(spec)
                       for role, spec in PANEL.ROLE_SPECS.items()}
            configuration = PANEL.N.instrument_configuration(
                prompts, schemas, [(1, 1), (2, 2), (3, 3)], PANEL.N.DEFAULT_IDENTITIES)
            for mode in SCOPE.HF.MODES:
                folder = base / "outputs" / mode
                folder.mkdir()
                PANEL.N.write_summary(
                    folder / "judge-summary.json", control_summary(configuration, mode))
            SCOPE.HF.finalize(configuration)
            receipt = base / SCOPE.HF.RECEIPT
            receipt_before = (receipt.read_bytes(), receipt.stat().st_dev, receipt.stat().st_ino)
            summary = SCOPE.HF.summaries()[0]
            replacement = summary.with_name("replacement.json")
            replacement.write_bytes(summary.read_bytes())
            replacement.chmod(0o444)
            summary.chmod(0o644)
            replacement.replace(summary)

            reads, stable = [], SCOPE.HF._read_stable
            out = Path(tmp) / "product-output"
            argv = ["judge_panel.py", "--ours", "ours", "--ref", "ref",
                    "--out", str(out)]
            def read(path, identity):
                reads.append(Path(path))
                return stable(path, identity)
            with mock.patch.object(sys, "argv", argv), \
                    mock.patch.object(SCOPE.HF, "_read_stable", side_effect=read), \
                    mock.patch.object(PANEL.SCOPE, "guard") as guard, \
                    mock.patch.object(PANEL.E, "load_chapters") as load, \
                    mock.patch.object(PANEL.N, "complete") as native, \
                    mock.patch.object(PANEL.Path, "mkdir") as mkdir, \
                    mock.patch("sys.stderr"):
                with self.assertRaises(SystemExit):
                    PANEL.main()
            self.assertEqual(reads, [base / SCOPE.HF.RECEIPT])
            guard.assert_not_called()
            load.assert_not_called()
            native.assert_not_called()
            mkdir.assert_not_called()
            self.assertFalse(out.exists())
            self.assertEqual(receipt_before,
                             (receipt.read_bytes(), receipt.stat().st_dev, receipt.stat().st_ino))

    def test_stale_or_tampered_product_identity_has_zero_judge_side_effects(self):
        """OpenSpec scenario: A grounded blocker remains."""
        candidate = self.frozen("judge-stale")
        pass_review(candidate)
        tested = PAIR.seal(candidate)
        manifest = PAIR.load(candidate)
        ours = PAIR.candidate_tree(candidate) / manifest["run"]["book"] / "chapters"
        ref = PAIR.evaluation_tree(candidate) / "calibration/reference/book"
        out = PAIR.evidence_tree(candidate) / "product-judge"
        base = ["judge_panel.py", "--ours", str(ours), "--ref", str(ref),
                "--chapters", "1-2", "--out", str(out), "--candidate-root",
                str(candidate), "--tested-pair-hash"]
        for name, identity in (("stale", "0" * 64), ("tampered", tested)):
            if name == "tampered":
                raw = CALL.raw_path(candidate, 1)
                raw.chmod(0o644)
                raw.write_text(raw.read_text().replace('"PASS"', '"BLOCK"'))
                raw.chmod(0o444)
            with self.subTest(name=name), mock.patch.object(sys, "argv", base + [identity]), \
                    mock.patch.object(PANEL.E, "load_chapters") as load, \
                    mock.patch.object(PANEL.N, "complete") as native, \
                    mock.patch.object(PANEL.Path, "mkdir") as mkdir, \
                    mock.patch("sys.stderr"):
                with self.assertRaises(SystemExit):
                    PANEL.main()
                load.assert_not_called()
                native.assert_not_called()
                mkdir.assert_not_called()
                self.assertFalse(out.exists())

    def test_only_exact_anonymous_h_f04_control_layout_bypasses_product_identity(self):
        """OpenSpec scenario: H-F04 calibrates on a reference-as-candidate."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "calibration/h-f04"
            ours, ref, outputs = root / "anonymous-a", root / "anonymous-b", root / "outputs"
            ours.mkdir(parents=True)
            ref.mkdir()
            outputs.mkdir()
            exact = args(h_f04_root=str(root), control="identical", ours=str(ours),
                         ref=str(ref), out=str(outputs / "identical"))
            with mock.patch.object(SCOPE, "ROOT", Path(tmp)), \
                    mock.patch.object(SCOPE.HF, "ROOT", Path(tmp)):
                self.assertEqual("h-f04-control", SCOPE.guard(exact)["mode"])
                for key, value in (("out", str(root / "leak")), ("ours", str(ref)),
                                   ("chapters", "1-2"), ("candidate_root", str(root))):
                    with self.subTest(key=key), self.assertRaises(SCOPE.ScopeError):
                        SCOPE.guard(args(**{**vars(exact), key: value}))
                with self.assertRaises(SCOPE.ScopeError):
                    SCOPE.guard(exact, legacy=True)


if __name__ == "__main__":
    unittest.main()
