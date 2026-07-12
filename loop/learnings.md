# Loop learnings — factory-v2 authenticity campaign

The single accumulating memory of the boring loop (see `PROGRAM.md`). One entry
per iteration, appended in Step 4 RECORD — **pass or fail, always**. Intelligence
goes into chapters and diagnosis, never into redesigning the loop. This file is
the diagnosis half.

**Definition of done:** a blind judge told "one of these two chapters is from a
real published Easyway book" guesses at ~50% (detection accuracy → 0.5). Fear,
shame, and medical overreach are FEATURES of authentic Carr to reproduce, not
defects to sand off.

**Instrument (pinned this campaign, `fac-auth-1`):** reward = mean blind pairwise
authenticity win-rate of our chapter vs the matched real *Good Sugar Bad Sugar*
chapter, k=4 order-swapped calls per pair, cross-family judges (never
MiniMax-family). Secondary: blind detection accuracy toward 0.5. Hard checks
(gate-blocking): originality tripwire, mantra/repetition law, ±40% length sanity.
Changing the instrument starts a new campaign with fresh baselines.

---

## Carry-in evidence — run-012 baseline (the sanitization diagnosis)

Run-012 wrote quit-sugar Chapters 1–3 (drafts frozen at
`calibration/runs/run-012/chapters/`). It was judged by the now-RETIRED 3-role
Stage-A v2.3 panel (efficacy / craft / integrity), so its numbers are NOT
comparable to this campaign's reward — but the *pattern* is the reason this loop
exists.

**The panel split (retired 3-role instrument, `judgments/product-v2.3/`):**

| role / target | ours / tie / ref | preference |
|---|---:|---:|
| efficacy / block | 1 / 0 / 3 | **0.25** |
| craft / Chapter 1 | 4 / 0 / 0 | **1.00** |
| craft / Chapter 2 | 0 / 0 / 4 | **0.00** |
| craft / Chapter 3 | 1 / 0 / 3 | **0.25** |
| integrity / block | 4 / 0 / 0 | 1.00 |

Craft **won Ch1 4–0** but **efficacy lost 1–3**, and craft cratered on Ch2/Ch3.
Equal-role macro 0.5556 — cleared the arbitrary 0.45 macro but failed target
non-inferiority, the efficacy floor, and critical safety.

**The sanitization diagnosis (why the old panel optimized AWAY from the target):**
the retired integrity judge flagged the REFERENCE side — the REAL Allen Carr book
— with a critical-failure union of `fear_as_motivator`, `medical_overreach`,
`shame_moralizing` (plus `repetitive_sag`, `unsupported_authority_or_testimony`).
An instrument that punishes authentic Carr for fear/shame/overreach rewards a
*sanitized* imitation. That is backwards. This campaign deletes the role panel
and asks ONE blind question — "which reads more like real Carr, could it pass as
the same author?" — with fear/shame/overreach treated as authenticity signals.

**Choppiness signature (objective diagnostics, reproduced by `score.py`
2026-07-12 against the run-012 fixtures — the numbers match the run-012 report):**

| metric | our drafts (Ch1–3 mean) | real GSBS Ch1–3 mean |
|---|---:|---:|
| mean sentence length | **13.2** | **18.4** |
| short sentences (≤8w) | **45.9%** | **14.7%** |
| second person / 1k | 35.9 | 42.4 |
| questions / 100 sentences | 10.3 | 11.3 |

Our prose is markedly choppier and more interrogative than the real book — a
persistent, measurable voice gap (mean sentence 0.72×, short-sentence share
3.1× the reference). Diagnostic only; never a gate.

**Objective hard-check facts (run-012, confirmed by `score.py`):**
- Originality overlap **0.000%** vs the reference (well under the 0.3% tripwire)
  — the drafts are original, not lifted.
- Repetition law: **3 overlapping 12-gram** non-mantra repeats across Ch1 and
  Ch3 — both chapters followed the scheduled M-01 mantra with the identical
  surrounding sentence "…your right to choose. Read that again." The mantra
  itself is exempt; its identical wrapper prose is not.
- Length: Ch2 ran 4,093w against a 2,800 budget — over even the loose ±40% band.

**Evidence-invention finding (the writer-prior problem):** grounded specialists
found MATERIAL evidence invention in **3/3** first drafts (13 findings in C-01,
6 in C-02, 8 in C-03) — unsupported identities, attribution, prevalence,
counterfactual outcomes, mechanisms, efficacy/closure claims. This survived
FAITHFUL source-grounded commissions. **The four refuted levers agree on one
autopsy:**
- **H-045** (refuted run-008) — two fresh same-model reviews before one revision.
- **H-046** (refuted run-009) — an explicit "evidence ownership > assertiveness"
  priority rule in the writer prompt.
- **H-047** (refuted run-010) — a focused model-authored commission replacing the
  full plan in the writer's context.
- **H-049** (refuted run-012) — source-grounded commissions carrying real packet
  texture and limits.

**Conclusion carried forward: "the Opus completion prior remains sufficient to
invent."** Grounding the commission fixes what the writer KNOWS but does not
constrain its persuasive connective tissue. Note the writer model has since
changed (founder 2026-07-12: MiniMax-M3, cheap iteration) — whether MiniMax
shares this invention prior is itself an open question for a later iteration.

---

## Surviving untested hypotheses (migrated from calibration/hypotheses.md)

These four were never tested and remain live. All are ONE change to ONE tunable
asset (the master-plan prompt / plan), so they fit the loop's one-lever rule.

- **H-001 — explicit per-chapter word budgets.** Nothing forces chapter lengths,
  so book length is emergent. Lever: master-plan assigns every chapter a word
  budget summing to 0.9–1.1× target. Prediction: total-words ratio into ±15%,
  per-chapter deviation < ±20%. (Directly relevant: run-012 Ch2 overshot.)
- **H-015 — per-chapter "objection to kill".** Chapters argue FOR conclusions but
  under-address the reader's live counter-thought, so the click doesn't land for
  skeptics. Lever: each chapter spec names the single strongest reader objection
  it must dissolve. Prediction: authenticity/efficacy rises; judge reasons stop
  citing "asserted, not argued". (Directly relevant: efficacy lost 1–3.)
- **H-016 — reference-shaped length curve vs uniform.** Real Carr books breathe —
  long demolition chapters, short bridges. Lever: master-plan supplies numeric
  curve targets (from reference-metrics.json aggregates; pipeline stays
  text-blind) vs flat budgets, both summing to target. Prediction: pacing/flow
  rise at equal total length.
- **H-017 — mantra debut front-loading.** If debuts spread evenly, late chapters
  debut refrains with no runway to compound. Lever: schedule the majority of
  mantra debuts in the first ~40% of chapters; the back half echoes and
  escalates. Prediction: refrain spine + ending force rise; mantra discipline
  unchanged. (Note: quit-sugar's sheet already front-loads M-01/02/03/06 in CH-01
  — a partial natural experiment.)

Also parked (analysis-only, now first-class): **H-024 — detection probe as
leading indicator.** The probe deleted in instrument v2.2/v2.3 returns as this
campaign's secondary metric; watch whether it moves ahead of the pairwise reward.

---

## Iteration ledger

### iter-001 — FROZEN HYPOTHESIS (pre-registered, do not edit mid-run)

**Change (one lever, already applied to canon):** remove the sanitization layer —
the guardrail flip that stops treating fear / shame / medical-overreach as
defects to avoid and instead allows the authentic Carr register. The flip is
already in the tunable assets (style guide / writer prompt guardrails).

**Prediction:** vs the run-012 baseline, BOTH the pairwise authenticity win-rate
AND belief-change efficacy jump — because the previous drafts were optimized by
an instrument that punished the very features that make Carr read as Carr.
Concretely: pairwise reward > 0.5 (our chapters start winning some pairs against
the real book) and detection accuracy moves toward 0.5.

**How it will be measured:** `score.py --book production-books/quit-sugar
--chapters 1-3 --iter 1` under `fac-auth-1` with judge keys present; then
`gate.py --iter 1`. iter-001 is the first real reward of the campaign, so the
gate accepts it as the baseline (first-iteration rule) provided hard checks pass.

**Result:** — (pending: requires OPENROUTER_API_KEY for the judges and a MiniMax-M3
write pass; hard checks + diagnostics already run clean in DRY-RUN.)
