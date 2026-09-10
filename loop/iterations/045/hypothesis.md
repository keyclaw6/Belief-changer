## Failure evidence

Lane `carr-distance`, both subjects — KEEP-eligible PRIMARY intersection (deficit 32/30; also missing 8/1, partial 9/6 in both; blocking 0 both).

Census 044: quit-sugar `score-deficit` 32 (score 68); quit-smoking `score-deficit` 30 (score 70). Words 62791/54953, floors met.

Trace-analysis 044, both-subjects signal:
- Mandated inventory: §B10 mandates IN THIS CHAPTER + SUMMARY + twice-per-chapter reframes; writer anatomy executes; reviewer seals them; voice counts 0 while Carr-distance penalizes. Cards never assign them — they survive every regen in both subjects. First NEW-level deficit diagnosis in three iterations.
- Hedge / limit transplant: routing every prong's limits onto cards made the writer narrate limits as clinician-grade caveats ("laboratories report mild, though well-defined"; "bodies differ, no timetable") — deficit up both.
- Catalogue at peaks/openings unfired; thin second prong persists.

## Root cause

PRIMARY root: `prompts/style-guide.md` §B10 recap-license line — orders in every chapter what Carr-distance penalizes as inventory. Trace names it the only shared floor outside plan-card.

Secondary root: hedge-transplant licenses at writer + style-guide (§B10 Hard-facts slot). After the 044 restore to 041 text both licenses are live again. 042 verified deleting them removes Reason 3 both (grep 12/13→1/13, 9/14→0/15).

## Targeted fix

**Change 1 (PRIMARY)** — `prompts/style-guide.md` — class `carr-distance` `score-deficit` — component: §B10 twice-per-chapter recap license — both subjects. Replace:

> The reader meets every reframe at least twice per chapter (argued + recapped). **Previews and summaries are licensed recap zones — exempt from the no-verbatim-repetition rule, exactly like mantras.**

with:

> The reader meets the reframe in the argument and once in SUMMARY. IN THIS CHAPTER stays: one line naming only this chapter's rooms/pictures. SUMMARY stays: at most three bullets, each one ordinary sentence stating the belief that changed with the belief verb in the sentence — never a token roll-call, instruction recap, preview list, or study-design note. No preview list beyond the one IN THIS CHAPTER line; summaries are not exempt inventory zones.

**Change 2** — `prompts/chapter-writer.md` — class `carr-distance` `score-deficit` — component: Method and voice, evidence-honesty bullet — both subjects. Replace the 041-text bullet (license + front-matter note + no-paste + never-disclaimer) with:

> Honour those limits by not overclaiming and by saying nothing about them. Never narrate study design, grades, or methods — in the body or in SUMMARY. When a hard fact would otherwise read as a sentence on this reader, the only spoken relief is Carr's: tell the reader not to change from fear, and that the method takes care of it. A safety limit or the plan-wide advisory on your card is held silently — never spoken as a clinician referral, "speak to your doctor," "I give no medical orders," "I am not your clinician," "this is not a diet," "I prescribe nothing," or any sentence about what this book does not advise. The clinician referral appears in the book exactly once, as the front-matter advisory, plus one plain sentence at the vow only when that card assigns it. Never paste CA-SAFE / CA-01 / PRACTICAL SAFETY GUARDRAIL titles mid-chapter and never add "this notice is not part of the belief argument."

**Change 3** — `prompts/style-guide.md` — class `carr-distance` `score-deficit` — component: §B10 structural slot Hard facts, then relief — both subjects. Replace:

> One short spoken clause only if the scare would otherwise be taken as a personal sentence.

with:

> The only spoken relief is Carr's own: tell the reader not to change from fear. Never a clinician referral or a sentence about what this book does not advise.

**Why this component:** the trace names the §B10 recap license as the only both-subjects deficit floor that survives every regen unassigned by cards.

Retry status: Changes 2–3 are the verified 042 clinician ban as a carried line — RESTORE is not a ban, not a replay; verified under this panel. No 039/040, 020–024, 028–032 wording reused. No card-field / plan-skill / plan-reviewer edit; no route-every-limit; no model/route change. Pre-spend GSBS control: Change 1 keeps IN THIS CHAPTER and SUMMARY in Carr's rooms/pictures + ordinary-sentence form (GSBS ch2 prints both) — control does not fire; GSBS ch17 GP line permitted by front-matter-plus-vow placement — control does not fire.

## Predicted impact

PRIMARY: `carr-distance` `score-deficit` falls in BOTH subjects vs 044 (sugar 32→≤24, smoking 30→≤22, ≥25% and ≥4 band). Secondary: comparison missing 8/1 and partial 9/6 flat-to-noise.

What might regress: capping previews/summaries could thin recap for long-arc readers — IN THIS CHAPTER plus SUMMARY plus mantra echoes still carry repetition; silencing limits could push narrow facts toward overclaim — reviewer OVERCLAIM still governs.

How we'll know it worked: PRIMARY deficit must fall in BOTH replicates, with neither report quoting an IN THIS CHAPTER itinerary / token roll-call / preview inventory or a spoken clinician/limit caveat outside front matter or vow.

```
parent: ae1afba5
instrument: 2026-09-06 Carr-distance panel
```
