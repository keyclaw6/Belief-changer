# v2 agent wrappers

Pi wrappers are the canonical role runtime. They name roles and point to active contracts; OpenCode is the persistent controller, not a duplicate role registry.

Runtime role → Pi wrapper:
- evidence-reviewer → evidence-reviewer
- planner → plan-writer
- plan-reviewer → plan-reviewer
- writer → chapter-writer
- chapter-reviewer → chapter-reviewer
- state-editor → state-editor
- book-editor → book-editor
- final-auditor → final-auditor

Research and outer-learning helpers use researcher, factory-learner, factory-learning-reviewer, hypothesizer, judge, and trace-analyzer.

Wrappers do not choose substitute evaluators or bypass frozen task/result validation. Use factory/config.json and explicit operator authorization. Read docs/FACTORY-V2.md for stdin adapters and imported response metadata.
