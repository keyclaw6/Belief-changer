# Worker shard — AOG-XSYS-01 (identity/boundary/authority/handoff reviewer)

- Reviewer: GPT-5.6 Terra medium sub-agent (nickname James), read-only
- Scope: orchestrator + all spawned roles; pi spawn/runtime routing; extensions + models.json inspected

## Candidates

### CAND-AOG-XSYS-01-001 — Configured role parameters are not consumed by the spawn path (MATERIAL-RISK, MEDIUM/HIGH)

Evidence:
- loop/config.yaml:11-16,23-26,40-43,58-65 declares models, endpoints, auth, reasoning, writer temperature
- ~/.pi/agent/extensions/subagent/agents.ts:12-16,64-68 parses only tools + model from frontmatter
- ~/.pi/agent/extensions/subagent/index.ts:294-327 invokes pi with only --model and --tools

No active consumer passes config endpoints, auth env names, reasoning values, writer temperature, or the no-max_tokens constraint. Plan-reviewer pinned `commandcode/gpt-5.6-luna` with no reasoning suffix despite config `max`. Impact: config edit claims a parameter change while spawned calls use defaults; run trace cannot prove the declared parameter contract; calibration attribution invalid.

### CAND-AOG-XSYS-01-002 — Valid writer refusals terminate without routing to their named repair owner (CONFIRMED-DEFECT, HIGH/HIGH)

Evidence:
- prompts/chapter-writer.md:21-27 refusal encodes action_code `repair_owner_and_regenerate_downstream` + named owner
- prompts/chapter-writer.md:63-67 missing mantra deterministically requires owner `plan` refusal
- prompts/chapter-writer.md:119-122 caller saves refusal to traces only
- loop/PROGRAM.md:204-211 iteration marked INCONCLUSIVE; no dispatch to named owner defined

No stage consumes the action code or invokes the plan writer/research lead/brief owner. Recovery depends on operator inference. One-retry rule covers transport only; 3-strike rule governs judged hypotheses, not refusals.

## Passes
- Miners cannot recursively delegate (tool allowlist excludes subagent)
- Plan-review gate binding; orchestrator owns the loop; BLOCK cannot be waived
- 3-strike rule is not a plan-review escape hatch

## Question
- Q-AOG-XSYS-01-001: "Escalate to the founder" has no defined delivery mechanism (no notification channel, task handoff, or required acknowledgement defined in scripts or runbook).

## Integrity
- No files written; no services called.
