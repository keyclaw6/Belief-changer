"""Focused runnable-path tests for RF-16/RF-18 product observations."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/eval"))
sys.path.insert(0, str(ROOT / "scripts/loop"))
import product_effect as EFFECT  # noqa: E402
import product_effect_panel as PANEL  # noqa: E402
import product_decision as DECISION  # noqa: E402

TESTED = "a" * 64


def verdict(task, preferred="A"):
    return {"schema": 1, "task_sha256": task["task_sha256"],
            "mode": task["mode"], "preferred": preferred, "confidence": "MEDIUM",
            "decisive_reason": "The preferred candidate enacts the discovery."}


class ProductEffectPanelTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cfg = {
            "tasks_dir": str(Path(self.tmp.name) / "iterations"),
            "product_effect_rubric": str(Path(self.tmp.name) / "rubric.md"),
            "judge_model": "gpt-5.6-sol", "judge_route": "codex-native",
            "judge_reasoning": "xhigh",
        }
        Path(self.cfg["product_effect_rubric"]).write_bytes(
            (ROOT / "calibration/judges/product-effect-rubric.md").read_bytes())
        self.task = EFFECT.whole_opening(
            "compulsive checking", ["A one.", "A two."],
            ["B one.", "B two."])
        self.envelope = EFFECT.h_f04_envelope(self.task, "B")

    def test_h_f04_requires_envelope_and_dispatches_anonymous_fresh_contexts(self):
        """OpenSpec scenario: H-F04 calibrates on a reference-as-candidate."""
        seen = []

        def complete(content, identity, schema):
            seen.append((content, identity, schema))
            return (json.dumps(verdict(self.task)),
                    {"thread_id": f"thread-{identity}"}, None)

        with self.assertRaises(EFFECT.ContractError):
            PANEL.dispatch(self.cfg, "h-f04", self.task, h_f04=True,
                           complete=complete)
        rows = PANEL.dispatch(self.cfg, "h-f04", self.envelope, h_f04=True,
                              complete=complete)
        summary = PANEL.aggregate(self.cfg, "h-f04", self.envelope, h_f04=True)
        records = PANEL.records(self.cfg, "h-f04", self.envelope, h_f04=True)

        self.assertEqual(2, len(rows))
        self.assertTrue(all("/judging/h-f04/tasks/" in str(row[2]) for row in rows))
        self.assertEqual(2, len({row[1] for row in rows}))
        self.assertEqual("A", summary["status"])
        self.assertFalse(summary["promotion_eligible"])
        self.assertEqual(2, len(set(summary["raw_verdict_ids"])))
        self.assertEqual(EFFECT.output_schema(), seen[0][2])
        for content, _identity, _schema in seen:
            for leak in ("reference_candidate", "promotion_eligible", "h_f04"):
                self.assertNotIn(leak, content)
        task_payload = json.dumps(self.task)
        for leak in ("condition", "provenance", "history", "scores"):
            self.assertNotIn(leak, task_payload)
        with self.assertRaisesRegex(PANEL.PanelError, "cannot enter"):
            PANEL.decision_row(self.cfg, records[0], self.task, "A", TESTED)

    def test_material_repeat_disagreement_is_inconclusive(self):
        """OpenSpec scenario: Evaluator disagreement is too large."""
        def complete(_content, identity, _schema):
            preferred = "A" if identity.endswith("r1") else "B"
            return (json.dumps(verdict(self.task, preferred)),
                    {"thread_id": f"thread-{identity}"}, None)

        PANEL.dispatch(self.cfg, "variance", self.envelope, h_f04=True,
                       complete=complete)
        summary = PANEL.aggregate(self.cfg, "variance", self.envelope, h_f04=True)
        self.assertEqual("INCONCLUSIVE", summary["status"])
        self.assertEqual("two_fresh_native_same_family_repeats", summary["panel"])

    def test_ordinary_task_has_no_reference_envelope_and_maps_one_blind_vote(self):
        """Infra: ordinary paired dispatch remains blind and non-calibration."""
        def complete(_content, identity, _schema):
            return (json.dumps(verdict(self.task)),
                    {"thread_id": f"thread-{identity}"}, None)

        rows = PANEL.dispatch(self.cfg, "product", self.task,
                              tested_pair_hash=TESTED, complete=complete)
        records = PANEL.records(self.cfg, "product", self.task,
                                tested_pair_hash=TESTED)
        mapped = PANEL.decision_row(self.cfg, records[0], self.task, "A", TESTED)
        self.assertTrue(all("/judging/tasks/" in str(row[2]) for row in rows))
        self.assertNotIn("reference_candidate", json.dumps(self.task))
        self.assertEqual("PASS", mapped["verdict"])
        self.assertEqual(records[0]["task_id"], mapped["task_id"])
        self.assertEqual(records[0]["raw_verdict_id"], mapped["raw_verdict_id"])

    def test_hf01_single_reader_dispatch_binds_position_and_gsbs_receipt(self):
        """OpenSpec scenario: Stage A uses position-swapped direct GSBS panels."""
        files = {"calibration/reference/gsbs/chapter-3.txt": "c" * 64}
        cases = (("sol-xhigh-r1", "B", "GSBS", "treatment"),
                 ("sol-xhigh-r2", "A", "treatment", "GSBS"))
        rows = []
        for identity, support, first, second in cases:
            task = EFFECT.chapter_pair("sugar", first, second)
            envelope = EFFECT.h_f01_envelope(task, "b" * 64, files, support, identity)
            def complete(_content, actor, _schema, model, reasoning, preferred=support):
                return (json.dumps(verdict(task, preferred)),
                        {"thread_id": f"thread-{actor}", "model": model,
                         "reasoning_effort": reasoning, "command": PANEL.N.command(
                             "<isolated-tmp>", "<isolated-tmp>/judge-output-schema.json",
                             model, reasoning)}, None)
            PANEL.dispatch(self.cfg, identity, task, identities=(identity,),
                tested_pair_hash=TESTED, complete=complete, single=True)
            record = PANEL.records(self.cfg, identity, task, identities=(identity,),
                                   tested_pair_hash=TESTED, single=True)[0]
            rows.append(PANEL.h_f01_decision_row(self.cfg, record, envelope, TESTED))
        self.assertEqual(("B", "A"), tuple(row["treatment_candidate"] for row in rows))
        self.assertTrue(all(row["verdict"] == "PASS" for row in rows))
        self.assertEqual(2, len({row["raw_record_sha256"] for row in rows}))
        self.assertEqual(EFFECT._hash(files), rows[0]["gsbs_sha256"])
        self.assertEqual({"gpt-5.6-sol"}, {row["model"] for row in rows})

    def test_prompt_correction_changes_call_id_and_rejects_stale_record(self):
        """Infra: paired records bind the current rubric and rendered input."""
        def complete(_content, identity, _schema):
            return (json.dumps(verdict(self.task)),
                    {"thread_id": f"thread-{identity}"}, None)

        old = PANEL.dispatch(self.cfg, "stale", self.task,
                             tested_pair_hash=TESTED, complete=complete)
        rubric = Path(self.cfg["product_effect_rubric"])
        rubric.write_text(rubric.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        new = PANEL.emit(self.cfg, "stale", self.task, tested_pair_hash=TESTED)
        self.assertNotEqual([row[1] for row in old], [row[1] for row in new])
        with self.assertRaisesRegex(PANEL.PanelError, "missing raw verdict"):
            PANEL.records(self.cfg, "stale", self.task, tested_pair_hash=TESTED)

    def test_named_human_and_second_family_use_the_same_validated_flow(self):
        """Infra: paired evidence preserves independent evaluator identities."""
        def complete(_content, identity, _schema):
            return (json.dumps(verdict(self.task)),
                    {"thread_id": f"thread-{identity}"}, None)

        PANEL.dispatch(self.cfg, "external", self.task,
                       tested_pair_hash=TESTED, complete=complete)
        native = PANEL.records(self.cfg, "external", self.task,
                               tested_pair_hash=TESTED)[0]
        model = PANEL.ingest(self.cfg, self.task, TESTED, {
            "raw_verdict_id": "anthropic-thread-1", "actor": "anthropic-r1",
            "kind": "model", "family": "anthropic",
            "raw_verdict": json.dumps(verdict(self.task)),
        })
        human = PANEL.ingest(self.cfg, self.task, TESTED, {
            "raw_verdict_id": "human-form-1", "actor": "Founder Kristian",
            "kind": "human", "family": None,
            "raw_verdict": json.dumps(verdict(self.task)),
        })
        native_row = PANEL.decision_row(self.cfg, native, self.task, "A", TESTED)
        for external, panel in ((model, "two_model_families"),
                                (human, "model_plus_named_human")):
            external_row = PANEL.decision_row(
                self.cfg, external, self.task, "A", TESTED)
            self.assertEqual(panel, DECISION.aggregate_pair(
                [native_row, external_row], tested_pair_hash=TESTED)["panel"])


if __name__ == "__main__":
    unittest.main()
