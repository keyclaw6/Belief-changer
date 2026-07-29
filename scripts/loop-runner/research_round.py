#!/usr/bin/env python3
"""One round of the deep-research stage (PROGRAM Step 3, research-agent.md).

The LEAD is a fresh DeepSeek research call that owns the method. It emits
subagent commissions in a strict fence; this driver runs each commission as
its own fresh DeepSeek research call (web_search + web_fetch, no limits),
then the next round feeds the lead every visible result for integration,
gap-fill, or synthesis. State lives on disk; every round is resumable.

Usage: research_round.py --round N
Round dirs: production-books/quit-sugar/research/_rounds/round-N/
  lead/            lead call trace (request/response/metadata)
  commissions/K-XX.md         parsed commissions
  subagents/K-XX/  each commission's call trace
"""
import argparse, os, re, subprocess, sys, time

import os as _os
REPO = _os.environ.get("BC_REPO") or _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", ".."))
CFG = f"{REPO}/loop/config.yaml"
BOOK = f"{REPO}/production-books/quit-sugar"
ROUNDS = f"{BOOK}/research/_rounds"
# Transport per loop/config.yaml: chat-tools -> tool-loop runner on the
# opencode Go gateway (founder instruction 2026-07-29); else OpenRouter.
def _research_call():
    cfg = open(CFG).read()
    if "researcher_transport: chat-tools" in cfg:
        return ["python3", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "research_toolloop_call.py"),
                "--config", CFG]
    return ["python3", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "openrouter_call.py"),
            "--config", CFG, "--role", "research"]
CALL = _research_call()
RESEARCH_PROMPT = f"{REPO}/prompts/research-agent.md"

LEAD_COVER = """You are the RESEARCH LEAD for this book. The full research
doctrine you must follow is your system prompt. You cannot spawn subagents
yourself; per the doctrine, return focused commissions for the caller to run
as fresh independent research calls, and you will receive their complete
visible results next round.

Emit each commission in EXACTLY this fence (the caller parses it):

=== COMMISSION K-01 ===
<complete, self-contained commission text: the lane, the targeted slot/bank,
the personas or communities to mine, the search patterns to run, and the
exact output format required (packets + raw-bank lines per the doctrine)>
=== END COMMISSION ===

Number commissions K-01, K-02, ... You choose how many and what they do —
you own the method. Also write (before the commissions) the parameter block
from doctrine §1, filled from the brief.

When — and only when — the slot-filling completion criterion (§6) is met
across the accumulated results, respond instead with the line
SYNTHESIZE READY
followed by your complete bank audit, and no commissions.
"""

ROUND_COVER = """You are the RESEARCH LEAD, continuing your multi-round
operation. Below are (1) your own previous-round notes and (2) the COMPLETE
visible results of every commission you issued last round. Integrate them:
update your parameter block if needed, audit banks/slots/personas against
the doctrine's floors and completion criterion, and either issue the next
wave of commissions (same exact fence format) targeting the remaining gaps,
or — if §6 truly clears — respond with the line
SYNTHESIZE READY
followed by your complete bank audit and no commissions.
Never lower a floor, never stop early because a number was hit.
"""

def run_call(user_text, out_dir, tag):
    os.makedirs(out_dir, exist_ok=True)
    uf = os.path.join(out_dir, "input.md")
    open(uf, "w").write(user_text)
    r = subprocess.run(CALL + ["--system-file", RESEARCH_PROMPT,
                               "--user-file", uf, "--out-dir", out_dir])
    if r.returncode != 0:
        print(f"CALL FAILED: {tag}", file=sys.stderr)
        return False
    return True

def parse_commissions(text):
    out = {}
    for m in re.finditer(r"=== COMMISSION (K-\d+) ===\n(.*?)\n=== END COMMISSION ===",
                         text, re.S):
        out[m.group(1)] = m.group(2).strip()
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", type=int, required=True)
    a = ap.parse_args()
    rd = f"{ROUNDS}/round-{a.round}"
    os.makedirs(rd, exist_ok=True)
    brief = open(f"{BOOK}/00-brief.md").read()

    # 1. Lead call
    lead_out = f"{rd}/lead"
    if not os.path.exists(f"{lead_out}/response.md"):
        if a.round == 1:
            user = f"{LEAD_COVER}\n\n# THE BRIEF\n\n{brief}"
        else:
            prev = f"{ROUNDS}/round-{a.round-1}"
            prev_lead = open(f"{prev}/lead/response.md").read()
            parts = [ROUND_COVER, "\n\n# THE BRIEF\n\n" + brief,
                     "\n\n# YOUR PREVIOUS-ROUND NOTES\n\n" + prev_lead]
            subdir = f"{prev}/subagents"
            for k in sorted(os.listdir(subdir)) if os.path.isdir(subdir) else []:
                resp = f"{subdir}/{k}/response.md"
                body = open(resp).read() if os.path.exists(resp) else "[CALL FAILED — no result]"
                parts.append(f"\n\n# RESULT OF {k}\n\n{body}")
            user = "".join(parts)
        if not run_call(user, lead_out, f"lead round {a.round}"):
            sys.exit(1)

    lead_text = open(f"{lead_out}/response.md").read()
    if "SYNTHESIZE READY" in lead_text.splitlines()[0:5].__str__() or \
       re.search(r"^SYNTHESIZE READY\s*$", lead_text, re.M):
        print("LEAD SIGNALS: SYNTHESIZE READY")
        return

    comms = parse_commissions(lead_text)
    if not comms:
        print("NO COMMISSIONS PARSED — inspect lead response", file=sys.stderr)
        sys.exit(3)
    os.makedirs(f"{rd}/commissions", exist_ok=True)
    for k, body in comms.items():
        open(f"{rd}/commissions/{k}.md", "w").write(body)
    print(f"parsed {len(comms)} commissions: {', '.join(sorted(comms))}")

    # 2. Run commissions in bounded batches (egress proxy closes connections
    #    opened beyond a concurrency cap — see diagnosis-connection-close.md)
    MAX_PARALLEL = int(os.environ.get("RESEARCH_MAX_PARALLEL", "4"))
    pending = []
    for k in sorted(comms):
        out = f"{rd}/subagents/{k}"
        if os.path.exists(f"{out}/response.md"):
            print(f"skip {k} (done)")
            continue
        os.makedirs(out, exist_ok=True)
        uf = f"{out}/input.md"
        open(uf, "w").write(
            "You are a fresh research SUBAGENT. Your system prompt is the "
            "research doctrine. You receive ONLY: the brief and your specific "
            "commission. Execute the commission exactly — search and fetch as "
            "wide and deep as still brings results (no ceilings), and deliver "
            "in the exact output format the commission and doctrine require, "
            "with full provenance.\n\n# THE BRIEF\n\n" + brief +
            "\n\n# YOUR COMMISSION\n\n" + comms[k])
        pending.append((k, uf, out))
    fails = []
    for i in range(0, len(pending), MAX_PARALLEL):
        batch = pending[i:i + MAX_PARALLEL]
        procs = []
        for k, uf, out in batch:
            p = subprocess.Popen(CALL + ["--system-file", RESEARCH_PROMPT,
                                         "--user-file", uf, "--out-dir", out])
            procs.append((k, p))
            time.sleep(15)
        fails += [k for k, p in procs if p.wait() != 0]
    if fails:
        print(f"FAILED subagents: {fails}", file=sys.stderr)
        sys.exit(1)
    print(f"round {a.round} complete: lead + {len(comms)} subagents")

if __name__ == "__main__":
    main()
