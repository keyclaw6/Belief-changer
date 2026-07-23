"""Offline durability and route-binding checks for H-F01 Carr calls."""
import hashlib, json, os, re, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "scripts/loop"), str(ROOT / "scripts/eval")]
import hf01_carr as CARR  # noqa: E402
import hf01_preflight as HF  # noqa: E402
import judges  # noqa: E402

PAIR = "a" * 64
LABELS = ("chapter-1", "chapter-2", "chapter-3")

class CarrNativeTests(unittest.TestCase):
    @staticmethod
    def _replace(source, target):
        target = Path(target)
        if target.exists() and not target.is_symlink(): target.chmod(0o644)
        os.replace(source, target)
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name); tasks = self.root / "evidence/iterations"
        self.root_patch = mock.patch.object(HF, "AUTHORIZED_ROOT", self.root)
        self.root_patch.start(); self.addCleanup(self.root_patch.stop)
        self.sync_patch = mock.patch.object(CARR.PS, "_sync", return_value=None)
        self.sync_patch.start(); self.addCleanup(self.sync_patch.stop)
        self.replace_patch = mock.patch.object(CARR.PS, "_replace_file", side_effect=self._replace)
        self.replace_patch.start(); self.addCleanup(self.replace_patch.stop)
        self.cfg = {"tasks_dir": str(tasks), "judge_k": 2, "judge_model": "gpt-5.6-sol",
                    "judge_route": "codex-native", "judge_reasoning": "xhigh"}
        base = judges.judging_dir(self.cfg, "001")
        (base / "tasks").mkdir(parents=True); (base / "verdicts").mkdir()
        for stem in judges._stems(LABELS, 2):
            body = f"strict Carr comparison {stem}\n"
            digest = hashlib.sha256(body.encode()).hexdigest()
            (base / "tasks" / f"{stem}.md").write_text(
                f"RF-02 SEALED BINDING — return top-level JSON fields pair_hash={PAIR} "
                f"and task_hash={digest} unchanged.\n\n{body}", encoding="utf-8")
        self.blind = {"frozen_at_utc": "2000-01-01T00:00:00+00:00",
                      "authority_sha256": "b" * 64}
        self.calls = []
    def complete(self, content, actor, _schema, model, reasoning):
        match = re.search(r"pair_hash=([0-9a-f]{64}).*task_hash=([0-9a-f]{64})", content)
        pair_hash, task_hash = match.groups()
        value = {"pair_hash": pair_hash, "task_hash": task_hash,
            "scores": {name: 7 for name in judges.DIMS},
            "evidence": {name: f"evidence for {name}" for name in judges.DIMS},
            "worst_dimension": judges.DIMS[0], "gap_summary": "one bounded craft gap",
            "suggestions": [{"suggestion": f"mechanical change {n}", "owner": "prose"}
                            for n in range(3)]}
        self.calls.append(actor)
        transport = {"thread_id": f"thread-{actor}", "model": model,
            "reasoning_effort": reasoning, "command": CARR.NATIVE.command(
                "<isolated-tmp>", "<isolated-tmp>/judge-output-schema.json", model, reasoning)}
        return json.dumps(value), transport, None
    def test_six_calls_are_durable_fresh_and_exactly_route_bound(self):
        receipt = CARR.dispatch(self.root, self.cfg, LABELS, "001", PAIR,
                                self.blind, complete=self.complete)
        self.assertEqual((6, 6), (len(self.calls), len(set(self.calls))))
        self.assertEqual(receipt, CARR.verify(
            self.root, self.cfg, LABELS, "001", PAIR, self.blind))
        self.assertEqual(6, len(receipt["calls"]))
        first = self.root / CARR.FOLDER / "calls/chapter-1-j1.json"
        original = first.read_bytes()
        value = json.loads(first.read_text()); value["command"] = ["wrong"]
        first.chmod(0o644); first.write_text(json.dumps(value)); first.chmod(0o444)
        with self.assertRaisesRegex(CARR.CarrError, "binding is stale"):
            CARR.verify(self.root, self.cfg, LABELS, "001", PAIR, self.blind)
        first.chmod(0o644); first.write_bytes(original); first.chmod(0o444)
        first.chmod(0o644); first.unlink()
        with self.assertRaisesRegex(CARR.CarrError, "ambiguous; do not replay"):
            CARR.verify(self.root, self.cfg, LABELS, "001", PAIR, self.blind)

if __name__ == "__main__": unittest.main()
