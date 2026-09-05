# Experiment Ledger

> The full story of every experiment the loop has run — written so a human (or
> a fresh agent) can read it top to bottom and understand not just *what
> happened* but *why*, and *what to try next*. This is the learning record of
> the whole campaign.
>
> **How it relates to the other records:**
> - `loop/results.tsv` — the canonical machine row (one line per iteration).
>   The verdict and lesson here are copied from it, never re-worded.
> - `loop/learnings.md` — the terse evidence log the *hypothesizer* reads
  (REVERT is not a ban; see founder 2026-08-24).
> - **This file** — the explanation. Where you come to actually understand an
>   experiment and decide the next move.
>
> **Rules:** one entry per iteration, newest at the bottom. Append-only — never
> edit or reword a past entry; a correction is a new entry. Write for a reader
> who wasn't there: enough detail that the *reasoning* is visible, not just the
> outcome.

---

## Entry format

Each iteration gets an entry like this:

```markdown
### iter-NNN — <short title>  ·  <date>  ·  <KEEP | REVERT | INCONCLUSIVE | BASELINE>

**Hypothesis.** What we believed and why — the failure we were attacking and
the causal reasoning ("if we change X, gap Y closes because Z").

**Change.** Exactly what was done: the file, the section, and the nature of the
edit — enough that the diff is confirmable but the intent is stated in words.

**What happened.** The evidence. What the judges saw, what the traces showed,
whether the predicted cluster closed, and anything unexpected. Quote the
decisive finding, don't summarize it away.

**Verdict & why.** KEEP / REVERT / INCONCLUSIVE and the reasoning — including
whether the prediction was accurate, partial, or wrong.

**What we learned.** The durable lesson about the factory — copied verbatim
from the results.tsv lesson.

**What this opens next.** The direction this points to: the cluster to attack
next, the component level to move to if this one is spent, or the question this
raised. This is what makes the ledger tell you what to do next.
```

---

## Entries

### iter-000 — BASELINE  ·  2026-08-17  ·  BASELINE

**Hypothesis.** None — this is the baseline. We established where the factory stands with a fresh full run (no causal change) so every later iteration has an accepted starting state and an honest noise calibration. We asked the whole panel (3 chapter lanes × 18 + book-arc + trace analyzer + an A/A rerun of chapter 01) what it measures, and whether its per-chapter verdicts are repeatable enough to trust for decisions.

**Change.** None. Full end-to-end factory run only: research (10 banks, 1040 packets) → accepted 18-chapter master plan → 18 chapters generated → reference-alignment table → judging → A/A noise check → trace analysis. Committed nothing beyond the records of measurement.

**What happened.** The panel is overwhelmingly favorable on the substance of the method and split on its delivery. **Belief-mechanic: 18/18 PASS** — every chapter completes its assigned belief transition; the false beliefs are named, credits reassigned, sacrifice removed, reframes settled, reader does the work. **Reader-journey: 13/18 PASS** — the 5 failures (C02, C06, C11, C14, C15) are momentum/continuity stalls, not destination failures; they stall where a scene or evidence block is re-argued or where an analytical block interrupts an emotional peak. **Book-arc: PASS** with two noted cross-chapter repetitions (C01→C02 confidence trick and prevalence; C05→C11 cinema scene and lived lines). **Voice-emotion: 4/18 PASS, 14 FAIL** — the concentrated failure, driven by two systemic clusters whose root component is the **writer-prompt**. Trace analysis merged the 58 reports into four causal clusters:
1. evidence-grading scaffold leaked verbatim into reader prose — `SUPPORTED/MIXED/CONTESTED`, `Permitted/Prohibited inference`, `E-0x` IDs, consent vocabulary — at the emotional peaks (writer-prompt; systemic);
2. factory-internal taxonomy & drafting scaffolding surfaced — `S-01`/`P-03`/`I-05`/`M-07`, "Killer-line pair.", "Short sentences for the peak", "as Carr does", "argue-to-compress beat made visible" (writer-prompt; systemic);
3. cross-chapter re-argument of settled scenes/evidence instead of invoke-by-token (plan; positional C01→C02 and C05→C11);
4. local grammatical/lexical fabrication in C02 — "We trapped.", "marksman-shipped" (model; local).
The A/A rerun of chapter 01 (identical inputs, same model) came back belief-mechanic PASS + reader-journey PASS + voice-emotion FAIL on the evidence-grading register — so the material failure-class set **differed** between the two runs (run 1 none, run 2 one). That is the noise floor for this battle: the systemic Cluster-1 leak is real across the book but sampling-sensitive in any one chapter.

**Verdict & why.** BASELINE. The panel and trace analysis are complete and valid: every judge report finished after retries, so we may decide on the full evidence. As a baseline there is no target cluster to close — the verdict is a measurement, not a pass/fail on a hypothesis. The measurement is: the factory currently produces the correct belief-change work (belief-mechanic and the arc are sound) but fails the voice lane at scale because the writer-prompt keeps implementation grammar in the reader's ear.

**What we learned.** Baselines are calibrated. The durable lesson: belief-change mechanics are strong (18/18) and the book lands as a journey (arc PASS); the loop's first real target is voice — the writer-prompt over-orders "preserve every evidence grade … permitted/prohibited inference" and never forbids surfacing internal identifiers/craft directives, so the strongest chapters carry the factory's research scaffolding where the reader should hear one warm voice. What "material" means is now calibrated from the A/A gap: decisions compare failure-class sets across the book, never a single chapter's instance.

**What this opens next.** The baseline gives iteration 001 a clear target: hypothesize one causal change to the **writer-prompt** that (a) converts each evidence-limits constraint into plain Carr register (or quarantines it) and (b) bans internal identifiers/draft directives from reader prose; then rerun the full book and re-judge the voice lane. The plan-level cross-chapter re-argument (Cluster 3) is a second, lower-priority thread for a later iteration. Route/model: the writer stays on the Command Core proxy (Muse Spark contributor); judges/trace-analyzer stay on opencode-go/deepseek-v4-flash.

### iter-001 — scaffold firewall  ·  2026-08-21  ·  REVERT

**Hypothesis.** If the writer-prompt stops commanding "preserve every evidence grade / permitted-prohibited inference" and instead holds those limits internally while forbidding ledger IDs, grades, persona/scene codes, and craft labels in reader prose, voice Clusters 1 and 2 close because the model can no longer obey by dumping the factory tongue at climaxes.

**Change.** One clause in `prompts/chapter-writer.md` (evidence-honesty). Already applied on campaign-001 as `be106a5` before the 001 rewrite. Research and plan reused. All 18 chapters regenerated on Vercel `meta/muse-spark-1.2-contributor`. Judges: Cursor composer-2.5 (preflight 18/18 PASS). Confound vs 000 DeepSeek panel: class comparison only.

**What happened.** Targeted clusters **partially closed**. Leak log: most chapters 0 hits; residual `P-0x` / `Killer-line` / `your card assigns` in C05–C09 and C17; one `CONTESTED` in C08. Voice judges still FAIL 14/18 — now quoting research-report register (C01 "validated self-report scales"), craft stage-direction (C08 "full argue-to-compress beat"), and instruction-as-paperwork (I-05 clinician tails). Belief 17/18 PASS (C13 FAIL: Nature's Guide as installed instruments). Reader 16/18 PASS (C13, C15). Book-arc FAIL (M-03 misses; mechanism names before C08; C10 re-ledger; C12 100-cord restage; health-scare loop). Trace analysis: 000 Cluster 1 partially closed (labels gone, briefing remains); Cluster 2 partially closed (same class, fewer instances); Cluster 3 persists; Cluster 4 (C02 grammar) closed.

**Verdict & why.** REVERT. Predicted close of Clusters 1 and 2 did not happen. Partial label-ban is not material class closure while factory speech still appears in reader prose. Prediction: partial. The 001 book is not accepted. The founder-applied firewall text stays on campaign (reverting it would restore the worse preserve-every-grade command); this iteration does not promote a new accepted book.

**What we learned.** Banning ledger labels is not the same as banning factory speech. Verbatim SUPPORTED/Permitted-inference dumps largely vanished, but Binding chapter craft still uses speakable diction (`killer-line pair`, `argue-to-compress`, `your card assigns`, persona codes) and the model emits it; Cluster 1 mutated into research-report register. Voice FAIL count stayed 14/18. Do not repeat the evidence-honesty clause swap. Next writer-prompt change must make craft instructions execute-silently, or the 3-strike clock on this component continues.

**What this opens next.** Attack residual factory scaffolding at a *different* instruction in the same file: Binding chapter craft still names devices in speakable English. One change. Then full rewrite. Plan re-argument and frozen legal instruction strings wait. Writer-prompt is 2/3 strikes on this failure class if 002 also REVERTs at this component.

### iter-002 — debut-once echo-by-token  ·  2026-08-21  ·  REVERT

**Hypothesis.** If the plan skill's repetition law covers scenes and evidence rows — debut-once, later cards echo by token in ≤1 sentence — Cluster 4 closes because writers will no longer receive cards that re-assign S-04/E-11, S-08, the awe catalogue, or scare bullets for full re-argument.

**Change.** One sentence in `prompts/master-plan-skill-v2.md` (`### Mantra and frozen-token sheet`). Worktree `../quit-sugar-iter-002` on `iter-002`. Research reused from campaign. New master plan through 9 review rounds to `fit to write from`. 19 files written (FM + 18 chapters) on Vercel `meta/muse-spark-1.2-contributor`. Panel: Cursor composer-2.5, 57 chapter + book-arc.

**What happened.** Targeted Cluster 4 **partially closed**. Closed 001 instances: C10 FOR-ledger re-walk, C12 hundred-cord restage, health-scare loop, reader C02 rebuilds. **Reader-journey 19/19 PASS.** Belief 18/19 PASS (file 03 FAIL: pleasure credit held open at confidence-trick). **Book-arc FAIL** on mutated re-argument: Gap 2 wanting-is-not-liking rebuilt at Sunlit Table after the taste chapter; Gap 3 Willpower Method fully re-defined in plan Ch.14 after Ch.1; Gaps 1/4 M-10 and M-09 before assigned debuts. **Voice 0/19 PASS.** Trace Cluster 1 (NEW): cards wrote echo instructions as parentheticals (`recalled by name`, `≤1 sentence`); writer emitted `Remember X by name in one sentence here` in C16–C17. Persistent writer-prompt factory speech (P-0x, peak-verdict meta, research-report register) still dominates voice.

**Verdict & why.** REVERT. Owning book-arc lane did not PASS. Same failure class persists in mutated form. Voice also vetoes KEEP: quoted new class absent from 000/001. Prediction: partial. Factory change and 002 book are not promoted.

**What we learned.** Debut-once on S-xx/E-xx closed the named 001 instances (ledger re-walk, 100-cord restage, scare loop; reader 19/19 PASS) but book-arc still FAIL on the same class mutated (wanting/liking rebuilt at Sunlit Table; Willpower Method re-installed; M-09/M-10 before debut). Voice 0/19 PASS with a NEW class: echo-law placeholders (`by name in one sentence here`) copied from card parentheticals into prose. Do not repeat this plan-skill sentence swap. Next plan change must bind chapter jobs and evidence re-lists without writing speakable echo templates onto cards; writer-prompt factory speech still dominates voice.

**What this opens next.** Do not retry the 002 sentence. Remaining arc failures are chapter jobs that re-dissect settled verdicts and evidence rows re-listed for full use (trace Cluster 5), plus model-level mantra debut misses (Cluster 6). Voice still has writer-prompt Binding craft (3-iteration persistence, only 001 targeted it). Hypothesizer picks one file, one causal change. Inbox empty.

### iter-003 — card job/evidence re-own ban  ·  2026-08-21  ·  REVERT

**Hypothesis.** If Compact chapter cards forbid re-owning settled jobs/evidence for a second full demolition and ban speakable echo parentheticals, 002 Cluster 5 closes because later cards can no longer legally assign wanting/liking rebuild or Willpower re-definition.

**Change.** Job + evidence bullets and superseding paragraph in `prompts/master-plan-skill-v2.md` (`### Compact chapter cards`). Worktree `../quit-sugar-iter-003`. Research reused. New master plan (20 chapters) to `fit to write from` in 2 review rounds. 20 chapters on Vercel Muse Spark. Panel: composer-2.5, 60 chapter + book-arc.

**What happened.** Targeted 002 Cluster 5 **symptoms closed** (no wanting/liking second section; no Willpower full re-definition; no `by name in one sentence here`). Belief 20/20 PASS; reader 19/20 PASS (C20 FAIL); voice 6/20 PASS; **book-arc FAIL** on mutated class: A01 tight-shoes full re-perform C03→C07; T04 instant-freedom in C09 before C18 debut; M01 missing C10 echo; C16→C17 readiness duplication; C19 I-11 forward-reference. Trace: plan-skill bound evidence/jobs but not scene IDs or seam ownership; writer-prompt factory speech persists (clusters 7–8).

**Verdict & why.** REVERT. Owning book-arc still FAIL. Same re-argument class persists via scene/seam channels. Prediction: partial. Factory change and 003 book not promoted.

**What we learned.** Binding job/evidence re-lists closed the named 002 symptoms (wanting/liking rebuild, Willpower re-definition; echo placeholders gone; belief 20/20; reader 19/20; voice 6/20). Book-arc still FAIL on the same class mutated via scene IDs (A01 tight-shoes re-performed C03→C07), token pre-debut (T04 in C09), readiness seam duplication (C16→C17), and hand-off rebuild (C20). Plan-skill edits that only constrain evidence/job fields leave scene-bank re-assignment and adjacent-card seam ownership free. Do not repeat this Compact-cards job/evidence wording. Writer-prompt factory speech still dominates voice (14/20 FAIL).

**What this opens next.** Founder stop for reconsideration. Stream disconnects (0x8) keep killing long orchestrator turns. Substantive: either extend debut-once to scene/analogy IDs + seam ownership, or pivot to writer-prompt Binding craft silence (voice still 14/20 FAIL after four iterations of plan/writer partials). Do not start 004 until founder decides.

### iter-004 — scene-bank debut-once  ·  2026-08-21  ·  REVERT

**Hypothesis.** If the Scene and analogy bank requires one debut chapter for full staging and later cards may only token-echo, 003 Cluster 1 closes because C07 can no longer legally re-stage A01 at full length.

**Change.** Scene and analogy bank bullets + token-echo rule in `prompts/master-plan-skill-v2.md`. Worktree `../quit-sugar-iter-004`. Research reused. New plan (FM+20) to `fit to write from` in 5 review rounds. 21 chapters on Vercel Muse Spark. Panel: composer-2.5, 63 chapter + book-arc.

**What happened.** Targeted A01 symptom **closed** (one full stage in C07; later token echoes). Belief 21/21 PASS; reader 16/21 PASS; voice 3/21 PASS; **book-arc FAIL** on mutated re-argument (FM inversion early; A-07 safe doubled; token pre-debut; C16 re-litigation). Trace: plan-skill scene debut-once works for the bound ID but FM scope and other scene IDs remain free; writer-prompt factory speech persists.

**Verdict & why.** REVERT. Owning book-arc still FAIL. Same class mutated. Prediction: partial. Factory change and 004 book not promoted. **3-strike on plan-skill for re-argument class — pivot.**

**What we learned.** Scene debut-once closed the named A01 C03→C07 double full stage, but book-arc still FAIL on the same re-argument class mutated (FM completes inversion early; A-07 vault-safe doubled FM→C01; mantra/token pre-debut; C16 encyclopaedic re-litigation). Third consecutive plan-skill REVERT on this class (002, 003, 004) — **PIVOT** off plan-skill for re-argument. Voice still 3/21 PASS; writer-prompt Binding craft remains the unpaid voice target.

**What this opens next.** Pivot to writer-prompt Binding craft silence for iter-005 (voice unpaid across 000–004). Do not start another plan-skill re-argument patch. Continue through 008 then stop.

### iter-005 — Binding craft silent-execution  ·  2026-08-22  ·  REVERT

**Hypothesis.** If chapter-writer Binding craft forbids speakable craft labels and requires silent execution, voice Cluster 6 closes and voice-emotion PASS rises.

**Change.** Three hunks in `prompts/chapter-writer.md`. Writer-only; campaign plan+research reused. 18 chapters Muse Spark. Panel composer-2.5.

**What happened.** Voice 0/18 FAIL (worse than 004). Belief 17/18; reader 13/18; book-arc FAIL. Some literal label leaks down; trap-question/persona-code scaffolding persists. Trace: Cluster 6 regressed, not closed.

**Verdict & why.** REVERT. Owning voice-emotion still FAIL. Factory change not promoted.

**What we learned.** Silent-execution writer patch insufficient for Muse Spark voice lane; factory speech class persists across 5 iterations.

**What this opens next.** Style-guide, plan-reviewer, config/model, or arc mechanism — not another 005 repeat. Continue through 008.

### iter-006 — Speakable Card Sanitization  ·  2026-08-22  ·  REVERT

**Hypothesis.** If plan-reviewer Gate 4 forbids speakable craft/persona literals on cards, voice Cluster 6 and persona Cluster 3 close before generation.

**Change.** Gate 4 in `master-plan-reviewer-v2.md`. New 20-chapter plan; full book. Panel composer-2.5.

**What happened.** Persona codes gone; voice 5/20 PASS (up from 0/18); belief 20/20; reader 18/20; book-arc FAIL; trap question in 17 chapters.

**Verdict & why.** REVERT. Owning voice still majority FAIL; book-arc FAIL. Partial win on persona only.

**What we learned.** Upstream card sanitization helps persona leaks but not trap-question factory speech or arc curve.

**What this opens next.** style-guide or config route for 007. Finish 008 then stop.

### iter-007 — style-guide craft ban  ·  2026-08-22  ·  REVERT

**Hypothesis.** Style-guide speakable craft ban closes Cluster 1 and raises voice PASS.

**Change.** style-guide.md toolkit + §9 ban. Reused iter-006 plan; full 20-chapter rewrite.

**What happened.** trap question 3/20 (was 17); voice 1/20 PASS; belief 20/20; book-arc FAIL.

**Verdict & why.** REVERT. Owning voice regressed. Partial literal improvement insufficient.

**What this opens next.** Config/model surface for final iter-008.

### founder-2026-08-24 — REVERT is not a ban  ·  2026-08-24  ·  AMENDMENT

**Hypothesis.** None — founder process amendment after the judge census redesign.

**Change.** North Star, PROGRAM, hypothesizer, and learnings: a REVERT verdict does not forbid retrying that factory change. Exact prior wording from 001–007 stays eligible under the new census judges. The 001–008 3-strike/PIVOT notes do not bind 009 onward. 008's non-contributor model swap stays forbidden because models are founder-only.

**What happened.** 001–008 were scored on the retired PASS/FAIL-by-label instrument. Several of those prompt changes closed named symptoms and may still be the right factory move; the old KEEP/REVERT gate could not see NOTED-class improvement.

**Verdict & why.** Amendment, not an experiment. Records stay; eligibility reopens.

**What we learned.** Learnings are evidence of what happened under a given instrument, not a ban list.

**What this opens next.** After 009's instrument baseline, 010+ may retry writer-prompt, plan-skill, plan-reviewer Gate 4, and style-guide changes from 001–007 when the new traces point there.

### iter-009 — instrument baseline  ·  2026-08-24  ·  BASELINE

**Hypothesis.** None. Judge census redesign requires a fresh two-book baseline.

**Change.** No factory edit. Reused accepted research and the 000 18-chapter plan. Wrote replicate A then B on Muse Spark Zen contributor-free (A ch09 one Vercel contributor fallback). Judged with composer-2.5 census panel.

**What happened.** Belief 18/18 PASS both books, journey 18/18 PASS both, book-arc PASS both. Voice 11/18 PASS both. Blocking in both books: `factory-speech` 18+19, `instruction-paperwork` 2+5. Noted in both: willpower-lexicon ~70 each, factory-speech noted 60 each, trap-question-label 23/11, coach-register 16/25, journey re-argument 11/14, book-arc re-argument 7/8. Voice FAIL chapters overlap only at ch01.

**Verdict & why.** BASELINE. Measurement, not KEEP/REVERT. Accepted snapshot is replicate A.

**What we learned.** Under census judges the factory's belief and arc work hold. The unpaid KEEP object is writer-prompt factory-speech at assigned peaks (BOXED DEFINITION, killer-line, FOR column, trap-question labels). Plan frozen instructions carry clinical/cross-ref tails that fire instruction-paperwork. 001–007 prompt changes remain eligible.

**What this opens next.** One causal writer-prompt change targeting factory-speech blocking counts in both books — 005 silent-execution wording is eligible to retry, or a tighter Binding-craft subtraction. Do not swap models.

### iter-010 — silent craft + workshop-token translation  ·  2026-08-25  ·  KEEP

**Hypothesis.** If the writer contract forbids naming craft and outranks card workshop strings, voice blocking `factory-speech` falls in both books.

**Change.** Four hunks in `prompts/chapter-writer.md` (silent trap-questions; expanded never-surface + translation supremacy; Binding 2 and 7). Plan and research reused. Two 18-chapter books on Muse Spark Zen.

**What happened.** factory-speech blocking 18→6 (A) and 19→8 (B). trap-question-label noted 23→7 / 11→0. Voice PASS 11→13 (A), 11→11 (B). Belief 18/18, journey 18/18, book-arc PASS both. Residual factory-speech: FOR-column / BOXED residual, anatomy checklist, mantra slugs. instruction-paperwork 2→3 / 5→6. method-promise-hedge 1 in B only.

**Verdict & why.** KEEP. Targeted class improved in both books; no shared new blocking class. Prediction was near-zero; result is material drop, not close (partial).

**What we learned.** Speakable Binding diction was a real cause of boxed-definition / killer-line / trap-question leaks. Plan workshop tokens and the bundled style-guide anatomy checklist still leak after that ban.

**What this opens next.** Residual factory-speech (plan-card tokens or style-guide bundle) or plan instruction-paperwork. New mechanism — do not re-apply 010 hunks unchanged.

### iter-011 — style-guide silent operators  ·  2026-08-25  ·  KEEP

**Hypothesis.** If the bundled style-guide stops naming craft operators, voice blocking `factory-speech` falls in both books.

**Change.** Four hunks in `prompts/style-guide.md` (§B5 header + operators 3/6/8/11; §B7 item 5; §B9 checklist). Plan and research reused. Two 18-chapter books on Muse Spark Zen.

**What happened.** factory-speech blocking 6→4 (A) and 8→2 (B). Operator-vocabulary peaks closed as blocking. Residual factory-speech is plan I-06 `as in I-05` plus A-only FT-06 (noise). instruction-paperwork 3→5 / 6→5. Voice PASS 13→15 / 11→16. Belief 18/18, journey 18/18, book-arc PASS both.

**Verdict & why.** KEEP. Targeted class improved in both books; no shared new blocking class. Prediction accurate on the drop and on paperwork persistence.

**What we learned.** Speakable style-guide operator names were a real remaining cause after 010's writer-prompt ban. Frozen instruction-spine safety tails and ID cross-refs are now the unpaid KEEP object (plan, PERSISTENT 3×).

**What this opens next.** Plan instruction spine. Founder halt — do not start 012 until asked.

### iter-012 — plan-skill instruction-spine split  ·  2026-08-27  ·  KEEP

**Hypothesis.** If the plan skill forbids fusing clinical tails and ID cross-refs into frozen instruction rows, voice blocking `instruction-paperwork` falls in both books.

**Change.** Instruction-spine paragraph in `prompts/master-plan-skill-v2.md` (spoken Carr imperative only; CA-01 boxed advisory; no `as in I-05`). Plan regenerated (17 chapters). Two books on Muse Spark Zen.

**What happened.** instruction-paperwork blocking 5→0 (A) and 5→0 (B). `as in I-05` factory-speech at old C15/C18 gone. factory-speech blocking 4→3 / 2→9. Voice PASS 15/17 and 13/17. Belief 17/17, journey 16/17, book-arc PASS both. Journey `compliance-missing` 2/1 traces as I-08/M-08 ID collision, not missing mantra-sheet wording.

**Verdict & why.** KEEP. Targeted class closed in both books. New `compliance-missing` class name is not a material book regression (wrong frozen target). factory-speech B regression is not a both-books new class.

**What we learned.** The 011 frozen-spine rule was the real cause of paperwork. Regenerating the plan was required. Residual factory-speech after the split is style-guide beat labels and ledger-token callbacks, not liability tails.

**What this opens next.** Style-guide toolkit names / writer-prompt ledger framing, or plan I-08 vs M-08 numbering. Founder halt — do not start 013.

### iter-013 — founder-batch spine and packet hygiene  ·  2026-08-27  ·  KEEP

**Hypothesis.** If writer, plan-skill, plan-reviewer, and style-guide are rewritten together for Carr spine, packet hygiene, and lettered mantra IDs, voice blocking `factory-speech` falls in both books and journey `compliance-missing` from M-08/I-08 closes.

**Change.** Four prompt files (see `loop/iterations/013/change.diff`). Plan regenerated (14 chapters). Two books on Muse Spark Zen. Panel composer-2.5, 43+43.

**What happened.** factory-speech blocking 3→2 (A) and 9→2 (B). Named 012 surfaces gone. compliance-missing 2→0 / 1→0. Voice 13/14 both (FAIL ch08 only). Belief 14/14, journey 14/14, book-arc PASS both. Residual: CH-08 announces register/job from card Voice/guardrail lines; A also grafts T-A (noise). Noted factory-speech floor still ~29/28.

**Verdict & why.** KEEP. Both targeted clusters improved in both books. No shared new blocking class. Attribution weak (founder batch).

**What we learned.** Lettered mantra IDs closed the I-08/M-08 instrument collision. Packet hygiene closed the named 012 craft-label leaks. The factory-speech class mutated to plan-card Voice operators at the fear hinge — PERSISTENT after 010–012 prompt-level attempts.

**What this opens next.** CH-08 plan-card speakable Voice/guardrail lines, or a different level than more silent-execution bans. Founder halt — do not start 014 unless asked.

### iter-014 — founder-batch card operators and rooms  ·  2026-08-28  ·  KEEP

**Hypothesis.** If writer, plan-skill, plan-reviewer, and style-guide strip speakable Voice/guardrail operators from cards, ban Maya as pupil, and stop CA-SAFE title paste, voice blocking `factory-speech` falls in both books.

**Change.** Four prompt files (see `loop/iterations/014/change.diff`). Plan regenerated (15 chapters). Two books on Muse Spark Zen. Panel composer-2.5, 46+46.

**What happened.** factory-speech blocking 2→0 (A) and 2→0 (B). Named 013 CH-08 announcement strings gone. Voice 15/15 both. Belief 15/15, journey 15/15, book-arc PASS both. Noted factory-speech 29→17 / 28→38. B CH-09 one job-recap line is A-absent noise.

**Verdict & why.** KEEP. Targeted blocking class closed in both books. No shared new blocking class. Attribution weak (founder batch). Noted B rise is hydra, not a veto.

**What we learned.** Removing speakable operators from the card (not another writer never-announce) closed the CH-08 announcement class. The noted factory-speech floor mutated to evidence-limit register and frozen-token echo paste.

**What this opens next.** Plan-card evidence-limit vocabulary / verbatim echo paste, or a different level than more silent-execution bans. Founder halt — do not start 015 unless asked.

### iter-015 — founder-batch seed subtraction and job-ownership  ·  2026-08-29  ·  REVERT

**Hypothesis.** If writer, plan-skill, plan-reviewer, and style-guide subtract remaining pasteable seeds (evidence IDs only, echo ID-only, headline-only instructions, no trap-question formula) and bind semantic job-ownership so later cards cannot re-own a demolition under a new SC-ID, voice noted `factory-speech` and book-arc noted `re-argument` drop in both books.

**Change.** Four prompt files (see `loop/iterations/015/change.diff`). Plan regenerated (16 chapters). Research reused. Two books on Muse Spark Zen. Panel composer-2.5, 49+49.

**What happened.** Noted factory-speech 17→20 (A) and 38→13 (B). Book-arc re-argument 5→6 / 4→5. Blocking factory-speech 0→1 / 0→3. Voice 15/16 and 14/16. Belief 16/16, journey 16/16, book-arc PASS both. Named close: `trap-question-label` 3/1→0/0. A FAIL is ch05 "Let me land it as one short verdict, because this is the belief that changes in this chapter". B FAIL is ch14–15 numbered instruction headlines on assigned I-lines.

**Verdict & why.** REVERT. Targeted conjunction did not improve in both books. Blocking `factory-speech` returned in both (class that was 0 blocking last iter). Prediction wrong on the KEEP bar.

**What we learned.** Seed subtraction closed the trap-question formula and did not close the noted factory-speech floor or re-argument. The blocking class mutated to writer-prompt landing-meta (A) and numbered instruction anatomy (B). Prompt-level hydra continues.

**What this opens next.** A different level than another seed-subtraction batch on the same classes. Founder halt — do not start 016 unless asked.

### iter-016 — founder-batch trap-question keep + echo density  ·  2026-08-30  ·  INCONCLUSIVE

**Hypothesis.** If writer, plan-skill, plan-reviewer, and style-guide keep 015’s trap-question formula deletion, keep echo-ID-only with a mantra-density cap, and strip speakable verdict-landing / historical-evidence operators, trap-question closes 0/0 and noted factory-speech drops in both books vs 014.

**Change.** Four prompt files (see `loop/iterations/016/change.diff`). Plan regenerated (15 chapters). Research reused. Two books on Muse Spark Zen. Panel composer-2.5, 46+46.

**What happened.** Trap-question 3→0 (A) and 1→1 (B). Noted factory-speech 17→23 (A) and 38→13 (B). Blocking factory-speech 0 / 1. Voice 15/15 and 14/15. Belief 15/15, journey 15/15, book-arc PASS both. Named 015 kills absent. A ch14 noted factory-speech 7→2 under the density cap. B FAIL is ch04 assigned M-F echo as L-01 pipeline placeholder.

**Verdict & why.** INCONCLUSIVE. Each KEEP object improved in only one book. Blocking 0/1 is one-book noise, not a both-books veto and not REVERT.

**What we learned.** Echo-density closed the 015 vow-card inventory path and did not close the noted factory-speech floor in both books. Style-guide fact-assertion / evidence-framing still counts as noted factory-speech when the writer leans on it (A). Trap-question formula deletion mostly held; one `Ask:` prefix remains B-only.

**What this opens next.** Do not promote this batch. Next iteration needs a new mechanism on the both-books noted factory-speech hydra, not a replay of 015/016 seed subtraction. Founder halt — do not start 017 unless asked.

### iter-017 — trap-question isolation vs 014  ·  2026-08-30  ·  REVERT

**Hypothesis.** If writer and style-guide delete only the pasteable trap-question formula (015 S1–S5 EXACT; W1 ask without `land one short verdict`), `trap-question-label` closes 3/1 → 0/0 both vs 014.

**Change.** Two prompt files (see `loop/iterations/017/change.diff`). Plan reused (014, 15 chapters). Research reused. Two books on Muse Spark Zen. Panel composer-2.5, 46+46.

**What happened.** Trap-question 3→0 (A) and 1→1 (B). Blocking factory-speech 0→1 / 0→1. Voice 14/15 both. A FAIL ch09 chapter-job landing meta; B FAIL ch01 warmth-policy quote. B leftover trap-question is `Ask the simplest Socratic trap`. Journey A ch12 `compliance-missing` (one-book paraphrase). Belief 15/15, book-arc PASS both. Noted factory-speech 17→18 / 38→10.

**Verdict & why.** REVERT. KEEP object not 0/0 both. Blocking `factory-speech` returned in both (class that was 0 blocking last KEEP). Prediction wrong.

**What we learned.** Isolating the 015 trap-formula hunk does not hold a both-books close when the 014 plan still names `Socratic trap` on a card, and stripping `land one short verdict` does not close the landing-meta family. Blocking mutates.

**What this opens next.** Do not replay this isolation against the same census object. Founder halt — do not start 018 unless asked.

### iter-018 — trap-question prefix ban vs 014  ·  2026-08-30  ·  INCONCLUSIVE

**Hypothesis.** If the writer never-surface list adds `no trap-question or Socratic-trap prefixes` and the rest of the factory stays at 014 KEEP, voice noted `trap-question-label` closes 3/1 → 0/0 both vs 014.

**Change.** One line in `prompts/chapter-writer.md` (see `loop/iterations/018/change.diff`). Plan reused (014, 15 chapters). Research reused. Two books on Muse Spark Zen. Panel composer-2.5, 46+46.

**What happened.** Trap-question 3→0 (A) and 1→0 (B). Blocking factory-speech 0→2 / 0. method-promise-hedge blocking 1 / 0. Voice 13/15 and 15/15. A FAIL ch07 Burgeon `almost automatically`; A FAIL ch09 population-level / follow-up audit at the TO/FOR climax. Named 015/017 kills absent. Belief 15/15, journey 15/15, book-arc PASS both. Noted factory-speech 17→17 / 38→12.

**Verdict & why.** INCONCLUSIVE. KEEP object closed in both books. Founder veto (blocking factory-speech 0/0) failed in A only — PROGRAM one-book class, not REVERT, not KEEP. Prediction partial.

**What we learned.** A prefix ban can close trap-question labels without deleting the 014 ask-teaching. It does not hold the blocking factory-speech floor at 0/0 when A samples evidence-register at a climax. Plan-card still names `Socratic trap question`; neither book spoke it.

**What this opens next.** Do not promote this line. Founder halt — do not start 019 unless asked.

### iter-019 — Spark 1.3 BASELINE  ·  2026-09-04  ·  BASELINE

**Hypothesis.** None — measurement after the founder pin to Muse Spark 1.3 contributor. Same 009 pattern: a founder model change requires a fresh baseline. Factory files stay at KEEP 014. 015–018 were not re-applied. Word-budget sentence not bundled.

**Change.** None. Research reused. Plan regenerated (13 chapters, `fit to write from` on review r1). Two books on Zen `muse-spark-1.3-contributor-free` (every chapter both replicates; no Vercel fallback). Panel composer-2.5, 40+40. Card headers wrapped `**CH-NN**` after review so the writer parser locates them (014 format).

**What happened.** All lanes PASS, blocking 0 both books. Belief 13/13 both; journey 13/13 both; voice 13/13 both; book-arc PASS both. Noted signal in both: willpower-lexicon 21/33, factory-speech 6/21, journey re-argument 7/5, book-arc re-argument 3/2, belief re-argument 3/1, coach-register 6/3, wrong-register 5/2, copied-mannerism 2/7, pre-debut-spend 1/1. A-only: trap-question-label 3, journey-stall 1. Trace analysis: late-arc plan-card re-owns CH-10 totality jobs in CH-11–13; factory-speech noted hydra persists (instruction-spine serialization + chapter-meta narration); willpower-lexicon is structurally required by the anti-method chapter.

**Verdict & why.** BASELINE. No target cluster. Accepted snapshot is replicate A. 3-strike clock resets. North Star not met (noted floors remain). Continue 020–040.

**What we learned.** Spark 1.3 on KEEP-014 prompts plus a new 13-chapter plan closed blocking in both books. The remaining KEEP surface is noted classes that appear in both books, led by late-arc `re-argument` (plan-card) and `factory-speech` (PERSISTENT).

**What this opens next.** 020 hypothesizer (Fable 5.1 Cursor Task) from this trace. PRIMARY = highest-priority class in both books (belief → arc/journey → voice). Anti-slop may ride secondary only if PRIMARY is factory-speech or a hedge class.

### iter-020 — continuity closed-list + fact-assertion  ·  2026-09-04  ·  INCONCLUSIVE

**Hypothesis.** If every card names the preceding belief as closed and lists settled jobs as one-sentence token echoes only — especially after the vow — journey `re-argument` falls in both books because CH-11–13 stop re-running CH-10 demolitions as a second manual.

**Change.** One bullet in `prompts/master-plan-skill-v2.md` (continuity intent). Secondary: `prompts/style-guide.md` §B5 fact-assertion. Plan regenerated. Research reused. Two Spark 1.3 books. Panel 40+40.

**What happened.** Journey re-argument 7→4 (A) and 5→5 (B). Belief 13/13, journey 13/13, voice 13/13, book-arc PASS both; blocking 0/0. Factory-speech noted 6→6 / 21→4. Book-arc re-argument 3→3 / 2→1.

**Verdict & why.** INCONCLUSIVE. PRIMARY improved in one book only. No both-books new blocking class. Do not promote.

**What we learned.** Journey `re-argument` 7→4 (A) and 5→5 (B) — one book only. Blocking stayed 0/0. Secondary factory-speech 6→6 / 21→4 also one-book. Card-field bind is sampling-sensitive on Spark 1.3. Do not promote. Same PRIMARY eligible with a new mechanism.

**What this opens next.** New mechanism on the same PRIMARY (plan-card re-argument), not this exact continuity sentence. Strikes: 1 on re-argument + plan-skill under Spark 1.3 census.

### iter-021 — writer previous-chapter closed-list  ·  2026-09-04  ·  INCONCLUSIVE

**Hypothesis.** If the writer previous-chapter clause names N−1 as closed except voice-match and one-sentence entry, journey `re-argument` falls in both books versus 019 (A 7, B 5).

**Change.** One clause in `prompts/chapter-writer.md` (see `loop/iterations/021/change.diff`). Plan reused (019, 13 chapters). Research reused. Two Spark 1.3 books (A Zen contributor-free; B Go contributor). Panel composer-2.5, 40+40.

**What happened.** Journey re-argument 7→6 (A) and 5→7 (B). Belief 13/13, journey 13/13, voice 13/13, book-arc PASS both; blocking 0/0. Belief re-argument 3→5 / 1→7. Book-arc re-argument 3→3 / 2→7. Factory-speech noted 6→15 / 21→8.

**Verdict & why.** INCONCLUSIVE. PRIMARY improved in one book only. No both-books new blocking class. Do not promote.

**What we learned.** The hypothesized sentence is not the whole assembled contract: `write_replicate.py` still injects "voice continuity and the handoff seam" as the last assignment line. N←N−1 remains the journey shape. Plan-card still assigns overlapping demolitions the writer cannot refuse.

**What this opens next.** Do not replay this exact clause. Strike 1 on re-argument + writer-prompt (assembled) under Spark 1.3 census. Next mechanism must not be this paragraph alone.

### iter-022 — Binding craft 3 one-sentence handoff  ·  2026-09-04  ·  INCONCLUSIVE

**Hypothesis.** If Binding craft 3 defines settled work and makes one spoken sentence the whole handoff seam, journey `re-argument` falls in both books versus 019 (A 7, B 5).

**Change.** One rule in `prompts/chapter-writer.md` (see `loop/iterations/022/change.diff`). Plan reused (019, 13 chapters). Research reused. Two Spark 1.3 Go-contributor books. Panel composer-2.5, 40+40.

**What happened.** Journey re-argument 7→6 (A) and 5→7 (B). Belief 13/13, journey 13/13, voice 13/13, book-arc PASS both; blocking 0/0. Belief re-argument 3→3 / 1→2. Book-arc re-argument 3→1 / 2→2. Factory-speech noted 6→6 / 21→11. Journey-stall 1→3 / 0→2.

**Verdict & why.** INCONCLUSIVE. PRIMARY improved in one book only. No both-books new blocking class. Do not promote.

**What we learned.** Licensed one-sentence invoke did not close N←N−1 in both books. Plan-card double-ownership (CH-10/11, late-arc) still assigns rebuilds. B mid-arc seams rebuilt despite one-sentence openers.

**What this opens next.** Do not replay Binding craft 3. Strike 2 on re-argument + writer-prompt under Spark 1.3 census. Prefer plan-card next if PRIMARY stays this class.

### iter-023 — one-correction-one-card plan law  ·  2026-09-04  ·  INCONCLUSIVE

**Hypothesis.** If the planner may name a correction on exactly one card and the reviewer blocks any later card that re-opens it, journey `re-argument` falls in both books versus 019 (A 7, B 5).

**Change.** `prompts/master-plan-skill-v2.md` (one-correction-one-card). `prompts/master-plan-reviewer-v2.md` (pair-named reopen gate). Plan regenerated (15 chapters, r2 `fit to write from`). Research reused. Two Spark 1.3 Go books. Panel 46+46.

**What happened.** Journey re-argument 7→6 (A) and 5→5 (B). Named tomorrow pair closed both. Belief 15/15 both; voice 14/15 A (blocking factory-speech 1) and 15/15 B; journey 15/15 A and 12/15 B (`journey-incomplete` 3 B-only). Book-arc PASS both.

**Verdict & why.** INCONCLUSIVE. PRIMARY improved in one book only. One-book blocking is not a veto. Do not promote.

**What we learned.** Folding delay into totality closed the 019 named pair. The class survived via other card overlaps (EV double-routing, T-H triple-ownership per trace). B incomplete landings are one-book.

**What this opens next.** Do not replay this exact one-correction paragraph. Consecutive no-KEEP: 4. New plan-card mechanism if PRIMARY stays `re-argument`.

### iter-024 — room-name-only cards + evidence single-cite  ·  2026-09-04  ·  REVERT

**Hypothesis.** If Compact chapter cards name one style-guide room instead of listing relapse doors/scripts, and every ledger row is cited once, journey `re-argument` falls in both books versus 019 (A 7, B 5).

**Change.** `prompts/master-plan-skill-v2.md` (room-name-only structural responsibility; evidence single-cite). `prompts/master-plan-reviewer-v2.md` (repeated-ID and slot-list blockers). Plan regenerated (16 chapters, r2 `fit to write from`). Research reused. Two Spark 1.3 Go books. Panel 49+49.

**What happened.** Journey re-argument 7→7 (A) and 5→5 (B). Belief 16/16 both; journey 16/16 both; voice 16/16 A and 14/16 B; book-arc PASS both. Both-books late-arc: C-14–16 pink-elephant / blip / pity / FANTASTIC replay. Mid-arc: C-03→C-04 and C-06→C-07 mechanism reruns. Evidence IDs single-use. C-14 `structural responsibility: last ordinary instance` but guardrails still listed pity/slips and debuted AN-03.

**Verdict & why.** REVERT. PRIMARY improved in neither book. B-only blocking is not a veto. Do not promote.

**What we learned.** Binding one card field does not remove the second manual from guardrails, continuity, scene debut, or adjacent-job overlap. Plan-card remains PERSISTENT for this class after 020/023/024.

**What this opens next.** PIVOT off plan-skill card-field binds (3-strike). Do not replay 020–024 named wording. `convergence-report.md` written. Continue 025 under founder override.

### iter-025 — Carr-convergence architecture BASELINE  ·  2026-09-05  ·  BASELINE

**Hypothesis.** None — measure the founder-authorized architecture (chapter reviewer, GSBS comparison lane, 80% length KEEP floor) on the reused 019 13-chapter plan.

**Change.** No writer/planner/style-guide wording. Writer now draft → review → ≤1 rewrite. Panel adds `chapter-comparison`. Research and 019 plan reused. Two Spark 1.3 Go books.

**What happened.** Words A 52182 / B 51144 (019 A was 26984). Belief 13/13, journey 13/13, voice 13/13, comparison 13/13, book-arc PASS both; blocking 0/0. Comparison `missing` 3/3, same three moves in both: G06-M2 (incredible machine), G15-M1 (be selfish), G20-M2 (page-skipper). Journey `re-argument` 12/10 under the repaired section-rebuild definition. Voice floors: willpower-lexicon 29/33, factory-speech 18/16 (ease-operators and card leaks, not chatbot openers). Reviewer REVISE→rewrite 24/26; ACCEPT A ch11, B ch12.

**Verdict & why.** BASELINE. Measurement, not a KEEP test. Length floor met. 3-strike clock resets. Accepted snapshot is replicate A.

**What we learned.** Reviewer made length KEEP-visible: A 52182 / B 51144 vs 019 A 26984 (floor 48000 met both). All-PASS / zero blocking both books. New floors in both: comparison `missing` 3/3 (G06-M2, G15-M1, G20-M2), journey `re-argument` 12/10 (repaired class, still ≥8), willpower-lexicon 29/33, factory-speech 18/16. `coach-register` 3/8 (not ≥8 both). `method-promise-hedge` 0/0. 3-strike resets.

**What this opens next.** 026 anti-slop PRIMARY `factory-speech`. Skip 027/028 (coach-register not ≥8 both; hedges absent). Then attack comparison `missing` in both. Do not replay 020–024 wording.

### iter-026 — anti-slop chatbot residue  ·  2026-09-05  ·  KEEP

**Hypothesis.** If Part B forbids chatbot openers, throat-clearing, summary closers, and stacked-triplet padding, voice `factory-speech` falls in both books versus 025 (A 18, B 16).

**Change.** One operator plus one checklist bullet in `prompts/style-guide.md` (see `loop/iterations/026/change.diff`). Plan reused. Research reused. Two Spark 1.3 Go books with chapter-reviewer. Panel 53+53.

**What happened.** factory-speech 18→13 (A) and 16→8 (B). Words 50404 / 49067. All chapter lanes 13/13 PASS, book-arc PASS, blocking 0/0. Comparison `missing` 3→4 both. Journey re-argument 12→5 / 10→15 (one book only). A-only `trap-question-label` 5. B-only `journey-stall` 3.

**Verdict & why.** KEEP. PRIMARY improved materially in both books. No new both-books failure class. Prediction partial: the named chatbot list was not the 025 leak pattern, but the census class still fell.

**What we learned.** factory-speech 18→13 / 16→8 (drop ≥2 both). Length floor met (50404/49067). Blocking 0/0. No new both-books class. Prediction partial (025 leaks were ease-operators/card titles; count still fell). Comparison `missing` 3→4 both (G04-M1 joined G06-M2/G15-M1/G20-M2). Skip further anti-slop (coach-register 8/6; hedges 0/0).

**What this opens next.** Attack comparison `missing` 4/4. Do not replay 020–024 wording. Do not give GSBS to writer, planner, or chapter-reviewer.

### iter-027 — unpaid belief-moves on four Jobs  ·  2026-09-05  ·  KEEP

**Hypothesis.** If CH-03/08/09/13 Jobs name the four unpaid comparison moves, `missing` falls in both versus 026 (4/4).

**Change.** Four Job tails in `production-books/quit-sugar/master-plan.md` (see `loop/iterations/027/change.diff`). No GSBS IDs. Plan otherwise reused. Two Spark 1.3 Go books with reviewer. Panel 53+53.

**What happened.** comparison `missing` 4→1 (A) and 4→0 (B). G06-M2, G15-M1, G20-M2 PRESENT on A; G04-M1 PARTIAL. A residual miss G06-M1 only. Words 52861 / 51952. All lanes PASS, blocking 0/0. factory-speech 13 / 16 (B rose from 8).

**Verdict & why.** KEEP. PRIMARY improved materially in both. No new both-books material class. Prediction accurate on the three stable misses.

**What we learned.** comparison `missing` 4→1 / 4→0. Targeted G06-M2, G15-M1, G20-M2 PRESENT; G04-M1 PARTIAL (A). Residual A miss is G06-M1 (untargeted). Length 52861/51952. Blocking 0/0. factory-speech 13/16 (B rose). Next PRIMARY is voice noted ≥8 both (willpower-lexicon 28/36 or factory-speech 13/16).

**What this opens next.** 028 from 027 floors. Comparison missing is no longer a both-books PRIMARY. Do not replay 020–024 wording.

### iter-028 — card-header paste ban in instruction voice  ·  2026-09-05  ·  INCONCLUSIVE

**Hypothesis.** If operator 11 forbids pasting card headers, workshop staging, seed/later placeholders, and a numbered plan-index with no spoken body, voice `factory-speech` falls in both versus 027 (A 13, B 16).

**Change.** One sentence on `prompts/style-guide.md` §B5 operator 11 plus one B9 bullet (see `loop/iterations/028/change.diff`). Plan reused. Research reused. Two Spark 1.3 Go books with chapter-reviewer. Panel 53+53.

**What happened.** factory-speech 13→18 (A) and 16→10 (B). Words 52626 / 52802. All lanes 13/13 PASS, book-arc PASS, blocking 0/0. Comparison `missing` stayed 1/0. Every chapter in both books still opens `**IN THIS CHAPTER**` (§B10 anatomy item 1). 027 workshop/seed-later strings did not recur. A ch13 noted factory-speech 7 on a repeated "There is only one honest reading" refrain.

**Verdict & why.** INCONCLUSIVE. PRIMARY improved in one book only. No both-books new material class. Do not promote.

**What we learned.** Banning card-header paste in the sentence operator does not override B10's required `IN THIS CHAPTER` header. A can rise on a different factory-speech mechanism (formula repetition) in the same census class. Grep for the banned strings is not KEEP.

**What this opens next.** Do not replay this operator-11 sentence. Next factory-speech mechanism should change §B10 anatomy (the header the writer is still required to emit), not operator 11 again. PRIMARY stays 027 floors 13/16. willpower-lexicon is not PRIMARY.

### iter-029 — B10 opening-pictures instead of IN THIS CHAPTER  ·  2026-09-05  ·  INCONCLUSIVE

**Hypothesis.** If §B10 no longer requires the workshop header `IN THIS CHAPTER`, voice `factory-speech` falls in both versus 027 (A 13, B 16).

**Change.** One anatomy line in `prompts/style-guide.md` §B10 (see `loop/iterations/029/change.diff`). Plan reused. Research reused. Two Spark 1.3 Go books with chapter-reviewer. Panel 53+53.

**What happened.** factory-speech 13→9 (A, 8 noted + 1 blocking) and 16→18 (B). Words 48477 / 51991. Voice A 12/13 (ch09 FAIL). Comparison `missing` 0/1. Every chapter still opens `IN THIS CHAPTER`. A blocking quote is `10. IGNORE ANYONE WHO QUIT BY WILLPOWER` at a mantra echo.

**Verdict & why.** INCONCLUSIVE. PRIMARY improved in one book only. One-book blocking is not a veto. Do not promote.

**What we learned.** Renaming the B10 slot does not stop the model from emitting Carr's GSBS preview header. Grep for the header is not KEEP. Numbered instruction paste can block even when the preview header is ignored by the judge.

**What this opens next.** Do not replay 028 operator 11 or 029 B10 item 1. Style-guide + factory-speech strike 2 — next try a different component (chapter-reviewer or writer), not a third style-guide header sentence. PRIMARY stays 027 floors 13/16.

### iter-030 — reviewer HEADER finding  ·  2026-09-05  ·  KEEP

**Hypothesis.** If the chapter-reviewer can REVISE a draft that opens with `IN THIS CHAPTER` or a numbered plan-index with no spoken body, voice `factory-speech` falls in both versus 027 (A 13, B 16).

**Change.** One finding type in `prompts/chapter-reviewer.md` (see `loop/iterations/030/change.diff`). Still one rewrite. Plan reused. Two Spark 1.3 Go books. Panel 53+53.

**What happened.** factory-speech 13→9 (A) and 16→7 (B). Words 51753 / 51097. All chapter lanes PASS, book-arc PASS, blocking 0/0. Comparison `missing` 0/0. Reviewer fired HEADER on most drafts; rewrites kept the header in 13/13 A and 12/13 B.

**Verdict & why.** KEEP. PRIMARY improved materially in both. No new both-books material class. Prediction accurate on the census class; grep for the header is not KEEP.

**What we learned.** A one-rewrite HEADER gate can move factory-speech even when the header string survives. Style-guide header sentences (028/029) did not KEEP; the unused rewrite component did.

**What this opens next.** New floors: factory-speech 9/7 (no longer ≥8 both). willpower-lexicon 30/30 is not PRIMARY. No other noted class is ≥8 in both. Do not replay this HEADER finding. Do not start a willpower PRIMARY.

### iter-031 — unpaid comparison halves + CH-13 budget  ·  2026-09-05  ·  KEEP

**Hypothesis.** If the CH-05/06/09/10 Jobs name the unpaid half of each aligned move, and CH-13's budget drops to 1700 so LENGTHEN cannot force a second demolition, comparison `partial` falls in both versus 030 (A 9, B 11).

**Change.** Job and Budget fields in `production-books/quit-sugar/master-plan.md` (see `loop/iterations/031/change.diff`). Two Spark 1.3 Go books with reviewer. Panel 53+53.

**What happened.** comparison `partial` 9→5 (A) and 11→5 (B). Words 52392 / 51940. All chapter lanes PASS, book-arc PASS, blocking 0/0. CH-13 landed 1584 / 1462. G20-M3 stayed PARTIAL both. factory-speech 14/10.

**Verdict & why.** KEEP. PRIMARY improved materially in both. No new both-books blocking class. Prediction accurate on the census class; CH-13 mechanism only partial.

**What we learned.** Cards that omit the second half of a comparison move produce PARTIAL every time. A reminders Job cannot KEEP G20-M3 while a 3800-word LENGTHEN still forces rebuild; cutting the budget stopped the 4000-word rewrite but a short second-pass argument still scored PARTIAL.

**What this opens next.** New floors: factory-speech 14/10 (≥8 both — next PRIMARY). comparison `partial` 5/5 is below the band. willpower-lexicon 34/26 is not PRIMARY. Do not replay 028/029/030 header mechanisms. Do not replay 020–024 wording.
