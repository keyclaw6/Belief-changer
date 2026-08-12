# Dry Run — Worktree + Promote-on-KEEP scenario family

Audited revision: `main` @ `afca11f` ("feat(loop): iterations run in git worktrees;
KEEP promotes to campaign branch").
Scope: `loop/PROGRAM.md` (§1 State discipline, §3 baseline-on-branch, §4 Step 6
decision, §4 Step 7 record/promote), the loop-facing parts of `AGENTS.md`
(§Workflow, §Content Rules, §Auto-tuning campaign), `docs/AUTO-TUNING-LOOP.md`,
plus the supporting files `loop/state.md`, `loop/ledger.md`, `loop/results.tsv`,
`loop/learnings.md`, `scripts/loop-runner/*`, `scripts/repo-push.sh`.
Read-only simulation — no files edited outside this audit tree, no model calls.

Declared precedence (from `SOURCE_OF_TRUTH.md`): AGENTS.md → AUTO-TUNING-LOOP.md
(North Star, locked) → PROGRAM.md (sole runbook, self-locked) → config.yaml.

Key facts about the audited model first, so the traces below are readable:

- **Baseline (000) runs on the campaign branch directly** — "no worktree; there
  is nothing to accept or reject yet, only to measure. Iteration worktrees begin
  at 001." (PROGRAM §3)
- **All iterations 001+ run in a separate worktree** at `../quit-sugar-iter-NNN/`
  on an iteration branch. (PROGRAM §1)
- **KEEP**: change promoted to the campaign branch as one commit
  `loop(iter-NNN): KEEP — short hypothesis`; `loop/iterations/NNN/` records merge
  with it. (PROGRAM §4 Step 7)
- **REVERT / INCONCLUSIVE**: factory change NOT promoted; only records
  (`iterations/NNN/`, results row, ledger entry) are committed to the campaign
  branch. (PROGRAM §4 Step 6 + Step 7)
- **Worktree removed** once its records are committed. (PROGRAM §4 Step 7)
- **main vs campaign**: campaign branch created fresh from `main` when a campaign
  starts; `main` carries only founder-merged winners. (PROGRAM §1, AGENTS.md
  §Workflow)

Trace context checks (all COMPLETES):
- Baseline state: `state.md` shows 000 baseline pending, preflight PASS
  (2026-08-07). `ledger.md` "Entries: (none yet — the baseline experiment will
  be the first entry)". `results.tsv` has header only. On-disk markers agree.
  Consistent across all files. ✓
- No automation exists for worktree create/remove, promotion, or merge — all
  git mechanics are left to the orchestrator by hand per PROGRAM prose. This is
  the central source of risk below.

---

## (a) Iteration 001 runs in worktree `../quit-sugar-iter-001`, gets KEEP — is promotion (one commit) + records merge + worktree removal fully specified and reachable?

**Verdict: COMPLETES-WITH-RISK**

### Why it completes

- **Worktree location is specified.** PROGRAM §1 names the exact sibling path
  `../quit-sugar-iter-NNN/` and says the change + generated artifacts live there
  on an iteration branch. That is concrete and reachable: `git worktree add`
  from `main` gives a HEAD-lagging branch safely isolated from the checkout. ✓
- **KEEP verdict is reachable** (§4 Step 6): decision valid iff every judge
  report completed; KEEP fires when the targeted cluster improved materially and
  no lane shows a material regression. All role mechanics referenced exist
  (`loop/judges/*` prompts present; judge/trace-analyzer/hypothesizer spawn
  documented in §1 and config.yaml). ✓
- **One-commit promotion is specified.** §4 Step 7: "promote the iteration's
  change to the campaign branch as one commit (`loop(iter-NNN): KEEP — short
  hypothesis`) and merge the `loop/iterations/NNN/` records with it." The commit
  message subject-line format is given verbatim. ✓
- **Records merge is specified.** Reached by the same Step 7 sentence plus §4
  Step 6 ("promote it to the campaign branch (Step 7) and keep the generated
  artifacts"). ✓
- **Worktree removal is specified.** §4 Step 7 last line: "Remove the iteration
  worktree once its records are committed." Order is explicit (records first,
  then remove). ✓

### The risk — "one commit" is contradicted by the same sentence

This is the sharpest defect in the whole model. §4 Step 7 says promotion is **one
commit**, but the very sentence that says "one commit" also says the iteration
change **and** the `loop/iterations/NNN/` factory-change path are merged **with
it**. Two distinct blobs cannot land in one commit through any plumbing, because
two nominations were never separated:

1. **The iteration worktree contains BOTH the factory change AND the
   `iterations/NNN/` records** — the records are generated inside the worktree
   (§4 Step 4/5 write `judgments/`, `trace-analysis.md`, `hypothesis.md`,
   `change.diff`, `decision.md` into `loop/iterations/NNN/` "in this iteration's
   traces"). Git cannot independently lift "the factory change only" out of a
   worktree whose HEAD branch only has the iteration branch — the promotion has
   no `git add` source that separates change-files from record-files.
2. Because both live on one branch, executing "one commit with change + records"
   is impossible, and executing the only mechanically valid version (two commits:
   factory change, then records) contradicts the program's literal "one commit".

So the program stipulates a git state that has **no mechanical realization** at
Step 7, without its own implementation precedent. The instruction text gives the
orchestrator enough intent to *whiteboard* the right end state (change promoted,
records captured, one logical promotion), but it does not give a runnable blob
list, and a fresh agent has no script to consult and no prior-commit precedent to
copy in this campaign (the campaign branch does not exist yet on disk).

**The records-merge problem is worse for REVERT/INCONCLUSIVE** — see (b). For
KEEP specifically, an asymmetric wrinkle: `change.diff` records the diff of the
factory change; the generated artifacts (research/runtime copies under
`iterations/NNN/traces/`) are big and are *evidence*, not hypotheses (§1). "Merge
the `loop/iterations/NNN/` records with it" bundles them into the KEEP commit,
which inflates the single commit with the whole trace tree. That is arguably
intended (records kept), but it is not made explicit that the KEEP commit
therefore also carries `traces/`. Risk that promotion too eagerly includes giant
generated artifacts, or omits them and loses trace evidence — either way the
program does not govern the choice.

**Reachability conclusion:** the *mechanics* are all reachable (worktree add,
commit, merge, worktree remove are primitives any git-capable agent has). What is
not reachable is the program's stated *unit* ("one commit"). Because no file
source is separated, a faithful agent will either (i) two-commit and violate the
letter, or (ii) attempt one commit and be unable to produce it mechanically and
find itself improvising. Neither is acceptable under §5 "no deterministic
validation / prompts are the real surface" — for *this* section there is no
prompt; it is raw git, so the lack of a spec is material.

### Mitigations that would make it COMPLETES

- Pin the **current working directory / worktree root** for each step,
  eliminating the "cross-check against main" ambiguity from (d).
- Define whether promotion is **two commits** ("one logical promotion" = change
  commit + records commit) or a single commit containing both, with an explicit
  `git add <paths>` file list.
- Define where the **generated artifacts** (`iterations/NNN/traces/`) and the
  records go on promotion — in the commit, in the tree only, or on the campaign
  branch at all.

---

## (b) Iteration gets REVERT — is the factory change correctly NOT promoted while `iterations/NNN/` records + ledger entry ARE committed to the campaign branch?

**Verdict: COMPLETES-WITH-RISK**

### Why it completes

- **The decision rule for REVERT** is fully specified (§4 Step 6: targeted
  cluster did not improve, or a material regression appeared → REVERT; also
  INCONCLUSIVE path when evidence is incomplete). ✓
- **"Change not promoted"** is stated plainly twice — §4 Step 6 ("REVERT /
  INCONCLUSIVE: the change is not promoted — the iteration's worktree and its
  factory change are discarded") and §4 Step 7 ("commit only the records
  (…), never the factory change"). ✓
- **Record files are committed** to the campaign branch: the program names
  `iterations/NNN/`, results row, and ledger entry. ✓
- **Ledger entry is committed.** §4 Step 7 ordering: results row → learnings →
  ledger → then the branch commit; the ledger header explicitly says the ledger
  entry is part of the keep-always set. ✓
- **Worktree removed after records committed.** Last line of Step 7; applies to
  REVERT/INCONCLUSIVE equally. ✓

### The risk — same cohabitation defect, and now it bites harder

The records the program wants to commit live **inside the iteration worktree,
which has just been declared "discarded."** The program never separates the
record blob from the change blob, so the ONLY way to "commit only the records,
never the factory change" is to hand-assemble a commit from cherry-picked paths.
Two practical failures are unattended:

1. **`change.diff` is a record AND is the factory change.** §4 Step 2 writes the
   hypothesis diff into `iterations/NNN/change.diff`. If that file is committed
   as a "record" (it is under `iterations/NNN/`), then the *prerevert* factory
   change is captured on the campaign branch in diff form — fine for diagnosis,
   but the program calls the record set "not the factory change," and nothing
   says the post-promotion campaign tree is restored to pre-iteration state.
   The three declarations — change "discarded," records committed, worktree kept
   "so the campaign never re-tries a failed hypothesis blindly" (§4 Step 6) —
   interact such that the *actual factory files* on the campaign branch are the
   only thing provably NOT committed; verification of "reverted cleanly" is not
   a step in the program.
2. **No rollback instruction.** "The iteration's worktree and its factory change
   are discarded" says the worktree is the revert mechanism, but nothing tells
   the orchestrator to confirm the campaign branch's factory file matches the
   baseline's before/after. If a record-commit accidentally stages an editable
   file, there is no check for it.

So (b) is *specified* (all the words are there) yet *under-specified* (no
mechanical way to do it as one operation, no post-revert verification, no
path-level nomination). Reachable by a careful agent; a genuine failure path for
a fresh agent. This is the verdict's "WITH-RISK," not BLOCKED: the intent is
unambiguous, and a disciplined orchestrator can hand-run `git restore`/partial
`git add`.

### Mitigations

- Add an explicit **"revert = restore campaign-branch factory files to the
  previous KEEP/baseline state before committing records,"** with a post-step
  check against the last accepted state.
- Nominate the record blob exactly (e.g. `loop/iterations/NNN/` + `results.tsv`
  + `ledger.md` + `learnings.md`) and state that `change.diff` is a **record**
  and must not migrate into the factory.

---

## (c) Does the KEEP commit contain the right file set (tuning change + `iterations/NNN/`) and exclude stray worktree artifacts?

**Verdict: COMPLETES-WITH-RISK**

### Why it completes

- **Tuning change is named by §1 Editable list** (`prompts/style-guide.md`,
  `prompts/research-agent.md`, `prompts/master-plan-skill-v2.md`,
  `prompts/master-plan-reviewer-v2.md`, `prompts/chapter-writer.md`,
  `loop/config.yaml`) and by §5 "one causal change in one editable file."
  The KEEP commit is supposed to carry exactly that one file's change. ✓
- **`iterations/NNN/` is named** as the record set to merge in. ✓

### Why it does not quite meet the letter

- **No file-set is named at commit time.** The program never enumerates
  `git add`/commit paths for the promotion. It leans on "the change" + "the
  records," but because (a)/(b) showed those two are a single blob on the
  iteration branch, the orchestrator must infer the boundary.
- **Stray-artifact exclusion is unaddressed.** §4 Step 3 runs the whole factory
  in the worktree, which produces generated research, plans, and chapters under
  `production-books/quit-sugar/` — §1 explicitly hides these is "evidence, not
  editable hypotheses." Nothing says whether the KEEP commit carries them
  (probably not — they are evidence and the source files are committed baseline
  artifacts), whether `trace-analysis.md`/judgment copies ride in as records
  (probably yes — §4 Step 7 "merge the `loop/iterations/NNN/` records"), or how
  the worktree's `.loop-work`/scratch (gitignored) and temp files stay out. The
  only git discipline force-multiplier present is the `.gitignore` (`.loop-work/`
  is ignored), but generated chapters are NOT ignored and would be swept in by a
  naive `git add -A`.
- **No post-commit verification step** (e.g., `git show --stat`, compare against
  the editable-files allowlist) exists anywhere in §4. So "contains the right
  file set and excludes strays" is an intent, not a checkable contract.

Thus the *right* file set is fully inferable from §1+§5, and a careful agent
would likely get it right; but the program puts no guardrail between "naive
`git add -A` in the worktree" and "KEEP commit now also carries a regenerated
chapter + research tree." That is exactly a stray-artifact risk.

### Mitigations

- Add a **commit-content postcondition**: after promotion, `git show --stat`
  must touch only the single editable file + the nominated records path.
- State explicitly that generated book artifacts (`production-books/
  quit-sugar/…`, `research/`, `traces/` inside `iterations/NNN/`) are or are not
  part of the KEEP commit, and how (record-copies yes; regenerated chapters no).

---

## (d) Is the campaign branch's relationship to `main` (founder merges winners) consistent with §1 and AGENTS.md §Workflow?

**Verdict: COMPLETES**

- **Both documents state the same split.** PROGRAM §1: "`main` carries only
  founder-merged winners; the campaign branch is created fresh from `main` when a
  campaign starts." AGENTS.md §Workflow: "each iteration runs in an isolated git
  worktree and only a KEEP is promoted to the campaign branch, one commit per
  KEPT iteration (…); only the founder merges winning amendments to `main`."
  AGENTS.md §Content Rules says the same ("winning amendments merge in
  founder-reviewed batches"). No contradiction between the two. ✓
- **The promotion target is the campaign branch, never `main`.** All of §4
  Step 6/7 promotion language targets the campaign branch; the orchestrator is
  never told to touch `main`. ✓
- **Founder inbound path from `main` to the campaign is in scope and consistent
  with the cache-era founder-inbox flow** (PROGRAM §4 Step 1 founder inbox →
  hypothesizer). The North Star's invariants are not weakened: `AUTO-TUNING-LOOP`
  step 11 "repeat until no material gap" is preserved; nothing in the worktree
  model reinterprets the role split. ✓
- **The baseline exception is consistent.** §3 runs 000 on the campaign branch
  directly (nothing to accept yet); the campaign branch still derives from
  `main`. No conflict.

**Residual note (not a verdict mover):** the campaign branch is never created in
any document, only said to be "created fresh from main when a campaign starts."
Because no `campaign-001`/`campaign-NNN` branch exists on disk and `state.md`
still says "Iteration: 000 (baseline)," the milestone at which the campaign
branch materializes (before baseline? after baseline?) is not pinned. That is a
trace-logic gap (below), not a contradiction between §1 and AGENTS.md.

---

## Cross-cutting gap uncovered by the family

**Not one of the four verdicts is BLOCKED or UNDEFINED; all four COMPLETE, with
(a)–(c) marked WITH-RISK for the same root cause.** The single structural gap
behind all three risks:

> The git worktree model is specified at the level of **intent and commit-message
> strings**, but the orchestrator has no separated blob sources and no
> commit-nomination/verification step. Because the iteration (change + records +
> generated artifacts + records-including-`change.diff`) all live on ONE branch in
> ONE worktree, the "one commit / change-only-not-promoted / right-file-set "
> guarantees in §4 Step 6/7 have no mechanical realization as written. A
> disciplined orchestrator can hand-drive the correct end state; a fresh agent
> cannot *prove* it from the program alone.

Supporting observations:
- **No automation in-tree** for the worktree mechanics: `grep` for `worktree`
  across `scripts/**/*.sh` and `*.py` finds nothing; `scripts/loop-runner/`
  contains only `web_tools.py`, `research_reuse.sh`, `daemon.sh`,
  `queue_runner.sh`, `run_preflight.sh`; `scripts/repo-push.sh` pushes `main`
  only. All worktree create/remove/promote is hand-git by the orchestrator.
- **HANDOFF.md still describes the pre-worktree commit model.** Lines "Commit
  after every stage on campaign-001" and "one commit per iteration on
  campaign-001" predate afca11f's worktree + promote-on-KEEP model and are not
  reconciled, so a fresh operator reading HANDOFF (its stated purpose) gets the
  older model. It nominates `campaign-001` as the concrete campaign-branch name —
  useful — but its per-stage-commit habit would race an in-flight iteration
  worktree if followed literally after a KEEP.
- **STATE is at baseline**; the campaign branch does not yet exist. The
  milestone for "create the campaign branch fresh from main" is not pinned in
  `state.md` or PROGRAM §3 — a small trace-logic undefinedness on the campaign
  branch's birth, resolved implicitly at baseline.

## Verdict summary

| # | Trace | Verdict |
|---|-------|---------|
| a | 001 worktree + KEEP → one-commit promotion + records merge + worktree removal | **COMPLETES-WITH-RISK** |
| b | REVERT → change not promoted, records+ledger committed | **COMPLETES-WITH-RISK** |
| c | KEEP commit = tuning change + `iterations/NNN/`, excludes strays | **COMPLETES-WITH-RISK** |
| d | campaign branch ↔ main (founder merges winners) consistent with §1 / AGENTS.md | **COMPLETES** |

## Required-action logs

**No BLOCKED. No UNDEFINED.** Three COMPLETES-WITH-RISK, one COMPLETES.

Differences between PROGRAM §4 Step 6/7's stated unit ("one commit", "records
only, never the change") and the mechanically possible git states are the source
of the three WITH-RISK marks. Recommended hardening (all are read-only findings —
no file was edited here):
1. Pin a worktree root and add per-step `git add <paths>` nominations so the
   change blob, the records blob, and the generated-artifact blob are separable.
2. Reconcile "one commit" with the co-promoted records (declare either two
   commits constituting one logical promotion, or one commit with an explicit
   path list).
3. Add a commit-content postcondition (post-promotion `git show --stat` limited
   to the editable file + records path) and a REVERT restore-and-verify step.
4. Reconcile HANDOFF.md's per-stage-commit/campaign-001 copy with the worktree +
   promote-on-KEEP model, and pin where the campaign branch is created relative
   to baseline 000.
