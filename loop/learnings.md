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

