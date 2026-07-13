# PROGRAM — the self-improvement loop (operator runbook)

A boring, fixed loop, copied in shape from github.com/neosigmaai/auto-harness:
**RUN the pipeline → SCORE against the real Carr book → GATE keep/revert → RECORD → ONE hypothesis → repeat.** Intelligence goes into the chapters and the diagnosis — never into redesigning the loop mid-run. The 2026-07-11/12 "calibration lab" (branch `calibration-lab`) died because ~90% of tokens went to process (preregistrations, judge-instrument rebuilds, commission audits, direction audits) instead of prose; this loop refuses that. A mechanical failure is fixed mechanically, noted in one line, never treated as a semantic event. Loop grievances go under "Harness debt" in `loop/learnings.md`; the founder addresses them between blocks.

**Goal.** A factory that takes ANY subject brief and produces an Allen Carr Easyway book — the same voice, method, structure, and nerve as the real corpus. We are not competing with Carr and not sanitizing him: **the reference IS the target.** Fear, shame-at-the-trap, stern commands, and confident medical-sounding assertions are features of authentic Carr to reproduce.

**How closeness is measured (founder direction, 2026-07-13).** Not a blind A/B contest — "ours beat Carr's in some judge's opinion" proves nothing, because Easyway is the goal, not the opponent. Instead a **reference-anchored rubric**: the judge reads the real GSBS chapter (ground truth) next to our chapter for the same position, scores **distance from the reference** on six anchored craft dimensions (voice, method, structure, repetition, register, rhythm — 0–10 each), and returns the **3–5 highest-impact improvement suggestions**, each tagged with the factory asset that owns the fix. Those suggestions are the tuning engine. Judge prompt: `calibration/judges/carr-likeness-rubric.md` (frozen per campaign). The pairwise/detection instrument is retired from the loop; a blind detection probe may return at Stage C as a final exam, never as the loop metric.

**Target this campaign:** `production-books/quit-sugar/` (master plan R2, reviewed "fit to write from"). Reference: *Good Sugar Bad Sugar*, extracted locally (step §2).

## §0 Operator handoff (paste into Codex — fresh session)

```
Read PROGRAM.md at the root of https://github.com/keyclaw6/Belief-changer
(branch factory-v2-owner) and execute the loop exactly as written. You are
the OPERATOR: you execute; you do not redesign the loop, the judge rubric,
the scoring, or the thresholds.

PROTECT YOUR CONTEXT WINDOW: drive the loop through fresh subagents and
keep only compact results in your own context. Chapter writing, reviewer
passes, judge tasks, and ALL whole-chapter or whole-book reading happen
inside subagents — you handle file paths, score summaries, suggestions,
and ledger rows, never full prose. Read the style guide once at session
start, then reference it by path. If your context runs low, finish the
current step, commit, and start a fresh session — the loop resumes from
loop/results.tsv + loop/learnings.md by design.

Read, in order: PROGRAM.md, AGENTS.md, prompts/style-guide.md (both parts),
then the tail of loop/results.tsv and loop/learnings.md for current state.
Then run the next iteration (§4). Commit after every iteration. Stop for
founder review each block (§5).
```

## §1 Model matrix & routing (founder, 2026-07-13 — supersedes everything earlier)

| Role | Model | Route |
|---|---|---|
| Chapter writer | **Claude Opus 4.6, reasoning disabled** | OpenRouter (`OPENROUTER_API_KEY`) |
| Research agents | **DeepSeek V4 Pro, top reasoning** | OpenRouter |
| Master-plan writer | **GPT‑5.6 Sol, reasoning `xhigh`** | **fresh native Codex subagent (founder's OpenAI subscription)** |
| Judges (rubric panel) | **GPT‑5.6 Sol, reasoning `xhigh`** | **fresh native Codex subagents** |
| Plan/chapter reviewers | strongest available non-writer model | native surface preferred |

- **GPT models NEVER route through OpenRouter.** Sol runs only as fresh native Codex subagents on the founder's subscription. OpenRouter carries ONLY Opus chapter-writing and DeepSeek research.
- The 2026-07-12 "MiniMax-M3 writer" note in the old config was a founder mix-up from another project and is **RESCINDED**.
- One judge model per campaign; `judge_k` fresh contexts per chapter, scores averaged.

## §2 Setup (once per environment)

1. Clone the repo, branch `factory-v2-owner`; you need push access.
2. `python3` (stdlib only). `OPENROUTER_API_KEY` exported — used ONLY for writer + research calls.
3. Extract the reference (local only — `calibration/reference/` is gitignored; never commit extracted text):
   ```
   python3 scripts/eval/extract_reference.py \
     --epub "analysis/reference-books/The easyway Good Sugar Bad Sugar.epub" \
     --out calibration/reference/gsbs
   ```
   Front-matter pairing is handled by `reference_chapter_offset` in `loop/config.yaml` (verified: list positions 1–2 are front matter; position 3 = Chapter 1).
4. **Instrument ceiling check (once per campaign):** `python3 scripts/loop/score.py --control-ref --chapters 1-3 --iter 0` → dispatch the 6 emitted judge tasks as fresh native Sol subagents → re-run the same command to aggregate. The real chapters judged as candidate should score ≈1.0 — that number is the rubric's ceiling and your first noise sample. Record it in `loop/learnings.md`. **Do NOT run gate.py on the control** (a control row would poison the baseline); product iterations start at iter-001.

## §3 The tunable surface (the ONLY files an amendment may touch)

`prompts/style-guide.md` · `prompts/chapter-writer.md` · `prompts/chapter-reviewer.md` · `prompts/master-plan-skill-v2.md` · `prompts/master-plan-reviewer-v2.md` · `prompts/research-agent.md` · `production-books/_template/` · the book's `master-plan.md` (only by re-running the plan stage — never hand-edited)

- **One amendment per iteration** — one asset, one mechanism, written as a one-paragraph hypothesis in `loop/learnings.md` BEFORE the iteration runs. Source hypotheses from the judges' suggestions and reviewer diagnostics.
- **Research amendments are out of scope during unattended blocks.** Regenerating research runs under the research prompt's own quality-only laws (no cost/time stop conditions) and cannot fit the per-iteration budget. If the judges' top suggestion targets `research`, record it in learnings as a block-boundary proposal for the founder and take the next best asset-tagged suggestion instead. Research regeneration happens only with the founder's explicit go, outside the ≤40-call iteration budget.
- **Behavior-agnostic only**: the amendment must help a gaming or doom-scrolling book equally ("verdict lines are being diluted", never "GSBS does X on page 40"). Never hand-edit chapters, plans, or research.
- **FROZEN (not the operator's):** this PROGRAM, `calibration/judges/*`, `scripts/loop/*`, `scripts/eval/*`, `loop/config.yaml`, thresholds, rubric weights. **No preregistrations, no direction audits, no commissions, no instrument rebuilds mid-run.** Changing the rubric, weights, `judge_k`, writer model, or epsilon = a **new campaign** with fresh baselines (new `loop/results.tsv` lineage; never compare rewards across campaigns) — founder decision only.

## §4 One iteration

Budget ≤40 model calls (research excluded — see §3). Artifacts: `loop/iterations/iter-NNN/` + `loop/scores/`. **Context discipline:** the operator's own window is a resource — every prose-heavy step (writing, reviewing, judging) runs in a fresh subagent; the root reads paths, summaries, and ledger rows, never full chapters. Any interrupted iteration resumes safely: score.py is idempotent (re-emits only missing judge tasks, aggregates when verdicts are complete).

**Order matters: the amendment under test stays UNCOMMITTED until the gate decides it** — that is what makes REVERT a real `git checkout`. Never commit mid-iteration.

0. **COLD START (iter-001 only).** The Carr-fidelity flip (2026-07-13) invalidated the framing fork positions and the master plan produced under the old register — they explicitly mandate the retired positions ("no fear/command/inner creature", "lead with full autonomy"). iter-001 therefore: (a) re-decide `framing.md`'s fork table to the style guide v3 Carr defaults (per the brief; this applies founder law, it is not a tunable amendment); (b) regenerate the master plan (Sol `xhigh` native, one reviewer cycle) — it must explicitly select Carr's personification, command/total-cessation, and full-force scare-then-disown positions; (c) write chapters 1–3 fresh. Ledger hypothesis: "Carr-fidelity baseline". There is no amendment under test in iter-001.
1. **AMEND (iter-002+)** — apply THIS iteration's hypothesis (written in learnings at the end of the previous iteration) to its ONE asset, as a plain uncommitted worktree edit.
2. **RUN** — regenerate only what the amendment invalidated (plan-side change → plan + chapters; prose-side change → chapters only; research: see §3). Plan per `prompts/master-plan-skill-v2.md` (Sol `xhigh`, native), ONE reviewer cycle — note residual objections and proceed; the scoreboard decides. Chapters 1–3 (Stage A): fresh context per chapter — **style guide + master plan + previous chapter ONLY**; then **≤2 reviewer cycles per chapter** (fresh subagents on `prompts/chapter-reviewer.md`; after the second REVISE, proceed with the latest draft and note residual blockers in learnings). Convenience wrapper: `python3 scripts/loop/run_iteration.py --book production-books/quit-sugar --chapters 1-3 --iter N --hypothesis "..."` — it writes the chapters (Opus via OpenRouter, with an API output contract so the reply IS the chapter), then STOPS for the reviewer cycles and prints the exact resume command (`--no-write`); `--score-now` skips the pause (controls/baselines only). No key → printed manual dispatch.
3. **SCORE** — `python3 scripts/loop/score.py --book production-books/quit-sugar --chapters 1-3 --iter N`:
   - **HARD CHECKS (gate-blocking):** originality tripwire vs the reference corpus; **near-copy word-sequence similarity vs the matched chapters** (catches paraphrase-spaced copying); mantra/repetition law; loose length sanity (±40% of plan budget).
   - **REWARD (rubric panel):** for each chapter, `judge_k` fresh **native Sol-`xhigh`** contexts receive the rubric with the REAL chapter as reference, ours as candidate, and the candidate's mantra sheet + plan card as context; reward = weighted composite in [0,1], averaged over judges and chapters. score.py prints an explicit `task → verdict` path mapping; dispatch each task file as a fresh subagent and save each raw JSON reply to its EXACT mapped path. **No Sol API fallback exists and judge output is NEVER fabricated.** Judge task files embed reference text: they are **gitignored — never commit them** (verdicts ARE committed).
   - **SUGGESTIONS:** validated (3–5 per judge, asset-tagged from the fixed whitelist), rank-weighted across judges and chapters — printed and stored for the next hypothesis.
   - **DIAGNOSTICS (never gate):** stylometrics vs the reference, for the learnings file.
4. **GATE** — `python3 scripts/loop/gate.py --iter N --hypothesis "..." [--asset prompts/style-guide.md]` → `FAIL-HARD` (hard checks failed; reward not consulted) · `BASELINE` · `NEW-BEST` · `KEEP` (within epsilon of best) · `REVERT`. On REVERT/FAIL-HARD, run the printed `git checkout` commands NOW — the amendment was uncommitted, so this genuinely restores the accepted state. **Exit code 0 = decision made (including REVERT); the verdict lives in the row, never in the exit code.** Epsilon 0.03 is a placeholder until three same-config baseline repeats measure the real judge noise floor; the founder then resets it.
5. **RECORD + COMMIT** — append one short `loop/learnings.md` entry — **pass or fail, always**: hypothesis → verdict → the judges' top suggestions (verbatim) → next hypothesis (from the suggestions; must carry a whitelist asset tag). Then ONE commit — chapters, scores, verdicts, ledger row, learnings, and the amendment **only if the gate kept it** (on REVERT it is already gone from the worktree): `iter-NNN: <hypothesis> — <verdict>`.

**Spec gap found by the writer** (missing quote/study/mantra/ambiguous assignment — the writer's reply starts `SPEC GAP:`) = a **master-plan defect**: re-run the plan stage, restart the chapter; the writer never improvises missing content.

## §5 Blocks, stages, done

- **Block = 5 iterations**, then STOP for founder review: `results.tsv` + latest learnings + skim the chapters. Escalate early only for 3 consecutive non-improvements on the same dimension (write the wall summary; do not invent a fifth clever lever) or a missing credential/access.
- **Stage A** (chapters 1–3) → **Stage B** (full book; same loop, rubric sampled across positions) at composite ≥ **0.85** with hard checks green on two consecutive iterations — provisional threshold; founder recalibrates after the first block. **Stage C** (holdout, untouched by all tuning): one zero-amendment run on quit-caffeine vs its real Easyway book; optionally the retired blind detection probe as a final exam. Passing = the factory generalizes; any-subject production opens.
- The real done: **the founder reads the chapters and can't tell the factory from the corpus.**

## §6 Records (all of them)

`loop/results.tsv` (one row/iteration) · `loop/learnings.md` (one entry/iteration + harness debt) · `loop/iterations/` (verdicts; the reference-bearing `judging/tasks/` subdirs are **gitignored**) + `loop/scores/` (score JSONs) · one commit per iteration. Nothing else — no manifests, preregistrations, direction audits, instrument versions, or run reports. If you find yourself building an auditor, a commissioner, a preregistration, or a new judge taxonomy, you have left the loop — stop and come back. Historical `calibration/runs/` + `calibration/FAILURE-ANALYSIS.md` from the retired lab remain as read-only archaeology (`scripts/loop/RETIREMENT.md`).

## §7 Anti-overfit (absolute)

1. **Pipeline sub-calls stay blind**: researcher, planner, writer, reviewer never receive the reference EPUB, `calibration/reference/`, `analysis/`, judge outputs, or scores. The style guide is the only sanctioned carrier of reference-derived generic patterns. **The judge is reference-sighted by design** — that sight flows back only as behavior-agnostic suggestions. Judge task files embed reference chapters and are therefore gitignored (`loop/iterations/*/judging/tasks/`) — never commit them, never feed them to a pipeline sub-call.
2. Research never uses Allen Carr / Easyway-derivative sources.
3. Cross-book n-gram overlap vs the reference is a hard originality gate; rising overlap across iterations = mimicry drift → revert.
4. Amendments quote mechanisms, never reference passages. The caffeine reference stays untouched until Stage C.
