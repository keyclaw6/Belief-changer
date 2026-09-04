# Auto-Tuning Loop — North Star

> Founder-locked mission and invariants for the auto-research loop that tunes
> the book factory. `BOOK-FACTORY-VISION.md` remains the product vision; this
> is how we get there. Operational procedure lives only in `loop/PROGRAM.md`;
> model routes and parameters live only in `loop/config.yaml`.

## Mission

Build an auto-research loop around the book factory that tunes it through
experimentation until it reliably produces Allen Carr Easyway-style books for
any input subject. The loop changes factory prompts, research process, planning
process, and structure based on evidence from direct comparison with a known
Carr book. **Models and routes are founder-only.** The loop must never
hypothesize or apply a model, fallback-model, route, or endpoint change. If
prompt and structure tuning cannot hit the target, the founder changes models
by hand.

## Calibration Target

We tune against "Good Sugar Bad Sugar" (GSBS) by Allen Carr, which is in this
repo. We generate our version of that book and compare directly against the
real one. The goal is not blind preference or A/B testing — we already have
the target. The judge reads both and says what's working and what's not.

## What We Optimize For

**Belief change.** The book must change the reader's belief about the subject
the way Carr changes it. Not sentence length. Not word count. Not surface
metrics. The question is: does our book do to the reader what GSBS does to its
reader? Does it expose the trap, dismantle the perceived benefits, remove the
sense of sacrifice, and make change follow from corrected belief?

Secondary signals (voice, warmth, certainty, structure, emotional movement)
matter only insofar as they serve belief change.

## The Loop

```
1. RUN FACTORY   — research → plan → write ALL chapters
                   (the whole book, every iteration — chapters change what
                   they optimize across the arc, so partial runs mislead)
                   TWO independent books per iteration from the same plan
                   (replicate A and B) so writer/judge sampling is not
                   mistaken for a real effect
2. COMPARE       — Judge panel reads each replicate + real GSBS chapters
                   "Which belief-change function, reader effect, or chapter
                   transition is weaker than in the matched reference?"
3. TRACE ANALYSIS — Read both replicates' traces. What happened during writing?
                   Where did the writer diverge from intent? What did the
                   research provide or fail to provide? Clusters in both
                   replicates are signal; a cluster in only one is noise.
4. DIAGNOSE      — Map each gap to a factory component:
                   research? plan? writer prompt? style guide? model?
5. HYPOTHESIZE   — 1–3 bound changes under the convergence budget (fewer
                   and smaller as the census approaches zero), one PRIMARY
                   with a prediction
6. APPLY         — Make the change
7. RE-RUN        — Re-run affected stage(s); write and judge two books
8. COMPARE AGAIN — Same judge panel, same comparison, both replicates
9. KEEP/REVERT   — KEEP only when BOTH replicates show the targeted cluster
                   improved materially. REVERT when NEITHER improved, or
                   BOTH show the same new failure class. Disagreement
                   between A and B is INCONCLUSIVE (noise). Owning-lane
                   FAIL is not itself a veto.
10. RECORD       — What we tried, what happened, what we learned
11. REPEAT       — Next gap. 3-strike rule (same failure 3× under the same
                   judge instrument → abandon that approach). REVERT is not
                   a ban on retrying the factory change.
                   Stop when the panel finds no material gap in belief-change
                   work, reader-state transition, or voice effect against
                   the matched reference.
```

## The Judge Panel

The judges are the critical piece. If they optimize for the wrong thing, we
get the wrong results. The panel must be tuned carefully.

**What judges do:**
- Read our chapter and the corresponding real GSBS chapter side by side
- Emit `CLUSTER CENSUS`: stable class names, BLOCKING vs NOTED counts
- FAIL a chapter/book only on BLOCKING sentence tests. NOTED leaks stay
  visible so KEEP can see 17→3 without a PASS-rate collapse
- Identify where ours feels like a generic AI book instead of Carr
- Assess whether the reader's belief would actually shift

**What judges do NOT do:**
- Score sentence length, word count, or surface formatting metrics
- Fail a chapter on one greppable craft label (`trap question`)
- Fail a book because the same job used a new scene ID
- Blind comparison, A/B preference, "sounding literary" divorced from
  belief-change effect

**Panel composition:** Multiple judges with slightly different lenses:
- One focused on belief-change mechanics (does the argument land?)
- One focused on voice and emotional register (does the prose create Carr's
  reader-facing effects?)
- One focused on the reader journey (does the assigned reader-state
  transition complete?)
- One reading the whole book (the cumulative arc, the mantra system in
  execution, escalation across chapters, the ending)

If the judges are wrong, we fix the judges — as a separate founder-guided
calibration activity, never inside a factory iteration. A judge change
stops the campaign and requires a fresh baseline.

## Trace Analysis

Two signals drive hypotheses:
1. **Judge output** — what the panel says about the gap between ours and real
2. **Generation traces** — what actually happened during research, planning,
   and writing. Where did the process diverge from intent? What did the
   research provide? What did the writer do with it?

The trace, not just the score, is the unit of work. A judge says "this feels
academic." The trace shows "the research returned only clinical studies and no
lived experience, so the writer had no human material to work with." The
hypothesis then targets the research stage, not the writer.

## The Tuning Surface (Everything Is Changeable)

Nothing inside the factory is fixed. The loop can change:

- Style guide (method rules, prose engine, voice parameters)
- Writer prompt (contract, context, instructions)
- Planner prompt and planning process
- Research prompts and research process (search strategy, lanes, depth)
- Chapter structure and anatomy decisions
- Plan card contract
- Any other factory component — except the judges: judge calibration
  remains a separate founder-guided activity

## Deep Research

The research stage must be as wide and deep as still brings results. No
artificial limits on search count or fetch count. Muse Spark contributor is
the founder research pin; the constraint is quality of results, not cost. Allow
1,000+ searches and 1,000+ fetched resources if that's what it takes.
Filter results afterwards — never limit the search upfront.

The research must find people who have shame and are willing to share.
Many subjects are sensitive (pornography, addiction, compulsive behavior).
The lived-experience lane must go into forums, Reddit, support communities,
and niche spaces where people confess, describe, and narrate their
experience honestly. This is the material that makes the book feel like it
was written by someone who truly understands the reader's situation.

The loop optimizes the research stage too: are we finding the right user
experiences? The right websites? The right scientific evidence? The right
dialect and sensory material? Are we reaching the shame-filled confessions
and honest narratives that give the book its recognition power? If the
research is shallow or misdirected, the writer has nothing to work with.

## Generalization Check

After the loop converges on GSBS, we test generalization: feed the factory
"quit smoking" (or another subject) with zero subject-specific tuning. If it
produces a convincing Carr-style book, the factory works. If not, the loop
continues with the new subject as additional signal.

The goal is not to overfit to sugar. The goal is a universal Easyway-book
creation machine.

## Implementation Principles

- **Simple orchestration, clever prompts.** The loop is agent orchestration
  with well-crafted prompts, not a large codebase. The intelligence lives in
  the prompts and the judges, not in Python machinery.
- **One PRIMARY KEEP object per iteration.** Secondary changes are
  recorded predictions. Attribution is by prediction against the census,
  not by isolation.
- **Two books per iteration.** The same change is written and judged twice
  (same research, same plan, two independent full books). KEEP requires
  the improvement in both books; a one-book swing is noise, not a result.
- **Prediction-based attribution.** Every hypothesis predicts what will
  improve. Prediction guides attribution; observed material improvement
  in both replicates decides KEEP. An inaccurate prediction is recorded as a learning.
- **3-strike rule.** Same failure class persists 3 iterations *under the
  same judge instrument* → abandon that approach and try a different
  level (prompt → structure → research). Never pivot to a model change;
  stop and surface to the founder. A judge change resets the clock.
- **Convergence rule.** Stop after 5 consecutive iterations with no
  improvement. Surface findings to the founder.
- **Learnings accumulate.** Every iteration (pass or fail) appends to a
  learnings file. REVERT means the change was not promoted under the
  instrument then in force — it is evidence, not a ban. The hypothesizer
  may retry a reverted factory change, including exact prior wording,
  especially after a judge change. Do not blindly re-run the identical
  hypothesis against the same census class on the same instrument
  without a new mechanism. Founder-only model/route swaps stay forbidden.

## Models (Founder-only)

Model routes live in `loop/config.yaml` as the founder's preferred defaults.
The hypothesizer, orchestrator, and any spawned role must not edit `*_model`,
`*_fallback_model`, `*_route`, or endpoint fields. Contributor vs
non-contributor aliases of the same weights are not different models; swapping
them is not a hypothesis. Writer, plan-writer, plan-reviewer, research, and
trace-analyzer use OpenCode Go `muse-spark-1.3-contributor` as primary, Zen
`muse-spark-1.3-contributor-free` as the mid-chain (`OPENCODE_API_KEY`),
and Vercel `meta/muse-spark-1.3-contributor` as the last per-call fallback.
Cursor chapter judges stay Composer 2.5 (the 019/020 panel instrument).
the next unit always starts on the primary. If prompt and structure tuning cannot produce
Carr-quality output, the founder changes models manually.

## Success Criteria

The loop succeeds when:
1. The judge panel reads our GSBS chapters and says they do belief change the
   way the real book does
2. The factory produces a convincing Carr-style book for a novel subject
   (generalization check) without subject-specific tuning
3. The loop's learnings explain WHY the factory works, not just THAT it works
