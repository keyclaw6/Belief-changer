# Hypothesis Inbox

Drop a markdown file here to propose your own hypothesis for the loop to
test. One hypothesis per file. The orchestrator reads this inbox before
spawning the hypothesizer (PROGRAM §4 Step 1).

## File format

Name it anything, e.g. `2026-08-12-shorten-instructions.md`. Inside:

```markdown
# Hypothesis: <one line>

**Change 1 (PRIMARY):** <editable file> — class: <census class> — component: <root component> — <the instruction change>
**Change 2:** <optional; same fields; bound to a census class>
**Change 3:** <optional; same fields; bound to a census class>
**Because:** <the failure or intuition you're acting on>
**Prediction:** <PRIMARY class X falls in BOTH books; secondaries predicted, not decisive>
```

A note may carry up to the current convergence budget (see
`loop/prompts/hypothesizer.md`). Each change names its census class.
Exactly one change is marked PRIMARY.

## Rules

- The orchestrator tests inbox hypotheses **before** machine-generated ones.
  **Oldest = the lexicographically-first filename**, so name files with a date
  prefix (`2026-08-12-shorten-instructions.md`) and arrival order = sort order.
- **One note per iteration.** If several are waiting, only the oldest is tested
  each iteration; the rest wait their turn.
- When a file is picked up it is moved to `loop/inbox/used/` and recorded in
  the iteration, so the inbox only ever holds untested ideas.
- A vague note, or a multi-change note without one change marked PRIMARY and
  each change bound to a census class, is not a hypothesis — the orchestrator
  moves it to `loop/inbox/used/REJECTED-NNN-<name>.md` and tells you what to
  sharpen, rather than guess. Bound multi-change within the budget is valid.
