# DRY-RUN — Role-Play of Stop / Continue in the Auto-Tuning Loop

> Simulation only. Nothing implemented, nothing run. Walks the *founder's
> experience* of "run the loop" and "continue from where we left off", plus the
> harder un-clean-stop case, against `loop/PROGRAM.md` §0 (Recovery) and
> `loop/state.md` §4 as they exist today.

## Ground truth recorded first (state of the repo the simulation rests on)

- `loop/state.md` → **Status: IDLE**, Iteration 000 (baseline), campaign branch
  `campaign-001`, Next unit = baseline research (§3). Preflight already PASS
  (2026-08-07).
- `loop/results.tsv` → header only, **no data rows** ⇒ `baseline pending`.
- `loop/iterations/` → **empty** (no NNN dirs yet).
- `loop/preflight/results.md` → OVERALL: PASS.
- `production-books/quit-sugar/` → `research/` (banks + log exist), `master-plan.md`
  (still template placeholders, no chapter cards filled), `master-plan-review.md`,
  `chapters/` (README only, **no chapter files**).
- `loop/open-questions.md` → founder REJECTED adding stop-guard authority and
  unbounded-loop caps; **single-operator, resume-from-markers accepted as-is**.
- `docs/AUTO-TUNING-LOOP.md` → North Star locked; "RUN FACTORY — write ALL
  chapters; partial runs mislead."
- Repo is on `main`, baseline would run directly on `campaign-001` (no worktree).

Key protocol facts the simulation relies on:
- **The chapter file IS the completeness marker.** "the spawned writer produces
  no separate marker; the chapter file IS the marker." (PROGRAM §4 Step 3)
- **§0 cross-check beats a stale state.md.** "If they disagree with what's
  written here, trust the markers and resume from the furthest point they support."
- **`results.tsv` row = iteration-completion marker.** Written LAST in Step 7;
  an existing row for the same iteration means "only the final commit may be
  missing — treat as done, never re-run."
- **`Status` must be exactly `IDLE` or `IN PROGRESS`.**
- **Writing and judging are separate stages** (§4 Step 3 Writing → Step 4 Judge →
  Step 5 Trace → Step 6 Decide → Step 7 Record).
- **There is NO first-class "stop" verb in PROGRAM.md.** Stop is an implied
  act; its safety rests entirely on the boundary-write + marker-cross-check
  discipline.

---

## Scenario A — Clean mid-run "stop" (founder says *stop* mid-writing, chapter 05 done)

### What is running
Baseline (000). Writing stage: chapters are being produced sequentially, chapter
05 just landed (scenario says done). The orchestrator is *waiting* (per §4
"Patience": single long wait between wakes — doing nothing while a healthy run
proceeds is correct).

### What the orchestrator does on "stop"
1. Halt — do NOT spawn the chapter-06 writer call that was scheduled next.
2. Write `loop/state.md` at this boundary:
   - `Status:` **`IN PROGRESS`**
   - `Last completed unit:` baseline writing — chapters 01–05 on disk (not yet
     judged)
   - `Next unit:` baseline writing — chapter 06
   - Log the stop in the Journal table with a timestamp.
3. Do NOT commit anything. Baseline's §3 step-7 commit happens only after the
   book + judges + trace. Stop leaves the working tree exactly as it is.
4. Do NOT touch `results.tsv` (no BASELINE row yet — correct; the iteration is
   not done).
5. Yielding cleanly after the write means the recovery path in §0 now finds an
   accurate IN PROGRESS state.

### State left behind
- `state.md` = IN PROGRESS, chapter 05, next = 06. ✅
- `production-books/quit-sugar/chapters/chapter-01.md … chapter-05.md` present,
  `chapter-06.md` absent. ✅
- `results.tsv` = header only (baseline incomplete — correct). ✅
- No worktree, no commit, no branch changes.

**Founder experience:** one clean word, the run simply pauses at the safest
point (a chapter boundary), state is left unambiguous.

### Is there any ambiguity? → No, in the clean case.
The marker (chapters 01–05 present) and the state.md boundary agree exactly.
A resuming agent has zero decisions to make about what to continue from.

---

## Scenario B — Fresh agent: "continue from where we left off" (clean stop from A)

### What the fresh agent does (walking §0 + state.md)
1. Reads `PROGRAM.md`, `docs/AUTO-TUNING-LOOP.md`, tail of `learnings.md`
   (empty), last data row of `results.tsv` (**none ⇒ baseline pending**), then
   `loop/state.md`.
2. States: "Baseline (000) partially complete — writing interrupted at chapter
   05, Status IN PROGRESS."
3. **Cross-checks markers against state.md** (§0): `chapters/chapter-01.md` …
   `chapter-05.md` present, no `chapter-06.md`. Matches. Resume point = chapter
   06.
4. Confirms it is on the active branch (`campaign-001`), because iteration work
   never happens on `main` (§0 last para).
5. Spawns the chapter-06 writer exactly as §4 Step 3 prescribes (master plan +
   chapter-06 card + style guide + previous chapter **05**), then 07 … last.
6. After the whole book: Step 4 judge every chapter (+ book-arc), Step 5 trace
   analysis, Step 6 decide, Step 7 record. Baseline commit lands on
   `campaign-001`.

### No redo, no ambiguity
- Chapters 01–05 are **never regenerated** — "do not restart the iteration, do
  not redo completed units."
- The empty `results.tsv` correctly tells the agent NOT to treat 000 as done.
- Since chapters 01–05 each exist as complete files, "write 06 referencing 05"
  is well-defined.

**Founder experience:** "continue from where we left off" works exactly as
intended — pick up at the next chapter, no redo, no re-run gate to trip.

---

## Scenario C — HARD CRASH, no clean stop (state.md IN PROGRESS, chapters 01–05 on disk)

### What the crash left
- A mid-baseline process died. `state.md` was last written at some earlier
  boundary. Two sub-cases matter:

**C1 — state.md lagged:** it claims "chapter 04 done, next = 05" (the last
boundary write before the crash), but `chapters/` actually holds 01–05 (writing
the 5th happened after the state write, then the process died before the next
boundary write).

**C2 — state.md current:** it claims "chapter 05 done," matching disk.

### What the fresh agent does (§0 recovery)
1. Reads state.md → Status **IN PROGRESS**. Good — this single token is the
   whole "were we interrupted?" signal.
2. **Cross-checks against on-disk markers FIRST** (§0 explicitly instructs this
   because "state.md can lag the stage it names").
3. In **C1**: markers (01–05) beat the stale state (04) ⇒ resume from **chapter
   06**, *ignoring* state.md's stale "04." This is exactly the case §0 was
   written for. **Clean, no redo of 05, no redo of the iteration.**
4. In **C2**: markers agree with state ⇒ resume chapter 06. **Clean.**
5. On the campaign branch (baseline, no worktree) the chapter files survive the
   crash in the working tree, uncommitted but fully readable. No data loss; the
   eventual §3 step-7 commit picks them up for KEEP/promotion.

### Verdict on the crash case
Recovery is **recoverable and clean** for the *whole chapters 01–05* set. The
designed marker-vs-state conflict resolution works and prevents a full-iteration
redo if the process dies between boundary writes.

### THE one genuine fragility (the only real "redo/ambiguity" in the whole exercise)
The completeness signal for the **current (highest-index) chapter** is
*file-existence only* — there is **no** per-chapter END sentinel, no size floor,
no "judged" flag consulted at the boundary.

- If the crash truncated **chapter-05.md** mid-write but the file object still
  exists, the fresh agent cannot distinguish "complete chapter 05" from
  "partial chapter 05." It will assume 05 is done.
- Writing of chapter 06 then runs against a **silently damaged predecessor**,
  compounding the defect.
- Because judging is a **post-whole-book stage** (§4 Step 4 runs after Step 3
  writes every chapter), the truncation is NOT caught at the boundary. It only
  surfaces when the judge reads chapter 05 — i.e. after chapters 06…last have
  already been written. Fixing it then costs **a regenerated chapter 05 +
  a rewritten chapter 06 + re-judging of the affected chapters** — a localized
  redo, not a whole-run redo, but a non-trivial one that arrives much later than
  it should.

This is the ONLY moment in all three scenarios where "continue from where we
left off" can silently resume onto a partially-written unit. It is an edge of
the crash case, not of the clean-stop case.

---

## Bottom line (founder-experience)

- **"Run the loop"** — works. §0 recovery + IDLE state + empty results.tsv
  resolve unambiguously to "baseline pending, start §3 research."
- **"Continue from where we left off" (clean stop)** — **works cleanly.**
  Resume-point is a chapter boundary, exact on-disk match, zero redo, zero
  ambiguity.
- **Crash with no clean stop** — **recovers cleanly for the completed-chapters
  set**; the stale-state-vs-marker cross-check is genuinely load-bearing and
  prevents any full-iteration redo, even when state.md lags by a chapter.
- **The single fragile seam:** a *truncated highest-index chapter file* is
  indistinguishable from a complete one at the boundary. Everything else is
  deterministic and unambiguous.

## Optional hardening (NOT requested to implement — noted only)
1. Add a first-class, atomic "stop" step to §0/PROGRAM: on founder stop, write
   state.md IN PROGRESS with the furthest marker BEFORE yielding (removes
   reliance on orchestrator diligence alone).
2. Give each chapter a completeness signal that file-existence alone cannot
   fake, or have the boundary check verify it (e.g. an END sentinel / a size
   floor / run the per-chapter judge immediately after each write rather than
   deferring all judging to the end). Judging-per-chapter would catch a torn
   chapter at the boundary instead of after the whole book.
   - Trade-off to weigh against North Star: the runbook currently defers judging
     to keep writing fast; per-chapter judging trades speed for a tighter
     crash-safety seam. Founder has REJECTED adding machinery into judges
     (preflight option-C), so the sentinel/floor would be the lighter touch.
