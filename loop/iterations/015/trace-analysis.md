# Trace Analysis — Iteration 015

**Hypothesis tested:** Founder batch — seed subtraction from 014 Voice-operator strip: cards cite evidence IDs only; echo cites ID only; instruction frozen wording is ALL-CAPS headline only; trap-question formula deleted; semantic job-ownership on scene bank (`chapter-writer.md`, `master-plan-skill-v2.md`, `master-plan-reviewer-v2.md`, `style-guide.md`). Regenerated 16-chapter plan. Research reused. Two books. Judges: composer-2.5. Writer: Muse Spark contributor-free (`metadata.json` both replicates: `muse-spark-1.2-contributor-free`, `opencode`; no coded fallback on sampled chapters).

**KEEP objects this iteration targeted:** (1) voice noted `factory-speech` — 014 A **17** / B **38**; (2) book-arc noted `re-argument` — 014 A **5** / B **4**. Secondary prediction: blocking `factory-speech` stays **0**.

**Outcome vs 014 KEEP baseline:**

| Metric | 014 A / B | 015 A / B | KEEP prediction |
|--------|-----------|-----------|-----------------|
| Voice blocking `factory-speech` | 0 / 0 | **1** / **3** | stay 0 — **FAILED (reopened)** |
| Voice noted `factory-speech` | 17 / 38 | **20** / **13** | drop both — **FAILED** (A regressed; B improved; merged 55→33) |
| Book-arc noted `re-argument` | 5 / 4 | **6** / **5** | drop both — **FAILED** |
| Voice PASS | 15/15 | 15/16 | — |
| Voice PASS | 15/15 | 14/16 | B regressed (ch14, ch15 FAIL) |
| Belief / journey / book-arc | PASS both | PASS both | hold — **confirmed** |
| `trap-question-label` noted | 3 / 1 | **0** / **0** | confirming only — **closed** |

**PERSISTENT:** `factory-speech` at writer-prompt / plan-card level has been the residual or blocking root across iter-010 through iter-014 noted floor and iter-013 blocking — **6 times in learnings**. Iter-015 closed 014 blocking (CH-08 register operators) but reopened blocking on new local forms; the approach at this prompt level may still be wrong for the hydra.

---

| Causal cluster | Spread | Judge sources | Root component | Priority reason |
|----------------|--------|---------------|----------------|-----------------|
| Blocking factory-speech — verdict-landing assignment meta (A-only) | positional | A voice-emotion-ch05 blocking `factory-speech` 1; A voice-emotion-ch04/ch06 noted adjacent | writer-prompt | **KEEP blocking reopened** — A ch05 FAIL at primary-job peak |
| Blocking factory-speech — instruction spine serial prefix (B-only) | positional | B voice-emotion-ch14 blocking `factory-speech` 2; B voice-emotion-ch15 blocking `factory-speech` 1 | writer-prompt | **KEEP blocking reopened** — B vow chapters FAIL on assigned I-lines |
| Trap-question stage-direction prefixes (resolved) | systemic | 014 A ch07–09, B ch07; 015 census `trap-question-label` 0 both | style-guide | **Closed** — style-guide §5.8/§9 formula deletion worked |
| Noted factory-speech — evidence-limit / audit register | systemic | A voice ch02,06,07,08; B voice ch02,03,04,11; wrong-register paired | writer-prompt | **SIGNAL** — both books; cards ID-only but ledger resolution still reads as briefing |
| Noted factory-speech — mantra echo inventory density | systemic | A voice ch14 noted `factory-speech` 7; B ch02/09 patterns lower than 014 | plan | **SIGNAL** — both books; echo assignments + exact-echo contract still paste frozen tokens |
| Cross-chapter semantic re-argument | systemic | book-arc A `re-argument` 6, B 5; journey A 13, B 7; belief A 11, B 4 | plan | **KEEP object failed** — same settled jobs re-proved under new encounters |
| CH-08 register/job announcement (014 resolved) | — | 014 blocking 0; 015 A/B voice-emotion-ch08 PASS | plan-card | **Stays closed** — 014 Voice-operator strip held |

---

### Blocking factory-speech — verdict-landing assignment meta (A-only)

**Judge sources:** A replicate-a/judgments/voice-emotion-ch05 (`factory-speech` blocking 1). A voice-emotion-ch04 PASS (same template noted-adjacent). No B voice judge flags this string; grep B `replicate-b/traces/**/response.md`: no `Let me land it` / `belief that changes in this chapter`.

**Shared symptom:** At a demolition peak, the narrator announces what the chapter is doing instead of delivering the verdict inside the scene: `Let me land it as one short verdict, because this is the belief that changes in this chapter and you will carry it:`

**Distinct effects:** A-only at blocking severity. The template propagates A ch04→ch05→ch06 via previous-chapter continuity in the writer packet; ch07 mutates to `So let me leave you with the one short verdict this chapter exists to install…` (noted, not blocking). B never develops the chain.

**Root component:** writer-prompt

**Evidence:** Writer prompt Method and voice (both replicates, ch05 `prompt.md` L45): `land one short verdict`. Binding bans assignment-fulfillment narration (`Never announce the one job…`) but does not ban this verdict-landing preamble. Upstream continuity in A ch05 `prompt.md` L1738 seeds the exact blocking line from ch04 `response.md` L117. Downstream A ch05 `response.md` L119 repeats it at the fuel-lie peak — judge blocking gap. B ch05 same card, same packet craft rules, no matching prose.

**Mechanism:** The 015 batch removed card-level speakable operators but left a craft instruction (`land one short verdict`) the model can surface as reader-facing syllabus meta. In A, the previous-chapter seam amplifies a one-line ch03 landing (`Let me land it as you will carry it from now on`) into a full chapter-job announcement by ch04; ch05 copies the matured template at the assigned peak. Adequate inputs in B without the contamination chain → **ONE-BOOK NOISE** for this local blocking form; merged blocking class still reopens because B carries a different local form (below).

---

### Blocking factory-speech — instruction spine serial prefix (B-only)

**Judge sources:** B voice-emotion-ch14 (`factory-speech` blocking 2 on `8. NEVER DOUBT THE DECISION — REJOICE AT A DEAD ENEMY` and `10. TAKE YOUR LAST ORDINARY MEAL AND MAKE A SOLEMN VOW — YOU ARE FREE`). B voice-emotion-ch15 (`factory-speech` blocking 1 on `9. NEVER ENVY SOMEONE EATING BAD SUGAR — PITY THEM`). A voice-emotion-ch14 PASS — same assigned instructions without serial prefixes.

**Shared symptom:** Assigned instruction peaks read as pipeline checklist lines: ledger serial + frozen headline pasted into reader prose instead of plain Carr command.

**Distinct effects:** B pastes spine row numbers (`8.`, `10.`, `9.`); A renders bare ALL-CAPS headlines only (`NEVER DOUBT THE DECISION — REJOICE AT A DEAD ENEMY`; `TAKE YOUR LAST ORDINARY MEAL AND MAKE A SOLEMN VOW — YOU ARE FREE`) and passes. Same C-14/C-15 cards both replicates.

**Root component:** writer-prompt

**Evidence:** Plan instruction spine (`plan.md` L451–466): rows `I-08`…`I-10` with bare frozen wording; plan note: `Instruction wording is the bare imperative`. C-14 card (`chapter-card.md`): `new instruction: I-08 NEVER DOUBT THE DECISION — REJOICE AT A DEAD ENEMY; I-10 TAKE YOUR LAST ORDINARY MEAL…` — ID couples to headline for resolution, not for speech. Writer prompt Full-length chapter anatomy §5 (`chapter-writer.md` L122–126, echoed in ch14 `prompt.md`): `When an instruction is assigned: the numbered ALL-CAPS spoken headline at the climax.` That is the first point the factory **requires** serial numbering in prose. Downstream B ch14 `response.md` L122/L126: `8. NEVER DOUBT…` / `10. TAKE YOUR LAST…`. Downstream A ch14 `response.md` L125/L129: headlines without numbers — judge PASS on assigned I-lines.

**Mechanism:** 015 plan-skill narrowed frozen instruction wording to ALL-CAPS headline only and cards dropped second slogans, but writer anatomy §5 still mandates a **numbered** headline. B follows the numbering contract; judges count the serial as factory-speech on assigned moments. A omits numbers on adequate card/spine inputs → sampling on execution, not a both-books structural fix. **ONE-BOOK NOISE** at chapter FAIL level; contributes to merged blocking `factory-speech` 0→1/3.

---

### Trap-question stage-direction prefixes (resolved)

**Judge sources:** 014 census `trap-question-label` A 3 / B 1 (A ch07–09 `Ask the trap questions whose only honest answer concedes the point:`). 015 all 32 voice reports: `trap-question-label` 0. Grep 015 `replicate-*/traces/**`: no `Ask the trap` / trap-question stage-direction strings.

**Shared symptom:** Live Socratic questions preceded by a factory label naming the device.

**Distinct effects:** None in 015 — class absent both books.

**Root component:** style-guide (014 root; closed in 015)

**Evidence:** `change.diff` deletes style-guide speakable trap formula (`runs the trap questions whose only honest answer concedes the point` → `asks`). Writer packet ch08 `prompt.md` carries revised §5.8 (`The question is the next sentence`). Downstream traces: questions arrive unprefixed (e.g. A voice-emotion-ch04: `Did sugar create pleasure? Or did sugar hide the absence of it?`).

**Mechanism:** 015 style-guide + writer silent-execution edit removed the pasteable trap-question definition 014 identified. Confirming improvement; not the KEEP gate.

---

### Noted factory-speech — evidence-limit / audit register

**Judge sources:** A voice ch02 (`factory-speech` 1: validated-scale prevalence), ch06 (`factory-speech` 1: population cohort paragraph), ch07 (`factory-speech` 1: bounded qualifier), ch08 (`factory-speech` 3: neurochemical/report cadence). B voice ch02 (`factory-speech` 1: validated scales), ch03 (`factory-speech` 2: writer-meta + WHO register), ch04 (`factory-speech` 1: `I say seems to because…`), ch11 (`factory-speech` 4: circuitry diction). Spread: early through late middle.

**Shared symptom:** Unassigned passages briefly read as epidemiology briefing, study-design audit, or methods-section qualification where Carr keeps one person in the room.

**Distinct effects:** 014 had plan-card SUPPORTED/permitted paste as first wrong point; 015 cards are ID-only (e.g. C-05 card: `evidence: E-11, E-15, E-02` with no limit vocabulary). A count rose 17→20; B fell 38→13.

**Root component:** writer-prompt

**Evidence:** 015 C-05 card — evidence IDs only, guardrail `clinical limits honoured (CA-SAFE)` without row paste. Writer packet still embeds full evidence ledger rows the writer must resolve (`Honour those rows by not overclaiming`). Downstream A ch06 `response.md`: `Across large groups of people followed over time… checking whether low mood was driving the sweet-eating did not explain it away` — judge-noted audit register. Downstream B ch04: `I say seems to because that extra kick is the best reading of engineered desirability so far, not a proven law` — honest limit rendered as grading narration.

**Mechanism:** 015 plan-card subtraction removed the first factory paste surface 014 traced, but the writer contract still obligates ledger resolution without a translate-to-one-spoken-clause rule strong enough to prevent methods register. Both books retain the cluster; B improved, A did not — **SIGNAL** for noted floor, not KEEP success (A regressed).

---

### Noted factory-speech — mantra echo inventory density

**Judge sources:** A voice ch14 (`factory-speech` noted 7: consecutive mantra-token sentences in unassigned vow buildup). B voice ch09 (`factory-speech` noted 1: `I named it — the Nibbler's last whimper`). 014 cluster: backtick/frozen-token echo paste from mantra sheet + multi-echo cards (B ch02 ×5).

**Shared symptom:** Mandated frozen phrases stack as visible inventory — mechanism names and sensory slugs listed in factory cadence rather than absorbed into Carr speech.

**Distinct effects:** B echo paste count dropped sharply (38→13 noted `factory-speech` overall); A ch14 vow chapter concentrates seven noted hits. Echo cards now cite ID only (C-14: `echo M-A, M-B, M-C, M-H`; no pinned quotes per 015 plan-skill).

**Root component:** plan

**Evidence:** Plan mantra sheet + card echo assignments (C-14 four echoes; C-02 debut pins in plain text). Writer Binding: `land it exact in wording` / echo `brief grammatical spoken sentence`. C-14 structural responsibility assigns four echoes plus M-J debut at vow detonation. Downstream A ch14 noted block: six consecutive lines naming Sugar Trap / Nibbler / Big Confection / `faint, empty…` / `tired, wired and craving` as inventory.

**Mechanism:** 015 echo-card ID-only rule reduced B's early-chapter backtick paste (014's worst locus), but plan still stacks multi-echo vow chapters; writer exact-echo contract produces judge-noted factory texture when echoes cluster. Both books → **SIGNAL**; partial B improvement does not satisfy KEEP "drop in both."

---

### Cross-chapter semantic re-argument

**Judge sources:** Book-arc A `re-argument` 6, B 5 (semantic repetition: two-creature split, yo-yo, switchboard, 3pm fuel, contested-science blocks rebuilt from scratch). Journey A `re-argument` 13, B 7 (e.g. B reader-journey-ch08: Ch.7 dopamine/cue wheel re-run at length; B reader-journey-ch10: Ch.9 hunger/satisfaction replay). Belief A noted `re-argument` 11, B 4 (e.g. A belief-mechanic-ch07: `It's the other way around` re-proved after ch06; A belief-mechanic-ch13: contested-science re-proved after ch12; A belief-mechanic-ch15: 3pm fuel re-proved post-vow).

**Shared symptom:** Settled demolition jobs fully re-staged under new encounter tokens — same **job**, new scene/chapter ID — instead of brief token-echo.

**Distinct effects:** A journey/belief re-argument counts rose (journey 7→13; belief aggregate higher). B journey improved (12→7) but book-arc still 4→5. C-09 plan now restricts cinema/birthday to one full staging with token-only cinema/3pm echoes (improvement vs 014 cinema ch4→ch12 restage), yet middle chapters still overlap mechanism depth.

**Root component:** plan

**Evidence:** Plan scene-bank law (`plan.md` L365, L403; C-09 card L660): `cinema/3pm invoked only as one-phrase token echoes (no second staging)` — **014 cinema restage class improved**. Overlap persists elsewhere: C-07 card owns inversion/T-B debut + mechanism deepening; C-08 card primary job is recruitment (`engineered recruitment`) but shares demolition-high curve and overlapping evidence (`E-08, E-02`) with mechanism vocabulary — writers re-prove dopamine/cue wheel (B belief-mechanic-ch08 `re-argument` 1; B reader-journey-ch08). C-15 card L7: `not a restage of settled scenes` / `thoughts already owned, once`; A belief-mechanic-ch15 `re-argument` 1: 3pm fuel paragraph re-proved after C-05 settled fuel demolition. Plan-skill 015 semantic job-ownership block (`change.diff` master-plan-skill: `A later card must not make that same demolition true again under a new encounter or a new scene ID`) did not prevent regenerated cards from assigning encounters whose structural responsibility still requires full re-proof of prior settled jobs.

**Mechanism:** 015 tightened scene-ID debut-once and removed card evidence paste, but the regenerated sequence still schedules adjacent chapters whose primary jobs invite paragraph-length re-demolition of already-true inversions (mechanism wheel, inhabit beats, fuel credit, contested-science hedge). Reviewer law blocks **later** re-ownership in wording; accepted plan still carries the overlap judges count as `re-argument`. Both books → **SIGNAL**; book-arc counts did not drop in either replicate — **KEEP object failed**.

---

### CH-08 register/job announcement (014 resolved — stays closed)

**Judge sources:** 013–014 blocking class; 015 A/B voice-emotion-ch08 PASS, blocking `factory-speech` 0.

**Shared symptom:** N/A — class absent.

**Root component:** plan-card (014 fix held)

**Evidence:** C-08 cards (both replicates): no `Voice:` field, no `hard truth flat` / `deliver at full Carr force` operators. A/B ch08 responses open in scene (`Walk with me…`) without register meta. Grep 015 ch08 responses: no `I will say`, `We delivered`, `full strength`, `without hedging`.

**Mechanism:** 014 founder batch removal of speakable Voice/guardrail operators on cards held through 015 regeneration. Do not re-target as KEEP.

---

### Cross-check: blocking factory-speech local forms vs shared upstream

| Local form | 014 | 015 A | 015 B | Both-books? |
|------------|-----|-------|-------|-------------|
| CH-08 register/job announcement | blocking B | absent | absent | closed |
| Verdict-landing assignment meta | absent | **blocking ch05** | absent | A-only FAIL |
| Instruction spine serial (`8.`/`9.`/`10.`) | absent | absent (bare headline) | **blocking ch14–15** | B-only FAIL |
| Trap-question stage-direction | noted 3/1 | 0 | 0 | closed |
| Noted factory-speech merged | 55 | 20 | 13 | both non-zero; A worse |

Belief/journey/book-arc remain PASS both. Voice blocking reopened on **mutated** factory-speech forms, not the 013/014 CH-08 class.

---

### Unpaid residual for the next hypothesizer

**Closed (do not re-target as KEEP):** 014 CH-08 register/job announcement; 015 `trap-question-label` (0 both).

**KEEP failed — blocking `factory-speech` reopened (0/0 → 1/3):** two local hydra heads — (1) **verdict-landing assignment meta** seeded by writer-prompt `land one short verdict` + A continuity chain (A-only chapter FAIL); (2) **instruction spine serial prefix** required by writer anatomy §5 `numbered ALL-CAPS spoken headline` against bare-imperative plan spine (B-only chapter FAIL). Shared upstream: **writer-prompt** contradictory execution contracts. **PERSISTENT** (6th iteration).

**KEEP failed — noted `factory-speech` drop in both:** merged 55→33 but A 17→**20**. Residual both-books noted hydra: (1) **ledger-resolution audit register** (writer-prompt; plan-card paste removed); (2) **multi-echo inventory paste** on stacked vow/echo chapters (plan echo assignments + writer exact-echo rule). B improved; A did not.

**KEEP failed — book-arc noted `re-argument` drop in both (5/4 → 6/5):** **plan** still schedules paragraph-length re-proof of settled demolitions across middle/late cards (mechanism wheel ch7→ch8, inhabit replay ch9→ch10, contested-science ch12→ch13, fuel ch5→ch15) despite semantic job-ownership wording. C-09 cinema/birthday restage class improved vs 014; yo-yo/switchboard/two-creature/fuel jobs did not.

**Do not inherit as targets:** A-only verdict-landing template chain for blocking (B same inputs, no FAIL); B-only instruction serial blocking (A same cards, PASS); noted `willpower-lexicon` (Carr attacking anti-method); any judge initial-suspicion not verified above.
