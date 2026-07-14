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

## 2026-07-13 — instrument change + campaign reset (founder direction)

- **The pairwise/detection instrument is retired before ever measuring an iteration.** Founder reasoning: this is not an A/B contest — Easyway IS the goal, so "ours beat Carr's in a judge's opinion" proves nothing. Replaced by the **reference-anchored carr-likeness rubric** (`calibration/judges/carr-likeness-rubric.md`): the judge sees the real GSBS chapter as ground truth beside our candidate, scores DISTANCE from the reference on six anchored dimensions, and returns 3–5 concrete improvement suggestions tagged with the owning asset. The suggestions drive each iteration's ONE amendment.
- Campaign reset: `factory-v3-rubric-1`, instrument `carr-likeness-rubric-1`. results.tsv restarted (new columns incl. worst_dimension + top_suggestion).
- **MiniMax-M3 writer note RESCINDED** — founder mix-up from another project. Model matrix (PROGRAM §1): writer Opus 4.6 reasoning-none via OpenRouter; research DeepSeek V4 Pro via OpenRouter; planner + judges GPT-5.6 Sol xhigh as fresh NATIVE CODEX subagents (founder subscription) — GPT models never via OpenRouter.
- Best-of-both merge: deep Carr-fidelity style guide (all five §4 forks flipped to Carr's practice) + fidelity doctrine note; owner-branch writer/reviewer retrofits kept (sanitization + fear-then-relief blockers); owner-branch 10× research engine kept; retired-lab operator docs deleted (HARNESS/STATE/ESCALATION/hypotheses + old judge prompts); runs/ + FAILURE-ANALYSIS kept as archaeology.

## Seed hypotheses (evidence: the retired lab's one valid measurement, run-012)

Chapter 1 craft BEAT the real GSBS 4–0 blind; efficacy lost 1–3; Chapters 2–3 sagged (repetitive_sag, weak_ending_handoff); all chapters missed length budgets; prose ran 3× choppier than Carr (46% short sentences vs his 15%).

1. **iter-001 = Carr-fidelity baseline.** The old style guide's sanitized forks (no personification, autonomy-instead-of-command, softened scares) plausibly caused the efficacy gap. The v3 flip is already applied — iter-001 regenerates chapters 1–3 fresh (research + accepted plan R2 reused) and measures the flipped baseline. Hypothesis text for the ledger: "Carr-fidelity baseline — v3 style guide, rubric instrument".
2. **Rhythm:** short-sentence pulse overdriven everywhere instead of clustered at 1–3 peaks; Carr's default is flowing certainty (~18-word sentences). Candidate asset: style-guide §B5.
3. **Later-chapter sag:** sections catalog instead of escalate; every section must advance the one belief-move a notch; end on a hand-off seam. Candidate asset: chapter-writer anatomy or master-plan chapter cards.
4. **Length control:** writers miss per-chapter budgets; make the budget echo louder in the chapter card or writer contract.

## Harness debt (operator grievances — founder reads between blocks)

- `prompts/master-plan-skill-v2.md` and `prompts/master-plan-reviewer-v2.md` still contain pre-v3 lines that reject the mandatory Carr personification; the iter-001 agents had to follow the newer PROGRAM/style-guide founder law explicitly.
- The generated mantra table used semantically clear headers (`Frozen exact wording`, `Echo route`) that the hard-check parser does not accept; the planner repaired them mechanically to `Frozen wording` and `Echo chapters` with no semantic change.
- `gate.py` checks for a non-null reward before honoring hard-check failure, then prints generic tunable/plan checkout and score-deletion commands even for the zero-amendment cold start. Those commands would restore the explicitly deprecated plan and delete a required iteration record, so no nonexistent amendment was reverted.
- There is no canonical Opus chapter-revision transport after a reviewer returns `REVISE`; iter-002 required ad-hoc guarded runners, and tuple/JS handoff errors plus one plan-concurrency mismatch wasted model completions without changing files.

## 2026-07-13 — external pre-flight review: 6 critical + 4 high findings, all fixed

An independent static review (full report in the founder's thread) found the loop NOT READY. Fixes applied the same day, before any iteration ran:
- **Writer contract (C1):** API wrapper now appends an explicit output contract (reply = the whole chapter, nothing else), strips code fences, and hard-fails on <800-word replies. chapter-writer.md gained an API-dispatch-mode section (SPEC GAP: line convention).
- **Stale plan register (C3):** framing.md + master plan R2 were written under the retired sanitized register (no-fear/no-command/no-creature, autonomy-led). iter-001 cold start (PROGRAM §4.0) now regenerates framing forks + plan under the v3 Carr defaults before writing. R2 is DEPRECATED as a writing input.
- **Commit/revert ordering (C2):** iteration order is now AMEND (uncommitted) → RUN → SCORE → GATE → RECORD+COMMIT (amendment committed only if kept). gate's checkout commands now genuinely restore; gate prints the real book's plan path; --asset sharpens the commands.
- **Verdict filenames (C1):** emit prints an explicit task→verdict path mapping per file; WAITING lists missing stems.
- **Rubric information gap (C2):** judge tasks now embed the candidate's frozen mantra sheet + chapter plan card ({{CONTEXT}}); rubric instructs dims 3–4 to score against them (control runs get a defined fallback). Instrument amended pre-baseline — no rebaseline needed (zero scored iterations existed).
- **Near-copy + reference exposure (C4):** new hard check — word-sequence similarity vs the matched reference chapter (near_copy_tripwire 0.5) catches paraphrase-spaced copying that defeats exact 12-grams; judging/tasks/ dirs (which embed reference text) are now gitignored.
- **Research scope (H):** research amendments are out of scope during unattended blocks — recorded as block-boundary proposals instead (PROGRAM §3).
- **Suggestion pipeline (H):** verdicts now require exactly 3–5 suggestions with whitelist asset tags (else the single judge task is re-dispatched); aggregation is rank-weighted with chapter-spread tie-breaks.
- **Wrapper flow + exit codes (H):** run_iteration stops after writing for the ≤2 reviewer cycles (resume --no-write; --score-now for controls); gate exits 0 on every decided verdict incl. REVERT.
- **Style-guide stragglers (H):** §7 Fork-1 vocabulary line, §10 step 6 default, §11 autonomy-close annotation, §12 ask-vs-assert checklist item — all aligned to the v3 Carr defaults.

Reviewer's noise estimate: pure-noise reward movement plausibly 0.017–0.05; epsilon 0.03 stays a placeholder pending the three-repeat measurement.

## 2026-07-13 — instrument ceiling check

The reference-as-candidate control for Chapters 1–3 scored **1.000** across all six fresh native judge verdicts (every anchored dimension 10/10), with hard checks green. This confirms the frozen rubric ceiling; this first control sample showed zero observed judge spread. No gate was run and no product baseline row was added.

### iter-001 — Carr-fidelity baseline

**Outcome:** `FAIL-HARD` at **0.6217**; all six judges voted `emotional_register` worst. Originality, mantra scheduling, and length passed. The hard failure was one non-mantra sentence fragment repeated across Chapters 2–3. There was no amendment to revert, so the Carr-fidelity cold-start framing, plan, and scored chapters remain as the iteration artifacts.

**Judges' top suggestions (verbatim):**

1. `[chapter-writer]` Rewrite the repeated 'test' and 'investigation' framing, especially the concession 'What you do with that clarity is yours,' so each reader objection is answered by a settled fact, a trap question with only one honest answer, and a cheerful command.
2. `[style-guide]` Forbid the permission-and-caveat register exemplified by “What you do with that clarity is yours” and “that care outranks every word”; require settled-fact assertions and cheerful commands once a claim is within the book’s evidence boundary.
3. `[chapter-writer]` Make each major section end in a blunt compression of the belief move: after THE CONFIDENCE TRICK and THE SUGAR TRAP, replace one explanatory paragraph with a short verdict line, and make the next section escalate it rather than reopen it.
4. `[chapter-writer]` In 'THE COUNTERFEIT MEMBERSHIP CARD' and 'THE CONFIDENCE TRICK,' stop re-explaining the same deal metaphor: move through two or three sharply different concrete observations, force each through a trap question, and end the sequence with a short ALL-CAPS verdict.
5. `[style-guide]` Replace the repeated reservations around "If it does" and "following the evidence wherever it leads" with one ventriloquized objection followed by a flat settled-fact answer; keep conditionals in the reader's objection, not the narrator's conclusion.

**Reviewer residuals at the two-cycle cap:** Chapter 1 — mantra infidelity, illicit repetition, missing anatomy, evidence overstatement. Chapter 2 — mantra infidelity, re-argument/job drift, missing anatomy, evidence overstatement. Chapter 3 — mantra infidelity, job drift, narrator hedging, missing anatomy, evidence overstatement. No reviewer found a master-plan spec gap. Plan-review residuals: CH-14 evidence/certainty balance; CH-20 hand-off density.

**Next hypothesis (`chapter-writer`):** The writer contract's investigation/permission framing leaves the narrator conditional and autonomy-led. Require conditionals to remain inside ventriloquized reader objections, then answer each with **settled fact → trap question → cheerful command**, and forbid narrator-side outcome permission or caveat language. Prediction: `emotional_register` and `voice_certainty` rise, sections escalate instead of reopening the case, and the recurring test-language sentence disappears.

### iter-002 — objection-only conditionals

**Outcome:** `BASELINE` at **0.6658** with every hard check green, a **+0.0441** lift over iter-001's diagnostic score. `emotional_register` remained worst (4 votes), followed by `voice_certainty` (2). The kept amendment is `prompts/chapter-writer.md`. A non-semantic plan scheduling defect was corrected during RUN so CH-03 alone owns the exact justification menu; CH-02/CH-07 paraphrase it.

**Judges' top suggestions (verbatim):**

1. `[chapter-writer]` Replace the hedge cluster around 'That question stays open,' 'Does looking guarantee a result? No,' and 'the possibility — not the guarantee' with one brief open-mind invitation followed by flat conclusions and direct answers to the reader's objections, so the chapter's belief move actually lands.
2. `[style-guide]` Replace the repeated hedge-contract sequence — "If the investigation finds...", "Does looking guarantee a result? No", and "the possibility — not the guarantee" — with one ventriloquized objection, a trap question, and a flat settled-fact answer.
3. `[chapter-writer]` Delete the evidence-reporting tails after "the holding, the lapse, the slide" and "reduced decision time and not missing desserts"—especially "one person's experience, not everyone's" and "not a promise and not a prediction"—and state the observed pattern once in a settled voice before posing the trap question.
4. `[style-guide]` Remove the narrator's evidence-lawyer interruptions—"That is one person's experience, not everyone's," "For many of us," and "not a promise and not a prediction"—once a claim is within its evidence boundary; either state the bounded observation flatly or cut it, so the chapter never retreats from its own verdict.
5. `[style-guide]` Strip the parenthetical source-status labels from THE INVESTIGATION MENU and let each objection speak directly in the reader's voice; keep provenance outside chapter prose so the spell is not broken by research-report language.

**Reviewer residuals at the two-cycle cap:** Chapter 1 — evidence overstatement and scope-definition contradiction. Chapter 2 — spec omission, evidence overstatement, qualifier creep. Chapter 3 — evidence integrity, job drift/assignment trespass, illicit repetition, qualifier creep. The single plan review left later-card mantra-route and J-05 ownership objections; no remaining blocker targeted Chapters 1–3.

**Next hypothesis (`style-guide`):** Provenance narration and source-status caveats make the escaped expert sound like an evidence lawyer. Keep provenance and grading labels outside chapter prose; once the plan places an observation inside its evidence boundary, the narrator must **state the bounded observation flatly or cut it**, preserving contested scope through precise wording rather than retreating caveats. Prediction: `emotional_register` and `voice_certainty` rise without weakening evidence integrity.

### iter-003 — provenance outside prose

**Outcome:** `FAIL-HARD` at **0.5783**, **-0.0875** below the accepted iter-002 baseline. `emotional_register` was worst in 5 votes and `voice_certainty` in 1. Originality and length were green, but the hard gate found no parseable mantra sheet after the spec-gap plan rerun plus repeated non-mantra 12-grams. The `prompts/style-guide.md` amendment and regenerated plan were reverted; the accepted iter-002 plan is active again.

**Judges' top suggestions (verbatim):**

1. `[chapter-writer]` At 'That question has only one honest answer. But I am not going to give it to you yet,' stop postponing the chapter's belief move: force the trap question to its answer, reassign the claimed benefit to its real source, and compress that answer into a blunt verdict line.
2. `[style-guide]` Replace lines such as "That exhaustion is real. It is valid." and "That is not a slogan. It is a testable claim." with flat settled-fact assertions, then issue the next command cheerfully; remove therapy and evaluation vocabulary wherever the argument already knows its answer.
3. `[chapter-writer]` Compress the policy-toned opening of "BUT I AM POWERLESS"—especially "Let me be very careful here" and the two numbered truths—into one brisk boundary sentence, then return immediately to direct-address assertion and dismantling of the trap; apply this rule whenever necessary safety language interrupts the narrator's settled voice.
4. `[chapter-writer]` Compress the multi-paragraph "Let me be very careful here" and "two things are true at once" disclaimer into one narrow boundary sentence, then answer the reader's objection in flat, categorical language so a necessary safeguard does not take over the chapter's voice.
5. `[chapter-writer]` In "TWO HONEST CONCESSIONS" and "KEEP EACH SCENE IN ITS LANE," stop repeating what the chapter will not decide: drive one concession through credit reassignment to an unavoidable conclusion, then state that conclusion in one short verdict line.

**Reviewer residuals at the two-cycle cap:** Chapter 1 — evidence overstatement/provenance narration, unsupported external attribution, qualifier creep. Chapter 2 — mantra infidelity/both-sides qualification, illicit repetition, invented evidence/premature mechanism work, clinical-perimeter violations. Chapter 3 — mantra infidelity and missing anatomy/SUMMARY mantra fidelity. No final chapter review found a master-plan spec gap.

**Plan recovery:** The first Chapter 3 review exposed a genuine contradiction between the amended style guide and the accepted plan's source-status instruction. The exact-input plan stage was rerun and received its one allowed review. Residual objections were EV-L06/SLOT-06/CH-06 testimonial limits; MAN-01/MAN-02/CH-02/CH-16/SLOT-13/CH-14/JUST-09–JUST-15 routing contradictions; and the CH-22 concrete handoff. PROGRAM required proceeding after that single review; the resulting plan later failed the mantra parser and was reverted by the hard gate.

**Next hypothesis (`chapter-writer`):** Strict chapter ownership is leaking into reader-facing postponement. Require every argument-bearing chapter to complete its present-tense value correction before the handoff: force the decisive trap question to its answer, reassign the claimed benefit, state the inversion as settled fact, and compress it into the scheduled verdict; later chapters may unpack support but may never be advertised as the place where today's conclusion will finally be decided. Prediction: `emotional_register` and `voice_certainty` rise while roadmap hedges and “not deciding today” deferrals disappear.

**Harness debt:** When a failed iteration reruns the plan, `gate.py` prints a restore for `master-plan.md` but omits its paired `master-plan-review.md`; the operator restored the paired review manually to avoid a mismatched accepted state. The planner prompt also does not guarantee the exact mantra-table surface syntax required by the frozen score parser, so a semantically populated regenerated plan can hard-fail as “no parseable mantra sheet.”

### iter-004 — complete the value correction now

**Outcome:** `NEW-BEST` at **0.6675** with every hard check green, **+0.0017** over the accepted iter-002 baseline. Mantra fidelity rose sharply (Chapter 1: 9.0; Chapter 2: 9.0; Chapter 3: 8.5), while `emotional_register` remained worst in 4 votes and `voice_certainty` in 2. The kept amendment is `prompts/chapter-writer.md`.

**Judges' top suggestions (verbatim):**

1. `[chapter-writer]` Compress the paragraphs beginning "I should be equally clear about the authority behind it" and the later "bounded reports" asides into one brief honesty boundary, then state the core conclusion as settled fact; repeated audit language mechanically brakes the direct-address authority.
2. `[chapter-writer]` Replace the two meta-authority passages beginning "I am not going to open with a dramatic personal escape" and "Every important boundary will stay visible" with a brief direct-address sequence of assertion, reader objection, answer, and verdict; keep provenance limits outside the narrative voice so the chapter speaks in settled facts.
3. `[chapter-writer]` In 'WHAT THE ACCOUNTS ACTUALLY SHOW,' cut the disclaimer cluster beginning 'Neither account proves' and state only the narrow fact the evidence supports in one plain sentence before driving immediately into the trap question and verdict.
4. `[style-guide]` Ban clusters of research-lawyer diction exemplified by "bounded accounts", "universal mechanism", "clinical syndrome", and "active catalogue"; allow one plain boundary sentence, then require a direct claim or trap question.
5. `[chapter-writer]` Rewrite the source-status passages in "THE INVESTIGATION MENU" as compact objections spoken in the reader's dialect; keep provenance out of the narrative voice, then drive each group into one short verdict instead of repeatedly classifying quotations, synthesis, and logic.

**Reviewer residuals at the two-cycle cap:** Chapter 1 — `ACCEPT`, no residual blockers. Chapter 2 — unsupported causal provenance/universalization, bounded accounts converted into a shared mechanism, and CH-05 anti-method reargument with unsupported inevitability. Chapter 3 — unlicensed universal reader/prevalence claims and a missing body ALL-CAPS verdict landing. No reviewer found a master-plan spec gap.

**Next hypothesis (`chapter-writer`):** Evidence-honesty guardrails are leaking into reader-facing audit prose. Permit at most one plain boundary sentence for an evidence item or cluster, then state only the narrow supported fact and drive immediately into the trap question and verdict; forbid narrator-side meta-authority, provenance/grading narration, and stacked catalogues of what the evidence cannot prove. Prediction: `emotional_register` and `voice_certainty` rise without weakening evidence integrity, while the research-lawyer diction disappears.

### iter-005 — one plain evidence boundary

**Outcome:** `REVERT` at **0.6333** with every hard check green, **-0.0342** below the 0.6675 best and just outside epsilon. `voice_certainty` and `emotional_register` split the six worst-dimension votes 3–3. The `prompts/chapter-writer.md` amendment and regenerated plan were reverted; iter-004 remains the accepted state.

**Judges' top suggestions (verbatim):**

1. `[style-guide]` Replace caveat cascades like "It is not a clinical trial. It is not proof... It is not a guarantee" with one concise limitation, then pivot immediately to a flat settled claim and a cheerful direct command; preserve evidence honesty without letting qualification become the narrator's dominant register.
2. `[chapter-writer]` Compress the caveat run beginning "One person I can point to" to one adjacent limitation, then return immediately to flat assertions and the I/we/you triangle; do not let procedural qualification become the chapter's dominant voice.
3. `[chapter-writer]` In 'FOUR DOORS THAT LOOK THE SAME FROM OUTSIDE,' replace the stacked caveats—'a single self-reported account, not a trial, not proof of universal ease' and 'None of these is proof'—with one brief evidence boundary, then return immediately to flat, settled-fact narration.
4. `[chapter-writer]` Compress the clustered proof-limit language in "Early signals" and the fourth-door account into one brief boundary after the evidence; let the surrounding paragraphs state the chapter's belief conclusion as settled fact and end on a short verdict rather than another qualification.
5. `[chapter-writer]` Rewrite the caveat clusters in A PERFECTLY REASONABLE DEFENSE and THE CASTING DIRECTORS—especially "I respect it," "does not prove," and "not a verdict I am going to rush"—as one flat assertion followed by one warm reassurance, so each objection ends in certainty rather than negotiated balance.

**Reviewer residuals:** Chapter 1 — unsupported evidence/causal claims, EV-09 overreach, job drift, BAD SUGAR boundary mismatch, missing safety box, and an M-02/EV-09 plan tension; its one revision failed frozen-mantra validation and was not saved. Chapter 2 — EV-06/07/09/10 overreach, Chapter 1 re-argument, and missing body verdict; its one revision failed evidence validation and was not saved. Chapter 3 — after one saved revision, overstated EV-14/EV-05/EV-22, unsupported causal learning mechanism, and a CH-03/EV-20/EV-21/CH-15 plan tension remained at cycle cap.

**Plan recovery:** A Chapter 1 reviewer found an ST-01/EV-L13/AN-17 routing gap, triggering an exact-input plan rerun. The first candidate's valid nested review found mantra-route contradictions; a later Chapter 1 review exposed PG-CH01-RV12-EVL08, triggering a second exact-input rerun. The final 22-chapter/61,600-word plan had no unresolved routing mechanically, while its one review left later-card residuals at M-03/CH-11 and INS-09/INS-12/CH-21. The gate reverted the plan and paired review. One invalid plan review accidentally ran against the outer clone; its file was immediately restored and the verdict discarded before the valid nested review.

**Next hypothesis (`chapter-writer`):** The writer leaves two outcomes equally live after stating an evidence boundary, so the chapter ends in suspended judgment. After the single necessary limit, require the strongest reader objection in their dialect, two or three trap questions whose answers force concession, the credit inversion, and one short settled verdict; forbid open forks such as “if the claim survives / if it does not” at the chapter's belief landing. Prediction: `voice_certainty`, `method_execution`, and `emotional_register` rise without weakening evidence honesty.

**Harness debt:** Exact-input plan reruns can consume most of the 40-call budget while introducing new routing gaps unrelated to the tested prose amendment. Revision transport also discarded two completed Opus outputs after fail-closed validation; this protected the chapters but left no canonical raw-output recovery path. Fresh subagents must receive the absolute nested repo path because the outer clone is also a valid Git worktree.

### iter-006 — close the open fork

**Outcome:** `KEEP` at **0.6542** with every hard check green, **-0.0133** below the 0.6675 best and inside epsilon. Chapter 2 rose to **0.7325**, while Chapter 1 remained the drag at **0.5525**. All 6 judges selected `emotional_register` as the worst dimension. The amendment to `prompts/chapter-writer.md` stays; the best remains iter-004.

**Judges' top suggestions (verbatim):**

1. `[chapter-writer]` Rewrite the caveat stack in 'A BOUNDED POSSIBILITY' ('not proof, not a promise', 'what it can and cannot show', 'If a finding is contested') as one brief qualification followed by flat settled-fact assertions and cheerful direct commands.
2. `[research]` Rewrite the caveat stack in "A BOUNDED POSSIBILITY" so one concrete, high-stakes fact lands at full force first, then explicitly disown fear as the reason to change; do not let "not proof, not a promise" and repeated study limitations consume the emotional peak.
3. `[style-guide]` Confine mandatory qualifications to the assigned instruction block; in the main argument, replace retreats such as 'That single account does not prove everyone's experience,' 'though it may,' and 'I am confident you will see' with flat settled-fact assertions followed by trap questions.
4. `[chapter-writer]` At "That single account does not prove everyone's experience" and "though it may," stop narrating evidentiary caution inside the persuasion: retain only a genuinely required qualification, then follow the example with a flat settled-fact verdict.
5. `[chapter-writer]` In "THE INVESTIGATION MENU", compress provenance phrases such as "small qualitative study" and "not a clinical diagnosis and not a prevalence claim" into unobtrusive clauses, then state each reader objection in plain spoken language and answer it with settled-fact certainty.

**Reviewer residuals at the cap:** Chapter 1 — invented testimony/evidence overreach, premature paraphrased IN-02, early/reused analogies, CH-05 anti-method job drift, and a “no quitting yet”/IN-02 ownership ambiguity. Chapter 2 — evidence overreach, hedged core reframe, job/evidence-owner drift, assigned-evidence omission, and one corrupted character; no planner gap. Chapter 3 — MN-04/MN-02 casing, altered IN-03 and J-04 exact text, unsupported “emotional lift” attribution, plus an instruction-numbering presentation tension.

**Research proposal deferred:** The rank-2 suggestion asks for new research-backed hard-stakes material. PROGRAM §3 forbids unattended research regeneration, so it is recorded for the next founder-approved research boundary and the next eligible prompt/style suggestion is used instead.

**Next hypothesis (`style-guide`):** Academic and legal-process diction is suppressing the escaped expert's emotional authority even when the logic lands. Ban institutional abstractions in reader-facing prose—terms such as “categorical core,” “transparent evidence,” “qualitative study,” and “prevalence claim”—and require any necessary evidence status to be translated into ordinary I/we/you language as concrete observation → reader objection → trap question → short verdict. Prediction: `emotional_register`, `voice_certainty`, and rhythm rise without weakening evidence honesty.
