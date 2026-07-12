# Retirement recommendations (RECOMMEND ONLY — not executed here)

The new loop (`PROGRAM.md` + `scripts/loop/` + `loop/`) supersedes most of the
old calibration-lab scaffolding. This file lists what the founder can retire and
why. **Nothing here has been deleted or moved** — per the build constraints, this
agent writes files only. Execute (or don't) after review.

## Safe to delete — superseded, no code dependency

- `calibration/HARNESS.md` — superseded by `PROGRAM.md` (the loop is now a boring
  fixed 5-step runbook, not a 40 KB doctrine). NOTE: its §3b research doctrine is
  being migrated separately by another agent; confirm that migration landed
  before deleting.
- `calibration/STATE.md` — the STOPPED recovery checkpoint; the loop's live state
  is `loop/results.tsv` + `loop/learnings.md`. Its route law ("OpenRouter only
  for Opus 4.6 writing") is already SUPERSEDED by the founder's 2026-07-12
  decision (MiniMax-M3 writer + cross-family judges over OpenRouter).
- `calibration/ESCALATION.md` — the escalation rule is now one paragraph in
  `PROGRAM.md` (3 consecutive non-improvements → stop, summarize, surface).
- `calibration/hypotheses.md` — its live content (untested H-001/H-015/H-016/
  H-017 and the refuted-lever autopsy H-045/046/047/049) is absorbed into
  `loop/learnings.md`. Delete only after confirming nothing else references it.
- `prompts/chapter-commissioner.md` — the commission subsystem was refuted in
  run-014 (and H-047/H-049); the loop's writer reads the master plan directly, no
  commissioner. Confirm no pipeline/prompt still dispatches it before deleting.

## Retired judge prompts (3-role panel) — delete the prompts, mind the code

The retired 3-role Stage-A panel punished the REAL Carr book for fear/shame/
overreach (the sanitization failure). Replaced by the two one-question prompts in
`calibration/judges/factory-authenticity-pairwise.md` and
`factory-detection-probe.md`.

- `calibration/judges/method-integrity-epistemic-safety.md` — retired role prompt.
- `calibration/judges/literary-craft.md` — retired role prompt.
- `calibration/judges/belief-change-efficacy.md` — retired role prompt.

CAUTION: `scripts/eval/judge_protocol.py` (`ROLE_SPECS`) names these three files,
and `scripts/eval/judge_panel.py` + the tests load them. Deleting the prompts
without also retiring the role-panel code path will break
`judge_panel.py --prompt`-less (native) mode and the taxonomy tests. Retire the
prompts and their code path together, or leave both.

## DO NOT DELETE YET — blocking import dependency (import findings)

- `scripts/eval/judge_v23.py` and `scripts/eval/judge_legacy.py` are described as
  "prior instrument generations," but they are **still imported**:
  - `scripts/eval/judge_panel.py` lines 8–11:
    `from judge_legacy import DIMS, aggregate, map_verdict, validate_pairwise`,
    `import judge_v23 as V23` (also `import native_judge as N`,
    `import judge_protocol as V2`).
  - Tests import them: `tests/test_judge_v23.py`, `tests/test_judge_panel.py`,
    `tests/test_judge_protocol_v2.py`, `tests/test_native_judge*.py` — all
    discovered by `scripts/check.sh` step 4.
  Deleting either module now breaks `judge_panel.py` at import time and fails
  `check.sh`. The new loop does NOT import any of them (it uses
  `scripts/loop/judges.py` over `scripts/eval/model_endpoint.py`), so they are
  dead weight for the loop — but they are LIVE for `judge_panel.py` and its
  tests. Retire `judge_panel.py` + `native_judge.py` + `judge_protocol.py` +
  their tests as one unit FIRST, then `judge_v23.py`/`judge_legacy.py` can go.
  Until then, leave all of them in place.

## Keep (reused by the new loop — do NOT retire)

`scripts/eval/evallib.py`, `metrics.py`, `repetition.py`, `mantra_check.py`,
`extract_reference.py`, `model_endpoint.py`, and their tests
(`tests/test_eval_scope.py`, `test_repetition.py`, `test_mantra_check.py`,
`test_pipeline_contract.py`, `test_judge_history.py`). `score.py` wraps these
directly.
