# Hypothesis Inbox

Drop a markdown file here to propose your own hypothesis for the loop to
test. One hypothesis per file. The orchestrator reads this inbox before
spawning the hypothesizer (PROGRAM §4 Step 1).

## File format

Name it anything, e.g. `2026-08-12-shorten-instructions.md`. Inside:

```markdown
# Hypothesis: <one line>

**Change:** <which editable file, what change>
**Because:** <the failure or intuition you're acting on>
**Prediction:** <what should improve, and how the judges will show it>
```

## Rules

- The orchestrator tests inbox hypotheses **before** machine-generated ones.
  **Oldest = the lexicographically-first filename**, so name files with a date
  prefix (`2026-08-12-shorten-instructions.md`) and arrival order = sort order.
- **One note per iteration.** If several are waiting, only the oldest is tested
  each iteration; the rest wait their turn.
- When a file is picked up it is moved to `loop/inbox/used/` and recorded in
  the iteration, so the inbox only ever holds untested ideas.
- A vague or multi-change note is not a hypothesis — the orchestrator moves it
  to `loop/inbox/used/REJECTED-NNN-<name>.md` and tells you what to sharpen,
  rather than guess.
