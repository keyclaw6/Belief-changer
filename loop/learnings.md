# Auto-Tuning Loop — Learnings

> Every iteration (pass or fail) appends here. Format: iteration number,
> date, hypothesis, what changed, what happened, verdict, lesson.
>
> **Founder 2026-08-24:** REVERT is not a ban. A reverted factory change
> remains eligible, including exact prior wording. Iterations 001–008
> were scored on the retired PASS/FAIL-by-label instrument; their
> "Do not repeat" / PIVOT lines do not bind 009 onward. 3-strike resets
> with the judge change. 008's model swap stays forbidden because models
> are founder-only, not because it REVERTed. Under one stable instrument,
> do not blindly re-run the identical hypothesis against the same census
> class with no new mechanism.

---

### iter-000 — BASELINE
**Hypothesis:** none — baseline (no hypothesis, no change); establish the accepted state of the factory.
**Change:** (none — full fresh run: research → plan → 18 chapters → panel → A/A → trace analysis)
**Verdict:** BASELINE
**Lesson:** The factory's belief-mechanic work is solid (18/18 PASS) and the book arc lands (book-arc PASS); the recurring material failure is the *voice lane* — evidence-grading scaffold and factory-internal taxonomy (S/P/I/M codes, craft directives) leak verbatim into reader prose at emotional peaks. Root: writer-prompt over-orders ("preserve every evidence grade … permitted/prohibited inference") with no translate-or-strip rule; and no ban on surfacing internal identifiers. Secondary: plan schedules the same scene/evidence (S-04/E-11; S-09/E-01/E-03) into adjacent chapters causing cross-chapter re-argument; a local model error in C02. Hood: 4 causal clusters; Cluster 1 and 2 (both writer-prompt) dominate the voice lane.
**Next direction:** hypothesize one causal change — writer-prompt: replace "preserve every evidence grade/permitted-prohibited inference …" with a rule that translates each evidence-limits constraint into plain Carr register (or quarantines it), and forbid surfacing internal identifiers/draft directives in reader prose. Then rerun full book and re-judge the voice lane.

Baseline established. Top causal clusters: (1) evidence-grading scaffold leaked verbatim into reader prose — writer-prompt — systemic; (2) factory-internal taxonomy & drafting scaffolding leaked into reader prose — writer-prompt — systemic; (3) cross-chapter re-argument of settled scenes/evidence instead of invoke-by-token — plan — positional; (4) local grammatical/lexical fabrication in chapter 2 — model — local.

**A/A noise observation:** chapter 01 run 1 = PASS across all three lanes; chapter 01 run 2 (identical inputs, regenerated) = belief-mechanic PASS + reader-journey PASS + voice-emotion FAIL (one material gap: the evidence-grading register at the shame-removal peak). The material failure-class set **differs** between the two runs (run 1: none; run 2: one voice class = Cluster 1 evidence-grading leak). This calibrates "material": the dominant systemic cluster is present across many chapters but its *appearance in any single chapter is sampling-sensitive* — the same chapter can pass or fail the voice lane on a re-run. Decisions must be made on the failure-class set across the book, never on a single chapter's instance.

### iter-001 — scaffold firewall
**Hypothesis:** Replace the writer-prompt "preserve every evidence grade…" command with an internally-hold / never-surface-ledger-vocabulary rule so voice-lane Clusters 1 and 2 close.
**Change:** `prompts/chapter-writer.md` evidence-honesty clause (already on campaign as `be106a5`); regenerated all 18 chapters.
**Verdict:** REVERT
**Lesson:** Banning ledger labels is not the same as banning factory speech. Verbatim SUPPORTED/Permitted-inference dumps largely vanished, but Binding chapter craft still uses speakable diction (`killer-line pair`, `argue-to-compress`, `your card assigns`, persona codes) and the model emits it; Cluster 1 mutated into research-report register. Voice FAIL count stayed 14/18. Old-instrument result — eligible to retry after the 2026-08-24 judge change.
**Next direction:** Writer-prompt Binding craft silence was the then-next move. 001 wording is eligible again under census judges.

### iter-002 — debut-once echo-by-token
**Hypothesis:** Replace the plan-skill mantra-only repetition law with a debut-once / echo-by-token law covering mantras, scenes (S-xx), and evidence rows (E-xx) so 001 Cluster 4 (cross-chapter re-argument) closes in book-arc.
**Change:** `prompts/master-plan-skill-v2.md` (Mantra and frozen-token sheet — one sentence). Research reused; new plan; 19 chapter files regenerated on Vercel Muse Spark. Judges: composer-2.5.
**Verdict:** REVERT
**Lesson:** Debut-once on S-xx/E-xx closed the named 001 instances (ledger re-walk, 100-cord restage, scare loop; reader 19/19 PASS) but book-arc still FAIL on the same class mutated (wanting/liking rebuilt at Sunlit Table; Willpower Method re-installed; M-09/M-10 before debut). Voice 0/19 PASS with a NEW class: echo-law placeholders (`by name in one sentence here`) copied from card parentheticals into prose. Old-instrument result — eligible to retry after the 2026-08-24 judge change.
**Next direction:** Then-next was bind jobs/evidence without speakable echo templates. 002 wording is eligible again under census judges.


### iter-003 — card job/evidence re-own ban
**Hypothesis:** Bind Compact chapter cards so settled jobs/evidence cannot be re-owned for a second full demolition, and ban speakable echo parentheticals on cards, so 002 Cluster 5 closes in book-arc.
**Change:** `prompts/master-plan-skill-v2.md` (Compact chapter cards — job + evidence bullets + superseding paragraph). Research reused; new plan (20 chapters); full rewrite on Vercel Muse Spark. Judges: composer-2.5.
**Verdict:** REVERT
**Lesson:** Binding job/evidence re-lists closed the named 002 symptoms (wanting/liking rebuild, Willpower re-definition; echo placeholders gone; belief 20/20; reader 19/20; voice 6/20). Book-arc still FAIL on the same class mutated via scene IDs (A01 tight-shoes re-performed C03→C07), token pre-debut (T04 in C09), readiness seam duplication (C16→C17), and hand-off rebuild (C20). Plan-skill edits that only constrain evidence/job fields leave scene-bank re-assignment and adjacent-card seam ownership free. Old-instrument result — eligible to retry after the 2026-08-24 judge change.
**Next direction:** Founder later resumed. 003 wording is eligible again under census judges.

### iter-004 — scene-bank debut-once
**Hypothesis:** Bind Scene and analogy bank so each scene/analogy ID gets one full staging at a debut chapter; later cards may only token-echo, closing 003 Cluster 1 (A01 tight-shoes double full stage).
**Change:** `prompts/master-plan-skill-v2.md` (Scene and analogy bank). Research reused; new plan (21 files); full rewrite on Vercel Muse Spark. Judges: composer-2.5.
**Verdict:** REVERT
**Lesson:** Scene debut-once closed the named A01 C03→C07 double full stage, but book-arc still FAIL on the same re-argument class mutated (FM completes inversion early; A-07 vault-safe doubled FM→C01; mantra/token pre-debut; C16 encyclopaedic re-litigation). Third consecutive plan-skill REVERT on this class under the old instrument (002, 003, 004). That PIVOT does not bind after the 2026-08-24 judge change. Voice still 3/21 PASS; writer-prompt Binding craft was the unpaid voice target then.
**Next direction:** Plan-skill re-argument wording from 002–004 is eligible again under census judges.

### iter-005 — Binding craft silent-execution
**Hypothesis:** Make craft execute silently in `prompts/chapter-writer.md` — delete speakable craft diction (trap question, killer-line, argue-to-compress, future-pacing, persona codes) to close voice Cluster 6 after plan-skill 3-strike pivot.
**Change:** Three hunks in `prompts/chapter-writer.md` (Method and voice + Binding bullets 2 and 7). Research+plan reused; 18 chapters rewritten on Muse Spark. Judges: composer-2.5.
**Verdict:** REVERT
**Lesson:** Voice **0/18 PASS** — regression from 004 (3/21) on the old instrument. Some literal craft-label leaks reduced but factory scaffolding, research-register, persona codes, and meta-commentary persist or worsen. Silent-execution ban did not change model behavior enough then; voice Cluster 6 unpaid. Book-arc still FAIL (mantra echoes, repeated scenes). Eligible to retry after the 2026-08-24 judge change.
**Next direction:** 005 wording is eligible again under census judges.

### iter-006 — Speakable Card Sanitization gate
**Hypothesis:** plan-reviewer Gate 4 strips speakable craft/persona literals from compact cards before generation, closing voice Cluster 6 + persona Cluster 3.
**Change:** `prompts/master-plan-reviewer-v2.md` Gate 4. New 20-chapter plan (3 review rounds); full rewrite Muse Spark. Judges composer-2.5.
**Verdict:** REVERT
**Lesson:** Persona P-xx codes eliminated from prose; voice rose 0/18→5/20 but still 14 FAIL on the old instrument; trap-question phrasing persists in 17 chapters; book-arc FAIL on arc-timing/re-litigation. Reviewer gate improved cards but did not close owning voice class then. Eligible to retry after the 2026-08-24 judge change.
**Next direction:** Gate 4 wording is eligible again under census judges.

### iter-007 — style-guide speakable craft ban
**Hypothesis:** Remove craft-label vocabulary from style-guide so trap question etc. stop surfacing; voice Cluster 1 closes.
**Change:** `prompts/style-guide.md` — disarming one-answer question, speakable craft ban in §9, toolkit renames.
**Verdict:** REVERT
**Lesson:** trap question 17→3 but voice **1/20** (worse than 006) on the old instrument. Belief 20/20; book-arc FAIL. Style-guide surface alone did not close voice then while writer-prompt still names devices. Eligible to retry after the 2026-08-24 judge change.
**Next:** 007 wording is eligible again under census judges. 008's model swap is still founder-only — not a retry candidate.

### iter-008 — writer non-contributor model (FINAL)
**Hypothesis:** meta/muse-spark-1.2 primary improves craft-ban adherence vs contributor.
**Change:** `loop/config.yaml` writer_model → meta/muse-spark-1.2.
**Verdict:** REVERT
**Lesson:** Voice 5/20; trap question 17/20 on the old instrument. Campaign 004–008 all REVERT under that instrument. **008 is not eligible to retry as a hypothesis** — models/routes are founder-only. The *prompt and structure* changes from 001–007 remain eligible under census judges.

### founder-2026-08-24 — REVERT is not a ban
**Hypothesis:** none — founder process amendment.
**Change:** Hypothesizer, PROGRAM, North Star, and this file: REVERT does not forbid retrying a factory change. 001–008 prompt/structure wording is eligible under the census judges. 3-strike resets with the judge change. 008 model swap remains founder-only.
**Verdict:** n/a
**Lesson:** Last campaign's reverted writer-prompt, plan-skill, plan-reviewer, and style-guide edits may still be the right move. Treat old Lessons as what happened under the retired instrument, not as a never-repeat list.
**Next direction:** 010+ may retry 001–007 changes when 009 traces point at the same component.

### iter-009 — instrument baseline (census judges)
**Hypothesis:** none — fresh baseline after judge census redesign.
**Change:** none. Two books from the accepted 000 18-chapter plan. Writer Muse Spark Zen contributor-free (A ch09 one Vercel fallback). Judges composer-2.5.
**Verdict:** BASELINE
**Lesson:** Belief 18/18 PASS both; journey 18/18 PASS both; book-arc PASS both. Voice 11/18 PASS both. KEEP objects: blocking `factory-speech` (merged 37) at writer-prompt Binding craft / speakable device names — PERSISTENT; blocking `instruction-paperwork` (merged 7) at plan frozen instruction+safety strings. Noted floor: willpower-lexicon 142, factory-speech 120, coach-register 41, trap-question-label 34, journey/arc re-argument 40. Voice FAIL chapter overlap is ch01 only (sampling). Noise floor: classes in both books; chapter PASS/FAIL is not the KEEP object.
**Next direction:** Close factory-speech in both books (writer-prompt silent craft, or 005-style Binding rewrite now eligible). Secondary: plan instruction-paperwork. Re-argument remains noted-only.

### iter-010 — writer-prompt silent craft + workshop-token translation
**Hypothesis:** Silent craft execution plus workshop-token translation supremacy in `prompts/chapter-writer.md` drops voice blocking `factory-speech` in both books.
**Change:** `prompts/chapter-writer.md` (Method and voice trap-question line; never-surface/workshop ban; Binding bullets 2 and 7). Research+plan reused; 18×2 rewrite on Muse Spark Zen. Judges: composer-2.5.
**Verdict:** KEEP
**Lesson:** factory-speech blocking 18→6 (A) and 19→8 (B). Trap-question labels and boxed-definition/killer-line meta mostly gone. Residual factory-speech is plan workshop tokens (`FOR column`, BOXED residual), anatomy/style-guide checklist leaks, and verbatim mantra slugs. instruction-paperwork 2→3 / 5→6 on unchanged plan strings. method-promise-hedge B-only. Belief/journey/arc still hold.
**Next direction:** Residual factory-speech at plan-card/style-guide bundle and frozen-token paste — or plan instruction-paperwork. Do not repeat the exact 010 hunks blindly; 005/010 writer-prompt surface still eligible with a new mechanism.

### iter-011 — style-guide silent operators
**Hypothesis:** Silent-execution rewrite of `prompts/style-guide.md` §B5/B7/B9 drops voice blocking `factory-speech` in both books.
**Change:** `prompts/style-guide.md` (B5 header + operators 3/6/8/11; B7 §5; B9 checklist). Research+plan reused; 18×2 rewrite on Muse Spark Zen. Judges: composer-2.5.
**Verdict:** KEEP
**Lesson:** factory-speech blocking 6→4 (A) and 8→2 (B). §B5 operator labels (`killer pair`, `Future-pace`, `Warm rationale:`) no longer block. Residual factory-speech is plan I-06 ID cross-ref (`as in I-05`) plus A-only FT-06 inventory. instruction-paperwork 3→5 / 6→5 on unchanged plan safety tails (PERSISTENT, 3rd time). Belief/journey/arc still hold. Voice PASS 13→15 / 11→16.
**Next direction:** Plan instruction spine (paperwork + I-06 factory ID). Founder halt after 011 — do not start 012 until asked.

### iter-012 — plan-skill instruction-spine split
**Hypothesis:** Frozen instruction wording as spoken Carr imperative only, clinical limits in boxed CA-01, no `as in I-05` cross-refs, drops voice blocking `instruction-paperwork` in both books.
**Change:** `prompts/master-plan-skill-v2.md` (Lexicon / instruction spine). Plan regenerated (17 chapters). Two books on Muse Spark Zen. Judges: composer-2.5.
**Verdict:** KEEP
**Lesson:** instruction-paperwork blocking 5→0 / 5→0 — named close. I-05/I-06 tails and `as in I-05` gone from spine and chapters. factory-speech blocking 4→3 / 2→9 (B regressed on craft-label / ledger surfaces, not the old I-06 ID). Journey `compliance-missing` 2/1 is I-08 vs M-08 ID collision (mantra-sheet wording present). Belief/arc hold; journey 16/17 both.
**Next direction:** Residual factory-speech at style-guide toolkit/beat labels and writer-prompt ledger callbacks. Plan I-08/M-08 numbering. Founder halt: do not start 013.

### iter-013 — founder-batch spine and packet hygiene
**Hypothesis:** Simultaneous rewrite of writer, plan-skill, plan-reviewer, and style-guide (Carr spine + packet hygiene + lettered mantra IDs) drops factory-speech blocking and closes I-08/M-08 compliance-missing in both books.
**Change:** `prompts/chapter-writer.md`, `prompts/master-plan-skill-v2.md`, `prompts/master-plan-reviewer-v2.md`, `prompts/style-guide.md`. Plan regenerated (14 chapters). Two books on Muse Spark Zen. Judges: composer-2.5.
**Verdict:** KEEP
**Lesson:** factory-speech blocking 3→2 / 9→2; named 012 craft-label/ledger/P-xx surfaces gone. compliance-missing 2→0 / 1→0 (lettered M-A…M-I). Belief/journey 14/14, book-arc PASS both. Residual blocking is CH-08 register/job announcement from plan-card Voice/guardrail lines (PERSISTENT factory-speech at prompt/card level). Attribution is a founder batch, not one cause.
**Next direction:** Residual factory-speech at CH-08 plan-card Voice operators (speakable "hard truth flat"). PERSISTENT — prompt-level bans are mutating the class, not closing it. Founder halt: do not start 014 unless asked.

### iter-014 — founder-batch card operators and rooms
**Hypothesis:** Simultaneous rewrite of writer, plan-skill, plan-reviewer, and style-guide (strip speakable Voice/guardrail operators; no Maya; CA-SAFE title not pasted; inhabit as primary job; IN THIS CHAPTER as rooms) drops factory-speech blocking in both books.
**Change:** `prompts/chapter-writer.md`, `prompts/master-plan-skill-v2.md`, `prompts/master-plan-reviewer-v2.md`, `prompts/style-guide.md`. Plan regenerated (15 chapters). Two books on Muse Spark Zen. Judges: composer-2.5.
**Verdict:** KEEP
**Lesson:** factory-speech blocking 2→0 / 2→0; CH-08 register/job announcement gone from both traces. Voice 15/15 both. Belief/journey 15/15, book-arc PASS both. Noted factory-speech A 29→17 / B 28→38 — hydra (evidence-limit register, frozen-echo paste, trap-question prefixes). Attribution is a founder batch, not one cause.
**Next direction:** Residual noted factory-speech at plan-card evidence-limit vocabulary and verbatim mantra-echo paste. PERSISTENT (5th time). Founder halt: do not start 015 unless asked.

### iter-015 — founder-batch seed subtraction and job-ownership
**Hypothesis:** Cards cite evidence/echo IDs only, instruction freeze is headline-only, trap-question formula deleted, and later cards must not re-own a demolition under a new scene ID — so voice noted `factory-speech` and book-arc noted `re-argument` drop in both books.
**Change:** `prompts/chapter-writer.md`, `prompts/master-plan-skill-v2.md`, `prompts/master-plan-reviewer-v2.md`, `prompts/style-guide.md`. Plan regenerated (16 chapters). Research reused. Two books on Muse Spark Zen. Judges: composer-2.5.
**Verdict:** REVERT
**Lesson:** KEEP conjunction failed. Noted factory-speech 17→20 / 38→13 (A rose; B dropped — not both). Book-arc re-argument 5→6 / 4→5 (neither dropped). Blocking factory-speech reopened 0→1 / 0→3 (A chapter-job landing meta; B numbered I-line prefixes). `trap-question-label` closed 3/1→0/0. Belief/journey/book-arc PASS both. PERSISTENT factory-speech hydra at writer-prompt/plan (6th). Attribution would have been weak (batch).
**Next direction:** Do not re-run this seed-subtraction batch against the same census objects. Blocking reopened as instruction-serial and verdict-landing meta — different local forms, same class. Founder halt: do not start 016 unless asked.

### iter-016 — founder-batch trap-question keep + echo density
**Hypothesis:** Keep 015 trap-question formula deletion, keep+alter echo-ID-only with mantra density ≤2 IDs/card, and strip Carr extras (no “land one short verdict”, no historical-evidence operator) so trap-question closes 0/0 and noted factory-speech drops in both books vs 014.
**Change:** `prompts/chapter-writer.md`, `prompts/master-plan-skill-v2.md`, `prompts/master-plan-reviewer-v2.md`, `prompts/style-guide.md`. Plan regenerated (15 chapters). Research reused. Two books on Muse Spark Zen. Judges: composer-2.5.
**Verdict:** INCONCLUSIVE
**Lesson:** KEEP conjunction split. Trap-question 3→0 / 1→1 (not 0/0 both). Noted factory-speech 17→23 / 38→13 (A rose; B dropped). Blocking 0 / 1 (B-only M-F echo assembly — not 015 verdict-landing or instruction serials). Echo-density cap cut A ch14 noted 7→2 and closed B’s 015 vow-inventory hotspot; A’s aggregate rise is style-guide `The fact is` / research-pooling / chapter-job meta. Belief/journey/book-arc PASS both. Do not promote. Attribution would have been weak (batch).
**Next direction:** Do not KEEP this batch. Echo-density is a real one-book/local win, not a both-books KEEP. Residual noted factory-speech still hydra at style-guide operators. Founder halt: do not start 017 unless asked.

### iter-017 — trap-question isolation vs 014
**Hypothesis:** Delete only the pasteable trap-question formula (015 S1–S5 EXACT; W1 ask + strip `land one short verdict`) so `trap-question-label` closes 3/1 → 0/0 both vs 014, with plan reuse.
**Change:** `prompts/chapter-writer.md`, `prompts/style-guide.md`. Plan reused (014, 15 chapters). Research reused. Two books on Muse Spark Zen. Judges: composer-2.5.
**Verdict:** REVERT
**Lesson:** Isolation did not KEEP. Trap-question 3→0 / 1→1 (B `Ask the simplest Socratic trap`). Blocking factory-speech reopened 0→1 / 0→1 (A chapter-job landing meta; B style-guide posture spoken). Named 015 serials stayed closed; verdict-landing mutated. Noted factory-speech 17→18 / 38→10. Do not promote. PERSISTENT factory-speech hydra (7th).
**Next direction:** Do not replay trap-formula deletion as the KEEP object. Blocking class still mutates at writer/style-guide. Founder halt: do not start 018 unless asked.

### iter-018 — trap-question prefix ban vs 014
**Hypothesis:** One never-surface line (`no trap-question or Socratic-trap prefixes`) in `prompts/chapter-writer.md` closes voice noted `trap-question-label` 3/1 → 0/0 both vs 014, with plan reuse.
**Change:** `prompts/chapter-writer.md` (never-surface list, one clause). Plan reused (014, 15 chapters). Research reused. Two books on Muse Spark Zen. Judges: composer-2.5.
**Verdict:** INCONCLUSIVE
**Lesson:** Prefix ban closed trap-question 3→0 / 1→0 both. Founder veto missed: blocking factory-speech 0→2 A-only (evidence-register at ch09 climax, not 015/017 named kills). method-promise-hedge A-only (`almost automatically` Burgeon paste). Named 015/017 kills stayed closed. Do not promote. PERSISTENT factory-speech hydra (8th).
**Next direction:** Do not KEEP this line. The targeted prefix class closed; blocking factory-speech still mutates at evidence-register in one book. Founder halt: do not start 019 unless asked.

### founder-prep 2026-09-04 — Spark 1.3 live pins + judge probes
**Note:** Writer/planner live pins moved to Muse Spark 1.3 contributor (`muse-spark-1.3-contributor-free` / `meta/muse-spark-1.3-contributor`). Hypothesizer is Claude Fable 5.1 as a Cursor Task (`harness-subagent`); no Muse fallback.
**Smoke:** OpenCode Zen `muse-spark-1.3-contributor-free` POST `/zen/v1/responses` → HTTP 200, model echo `muse-spark-1.3-contributor-free`, text `SPARK13_OK` (3.2s). Vercel `meta/muse-spark-1.3-contributor` → HTTP 402 `insufficient_funds` (id accepted, gateway has no credits). Primary route is live; fallback needs Vercel top-up before a Zen outage.
**Probes:** `loop/preflight/runs-2026-09-04-composer-2.5-belief-journey-probe/` — b1/b2/j1 must-FAIL classes fired; b3/j2 PASS. b1 run1 vs run2: both FAIL with `credit-intact`, but run1 also blocked `sacrifice-standing` and `reader-does-not-work` (BLOCKING set not identical). 18-call 2026-08-24 battery not replayed.
**Next direction:** Founder authorized 019→040 on 2026-09-04. 019 is a Spark 1.3 BASELINE (research reuse, plan regenerate, two books), not a hypothesis. Do **not** bundle the chapter-writer word-budget sentence (unanswered → default no). Strikes reset. Hypothesizer idle until 020. Parked: chapter reviewer, anti-slop, parallel A/B. Hard stop only on Muse usage exhaustion (both routes) or North Star (D=0 both books) or 040 complete.

### iter-019 — Spark 1.3 BASELINE
**Hypothesis:** none — baseline after founder pin to Muse Spark 1.3; no factory change.
**Change:** none. Research reused. Plan regenerated (13 chapters). Two books on Spark 1.3 Zen (no Vercel fallback). Judges: composer-2.5. Factory files stay at KEEP 014.
**Verdict:** BASELINE
**Lesson:** Spark 1.3 on a fresh 13-chapter plan produces all-PASS / zero blocking in both books (belief 13/13, journey 13/13, voice 13/13, book-arc PASS). KEEP objects (blocking in both) are empty. Noted floors that appear in both: willpower-lexicon 21/33, factory-speech 6/21, journey re-argument 7/5, book-arc re-argument 3/2, belief re-argument 3/1, coach-register 6/3, wrong-register 5/2, copied-mannerism 2/7, pre-debut-spend 1/1. A-only noise: trap-question-label 3, journey-stall 1. Trace: late-arc plan-card re-argument (CH-10→13 re-owns settled jobs) and noted factory-speech hydra (PERSISTENT) are the 020 signal. 3-strike resets.
**Next direction:** Hypothesize from both-books noted classes. Priority: belief → arc/journey → voice. PRIMARY is the highest-priority class present in both (late-arc `re-argument` at plan-card, or noted `factory-speech` if the hypothesizer treats belief/journey/arc noted as below blocking). Anti-slop may ride secondary only if PRIMARY is factory-speech or a hedge class. Do not implement chapter reviewer or parallel A/B.

### iter-020 — continuity closed-list + fact-assertion
**Hypothesis:** PRIMARY: plan-skill continuity field binds settled jobs as token-echo only after the vow, so journey `re-argument` falls in both. Secondary: style-guide fact-assertion may not carry evidence-scope hedges.
**Change:** `prompts/master-plan-skill-v2.md` (continuity bullet); `prompts/style-guide.md` (§B5 operator 1). Plan regenerated (13 chapters). Research reused. Two books Spark 1.3 Zen. Judges composer-2.5.
**Verdict:** INCONCLUSIVE
**Lesson:** Journey `re-argument` 7→4 (A) and 5→5 (B) — one book only. Blocking stayed 0/0. Secondary factory-speech 6→6 / 21→4 also one-book. Card-field bind is sampling-sensitive on Spark 1.3. Do not promote. Same PRIMARY eligible with a new mechanism.
**Next direction:** New mechanism on journey/arc `re-argument` (plan-card) or re-read priority if hypothesizer picks a different both-books class. Do not replay this exact continuity bullet. Anti-slop still only if PRIMARY is factory-speech or hedge.

### iter-021 — writer previous-chapter closed-list
**Hypothesis:** PRIMARY: replace the previous-chapter clause so N cannot re-run, re-prove, or roll-call N−1, so journey `re-argument` falls in both vs 019.
**Change:** `prompts/chapter-writer.md` (previous-chapter clause only). Research reused. Plan reused (019, 13 chapters). Two books Spark 1.3 (A Zen contributor-free; B Go contributor). Judges composer-2.5.
**Verdict:** INCONCLUSIVE
**Lesson:** Journey `re-argument` 7→6 (A) and 5→7 (B) — one book only; B rose. Blocking 0/0. Belief/arc re-argument also rose. Assembled runtime prompt still ends with the old "handoff seam" assignment from `write_replicate.py`. Do not promote. Same PRIMARY eligible with a new mechanism (assembled contract or plan-card), not this exact clause.
**Next direction:** Do not replay this previous-chapter paragraph. If PRIMARY stays journey re-argument, change a different component (assembled writer assignment, or plan-card job overlap). Anti-slop still only if PRIMARY is factory-speech or hedge.

### iter-022 — Binding craft 3 one-sentence handoff
**Hypothesis:** PRIMARY: Binding craft 3 licenses one-sentence invoke of settled work as the whole handoff seam, so journey `re-argument` falls in both vs 019.
**Change:** `prompts/chapter-writer.md` (Binding craft 3 only). Research reused. Plan reused (019, 13 chapters). Two books Spark 1.3 Go contributor. Judges composer-2.5.
**Verdict:** INCONCLUSIVE
**Lesson:** Journey `re-argument` 7→6 (A) and 5→7 (B) — one book only; B rose. Blocking 0/0. Plan-card CH-10/11 and late-arc overlaps survived. Do not promote. Writer-prompt + re-argument strike 2 under Spark 1.3 census.
**Next direction:** Do not replay Binding craft 3 or the 021 previous-chapter clause. If PRIMARY stays journey re-argument, prefer plan-card (different component) — one more writer-prompt miss is a 3-strike PIVOT. Anti-slop still only if PRIMARY is factory-speech or hedge.

### iter-023 — one-correction-one-card plan law
**Hypothesis:** PRIMARY: plan-skill one-correction-one-card so later cards cannot re-open a demolished door, so journey `re-argument` falls in both vs 019. Secondary: reviewer gate.
**Change:** `prompts/master-plan-skill-v2.md` (Arc/belief-now); `prompts/master-plan-reviewer-v2.md` (cumulative walk). Plan regenerated (15 chapters). Research reused. Two books Spark 1.3 Go. Judges composer-2.5.
**Verdict:** INCONCLUSIVE
**Lesson:** Journey `re-argument` 7→6 (A) and 5→5 (B) — one book only. Named CH-10/11 tomorrow pair closed both. Blocking factory-speech A-only; journey-incomplete B-only. Do not promote. Plan-card + re-argument still open.
**Next direction:** Do not replay this one-correction wording. If PRIMARY stays journey re-argument, new plan-card mechanism (evidence double-routing / token triple-ownership per 023 trace). Consecutive no-KEEP: 4. Anti-slop still only if PRIMARY is factory-speech or hedge.

### iter-024 — room-name-only structural responsibility
**Hypothesis:** PRIMARY: plan-skill Compact chapter cards `structural responsibility` is a room name only, so journey `re-argument` falls in both vs 019. Secondary: one ledger row per card; reviewer blocks repeated IDs and slot-list structure.
**Change:** `prompts/master-plan-skill-v2.md` (structural responsibility + evidence routing); `prompts/master-plan-reviewer-v2.md` (writer-facing blockers). Plan regenerated (16 chapters). Research reused. Two books Spark 1.3 Go. Judges composer-2.5. Panel 49+49.
**Verdict:** REVERT
**Lesson:** Journey `re-argument` 7→7 (A) and 5→5 (B) — neither book. Blocking 0 A; B-only voice hedges + factory-speech. Room-name field applied; C-14 guardrails/AN-03/continuity still assigned the post-vow second manual. Evidence IDs were single-use; re-argument is adjacent-job + late-arc scene/guardrail overlap. Do not promote. Plan-card + re-argument 3-strike (020, 023, 024) — PIVOT off plan-skill card-field binds.
**Next direction:** Do not replay room-name-only, 020 continuity, 021 previous-chapter, 022 craft 3, or 023 one-correction. PIVOT off plan-skill Compact-cards field swaps. Consecutive no-KEEP: 5 (`convergence-report.md`). Founder override: continue. Anti-slop still only if PRIMARY is factory-speech or hedge.

### founder-halt 2026-09-04 — instrument stop after 020–024
**Hypothesis:** none — founder halted the 019→040 drive after five no-KEEP. Not a factory iteration.
**Change:** Judge `re-argument` (journey / belief / book-arc) now fires only on a rebuilt section (argument + evidence + turn); token/mantra/one-paragraph Carr echoes count 0. `_shared.md` + PROGRAM Step 6: material KEEP = beyond the book-level noted band, rate-normalized (same-n drop of 1 is REVERT, not INCONCLUSIVE). Hypothesizer: PRIMARY must be blocking or a noted class ≥ 8 in both books; voice noted-only may be PRIMARY when belief/journey/arc have no blocking. Late-Carr PASS test added (`pass-test-reader-journey-late.md`, belief equivalent).
**Verdict:** HALTED (instrument). Late-Carr Preflight PASS ×4, `re-argument` 0. Do not start 025 until a fresh 13-chapter BASELINE is recorded.
**Lesson:** 020–023 were correctly INCONCLUSIVE under the old "any −1" reading of Step 6; read materially, 021–023 were REVERT and only 020 A (7→4) moved. KEEP object was journey `re-argument` at 5–7, inside the judges' ±1/chapter band, never calibrated on a late Carr chapter with its previous chapter. B never fell below 5. 023/024 compared raw counts on 15/16 chapters to a 13-chapter baseline. Voice floors that did move (024 willpower-lexicon 21→16 / 33→17, factory-speech 6→3 / 21→6) were locked out as PRIMARY.
**Next direction:** Finish late-Carr Preflight (journey + belief, ×2). If `re-argument` > 0 on Carr, tighten the class again. Then BASELINE with factory files at KEEP 014, 019 13-chapter plan reused, new noted floors, 3-strike clock reset. No 025 plan-skill or writer sentence. No model swap.

### founder-resume 2026-09-04 night — Carr comparison + reviewer + anti-slop
**Hypothesis:** none yet — founder un-parked chapter reviewer and anti-slop, asked Fable for a Carr-convergence plan.
**Change:** Fable plan implemented: chapter-reviewer (write→review→≤1 rewrite, length ±15%); chapter-comparison judge (GSBS belief-moves PRESENT/PARTIAL/MISSING, lecture lines); KEEP adds 80% plan-word floor and may use comparison `missing` ≥2 drop; hypothesizer PRIMARY order blocking → comparison missing → noted ≥8. Anti-slop scheduled 026–028 after 025 BASELINE.
**Verdict:** RESUME (architecture). 025 is BASELINE with reviewer on, 019 13-chapter plan reused, two books, full panel + comparison.
**Lesson:** 019 A is 26,984 words vs 60,000 planned. Length was invisible to KEEP. Census KEEP on `re-argument` 5–7 could not converge toward a Carr-length book.
**Next direction:** Smoke CH-06 reviewer + comparison PASS tests, then 025 BASELINE. Do not replay 020–024 wording. Anti-slop only after 025 floors exist.

### iter-025 — Carr-convergence architecture BASELINE
**Hypothesis:** none — baseline after chapter-reviewer + comparison lane + length KEEP floor. No factory wording change.
**Change:** none in writer/planner/style-guide. Research reused. Plan reused (019, 13 chapters). Two books Spark 1.3 Go with write→review→≤1 rewrite. Judges: composer-2.5, four chapter lanes + book-arc (53+53).
**Verdict:** BASELINE
**Lesson:** Reviewer made length KEEP-visible: A 52182 / B 51144 vs 019 A 26984 (floor 48000 met both). All-PASS / zero blocking both books. New floors in both: comparison `missing` 3/3 (G06-M2, G15-M1, G20-M2), journey `re-argument` 12/10 (repaired class, still ≥8), willpower-lexicon 29/33, factory-speech 18/16. `coach-register` 3/8 (not ≥8 both). `method-promise-hedge` 0/0. 3-strike resets.
**Next direction:** 026 anti-slop (chatbot openers / throat-clearing / summary closers / stacked-triplet padding) with PRIMARY `factory-speech` 18/16. Skip 027 (`coach-register` not ≥8 both). Skip 028 (hedge classes absent). Then comparison `missing` in both. Do not replay 020–024 wording.

### iter-026 — anti-slop chatbot residue
**Hypothesis:** PRIMARY: style-guide §B5 chatbot-residue operator so voice `factory-speech` falls in both vs 025 (18/16).
**Change:** `prompts/style-guide.md` (§B5 operator 12 + §B9 checklist). Plan reused (019, 13 chapters). Research reused. Two books Spark 1.3 Go with reviewer. Judges composer-2.5, 53+53.
**Verdict:** KEEP
**Lesson:** factory-speech 18→13 / 16→8 (drop ≥2 both). Length floor met (50404/49067). Blocking 0/0. No new both-books class. Prediction partial (025 leaks were ease-operators/card titles; count still fell). Comparison `missing` 3→4 both (G04-M1 joined G06-M2/G15-M1/G20-M2). Skip further anti-slop (coach-register 8/6; hedges 0/0).
**Next direction:** 027 PRIMARY comparison `missing` 4/4 (G04-M1, G06-M2, G15-M1, G20-M2). Do not replay 020–024 wording. Do not put GSBS in writer/planner/reviewer.

### iter-027 — unpaid belief-moves on four Jobs
**Hypothesis:** PRIMARY: Job tails on CH-03/08/09/13 so comparison `missing` falls in both vs 026 (4/4).
**Change:** `production-books/quit-sugar/master-plan.md` (four Job clauses). Plan reused otherwise. Two books Spark 1.3 Go with reviewer. Judges composer-2.5, 53+53.
**Verdict:** KEEP
**Lesson:** comparison `missing` 4→1 / 4→0. Targeted G06-M2, G15-M1, G20-M2 PRESENT; G04-M1 PARTIAL (A). Residual A miss is G06-M1 (untargeted). Length 52861/51952. Blocking 0/0. factory-speech 13/16 (B rose). Next PRIMARY is voice noted ≥8 both (willpower-lexicon 28/36 or factory-speech 13/16).
**Next direction:** 028 from 027 both-books floors. Comparison `missing` is no longer in both (1/0). Do not replay 020–024 wording.

### iter-028 — card-header / workshop-staging factory-speech
**Hypothesis:** PRIMARY: style-guide §B5 operator 11 ban on card-header paste, workshop staging, seed/later placeholders, and numbered plan-index with no spoken body, so voice `factory-speech` falls in both vs 027 (13/16).
**Change:** `prompts/style-guide.md` (§B5 operator 11 + §B9). Plan reused (027 Jobs). Two books Spark 1.3 Go with reviewer. Judges composer-2.5, 53+53.
**Verdict:** INCONCLUSIVE
**Lesson:** factory-speech 13→18 (A) and 16→10 (B) — one book only. Length 52626/52802. Blocking 0/0. §B10 still requires `IN THIS CHAPTER` on every chapter; both books emitted it. A rose on ch13 formula-repetition (7) plus numbered-instruction leaks, not the 027 workshop/seed-later strings (those did not recur). Do not promote.
**Next direction:** New mechanism on factory-speech (B10 anatomy vs operator 11). Do not replay this operator-11 sentence. PRIMARY remains 027 floors (13/16). willpower-lexicon stays non-PRIMARY (attack-the-illusion). Do not replay 020–024 wording.

### iter-029 — B10 opening-pictures instead of IN THIS CHAPTER
**Hypothesis:** PRIMARY: style-guide §B10 anatomy item 1 no longer requires the workshop header `IN THIS CHAPTER`, so voice `factory-speech` falls in both vs 027 (13/16).
**Change:** `prompts/style-guide.md` (§B10 chapter anatomy item 1). Plan reused (027 Jobs). Two books Spark 1.3 Go with reviewer. Judges composer-2.5, 53+53.
**Verdict:** INCONCLUSIVE
**Lesson:** factory-speech 13→9 (A, including 1 blocking) and 16→18 (B) — one book only. Length 48477/51991. Both books still opened every chapter with `IN THIS CHAPTER`. A ch09 FAIL is a numbered instruction paste at mantra echo, not the preview header. Do not promote. Style-guide + factory-speech strike 2.
**Next direction:** Do not replay 028 operator 11 or 029 B10 item 1. Next factory-speech mechanism must change a different component (reviewer or writer), not another style-guide header sentence. PRIMARY remains 027 floors 13/16. Do not replay 020–024 wording.

### iter-030 — reviewer HEADER finding
**Hypothesis:** PRIMARY: chapter-reviewer `HEADER` finding so voice `factory-speech` falls in both vs 027 (13/16).
**Change:** `prompts/chapter-reviewer.md` (`HEADER` finding + ACCEPT gate). Plan reused (027 Jobs). Two books Spark 1.3 Go with reviewer. Judges composer-2.5, 53+53.
**Verdict:** KEEP
**Lesson:** factory-speech 13→9 / 16→7 (drop ≥2 both). Length 51753/51097. Blocking 0/0. Reviewer fired HEADER widely; one rewrite often kept `IN THIS CHAPTER` (grep 13/12). Census class still fell. Comparison `missing` 0/0. New floors: factory-speech no longer ≥8 both (9/7). willpower-lexicon 30/30 is not PRIMARY.
**Next direction:** No KEEP-eligible PRIMARY except willpower-lexicon (forbidden). Do not replay 028/029 style-guide sentences or this HEADER finding. Do not replay 020–024 wording. Do not start a willpower-lexicon PRIMARY.

### iter-031 — unpaid comparison halves + CH-13 budget
**Hypothesis:** PRIMARY: plan-card Job tails on CH-05/06/09/10 plus CH-13 budget 3800→1700 so comparison `partial` falls in both vs 030 (9/11).
**Change:** `production-books/quit-sugar/master-plan.md` (four Job tails, CH-05/09/13 budgets, CH-01 Job ride). Two books Spark 1.3 Go with reviewer. Judges composer-2.5, 53+53.
**Verdict:** KEEP
**Lesson:** comparison `partial` 9→5 / 11→5 (drop ≥2 both). Length 52392/51940. Blocking 0/0. Underpaid halves G05-M1, G13-M2, G15-M2, G14-M2 closed both. G20-M3 stayed PARTIAL both (CH-13 1584/1462 still rebuilt sweetness/life-choice). factory-speech rose 9→14 / 7→10 (noted, not a veto).
**Next direction:** PRIMARY factory-speech 14/10 (noted ≥8 both). Do not replay 028/029 style-guide header sentences or 030 HEADER. Do not replay 020–024 wording. willpower-lexicon stays non-PRIMARY. comparison `partial` 5/5 is below the ≥8 band.

### iter-032 — writer anatomy drop IN THIS CHAPTER
**Hypothesis:** PRIMARY: delete required `IN THIS CHAPTER` from writer anatomy and replace bare list-number instructions with a spoken number-in-words lead-in so voice `factory-speech` falls in both vs 031 (14/10).
**Change:** `prompts/chapter-writer.md` (anatomy items 2–5 + Method-and-voice). Plan reused (031 Jobs). Two books Spark 1.3 Go with reviewer. Judges composer-2.5, 53+53.
**Verdict:** REVERT
**Lesson:** factory-speech 14→22 / 10→13 (both rose). Length 51349/50428. Blocking 0/0. Header grep 0/0 — the string died; the replacement lead-in (`So here is my sixth instruction:`) scored as factory-speech in both. A also rose on `Hear the verdict and let it stand:` formula. Writer restored to 031 KEEP text.
**Next direction:** PRIMARY remains 031 floors factory-speech 14/10. Do not replay this writer-anatomy change. Do not replay 028/029/030 header mechanisms. Do not replay 020–024 wording. Architecture pivot (reviewer-until-ACCEPT + dual subject) is a founder gate — do not start 033 on the old two-sugar protocol.

### iter-033 — dual-subject BASELINE (A1 + K1)
**Hypothesis:** None — first dual-subject BASELINE after A1 reviewer loop and K1 (quit-sugar + quit-smoking).
**Change:** None. Factory files at 031 KEEP. Sugar plan reused. Smoking plan accepted. Writer A1 K=3. Judges composer-2.5, 53+57.
**Verdict:** BASELINE
**Lesson:** All-PASS, blocking 0 both. Words 53208 / 54277. Floors in both: factory-speech 20/18, willpower-lexicon 40/31 (not PRIMARY), journey re-argument 16/8. Comparison missing 0/2 and partial 2/9 are not ≥8 both. PASS probe factory-token FAIL was setup; Carr-native Ch6 journey PASS.
**Next direction:** PRIMARY factory-speech 20/18. Journey re-argument 16/8 secondary. Do not replay 020–024 / 028 / 029 / 030 HEADER / 032 writer anatomy. Do not start a willpower-lexicon PRIMARY.

### iter-034 — §B4 Freedom-register ease-operators
**Hypothesis:** PRIMARY: replace style-guide §B4 Freedom-register token list so Spark cannot satisfy the crescendo with ease-operator tags, so voice `factory-speech` falls in both vs 033 (20/18).
**Change:** `prompts/style-guide.md` (§B4 Freedom-register bullet). Plan reused both subjects. Writer Spark 1.3 Go, A1 K=3. Judges composer-2.5, 53+57.
**Verdict:** KEEP
**Lesson:** factory-speech 20→6 / 18→12. Ease-operator grep 0/0 both and census fell with it. Length 53366/56466. Sugar blocking 0; smoking CH-01 voice FAIL method-promise-hedge 1 (one-book, not a veto). Comparison partial 2→4 / 9→11 (noted). New floors: factory-speech no longer ≥8 both (6/12).
**Next direction:** factory-speech residual is smoking-worse (12); sugar 6 is below band. willpower-lexicon 26/28 is not PRIMARY. Do not replay 028/029/030/032. Do not replay 020–024. Do not start a willpower-lexicon PRIMARY.

### iter-035 — §B5 permission paradox spine-owned
**Hypothesis:** PRIMARY scope quit-smoking: replace style-guide §B5 operator 9 so standing permission is spine-owned, not a per-chapter tag, so smoking factory-speech 12→≤8. Sugar 6 is non-regression (≤7).
**Change:** `prompts/style-guide.md` (§B5 operator 9). Plan reused both. Writer Spark 1.3 Go, A1 K=3. Judges composer-2.5, 53+57.
**Verdict:** QUANTIFY
**Lesson:** smoking factory-speech 12→3 (PRIMARY hit). Sugar 6→8 (non-regression miss). Length 55356/56649. Blocking 0 both. Restored: no. A1 sugar 9 ACCEPT / 4 CAP; smoking 11 ACCEPT / 3 CAP.
**Next direction:** §B5 op 9 stays. Journey re-argument 15/16 is ≥8 both (KEEP-eligible). factory-speech 8/3 is not ≥8 both. willpower-lexicon 33/21 not PRIMARY. Do not replay 028–032 / 020–024.

### iter-036 — reviewer RE-ARGUMENT backward fence
**Hypothesis:** PRIMARY: chapter-reviewer `RE-ARGUMENT` finding so journey `re-argument` falls in both vs 035 (15/16).
**Change:** `prompts/chapter-reviewer.md` (`RE-ARGUMENT` after `RESERVED-REACH` + ACCEPT gate). Runner parse includes `RE-ARGUMENT`. Plans reused. Writer Spark 1.3 Go, A1 K=3. Judges composer-2.5, 53+57. Hypothesizer: Fable 5.1.
**Verdict:** KEEP
**Lesson:** journey re-argument 15→8 / 16→9 (drop ≥2 both). Length 53680/54213. Blocking 0 both. Residual 8/9 still ≥8 both. factory-speech 8→9 / 3→2. willpower-lexicon 28/31 not PRIMARY.
**Next direction:** PRIMARY remains journey re-argument 8/9. New mechanism on a different component or a sharper reviewer cut — do not replay this finding text. Do not replay 020–024 / 028–032. Do not start a willpower-lexicon PRIMARY.

### iter-037 — LENGTHEN expansion assignment
**Hypothesis:** PRIMARY: chapter-reviewer LENGTHEN must name an unspent expansion target (unfinished encounter / unanswered objection / undeveloped consequence), so journey `re-argument` falls in both vs 036 (8/9).
**Change:** `prompts/chapter-reviewer.md` (Rules / LENGTHEN expansion assignment). 036 `RE-ARGUMENT` and ACCEPT gate unchanged. Plans reused. Writer Spark 1.3 Go, A1 K=3. Judges composer-2.5, 53+57. Hypothesizer: GPT-6 Astra.
**Verdict:** KEEP
**Lesson:** journey re-argument 8→6 / 9→5 (drop ≥2 both). Length 54612/57583. Sugar voice FAIL CH-01 method-promise-hedge 1 (one-book, not a veto); smoking blocking 0. Residual 6/5 is below ≥8 both. factory-speech 9→10 / 2→5. willpower-lexicon 26/19 not PRIMARY.
**Next direction:** Empty KEEP-eligible intersection (willpower locked). PRIMARY is the top class of the worse subject: sugar factory-speech 10; smoking 5 is non-regression. Do not replay this LENGTHEN assignment, 036 RE-ARGUMENT, 020–024, or 028–032. Do not start a willpower-lexicon PRIMARY.

### iter-038 — OVERCLAIM repair
**Hypothesis:** PRIMARY scope quit-sugar: chapter-reviewer `OVERCLAIM` must delete or narrow the unsupported claim instead of transplanting the evidence bound into prose, so sugar factory-speech 10→≤8. Smoking 5 is non-regression (≤6).
**Change:** `prompts/chapter-reviewer.md` (`OVERCLAIM` repair instruction). Plans reused. Writer Spark 1.3 Go, A1 K=3. Judges composer-2.5, 53+57. Hypothesizer: GPT-6 Astra.
**Verdict:** QUANTIFY
**Lesson:** sugar factory-speech blocking+noted 10→10 (noted 10→9 + blocking 1). Smoking non-regression 5→8 (noted 5→7 + blocking 1). Length 55336/56793. New blocking factory-speech both (sugar CH-09 numbered mantra echo; smoking CH-03 numbered instruction header). `OVERCLAIM` fired once (smoking CH-12). Restored: yes. Consecutive no-KEEP: 1.
**Next direction:** PRIMARY is blocking factory-speech 1/1 both (KEEP-eligible intersection). Numbered instruction/mantra headers. Do not replay this OVERCLAIM repair. Do not replay 037 LENGTHEN / 036 RE-ARGUMENT / 020–024 / 028–032. willpower-lexicon 30/31 is not PRIMARY.

### iter-039 — HEADER ownership test
**Hypothesis:** PRIMARY both subjects: replace the reviewer HEADER exemption (“numbered ALL-CAPS + one rationale line is not HEADER”) with an ownership-and-earned-landing test, so factory-speech 10→≤8 / 8→≤6 and blocking 1→0 each vs 038. Also report vs 037 10/5.
**Change:** `prompts/chapter-reviewer.md` (HEADER bullet). Plans reused. Writer Spark 1.3 Go, A1 K=3. Judges composer-2.5, 53+57. Hypothesizer: GPT-6 Astra.
**Verdict:** QUANTIFY
**Lesson:** factory-speech blocking+noted 10→13 / 8→10 (vs 038; vs 037 10→13 / 5→10). Length 55404/55597. Sugar blocking 0 (CH-09 numbered mantra now noted willpower). Smoking CH-03 still blocking factory-speech + instruction-paperwork on the same numbered instruction. HEADER fired on `IN THIS CHAPTER` openings. Restored: yes — PRIMARY worsened ≥ band both. Consecutive no-KEEP: 2.
**Next direction:** factory-speech noted 13/8 is ≥8 both. Do not replay this HEADER ownership test. Do not replay 038 OVERCLAIM / 037 LENGTHEN / 036 RE-ARGUMENT / 020–024 / 028–032. willpower-lexicon 32/20 is not PRIMARY.

### iter-040 — writer instruction landing
**Hypothesis:** PRIMARY both subjects: rewrite writer anatomy item 5 so the numbered ALL-CAPS imperative completes the preceding concrete decision, so factory-speech 13→≤11 / 10→≤8 vs 039. Also report vs 037 10/5.
**Change:** `prompts/chapter-writer.md` (Full-length chapter anatomy item 5). Plans reused. Writer Spark 1.3 Go, A1 K=3. Judges composer-2.5, 53+57. Hypothesizer: GPT-6 Astra.
**Verdict:** QUANTIFY
**Lesson:** factory-speech blocking+noted 13→25 / 10→19 (vs 039; vs 037 10→25 / 5→19). Length 53858/57512. Blocking 0→1 / 2→12. Writer prefixed assigned commands with plan IDs (`I-01 — KEEP AN OPEN MIND`). Restored: yes — PRIMARY worsened ≥ band both. Consecutive no-KEEP: 3. Halt at 040.
**Next direction:** Halt. Do not invent 041. Do not replay this writer anatomy item 5, 039 HEADER ownership, 038 OVERCLAIM, 037 LENGTHEN, 036 RE-ARGUMENT, 020–024, or 028–032. willpower-lexicon 32/21 is not PRIMARY.

### iter-040-instrument — Carr ALL-CAPS is not factory-speech
**Hypothesis:** The voice judge was the defect. Numbered ALL-CAPS assigned commands are Carr method, not factory-speech.
**Change:** `loop/judges/voice-emotion.md` (factory-speech + instruction-paperwork). Writer: no `I-01 —`, no `IN THIS CHAPTER`. Reviewer HEADER: `I-NN —` is HEADER. Hypothesizer: do not PRIMARY-ban ALL-CAPS. 038 OVERCLAIM re-applied. 039 HEADER and 040 item 5 stay dropped.
**Verdict:** founder instrument fix (not a dual-subject KEEP)
**Lesson:** 038–040 restorations used a class that included Carr's instruction typography. Blocking quotes were `3. BEGIN BY FEELING GREAT TO BE ESCAPING` and `10. IGNORE ANYONE WHO QUIT BY WILLPOWER`. 040 `I-01 —` prefixes remain real factory-speech under the corrected judge.
**Next direction:** Do not start 041 unless the founder asks. PRIMARY on the corrected instrument is remaining inventory diction, not ALL-CAPS commands.

### campaign-001 close-out — Carr-distance instrument (2026-09-06)
**Hypothesis:** none — founder-guided instrument-and-rules change from the Astra + Fable consult. Not a dual-subject KEEP.
**Change:** judges (factory-speech = inventory only, including Carr `IN THIS CHAPTER` and numbered ALL-CAPS = 0; drop noted willpower-lexicon and copied-mannerism; demote `re-argument` from PRIMARY; `literary-stylization`; Carr-distance 0–100 judge; KEEP band ≥25% and ≥4; 3-strike by class; empty intersection → stop; GSBS control; CAP ≠ ACCEPT; chapter-reviewer editable; CH-01 flat promise; style-guide plain Carr + runtime Carr DEFAULT lock; Reddit in scope; miners write parent; plan-writer/plan-reviewer read banks in full). Git: only `campaign-001` and `main`. Handoff: `loop/CONTINUE.md`.
**Verdict:** founder instrument fix
**Lesson:** 037 is ~42% indistinguishable from Carr and ~60–73% Easyway-engine-present. The census was near-perfect because the remaining distance (CH-01 hedge, fragment prose, private vocabulary, clinician disclaimers) was off-instrument. 038–040 spent three paid dual runs on a class that included Carr's instruction typography. KEEP of 2 was inside declared noise. Research quality was capped by a 25 kB synthesis funnel and a Reddit exclusion that contradicted the North Star. CAP silently accepted K=3 unreviewed rewrites. Bank truncation at 100 kB would have reopened that funnel — it is removed. Extra `iter-*` / `cursor/*` branches were leftover worktrees, not campaign truth.
**Next direction:** Next session starts at `loop/CONTINUE.md`. 041 = dual BASELINE: rejudge frozen 037 under this instrument, no factory wording. First hypothesis after that: CH-01 + Part B already in the files, scored on Carr-distance and comparison `partial`. Empty PRIMARY intersection → stop. Do not replay 039/040. 038 OVERCLAIM stays.






### iter-041 — dual BASELINE on the Carr-distance instrument
**Hypothesis:** none — rejudge frozen 037 under the 2026-09-06 panel with Muse Spark 1.3 judges (recalibrated 2026-09-07).
**Change:** none. 037 chapters + plans copied identically. New judge runner `scripts/loop-runner/judge_replicate_spark.py` (opencode-run spawns; Cursor composer-2.5 script unusable on this harness).
**Verdict:** BASELINE
**Lesson:** All-PASS / zero blocking both books on Muse judges too (54 + 58 reports, no retries). New floors: factory-speech 6/9, literary-stylization 5/1, comparison partial 3/4 (+missing 2 smoking-only), book-arc re-argument 1/1, Carr-distance 60/72 (deficits 40/28). No noted class ≥12 both — empty census intersection. The Carr-distance reasons name the real gap (appendix-banished scare, sensory catalogue, clinician disclaimers, private vocab, fragment chains, soft-contract promise) — all already addressed by the unmeasured CH-01 rule + Part B in the files.
**Next direction:** 042 regenerates plans + chapters so CH-01 + Part B fire; PRIMARY Carr-distance deficit, secondary comparison partial. Research reuse. Do not PRIMARY factory-speech / willpower / re-argument. Do not replay 039/040.

### iter-042 — clinician-disclaimer subtraction
**Hypothesis:** PRIMARY Carr-distance deficit: delete the writer's "one spoken clause" license + unroute advisory to two cards + remove style-guide duplicate, so deficit falls both (40→≤32 / 28→≤22).
**Change:** `prompts/chapter-writer.md` (evidence-honesty bullet); `prompts/master-plan-skill-v2.md` (two-card rule + duplicate deletion); `prompts/style-guide.md` (§B10 relief). Both plans regenerated (sugar 13, smoking 15). Research reused. Writer Spark Go. Judges Muse Spark.
**Verdict:** QUANTIFY
**Lesson:** Mechanism verified, verdict split. Clinician Reason 3 gone both reports; grep 12/13→1/13 and 9/14→0/15; factory-speech 6→0 / 9→1. Sugar deficit 40→24 (KEEP-direction); smoking 28→32 (noise — opposite move on identical change, no shared trace mechanism; catalogue/header residuals the hypothesis didn't touch). Sugar comparison missing 0→6 / partial 3→8 is plan-level: regenerated cards don't assign G08/G12/G06/G15 jobs (PERSISTENT plan). No restore (no both-blocking, no both-worsen, floors 92/95.5%).
**Next direction:** 043 PRIMARY from eligible intersection (deficit, comparison missing 6/2, partial 8/4). Do not chase smoking +4. Do not replay 039/040. Comparison repair needs owning-encounter mechanism, not field swaps.

### iter-043 — planner coverage law
**Hypothesis:** PRIMARY comparison missing: J-coverage law (every lived justification owned by one card) + reviewer coverage block, so missing falls both (6→≤4 / 2→0). Hypothesizer Muse Spark (Astra quota, Fable 429, agent CLI now Grok TUI — confound recorded).
**Change:** `prompts/master-plan-skill-v2.md` (coverage law); `prompts/master-plan-reviewer-v2.md` (coverage block). Both plans regenerated (15 ch each). Research reused. One SIGUSR2 factory kill per subject mid-run; retried + resumed from markers; both FACTORY DONE.
**Verdict:** QUANTIFY
**Lesson:** Law obeyed on the wrong ontology. Planner owned J-justifications once each (reviewer PASS) while GSBS moves stayed unassigned; re-cut added new unowned slots (G01-M3, G04-M1 re-demand, G16, G20 gate) and double-counted G15-M1. Missing 6→11 / 2→1; mechanism REJECTED. PERSISTENT plan (8+). Partials are thin one-prong owners. Deficit fell both anyway (24→18 / 32→22) as a side-channel: distinct encounters enforce in-argument Carr architecture. Comparison chase has now worsened sugar missing twice (0→6→11) across two regens. No restore (no both-blocking/worsen; floors 90/97%).
**Next direction:** PRIMARY the deficit residuals (private vocab, catalogue/chains, clinician hedges) or a GSBS-prong-as-evidence repair — never another assignment law, factory-speech, willpower, or re-argument. Do not replay 039/040.

### iter-044 — awe grounding + prong evidence (RESTORED)
**Hypothesis:** PRIMARY deficit: ground §6 awe in one encounter sentence + route every prong's ledger row onto owning cards, so deficit falls both (18→≤13 / 22→≤16).
**Change:** `prompts/style-guide.md` (§6 awe); `prompts/master-plan-skill-v2.md` (card evidence bullet). Both plans regenerated (sugar 18 cards, smoking 15). Sugar plan-loop wedge: accepted plan recovered from traces, synced to production before judging.
**Verdict:** QUANTIFY with restore — PRIMARY worsened ≥ band BOTH (18→32 / 22→30).
**Lesson:** Both mechanisms failed as built. Awe rewrite never fired (cards override with staging inventory; only smoking C-07 carried the field; reviewer style-blind). Change 2 backfired as its own shared mechanism: routing every prong's limits made the writer narrate them as clinician-grade caveats in both books. New diagnosis: style-guide anatomy (IN THIS CHAPTER / SUMMARY / roll-calls) is the shared floor the factory orders and the judge penalizes. Partials persist (guardrails cap second prong; some prongs unroutable). Factory files + production plans restored to 041 text. RESTORE is not a ban — 042 ban, 043 law stay eligible; route-every-limit must never return in 044 form.
**Next direction:** 045 PRIMARY deficit 32/30 from the anatomy floor and/or hedge-transplant guard. Never card-field edits (plan-card 3-strike), factory-speech, willpower, re-argument. Do not replay 039/040 or route-every-limit.

### iter-045 — anatomy reshape + clinician-ban reprise
**Hypothesis:** PRIMARY deficit: reshape recap furniture toward Carr form (Change 1) + re-apply verified 042 clinician ban (Changes 2-3, carried line post-restore), so deficit falls both (32→≤24 / 30→≤22).
**Change:** `prompts/style-guide.md` (§B10 recap reshape); `prompts/chapter-writer.md` (evidence-honesty silence); `prompts/style-guide.md` (Hard-facts relief). Sugar plan regenerated (15 cards; traces/production wedge again — accepted plan recovered from traces). Smoking plan reused (037). Research reused.
**Verdict:** QUANTIFY
**Lesson:** Deficit 32→30 / 30→26 — right direction, inside noise, band missed both. Change 1 half-fired (rooms-form complied; presence still quoted; voice-vs-distance asymmetry on identical strings; deletion forbidden by GSBS control → presence is instrument property, stop chasing it). SUMMARY cap dropped at writer contract (fired ~2/3 both; reviewer never trims; unscored by all lanes). Clinician ban disobeyed once (sugar CH-15 speaks, vow CH-14 silent — model local). Smoking moved on reused plan (variance, not file effect). Cleanest new signal: private creature vocab both (Mite/Talker, Nipper/Smokescreen) minted by plan sheets under style-guide Fork-1 DEFAULT — but renaming to Carr's pair collides with original-text-only doctrine (founder tension, flagged). Floors 90/~97%. No restore (improved both, no both-blocking).
**Next direction:** 046 PRIMARY: private-vocab discipline (resolve originality tension, no silent Carr wording) or writer-contract SUMMARY cap + reviewer finding. Never card-field edits, route-every-limit, factory-speech, willpower, re-argument. Consecutive no-KEEP: 4.

### iter-046 — vocab discipline + SUMMARY cap
**Hypothesis:** PRIMARY deficit: Fork-1 no frozen brands (plain common nouns) + writer SUMMARY ≤3 belief-verb bullets + reviewer SUMMARY finding, so deficit falls both (30→≤22 / 26→≤19).
**Change:** `prompts/style-guide.md` (Fork-1); `prompts/chapter-writer.md` (anatomy 6); `prompts/chapter-reviewer.md` (SUMMARY finding + gate). Sugar plan regenerated (13 cards; wedge a third time — recovered from traces). Smoking reused (037). Research reused.
**Verdict:** QUANTIFY
**Lesson:** Change 1 fired both (0 brand hits; common-noun rendering; brand-penalized moves PRESENT). Changes 2-3 fired (SUMMARY 13/13 + 14/14, findings enforced). Sugar hit band (30→20). Smoking +2 noise on reused plan (unassigned 037 moves, new re-argument counts, Latinate crescendo). Tight-shoes misfire CONFIRMED (reference ch06:31, ch37:59/61) — calibration note for founder, no loop action. Headers = instrument property (stop chasing). Register gap precisely located: §B5 never bans Latinate; reviewer has no register finding. Floors 92/~97%. No restore. Consecutive no-KEEP: 5 → convergence report written, founder override continues.
**Next direction:** 047 PRIMARY: REGISTER rule (Latinate ban + reviewer finding) and/or smoking plan vintage. Never card-field edits, route-every-limit, factory-speech, willpower, re-argument, headers, tight-shoes.

### iter-047 — REGISTER rule (RESTORED)
**Hypothesis:** PRIMARY deficit: ban Latinate crescendos (build Anglo-Saxon blunt verdicts) + reviewer REGISTER finding, so deficit falls both (20→≤15 / 28→≤21).
**Change:** `prompts/style-guide.md` (Plain Carr Latinate ban); `prompts/chapter-reviewer.md` (REGISTER finding + gate). Both plans regenerated (sugar 13, smoking 15). Research reused.
**Verdict:** QUANTIFY with restore — PRIMARY worsened ≥ band BOTH (20→35 / 28→35).
**Lesson:** Mechanism caused shared harm. Latinate→zero but fragments replaced it as avoidance (R1 both; reviewers certify fragments as bluntness). No-brand + mandatory novelty → one-off metaphor proliferation (R2 sugar). Card-routed advisory overrode carried silence rule (R3 both; six sugar cards, ADV-01 every smoking row; reviewers ratify as ID-compliance). REGISTER fired once, blind by construction otherwise. Same three-reason shape both = shared mechanism. Roots: style-guide (avoidance, metaphor demand, gate definition) + plan-card (advisory routing). Factory + plans restored to 041. 047 mechanism must never return in its form; REGISTER-kin-list proven blind.
**Next direction:** 048 PRIMARY deficit 35/35: fragment ban WITH reviewer finding (no new bluntness pressure), novelty-demand relief (cut debut quota, style level), advisory-presence rule (042 two-card line eligible). Never card-field edits, route-every-limit, Latinate-ban-alone, factory-speech, willpower, re-argument, headers, tight-shoes. Consecutive no-KEEP: 6.

### iter-048 — FRAGMENT finding + quota relief + silence line
**Hypothesis:** PRIMARY deficit: reviewer FRAGMENT finding (enforce carried ban, no new pressure) + style quota→assigned-only + writer silence line, so deficit falls both (35→≤26 / 35→≤26).
**Change:** `prompts/chapter-reviewer.md` (FRAGMENT + gate); `prompts/style-guide.md` (§B7 quota relief); `prompts/chapter-writer.md` (042 silence line). Both plans regenerated (sugar 19, smoking 15). Research reused.
**Verdict:** QUANTIFY
**Lesson:** FRAGMENT fired both (quoted runs repaired; R1s no longer quote fragments; generation still re-offends). Quota relief half-fired (guide removed, writer craft-7 retained — residual pressure in one sentence). Nipper BACK because the 047 restore wiped the verified 046 line and the 047→048 direction omitted the rebuild — process failure: post-restore hypotheses must explicitly rebuild verified parts. Sugar R3 redefinition is brief doctrine ("refined/added sugar and junk carbs") — not a defect, do not chase. Smoking timetable hedges unclosable without row/routing change (barred). Headers = instrument property. Comparison rose on regen (PERSISTENT plan). Floors 99.7/98%. No restore (sugar improved, smoking flat). Consecutive no-KEEP: 7.
**Next direction:** 049 PRIMARY deficit 28/35 — explicit rebuild list: Fork-1 no-brand re-applied + craft-7 aligned + FRAGMENT carried. Do not chase brief line, headers, tight-shoes, noise. Never card-field edits, route-every-limit, Latinate-ban-alone, factory-speech, willpower, re-argument.

### iter-049 — Fork-1 rebuild + craft-7 alignment (restore-rebuild)
**Hypothesis:** PRIMARY deficit: re-apply verified 046 no-brand line (wiped by 047 restore) + align writer craft-7 with guide quota relief; FRAGMENT/silence carried. Deficit falls both (28→≤21 / 35→≤26).
**Change:** `prompts/style-guide.md` (Fork-1); `prompts/chapter-writer.md` (craft 7). Both plans regenerated (sugar 15, smoking 15). Research reused.
**Verdict:** QUANTIFY
**Lesson:** Rebuild fired both (0 brand hits; common nouns). FRAGMENT still fires; generation re-offends. Deficits did not follow brands: sugar +2 noise, smoking +5 below-band (new residuals: pastoral-refrain family — chorus+never-verbatim+rooms evaded by variant endings, UNASSIGNED-REFRAIN blind; drilled-you vs quarantined-I — plan slot law; vow clinician collision; headers). Guide contradiction found (:224 original-names vs Fork-1 no-brand — cleanup needed). Comparison diverged by regen draw (PERSISTENT plan). Floors 103/96%. No restore (below band both). Consecutive no-KEEP: 8.
**Next direction:** 050 (final authorized) PRIMARY deficit 30/40: refrain-family discipline and/or I-distribution (non-card or founder call) and/or contradiction cleanup. Never card-field edits, route-every-limit, diction pressure, factory-speech, willpower, re-argument, headers, tight-shoes, brief line, timetables.
