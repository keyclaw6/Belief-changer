# Trace Analysis — Iteration 022

**Hypothesis tested:** Binding craft rule 3 rewrite in `prompts/chapter-writer.md` — define settled work, one-sentence handoff seam, ban rebuilds, lawful overlap handling.

**PRIMARY KEEP object:** journey-lane `re-argument` vs iter-019 baseline (A 7, B 5).

**022 result:** A 6, B 7 — merged **13** vs baseline **12**. **KEEP conjunction failed** (B rose 5→7; only A improved 7→6).

**Factory change verified in traces:** Craft 3 appears in every assembled `prompt.md` (e.g. `replicate-a/traces/chapter-11/prompt.md` lines 90–101). Runner closing line still reads *"Use the immediately previous chapter only for voice continuity and the handoff seam"* (`write_replicate.py` lines 48–53); craft 3 now defines that term.

---

| Causal cluster | Spread | Judge sources | Root component | Priority reason |
|----------------|--------|---------------|----------------|-----------------|
| Tomorrow/delay double-ownership (CH-10→CH-11) | systemic (late arc) | A journey-ch11, belief-ch11, book-arc; B journey-ch11, belief-ch11, book-arc (×2) | **plan-card** | Survives in both books at the PRIMARY seam; verbatim token echo across 10→11; craft-3 one-sentence openings present but full sections still rebuild |
| N←N−1 seam rebuild (card does not re-own prior transition) | systemic | B journey-ch06, ch07, ch08, ch09; A journey-ch09; belief/journey overlap on several | **model** | Adequate writer contract (craft 3 + one-sentence openers in traces); rebuilds occur inside new card jobs without plan assignment |
| Plan-mandated full restage (instruction/scene debut) | positional (early) | A journey-ch02 (×2: eat contract + peach); B journey-ch02 (childhood frame) | **plan-card** | Cards/plan schedule I-02, SC-02 full staging and CH-01 preview of same beats — rebuild is upstream-required before writer runs |
| Late-arc ordinary-life overlap (shop walk; sweet-thought) | positional (late) | A journey-ch12, ch13; B journey-ch13; belief A ch12–13, B ch12 | **plan-card** | CH-12 encounter list + CH-13 recap job restage CH-08/CH-12 settled scenes despite guardrail language |
| Cross-gap willpower-quitter re-argument | local (B only) | B book-arc, journey-ch09 (partial) | **plan-card** | Book-arc documents CH-04→CH-09 re-proof; not a both-books cluster — record only |
| `willpower-lexicon` noted floor | systemic (voice) | A voice 16 hits / 10 chapters; B voice 31 hits / 13 chapters | **style-guide** | Both books; B rose sharply (33→31 is slight drop, A 21→16 improved); attacks-on-wrong-method still counted |
| `factory-speech` / IN THIS CHAPTER leaks | systemic (voice) | A voice 6; B voice 11; multiple chapters | **plan-card** | Plan-card scene tokens and numbered instruction headlines paste into prose |
| `copied-mannerism` scaffold | systemic (voice) | A voice 3; B voice 7 | **model** | Repeated Carr-shaped tics (`There is only one honest answer`, champing) across chapters |
| Intra-chapter `journey-stall` | systemic/local mix | A journey-ch01, ch07, ch09; B journey-ch05, ch12 | **model** | Same beat shape repeated within chapter after consolidation |
| `pre-debut-spend` (SC-08 compression) | local (B only) | B book-arc | **plan-card** | CH-05 seeds rescuer line; CH-07 owns SC-08 full staging — B-only, not KEEP veto |

---

### Tomorrow/delay double-ownership (CH-10→CH-11)

**Judge sources:** A reader-journey-ch11 (`re-argument` 1); A belief-mechanic-ch11 (`re-argument` 1); A book-arc (`re-argument` 1); B reader-journey-ch11 (`re-argument` 1); B belief-mechanic-ch11 (`re-argument` 1); B book-arc (`re-argument` 2, includes tomorrow pair).

**Shared symptom:** Chapter 11 re-runs the full tomorrow/postponement demolition Chapter 10 already closed.

**Distinct effects:** Book-arc B also counts CH-04→CH-09 willpower-quitter rebuild as a second arc-level `re-argument` (separate cluster below). Belief judges frame it as re-proving a settled token; journey judges call it momentum drag before the vow.

**Root component:** plan-card

**Evidence:**
- **Upstream (plan):** CH-10 job includes *"tomorrow"* in its enacted transition (`plan.md` CH-10: *"inside BAD SUGAR there is no safe cut-down, special occasion, **tomorrow** or substitute"*). CH-11 job is *"waiting is the Trap"* with Belief-now *"enters lingering that **tomorrow is safer**"* (`chapter-card.md` CH-11). Both cards require the same demolition move.
- **Downstream (CH-10):** B ch10 — *"Delay is the dose. Waiting keeps the glow alive by making the next hit feel final, therefore intense, therefore memorable, therefore missed."*
- **Downstream (CH-11):** B ch11 — *"Delay is a dose. Waiting keeps the glow alive by making the next hit feel final, therefore intense, therefore memorable, therefore missed."* A ch11 opens with compliant one-liner (*"You have seen there is no safe sweet left to negotiate with."*) then full **TOMORROW IS THE TRAP** section anyway.

**Mechanism:** Plan schedules tomorrow/delay as CH-10's totality job and again as CH-11's entering belief and section title. Craft 3's overlap sentence (*"When your card's job or encounter overlaps settled work… spend the chapter on what remains after that one sentence"*) makes the card job lawful grounds to rebuild the entire settled transition after a one-line handoff. The writer executes what the card still owns.

---

### N←N−1 seam rebuild (card does not re-own prior transition)

**Judge sources:** B reader-journey-ch06 (`re-argument` 1 — dose lift/drop echo); B reader-journey-ch07 (`re-argument` 1 — ditch-and-hand); B reader-journey-ch08 (`re-argument` 1 — cue-firing); B reader-journey-ch09 (`re-argument` 1 — sofa/stress comfort); A reader-journey-ch09 (`re-argument` 1 — reward-table excuses).

**Shared symptom:** Prior chapter's transition reappears at partial or full length inside the new chapter's body, not as a one-sentence handoff.

**Distinct effects:** A ch08 journey `re-argument` 0 while B ch08 journey `re-argument` 1 on the same cue passage — sampling split on one seam. A ch09 also carries `journey-stall` 1 on tea/slow-boil after cinema consolidation.

**Root component:** model

**Evidence:**
- **Upstream (prompt):** Craft 3 in `chapter-11/prompt.md` (and all chapters): *"Invoke settled work in one plain spoken sentence… and that one sentence is the whole handoff seam. **Never rebuild settled work at any length**…"*
- **Downstream openings often comply:** B ch08 line 8 — *"You have seen the evening twitch is the Nibbler starving while the Sweet Con does the shouting."* B ch06 line 8 — *"You have seen the afternoon lift was never fuel…"*
- **Downstream rebuild without card assignment:** B ch08 lines 52–56 embed CH-07 cue work: *"why does the wrapper rustle fire the mouth before the bite, and the bakery smell on cold air turn your feet, and eight o'clock on the sofa call louder than hunger…"* CH-08 card job is manufacture/identity/fear, not cue-firing (CH-07 owns cues). B ch07 lines 36–36 re-prove spike/drop/rescuer cycle CH-05/06 already inverted — not CH-07 card's primary Nibbler/Sweet Con split debut.

**Mechanism:** Inputs are adequate and consistent: one-sentence seam is defined, previous chapter is supplied, and cards do not assign these rebuilds. The model honors the opening handoff line then re-derives the prior transition at length inside the new argumentative section — classic N←N−1 pattern. Craft 3 did not eliminate this class; B's count rose.

---

### Plan-mandated full restage (instruction/scene debut)

**Judge sources:** A reader-journey-ch02 (`re-argument` 2 — eat-while-reading + peach-child); B reader-journey-ch02 (`re-argument` 1 — childhood brainwashing frame).

**Shared symptom:** Early-chapter material from CH-01 reappears at full length in CH-02.

**Distinct effects:** A flags two separate rebuilds (I-02 eat contract + SC-02 peach); B flags one (childhood conditioning paragraph). Belief lane: `re-argument` 0 on both ch02 belief reports.

**Root component:** plan-card

**Evidence:**
- **Upstream (plan):** CH-02 card assigns **New-instruction I-02** (*"DON'T STOP OR CUT DOWN UNTIL YOU FINISH / Carry on exactly as normal while you read"*) and **SC-02 debut full staging** (*"small child eats peach hungrily, stops mid-bite"*). CH-01 already delivered eat contract (lines 94, 132) and peach preview (line 132).
- **Downstream:** A ch02 — *"Do not change what you eat because of what you have just seen…"* vs CH-01 *"Do not stop. Do not cut down… Carry on eating exactly as normal while you read."* Peach restaged lines 97–99 vs CH-01 line 132.

**Mechanism:** The plan requires CH-02 to own instruction debut and scene debut that CH-01 already previewed. The writer is instructed to execute the card, not to compress CH-01's settled work. This is plan-scheduled overlap, not a seam-handoff failure.

---

### Late-arc ordinary-life overlap (shop walk; sweet-thought)

**Judge sources:** A reader-journey-ch12 (`re-argument` 1); A reader-journey-ch13 (`re-argument` 1); B reader-journey-ch13 (`re-argument` 1); A belief-mechanic-ch12, ch13 (`re-argument` 1 each); B belief-mechanic-ch12 (`re-argument` 1).

**Shared symptom:** Post-vow chapters restage settled ordinary-life transitions at recognizable length instead of peaking the close.

**Distinct effects:** A ch12 shop paragraph echoes CH-08 aisle beat; ch13 sweet-thought block mirrors ch12 section title **WHEN A SWEET THOUGHT DRIFTS BY**. B ch13 echoes ch12 peach/market catalogue per journey judge.

**Root component:** plan-card

**Evidence:**
- **Upstream (plan):** CH-12 card Encounter lists *"breakfast, aisle, checkout, evening sofa lived with ease"*; CH-13 job is *"recap — photographable instruction list, outward push"*. CH-12 guardrail says *"no settled-scene restaging"* but still assigns shop/aisle encounter after CH-08 aisle debut.
- **Downstream:** A ch12 line 47 — *"We all know that walk. We went in for milk and came out with a bright packet we had sworn not to touch…"* (parallel to CH-08 aisle). A ch13 line 52 — sweet-thought maintenance block quoted in journey-ch13 judgment, beat-for-beat with ch12 § **WHEN A SWEET THOUGHT DRIFTS BY**.

**Mechanism:** Late-arc cards schedule lived vignettes and closing maintenance that overlap scenes/transitions already landed. CH-13 card says *"no token-echo needed"* yet the writer rebuilds ch12's sweet-thought curriculum — overlap is structural in the plan's encounter/recap split, not absent from upstream artifacts.

---

### Cross-gap willpower-quitter re-argument (B only)

**Judge sources:** B book-arc (`re-argument` 2 — second anchor); B reader-journey-ch09 (partial — hard-quitter section).

**Shared symptom:** CH-09 re-proves that willpower-quitters' suffering proves the wrong method, already settled in CH-04.

**Distinct effects:** B-only; A book-arc does not flag this pair.

**Root component:** plan-card

**Evidence:** B book-arc quotes CH-04 *"His struggle is not proof that freedom is hard. It is proof that his method is hard."* vs CH-09 *"Her struggle was never proof that freedom is hard. Her struggle was the wrong method talking."* CH-09 card job is exception-killing, not willpower-method re-demolition.

**Mechanism:** Record as sampling noise / one-book cluster per census rules — do not map as next hypothesis target.

---

### `willpower-lexicon` noted floor

**Judge sources:** A voice-emotion ch01–ch13 (16 noted hits across 10 chapters); B voice-emotion (31 noted hits across 13 chapters). vs 019: A 21→16, B 33→31.

**Shared symptom:** Banned lexicon (`will`, `white-knuckle`, `battle`, `force`, `struggle`) appears in reader prose.

**Distinct effects:** Nearly all judges classify hits as attacking the wrong method, not prescribing it — noted, not blocking. B count remains the higher floor.

**Root component:** style-guide

**PERSISTENT —** writer-prompt and style-guide have been the attributed root for voice-lane lexicon/register failures in iter-000, 001, 005, 007, 009–018 learnings (8+ iterations on the voice hydra).

**Evidence:** Writer craft 4 bans willpower-register *"except to expose the illusion or wrong method."* Style guide carries the same exposure exception. Judges still count exposure uses (e.g. B ch08 — *"will is thinnest when feet ache"*; B ch11 — *"ugly things need no will to leave"*).

**Mechanism:** The permitted exception is broad enough that demolition prose routinely triggers the census class. This is a definitional boundary in the style/writer stack, not missing research or plan content.

---

### `factory-speech` / IN THIS CHAPTER leaks

**Judge sources:** A voice 6 noted; B voice 11 noted. vs 019: A 6→6, B 21→11 (B improved vs 019 but still elevated).

**Shared symptom:** Plan-card scaffolding surfaces in reader prose — `IN THIS CHAPTER` scene lists, numbered instruction headlines.

**Distinct effects:** B ch09, ch11 carry multi-hit `factory-speech`; A ch11, ch13 carry instruction-headline leaks.

**Root component:** plan-card

**PERSISTENT —** factory-speech at writer-prompt/plan-card level flagged in learnings iter-009 through iter-018 (9th+ iteration on the hydra).

**Evidence:** A ch11 response opens with plan-card scene tokens as prose (lines 4–8). B ch11 voice judge quotes *"**IN THIS CHAPTER** — late kitchen with ordinary biscuit tin…"* and *"11. TAKE YOUR LAST ORDINARY TREAT AND VOW FREEDOM"* in reader text. Cards supply these as compact headers; writer executes them literally.

**Mechanism:** Speakable plan-card headers and instruction serials reach the writer as card authority; no downstream strip rule removes them before generation.

---

### `copied-mannerism` scaffold

**Judge sources:** A voice 3; B voice 7. vs 019: A 2→3, B 7→7.

**Shared symptom:** Repeated Carr-shaped devices without fresh argumentative work — especially *"There is only one honest answer"* and *"champing at the bit"*.

**Distinct effects:** B ch08 notes the honest-answer tic 3× in one chapter; A ch12 notes plate-question trio reuse.

**Root component:** model

**Evidence:** B ch08 voice judge: *"`copied-mannerism` (1): 'There is only one honest answer.' (repeated at lines 24, 54, 128)"*. A/B ch11 voice: *"You should be champing to cross"* / *"champing at the bit"* vs Carr's nerve-normalization beat — `wrong-register` + `copied-mannerism` on same line.

**Mechanism:** Model reuses high-salience rhetorical templates across sections/chapters. No plan card assigns the tic; style guide does not mandate it.

---

### Intra-chapter `journey-stall`

**Judge sources:** A journey-ch01, ch07, ch09 (`journey-stall` 1 each); B journey-ch05, ch12 (`journey-stall` 1 each). vs 019: A 1→3, B 0→2.

**Shared symptom:** After a section consolidates, the chapter revisits the same beat shape before advancing.

**Distinct effects:** A ch01 ease-triple repetition; A ch07 ditch circles perpetrator/rescuer; B ch12 morning/shop/meals repeat scene→belief→triad→honest-answer shape.

**Root component:** model

**Evidence:** A journey-ch07 — after *"Kill the chant and the grumble starves on its own"*, ditch section restates perpetrator/rescuer before kitchen scene. B journey-ch12 — repeated *"There is only one honest answer"* blocks across vignettes.

**Mechanism:** Within-chapter structural repetition; distinct from cross-chapter `re-argument` but contributes to momentum drag noted in 022.

---

### `pre-debut-spend` SC-08 (B only)

**Judge sources:** B book-arc (`pre-debut-spend` 1).

**Shared symptom:** Rescuer-as-perpetrator compression appears in CH-05 before SC-08's scheduled CH-07 full debut.

**Root component:** plan-card

**Evidence:** Plan — CH-05 *"SC-08 seed only as question, full staging reserved for CH-07"*. B ch05 — *"You were never refuelled. You were rescued from the last rescue."* B ch07 opens full ditch-and-hand staging.

**Mechanism:** B-only sampling noise; record, do not target.

---

## Iteration 022 verdict on PRIMARY hypothesis

**Binding craft 3 did not achieve both-books fall** on journey `re-argument` (A improved one count; B worsened two counts; merged count rose).

**Trace diagnosis of why:**

1. **Plan-card overlaps survived unchanged** — the reused 019 plan still double-owns tomorrow (CH-10 + CH-11) and late-arc vignettes. Craft 3's overlap clause explicitly licenses spending the chapter on card-assigned overlap after one sentence, so the highest-salience late-arc rebuilds persist in both books.

2. **Model non-compliance on pure N←N−1 seams** — where cards do not re-own prior transitions, one-sentence openers appear in traces but body rebuilds continue (especially B mid-arc). Inputs were adequate; failures land at **model**.

3. **Writer-prompt is not cleanly isolatable this run** — the only editable change introduced a mechanism (overlap exception) that can absorb plan-card double-ownership instead of forbidding it, while the runner's last-line *"handoff seam"* assignment remains co-equal with craft 3. **PERSISTENT — writer-prompt** has been the attributed root component for re-argument / voice-lane failures across iter-000–001, 005, 009–018, 021–022 (10+ iterations); approach at this level may be wrong for journey `re-argument` while plan-card scheduling remains unrevised.

**Blocking:** 0 both books all lanes — no KEEP veto classes.

**Notable secondary census vs 019:** `willpower-lexicon` A improved, B flat; `factory-speech` B improved sharply; `journey-stall` rose both books; `belief re-argument` 4→5 merged; `book-arc re-argument` 5→3 merged (improvement).
