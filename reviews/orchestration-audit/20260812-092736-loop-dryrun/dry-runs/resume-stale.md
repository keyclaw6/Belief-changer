# Dry Run — RESUME + STALE/CONCURRENT STATE

Simulated against `main @ afca11f`. **Read-only trace** — no files edited, no model
calls made. Every "decision" below is what the runbook literally authorizes an actor to do,
traced step-by-step. Deliverable path:
`reviews/orchestration-audit/20260812-092736-loop-dryrun/dry-runs/resume-stale.md`.

## Normative anchors consulted

- `loop/PROGRAM.md` §0 Recovery (lines 8–32): `state.md` **Status** is exactly `IDLE` or `IN PROGRESS`
  (verbatim); IN PROGRESS → continue from last completed unit, no restart, no redo of completed units;
  **results.tsv exception** → if a row exists for the same iteration, Step 7 already ran, treat as done,
  never re-run; **cross-check** → state.md can lag, confirm each claimed unit against on-disk markers
  (research bank, `production-books/quit-sugar/chapters/`, `loop/iterations/NNN/judgments/`), resume from
  the *furthest* point the markers support, not the stale marker; orchestrator updates state.md at every
  boundary and before every long wait (§4 Step 3 "Patience").
- `loop/state.md`: live checkpoint, "Write the *next* unit before starting it, so a crash mid-unit never loses it."
- On-disk markers: `production-books/quit-sugar/chapters/` for chapter completion; `loop/iterations/NNN/judgments/`
  for judge reports; `loop/results.tsv` last row for iteration completion. GSBS reference is 20 chapters (01–20).
- Current checked-out facts at trace time: `state.md` = Status `IDLE`, baseline pending; `results.tsv` = header only
  (no data row); `production-books/quit-sugar/chapters/` = only `README.md` (no chapters yet).

**Split-brain guard search (relevant to case d):** grepped the loop surface — `PROGRAM.md`, `state.md`,
`AUTO-TUNING-LOOP.md`, `AGENTS.md`, `config.yaml`, `HANDOFF.md` — for `incarnation`, `token`, `lease`, `lock`,
`mutex`, `fence`, `owner`, `pid`, `split-brain`. **No iteration-level guard exists.** The only pid-guards are
inside `scripts/loop-runner/daemon.sh` (`kill -0 $PIDF`) and `queue_runner.sh` (single runner); these fence the
shell job-runners, not the orchestrator actor that controls the loop. `state.md` carries only `IDLE|IN PROGRESS`,
with **no owner / incarnation / heartbeat / lease field** and no instruction to detect a live concurrent run.

---

## Case (a) — crash mid-Writing at chapter-07 of 20; state.md = IN PROGRESS

**Scenario.** A full-book run (Writing stage) crashed while chapter-07's writer was in flight.
`state.md`: `Status IN PROGRESS`, last completed unit = Writing ch-06, Next = ch-07. `results.tsv` has no
row for this iteration (writing incomplete). On-disk: `chapters/` holds 01–06; ch-07 absent/partial.

**Trace table.**

| step | role | trigger | state-before | decision + authority | state-after | status |
|---|---|---|---|---|---|---|
| 1 | fresh agent | new run begins | `results.tsv` empty; state.md IN PROGRESS / next ch-07 | §0 Recovery: read PROGRAM, North Star, state.md, learnings tail, last results row. No data row → names what the interrupted run was (Writing, worse same) | position stated | start |
| 2 | fresh agent | IN PROGRESS detected | chapters/ = 01–06; ch-07 absent/partial; no results row | §0 *cross-check*: state claims ch-07 in flight; markers support 01–06 complete. Furthest completed unit = ch-06. Confirm **no results row** → results-rule (§0) NOT triggered | furthest = ch-06; in-flight unit = ch-07 | recover |
| 3 | fresh agent | — | — | §0 IN PROGRESS rule: continue from last completed unit → re-run **ch-07**; do NOT restart the iteration, do NOT redo 01–06. Per state.md, write *next* unit (ch-08) before starting so a new crash loses nothing | state.md → IN PROGRESS, next = ch-08; spawn writer for ch-07 | in progress |
| 4 | chapter-writer | ch-07 spawn | — | §4 Step 3 Writing: spawn with 4 inputs (plan card authority, chapter card, style guide, prev chapter) | `chapters/chapter-07.md` (re)generated | resumed |
| 5 | fresh agent | ch-07 done | — | Continue ch-08 → 20 sequentially; 01–06 untouched | rest of book written | recovering |

**Answer to (a).** Recovery **does NOT resume at ch-08 "without rework."** The IN PROGRESS token names the
interrupted unit; the marker cross-check confirms the furthest *completed* unit is ch-06; so the correct resume
point is **ch-07 — re-running exactly the one incomplete unit**. It does not restart the iteration and does not
rework 01–06. Resuming at ch-08 would silently drop a chapter no marker supports, which §0 forbids.

**Verdict: COMPLETES.** (Recovery is well-defined and correct. The only way to reach the "ch-08 without rework"
bug is to skip §0's mandatory marker cross-check — outside spec.)

---

## Case (b) — crash between "append results.tsv row (Step 7)" and "mark IDLE"

**Scenario.** The run completed decision Step 6 and appended the iteration's data row to `results.tsv`
(Step 7), but crashed before Step 7's final act "Mark the iteration done in `loop/state.md` (status `IDLE`)".
`state.md` therefore still reads IN PROGRESS, while `results.tsv` already holds the iteration's row.

**Trace table.**

| step | role | trigger | state-before | decision + authority | state-after | status |
|---|---|---|---|---|---|---|
| 1 | fresh agent | new run begins | state.md IN PROGRESS (stale — not yet IDLE); results.tsv **has** a data row naming iteration NNN | §0: read `state.md` **and** the last data row of `results.tsv`. Row present → Step 7 already ran | exception precondition met | — |
| 2 | fresh agent | row present for same iteration | — | §0 results rule (verbatim): "if `results.tsv` already holds a row for that same iteration, the iteration completed (Step 7 ran) and only the final commit may be missing — treat it as done; never re-run it." `IDLE` branch of §0 points to the same rule | iteration declared DONE; **no re-run** | resolved |
| 3 | fresh agent | — | — | Do NOT re-run the iteration and do NOT re-append the results row (Step 7 already completed). Finish only what the crash interrupted: learnings/ledger entries if cut off, the final commit (KEEP promote — or records-only commit for REVERT/INCONCLUSIVE, §4 Step 7), then mark state.md IDLE | state.md → IDLE, last completed unit = iteration NNN decision; records committed | complete |

**Answer to (b).** **Yes — the results-row-wins exception prevents a double iteration.** Because §0 mandates
reading `state.md` together with the last `results.tsv` row, and the exception explicitly overrides the stale
IN PROGRESS ("never re-run it"), the fresh agent treats the iteration as done and only completes the missing
final commit + IDLE flip. No duplicate results row, no second execution of the iteration.

**Verdict: COMPLETES.** Caveat (not a spec failure for the stated case): it depends on the row being *fully*
appended before the crash. A crash mid-append (partial/corrupt line) isn't defined — the spec has no row-format
validation — but the stated scenario is a clean append-then-crash.

---

## Case (c) — state.md = IN PROGRESS ch-07, but markers show chapters 01–12 written

**Scenario.** `state.md` lags: it claims IN PROGRESS at next unit ch-07 (stale), while on-disk markers
`production-books/quit-sugar/chapters/` show chapters 01–12 already written. Fresh agent starts recovery.

**Trace table.**

| step | role | trigger | state-before | decision + authority | state-after | status |
|---|---|---|---|---|---|---|
| 1 | fresh agent | new run begins | state.md IN PROGRESS / next ch-07 (stale); chapters/ markers show 01–12 present | §0 *cross-check*: "state.md can lag… trust the markers… resume from the furthest point they support, not the stale marker." Also in state.md header | state.md found stale | recover |
| 2 | fresh agent | marker/state disagreement | — | Confirm furthest completed unit from markers = **ch-12** (not the stale ch-06/ch-07). Rule: markers are ground truth over the written token | furthest = ch-12; resume unit = ch-13 | — |
| 3 | fresh agent | — | — | Spawn chapter-writer at ch-13; do NOT restart the stage, do NOT redo 01–12. Write next unit (ch-14) into state.md before starting (crash-safety) | state.md → IN PROGRESS, next ch-14; ch-13 in flight | recovering |

**Answer to (c).** **Yes — the marker cross-check recovers to the furthest point (resume at chapter-13).** It
explicitly privileges on-disk markers over the stale IN PROGRESS claim, so none of chapters 01–12 is reworked and
the run continues from where the work actually stands. The rule is present and mandatory in **both** PROGRAM §0
(lines 26–32) and the `state.md` header.

**Verdict: COMPLETES.** Residual risk (shadow, not a spec failure): "furthest point" is an orchestrator
*reasoning* step, not deterministic code — the spec defines no file-validity/truncation check (the writer writes
directly to `chapters/chapter-NN.md`; nothing distinguishes a complete ch-12 from a partial/truncated one). A
mistake here could resume over-far. For the clean stated scenario the rule does what it promises.

---

## Case (d) — two actors: resumed agent + still-running old agent

**Scenario.** A prior run was interrupted, then a fresh agent begins §0 recovery to resume it — but the *original*
agent is still alive and still driving the same iteration from the same state. Both read the identical `state.md`
(IN PROGRESS) and both treat it as theirs to resume. No incarnation/token/lease/owner exists anywhere in the loop
surface (grep evidence above). `state.md` holds only `IDLE|IN PROGRESS` — it cannot say *which* actor owns the run
or whether the run is genuinely dead.

**Trace table.**

| step | role | trigger | state-before | decision + authority | state-after | status |
|---|---|---|---|---|---|---|
| 1 | old agent | still running | IN PROGRESS | continues the live round: spawns writers for ch-N+, updates `state.md`, before waits updates state again (§4 Step 3) | advancing; state.md rewritten by old agent | live |
| 2 | resumed agent | starts §0 | the **same** IN PROGRESS token both read | §0 says "continue from last completed unit — do not restart." **No check asks "is a live actor already driving this?"** No lease/token to acquire, no fence to clear | both consider themselves the owner | concurrent |
| 3 | both | Writing | same `chapters/` target | Both spawn `chapter-writer` for overlapping units; both update `state.md` (last-writer-wins, no ownership guard); both later append `results.tsv` rows and `ledger.md`/`learnings.md`; both may attempt the Step 7 `loop(iter-NNN)` promotion commit on the campaign branch | duplicate writes; duplicate results rows; duplicate ledger entries; split/conflicting promotion | racing |

**Answer to (d).** **There is NO split-brain guard.** No incarnation token, no lease, no heartbeat, no owner field
(verified by grep of the full loop surface). The `IDLE|IN PROGRESS` bit is binary and ownerless, so it cannot
distinguish "crashed, safe to resume" from "still alive, hands off." §0 recovery presumes the prior run was
interrupted and says nothing about detecting a live concurrent actor or fencing it out. **Two agents resuming the
same iteration from the same state is completely undefined behavior** — nothing deterministic prevents overlapping
chapter writes, duplicate `results.tsv` rows, duplicate ledger entries, and a contested KEEP promotion.

**Verdict: UNDEFINED** (and, if it must yield a deterministic safe outcome, effectively **BLOCKED** until a guard
exists).

Suggested (not applied — read-only) fix: add an **owner/incarnation token** to `state.md` (actor id + heartbeat +
acquired lease) and make §0 Recovery *refuse to resume* while a live lease/heartbeat is present, or add a
fencing primitive (`flock` on a lockfile, or the pid-guard pattern already used in `daemon.sh`) acquired at each
iteration start and held through Step 7.

---

## Verdict summary

| Case | Scenario | Verdict |
|---|---|---|
| (a) | Crash mid-Writing at ch-07 of 20, state.md IN PROGRESS | **COMPLETES** (resume at ch-07 = re-run the interrupted unit; no iteration restart, no redo of 01–06; here "rework" is only the genuinely incomplete unit) |
| (b) | Crash between results.tsv append (Step 7) and mark IDLE | **COMPLETES** (results-row-wins exception prevents double iteration; row read before acting, stale IN PROGRESS overridden, done → finish final commit + IDLE) |
| (c) | state.md IN PROGRESS ch-07; markers show 01–12 written | **COMPLETES** (mandatory marker cross-check recovers to furthest point = resume ch-13; no completed chapter reworked) |
| (d) | Resumed agent + still-running old agent | **UNDEFINED** — no split-brain guard exists (no incarnation/token/lease/owner); effectively **BLOCKED** for the concurrent scenario |

**BLOCKED / UNDEFINED:** Case (d) only. (a)(b)(c) all complete per the runbook as written at `afca11f`.
