# Worker shard — AOG-RES-01 (research-stage entity reviewer)

- Reviewer: GPT-5.6 Terra medium sub-agent (nickname Singer), read-only
- Scope: research doctrine, miner contract, web primitives, source-packet contract, research routing config, round-1 residue
- Entities reviewed: 91 (research-agent.md 52, researcher.md 11, web_tools.py 9, sources/README.md 11, config research fields 4, round-1 history 4)
- Requirements reviewed: R-001..R-004, R-009..R-011 + research→planning handoff

## Candidate

### CAND-AOG-RES-01-001 — Miner packet handoff has no defined on-disk target or compatible format (MATERIAL-RISK, HIGH/HIGH)

Evidence:
- prompts/research-agent.md:82-90 require miners to return packets "into the ten banks on disk (§5)" and reserve synthesis for the orchestrator
- prompts/research-agent.md:141-158 define ten semantic banks but neither files nor a raw-bank schema
- prompts/research-agent.md:212-218 define only final syntheses and sources/
- .pi/agents/researcher.md:9-10: "the exact output bank file to write"
- .pi/agents/researcher.md:27-28: "Write every accepted packet into the assigned bank file (append, dedupe by source URL)"
- production-books/quit-sugar/research/sources/README.md:3-5 defines a packet as one Markdown file per accepted URL under sources/ (schema lines 16-55)

Mismatch: miner told to write "packets" to an unspecified bank file; only concrete packet contract is per-URL files in sources/. Causal mechanism: a compliant lead cannot derive the promised exact bank-file path or a format compatible with both raw-bank provenance and source packets; runs can write incompatible artifacts, overwrite shared syntheses, or omit sources/ packets needed to validate quotes. Reachable on every research dispatch (PROGRAM.md:155-169). Impact: lead cannot reliably integrate/audit §6/§7; planning can receive incomplete syntheses.

## Passes
- Unlimited depth coherent across doctrine, web_tools.py, config, program (R-001, R-010 PASS)
- §5 floors vs §7 completion criterion consistent (R-004 PASS)
- Research/planning boundary coherent (synthesis reserved; planning limited to the two syntheses)
- Provenance/rights rules align with source-packet schema (R-003 PASS)
- No evidence-editor/framing/commission residue in current doctrine (research-agent.md:88-91) — round-1 artifacts are history only

## Question
- Q: does an external runtime work-order template supply the missing bank mapping? Not discoverable from declared contract.

## Integrity
- No files written; no services called; historical responses sampled not exhaustively read.
