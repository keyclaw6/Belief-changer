# CALIBRATION HARNESS — Operator Manual

You are the **Calibration Operator** of the Belief-Changer book factory. Your mission: run the factory to generate an original quit-sugar book, measure it against the real Allen Carr *Good Sugar Bad Sugar* (the reference), and iterate on the factory's **generic method assets** until the factory reliably produces books at parity with — then surpassing — the reference, **without overfitting to it**. You tune the machine, never the one book.

Read first, in order: this file → `AGENTS.md` → `docs/VISION.md` (Part I + Part II "Adopted Plan") → `prompts/style-guide.md`. The style guide Part B carries THE LAW: **mantras are repeated verbatim, on schedule, from the master plan's mantra sheet; everything else is never repeated verbatim.**

## True north and compaction recovery

The product is a universal factory: given a subject, the belief or behavior to change, the desired outcome, and optional consented first-person experience, it researches science and lived experience, frames the belief change, plans the intervention, and writes a complete original book with Easyway-level persuasive effect. It must remove the illusion of benefit without willpower, shame, fear, or copied Allen Carr expression. Quit-sugar is only the calibration specimen; the reference is evaluator-only. Zero-tuning holdout performance—not resemblance on sugar—proves the factory.

After any context compaction, resumed task, or operator handoff, read `calibration/STATE.md` first, then verify its checkpoint against this section, the final row of `calibration/runs/LEDGER.md`, the current run's `manifest.json` and `report.md`, and `git log -5`. Before taking action, identify four things: the last accepted product artifact, the next product artifact, the one active generic hypothesis, and any external blocker. If research, framing, and plan are accepted, the next artifact is prose. Do not fill an access block with schemas, prompts, framework work, or speculative research.

The root context is the orchestrator and decision owner; it delegates model calls, reviews, tests, edits, and verification to bounded fresh-context subagents, then records accepted decisions in the checkpoint and run record. Subagents are hands, not an independent source of direction, and no decision may exist only in chat context.

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
   native Sol-ultra judge-control call to prove the spawned-subagent route;
   fix anything broken
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
3. Model access is route-restricted by founder law. `OPENROUTER_API_KEY` may be used **only** for Claude Opus 4.6 chapter-writing calls with reasoning disabled and DeepSeek research calls at its top supported mode. Never send GPT/OpenAI, Gemini, Grok, planning, framing, reviewing, auditing, summarization, or judging traffic through OpenRouter. Product judges use fresh native Codex subagents pinned to `gpt-5.6-sol` with `model_reasoning_effort="ultra"`; record each spawned identity, exact pin, setting, inputs, and output. Other allowed non-writer arms require a native or direct authorized surface and are unavailable—not silently rerouted—when no such surface exists. Provider credentials stay in environment variables and never enter repository files.
   **Quality-only execution law (founder correction, 2026-07-10; clarified 2026-07-11):** cost, speed, latency, and token use are observations, never optimization targets or stop conditions. For an allowed OpenRouter call, request the endpoint maximum; if the endpoint or supplied key returns a lower exact authorization ceiling, use that greatest available allowance rather than inventing a smaller cap or blocking the run. Continue on `finish_reason=length`; never compress the objective for economy or convenience. Usage and cost remain records only.
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
- Judge gate (prospective Stage-A v2.3, §9): both fresh controls hard-pass; the exact role/target/replica/order matrix is complete; every role target has at least three of four raw verdicts in {ours, tie}; zero raw verdict/rubric coherence contradictions; equal-role macro preference (ties = 0.5) ≥ **0.45**; every role ≥ **0.35**; zero critical failures on ours after unioning every raw call, including labels also applied to the reference. Targets and contradictory calls never disappear from the record or aggregate. Replica labels are trace metadata and never define an aggregate. V2.3 has no authorship-detection probe.
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

**Stage-A sequencing law.** One iteration is one frozen Chapters 1–3 first-draft batch under held-constant inputs. Generate all three readable first drafts before opening any chapter review or revision; one chapter may not gate production or diagnosis of the other two. Once the batch exists, run objective metrics, internal review, and the blind target panel. Metrics and internal review remain diagnostic evidence and promotion gates, but they cannot veto target-panel diagnosis. Skip the panel only when an artifact is missing or unreadable, reference blindness is compromised, or the judge instrument itself failed validation. Record panel evidence before forming the next hypothesis. These sequencing rules do not lower any promotion gate or change Stage-A stability, Stage B, or Stage C.

1. `cp -r calibration/runs/_template calibration/runs/run-NNN` (NNN sequential).
2. Fill `manifest.json`: stage, models per role, asset versions (`git log -1 --format=%h -- <file>` per method asset), hypotheses under test.
3. Execute the stage recipe (§3). **run-001 is the post-bootstrap baseline:** zero calibration-driven amendments. Pre-run repairs required to make the documented contracts executable (eval correctness, blindness, role-model isolation, and the founder-mandated deep-research handoff) are recorded by commit in the manifest's `baseline_boundary`; they are not quality-tuning outcomes.
4. Objective evals: `python3 scripts/eval/run_evals.py --book production-books/quit-sugar --ref-dir calibration/reference/gsbs --run-dir calibration/runs/run-NNN [--chapters 1-3]`.
5. Stage-A judge panel: commission fresh native Codex judge subagents pinned to `gpt-5.6-sol` with `model_reasoning_effort="ultra"` for every Stage-A v2.3 role, target, replica label, and A/B order (§9). Run the identical and degraded-reference controls from scratch through the exact same native configuration to new, separate output directories before product judgment; the product invocation must pass both summaries through `--validated-controls`. Preserve every exact prompt/input hash and raw result under `calibration/runs/run-NNN/judgments/`, then aggregate only after the complete matrix exists. Never use OpenRouter for a judge call.
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
| Chapter reviewer | strongest allowed planning/judge model | native/direct route only; independent of the writer |
| Summarizer (Stage B) | one allowed planning/judge model at top reasoning | same model and prompt for both books |
| Product judges | **fresh native `gpt-5.6-sol` subagents, `ultra`** | exactly two same-model replica labels in Stage-A v2.3; labels are trace metadata, never OpenRouter |

**Planner/reviewer arms (H-005):** P1 GPT 5.6 Sol (native surface `ultra`) · P2 Gemini 3.1 Pro (`high`) · P3 Grok 4.5 (`high`). Each requires a native or direct authorized surface; absence of one never authorizes an OpenRouter fallback. Product judging is fixed to replicated fresh native GPT 5.6 Sol `ultra` subagents. No lower-effort sweep: top reasoning is fixed.

**Gemini 3.1 Flash Lite is forbidden in every role.** Framers, planners, plan/chapter reviewers, Stage-B summarizers, and judges use only the three planning/judge arms above.

For subscription-backed native Sol in this Codex environment, spawn a fresh Codex subagent only with an explicit `gpt-5.6-sol` pin and per-call `model_reasoning_effort="ultra"`; the current native surface accepted that configuration on 2026-07-10. Record the spawned identity and configuration in the manifest. Do not infer the model from the mutable global Codex default. OpenRouter Sol is forbidden even when its endpoint is available.

**Researcher arms (H-009):** R1 `deepseek/deepseek-v4-pro` (`xhigh`) · R2 `minimax/minimax-m3` (reasoning enabled; `/models` exposes no effort ladder) · R3 GPT 5.6 Luna (`max`, runtime-resolved ID). Rank only by research quality: community and persona coverage, source depth, verified verbatim evidence, belief-changing insight, scientific rigor, and synthesis quality. Usage, cost, and latency are descriptive metadata and never break a quality tie.

**Muse route status (2026-07-11):** the official OpenRouter catalog has no Muse entry, and the founder's route law would forbid OpenRouter Muse even if one appeared. Meta's direct model ID is `muse-spark-1.1`; it requires a separate Meta Model API credential and rejects reasoning `none`. Direct-route availability is checked again after run-001 and never blocks the Opus baseline.

Use as many independent allowed arms as quality and adversarial diversity demand; record every exact model pin, route, reasoning config, and output allowance in the manifest. If an allowed arm or its required top-reasoning native/direct route is unavailable, note it in the ledger and proceed only where the experiment remains valid; never substitute OpenRouter outside the two permitted uses.

## §9 Judging protocol

- **Stage-A v2.3 has three independent blind roles:** belief-change efficacy and method-integrity/epistemic safety each judge the complete three-chapter block; literary craft judges each chapter. Each returns the unchanged strict v2.2 role-specific JSON and one behavior-agnostic mechanism. No role guesses authorship or receives run history, hypotheses, amendments, source packets, or review output.
- **Independent-context replication rule:** exactly two native Sol-ultra replica labels cover every role target. Each replica/order judgment runs as a separately spawned fresh context and receives no other judge output. The labels preserve traceability only: they do not select a different prompt, model, seed, state, or aggregate. Replication comes from independent same-model contexts, not provider-family variation; it is not cross-family evidence. A missing replica, role target, or order invalidates the panel.
- Every replica label covers every role target in both A/B orders. With three chapters the fixed matrix remains exactly 20 raw judgments: four exchangeable raw calls per role target, stratified as two calls in each presentation order. For preference, map each raw verdict to ours = 1, tie = 0.5, reference = 0; average within each order stratum, then average the two stratum means for the target. A role score is the mean of its target scores, and the equal-role macro is the mean of the three role scores. This is equivalent to the mean of all four raw verdict values only because the two order strata have equal size. Every decision-relevant aggregate and control verdict must remain unchanged under arbitrary replica-label permutations within each order after trace-only identity metadata is normalized.
- **Target non-inferiority guard:** every efficacy block, integrity block, and individual craft chapter used in a Stage-A pass must have at least three of its four raw verdicts in {ours, tie}, equivalently no more than one raw reference verdict. A polarized target such as `[ours, ours, ref, ref]`, including perfect order reversal, fails the judge gate rather than averaging to apparent parity. Failed or unresolved targets remain in all reported target, role, and macro means; they are never dropped, and the complete panel remains diagnostic.
- **Symmetric verdict/rubric coherence guard:** in one mapped raw call, candidate X strictly dominates candidate Y only when X scores strictly higher on every role dimension and `critical_X` is a subset of `critical_Y` (equality allowed), so X has no unique publication blocker. If either candidate strictly dominates, any verdict other than that candidate is a semantic contradiction. Apply the rule symmetrically after rebuilding the mapping from parsed A/B plus order. A higher-scoring candidate with a unique critical failure does not dominate, so a verdict for the lower-scoring candidate is not rejected mechanically. Stage-A product eligibility requires zero contradictions across all raw calls; contradictory calls are preserved and reported, never dropped, rewritten, or repaired. Preregister symmetric synthetic tests for both candidate directions, tie/opposite contradictions, candidate/order swaps, and the unique-critical exception before implementation freeze.
- Score values, score-winner signs, and non-core critical-label variation remain visible as order-stratified uncertainty diagnostics; they do not independently veto a target aggregate. Only the explicit symmetric coherence rule above can turn their joint relationship with a verdict and critical sets into an eligibility failure. Conservative safety is stricter than the preference aggregate: `critical_ours` and `critical_ref` each union the labels from all four raw calls for that role target, including labels applied to both candidates. Product use still requires zero unioned critical failures on ours; consensus, sharing with the reference, or a favorable mean cannot waive one.
- **Only v2.3 lever:** replace v2.2's identity-paired comparative-signature collapse with the pooled, order-balanced, permutation-invariant aggregation and control attribution above, including the target-level non-inferiority guard. V2.2 remains an immutable FAIL. Prompts, output schemas, label enums and operational definitions, response fields, score dimensions and scales, native structured transport, `gpt-5.6-sol` at `ultra`, exact 20-cell matrix, identical/product/degraded materials and degradation transform, blindness, existing numerical macro/role thresholds, and unioned safety remain fixed.
- **Matrix and transport invariants:** every control and product invocation has exactly 20 raw cells, 20 unique fresh native thread IDs, and exactly two raw replicas for each role-target-order stratum. Within a stratum the two calls have identical input and output-schema hashes. Aggregation revalidates each mapped ours/reference object from the parsed A/B object plus recorded order rather than trusting stored mapping. Each control must match the frozen v2.3 configuration, and product must match both validated control summaries and that frozen configuration. Any mismatch fails closed.
- **Fresh control hard gate:** both controls run from scratch into new v2.3 directories, with no v2.2 judgment reused. Across them, all 40 first responses must be strict-valid with zero retry, repair, extraction, or tolerant parsing, and both matrices must satisfy every matrix/transport invariant. Identical must produce 20/20 raw ties, equality of A and B on every raw score dimension, and identical A/B critical sets in every raw call. Degraded must produce 20/20 raw preferences for the intact reference; every raw call must put its role core label on the degraded candidate only (`incoherent_block_arc` for efficacy, `broken_chapter_flow` for craft, `broken_continuity` for integrity); and every raw transform-aligned dimension must favor intact (`cumulative_progression`; `flow_and_momentum` and `ending_handoff`; `cross_chapter_consistency`, respectively). The decision-relevant aggregates and pass/fail result must also satisfy the replica-label permutation invariant. Any miss fails closed.
- **New-baseline discipline and final stop:** v2, v2.1, and v2.2 keep their recorded verdicts and evidence; v2.3 is prospective, non-comparable, and never a reclassification or reuse of a prior control. Freeze and test the aggregation implementation before inference. If either fresh hard control or the permutation invariant fails, do not create v2.4 on this same synthetic specimen; escalate to a different validation family or a human benchmark. If both pass, run the frozen product panel immediately with the same configuration—no further prompt, schema, label, control, or material work may intervene.
- **V2.3 implementation freeze (2026-07-12):** commit `00fce429f06ebe07c4fd5b5241d239e82e18a316` implements only the preregistered pooled aggregation/control attribution under protocol `stage-a-v2.3-native-sol-ultra-1`; canonical configuration SHA-256 `3131a73a35c7e1624d46a1b36ffe9317716fc6bf05d34003569ea7afc62a0706`. The v2.2 prompt and schema hashes are unchanged; full implementation hashes are frozen in run-012's manifest. Independent review passed, focused tests passed 32/32, the canonical gate passed 77/77 with shellcheck unavailable, historical control bytes/verdicts stayed frozen, and a heterogeneous exhaustive `2^10` permutation test preserved every decision-relevant aggregate and verdict while retaining exact 20-raw/5-target semantics. No inference or provider call occurred. Next: fresh identical; degraded only if it passes; product immediately only if both pass, with no intervening instrument work.
- **Control and scope limits:** the degraded-reference control intentionally applies gross damage, so passing proves only sensitivity to severe incoherence—not fine parity discrimination. The blind integrity role sees finished prose but no source packets; it can flag internally unsupported authority or overreach, but it cannot verify source fidelity. Source-grounded audits remain a separate instrument. Same-model replication makes no cross-family claim, and a product-panel preference cannot override any failed objective, length, or method gate when deciding Stage A.
- Aggregates live in `judgments/judge-summary.json`. Product parity and causal movement are separate: the panel compares finished products but cannot establish why a candidate moved. Stage-A v2.3 is the prospective run-012 baseline after v2.2 failed its degraded control; its results are not numerically comparable with v2.2, v2.1, v2, or legacy panels.
- Historical reproduction remains available only by explicitly passing `--prompt calibration/judges/pairwise-judge.md`; that selects the frozen legacy schema, independent-order aggregation, and detection probe. It is not the canonical Stage-A quality instrument and does not authorize an API route forbidden by §2.

## §10 Observability & records

Per run: `manifest.json` (config), `metrics.json` (objective), `judgments/` (raw judge transcripts + summary), `report.md` (analysis) — all committed. Cross-run: `LEDGER.md` (one row per run: stage, verdict, key numbers, hypothesis, amendment) and `hypotheses.md` (the science log). The founder reads the ledger + reports asynchronously; keep both current enough that a fresh agent could resume from files alone (repo law).

**Failure autopsies (required — founder law).** A run or hypothesis marked FAIL/REFUTED must carry an examined WHY before it can be retired: the mechanism that actually produced the result, with evidence (metric deltas, judge notes, transcript excerpts). Nothing is dismissed preemptively — a good idea with a broken implementation gets a corrected re-test, not a burial. The ledger row links to the autopsy in the run report.

**Causal experiment record (required).** Before changing a lever, log the observed product failure, proposed mechanism, one generic lever, held-constant assets/config, and a falsifiable prediction. After the run, record the raw outcome separately from the causal interpretation, cite the deciding artifacts/numbers, name rival explanations and false-positive/false-negative risks, and choose `SUPPORTED`, `REFUTED`, or `INCONCLUSIVE`. Reviewer acceptance is not product evidence. `REFUTED` is valid only when the intended lever was actually instantiated and the measurement could have detected its predicted effect; otherwise correct the implementation or run a discriminating test. `SUPPORTED` requires the predicted blind product movement and survives obvious confounds. The next test must distinguish remaining explanations rather than merely retrying.

**Canonical store is git** — manifests, metrics, judgments, reports are diffable, portable, and survive any tooling change. **MLflow: all-or-nothing (founder, 2026-07-10).** If you adopt it, use it in FULL depth, not as a metrics mirror: trace every sub-call (writer/reviewer/judge/researcher) via its GenAI tracing, log params (manifest) + metrics (objective evals, per-dimension win-rates, detection) + artifacts (plan, chapters, judge transcripts, reports) per run, register method-asset versions in the prompt registry so run↔prompt-version links are queryable, and use the comparison UI for cross-run diagnosis. Local file store `calibration/mlruns/` (gitignored) or a local sqlite backend — no external service. Decide by ~run-003 (is cross-run diagnosis consuming your time?); log the decision as H-025 either way. Git records remain the source of truth regardless.

## §11 Escalation & stop rules

STOP and write `calibration/ESCALATION.md` (committed, with run refs) when:
- 3 consecutive runs show no gate progress on the same failing dimension;
- a method-integrity violation (shame/willpower/fear framing) recurs after a targeted amendment;
- independent judge identities disagree by >2 points on the same dimension across a whole run (judge-prompt defect — do not tune it silently; propose the fix in the escalation);
- an amendment would need to touch founder-gated canon in a way you can't phrase behavior-agnostically;
- you lack push access, web access for research, the permitted Opus writer route, or the native Sol-ultra judge-subagent route;
- anything in this manual is ambiguous in practice (name the gap; the founder/Hyperagent fixes the manual, per the AGENTS.md harness rule).

Founder merges: canon (`main`) style-guide/prompt changes are founder-approved — batch your winning amendments in the escalation/ledger notes; do not merge `calibration-lab` → `main` yourself.

## §12 Definition of done

Stage C passes (parity on the caffeine holdout with zero new tuning) → write the final ledger entry + a summary report, escalate DONE. The factory is then declared calibrated; quit-porn (paused at framing) resumes as the first novel-topic production book, and the standalone harness product (VISION Part II, Q1) inherits this loop's proven requirements.

## §13 Tooling doctrine: prompts over determinism

**Founder doctrine (corrected 2026-07-10): current LLMs systematically underestimate how intelligent current LLMs are — including themselves.** Left alone, they wrap problems in deterministic scaffolding (state machines, retry matrices, format validators) that a well-briefed intelligent agent simply doesn't need. Research, framing, planning, reviewing, and writing remain agentic: improve prompts, add independent subagents, or add a stronger fresh-context reviewer. Deterministic code is reserved for measuring completed artifacts and reproducibility records; it must not decide research steps, render a model's plan, cap reasoning, or replace an intelligent quality review. Bloat is a failure mode; delete it.

The same doctrine applies inside prompts: a plan is not a manually normalized database. Do not make a model reproduce one decision across counts, audit tables, chapter prose, and cumulative-state matrices, then mistake copy disagreement for book quality. Preserve semantic context once; let the planner architect and the reviewer judge outcomes.

The eval scripts are **measurement instruments** — deterministic, stdlib-only, runnable anywhere. They are not the orchestration layer; YOU and the model subagents are. A runner or adopted agent framework may transport fresh contexts, parallel calls, tools, and file handoffs, but it may not prescribe the research reasoning path or trade quality for throughput. The repo file contract remains the interface and every decision stays reconstructable. Log any adoption as H-008. Your experience here becomes the requirements list for the standalone harness product (VISION Part II, Q1 — decided direction: Agents SDK or PI fork, base chosen from real calibration experience).
