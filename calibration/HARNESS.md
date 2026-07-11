# CALIBRATION HARNESS — Operator Manual

You are the **Calibration Operator** of the Belief-Changer book factory. Your mission: run the factory to generate an original quit-sugar book, measure it against the real Allen Carr *Good Sugar Bad Sugar* (the reference), and iterate on the factory's **generic method assets** until the factory reliably produces books at parity with — then surpassing — the reference, **without overfitting to it**. You tune the machine, never the one book.

Read first, in order: this file → `AGENTS.md` → `docs/VISION.md` (Part I + Part II "Adopted Plan") → `prompts/style-guide.md`. The style guide Part B carries THE LAW: **mantras are repeated verbatim, on schedule, from the master plan's mantra sheet; everything else is never repeated verbatim.**

## True north and compaction recovery

The product is a universal factory: given a subject, the belief or behavior to change, the desired outcome, and optional consented first-person experience, it researches science and lived experience, frames the belief change, plans the intervention, and writes a complete original book with Easyway-level persuasive effect. It must remove the illusion of benefit without willpower, shame, fear, or copied Allen Carr expression. Quit-sugar is only the calibration specimen; the reference is evaluator-only. Zero-tuning holdout performance—not resemblance on sugar—proves the factory.

After any context compaction, resumed task, or operator handoff, reread this section, the final row of `calibration/runs/LEDGER.md`, the current run's `manifest.json` and `report.md`, and `git log -5`. Before taking action, identify four things: the last accepted product artifact, the next product artifact, the one active generic hypothesis, and any external blocker. If research, framing, and plan are accepted, the next artifact is prose. Do not fill an access block with schemas, prompts, framework work, or speculative research.

Use a fresh read-only direction auditor only at run start, first prose output, and stage promotion. It returns `GO` or `CORRECT COURSE` by asking whether the work is producing or blindly evaluating a real chapter/book, whether the lever answers an observed product failure, whether it is behavior-agnostic, and whether it could survive an unseen topic. The auditor does not design workflows, prompts, schemas, or content.

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
   run the eval suite against the reference itself; make one
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
3. Model access: env `OPENROUTER_API_KEY` (the founder's key; base `https://openrouter.ai/api/v1`, OpenAI-compatible). Alternate: `LITELLM_BASE_URL` + `LITELLM_API_KEY` (the founder's proxy); `scripts/eval/judge_panel.py` accepts either. **Resolve exact model IDs at runtime from `GET /api/v1/models`** (bearer auth) — never guess an ID. Every non-writer role uses the highest mode reported by that model's `reasoning` object. The run-001 writer is the exception: Opus 4.6 with reasoning disabled via `{"reasoning": {"enabled": false}}`.
   **Quality-only execution law (founder correction, 2026-07-10; clarified 2026-07-11):** cost, speed, latency, and token use are observations, never optimization targets or stop conditions. Request the endpoint maximum; if the endpoint or supplied key returns a lower exact authorization ceiling, use that greatest available allowance rather than inventing a smaller cap or blocking the run. Continue on `finish_reason=length`; never compress the objective for economy or convenience. Usage and cost remain records only.
4. Extract the reference (LOCAL ONLY — `calibration/reference/` is gitignored; never commit extracted book text):
   ```
   python3 scripts/eval/extract_reference.py \
     --epub "analysis/reference-books/The easyway Good Sugar Bad Sugar.epub" \
     --out calibration/reference/gsbs --split-level 1 --drop 1,2
   ```
   Expected: **20 chapters, 59,766 words, mean 2,988 w/ch** (drops 1,2 = author bio + the John Dicey foreword; front/back matter auto-skipped). Eyeball `head -2` of each file on first setup.
5. Sanity check: `python3 scripts/eval/metrics.py --book calibration/reference/gsbs --ref calibration/reference/gsbs/reference-metrics.json` → all ratios 1.0.

## §3 The factory under test (stage recipes)

The factory is a file-contract pipeline in `production-books/quit-sugar/`. **Every sub-role runs in a FRESH context whose inputs are EXACTLY the files listed — your own operator context must never leak into a sub-call.** How you spawn fresh sub-calls is your environment's affair; the contract is:

| Stage | Prompt | Inputs (exactly) | Output | Gate |
|---|---|---|---|---|
| Research | `prompts/research-agent.md` | lead gets prompt + `00-brief.md`; its subagents get only their lead-chosen commission and needed visible artifacts | `research/sources/*`, `research-log.md`, then the two research syntheses | one fresh reviewer accepts depth, traceability, rights/privacy, and bank/persona coverage |
| Framing | template in book folder | `00-brief.md` + `framing.md` template + style guide + the two research files | filled `framing.md` | operator decides forks for THIS calibration book; log decisions in the run report |
| Master plan | `prompts/master-plan-skill-v2.md` | that prompt + style guide + `00-brief.md` + `framing.md` + the two research files | `master-plan.md`: authoritative book/evidence/mantra/instruction ledgers + arc + compact chapter cards | fresh-context outcome reviewer (`prompts/master-plan-reviewer-v2.md`, strongest model) iterated to **"fit to write from"**, ≤3 cycles |
| Chapter N | `prompts/chapter-writer.md` | that prompt + style guide + `master-plan.md` + chapter N−1 ONLY | `chapters/chapter-NN.md` | fresh-context reviewer (`prompts/chapter-reviewer.md`) to ACCEPT, ≤3 cycles each |

The anti-repetition context law (writer sees only plan + previous chapter + style guide) is the factory's core design — never widen a writer's inputs.

**Run-002 planning amendment (H-039): one source of truth.** Run-001 exhausted three plan reviews while every candidate already had a coherent arc, all engine/slot coverage, and an exact 62,000-word budget; the repeated blockers were contradictions among duplicated mantra counts, audits, summaries, continuity state, evidence copies, and matrices. The normalized plan therefore defines every shared decision once and references it by ID from compact chapter cards. Plan review blocks only method-integrity, evidence-honesty, blindness, missing-context, safety, invalid-length, or incoherent-architecture failures. It MUST NOT demand occurrence arithmetic, duplicate audits/state tables, repeated full payloads, prewritten chapter anatomy, or prose-density metrics before prose exists. Chapter writers own anatomy from the style guide; chapter reviewers judge the completed text.

## §3b Research depth doctrine (founder, 2026-07-10; corrected 2026-07-11)

Shallow research produces generic books. A fresh top-reasoning lead therefore owns the research method: it chooses personas, communities, source families, searches, tools, delegation, recursion, and sufficiency. It must use multiple fresh-context subagents for independent depth, but no prompt, matrix, caller, or framework prescribes a scout→worker→specialist chain, role count, search order, or numeric stopping quota. Repo schemas record the evidence after intelligent work; they do not plan the work.

Research must reach specific lived experience, recovery texture, independent science, and investigative evidence across all ten style-guide banks. Counts expose gaps but never manufacture completion. The lead continues when material is generic, repetitive, contradictory, or thin for a materially distinct persona, regardless of cost, time, calls, searches, or tokens.

Every retained claim traces to an accepted packet. Exact quotes are character-for-character; interpretations are unquoted; scientific disagreement remains `CONTESTED`. One fresh top-reasoning reviewer audits the complete packets and syntheses for depth, usefulness, provenance, rights/privacy, persona coverage, and scientific rigor, then accepts or commissions more work. The operator never patches evidence by hand.

Evidence enters Git only after its access, excerpt, retention, redistribution, attribution, and privacy basis passes. Store the minimum necessary permitted excerpt—never full community posts, bulk user dumps, identity mappings, or deletion-sensitive/nonredistributable user content. Run-001 has no speculative external store; material that needs one stays outside Git and outside evidence. Reddit remains excluded without explicit Reddit authorization, and browser stealth is never a substitute.

**Run-001 implementation:** H-010 is a prompt-structured, model-led multi-agent run with repo files as visible handoffs. H-011 stays unadopted because audited frameworks have not proved a quality/reliability gain over that baseline. RP-000–RP-027 are the completed autopsy of an over-prescribed bootstrap protocol. They prove routing, blindness, and provenance review but contribute no run evidence. No more pilot is required: version this corrected boundary, create `run-001`, and perform real research there.

## §4 Blindness & anti-overfit rules (absolute)

1. **Pipeline sub-calls are blind to the reference.** No sub-role (researcher, framer, planner, writer, reviewer) may receive: anything in `calibration/reference/`, the reference EPUB, anything in `analysis/`, or judge outputs. The style guide is the ONLY sanctioned carrier of reference-derived (generic) patterns.
   The exact-input `00-brief.md` must therefore contain only product facts (behavior, reader, forks, belief, scope/non-goals): reference identity, calibration paths, aggregate targets, and run instructions stay in the book README, HARNESS, and run manifest.
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
3. Execute the stage recipe (§3). **run-001 is the post-bootstrap baseline:** zero calibration-driven amendments. Pre-run repairs required to make the documented contracts executable (eval correctness, blindness, role-model isolation, and the founder-mandated deep-research handoff) are recorded by commit in the manifest's `baseline_boundary`; they are not quality-tuning outcomes.
4. Objective evals: `python3 scripts/eval/run_evals.py --book production-books/quit-sugar --ref-dir calibration/reference/gsbs --run-dir calibration/runs/run-NNN [--chapters 1-3]`.
5. Judge panel: `python3 scripts/eval/judge_panel.py --ours production-books/quit-sugar/chapters --ref calibration/reference/gsbs --chapters 1-3 --models google/gemini-3.1-pro-preview,openai/gpt-5.6-sol --reasoning-efforts google/gemini-3.1-pro-preview=high,openai/gpt-5.6-sol=max --prompt calibration/judges/pairwise-judge.md --out calibration/runs/run-NNN/judgments` (§9 for family rules; resolve IDs and endpoint completion maxima again at runtime).
6. Write `report.md` (template provided): results → gate verdict → ranked diagnosis (each gap mapped to the generic asset that owns it) → hypothesis outcomes → amendments proposed for the next run.
7. Update `calibration/runs/LEDGER.md` (one row) and `calibration/hypotheses.md` (statuses; new hypotheses from the diagnosis).
8. Amend method assets for the next run: **≤1 lever per run** (or a small batch ONLY if each item carries its own attribution rationale and touches a different failure).
9. Regenerate only what the amendment invalidates: writer-prompt change → re-run chapters; plan-template/style-guide §B8 change → re-run plan + chapters; research-prompt change → re-run research. Never hand-patch outputs.
10. Commit everything: `cal(run-NNN): <stage> — <verdict> — <one-line delta>`.

## §7 Length-control doctrine

Length is planned, not hoped for: (a) the master plan's curve map assigns **every chapter a word budget**; budgets must sum to 0.9–1.1× the reference total (~54k–66k words, ~20 chapters, ~3,000-word mean — see `reference-metrics.json` for the real curve); (b) each chapter spec hands its budget to the writer; (c) the chapter reviewer flags >±20% deviations as revision items; (d) `metrics.py` verifies. If budgets are systematically missed, that's a writer-prompt or plan-spec hypothesis — not a manual trim.

## §8 Model matrix & arms (roles are config, not code)

**BASELINE FIXED:** run-001 uses Claude Opus 4.6 with `"reasoning": {"enabled": false}`, and Opus serves no other role. After that baseline, Muse Spark 1.1 may run as a separate same-plan Stage-A writer arm at its highest supported reasoning when an official route and credential exist. Muse cannot disable reasoning, so report model + inference-time reasoning as one end-to-end comparison rather than a causal model-only A/B.

| Role | Model | Note |
|---|---|---|
| Run-001 writer | **Opus 4.6, reasoning disabled — FIXED BASELINE** | chapter prose only; never research, plan, review, or judge |
| Later writer arm | **Muse Spark 1.1, top reasoning** | same plan/inputs/reviewers/judges; only after Opus baseline and only through an official route |
| Research lead + chosen subagents | **ARMS below** (needs web access + long context) | DeepSeek V4 Pro / MiniMax M3 / GPT 5.6 Luna only; the lead chooses the organization |
| Planner | **ARMS below** | Gemini 3.1 Pro / GPT 5.6 Sol / Grok 4.5 only |
| Plan reviewer | strongest allowed planning model | "fit to write from" is the highest-leverage gate |
| Chapter reviewer | strongest allowed planning/judge model | cross-family to the configured writer |
| Summarizer (Stage B) | one allowed planning/judge model at top reasoning | same model and prompt for both books |
| Judges | ≥2 of the allowed planning/judge models | every panel remains independent of the writer family |

**Planner/reviewer/judge arms (H-005):** P1 GPT 5.6 Sol (OpenRouter `max`; native surface's top setting) · P2 Gemini 3.1 Pro (`high`) · P3 Grok 4.5 (`high`). Use native GPT 5.6 Sol when the environment can pin the exact model/top setting and preserve the exact-input/fresh-context contract; otherwise use the runtime-resolved OpenRouter ID. No lower-effort sweep: top reasoning is fixed.

**Gemini 3.1 Flash Lite is forbidden in every role.** Framers, planners, plan/chapter reviewers, Stage-B summarizers, and judges use only the three planning/judge arms above.

For subscription-backed native Sol in this Codex environment, use a fresh `codex exec --ephemeral --model gpt-5.6-sol` invocation with the per-call top setting `model_reasoning_effort="ultra"`; the current CLI accepted that exact preflight on 2026-07-10. Record the command/config in the manifest. Do not infer the planner model from the mutable global Codex default or from a collaboration spawn that exposes no model selector. OpenRouter Sol continues to use its endpoint-reported `max` setting.

**Researcher arms (H-009):** R1 `deepseek/deepseek-v4-pro` (`xhigh`) · R2 `minimax/minimax-m3` (reasoning enabled; `/models` exposes no effort ladder) · R3 GPT 5.6 Luna (`max`, runtime-resolved ID). Rank only by research quality: community and persona coverage, source depth, verified verbatim evidence, belief-changing insight, scientific rigor, and synthesis quality. Usage, cost, and latency are descriptive metadata and never break a quality tie.

**Muse route status (2026-07-11):** the official OpenRouter catalog has no Muse entry, so do not guess a slug. Meta's direct model ID is `muse-spark-1.1`; it requires a separate Meta Model API credential and rejects reasoning `none`. Route availability is checked again after run-001 and never blocks the Opus baseline.

Use as many independent allowed arms as quality and adversarial diversity demand; record every exact resolved ID, reasoning config, and maximum output allowance in the manifest. If an allowed arm or its required top-reasoning config is unavailable at runtime, note it in the ledger and proceed with the remaining allowed arms.

## §9 Judging protocol

- Pairwise judge prompt: `calibration/judges/pairwise-judge.md`. Blind A/B; per-dimension 1–9 scores; which-is-real-Carr probe; strict JSON.
- **Cross-family rule:** every panel includes ≥1 judge model from a family different from the configured writer. The allowed Google/OpenAI/xAI panel is cross-family to both the Anthropic baseline and the later Meta arm. A parity verdict counts only if the cross-family judge's win-rate alone also clears the gate (−0.05 tolerance).
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
- you lack push access, web access for research, or both supported model endpoints;
- anything in this manual is ambiguous in practice (name the gap; the founder/Hyperagent fixes the manual, per the AGENTS.md harness rule).

Founder merges: canon (`main`) style-guide/prompt changes are founder-approved — batch your winning amendments in the escalation/ledger notes; do not merge `calibration-lab` → `main` yourself.

## §12 Definition of done

Stage C passes (parity on the caffeine holdout with zero new tuning) → write the final ledger entry + a summary report, escalate DONE. The factory is then declared calibrated; quit-porn (paused at framing) resumes as the first novel-topic production book, and the standalone harness product (VISION Part II, Q1) inherits this loop's proven requirements.

## §13 Tooling doctrine: prompts over determinism

**Founder doctrine (corrected 2026-07-10): current LLMs systematically underestimate how intelligent current LLMs are — including themselves.** Left alone, they wrap problems in deterministic scaffolding (state machines, retry matrices, format validators) that a well-briefed intelligent agent simply doesn't need. Research, framing, planning, reviewing, and writing remain agentic: improve prompts, add independent subagents, or add a stronger fresh-context reviewer. Deterministic code is reserved for measuring completed artifacts and reproducibility records; it must not decide research steps, render a model's plan, cap reasoning, or replace an intelligent quality review. Bloat is a failure mode; delete it.

The same doctrine applies inside prompts: a plan is not a manually normalized database. Do not make a model reproduce one decision across counts, audit tables, chapter prose, and cumulative-state matrices, then mistake copy disagreement for book quality. Preserve semantic context once; let the planner architect and the reviewer judge outcomes.

The eval scripts are **measurement instruments** — deterministic, stdlib-only, runnable anywhere. They are not the orchestration layer; YOU and the model subagents are. A runner or adopted agent framework may transport fresh contexts, parallel calls, tools, and file handoffs, but it may not prescribe the research reasoning path or trade quality for throughput. The repo file contract remains the interface and every decision stays reconstructable. Log any adoption as H-008. Your experience here becomes the requirements list for the standalone harness product (VISION Part II, Q1 — decided direction: Agents SDK or PI fork, base chosen from real calibration experience).
