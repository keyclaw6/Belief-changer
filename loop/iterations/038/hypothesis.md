## Failure evidence

**PRIMARY scope: quit-sugar, voice `factory-speech` — 10 noted occurrences.** Quit-smoking has 5 and is scored for non-regression only. The eligible intersection is empty: journey `re-argument` is below eight in both subjects, comparison `missing` is sugar 0 / smoking 2, and willpower-lexicon remains excluded by the accumulated learnings.

The 037 decision reports:

> “factory-speech 9→10 / 2→5.”

The supplied trace-analysis is empty, and no current passage-level judge findings are supplied. Consequently, the evidence establishes the class’s book-wide count, **not which chapters or surface forms account for those occurrences**.

Historical evidence identifies one recurring form worth testing: iteration 018 recorded:

> “blocking factory-speech 0→2 A-only (evidence-register at ch09 climax...)”

Iteration 014 likewise described residual factory-speech as:

> “evidence-limit register, frozen-echo paste, trap-question prefixes”

These are historical diagnoses, not quotations from current judges or claims that those exact passages survived 037. The hypothesized reader effect is an interruption of direct persuasion by narration of what the evidence permits the author to say.

## Root cause

**Candidate root component: `prompts/chapter-reviewer.md`, Output / `OVERCLAIM` finding.** With no fresh trace attribution, this is a bounded causal test rather than a confirmed localization.

The reviewer currently orders:

> “The writer must speak the bound; never print the ledger ID or grade in prose.”

That instruction converts every evidence correction into an obligation to verbalize the research boundary. It conflicts with the writer’s more selective evidence-honesty instruction:

> “Honour those limits by not overclaiming.”

and:

> “Add one short spoken clause only when a hard fact would otherwise be taken as a sentence on this reader.”

Thus an initially overbroad sentence can be repaired into evidence-report prose rather than into a narrower, truthful sentence. Suppressing IDs and grades does not remove that reader-facing scaffolding.

Learnings 001 and 018 show why label removal alone is insufficient. This proposal does not replay their bans, the 028–032 header mechanisms, or the successful 036–037 re-argument instructions: it changes **how the reviewer commissions an evidence repair**.

## Targeted fix

**Change 1 (PRIMARY) — `prompts/chapter-reviewer.md` — voice `factory-speech` — Output / `OVERCLAIM` repair instruction — targets quit-sugar primarily and quit-smoking for non-regression — replacement text.**

Replace the complete existing `OVERCLAIM` bullet:

```text
- `OVERCLAIM` — a claim exceeds the permitted-inference line of the evidence-ledger entry the card routes. Quote the overclaim and the bound. The writer must speak the bound; never print the ledger ID or grade in prose.
```

with:

```text
- `OVERCLAIM` — a claim exceeds the permitted-inference line of the evidence-ledger entry the card routes. Quote the overclaim and the bound in the review. Require the writer to delete the unsupported claim or narrow the sentence to what the evidence actually supports, rather than append commentary about the evidence, its scope, or what it can establish. The bound governs the repair; it is not text to transplant into the chapter. Retain any qualification needed for factual accuracy or reader safety, expressed directly in ordinary language; never remove a necessary limitation merely to sound certain, and never print the ledger ID or grade in prose.
```

Leave the finding name, ACCEPT gate, HEADER finding, RE-ARGUMENT finding, and LENGTHEN assignment unchanged. No other edits.

**Why this component:** The reviewer explicitly requires spoken boundaries where the writer already permits silent compliance, so correcting that repair instruction addresses a concrete contradiction without adding another general voice ban.

## Predicted impact

**PRIMARY prediction:** quit-sugar voice `factory-speech`, counting blocking plus noted occurrences, falls **10 → ≤8** at the same chapter count. Evidence repairs should leave the reader with a truthful observation or argument rather than a report about its evidentiary permissions.

Quit-smoking factory-speech is also predicted to fall **5 → ≤4**, but that improvement is recorded, not decisive; its formal non-regression ceiling is **≤6**, consistent with the prior scoped test’s one-count allowance.

**What might regress:** Evidence honesty could weaken if narrowing becomes deletion of necessary qualifications. The replacement explicitly preserves factual and safety limits; any newly unsupported claims must be tracked. Removing explanatory caveats could also reduce length, so both books must retain the **48,000-word floor**.

**How we’ll know it worked:** Under this declared scoped exception, KEEP requires a material PRIMARY reduction in sugar and non-regression in smoking—not a mandatory decrease in both. Fewer printed evidence labels, reviewer ACCEPT rates, or voice-lane PASS alone cannot establish success. If current factory-speech is unrelated to evidence repairs, this mechanism may have little effect; the missing passage-level traces make that a material uncertainty.
