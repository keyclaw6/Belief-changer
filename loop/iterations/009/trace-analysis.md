# Trace Analysis — Iteration 009 (instrument baseline)

**Iteration:** 009 — instrument baseline after judge census redesign. No factory hypothesis. Two independent 18-chapter books from the accepted iter-000 master plan (`production-books/quit-sugar/master-plan.md`, trace copy at `traces/plan.md`). Writer: Muse Spark contributor-free via OpenCode Zen (replicate-a ch09 fell back to Vercel contributor once). Judges: composer-2.5.

**Instrument note:** Two voice judgments (replicate-a ch09, ch13) carry `PASS` as the first-line verdict but `verdict: FAIL` inside `CLUSTER CENSUS` with nonzero blocking counts. This analysis uses the census verdict field and blocking counts (7 voice FAIL per replicate), not the inconsistent header line.

---

## Merged CLUSTER CENSUS (verified from judgment reports)

Counts summed across replicate-a and replicate-b. **Signal** = class appears in both books. **Noise** = class appears in only one book (none at class level for blocking; chapter-level voice FAIL overlap is thin — see noise floor).

### Belief-mechanic (36 chapter judgments)

| Class | A blocking | B blocking | Merged blocking | Signal |
|-------|------------|------------|-----------------|--------|
| (all blocking classes) | 0 | 0 | **0** | — |
| belief 18/18 PASS each replicate | | | | |

### Reader-journey (36 chapter judgments)

| Class | A noted | B noted | Merged noted | Signal |
|-------|---------|---------|--------------|--------|
| journey-stall | 5 | 4 | **9** | yes |
| re-argument | 11 | 14 | **25** | yes |
| placement-miss | 1 | 1 | **2** | yes |
| blocking (all) | 0 | 0 | **0** | — |
| journey 18/18 PASS each replicate | | | | |

### Voice-emotion (36 chapter judgments)

| Class | A blocking | B blocking | Merged blocking | A noted | B noted | Merged noted | Signal |
|-------|------------|------------|-----------------|---------|---------|--------------|--------|
| factory-speech | 18 | 19 | **37** | 60 | 60 | **120** | yes |
| instruction-paperwork | 2 | 5 | **7** | — | — | — | yes |
| willpower-lexicon | 0 | 0 | 0 | 70 | 72 | **142** | yes (noted) |
| trap-question-label | — | — | — | 23 | 11 | **34** | yes (noted) |
| coach-register | — | — | — | 16 | 25 | **41** | yes (noted) |
| wrong-register | — | — | — | 12 | 18 | **30** | yes (noted) |
| copied-mannerism | — | — | — | 10 | 13 | **23** | yes (noted) |
| voice PASS/FAIL | 11/18 | 11/18 | — | | | | |

**Voice FAIL chapters (census verdict):**

- **Replicate A:** ch01, ch02, ch07, ch09, ch12, ch13, ch15 (7)
- **Replicate B:** ch01, ch03, ch04, ch06, ch14, ch16, ch18 (7)
- **Overlap:** ch01 only (1/7) — chapter-level FAIL sets are largely non-overlapping sampling.

### Book-arc (2 judgments)

| Class | A noted | B noted | Merged noted | Signal |
|-------|---------|---------|--------------|--------|
| re-argument | 7 | 8 | **15** | yes |
| curve-flatten | 1 | 1 | **2** | yes |
| pre-debut-spend | 2 | 1 | **3** | yes (asymmetric count) |
| blocking (all) | 0 | 0 | **0** | — |
| book-arc PASS both | | | | |

### KEEP objects (blocking in both books)

1. **factory-speech** — merged blocking **37** (systemic)
2. **instruction-paperwork** — merged blocking **7** (positional: threshold / recap chapters)

---

## Noise floor

| Observation | Classification |
|-------------|----------------|
| Voice chapter FAIL overlap (ch01 only) | **A/A sampling noise** at chapter grain; failure *classes* are not noise |
| Replicate-a ch09 Vercel fallback | **Not explanatory** — factory-speech blocking appears across both routes and replicate-b ch09 PASS |
| willpower-lexicon 142 noted, 0 blocking | **Noted-only signal** — lexicon names the enemy method; judges treat as census, not gate |
| placement-miss 2 total | **Weak signal** — present in both but count=1 each |
| pre-debut-spend A=2, B=1 | **Class in both, asymmetric** — noted craft debt, not blocking |

---

## Cluster summary

| Causal cluster | Spread | Judge sources | Root component | Priority reason |
|----------------|--------|---------------|----------------|-----------------|
| Factory craft/meta speech in reader prose | systemic | voice-emotion blocking `factory-speech` 37; noted `factory-speech` 120; belief/journey unaffected | writer-prompt | **KEEP object** — only blocking voice class in both books at scale; PERSISTENT (iter 000, 001, 005, 009) |
| Compliance instruction / clinical boilerplate in assigned lines | positional (C06, C15–C18) | voice-emotion blocking `instruction-paperwork` 7 | plan | **KEEP object** — second blocking class in both books; lands at vow/recap peaks |
| Cross-chapter semantic re-argument of settled scenes | systemic | reader-journey noted `re-argument` 25; book-arc noted `re-argument` 15 | plan | Largest arc craft debt; noted-only under Hydra lock |
| Research-report / epidemiology register in voice peaks | systemic (noted) | voice-emotion noted `wrong-register` 30; ch14 B blocking factory-speech litany | plan-card (+ research routing on C14) | Corroborates factory cluster; blocking only where litany job assigned |
| Speakable craft-label echo (`trap question`, coaching stage-direction) | systemic (noted) | voice-emotion noted `trap-question-label` 34, `coach-register` 41 | writer-prompt | High noted volume; never blocking under census judges |
| Mantra/ledger token pasted without naturalization | mixed systemic/local | voice A ch07, ch12; voice B ch03; plan FT-03 / mantra sheet | plan-card | Local FAIL driver where card tokens break grammar |
| Carr device mimicry without new grip | systemic (noted) | voice-emotion noted `copied-mannerism` 23 | model | Noted-only; adequate inputs still produce echo |

---

## Factory craft and internal meta speech leak into reader prose

**Judge sources:** voice-emotion blocking `factory-speech` — replicate-a 18, replicate-b 19 (merged **37**); noted `factory-speech` — 60+60=**120** across all chapters; corroborating noted `trap-question-label` 34, `coach-register` 41, `wrong-register` 30. Belief-mechanic and reader-journey blocking all zero.

**Shared symptom:** At emotional peaks, verdict moments, and mantra debuts, prose names factory machinery — craft labels, plan typography, ledger workshop vocabulary, production templates, persona codes, or stage-direction about how the line should land — instead of performing the move in Carr register. Reader hears assembly/audit, not one escaped guide.

**Distinct effects:**
- **BOXED DEFINITION / Decree template** at FT-01 debut (voice ch01 both replicates).
- **Killer-line / future-pace / emotional-turn meta** at demolition peaks (voice A ch02, ch09; noted widely).
- **FOR column / doing TO vs FOR workshop speech** in verdict lines (voice A ch07, ch09, ch12; voice B ch03, ch14).
- **Mantra fulfillment narration** — "We have named…" (voice A ch02).
- **Research-register litany** at readiness gate (voice B ch14 blocking 8).
- **Carr self-reference** in unassigned peaks (voice B ch10 noted).

**Root component:** writer-prompt — **PERSISTENT — this component has been the root cause 4 times (iter 000 Clusters 1–2, 001, 005, 009).** The Method and voice clause forbids surfacing internal identifiers (lines 51–56 of `prompts/chapter-writer.md`), but Binding chapter craft immediately re-introduces speakable craft diction the model copies into prose (lines 71, 92–94: `argue-to-compress`, `trap questions`, `killer-line pair`, `future-pacing`). Style-guide §9 repeats `trap questions` in checklist form echoed in the runtime prompt. Plan and cards supply workshop tokens (`BOXED DEFINITION`, `FOR column`, `frozen doctrine`) that the writer faithfully renders; the **first** contradiction is the writer contract ordering craft by name without a silent-execution rule strong enough to override the Binding list.

**Evidence:**

*Upstream — writer prompt (replicate-a ch01 `prompt.md`, identical contract in repo `prompts/chapter-writer.md`):*
```
Never surface the ledger's own vocabulary in reader-facing text: ... no internal drafting or craft labels
```
```
Use ... trap questions, ventriloquism, inversion, one killer-line pair per major argument, reassurance–challenge, future-pacing ...
```

*Upstream — plan (`traces/plan.md`):*
```
BOXED DEFINITION in Ch1 and Ch13, repeated as CAPS token thereafter: **BAD SUGAR = ...
```
```
Margin for error — frozen doctrine: *Your body can cope with an occasional blip, but your mind cannot.*
```

*Downstream — replicate-a ch01 `response.md`:*
```
> **BOXED DEFINITION — READ CAREFULLY**
> **Decree: When this book says "sugar," take it to mean BAD SUGAR.**
```

*Downstream — replicate-a ch02 `response.md`:*
```
But let me ask you a simple question. A trap question whose only honest answer concedes the point.
...
Two sentences. One killer pair. Let them close this move.
We have named the Sugar Trap.
```

*Downstream — replicate-a ch09 `response.md` (Vercel fallback; same failure class as Zen chapters):*
```
I will give you the killer-line pair at the peak of this movement.
Short sentences. Settled fact. They do not reopen.
Feel the emotional turn?
...
because we have reassigned every benefit and the FOR column is empty
That is frozen doctrine: your body can cope with an occasional blip, but your mind cannot.
Future-pace this with me, because prediction transfers authority and pre-labels the script so it arrives already disarmed.
```

*Downstream — replicate-a ch07 `response.md` (assigned FT-03 echo):*
```
That is the doing TO you vs doing FOR you switch. Capital TO, capital FOR. It makes the accounting honest.
```

*Downstream — replicate-b ch03 `response.md` (card token breaks grammar):*
```
*BAD SUGAR does plenty TO you and nothing FOR you — there is no a genuine pleasure or treat to weigh at all*
...
there is no **a genuine pleasure or treat** to weigh
```

**Mechanism:** The runtime writer contract tells the model to *use* named devices and plan workshop strings while a parallel clause says never to *say* them. Cards and plan pass production labels (`BOXED DEFINITION`, `FOR column`, `frozen doctrine`, mantra slot text) as authoritative content. The model resolves the conflict by literal compliance — copying craft names, typography instructions, and card tokens into peak prose. Judges classify literal craft/meta as blocking `factory-speech` at assigned moments; the same pattern in unassigned passages inflates noted counts without flipping chapter PASS where assigned lines stay clean.

---

## Compliance instruction and clinical boilerplate in assigned instruction lines

**Judge sources:** voice-emotion blocking `instruction-paperwork` — replicate-a **2** (ch15), replicate-b **5** (ch06, ch16, ch18); voice A ch15 blocking `factory-speech` 2 on same passages (cross-class corroboration).

**Shared symptom:** Assigned ALL-CAPS instructions read as terms-of-service or compliance paste — numbered clauses, internal instruction cross-references (`as in I-05 still applies`), chapter pointers `(Ch15)`, and appended clinical disclaimers inside the bold instruction line — at vow, firewall, and final-recap moments.

**Distinct effects:**
- **I-06 vow** with I-05 cross-ref repeated at climax (voice A ch15; voice B ch18).
- **I-05 firewall** with full medical tail as instruction body (voice B ch06).
- **I-07 / I-11** with "this is not medical advice" inside recap headers (voice B ch18).

**Root component:** plan — frozen instruction spine strings embed safety boilerplate and cross-references as part of the verbatim wording requirement; cards assign them at climax/recap with no spoken adaptation layer.

**Evidence:**

*Upstream — plan (`traces/plan.md` instruction spine):*
```
| I-05 | 5. IGNORE ANY ADVICE ... continue to follow your clinician's advice ... this book does not replace medical care. | C06 | mid C08, final C18 |
| I-06 | 6. NEVER DOUBT ... referral to clinician exception as in I-05 still applies. | C15 | final C18 |
```
```
Any instruction touching food change carries that exception verbatim.
```

*Upstream — replicate-a ch15 `chapter-card.md`:*
```
instruction: I-06 (never doubt decision — with safety exception)
```

*Downstream — replicate-a ch15 `response.md`:*
```
**6. NEVER DOUBT YOUR DECISION TO QUIT BAD SUGAR — Once you make the vow, never reopen the question; referral to clinician exception as in I-05 still applies.**
```
(same string at lines 136, 382, 406)

*Downstream — replicate-b ch18 `response.md` (judge quote):*
```
**6. NEVER DOUBT YOUR DECISION TO QUIT BAD SUGAR — ... referral to clinician exception as in I-05 still applies. (Ch15)**
**7. DO NOT USE SUBSTITUTES ... this is not medical advice. (Ch16)**
```

*Downstream — replicate-b ch06 `response.md`:*
```
5. IGNORE ANY ADVICE THAT CONFLICTS WITH THIS METHOD — ... this book does not replace medical care.
```

**Mechanism:** Plan safety policy folds clinician exceptions into frozen instruction text. Writer prompt requires exact instruction wording at climax (`prompts/chapter-writer.md` anatomy §5). Model outputs legal/compliance register inside assigned MATERIAL lines; voice judge fires blocking `instruction-paperwork` while belief-mechanic still PASS (instructions semantically present).

---

## Cross-chapter semantic re-argument of settled scenes and verdicts

**Judge sources:** reader-journey noted `re-argument` — A **11**, B **14** (merged **25**); book-arc noted `re-argument` — A **7**, B **8** (merged **15**); journey-stall noted A **5**, B **4**. No blocking journey or arc classes.

**Shared symptom:** Settled moves — confidence trick (S-04), tight-shoes inversion (S-01), rescuer-as-perpetrator, hundred-cords totality, empty FOR ledger, cinema credit reassignment — are rebuilt at full argumentative length in later chapters instead of brief token echo.

**Distinct effects:**
- Book-arc names confidence trick, tight-shoes, rescuer-perpetrator, hundred-cords as repeat offenders (replicate-a book-arc report).
- Journey ch08 both: `re-argument` 2 (mid-recap + scene re-stage).
- Journey ch18 both: pet rock / future-pace replay vs ch17.
- Book-arc `pre-debut-spend` — taste-recovery reframe spent before ch18 owns it (A **2**, B **1**).

**Root component:** plan — accepted iter-000 plan assigns the same scene IDs and ledger jobs to multiple chapter cards without a debut-once / echo-by-token law on scenes; cards say `scene: S-01 tight shoes` on C05, C07, C16 and full S-09 on C11 while earlier chapters already staged them.

**Evidence:**

*Upstream — plan scene bank + cards (`traces/plan.md`):*
```
| S-01 | **Tight shoes** — ... | Inversion flagship |
```
```
C05 card: scene: S-09 cinema fragment, S-01 tight shoes (reward ...)
C07 card: scene: S-01 tight shoes (cope ...)
C14 card: recap litany "• You know that ..." restating E-01–E-19
```

*Downstream — replicate-b ch14 `response.md` (full re-litigation before gate):*
```
* You know that the sweet lift you reach for at 3pm is a short spike ...
* You know that one bite can carry the box ...
* You know that each binge can release dopamine in the reward circuitry ...
```
(fourteen bullet-length replays — reader-journey ch14 noted `re-argument` 1)

*Downstream — replicate-a ch12 `response.md` (ledger + hundred-cord re-owned):*
```
Let us bring the ledger to this fear chapter ...
The hundred-cord image: one special exception keeps the machine humming ...
```

**Mechanism:** Plan optimizes for coverage per chapter card; writer prompt Binding §3 allows token invoke but does not forbid full re-demolition when the card re-assigns the scene job. Writer executes card literally → journey/arc judges note `re-argument`; arc still PASS because inversion completes.

---

## Research-report register at voice peaks (noted + local blocking)

**Judge sources:** voice-emotion noted `wrong-register` **30**; blocking factory-speech on replicate-b ch14 litany (**8**); voice B ch10 noted factory-speech (Carr self-reference); voice A ch16 noted wrong-register at supermarket cue.

**Shared symptom:** Prevalence statistics, neurochemistry pathways, observational-study hedging, and persona-code narration replace Carr's flat social speech at peaks where the reader should feel recognized, not studied.

**Root component:** plan-card — C14 card explicitly assigns `recap litany "• You know that ..." restating E-01–E-19 installed beliefs` with no translation rule; evidence rows route graded claims into recap without a voice layer. Research inputs are adequate; failure is how the card job is stated.

**Evidence:**

*Upstream — replicate-b ch14 `chapter-card.md`:*
```
evidence: none new — recap litany "• You know that ..." restating E-01–E-19 installed beliefs
```

*Downstream — replicate-b ch14 `response.md`:*
```
You know that each binge can release dopamine in the reward circuitry as part of the loop.
You know many people — about one in seven adults in pooled self-report scales ...
You know that refined carbs and fats together can evoke striatal dopamine ...
```

*Judge — replicate-b voice-emotion-ch14:* classifies litany as "research appendix" / "neurochemistry lecture" (factory-speech blocking).

**Mechanism:** Readiness-gate card treats prior evidence blocks as a checklist to restate; writer imports ledger-grade phrasing into `You know that` bullets → wrong-register and factory-speech at primary-job promise.

---

## Speakable craft-label echo (noted-only systemic)

**Judge sources:** voice-emotion noted `trap-question-label` **34**, `coach-register` **41**; zero blocking for these classes.

**Shared symptom:** Prose labels the device ("trap question," "Ask the trap question," "Future-pace it with me," "Feel the emotional turn?") or coaches the reader through the move instead of performing it.

**Root component:** writer-prompt — Method and voice and Binding craft name `trap questions` and related devices as obligations; style-guide §9 checklist repeats the phrase in the runtime bundle.

**Evidence:**

*Upstream — `prompts/chapter-writer.md` line 44:* `answer with two or three trap questions whose only honest answer concedes the point`

*Downstream — replicate-a ch02 `response.md`:* `A trap question whose only honest answer concedes the point.`

*Downstream — replicate-a ch07 `response.md`:* `Ask the trap question that ends the calm story.`

**Mechanism:** Model copies prompt diction into meta-narration; census judges note but do not block unless inside assigned verdict/instruction lines.

---

## Mantra and frozen-token paste without naturalization (local blocking)

**Judge sources:** voice blocking on replicate-a ch07, ch12; replicate-b ch03; MATERIAL assigned-moment lines on FT-03 / mantra debuts.

**Shared symptom:** Mantra sheet tokens (`doing TO you vs doing FOR you`, `a genuine pleasure or treat`) appear as slot-fillers with broken grammar or explicit annotation ("stated as settled fact, not as opinion").

**Root component:** plan-card — frozen token sheet supplies phrases that are not always grammatical when inserted verbatim into verdict sentences; cards mark debuts/echoes without spoken forms.

**Evidence:**

*Upstream — plan frozen tokens (`traces/plan.md`):* mantra and FT entries with exact strings including `doing TO you vs doing FOR you`.

*Downstream — replicate-b ch03 `response.md`:* `there is no a genuine pleasure or treat`

*Downstream — replicate-a ch12 `response.md`:* `Plenty **doing TO you vs doing FOR you**.` / `This is **doing TO you vs doing FOR you** stated as settled fact, not as opinion.`

**Mechanism:** Writer obeys verbatim-token rule (Binding §2–3) over Carr register; broken or annotated tokens trigger blocking `factory-speech` on assigned moments.

---

## Copied Carr mannerism (noted-only)

**Judge sources:** voice-emotion noted `copied-mannerism` **23** (A 10, B 13).

**Shared symptom:** Images and beats echo reference devices ("safe combination clicking," Carr stage-direction) without adding behavior-specific grip.

**Root component:** model — inputs are adequate; failure is generative echo under pressure to match Carr cadence.

**Evidence:** voice B ch01 noted `Like a safe combination finally clicking.`; voice A ch01 noted safe-combination echo. Writer prompt forbids reference imitation (line 61–62) yet mannerism still appears sporadically — noted only.

**Mechanism:** Sampling noise at line level; class present in both books at low noted volume, never blocking.

---

## Lanes that hold

- **Belief-mechanic:** 18/18 PASS both replicates; blocking all zero. Credit extraction, sacrifice inversion, trap questions as belief work, and assigned transitions complete.
- **Reader-journey:** 18/18 PASS both; blocking all zero. Noted `re-argument` and `journey-stall` do not break momentum under Hydra lock.
- **Book-arc:** PASS both; instruction spine, mantra debuts, curve, and escape arc complete. Noted re-argument is craft debt, not arc failure.

---

## Iteration 009 baseline read

Under the census instrument, the factory's **belief and journey mechanics are stable**; the **voice lane** fails on two blocking classes present in **both** replicates: systemic **factory-speech** (writer-prompt craft/meta leakage, PERSISTENT) and positional **instruction-paperwork** (plan frozen instruction + safety strings). Noted-only systemic classes (`willpower-lexicon`, `trap-question-label`, `coach-register`, `wrong-register`, `re-argument`) form the noise floor and secondary targets. Chapter-level voice FAIL overlap is minimal (ch01 only), consistent with iter-000 A/A observation: class sets across the book matter more than any single chapter's PASS/FAIL draw.
