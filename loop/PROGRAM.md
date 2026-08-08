# Auto-Tuning Loop — PROGRAM

> The operating system for the book factory tuning loop. A coding agent reads
> this and executes it. One iteration per run. North Star: `docs/AUTO-TUNING-LOOP.md`.
> Every iteration generates and judges the WHOLE book — chapters change what
> they optimize across the arc, so partial runs measure the wrong thing.

## 0. Recovery

Read this file, `docs/AUTO-TUNING-LOOP.md`, `loop/learnings.md` (tail), and the
last DATA row of `loop/results.tsv`, ignoring the header. If no data row
exists, state `baseline pending` and run Section 3. Otherwise state the last
completed iteration, its verdict, and the next hypothesis before acting.

## 1. File ownership

**Editable (the tuning surface):**
- `prompts/style-guide.md`
- `prompts/research-agent.md`
- `prompts/research-evidence-editor.md`
- `prompts/master-plan-skill-v2.md`
- `prompts/master-plan-reviewer-v2.md`
- `prompts/chapter-writer.md`
- `loop/config.yaml` (routes, models, parameters)

Generated research, framing, plans, and chapters under
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
pins its model per `loop/config.yaml`. All roles route their model calls
through the founder's Command Code proxy loopback (credential via
`COMMANDCODE_API_KEY` or the founder's Command Code CLI login). A role call
carries ONLY its role prompt and the listed inputs: no host system prompt, no
shared context with sibling roles. Nothing else ever uses the proxy. No
fallback route is coded: a missing credential or unreachable proxy stops the
run and escalates to the founder.

Spawned roles (agent → contract prompt):
- `researcher` — `.pi/agents/researcher.md` → `prompts/research-agent.md`;
  orchestrator/lead runs on MiniMax M3 (commandcode), the spawned research
  sub-agents on GPT-5.6 Luna max (openai-sub)
- `evidence-editor` — `.pi/agents/evidence-editor.md` →
  `prompts/research-evidence-editor.md`
- `framing`, `framing-reviewer` — `.pi/agents/framing*.md` →
  `production-books/_template/framing.md`
- `plan-writer`, `plan-reviewer` — `.pi/agents/plan-*.md` →
  `prompts/master-plan-skill-v2.md` / `prompts/master-plan-reviewer-v2.md`
- `chapter-writer` — `.pi/agents/chapter-writer.md` →
  `prompts/chapter-writer.md`
- `judge` — `.pi/agents/judge.md` → `loop/judges/*.md`; GPT-5.6 Luna high via
  the OpenAI subscription (openai-sub)
- `trace-analyzer` — `.pi/agents/trace-analyzer.md` → `loop/prompts/
  trace-analyzer.md`; GPT-5.6 Luna high via openai-sub
- `hypothesizer` — `.pi/agents/hypothesizer.md` → `loop/prompts/
  hypothesizer.md`; GPT-5.6 Sol high via openai-sub

**The orchestrator manages the loop** (per this file): it spawns roles, hands
them their exact inputs, runs the deterministic gates, saves traces, and
makes the intelligent decisions on failure — retry a failed role once, then
INCONCLUSIVE or escalate to the founder. Mechanical checks stay deterministic
tools the orchestrator runs: the validity gate
(`scripts/validate_chapter_anatomy.py`), web primitives
(`scripts/loop-runner/web_tools.py`), and the canonical gate.

**State discipline:** the campaign runs on a campaign branch. Every iteration
ends with exactly one commit (`loop(iter-NNN): DECISION — short hypothesis`).
Only the founder merges winning amendments to `main`.

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

Where is the factory now? Fresh full run, no hypothesis, no change.

1. Run the factory END TO END per Step 3 below: research → framing → plan →
   full book. Nothing is reused from before the campaign; the current factory
   must own every artifact and trace it produces.
2. Build `loop/reference-alignment.md` from the freshly accepted plan (its
   procedure lives in that file).
3. Validity-gate and judge every chapter, plus the book-arc judge (Step 4).
4. Run the trace analyzer (Step 5). Save `loop/iterations/000/trace-analysis.md`.
5. **A/A noise check (once):** regenerate chapter 01 a second time from the
   identical inputs (master plan, chapter card, style guide, previous
   chapter); judge it. If the material failure-class
   set differs between the two runs, record the observed noise level in
   `loop/learnings.md` — decisions compare failure classes, never instances,
   and this calibrates what "material" means.
6. Append a `BASELINE` row to `loop/results.tsv` and a learnings entry:
   "Baseline established. Top causal clusters: [list]."

## 4. One iteration (001+)

### Step 1: Declare hypothesis

Spawn the `hypothesizer` sub-agent (contract: `loop/prompts/hypothesizer.md`)
with:
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
generation**. Reuse only artifacts upstream of the change. A research,
framing, or planning hypothesis is never judged without regenerated chapters.

**Stage: Research** — rerun ONLY when the hypothesis changed the research
stage (research prompt, evidence editor, researcher model/params) or the
brief. Deep research is slow; when unchanged, reuse the last accepted
research artifacts and copy them into this iteration's traces.
- The orchestrator (the pi coding agent) IS the research lead. It reads
  `prompts/research-agent.md`, fills the parameter block, and runs one
  relentless search for depth: it searches and fetches itself via
  `scripts/loop-runner/web_tools.py`, and spawns fresh research sub-agents
  with the `subagent` tool (project agent `.pi/agents/researcher.md`,
  parallel mode) per lane, persona, and community. Each sub-agent mines and
  writes source-traceable packets into the ten research banks. The
  orchestrator integrates, names the gaps, and dispatches again — until the
  completion criterion in the research prompt clears across at least three
  personas. Lived experience from recovery communities is the primary
  target; scientific studies are secondary.
- Route/model per config (researcher model via the Command Code proxy).
- Depth is sacred and unlimited: go as wide and deep as still brings
  results; filter afterwards, never limit upfront.
- Gate: a fresh independent editor per `prompts/research-evidence-editor.md`
  must return PASS on the research digest before framing may consume it.
- Output: `production-books/quit-sugar/research/`

**Stage: Framing** — the orchestrator spawns the `framing` sub-agent, which
completes `production-books/quit-sugar/framing.md` per the framing contract
(`production-books/_template/framing.md`) from the style guide, brief, and
accepted research syntheses; then the orchestrator spawns the
`framing-reviewer` sub-agent and hands the result back to the framing agent,
iterating until the review is accepted in `framing-review.md`. Planning is
blocked until accepted.

**Stage: Planning** — the orchestrator spawns the `plan-writer` sub-agent
(follows `prompts/master-plan-skill-v2.md`; exact five inputs, no reference
contamination), then the `plan-reviewer` sub-agent
(`prompts/master-plan-reviewer-v2.md`), handing the plan back to the
plan-writer until `master-plan-review.md` ends `fit to write from`. When the
accepted plan changed, rebuild `loop/reference-alignment.md` before judging.

**Gate before dispatching the writer (per chapter):** extract the target
chapter card from the accepted plan and verify it resolves directly against
the plan-wide inventories:
  `grep -En '(MN|IN|EV-[LS]|RD|AN|ST|PR|CH|BG|RS|AU|LEU|SEU)-?[0-9]+' <card>`
  A card legitimately cites plan-wide IDs (the normalization law forbids
  copying inventory rows into cards), so an ID itself is not a defect: every
  cited ID must have a matching plan-wide inventory entry with a non-empty
  payload. An ID with no matching entry — or an entry with an empty payload —
  blocks dispatch as an orchestration failure, not a plan failure. The plan
  review gate already guarantees cards are writable directly; this check is
  the mechanical backstop.

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

**Validity gate (per chapter, before judging):** run
`scripts/validate_chapter_anatomy.py` with the chapter and its assignment
manifest (instruction wording, mantra wordings, banned register — extracted
from the accepted plan). It checks the writer-contract anatomy facts:
preview, thesis line, SUMMARY, assigned instruction present verbatim,
assigned mantras present verbatim, banned-register hits, non-mantra verbatim
repetition (within chapter and against all prior chapters). Judges never
check presence; they judge effect. A chapter that fails the gate is rerun
once; if still invalid, the iteration is INCONCLUSIVE and the validity
failure becomes the next hypothesis's failure evidence.

**Trace format (mandatory):**
```
loop/iterations/NNN/traces/
  research/              # exact accepted research inputs used by this run —
                         # copied every iteration; call traces added when rerun
  framing.md             # framing used (copy)
  plan.md                # accepted master plan used (copy)
  chapter-01/
    chapter-card.md      # the target chapter card used (copy)
    prompt.md            # exact system + user message sent to writer
    response.md          # exact model response
    anatomy.json         # validity gate result
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

A decision is valid only when every written chapter passed the validity
gate and every judge report completed (after retries). Otherwise the
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

KEEP: retain the source change and the generated artifacts (they are the new
accepted state). REVERT / INCONCLUSIVE: restore the edited file AND all
generated artifacts to the last accepted commit (`git checkout <last-KEEP>
-- <tuning-file> production-books/quit-sugar/`); the iteration directory
itself is always kept.

Record prediction accuracy: "Predicted X. Observed Y. [accurate/partial/wrong]."
Write `loop/iterations/NNN/decision.md` with the verdict and reasoning.

### Step 7: Record

Append one tab-separated data row to `loop/results.tsv` matching the existing
header. Do not append the header again.

Append to `loop/learnings.md`:
```
### iter-NNN — [short title]
**Hypothesis:** [one line]
**Change:** [file + what changed]
**Verdict:** BASELINE/KEEP/REVERT/INCONCLUSIVE
**Lesson:** [what we learned about the factory]
**Next direction:** [what to try next based on this]
```

Commit the iteration on the campaign branch.

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
