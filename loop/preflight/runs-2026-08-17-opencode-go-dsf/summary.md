# Preflight — Judge Calibration Battery re-run on opencode-go/deepseek-v4-flash (opencode harness)

Date: 2026-08-17. Harness: opencode. Judge model: `opencode-go/deepseek-v4-flash`
(each call spawned as a clean-context `task` sub-agent; judge rubric served verbatim (inlined)
from `loop/judges/`, inputs verbatim from `loop/preflight/inputs/`). Mirrors the
2026-08-14 DeepSeek V4 Flash battery layout, inputs, and per-call naming.

## VERDICT: PREFLIGHT 18/18 PASS

## Result table (18 calls)

| # | Check | Judge | Run | Expected | Observed | PASS/FAIL |
|---|-------|-------|-----|----------|----------|-----------|
| 1 | PASS test | belief-mechanic | run1 | PASS | PASS | OK |
| 2 | PASS test | belief-mechanic | run2 | PASS | PASS | OK |
| 3 | PASS test | voice-emotion | run1 | PASS | PASS | OK |
| 4 | PASS test | voice-emotion | run2 | PASS | PASS | OK |
| 5 | PASS test | reader-journey | run1 | PASS | PASS | OK |
| 6 | PASS test | reader-journey | run2 | PASS | PASS | OK |
| 7 | Repeatability | belief-mechanic | run1 | same as run8 | PASS | OK |
| 8 | Repeatability | belief-mechanic | run2 | same as run7 | PASS | OK |
| 9 | Repeatability | voice-emotion | run1 | same as run10 | FAIL (instruction MATERIAL) | OK |
| 10 | Repeatability | voice-emotion | run2 | same as run9 | FAIL (instruction MATERIAL) | OK |
| 11 | Repeatability | reader-journey | run1 | same as run12 | PASS | OK |
| 12 | Repeatability | reader-journey | run2 | same as run11 | PASS | OK |
| 13 | Voice probe | voice-emotion | p1 hedged-core-verdict | FAIL (must flag) | FAIL — hedged verdict flagged MATERIAL | OK |
| 14 | Voice probe | voice-emotion | p2 hedged-method-promise | FAIL (must flag) | operative FAIL — method promise flagged MATERIAL (header line "PASS/FAIL: FAIL") | OK |
| 15 | Voice probe | voice-emotion | p3 bounded-empirical-claim | PASS (must not flag) | PASS | OK |
| 16 | Voice probe | voice-emotion | p4 bounded-source-limit | PASS (must not flag) | PASS | OK |
| 17 | Voice probe | voice-emotion | p5v2 reader-present-doubt | PASS (must not flag) | PASS | OK |
| 18 | Voice probe | voice-emotion | p6v2 reader-present-doubt | PASS (must not flag) | PASS | OK |

## Check-by-check verdict

1. **PASS test — PASS (6/6).** All three chapter judges returned PASS on the real GSBS
   chapter-02 fixture given as both texts (reader-journey with the PREVIOUS CHAPTER input),
   twice per judge. No manufactured material gap.
2. **Repeatability — PASS (3/3, the two 2026-08-17-0731 failure lanes).** belief-mechanic:
   PASS/PASS with byte-identical ASSIGNED-TRANSITION verdict blocks (all OK / NONE ASSIGNED).
   voice-emotion: FAIL/FAIL with the same highest-impact failure class both times (assigned
   first-instruction reads as clinical consent/compliance paperwork, Gap 1 MATERIAL — the
   known legitimate FAIL on this article); run2 additionally marked `unassigned passages`
   MATERIAL (The Two Reports citation register) — a lower-impact divergent line. This
   satisfies the founder amendment 2026-07-28 option C: consistency measured on per-moment
   verdicts as failure classes, never instances; the decision-relevant failure class is
   identical both runs. reader-journey: PASS/PASS.
3. **Voice honesty probe — PASS (6/6 functional intents).** Both hedged core-verdict and
   method-promise passages were flagged; both bounded empirical/source-limits and both
   reader-present-doubt acknowledgments were not flagged.

## Notes

- **probe-p2 header spelling.** The judge wrote its gate line as `PASS/FAIL: FAIL` rather
  than a bare `FAIL`. The operative verdict is FAIL and the mandatory ASSIGNED-MOMENT block
  marks primary-job promise MATERIAL, so the hedge WAS flagged — the probe's functional
  intent is met. Header is a non-standard spelling of the gate, not a PASS/conflict
  (contrast: the 2026-08-17-0731 run's probe-p2 header said PASS while the block was not all
  OK; here no such contradiction exists).
- **voice-emotion repeatability line variance (row 10).** The additional `unassigned
  passages: MATERIAL` is a second, lower-impact finding present in only one run. It does not
  change PASS/FAIL and does not change the highest-impact failure class; recorded here for
  transparency.
- **PASS-test judge self-notes.** One belief-mechanic run noted that the fixture is verbatim
  Carr prose and flagged the copyright concern (out of lane); both runs still returned PASS
  as the rubric requires for a byte-identical chapter.
- No judge prompt, input, `loop/config.yaml`, or PROGRAM.md was edited. This battery is a
  fresh runs dir; old results were never touched.
- Input substitutions: none — all 18 calls used the existing inputs in `loop/preflight/inputs/`
  (mirror of the 2026-08-14 battery; reader-journey PASS test carries its PREVIOUS CHAPTER
  block as shipped).