# Trace Analysis — Iteration 023

## Census merge vs 019 baseline

| Lane / class | 019 A | 019 B | 023 A | 023 B | Merged Δ | KEEP note |
|---|---:|---:|---:|---:|---|---|
| journey `re-argument` (noted) | 7 | 5 | 6 | 5 | 12→11 | PRIMARY object: A improved, **B flat** → KEEP fails |
| belief `re-argument` (noted) | 3 | 1 | 2 | 3 | 4→5 | Worse merged |
| book-arc `re-argument` (noted) | 3 | 2 | 2 | 2 | 5→4 | Slight drop |
| journey `journey-incomplete` (blocking) | 0 | 0 | 0 | 3 | 0→3 | B-only noise |
| voice `factory-speech` (blocking) | 0 | 0 | 1 | 0 | 0→1 | A-only noise |
| book-arc `pre-debut-spend` (noted) | 1 | 1 | 1 | 1 | 2→2 | Flat |

**Hypothesis seam check:** CH-10→CH-11 tomorrow/delay double-ownership — **absent** in both books (journey/belief/arc judges all score `re-argument 0` on ch10 and ch11). That 019 PRIMARY cluster is closed. Journey `re-argument` did not fall in **both** replicates; new both-books clusters replaced it.

---

## Cluster summary

| Causal cluster | Spread | Judge sources | Root component | Priority reason |
|---|---|---|---|---|
| EV-13 men's-mood paragraph (C04→C05) | systemic | A journey-ch05, book-arc; B journey-ch05, book-arc | plan-card | Highest-count both-books `re-argument`; survives new one-correction law |
| Accidental-blip / T-H doctrine (C10/C13→C14) | systemic | A journey-ch14, belief-ch14; B journey-ch14 | plan-card | Late-arc `re-argument` in both books; replaces old CH-10/11 seam |
| Willpower-method re-demolition (C11→C12) | positional (late) | A journey-ch12; B journey-ch12 | plan-card | Same late-arc pair in both books |
| Relief-not-benefit mechanism (C02→C03) | systemic | A journey-ch03; B journey-ch03 (+ B book-arc C03→C07 variant) | plan-card | Early-arc `re-argument` in both; B adds SA-01 restage |
| Afternoon-loan variant of relief beat (C03→C04) | local (A) | A journey-ch04 | plan-card | A-only; sampling noise |
| Early conned-not-flawed re-proof (C01→C02) | positional (early) | A journey-ch02, belief-ch02; B belief-ch02 | plan-card / model | Belief in both; journey overshoot B-only (see below) |
| Withdrawal-shake courtroom (C07/C10→C12) | positional (late) | A book-arc only | plan-card | A-only; sampling noise |
| SA-09 cinema pre-debut in C05 | systemic (noted) | A book-arc; B book-arc | model | Both books; noted only |
| SA-01 party-shoes full restage (C03→C07) | local (B) | B book-arc | model | B-only; card says token echo |
| Journey leaving-belief overshoot | local (B) | B journey-ch02, ch03, ch05 (blocking `journey-incomplete`) | plan-card | B-only blocking; not KEEP veto |
| M-D echo template garble | local (A) | A voice-ch05 (blocking `factory-speech`) | plan-card | A-only blocking |
| Body-hunger / trap-mechanics N←N−1 rebuilds | local (B) | B belief-ch07, belief-ch09 | model | B-only; may hold B journey count flat |

---

### EV-13 men's-mood paragraph (C04→C05)

**Judge sources:** A journey-ch05 (`re-argument` 1), A book-arc (`re-argument` men's mood); B journey-ch05 (`re-argument` 1), B book-arc (`re-argument` low-mood epidemiology)

**Shared symptom:** Near-verbatim men's cohort mood scare runs twice:
- C04: *"In one long look at men, those who ate sweets day after day were more likely to feel low and flat in the months and years after."*
- C05: *"In one long look at men, those who ate sweets day after day were more likely to feel low and flat months and years later."* (B: *"Men who ate sweet treats every day were more likely to find low mood waiting for them in the years that followed."*)

**Distinct effects:** A book-arc also flags C12 withdrawal re-litigation (separate cluster). B pairs this with party-shoes arc finding, not withdrawal.

**Root component:** plan-card

**Evidence:** Accepted plan assigns **EV-13** on **both** cards:
- C-04 evidence: `EV-13 treat predicts mood in men`
- C-05 evidence: `EV-13 mood link plus men-only limit`

Justification menu maps *fuel frame → C04* and *reward frame → C05* but does not exclusive-route EV-13. Plan reviewer r2: `Evidence: PASS — EV-01 to EV-21 single-use` — yet both cards carry EV-13. Writer executes both assignments (A ch04/ch05 responses).

**Mechanism:** Planner double-assigns the same evidence unit to adjacent demolition cards. New one-correction law targets *justifications / relapse doors / valuations* in enacted transitions; **evidence-row duplication is outside that test**, so reviewer passes and writer re-prosecutes the same scare block.

**PERSISTENT — plan-card** has been root cause for `re-argument` across 019–023 (5 iterations). The one-correction law closed the tomorrow seam but not evidence/evidence-routing overlap.

---

### Accidental-blip / T-H doctrine (C10/C13→C14)

**Judge sources:** A journey-ch14, A belief-ch14 (`re-argument` 1 each); B journey-ch14 (`re-argument` 1)

**Shared symptom:** Full blip/rumble-strip paragraph in C14 repeats C13 almost verbatim:
- C13: *"If by accident some BAD SUGAR passes your lips… Your body copes with the blip. Your mind simply does not reopen the door."*
- C14: *"And if by accident some BAD SUGAR passes your lips… Your body can cope with a blip, but your mind must never reopen the door."*

**Distinct effects:** Belief judge (A) treats it as re-proof of settled accidental-blip token; journey judges call consolidation overlap.

**Root component:** plan-card

**Evidence:** Plan triple-owns margin doctrine:
- C-10: debuts `T-H` + `SA-08` full staging in totality chapter
- C-13 responsibility: `two relapse doors guarded as owned thoughts` (writer assigns full blip prose)
- C-14 responsibility: `slip pre-forgiven as rumble strip never licence` + mantra echo `T-H`

First contradiction: C-13 assigns **new** blip-door prose after C-10's enacted transition already debuted T-H as settled margin doctrine.

**Mechanism:** One-correction law forecloses *doors named in an earlier enacted transition*; T-H is debuted as margin/token in C-10, then C-13/C-14 each assign fresh blip encounters instead of frozen-token receipt. Writer follows card responsibilities; downstream chapters re-argue.

---

### Willpower-method re-demolition (C11→C12)

**Judge sources:** A journey-ch12 (`re-argument` 1); B journey-ch12 (`re-argument` 1)

**Shared symptom:** C12 re-runs Willpower-vs-easy transition after C11 settled it:
*"It is the voice of the Willpower Method. / That method taught you that escape must be earned by pain…"* (A)
*"Or that freedom comes from the Willpower Method, forcing yourself daily not to have a wonderful pleasure…"* (B)

**Distinct effects:** Belief judges score `re-argument 0` on ch12 (new FAQ beats absorb overlap); journey lane counts the Willpower block as momentum drag.

**Root component:** plan-card

**Evidence:** Justification menu: *born-this-way / willpower-shame / fear → C11*; *method-too-good → C12*. C-12 `resolves` line still lists objections that re-open method comparison; C-12 mantra echoes `T-A "the Willpower Method"`. C-11 job already completes *past failures seen as Willpower Method*.

**Mechanism:** C-11 owns willpower demolition; C-12's Q&A bucket and T-A echo license a second full Willpower contrast. Reviewer passed (`justification menu mapped once each`) because menu maps *categories* but C-12 `resolves` and structure still name the settled valuation.

---

### Relief-not-benefit mechanism (C02→C03)

**Judge sources:** A journey-ch03 (`re-argument` 1); B journey-ch03 (`re-argument` 1), B book-arc (`re-argument` party-shoes C03→C07)

**Shared symptom:** Dose-relief inversion re-proved at paragraph scale after C02/C03 debut:
- A ch03: *"A dose creates a faint, fretful low. The next dose briefly ends that low. We thank the dose for the lift."*
- B ch03: *"They gave you pain, then lent you the relief… To call them pleasurable because taking them off felt marvellous would be upside down."*

**Distinct effects:** B book-arc adds C07 full SA-01 party-shoes restage (separate local cluster, model).

**Root component:** plan-card

**Evidence:** C-03 job: `evaluation switches from harm-balance to demanding any genuine benefit`; C-03 scene: `SA-01 debut full staging` (shoes = relief-not-benefit flagship). C-02 already runs swimmer/rescuer-pusher (same mechanism). Cards do not mark SA-01 mechanism as settled at C-02; C-03 legitimately re-enters the inversion as its whole job.

**Mechanism:** Adjacent cards own distinct *encounters* but the same *belief correction* (relief mistaken for benefit). New law's "one correction, one card" is not enforced on mechanism-level corrections when encounters differ — planner regenerates early-arc double-ownership in a new shape.

---

### Afternoon-loan variant of relief beat (C03→C04) — A only

**Judge sources:** A journey-ch04 (`re-argument` 1)

**Shared symptom:** C04 re-runs Ch3's relief-not-benefit move on afternoon fuel: *"It was relief from a restlessness the previous dose had left behind, sold back to you as help. A loan, not a wage."*

**Root component:** plan-card (same mechanism class as above; A-only sampling)

**Evidence:** C-03 settles benefit-demand axis; C-04 job is afternoon *fuel* — distinct encounter, same underlying correction. Not mapped as KEEP target (one book).

---

### Early conned-not-flawed re-proof (C01→C02) — partial both

**Judge sources:** A belief-ch02, A journey-ch02 (`re-argument` 1); B belief-ch02 (`re-argument` 1)

**Shared symptom:** *"You were conned, not flawed"* re-proved after C01 settled method-not-character.

**Root component:** plan-card (C-02 job: `unable to stop proves con not character flaw` while continuity from C01 already handed contracted investigator)

**Evidence:** C-02 continuity: `hands conned not flawed investigator` — card assigns the same correction C01 began. Writer executes job; belief lane counts re-argument, journey PASS in A.

**Mechanism:** Entering-belief / job overlap on early shame beat. B journey fails for different reason (overshoot, below).

---

### Withdrawal-shake courtroom (C07/C10→C12) — A only

**Judge sources:** A book-arc (`re-argument` stopping-shake fear)

**Shared symptom:** C12 rebuilds shake fear after C07 (`EV-19 hump`) and C10 (`small rough patch`) already settled it: *"But the shakes… If stopping created collapse, how do children run and laugh…"*

**Root component:** plan-card

**Evidence:** Justification menu maps `withdrawal unbearable → C12` only, but C-07 and C-10 evidence both include `EV-19 hump 2–5 days`; C-12 `resolves` lists `withdrawal unbearable`.

**Mechanism:** Evidence routed to mechanism + totality chapters, then C-12 assigned full withdrawal Q&A — writer re-litigates. A-only; record, do not map as next hypothesis target.

---

### SA-09 cinema pre-debut in C05 — both (noted)

**Judge sources:** A book-arc, B book-arc (`pre-debut-spend` 1)

**Shared symptom:** C05 stages mini cinema before C09 flagship: *"Friday late show, lights low, hard week behind you, shared box opened while the film begins."*

**Root component:** model

**Evidence:** C-05 card: `scene: SA-09 token hint only, full reserved C09`. SA-09 bank: `full staging only C09; elsewhere token echo only`. Writer prompt carries same constraint; response still full-stages.

**Mechanism:** Adequate card; writer previews assigned peak scene. Both books; noted only.

---

### SA-01 party-shoes full restage (C03→C07) — B only

**Judge sources:** B book-arc (`re-argument` party-shoes C03→C07)

**Shared symptom:** C07 rebuilds C03 inversion: *"dancing all evening in borrowed party shoes two sizes too tight…"*

**Root component:** model

**Evidence:** C-07 card: `scene: SA-01 token echo tight shoes only`. B ch07 response lists `Borrowed party shoes worn too tight till midnight` and runs full metaphor.

**Mechanism:** Card adequate; model ignores token-echo constraint. B-only noise.

---

### Journey leaving-belief overshoot — B only (blocking)

**Judge sources:** B journey-ch02, ch03, ch05 (blocking `journey-incomplete` ×3)

**Shared symptom:** Chapters complete demolition past card `belief now` / `leaving belief` tokens:
- C02: card requires reader *still believes choice explains persistence*; chapter closes *"You were caught without choosing"*
- C03: card requires *still weighs harm versus pleasure*; chapter *"The benefit side of your scales is empty"*
- C05: card `belief now` duplicates leaving state *still feels celebration needs sweet payment*; continuity hands `reward-disillusioned` — chapter lands reward-disillusioned

**Root component:** plan-card

**Evidence:** C-02 belief-now and continuity handoff contradict (`choice explains persistence` vs `conned not flawed`). C-03 entering = leaving belief token. C-05 belief-now equals its own leaving line while continuity names different exit state.

**Mechanism:** Planner writes demolition cards whose `belief now` / `leaving belief` fields don't match enacted job or continuity — writer follows job, journey gate fails. B-only blocking; not KEEP veto.

---

### M-D echo template garble — A only (blocking)

**Judge sources:** A voice-ch05 (blocking `factory-speech` 1)

**Shared symptom:** *"You think, in your own kind voice: "I've earned a 'treat'… when you feel you deserve one.""* — stitched lexicon fragments, not lived inner speech.

**Root component:** plan-card

**Evidence:** Plan lexicon sheet (§5): `"'treat'… when you feel you deserve one"` as mined community dialect. C-05 mantra: `echo M-D pin "a genuine treat or lift"`. Writer splices lexicon ellipsis into M-D echo moment.

**Mechanism:** Speakable mined-form literals on plan lexicon/card surface reach writer as pasteable echo template. First wrong point is plan lexicon routing, not writer-prompt (inputs carry broken form). A-only.

---

### Body-hunger / trap-mechanics N←N−1 rebuilds — B only

**Judge sources:** B belief-ch07 (`re-argument` 1 hunger vs sweet); B belief-ch09 (`re-argument` 1 animal dopamine paragraph)

**Root component:** model

**Evidence:** Cards assign new encounters (evening biscuit; cinema night). Prior chapters settled body-hunger and design-seer tokens. Writer re-opens mechanism paragraphs at paragraph scale despite brief continuity handoffs.

**Mechanism:** Hypothesis predicted B might stay flat due to model-attributed N←N−1 rebuilds; consistent with B journey `re-argument` 5→5 while plan-card seams shifted.

---

## Iteration 023 verdict vs hypothesis

| Prediction | Outcome |
|---|---|
| CH-10/11 tomorrow double-ownership gone | **Confirmed** — 0 `re-argument` on ch10/ch11 both books |
| Journey `re-argument` A < 7 and B < 5 | **Partial** — A 6, B 5 |
| No new both-books blocking class | **Failed** — B gained `journey-incomplete` ×3 (not PRIMARY class) |
| Book-arc / belief `re-argument` fall both | **Mixed** — arc 5→4 merged; belief 4→5 merged (worse) |

**Diagnosis:** The one-correction / reviewer gate **closed the named 019 PRIMARY seam** (tomorrow/totality → delay) by folding quit-tomorrow into C-10 totality and C-11 willpower/fear. It **did not** close `re-argument` as a class because overlap migrated to **evidence double-routing** (EV-13), **token/responsibility triple-ownership** (T-H blip), and **resolves-field leakage** (willpower, withdrawal). Plan reviewer falsely certifies `EV-01 to EV-21 single-use` while EV-13 appears on two cards.

**PERSISTENT — plan-card** is root for `re-argument` in **5 consecutive iterations** (019–023). Writer-prompt strikes on this class (021, 022) did not move B; 023 plan-card change moved one book only — same sampling pattern as 020–022.

**Do not map as next KEEP targets (one-book only):** B `journey-incomplete`, A blocking `factory-speech`, B party-shoes restage, A withdrawal-shake arc-only, B belief N←N−1 rebuilds.
