# Cross-iteration learning and no-regression gate

This layer makes repeated book iterations a controlled optimization process. It is separate from release promotion and from `factory/champion.json`.

## 1. Freeze what the previous iteration taught

A completed baseline may emit one sealed `regression/learning-next.json`. The first baseline is bootstrapped from an explicitly reviewed lessons file with `learning-seed`. Later immutable learning revisions may be appended even when the book baseline is preserved; a candidate replaces the book baseline only after a no-regression `ADVANCE`.

A learning packet can contain:
- quality dimensions to preserve;
- dimensions to improve;
- recurring repairs that must not reappear;
- targeted research gaps.

Learning is editorial/evaluation feedback. It is never empirical evidence and cannot support a factual manuscript claim.

## 2. Give learning to research before retrieval

Prepare the brief first, then emit deterministic pre-research guidance:

`python3 scripts/factory.py research-guidance --learning-from BASELINE_RUN --brief BRIEF --out GUIDANCE`

Give GUIDANCE to the research lead before retrieval. The resulting research.json must bind the exact guidance hash and explicitly resolve every inherited research gap as addressed, scoped_out, or unresolved. Only then prepare the next run with `--learning-from BASELINE_RUN`. Preparation recomputes the guidance and rejects stale/unbound research.

Every later role receives that same frozen learning packet. A changed or missing baseline artifact fails closed.

## 3. Finish the candidate normally

The candidate still runs the normal evidence -> plan -> chapters -> state -> whole-book edit -> assembly -> independent final audit pipeline.

`COMPLETE_UNRELEASED` means the candidate is internally valid. It does not mean the candidate is better than the inherited baseline.

## 4. Run the no-regression comparison

After the candidate's latest assembly has an independent ACCEPT audit, create pairwise tasks for both label orders:
- AB
- BA

Use an independent evaluator family, then submit the two judgments with `regression-submit` and evaluate them with `regression-decide`.

The decision is fail-closed:
- consistent candidate loss on any quality dimension -> `REPAIR_REQUIRED`;
- any critical candidate defect -> `REPAIR_REQUIRED`;
- AB/BA disagreement on any dimension -> `INCONCLUSIVE`;
- at least one stable candidate win, with no losses/criticals/order instability -> `ADVANCE`;
- stable ties on every dimension -> `PRESERVE_BASELINE`.

Ties are acceptable. The purpose is to stop regressions, not to manufacture a win.

## 5. Repair or advance

`REPAIR_REQUIRED` may reopen only the whole-book editor in the same logical run. The editor receives the sealed regression feedback and edits the accepted assembly copy; accepted chapters and earlier assemblies remain immutable. The repaired assembly then requires:
1. a new independent final audit;
2. a fresh AB/BA no-regression gate.

The previous comparison is stale once the book changes.

`INCONCLUSIVE` authorizes neither repair nor baseline update.

`advance-baseline` accepts only `ADVANCE` or `PRESERVE_BASELINE`. On ADVANCE, it binds the next packet to the exact candidate book/audit. On PRESERVE_BASELINE, it keeps the prior book baseline and appends a new immutable learning revision there, so repaired defects and new research gaps are remembered without neutral book drift.

## 6. Learn about the factory, separately

The per-book learning packet and no-regression gate protect a book lineage. Factory improvement happens one level higher, after complete iteration judgments are frozen.

On an isolated experimental branch, first run `factory-learning-evidence` with the exact completed training run IDs and any additional judgment/trace artifacts. This seals their manifests/books/audits and extra artifact hashes. Give only that manifest and its named evidence to the Factory Learner; its output must bind the evidence SHA-256. Give the same manifest plus exact learner output to the independent Factory-Learning Reviewer; its output must bind both hashes. Only then may `factory-learning-register` seal the intervention proposal and metadata BEFORE changing code/prompts.

Implement only the approved change surface and commit it. `factory-learning-freeze-change` binds the actual Git diff. Only after that freeze may a selector from a family independent of the learner, reviewer, and generator name the exact unseen topics through `factory-learning-holdout-submit`. That command creates both ignored cycle state and a tracked immutable `loop/holdout-registry/CYCLE.json`; commit the registry record before transfer binding. Register the transfer experiment on exactly those topics, bind it with `factory-learning-bind-experiment`, and evaluate with `factory-learning-decide`. The change is retained only if the bound held-out experiment passes the fixed `strict_transfer_v1` non-promotional engineering transfer gate. Learner/reviewer prose can explain expected success/failure signals but cannot redefine the machine threshold. This gate intentionally omits human release calibration; it can guide factory development but cannot publish, promote, or claim reader efficacy.

Once a held-out topic has been revealed, it is no longer unseen. The tracked retirement record is the portable source of that fact. Once the transfer panel is complete, `factory-learning-decide` also writes a compact tracked `loop/factory-learning-history/CYCLE.json` containing only content hashes, subjects, frozen commits and the terminal engineering decision. Commit it immediately. A rejected or terminally inconclusive intervention still requires its ledger/history-only commits to be preserved on `main` before the experimental branch is discarded. Its failure may inform the NEXT cycle; never tune the already-frozen intervention against the same revealed test set.

Lower-level researchers, planners, writers and reviewers remain book-focused. They receive only the frozen transferable constraints relevant to the current run; they do not redesign the factory while generating a manuscript.

## 7. Release gate remains separate

This optimization baseline never publishes a book, updates `factory/champion.json`, proves efficacy, replaces preregistered confirmatory experiments, or replaces human/qualified release review. It only controls what the next iteration is allowed to inherit as the current best-known book baseline.
