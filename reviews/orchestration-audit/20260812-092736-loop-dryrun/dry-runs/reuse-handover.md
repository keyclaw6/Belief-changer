# Dry Run — Research Reuse–Handover

**Audited revision:** `main` @ `afca11f` (`feat(loop): iterations run in git worktrees…`)
**Scope:** the one deterministic loop handover — `scripts/loop-runner/research_reuse.sh` — and
its integration with `loop/PROGRAM.md` §4 Step 3 ("Stage: Research") and §1 (File ownership).
**Mode:** READ-ONLY dry-run simulation. No repo files were edited. The script was executed
only in a throwaway `/tmp/rs-reuse-test/` copy. Results and verdicts below.

---

## Files read

- `scripts/loop-runner/research_reuse.sh` (script under test)
- `loop/PROGRAM.md` — §1 File ownership, §4 Step 3 (Stage: Research + Trace format), §0, §5
- `loop/config.yaml` — researcher model/route/params keys
- `loop/prompts/trace-analyzer.md` — the downstream receiver of `traces/research/`
- `prompts/master-plan-skill-v2.md` — the planner's actual research input contract
- `AGENTS.md`, `docs/VISION.md`, `loop/HANDOFF.md`, `state.md`, `reviews/…/SOURCE_OF_TRUTH.md`
  — corroboration that research-reuse is "the one deterministic handover"

---

## Trace: MECHANISM the script actually implements

`research_reuse.sh` decides **REUSE | RERUN** as a pure function of the single changed-file
path plus disk state. Two independent gates (any trigger → RERUN; no reusable research → RERUN):

**Gate 1 — trigger match** (a research trigger ⇒ RERUN):
```sh
is_research_trigger() {
  case "$1" in
    prompts/research-agent.md)      return 0 ;;
    loop/config.yaml)               return 0 ;;
    production-books/*/00-brief.md) return 0 ;;
    */00-brief.md)                  return 0 ;;
    *)                              return 1 ;;
  esac
}
```

**Gate 2 — fail-safe existence** (nothing to reuse ⇒ RERUN):
```sh
if ls production-books/*/research/ >/dev/null 2>&1 && \
   find production-books/*/research/ -type f 2>/dev/null | grep -q .; then
  echo "REUSE"
else
  echo "RERUN"
fi
```
Note: Gate 2 runs even on a REUSE-eligible binary. Logically the two are ANDed: REUSE prints
only when *not a trigger* AND *≥1 research file exists anywhere under `production-books/*/research/`*.

---

## Trace table

| # | /tmp test | repo state | cmd `changed_file` | shell result | expected | PASS? |
|---|---|---|---|---|---|---|
| 1 | style-guide.md edit, research present | seed present | `prompts/style-guide.md` | `REUSE` | REUSE | ✅ |
| 2 | master-plan-skill-v2.md edit, research present | seed present | `prompts/master-plan-skill-v2.md` | `REUSE` | REUSE | ✅ |
| 3 | chapter-writer.md edit, research present | seed present | `prompts/chapter-writer.md` | `REUSE` | REUSE | ✅ |
| 4 | master-plan-reviewer-v2.md edit, research present | seed present | `prompts/master-plan-reviewer-v2.md` | `REUSE` | REUSE | ✅ |
| 5 | **research-agent.md edit** | seed present | `prompts/research-agent.md` | `RERUN` | RERUN | ✅ |
| 6 | **loop/config.yaml edit** (researcher route/params) | seed present | `loop/config.yaml` | `RERUN` | RERUN | ✅ |
| 7 | **quit-sugar 00-brief.md edit** | seed present | `production-books/quit-sugar/00-brief.md` | `RERUN` | RERUN | ✅ |
| 8 | no resource change (empty arg), research present | seed present | `""` | `REUSE` | REUSE | ✅ |
| 9 | non-editable change (docs/AUTO-TUNING-LOOP.md), research present | seed present | `docs/AUTO-TUNING-LOOP.md` | `REUSE` | REUSE | ✅ |
| 10 | **research dir MISSING entirely** | dir removed | `prompts/style-guide.md` | `RERUN` | RERUN (fail-safe) | ✅ |
| 11 | research dir EXISTS but EMPTY | empty dir | `prompts/style-guide.md` | `RERUN` | RERUN (fail-safe) | ✅ |
| 12 | research has only subdirs, zero files | subdir only | `prompts/style-guide.md` | `RERUN` | RERUN (fail-safe) | ✅ |
| 13 | nested depth (bank `_rounds/` file) counts as research | nested file | `prompts/style-guide.md` | `REUSE` | REUSE | ✅ |
| 14 | REVERT-style deletion of research-agent.md (file gone, path still passed) | seed present | `prompts/research-agent.md` | `RERUN` | RERUN | ✅ |
| 15 | brief path for any book `production-books/_template/00-brief.md` | seed present | `production-books/_template/00-brief.md` | `RERUN` | RERUN | ✅ |
| 16 | **multi-book mask:** quit-sugar research empty, quit-porn research present | porn seeded, sugar empty | `prompts/style-guide.md` | `REUSE` ⚠️ | RERUN (fail-safe for the ACTIVE book) | ❌ |

**Test 18 (breadth):** `find production-books/*/research/ -type f 2>/dev/null` returned
`production-books/quit-porn/research/lived-experience.md` — confirming the Gate-2 glob spans
**every** book directory, not the active iteration's book. This is the one fail-safe defect.

---

## Verdicts

### (a) Hypothesis edits `prompts/style-guide.md` with research present → REUSE; copy-into-traces step defined
**COMPLETES**
Test 1 → `REUSE`. The copy-into-traces step IS defined: PROGRAM §4 Step 3 "Trace format (mandatory)"
specifies `loop/iterations/NNN/traces/research/` — "exact accepted research inputs used by this
run — **copied every iteration**; call traces added when rerun". The copied artifact is what the
trace analyzer consumes (`trace-analyzer.md` inputs item 2: "`research/` — the exact accepted
research inputs this run used"). Note: the copy-from source (`production-books/<slug>/research/`)
and the trace-analyzer consumer are each specified; the *orchestrator instruction that performs
the copy* is asserted in PROGRAM text ("copy them into this iteration's traces") rather than in a
deterministic script — consistent with the §1 doctrine "prompts over determinism". COMPLETES.

### (b) Hypothesis edits `prompts/research-agent.md`, `loop/config.yaml`, or the brief → RERUN
**COMPLETES**
Tests 5, 6, 7 → `RERUN`. Trigger list = `{prompts/research-agent.md, loop/config.yaml, */00-brief.md}`
(all live under `is_research_trigger`), which equals the §1 editorially-listed research-relevant
editable files plus the brief. Config carries `researcher_model/endpoint/auth/reasoning` +
`research_subagent_*` (verified in `loop/config.yaml` 21–30), squarely the "researcher model/params";
the brief (`production-books/<slug>/00-brief.md`) is the research prompt's scoping input (HANDOFF
lists the brief → brief is where the subject is defined). COMPLETES.

### (c) Baseline / research dir missing or empty → RERUN (fail-safe)
**COMPLETES-WITH-RISK**
Tests 10, 11, 12 → `RERUN` (fresh checkout / baseline / clean fail safe). **RISK:** the Gate-2
existence glob `production-books/*/research/` is **book-agnostic** — Test 16/18 showed that when the
active book (`quit-sugar`) has empty/no research but a *different* book (`quit-porn`) still holds
files, the script prints **REUSE** for the active iteration, defeating the fail-safe. Any change to
a book with no accepted research yet (baseline, REVERT-wiped, or a fresh subject) can be handed the
wrong book's stale research. The glob should be scoped to the active book's slug (the same
`production-books/quit-sugar/` the brief and trace format assume), or the resemblance of a
"reuse-baseline-research-from-quit-porn" mulebook is possible. Not currently a live hazard (repo is
mid-baseline-000, iterations haven't started; `state.md` says baseline research is next), but it is
the one place the "one deterministic code in the loop" can silently hand the planner wrong inputs.
FAIL-SAFE BROKEN AT EDGE; fix by passing/deriving the book slug.

### (d) Does the trigger list exactly cover the §1 editable files that affect research, no more no less?
**COMPLETES-WITH-RISK**
Direct mapping over §1's six editable files:

| §1 editable | affects research? | script trigger | consistent? |
|---|---|---|---|
| `prompts/style-guide.md` | No (style/voice only) | no | ✅ REUSE (Test 1) |
| `prompts/research-agent.md` | Yes — the research contract | yes | ✅ RERUN (Test 5) |
| `prompts/master-plan-skill-v2.md` | No — consumes research output | no | ✅ REUSE (Test 2) |
| `prompts/master-plan-reviewer-v2.md` | No | no | ✅ REUSE (Test 4) |
| `prompts/chapter-writer.md` | No | no | ✅ REUSE (Test 3) |
| `loop/config.yaml` | Yes — `researcher_*` keys | yes (whole file) | ⚠️ RISK below |

No wrong negatives detected (every research-affecting change forces a rerun). **RISK 1 — file-granularity:**
`loop/config.yaml` is one catch-all trigger, but it also holds `writer_*`, `planner_*`, `judge_*`, etc.
An edit to only the **writer** JSON block in `config.yaml` (a legitimate §1 non-research editable
hypothesis — e.g. `writer_model`) would be misclassified as a **research** trigger and force a needless
deep-research rerun. Because config mixes research and non-research keys in one file, the trigger cannot
distinguish. This breaks the "pure function of WHICH file" illusion — it's a pure function of the *whole
file*, one immutable chunk too coarse. The brief+research prompts are correct; config is one-eighth risk.
(There is no separate researcher params file — they share `loop/config.yaml`.) **RISK 2 — glob breadth** from
(c) also slightly over-triggers nothing in (d); the only over-broad trigger is Gate 2's cross-book glob,
already captured in (c).

### (e) Is the 'copy last accepted research into this iteration's traces' handoff fully specified for the receiver (planner)?
**COMPLETES-WITH-RISK**
Receiver side is well-specified:
- **Where the planner reads research from:** `prompts/master-plan-skill-v2.md` — "the accepted
  lived-experience synthesis `production-books/<slug>/research/lived-experience.md`" and "the accepted
  scientific-evidence synthesis `…/research/scientific-evidence.md`" (its initial call carries exactly
  style-guide, brief, lived-experience, scientific-evidence; PROGRAM §4 Planning: "four file inputs — …
  no reference contamination"). The planner reads the *working* research dir, not `traces/`, so a REUSE
  iteration must have already landed accepted research in `production-books/<slug>/research/` during
  baseline 000 (true) and it must be left intact across iterations (true — iterations run in git
  worktrees that branch off the campaign, per §1 State discipline).
- **The trace copy is defined:** Trace format mandates `traces/research/` "copied every iteration".
- **The trace consumer is defined:** `trace-analyzer.md` reads `traces/research/` as its research input.

**RISK (the gap):** nothing deterministically *performs* the copy and nothing names the *source path* for
a REUSE iteration. "…**copy them into this iteration's traces**" (PROGRAM §4 Step 3) reads as the
orchestrator's job, but the source is left implicit as "the last accepted research artifacts" and the copy
is a prompt-level instruction, not a `cp`. Under the §1 doctrine "prompts over determinism — deterministic
code only for…handovers", a handover that the PROGRAM itself calls out as the loop's *deterministic* one
is the very thing that would warrant code; it is currently the one handover implemented as prose. Consequence
if the orchestrator skips/mis-copies: the trace analyzer gets `traces/research/` empty-or-stale while the
planner still reads the live worktree research — a silent trace-truth gap (the analyzer's diagnosis of
"research" root cause would be built on wrong inputs). Low runtime probability (single orchestrator doing a
walked copy after a REUSE verdict), but the contract relies on prompt discipline for what the loop labels
its deterministic handover. **Fix candidates:** (i) extend `research_reuse.sh` (or a sibling
`copy_research_traces.sh`) to emit/perform `cp production-books/<slug>/research → loop/iterations/NNN/traces/research`
on a REUSE verdict — scoped to the active slug (also fixes (c)); (ii) at minimum harden the trace-format
source path and the receiver's expectation.

---

## Evidence / how verified
- Script executed in throwaway `/tmp/rs-reuse-test/` (copy of the script + a fake
  `production-books/quit-sugar/research/` tree seeded with `lived-experience.md`,
  `scientific-evidence.md`, `sources/`). All 18 branch/trace cases ran there; none touched the repo.
- Trigger gates confirmed against background truth: `loop/config.yaml` `researcher_*` keys (21–30);
  `master-plan-skill-v2.md` research input contract (11–12); trace-format + `traces/research/` comment
  (PROGRAM 266–267); `trace-analyzer.md` input 2. Cross-referenced with `SOURCE_OF_TRUTH.md` §"research
  reused unless research/brief/config changed".

## Bottom line
`REUSE`/`RERUN` decision logic and the trigger set are essentially correct and fail closed on a clean
checkout/baseline. Two residual risks, both stemming from the same root (ambiguity over *which book* and
*which granularity* constitute "the research stage"):
1. **(c)** Gate-2's cross-book glob can return REUSE for an active book with no research if any sibling
   book still has research — the fail-safe is broken at that edge.
2. **(d/e)** `config.yaml` is an all-or-nothing trigger (a writer-only config edit forces a research
   rerun), and the copy-into-traces step is prompt-level prose, not the deterministic handover code the
   PROGRAM claims; both reduce determinism exactly where this handover is supposed to be deterministic.
