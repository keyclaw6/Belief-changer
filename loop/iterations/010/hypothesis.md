# Hypothesis — Iteration 010

source: hypothesizer (from 009 traces)

## Failure evidence

Voice-emotion blocking **`factory-speech`** — replicate-a **18**, replicate-b **19**, merged **37** (only blocking voice class in both books at scale); noted **`factory-speech`** 120 across all chapters. Judges classify literal craft/meta/workshop speech at emotional peaks and assigned verdict moments, not belief failure: replicate-a ch01 `> **BOXED DEFINITION — READ CAREFULLY**` / `> **Decree: When this book says "sugar," take it to mean BAD SUGAR.**`; replicate-a ch02 `A trap question whose only honest answer concedes the point` / `Two sentences. One killer pair. Let them close this move.` / `We have named the Sugar Trap.`; replicate-a ch09 `I will give you the killer-line pair at the peak of this movement.` / `Feel the emotional turn?` / `the FOR column is empty` / `That is frozen doctrine:` / `Future-pace this with me, because prediction transfers authority`; replicate-a ch07 `That is the doing TO you vs doing FOR you switch. Capital TO, capital FOR.`; replicate-b ch14 blocking factory-speech **8** on research-litany bullets. Belief-mechanic and reader-journey blocking all **0**.

## Root cause

`prompts/chapter-writer.md` — **PERSISTENT** (iter 000, 001, 005, 009). The evidence-honesty clause (lines 51–56) forbids surfacing internal identifiers and craft labels, but **Method and voice** (line 44) and **Binding chapter craft** (lines 71, 92–94) immediately re-order speakable device names (`trap questions`, `argue-to-compress`, `killer-line pair`, `future-pacing`) the model copies into peak prose. Cards and the accepted plan also pass production workshop strings (`BOXED DEFINITION`, `FOR column`, `frozen doctrine`, decree templates) as authoritative content; with no **translation-supremacy** rule, the model resolves the conflict by literal compliance — pasting labels, typography, and assignment narration (`We have named…`, stage-direction coaching) into reader text. **Retry note:** iter-005 tried writer-prompt silent craft under the retired PASS/FAIL-by-label instrument (REVERT, voice 0/18); this hypothesis retries that surface on the census instrument with a **new mechanism** — workshop-token translation supremacy over card assignments — which 009 traces show as the dominant blocking pattern and which 005 did not instruct.

## Targeted fix

File: `prompts/chapter-writer.md` — one causal change: silent craft execution plus workshop-token translation supremacy. Replace the canonical never-surface rule and delete speakable duplicates in the same file.

**Hunk 1 — Method and voice, paragraph 4 (lines 43–47):** Replace
```
  objection, answer with two or three trap questions whose only honest answer
  concedes the point, perform the credit inversion, and land one short verdict.
  Do not reopen a landed verdict with permission language, coaching stage
  directions, both-sides framing, or narrator-side hedges.
```
with
```
  objection, pose two or three questions whose only honest answer concedes
  the point, perform the credit inversion, and land one short verdict. Perform
  every rhetorical move silently — never name, count, announce, or stage-direct
  it in reader prose. Do not reopen a landed verdict with permission language,
  coaching stage directions, both-sides framing, or narrator-side hedges.
```

**Hunk 2 — Method and voice, evidence-honesty bullet (lines 51–56):** Replace
```
  Never surface the ledger's own vocabulary in reader-facing text: no ledger or source IDs,
  no SUPPORTED/MIXED/CONTESTED grades, no persona codes, no scene, mantra, or
  device-code strings, no internal drafting or craft labels, and no
  "Permitted inference / Prohibited inference / Empirical limit / Safety
  limit" headings — convert each boundary into plain Carr-voice prose that
  states the same claim, its scope, and its limit.
```
with
```
  Never surface the ledger's own vocabulary in reader-facing text: no ledger or source IDs,
  no SUPPORTED/MIXED/CONTESTED grades, no persona codes, no scene, mantra, or
  device-code strings, no internal drafting or craft labels, no plan or card
  production typography or workshop strings (boxed-definition headers, decree
  templates, FOR-column ledger talk, frozen-doctrine labels, device or beat
  names even when assigned on the card), and no assignment-fulfillment narration
  ("We have named…", "I will give you the killer-line pair", "Feel the emotional
  turn?") — translate each into plain Carr-voice prose that performs the move,
  and no "Permitted inference / Prohibited inference / Empirical limit / Safety
  limit" headings. When a card assigns a device name or workshop string, deliver
  the semantic job only; this ban outranks the assignment. Convert each evidence
  boundary into plain Carr-voice prose that states the same claim, its scope,
  and its limit.
```

**Hunk 3 — Binding chapter craft bullet 2 (lines 71–72):** Replace
```
   gets its full argue-to-compress beat; an echo is brief and is never
   re-argued.
```
with
```
   gets its full argument-then-compression rendered as lived reader experience,
   with no beat or device label; an echo is brief and is never re-argued.
```

**Hunk 4 — Binding chapter craft bullet 7 (lines 90–95):** Replace
```
7. Use at least one card-assigned concrete analogy or scene to do the
   argumentative job your card declares for it. Use fact-assertion,
   self-answered questions, trap questions, ventriloquism, inversion, one
   killer-line pair per major argument, reassurance–challenge, future-pacing,
   permission paradox, credit reassignment, and warm imperative instruction
   where your card assigns them.
```
with
```
7. Use at least one card-assigned concrete analogy or scene to do the
   argumentative job your card declares for it. Execute every assigned
   rhetorical move silently in Carr voice — render direct lived experience
   and verdict only; never label, count, coach, or announce the move, and never
   write meta-commentary about the assignment.
```

No other file touched.

**Why this component:** Trace analysis names **writer-prompt** as the PERSISTENT root for the only systemic blocking voice class (**factory-speech** 37); **instruction-paperwork** (7) is plan-owned and second priority; plan/card edits are out of scope for this single causal change.

## Predicted impact

What will improve: **`factory-speech`** blocking will fall because the writer can no longer obey speakable Binding diction or paste plan workshop labels (`BOXED DEFINITION`, `FOR column`, `frozen doctrine`, killer-line/future-pace coaching) — the census class whose merged blocking count must drop in **both** replicates.
What might regress: Ch1 BAD SUGAR debut may lose typographic punch if translation over-strips; trap-question force could soften without the explicit label scaffold; noted **`trap-question-label`** (34) may persist as non-blocking echo.
How we'll know it worked: Voice-emotion census judges should report **`factory-speech` blocking near zero in BOTH replicates** at the 009 quoted peaks (ch01 boxed-definition/decrees, ch02 trap-question/killer-pair/`We have named`, ch07 FOR-column switch, ch09 killer-line/future-pace/frozen-doctrine, ch12/ch14 litany register) without reopening belief-mechanic or reader-journey blocking.
