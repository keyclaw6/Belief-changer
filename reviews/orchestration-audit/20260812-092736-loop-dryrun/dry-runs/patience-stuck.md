# Dry Run — Patience / Stuck-Detection path (thrust 2, sen B)

**Audited revision:** `main` @ afca11f (verified `git rev-parse --short HEAD` = `afca11f`).
**Mode:** read-only simulation. No file edits outside this report's output bank, no model calls.
**Normative source:** `loop/PROGRAM.md` §4 Step 3 "Patience" + §1 Error handling + §0 Recovery; `loop/config.yaml`; `.pi/agents/*.md`; `scripts/loop-runner/daemon.sh`, `queue_runner.sh`, `research_reuse.sh`; `AGENTS.md`; `docs/AUTO-TUNING-LOOP.md`; SOURCE_OF_TRUTH.md.
**In scope:** the PATIENCE / STUCK-DETECTION path (§4 Step 3 Patience block) and failure handling (§1 retry-once, §4 error handling), mechanically against the stage-daemon / queue-runner `.exit` markers under `.loop-work/`.

---

## 0. Ground truth read by the dry run

- **The runner is a human-coded orchestrator** reading `PROGRAM.md` §4 Step 3. Deterministic code exists only for `research_reuse.sh` + `check.sh` + `web_tools.py`; everything else is the orchestrator acting on marker observation.
- **Marker authorship.** Two distinct marker writers, two distinct trees (both under the repo root, `$(dirname "$0")/../../.loop-work/…`):
  - `daemon.sh` (`$NAME`) → `.loop-work/daemons/<name>.exit` (+ `.log`, `.pid`). Self-exits when the wrapped command returns and writes its exit code.
  - `queue_runner.sh` → `.loop-work/queue/done/<name>.exit` (+ `logs/`, `runner.status`, `STOP`). Notive: it runs "indefinitely" (a long-lived loop), writing a job's `.exit` only after that job's process returns.
- **Stack relationship.** PROGRAM.md labels both `.exit` variants the stage markers the runner waits on. `.loop-work/` is the watcher registry; content markers (research bank files, `chapters/`, `judgments/`, `traces/`) are corroboration.
- **Current state (`loop/state.md`):** Iteration 000 (baseline), `Status: IDLE`, next unit = baseline research. No iteration worktree active, no `.loop-work/` present on disk. Conflict-free for the traced scenarios (all of which run inside an iteration worktree).

### Marker-behavior observations baked into the traces

1. **`.exit` is written once, exactly when the wrapped process returns** (`daemon.sh` line 17: `"$*; echo \$? > '$DONE'"`). It is not a heartbeat and does not move while a process is *running*. So ".exit marker present" is unambiguously the "stage finished in a daemon wrapper" signal (scenario c).
2. **`.exit` is removed at spawn** (`daemon.sh` line 16 `rm -f "$DONE"`) — so between spawn and its eventual write, the `.exit` path simply does not exist. Absence-of-`.exit` is therefore NOT a liveness signal on its own; it only means "not yet recorded as finished."
3. **A stage run under the queue steadily advances `runner.status`** (`queue_runner.sh` line 21/26 write "running…/finished…" timestamps) — a *moving* marker a healthy long job produces even while no content appears.
4. **For the writer specifically there is no daemon/quework wrapper at all** — the orchestrator spawns `chapter-writer` as a sub-agent with the `subagent` tool (PROGRAM §3, Writing; §1 role calls) and saves `chapter-NN/response.md`. Its "markers" are content (chapters written, traces saved), which is exactly why "stopped markers" for the writer are really "production stopped + removed `.exit`/`.pid`" — an invalidation gap the traces flag.

---

## Scenario (a) — Healthy 6-hour research stage

**Setup.** Iteration NNN, hypothesis changed the research stage ⇒ `research_reuse.sh` printed `RERUN`. The orchestrator begins "Stage: Research" (PROGRAM §3 / §4 Step 3). It IS the research lead: it will itself search/fetch via `web_tools.py` and spawn/research sub-agents whose fetched artifacts land in the ten research banks under `production-books/quit-sugar/research/`. Because reruns are credential-bearing and long, the orchestrator launches the long-poll-as-daemon variant of the research run through `daemon.sh` (`RunWithCredentials` env inherited, so `COMMANDCODE_API_KEY`/openai-sub creds reach the detached child; `daemon.sh` returns immediately). It then enters the Patience block.

### Step table

| Step | Actor | Action | Marker state observed |
|---|---|---|---|
| a1 | Orchestrator | Writes `loop/state.md` → `IN PROGRESS`, stage=research, next unit=research | — |
| a2 | Orchestrator | Shells `daemon.sh research_nnn "<lead command>"`; daemon writes `$PIDF`, clears `$DONE`, starts detached log `$LOG`. Returns immediately | `.exit`: absent (cleared at spawn); `.pid` present; `.log` present/empty |
| a3 | Orchestrator | Enters Patience per §4 Step 3: updates state, then **one long wait** (sleep / scheduled wake) — not a poll loop | — |
| a4 | Orchestrator | Wakes. Reads `.loop-work/daemons/research_nnn/`: `.exit` **absent**; corroborates against content — research banks growing, `runner.status`/log timestamps advancing across the 6h | `.exit` absent; content moved & not looping; log tail timestamped mid-run |
| a5 | Orchestrator | Decision per line 208-215: markers moved, not looping ⇒ still working ⇒ **wait again** (state updated first). Repeats a4/a5 for the full 6 hours | `.exit` still absent; content continues advancing |
| a6 | Orchestrator (after ~6h) | Wakes; sees `.exit` present via `echo $?` (exit 0) AND content complete (≥3 personas clear per research prompt completion criterion) | `.exit` present; content complete |
| a7 | Orchestrator | Reads `.log` tail, checks exit 0, copies accepted research into `traces/research/`, proceeds to Stage: Planning | `.exit` consumed; research accepted |

**Verdicts.**

- Wait-without-busy-looping: **COMPLETES** — the block mandates a *single* wait + wake + marker-check per heartbeat and explicitly forbids continuous polling ("When a stage or a spawned role is running, the orchestrator does NOT poll it continuously… a long `sleep`, a scheduled wake, or a single wait").
- No spurious "stuck" verdict on the healthy run: **COMPLETES** — line 208-215 gates stuck-judgment on *both* "markers have stopped moving" AND "a fresh read of the traces shows no progress." A healthy 6h run fails the first conjunct on every wake (markers moved each cycle a1-a5), so no stuck sub-agent is ever spawned and "doing nothing while a healthy run proceeds is correct behavior."
- Overall scenario (a): **COMPLETES**. (Residual risk: because mandate is prose, a given coding agent could still *implement* a poll loop, but the block as written compels one-wait-per-check and explicit continuous-poll avoidance — so the risk is implementation-fidelity, not spec.)

---

## Scenario (b) — Genuinely wedged chapter-writer

**Setup.** Research/planning done (markers set, research reused or rerun). The orchestrator is in "Stage: Writing (sequential, chapter 01 → last)" (PROGRAM §3). It spawns `chapter-writer` via the `subagent` tool with exactly the four inputs (plan, chapter card, style guide, previous chapter); contract `.pi/agents/chapter-writer.md` → `prompts/chapter-writer.md`. **The writer goes wedged: emits nothing, `chapter-NN.md` is never written, and — critically — no `.exit`/`.pid`/`.log` marker tree for the writer ever exists**, because the Writing stage has no daemon/quework wrapper (observation 4 above).

### Step table

| Step | Actor | Action | Marker state observed |
|---|---|---|---|
| b1 | Orchestrator | Updates `loop/state.md` (stage=writing, chapter-N) → one wait | — |
| b2 | Orchestrator | Wakes; writer marker set absent by design. Checks content markers: `chapters/chapter-NN.md` absent; `traces/chapter-NN/response.md` absent; `metadata.json` absent | no `.exit`, no `.pid`, no content — whole marker set **absent**, nothing "stopped" vs "moving" |
| b3 | Orchestrator | Awaits `loop/iterations/NNN/traces/chapter-NN/response.md` (or the `.exit` the wrapper would have written). It never appears. Per Patience, waits again | still absent |
| b4 | Orchestrator | After a fresh wake: **markers stopped moving (a fortiori: never moved) AND a fresh read of the traces shows no progress.** Both conjuncts of the stuck gate (line 211-214) now hold. Spawns a **stuck-judgment sub-agent** ("a sub-agent to judge whether the run is stuck") | absent; two fresh reads confirm no progress |
| b5 | Stuck-judge | Reads fresh trace; on genuine wedge returns `STUCK` | — |
| b6 | Orchestrator | Retries the writer **once with same inputs** per §1 ("retry a failed role once with the same inputs") — the retry is itself a fresh spawn, re-entering the Patience block | stale evidence cleared; recheck cycle b2-b4 |
| b7 | Orchestrator | Wedge recurs; second failure. Per §1 + §4 error handling: no verdict on partial evidence (Step 6 "never decide on partial evidence"), iteration marked **INCONCLUSIVE** or escalated to founder if the failure is route/credential | iteration `INCONCLUSIVE`; records kept on campaign branch, change not promoted (`loop/iterations/NNN/` kept per §1, Step 7) |

**Verdict.**

- **COMPLETES-WITH-RISK** (the gate *can* fire, but the trigger is under-specified — see scenario (d) for the definitional gap):
  - Detection *via stopped markers* is only half-true here. Because the Writing stage has **no `.exit`/`.pid`/`.log` marker tree** (observation 4), the runner cannot observe "markers stopped moving" from a *watcher* — every wake sees a marker set that is absent wholesale. The block's second conjunct ("a fresh read of the traces shows no progress") is what actually catches it, and it is the sole load-bearing signal for the writer; "stopped markers" contributes nothing for this role.
  - Detection *via fresh trace read* then spawn of stuck-judgment sub-agent: **available and correct** — b4-b5 implement lines 211-214 faithfully.
  - Retry-once then INCONCLUSIVE/escalate: **COMPLETES** — §1 (retry failed role once with same inputs) and §4 error handling (INCONCLUSIVE; escalate on route/credential) are explicit and unambiguous.
  - Risk qualification is twofold: (i) the writer's wedge can only be caught by *elapsed-time-plus-no-progress* logic the block refuses to codify as a timeout (see (d)); (ii) a writer that periodically emits *truncated/noise* output (a partial `response.md`) is not caught at all — "markers moved" reads as healthy, and no "no progress" conjunct fires (this is the truncation sub-case of §4 error handling, which the block does describe but the Patience detection does not).

---

## Scenario (c) — The `.exit` marker appears (job done)

**Setup.** A daemon-wrapped stage (research rerun, `daemon.sh` patient-mode) is in flight; the orchestrator enters the same Patience cycle. The wrapped stage completes.

### Step table

| Step | Actor | Action | Marker state observed |
|---|---|---|---|
| c1 | Orchestrator | Patience wait on stage; reads `.loop-work/daemons/<name>.exit` | `.exit` **absent** (cleared at spawn) — still running |
| c2 | Stage daemon | Wrapped command returns; `daemon.sh` line 17 writes `echo $? > $DONE` and the detached child exits; `.pid` may linger | `.exit` **present** (contains exit code) |
| c3 | Orchestrator | Wakes; observes `.exit` present; corroborates content complete; reads exit code + `.log` tail; exit 0 ⇒ stage done | `.exit` present + content complete |
| c4 | Orchestrator | Proceeds to next stage (reuse accepted artifacts; copy traces per Trace format). Queue variant: reads `.loop-work/queue/done/<name>.exit` + `runner.status` tail the same way | `.exit` present in `done/` |

**Verdict.**

- **COMPLETES** — "Markers moved" (the `.exit` changed absent→present) + content completed, both required conjuncts are cleanly satisfied, so the runner observes completion and proceeds, unambiguous, no spurious stuck verdict, no timeout.
- Crossover note to (a)/(b): when the runner's wait target is the `.exit` file, **its presence, not its movement, is the completion signal**; "stopped moving" only ever means `.exit` stayed absent across two-plus reads. That asymmetry is harmless for the daemon path and is exactly what makes (c) clean while (b) is fuzzy.

---

## Scenario (d) — Is "markers stopped moving" well-defined enough to act on, given research is sacred/unlimited?

**The conflict, verbatim.**

- Line 208-211: "There is no fixed per-stage timeout: deep research is sacred and unlimited, so a stage is never declared stuck on **elapsed time**. Only when markers have **stopped moving** AND a fresh read of the traces shows **no progress** does the orchestrator spawn a sub-agent to judge whether the run is stuck."
- North Star (AUTO-TUNING-LOOP.md "Deep Research") / `AGENTS.md` "Sacred": "No artificial limits on search count or fetch count… Filter afterwards, never limit upfront… No agent may impose search or fetch ceilings."
- "Stopped moving" is inherently a time-derived predicate — it is defined on *changes in marker state across two reads at two times*. If a stage is never allowed to be declared stuck "on elapsed time," and "stopped moving" requires observing elapsed time between two no-change reads, those two directives collide: over a fixed wall-clock span, a marker set that is simply *absent* (writer case) or *idle* is silently consistent with both "wedged" and "legitimately paused" because the block supplies no threshold at which non-movement earns a stuck-judgment.

**Definitional gaps (what the predicate is and is not):**

1. **"Stopped moving" has no quantitative and no qualitative anchor.** No unit (youngest-mtime delta, log tail timestamps, runner.status deltas), no refresh interval, no miss-count that upgrades "not moved lately" into "stopped," and no liveness steam from the queue's `runner.status`/`STOP`. The only quantity available is *when the orchestrator happens to wake*, which is not a measurable liveness threshold.
2. **"Fresh read of the traces shows no progress" is the real gate but has no time signature either.** For the research lead it is re-declared as deliberately non-terminating: a healthy research run *can look* 100% idle between dispatch gaps yet is mandated not to be judged stuck ("no fixed timeout… deep research is sacred and unlimited"). Nothing in the spec pins how long "no progress" must hold before it ceases to be "a paused, thinking lead" and becomes "stuck."
3. **The writer (no daemon wrapper) has no moving-marker to staleness-test** (observation 4) — the predicate cannot even be applied; only the no-progress conjunct works, and it too lacks a time bound.
4. **Catchable vs. uncatchable.** "Markers stopped moving" will catch: a *daemonized* stage whose process died (`.pid` gone, `.exit` never written, mtime frozen), a *queue* stage where the queue runner died (`runner.status` frozen, `STOP` untouched). It will NOT catch: a writer that wedges while its wrapper/session is live, or a sub-process that wedges *inside* a still-alive daemon/log session (log mtime may tick from the process's own heartbeat) — precisely the deep beaded-loops a "sacred/unlimited" stage is most prone to.
5. **Where the escape valve lives.** Because no elapsed-time rule is permitted, the spec pushes the termination decision onto a **stuck-judgment sub-agent** (line 211-214). That is a *judgment* call, not a deterministic threshold — but the block gives the sub-agent *no contract prompt* (PROGRAM.md names the analyst pipeline agents — trace-analyzer, hypothesizer — but no `.pi/agents/stuck-judge.md` / `loop/prompts/stuck-judge.md` exists in this repo; grep confirms zero `stuck` hits across all `.sh`/`.md`). The sub-agent receives "traces + marker sample" with no scoring rubric, no definition of stuck, no escalation trigger, i.e. exactly the same under-specified predicate it is asked to adjudicate.

**Verdict.**

- **COMPLETES-WITH-RISK** for the bounded-role sub-cases (destroyed daemon/quework sesion ⇒ `.exit` absent + `.pid` dead + frozen mtime ⇒ stuck-judge fired correctly), because "no output, markers stop" does produce a workable observation for those two wrappers.
- **UNDEFINED** for the *definition of "stuck" as a validable, act-on-able predicate*, and critically for the **research lead** role, because:
  - the sacred/unlimited directive plus no-fixed-timeout (a) prohibits the only reliable detector (a timeout), and (b) denies the predicate a time anchor, so "markers stopped moving" has no threshold at which it is safe to act;
  - the substitute detector (no-progress + judge sub-agent) is under-specified and, in the research role, is *specified to fire only on a condition research is affirmatively protected from being judged on*;
  - a genuine research deadlock can be, by construction, indistinguishable from "the sacred research lead is mid-dispatch thinking."
- Reconciliation with the audit's central claim (SOURCE_OF_TRUTH 30: "Runner is patient: waits on `.exit`/content markers, no fixed timeout, stuck judged from traces"): the sentence describes the *design intent*, and every scenario (a)-(c) satisfies it. But the intent is realized by two heterogeneous, at times divergent mechanisms, and scenario (b)'s writer + (d)'s research roll both expose where "patient" is not the same as "eventually termininates," because the only termination detector is, in those two roles, a judgment without a contract.

---

## Summary of verdicts

| Scenario | Verdict | One-line reason |
|---|---|---|
| (a) healthy 6h research wait | **COMPLETES** | One long wait + wake + marker check, explicit continuous-poll ban; markers moved each wake so stuck gate never fires ("doing nothing is correct") |
| (b) wedged chapter-writer | **COMPLETES-WITH-RISK** | Detection *via the no-progress conjunct* + retry-once + INCONCLUSIVE/escalate all work; but the writer has no `.exit` marker tree, so "stopped markers" never fires and a truncated/noise writer is also missed |
| (c) `.exit` appears (done) | **COMPLETES** | `.exit` absent→present + content complete satisfies both conjuncts; clean, unambiguous completion |
| (d) "markers stopped moving" vs sacred/unlimited | **COMPLETES-WITH-RISK** (bounded wrapper sub-cases) / **UNDEFINED** (as a general, act-on-able predicate; specifically the research-lead role) | "Stopped moving" is a time-derived predicate with no time anchor, expressly disconnected from elapsed time by the no-timeout/sacred rules; the backstop (stuck-judgment sub-agent) has no contract prompt and would adjudicate the same under-specified predicate |

**BLOCKED:** none — every scenario resolves to a stated verdict (no scenario was un-auditable).
**UNDEFINED:** scenario (d), research-lead role, and (as a knock-on) the "no-progress" conjunct in scenario (b).

---

## Material finding for the owners

The loop's stuck-detection is a **two-detector design under one name**:
- *Detector 1 (movement)* — reliable for daemon- and queue-wrapped stages (destroyed session ⇒ `.exit` stays absent, `.pid`/mtime/`runner.status` freeze). Fires for research reruns run as a patient daemon.
- *Detector 2 (no-progress)* — single load-bearing detector for the writer and for live-spawned roles; equals "absence of required artifact" and has no time or freshness bound.

**Actionable, non-functional only:** (1) decide whether the loop will allow a *time-based* stuck rule for non-research stages (writing is not sacred-unlimited) and pin it; (2) if the writer should keep no watcher, give the orchestrator a deterministic no-progress trigger (e.g., refresh-interval × miss-count, or a writer-wrap that writes a heartbeat `.html`/`.pid`+`.log` like the daemon) instead of leaving it to a contractless advisory; (3) if research is to stay unconditionally patient, *accept* that a research deadlock is not detectable and say explicitly that the loop will wait on research indefinitely — closing the "undefinable" gap by renaming it a bounded policy decision rather than a detection rule. Any of these is a change to orchestration behavior (PROGRAM.md / a prompt contract), **not** a file I touched — flag to the parent for a mutation decision.
