"""Offline repair-path tests for the cross-iteration no-regression gate."""
from __future__ import annotations
import copy
from pathlib import Path
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SOURCE / "scripts"))

from bc_factory.common import FactoryError, digest
from bc_factory.demo import accepted, finish, inputs, metadata, scaffold
from bc_factory.learning import advance, load_next, research_guidance, seed
from bc_factory.regression import decide, submit, task
from bc_factory.runs import Run, prepare
from bc_factory.schema import DIMENSIONS


class NoRegressionRepairTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        scaffold(SOURCE, self.repo)
        self.brief, self.research, self.plan = inputs()
        prepare(self.repo, "baseline", self.brief, self.research, fixture=True)
        base = Run(self.repo, "baseline")
        finish(base, self.plan)
        lessons = {"schema_version": 2, "subject": self.brief["subject"],
                   "preserve": [{"dimension": "argument", "instruction": "Preserve bounded reasoning.",
                                 "evidence": "Prior comparison."}],
                   "improve": [],
                   "recurring_repairs": [], "research_gaps": [], "note": "Fixture bootstrap."}
        seed(self.repo, "baseline", lessons)
        packet = load_next(base)
        guidance = research_guidance(packet, self.brief)
        research = copy.deepcopy(self.research)
        research["learning_context"] = {"guidance_sha256": guidance["guidance_sha256"], "baseline_run": "baseline",
                                        "gap_resolutions": []}
        prepare(self.repo, "candidate", self.brief, research, fixture=True, learning_from="baseline")
        self.candidate = Run(self.repo, "candidate")
        finish(self.candidate, self.plan)

    def tearDown(self):
        self.tmp.cleanup()

    @staticmethod
    def judgment(judge_task, voice_winner):
        quote = "One unsuccessful attempt is one observation."
        return {"schema_version": 2,
                "preferences": {d: {"winner": voice_winner if d == "voice" else "tie",
                                    "a_quote": quote, "b_quote": quote,
                                    "reason": "Synthetic fixture comparison."} for d in DIMENSIONS},
                "critical": {"A": [], "B": []}}

    def test_consistent_loss_allows_bounded_repair_and_learning_accumulates(self):
        for order, winner in (("AB", "A"), ("BA", "B")):
            frozen = task(self.repo, "candidate", order)
            submit(self.repo, "candidate", order, self.judgment(frozen, winner), metadata(True))
        gate = decide(self.repo, "candidate")
        self.assertEqual(gate["decision"], "REPAIR_REQUIRED")
        self.assertEqual(gate["losses"], ["voice"])
        editor = self.candidate.task("book-editor", round_no=2)
        self.assertEqual(editor["inputs"]["regression_feedback"]["decision"], "REPAIR_REQUIRED")
        self.assertIn("regression/decision-r01.json", editor["dependency_hashes"])
        self.candidate.submit(editor, {"schema_version": 2, "operations": [],
                                       "explanation": "Synthetic no-regression repair."}, metadata())
        second = self.candidate.assemble()
        with self.assertRaises(FactoryError):
            self.candidate.complete()
        audit = accepted()
        audit["claim_checks"] = [{"quote": "One unsuccessful attempt is one observation.",
                                  "evidence_ids": [], "support": "nonempirical",
                                  "explanation": "Synthetic logical fixture."}]
        audit["screening_resolutions"] = {f["id"]: "Synthetic fixture triage."
                                           for f in second["assembly"]["screening"]}
        self.candidate.submit(self.candidate.task("final-auditor", round_no=2), audit, metadata(True))
        fresh = decide(self.repo, "candidate")
        self.assertEqual(fresh["decision"], "INCONCLUSIVE")
        self.assertEqual(set(fresh["missing"]), {"AB", "BA"})
        with self.assertRaises(FactoryError):
            advance(self.repo, "candidate")
        # Fresh round ties: keep the old book, but remember the voice regression.
        for order in ("AB", "BA"):
            frozen = task(self.repo, "candidate", order)
            submit(self.repo, "candidate", order, self.judgment(frozen, "tie"), metadata(True))
        self.assertEqual(decide(self.repo, "candidate")["decision"], "PRESERVE_BASELINE")
        result = advance(self.repo, "candidate")
        self.assertEqual(result["status"], "BASELINE_PRESERVED_LEARNING_UPDATED")
        packet = load_next(Run(self.repo, "baseline"))
        self.assertTrue(any(x["dimension"] == "voice" for x in packet["improve"]))

    def test_order_instability_neither_advances_nor_authorizes_repair(self):
        frozen = task(self.repo, "candidate", "AB")
        submit(self.repo, "candidate", "AB", self.judgment(frozen, "B"), metadata(True))
        frozen = task(self.repo, "candidate", "BA")
        submit(self.repo, "candidate", "BA", self.judgment(frozen, "tie"), metadata(True))
        gate = decide(self.repo, "candidate")
        self.assertEqual(gate["decision"], "INCONCLUSIVE")
        self.assertIn("voice", gate["order_instability"])
        with self.assertRaises(FactoryError):
            self.candidate.task("book-editor", round_no=2)
        with self.assertRaises(FactoryError):
            advance(self.repo, "candidate")


if __name__ == "__main__":
    unittest.main()
