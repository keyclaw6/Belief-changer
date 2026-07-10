# CALIBRATION HARNESS — Operator Manual

You are the **Calibration Operator** of the Belief-Changer book factory. Your mission: run the factory to generate an original quit-sugar book, measure it against the real Allen Carr *Good Sugar Bad Sugar* (the reference), and iterate on the factory's **generic method assets** until the factory reliably produces books at parity with — then surpassing — the reference, **without overfitting to it**. You tune the machine, never the one book.

Read first, in order: this file → `AGENTS.md` → `docs/VISION.md` (Part I + Part II "Adopted Plan") → `prompts/style-guide.md`. The style guide Part B carries THE LAW: **mantras are repeated verbatim, on schedule, from the master plan's mantra sheet; everything else is never repeated verbatim.**

## §0 Operator handoff (paste into Codex — GPT 5.6 Sol)

```
Use your goal feature. GOAL: calibrate the Belief-Changer book factory to
parity with real Allen Carr books — Stage A (chapter parity) → Stage B
(full-book parity, then surpass) → Stage C (holdout generalization) — per
calibration/HARNESS.md in https://github.com/keyclaw6/Belief-changer,
working on branch calibration-lab (create from main).

First actions, in order:
1. Read calibration/HARNESS.md fully — it is your manual and you OWN it
   (§1 full reign) — then AGENTS.md, docs/VISION.md Parts I–II, and
   prompts/style-guide.md.
2. BUILD-AND-TEST the harness before any book run: env per §2
   (OPENROUTER_API_KEY, push access, web access); extract the reference;
   run the eval suite against the reference itself; make one cheap
   judge_panel call to prove endpoint connectivity; fix anything broken
   and commit the fixes.
3. Design the deep-research subsystem per §3b — structured multi-subagent
   decomposition into recovery/experience communities; evaluate adopting
   an OSS deep-research project (H-011) vs prompt-structured own build
   (H-010); researcher arms incl. deepseek/deepseek-v4-pro (H-009).
4. Execute run-001 (Stage A baseline; writer FIXED: Opus 4.6, reasoning
   none — §8) and iterate per §6. Commit every run; keep the ledger,
   hypothesis statuses, and failure autopsies current (§10).
Escalate per §11. The hypothesis bank in calibration/hypotheses.md is your
seed capital — test, autopsy, extend it.
```

## §1 The prime rule — tune the machine, not the book

Every improvement must land in a **generic method asset** (`prompts/style-guide.md`, `prompts/master-plan-skill-v2.md`, `prompts/master-plan-reviewer-v2.md`, `prompts/chapter-writer.md`, `prompts/chapter-reviewer.md`, `prompts/research-agent.md`, or the `production-books/_template/` structure), phrased **behavior-agnostically** so it would help a book on gaming or doom-scrolling equally. Amendments that mention sugar, this reference book, or any of its phrasings are FORBIDDEN. Fixing the quit-sugar artifacts directly (plan, chapters) is only legitimate as the *output of re-running a stage* with amended generic assets — never by hand-editing prose.

**Operator authority (full reign).** You are the DESIGN AGENT of this auto-research, not the executor of a fixed script. On `calibration-lab` you own everything: this manual (improve it and commit — it must always describe what the loop actually does), the judge prompts and gate thresholds (under the new-baseline + ledger discipline of §4/§5), the eval scripts, the run and experiment design, and any tooling you build or adopt (§13). Only four things are founder-law, outside your reign: the method-integrity rules, the blindness/anti-overfit rules (§4), the records discipline (§10 — every decision reconstructable from files), and canon `main` (merges are founder-approved). Everything else: decide, log, proceed — do not wait for permission.

## §2 Environment setup

1. `git clone https://github.com/keyclaw6/Belief-changer.git` (if the clone 407s behind a proxy, retry with `git -c http.proxyAuthMethod=basic clone …`). Work on branch **`calibration-lab`**. You need push access; if you lack it, escalate (§11).
2. `python3` (stdlib only — no pip installs needed).
3. Model access: env `OPENROUTER_API_KEY` (the founder's key; base `https://openrouter.ai/api/v1`, OpenAI-compatible) — needed for the writer arms (§8) and cross-family judging. Alternate: `LITELLM_BASE_URL` + `LITELLM_API_KEY` (the founder's proxy); `scripts/eval/judge_panel.py` accepts either. **Resolve exact model IDs at runtime from `GET /api/v1/models`** (bearer auth) — never guess an ID; each model's `reasoning` object there lists its supported effort levels and whether reasoning is mandatory. Reasoning is the unified body param: `"reasoning": {"effort": "medium"}`, or `{"effort": "none"}` to disable.
4. Extract the reference (LOCAL ONLY — `calibration/reference/` is gitignored; never commit extracted book text):
   ```
   python3 scripts/eval/extract_reference.py \
     --epub "analysis/reference-books/The easyway Good Sugar Bad Sugar.epub" \
     --out calibration/reference/gsbs --split-level 1 --drop 1,2
   ```
   Expected: **20 chapters, 59,766 words, mean 2,988 w/ch** (drops 1,2 = author bio + the John Dicey foreword; front/back matter auto-skipped). Eyeball `head -2` of each file on first setup.
5. Sanity check: `python3 scripts/eval/metrics.py --book calibration/reference/gsbs --ref calibration/reference/gsbs/reference-metrics.json` → all ratios 1.0.

## §3 The factory under test (stage recipes)

The factory is a file-contract state machine in `production-books/quit-sugar/`. **Every sub-role runs in a FRESH context whose inputs are EXACTLY the files listed — your own operator context must never leak into a sub-call.** How you spawn fresh sub-calls is your environment's affair; the contract is:

| Stage | Prompt | Inputs (exactly) | Output | Gate |
|---|---|---|---|---|
| Research | `prompts/research-agent.md` | the prompt + `00-brief.md` | `research/sources/*`, then synthesized `research/lived-experience.md` + `research/scientific-evidence.md` | operator judges bank coverage vs the prompt's slot list |
| Framing | template in book folder | `framing.md` template + style guide + the two research files | filled `framing.md` | operator decides forks for THIS calibration book; log decisions in the run report |
| Master plan | `prompts/master-plan-skill-v2.md` | that prompt + style guide + `00-brief.md` + `framing.md` + the two research files | `master-plan.md` (§B8 book sheets FIRST) | fresh-context reviewer (`prompts/master-plan-reviewer-v2.md`, strongest model) iterated to **"fit to write from"**, ≤3 cycles |
| Chapter N | `prompts/chapter-writer.md` | that prompt + style guide + `master-plan.md` + chapter N−1 ONLY | `chapters/chapter-NN.md` | fresh-context reviewer (`prompts/chapter-reviewer.md`) to ACCEPT, ≤3 cycles each |

The anti-repetition context law (writer sees only plan + previous chapter + style guide) is the factory's core design — never widen a writer's inputs.

## §3b Research depth doctrine (founder, 2026-07-10)

Shallow research produces generic books. Research must go **deep into the places people actually talk** — recovery forums, subreddits, support communities, comment threads under quit-content — first-person experience in the community's own words. A research run is sufficient only when:
1. **Structured decomposition, not one long prompt:** a research-lead spawns focused sub-researchers (per community, per persona, per bank slot) and merges their yield into the banks. The single-agent-long-prompt approach is the H-010 baseline arm, expected to lose — prove it.
2. **Slot-filling against the style guide's bank schema** (lived-experience themes, justification menu, community lexicon, persona segmentation) with per-slot sufficiency targets — research ends when the slots are full, not when the agent is tired.
3. **Verbatim + provenance:** quotes captured verbatim with source references; never fabricated, never paraphrased into blandness; CONTESTED tags where the science is disputed.
4. **OSS deep-research frameworks are on the table** (H-011; verified candidates as of 2026-07: `langchain-ai/open_deep_research` — most established, LangGraph, any provider; `RobertoDeLaCamara/Research-Agent` — parallel Reddit/HN/SO mining + fact-check layer, OpenAI-compatible endpoints; `extracurricular-ai/open-deep-research-with-web-ui` — smolagents, Reddit connectors, built-to-fork). Adopt or tune one ONLY per §13 doctrine: it must measurably beat the prompt-structured approach it replaces.

## §4 Blindness & anti-overfit rules (absolute)

1. **Pipeline sub-calls are blind to the reference.** No sub-role (researcher, framer, planner, writer, reviewer) may receive: anything in `calibration/reference/`, the reference EPUB, anything in `analysis/`, or judge outputs. The style guide is the ONLY sanctioned carrier of reference-derived (generic) patterns.
2. **Research source exclusions:** no Allen Carr / Easyway books or derivatives (incl. EasyPeasy-style rewrites) as sources for this book's research. Lived experience comes from real communities; science from studies.
3. **Amendment scope:** generic assets only (§1). Justify every amendment by a *mechanism* ("echoes land at paragraph ends, weakening hand-over") — never by resemblance to the reference ("GSBS does X here").
4. **Judge-prompt discipline:** judge prompts + gate thresholds are yours to improve (§1 authority), but changing either invalidates comparability: it requires a new baseline run, a ledger entry, and a stated mechanism. Never tune judges to move numbers on the same candidate.
5. **Overfit tripwires:** cross-book n-gram overlap is a hard originality gate (`run_evals`); rising overlap across runs = mimicry drift → revert. Stage C (holdout) is the final proof: `analysis/easyway-caffeine.md` and the caffeine PDF stay untouched by all tuning.

## §5 Stages and gates (initial thresholds — founder-tunable; changes are ledger entries)

**Stage A — chapter parity.** Scope: framing + master plan + chapters 1–3.
- Objective gate: `run_evals.py --chapters 1-3` exit 0 (mantra debut/schedule verbatim; no ≥12-gram non-mantra repeats; cross-overlap < 0.3%).
- Judge gate (pairwise, §9): overall win-rate (ties = 0.5) ≥ **0.45**; every dimension ≥ **0.35**; real-Carr detection ≤ **0.70**; zero critical failures on ours.
- Plan-length gate: plan chapter budgets sum to 0.9–1.1× reference total; ch 1–3 within ±20% of their budgets.
- **Exit Stage A:** gates pass on **two consecutive runs with zero amendments between them** (stability, not luck).

**Stage B — full-book parity, then surpass.** Scope: all planned chapters (plan architecture ≈ reference scale: ~18–22 chapters, total within ±15% of 59,766 words).
- Objective gate over the full range; mantra schedule fully executed; every chapter debuts or echoes ≥1 mantra.
- Pairwise judging on sampled positions (first / early-mid / mid / late / final; `--pairs` maps ours↔ref positions).
- Whole-book judging per `calibration/judges/wholebook-judge.md` (arc, escalation, schedule feel, pacing distribution, ending force): overall ≥ 0.45, detection ≤ 0.65, zero critical.
- **Surpass target (the goal):** overall win-rate ≥ **0.55** on both pairwise and whole-book.
- Exit: parity on two consecutive runs; record best surpass score.

**Stage C — universality (the holdout).** Fresh factory run on **quit-caffeine** against *The Easy Way to Quit Caffeine*, with **zero amendments during the attempt**. Same gates as Stage B. Passing = the machine generalizes; only then do novel-topic books (quit-porn first) proceed. *(Dependency: the caffeine reference is a PDF; text extraction for it isn't built yet — escalate when you reach Stage C and it will be provided.)*

## §6 The run lifecycle (every run, no exceptions)

1. `cp -r calibration/runs/_template calibration/runs/run-NNN` (NNN sequential).
2. Fill `manifest.json`: stage, models per role, asset versions (`git log -1 --format=%h -- <file>` per method asset), hypotheses under test.
3. Execute the stage recipe (§3). **run-001 is the baseline: zero amendments, current canon assets.**
4. Objective evals: `python3 scripts/eval/run_evals.py --book production-books/quit-sugar --ref-dir calibration/reference/gsbs --run-dir calibration/runs/run-NNN [--chapters 1-3]`.
5. Judge panel: `python3 scripts/eval/judge_panel.py --ours production-books/quit-sugar/chapters --ref calibration/reference/gsbs --chapters 1-3 --models <family-A>,<family-B> --prompt calibration/judges/pairwise-judge.md --out calibration/runs/run-NNN/judgments` (§9 for family rules).
6. Write `report.md` (template provided): results → gate verdict → ranked diagnosis (each gap mapped to the generic asset that owns it) → hypothesis outcomes → amendments proposed for the next run.
7. Update `calibration/runs/LEDGER.md` (one row) and `calibration/hypotheses.md` (statuses; new hypotheses from the diagnosis).
8. Amend method assets for the next run: **≤1 lever per run** (or a small batch ONLY if each item carries its own attribution rationale and touches a different failure).
9. Regenerate only what the amendment invalidates: writer-prompt change → re-run chapters; plan-template/style-guide §B8 change → re-run plan + chapters; research-prompt change → re-run research. Never hand-patch outputs.
10. Commit everything: `cal(run-NNN): <stage> — <verdict> — <one-line delta>`.

## §7 Length-control doctrine

Length is planned, not hoped for: (a) the master plan's curve map assigns **every chapter a word budget**; budgets must sum to 0.9–1.1× the reference total (~54k–66k words, ~20 chapters, ~3,000-word mean — see `reference-metrics.json` for the real curve); (b) each chapter spec hands its budget to the writer; (c) the chapter reviewer flags >±20% deviations as revision items; (d) `metrics.py` verifies. If budgets are systematically missed, that's a writer-prompt or plan-spec hypothesis — not a manual trim.

## §8 Model matrix & arms (roles are config, not code)

**FIXED (founder correction, 2026-07-10): the chapter writer is Claude Opus 4.6 with `"reasoning": {"effort": "none"}`.** Resolve the exact OpenRouter ID at runtime; do NOT run writer-model experiments. Writer-stage hypotheses tune HOW it writes (H-018..H-021), never WHICH model writes.

| Role | Model | Note |
|---|---|---|
| Writer | **Opus 4.6, reasoning none — FIXED** | the one non-negotiable in this matrix |
| Researcher | **ARMS below** (needs web access + long context) | if no web access: escalate |
| Planner | **ARMS below** | plan quality dominates book quality |
| Plan reviewer | strongest available | "fit to write from" is the costliest gate to get wrong |
| Chapter reviewer | strong **non-Anthropic** default | cross-family to the fixed Opus writer |
| Summarizer (Stage B) | cheap fast model | same prompt for both books |
| Judges | multiple families, **always ≥1 strong non-Anthropic** (§9) | writer family is fixed ⇒ guard is concrete |

**Planner arms (H-005):** P1 GPT 5.6 Sol · P2 Opus 4.6 `effort: medium` · P3 Gemini 3.1 Pro · P4 Moose Spark 1.1 (Meta — poll `/models` until live). Plus the reasoning-effort sweep on the winning planner (H-007).

**Researcher arms (H-009):** R1 GPT 5.6 Sol (operator-native) · R2 **`deepseek/deepseek-v4-pro`** (founder-flagged for cost — verified on OpenRouter 2026-07-10: 1M-token context, ~$0.435/$0.87 per M tokens, tool calling, reasoning modes; the 1M context is a real edge for synthesis over huge forum yields) · R3 Gemini 3.1 Pro. Measure: bank slots filled per dollar, verbatim-quote yield with provenance, synthesis quality into the two banks.

One arm change per attempt; record exact resolved IDs + reasoning configs in the manifest (`arm` field). Unavailable arms (P4 pre-release) or rejected configs (check each model's `reasoning.mandatory` flag in `/models`): note in the ledger, proceed with the rest.

## §9 Judging protocol

- Pairwise judge prompt: `calibration/judges/pairwise-judge.md`. Blind A/B; per-dimension 1–9 scores; which-is-real-Carr probe; strict JSON.
- **Cross-family rule:** every panel includes ≥1 judge model from a family DIFFERENT from the writer's (self-preference guard). With the writer fixed to Opus 4.6, this means **every panel carries ≥1 strong non-Anthropic judge**. A parity verdict counts only if the cross-family judge's win-rate alone also clears the gate (−0.05 tolerance).
- Both A/B orders per pair (the runner does this); ≥2 models × 2 orders × 3 chapters = 12 judgments minimum per Stage A run.
- Aggregates come from `judgments/judge-summary.json`; `real_detection_accuracy` ≈ 0.5 means judges can't tell ours from Carr — the convergence signal.
- Judges judge ONLY the two texts in front of them; never show them run history, hypotheses, or amendments.

## §10 Observability & records

Per run: `manifest.json` (config), `metrics.json` (objective), `judgments/` (raw judge transcripts + summary), `report.md` (analysis) — all committed. Cross-run: `LEDGER.md` (one row per run: stage, verdict, key numbers, hypothesis, amendment) and `hypotheses.md` (the science log). The founder reads the ledger + reports asynchronously; keep both current enough that a fresh agent could resume from files alone (repo law).

**Failure autopsies (required — founder law).** A run or hypothesis marked FAIL/REFUTED must carry an examined WHY before it can be retired: the mechanism that actually produced the result, with evidence (metric deltas, judge notes, transcript excerpts). Nothing is dismissed preemptively — a good idea with a broken implementation gets a corrected re-test, not a burial. The ledger row links to the autopsy in the run report.

**Canonical store is git** — manifests, metrics, judgments, reports are diffable, portable, and survive any tooling change. **MLflow: all-or-nothing (founder, 2026-07-10).** If you adopt it, use it in FULL depth, not as a metrics mirror: trace every sub-call (writer/reviewer/judge/researcher) via its GenAI tracing, log params (manifest) + metrics (objective evals, per-dimension win-rates, detection) + artifacts (plan, chapters, judge transcripts, reports) per run, register method-asset versions in the prompt registry so run↔prompt-version links are queryable, and use the comparison UI for cross-run diagnosis. Local file store `calibration/mlruns/` (gitignored) or a local sqlite backend — no external service. Decide by ~run-003 (is cross-run diagnosis consuming your time?); log the decision as H-025 either way. Git records remain the source of truth regardless.

## §11 Escalation & stop rules

STOP and write `calibration/ESCALATION.md` (committed, with run refs) when:
- 3 consecutive runs show no gate progress on the same failing dimension;
- a method-integrity violation (shame/willpower/fear framing) recurs after a targeted amendment;
- judge families disagree by >2 points on the same dimension across a whole run (judge-prompt defect — do not tune it silently; propose the fix in the escalation);
- an amendment would need to touch founder-gated canon in a way you can't phrase behavior-agnostically;
- you lack push access, web access for research, or the LiteLLM endpoint;
- anything in this manual is ambiguous in practice (name the gap; the founder/Hyperagent fixes the manual, per the AGENTS.md harness rule).

Founder merges: canon (`main`) style-guide/prompt changes are founder-approved — batch your winning amendments in the escalation/ledger notes; do not merge `calibration-lab` → `main` yourself.

## §12 Definition of done

Stage C passes (parity on the caffeine holdout with zero new tuning) → write the final ledger entry + a summary report, escalate DONE. The factory is then declared calibrated; quit-porn (paused at framing) resumes as the first novel-topic production book, and the standalone harness product (VISION Part II, Q1) inherits this loop's proven requirements.

## §13 Tooling doctrine: prompts over determinism

**Founder doctrine (2026-07-10): current LLMs systematically underestimate how intelligent current LLMs are — including themselves.** Left alone, they wrap problems in deterministic scaffolding (state machines, retry matrices, format validators) that a well-briefed intelligent agent simply doesn't need. In this lab, optimize with PROMPTS and clever HANDOFFS first: a better-briefed sub-agent beats a thicker wrapper, every time it's tried honestly. Add deterministic code only where determinism IS the point (measurement, reproducibility, gates — the eval scripts) or after a prompt-level fix has failed twice and the failure is understood (autopsied, §10). Bloat is a failure mode; delete it.

The eval scripts are **measurement instruments** — deterministic, stdlib-only, runnable anywhere. They are not the orchestration layer; YOU are. If sub-call management (fresh contexts, retries, parallel arms) becomes your bottleneck, build a small runner or adopt a framework (OpenAI Agents SDK, a PI fork, or your environment's native harness) on the lab branch — provided the file contract stays the interface: every artifact readable/writable as repo files, evals runnable standalone. Log the decision as hypothesis H-008 (what it replaces, what it must measurably improve). Your experience here becomes the requirements list for the standalone harness product (VISION Part II, Q1 — decided direction: Agents SDK or PI fork, base chosen from real calibration experience).
