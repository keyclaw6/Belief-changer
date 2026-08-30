# Trace Analysis — Iteration 018

**Hypothesis tested:** One never-surface clause in `prompts/chapter-writer.md` (`no trap-question or Socratic-trap prefixes`). Style-guide, plan-skill, plan-reviewer, anatomy item 5, and `land one short verdict` stay 014. Plan reuse 014 15-chapter plan. Research reuse. Two books. Judges: composer-2.5. Writer: Muse Spark contributor-free (`metadata.json` both replicates: `muse-spark-1.2-contributor-free`, `route` `opencode`; no fallback on sampled A/B chapter metadata).

**KEEP object this iteration targeted:** voice noted `trap-question-label` 014 **3 / 1** → **0 / 0** both.

**Veto surfaces:** blocking `factory-speech` stay **0 / 0**. Named 015/017 kills (verdict-landing, instruction serials, chapter-job meta, warmth-policy quote) in either book → do not KEEP.

**Outcome vs 014 KEEP baseline (15 ch, 46/46 both):**

| Census class | 014 A / B | 018 A | 018 B | vs 014 KEEP target |
|---|---|---|---|---|
| Voice noted `trap-question-label` | **3 / 1** | **0** | **0** | **both 0 — KEEP object hit** |
| Voice blocking `factory-speech` | **0 / 0** | **2** (ch09) | **0** | A **0→2** — founder veto failed (one-book) |
| Voice blocking `method-promise-hedge` | 0 / 0 | **1** (ch07) | **0** | A-only new blocking class |
| Voice noted `factory-speech` | 17 / 38 | **17** | **12** | confirming only (not KEEP object) |
| Voice PASS | 15/15 | **13/15** | 15/15 | A FAIL ch07+ch09 |
| Journey PASS | 15/15 | 15/15 | 15/15 | hold |
| Belief PASS | 15/15 | 15/15 | 15/15 | hold |
| Book-arc PASS | both | PASS | PASS | hold |
| Book-arc noted `re-argument` | 5 / 4 | 5 | 5 | confirming |

**Named 015/017 kills (trace grep):** No `Let me land`, `the one belief move this chapter`, `I am warm to you and vicious`, `Ask the trap`, `Ask the simplest Socratic trap` in either replicate’s `chapters/` or `traces/chapter-*/response.md`. Plan-card CH-05 still names `Socratic trap question` in Guardrails (014 leftover); neither book surfaced it as a prefix. Instruction-serial blocking family stays closed.

**PERSISTENT:** `factory-speech` at writer-prompt / plan-card / style-guide level has been residual or blocking root across iter-010 through iter-017 — **8th time in learnings**. Iter-018 closes trap-question prefixes in both books and reopens blocking factory-speech as evidence-register in A only.

---

| Causal cluster | Spread | Judge sources | Root component | Priority reason |
|----------------|--------|---------------|----------------|-----------------|
| Trap-question-label closed both | systemic (absence) | census A 0 / B 0; all 30 voice-emotion reports `trap-question-label 0` | writer-prompt | KEEP object hit 3/1 → 0/0 |
| Blocking factory-speech — evidence-register at primary job (A) | local | A voice-emotion-ch09 FAIL `factory-speech` 2 | writer-prompt | **Founder veto** — blocking 0→2 A-only; not 015/017 named kills |
| Blocking method-promise-hedge — Burgeon hedge pasted (A) | local | A voice-emotion-ch07 FAIL `method-promise-hedge` 1 | model | A-only; same plan seed in B, B did not paste |
| Noted factory-speech — asymmetric delta | systemic | census A 17 (=014); census B 12 (−26 vs 014) | — | confirming only; not KEEP object |
| Book-arc / journey re-argument (noted) | systemic | book-arc A 5, B 5; journey A 8, B 8; belief A 6, B 3 | plan | confirming; unchanged 014 plan |

---

### Trap-question-label closed both (A 0 / B 0)

**Judge sources:** census-a (no `trap-question-label` key — zeros omitted); census-b (same); every `voice-emotion-ch01`–`ch15` report both replicates lists `trap-question-label 0`.

**Shared symptom:** Stage-direction prefixes that name the rhetorical device (`Ask the trap question…`, `Ask the simplest Socratic trap`) are absent from both books.

**Distinct effects:** 014 A had 3, 014 B had 1, 017 B reopened 1 (`Ask the simplest Socratic trap`). 018 both books 0. A ch05 has participatory `Ask yourself plainly, and answer honestly as you sit in that drawer moment:` — voice-emotion-ch05 scored trap-question-label 0 (not a device-label prefix). B ch05 voice-emotion PASS, trap-question-label 0; 017’s B-ch05 prefix string is gone.

**Root component:** writer-prompt

**Evidence:**
- 018 `prompts/chapter-writer.md` L64 (the sole factory change): `no trap-question or Socratic-trap prefixes` inside the existing never-surface list.
- CH-05 card still says `Socratic trap question to let reader concede` (`replicate-{a,b}/traces/chapter-05/chapter-card.md` Guardrails) — same 014 plan. Neither response.md emits `Socratic trap` or `Ask the trap`.
- Grep of both `chapters/` and `traces/chapter-*/response.md`: no `Ask the trap`, `Socratic trap`, `Ask the simplest`.

**Mechanism:** A one-line never-surface ban stopped the writer from speaking the workshop label in front of a live question, without deleting the 014 ask-teaching. The plan-card still names the device; the prefix did not leak in either sample. **Both-books signal** for the targeted class.

---

### Blocking factory-speech — evidence-register at primary job (A)

**Judge sources:** A voice-emotion-ch09 FAIL (`factory-speech` blocking 2); B voice-emotion-ch09 PASS (blocking factory-speech 0).

**Shared symptom:** At the assigned TO/FOR climax, narrator audits evidence instead of speaking the verdict as lived certainty.

**Distinct effects:** A-only blocking. B ch09 has no matching FAIL. Named 017 ch09 string (`the one belief move this chapter had to make and it is made`) is **absent**.

**Root component:** writer-prompt

**Evidence:**
- Writer Binding still requires silent craft and evidence-honesty; the never-surface add did not touch evidence-register.
- Downstream A ch09 (judge blocking gaps):
  - `"It is doing deferred load TO your heart and vessels at population level — not one hit equals one heart attack, but high intake linked with higher risk, year after year."`
  - `"In the only long follow-up we can honestly lean on, the sweets-comfort predicted worse mood, not better."`
- Same 014 plan and research on B; B voice 15/15, factory-speech blocking 0.

**Mechanism:** The prefix ban did not cause this class. A sampled research-report register inside the primary-job block (014 hydra, now blocking in one book). **One-book** — not a both-books PROGRAM veto; founder KEEP bar still requires blocking factory-speech **0/0**.

---

### Blocking method-promise-hedge — Burgeon hedge pasted (A)

**Judge sources:** A voice-emotion-ch07 FAIL (`method-promise-hedge` 1); B voice-emotion-ch07 PASS (`method-promise-hedge` 0).

**Shared symptom:** Method promise softened with `almost` at the understanding→change landing.

**Distinct effects:** A-only. B ch07 response.md does not contain `automatically` / `dissolves`.

**Root component:** model

**Evidence:**
- Plan/research seed is in both writer prompts (`replicate-b/traces/chapter-07/prompt.md`): `*"When deep understandings are made, changes happen almost automatically."* (Burgeon)` — 014 plan reuse.
- Downstream A ch07 `response.md`: `When deep understandings are made, changes happen almost automatically, because the want itself dissolves.`
- Same card and quote on B; B did not paste it. Inputs adequate and identical across replicates.

**Mechanism:** A copied a pasteable hedge from the plan inventory into the method-promise landing; B did not. **One-book sampling.** Would-be new blocking class name vs 014 (014 blocking method-promise-hedge 0/0) appearing in only one book.

---

### Noted factory-speech — asymmetric delta

**Judge sources:** census A noted factory-speech 17 (=014 A 17); census B 12 (014 B 38).

**Shared symptom:** Residual factory-speech floor (evidence-limit register, frozen-echo paste, research framing) continues.

**Root component:** — (confirming; not KEEP object)

**Mechanism:** B dropped; A unchanged. Not both-books improvement on this class and not this iteration’s target. PERSISTENT hydra (8th).

---

### Book-arc / journey re-argument (noted)

**Judge sources:** book-arc A 5 / B 5; journey re-argument A 8 / B 8.

**Root component:** plan

**Mechanism:** Unchanged 014 15-chapter plan. Confirming only.
