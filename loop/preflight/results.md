# Preflight — Judge Calibration Battery (campaign-001)

Date: 2026-07-28. Judge model per config: gpt-5.6-sol, reasoning medium.
Raw traces in `loop/preflight/runs/` (request.json with Authorization
REDACTED, response.sse, response.md, metadata.json). Inputs in
`loop/preflight/inputs/`.

## Overall: FAIL — campaign STOPPED for founder-guided judge repair

| Check | Result |
|---|---|
| 1. PASS test (real GSBS ch-02 as both texts, 2× per judge) | **PASS** — 6/6 runs returned PASS |
| 2. Repeatability (run-012 generated ch-01, identical context, 2× per judge) | **FAIL** — voice-emotion judge |
| 3. Voice honesty probe (6 passage pairs) | **PASS** (after operator probe correction; see notes) |

## Check 1 — PASS test

Article: GSBS chapter-02 "Nature's Guide" supplied as BOTH our chapter and
the real chapter, with honest chapter context. All three judges returned
PASS on both runs. No manufactured material gap: the judges recognize
success.

## Check 2 — Repeatability (FAILING)

Article: `calibration/runs/run-012/chapters/chapter-01-r1.md` (generated
C-01) vs GSBS chapter-01, identical honest context from the run-012 C-01
commission, two runs per judge.

- belief-mechanic: PASS / PASS — consistent. ✓
- reader-journey: PASS / PASS — consistent. ✓
- voice-emotion: FAIL / FAIL — verdict consistent, **but the
  highest-impact failure class differs between runs**:
  - Run 1 top class: the assigned instruction reads as compliance/legal
    language ("chosen threshold", "compensation plan", "qualified clinical
    instruction") plus repeated conditionals hedging the entry promise —
    an authority-hedging class.
  - Run 2 top class: recognition outsourced to researched case reports
    ("Nell Kauls… in a 2024 interview", "Now consider a different
    report") plus facilitator phrases — a report/coaching-register
    distance class.
  - Overlap exists at lower ranks (coaching language appears in both
    reports; case-report distance appears in both), but the top-ranked
    class flips between authority-hedging and report-register distance.

Per PROGRAM §2.2 the remedy is to tighten the voice-emotion judge's
materiality rule (no scoring machinery). `loop/judges/` is read-only for
the loop; judge repair is founder-guided. **Campaign stopped here.**

Suggested (founder decision, not applied): a one-line materiality rule in
`loop/judges/voice-emotion.md` directing the judge to rank the failure
whose exact wording most weakens the chapter's ASSIGNED moment (per
CHAPTER CONTEXT) as highest-impact, so top-rank selection stops flipping
between co-present classes. After any edit: re-run this battery, then a
fresh baseline.

## Check 3 — Voice honesty probe

- p1 hedged core verdict → FAIL (flagged the hedge). ✓ must-flag
- p2 hedged method promise → FAIL (flagged the hedge). ✓ must-flag
- p3 bounded empirical claim → PASS. ✓ must-not-flag
- p4 bounded source limit → PASS. ✓ must-not-flag
- p5/p6 acknowledgment of present doubt, first attempt → FAIL, **but not
  on the doubt acknowledgment**: both reports explicitly endorse the
  acknowledgment and instead flag other material the operator had baked
  into the constructed passages (coaching-speak "keep reading with an open
  mind"; invented absolute failure history "every attempt to stop has
  ended the same way" — itself willpower framing). Operator
  probe-construction defect, not a judge defect. Originals kept.
- p5v2/p6v2 with properly isolated doubt-acknowledgment passages → PASS /
  PASS. ✓ must-not-flag

Verdict: the voice judge flags core-verdict/method-promise hedges and
preserves bounded empirical claims and doubt acknowledgment. Check 3
passes on the corrected instrument.

## State

- Loop position: baseline pending (results.tsv has no data rows).
- Route verification (step 0): all three transports green; kimi-k3 exact
  id confirmed in the Zen Go /models list — config.yaml unchanged.
- Next action: founder-guided repair of `loop/judges/voice-emotion.md`
  materiality rule → re-run preflight → §3 baseline.

---

# Repair ladder addendum (2026-07-28, founder instruction: "find root cause, fix, run again")

Four repairs applied and tested; full traces in runs2/–runs5/.

| Attempt | Change (commit) | Result on check 2 (voice-emotion) |
|---|---|---|
| 1 | Materiality ranking rule: assigned moments outrank unassigned drift (6c4f717) | FAIL — Gap 1 flipped between two assigned moments (mantra debut vs promise) |
| 2 | Fixed precedence among assigned moments: promise > instruction > debuts > echoes (5212c42) | FAIL — ranking held, but one run failed to DETECT the promise gap at all |
| 3 | Mandatory sweep: every assigned moment checked in fixed order, all failures reported (043153c) | FAIL — sweep held, but the materiality call flipped (instruction judged material in one run, immaterial in the other) |
| 4 | config: judge_reasoning medium → high, prompts unchanged (0c2401d) | FAIL — run1 top: promise-hedging; run2 top: M-06 coaching-speak; run2 judged the promise moment immaterial |

Constant across all five batteries: check 1 PASS test 6/6, check 3 probes
6/6 (with v2 doubt probes), belief-mechanic and reader-journey repeatability
consistent. The voice judge discriminates correctly; it is unstable only in
the boundary materiality call among co-present borderline flaws in the
repeatability article (run-012 generated chapter), which carries 2–3 real
voice flaws of similar size (promise-hedging, M-06 coaching-speak,
case-report distance — the same classes recur across every run).

## Root cause (final)

A single-sample judge cannot deterministically pick one top class among
several co-present failures of comparable materiality. Prompt tightening
moved the flip (ranking → detection → materiality) without removing it;
reasoning effort did not remove it either.

## Founder options (not applied)

A. Restructure the voice judge's output: one explicit MATERIAL/OK verdict
   per assigned moment (sweep becomes the format, top class becomes
   derived, not sampled). Judge edit — founder-guided; then re-run battery.
B. Rule that check 2 consistency for the voice lane means: same PASS/FAIL
   and same per-assigned-moment verdicts, rather than one top class.
   Requires a founder edit to PROGRAM §2.2.
C. Both A and B together (most robust; makes the repeatability criterion
   match how decisions actually use judge output — failure classes, not
   instances).
D. Also rule on judge_reasoning: high produced no repeatability gain at
   ~2× latency; recommend reverting to medium unless kept for other
   reasons.
