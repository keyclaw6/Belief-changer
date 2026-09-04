# Iteration 021 — Trace Analysis

**Hypothesis:** Replace the previous-chapter clause in `prompts/chapter-writer.md` to close adjacent N←N−1 `re-argument` in the journey lane (PRIMARY vs 019: A 7, B 5).

**Outcome vs PRIMARY KEEP object:** **FAILED.** Journey `re-argument` merged **12 → 13** (A **7 → 6**, B **5 → 7**). All lanes PASS; blocking 0/0. One-book movement only — not KEEP.

**Secondary recorded movement:** Belief `re-argument` **4 → 12** (A 3→5, B 1→7). Book-arc `re-argument` **5 → 10** (A 3→3, B 2→7). `factory-speech` noted improved in B (21→8) but rose in A (6→15) — not decisive.

---

| Causal cluster | Spread | Judge sources | Root component | Priority reason |
|----------------|--------|---------------|----------------|-----------------|
| Adjacent N←N−1 seam re-argument | systemic | Journey A ch02,08,09,10,11,13; B ch05,08,11,12,13; Belief A ch08,11,12,13; B ch08,11,12,13; overlaps book-arc | writer-prompt | PRIMARY KEEP object; 13/13 journey hits are N←N−1; runtime prompt contradicts itself |
| Plan-scheduled duplicate demolition (adjacent + cross-gap) | systemic | Book-arc A,B; Journey A ch11; B ch05,11; Belief ch11 both | plan-card | Cards re-own settled jobs the writer contract cannot refuse; explains non-seam and arc-scale hits |
| Late-arc CH-12→CH-13 freedom recap re-run | positional | Journey B ch13 (re-argument 3, journey-stall 1); A ch13; Belief B ch12,13; A ch12,13 | plan-card | Closing recap card overlaps CH-12 ordinary-life scripts without a restaging ban |
| willpower-lexicon noted floor | systemic | Voice both (28 each, all chapters) | style-guide | Both-books design floor; unchanged vs 019 |
| factory-speech noted hydra | systemic | Voice A (15), B (8) | writer-prompt | PERSISTENT — 9th+ iteration at this component; not PRIMARY |
| copied-mannerism | A-heavy | Voice A (9), B (4) | model | B below A; not both-books signal for targeting |
| trap-question-label | A-only | Voice A (6), B (0) | — | Sampling noise; do not map |
| journey-stall | positional | Journey B ch13 (1); A none in journey census* | plan-card | *A stall only in B ch13 ledger; paired with late-arc cluster |

---

### Adjacent N←N−1 seam re-argument

**Judge sources:** Journey A ch02,08,09,10,11,13 (`re-argument` 6); Journey B ch05,08,11,12,13 (`re-argument` 7); Belief A ch08,11,12,13 (5); Belief B ch08,11,12,13 (7); book-arc instances that are the same passages counted once at arc scope.

**Shared symptom:** Chapter N re-runs chapter N−1's settled transition at (near) full length instead of entering one sentence past the installed belief. Examples:
- A ch08: CH-07 — *"The wrapper rustle from the next room. The bakery smell in the street. The clock striking nine…"* → CH-08 — *"Wrapper from the next room and mouth floods. Bakery smell in the street and feet turn. Clock strikes nine…"*
- B ch12: CH-11 faint-echo / dying-loop block → CH-12 same transition at full section length.
- A ch02: CH-01 free-choice seed → CH-02 *"If sweet food is your free choice… why are you reading a book about how to stop?"* at fuller length.

**Distinct effects:** A lost late-arc concentration (019 had ch11×2, ch12, ch13×2; 021 has ch13×1 in journey) but gained mid-arc seams (ch09, ch10). B lost ch02 hit but gained ch05 and ch13×3. Pattern shifted position; class did not fall in both books.

**Root component:** writer-prompt

**Evidence:** `prompts/chapter-writer.md` lines 13–18 carry the new closed-for-this-chapter ban. Every assembled runtime prompt in both replicates embeds that text **and** contradicts it in the closing assignment injected by `scripts/loop-runner/write_replicate.py` lines 48–53:

```48:53:scripts/loop-runner/write_replicate.py
    assignment = (
        f"Write {title_s} of `production-books/{SLUG}` as the complete chapter file. "
        "Your chapter's card is the authoritative semantic authority. Resolve every ID it cites "
        "against the plan-wide inventories in the master plan. Use the immediately previous chapter "
        "only for voice continuity and the handoff seam. Do not read or seek anything beyond these "
        "four inputs."
```

Trace confirmation — `replicate-a/traces/chapter-08/prompt.md` line 13–18 (new ban) vs line 155 (old *"handoff seam"* closing line). Downstream, `chapter-08/response.md` line 105 reproduces CH-07 cue-firing verbatim-expanded despite CH-08 card job being manufacture/fear (no cue-firing assignment on `chapter-card.md`).

Binding craft 3 (`prompts/chapter-writer.md` ~97) licenses only **frozen-token** echoes; most flagged transitions (cue-firing, deserve-it loop, dying-loop, free-choice block) have no pinned token, leaving no short licensed form when the closing line re-opens the seam.

**Mechanism:** Hypothesis updated the static writer template but not the runner's closing assignment. The last task-specific instruction before plan/card/previous-chapter inputs re-authorizes *handoff seam* work. The model receives the full previous chapter as input and rebuilds its argued transitions to bridge into the card job — exactly what journey judges measure as N←N−1. A partial drop in A (7→6) is consistent with sampling on the same contradictory contract, not a both-books close.

**PERSISTENT — writer-prompt has been named root cause in iterations 001, 005, 010–011, 013–014, 015–018 (voice hydra) and now 021 (journey seam). The approach at this level may be wrong unless the **assembled** runtime contract is made single-voiced.**

---

### Plan-scheduled duplicate demolition (adjacent + cross-gap)

**Judge sources:** Book-arc A (`re-argument` 3): ch4 re-runs ch2 yo-yo / evening-box; ch7 re-runs ch3 rescuer. Book-arc B (`re-argument` 7): tight-shoes in ch4/5/7; Monday diary after ch2 kitchen con; seatbelt ch8/10; tomorrow ch10/11; willpower-quitter ch4/9; favourite-meal ch12 after ch6. Journey A ch11; B ch05, ch11. Belief both ch11.

**Shared symptom:** A later card performs a **full demolition** of a job already settled one or more cards earlier, not a one-sentence token echo.

**Distinct effects:** Book-arc A hits are **non-adjacent** (ch4←ch2, ch7←ch3). Book-arc B spreads the same scene/analogy (tight shoes) across three cards. Journey ch11 in both books re-proves tomorrow/postponement after ch10 already owns that voice-pool line.

**Root component:** plan-card

**Evidence:** Adjacent overlap — CH-10 card (`plan.md`): Job resolves *"I'll allow Fridays / just one / I'll wean"* and voice pool assigns *"I'll quit tomorrow / after birthday / after holidays — CH-10."* CH-11 card: Job resolves *"I'll start after holidays / when ready someday"* with Belief-now *"enters lingering that tomorrow is safer."* That makes re-demolition the **assigned semantic work**, which the writer prompt elevates as *"authoritative semantic authority"* over the previous-chapter closure. Cross-gap — CH-02 Encounter: *10pm kitchen… cupboard*; CH-04 Encounter: *diet-week diary… forbidden-must-have rebound* with SC-04 *evening-box proof* — book-arc judge quotes both as full re-stagings of yo-yo/evening permission settled in ch2. CH-04 introduces tight shoes briefly; CH-05 card Encounter is fuel afternoon — journey B ch05 flags shoes rebuilt at length.

Plan-skill line 94 requires adjacent cards to *"build cumulatively rather than repeat"* but cards still assign overlapping encounters; continuity fields are one-line handoffs only (`Continuity: receives totality; hands free identity to CH-12.`) with no closed-list of settled jobs on the card (020's expanded continuity bullet is **not** in the reused plan's card shape).

**Mechanism:** When the card assigns the same semantic demolition as the prior card (or an earlier card under a new scene ID), the writer must re-argue to fulfill the card. Journey judges count this whether or not it is strictly N←N−1. This cluster explains book-arc rise B 2→7 and belief ch11 hits both books; it is **not** fixed by the previous-chapter clause alone.

**Note on judge suspicion:** Journey ch11 *"initial suspicion: plan-card"* — **verified** for the tomorrow/postponement overlap. It does **not** explain cue-firing (ch08) or free-choice (ch02), where cards assign different jobs.

---

### Late-arc CH-12→CH-13 freedom recap re-run

**Judge sources:** Journey B ch13 (`re-argument` 3, `journey-stall` 1); Journey A ch13 (`re-argument` 1); Belief B ch12 (3), ch13 (2); Belief A ch12 (1), ch13 (2).

**Shared symptom:** Closing chapter re-inhabits CH-12 ordinary-life beats (breakfast/shop/cinema/sofa list, pity-not-envy, doubt-witness, BAD SUGAR treat credit) at paragraph length before new closing layers.

**Distinct effects:** B journey ch13 carries three separate re-argument counts plus journey-stall on the scene list; A ch13 journey is lighter (1) but belief still records 2 paragraph-scale re-proofs.

**Root component:** plan-card

**Evidence:** CH-12 card: Job *"non-argument — bridge — inhabits mornings, shops, food…"*; Guardrail *"no settled-scene restaging."* CH-13 card: Job *"non-argument — recap — photographable instruction list…"*; Structure *"short recap list… without callbacks"*; Scenes *"none new."* No field forbids re-running CH-12's ordinary-life **scripts** (only "no callbacks" to earlier chapters). Writer receives CH-12 as the previous-chapter input for CH-13. Downstream — B journey ch13 quotes CH-12 pity/envy and doubt passages at near full length; journey-stall on *"Go to breakfast hungry. Go to the shop with clear eyes…"* scene list.

**Mechanism:** Recap card + previous-chapter input + no restaging ban on the immediately prior ordinary-life chapter invites the writer to pad the recap by replaying CH-12 vignettes. This is positional (late arc) but appears in **both** books at belief lane; journey concentration is B-heavy.

---

### willpower-lexicon noted floor

**Judge sources:** Voice both replicates — `willpower-lexicon` 28 each (every chapter).

**Shared symptom:** Banned lexicon (`willpower`, `discipline`, `resist`, etc.) appears while attacking the wrong method, not prescribing it.

**Root component:** style-guide

**Evidence:** Voice judges consistently mark these as NOTED with *"names illusion, does not prescribe."* Count unchanged 019→021 in both books. Style-guide and writer Binding craft 4 permit lexicon only to expose the wrong method.

**Mechanism:** Census design floor under current style-guide; not a factory regression and not the PRIMARY object.

---

### factory-speech noted hydra

**Judge sources:** Voice A (`factory-speech` 15); Voice B (`factory-speech` 8). 019 baseline: A 6, B 21.

**Shared symptom:** Workshop/register leakage — evidence-limit narration, unassigned operators, instruction-line artifacts, meta-commentary.

**Root component:** writer-prompt

**Evidence:** A ch08 voice judge: `factory-speech` 6 including prevalence-room narration. A ch09: instruction context `I-04: (unresolved)` flagged numbered instruction lines. Writer never-surface list (`chapter-writer.md` ~66–74) bans many surfaces but hydra mutates (e.g. ch13 *"Let visible ease do any talking"*).

**Mechanism:** **PERSISTENT — this component has been the root cause 9+ times** (learnings iter 001, 005, 009–018). Partial B improvement is one-book sampling, not both-books KEEP.

---

### copied-mannerism

**Judge sources:** Voice A (9); Voice B (4).

**Shared symptom:** Repeated closing cadences and stock phrases across chapters (*"There is only one honest answer"*, *"Rejoice… Pity the hunt, do not obey it"*, *"champing at the bit"*).

**Root component:** model

**Evidence:** Inputs adequate — no card assigns these phrases. A ch05/ch06 voice judges quote identical house-pattern closings across adjacent chapters. B count half of A on the same plan.

**Mechanism:** Model habit under Muse Spark 1.3; one-book skew. Record, do not target for KEEP.

---

## PRIMARY verdict summary

| Metric | 019 baseline | 021 result | KEEP? |
|--------|-------------|------------|-------|
| Journey `re-argument` A | 7 | 6 | partial |
| Journey `re-argument` B | 5 | 7 | **no** |
| Merged journey | 12 | 13 | **REVERT / INCONCLUSIVE** |

**Diagnosis:** The 021 writer-only previous-chapter clause did not produce the predicted both-books fall. Trace shows the fix was **incomplete at the writer-prompt assembly layer** (`write_replicate.py` closing line contradicts `chapter-writer.md`), and a **second systemic cluster** remains at plan-card: cards still assign full re-demolition of settled adjacent and cross-gap jobs, which the writer cannot refuse. Late-arc CH-12→CH-13 recap overlap is a third positional cluster in both books at belief lane.

**What improved (noted, not PRIMARY):** A journey −1; B `factory-speech` 21→8.

**What regressed:** B journey +2; belief and book-arc `re-argument` materially worse merged.

**INSUFFICIENT TRACE for model-only attribution:** Runtime inputs are **not** mutually consistent (contradicting previous-chapter instructions), so `model` is not assigned for the PRIMARY cluster.
