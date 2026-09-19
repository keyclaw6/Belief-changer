"""Store-level provider-state recovery: targeted sanitation, count/ID
preservation, transcript immutability, fail-closed behavior. All against a
fabricated temp sqlite store; never the live session DB."""
from __future__ import annotations
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "scripts/opencode_provider_state_recover.py"


def make_db(path: Path) -> None:
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE message (id TEXT PRIMARY KEY, session_id TEXT NOT NULL, time_created INTEGER NOT NULL, time_updated INTEGER NOT NULL, data TEXT NOT NULL)")
    con.execute("CREATE TABLE part (id TEXT PRIMARY KEY, message_id TEXT NOT NULL, session_id TEXT NOT NULL, time_created INTEGER NOT NULL, time_updated INTEGER NOT NULL, data TEXT NOT NULL)")
    con.commit()
    con.close()


def add_message(con: sqlite3.Connection, mid: str, session: str, t: int) -> None:
    con.execute("INSERT INTO message VALUES (?,?,?,?,?)",
                (mid, session, t, t, json.dumps({"role": "assistant"})))


def add_part(con: sqlite3.Connection, pid: str, mid: str, session: str, t: int, data: dict) -> None:
    con.execute("INSERT INTO part VALUES (?,?,?,?,?,?)",
                (pid, mid, session, t, t, json.dumps(data)))


def run_recover(db: Path, session: str, cutoff: int, extra: list | None = None):
    tmp = Path(tempfile.mkdtemp())
    cmd = [sys.executable, str(SCRIPT), "--db", str(db), "--session", session,
           "--cutoff-ms", str(cutoff), "--audit", str(tmp / "audit.jsonl"),
           "--backup-dir", str(tmp / "backups")]
    if extra:
        cmd.extend(extra)
    return subprocess.run(cmd, capture_output=True, text=True), tmp


class RecoverTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "store.db"
        make_db(self.db)
        con = sqlite3.connect(self.db)
        add_message(con, "m1", "ses_a", 100)
        add_message(con, "m2", "ses_a", 200)
        add_message(con, "m9", "ses_b", 100)
        old_meta = {"openai": {"itemId": "opaque-old", "reasoningEncryptedContent": "cipher-old", "keep": "x"},
                    "other": {"keep": True}}
        self.old_reasoning = {"type": "reasoning", "text": "visible-thought", "time": {"start": 100, "end": 101},
                              "metadata": old_meta}
        add_part(con, "p_old", "m1", "ses_a", 100, self.old_reasoning)
        self.new_reasoning = {"type": "reasoning", "text": "fresh", "time": {"start": 900, "end": 901},
                              "metadata": {"openai": {"itemId": "opaque-new", "reasoningEncryptedContent": "cipher-new"}}}
        add_part(con, "p_new", "m1", "ses_a", 900, self.new_reasoning)
        self.text_part = {"type": "text", "text": "hello reader",
                          "metadata": {"openai": {"itemId": "must-stay"}}}
        add_part(con, "p_text", "m1", "ses_a", 100, self.text_part)
        self.tool_part = {"type": "tool", "tool": "read", "callID": "c1",
                          "state": {"status": "completed", "output": "file-bytes encrypted_content mentioned here"}}
        add_part(con, "p_tool", "m2", "ses_a", 200, self.tool_part)
        add_part(con, "p_other", "m9", "ses_b", 100,
                 {"type": "reasoning", "text": "b", "time": {"start": 100},
                  "metadata": {"openai": {"itemId": "opaque-b", "reasoningEncryptedContent": "cipher-b"}}})
        con.commit()
        con.close()

    def tearDown(self):
        self.tmp.cleanup()

    def read(self, pid: str) -> dict:
        con = sqlite3.connect(self.db)
        try:
            return json.loads(con.execute("SELECT data FROM part WHERE id=?", (pid,)).fetchone()[0])
        finally:
            con.close()

    def test_sanitizes_only_stale_reasoning_provider_keys(self):
        proc, tmp = run_recover(self.db, "ses_a", 500)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["parts_sanitized"], 1)
        self.assertEqual(self.read("p_old")["metadata"]["openai"], {"keep": "x"})
        self.assertEqual(self.read("p_old")["metadata"]["other"], {"keep": True})
        self.assertEqual(self.read("p_old")["text"], "visible-thought")
        self.assertEqual(self.read("p_new")["metadata"]["openai"]["itemId"], "opaque-new")
        self.assertEqual(self.read("p_text")["metadata"]["openai"]["itemId"], "must-stay")
        self.assertIn("encrypted_content mentioned here", self.read("p_tool")["state"]["output"])
        self.assertEqual(self.read("p_other")["metadata"]["openai"]["itemId"], "opaque-b")
        audit = (tmp / "audit.jsonl").read_text().strip().splitlines()
        self.assertEqual(len(audit), 1)
        entry = json.loads(audit[0])
        self.assertEqual(entry["session"], "ses_a")
        self.assertEqual(entry["parts_sanitized"], 1)
        self.assertTrue(os.path.isfile(entry["backup"]))

    def test_counts_and_ids_preserved(self):
        con = sqlite3.connect(self.db)
        before_m = con.execute("SELECT id FROM message ORDER BY id").fetchall()
        before_p = con.execute("SELECT id FROM part ORDER BY id").fetchall()
        con.close()
        proc, _ = run_recover(self.db, "ses_a", 500)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        con = sqlite3.connect(self.db)
        try:
            self.assertEqual(con.execute("SELECT id FROM message ORDER BY id").fetchall(), before_m)
            self.assertEqual(con.execute("SELECT id FROM part ORDER BY id").fetchall(), before_p)
        finally:
            con.close()

    def test_unknown_session_fails_closed(self):
        proc, _ = run_recover(self.db, "ses_missing", 500)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("unknown session", proc.stderr)

    def test_bad_cutoff_fails_closed(self):
        proc, _ = run_recover(self.db, "ses_a", 0)
        self.assertNotEqual(proc.returncode, 0)

    def test_empty_openai_object_removed(self):
        con = sqlite3.connect(self.db)
        add_part(con, "p_bare", "m2", "ses_a", 100,
                 {"type": "reasoning", "text": "t", "time": {"start": 50},
                  "metadata": {"openai": {"itemId": "x"}}})
        con.commit()
        con.close()
        proc, _ = run_recover(self.db, "ses_a", 500)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn("openai", self.read("p_bare").get("metadata", {}))


if __name__ == "__main__":
    unittest.main()
