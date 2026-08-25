# Trace Analysis — Iteration 011

**Hypothesis tested:** Silent-execution rewrite of `prompts/style-guide.md` §B5 operators 3/6/8/11, §B7 §5, and §B9 — remove speakable craft labels (`Trap question`, `Killer-line pair`, `Future-pacing`, `warm rationale`) that contradicted the writer-prompt silent-execution ban after iter-010.

**Outcome vs 010 KEEP baseline:** Blocking `factory-speech` merged **14 → 6** (A 6→4, B 8→2). Blocking `instruction-paperwork` merged **9 → 10** (A 3→5, B 6→5). Voice PASS **13/18 → 15/18** (A), **11/18 → 16/18** (B). Belief, journey, and book-arc hold at 18/18 and PASS both books. The §B5 fix closed the targeted operator-vocabulary blocking class; residual blocking is plan-owned frozen strings, not style-guide checklist primes.

---

| Causal cluster | Spread | Judge sources | Root component | Priority reason |
|----------------|--------|---------------|----------------|-----------------|
| Frozen-instruction compliance paste | systemic (C06 A, C15 B, C18 both) | voice-emotion A ch06, B ch15, A/B ch18 — `instruction-paperwork` blocking 10 merged | plan | KEEP object in both books; unchanged plan strings; 8/10 blocking concentrated in shared C18 checklist |
| Instruction-ID cross-reference in frozen I-06 | positional (C15 B, C18 both) | voice-emotion B ch15, A/B ch18 — `factory-speech` blocking 3 merged (subset of 6 total) | plan | Same frozen spine string in both books; factory metadata inside assigned instruction lines |
| FT-06 instrument inventory in echo prose | local (C17 A only) | voice-emotion A ch17 — `factory-speech` blocking 3 | model | One-book sampling noise; B ch17 PASS on same card with lighter instrument touch |
| B5 operator-label leak at peaks | systemic (noted only) | voice-emotion A ch01/ch16 noted `Warm rationale:`; B ch05/ch09 noted `killer pair` / `trap question`; blocking 0 both | style-guide (fixed) | Blocking class largely closed; residual noted leaks are not KEEP gates |
| Persona-token scaffolding in scene prose | systemic (noted) | voice-emotion A ch06/ch09/ch16, B ch03/ch16 — `factory-speech` noted | plan-card | Plan assigns P-01..P-04; noted floor only |
| Research-brief register in science passages | systemic (noted) | voice-emotion A/B ch10/ch14/ch16 — `wrong-register` + `factory-speech` noted | plan + model | Mid-book evidence passages; noted-only; does not gate |

---

### Frozen-instruction compliance paste

**Judge sources:** voice-emotion replicate-a ch06 (`instruction-paperwork` 1, FAIL); replicate-a ch18 (`instruction-paperwork` 4, FAIL); replicate-b ch15 (`instruction-paperwork` 1, FAIL); replicate-b ch18 (`instruction-paperwork` 4, FAIL). Merged blocking **10** (A 5, B 5).

**Shared symptom:** Assigned instruction lines paste plan frozen wording with embedded clinical-disclaimer tails and semicolon-chained compliance clauses. Judges quote:

- A ch06: `"5. IGNORE ANY ADVICE THAT CONFLICTS WITH THIS METHOD — INCLUDING DIETS, WILLPOWER TIPS, AND STORIES FROM PEOPLE WHO QUIT BY SUFFERING; IF YOU HAVE DIABETES, AN EATING DISORDER, OR ARE UNDER MEDICAL NUTRITION THERAPY, CONTINUE TO FOLLOW YOUR CLINICIAN'S ADVICE ON FOOD AND MEDICATION — THIS BOOK DOES NOT REPLACE MEDICAL CARE."`
- A/B ch18: `"**5. IGNORE ANY ADVICE… this book does not replace medical care.**"`; `"**7. DO NOT USE SUBSTITUTES… this is not medical advice.**"`; `"**11. FORGIVE A BLIP… this method does not override medical care.**"`

**Distinct effects:** A ch06 fails at I-05 debut (single line). B ch15 fails only on I-06 cross-ref (see next cluster) but shares the same spine. C18 accounts for **8/10** merged blocking — the hand-over checklist in both books.

**Root component:** plan

**Evidence:** The move first goes wrong in `traces/plan.md` §5 Instruction spine — frozen table rows embed safety tails inside instruction sentences:

```
| I-05 | 5. IGNORE ANY ADVICE THAT CONFLICTS WITH THIS METHOD — Including diets, willpower tips, and stories from people who quit by suffering; if you have diabetes, an eating disorder, or are under medical nutrition therapy, continue to follow your clinician's advice on food and medication — this book does not replace medical care. | C06 | mid C08, final C18 |
| I-06 | 6. NEVER DOUBT YOUR DECISION TO QUIT BAD SUGAR — Once you make the vow, never reopen the question; referral to clinician exception as in I-05 still applies. | C15 | final C18 |
| I-07 | 7. DO NOT USE SUBSTITUTES THAT KEEP THE ADDICTION ALIVE — If you have diabetes, an eating disorder, or are under medical care, follow your clinician's guidance on any substitute — this is not medical advice. | C16 | final C18 |
```

Plan also mandates verbatim delivery: *"Mid-book recap of I-01–I-05 verbatim in C08 SUMMARY. Final chapter C18 is nothing but verbatim recap of I-01–I-12."* Writer prompt carries this as a licensed recap zone. Downstream, `chapter-18/response.md` reproduces the frozen strings inside the portable manual.

**Mechanism:** Safety requirements are fused into instruction spine rows at plan time. The writer contract requires verbatim instruction recaps. The model correctly obeys plan + writer-prompt and pastes consent-form register into assigned ALL-CAPS instruction moments. Judges classify as `instruction-paperwork` because Carr's reference close uses bare spoken imperatives without inline liability language.

**PERSISTENT — this component has been the root cause 3 times (iter-009, iter-010, iter-011).** The approach at this level may be wrong; a different level may be needed.

---

### Instruction-ID cross-reference in frozen I-06

**Judge sources:** voice-emotion replicate-b ch15 (`factory-speech` 1 + `instruction-paperwork` 1, FAIL); replicate-a ch18 (`factory-speech` 1, FAIL); replicate-b ch18 (`factory-speech` 1, FAIL). Three blocking hits on the same underlying string; merged **3** of **6** total `factory-speech` blocking.

**Shared symptom:** Assigned I-06 carries factory instruction-ID cross-reference instead of spoken plain limit:

- B ch15 / A ch18 / B ch18: `"6. NEVER DOUBT YOUR DECISION TO QUIT BAD SUGAR — Once you make the vow, never reopen the question; referral to clinician exception as in I-05 still applies."`

Judge (B ch15): *"The numbered rule, cross-reference to I-05, and plan-card phrasing read like internal compliance documentation dropped into the ceremonial peak."*

**Distinct effects:** Replicate-a ch15 **PASS** — same card, but the model substituted the cross-ref with an expanded clinical disclaimer instead of the plan's `referral to clinician exception as in I-05 still applies` string. That sampling variation avoided this blocking class at C15 in A only. Replicate-b pasted the plan string verbatim at C15 and failed.

**Root component:** plan

**Evidence:** First wrong in plan instruction spine I-06 row. Lands in B `chapter-15/response.md` and both `chapter-18/response.md`.

**Mechanism:** Plan encodes inter-instruction compliance as an internal ID reference (`as in I-05`). Verbatim-recap license prevents the writer from translating it into Carr speech. Where the model pastes faithfully (B C15, both C18), judges hear spec-card metadata inside a vow/checklist moment and count `factory-speech` blocking. This is orthogonal to the iter-011 style-guide fix — §B5 silent execution does not reach frozen instruction spine text.

---

### FT-06 instrument inventory in echo prose (one-book noise)

**Judge sources:** voice-emotion replicate-a ch17 only (`factory-speech` blocking 3, FAIL). Replicate-b ch17 PASS (`factory-speech` blocking 0).

**Shared symptom:** Assigned FT-06 echo moments unpack the full Nature's Guide instrument list as operating-manual prose.

**Root component:** model

**Evidence:** Upstream inputs are adequate and mutually consistent. Plan card C17 assigns `mantra: echo M-08, FT-06 (Nature's Guide instruments in use)`. B executes the same assignment without blocking; A over-enumerates. Same inputs, divergent execution → model.

**Mechanism:** Not a KEEP-cluster target per contract (one-book blocking). Record for sampling context only.

---

### B5 operator-label leak at peaks (improvement cluster)

**Judge sources:** Blocking **0** both books for `killer pair`, `Future-pace`, `Warm rationale:` at assigned peaks. Noted residuals: A ch01 `*Warm rationale:*` prefixes (noted); B ch05 `"I want to land this with a small killer pair"` (noted); B ch09 `"Try this trap question now"` (noted).

**Shared symptom:** Iter-010 blocking peaks (`killer pair I promised`, `Future-pace this with me`, `Warm rationale:` headers) no longer appear as blocking `factory-speech` in either replicate. `trap-question-label` noted merged **7 → 2**.

**Root component:** style-guide (iter-011 change)

**Evidence:** Writer prompt bundle now embeds the fixed §B5 header and silent operators. Downstream chapters that previously blocked on operator vocabulary no longer gate on those strings.

**Mechanism:** Removing speakable operator names from the runtime style-guide bundle eliminated the contradiction that caused models to satisfy §B7/B9 checklist metrics by pasting labels at peaks. Partial hypothesis confirmation; does not address plan-spine clusters.

---

### Persona-token scaffolding in scene prose (noted floor)

**Judge sources:** voice-emotion A ch06 noted `factory-speech` (`P-02`, `FOR column`); B ch03/ch16 noted persona tokens. Blocking 0.

**Root component:** plan-card

**Mechanism:** Noted-only sampling floor; not a KEEP gate.

---

### Research-brief register in science passages (noted floor)

**Judge sources:** voice-emotion A/B ch10/ch14/ch16 noted research-summary register. Blocking 0.

**Root component:** plan (evidence routing density on cards) with model execution variance

**Mechanism:** Noted improvement surface only; does not block either book.

---

## Hypothesis verdict

| Predicted | Observed |
|-----------|----------|
| `factory-speech` blocking falls materially below 14 in both books | **Yes** — merged 14 → 6; B5 operator-vocabulary blocking largely eliminated |
| `instruction-paperwork` persists on unchanged plan strings | **Yes** — merged 9 → 10; C18 checklist dominates |
| Plan-ledger lines (`FOR column`, `first valence`, FT-03) may still block | **Partially** — `FOR column` noted A ch06 only; FT-06 blocking A ch17 only (one-book noise); no new blocking class |
| `trap-question-label` / `coach-register` noted counts fall | **trap-question-label** noted 7 → 2; **coach-register** modest drop |

**KEEP implication:** Targeted `factory-speech` blocking fell in **both** books (6→4, 8→2). Residual blocking is plan instruction-spine (`instruction-paperwork`, I-06 ID cross-ref), not a new class and not a veto. One-book FT-06 enumeration (A ch17) is noise.
