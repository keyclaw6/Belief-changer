# Worker shard — AOG-AMB-03 (independent ambiguity interpreter)

- Reviewer: GPT-5.6 Terra medium sub-agent (nickname Popper), read-only, isolated

## E1 — Miner packet write target
Primary: "bank file" = orchestrator-provided packet path under research/sources/ (one packet per URL, enriched by repeated use); ten banks are semantic destinations via Bank-slot fields, not ten filenames. The sources/README.md schema resolves format but not how the orchestrator chooses the "exact output bank file." Alternative: ten separate raw-bank files (per researcher.md:9-10,27-28 and "ten banks on disk") — changes file routing, output shape, concurrent-write behavior, downstream integration. Material.

## E2 — Reddit authorization
Primary: mirrors/archives can satisfy the completion criterion because §7 requires slots and personas, not direct Reddit; no source grants direct Reddit authorization. Alternative: "must reach Reddit" (AGENTS.md:13; AUTO-TUNING-LOOP.md:127-132) requires direct Reddit; mirrors are fallback only, so completion cannot legitimately occur without authorization — changes authorization, routing, termination. No higher-priority source defines whether a mirror counts as "Reddit"; the explicit direct-access prohibition remains controlling for direct access.

## E3 — Plan-review cycle limit
Primary: continue cycling after the third BLOCK — PROGRAM.md:171-177 "until" + reviewer's no-waive rule (:100-103) exclude acceptance regardless. Alternative: "up to three cycles" (master-plan-skill-v2.md:141-150) is a hard cap; stop planning and escalate — changes termination and escalation; post-cap escalation action not stated.

## E4 — Writer refusal action code
Primary: `repair_owner_and_regenerate_downstream` is a label; PROGRAM.md:204-212 specifies the actual behavior exhaustively (save, no chapter, owner as finding, INCONCLUSIVE). Alternative: mandatory same-iteration repair+regeneration — inconsistent with the runbook's stated INCONCLUSIVE outcome; changes authority, routing, state, output, termination.

## Integrity
- No files written; no services called; did not inspect other interpreters' outputs.
