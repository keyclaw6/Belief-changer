"""RF22 resumes deterministic materialization from durable native call records."""
import json, sys, unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "scripts/loop"), str(ROOT / "scripts/eval/tests")]
import commission_set as SET  # noqa: E402
import hf01_upstream as UP  # noqa: E402
import test_hf01_preflight as FIXTURE  # noqa: E402

class CommissionResumeTests(unittest.TestCase):
    def test_resume_after_first_durable_commission_materialization(self):
        fixture = FIXTURE.Hf01Tests(); fixture.setUp(); self.addCleanup(fixture.tearDown)
        _folder, authority, authority_sha = fixture.freeze(); calls = []
        def native(*args, **kwargs):
            calls.append(json.loads(args[0])["id"])
            return fixture.native(*args, **kwargs)
        UP.dispatch_stage(
            fixture.root, authority, authority_sha, "RF-21", complete=native)
        fixture._ledger("IN_PROGRESS", "BLOCKED", rf21="DONE")
        original, stopped = SET._write_commission, False
        def interrupt(root, manifest, relative, text):
            nonlocal stopped
            original(root, manifest, relative, text)
            if not stopped and relative.endswith("chapter-01.md"):
                stopped = True; raise RuntimeError("after durable commission materialization")
        with mock.patch.object(SET.SC, "require_subject_contract"), \
                mock.patch.object(SET, "_write_commission", side_effect=interrupt), \
                self.assertRaisesRegex(RuntimeError, "durable commission"):
            UP.dispatch_stage(
                fixture.root, authority, authority_sha, "RF-22", complete=native)
        experiment = fixture.arms["treatment"]["experiment"]
        self.assertTrue((experiment / "candidate/production-books/quit-sugar/commissions/chapter-01.md").is_file())
        self.assertFalse((experiment / "evidence" / SET.RECEIPT).exists())
        with mock.patch.object(SET.SC, "require_subject_contract"):
            UP.dispatch_stage(
                fixture.root, authority, authority_sha, "RF-22", complete=native)
        self.assertEqual(list(UP.IDS), calls)
        with mock.patch.object(SET.SC, "require_subject_contract"):
            self.assertEqual(64, len(SET.require_writer_eligible(experiment)))

if __name__ == "__main__": unittest.main()
