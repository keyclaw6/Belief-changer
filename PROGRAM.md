# PROGRAM — the self-improvement loop (operator runbook)

A boring, fixed loop. Copied in shape from github.com/neosigmaai/auto-harness:
**run pipeline → score vs reference → gate keep/revert → record → ONE hypothesis
→ repeat.** Intelligence goes into the chapters and the diagnosis — NEVER into
redesigning the loop mid-run. The previous "calibration lab" died because ~90% of
tokens went to process (preregistrations, judge-instrument rebuilds, commission
audits, direction audits) instead of prose. This loop refuses that.

**Goal.** Produce chapters a blind judge cannot tell from authentic Allen Carr.
**Done when** a blind judge told "one of these two is from a real published
Easyway book" guesses at ~50%. Fear, shame, and medical overreach are FEATURES of
authentic Carr to REPRODUCE — not defects.

**Target this campaign:** `production-books/quit-sugar/` (master plan R2, reviewed
"fit to write from"). Reference: *Good Sugar Bad Sugar*, extracted to
`calibration/reference/gsbs/` (gitignored — regenerate locally; see step 0).

## Step 0 — once per machine

```
python3 scripts/eval/extract_reference.py \
  --epub "analysis/reference-books/The easyway Good Sugar Bad Sugar.epub" \
  --out calibration/reference/gsbs
```

## The loop (per iteration N)

**Step 1 — RUN.** Write/rewrite chapters 1–3 of the target book using
`prompts/chapter-writer.md` with the writer model from `loop/config.yaml`.
**Fresh context per chapter:** the writer sees ONLY the style guide + master plan
+ the immediately previous chapter (none for ch1). Research and master plan are
reused as-is UNLESS the current hypothesis explicitly targets them. Convenience
wrapper: `python3 scripts/loop/run_iteration.py --book production-books/quit-sugar
--chapters 1-3 --iter N --hypothesis "..."` (degrades to manual dispatch when no
writer key).

**Step 2 — SCORE.** `python3 scripts/loop/score.py --book
production-books/quit-sugar --chapters 1-3 --iter N` → prints one reward line +
writes `loop/scores/iter-NNN.json`. It runs, wrapping `scripts/eval/`:
- HARD CHECKS (gate-blocking): originality tripwire vs the reference corpus;
  mantra/repetition law (assigned mantras verbatim, no accidental verbatim
  repeats); loose length sanity (±40% of the plan budget — a sanity check, not a
  style gate).
- REWARD: blind pairwise authenticity vs the matched real GSBS chapter, k=4
  order-swapped, cross-family judges.
- DETECTION PROBE (reported, not gated): blind "which is the real book?" —
  accuracy toward 0.5 = indistinguishable.
- DIAGNOSTICS (never gate): stylometrics vs the reference, for the learnings file.
- No judge key → `reward=null`, "judges: DRY-RUN (no key)"; hard checks +
  diagnostics still run for real. Judge output is NEVER fabricated.

**Step 3 — GATE.** `python3 scripts/loop/gate.py --iter N --hypothesis "..."` →
ACCEPT (keep changes) or REVERT (prints the exact `git checkout` commands to undo
this iteration's tunable-asset changes; the operator runs them). ACCEPT iff all
hard checks pass AND (reward ≥ last_accepted + epsilon OR first iteration).
Epsilon default 0.03 — recalibrate after 3 same-config baseline repeats measure
judge noise.

**Step 4 — RECORD.** The gate appends the `loop/results.tsv` row automatically.
YOU append the hypothesis outcome — **pass or fail, always** — to
`loop/learnings.md`.

**Step 5 — HYPOTHESIZE.** ONE change to ONE tunable asset for iteration N+1.
Write it into the learnings ledger as the next FROZEN hypothesis before running.

## The tunable surface (the ONLY files the loop operator edits between iterations)

- `prompts/style-guide.md`
- `prompts/chapter-writer.md`
- `prompts/chapter-reviewer.md`
- the book's `master-plan.md`

Everything else is **infrastructure** — never edited by the loop operator:
`scripts/**`, `loop/config.yaml`, the judge prompts, the eval library, the
reference. State plainly: **no preregistrations, no direction audits, no
commissions, no instrument rebuilds mid-run.** The judge instrument version is
pinned per campaign in `loop/config.yaml`. Changing it — or the writer, judges,
k, epsilon, length band, or originality threshold — starts a NEW campaign with
fresh baselines (a new `loop/results.tsv` lineage; do not compare rewards across
campaigns).

## Escalation & defects

- **3 consecutive non-improvements** (REVERT or no reward gain) → STOP, write a
  summary of what was tried and the current wall, surface to the founder. Do not
  invent a fifth clever lever.
- **Spec gap found by the writer** (a missing quote / study / mantra / ambiguous
  assignment) → that is a **master-plan defect**. Fix the plan, restart the
  chapter. Do not let the writer improvise the missing content.
- A hard-check FAIL always blocks ACCEPT; the reward is not even consulted.

## One iteration = one product batch

Follow one visible path: (edit one tunable asset) → write Ch1–3 → score → gate →
record → one new hypothesis. If you find yourself building an auditor, a
commissioner, a preregistration, or a new judge taxonomy, you have left the loop.
Stop and come back to it.
