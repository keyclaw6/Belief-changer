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

Autoresearch lives under `loop/` and is executed by the outer controller, not through Pi wrappers. That includes pairwise judging, hypothesizing, trace analysis, Factory Learner/Reviewer, baseline comparison and held-out experiments.

Factory-runtime rules:
- operate only from the supplied/frozen book-factory inputs;
- use the configured routes; never silently substitute a model family;
- external evidence/final reviewers remain independent of the generating family;
- no implicit paid calls, fabricated task outputs, publication, or autoresearch decisions;
- return control at `COMPLETE_UNRELEASED`.

Wrappers do not bypass frozen task/result validation. Use `factory/config.json`, explicit operator authorization, and `docs/FACTORY-V2.md` as the standalone factory contract.
