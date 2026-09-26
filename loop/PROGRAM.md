# Controlled auto-research program — v2

## Recovery and authorization
Read AGENTS.md, docs/FACTORY-V2.md, factory/champion.json, the relevant immutable run/experiment registration and actual artifacts. Use CLI status/verify; do not infer completion from a marker in a conversation. The 000–050 campaign is closed. The upgrade authorizes code changes and offline tests, not new paid runs.


## Execution ownership for auto-research iterations
Autoresearch is the OUTER controller. It invokes the reusable book factory as a component; autoresearch agents themselves do not run as Pi agents. Deterministic outer comparison/baseline/release commands use `python3 scripts/autoresearch.py ...`; they are intentionally not commands of `scripts/factory.py`.

For each requested book, start or resume one persistent Pi `factory-orchestrator`. Inside that factory call, only the factory roles under `.pi/agents/` own research, evidence review, planning, writing/review, state, whole-book editing and final audit. The autoresearch controller itself stays outside Pi and stays hands-off while the factory is healthy. The factory returns control when `verify` reaches `COMPLETE_UNRELEASED`.

Only after that handoff does autoresearch resume: run blinded comparisons, baseline/no-regression decisions, Factory Learner/Reviewer, held-out evaluation and selection of the next intervention. If no-regression evaluation returns `REPAIR_REQUIRED`, autoresearch seals a generic caller-repair request bound to the exact accepted book and audit, then may call the SAME factory run back for its bounded whole-book repair. The factory consumes only that generic handoff and does not parse the autoresearch decision schema; autoresearch takes control again after the repaired book is independently audited and verified.

The heartbeat may inspect progress, but must not become a shadow writer or manually synthesize factory-stage outputs. It intervenes only to repair genuine infrastructure/tooling/provider/browser/auth/parser/session failures or a fail-closed violation, then resumes the same durable factory session. The factory controller model remains fixed unless the owner explicitly authorizes a change.

## Cross-iteration learning and no-regression baseline

Iteration learning is explicit autoresearch state, not a memory/prompt convention. After a completed baseline, autoresearch creates a sealed learning packet containing dimensions to preserve/improve, recurring repairs and targeted research gaps, plus the exact baseline hashes/provenance that justify it. `learning-seed` may bind an explicitly reviewed historical lessons file to one exact COMPLETE baseline; thereafter only `advance-baseline` may create the next packet. Autoresearch also derives a smaller `factory-context.json` that strips all baseline/provenance/decision fields.

Prepare the next candidate with `--caller-context runs/BASELINE_RUN/caller-feedback/factory-context.json`. The factory freezes and passes that generic caller context through without parsing autoresearch semantics. Baseline validation, fixture/live trust and the mapping from learning packet to caller context stay outside the factory. Caller context is editorial/evaluation guidance only; it never counts as empirical evidence and cannot establish a manuscript claim.

After the candidate's own final audit ACCEPTS its latest assembly, run a blinded comparison against the selected baseline in both AB and BA orders using the independent pairwise instrument; the outer commands take `--baseline BASELINE_RUN` explicitly and verify that the candidate's frozen caller context matches that baseline's learning state. The internal baseline gate is deliberately stricter and simpler than a release experiment:
- a consistent baseline win on ANY quality dimension -> `REPAIR_REQUIRED`;
- any critical candidate finding -> `REPAIR_REQUIRED`;
- order disagreement on any dimension -> `INCONCLUSIVE`;
- at least one stable candidate win with no losses/criticals/order instability -> `ADVANCE`;
- stable ties on every dimension -> `PRESERVE_BASELINE`.

`REPAIR_REQUIRED` may reopen the book-editor only in the SAME logical run and only against the sealed accepted assembly plus the generic caller-repair handoff derived from the bound regression decision. Accepted chapters remain immutable; assembly edits remain versioned. The resulting assembly must receive a new independent final audit and a fresh AB/BA no-regression gate; the earlier gate becomes stale by construction. `INCONCLUSIVE` authorizes neither repair nor advancement. A round-cap failure remains a system defect, not permission to reset the lineage.

`advance-baseline` advances only on `ADVANCE`. On `PRESERVE_BASELINE`, the old book remains the baseline and no new baseline state is created. This optimization baseline is NOT the release champion. It does not update `factory/champion.json`, cannot substitute for confirmatory experiments, human calibration/review, or claim efficacy.

### Factory-learning boundary

This section is AUTORESEARCH, not book-factory runtime. The no-regression packet protects what the next book must not forget; it does not by itself decide how the FACTORY should change. Factory changes use this outer learning boundary after complete iteration judgments are frozen. These roles are executed by the autoresearch controller directly from `loop/prompts/` / `loop/judges/`, never as Pi factory agents.

1. Run `loop/prompts/factory-learner.md` on TRAINING-subject books/research/audits/judgments/traces. The learner must separate subject-local lessons from transferable mechanisms and may return CHANGE_FACTORY, KEEP_FACTORY, or MEASURE_MORE.
2. Run `loop/prompts/factory-learning-reviewer.md` independently on the learner proposal and underlying evidence. Only an ACCEPTed proposal may become a factory intervention.
3. Persist both exact outputs before changing code/prompts. The accepted review fixes the change surface, protected strengths, expected transfer mechanism, training subjects, generic holdout requirements, judge/instrument, and falsification criteria.
4. After the intervention and criteria are frozen, the orchestrator chooses exact unseen held-out subjects matching those requirements. Do not use their results to tune the same intervention.
5. A change that improves training subjects but regresses or fails to transfer on held-out subjects is NOT a factory improvement. Reject/revise it for the next cycle rather than tuning the same intervention against the revealed test results.
6. Never globalize a one-book wording repair unless the learner/reviewer identifies and accepts the deeper generating mechanism. Never use a held-out topic as both development feedback and held-out evidence in the same cycle.
7. When competing mechanisms remain plausible, prefer MEASURE_MORE or a controlled ablation over multiple prompt tweaks.

The outer loop's optimization target is transferable factory quality across unseen suitable subjects, not maximum score on the current book and not resemblance to any named author. Carr-inspired belief-change mechanisms may be studied as abstract argument moves, but no addiction/abstinence anatomy is mandatory across domains.

Evidence research has a finite convergence loop. A non-ACCEPT evidence review is repaired in a new immutable research snapshot using `prepare --research-revision-of PRIOR_RUN`; this carries the previous independent findings forward. Successor review first checks that finite blocking set. It does not reopen repaired findings or introduce release-stage/title/manuscript requirements. New findings beyond the inherited set are reserved for newly revealed critical truth/safety contradictions. Gaps in adjacent topics that can be safely excluded from the eventual plan are non-blocking open questions, not reasons to keep widening research.

Whole-book revision has a finite in-place convergence loop. A final-audit REVISE is repaired by the next book-editor round in the SAME run against the previous assembly plus cumulative audit findings — never by restarting the pipeline, rewriting accepted chapters, or hand-editing book.md. Chapter anchors, exact-anchored front-matter repairs (title/reader-promise/limits/safety; safety narrowed, never deleted), retitle for rendered headers, and exact-anchored source-note repairs transform copies at assembly time. Assemblies are immutable and versioned; successor audits verify the finite inherited set and may widen it only for revision-caused defects or newly revealed critical truth/safety contradictions. A frozen pre-architecture run with a fixable REVISE audit continues via `prepare --remediation-of SOURCE` (sealed history inherited byte-identical; whole-book rounds only). A final-audit BLOCKED, an exhausted round budget, or any unresolved defect stops the run; CAP is never acceptance.

Planner and chapter retries use the same convergence principle inside a run: each revision/review receives cumulative prior-round history, prior repairs remain constraints, and a later reviewer does not reopen repaired issues just because another round exists. Six bounded rounds are available; exhausting them repeatedly is a factory-design signal that requires root-cause repair, not routine successor churn. When development code changes while a study run is frozen, continue that run with its snapshotted factory runtime rather than mutating its sealed inputs or duplicating it solely to pick up code.

## Baseline and separate candidates
There is no validated v2 champion yet. Historical 037/043/046/050 books are recoverable from the pre-compaction Git commit, not working-tree candidates or automatic winners. First prepare fresh v2 baseline/candidate runs with parent=null and obtain valid evidence, plan and publication audits. Both arms of an initial experiment must be completed and human-reviewed before any release; the same promotion gate applies even with a null initial parent.

A run snapshots brief, research, actual code, prompts and config. Changing anything upstream means a new run ID. A candidate can remain on an experimental branch after an inconclusive result, but factory/champion.json changes only through promote. No KEEP/QUANTIFY rule may silently modify that pointer.

## Preregister
Create an experiment specification from factory/experiment.example.json. State the parent release, actual intervention paths, primary quality dimension, matched brief/research policy, plan-freeze policy, at least two subjects and at least three independent generated pairs per subject. Register confirmatory experiments BEFORE writing chapters. An exploratory historical comparison may be registered with confirmatory=false, but cannot promote.

All pairs use one parent factory and one candidate factory. Reusing a book under another sample ID is rejected. Default fixed-plan tests compare byte-identical canonical plans. Model/route changes require factory/config.json in the declared intervention; otherwise actual generator metadata must match.

Three samples are a screening allocation, not statistical sufficiency. The promotion rule requires the lower endpoint of a 95% Wilson interval for candidate wins to exceed 0.5 in EVERY subject. Ties are not wins. Reversed label orders are repeat measurements of the same sample, never doubled sample size. Preregister a sufficiently large follow-on experiment rather than sampling until a threshold happens to pass.

## Measure and decide
Each book passes evidence/plan/chapter/state/editor/assembly/final-audit stages. Then create pair tasks in AB and BA order, using the frozen external rubric without run identities. Every dimension has exact quotes from both books. Final audits and external judges must be independent of the generating family; no same-family fallback. Do not equate fresh sessions with independent validation.

Supply human calibration tied to the exact instrument and actual judge model, with the required positive/negative, originality, order/repeatability and transfer controls. Never label fixture ratings as human evidence. Calibration results are only as trustworthy as the retained case artifacts and actual human ratings; their hashes are integrity checks, not proof of who rated them.

The deterministic decision is KEEP_ELIGIBLE, INCONCLUSIVE or REJECT. Missing evidence, uncalibrated/mixed judges, order sensitivity, exploratory design or fixture data cannot KEEP. Any critical candidate defect or observed secondary-dimension loss in any subject blocks promotion. Do not average away one subject's collapse. No phrase ban or three-strike rule forbids investigating an upstream cause.

## Promote
Bind a human approval to the exact selected book hashes. Selection is fixed before judging: first registered candidate for each subject. Qualified review is required for health/high-risk work. `promote` rechecks the current champion against the declared parent, builds a complete immutable release bundle, then atomically updates the champion pointer. It does not overwrite old manuscripts, commit Git changes, publish a website or claim efficacy.

If the champion changes, compare against the new real parent. Restoring files plus a new edit is a combined intervention, not merely the edit. Preserve all failed/unfinished artifacts and actual confounds. Reports distinguish supported observations from proposed causal explanations.

## Next architectural study
Test the four conditions documented in docs/EXPERIMENTS-AND-READERS.md: current/simplified contract × local/manuscript-informed editing, with matched research and plans, repeated independent generations, predeclared outcomes and held-out transfer. The v2 software is the new candidate architecture, not evidence that it wins.


## Research-access gate (2026-09-11)
Before the next real campaign, follow `docs/RESEARCH-ACCESS.md`: verify live read behavior (general web, Reddit, X) over the default bridge route or, where needed, install the pinned Agent-Reach/OpenCLI/CloakBrowser tools, load NopeCHA, complete the authorized local X login (Reddit login is diagnostic-only on the bridge route), and run fresh live preflight for each subject. Every real `prepare` requires `--research-preflight`. Research expands to full web + substantial Reddit + substantial X passes; default added-effort allocation is 1:1:1, with documented subject-specific adjustment, never reduced general-web research. Browser access uses the working signed-in Chromium/OpenCLI bridge by default; the dedicated CloakBrowser profile is an optional fallback for constrained hosts. Do not publish keys, cookie values or bulk recovery-thread captures. Offline fixtures remain credential-free and cannot certify live access.
