# Auto-Tuning Loop — North Star

> Founder-locked vision for the auto-research loop that tunes the book factory.
> This document is the operational North Star. `BOOK-FACTORY-VISION.md` remains
> the product vision; this is how we get there.

## Mission

Build an auto-research loop around the book factory that tunes it through
experimentation until it reliably produces Allen Carr Easyway-style books for
any input subject. The loop changes anything inside the factory — prompts,
models, research process, planning process, structure — based on evidence from
direct comparison with a known Carr book.

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
1. RUN FACTORY   — research → framing → plan → write chapters
2. COMPARE       — Judge panel reads our chapters + real GSBS chapters
                   "What's working? What's not? Where are we not Carr?"
3. TRACE ANALYSIS — Read the generation traces. What happened during writing?
                   Where did the writer diverge from intent? What did the
                   research provide or fail to provide?
4. DIAGNOSE      — Map each gap to a factory component:
                   research? framing? plan? writer prompt? style guide? model?
5. HYPOTHESIZE   — One change to one factory component, with prediction:
                   "If we change X, then gap Y will close because Z"
6. APPLY         — Make the change
7. RE-RUN        — Re-run affected stage(s)
8. COMPARE AGAIN — Same judge panel, same comparison
9. KEEP/REVERT   — Did the gap close? Keep. Did it not? Revert.
10. RECORD       — What we tried, what happened, what we learned
11. REPEAT       — Next gap. 3-strike rule (same failure 3× → abandon approach).
                   Stop when the judge panel says "this reads like Carr."
```

## The Judge Panel

The judges are the critical piece. If they optimize for the wrong thing, we
get the wrong results. The panel must be tuned carefully.

**What judges do:**
- Read our chapter and the corresponding real GSBS chapter side by side
- Say what's working and what's not, in terms of belief change effect
- Identify where ours feels like a generic AI book instead of Carr
- Assess whether the reader's belief would actually shift reading our version
- Compare emotional movement: does ours build, escalate, and land like Carr?

**What judges do NOT do:**
- Score sentence length, word count, or surface formatting metrics
- Blind comparison (we know which is ours — that's the point)
- A/B preference testing
- Optimize for "sounding literary" divorced from belief-change effect

**Panel composition:** Multiple judges with slightly different lenses:
- One focused on belief-change mechanics (does the argument land?)
- One focused on voice and emotional register (does it feel like Carr?)
- One focused on the reader journey (would a real reader be moved?)

The panel's calibration is itself part of what the loop tunes. If the judges
are wrong, we fix the judges.

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
- Reviewer/judge prompts
- Models (writer, planner, researcher, judge)
- Chapter structure and anatomy decisions
- Framing decisions
- Commission structure
- Any other factory component

## Deep Research

The research stage must be as wide and deep as still brings results. No
artificial limits on search count or fetch count. DeepSeek V4 Pro is
essentially free; the constraint is quality of results, not cost. Allow
1,000+ searches and 1,000+ fetched resources if that's what it takes.
Filter results afterwards — never limit the search upfront.

The research must find people who have shame and are willing to share.
Many subjects are sensitive (pornography, addiction, compulsive behavior).
The lived-experience lane must go into forums, Reddit, support communities,
and niche spaces where people confess, describe, and narrate their
experience honestly. This is the material that makes the book feel like it
was written by someone who truly understands the reader's situation.

The existing research factory provides:
- 5 lanes: lived experience, scientific-mechanistic, industry-cultural,
  pro-behavior-counter-corpus, dialect-sensory
- Web search and content fetching via OpenRouter tools
- Configurable ceilings (to be raised or removed for production use)

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
- **One hypothesis per iteration.** Small, reversible changes. We can
  attribute effect because we changed one thing.
- **Prediction-based attribution.** Every hypothesis predicts what will
  improve. If the prediction doesn't hold, the hypothesis is wrong regardless
  of score movement.
- **3-strike rule.** Same failure class persists 3 iterations → abandon that
  approach and try a different level (prompt → structure → model → research).
- **Convergence rule.** Stop after 5 consecutive iterations with no
  improvement. Surface findings to the founder.
- **Learnings accumulate.** Every iteration (pass or fail) appends to a
  learnings file. The loop never repeats a failed hypothesis.

## Models (Starting Point, Not Fixed)

- Writer: Muse Spark 1.1 via OpenRouter
- Research: DeepSeek V4 Pro via OpenRouter
- Planning: Kimi K3 (or alternative — the loop can change this)
- Judges: Codex sub-agents (GPT-5.6 Sol)

These are starting points. If a model can't produce Carr-quality output after
prompt tuning, the loop hypothesizes a model change and tests it.

## Success Criteria

The loop succeeds when:
1. The judge panel reads our GSBS chapters and says they do belief change the
   way the real book does
2. The factory produces a convincing Carr-style book for a novel subject
   (generalization check) without subject-specific tuning
3. The loop's learnings explain WHY the factory works, not just THAT it works
