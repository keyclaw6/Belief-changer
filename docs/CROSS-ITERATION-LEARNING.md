# Cross-iteration learning and no-regression gate

This is an AUTORESEARCH-side layer around the reusable book factory. The Pi factory itself ends at `COMPLETE_UNRELEASED`; this layer compares completed factory outputs and decides what, if anything, should change next. Its deterministic commands use `python3 scripts/autoresearch.py ...`, not `scripts/factory.py`. It is separate from release promotion and from `factory/champion.json`.

## 1. Freeze what the previous iteration taught

Autoresearch stores one sealed `caller-feedback/learning-next.json` beside the completed baseline. The first packet is bootstrapped from an explicitly reviewed lessons file with `learning-seed`; later packets are produced only when a candidate demonstrates a stable improvement. Autoresearch also derives `caller-feedback/factory-context.json`, a deliberately smaller generic handoff containing only research priorities and editorial constraints.

The learning packet may contain quality dimensions to preserve or improve, recurring repairs, targeted research gaps, and the baseline hashes/provenance that justify them. Those lineage and decision fields remain autoresearch-owned. The generic factory context strips them before crossing the factory boundary. Neither artifact is empirical evidence.

## 2. Prepare the next candidate from that exact baseline

Autoresearch validates the baseline packet against the completed baseline book/audit and then prepares the next run with `--caller-context runs/BASELINE_RUN/caller-feedback/factory-context.json`. The reusable factory only freezes, hashes, and passes that generic context through to its roles; it does not know which comparison, baseline rule, or optimization decision produced it.

Every role receives the same frozen `caller_context`. A changed context fails the factory's hash binding. The later outer no-regression commands take `--baseline BASELINE_RUN` explicitly and verify that the candidate's frozen caller context matches the selected baseline's validated learning packet.

## 3. Finish the candidate normally

The candidate still runs the normal evidence -> plan -> chapters -> state -> whole-book edit -> assembly -> independent final audit pipeline.

`COMPLETE_UNRELEASED` means the candidate is internally valid. It does not mean the candidate is better than the inherited baseline.

## 4. Run the no-regression comparison

After the candidate's latest assembly has an independent ACCEPT audit, create pairwise tasks for both label orders:
- AB
- BA

Use an independent evaluator family. Every `regression-task`, `regression-submit`, `regression-decide`, and `advance-baseline` call names the selected baseline explicitly with `--baseline BASELINE_RUN`; this keeps baseline lineage entirely in autoresearch.

The decision is fail-closed:
- consistent candidate loss on any quality dimension -> `REPAIR_REQUIRED`;
- any critical candidate defect -> `REPAIR_REQUIRED`;
- AB/BA disagreement on any dimension -> `INCONCLUSIVE`;
- at least one stable candidate win with no losses/criticals/order instability -> `ADVANCE`;
- stable ties on every dimension -> `PRESERVE_BASELINE`.

Ties are acceptable. The purpose is to stop regressions, not to manufacture a win.

## 5. Repair or advance

`REPAIR_REQUIRED` may reopen only the whole-book editor in the same logical run. Autoresearch seals its decision inside the factory's generic caller-repair envelope, bound to the exact accepted book and audit; the editor receives that feedback as opaque editorial constraints and edits the accepted assembly copy. Accepted chapters and earlier assemblies remain immutable. The repaired assembly then requires:
1. a new independent final audit;
2. a fresh AB/BA no-regression gate.

The previous comparison is stale once the book changes.

`INCONCLUSIVE` authorizes neither repair nor advancement.

`advance-baseline` replaces the baseline only on ADVANCE. On PRESERVE_BASELINE it simply reports that the previous baseline remains current.

## 6. Learn about the factory, separately

The per-book learning packet and no-regression gate protect a book lineage. Factory improvement happens one level higher, after complete iteration judgments are frozen.

Run `loop/prompts/factory-learner.md` on development/training subjects. It must separate local book repairs from transferable factory mechanisms, protect demonstrated strengths, propose the smallest coherent intervention, and predeclare what would falsify it.

Then run `loop/prompts/factory-learning-reviewer.md` independently. Only an ACCEPTed transfer hypothesis/change surface may be implemented as a factory-level change.

The learner states generic holdout requirements, not the exact test topics. Freeze the intervention, evaluator and success/failure criteria first; then choose genuinely unseen held-out subjects and evaluate transfer. A change that improves training books but does not transfer is not retained as a general factory improvement. Revealed held-out failures can inform the next cycle, not retroactive tuning against the same test set.

Lower-level researchers, planners, writers and reviewers remain book-focused. They receive only the frozen transferable constraints relevant to the current run; they do not redesign the factory while generating a manuscript.

## 7. Release gate remains separate

This optimization baseline never publishes a book, updates `factory/champion.json`, proves efficacy, replaces preregistered confirmatory experiments, or replaces human/qualified release review. It only controls what the next iteration is allowed to inherit as the current best-known book baseline.
