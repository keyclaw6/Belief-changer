"""RF-14 durable API/manual writer refusal regressions."""
import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/loop"))
sys.path.insert(0, str(ROOT / "scripts/eval/tests"))
import candidate_pair as PAIR  # noqa: E402
import commission_set as SET  # noqa: E402
import defect_routing as ROUTING  # noqa: E402
import first_draft_batch as BATCH  # noqa: E402
import run_iteration as RUN  # noqa: E402
import writer_refusal as REFUSAL  # noqa: E402
from writer_context_fixture import WriterFixture  # noqa: E402


def refusal(owner, finding="Required authority is absent."):
    value = {"action_code": REFUSAL.ACTION, "finding": finding, "owner": owner}
    return REFUSAL.PREFIX + json.dumps(value, sort_keys=True, separators=(",", ":"))


class WriterRefusalTests(WriterFixture, unittest.TestCase):
    def prepared(self, name):
        candidate = self.candidate(name)
        self.generate(candidate)
        return candidate

    def api_refusal(self, candidate, owner="plan", interrupt=None):
        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", return_value=("api", "key")), \
                mock.patch.object(RUN.ME, "chat", return_value=refusal(owner)):
            with self.assertRaisesRegex(SystemExit, f"writer routed refusal to {owner}"):
                RUN.write_chapters({"writer_model": "writer/model"},
                                   self.book(candidate), [1, 2], candidate, interrupt)

    def assert_replay_blocked_before_dispatch(self, candidate, owner):
        endpoint, api, manual = mock.Mock(), mock.Mock(), mock.Mock()
        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", endpoint), \
                mock.patch.object(RUN.ME, "chat", api), \
                mock.patch.object(RUN.MD, "writer", manual):
            with self.assertRaisesRegex(SystemExit, f"writer routed refusal to {owner}"):
                RUN.write_chapters({"writer_model": "writer/model"},
                                   self.book(candidate), [1, 2], candidate)
        endpoint.assert_not_called()
        api.assert_not_called()
        manual.assert_not_called()

    def test_api_refusal_is_hash_bound_recoverable_and_blocks_advancement(self):
        """OpenSpec scenario: A writer detects an upstream defect."""
        candidate = self.prepared("api-route")
        chapter = self.book(candidate) / "chapters/chapter-01.md"
        before = chapter.read_bytes()
        self.api_refusal(candidate)
        batch = PAIR.load(candidate)["draft_batch"]
        self.assertEqual([], batch["drafts"])
        self.assertIsNotNone(batch["call"])
        self.assertEqual(before, chapter.read_bytes())
        plan = REFUSAL.require(candidate, batch)
        self.assertEqual("plan", plan["next_owner"])
        self.assertEqual(["master-plan.md", "master-plan-review.md"],
                         plan["repair_artifacts"])
        self.assertNotIn("research/synthesis", plan["invalidate_owners"])
        ROUTING.require_regeneration(plan, plan["regenerate_owners"])
        with self.assertRaises(ROUTING.RoutingError):
            ROUTING.require_regeneration(plan, ["research/synthesis",
                                                *plan["regenerate_owners"]])
        receipt = REFUSAL.receipt_path(candidate)
        expected = receipt.read_bytes()
        receipt.chmod(0o644)
        receipt.unlink()
        self.assert_replay_blocked_before_dispatch(candidate, "plan")
        self.assertEqual(expected, receipt.read_bytes())
        with self.assertRaisesRegex(REFUSAL.RoutedRefusal, "writer routed refusal"):
            BATCH.freeze(candidate)

    def test_manual_refusal_wins_over_complete_prose_and_replays_same_route(self):
        """OpenSpec scenario: A manual agent is dispatched."""
        candidate = self.prepared("manual-route")
        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", return_value=("api", "")):
            self.assertFalse(RUN.write_chapters(
                {"writer_model": "writer/model"}, self.book(candidate), [1, 2], candidate))
        complete = b"# Chapter 1\n" + b"word " * 900
        (self.book(candidate) / "chapters/chapter-01.md").write_bytes(complete)
        sidecar = REFUSAL.manual_path(candidate, 1)
        sidecar.write_text(refusal("research/synthesis"), encoding="utf-8")
        with self.assertRaisesRegex(REFUSAL.RoutedRefusal,
                                    "writer routed refusal to research/synthesis"):
            BATCH.accept_manual(candidate)
        batch = PAIR.load(candidate)["draft_batch"]
        self.assertEqual([], batch["drafts"])
        self.assertEqual(complete, (self.book(candidate) /
                                   "chapters/chapter-01.md").read_bytes())
        plan = REFUSAL.require(candidate, batch)
        self.assertEqual("research/synthesis", plan["next_owner"])
        self.assertEqual(["research/**"], plan["repair_artifacts"])
        self.assertNotIn("brief", plan["invalidate_owners"])
        self.assert_replay_blocked_before_dispatch(candidate, "research/synthesis")

    def test_manifest_refusal_downgrade_is_rejected(self):
        """Infra: routed refusal state cannot be silently removed on restart."""
        candidate = self.prepared("route-downgrade")
        self.api_refusal(candidate, "brief")
        path = candidate / PAIR.MANIFEST
        value = json.loads(path.read_text(encoding="utf-8"))
        value["draft_batch"]["refusal"] = None
        path.write_text(json.dumps(value), encoding="utf-8")
        with self.assertRaisesRegex(PAIR.PairError, "removed or downgraded"):
            PAIR.load(candidate)

    def test_descriptor_commit_without_receipt_recovers_on_restart(self):
        """Infra: restart after the durable refusal-state boundary is deterministic."""
        candidate = self.prepared("route-crash")

        def interrupt(step):
            if step == "refusal-recorded":
                raise RuntimeError("simulated crash")

        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", return_value=("api", "key")), \
                mock.patch.object(RUN.ME, "chat", return_value=refusal("framing")):
            with self.assertRaisesRegex(RuntimeError, "simulated crash"):
                RUN.write_chapters({"writer_model": "writer/model"},
                                   self.book(candidate), [1, 2], candidate, interrupt)
        self.assertFalse(os.path.lexists(REFUSAL.receipt_path(candidate)))
        self.assert_replay_blocked_before_dispatch(candidate, "framing")
        self.assertTrue(REFUSAL.receipt_path(candidate).is_file())

    def test_api_rejects_every_noncanonical_refusal_serialization(self):
        """Infra: API refusal bytes have one exact canonical serialization."""
        action = REFUSAL.ACTION
        canonical = refusal("plan")
        malformed = (
            canonical + "\n",
            " " + canonical,
            REFUSAL.PREFIX + json.dumps({
                "action_code": action, "finding": "Required authority is absent.",
                "owner": "plan"}),
            REFUSAL.PREFIX + ('{"owner":"plan","finding":"Required authority is '
                              'absent.","action_code":"' + action + '"}'),
            REFUSAL.PREFIX + ('{"action_code":"' + action + '","finding":'
                              '"Required authority is absent.","owner":"plan",'
                              '"owner":"brief"}'),
            REFUSAL.PREFIX + ('{"action_code":"' + action + '","finding":1,'
                              '"owner":"plan"}'),
            REFUSAL.PREFIX + ('{"action_code":"' + action + '","finding":'
                              '"Required authority is absent."}'),
        )
        for index, response in enumerate(malformed):
            with self.subTest(case=index):
                candidate = self.prepared(f"api-malformed-{index}")
                before = (self.book(candidate) / "chapters/chapter-01.md").read_bytes()
                with mock.patch.object(SET.SC, "require_subject_contract"), \
                        mock.patch.object(RUN.judges, "endpoint",
                                          return_value=("api", "key")), \
                        mock.patch.object(RUN.ME, "chat", return_value=response):
                    with self.assertRaisesRegex(SystemExit,
                                                "invalid writer route refusal"):
                        RUN.write_chapters({"writer_model": "writer/model"},
                                           self.book(candidate), [1, 2], candidate)
                batch = PAIR.load(candidate)["draft_batch"]
                self.assertIsNone(batch["refusal"])
                self.assertEqual([], batch["drafts"])
                self.assertFalse(os.path.lexists(REFUSAL.anchor_path(candidate)))
                self.assertEqual(before, (self.book(candidate) /
                                          "chapters/chapter-01.md").read_bytes())

    def test_manual_rejects_duplicate_keys_and_outer_newline(self):
        """Infra: manual refusal sidecars obey the same exact byte contract."""
        duplicate = (REFUSAL.PREFIX + '{"action_code":"' + REFUSAL.ACTION +
                     '","finding":"Missing.","owner":"plan","owner":"brief"}')
        for index, response in enumerate((duplicate, refusal("plan") + "\n")):
            with self.subTest(case=index):
                candidate = self.prepared(f"manual-malformed-{index}")
                with mock.patch.object(SET.SC, "require_subject_contract"), \
                        mock.patch.object(RUN.judges, "endpoint",
                                          return_value=("api", "")):
                    self.assertFalse(RUN.write_chapters(
                        {"writer_model": "writer/model"}, self.book(candidate),
                        [1, 2], candidate))
                REFUSAL.manual_path(candidate, 1).write_text(response, encoding="utf-8")
                with self.assertRaises(REFUSAL.RefusalError):
                    BATCH.accept_manual(candidate)
                batch = PAIR.load(candidate)["draft_batch"]
                self.assertIsNone(batch["refusal"])
                self.assertEqual([], batch["drafts"])
                self.assertFalse(os.path.lexists(REFUSAL.anchor_path(candidate)))

    def test_anchor_blocks_coordinated_local_route_deletion_and_prose_acceptance(self):
        """Infra: local refusal state cannot be jointly cleared after restart."""
        candidate = self.prepared("route-coordinated-delete")
        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", return_value=("api", "")):
            self.assertFalse(RUN.write_chapters(
                {"writer_model": "writer/model"}, self.book(candidate), [1, 2], candidate))
        sidecar = REFUSAL.manual_path(candidate, 1)
        sidecar.write_text(refusal("plan"), encoding="utf-8")
        with self.assertRaises(REFUSAL.RoutedRefusal):
            BATCH.accept_manual(candidate)
        anchor = REFUSAL.anchor_path(candidate)
        anchor_bytes = anchor.read_bytes()
        receipt = REFUSAL.receipt_path(candidate)
        receipt.chmod(0o644)
        receipt.unlink()
        sidecar.chmod(0o644)
        sidecar.unlink()
        value = json.loads((candidate / PAIR.MANIFEST).read_text(encoding="utf-8"))
        value["draft_batch"]["refusal"] = None
        (candidate / PAIR.MANIFEST).write_text(json.dumps(value), encoding="utf-8")
        (self.book(candidate) / "chapters/chapter-01.md").write_bytes(
            b"# Chapter 1\n" + b"word " * 900)
        endpoint, api, manual = mock.Mock(), mock.Mock(), mock.Mock()
        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", endpoint), \
                mock.patch.object(RUN.ME, "chat", api), \
                mock.patch.object(RUN.MD, "writer", manual):
            with self.assertRaisesRegex(SystemExit, "removed or downgraded"):
                RUN.write_chapters({"writer_model": "writer/model"},
                                   self.book(candidate), [1, 2], candidate)
        endpoint.assert_not_called()
        api.assert_not_called()
        manual.assert_not_called()
        self.assertEqual(anchor_bytes, anchor.read_bytes())
        raw = json.loads((candidate / PAIR.MANIFEST).read_text(encoding="utf-8"))
        self.assertEqual([], raw["draft_batch"]["drafts"])

    def test_anchor_replacement_blocks_restart_before_dispatch(self):
        """Infra: the operation-level route anchor is identity-bound."""
        candidate = self.prepared("route-anchor-replaced")
        self.api_refusal(candidate, "brief")
        anchor = REFUSAL.anchor_path(candidate)
        anchor.chmod(0o644)
        anchor.write_text("{}\n", encoding="utf-8")
        endpoint = mock.Mock()
        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(RUN.judges, "endpoint", endpoint):
            with self.assertRaisesRegex(SystemExit, "monotonic anchor changed"):
                RUN.write_chapters({"writer_model": "writer/model"},
                                   self.book(candidate), [1, 2], candidate)
        endpoint.assert_not_called()


if __name__ == "__main__":
    unittest.main()
