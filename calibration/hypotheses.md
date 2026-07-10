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

## H-005 — writer-model arms (founder-specified bake-off)   [PROPOSED]
- Gap: unknown which model/reasoning config writes this register best; assumption untested.
- Lever: manifest only — same plan, same prompts, ONE arm per attempt (HARNESS §8):
  W1 GPT 5.6 Sol · W2 Opus 4.6 reasoning-none · W3 Opus 4.6 reasoning-medium · W4 Gemini 3.1 Pro · W5 Moose Spark 1.1 (when on OpenRouter).
- Prediction: none (measurement). Cross-family judging (§9) guards scoring; exact OpenRouter IDs + reasoning configs recorded in each manifest.
- Result: —

## H-007 — planner reasoning effort                  [PROPOSED]
- Gap: does high reasoning effort at the PLAN stage buy chapter quality downstream, or only cost?
- Lever: manifest only — same inputs, planner at reasoning effort none vs medium vs high; compare plan-review cycles + downstream judge scores.
- Prediction: none (measurement); expectation to test: plan-stage effort matters more than writer-stage effort.
- Result: —

## H-008 — tooling adoption (scripts vs framework)   [PROPOSED — operator's decision]
- Gap: plain scripts + operator orchestration may bottleneck on sub-call management (fresh contexts, retries, parallel arms) as runs scale.
- Lever: HARNESS §13 — build a small runner or adopt Agents SDK / PI fork on the lab branch; the file contract stays the interface.
- Prediction: adopt only if it measurably cuts run wall-time or error rate; log what it replaced and what it improved.
- Result: —

## H-006 — reviewer criteria aligned to judge dimensions [PROPOSED]
- Gap: chapter reviewer can ACCEPT chapters that pairwise judges then score low (reviewer checklist and judge dimensions measure different things).
- Lever: chapter-reviewer prompt — add the six judge dimensions as explicit accept criteria (without naming the reference or judges).
- Prediction: fewer writer↔reviewer cycles wasted; judge scores rise per accepted chapter.
- Result: —
