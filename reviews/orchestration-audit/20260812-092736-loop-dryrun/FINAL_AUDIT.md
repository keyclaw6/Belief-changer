# FINAL AUDIT — auto-research loop dry-run

Run: 20260812-092736-loop-dryrun · Target: loop orchestration (not book content)
Revision: main @ afca11f · Read-only audit; six independent workflow dry-runs +
one independent skeptical verifier. Dry-run records in `dry-runs/`.

## Workflow verdicts

| Workflow | Verdict |
|---|---|
| Happy path (one iteration, KEEP) | COMPLETES |
| Resume mid-iteration / results-row exception / stale markers | COMPLETES |
| Patience — healthy long stage + .exit completion | COMPLETES |
| Patience — wedged writer (no .exit marker) | COMPLETES-WITH-RISK → F2 |
| Inbox — well-formed / vague note | COMPLETES |
| Inbox — oldest-first + multi-note drain | COMPLETES-WITH-RISK → F6 |
| Worktree + promote-on-KEEP | COMPLETES-WITH-RISK → F5 |
| Research-reuse handover | COMPLETES-WITH-RISK → F3, F4 |

## Confirmed findings (skeptic-verified)

- **F1 (MEDIUM)** No split-brain/incarnation guard: two actors can resume the
  same IN-PROGRESS run; no lock/lease/owner/token anywhere.
- **F2 (MEDIUM)** Writer stage has no completion marker (no daemon/queue
  wrapper), so "markers stopped" can't fire for a wedged writer; "stuck" rests
  on an undefined "no progress" judgment.
- **F3 (LOW/latent)** `research_reuse.sh` existence glob spans
  `production-books/*/research/` (all books) — should be scoped to the active
  book. Not triggering today; wrong threshold.
- **F4 (MEDIUM)** `config.yaml` is an all-or-nothing research trigger: a
  writer-only config change forces a needless full research rerun.
- **F5 (MEDIUM)** The "one commit" KEEP promotion isn't mechanically pinned —
  change and records live on one branch/worktree; nothing enforces the commit
  file set. REVERT relies on the same manual split.
- **F6 (LOW)** Inbox "oldest first" has no defined sort key; multi-note drain
  (one-per-iteration vs drain-all) is undefined.

## Remediation (applied this session)

F1 → `state.md` gains an `Owner`/incarnation token; §0 refuses to resume when a
live foreign token is present. F2 → writer stage writes a `.exit` marker per
chapter via the runner. F3 → glob scoped to active book. F4 → research-relevant
config keys isolated so only their change triggers rerun. F5 → KEEP/REVERT
commit file-set pinned by an explicit manifest. F6 → oldest = lexicographic
basename; inbox drains one note per iteration.
