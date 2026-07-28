# Auto-Tuning Loop — PROGRAM

> The operating system for the book factory tuning loop. A coding agent reads
> this and executes it. One iteration per run. North Star: `docs/AUTO-TUNING-LOOP.md`.

## 0. Recovery

Read this file, `docs/AUTO-TUNING-LOOP.md`, `loop/learnings.md` (tail), and
`loop/results.tsv` (last line). State the last iteration, its verdict, and the
next hypothesis before acting.

## 1. File ownership

**Editable (the tuning surface):**
- `prompts/style-guide.md`
- `prompts/chapter-writer.md`
- `prompts/chapter-reviewer.md`
- `prompts/master-plan-skill-v2.md`
- `prompts/research-agent.md`
- `prompts/research-evidence-editor.md`
- `prompts/chapter-commissioner.md`
- `production-books/quit-sugar/` (all outputs)
- `loop/config.yaml` (model choices, parameters)

**Read-only (never edit):**
- `calibration/reference/gsbs/` (the real book)
- `analysis/sugar-prose-patterns.md`
- `docs/AUTO-TUNING-LOOP.md`
- `docs/BOOK-FACTORY-VISION.md`
- `loop/PROGRAM.md` (this file)
- `loop/judges/` (judge prompts — tuned separately by founder)

## 2. One iteration

### Step 1: Declare hypothesis

Write `loop/iterations/NNN/hypothesis.md` with exactly four fields:

```
## Failure evidence
[What the judge panel found. Quote specific passages.]

## Root cause
[Why the factory produced this gap. Which component is responsible?]

## Targeted fix
[Exact change to exact file and section. One change only.]

## Predicted impact
[What will improve. What might regress. How we'll know it worked.]
```

Check `loop/learnings.md` — never repeat a failed hypothesis.

### Step 2: Apply the change

Edit exactly one file from the editable list. Record the diff in
`loop/iterations/NNN/change.diff`.

### Step 3: Run the factory

Generate chapters 1-3 of quit-sugar using the current prompts and config.

**Research** (if research stage is targeted):
- Model: DeepSeek V4 Pro via OpenRouter
- Search depth: unlimited (1,000+ searches, 1,000+ fetches)
- Lanes: lived-experience, scientific-mechanistic, industry-cultural,
  pro-behavior-counter-corpus, dialect-sensory
- Output: `production-books/quit-sugar/research/`

**Planning** (if planning stage is targeted):
- Model: per `loop/config.yaml` planner_model
- Input: style guide + brief + framing + research syntheses
- Output: `production-books/quit-sugar/master-plan.md`

**Writing** (always, unless only research/plan is being tested):
- Model: Muse Spark 1.1 via OpenRouter (reasoning: high, temp: 0.7)
- Input: commission + style guide + previous chapter
- Output: `production-books/quit-sugar/chapters/chapter-NN.md`

Save generation traces in `loop/iterations/NNN/traces/`.

### Step 4: Judge

Run all three judges on each generated chapter vs its matched reference:
- `loop/judges/belief-mechanic.md`
- `loop/judges/voice-emotion.md`
- `loop/judges/reader-journey.md`

Each judge receives: the judge prompt, our chapter text, the real GSBS
chapter text (from `calibration/reference/gsbs/`). Chapter N maps to
reference file `N+2` (offset 2 for front matter).

Save verdicts in `loop/iterations/NNN/judgments/`.

### Step 5: Decide

Read all judge verdicts. Answer one question: **Did the predicted gap close?**

- **KEEP** — the gap closed or materially improved. No regression on other
  dimensions. The change stays.
- **REVERT** — the gap did not close, or a worse regression appeared.
  Undo the change (restore from `change.diff`).

Write `loop/iterations/NNN/decision.md` with the verdict and reasoning.

### Step 6: Record

Append one line to `loop/results.tsv`:
```
iter\tdate\thypothesis\tcomponent_changed\tpredicted_impact\tjudge_verdict\tdecision\tlesson
```

Append to `loop/learnings.md`:
```
### iter-NNN — [short title]
**Hypothesis:** [one line]
**Change:** [file + what changed]
**Verdict:** KEEP/REVERT
**Lesson:** [what we learned about the factory]
**Next direction:** [what to try next based on this]
```

## 3. Rules

- **One hypothesis per iteration.** One change to one file. No bundles.
- **3-strike rule.** If the same failure class persists 3 iterations,
  abandon that approach entirely. Try a different level:
  prompt → structure → model → research.
- **Convergence rule.** After 5 consecutive iterations with no KEEP,
  stop. Write a summary in `loop/iterations/NNN/convergence-report.md`
  and surface to the founder.
- **Never edit judges during an iteration.** Judge calibration is a
  separate founder-guided activity.
- **Never edit this PROGRAM.md.** The loop follows it; it does not change it.
- **Prediction binds the decision.** If the prediction said "voice will
  improve" and voice didn't improve but something else did, that's
  INCONCLUSIVE, not KEEP. Revert and form a better hypothesis.

## 4. Models (starting config)

Recorded in `loop/config.yaml`:
```yaml
writer_model: meta/muse-spark-1.1
writer_reasoning: high
writer_temperature: 0.7
writer_endpoint: https://openrouter.ai/api/v1/chat/completions

researcher_model: deepseek/deepseek-v4-pro
researcher_endpoint: https://openrouter.ai/api/v1/responses
researcher_reasoning: xhigh

planner_model: kimi-k3
planner_endpoint: TBD

judge_route: codex-native
```

These are starting points. The loop can hypothesize model changes.

## 5. Generalization check

After the judge panel says "this reads like Carr" for GSBS chapters 1-3,
run a generalization test:

1. Create `production-books/quit-smoking/` with a brief for smoking cessation
2. Run the factory with ZERO subject-specific tuning
3. Judge against a smoking reference (if available) or against the panel's
   internal model of Carr
4. If it passes: the factory works. If not: continue tuning with both
   subjects as signal.

## 6. What success looks like

The loop succeeds when:
1. The judge panel reads our GSBS chapters and says they do belief change
   the way the real book does
2. The factory produces a convincing Carr-style book for a novel subject
3. `loop/learnings.md` explains WHY the factory works
