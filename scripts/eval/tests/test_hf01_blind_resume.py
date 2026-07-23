"""Offline crash-boundary checks for H-F01 blind native calls."""
import json, os, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "scripts/loop"), str(ROOT / "scripts/eval")]
import hf01_blind as BLIND  # noqa: E402
import hf01_carr as CARR  # noqa: E402
import hf01_upstream as UPSTREAM  # noqa: E402
import pair_store as PS  # noqa: E402

AUTHORITY = "a" * 64
PAIR = "b" * 64

class BlindResumeTests(unittest.TestCase):
    @staticmethod
    def _replace(source, target):
        target = Path(target)
        if target.exists() and not target.is_symlink(): target.chmod(0o644)
        os.replace(source, target)
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root_patch = mock.patch.object(BLIND.HF, "AUTHORIZED_ROOT", Path(self.tmp.name))
        self.root_patch.start(); self.addCleanup(self.root_patch.stop)
        self.sync_patch = mock.patch.object(PS, "_sync", return_value=None)
        self.sync_patch.start(); self.addCleanup(self.sync_patch.stop)
        self.replace_patch = mock.patch.object(PS, "_replace_file", side_effect=self._replace)
        self.replace_patch.start(); self.addCleanup(self.replace_patch.stop)
        self.base = BLIND.folder(self.tmp.name)
        task = BLIND.ABS.chapter("sugar", "one treatment chapter")
        self.row = {"key": "treatment-chapter-01", "identity": "hf01-absolute-treatment-01",
            "route": {"model": "gpt-5.6-sol", "route": "codex-native", "reasoning": "xhigh"},
            "envelope": BLIND.ABS.envelope(task, "treatment-chapter-01", PAIR)}
        observation = {field: "CLEAR" for field in BLIND.ABS.RATING_FIELDS}
        observation.update(entering_belief="old belief", leaving_belief="new belief",
            enacted_discovery="felt discovery", construct_sufficiency="MEETS",
            construct_reason="the chapter enacts the change", opening_sequence={
                field: BLIND.ABS.NOT_APPLICABLE for field in BLIND.ABS.SEQUENCE_FIELDS})
        self.raw = json.dumps({"schema": 1, "task_sha256": task["task_sha256"],
            "mode": "chapter", "observation": observation, "confidence": "HIGH"})
        self.prompt, self.calls = b"exact blind prompt", []
    def complete(self, _content, actor, _schema, model, reasoning):
        self.calls.append(actor)
        return self.raw, {"thread_id": f"thread-{actor}", "model": model,
            "reasoning_effort": reasoning, "command": BLIND.NATIVE.command(
                "<isolated-tmp>", "<isolated-tmp>/judge-output-schema.json", model, reasoning)}, None
    def assert_guarded(self, writer, error):
        with tempfile.TemporaryDirectory(dir=self.tmp.name) as temp:
            root, outside = Path(temp) / "evidence", Path(temp) / "outside"
            root.mkdir(); outside.mkdir()
            try: (root / "alias").symlink_to(outside, target_is_directory=True)
            except OSError as exc: self.skipTest(f"symlink privilege unavailable: {exc}")
            with self.assertRaises(error): writer(root / "alias/record.json")
            self.assertFalse((outside / "record.json").exists())
            sentinel = outside / "sentinel.json"; sentinel.write_bytes(b"outside")
            leaf = root / "record.json"; leaf.symlink_to(sentinel)
            with self.assertRaises(error): writer(leaf)
            self.assertEqual(b"outside", sentinel.read_bytes())
    def test_blind_writers_reject_unsafe_evidence_paths(self):
        """Scenario: An operation root contains an unsafe path."""
        for name, writer in (("json", lambda path: BLIND.write(path, {"schema": 1})),
                             ("bytes", lambda path: BLIND._write_bytes(path, b"task"))):
            with self.subTest(name=name): self.assert_guarded(writer, BLIND.BlindError)
    def test_upstream_writer_rejects_unsafe_evidence_paths(self):
        """Scenario: An operation root contains an unsafe path."""
        self.assert_guarded(lambda path: UPSTREAM._write(path, b"upstream"), UPSTREAM.UpstreamError)
    def test_carr_writer_rejects_unsafe_evidence_paths(self):
        """Scenario: An operation root contains an unsafe path."""
        self.assert_guarded(lambda path: CARR._write(path, b"carr"), CARR.CarrError)
    def test_durable_result_materializes_without_replay(self):
        task = BLIND.ABS.judge_task(self.row["envelope"])
        verdict = self.base / "absolute/verdicts/treatment-chapter-01.json"
        call = BLIND._native_call(self.base, self.row["identity"], AUTHORITY,
            task["task_sha256"], self.prompt, self.row["route"], BLIND.ABS.output_schema(),
            verdict, True, self.complete)
        self.assertFalse(verdict.exists()); self.assertEqual(AUTHORITY, call["authority_sha256"])
        record = BLIND._absolute_record(
            self.base, self.row, self.prompt, AUTHORITY, True, self.complete)
        self.assertEqual(1, len(self.calls)); self.assertEqual(AUTHORITY, record["authority_sha256"])
        self.assertEqual(PS.sha(PS.json_bytes(call)), record["native_call_sha256"])
    def test_marker_without_result_stops_ambiguously(self):
        task = BLIND.ABS.judge_task(self.row["envelope"])
        verdict = self.base / "absolute/verdicts/treatment-chapter-01.json"
        def interrupted(*args, **kwargs):
            self.calls.append("interrupted"); raise RuntimeError("injected transport interruption")
        with self.assertRaisesRegex(RuntimeError, "injected"):
            BLIND._native_call(self.base, self.row["identity"], AUTHORITY,
                task["task_sha256"], self.prompt, self.row["route"], BLIND.ABS.output_schema(),
                verdict, True, interrupted)
        with self.assertRaisesRegex(BLIND.BlindError, "ambiguous; do not replay"):
            BLIND._native_call(self.base, self.row["identity"], AUTHORITY,
                task["task_sha256"], self.prompt, self.row["route"], BLIND.ABS.output_schema(),
                verdict, True, interrupted)
        self.assertEqual(["interrupted"], self.calls)
    def test_emit_uses_one_durable_path_for_absolute_and_gsbs_calls(self):
        root = Path(self.tmp.name); paths = BLIND.HF.arm_paths(root)
        for arm in ("control", "treatment"):
            for number in BLIND.HF.CHAPTERS:
                path = paths[arm]["book"] / f"chapters/chapter-{number:02d}.md"
                path.parent.mkdir(parents=True, exist_ok=True); path.write_text(f"{arm} chapter {number}")
        matches, evaluation = [], paths["treatment"]["experiment"] / "evaluation"
        for number, position in zip(BLIND.HF.CHAPTERS, (3, 4, 5)):
            relative = f"calibration/reference/gsbs/chapter-{position}.txt"; path = evaluation / relative
            path.parent.mkdir(parents=True, exist_ok=True); path.write_text(f"GSBS chapter {position}")
            matches.append({"treatment_chapter": number, "reference_position": position,
                            "path": relative, "sha256": PS.sha(path.read_bytes())})
        absolute_rubric, paired_rubric = root / "absolute.md", root / "paired.md"
        absolute_rubric.write_text("absolute {{TASK}}")
        paired_rubric.write_text("paired {{TASK}}")
        cfg = {"tasks_dir": str(root / "iterations"),
            "product_effect_absolute_rubric": str(absolute_rubric),
            "product_effect_rubric": str(paired_rubric), "judge_model": "gpt-5.6-sol",
            "judge_route": "codex-native", "judge_reasoning": "xhigh",
            "scores_dir": str(root / "scores")}
        authority = {"identity": {"gsbs_matches": matches, "gsbs_sha256": PS.state_hash(matches)},
            "route": {"judge_model": "gpt-5.6-sol", "judge_route": "codex-native",
                      "judge_reasoning": "xhigh"}, "next_command": "resume-hf01"}
        bundle = BLIND.bundle(root, {"control": "e" * 64, "treatment": PAIR},
            {"status": "PASS"}, authority, "f" * 64)
        calls = []
        def complete(content, actor, _schema, model, reasoning):
            kind, payload = content.split(" ", 1); task = json.loads(payload); calls.append(actor)
            if kind == "absolute":
                observation = {field: "CLEAR" for field in BLIND.ABS.RATING_FIELDS}
                observation.update(entering_belief=f"enter {task['task_sha256'][:8]}",
                    leaving_belief=f"leave {task['task_sha256'][:8]}", enacted_discovery=f"discover {task['task_sha256'][:8]}",
                    construct_sufficiency="MEETS", construct_reason="belief changed", opening_sequence={
                        field: BLIND.ABS.NOT_APPLICABLE for field in BLIND.ABS.SEQUENCE_FIELDS})
                raw = json.dumps({"schema": 1, "task_sha256": task["task_sha256"],
                    "mode": task["mode"], "observation": observation, "confidence": "HIGH"})
            else:
                raw = json.dumps({"schema": 1, "task_sha256": task["task_sha256"], "mode": task["mode"],
                    "preferred": "A", "confidence": "HIGH", "decisive_reason": "belief changed"})
            return raw, {"thread_id": f"thread-{len(calls)}", "model": model,
                "reasoning_effort": reasoning, "command": BLIND.NATIVE.command(
                    "<isolated-tmp>", "<isolated-tmp>/judge-output-schema.json", model, reasoning)}, None
        view = {"config": cfg}
        with mock.patch.object(BLIND.CP, "open_sealed", return_value=view):
            self.assertEqual(view, BLIND.emit(root, bundle, authority, True, complete))
            self.assertEqual(view, BLIND.emit(root, bundle, authority, True, complete))
        receipt = BLIND.freeze(root, bundle, view, "999")
        self.assertEqual(14, len(calls)); self.assertEqual(bundle["authority_sha256"], receipt["authority_sha256"])
        records = [BLIND.read(path) for path in sorted((self.base / "native/calls").glob("*.json"))]
        self.assertEqual((14, {bundle["authority_sha256"]}),
                         (len(records), {row["authority_sha256"] for row in records}))

if __name__ == "__main__": unittest.main()
