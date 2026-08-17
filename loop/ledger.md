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
