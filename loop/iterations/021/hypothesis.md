## Failure evidence

Census class: **`re-argument`**, journey lane — present in both books of the accepted baseline (019: A **7** / B **5**; merged 12), plus the same class in book-arc (3/2) and belief (3/1). All lanes PASS, blocking 0/0; it is the highest-priority noted class present in both books (journey/arc lanes above voice). 020's plan-card attempt left it at 4/5 — one book only.

What the judges actually flagged, across both plans and all four books, is one shape: **chapter N re-runs chapter N−1 at (near) full length.**

019 A (7): ch02 re-expands CH-01 — *"if you freely choose this and enjoy it, why are you holding a book about getting free from it?"*; ch08 re-runs Chapter 7's Sweet Con *"at nearly full length"*; ch11 (×2) rebuilds CH-10 — *"If tomorrow were safer, why has every yesterday…"* / *"If one were nothing, why… did one never stay one?"*; ch12 *"re-teaches the Ch. 11 freedom response at nearly full length"*; ch13 (×2) *"shop-and-pity beat from Chapter 12 is re-run at length"* / *"'BRILLIANT! I'M FREE!' echo protocol from Chapter 12 is re-run verbatim in structure."*
019 B (5): ch02 re-opens Chapter 1's cupboard fraud *"at full length"*; ch08 *"substantially repeat[s] Chapter 7's already-settled blocks"*; ch11 ← CH-10; ch12 *"re-runs CH-11's settled deliberate-vs-accidental distinction at full length"*; ch13 GO AND LIVE *"re-runs Ch. 12 transitions at nearly full length."*
020 A (4): ch04 *"re-runs the C03 pleasure/treat/lift dismantling at length"*; ch09 *"Brief re-run of C08's body-echo reassurance"*; ch10 *"'NO OCCASION HOLDS IT' re-runs the no-occasional-benefit argument already closed in the previous chapter"*; ch13 trap re-proof.
020 B (5): ch05 *"Let us do what we did with the afternoon: run the whole film"* (← C04); ch07 *"C06 already ran the edgy-rattle-is-not-hunger transition… Ch. 7 re-runs it at full length"*; ch08 *"re-consolidates C07"*; ch09 C08 rhythm callback; ch10 *"compressed re-run of prior demolition tokens (energy, reward, hunger, willpower, leftovers)… closed in C09."*

20 of 21 journey hits are N←N−1. Reader effect: every chapter opens by sitting the reader back down for the argument they finished one chapter ago; the book reads as thirteen restarts rather than one cumulative climb.

## Root cause

The 020 trace analyzer names **plan-card** and says *"Late-arc re-proof of settled jobs still appears in both books… B regenerated the same 5 noted hits on the same plan."* The judge reports contradict that location: 020 B ch11 *"re-argument 0 — Prior demolitions appear as one-sentence tokens only"*, ch12 **0**, ch13 **0**. The late-arc cluster the card field targeted **did close in B**; B's five hits moved to ch05/07/08/09/10, each re-running the chapter immediately before it. Two different plans (019, 020) produced the same N←N−1 shape at different positions — so the cause is not any card or card field; it is the component that is constant across both plans and all four books: the writer's **previous-chapter input** and the one sentence governing it.

`prompts/chapter-writer.md`, opening contract: *"The immediately previous chapter exists only for voice continuity and the handoff seam."* This is the sole instruction about the one input that contains actual argued prose. It names a permitted use ("handoff seam") that the model reads as *re-join the previous argument*, and forbids nothing. Binding craft 3 covers only tokenized work (*"Invoke settled prior work by speaking its frozen token"*); most of N−1's transitions (rattle-is-not-hunger, run-the-whole-film, the animal-binge block, the Sweet Con) carry no frozen token, so the writer has no licensed short form and rebuilds them. Binding craft 8 (*"Do not retest or re-explain its conclusion"*) is intra-chapter only. The journey judge receives exactly chapter N and N−1 (`reader-journey.md` input 4), so the measured class is precisely this seam.

Plan-level rules for this already exist and passed review in both iterations (plan-skill: *"Adjacent cards must use distinct encounters and build cumulatively"*; reviewer: *"Block adjacent cards that… re-argue settled work"*). The remaining gap is downstream, at the writer.

## Targeted fix

**Change 1 (PRIMARY) — `prompts/chapter-writer.md` — class `re-argument` (journey lane, decisive; belief and book-arc `re-argument` recorded) — component writer-prompt (opening contract, previous-chapter clause).**

Replace the sentence

> `The immediately previous chapter exists only for voice continuity and the handoff seam.`

with

> `The immediately previous chapter is supplied for two uses only: match its voice, and enter from the belief it left installed. Everything it argued, staged, asked, warned, or landed is closed for this chapter — do not re-run, re-prove, re-warn, restage, or roll-call any of it at any length, whether as an opening recap, a bridge, or a "we have seen" list. Enter in at most one plain spoken sentence (a frozen token where one exists), then advance.`

No other line changes. Binding craft 3 and 8 are not exact duplicates and stay as they are. No plan regeneration is required by this change (writer-only); the orchestrator applies PROGRAM's plan-reuse rule.

**Retry disclosure:** not a retry. The previous-chapter clause has never been a target. Prior moves on this class were plan-skill (002–004 on the retired instrument; 015 batch and 020 continuity field on the composer-2.5 census instrument). Prior writer-prompt moves (005, 010, 018) targeted craft silence and trap-question prefixes, not this input. Same class as 020, new component and new mechanism, same instrument (composer-2.5 census judges).

**Why this component:** across two plans and four books, 20/21 journey hits are chapter N re-running N−1, and the writer's previous-chapter input — governed by one unbounded sentence — is the only component held constant through both plans, whereas the plan-card field bound in 020 closed the late cards in B and the class simply reappeared wherever two cards were adjacent.

## Predicted impact

**PRIMARY:** journey-lane `re-argument` (blocking + noted) falls in **BOTH** books versus the accepted 019 baseline (A 7 → below 7, B 5 → below 5), with the fall spread across whichever adjacent seams the regenerated-or-reused plan produces, not concentrated in CH-11–13. Reader effect: chapters open one sentence past the last verdict and climb, so the book reads as one cumulative argument. **Secondary, recorded not decisive:** belief `re-argument` (3/1) and book-arc `re-argument` (3/2) fall in both where their instances were N−1 re-runs (019: CH-10→11, CH-12→13); `journey-stall` (A-only noise) is expected to stay at or below 1.

**What might regress:** (a) `continuity-break` (journey, blocking) could appear if the writer over-applies and opens without entering from the installed belief — the "at most one plain spoken sentence" clause is there to hold the seam; (b) chapters lose the padding the re-run supplied and may underfill budgets or fill with unassigned material (`journey-stall`, second thesis); (c) the one-sentence entry could itself harden into a settled-list mannerism (*"All that was argued is settled…"*, 020 B ch11/ch12) and register as `wrong-register`/`factory-speech` noted — the roll-call ban is meant to pre-empt this. `willpower-lexicon` is a design floor and is not expected to move. Measurement note for the founder, not a hypothesis: in 020 several noted `factory-speech` hits are the card-assigned numbered instruction line (e.g. *"4. JUDGE BY WHAT IT DOES FOR YOU"*) flagged because the judge CHAPTER CONTEXT showed `Instruction: I-04: (unresolved)`; that is a judge-harness card-resolution artifact inflating the voice floor, and it is why `factory-speech` is not a secondary here.

**How we'll know it worked:** the PRIMARY class count — journey-lane `re-argument`, blocking + noted — must fall in BOTH replicates versus 019 (A 7, B 5), with no new blocking class appearing in both books. Lane PASS, voice score, or grep-only absence of "we have seen" openings is not evidence of KEEP.
