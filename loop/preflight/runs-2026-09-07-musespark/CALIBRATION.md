# Preflight recalibration — Muse Spark 1.3 contributor via opencode go

Date: 2026-09-07. Harness: OpenCode (`opencode run --model
opencode-go/muse-spark-1.3-contributor --variant high --auto`, one fresh
session per call, prompt = role prompt + rubric + one input file).
Fresh runs dir per PROGRAM §2 (no stale reuse). Judge prompts unchanged
(this instrument = 2026-09-06 Carr-distance panel).

## Overall: PASS (29/29 conclusive after 2 retries)

| Check | Result |
|---|---|
| 1. PASS test, belief/voice/journey/comparison ×2 + late belief/journey ×1 | **PASS** — 12/12 runs PASS, all counts 0 |
| 2a. Defective controls (voice P2 method-promise hedge; belief b1/b2) | **PASS** — all fire with the required BLOCKING class |
| 2b. Carr-as-OUR vs matched other Carr chapter | **NOT RUN** — no input file exists for it |
| 3. Repeatability (repeat-* ×2 per lane) | **PASS** — PASS/PASS, identical BLOCKING sets, NOTED diffs 0 (≤ ±1 allowed) |
| 4. Voice honesty probe (P1–P6) | **PASS** — P1→`assigned-verdict-hedge` FAIL, P2→`method-promise-hedge` FAIL, P3–P6 PASS |
| 5. Belief/journey honesty probe | **PASS** — b1 FAIL `credit-intact` ×2, b2 FAIL `harm-not-belief`, b3 PASS, j1 FAIL `journey-incomplete`, j2 PASS |
| 6. Carr-distance GSBS-vs-GSBS probe | **PASS** — score 100, deficit 0 (reduced scale: ch1–3 slice as both books, see below) |

## Notes

- 2/29 first attempts returned empty replies (`repeat-belief-mechanic-run2`,
  `repeat-voice-emotion-run2`, exit 0, no text). Retry on the same primary
  succeeded. Watch for this in the loop's judge runner (empty ≠ done).
- b1 probe rerun adds blocking `reframe-unsettled=1` beside the required
  `credit-intact=1` (FAIL both times, required class present). Same wobble
  the 2026-09-04 composer-2.5 probe showed — parity with the old instrument,
  not a regression.
- Carr-distance probe is reduced-scale (GSBS ch1–3 ≈ 11k words per side;
  full-book 60k×2 was judged too heavy for a calibration probe). The 100-path
  logic is verified; 041's dual rejudge is the first full-book sample.
- `response.md` files start with a dotenvx injection line (`⟐ ...`); graders
  must skip it. `prompt.md` + `metadata.json` + `stderr.log` sit beside each.
- Raw-HTTP Muse calls from repo scripts fail on this harness (Go: 400
  MissingSessionID — needs the OpenCode session header; Zen free: 400
  OpenCode-only; Vercel: 402). Judge spawns must go through `opencode run`.
- Experiential 2026-09-07: `gpt-6-astra` → 429 free daily limit (resets 00:00
  UTC); `claude-fable-5.1` (dot alias) → 200 OK. The dash alias
  `claude-fable-5-1...` is not granted.
