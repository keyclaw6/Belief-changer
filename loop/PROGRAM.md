# Auto-Tuning Loop — PROGRAM

> The operating system for the book factory tuning loop. A coding agent reads
> this and executes it. One iteration per run. North Star: `docs/AUTO-TUNING-LOOP.md`.
> Every iteration generates and judges the WHOLE book — chapters change what
> they optimize across the arc, so partial runs measure the wrong thing.

## 0. Recovery

Read this file, `docs/AUTO-TUNING-LOOP.md`, `loop/state.md`, `loop/learnings.md`
(tail), and the last DATA row of `loop/results.tsv`, ignoring the header. If no
data row exists, state `baseline pending` and run Section 3. Otherwise state
the last completed iteration, its verdict, and the next hypothesis before
acting.

**`loop/state.md` is the live checkpoint.** Its `Status` field is exactly
`IDLE` or `IN PROGRESS` (verbatim — no other token). It governs resumption:

- **`IN PROGRESS`** — the run was interrupted in that iteration/stage. The loop
  is **single-operator**: exactly one orchestrator drives it at a time, and a
  resuming agent is by definition the only one — there is no ownership token to
  check. Continue from the last completed unit; do not restart the iteration,
  do not redo completed units. *Exception:* if `results.tsv` already holds a row
  for that same iteration, the iteration completed (Step 7 ran) and only the
  final commit may be missing — treat it as done; never re-run it.
- **`IDLE`** — no run in flight; the `results.tsv` rule above governs.

**Cross-check before resuming.** `state.md` can lag the stage it names (it is
written at boundaries, work lands between them). Before acting, confirm each
claimed completed unit against the on-disk markers — research bank files
(`research/banks/`), the accepted plan (`master-plan.md`) and its review
(`master-plan-review.md`), `production-books/quit-sugar/chapters/`,
`loop/iterations/NNN/judgments/`, `trace-analysis.md`, and `decision.md` — and
resume from the *furthest* point the markers support, not the stale marker.
Only final-named files count; a `.partial` file is unfinished work to redo
(§4 Step 3). **A baseline (000) has no `results.tsv` row until it completes, so
an interrupted baseline reads as "no data row" — in that case trust
`state.md`'s IN PROGRESS + the markers and continue the baseline in place; do
not restart it.** Also confirm you are on the right branch: iteration work
happens on the campaign branch (or the iteration branch inside its worktree),
never on `main`; `state.md` names the active campaign branch. The orchestrator
updates `loop/state.md` at every stage boundary and before every long wait (see
§4 Step 3, "Patience").

## 1. File ownership

**Editable (the tuning surface):**
- `prompts/style-guide.md`
- `prompts/research-agent.md`
- `prompts/master-plan-skill-v2.md`
- `prompts/master-plan-reviewer-v2.md`
- `prompts/chapter-writer.md`
- `loop/config.yaml` (routes, models, parameters)

Generated research, plans, and chapters under
`production-books/quit-sugar/` are **evidence, not editable hypotheses**.
A hypothesis changes the factory that produces them, never the artifact itself.

**Read-only (never edit during a campaign):**
- `calibration/reference/gsbs/` (the real book)
- `analysis/sugar-prose-patterns.md`
- `docs/AUTO-TUNING-LOOP.md`, `docs/BOOK-FACTORY-VISION.md`
- `loop/PROGRAM.md` (this file)
- `loop/judges/` (judge calibration is a separate founder-guided activity)
- `loop/reference-alignment.md` (rebuilt only when the accepted plan changes)

**Config authority:** `loop/config.yaml` is the single record of routes,
models, reasoning, and parameters for every role; the pi agent definitions in
`.pi/agents/` pin the same models. No value elsewhere overrides config.

**Role calls — every role is a spawned pi sub-agent.** The orchestrator (the
pi coding agent) runs the loop by spawning one fresh sub-agent per role with
the `subagent` tool. Each agent definition lives in `.pi/agents/` (project
scope) and is a thin wrapper: it points at its contract prompt under
`prompts/` or `loop/prompts/` — the prompts are the real tuning surface — and
pins its model per `loop/config.yaml`. Two routes (all per config): the
founder's **Command Code** proxy loopback (`COMMANDCODE_API_KEY` or the
founder's Command Code CLI login) carries ONLY the Muse Spark roles — writer,
plan-writer, hypothesizer (Muse Spark 1.2 contributor, non-contributor
fallback); the **OpenCode Zen** subscription (`OPENCODE_API_KEY`, `opencode`
route) carries every other role — research lead + sub-agents, plan-reviewer,
judges, trace-analyzer — on DeepSeek V4 Flash. A role call carries ONLY its
role prompt and the listed inputs: no host system prompt, no shared context
with sibling roles. Nothing else ever uses either route. On a route/credential
failure the run stops and escalates to the founder (the only coded fallback is
the Muse Spark contributor→non-contributor model).

Spawned roles (agent → contract prompt):
- `researcher` — `.pi/agents/researcher.md` → `prompts/research-agent.md`;
  lead and spawned research sub-agents both on DeepSeek V4 Flash (opencode)
- `plan-writer`, `plan-reviewer` — `.pi/agents/plan-*.md` →
  `prompts/master-plan-skill-v2.md` / `prompts/master-plan-reviewer-v2.md`;
  plan-writer on Muse Spark 1.2 contributor (commandcode), plan-reviewer on
  DeepSeek V4 Flash (opencode)
- `chapter-writer` — `.pi/agents/chapter-writer.md` →
  `prompts/chapter-writer.md`; Muse Spark 1.2 contributor (commandcode)
- `judge` — `.pi/agents/judge.md` → `loop/judges/*.md`; DeepSeek V4 Flash high
  via the OpenCode Zen subscription (opencode)
- `trace-analyzer` — `.pi/agents/trace-analyzer.md` → `loop/prompts/
  trace-analyzer.md`; DeepSeek V4 Flash high via opencode
- `hypothesizer` — `.pi/agents/hypothesizer.md` → `loop/prompts/
  hypothesizer.md`; Muse Spark 1.2 contributor (commandcode),
  non-contributor fallback

**The orchestrator manages the loop** (per this file): it spawns roles, hands
them their exact inputs, saves traces, and makes the intelligent decisions on
failure — retry a failed role once, then INCONCLUSIVE or escalate to the
founder. There is NO deterministic validation in the pipeline: every check of
the writer's work, the plan's resolvability, and the handovers is done by the
role agents per their prompts. The only tools the orchestrator runs are web
primitives (`scripts/loop-runner/web_tools.py`), the canonical repo gate
(`scripts/check.sh`), and the research-reuse handover
(`scripts/loop-runner/research_reuse.sh`) — the one deterministic decision in
the loop (whether research reruns), which validates nothing about the work.

**State discipline — iterations run in git worktrees.** Each iteration runs in
its own isolated worktree (a sibling directory beside the main checkout, e.g.
`../quit-sugar-iter-NNN/`), so an experimental run never touches the main
checkout and a crash leaves the tree intact for inspection. The iteration's
change and generated artifacts live in that worktree on its iteration branch.
On a **KEEP** the change is promoted to the campaign branch — one commit per
KEPT iteration (`loop(iter-NNN): KEEP — short hypothesis`). REVERT /
INCONCLUSIVE iterations are recorded (their `loop/iterations/NNN/` directory
and ledger entry) but their factory change is not promoted. `main` carries only
founder-merged winners; the campaign branch is created fresh from `main` when a
campaign starts.

**Branch + worktree mechanics.** The campaign branch is `campaign-NNN`
(`campaign-001` for the first), created from `main` at campaign start:
`git branch campaign-001 main`. Each iteration's worktree is created from the
campaign branch tip: `git worktree add ../quit-sugar-iter-NNN -b iter-NNN campaign-001`.
Inside its worktree the iteration's work (change + generated book + records) is
committed on the `iter-NNN` branch as it lands, so Step 7 can promote it with a
merge. The baseline (§3) runs directly on the campaign branch — no worktree —
and is committed there (§3 step 7). Before any Step 7 commit, confirm the
branch: `git rev-parse --abbrev-ref HEAD` must be the campaign branch (or the
iteration branch inside its worktree) — never commit iteration output on
`main`. `loop/state.md` records the active campaign branch so a resuming agent
can verify it.

## 2. Preflight — judge calibration battery

Run once before the baseline, and again after any founder edit to a judge.
Save results in `loop/preflight/`. Do not proceed while any check fails;
judge repair is founder-guided, not a loop iteration.

1. **PASS test.** Give each chapter judge one real GSBS chapter as BOTH
   "our chapter" and "the real chapter", with honest context. Run twice per
   judge. Every run must return PASS. A manufactured material gap means the
   judge cannot recognize success and must be recalibrated first.
2. **Repeatability.** Run each judge twice on one identical generated chapter
   with identical context. Same PASS/FAIL both times; for a judge that emits
   a per-moment/per-component verdict block (voice-emotion, belief-mechanic),
   the verdict lines must be identical both times, otherwise the same
   highest-impact failure class both times. If not, tighten that judge's materiality rule — do not add scoring
   machinery. [Founder amendment 2026-07-28: option C — consistency is
   measured on per-moment verdicts, matching how decisions use judge output
   (failure classes, never instances).]
3. **Voice honesty probe.** Give the voice judge six isolated passage pairs:
   two core-verdict hedges (must flag), two properly bounded empirical claims
   (must not flag), two acknowledgments of the reader's present doubt (must
   not flag).

## 3. Baseline (iteration 000)

Where is the factory now? Fresh full run, no hypothesis, no change. The
baseline establishes the accepted state — it runs directly on the campaign
branch (no worktree; there is nothing to accept or reject yet, only to
measure). Iteration worktrees begin at 001.

**First action:** begin the research stage (§4 Step 3, "Stage: Research") —
this is the opening move of the end-to-end run. At baseline nothing exists to
reuse, so `research_reuse.sh` is not consulted; research always runs at 000.

1. Run the factory END TO END per Step 3 below: research → plan →
   full book. Nothing is reused from before the campaign; the current factory
   must own every artifact and trace it produces.
2. Build `loop/reference-alignment.md` from the freshly accepted plan (its
   procedure lives in that file).
3. Judge every chapter, plus the book-arc judge (Step 4).
4. Run the trace analyzer (Step 5). Save `loop/iterations/000/trace-analysis.md`.
5. **A/A noise check (once):** regenerate chapter 01 a second time from the
   identical inputs (master plan, chapter card, style guide, previous
   chapter); judge it. If the material failure-class
   set differs between the two runs, record the observed noise level in
   `loop/learnings.md` — decisions compare failure classes, never instances,
   and this calibrates what "material" means.
6. Append a `BASELINE` row to `loop/results.tsv` and a learnings entry:
   "Baseline established. Top causal clusters: [list]."
7. **Commit the baseline onto the campaign branch** — the accepted book
   (`production-books/quit-sugar/`: research, plan, chapters) plus the
   `loop/iterations/000/` records and the `results.tsv` row
   (`loop(000): BASELINE`). The campaign-branch tip now owns the accepted
   state that every later iteration's worktree is cut from.

## 4. One iteration (001+)

### Step 1: Declare hypothesis

**Founder inbox first.** If `loop/inbox/` holds any `.md` file other than
`README.md`, the founder has proposed a hypothesis — test it before any
machine-generated one. **Oldest = the lexicographically-first filename** (name
files with a date prefix, e.g. `2026-08-12-shorten-instructions.md`, so sort
order is arrival order). One inbox note per iteration — extra notes wait for
the next iteration; they are never drained in a batch.

1. **Validate** the oldest (lexicographically-first) file against
   `loop/inbox/README.md`. If it is vague
   or multi-change, do NOT guess: move it to `loop/inbox/used/REJECTED-NNN-<name>.md`,
   note the defect to the founder, and fall through to the hypothesizer below.
2. Otherwise **feed it to the hypothesizer** (not the orchestrator) as the
   hypothesis source, alongside the normal inputs — so its never-repeat and
   one-causal-change guards still apply. The founder note supplies the change
   and rationale; the trace analysis supplies the failure evidence.
3. Save the hypothesizer's 4-field response as `loop/iterations/NNN/hypothesis.md`
   with `source: founder inbox`, and only then move the inbox file to
   `loop/inbox/used/NNN-<name>.md` (write the hypothesis first — never move
   before it is recorded).

If the inbox is empty, spawn the `hypothesizer` sub-agent (contract:
`loop/prompts/hypothesizer.md`) with:
- the previous iteration's `trace-analysis.md`
- `loop/learnings.md`
- the current editable factory files

Save its response unchanged as `loop/iterations/NNN/hypothesis.md`.

### Step 2: Apply the change

Apply the hypothesis: one causal change in one editable file (duplicate
representations of the same instruction may be replaced/deleted in the same
file). Record the diff in `loop/iterations/NNN/change.diff`.

### Step 3: Run the factory

Rerun the changed stage and every downstream stage **through full chapter
generation**. Reuse only artifacts upstream of the change. A research or
planning hypothesis is never judged without regenerated chapters.

**Patience (the runner never busy-loops).** Stages are slow — a full-book run
takes hours. When a stage or a spawned role is running, the orchestrator does
NOT poll it continuously. It updates `loop/state.md`, then waits — a long
`sleep`, a scheduled wake, or a single wait — and on waking checks the stage's
on-disk progress. **The progress markers are the real artifacts the stage
produces**: research bank files under `production-books/<slug>/research/`,
chapter files under `production-books/<slug>/chapters/`, judgment files under
`loop/iterations/NNN/judgments/`. (When a stage runs through
`daemon.sh`/`queue_runner.sh`, their `.exit` files under `.loop-work/` are an
extra completion signal — but those runners are optional and the spawned writer
produces no separate marker; the chapter file IS the marker.) New content since
the last wake = still working = wait again. There is no fixed per-stage
timeout: deep research is sacred and unlimited, so the *research* stage is
never declared stuck on elapsed time. For every other unit, stuck = no new
output artifact and no trace progress across two consecutive wakes; only then
does the orchestrator spawn a sub-agent to read the traces and confirm the
wedge. A confirmed stuck run is retried once per §1, then INCONCLUSIVE or
escalate. Doing nothing while a healthy run proceeds is correct behavior, not
a wasted wake. Update `loop/state.md` before every wait.

**A file only counts as a marker once it is complete.** The orchestrator never
writes a finished artifact straight to its final name: it writes to a temp name
(`<name>.partial`) and renames to the final name (`chapter-NN.md`,
`lived-experience.md`, a judgment report) only when the content is fully
written. When a spawned role returns content (e.g. a chapter), the orchestrator
holds it and writes the final file itself — so the convention covers
sub-agents too. On resume, a `.partial` file is unfinished work — discard it
and redo that unit; only the final-named file marks a completed unit. This is
how a crash mid-write can never leave a truncated file reading as done.

**Research reuse is the one deterministic handover.** Whether the research
stage reruns is decided by `scripts/loop-runner/research_reuse.sh`
(unchanged hypothesis+brief ⇒ reuse), the only deterministic code in the loop.

**Stage: Research** — rerun ONLY when the hypothesis changed the research
stage (research prompt, researcher model/params) or the
brief. Deep research is slow; when unchanged, reuse the last accepted
research artifacts and copy them into this iteration's traces.
- The orchestrator (the pi coding agent) IS the research lead. It reads
  `prompts/research-agent.md`, fills the parameter block, **names the persona
  set** (§7 of the research prompt), and runs one
  relentless search for depth: it searches and fetches itself via
  `scripts/loop-runner/web_tools.py`, and spawns fresh research sub-agents
  with the `subagent` tool (project agent `.pi/agents/researcher.md`,
  parallel mode) per lane, persona, and community. Each sub-agent mines and
  appends source-traceable packets into its bank file under
  `research/banks/` *as it works* — so a crash loses nothing already mined.
  The orchestrator integrates, names the gaps, and dispatches again — until the
  completion criterion in the research prompt clears across at least three
  personas. Lived experience from recovery communities is the primary
  target; scientific studies are secondary.
- Route/model per config (researcher model via the Command Code proxy).
- Depth is sacred and unlimited: go as wide and deep as still brings
  results; filter afterwards, never limit upfront.
- Output: `production-books/quit-sugar/research/` (banks under
  `research/banks/`; the synthesis writes `lived-experience.md`,
  `scientific-evidence.md`, `research-log.md`, `sources/`).

**Stage: Planning** — the orchestrator spawns the `plan-writer` sub-agent
(follows `prompts/master-plan-skill-v2.md`; the initial call carries exactly
four file inputs — style guide, brief, lived-experience, scientific-evidence
— no reference contamination), then the `plan-reviewer` sub-agent
(`prompts/master-plan-reviewer-v2.md`). On `needs changes first`, the
orchestrator passes the current candidate plan and the reviewer's findings
to a fresh `plan-writer` call, then dispatches a fresh reviewer; repeat until
`master-plan-review.md` ends `fit to write from`. When the accepted plan
changed, rebuild `loop/reference-alignment.md` before judging.

**Stage: Writing (sequential, chapter 01 → last)** — the orchestrator spawns
the `chapter-writer` sub-agent one chapter at a time, in order, until the
book is complete. Each spawn receives exactly four inputs, with
`prompts/chapter-writer.md` as the contract:
  1. The accepted master plan (its card for chapter N is the semantic
     authority; the plan-wide inventories resolve every ID the card cites)
  2. The target chapter card for chapter N (from the plan)
  3. The style guide: `prompts/style-guide.md`
  4. The previous chapter (for chapter 01: the plan's book-core section)
Output: `production-books/quit-sugar/chapters/chapter-NN.md`

**Trace format (mandatory):**
```
loop/iterations/NNN/traces/
  research/              # exact accepted research inputs used by this run —
                         # copied every iteration; call traces added when rerun
  plan.md                # accepted master plan used (copy)
  chapter-01/
    chapter-card.md      # the target chapter card used (copy)
    prompt.md            # exact system + user message sent to writer
    response.md          # exact model response
    metadata.json        # model, tokens, latency, errors
  chapter-02/ ...
```

**Error handling:**
- Sub-agent failure (transport error, invalid/truncated response, refused
  spawn): the orchestrator retries the role once with the same inputs. Still
  failing → iteration INCONCLUSIVE, or escalate to the founder when the
  failure is a route/credential problem.
- Writer refusal: the exact refusal line is saved to
  `traces/chapter-NN/refusal.md`; no chapter file is written; the refusal's
  named owner is the iteration's finding; iteration INCONCLUSIVE.
- Never skip a chapter and continue to a decision. Every error is logged.

### Step 4: Judge

**Chapter judges** — run all three on EVERY generated chapter against its
aligned GSBS chapter (`loop/reference-alignment.md`; WEAK alignments are
judged lightly per that file):
- `loop/judges/belief-mechanic.md`
- `loop/judges/voice-emotion.md`
- `loop/judges/reader-journey.md`

Each judge receives: the judge prompt, our chapter, the aligned real chapter,
CHAPTER CONTEXT (below), and for chapters 2+ the previous chapter.

**CHAPTER CONTEXT (copy from the accepted plan's chapter card — never
improvise):**
```
Chapter [N] of [total] — [card ID and working title].
Primary job: [the card's primary persuasive job declaration]
Entering belief: [card's entering belief]
Leaving belief: [card's leaving belief]
Arc and curve position: [card's arc position and qualitative curve position]
Continuity: [assumptions handed forward by the previous card; NONE for chapter 1]
Assigned compliance:
- Instruction: [exact frozen wording from the instruction spine, or NONE]
- Mantras: [exact frozen wording of each mantra assigned here, marked debut or echo, or NONE]
```

**Book judge** — run `loop/judges/book-arc.md` once on the complete book
(all chapters in order) with the plan's mantra sheet, instruction spine,
and curve map, plus the reference-alignment table as the GSBS skeleton.

All judges, the trace analyzer, and the hypothesizer are spawned sub-agents
(see Role calls, §1). Judge calls are independent — the orchestrator spawns
them in parallel.
A judge that fails is rerun once; a still-missing report blocks any KEEP
(the iteration is INCONCLUSIVE) but its diagnostic value is still recorded.

Save verdicts in `loop/iterations/NNN/judgments/`.

### Step 5: Trace analysis

Spawn the `trace-analyzer` sub-agent on the judgments and the exact
generation traces. Save its response as `loop/iterations/NNN/trace-analysis.md`.
It merges corroborating reports into causal clusters and maps each cluster to
the factory component that caused it. Diagnosis lives there, not in judge
reports.

### Step 6: Decide

A decision is valid only when every judge report completed (after retries).
Otherwise the
iteration is INCONCLUSIVE — never decide on partial evidence.

Answer one question: **did the predicted causal cluster close?**

- The judge lane that owns the targeted cluster decides whether it closed.
- Other lanes may veto only a material REGRESSION in their own lane:
  a NEW material failure class, absent from the previous iteration and
  evidenced by a quoted current passage. Re-worded, re-ordered, or re-ranked
  findings about a known problem are not regressions. Judge instances are
  noise; failure classes are signal.
- No voting, no averaging.

Verdicts:
- **KEEP** — the targeted cluster improved materially AND no lane shows a
  material regression. Improvement arriving through an unpredicted mechanism
  is still KEEP; record the prediction as wrong.
- **REVERT** — the targeted cluster did not improve, OR a material
  regression appeared.
- **INCONCLUSIVE** — invalid evidence, or no improvement and no regression.

KEEP: the iteration's change is the new accepted state — promote it to the
campaign branch (Step 7) **and commit the accepted book (chapters + research)
with it**, so the winning book survives worktree removal. REVERT /
INCONCLUSIVE: the change is not promoted — the iteration's worktree and its
factory change are discarded, but the iteration directory
(`loop/iterations/NNN/`) and the ledger entry are always kept on the campaign
branch so the campaign never re-tries a failed hypothesis blindly.

Record prediction accuracy: "Predicted X. Observed Y. [accurate/partial/wrong]."
Write `loop/iterations/NNN/decision.md` with the verdict and reasoning.

### Step 7: Record

Append to `loop/learnings.md`:
```
### iter-NNN — [short title]
**Hypothesis:** [one line]
**Change:** [file + what changed]
**Verdict:** BASELINE/KEEP/REVERT/INCONCLUSIVE
**Lesson:** [what we learned about the factory]
**Next direction:** [what to try next based on this]
```

Append one entry to `loop/ledger.md` — the explanatory experiment ledger —
using the entry format in that file: Hypothesis, Change, What happened (the
evidence, quoted), Verdict & why, What we learned, and **What this opens
next**. `results.tsv` is canonical; `learnings.md`'s Lesson is what the
hypothesizer reads; `ledger.md` is the explanation a reader uses to decide the
next move. `ledger.md` is append-only: never edit a past entry, corrections
become a new entry.

**Write the `results.tsv` row LAST.** The learnings and ledger entries land
first; the `results.tsv` row is the completion marker §0 checks, so append it
only after every other record is written — that way a mid-Step-7 crash can
never leave an iteration looking done while its learnings are missing. Append
one tab-separated data row matching the existing header. Do not append the
header again.

Mark the iteration done in `loop/state.md` (status `IDLE`, last completed unit
= iteration NNN decision). The commit lands on the campaign branch; how it gets
there depends on the verdict — never `git add -A`:

- **KEEP** — promote from the iteration worktree onto the campaign branch:
  `git checkout campaign-001` in the main checkout, then
  `git merge --no-ff iter-NNN` (or `git checkout iter-NNN -- <paths>` for the
  pinned set below). One commit (`loop(iter-NNN): KEEP — short hypothesis`)
  carrying: the one edited tuning file, the iteration records
  (`loop/iterations/NNN/`, the `results.tsv` row, the `learnings.md` and
  `ledger.md` entries, `loop/state.md`), and the accepted book —
  `production-books/<slug>/chapters/` and `research/` — so the winning book
  survives removal of the worktree. Nothing else.
- **REVERT / INCONCLUSIVE** — do NOT merge the iteration branch. On the
  campaign branch, commit only the records (`loop/iterations/NNN/`,
  `results.tsv`, `learnings.md`, `ledger.md`, `state.md`) — never the factory
  change or the rejected book.

After committing, verify with `git show --stat` that the file set matches and
holds no stray artifact. Remove the iteration worktree and its branch once the
campaign branch carries what it should.

## 5. Rules

- **One causal change per iteration.** One file. Duplicate representations of
  the same instruction may be normalized together. Never a second behavior.
- **3-strike rule.** Failure class = same causal cluster + same root
  component. If 3 iterations targeting one class produce no KEEP, PIVOT to a
  different component level (prompt → structure → model → research). The
  level is wrong; stop hammering it.
- **Convergence rule.** After 5 consecutive iterations with no KEEP, stop.
  Write `loop/iterations/NNN/convergence-report.md` and surface to the
  founder.
- **Judge separation.** Never edit judges during an iteration. A suspected
  judge defect stops the campaign; the judge is repaired separately
  (founder-guided, re-run Preflight) and a fresh baseline is established.
- **Never edit this PROGRAM.md.** The loop follows it; it does not change it.
- **Prediction informs, evidence decides.** Wrong prediction + real
  improvement = KEEP (note it). Right prediction + no improvement = REVERT.
- **Iterations are slow on purpose.** A full-book run takes hours. Prefer
  one well-evidenced hypothesis over three shallow ones.
- **Single operator.** One orchestrator drives the loop at a time; resume
  always continues from the on-disk markers. Deferred founder decisions (e.g.
  stop-guard authority, unbounded sub-loops) live in `loop/open-questions.md`.

## 6. Generalization check

After the panel finds no material gap on the quit-sugar book:

1. Create `production-books/quit-smoking/` with a brief for smoking cessation
2. Run the factory END TO END with ZERO subject-specific tuning
3. Judge against a smoking reference if the founder supplies one; otherwise
   the panel judges against the Carr method definitions in the judge prompts
   (generalization only — calibration judging always uses the real book)
4. If it passes: the factory works. If not: continue tuning with both
   subjects as signal.

## 7. What success looks like

The loop succeeds when:
1. The panel — three chapter lanes and the book lane — finds no material gap
   in belief-change work, reader-state transition, or voice effect between
   our book and GSBS
2. The factory produces a convincing Carr-style book for a novel subject
   with zero subject-specific tuning
3. `loop/learnings.md` explains WHY the factory works, not just THAT it works
