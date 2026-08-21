# Experiment Ledger

> The full story of every experiment the loop has run — written so a human (or
> a fresh agent) can read it top to bottom and understand not just *what
> happened* but *why*, and *what to try next*. This is the learning record of
> the whole campaign.
>
> **How it relates to the other records:**
> - `loop/results.tsv` — the canonical machine row (one line per iteration).
>   The verdict and lesson here are copied from it, never re-worded.
> - `loop/learnings.md` — the terse non-repeat log the *hypothesizer* reads.
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
