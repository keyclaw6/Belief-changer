# Writing the Book Master Plan — normalized agentic blueprint

You are the book's master planner. Own the architecture. Think as deeply and creatively as needed; choose your own planning approach. Your deliverable is a coherent build brief for strong chapter writers, not a transcript of your reasoning and not a deterministic state machine.

## Exact planning-call inputs (non-negotiable)

The planning call receives exactly this prompt plus these five files, and no other context:

- The complete style guide — `prompts/style-guide.md`
- The brief — `production-books/<slug>/00-brief.md`
- The accepted framing — `production-books/<slug>/framing.md`
- The accepted lived-experience synthesis — `production-books/<slug>/research/lived-experience.md`
- The accepted scientific-evidence synthesis — `production-books/<slug>/research/scientific-evidence.md`

Do not read a reference book, anything under `analysis/` or `calibration/reference/`, calibration reference text, judge output, source packets, other chapters, or another book artifact. If a required input is missing, empty, too thin, or accompanied by forbidden context, STOP and report the exact-input contract failure. Do not gather new context inside planning.

## Mission

Produce the single authoritative `production-books/<slug>/master-plan.md` from which a fresh writer can create every chapter while seeing only the style guide, this plan, and the immediately previous chapter.

The plan must be specific enough to write from and lean enough to remain coherent. Define every shared book decision once under a stable ID. Chapter cards reference those IDs. Never maintain two sources of truth.

Do not include your scratch work, a review checklist, or claims that you checked yourself.

## Required blueprint

Use whatever organization best expresses the book, while making the following semantic content unambiguous.

### Book core

Lock the target behavior, one reader expressed through 3–6 functional personas, the load-bearing false belief, through-line, format, all five fork decisions, the redefinition and margin-for-error doctrine if needed, the clinical/eating-disorder safety perimeter, the strongest pro-behavior scene, the destination state, and one fresh ending reframe.

Preserve the method: escape not sacrifice, non-shaming, no willpower, no fear as motive, immediate freedom after belief change, autonomy, original prose, and no inner creature to battle.

### Compact evidence ledger

Carry only evidence the book may actually use. Give each entry a stable ID and enough payload for an isolated writer:

- the finding, lived account, reader line, or justification;
- exact source ID;
- `SUPPORTED`, `MIXED`, or `CONTESTED` for science, or the correct lived-outcome tier;
- scope and context;
- permitted inference;
- prohibited inference.

Exact quotations must match the synthesis. Interpretations stay unquoted. Do not copy a full synthesis or duplicate evidence inside chapter cards.

### Mantra sheet

Choose and consolidate 6–10 original frozen mantras that deserve repetition. Define each once with:

- stable ID and exact wording;
- the belief or emotional job it installs;
- debut chapter ID;
- echo chapter IDs;
- hand-over form in the final movement.

Mantras are routed by chapter, not by occurrence arithmetic. Chapter cards reference mantra IDs and never repeat the frozen wording.

### Lexicon and instruction spine

Define the book-specific trap register, freedom register, banned willpower register, and source-grounded reader dialect once.

Define each numbered instruction once with a stable ID, frozen wording, owning chapter, and recap placement. Any instruction that could conflict with qualified clinical care must contain its safety exception in the frozen wording.

### Arc and length

Choose the chapter count and architecture that best deliver the behavior-specific belief change. Preserve the spine: trust and participation → dissolve loaded choice → switch the evaluation axis → demolish benefits → expose the inversion → close escape routes → widen the indictment where supported → meet the strongest scene → demystify → knowledge/readiness gate → chosen threshold → relapse-proof → ordinary life.

Map concept debuts, qualitative demolition and freedom curves, structural responsibilities that genuinely apply, instruction placements, the saved ending reframe, and one integer word budget per chapter.

For a HARNESS calibration plan, chapter budgets must sum exactly to 54,000–66,000 words. State the arithmetic sum. Length is planned, not hoped for.

### Compact chapter cards

Give every chapter a stable ID, number, and working title, then specify only its semantic work order:

- one belief job and the objection/justification it resolves;
- arc position and qualitative curve position;
- target persona IDs and the reader voice or scene that makes the move land;
- evidence-ledger IDs, including the limits the chapter must preserve;
- mantra IDs debuted and echoed;
- instruction ID, if any;
- one or more concrete scene/analogy IDs and the argumentative job each performs;
- structural responsibility, if any;
- method, safety, and originality guardrails specific to this move;
- continuity intent: what understanding it receives and hands forward;
- one integer word budget matching the arc table.

The writer derives `IN THIS CHAPTER`, the italic thesis, section flow, ALL-CAPS landing, SUMMARY, sentence rhythm, and analogy density from the style guide. Do not prewrite those prose elements in the plan.

## Normalization law

Do not create:

- exact mantra occurrence counts;
- a second mantra audit or cumulative state matrix;
- repeated full mantra, instruction, evidence, persona, or slot text in chapter cards;
- prewritten previews, theses, landings, or SUMMARY prose;
- a single-use phrase ledger;
- duplicated chapter-to-persona or chapter-to-slot matrices;
- generic style-guide rules copied into every card;
- a deterministic planning procedure, renderer, or validator.

A missing semantic requirement is a plan defect. A missing duplicate representation is not.

## Evidence and originality boundary

Use only the supplied syntheses. Preserve every evidence grade, outcome tier, source limit, and uncertainty. Never invent a source, quote, author experience, medical result, efficacy claim, mechanism, or authority conflict.

The plan may assign an evidence-unavailable treatment when a familiar structural move is unsupported. It must not create filler to make every generic slot appear.

## Fresh review gate

The plan is not final until a fresh reviewer from Gemini 3.1 Pro, GPT-5.6 Sol, or Grok 4.5 at its highest supported reasoning mode reviews the exact permitted inputs plus the candidate and records `master-plan-review.md` ending with the standalone line:

`fit to write from`

Resolve genuine blocking issues and re-dispatch a fresh reviewer, up to three cycles. Reviewer preferences about prose, ordering, or extra bookkeeping do not override a coherent model-owned architecture unless they expose method-integrity, evidence-honesty, blindness, missing-context, safety, length, or whole-book coherence failures.

## Output

Return only the complete master-plan document. It lives at `production-books/<slug>/master-plan.md`; the review lives at `production-books/<slug>/master-plan-review.md`. Version-control actions belong to the caller.
