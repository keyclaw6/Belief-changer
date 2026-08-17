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
- **Stage:** research COMPLETE — banks gap-filled + synthesis written; P-04 lane ≥3 personas clear. Preflight re-run on 0731 = BLOCKED (repeatability not met). Next unit: founder decision on the 0731 judge (re-run preflight on a more repeatable judge model), then planning.
- **Status:** IN PROGRESS — baseline end-to-end run
- **Campaign branch:** `campaign-001` (created from `main` 2026-08-14)
- **Last completed unit:** preflight (PROGRAM §2) re-run on 0731 = **BLOCKED** — NOT 18/18.
  Opencode harness, judge model `alibaba-token-plan/deepseek-v4-flash-0731`
  (`loop/preflight/runs-2026-08-17-alibaba-0731/`): PASS test 6/6 OK; repeatability
  1/3 OK (belief-mechanic run1 PASS vs run2 FAIL; voice-emotion run1 FAIL-token vs
  run2 PASS-token although both mark instruction MATERIAL); voice probes 6/6 functional
  (p1,p2 hedges flagged; p3-p6 not flagged), with a p2 header/verdict-block contradiction.
  The 2026-08-14 DeepSeek V4 Flash battery remains the last PASSING one (18/18).
- **Next unit:** founder decides judge model for judging on campaign-001; 0731 did not
  satisfy PROGRAM §2 repeatability in this harness. Planning (research complete) is gated on that.

## If you died / were stopped

Baseline research (iteration 000) is IN PROGRESS but the research stage is COMPLETE. Research banks under
`production-books/quit-sugar/research/banks/`: 10 banks, 1040 packets mined. Gap-fills done: bank-02 has 14
P-04 (energy-crash yo-yoer) belief-map packets across 4 domains; bank-07 now 75 packets with PMC at 49.33%
(37/75, ≤50%) and 8 distinct domains. Synthesis written under `production-books/quit-sugar/research/`:
`lived-experience.md`, `scientific-evidence.md`, `research-log.md` (all five tracking tables + dispatch
history), and `sources/` (26 source packets). Completion criterion (§7) clears across ≥3 personas (P-01,
P-02, P-03, P-04 all substantive). Resume at the next unit: preflight re-run on the quota's 0731 judge
model (PROGRAM §2, fresh runs dir), then planning. Confirm the branch is `campaign-001` before acting. Only
final-named files are markers; `<name>.partial` is unfinished work to redo. Old pre-campaign
`research/_rounds/round-1/` is archaeology, NOT reused by the baseline. Bank-09's leaked agent-monologue
tail (post-packet lines) was truncated 2026-08-17; its 168 packets are intact.

## Journal

| Time (UTC) | What happened | Next |
|---|---|---|
| 2026-08-12 | Loop state file created; preflight already PASS (2026-08-07) | baseline research |
| 2026-08-14 | Preflight re-run PASS on DeepSeek V4 Flash (18/18 checks) — prior runs dirs (runs2–runs8) stale on gpt-5.6-sol/gpt-5.6-luna | baseline research |
| 2026-08-14 | Campaign-001 branch created from main; preflight record committed; baseline started | research dispatch → banks |
| 2026-08-17 | Operator handoff → opencode-harness orchestrator (subagents on alibaba-token-plan/deepseek-v4-flash-0731); audit: 994 packets OK, bank-09 tail corrupt (not packets), gaps bank-02 P-04 + bank-07 diversity; checkpoint commit | gap-fill dispatch |
| 2026-08-17 | EXEC-A: bank-09 monologue tail removed (now 260 lines, 168 packets, 0 invoke); Miner-1 (bank-02 P-04) + Miner-2 (bank-07 diversity) spawned in parallel via backgrounded `opencode run` — both stalled after initial appends (bank-02 P-04 = 8, bank-07 untouched); re-dispatching as harness-native subagents | mine → synthesize |
| 2026-08-17 | EXEC-A research COMPLETE. Miner-1: bank-02 P-04 0→14 packets, 4 domains (bloodsugardiet/vanadia/deanebarker/johnfawkes.substack). Miner-2: bank-07 43→75 packets, PMC 86%→49.33% (37/75), 8 domains; +32 non-PMC (WHO/HSPH/Harvard/NHS/MedlinePlus/NIDA/Hopkins). Synthesis written: lived-experience.md (106L), scientific-evidence.md (34L), research-log.md tables + dispatch filled, sources/ 26 packet files. Total 1040 packets across 10 banks. | preflight re-run on 0731 → planning |
| 2026-08-17 | EXEC-B: preflight re-run on `alibaba-token-plan/deepseek-v4-flash-0731` via opencode `task` sub-agents (18 calls, runs-2026-08-17-alibaba-0731) = **BLOCKED**: PASS test 6/6 OK; repeatability 1/3 OK — belief-mechanic PASS/FAIL, voice-emotion FAIL-token/PASS-token (both mark instruction MATERIAL); voice probes 6/6 functional (p2 header/block contradiction). 0731 does not satisfy PROGRAM §2 repeatability in this harness. No judge/input/config edited. 2026-08-14 DeepSeek V4 Flash remains the last PASSING (18/18) battery. | founder: pick judge model for campaign-001 → planning |
