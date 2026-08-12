# Happy-Path Dry Run — Iteration 001 (KEEP)

> Read-only SIMULATION of the auto-research loop's primary happy path for ONE
> iteration (001), assuming baseline 000 is already complete. No files were
> edited, no model roles were spawned, no model calls made. Every observable
> transition below is traced against `loop/PROGRAM.md` §4 (Steps 1–7), §1, §5,
> `loop/state.md`, `loop/ledger.md`, `loop/inbox/README.md`, and the role
> contracts `loop/prompts/hypothesizer.md` + `loop/prompts/trace-analyzer.md`.
> Audited revision: `main` @ afca11f.
>
> **Scenario framing.** Campaign branch exists (`campaign-001`), baseline 000
> is done, preflight PASS (2026-08-07). `loop/inbox/` is empty on this run (we
> trace the machine-generated hypothesis path). The target hypothesis changes
> ONE editable file — `prompts/style-guide.md` — so `research_reuse.sh` must
> return REUSE. Everything downstream regenerates. The predicted causal
> cluster closes, no lane regresses → **KEEP** → promotion to the campaign
> branch → ledger + state update. Terminal state = IDLE.

---

## Precondition state (state-before of the whole iteration)

| Field | Value |
|---|---|
| `loop/state.md` Status | `IDLE` |
| Last completed unit | iteration 000 (baseline) decision |
| `loop/results.tsv` | header + 1 BASELINE data row (000) |
| `loop/inbox/` | only `README.md` present → empty of hypotheses |
| Editable file touched | `prompts/style-guide.md` (tuning surface, §1) |
| Research trigger changed? | No (not `research-agent.md`/`config.yaml`/`00-brief.md`) |
| Worktree | `../quit-sugar-iter-001/` on iteration branch |
| Trigger | "founder authorized iteration 001" |

---

## §0 Recovery (opening transition)

| step# | active role | trigger | state-before | decision+authority | output/handoff | state-after | next actor | status |
|---|---|---|---|---|---|---|---|---|
| R1 | orchestrator (pi coding agent) | new run / resume | `state.md` IDLE, last completed = 000 | read runbook + North Star + learnings tail + last results.tsv row (§0) | states "last iteration 000 (BASELINE), next hypothesis: none yet" | positioned to begin iter 001 | orchestrator → §4 Step 1 | ✅ |

**Handoff verification (§0):** the fresh agent reads `docs/AUTO-TUNING-LOOP.md`,
`loop/state.md`, `loop/learnings.md` (currently only header, empty body — a
not-yet-populated tail is read as "nothing yet"), and the last data row of
`loop/results.tsv` (header parse guard stated in PROGRAM §0: "ignoring the
header"). **Discoverable: yes** — all files are at canonical paths. **Parseable:
yes** — tsv is tab-separated with a known header. **Trusted/continue: yes** —
IDLE + no results.tsv row for 001 ⇒ can start 001; no interrupted-unit hazard.

---

## Step 1: Declare hypothesis

| step# | active role | trigger | state-before | decision+authority | output/handoff | state-after | next actor | status |
|---|---|---|---|---|---|---|---|---|
| S1 | orchestrator | iteration 001 authorized | inbox empty; state IDLE at iter 001, step not started | inbox first (§4 Step 1): if any non-README `.md` exists, test it oldest-first | inbox has none → **fall through to hypothesizer** | inbox path recorded empty; hypothesizer path chosen | → S2 spawn hypothesizer | ✅ |
| S2 | orchestrator | inbox empty | hypothesizer path chosen | spawn `hypothesizer` sub-agent (contract `loop/prompts/hypothesizer.md`), model `gpt-5.6-sol` high, route openai-sub (§1, config) | hands: iter-000 `trace-analysis.md`, `loop/learnings.md`, current editable factory files | hypothesizer called with clean context (no host prompt, only role prompt + listed inputs) | → S3 hypothesizer executes | ✅ |
| S3 | hypothesizer (sub-agent) | received trace analysis + learnings + factory state | inputs received | proposes ONE causal change; 4-field contract (failure evidence / root cause / targeted fix / predicted impact); never-repeat + one-causal-change guards | **hypothesis.md** declaring e.g. "style-guide.md §voice — replace the evidence-policy opening instruction"; prediction targets voice cluster | hypothesis authored (one causal change, one editable file) | → S4 save | ✅ |
| S4 | hypothesizer | authored | hypothesis complete | save its response **unchanged** as `loop/iterations/001/hypothesis.md` | `loop/iterations/001/hypothesis.md` written | hypothesis recorded with `source: machine` (no founder-inbox move needed) | → Step 2 | ✅ |

**Handoff verification (Step 1 → Step 2):** `loop/iterations/001/hypothesis.md`
is the canonical location the runbook names (§4 Step 1); Step 2's apply action
reads it from there. The hypothesis carries the exact file/section/targeted-fix
needed to build `change.diff`. **Discoverable/parseable/continue: yes.** The
inbox-empty path is exercised exactly as PROGRAM describes.

---

## Step 2: Apply the change

| step# | active role | trigger | state-before | decision+authority | output/handoff | state-after | next actor | status |
|---|---|---|---|---|---|---|---|---|
| S5 | orchestrator | hypothesis recorded | iter-001 worktree, hypothesis.md present | apply ONE causal change in ONE editable file (`prompts/style-guide.md`); duplicates of the same instruction may be normalized in the same file (§1, §5) | `prompts/style-guide.md` edited in the worktree; `loop/iterations/001/change.diff` records the diff | one causal change applied; diff recorded; no second behavior (§5) | → Step 3, research-reuse check | ✅ |

**Handoff verification (Step 2 → Step 3):** `change.diff` is written to the
iteration directory, exactly where §4 Step 3's `research_reuse.sh` expects its
`<changed-file>` argument. The changed file's path (`prompts/style-guide.md`)
is unambiguous. **Discoverable/parseable/continue: yes.**

---

## Step 3: Run the factory

### S6 — research-reuse decision (the ONE deterministic handover)

| step# | active role | trigger | state-before | decision+authority | output/handoff | state-after | next actor | status |
|---|---|---|---|---|---|---|---|---|
| S6 | orchestrator | change applied | worktree, change.diff present | call `scripts/loop-runner/research_reuse.sh prompts/style-guide.md` — the only deterministic code (§1, §4 Step 3) | **REUSE** (style-guide.md is not a research trigger; `production-books/*/research/` non-empty) | research to be reused, not rerun | → S7 copy research into traces | ✅ |

**Handoff verification (Step 3):** `research_reuse.sh` exit 0, prints `REUSE`.
The orchestrator copies the last accepted research artifacts into
`loop/iterations/001/traces/research/` (per "Reuse only artifacts upstream of
the change" + trace format). The planning stage consumes research that still
exists on disk (the worktree has the campaign-branch research copied in). The
planner is handed references only to accepted research packets.
**Discoverable/parseable/continue: yes** — this is the well-formed deterministic
handover, and its SAFE-to-RERUN branch (absent research) is not hit here because
research exists.

### S7–S9 — Planning stage

| step# | active role | trigger | state-before | decision+authority | output/handoff | state-after | next actor | status |
|---|---|---|---|---|---|---|---|---|
| S7 | orchestrator → plan-writer sub-agent | research available (reused) | traces/research copied | spawn `plan-writer` (Kimi K3, commandcode); initial call carries EXACTLY four file inputs (style-guide, brief, lived-experience, scientific-evidence) — no reference contamination (§4) | accepted master plan candidate `master-plan.md` | candidate plan + its chapter cards | → S8 plan-reviewer | ✅ |
| S8 | plan-reviewer sub-agent | candidate plan available | plan written | spawn `plan-reviewer` (gpt-5.6-luna, commandcode); follow `master-plan-reviewer-v2.md` | `master-plan-review.md` → ends `fit to write from` (happy path: no `needs changes first` loop) | plan accepted | → S9 rebuild reference-alignment (only if plan changed) | ✅ |
| S9 | orchestrator | plan accepted | accepted plan | **condition:** plan did NOT change (hypothesis touched style-guide, not the plan) ⇒ `loop/reference-alignment.md` stays frozen | no rebuild | reference table unchanged → judging proceeds on existing alignment | → S10 writing | ✅ |

**Handoff verification (Step 3 planning):** the accepted plan + cards land in
`production-books/quit-sugar/`; chapter cards carry the `primary job / entering
belief / leaving belief / arc / continuity / compliance` fields the writer and
judges read. Reference-alignment rebuild rule (§4 Step 3, `reference-alignment.md`
Procedure/Rebuild-rule) only fires when the accepted plan changes — here it
does not, so the frozen table is correctly reused. **Discoverable/parseable/
continue: yes.**

### S10–S14 — Writing stage (sequential chapter 01 → last)

The orchestrator spawns `chapter-writer` ONE chapter at a time, in order, until
the book is complete. Each call passes EXACTLY four inputs (§4): accepted master
plan, target chapter card for N, `prompts/style-guide.md` (the changed file),
and the previous chapter (ch-01 uses the plan's book-core). The happy path runs
every chapter; below we trace ch-01 fully and show ch-N as the same template
(this is the "sequential chapter writing" the prompt asks to cover).

| step# | active role | trigger | state-before | decision+authority | output/handoff | state-after | next actor | status |
|---|---|---|---|---|---|---|---|---|
| S10 | orchestrator | plan accepted | writing stage begins | spawn `chapter-writer` for chapter 01; inputs = plan + card-01 + style-guide(v2) + book-core; writer model `meta/muse-spark-1.2-contributor`, commandcode, streamed, no max_tokens (§1, HANDOFF) | `chapters/chapter-01.md`; trace dir `traces/chapter-01/{chapter-card,prompt,response,metadata}.md/json` | chapter 01 done, artifact written | → S11 ch-02 writer | ✅ |
| S11 | orchestrator | ch-01 done | chapter 01 trace complete | spawn `chapter-writer` for ch-02 (inputs = plan + card-02 + style-guide(v2) + **ch-01**) | `chapters/chapter-02.md` + `traces/chapter-02/*` | ch-02 done | → S12 ch-03 | ✅ |
| S12 | orchestrator | ch-02 done | ch-02 trace complete | sequentially produce ch-03 | `chapters/chapter-03.md` + traces | ch-03 done | → S13 ch-04 | ✅ |
| S13 | orchestrator | ch-03 done | ch-03 trace complete | sequentially produce ch-04 | `chapters/chapter-04.md` + traces | ch-04 done | → S14 ch-05…last | ✅ |
| S14 | orchestrator | ch-N-1 done | in progress | continue until the LAST chapter completes; never skip a chapter; refuse ⇒ refusal.md + INCONCLUSIVE (happy path: no refusal) | `chapters/chapter-NN.md` + complete per-chapter trace set | ALL chapters generated; full book on disk | → Step 4 judges (parallel) | ✅ |

**Handoff verification (Step 3 writing):**
- Writer reads the accepted plan's chapter card as semantic authority; plan-wide
  inventories resolve every cited ID — both are on disk at a stable path.
- Previous-chapter handover: ch-02 writer reads `chapters/chapter-01.md` (written
  one unit earlier) — ordering guarantees discoverability.
- **Metadata:** a failing/changed style-guide does not touch the plan/research,
  so the writer's other three inputs are unaffected; only the style guide differs,
  which is the intent.
- Error path (not exercised in the happy path but specified): retry once, then
  INCONCLUSIVE / escalate — never skip. **Discoverable/parseable/continue: yes.**

### S15 — patience / wait discipline

| step# | active role | trigger | state-before | decision+authority | output/handoff | state-after | next actor | status |
|---|---|---|---|---|---|---|---|---|
| S15 | orchestrator | long-running stage | writing running | updates `loop/state.md` before EACH wait (Status `IN PROGRESS`); waits on `.exit` markers + content progress; no fixed timeout; stuck ⇒ sub-agent judgment + retry once (§4 Step 3) | `state.md` Status `IN PROGRESS` at correct stage | stage markers move as chapters complete | → S10–14 resume from furthest marker | ✅ (not terminal — traversed throughout Step 3) |

**Handoff verification (wait discipline):** `state.md = IN PROGRESS` at every
boundary; on-Disk chapter/trace/judgment markers are the ground truth per §0,
so a crash mid-stage resumes from the furthest completed unit. The happy path
never triggers the stuck path.

---

## Step 4: Judge

### S16–S19 — parallel judging

All three chapter judges run on EVERY generated chapter; the book-arc judge
runs once on the complete book. Judge calls are independent → spawned in
PARALLEL. Each judge: `gpt-5.6-luna` high, openai-sub.

| step# | active role | trigger | state-before | decision+authority | output/handoff | state-after | next actor | status |
|---|---|---|---|---|---|---|---|---|
| S16 | orchestrator → 3 chapter judges (parallel) | all chapters generated | full book + aligned GSBS chapters | spawn `belief-mechanic`, `voice-emotion`, `reader-journey` for EVERY chapter; each receives judge prompt, our chapter, aligned real chapter, CHAPTER CONTEXT (copied from the accepted card — never improvised), prev chapter for ch2+ (§4) | per-chapter verdict reports saved to `loop/iterations/001/judgments/` | judgments accumulating (parallel) | → S17 book-arc | ✅ |
| S17 | book-arc judge | all chapters + plan assets ready | full book | spawn `book-arc` once on complete book with mantra sheet, instruction spine, curve map, reference-alignment skeleton | `book-arc` report | complete judge set for the book | → S18 retry check | ✅ |
| S18 | orchestrator | verdicts returned | judge set | failed judge rerun once; a still-missing report blocks KEEP → INCONCLUSIVE (happy path: none fail) | all reports present, PASS/FAIL verdicts | every judge report completed (decision validity precondition, §4 Step 6) | → Step 5 trace analysis | ✅ |
| S19 | orchestrator | all reports complete | judgments dir full | save verdicts in `loop/iterations/001/judgments/` | judgments persisted | evidence on disk for trace-analyzer | → Step 5 | ✅ |

**Handoff verification (Step 4):** judges read the aligned GSBS chapter from
`loop/reference-alignment.md` (frozen this iteration) and the CHAPTER CONTEXT
from the accepted cards — both stable/discoverable. Alignment quality STRONG/
PARTIAL/WEAK governs judge weight; WEAK judged lightly per that file.
**Discoverable/parseable/continue: yes.** The decision-validity precondition
(all judges completed) is met in the happy path.

---

## Step 5: Trace analysis

| step# | active role | trigger | state-before | decision+authority | output/handoff | state-after | next actor | status |
|---|---|---|---|---|---|---|---|---|
| S20 | orchestrator | all judgments complete | judgments + traces on disk | spawn `trace-analyzer` sub-agent (gpt-5.6-luna high, openai-sub) with the judgments AND the exact generation traces (§4 Step 5) | sends judge reports + `traces/research|plan|chapter-*` | analyzer called with clean context | → S21 analyzer | ✅ |
| S21 | trace-analyzer | received verdicts + traces | inputs received | merge corroborating reports into CAUSAL CLUSTERS; map each cluster to ONE root component (research→plan→plan-card→style-guide→writer-prompt→model); diagnose, do NOT prescribe; quote trace evidence; flag PERSISTENT at 3+ (§?/contract) | **`trace-analysis.md`:** cluster summary table + per-cluster root component + mechanism | e.g. "voice cluster → root = style-guide (evidence-policy opening)" — matches the hypothesis target | → S22 save | ✅ |
| S22 | orchestrator | response received | analysis authored | save as `loop/iterations/001/trace-analysis.md` | file persisted | diagnosis lives in trace-analysis.md, not judge reports (§4 Step 5) | → Step 6 decide | ✅ |

**Handoff verification (Step 5 → Step 6):** `loop/iterations/001/trace-analysis.md`
is where the runbook and the hypothesizer's prompt both read from next
iteration. The analyzer's rules (do-not-propose-fixes; quote trace evidence)
keep the handoff clean — it hands UP a diagnosis, not a fix, so Step 6's "did
the predicted cluster close?" stays answerable from evidence. Next iteration
(002), Step 1 feeds THIS file back to the hypothesizer. **Discoverable/parseable/
continue: yes.**

---

## Step 6: Decide

| step# | active role | trigger | state-before | decision+authority | output/handoff | state-after | next actor | status |
|---|---|---|---|---|---|---|---|---|
| S23 | orchestrator | trace-analysis written | decision precondition: EVERY judge report completed (sat in S18) | answer ONE question: **did the predicted causal cluster close?** (owning lane decides; other lanes may veto only a material REGRESSION = NEW failure class + quoted passage) | Verdict: **KEEP** — targeted style-guide cluster improved materially AND no lane shows a material regression | KEEP decision reached; no voting/averaging | → S24 record decision | ✅ |
| S24 | orchestrator | KEEP reached | decision made | record prediction accuracy "Predicted X. Observed Y. [accurate/partial/wrong]."; write `loop/iterations/001/decision.md` with verdict + reasoning | decision.md persists; prediction noted (e.g. accurate) | decision + verdict on disk | → Step 7 record | ✅ |

**Handoff verification (Step 6 → Step 7):** `loop/iterations/001/decision.md`
records the verdict, and KEEP's branch semantics are unambiguous: "promote to
the campaign branch + keep artifacts" (vs REVERT/INCONCLUSIVE discard). Because
this is KEEP, Step 7's promotion path is exercised. **Discoverable/parseable/
continue: yes.**

---

## Step 7: Record (+ promotion on KEEP)

| step# | active role | trigger | state-before | decision+authority | output/handoff | state-after | next actor | status |
|---|---|---|---|---|---|---|---|---|
| S25 | orchestrator | decision.md = KEEP | iteration 001 complete | append ONE tsv data row to `loop/results.tsv` matching the EXISTING header; do NOT re-append header (§4 Step 7) | row `001 … KEEP …` | `results.tsv` gains row 001 (canonical machine record) | → S26 learnings | ✅ |
| S26 | orchestrator | results row written | tsv updated | append a learnings entry (iter-NNN short title / hypothesis / change / verdict / lesson / next direction) to `loop/learnings.md` | learnings entry added ("Lesson" is what the hypothesizer reads next) | learnings tail = iter-001 | → S27 ledger | ✅ |
| S27 | orchestrator | learnings written | learnings updated | append ONE entry to `loop/ledger.md` in that file's format (Hypothesis, Change, What happened quoted, Verdict & why, What we learned, What this opens next); verdict + lesson copied VERBATIM from the results.tsv row; append-only, never edit a past entry (§4) | ledger entry for iter-001 | ledger tells the next reader what to try next | → S28 state | ✅ |
| S28 | orchestrator | ledger entry written | bookkeeping nearly complete | mark iteration done in `loop/state.md` (Status `IDLE`, last completed unit = iteration 001 decision); on KEEP promote the change to the campaign branch as one commit `loop(iter-001): KEEP — <short hypothesis>` and merge `loop/iterations/001/` records with it (§4 Step 7, §1) | `state.md` → `IDLE`; campaign-001 branch carries the change + records in ONE commit | terminal state reached: iteration 001 KEPT, worktree removed, campaign branch updated | → next iteration (002) | ✅ |

**Handoff verification (Step 7 / promotion):** Every append target is at a
canonical, discoverable path, and every record carries enough self-contained
detail for a fresh reader/agent:
- `loop/results.tsv` — machine-canonical; §0 Recovery reads its last row.
- `loop/learnings.md` — the hypothesizer's next-input; its tail is what §0 and
  Step 1 feed forward.
- `loop/ledger.md` — the human/fresh-agent explanation; its entry format is
  defined top-of-file.
- `loop/state.md` — Status reset to exactly `IDLE` (the only two allowed tokens),
  last-completed-unit named, so §0 Recovery on the next run resumes at 002.
- Promotion commits change + iteration records together onto the campaign
  branch; `main` is untouched (only founder-merged winners land on `main`, §1 /
  AGENTS.md Workflow) — verified consistent with the branch topology
  (`main` @ afca11f has the loop machinery but not campaign-001).
**Discoverable/parseable/trusted/continue: yes** across all four records.

---

## Terminal state

| Field | Value |
|---|---|
| `loop/state.md` Status | `IDLE` |
| Last completed unit | iteration 001 (KEEP) decision |
| `loop/results.tsv` | header + BASELINE(000) + KEEP(001) |
| `loop/learnings.md` tail | iter-001 entry |
| `loop/ledger.md` | iter-001 entry (newest at bottom) |
| `loop/iterations/001/` | hypothesis.md, change.diff, traces/, judgments/, trace-analysis.md, decision.md |
| Campaign branch `campaign-001` | ONE commit: `loop(iter-001): KEEP — <short hypothesis>` + records (KEEP promotion, §4 Step 7) |
| `main` | unchanged (campaign winners are founder-merged only) |
| Worktree | removed after records committed |
| Next | founder-authorized iteration 002; Step 1 feeds iter-001 trace-analysis back to the hypothesizer |

---

## Cross-cutting: handoff receiver can discover/parse/trust/continue — VERIFIED

| Handoff | Receiver | Discover | Parse | Trust | Continue |
|---|---|---|---|---|---|
| S4 hypothesis.md → Step 2 | orchestrator (`change.diff`) | ✅ canonical path | ✅ 4-field | ✅ produced by contract role | ✅ |
| S6 research REUSE → Step 3 planning | plan-writer | ✅ research on disk | ✅ | ✅ deterministic code | ✅ |
| S7–9 accepted plan → writing | chapter-writer | ✅ persisted plan+cards | ✅ card fields | ✅ review gate passed | ✅ |
| S10–14 chapter-N → chapter-N+1 | next chapter-writer | ✅ previous chapter on disk | ✅ | ✅ ordering | ✅ |
| S16–17 judgments → trace-analyzer | trace-analyzer | ✅ `iterations/001/judgments/` | ✅ verdict reports | ✅ all completed | ✅ |
| S21 trace-analysis → Step 6 decide | orchestrator | ✅ `iterations/001/trace-analysis.md` | ✅ cluster table | ✅ diagnosis-not-prescription | ✅ |
| S25–28 records → next run (§0) | orchestrator (002) | ✅ results/learnings/ledger/state | ✅ | ✅ verbatim verdict/lesson | ✅ |

**No handoff in the happy path is dropped, ambiguous, or undiscoverable.**

---

## Risks / deviations worth noting (do NOT block happy path)

1. **`loop/reference-alignment.md` table_ is still `[fill after plan accepted]`**
   on `main` @ afca11f. A happy-path 001 run assumes baseline 000 filled it;
   if baseline did NOT complete the table, the judges would lack the aligned
   GSBS chapter and the run would stall — that would move the verdict off
   COMPLETES. Treated as baseline-completed per the task framing. ⚠️ low-risk
   if baseline's §4 Step 4 filled it.
2. **State file lag authorizes the orchestrator to trust on-disk markers over
   `state.md` (§0).** Harmonious here (KEEP done → markers present → IDLE
   written), but a crash between marker-write and state-write relies on the
   marker cross-check to resume — not an error, just noted.
3. **Hypothesis model (Sol) vs analyzer/judges (Luna)** — per config; no
   conflict in the traced flow (different roles, clean contexts).
4. **REUSE depends on acceptance of the previous campaign's research bank.**
   The dry run assumes research artifacts exist and are valid; otherwise
   `research_reuse.sh` SAFE-fails to RERUN (a slower but still correct path).

---

## VERDICT: **COMPLETES**

The happy path for iteration 001 closes every transition from
"founder authorizes iteration 001" to terminal `IDLE` with records committed and
the KEEP promoted to the campaign branch. The sole deterministic decision
(research REUSE) is correctly exercised, the whole book regenerates and is
judged in parallel, the trace analyzer maps the cluster to its root component,
the KEEP decision is evidence-valid (all judges completed), and every handoff
receiver discovers/parses/trusts/continues its input from a canonical, stable
path. **No BLOCKED or UNDEFINED steps.**

With Risk 1 (reference-alignment filled before iter-001 judging) verified
during a real run, the verdict holds as COMPLETES. Absent that table, it would
downgrade to COMPLETES-WITH-RISK.
