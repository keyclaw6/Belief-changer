# Iteration-001 Handoff — factory-v2

You are the loop operator. Everything you need is in `PROGRAM.md` — read it
first, follow it exactly, and do not redesign the process.

## Preconditions (one-time)

1. `git clone https://github.com/keyclaw6/Belief-changer.git && git checkout factory-v2-owner`
2. Export `OPENROUTER_API_KEY`.
3. Verify the model IDs in `loop/config.yaml` resolve on OpenRouter
   (`minimax/minimax-m3` writer + the three judge IDs). Fix IDs there if the
   catalog spells them differently — that is a config correction, not a
   process change.
4. `python3 -m unittest discover -s scripts/eval/tests` → 26 tests green.

## Iteration 001 — the frozen hypothesis

From `loop/learnings.md`: **de-sanitization.** The Carr-fidelity flip is
already applied to the canon (style guide §9/§4/§6, writer, reviewer,
planner). Prediction: blind authenticity win-rate vs Good Sugar Bad Sugar
and belief-change efficacy both rise vs the run-012 baseline, whose sanitized
drafts lost efficacy 1–3 while "winning" a rigged integrity score.

## The run

1. Write chapters 1–3 of `production-books/quit-sugar/` per PROGRAM.md
   step 1 (fresh context per chapter: style guide + master plan + previous
   chapter only; the master plan R2 is accepted "fit to write from").
2. `python3 scripts/loop/score.py --book production-books/quit-sugar --chapters 1-3`
3. `python3 scripts/loop/gate.py`
4. Record per PROGRAM.md steps 4–5. Report to the founder: the results.tsv
   row, the three chapters, and one paragraph on what the scores say.

## Known open items (do not solve inside the run)

- Judge model IDs unverified against the live OpenRouter catalog (above).
- Epsilon 0.03 is provisional until 3 same-config baseline repeats measure
  judge noise (`loop/config.yaml` comment).
- No automated evidence-invention gate: the chapter reviewer's gravest
  defect covers it in-loop; escalate to the founder if invention appears.
