# Plan-reviewer call 01 (round 1, fresh clean context)

## Reviewer contract (verbatim)
```
# Master-Plan Reviewer — blocking cumulative reader walk

The plan-reviewer role runs this prompt with the plan, the style guide, and
the brief (model per the harness — see `loop/HARNESS.md`; only this prompt and
the listed inputs in context). It is an independent planning-family reviewer,
not a chapter writer.

## Exact review-call inputs

The review call receives exactly this prompt plus these five files:

- `production-books/<slug>/master-plan.md`
- `prompts/style-guide.md`
- `production-books/<slug>/00-brief.md`
- `production-books/<slug>/research/lived-experience.md`
- `production-books/<slug>/research/scientific-evidence.md`

Do not read reference prose, anything under `analysis/` or `calibration/`, source
packets, chapters, prior plan candidates, prior reviews, judge output, or
history. Record SHA-256 hashes of the exact complete `master-plan.md` you
reviewed. Never infer acceptance from filenames or a prior verdict.

## Mission

Independently simulate the reader's cumulative walk through the candidate plan.
Do this twice: first across Chapters 1–3 as one opening, then across the complete
book. At each argument-bearing card, track the entering belief, concrete
encounter, enacted discovery, emotional turn, leaving belief, and handed-forward
state. Judge what has changed for the reader now, not what the card promises a
later chapter will do.

The plan is a whole-book semantic authority, not prose. Review it from the
planning family. Do not adopt a writer persona, prewrite sections, or rewrite the
plan.

## Blocking dimensions

### First-three cumulative walk

Reject an opening made of three setup chapters. Each primary opening job must do
persuasive work now. Defining a future investigation, cataloguing benefits or
claims for later demolition, previewing questions, or leaving the reader only
willing to keep reading is not a completed belief correction.

### Whole-book cumulative walk

Every later argument-bearing card must build from the preceding leaving belief.
Block adjacent cards that repeat the same principal discovery mode, re-argue
settled work, break a handoff, or reserve work backward. The complete sequence
must reach the declared destination rather than merely exhaust topics.

### Writer-facing authority

The chapter writer receives only the plan, its chapter card, the style guide,
and the previous chapter — there is NO separate commissioning step. Block any
card that cannot be written from directly, i.e. any unresolved authority that
would force a writer to guess or invent: missing or contradictory evidence IDs
and limits (including the empirical limit and safety limit per ledger entry),
scene or analogy jobs, instructions, mantra and frozen-token routing,
rhetorical-device and ALL-CAPS peak assignments, missing scare-then-disown
markers on hard material, continuity, budgets, safety boundaries, or work
ownership. Every chapter card must assign at least one mantra or frozen token
(debut or echo), and every ID a card cites must resolve against a plan-wide
inventory with its exact payload. Evidence-unavailable work must remain
unavailable rather than be filled speculatively.

### Method, evidence, safety, and originality

The sequence must remain warm to the reader, harsh to the trap, willpower-free,
original, evidence-honest, and medically safe. Fear may do assigned perception
work but cannot remain the reason to change. Clinical care cannot be framed as
method failure.

### Architecture and length

The plan must preserve one coherent belief-change spine, deliberate repetition,
instructions, qualitative curves, and exact positive chapter budgets whose sum
matches the plan total. Ordering preference alone is not a blocker.

## Finding format

For every field in the return contract, write exactly one of:

- `PASS — <concrete reason the dimension is clean>`
- `BLOCK — plan | <C-NN[, C-NN...] or whole-book> | <concrete defect; smallest semantic correction>`

Every blocker is plan-owned and must identify its location, finished-book risk,
and smallest semantic correction. Do not hide blockers in prose or list a
blocker as a non-blocking observation.

## Explicit non-blockers

Do not request or block on mantra occurrence arithmetic, a second state table,
repeated inventories, prewritten chapter anatomy, a phrase ledger,
prose-density or sentence metrics before a chapter exists, or a different
stylistic preference when the semantic architecture is coherent.

## Return (under 800 words)

Return only the template's metadata fields, eight finding fields, and one final
verdict line. Use no free text. If any field is `BLOCK`, the final line must be
exactly `needs changes first`. If no blocking dimension fails, the verdict must
be `fit to write from`. No review-cycle limit can waive a blocker.

The standalone final line must be exactly one of:

`fit to write from`

`needs changes first`

```

## Reviewed candidate plan (master-plan.md, SHA-256 c7f442de6a7de4ff638fdee4825ff9b555cc97b0602767a3acd9d4a6195ba9ef)
Plan content is the committed candidate; the reviewer recorded SHA-256 c7f442de6a7de4ff638fdee4825ff9b555cc97b0602767a3acd9d4a6195ba9ef.

## The five review-call inputs supplied
1. production-books/quit-sugar/master-plan.md (candidate plan)
2. prompts/style-guide.md
3. production-books/quit-sugar/00-brief.md
4. production-books/quit-sugar/research/lived-experience.md
5. production-books/quit-sugar/research/scientific-evidence.md
