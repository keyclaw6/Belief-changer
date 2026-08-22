# Auto-Tuning Loop — Learnings

> Every iteration (pass or fail) appends here. The loop never repeats a failed hypothesis.
> Format: iteration number, date, hypothesis, what changed, what happened, verdict, lesson.

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
**Lesson:** Banning ledger labels is not the same as banning factory speech. Verbatim SUPPORTED/Permitted-inference dumps largely vanished, but Binding chapter craft still uses speakable diction (`killer-line pair`, `argue-to-compress`, `your card assigns`, persona codes) and the model emits it; Cluster 1 mutated into research-report register. Voice FAIL count stayed 14/18. Do not repeat the evidence-honesty clause swap. Next writer-prompt change must make craft instructions execute-silently, or the 3-strike clock on this component continues.
**Next direction:** One causal change in `prompts/chapter-writer.md` Binding chapter craft — replace speakable craft/plan diction with execute-invisibly instructions — then full rewrite. Plan-level re-argument and frozen legal instruction tails are later, lower-priority clusters. Judge instrument for 001 was composer-2.5 (000 was DeepSeek); class comparison only.

### iter-002 — debut-once echo-by-token
**Hypothesis:** Replace the plan-skill mantra-only repetition law with a debut-once / echo-by-token law covering mantras, scenes (S-xx), and evidence rows (E-xx) so 001 Cluster 4 (cross-chapter re-argument) closes in book-arc.
**Change:** `prompts/master-plan-skill-v2.md` (Mantra and frozen-token sheet — one sentence). Research reused; new plan; 19 chapter files regenerated on Vercel Muse Spark. Judges: composer-2.5.
**Verdict:** REVERT
**Lesson:** Debut-once on S-xx/E-xx closed the named 001 instances (ledger re-walk, 100-cord restage, scare loop; reader 19/19 PASS) but book-arc still FAIL on the same class mutated (wanting/liking rebuilt at Sunlit Table; Willpower Method re-installed; M-09/M-10 before debut). Voice 0/19 PASS with a NEW class: echo-law placeholders (`by name in one sentence here`) copied from card parentheticals into prose. Do not repeat this plan-skill sentence swap. Next plan change must bind chapter jobs and evidence re-lists without writing speakable echo templates onto cards; writer-prompt factory speech still dominates voice.
**Next direction:** One causal change. Do not repeat 001 evidence-honesty or 002 debut-once S/E wording. Arc still owns priority (book-arc FAIL). Residual writer-prompt Binding craft is the voice target if the hypothesizer follows voice over remaining plan-card re-argument.


### iter-003 — card job/evidence re-own ban
**Hypothesis:** Bind Compact chapter cards so settled jobs/evidence cannot be re-owned for a second full demolition, and ban speakable echo parentheticals on cards, so 002 Cluster 5 closes in book-arc.
**Change:** `prompts/master-plan-skill-v2.md` (Compact chapter cards — job + evidence bullets + superseding paragraph). Research reused; new plan (20 chapters); full rewrite on Vercel Muse Spark. Judges: composer-2.5.
**Verdict:** REVERT
**Lesson:** Binding job/evidence re-lists closed the named 002 symptoms (wanting/liking rebuild, Willpower re-definition; echo placeholders gone; belief 20/20; reader 19/20; voice 6/20). Book-arc still FAIL on the same class mutated via scene IDs (A01 tight-shoes re-performed C03→C07), token pre-debut (T04 in C09), readiness seam duplication (C16→C17), and hand-off rebuild (C20). Plan-skill edits that only constrain evidence/job fields leave scene-bank re-assignment and adjacent-card seam ownership free. Do not repeat this Compact-cards job/evidence wording. Writer-prompt factory speech still dominates voice (14/20 FAIL).
**Next direction:** STOP for founder reconsideration (requested). Do not start 004. Candidates if resumed: scene/analogy debut-once in plan skill; writer-prompt Binding craft silence; or change loop process to survive stream disconnects.

### iter-004 — scene-bank debut-once
**Hypothesis:** Bind Scene and analogy bank so each scene/analogy ID gets one full staging at a debut chapter; later cards may only token-echo, closing 003 Cluster 1 (A01 tight-shoes double full stage).
**Change:** `prompts/master-plan-skill-v2.md` (Scene and analogy bank). Research reused; new plan (21 files); full rewrite on Vercel Muse Spark. Judges: composer-2.5.
**Verdict:** REVERT
**Lesson:** Scene debut-once closed the named A01 C03→C07 double full stage, but book-arc still FAIL on the same re-argument class mutated (FM completes inversion early; A-07 vault-safe doubled FM→C01; mantra/token pre-debut; C16 encyclopaedic re-litigation). Third consecutive plan-skill REVERT on this class (002, 003, 004) — **PIVOT** off plan-skill for re-argument. Voice still 3/21 PASS; writer-prompt Binding craft remains the unpaid voice target.
**Next direction:** Pivot to `prompts/chapter-writer.md` Binding chapter craft (execute-silently / ban speakable craft diction) OR a non-plan-skill approach. Do not repeat 002–004 plan-skill re-argument wording.

### iter-005 — Binding craft silent-execution
**Hypothesis:** Make craft execute silently in `prompts/chapter-writer.md` — delete speakable craft diction (trap question, killer-line, argue-to-compress, future-pacing, persona codes) to close voice Cluster 6 after plan-skill 3-strike pivot.
**Change:** Three hunks in `prompts/chapter-writer.md` (Method and voice + Binding bullets 2 and 7). Research+plan reused; 18 chapters rewritten on Muse Spark. Judges: composer-2.5.
**Verdict:** REVERT
**Lesson:** Voice **0/18 PASS** — regression from 004 (3/21). Some literal craft-label leaks reduced but factory scaffolding, research-register, persona codes, and meta-commentary persist or worsen. Silent-execution ban did not change model behavior enough; voice Cluster 6 unpaid. Book-arc still FAIL (mantra echoes, repeated scenes).
**Next direction:** Do not repeat 005 wording. Try style-guide voice constraints, plan-reviewer gate, loop/config model route, or a non-writer surface. Continue 006–008.

### iter-006 — Speakable Card Sanitization gate
**Hypothesis:** plan-reviewer Gate 4 strips speakable craft/persona literals from compact cards before generation, closing voice Cluster 6 + persona Cluster 3.
**Change:** `prompts/master-plan-reviewer-v2.md` Gate 4. New 20-chapter plan (3 review rounds); full rewrite Muse Spark. Judges composer-2.5.
**Verdict:** REVERT
**Lesson:** Persona P-xx codes eliminated from prose; voice rose 0/18→5/20 but still 14 FAIL; trap-question phrasing persists in 17 chapters; book-arc FAIL on arc-timing/re-litigation. Reviewer gate improved cards but did not close owning voice class.
**Next direction:** style-guide, writer route in config, or combined surface — not another Gate 4 repeat. Continue 007–008.

### iter-007 — style-guide speakable craft ban
**Hypothesis:** Remove craft-label vocabulary from style-guide so trap question etc. stop surfacing; voice Cluster 1 closes.
**Change:** `prompts/style-guide.md` — disarming one-answer question, speakable craft ban in §9, toolkit renames.
**Verdict:** REVERT
**Lesson:** trap question 17→3 but voice **1/20** (worse than 006). Belief 20/20; book-arc FAIL. Style-guide surface alone cannot close voice while writer-prompt still names devices and model ignores bans.
**Next:** 008 final — try `loop/config.yaml` writer model/route (non-contributor fallback or alternate).

### iter-008 — writer non-contributor model (FINAL)
**Hypothesis:** meta/muse-spark-1.2 primary improves craft-ban adherence vs contributor.
**Change:** `loop/config.yaml` writer_model → meta/muse-spark-1.2.
**Verdict:** REVERT
**Lesson:** Voice 5/20; trap question 17/20. Campaign 004–008 all REVERT on targeted factory gaps. Loop IDLE.
