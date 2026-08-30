# Trace Analysis — Iteration 017

**Hypothesis tested:** Trap-question formula deletion only (015 S1–S5 EXACT; W1 ask + strip `land one short verdict`). Plan reuse 014 15-chapter plan. Research reuse. Files changed: `prompts/chapter-writer.md` + `prompts/style-guide.md` only. Two books. Judges: composer-2.5. Writer: Muse Spark contributor-free (`metadata.json` both replicates: `muse-spark-1.2-contributor-free`, `route` `opencode`; no `fallback` field on any sampled chapter metadata including B ch01).

**KEEP object this iteration targeted:** voice noted `trap-question-label` 014 **3 / 1** → **0 / 0** both.

**Veto surfaces:** blocking `factory-speech` stay **0 / 0**. Named 015 kills (verdict-landing / instruction serials) in either book → do not KEEP.

**Outcome vs 014 KEEP baseline (15 ch, 46/46 both):**

| Census class | 014 A / B | 017 A | 017 B | vs 014 KEEP target |
|---|---|---|---|---|
| Voice noted `trap-question-label` | **3 / 1** | **0** | **1** (ch05) | A met; B **not** 0 — **KEEP object failed** |
| Voice blocking `factory-speech` | **0 / 0** | **1** (ch09) | **1** (ch01) | **0→1 both** — **veto** |
| Voice noted `factory-speech` | 17 / 38 | **18** | **10** | confirming only (not KEEP object) |
| Voice PASS | 15/15 | **14/15** | **14/15** | both regressed 1 chapter |
| Journey PASS | 15/15 | **14/15** | 15/15 | A-only ch12 FAIL |
| Belief PASS | 15/15 | 15/15 | 15/15 | hold |
| Book-arc PASS | both | PASS | PASS | hold |
| Belief noted `re-argument` | — | 7 | 6 | confirming |
| Journey noted `re-argument` | 5/4 (book-arc) | 8 | 7 | confirming |
| Book-arc noted `re-argument` | 5 / 4 | 3 | 2 | confirming |

**Named 015 kills (trace grep):** No `Let me land` in either replicate’s `chapters/` or `traces/chapter-*/response.md`. No `8. NEVER` in chapter prose. A ch13 carries `**9. NEVER THINK…**` / `**10. NEVER USE A SUBSTITUTE…**` — voice-emotion-ch13 **PASS** (spoken Carr commands on assigned I-lines, not pipeline serials). B ch01 only `**1.**` / `**2.**` early instructions. Verdict-landing **family** reopens in A only (different string — see cluster below); instruction-serial **blocking** family stays closed.

**PERSISTENT:** `factory-speech` at writer-prompt / style-guide level has been the residual or blocking root across iter-010 through iter-016 — **7 times in learnings**. Iter-017 reopens blocking on two new local forms while trap-formula deletion largely holds.

---

| Causal cluster | Spread | Judge sources | Root component | Priority reason |
|----------------|--------|---------------|----------------|-----------------|
| Trap-question-label — B-only new prefix | local | B voice-emotion-ch05 noted `trap-question-label` 1; census B 1 / A 0 | plan-card | KEEP object missed 0/0 both; B-only sampling noise |
| Blocking factory-speech — chapter-job completion meta (A) | local | A voice-emotion-ch09 FAIL `factory-speech` 1; A reader-journey-ch09 cites same line as journey OK | writer-prompt | **Veto** — 015 verdict-landing kill family reopens in A |
| Blocking factory-speech — warmth policy declared (B) | local | B voice-emotion-ch01 FAIL `factory-speech` 1 | style-guide | **Veto** — blocking class in both books; different local form than A |
| Journey compliance-missing — meta-inoculation paraphrase (A-only) | local | A reader-journey-ch12 FAIL `compliance-missing` 1; B reader-journey-ch12 `compliance-missing` 0 | model | A-only; same card verbatim in B — sampling |
| Noted factory-speech — asymmetric delta | systemic | census A 18 (+1 vs 014); census B 10 (−28 vs 014) | — | confirming only; not KEEP object |
| Book-arc / journey re-argument (noted) | systemic | book-arc A 3, B 2; journey A 8, B 7; belief A 7, B 6 | plan | confirming; unchanged plan |

---

### Trap-question-label — B-only new prefix (A 0 vs B 1)

**Judge sources:** census-a (no `trap-question-label` key); census-b (noted 1); B voice-emotion-ch05 (`trap-question-label` 1, chapter PASS).

**Shared symptom:** Stage-direction prefix before a live reader question names the rhetorical device instead of asking it.

**Distinct effects:** A: zero noted across 15 chapters — grep `replicate-a/chapters/`: no `Ask the`, `Socratic trap`, `trap question`, or `only honest answer` strings. B: single hit ch05 only.

**Root component:** plan-card

**Evidence:**
- 014 formula **absent** from 017 `prompts/style-guide.md` and `prompts/chapter-writer.md`. Style-guide §5.8: `**Ask.** The question is the next sentence.` Operator 3: `ask; the question is the next sentence.` No `only honest answer concedes the point` anywhere in `prompts/`.
- CH-05 card (`replicate-b/traces/chapter-05/chapter-card.md` L11): `Guardrails: … flat fact assertion, Socratic trap question to let reader concede; …`
- Downstream B ch05 `response.md` L90 (judge-quoted):

  > Ask the simplest Socratic trap — not to shame you, but to let you catch the lie with your own mouth:

  followed by live questions (L92–94). This is **not** the 014 pasteable formula (`Ask the trap questions whose only honest answer concedes the point:` per 014 trace-analysis ch07–09). It is a **new** prefix: plan-card methodology label (`Socratic trap question`) + invented coaching frame (`not to shame you, but to let you catch the lie with your own mouth`).
- Same card on A replicate; A ch05 voice-emotion PASS, `trap-question-label` 0 — adequate inputs, no matching prose in A.

**Mechanism:** Trap-formula deletion removed the 014 speakable checklist strings; the plan-card guardrail still names `Socratic trap question` as a device type in the writer packet. B’s model run surfaces that label as a stage-direction header once; A does not on the same card. **One-book (B only)** — record as sampling noise; not the 014 formula reverted.

---

### Blocking factory-speech — chapter-job completion meta (A)

**Judge sources:** A voice-emotion-ch09 FAIL (`factory-speech` blocking 1); A reader-journey-ch09 PASS (same line cited as completed leaving-belief); A belief-mechanic-ch09 OK on verdict substance.

**Shared symptom:** At the primary-job landing, the narrator audits chapter completion instead of speaking the verdict as lived certainty.

**Distinct effects:** A-only blocking. B ch09 voice-emotion PASS — no matching string in B traces.

**Root component:** writer-prompt

**Evidence:**
- Writer Binding (`replicate-a/traces/chapter-09/prompt.md` L78–81): `Complete exactly one belief move — the one your card assigns — now, land it, and stop. … Never announce the one job, reserved-later fence, homework, a ledger, or an arriving peak.`
- W1 stripped `land one short verdict` from Method (L45–46: `ask, perform the credit inversion` only) — 015’s exact blocking string `Let me land it as one short verdict, because this is the belief that changes in this chapter` is **absent** from 017 traces.
- Downstream A ch09 `response.md` L103 (judge blocking gap):

  > That is the one belief move this chapter had to make and it is made: BAD SUGAR is doing plenty TO you and nothing FOR you.

- `metadata.json` ch09: `muse-spark-1.2-contributor-free` / `opencode`; no fallback.

**Mechanism:** Stripping the speakable verdict-landing cue removed 015’s `Let me land…` template but left Binding’s `belief move` / `land it` craft language. The model inverts the “never announce the one job” ban into completion-check meta at the assigned peak — same **015 verdict-landing kill family**, mutated string. **Named 015 kill surface present in A** (chapter-job landing meta, not the exact 015 sentence).

---

### Blocking factory-speech — warmth policy declared (B)

**Judge sources:** B voice-emotion-ch01 FAIL (`factory-speech` blocking 1); B reader-journey-ch01 PASS.

**Shared symptom:** Trust-establishment bridge delivers a factory posture label instead of embodied warmth.

**Distinct effects:** B-only blocking. A ch01 voice-emotion PASS — no `warm to you and vicious` in A ch01 response.

**Root component:** style-guide

**Evidence:**
- Chapter-writer Method (`prompts/chapter-writer.md` L34–36): `Be warm to the person and harsh to the trap and the willpower method.`
- Style-guide checklist (`prompts/style-guide.md` L419): `warm to the reader, harsh to the trap`
- Downstream B ch01 `response.md` L18 (judge blocking gap):

  > Put that down. I am warm to you and vicious to the trap. I will never scold you.

- `metadata.json` ch01: `muse-spark-1.2-contributor-free` / `opencode`; no `fallback` field — primary route, not fallback artifact.

**Mechanism:** House voice rule is planner-facing craft instruction; B’s run quotes it almost verbatim as reader-facing policy at the primary-job trust bridge. A same packet does not surface the line. **Not** the 015 verdict-landing or instruction-serial kill — a **different** local blocking form. Merged blocking class `factory-speech` is **0/0 → 1/1** across books despite unlike passages.

---

### Blocking factory-speech — same class, different local forms (diagnostic)

**Question:** Are A ch09 and B ch01 the same causal cluster?

**Answer:** Same **judge class** (`factory-speech` blocking) and same high-level failure (harness/craft language inside reader prose at an assigned peak). **Not** the same causal cluster for factory targeting: A root is writer-prompt Binding `belief move` completion meta (015 kill-family); B root is style-guide / chapter-writer warmth instruction quoted aloud (new local form). One replicate each → per runbook, neither local form alone maps as the next hypothesis target; the **merged blocking reopen in both books** is the veto signal.

---

### Journey compliance-missing — meta-inoculation paraphrase (A-only)

**Judge sources:** A reader-journey-ch12 FAIL (`compliance-missing` 1); B reader-journey-ch12 `compliance-missing` 0.

**Shared symptom:** Meta-inoculation beat answers the brainwashing objection in spirit but not with the card’s frozen compliance string.

**Distinct effects:** A paraphrases; B delivers verbatim on the same plan card.

**Root component:** model

**Evidence:**
- CH-12 card (both replicates, `chapter-card.md` L9): answer frozen as `"Blind belief does not help — understanding does; your primitive mind ignores a belief but cannot ignore a solved truth"`.
- Downstream A ch12 `response.md` L121:

  > Blind belief does not help — understanding does. Your deeper mind will ignore a belief you force on it, but it cannot ignore a solved truth you have seen for yourself.

- Downstream B ch12 `response.md` L108:

  > Blind belief does not help — understanding does. Your primitive mind ignores a belief but it cannot ignore a solved truth.

- Writer Binding (`prompt.md` L82–85): `land it exact in wording, capitalization, and punctuation` for frozen tokens. Inputs adequate and mutually consistent; B executes verbatim.

**Mechanism:** Same card and compliance obligation; A substitutes synonymous mind-language (`deeper mind` / `you force on it`) where B quotes the pinned string. **One-book (A only)** — sampling noise; do not map as next-hypothesis target.

---

### Noted factory-speech — confirming only (A 17→18 / B 38→10)

**Judge sources:** census-a (`factory-speech` noted 18); census-b (`factory-speech` noted 10).

**Shared symptom:** Factory-internal diction in unassigned passages — evidence-grade register, frozen-token echoes, arc scaffolding — at noted severity.

**Distinct effects:** A rose +1 vs 014 (18 vs 17); B dropped −28 vs 014 (10 vs 38). Asymmetric; not the iteration KEEP object. Hypothesis changed only trap-formula surfaces; plan and other style-guide operators unchanged from 014 — noted floor moves with sampling and chapter-local judge texture, not trap deletion.

**Root component:** — (confirming census only; no KEEP prediction)

**Evidence:** Census aggregates only; no both-books directional claim required by hypothesis.

**Mechanism:** Not diagnosed as a causal cluster for the trap-formula hypothesis; recorded for founder comparison.

---

### Book-arc / journey re-argument (noted)

**Judge sources:** book-arc A noted `re-argument` 3, B 2; journey A 8, B 7; belief A 7, B 6.

**Shared symptom:** Settled demolition jobs re-staged under new scene IDs without blocking journey or belief gates.

**Root component:** plan (unchanged 014 plan reused)

**Evidence:** Same plan.md both replicates; no plan regen in 017.

**Mechanism:** Not a KEEP object; flat or improved vs 014 book-arc re-argument (5/4). Noted-only.

---

### 015 named kills — trace verification

**Judge sources:** grep `replicate-*/chapters/` and `traces/chapter-*/response.md`; voice-emotion A ch13 PASS; census (no blocking `instruction-paperwork`).

| 015 kill surface | 017 trace |
|---|---|
| `Let me land it as one short verdict` / `belief that changes in this chapter` | **Absent** from chapter responses |
| Spoken `8.` / `9.` / `10.` instruction serials as blocking pipeline paperwork | **Absent** as blocking; A ch13 `9.`/`10.` judged OK |
| Chapter-job landing meta (015 family) | **Present A ch09** — mutated string, same family |

**Mechanism:** W1 strip closed the exact 015 `Let me land…` paste path. Binding `belief move` / `land it` still permits a related completion-meta variant in A. Instruction-serial blocking path stays closed.
