## Failure evidence

Census class `re-argument`, journey lane, accepted baseline 019: **A 7 / B 5** (present in both books; PRIMARY KEEP object in 020 and 021, both INCONCLUSIVE). Same class also present in both books at belief lane (019: 3/1) and book-arc lane (019: 3/2). 021's writer-only clause moved it A 7→6, B 5→7.

Trace analysis 021, PRIMARY cluster "Adjacent N←N−1 seam re-argument", spread systemic, **13/13 journey hits are N←N−1**:

- A ch08: CH-07 — *"The wrapper rustle from the next room. The bakery smell in the street. The clock striking nine…"* → CH-08 — *"Wrapper from the next room and mouth floods. Bakery smell in the street and feet turn. Clock strikes nine…"* — CH-08's card job is manufacture/fear, no cue-firing assignment.
- A ch02: CH-01 free-choice seed → CH-02 *"If sweet food is your free choice… why are you reading a book about how to stop?"* at fuller length.
- B ch12: CH-11 faint-echo / dying-loop block → CH-12 same transition at full section length.
- B ch13: CH-12 pity/envy and doubt passages re-run at near full length; `journey-stall` on the *"Go to breakfast hungry. Go to the shop with clear eyes…"* list.

Journey judge definition: *"re-argument — this chapter re-runs a prior transition at full length; assigned leaving-belief still lands."* The reader is made to sit through the previous chapter's transition again before the new work starts — the cumulative journey stalls at every seam.

Convergence budget: D ≥ 3 in the 019 baseline (`willpower-lexicon`, `factory-speech`, `re-argument`, `coach-register`, `wrong-register`, `copied-mannerism`, `pre-debut-spend` in both books). Up to three changes permitted; **one is proposed** — the census is all-PASS, zero blocking, noted-only, so the change is kept minimal and the plan is reused to keep the PRIMARY attributable.

## Root cause

Root component (trace analyzer): **writer-prompt**. Two quoted mechanisms:

1. **No licensed short form for untokened settled work.** Trace: *"Binding craft 3 (`prompts/chapter-writer.md` ~97) licenses only frozen-token echoes; most flagged transitions (cue-firing, deserve-it loop, dying-loop, free-choice block) have no pinned token, leaving no short licensed form when the closing line re-opens the seam."* Current craft 3 reads: *"Invoke settled prior work by speaking its frozen token as ordinary speech — never by chapter-number callbacks, 'as promised,' or ledger talk."* When the previous chapter's transition has no frozen token (most don't — the mantra sheet has ~9 tokens for 13 chapters of transitions), the only remaining way to "enter from" it is to rebuild it. The writer does exactly that.

2. **The assembled contract re-authorizes seam work with an undefined term.** Every runtime prompt ends with the runner's assignment (`scripts/loop-runner/write_replicate.py` lines 48–53, confirmed in `replicate-a/traces/chapter-08/prompt.md` line 155): *"Use the immediately previous chapter only for voice continuity and the handoff seam."* "Handoff seam" is never defined anywhere in the assembled prompt; the template's own input paragraph (line 13–14) and Procedure check list ("…recap, and handoff") use the same undefined term. The model, holding the full previous chapter as input, resolves "the handoff seam" as *rebuild the transition that bridges into my card job* — the N←N−1 pattern.

021 replaced the input paragraph's wording and dropped the phrase "handoff seam"; the runner's closing line reinstated the undefined phrase as the last task-specific instruction before the inputs, so the contract contradicted itself (trace: *"runtime prompt contradicts itself"*). The runner is **not on the editable surface** (`loop/PROGRAM.md` §1), so the fix must make the term the runner uses resolve to a bounded definition inside `prompts/chapter-writer.md`, not delete it. (Harness note for the founder, outside this hypothesis: the runner's assignment duplicates a template sentence; dedupe it in a non-loop commit so the template is the single voice.)

Secondary clusters (plan-card: CH-10/CH-11 tomorrow/postponement overlap, CH-12→CH-13 recap restaging, cross-gap CH-02→CH-04) are real and recorded, but they are not targeted this iteration: a plan-skill edit forces plan regeneration, which would change the card set the PRIMARY is measured against and make a both-books fall unattributable to the writer change. The proposed craft rule also gives the writer a lawful one-sentence path when a card re-owns settled work, so plan-scheduled overlaps should soften without a plan change.

## Targeted fix

**Change 1 (PRIMARY) — `prompts/chapter-writer.md` — class `re-argument` (journey lane) — component writer-prompt — Binding chapter craft rule 3.**

Replace, in full, the current rule 3:

> 3. Repeat assigned mantras verbatim; repeat no other striking prose verbatim. Previews, summaries, and assigned instruction recaps are licensed recap zones. Invoke settled prior work by speaking its frozen token as ordinary speech — never by chapter-number callbacks, "as promised," or ledger talk.

with:

> 3. Repeat assigned mantras verbatim; repeat no other striking prose verbatim. Previews, summaries, and assigned instruction recaps are licensed recap zones. Settled work is whatever the previous chapter, or any earlier card in the plan, already landed: its verdicts, scenes, warnings, questions, and transitions. Invoke settled work in one plain spoken sentence — its frozen token where one exists, otherwise the settled conclusion stated as fact — and that one sentence is the whole handoff seam. Never rebuild settled work at any length, whether as an opening recap, a bridge, a roll-call, or a fresh proof; never invoke it by chapter-number callbacks, "as promised," or ledger talk. When your card's job or encounter overlaps settled work, that is not a card defect — do not refuse; spend the chapter on what remains after that one sentence.

No other file changes. No duplicates to normalize (the input paragraph's "voice continuity and the handoff seam" at line 13–14 and the Procedure "handoff" check now point at this definition and stay as they are). Research reused. **Plan reused (019, 13 chapters).** Two books, judges composer-2.5, compared to the 019 baseline.

This is not a replay of 021: 021 rewrote the input-description paragraph (which the runner's closing line then contradicted) and left the writer with no licensed form for untokened settled work. 022 changes a different instruction (Binding craft 3), supplies the missing one-sentence licensed form, binds the runner's "handoff seam" term by definition so the assembled contract is single-voiced without editing the runner, and extends closure to earlier cards so a card that re-owns settled work is handled lawfully instead of being re-demolished. It is also not 020's plan-skill continuity bullet (no plan change).

**Why this component:** 13/13 journey hits are N←N−1 seam rebuilds, and the trace shows the writer contract offers no short licensed form for untokened settled work while the non-editable runner line re-authorizes "handoff seam" work — defining the seam inside the craft rule closes both mechanisms in the only editable file that reaches the assembled prompt.

## Predicted impact

**PRIMARY:** journey-lane `re-argument` falls in **BOTH** replicates vs 019 (A 7 → <7, B 5 → <5), blocking + noted counted together. Expected mechanism-specific closes: seam hits at ch02 (free-choice), ch08 (cue-firing), ch09/ch10 (mid-arc seams), ch12 (dying-loop). Plan-scheduled overlaps at ch11 (tomorrow/postponement) and ch13 (CH-12 ordinary-life restaging) may persist at reduced length; they are recorded for a plan-card hypothesis in 023 if this KEEPs.

**Secondary (recorded, not decisive):** belief-lane `re-argument` (019: 3/1) and book-arc `re-argument` (019: 3/2) predicted to fall or hold; neither may rise in both books. `journey-stall` (019: A 1, B 0) predicted to hold.

**What might regress:**
- `journey-stall` or under-budget chapters if the writer over-compresses and enters with nothing but the one sentence, leaving thin openings.
- `factory-speech` (voice, noted) could rise if "the settled conclusion stated as fact" is rendered as ledger-flavoured declaratives ("We have already settled…"); the rule's own ban on ledger talk and the existing never-surface list on assignment-fulfillment narration are the guard.
- Belief-lane job classes (e.g. `credit-intact`) could appear if the writer reads a card overlap as license to skip the card's assigned move rather than do "what remains"; the rule names the remaining work as the chapter's job and forbids refusal, so `ROUTE REFUSAL` runs should not increase.
- Blocking must stay 0/0 in all lanes; any new blocking class present in both books is a veto.

**How we'll know it worked:** journey-lane `re-argument` count must fall in BOTH replicates vs 019 (A < 7 and B < 5), with all lanes still PASS and no new both-books blocking class. One-book movement, owning-lane PASS, or a grep-only reduction in "handoff" wording is not KEEP.
