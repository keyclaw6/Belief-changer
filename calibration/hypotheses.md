# Hypothesis Ledger — factory calibration

The science log of the calibration loop. One entry per hypothesis; the operator
updates statuses every run (HARNESS §6). Amendments to method assets are only
legitimate as tests of a ledgered hypothesis.

**Entry format:**

```
## H-NNN — <short name>            [PROPOSED | TESTING run-NNN | SUPPORTED | REFUTED | RETIRED]
- Gap: <observed failure, from a run report — mechanism, not resemblance to the reference>
- Lever: <the ONE generic asset + the change>
- Prediction: <which metric/judge dimension moves, direction, roughly how much>
- Result: <what actually happened; run refs>
```

Seeded candidates below are examples of well-formed entries and likely first
levers. run-001 (baseline) tests nothing; derive real priorities from its
diagnosis before promoting any of these to TESTING.

---

## H-001 — explicit per-chapter word budgets        [PROPOSED]
- Gap: nothing in the plan template forces chapter lengths, so book length is emergent, not planned (HARNESS §7 requires planned).
- Lever: master-plan prompt — curve map must assign every chapter a word budget summing to 0.9–1.1× the target total; each chapter spec carries its budget.
- Prediction: total_words ratio moves into ±15%; per-chapter budget deviations < ±20%.
- Result: —

## H-002 — chapter-opening variety rule             [PROPOSED]
- Gap: writers converge on one opening move (typically a question) when the spec doesn't forbid it; flow judges read it as template smell.
- Lever: master-plan prompt — structural slots record each chapter's opening MOVE (scene / assertion / question / callback / instruction), no two consecutive chapters sharing one.
- Prediction: flow and voice win-rates rise; no objective metric regresses.
- Result: —

## H-003 — echoes land at argumentative peaks       [PROPOSED]
- Gap: scheduled mantra echoes placed as paragraph-end garnish read as pasted rhythm, not conviction (mantra_discipline scores mid despite schedule compliance).
- Lever: chapter-writer prompt — an echo must land where the argument it compresses has just been re-earned (post-demolition beat), never as a section sign-off by default.
- Prediction: mantra_discipline win-rate rises with schedule compliance unchanged.
- Result: —

## H-004 — explicit hand-over hooks in the plan     [PROPOSED]
- Gap: previous-chapter-only context gives local continuity, but chapter ENDINGS under-set the next chapter's opening promise; judges read weak hand-offs.
- Lever: master-plan prompt — every chapter spec carries "opens from:" and "hands to:" one-liners; reviewer checks the hand-off pair.
- Prediction: flow rises; whole-book escalation rises at Stage B.
- Result: —

## H-005 — writer-model arm                          [PROPOSED]
- Gap: unknown which family writes this register best; assumption untested.
- Lever: manifest only — same plan, writer = family A vs family B (one run each, no other changes).
- Prediction: none (measurement). Cross-family judge rule (§9) guards scoring.
- Result: —

## H-006 — reviewer criteria aligned to judge dimensions [PROPOSED]
- Gap: chapter reviewer can ACCEPT chapters that pairwise judges then score low (reviewer checklist and judge dimensions measure different things).
- Lever: chapter-reviewer prompt — add the six judge dimensions as explicit accept criteria (without naming the reference or judges).
- Prediction: fewer writer↔reviewer cycles wasted; judge scores rise per accepted chapter.
- Result: —
