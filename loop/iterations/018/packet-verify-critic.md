# Packet verify — independent critic (iter 018)

## Verdict

**GO**

## Scope check

| Criterion | Result |
|-----------|--------|
| Exactly one added never-surface clause (`no trap-question or Socratic-trap prefixes`) | **Yes** — sole hunk in `change.diff`; live `chapter-writer.md` line 64 matches |
| Diff base is 014 KEEP (`a6ff081`) | **Yes** — `change.diff` index `a6ff081..99151a5`; not `5291f90` (017) |
| Writer W1 intact (`pose two or three questions whose only honest answer` + `land one short verdict`) | **Yes** — live lines 45–46 unchanged from 014 |
| Style-guide trap formulas intact | **Yes** — §5.8 “Ask, don't assert…”, §9 trap-question line, §9.7 cushion rule, checklist, and operator 3 “Concession question” all retain 014 wording; no 017 “Ask. The question is the next sentence.” weakening |

## Replays 017 trap-formula deletion?

**No.** Iteration 017 deleted the pasteable W1 formula in `chapter-writer.md` and weakened six `style-guide.md` hunks (S1–S5 + checklist + operator 3). Iteration 018 touches **one file**, **one line**, in the never-surface ban only. Method teaching and style-guide Socratic/trap language are left on the 014 KEEP baseline.

## Second file or second causal change?

**None detected.** `change.diff` contains a single file (`prompts/chapter-writer.md`) and a single contiguous edit inside the never-surface list. No style-guide, plan-skill, plan-reviewer, anatomy, or other prompt deltas. Live tree matches the diff intent: only the prefix ban is new relative to 014.

## One-line summary

**GO** — single never-surface clause on 014 KEEP; W1 and style-guide trap formulas intact; does not replay 017.
