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

## 2. Baseline (iteration 000)

Before the first hypothesis, establish where we are:

1. Run the factory on quit-sugar chapters 1-3 (Step 3 below)
2. Run the judge panel (Step 4 below)
3. Record the baseline verdicts in `loop/iterations/000/`
4. Append to learnings: "Baseline established. Top gaps: [list]."

No hypothesis, no change. Just: where are we starting from?

## 3. One iteration (001+)

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

**How to make API calls:**

All model calls go through OpenRouter. Use curl or a simple script:

```bash
# Chat completions (writer, planner)
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "meta/muse-spark-1.1", "messages": [...],
       "reasoning": {"effort": "high"}, "temperature": 0.7}'

# Responses API with tools (research — enables web search + fetch)
curl https://openrouter.ai/api/v1/responses \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "deepseek/deepseek-v4-pro", "input": "...",
       "reasoning": {"effort": "xhigh"},
       "tools": [{"type": "web_search"}, {"type": "web_fetch"}]}'
```

The `OPENROUTER_API_KEY` env var must be set. Judges use Codex sub-agents
(spawn_agent), not OpenRouter.

**Research** (if research stage is targeted):
- Model: DeepSeek V4 Pro via OpenRouter
- API: Responses API with web_search + web_fetch tools enabled
- Search depth: unlimited (1,000+ searches, 1,000+ fetches)
- Lanes: lived-experience, scientific-mechanistic, industry-cultural,
  pro-behavior-counter-corpus, dialect-sensory
- The research prompt (`prompts/research-agent.md`) is the system prompt.
  The model uses web_search and web_fetch tools autonomously to find
  lived experiences, forums, Reddit, scientific papers, industry analysis.
- Output: `production-books/quit-sugar/research/`

**Planning** (if planning stage is targeted):
- Model: per `loop/config.yaml` planner_model
- Input: style guide + brief + framing + research syntheses
- Output: `production-books/quit-sugar/master-plan.md`

**Writing** (always, unless only research/plan is being tested):
- Model: Muse Spark 1.1 via OpenRouter (reasoning: high, temp: 0.7)
- Input assembly (the writer receives exactly 3 things):
  1. The commission: the chapter's semantic authority from the master plan
     (the chapter card from `production-books/quit-sugar/master-plan.md`)
  2. The style guide: `prompts/style-guide.md`
  3. The previous chapter: `production-books/quit-sugar/chapters/chapter-(N-1).md`
     (for chapter 1, use the master plan's book-core section instead)
- The writer prompt (`prompts/chapter-writer.md`) is the system prompt.
- Output: `production-books/quit-sugar/chapters/chapter-NN.md`

Save generation traces in `loop/iterations/NNN/traces/`.

**Trace format (mandatory):**
```
loop/iterations/NNN/traces/
  research/              # research outputs (if research was run)
  plan.md                # master plan used (copy)
  chapter-01/
    prompt.md            # exact system + user message sent to writer
    response.md          # exact model response (the chapter)
    metadata.json        # model, tokens, latency, errors
  chapter-02/ ...
  chapter-03/ ...
```

**Error handling:**
- API 429/rate limit: retry 3x with 30s/60s/120s backoff.
- Model refusal: log in traces/chapter-NN/refusal.md, skip chapter.
- Garbage output: re-run once. If still garbage, log and skip.
- Judge timeout: re-run once. If still failing, proceed with 2 judges.
- Never silently continue. Every error is logged in traces.

### Step 4: Judge

Run all three judges on each generated chapter vs its matched reference:
- `loop/judges/belief-mechanic.md`
- `loop/judges/voice-emotion.md`
- `loop/judges/reader-journey.md`

Each judge receives: the judge prompt, our chapter text, the real GSBS
chapter text (from `calibration/reference/gsbs/`), and CHAPTER CONTEXT:
"This is chapter N. Its role: [from master plan]. Previous chapter landed:
[one-line summary]." For chapters 2+, also pass the previous chapter.

**Reference alignment:** Use `loop/reference-alignment.md` to map our
chapters to GSBS chapters by CONTENT, not just offset. Create this
alignment table before the baseline run.

Save verdicts in `loop/iterations/NNN/judgments/`.

### Step 5: Decide

Read all judge verdicts. Answer one question: **Did the predicted gap close?**

- **KEEP** — the targeted gap improved materially AND no regression
  appeared. The improvement may manifest differently than predicted —
  that's fine. What matters: is the book better?
  Regression check: compare this iteration's verdicts to the previous
  iteration's. Any gap ABSENT before but PRESENT now = regression.
- **REVERT** — the targeted gap did NOT improve, OR a material regression
  appeared. Undo the change.
- **INCONCLUSIVE** — no improvement, no regression. Revert and sharpen
  the hypothesis.

Record prediction accuracy: "Predicted X. Observed Y. [accurate/partial/wrong]."

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

## 4. Rules

- **One hypothesis per iteration.** One change to one file. No bundles.
- **3-strike rule.** Failure class = same judge + same criterion + same
  root component. If 3 iterations targeting one class produce no KEEP,
  ROLLBACK and PIVOT to a different component level. The level is wrong.
  Example: 3 failed writer-prompt fixes for hedging → try style guide
  or model instead. Don't keep hammering the same level.
- **Convergence rule.** After 5 consecutive iterations with no KEEP,
  stop. Write a summary in `loop/iterations/NNN/convergence-report.md`
  and surface to the founder.
- **Never edit judges during an iteration.** Judge calibration is a
  separate founder-guided activity.
- **Never edit this PROGRAM.md.** The loop follows it; it does not change it.
- **Prediction informs, evidence decides.** A wrong prediction with a
  real improvement is KEEP (note the prediction was wrong). A right
  prediction with no improvement is REVERT.

## 5. Models (starting config)

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

## 6. Generalization check

After the judge panel says "this reads like Carr" for GSBS chapters 1-3,
run a generalization test:

1. Create `production-books/quit-smoking/` with a brief for smoking cessation
2. Run the factory with ZERO subject-specific tuning
3. Judge against a smoking reference (if available) or against the panel's
   internal model of Carr
4. If it passes: the factory works. If not: continue tuning with both
   subjects as signal.

## 7. What success looks like

The loop succeeds when:
1. The judge panel reads our GSBS chapters and says they do belief change
   the way the real book does
2. The factory produces a convincing Carr-style book for a novel subject
3. `loop/learnings.md` explains WHY the factory works
