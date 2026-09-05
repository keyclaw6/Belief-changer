## Failure evidence

Cluster: voice `factory-speech`, noted, 20 (quit-sugar, n=13) / 18 (quit-smoking, n=14). Blocking 0/0 in every lane; this is the only KEEP-eligible class in the ≥8-both intersection other than the founder-locked `willpower-lexicon` (40/31) and the secondary journey `re-argument` (16/8).

The judge's own sub-labelling splits the class into two mechanisms. The one that is fresh (never targeted) and present in both books is the **ease-operator** leak — the style guide's freedom-register vocabulary spoken as sentence-tags and refrains in the freedom-crescendo chapters:

- Sugar CH-12, `factory-speech ×8`, every one labelled "ease-operator in unassigned … passage": *"Get on with enjoying your life inside it."* / *"Let your shoulders drop. Think your joyful thought and walk on with ease."* / *"Colour belongs to you — noticed, savoured, left at enough, remembered with ease."* / *"Let yourself get on with enjoying your life."* / *"Think it and move on with ease."* / *"Belief guarded, behaviour follows with ease."* / *"Let visible ease do the recruiting."* / *"Then get on with enjoying your life beside them."* Judge's effect statement: "repeated ease-operators … make the reader feel slightly more coached-by-template than Carr's chatty, settled confidence after freedom is won."
- Sugar CH-11 (×2 of 3): *"think it and move on with ease."* / *"Mornings, shops, meals with ease."* Sugar CH-13 (×2): *"That is ease doing its own work."* / *"That joyful thought guards the belief and the behaviour follows with ease."*
- Smoking CH-11, `factory-speech ×3`: *"Note what happened, rejoice that you see it…"* / *"Think how exciting to be done with arithmetic. Think how marvellous to want nothing you have to count."* / *"Think how exciting to stop paying rent on rooms you own. … Rejoice that the door opens now…"* — judge: "Three unassigned ease-operators are noted factory-speech."
- Smoking CH-12, `factory-speech ×3`, "unassigned ease-operator leaks": *"Think how exciting to breathe easy without permission."* / *"You breathe easy through it."* / *"Breathe easy beside them."*

Spread: 12 of sugar's 20 and 6 of smoking's 18 are ease-operators, all in the final quarter (sugar CH-10–13, smoking CH-11–14). Token counts in the accepted chapters confirm the refrain: sugar "with ease" 0 in CH-01–09, then 2/2/6/2 in CH-10–13; smoking "rejoice" 3/4/4/5 and "breathe easy" 1/3/4/5 in CH-11–14; *"Let visible ease do the recruiting."* appears verbatim in both books' CH-12.

The remainder of the class is the burned header/tail mechanism (smoking `**IN THIS CHAPTER**` / `**SUMMARY**` ×8; sugar ×5 incl. numbered instructions) plus four one-offs (sugar "belief change only", "killer questions", neurochem sentence; smoking "Here is the turn this whole chapter stands on", "investigator to investigator" ×2, "counter-voice"). Those are not targeted here.

## Root cause

The trace analyzer names "writer + style-guide ease/anatomy (not another HEADER sentence; not 032 anatomy)". The evidence points at one style-guide instruction and the curve rule that amplifies it:

1. `prompts/style-guide.md` §B4, the Freedom-register bullet, hands the writer a bare token list with an "always" and one stock imperative:

> - **Freedom register** (for stopping and the stopped state, always): escape, free, freedom, marvellous, wonderful, exciting, rejoice, celebrate, relief, "get on with enjoying your life."

   Both plan lexicon sheets are verbatim copies of this list (sugar plan l.319; smoking plan l.274 adds "clean air, breathe easy"), and the sugar plan's destination line paraphrases §8/§B6/§B10's planner-facing room list "mornings, shops, food" into "inhabiting mornings, shops and meals with ease" — which the writer then pasted as the CH-11/12/13 refrain *"Mornings, shops, meals with ease."*

2. §B3 ("the last 20% of the book should contain more freedom-language than the rest combined") and §B7.3 ("a final-quarter chapter does [bathe in freedom language]") tell the writer to saturate late chapters with that register. Spark 1.3 satisfies "more freedom-language" by density of list words — "with ease" tails, "Think how exciting/marvellous/wonderful to…", "Rejoice that…" openers — rather than by pictured moments and the frozen terminal mantra. The previous-chapter input then propagates the refrain (CH-11 coins it, CH-12 and CH-13 repeat it).

3. Part A toolkit sentences written for the planner are speakable and get spoken: §5.10 "Let visible ease do the recruiting." (verbatim in both CH-12s), §6 "Think how proud you'll feel." / "You can get *excited* about this." (→ "Think how exciting to…"), §8 CLOSE "get on with enjoying your life" (used as a mid-chapter tag in sugar CH-11/12/13 and smoking CH-12/13/14, not as the single final imperative).

The judge's `factory-speech` definition lists "ease-operator" explicitly alongside P-xx and killer-line (`loop/judges/voice-emotion.md` l.85–89), so these are scored as the factory's freedom-register device surfacing, not as Carr voice. Since 025 the ledger has named "ease-operators" as the residual factory-speech floor (025: "ease-operators and card leaks, not chatbot openers"; 033: "factory-speech survives HEADER/A1 as ease-operators"). No iteration has ever edited §B4; 026/028/029 edited §B5/§B10 and left the vocabulary source untouched.

## Targeted fix

**Change 1 (PRIMARY)** — `prompts/style-guide.md` — class `factory-speech` (voice, noted) — component: §B4 lexicon sheet, Freedom-register bullet — targets both subjects (sugar CH-10–13 "with ease" / "get on with enjoying your life" refrains; smoking CH-11–14 "Think how…" / "Rejoice that…" / "breathe easy" tags; "Let visible ease do the recruiting" in both).

Replace this exact bullet (§B4, currently line 509):

> - **Freedom register** (for stopping and the stopped state, always): escape, free, freedom, marvellous, wonderful, exciting, rejoice, celebrate, relief, "get on with enjoying your life."

with:

> - **Freedom register** (for stopping and the stopped state): freedom is shown as a moment the reader lives — the clear morning, the quiet aisle, the meal closed, the breath taken at the kerb — and is *named* only by the mantra sheet's frozen lines. Ease, joy and relief are what the picture makes the reader feel, not words to distribute across the page. The freedom crescendo is built from more such moments and more mantra echoes, never from denser register words. Never write the register as a tag or refrain: no sentence-tail "with ease", no "Think how exciting / marvellous / wonderful to…", no "Rejoice that…" as a sentence opener, no "let visible ease do the recruiting", and no "get on with enjoying your life" anywhere except the book's single final outward imperative. A freedom-register word may appear at most once per titled section, inside a concrete sentence, and never in two consecutive sentences. Card fields that describe the reader's ease ("lived with ease", "Freedom high", "mornings, shops, food") are planner shorthand — live the scene; never paste the phrase.

No other file is edited. The §B3 crescendo sentence and §B7.3 stay as written; the replacement bullet is the more specific Part B rule and governs how the crescendo is executed. No writer, reviewer, plan-skill or plan change. No model, fallback or route change.

**Why this component:** The leaked strings are the §B4 list and its Part A cousins spoken verbatim, both plans copied that list, and §B4 is the one writer-read instruction that says "always" use these words — it is the source of the tokens, not a downstream symptom; the writer's anatomy (032) and the reviewer HEADER (030) are burned and never touched the vocabulary.

Not a retry of any reverted change: §B4 has never been edited (007 touched §9/toolkit; 011 §B5/§B7/§B9; 020 §B5 op 1; 026 §B5 op 12; 028 §B5 op 11; 029 §B10 item 1). Scored under the 033 dual-subject A1+K1 instrument, composer-2.5 panel, against the 033 BASELINE floors.

## Predicted impact

PRIMARY: voice `factory-speech` falls in BOTH subjects, beyond the rate-normalized noted band, against 033 floors 20 (sugar, n=13) / 18 (smoking, n=14). Expected: sugar 20 → ≤12 (the 12 ease-operator counts in CH-11–13 are the removed object; the 8 header/one-off counts stay), smoking 18 → ≤14 (the 6 ease-operator counts in CH-11–12 are the removed object; the 8 `IN THIS CHAPTER`/`SUMMARY` and 4 meta counts stay). Reader-effect claim: the CH-12 judge's "coached-by-template" gap closes — late chapters read as Carr's settled post-freedom confidence (scene, then frozen mantra) instead of a distributed ease refrain.

Secondary (recorded, not decisive): `copied-mannerism` (4/1) — sugar CH-12's two counts are the same refrain block, predicted to fall in sugar; `coach-register` (2/4) — the "Think how exciting to…" imperatives read as coaching, predicted to fall in smoking. Journey `re-argument` 16/8 is untouched by this change and is scored as non-regression only.

What might regress: book-arc `curve-flatten` (0/1) could rise if the writer, denied the register words, under-delivers the freedom crescendo instead of building it from moments and mantra echoes; comparison `partial` in late chapters (2/9) could rise if the comparison judge reads freedom parity through token density. `willpower-lexicon` (40/31) is not touched and should not move. The header/`SUMMARY` remainder cannot fall from this change; if factory-speech stays ≥8 in both after KEEP, the next PRIMARY is that residual and must use a mechanism other than 028–032.

How we'll know it worked: the noted `factory-speech` count must fall in BOTH replicates (sugar and smoking) by a material, rate-normalized margin against 20/18, with blocking still 0/0 in all lanes, word floors ≥48,000 met, and no new both-books class ≥8. A grep of "with ease" / "Think how" going to zero without the census falling is not KEEP. A fall in one book only is REVERT.
