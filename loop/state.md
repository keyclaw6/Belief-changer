# Loop State — the live checkpoint

> The orchestrator updates this file at every stage boundary and before any
> long wait. A fresh agent reads it first (PROGRAM §0) and can continue the
> run from exactly here.
>
> Two rules keep it honest:
> - **`Status` is exactly `IDLE` or `IN PROGRESS`** (verbatim — no other token).
> - **This file can lag real work.** The on-disk markers — research bank files,
>   `production-books/quit-sugar/chapters/`, `loop/iterations/NNN/judgments/` —
>   are the ground truth. If they disagree with what's written here, trust the
>   markers and resume from the furthest point they support (PROGRAM §0).
>   Write the *next* unit before starting it, so a crash mid-unit never loses it.
> - **Only final-named files are markers.** The orchestrator writes to
>   `<name>.partial` and renames when complete; a `.partial` file is unfinished
>   work to discard and redo, never a completed unit (PROGRAM §4 Step 3).
>
> **Single operator.** One orchestrator drives the loop at a time. There is no
> locking or ownership token: if you can edit this file, you are the driver. On
> resume, the previous run is by definition no longer running — just continue
> from the markers.

## Position

- **Iteration:** 000 (baseline)
- **Stage:** research — integrate + synthesize (banks populated; criterion NOT yet clear:
  bank-02 P-04 = 0 packets, bank-07 86% single-domain; synthesis pending)
- **Status:** IN PROGRESS — baseline end-to-end run
- **Campaign branch:** `campaign-001` (created from `main` 2026-08-14)
- **Last completed unit:** preflight (PROGRAM §2) re-run PASS on 2026-08-14
  with the DeepSeek V4 Flash judge model — 18/18 checks correct
  (`loop/preflight/runs-2026-08-14-deepseek-v4-flash/`): 6/6 PASS-test,
  6/6 repeatability (identical verdict blocks both runs), 6/6 voice probes
  (hedges flagged, bounded claims + present-doubt not flagged).
- **Next unit:** research gap-fill (bank-02 P-04; bank-07 domain diversity), then synthesis

## If you died / were stopped

Baseline research (iteration 000) is IN PROGRESS. Research banks under
`production-books/quit-sugar/research/banks/` are the live checkpoint together
with this file: 10 banks, 994 packets mined. Outstanding: bank-02 has zero P-04
(energy-crash yo-yoer) belief-map packets; bank-07 draws 86% of entries from
pmc.ncbi.nlm.nih.gov (§6 caps any single domain at 50%); synthesis
(`lived-experience.md`, `scientific-evidence.md`, `research-log.md` tables,
`sources/`) not written. Resume at PROGRAM §4 "Stage: Research": dispatch
targeted gap-fill sub-agents (P-04 lane; non-PMC science diversity), then
synthesize until the §7 completion criterion clears across ≥3 personas.
Confirm the branch is `campaign-001` before acting. Only final-named files are
markers; `<name>.partial` is unfinished work to redo. Old pre-campaign
`research/_rounds/round-1/` is archaeology, NOT reused by the baseline.
Bank-09's leaked agent-monologue tail (post-packet lines) was truncated
2026-08-17; its 168 packets are intact.

## Journal

| Time (UTC) | What happened | Next |
|---|---|---|
| 2026-08-12 | Loop state file created; preflight already PASS (2026-08-07) | baseline research |
| 2026-08-14 | Preflight re-run PASS on DeepSeek V4 Flash (18/18 checks) — prior runs dirs (runs2–runs8) stale on gpt-5.6-sol/gpt-5.6-luna | baseline research |
| 2026-08-14 | Campaign-001 branch created from main; preflight record committed; baseline started | research dispatch → banks |
| 2026-08-17 | Operator handoff → opencode-harness orchestrator (subagents on alibaba-token-plan/deepseek-v4-flash-0731); audit: 994 packets OK, bank-09 tail corrupt (not packets), gaps bank-02 P-04 + bank-07 diversity; checkpoint commit | gap-fill dispatch |
