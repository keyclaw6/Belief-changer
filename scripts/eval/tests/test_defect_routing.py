"""RF-14 owner routing and causal invalidation regressions."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
sys.path.insert(0, str(ROOT / "scripts/eval/tests"))
import defect_routing as ROUTING  # noqa: E402
import developmental_review as DEV  # noqa: E402
import grounded_review as GR  # noqa: E402
import judges  # noqa: E402
from developmental_review_fixture import (  # noqa: E402
    DevelopmentalFixture, finding as developmental_finding,
    proven_runner as developmental_runner, verdict as developmental_verdict)
from grounded_review_fixture import (  # noqa: E402
    finding as grounded_finding, proven_runner as grounded_runner,
    verdict as grounded_verdict)


class DefectRoutingTests(DevelopmentalFixture, unittest.TestCase):
    def test_catalogue_routes_to_plan_and_invalidates_only_downstream(self):
        """OpenSpec scenario: Review finds an upstream defect."""
        candidate = self.ready("routing-catalogue")
        task = DEV.prepare(candidate)
        defect = developmental_finding(
            task, category="deferred_transformation_repetition",
            basis="card_sequence_defect", symptom="catalogue_replaces_discovery")
        with self.assertRaisesRegex(DEV.DevelopmentalReviewError, "NEEDS_CHANGES"):
            DEV.advance(candidate, runner=developmental_runner(
                lambda exact: developmental_verdict(
                    exact, "NEEDS_CHANGES", [defect])))
        routing = json.loads(DEV.receipt_path(candidate).read_text())["routing"]
        self.assertEqual("plan", routing["next_owner"])
        self.assertEqual(["master-plan.md", "master-plan-review.md"],
                         routing["repair_artifacts"])
        self.assertEqual(list(ROUTING.OWNERS[4:]), routing["invalidate_owners"])
        self.assertNotIn("research/**", routing["invalidate_artifacts"])
        ROUTING.require_regeneration(routing, routing["regenerate_owners"])
        with self.assertRaises(ROUTING.RoutingError):
            ROUTING.require_regeneration(
                routing, ["research/synthesis", *routing["regenerate_owners"]])

    def test_grounded_missing_support_and_packet_leakage_route_upstream(self):
        """OpenSpec scenario: A grounded blocker remains."""
        cases = (
            ("missing-support", "invention", "research/synthesis"),
            ("packet-leakage", "ownership leakage", "commission/context"),
        )
        for name, classification, owner in cases:
            with self.subTest(owner=owner):
                candidate = self.frozen("routing-" + name)
                tasks = GR.prepare(candidate)
                defect = grounded_finding(tasks[1], classification, owner)
                defect["draft_span"] = tasks[1]["context"]["frozen_draft"][:80]

                def response(task):
                    return (grounded_verdict(task, "BLOCK", [defect])
                            if task["chapter"] == 1 else grounded_verdict(task))

                with self.assertRaisesRegex(GR.GroundedReviewError, "BLOCK"):
                    GR.advance(candidate, runner=grounded_runner(response))
                receipt = json.loads(GR.receipt_path(candidate).read_text())
                self.assertEqual("BLOCKED", receipt["state"])
                self.assertEqual(owner, receipt["routing"]["next_owner"])
                self.assertFalse((candidate / "judge-tasks").exists())
                with self.assertRaisesRegex(SystemExit, "grounded PASS"):
                    judges.emit_tasks({"tasks_dir": str(candidate / "judge-tasks"),
                                       "judge_k": 1}, [], "001", "", candidate)

    def test_judge_wording_defect_routes_to_prose_with_exact_vocabulary(self):
        """OpenSpec requirement: Owner-routed repair."""
        verdict = {"scores": {dimension: 5 for dimension in judges.DIMS},
                   "suggestions": [
                       {"owner": "prose", "suggestion": "Tighten this wording."},
                       {"owner": "plan", "suggestion": "Land one discovery."},
                       {"owner": "evaluation", "suggestion": "Clarify this diagnostic."}]}
        path = self.accepted / "judge.json"
        path.write_text(json.dumps(verdict), encoding="utf-8")
        parsed = judges._parse_verdict(path)
        wording = ROUTING.plan("judge", [parsed["suggestions"][0]],
                               "apply_judge_suggestion")
        self.assertEqual("prose", wording["next_owner"])
        self.assertEqual(["revision", "evaluation"],
                         wording["invalidate_owners"])
        invalid = dict(verdict)
        invalid["suggestions"] = [
            {"asset": "chapter-writer", "suggestion": "old route"},
            *verdict["suggestions"][1:]]
        path.write_text(json.dumps(invalid), encoding="utf-8")
        with self.assertRaisesRegex(SystemExit, "fields"):
            judges._parse_verdict(path)
        both = dict(verdict)
        both["suggestions"] = [
            {"owner": "prose", "asset": "chapter-writer",
             "suggestion": "mixed route"}, *verdict["suggestions"][1:]]
        path.write_text(json.dumps(both), encoding="utf-8")
        with self.assertRaisesRegex(SystemExit, "fields"):
            judges._parse_verdict(path)
        self.assertEqual(("brief", "research/synthesis", "framing", "plan",
                          "commission/context", "prose", "revision", "evaluation"),
                         ROUTING.OWNERS)

    def test_judge_route_uses_all_findings_before_display_truncation(self):
        """OpenSpec scenario: Judge findings route to their earliest owner."""
        cfg = {"tasks_dir": str(self.accepted / "judge-tasks"), "judge_k": 2,
               "weights": [f"{dimension}: {1 / len(judges.DIMS)}"
                           for dimension in judges.DIMS]}
        vdir = judges.judging_dir(cfg, "001") / "verdicts"
        vdir.mkdir(parents=True)
        prose = [{"owner": "prose", "suggestion": f"Prose display finding {i}."}
                 for i in range(5)]
        verdicts = (prose, [*prose[:4],
                            {"owner": "brief", "suggestion": "Repair the premise."}])
        for number, suggestions in enumerate(verdicts, 1):
            value = {"scores": {dimension: 5 for dimension in judges.DIMS},
                     "suggestions": suggestions}
            (vdir / f"ch1-j{number}.json").write_text(json.dumps(value),
                                                       encoding="utf-8")
        result = judges.aggregate(cfg, ["ch1"], "001")
        self.assertEqual(5, len(result["suggestions"]))
        self.assertNotIn("brief", [item["owner"] for item in result["suggestions"]])
        route = result["routing"]
        self.assertEqual("brief", route["next_owner"])
        self.assertEqual(["00-brief.md"], route["repair_artifacts"])
        self.assertEqual(list(ROUTING.OWNERS[1:]), route["invalidate_owners"])
        ROUTING.require_regeneration(route, list(ROUTING.OWNERS))


if __name__ == "__main__":
    unittest.main()
