#!/usr/bin/env python3
"""Durable OpenCode provider-state recovery (store-level, not hook-level).

Background: the `provider-state-portability` outbound hook
(`experimental.chat.messages.transform`) does not run before the provider
rejects stale reasoning `encrypted_content` — the failure occurs before
project chat hooks execute. Relying on the outbound hook alone leaves
recovery ineffective. This script is the durable path.

What it does, in order:
  1. Idle-writer check: refuses unless no other writer holds the session DB
     (BEGIN IMMEDIATE probe). Readers are fine.
  2. Bounded backup: transaction-consistent snapshot via `VACUUM INTO`,
     with size and time bounds; integrity-checked.
  3. Targeted sanitation: in the LIVE store, for one session's reasoning
     parts older than the cutoff, delete ONLY the provider-private keys
     `metadata.openai.itemId` and `metadata.openai.reasoningEncryptedContent`
     (dropping an emptied `openai` object). Visible text, tool I/O, message
     rows, IDs, counts, and post-cutoff reasoning are never touched.
  4. Verification: identical session/message/part IDs and counts, and every
     part's data equal to its pre-change form except the two removed keys.
  5. Audit entry: one JSONL line recording what was done.

Usage:
  python3 scripts/opencode_provider_state_recover.py --db PATH --session ID [--cutoff-ms N] [--audit PATH]
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import sqlite3
import sys
import time

PRIVATE_KEYS = ("itemId", "reasoningEncryptedContent")
BACKUP_MAX_BYTES = 64 * 1024**3
BACKUP_TIMEOUT_S = 600


def fail(msg: str) -> "NoReturn":
    print(f"provider-state-recover: ERROR: {msg}", file=sys.stderr)
    raise SystemExit(2)


def snapshot_ids(con: sqlite3.Connection, session: str) -> dict:
    msgs = [r[0] for r in con.execute(
        "SELECT id FROM message WHERE session_id=? ORDER BY id", (session,))]
    parts = [r[0] for r in con.execute(
        "SELECT id FROM part WHERE session_id=? ORDER BY id", (session,))]
    return {"messages": msgs, "parts": parts}


def part_payload(data: str) -> dict:
    try:
        obj = json.loads(data)
    except ValueError:
        fail("unparseable part data; refusing to sanitize blindly")
    if not isinstance(obj, dict):
        fail("non-object part data; refusing to sanitize blindly")
    return obj


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--session", required=True)
    ap.add_argument("--cutoff-ms", type=int, default=None)
    ap.add_argument("--audit", default=None)
    ap.add_argument("--backup-dir", default=None)
    args = ap.parse_args()
    cutoff = args.cutoff_ms if args.cutoff_ms is not None else int(time.time() * 1000)
    if cutoff <= 0:
        fail("cutoff must be positive epoch millis")
    if not os.path.isfile(args.db):
        fail(f"session store not found: {args.db}")
    backup_dir = args.backup_dir or os.path.join(os.path.dirname(os.path.abspath(args.db)), "provider-state-backups")
    os.makedirs(backup_dir, mode=0o700, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
    backup_path = os.path.join(backup_dir, f"opencode.db.pre-recovery-{stamp}")
    if os.path.exists(backup_path):
        fail(f"backup path already exists: {backup_path}")

    con = sqlite3.connect(args.db, timeout=30)
    con.execute("PRAGMA busy_timeout=5000")
    try:
        # 1. Idle-writer check: fail if another writer is active.
        try:
            con.execute("BEGIN IMMEDIATE")
            con.execute("COMMIT")
        except sqlite3.OperationalError:
            fail("session store has an active writer; recover only while idle")
        # 2. Bounded backup.
        size = os.path.getsize(args.db)
        if size > BACKUP_MAX_BYTES:
            fail(f"store too large for bounded backup ({size} bytes)")
        t0 = time.monotonic()
        con.execute("VACUUM INTO ?", (backup_path,))
        if time.monotonic() - t0 > BACKUP_TIMEOUT_S:
            fail("backup exceeded time bound")
        chk = sqlite3.connect(backup_path)
        try:
            if chk.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                fail("backup integrity check failed")
        finally:
            chk.close()
        backup_sha = hashlib.sha256(open(backup_path, "rb").read()).hexdigest()

        before_ids = snapshot_ids(con, args.session)
        if not before_ids["messages"]:
            fail(f"unknown session: {args.session}")
        before_payloads = {r[0]: r[1] for r in con.execute(
            "SELECT id, data FROM part WHERE session_id=?", (args.session,))}

        # 3. Targeted sanitation in one transaction.
        changed = 0
        with con:
            cur = con.execute("SELECT id, data FROM part WHERE session_id=?", (args.session,))
            for pid, data in cur.fetchall():
                obj = part_payload(data)
                if obj.get("type") != "reasoning":
                    continue
                try:
                    started = int(((obj.get("time") or {}).get("start")) or 0)
                except (TypeError, ValueError):
                    continue
                if started <= 0 or started >= cutoff:
                    continue
                meta = obj.get("metadata")
                if not isinstance(meta, dict):
                    continue
                openai = meta.get("openai")
                if not isinstance(openai, dict) or isinstance(openai, list):
                    continue
                if not any(k in openai for k in PRIVATE_KEYS):
                    continue
                cleaned = {k: v for k, v in openai.items() if k not in PRIVATE_KEYS}
                if cleaned:
                    meta["openai"] = cleaned
                else:
                    del meta["openai"]
                con.execute("UPDATE part SET data=? WHERE id=?", (json.dumps(obj, separators=(",", ":")), pid))
                changed += 1

        # 4. Verification: IDs, counts, and byte-level containment of the diff.
        after_ids = snapshot_ids(con, args.session)
        if after_ids != before_ids:
            fail("session/message/part IDs or counts changed; store left with committed sanitizer transaction — restore from backup")
        for pid, new_data in con.execute("SELECT id, data FROM part WHERE session_id=?", (args.session,)):
            old = part_payload(before_payloads[pid])
            new = part_payload(new_data)
            old_openai = (old.get("metadata") or {}).get("openai") if isinstance(old.get("metadata"), dict) else None
            new_openai = (new.get("metadata") or {}).get("openai") if isinstance(new.get("metadata"), dict) else None
            def pruned(value):
                if not isinstance(value, dict):
                    return value
                kept = {k: v for k, v in value.items() if k not in PRIVATE_KEYS}
                return kept or None
            if pruned(old_openai) != pruned(new_openai):
                fail(f"part {pid}: diff exceeds the two provider-private keys")
            if (old.get("type") == "reasoning" and isinstance(old_openai, dict)
                    and any(k in old_openai for k in PRIVATE_KEYS)):
                try:
                    started = int(((old.get("time") or {}).get("start")) or 0)
                except (TypeError, ValueError):
                    started = 0
                if 0 < started < cutoff and isinstance(new_openai, dict) and any(
                        k in new_openai for k in PRIVATE_KEYS):
                    fail(f"part {pid}: targeted provider-private keys were not removed")
            old_rest = dict(old)
            new_rest = dict(new)
            if isinstance(old.get("metadata"), dict):
                old_rest["metadata"] = {k: v for k, v in old["metadata"].items() if k != "openai"}
            if isinstance(new.get("metadata"), dict):
                new_rest["metadata"] = {k: v for k, v in new["metadata"].items() if k != "openai"}
            if old_rest != new_rest:
                fail(f"part {pid}: non-metadata transcript content changed")
    finally:
        con.close()

    # 5. Audit entry.
    audit_path = args.audit or os.path.join(os.path.dirname(os.path.abspath(args.db)),
                                            "provider-state-recovery-audit.jsonl")
    entry = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "db": args.db,
             "session": args.session, "cutoff_ms": cutoff, "backup": backup_path,
             "backup_sha256": backup_sha, "parts_sanitized": changed,
             "message_count": len(after_ids["messages"]), "part_count": len(after_ids["parts"]),
             "note": "Removed only metadata.openai itemId/reasoningEncryptedContent from pre-cutoff reasoning parts; visible/tool transcript untouched."}
    with open(audit_path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")
    print(json.dumps({"status": "RECOVERED", "parts_sanitized": changed,
                      "messages": len(after_ids["messages"]), "parts": len(after_ids["parts"]),
                      "backup": backup_path, "audit": audit_path}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
