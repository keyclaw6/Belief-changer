## Failure evidence

Census class: **voice `factory-speech`**, 031 A 14 / B 10 (noted, ≥8 in both). Blocking 0/0. Highest-priority KEEP-eligible class.

The 24 counts sort into buckets. Only the workshop-anatomy frame is present ≥2 in both: `IN THIS CHAPTER` header (A 2 / B 2 judged; grep 12/13 both after rewrite) and bare list-number instruction lines (`6. TRUST…`, `11. NEVER KEEP…`, `12. TAKE YOUR LAST…`). Reviewer fired HEADER on 26/26 drafts; 24/26 rewrites kept the header because the writer contract still requires it.

## Root cause

**PRIMARY — `prompts/chapter-writer.md` Full-length chapter anatomy item 2.** "Use every element in this order" plus `IN THIS CHAPTER` is a stronger mandate than the 030 reviewer HEADER finding. 028/029 changed the style guide and both books still emitted the header. Item 5's "numbered ALL-CAPS spoken imperative" is rendered as a bare markdown list number, which the judge reads as plan-index. Style-guide + factory-speech strike 2; reviewer HEADER is accepted KEEP — do not replay either. Writer anatomy has never been the object of a change.

## Targeted fix

**Change 1 (PRIMARY) — `prompts/chapter-writer.md` — voice `factory-speech` — Full-length chapter anatomy item 2 plus Method-and-voice duplicate.** Delete the required `IN THIS CHAPTER` element. Thesis line becomes item 2 and forbids the header and room-list anywhere in the chapter (supersedes style-guide B10 item 1). Normalize Method and voice: drop "or IN THIS CHAPTER" from the you/we address line.

**Change 2 — `prompts/chapter-writer.md` — voice `factory-speech` — anatomy instruction item.** Replace bare list-number ALL-CAPS with a spoken lead-in that carries the number in words, then the verbatim ALL-CAPS line. Numbered list allowed only on the final recap chapter.

No reviewer, style-guide, or plan edit.

**Why this component:** the writer contract is the only remaining mandate for the header; 24/26 rewrites obeyed it over HEADER.

## Predicted impact

**PRIMARY:** voice `factory-speech` falls in BOTH books versus 031 (A 14, B 10) by ≥2 at n=13 (target A ≤12, B ≤8). Header and bare list-number cannot occur.

**Possible regressions:** style-guide §B10 still names `IN THIS CHAPTER`; if Spark weights the style guide over the contract the header persists (REVERT). Length change is negligible vs 48000.

**How we'll know it worked:** factory-speech (noted + blocking) must fall by ≥2 in BOTH replicates versus 031. Grep for `IN THIS CHAPTER` going to 0 is mechanism, not KEEP.
