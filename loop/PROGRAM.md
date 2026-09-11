# Controlled auto-research program — v2

## Recovery and authorization
Read AGENTS.md, docs/FACTORY-V2.md, factory/champion.json, the relevant immutable run/experiment registration and actual artifacts. Use CLI status/verify; do not infer completion from a marker in a conversation. The 000–050 campaign is closed. The upgrade authorizes code changes and offline tests, not new paid runs.

## Baseline and separate candidates
There is no validated v2 champion yet. Preserve historical 037/043/046/050 books as candidates for investigation, not automatic winners. First prepare fresh v2 baseline/candidate runs with parent=null and obtain valid evidence, plan and publication audits. Both arms of an initial experiment must be completed and human-reviewed before any release; the same promotion gate applies even with a null initial parent.

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
