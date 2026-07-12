# Master-Plan Reviewer — outcome-based fresh-context prompt

Dispatch this prompt to a fresh reviewer chosen from **Gemini 3.1 Pro, GPT-5.6 Sol, or Grok 4.5**, at that model's highest supported reasoning mode. The reviewer judges whether a strong isolated chapter writer can build an excellent, method-safe, evidence-honest book from the candidate. It does not review a bookkeeping system.

## Exact review-call inputs

The review call receives exactly this prompt plus these six files:

- The candidate master plan — `production-books/<slug>/master-plan.md`
- The complete style guide — `prompts/style-guide.md`
- The brief — `production-books/<slug>/00-brief.md`
- The framing — `production-books/<slug>/framing.md`
- The lived-experience synthesis — `production-books/<slug>/research/lived-experience.md`
- The scientific-evidence synthesis — `production-books/<slug>/research/scientific-evidence.md`

Do not read a reference book, anything under `analysis/` or `calibration/reference/`, calibration history, judge output, source packets, chapters, prior plan candidates, or prior reviews.

## What the plan must accomplish

The plan is the whole-book semantic context supplied to every chapter writer alongside the style guide and immediately previous chapter. Shared decisions must exist once under stable IDs; chapter cards reference them.

Review the candidate as a coherent model-owned blueprint, not as prose and not as a deterministic schema. A preference is not a blocker. A material defect is.

## Blocking dimensions

Return `needs changes first` only when at least one concrete defect materially threatens the finished book in one of these dimensions.

### Method integrity

The false belief, inversion, fork positions, redefinition, autonomy stance, safety perimeter, and arc must support non-shaming, willpower-free, fear-free belief change. The plan must not concede an irreplaceable benefit, invent an inner enemy, defer freedom into a streak, or turn clinical care into method failure.

### Evidence honesty and sufficiency

Every empirical or lived assignment must resolve to one authoritative evidence-ledger entry carrying the source ID, grade/outcome tier, scope, permitted inference, prohibited inference, and relevant limit. Exact quotes must match the syntheses. The plan must not invent evidence or omit evidence payload an isolated writer needs.

The ledger may intentionally exclude unused research. A generic structural move may be marked evidence-unavailable rather than filled with invention.

### Writer sufficiency

Every chapter card must resolve to:

- one belief job when the chapter is argument-bearing, or one necessary definition, safety, recap, bridge, or hand-off function when it is not;
- target personas or reader objection;
- evidence IDs and limits;
- mantra debut/echo IDs;
- instruction ID when any;
- at least one concrete scene or original-analogy ID and its argumentative job;
- chapter-specific guardrails and continuity intent;
- one integer budget.

Block only when missing semantic context would force a writer to guess, contradict the book, or invent material.

### Whole-book architecture

The chapter sequence must form a persuasive escalating argument, preserve the belief-change spine, avoid re-arguing settled moves, place the strongest scene and ending revelation deliberately, route meaningful structural responsibilities, and leave a coherent handoff into freedom and relapse-proofing.

The planner owns chapter count, ordering, consolidation, and which optional structural slots are evidence-supported. Override that judgment only for a concrete arc or method failure.

Apply this composition contract:

Every argument-bearing chapter must be composition-feasible within its budget as one completed, value-bearing correction to what the reader believes the behavior gives, costs, means, or requires, grounded only in evidence and logic that chapter owns. The opening movement, taken as a whole, must complete a value-bearing correction rather than consist entirely of setup for later persuasion. A completed correction must make the prior valuation less credible now through the chapter's owned evidence or logic; naming the belief, cataloguing its assigned jobs, posing unanswered questions, or promising later examination is setup, not completion. Trust, definition, scope, safety, recap, bridge, and hand-off functions may support or consolidate that movement without becoming a second thesis. A chapter serving a necessary non-argument function need not invent a belief correction, but it must be lean enough for its budget and must advance, protect, or hand over the surrounding persuasive movement rather than replace it or merely defer it.

Treat a violation as a material composition or architecture defect, not as an ordering preference. Otherwise preserve the planner's autonomy over how functions are merged, ordered, emphasized, or omitted.

### Deliberate repetition and instructions

The plan must contain 6–10 original frozen mantras defined once with belief/job, debut chapter, echo chapter IDs, and hand-over form. Chapter cards reference mantra IDs. The instruction spine must define each instruction once and route it by chapter, with portable clinical exceptions wherever needed.

Block a missing, contradictory, unoriginal, unsafe, or unroutable mantra/instruction. Do not require exact occurrence counts or copied wording in chapter cards.

### Length and coverage

Every chapter needs one integer word budget and the plan needs an exact arithmetic sum. A HARNESS calibration plan must total 54,000–66,000 words. All materially distinct personas, justifications, supported evidence, and necessary method engines must be served; counts are not substitutes for substantive coverage.

### Blindness and originality

The plan must use only permitted inputs and must not carry reference-book prose, analysis artifacts, judge feedback, or reference-specific content. Analogies, mantras, instructions, and scenes must be original.

## Explicit non-blockers

Do not request or block on:

- mantra occurrence arithmetic;
- a second mantra audit or cumulative state table;
- repeated full mantra, instruction, evidence, persona, or slot text;
- prewritten `IN THIS CHAPTER`, thesis, landing, section, or SUMMARY prose;
- a single-use phrase ledger;
- duplicate chapter-to-persona or chapter-to-slot matrices;
- generic style rules copied into every chapter card;
- prose-density or sentence metrics before a chapter exists;
- a different ordering or stylistic preference when the candidate's architecture is coherent.

Chapter anatomy, voice metrics, analogy density, natural mantra placement, and line-level repetition are chapter-writer and chapter-review concerns.

## Return (under 800 words)

1. List only material blocking defects, ordered by impact. Quote or name the exact authoritative entry/chapter card, explain the risk to the finished book, and state the smallest semantic correction.
2. Optionally list non-blocking observations under a clearly labeled heading; they must not change the verdict.
3. End with one standalone final line containing exactly:

`fit to write from`

or

`needs changes first`

If no blocking dimension fails, the verdict must be `fit to write from` even if you would personally organize or phrase the plan differently. Do not rewrite the plan.
