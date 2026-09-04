# Auto-Tuning Loop — PROGRAM

> The operating system for the book factory tuning loop. A coding agent reads
> this and executes it. One iteration per run. North Star: `docs/AUTO-TUNING-LOOP.md`.
> Every iteration generates and judges TWO independent whole books from the
> same plan (replicate A and B) — chapters change what they optimize across
> the arc, so partial runs measure the wrong thing, and a single book
> confuses writer/judge noise with a real effect.

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
(`master-plan-review.md`), `loop/iterations/NNN/replicate-{a,b}/chapters/`,
`loop/iterations/NNN/replicate-a/judgments/` and `replicate-b/judgments/`,
`trace-analysis.md`, and `decision.md` — and
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
- `loop/config.yaml` (non-model parameters only — reasoning, search/fetch
  limits). **Never** `*_model`, `*_fallback_model`, `*_route`, or endpoint
  fields. Models and routes are founder-only.

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

**Config authority:** `loop/config.yaml` holds the founder's preferred role
defaults (models, routes, parameters). Models and routes are **founder-only**
— the loop may not hypothesize or apply a change to them. Remaining config
parameters (reasoning, research depth) stay on the tuning surface. A harness
maps each role to the model it can reach (see `loop/HARNESS.md`); the pi
adapter (`.pi/agents/`) pins the same defaults. Config guides; the harness's
trace `metadata.json` records what actually ran.

**Role calls — every role is a spawned sub-agent, in any harness.** The
orchestrator (whatever agent is running the loop) spawns one fresh sub-agent
per role using the harness's spawn capability. The role contract prompts under
`prompts/` and `loop/prompts/` and `loop/judges/` are the portable,
harness-neutral artifact. (In the pi harness, a role is realized via the
`subagent` tool and the thin `.pi/agents/*.md` adapter; another harness spawns
the same contract prompts directly.) The role→capability map, the spawn
contract, and per-harness bindings live in `loop/HARNESS.md`. **Pi harness:**
before the first Muse Spark spawn, export
`PI_PROVIDER_FALLBACK_CONFIG` to this repo's `.pi/provider-fallback.json`
(so `pi-provider-fallback` loads the Go→Zen→Vercel chain; without the export
the plugin looks in `~/.pi/agent/extensions/` and stays disabled). On a route, quota, or unavailable failure the orchestrator
retries that same unit once on the role's `*_fallback_model` (Muse Spark:
OpenCode Go `muse-spark-1.3-contributor` → Zen
`muse-spark-1.3-contributor-free` → Vercel
`meta/muse-spark-1.3-contributor`). The next unit always starts on the
primary — fallback is per-call, never sticky. All routes failing → stop
and escalate to the founder. Never swap contributor → non-contributor
(same weights, ~20× cost). The hypothesizer never proposes a model,
fallback, or route change.

Spawned roles (role → contract prompt):
- `researcher` — `prompts/research-agent.md` (lead) + research sub-agents
- `plan-writer`, `plan-reviewer` — `prompts/master-plan-skill-v2.md` /
  `prompts/master-plan-reviewer-v2.md`
- `chapter-writer` — `prompts/chapter-writer.md`
- `chapter-reviewer` — `prompts/chapter-reviewer.md` (one review, one rewrite)
- `judge` — `loop/judges/*.md`
- `trace-analyzer` — `loop/prompts/trace-analyzer.md`
- `hypothesizer` — `loop/prompts/hypothesizer.md`

**The orchestrator manages the loop** (per this file): it spawns roles, hands
them their exact inputs, saves traces, and makes the intelligent decisions on
failure — retry a failed role once on the primary, then once on the
fallback if the role has one and the error is route/quota/unavailable,
then INCONCLUSIVE or escalate to the founder. There is NO deterministic validation in the pipeline: every check of
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

Run once before the baseline, and again after any founder edit to a judge **or
any change of harness or judge model** (repeatability is sampling-sensitive).
Spawn the judge role for each check below per the harness's spawn capability
(in pi: `scripts/loop-runner/run_preflight.sh`). **A non-pi harness must NOT run
`run_preflight.sh`** (it is pi-CLI-bound) — instead it spawns the `judge` role
directly against the inputs in `loop/preflight/inputs/` per the checks below
(18 judge calls: 6 PASS-test, 6 repeatability, 6 voice-probe) and writes the
results to `loop/preflight/`. **Re-running after a model/harness change:** the
runner skips any check whose `response.md` already exists, so a stale battery
would be silently reused — run preflight into a FRESH directory instead
(`PREFLIGHT_RUNS_DIR=loop/preflight/runs-<date>-<model>`), never into one with
old results. Save results in
`loop/preflight/`. Do not proceed while any check fails; judge repair is
founder-guided, not a loop iteration.

1. **PASS test.** Give each chapter judge one real GSBS chapter as BOTH
   "our chapter" and "the real chapter", with honest context. Run twice per
   judge. Every run must return PASS. A manufactured material gap means the
   judge cannot recognize success and must be recalibrated first.
2. **Repeatability.** Run each judge twice on one identical generated chapter
   with identical context. Same PASS/FAIL both times; the BLOCKING class set
   in `CLUSTER CENSUS` must be identical. NOTED counts may differ by ±1 per
   class. If not, tighten that judge's blocking test — do not add scoring
   machinery. [Founder amendment 2026-08-24: KEEP reads census classes,
   not chapter PASS rate; repeatability matches that object.]
3. **Voice honesty probe.** Give the voice judge six isolated passage pairs:
   two core-verdict hedges (must BLOCKING `assigned-verdict-hedge`), two
   properly bounded empirical claims (must not FAIL), two acknowledgments of
   the reader's present doubt (must not FAIL). Noted classes on P3–P6 must
   not flip the probe to FAIL.
4. **Belief/journey honesty probe.** Six calls on isolated passage pairs
   (do not flag missing chapter anatomy). Belief-mechanic: `probe-b1-credit-intact.md`
   (must BLOCKING `credit-intact`), `probe-b2-harm-not-belief.md` (must
   BLOCKING `harm-not-belief`), `probe-b3-bounded-pass.md` (must PASS).
   Reader-journey: `probe-j1-transition-incomplete.md` (must BLOCKING
   `journey-incomplete`), `probe-j2-pass.md` (must PASS). Repeat b1 once
   for repeatability. This is a battery addition, not a judge-prompt edit,
   and does not by itself require replaying the 18-call calibration. If a
   must-FAIL probe PASSes, the lane is at ceiling — founder-guided repair,
   then the full 18+6 battery in a fresh runs dir.

## 3. Baseline (iteration 000)

Where is the factory now? Fresh full run, no hypothesis, no change. The
baseline establishes the accepted state — it runs directly on the campaign
branch (no worktree; there is nothing to accept or reject yet, only to
measure). Iteration worktrees begin at 001.

**First action:** create the campaign branch from `main` and move onto it
(`git branch campaign-001 main && git checkout campaign-001`) — all baseline
work lands here, never on `main`. Then begin the research stage (§4 Step 3,
"Stage: Research") — this is the opening move of the end-to-end run. At
baseline nothing exists to reuse, so `research_reuse.sh` is not consulted;
research always runs at 000.

1. Run the factory END TO END per Step 3 below: research → plan →
   two independent full books (replicate A and B concurrently) from that
   one plan. Nothing is reused from before the campaign; the current factory
   must own every artifact and trace it produces.
2. Build `loop/reference-alignment.md` from the freshly accepted plan (its
   procedure lives in that file). **The orchestrator builds this table itself** —
   it is not a spawned role: read each plan card's belief-work and the GSBS
   chapters, map by belief-move, fill the table before any judging.
3. Judge every chapter of **both** replicates, plus the book-arc judge on
   each complete book (Step 4).
4. Run the trace analyzer (Step 5) on **both** replicates. Save
   `loop/iterations/000/trace-analysis.md`.
5. **Noise floor:** the two baseline books are the A/A check. If the
   material failure-class set differs between replicate A and B, record
   that observed noise in `loop/learnings.md` — decisions compare failure
   classes that appear in **both** books, never a class that appears in only
   one. Do not regenerate a third chapter-01; two full books replace the
   old single-chapter A/A.
6. Append a `BASELINE` row to `loop/results.tsv` and a learnings entry:
   "Baseline established. Top causal clusters: [list]. Noise floor: [A vs B]."
7. **Commit the baseline onto the campaign branch** — the accepted book
   (`production-books/quit-sugar/`: research, plan, and the chapters of
   replicate A as the accepted snapshot) plus the `loop/iterations/000/`
   records (both replicates) and the `results.tsv` row
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
   `loop/inbox/README.md`. If it is vague, or multi-change without one
   change marked PRIMARY and each change bound to a census class, do NOT
   guess: move it to `loop/inbox/used/REJECTED-NNN-<name>.md`,
   note the defect to the founder, and fall through to the hypothesizer below.
2. Otherwise **feed it to the hypothesizer** (not the orchestrator) as the
   hypothesis source, alongside the normal inputs — so its convergence-budget
   and founder-only-model guards still apply. The founder note supplies the
   change and rationale; the trace analysis supplies the failure evidence.
3. Save the hypothesizer's 4-field response as `loop/iterations/NNN/hypothesis.md`
   with `source: founder inbox` (and `hypothesis-metadata.json` `{model, harness,
   spawn}`), and only then move the inbox file to
   `loop/inbox/used/NNN-<name>.md` (write the hypothesis first — never move
   before it is recorded).

If the inbox is empty, spawn the `hypothesizer` sub-agent (contract:
`loop/prompts/hypothesizer.md`) with:
- the previous iteration's `trace-analysis.md`
- `loop/learnings.md`
- the current editable factory files

The orchestrator writes `loop/iterations/NNN/hypothesis.md` unchanged and
`loop/iterations/NNN/hypothesis-metadata.json` `{model, harness, spawn}`.

### Step 2: Apply the change

Apply the hypothesis's 1–3 bound changes, each one instruction in one
editable file (≤ 3 files), per the convergence budget in
`loop/prompts/hypothesizer.md`. Record the diff in
`loop/iterations/NNN/change.diff`.

### Step 3: Run the factory

Rerun the changed stage and every downstream stage **through full chapter
generation, twice**. Reuse only artifacts upstream of the change. A research or
planning hypothesis is never judged without regenerated chapters.

**Two-book replicate (mandatory).** After the accepted plan is in hand,
write and judge the book twice from those identical inputs (master plan,
chapter cards, style guide). Research still runs once (reuse rule below).
Planning still runs once — two plans would produce two different books and
make cluster comparison unmeasurable. The two writes are replicate A and
replicate B in parallel (founder authorized, 2026-09-04):

1. Write A and B concurrently, each into its own
   `loop/iterations/NNN/replicate-{a,b}/chapters/` (chapters 01 → last).
   No extra git worktrees.
2. Judge A when write A's runner exits; judge B when write B's exits.
   Do not wait for both writes before starting the first judge.
3. Live `production-books/quit-sugar/chapters/` stays untouched until
   Step 6 (KEEP copies replicate A).

Within one book, chapters stay sequential (01 → last).

Each replicate is a complete book. Do not skip replicate B. Do not judge
only one book and call the other a check. The pair is the measurement.

**Patience (the runner never busy-loops).** Stages are slow — a full-book run
takes hours. When a stage or a spawned role is running, the orchestrator does
NOT poll it continuously. It updates `loop/state.md`, then waits — a long
`sleep`, a scheduled wake, or a single wait — and on waking checks the stage's
on-disk progress. **The progress markers are the real artifacts the stage
produces**: research bank files under `production-books/<slug>/research/banks/`,
chapter files under `loop/iterations/NNN/replicate-{a,b}/chapters/`, judgment files under
`loop/iterations/NNN/replicate-a/judgments/` and
`replicate-b/judgments/`. (The spawned writer produces no separate
marker; the chapter file IS the marker.) New content since
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
research artifacts and copy them into each replicate's `traces/research/`.
- The orchestrator IS the research lead. It reads
  `prompts/research-agent.md`, fills the parameter block, **names the persona
  set** (§7 of the research prompt), and runs one
  relentless search for depth: it searches and fetches itself via
  `scripts/loop-runner/web_tools.py` (or the harness's native search/fetch),
  and spawns fresh research sub-agents via the harness's spawn capability (pi
  example: the `subagent` tool with `.pi/agents/researcher.md`, parallel mode)
  per lane, persona, and community. Each sub-agent mines and
  appends source-traceable packets into its bank file under
  `research/banks/` *as it works* — so a crash loses nothing already mined.
  The orchestrator integrates, names the gaps, and dispatches again — until the
  completion criterion in the research prompt clears across at least three
  personas. Lived experience from recovery communities is the primary
  target; scientific studies are secondary.
- Route/model per config (preferred default; resolved per-harness, HARNESS.md).
- Depth is sacred and unlimited: go as wide and deep as still brings
  results; filter afterwards, never limit upfront.
- Output: `production-books/quit-sugar/research/` (banks under
  `research/banks/`; the synthesis writes `lived-experience.md`,
  `scientific-evidence.md`, `research-log.md`, `sources/`).
- **Pre-existing research:** research produced before the `research/banks/`
  layout may sit at `research/` root or under `research/_rounds/` with no
  `banks/` dir. Treat any real content there as already-mined evidence —
  integrate it and re-dispatch only what's still thin; never re-mine from zero
  just because the layout predates `banks/`.

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
Then the orchestrator spawns `chapter-reviewer` (`prompts/chapter-reviewer.md`)
on that draft with exactly: accepted plan, chapter card, draft text, and
one line `Delivered N words. Budget B.` Never GSBS, never a judge prompt,
never the style guide, never the previous chapter. `ACCEPT` keeps the draft.
`REVISE` triggers one writer rewrite (original four inputs + draft + review).
The rewrite is final. Cursor: `write_replicate.py` runs draft → review →
≤1 rewrite. Traces: `draft.md`, `review.md`, `rewrite-prompt.md`.
Output: `loop/iterations/NNN/replicate-{a,b}/chapters/chapter-NN.md`

**Trace format (mandatory):**
```
loop/iterations/NNN/
  replicate-a/
    traces/
      research/            # exact accepted research inputs used by this run
      plan.md              # accepted master plan used (copy)
      chapter-01/
        chapter-card.md
        prompt.md
        response.md
        metadata.json      # model, tokens, latency, errors; record fallback if used
      chapter-02/ ...
    judgments/
    chapters/              # writer output (previous-chapter source)
  replicate-b/
    traces/ ...
    judgments/
    chapters/
```
Shared (once per iteration, not per replicate): `hypothesis.md`,
`change.diff`, `trace-analysis.md`, `decision.md`.

**Error handling:**
- Sub-agent failure (transport error, invalid/truncated response, refused
  spawn): the orchestrator retries the role once with the same inputs on the
  primary model. If that retry fails with a route, quota, or unavailable
  error AND the role has a `*_fallback_model` in config, retry the same unit
  once on the fallback. Muse Spark 429s retry on that route (up to 4 × 90s)
  then fall to the next in the Go → Zen → Vercel chain; 403/401/402 fall
  through immediately. Record the model and `failed_routes` that actually
  ran in that unit's `metadata.json`. The next unit always starts on the
  primary. Still failing on all routes → iteration INCONCLUSIVE, or
  escalate to the founder when all routes are credential/route failures.
  Never fall back to a non-contributor `meta/muse-spark-*` alias.
- Judge failure: retryable unit failure (`.partial` only, no `response.md`); the runner waits for each `agent` to exit, retries once, then re-invoke fills gaps.
- Writer refusal: the exact refusal line is saved to
  `traces/chapter-NN/refusal.md` under the current replicate; no chapter file
  is written; the refusal's named owner is the iteration's finding;
  iteration INCONCLUSIVE.
- Never skip a chapter and continue to a decision. Every error is logged.

### Step 4: Judge

**Chapter judges** — run all four on EVERY generated chapter against its
aligned GSBS chapter (`loop/reference-alignment.md`; WEAK alignments are
judged lightly per that file):
- `loop/judges/belief-mechanic.md`
- `loop/judges/voice-emotion.md`
- `loop/judges/reader-journey.md`
- `loop/judges/chapter-comparison.md` (belief-moves from
  `loop/reference-moves.md`; lecture lines are hypothesizer/trace input,
  never writer/reviewer input)

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

**Book judge** — run `loop/judges/book-arc.md` once per replicate on that
complete book (all chapters in order) with the plan's mantra sheet, instruction
spine, and curve map, plus the reference-alignment table as the GSBS skeleton.

All judges, the trace analyzer, and the hypothesizer are spawned sub-agents
(see Role calls, §1). Judge calls are independent — the orchestrator spawns
them in parallel.
A judge that fails is rerun once; a still-missing report on **either**
replicate blocks any KEEP (the iteration is INCONCLUSIVE) but its diagnostic
value is still recorded.

Save verdicts in `loop/iterations/NNN/replicate-a/judgments/` and
`loop/iterations/NNN/replicate-b/judgments/`. Judge replicate A as soon as
its chapters exist; do not wait for B to start A's panel.

### Step 5: Trace analysis

Spawn the `trace-analyzer` sub-agent on **both** replicates' judgments and
generation traces. Save its response as `loop/iterations/NNN/trace-analysis.md`.
It merges corroborating reports into causal clusters and maps each cluster to
the factory component that caused it. A cluster that appears in both
replicates is signal; a cluster that appears in only one is noise and must
not drive KEEP, REVERT, or the next hypothesis. Diagnosis lives there, not
in judge reports.

### Step 6: Decide

A decision is valid only when every judge report completed on **both**
replicates (after retries). Otherwise the
iteration is INCONCLUSIVE — never decide on partial evidence or on one book.

Answer one question: **did the predicted causal cluster improve materially
in both books?** Named-symptom close counts. The class does not have to leave
the owning lane's FAIL set.

- The judge lane that owns the targeted cluster decides whether it improved,
  from `CLUSTER CENSUS` class counts (blocking + noted of that class,
  summed across chapters) in both books — not from that lane's chapter
  PASS rate. Named-symptom close counts. A drop in a NOTED class in both
  books is improvement even if PASS/N is unchanged or worse.
  [Founder amendment 2026-09-04 — instrument halt after 020–024:]
  **Materially** means beyond the `_shared.md` book-level noted band,
  rate-normalized: a same-n drop of 1 is not improvement; a drop of 2+
  at the same chapter count is; when chapter counts differ, compare
  rates (count / n) and require a rate drop greater than `1 / n_old`.
  7→6 / 5→5 / 5→7 are REVERT, not INCONCLUSIVE.
  [Founder amendment 2026-09-04 night — Carr convergence:]
  KEEP also requires both books' delivered word total ≥ 80% of the plan
  total (orchestrator sums `metadata.json` `words_final`; judges never
  score length). PRIMARY may be a census class (band rules) **or**
  comparison `missing` falling by ≥2 at the same chapter count in both
  books. Hypothesizer order: blocking → comparison missing-in-both →
  noted ≥8 both.
  - **both improved (beyond the band)** → candidate KEEP
  - **neither improved (both inside the band or flat/up)** → candidate REVERT
  - **one improved beyond the band, one did not** → INCONCLUSIVE (sampling noise)
- Other lanes may veto only a material REGRESSION that appears in **both**
  replicates: a NEW **BLOCKING** class *name* that was 0 last iteration and
  is >0 in both new books. A new scene ID under `re-argument` is not a new
  class.
- No voting, no averaging of PASS rates.

Verdicts:
- **KEEP** — both replicates show the targeted cluster improved materially
  AND neither book-pair shares a new material failure class. Improvement
  arriving through an unpredicted mechanism is still KEEP; record the
  prediction as wrong. Promote the factory change. Copy the chapters of
  replicate A into `production-books/<slug>/chapters/` (A is the accepted
  snapshot; B remains evidence under `loop/iterations/NNN/replicate-b/`)
  unless an untargeted systemic class still dominates **both** new books at
  scale (record that exception and keep those chapters only under
  `loop/iterations/NNN/`). Promote `research/` with the factory change.
- **REVERT** — neither replicate shows the targeted cluster improved, OR
  both replicates show the same new material failure class.
- **INCONCLUSIVE** — invalid evidence, the two books disagree on whether
  the cluster improved, or a would-be new class appears in only one book.

KEEP: the factory change is the new accepted state — promote it to the
campaign branch (Step 7). REVERT /
INCONCLUSIVE: the change is not promoted — the iteration's worktree and its
factory change are discarded, but the iteration directory
(`loop/iterations/NNN/`) and the ledger entry are always kept on the campaign
branch so later iterations know what was tried and under which instrument.
REVERT is not a ban: a reverted factory change remains eligible, including
exact prior wording, especially after a judge change. Do not blindly re-run
the identical hypothesis against the same census class on the same
instrument without a new mechanism. Founder-only model/route swaps stay
forbidden.

Record prediction accuracy: "Predicted X. Observed Y (A: …; B: …). [accurate/partial/wrong]."
Write `loop/iterations/NNN/decision.md` with the verdict, both replicates'
evidence, and reasoning.

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
  carrying: the edited tuning files (≤ 3), the iteration records
  (`loop/iterations/NNN/`, the `results.tsv` row, the `learnings.md` and
  `ledger.md` entries, `loop/state.md`), and — unless Step 6 recorded that
  an untargeted systemic class still dominates the new book — the accepted
  book (`production-books/<slug>/chapters/` and `research/`). Nothing else.
- **REVERT / INCONCLUSIVE** — do NOT merge the iteration branch. On the
  campaign branch, commit only the records (`loop/iterations/NNN/`,
  `results.tsv`, `learnings.md`, `ledger.md`, `state.md`) — never the factory
  change or the rejected book.

After committing, verify with `git show --stat` that the file set matches and
holds no stray artifact. Remove the iteration worktree and its branch once the
campaign branch carries what it should.

## 5. Rules

- **Convergence budget.** Up to 1–3 bound changes per the budget in
  `loop/prompts/hypothesizer.md`. KEEP/REVERT read the PRIMARY class only.
  One-book blocking on a non-primary class is logged, never a veto. A new
  blocking class in BOTH books is REVERT.
- **3-strike rule.** Failure class = same PRIMARY class + same root
  component, counted only under one judge instrument. If 3 iterations
  with the same PRIMARY class + root component produce no KEEP, PIVOT
  to a different component level (prompt → structure → research). Never
  pivot to a model change; stop and surface to the founder. The level is
  wrong; stop hammering it. A judge change resets the clock — 001–008
  3-strike/PIVOT notes do not bind 009 onward. A re-baseline after a
  founder model change resets the clock (as 009). REVERT never deletes
  an idea.
- **Never change models.** Hypothesizer and orchestrator must not edit
  `*_model`, `*_fallback_model`, `*_route`, or endpoint fields in
  `loop/config.yaml`. Models are founder-only.
- **Convergence rule.** After 5 consecutive iterations with no KEEP, stop.
  Write `loop/iterations/NNN/convergence-report.md` and surface to the
  founder.
- **Judge separation.** Never edit judges during an iteration. A suspected
  judge defect stops the campaign; the judge is repaired separately
  (founder-guided, re-run Preflight) and a fresh baseline is established.
- **Never edit this PROGRAM.md.** The loop follows it; it does not change it.
- **Prediction informs, evidence decides.** Wrong prediction + real
  improvement in both books = KEEP (note it). Right prediction + no
  improvement in both books = REVERT. The two books disagree = INCONCLUSIVE.
  "Improvement" uses the Step 6 band (founder 2026-09-04): ±1 at the same
  chapter count is not disagreement — it is REVERT.
- **Iterations are slow on purpose.** A two-book run takes longer than a
  one-book run. Prefer one well-evidenced hypothesis over three shallow ones.
- **Single operator.** One orchestrator drives the loop at a time; resume
  always continues from the on-disk markers. Deferred founder decisions (e.g.
  stop-guard authority, unbounded sub-loops) live in `loop/open-questions.md`.

## 6. Generalization check

After the panel finds no material gap on the quit-sugar book:

1. Create `production-books/quit-smoking/` with a brief for smoking cessation
2. Run the factory END TO END with ZERO subject-specific tuning
   (two independent books from the same plan, same as calibration)
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
