# Cross-iteration learning and no-regression gate

This layer makes repeated book iterations a controlled optimization process. It is separate from release promotion and from `factory/champion.json`.

## 1. Freeze what the previous iteration taught

A completed baseline may emit one sealed `regression/learning-next.json`. The first baseline is bootstrapped from an explicitly reviewed lessons file with `learning-seed`. Later packets are produced only by `advance-baseline` after a no-regression PASS.

A learning packet can contain:
- quality dimensions to preserve;
- dimensions to improve;
- recurring repairs that must not reappear;
- targeted research gaps.

Learning is editorial/evaluation feedback. It is never empirical evidence and cannot support a factual manuscript claim.

## 2. Prepare the next candidate from that exact baseline

Prepare the next run with `--learning-from BASELINE_RUN`. The factory verifies the baseline manifest, completed book hash, accepted final-audit hash, subject, and fixture/live trust before freezing the packet into the new run.

Every role receives that same frozen packet. A changed or missing baseline artifact fails closed.

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
- stable ties or candidate wins, with no criticals -> `PASS`.

Ties are acceptable. The purpose is to stop regressions, not to manufacture a win.

## 5. Repair or advance

`REPAIR_REQUIRED` may reopen only the whole-book editor in the same logical run. The editor receives the sealed regression feedback and edits the accepted assembly copy; accepted chapters and earlier assemblies remain immutable. The repaired assembly then requires:
1. a new independent final audit;
2. a fresh AB/BA no-regression gate.

The previous comparison is stale once the book changes.

`INCONCLUSIVE` authorizes neither repair nor advancement.

Only `PASS` allows `advance-baseline`. That command emits the next sealed learning packet bound to the exact accepted candidate book and audit.

## 6. Learn about the factory, separately

The per-book learning packet and no-regression gate protect a book lineage. Factory improvement happens one level higher, after complete iteration judgments are frozen.

Run `loop/prompts/factory-learner.md` on development/training subjects. It must separate local book repairs from transferable factory mechanisms, protect demonstrated strengths, propose the smallest coherent intervention, and predeclare what would falsify it.

Then run `loop/prompts/factory-learning-reviewer.md` independently. Only an ACCEPTed transfer hypothesis/change surface may be implemented as a factory-level change.

Held-out subjects are a sealed test set. Their books, judgments, traces and failure details stay unavailable to the learner while the intervention is designed. Freeze the intervention, evaluators and success/failure criteria first; only then evaluate transfer. A change that improves training books but does not transfer is not retained as a general factory improvement. Revealed held-out failures can inform the next cycle, not retroactive tuning against the same test set.

Lower-level researchers, planners, writers and reviewers remain book-focused. They receive only the frozen transferable constraints relevant to the current run; they do not redesign the factory while generating a manuscript.

## 7. Release gate remains separate

This optimization baseline never publishes a book, updates `factory/champion.json`, proves efficacy, replaces preregistered confirmatory experiments, or replaces human/qualified release review. It only controls what the next iteration is allowed to inherit as the current best-known book baseline.
