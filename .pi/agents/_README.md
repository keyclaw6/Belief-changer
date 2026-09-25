# v2 factory agent wrappers

`.pi/agents/` is the runtime for the reusable BOOK FACTORY only. Autoresearch/meta-optimization agents do not belong here.

Factory flow:
- factory-orchestrator
- researcher
- evidence-reviewer
- plan-writer
- plan-reviewer
- chapter-writer
- chapter-reviewer
- state-editor
- book-editor
- final-auditor

Runtime role → Pi wrapper:
- evidence-reviewer → evidence-reviewer
- planner → plan-writer
- plan-reviewer → plan-reviewer
- writer → chapter-writer
- chapter-reviewer → chapter-reviewer
- state-editor → state-editor
- book-editor → book-editor
- final-auditor → final-auditor

The Pi `factory-orchestrator` is the reusable factory controller. Run it as a normal saved top-level Pi session loaded with `.pi/agents/factory-orchestrator.md`; do not launch the controller itself through `subagent`, whose child processes are ephemeral. A host harness may launch or supervise that session, but the factory runtime itself is Pi plus these prompts/skills and the deterministic CLI. The controller uses Pi's `subagent` extension only for child factory roles, always with `agentScope: "project"`; it never substitutes its own prose for a missing role. If that extension is unavailable, the factory stops rather than falling back to OpenCode or the parent model.

The evidence-reviewer and final-auditor wrappers are controllers for the configured independent external profile: their inherited Pi model must not author those reviews. They execute/submit the frozen external task and fail closed when no independent profile is configured.

Autoresearch lives under `loop/` and is executed by the outer controller, not through Pi wrappers. That includes pairwise judging, hypothesizing, trace analysis, Factory Learner/Reviewer, baseline comparison and held-out experiments. Pi subprocesses automatically load the repository `AGENTS.md`, so that root contract must stay factory-safe; detailed host/autoresearch execution rules belong only in the host contract and `loop/PROGRAM.md`.

Factory-runtime rules:
- operate only from the supplied/frozen book-factory inputs;
- use the configured routes; never silently substitute a model family;
- external evidence/final reviewers remain independent of the generating family;
- no implicit paid calls, fabricated task outputs, publication, or autoresearch decisions;
- return control at `COMPLETE_UNRELEASED`.

Wrappers do not bypass frozen task/result validation. Use `factory/config.json`, explicit operator authorization, and `docs/FACTORY-V2.md` as the standalone factory contract.
