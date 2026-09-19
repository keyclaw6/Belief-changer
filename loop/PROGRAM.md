# Controlled auto-research program — v2

## Recovery and authorization
Read AGENTS.md, docs/FACTORY-V2.md, factory/champion.json, the relevant immutable run/experiment registration and actual artifacts. Use CLI status/verify; do not infer completion from a marker in a conversation. The 000–050 campaign is closed. The upgrade authorizes code changes and offline tests, not new paid runs.


## Execution ownership for auto-research iterations
When an auto-research iteration is explicitly authorized, one persistent factory/OpenCode executor owns the entire creation pipeline. The orchestrator starts or resumes that executor, then stays hands-off while it is healthy. Evidence-review revisions, plan-review revisions, chapter rewrites, state updates and editor loops are expected autonomous factory work; they are not heartbeat intervention points.

The heartbeat may inspect progress, but must not become a shadow writer or manually synthesize normal stage outputs. It intervenes only to repair a genuine execution failure (tooling, auth, provider, browser, parser, session, or a mechanical deadlock / fail-closed violation), and then resumes the SAME durable session from existing artifacts. At the boundary where both complete books for an iteration are assembled, audited and verified, the supervisor performs the independent judgment/quality-gate work and selects one generalizable learning intervention for the next iteration.

The persistent OpenCode job's configured controller model is part of that execution identity. Do not switch it to work around provider/context trouble unless the owner explicitly authorizes a model change.

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
Before the next real campaign, follow `docs/RESEARCH-ACCESS.md`: verify live read behavior (general web, Reddit, X) over the default bridge route or, where needed, install the pinned Agent-Reach/OpenCLI/CloakBrowser tools, load NopeCHA, complete the authorized local X and Reddit logins, and run fresh live preflight for each subject. Every real `prepare` requires `--research-preflight`. Research expands to full web + substantial Reddit + substantial X passes; default added-effort allocation is 1:1:1, with documented subject-specific adjustment, never reduced general-web research. Browser access uses the working signed-in Chromium/OpenCLI bridge by default; the dedicated CloakBrowser profile is an optional fallback for constrained hosts. Do not publish keys, cookie values or bulk recovery-thread captures. Offline fixtures remain credential-free and cannot certify live access.
