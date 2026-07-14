"""RF-02 recovery preserves valid-looking temps from another operation."""
import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
import candidate_pair as PAIR  # noqa: E402
import gate as GATE  # noqa: E402
import gate_decision as DECISION  # noqa: E402
import pair_store as STORE  # noqa: E402
from scripts.eval.tests import test_pair_recovery as RECOVERY  # noqa: E402
from scripts.eval.tests import test_pair_binding as BINDING  # noqa: E402


class RecoverySemanticTests(unittest.TestCase):
    def setUp(self):
        self.helper = RECOVERY.PairRecoveryTests(
            "test_promotion_requires_canonical_decision_and_exact_history")
        self.helper.setUp()

    def tearDown(self):
        self.helper.tearDown()

    @staticmethod
    def row(tested):
        row = {key: "" for key in GATE.COLUMNS if key != "timestamp_utc"}
        row.update(iter=1, reward=0.5, hard_ok=True, verdict="KEEP",
                   notes="test", tested_pair_hash=tested)
        return row

    def test_semantically_wrong_pair_temp_survives(self):
        """OpenSpec scenario: Promotion is killed at an atomic boundary."""
        _, experiment, _, _, _ = self.helper.fixture("wrong-pair", False)
        manifest = PAIR.load(experiment)
        manifest["state"], manifest["tested_hash"] = "CANDIDATE", None
        manifest.pop("sealed", None)
        target = experiment / PAIR.MANIFEST
        target.chmod(0o644)
        STORE.write_json(target, manifest)
        self.helper.crash(lambda: PAIR.seal(
            experiment, interrupt=lambda step: os.kill(os.getpid(), 9)
            if step == "write-prepared:pair.json" else None))
        temp = experiment / ".pair.json.rf02-tmp"
        wrong = json.loads(temp.read_text(encoding="utf-8"))
        wrong["run"]["iteration_id"] = 2
        wrong["tested_hash"] = PAIR._identity(wrong)
        temp.write_bytes(STORE.json_bytes(wrong))
        with self.assertRaisesRegex(PAIR.PairError, "do not belong"):
            PAIR.seal(experiment)
        self.assertEqual(STORE.json_bytes(wrong), temp.read_bytes())

    def test_semantically_wrong_gate_and_terminal_temps_survive(self):
        """OpenSpec scenario: Promotion is killed at an atomic boundary."""
        accepted, experiment, _, tested, _ = self.helper.fixture("wrong-gate", False)
        manifest, row = PAIR.load(experiment), self.row(tested)
        history_path = PAIR.evaluation_tree(experiment) / "loop/results.tsv"
        wrong_gate, _ = DECISION.expected(
            manifest, {"receipt_hash": "score-fixture"}, history_path, row,
            GATE.COLUMNS, 0.03, 0.5, "0", "KEEP", True,
            "2026-07-14T12:00:01+00:00")
        gate_temp = experiment / ".gate-decision.json.rf02-tmp"
        gate_temp.write_bytes(STORE.json_bytes(wrong_gate))
        with self.assertRaisesRegex(DECISION.DecisionError, "do not belong"):
            DECISION.ensure(
                experiment, manifest, {"receipt_hash": "score-fixture"}, history_path,
                row, GATE.COLUMNS, 0.03, 0.5, "0", "KEEP", True, RECOVERY.TIMESTAMP)
        self.assertEqual(STORE.json_bytes(wrong_gate), gate_temp.read_bytes())
        gate_temp.unlink()

        receipt, history = DECISION.ensure(
            experiment, manifest, {"receipt_hash": "score-fixture"}, history_path,
            row, GATE.COLUMNS, 0.03, 0.5, "0", "KEEP", True, RECOVERY.TIMESTAMP)
        terminal_temp = experiment / ".decision.json.rf02-tmp"
        terminal_temp.write_bytes(DECISION.terminal_bytes(wrong_gate))
        with self.assertRaisesRegex(PAIR.PairError, "do not belong"):
            PAIR.promote(experiment, accepted, tested, history)
        self.assertEqual(DECISION.terminal_bytes(wrong_gate), terminal_temp.read_bytes())
        self.assertEqual(receipt, DECISION.load(experiment, tested))

    def test_semantically_wrong_pointer_temp_survives(self):
        """OpenSpec scenario: Promotion is killed at an atomic boundary."""
        accepted, experiment, _, tested, decision = self.helper.fixture("wrong-pointer")
        old = STORE.current(accepted)[1]
        PAIR.promote(experiment, accepted, tested, decision[1])
        new = STORE.current(accepted)[1]
        temp = STORE.state_dir(accepted) / ".current.rf02-tmp"
        temp.symlink_to(Path("generations") / old)
        with self.assertRaisesRegex(STORE.StoreError, "invalid"):
            STORE.switch(accepted, new)
        self.assertEqual(Path("generations") / old, Path(os.readlink(temp)))

    def test_gate_replays_exact_gate_and_terminal_temps(self):
        """OpenSpec scenario: Promotion is killed at an atomic boundary."""
        for stage, module, name, event, temp_name in (
                ("gate", GATE.GD, "ensure", "write-prepared:gate-decision.json",
                 ".gate-decision.json.rf02-tmp"),
                ("terminal", GATE.CP, "promote", "write-prepared:decision.json",
                 ".decision.json.rf02-tmp")):
            with self.subTest(stage=stage):
                helper = BINDING.PairBindingTests("test_valid_receipt_promotes_exact_pair")
                helper.setUp()
                try:
                    accepted, experiment, tested, _, core, _, _ = helper.fixture(stage)
                    original = getattr(module, name)

                    def interrupted(*args, **kwargs):
                        kwargs["interrupt"] = lambda step: os.kill(os.getpid(), 9) \
                            if step == event else None
                        return original(*args, **kwargs)

                    self.helper.crash(lambda: self._run_patched(
                        helper, accepted, experiment, tested, core,
                        module, name, interrupted))
                    temp = experiment / temp_name
                    self.assertTrue(temp.is_file())
                    with self.assertRaises(SystemExit) as done:
                        helper.run_gate(accepted, experiment, tested, core)
                    self.assertEqual(0, done.exception.code)
                    self.assertEqual("PROMOTED", PAIR.status(experiment))
                    self.assertFalse(os.path.lexists(temp))
                finally:
                    helper.tearDown()

    @staticmethod
    def _run_patched(helper, accepted, experiment, tested, core,
                     module, name, replacement):
        with mock.patch.object(module, name, side_effect=replacement):
            helper.run_gate(accepted, experiment, tested, core)


if __name__ == "__main__":
    unittest.main()
