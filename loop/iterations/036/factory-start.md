# 036 factory start

`opencode run --agent factory --model opencode-go/muse-spark-1.3-contributor`
failed before any plan/chapter work:

1. Concurrent instances: `database is locked` on `~/.local/share/opencode/opencode.db`.
2. Go CLI: explicit workspace data-collection opt-in. This chat did not toggle that.

`prompts/factory-orchestrator.md` allows `write_replicate.py` once per slug when
the harness cannot spawn Muse chapter roles. Hypothesis is chapter-reviewer
only, so the plan loop is skipped and the accepted plans stay in
`production-books/<slug>/master-plan.md`.

Sessions: `f036-quit-sugar`, `f036-quit-smoking` (write_replicate A1 K=3, Muse Go).
