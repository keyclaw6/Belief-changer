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
