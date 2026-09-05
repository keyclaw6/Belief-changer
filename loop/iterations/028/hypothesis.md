## Failure evidence

Census class: **`factory-speech`** (voice, noted) in both 027 books: A 13 / B 16. Blocking 0/0. ≥8 both. Comparison `missing` is no longer in both (1/0). No blocking in belief/journey/arc. `willpower-lexicon` 28/36 is larger but the quotes name/attack the Willpower Method — Carr's own register; the judge already marks those NOTED-as-attack. Do not make that PRIMARY.

027 factory-speech quotes (unassigned):
- A ch01: "**IN THIS CHAPTER** — The full cupboard behind you, the boxed line on the table, the dossier of escape"
- A ch03: "### 3. JUDGE ONLY BY WHAT IT DOES FOR YOU" (plan-index, no spoken body)
- A ch05: "This room we stage fully" / "This staging we do fully" / "This naming we do carefully"
- A ch08: "That seatbelt saying stays seed here. Full road belongs later." / "### 8. IGNORE ANY ADVICE…"
- B ch11: "**IN THIS CHAPTER**" / "12. TAKE YOUR LAST ORDINARY TREAT AND VOW FREEDOM"
- B ch12: "13. NEVER REOPEN THE DECISION" as a next-chapter plan token

026 already KEEP'd chatbot openers. This is a new mechanism: card-header / workshop-staging / seed-later leaks.

## Root cause

**PRIMARY — style-guide `prompts/style-guide.md` §B5 operator 11.** The instruction-voice rule already bans "Warm rationale" headers and craft labels, but it still licenses a numbered ALL-CAPS line. The model pastes the card's inventory header and the plan-index number as if that were the spoken instruction. Workshop staging ("this room we stage") and reserved-later placeholders ("stays seed here") are legal under the current sentence.

## Targeted fix

**Change 1 (PRIMARY) — `prompts/style-guide.md` — class `factory-speech` (voice) — component style-guide (§B5 operator 11 + §B9).**

Replace operator 11 with the same instruction-voice rule plus an explicit ban on card-header paste, workshop staging, seed/later placeholders, and numbered plan-index lines with no spoken body. Matching B9 bullet. No judge edit. No 020–024 wording.

**Why this component:** 027 traces name those leaks; 026's chatbot list did not cover them. The writer reads Part B.

## Predicted impact

**PRIMARY:** voice `factory-speech` falls in BOTH books versus 027 (A 13, B 16) by ≥2 at the same n. **Secondary:** `copied-mannerism` may fall if card-title paste was double-counted.

**Possible regressions:** stripping numbered headlines could thin the instruction spine (Carr uses ALL-CAPS commands). Spoken instruction + one rationale line must remain. Length floor must stay ≥48000. `willpower-lexicon` is not expected to move.

**How we'll know it worked:** `factory-speech` (noted + blocking) must fall by ≥2 in BOTH replicates versus 027. Grep for "IN THIS CHAPTER" is not KEEP.
