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

Wrappers do not choose substitute evaluators or bypass frozen task/result validation. Use factory/config.json and explicit operator authorization. Read docs/FACTORY-V2.md for the standalone factory contract.
