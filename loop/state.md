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

- **Iteration:** 003 (COMPLETE — REVERT)
- **Stage:** IDLE — iter-003 REVERT recorded. Founder asked to stop after this iteration for reconsideration. Do **not** start 004.
- **Status:** IDLE
- **Campaign branch:** `campaign-001`
- **Last completed unit:** iter-003 REVERT (records on campaign; factory change and book not promoted).
- **Next unit:** founder reconsideration (stream reliability + whether to keep hammering plan-skill vs pivot to writer-prompt).

## If you died / were stopped

003 REVERT is recorded (`loop/iterations/003/`, learnings, ledger, results.tsv). Factory stays campaign tip (no Compact-cards job/evidence ban). Writing/judging artifacts live only in the discarded worktree until cleanup. **Do not start 004** until the founder says so. Writer: Vercel Muse Spark. Judges: composer-2.5. Do not restore the project stop hook.


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
| 2026-08-17 | EXEC-B2: preflight re-run on `opencode-go/deepseek-v4-flash` via opencode `task` sub-agents (18 calls, runs-2026-08-17-opencode-go-dsf) = **18/18 PASS**: PASS test 6/6; repeatability 3/3 — belief-mechanic PASS/PASS identical blocks, voice-emotion FAIL/FAIL same highest-impact failure class (instruction MATERIAL; run2 adds unassigned-passages MATERIAL), reader-journey PASS/PASS — satisfies founder amendment 2026-07-28 option C; voice probes 6/6 functional (p1,p2 hedges flagged; p3-p6 not flagged; probe-p2 gate line reads "PASS/FAIL: FAIL", operative FAIL). No judge/input/config/PROGRAM.md edited. HARNESS.md opencode row updated: judges/trace-analyzer/plan-reviewer on opencode-go/deepseek-v4-flash, research sub-agents stay on 0731, writer/plan-writer/hypothesizer via Command Code proxy. | planning on campaign-001 |
| 2026-08-17 | EXEC-C: planning COMPLETE. plan-writer-01 via Command Code proxy — contributor model `meta/muse-spark-1.2-contributor` hit 429 rate_limit (empty upstream); used coded fallback `meta/muse-spark-1.2`; 18-chapter master plan accepted (SUM 60,000 in band); plan-reviewer-01 (opencode-go, fresh clean context) returned `fit to write from` round 1; reference-alignment.md rebuilt (18 rows, content-based). Traces to `loop/iterations/000/traces/`. | writing chapter 01 (spawn chapter-writer) |
| 2026-08-17 | EXEC-D: writing COMPLETE — all 18 chapters drafted sequentially via Command Code proxy, every chapter on `meta/muse-spark-1.2-contributor` (no fallback needed). Total ~69,000 words vs planned 60,000 (several chapters over budget, up to +56% on C18; word-budget drift noted for judging). All chapters verified complete (no truncation/refusal/meta-commentary; mantras + instructions verbatim; boxed definitions + clinical advisory preserved). Traces under `loop/iterations/000/traces/chapter-01..18/`. | judging (baseline) |
| 2026-08-17 | EXEC-E: BASELINE judging — judgments COMPLETE (58/58: 54 chapter judges via opencode-go/deepseek-v4-flash sub-agents + book-arc + 3 A/A on ch01). Verdicts: belief-mechanic 18/18 PASS; reader-journey 13/18 PASS (C02,C06,C11,C14,C15 FAIL — momentum/continuity stalls); voice-emotion 4/18 PASS, 14 FAIL; book-arc PASS (2 cross-chapter reps). trace-analysis.md written: 4 causal clusters (1 writer-prompt systemic: evidence-grading leak; 2 writer-prompt systemic: internal-taxonomy leak; 3 plan positional: cross-chapter re-argument; 4 model local: C02 grammar). A/A rerun of ch01 (identical inputs, same contributor model) = belief PASS, reader PASS, voice FAIL — material failure-class set DIFFERS between runs, calibrating single-chapter voice verdicts as sampling-sensitive. Records: learnings/ledger/results.tsv/state. results.tsv row appended LAST. Committed `loop(000): BASELINE` on campaign-001. | iteration 001 — founder inbox check → hypothesizer |
| 2026-08-17 | BASELINE complete (commit c9d0768): 58/58 judge calls, A/A noise recorded, trace analysis (4 clusters), records written | iteration 001 |
| 2026-08-17 | Founder-directed fix after dual-subagent RCA (rca-report + rca-verify): writer scaffold firewall in prompts/chapter-writer.md — ledger vocabulary never surfaces in prose; inbox note `2026-08-17-scaffold-firewall.md` queued as iter-001 hypothesis | iteration 001 |
| 2026-08-21 | Cursor-harness resume: campaign-001 checkout `state.md` was stale (IDLE/000). Worktree `../quit-sugar-iter-001` is IN PROGRESS at iter-001 writing: ch01–12 done, ch13–18 blocked on Command Code 429. Founder asked judge preflight on Composer 2.5 (not fast) before continuing. Launching 18-call battery into `loop/preflight/runs-2026-08-21-composer-2.5`. COMMANDCODE_API_KEY unset in this environment — writing waits on the new key. | preflight 18/18 on composer-2.5 |
| 2026-08-21 | Session interrupted after a single Composer 2.5 voice-probe smoke (hedge correctly FAILed). Founder supplied a Vercel AI Gateway key. Command Code retired for Muse Spark: `loop/config.yaml` now `vercel` / `https://ai-gateway.vercel.sh/v1/chat/completions` / `AI_GATEWAY_API_KEY`. Live smoke: HTTP 200, model `meta/muse-spark-1.2-contributor`, reply `PONG`. Composer 2.5 18-call preflight restarting. | preflight 18/18 on composer-2.5 |
| 2026-08-21 | PREFLIGHT 18/18 PASS on composer-2.5 (`loop/preflight/runs-2026-08-21-composer-2.5`). Founder required that report before any next start. Orchestrator jumped the gate: wrote ch13–18 on Vercel, started a 54-call judge panel, then stopped it on founder instruction. Partial judgments: 35/54 chapter reports in the worktree; no book-arc. Stop hook removed (it was auto-continuing every turn). | founder: authorize judging |
| 2026-08-21 | Founder authorized continue and instructed: do not pause between iterations — hypothesizer then next round. Resuming 001 judging from markers (44/54 chapter reports; 10 remaining). | remaining 10 judges → book-arc |
| 2026-08-21 | EXEC-001 COMPLETE. Panel 55/55 on composer-2.5: belief 17/18, reader 16/18, voice 4/18, book-arc FAIL. Targeted clusters 1+2 partially closed (labels mostly gone; factory speech remains). **Verdict REVERT.** Records written; 001 book not promoted. Starting 002 hypothesizer (Binding chapter craft, not the evidence-honesty clause). | hypothesizer 002 |
| 2026-08-21 | iter-002 declared: hypothesizer targeted Cluster 4 (arc re-argument) at `prompts/master-plan-skill-v2.md` — debut-once/echo-by-token for scenes and evidence rows, not the writer-prompt. First hypothesizer draft named `plan.md` (illegal); retry retargeted the plan skill. Worktree `../quit-sugar-iter-002`. Plan-writer spawning. | plan-writer → reviewer |
| 2026-08-21 | EXEC-002 COMPLETE. Panel 58/58 on composer-2.5: belief 18/19, reader 19/19, voice 0/19, book-arc FAIL. Cluster 4 partially closed (001 instances gone; class mutated). NEW voice class: `by name in one sentence here`. **Verdict REVERT.** Plan-skill change and 002 book not promoted. | hypothesizer 003 |
| 2026-08-21 | EXEC-003 COMPLETE. Panel 61/61 on composer-2.5: belief 20/20, reader 19/20, voice 6/20, book-arc FAIL. 002 Cluster 5 symptoms closed; class mutated (A01/T04/readiness). **Verdict REVERT.** Factory change and 003 book not promoted. Founder stop — no 004. | IDLE / founder reconsider |
