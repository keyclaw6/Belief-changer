"""RF-17/RF-18 semantic decision-table regressions."""
import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
import product_decision as DECISION  # noqa: E402

TESTED, PROMPT = "a" * 64, "b" * 64


def core(**changes):
    checks = {
        "originality": {"tripped": False},
        "near_copy": [{"ratio": 0.1, "tripwire": 0.5}],
        "mantra": {"failures": []}, "length": [{"ok": True}],
        "repetition_within": {"hard_fails": []},
    }
    checks.update(changes)
    return {"checks": checks}


def verdict(prefix, index, vote="PASS", family="openai", kind="model",
            actor=None, base=None, input_hash=None):
    row = {
        "raw_verdict_id": f"raw-{prefix}-{index}",
        "actor": actor or f"judge-{prefix}-{index}", "kind": kind,
        "family": family if kind == "model" else None, "verdict": vote,
        "scope": "ordinary_product", "promotion_eligible": True,
        "base_task_sha256": base or DECISION.PS.state_hash(prefix),
        "tested_pair_hash": TESTED, "prompt_sha256": PROMPT,
        "input_sha256": input_hash or DECISION.PS.state_hash(f"input-{prefix}"),
    }
    row["task_id"] = DECISION.bound_task_id(row)
    return row


def pair(prefix, votes=("PASS", "PASS")):
    return [verdict(prefix, 1, votes[0], "openai"),
            verdict(prefix, 2, votes[1], "anthropic")]


def decide(**changes):
    values = {
        "core": core(), "grounded_review": {"state": "PASSED"},
        "developmental_review": {"state": "PASS"},
        "chapter_effect": pair("effect"),
        "whole_opening_sequence": pair("sequence"),
        "carr_craft": {"reward": 10, "diagnosis": "craft evidence only"},
        "tested_pair_hash": TESTED, "prompt_sha256": PROMPT,
    }
    values.update(changes)
    return DECISION.decide(**values)


class ProductDecisionTests(unittest.TestCase):
    def test_four_layers_stay_separate_without_a_master_reward(self):
        """OpenSpec scenario: Likeness improves without reader effect."""
        result = decide(chapter_effect=pair("effect", ("FAIL", "FAIL")),
                        carr_craft={"reward": 10, "verdict": "excellent"})
        self.assertEqual("REJECT", result["decision"])
        self.assertEqual({"integrity_hard_gate", "blind_chapter_effect",
                          "blind_whole_opening_sequence", "carr_craft_diagnostic"},
                         set(result["layers"]))
        self.assertEqual("DIAGNOSTIC_ONLY",
                         result["layers"]["carr_craft_diagnostic"]["role"])
        self.assertNotIn("reward", result)

    def test_recomputed_integrity_failures_are_non_overridable(self):
        """OpenSpec scenario: A candidate is too close to the matched reference."""
        failures = {
            "originality_pass": {"originality": {"tripped": True}},
            "near_copy_pass": {"near_copy": [{"ratio": 0.8, "tripwire": 0.5}]},
            "exact_mantra_pass": {"mantra": {"failures": ["missing"]}},
            "loose_length_pass": {"length": [{"ok": False}]},
        }
        for field, changes in failures.items():
            with self.subTest(field=field):
                result = decide(core=core(**changes))
                self.assertEqual("REJECT", result["decision"])
                self.assertIn(field, result["layers"]["integrity_hard_gate"]["failures"])
        with self.assertRaisesRegex(DECISION.ProductDecisionError, "receipts required"):
            decide(grounded_review={"state": "BLOCKED"})

    def test_repetition_is_repair_only_and_old_reward_cannot_override_effect(self):
        """OpenSpec requirement: Separated product evidence."""
        repeated = core(repetition_within={"hard_fails": [{"text": "echo"}]})
        result = decide(core=repeated)
        self.assertEqual("PROMOTE", result["decision"])
        self.assertEqual(["non_mantra_repetition"],
                         result["layers"]["integrity_hard_gate"]["repair_signals"])
        rejected = decide(chapter_effect=pair("effect", ("FAIL", "FAIL")),
                          carr_craft={"reward": 999})
        self.assertEqual("REJECT", rejected["decision"])

    def test_material_disagreement_is_inconclusive(self):
        """OpenSpec scenario: Evaluator disagreement is too large."""
        result = decide(chapter_effect=pair("effect", ("PASS", "FAIL")))
        self.assertEqual("INCONCLUSIVE", result["decision"])

    def test_two_families_or_one_model_plus_named_human_are_valid(self):
        """OpenSpec requirement: Blind and independent judgment."""
        self.assertEqual("two_model_families",
                         DECISION.aggregate_pair(pair("models"))["panel"])
        human = [verdict("mixed", 1), verdict(
            "mixed", 2, kind="human", actor="Founder Kristian")]
        self.assertEqual("model_plus_named_human",
                         DECISION.aggregate_pair(human)["panel"])

    def test_independence_and_task_pair_binding_fail_closed(self):
        """OpenSpec requirement: Blind and independent judgment."""
        cases = []
        for field in ("task_id", "raw_verdict_id"):
            rows = pair(field)
            rows[1][field] = rows[0][field]
            cases.append(rows)
        same_family = pair("family")
        same_family[1]["family"] = same_family[0]["family"]
        unrelated = pair("unrelated")
        unrelated[1]["base_task_sha256"] = "c" * 64
        unrelated[1]["task_id"] = DECISION.bound_task_id(unrelated[1])
        cases.extend((same_family, unrelated))
        for rows in cases:
            with self.subTest(rows=rows), self.assertRaises(
                    DECISION.ProductDecisionError):
                DECISION.aggregate_pair(rows)
        reused = pair("effect")
        with self.assertRaisesRegex(DECISION.ProductDecisionError, "reuse"):
            decide(whole_opening_sequence=reused)

    def test_calibration_rows_and_stale_rubric_are_rejected(self):
        row = verdict("scope", 1)
        row.update(scope="h_f04_calibration", promotion_eligible=False,
                   tested_pair_hash=None)
        with self.assertRaisesRegex(DECISION.ProductDecisionError, "calibration"):
            DECISION.aggregate_pair([row, copy.deepcopy(row)])
        with self.assertRaisesRegex(DECISION.ProductDecisionError, "stale"):
            DECISION.aggregate_pair(pair("stale"), prompt_sha256="c" * 64)

    def test_owner_vocabulary_covers_the_complete_factory(self):
        self.assertEqual(("brief", "research/synthesis", "framing", "plan",
                          "commission/context", "prose", "revision", "evaluation"),
                         DECISION.OWNERS)

    def test_hf01_recomputes_position_swapped_gsbs_five_of_six_and_two_of_two(self):
        control, treatment, gsbs = "c" * 64, "d" * 64, "e" * 64
        experiment = DECISION.PS.state_hash({"control_pair_hash": control,
            "treatment_pair_hash": treatment, "gsbs_sha256": gsbs})
        panel_hashes = [DECISION.PS.state_hash(f"gsbs-{n}") for n in range(4)]
        def panel(name, votes, gsbs_hash):
            rows = []
            for index, (actor, candidate, vote) in enumerate(zip(
                    DECISION.HF01_READERS, ("B", "A"), votes), 1):
                row = verdict(name, index, vote, actor=actor,
                    base=DECISION.PS.state_hash(f"{name}-task-{index}"),
                    input_hash=DECISION.PS.state_hash(f"{name}-input-{index}"))
                row.update(tested_pair_hash=experiment, reader_identity=actor,
                    treatment_candidate=candidate, gsbs_sha256=gsbs_hash,
                    envelope_sha256=DECISION.PS.state_hash(f"{name}-env-{index}"),
                    raw_record_sha256=DECISION.PS.state_hash(f"{name}-raw-{index}"),
                    authority_sha256="4" * 64,
                    native_call_sha256=DECISION.PS.state_hash(f"{name}-call-{index}"),
                    model="gpt-5.6-sol", route="codex-native", reasoning="xhigh",
                    command=DECISION.HF01_COMMAND)
                row["task_id"] = DECISION.bound_task_id(row); rows.append(row)
            return rows
        human = {"schema": 2, "reviewer": "Founder Kristian", "verdict": "APPROVE",
            "reviewed_at_utc": "2026-07-19T12:00:00+00:00", "control_pair_hash": control,
            "treatment_pair_hash": treatment, "gsbs_sha256": gsbs,
            "blind_receipt_sha256": "f" * 64, "reference_sighted_diagnostic_sha256": "1" * 64,
            "decision_context_sha256": "2" * 64}
        human["receipt_sha256"] = DECISION.PS.sha(DECISION.PS.json_bytes(human))
        common = {"integrity": {"status": "PASS",
                "unsupported_claim_comparison": {"increased": False}},
            "causal_diagnostic": {"role": "DIAGNOSTIC_ONLY", "status": "PASS",
                "task_ids": [DECISION.PS.state_hash(f"absolute-{n}") for n in range(6)]},
            "chapter_panels": [panel("chapter-1", ("PASS", "PASS"), panel_hashes[0]),
                panel("chapter-2", ("PASS", "PASS"), panel_hashes[1]),
                panel("chapter-3", ("PASS", "FAIL"), panel_hashes[2])],
            "whole_opening_panel": panel("opening", ("PASS", "PASS"), panel_hashes[3]),
            "carr_craft": {"role": "diagnostic"},
            "human_approval": human,
            "control_pair_hash": control, "treatment_pair_hash": treatment,
            "gsbs_sha256": gsbs, "gsbs_panel_sha256": panel_hashes,
            "prompt_sha256": PROMPT, "blind_receipt_sha256": "f" * 64,
            "reference_sighted_diagnostic_sha256": "1" * 64,
            "decision_context_sha256": "2" * 64}
        result = DECISION.decide_hf01(**common)
        self.assertEqual(("PROMOTE", 5, 2), (result["decision"],
            result["layers"]["blind_chapter_effect"]["pass_votes"],
            result["layers"]["blind_whole_opening_sequence"]["pass_votes"]))
        self.assertEqual((control, treatment),
                         (result["control_pair_hash"], result["tested_pair_hash"]))
        split = {**common, "whole_opening_panel": panel(
            "split", ("PASS", "FAIL"), panel_hashes[3])}
        self.assertEqual("INCONCLUSIVE", DECISION.decide_hf01(**split)["decision"])
        rejected = {**common, "chapter_panels": [
            panel("low-1", ("PASS", "FAIL"), panel_hashes[0]),
            panel("low-2", ("PASS", "FAIL"), panel_hashes[1]),
            panel("low-3", ("PASS", "FAIL"), panel_hashes[2])]}
        self.assertEqual("REJECT", DECISION.decide_hf01(**rejected)["decision"])
        with self.assertRaisesRegex(DECISION.ProductDecisionError, "treatment/GSBS"):
            DECISION.decide_hf01(**{**common, "control_pair_hash": "0" * 64})


if __name__ == "__main__":
    unittest.main()
