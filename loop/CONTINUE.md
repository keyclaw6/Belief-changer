# Continue the auto-research loop

Load-bearing handoff for the next auto-research session. Read this after
`AGENTS.md`, `docs/AUTO-TUNING-LOOP.md`, and `loop/PROGRAM.md` §0.

This chat closed 2026-09-06. It applied the Astra + Fable 5.1 Carr-distance
consult. It did **not** run 041.

## Who you are

You are the **auto-research** conversation (`loop/PROGRAM.md`). You are
not the book factory. Factory = Muse Spark 1.3 via
`prompts/factory-orchestrator.md` (or `write_replicate.py` as that
conversation's tool). Do not write chapters here. Do not send email.
Do not print API keys. Do not `pgrep -af 'agent --'`.

## Position

- **Campaign branch:** `campaign-001` (work here; never on `main`).
  After this close-out Git has only `main` and `campaign-001`
  (local and `origin`). Create iteration worktrees from
  `campaign-001` per PROGRAM. Do not recreate `iter-*` or
  `cursor/*` leftover branches.
- **Production books:** 037 KEEP (`production-books/quit-sugar/` 54612w,
  `quit-smoking/` 57583w). 038 OVERCLAIM is in the reviewer. 039 HEADER
  ownership and 040 writer landing stay dropped.
- **Last dual iteration:** 040 QUANTIFY + restore (invalid PRIMARY; the
  voice judge was counting Carr ALL-CAPS as factory-speech).
- **Instrument:** 2026-09-06 Carr-distance panel (this close-out).
  3-strike clock is reset.
- **Carr distance on 037 (consult, not yet rejudged):**
  indistinguishable-from-Carr **42%** (sugar 40, smoking 45). Easyway
  engine present 60–73%. Do not average those numbers. Census PASS is not
  Carr-likeness.
- **Status:** IDLE. Next unit is **041 BASELINE**.

## 041 — dual BASELINE (do this first)

No factory wording change. No new hypothesis. No plan rewrite.
Pi `run_preflight.sh` is still the old 18-call battery; do not treat it
as the Carr-distance probe. 041's dual rejudge *is* the first sample.

1. Copy frozen 037 chapters into `loop/iterations/041/<slug>/replicate-a/`
   (traces `response.md` + chapters). Reuse 037 plans.
2. Run `judge_replicate.py` on both subjects (one at a time). The panel
   now includes `carr-distance`. Record `score-deficit`.
3. That census is the new dual-subject floor and the first noise sample
   on this instrument. Do not KEEP. Do not restore. Write BASELINE.
4. Identify the carried factory: 030 HEADER exemption, 036 RE-ARGUMENT
   finding, 037 LENGTHEN, **038 OVERCLAIM**, style-guide §B4 + §B5 op 9,
   this instrument.

If a PRIMARY quote in a later run is Carr-shaped, halt (PROGRAM
pre-spend GSBS control).

## 042+ — first hypothesis after baseline

The CH-01 card rule and style-guide Part B (plain Carr sentences) are
already in the factory files. They have not been measured. First
KEEP-eligible experiment: regenerate plans + chapters so those rules
fire. Score on Carr-distance `score-deficit` and comparison `partial`,
never on `factory-speech`.

Then 10–20 iterations is authorized only on this instrument. Stay idle
rather than manufacture a hygiene PRIMARY. Empty intersection → stop.

## Do not replay

020–024, 028/029, 030 HEADER finding *text*, 032 writer anatomy drop
IN THIS CHAPTER + ordinal lead-in, 036 RE-ARGUMENT finding text,
037 LENGTHEN assignment, 039 HEADER ownership, 040 writer landing.
`willpower-lexicon` (naming the enemy) is not PRIMARY. `re-argument`
is never PRIMARY.

## Models (founder-only)

- Factory writer/reviewer/planner: Muse Spark 1.3 Go → Zen
  contributor-free → Vercel contributor.
- Judges: composer-2.5 via `judge_replicate.py`.
- Hypothesizer: GPT-6 Astra (`scripts/loop-runner/hypothesize.py`);
  Fable 5.1 fallback. No `temperature`. Optional Astra
  `reasoning_effort: low`.

## Cadence

Wake → sugar 13 / smoking 14 / PANEL DONE / live write or judge. If
unfinished and not stuck, sleep. One judge runner at a time. Census
with `census_judgments.py`. Hypothesize:

```
dotenvx run -f .env -- env BC_REPO=/home/kab/Belief-changer ITER=NNN \
  python3 -u scripts/loop-runner/hypothesize.py
```

Do not re-arm 20-minute timers. `git add` named files only — never
`git add -A`. Do not add `hypothesizer-input.md`, `.opencode/goals/`,
`.pi/npm/`, leftover 009/031 logs.

## What this close-out already landed

Judges, PROGRAM KEEP band, 3-strike by class, GSBS control, CAP ≠ ACCEPT,
chapter-reviewer on the editable list, CH-01 card rule, style-guide
plain Carr + runtime Carr DEFAULT lock, Reddit in scope, miners write
the parent checkout, plan-writer/plan-reviewer read banks in full (no
100 kB truncate), Carr-distance judge. Full lesson: `loop/learnings.md`
entry `campaign-001 close-out`.

## Known leftovers (do not treat as unfinished instrument)

- Pi `run_preflight.sh` is still the old 18-call battery. Cursor does
  not run it. Do not block 041 on rewriting it.
- Style-guide Part A still documents Freedom Model / Burgeon as
  brief-level overrides. Runtime contract is Carr DEFAULT + Part B.
- Plan-writer now receives full banks (~0.3–0.6 MB). If Muse refuses
  the context, record the failure — do not silently truncate.
- 041 has not been run. That is the next session.
