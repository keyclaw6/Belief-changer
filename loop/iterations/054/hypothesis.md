# Hypothesis — Iteration 054 (replacement v2 baseline A)

## Historical boundary

Iteration 053 remains aborted before the first successful factory model response and is not counted as a completed iteration. Its preregistration is immutable historical evidence and is not resumed because it named a now-prohibited ChatGPT evaluator route.

Iteration 054 is a fresh preregistration under the active runtime at commit `18f525b0d6302426b7be8a75a16286f505466c69`. No factory prompt, writing rule, model route or architecture change is introduced by this iteration.

## Purpose

Establish the first real end-to-end v2 repeatability baseline under the current architecture before testing any writing-system intervention.

The current evidence supports running the live system before changing it:
- iteration 052 showed that deterministic v2.1 research gates materially improved provenance/coverage mechanics but did not establish the acuity of the paid semantic review path;
- iteration 053 never produced a model response or book;
- no validated v2 champion exists;
- human calibration remains pending;
- W1–W4 in `loop/FUTURE-HYPOTHESES.md` remain untested hypotheses, not production rules.

## H-054

With the current v2 factory held unchanged, repeated complete-book runs on the two known development subjects will expose enough stable versus run-specific variation in independent reviews, revision behavior and final books to support one falsifiable next factory intervention without mistaking a single draw for a factory property.

This hypothesis is supported only if recurring strengths/defects can be separated from obvious replicate variance while all runtime, research and evaluator-independence gates remain real.

## Runtime invariant

- factory worker: one persistent top-level Pi Coding Agent per active book, using `.pi/agents/factory-orchestrator.md`;
- controller/provider path: OpenCode Go only;
- generator: family `meta`, model `muse-spark-1.3-contributor`, route `opencode-go`;
- independent evaluator/reviewer: family `deepseek`, model `deepseek-v4.1-flash`, route `opencode-go-deepseek-v4.1-flash`;
- credential: `OPENCODE_GO_API_KEY`, never printed or committed;
- the human-facing host controller owns hypothesis formation and does not author factory-role outputs;
- no ChatGPT, OpenCode Zen, Vercel, OpenCodex or OpenCode-CLI model fallback.

## Subjects and frozen inputs

Development subjects:
- quit-sugar
- quit-smoking

For each subject, use the current canonical v2 brief/research lineage derived from the retained `iter1-*-q` inputs, which validate against the current schema. Run a fresh live research-access preflight immediately before the corresponding new real prepare. The 24-hour rule applies to the access report, not the already gathered research.

If independent evidence review requires a research revision, repair the research once through the explicit `--research-revision-of` lineage before any book from that subject is counted as a baseline replicate. Do not silently widen or mutate frozen research after generation starts.

## Sampling

Preregistered allocation:
- 3 independent complete-book factory runs for quit-sugar;
- 3 independent complete-book factory runs for quit-smoking;
- no adaptive extension after seeing book or judge results.

Planned run IDs:
- `iter054-sugar-a`, `iter054-sugar-b`, `iter054-sugar-c`;
- `iter054-smoking-a`, `iter054-smoking-b`, `iter054-smoking-c`.

This is an end-to-end factory repeatability baseline. Planner variation, chapter-generation variation and bounded revision behavior are part of the measured system. Do not pretend the accepted plans are fixed across replicates unless the runtime actually freezes them identically.

## Startup proof before heartbeat

For the first active book, do not arm a recurring heartbeat until all four are observed:
1. intended saved Pi session identity exists;
2. Pi controller is on OpenCode Go;
3. at least one real configured factory model call returns a non-empty successful response with expected model/family/route metadata;
4. at least one durable factory marker advances.

A running PID, retry log or scheduler wake-up is not proof.

## Evaluation

Iteration 054 is exploratory baseline measurement, not a promotion experiment.

Retain for each completed run:
- evidence-review and final-audit verdicts/findings;
- plan/chapter/editor revision rounds and recurring finding classes;
- actual model/family/route metadata;
- accepted assembly hash and verification status;
- run trace needed to distinguish infrastructure defects from content defects.

Use blinded DeepSeek V4.1 Flash comparisons with AB/BA reversal when a pairwise diagnostic is used. Same-condition preferences are repeatability/variance observations, not candidate wins. Human calibration is still pending, so no `factory/champion.json` promotion or efficacy claim is allowed.

## Success / falsification

SUPPORT as an informative baseline only if:
- live access and provider gates pass honestly;
- at least 2 independent `COMPLETE_UNRELEASED` books per subject are obtained from the fixed three-run allocation;
- evaluator independence is preserved;
- recurring strengths and/or defects appear across replicates strongly enough to formulate one bounded transferable next hypothesis;
- observed differences are not dominated by infrastructure faults or order instability.

MEASURE_MORE / BLOCK rather than inventing learning if:
- research access cannot be made READY;
- the OpenCode Go generator or DeepSeek evaluator route fails after the bounded repair path;
- Pi cannot demonstrate a successful live factory response plus durable progress;
- fewer than 2 books per subject complete;
- judgments are too unstable to distinguish repeatability from noise.

## Stopping rule and next step

Do not change the factory during 054 merely because one book looks better or worse. Freeze the 054 outer evidence/decision first. Only then may the host hypothesizer choose one next intervention from the actual recurring evidence, including W1/W2/W3/W4 if the data supports them.

No publication, champion update or reader-effectiveness claim is authorized by this baseline.
