# Operating the v2 factory

## What is implemented, and what is not established

The tools implement immutable run preparation, explicit role tasks, strict output validation, dependency-bound results, retries through explicit revision rounds, actual-text reader state, whole-book edits, front matter/source assembly, independent final audit, blinded/reversed paired evaluation, conservative promotion and reproducible ZIP packaging.

The upgrade has not run paid live models, reverified the historical research, regenerated production books, chosen a new external model, collected human ratings, or measured reader outcomes. Default generator route names come from the owner's existing configuration; live availability is not claimed. Historical drafts are preserved, not republished as safe/effective books. Software checks cannot prove prose quality, factual truth, legal clearance or behavioral effectiveness.

## Requirements and first checks

Python 3.11 or newer, standard library only. Git is needed to clone/push and optional for runtime; ZIP exports work without Git. Do not install provider services or supply credentials merely to run tests.

```bash
bash scripts/check.sh
python3 scripts/factory.py demo --output /tmp/belief-changer-v2-demo
python3 scripts/factory.py --help
```

The demo emits synthetic, short prose and synthetic role responses to exercise every stage. `fixture=true` prevents promotion. It is not a sample-quality claim. Choose a new/empty demo output directory each time; the command will not delete an existing work area.

## Provider configuration

`factory/config.json` is the single public runtime configuration. The factory profile preserves the configured generator family and routes. Credentials are looked up by `auth_env`; no values belong in JSON, Git, logs or ZIPs. Existing local dotenvx-encrypted `.env` files may still be used locally but are now untracked.

The external profile is deliberately null. Configure an explicitly selected, authorized independent family before preparing a live run. Do not change models silently. For a compatible HTTPS provider, the profile shape is:

```json
{"adapter":"http","family":"ACTUAL-INDEPENDENT-FAMILY","reasoning":"high","timeout_s":600,
 "routes":[{"name":"chosen-evaluator","endpoint":"https://PROVIDER-ENDPOINT","model":"EXACT-CHOSEN-MODEL","auth_env":"EVALUATOR_API_KEY","api":"chat"}]}
```

Set api to chat or responses to match that provider. Remove unsupported optional reasoning settings. Endpoint/model strings above are placeholders, not a purchase recommendation or verified live integration. Profiles may instead use a trusted command adapter:

```json
{"adapter":"command","family":"ACTUAL-INDEPENDENT-FAMILY","argv":["/absolute/path/to/your-adapter"],"pass_env":["EVALUATOR_API_KEY"],"timeout_s":600}
```

It receives `{task,prompt}` JSON on stdin and returns exactly `{output,model,family,route,usage}` JSON on stdout. output is the role's JSON object (or a JSON string); metadata must identify the actual execution, not requested aliases. Unknown usage is null. A command runs without a shell in a fresh temporary directory with an allowlisted environment; this is not a security sandbox. Supply appropriate operating-system isolation for tool-enabled adapters. Do not let a judge read previous scores/history or ambient project instructions.

The existing agent harness can instead read a frozen task, execute an isolated role with appropriate source/browser capabilities and submit the result plus actual metadata. Imported metadata is an operator assertion, not cryptographic attestation. If a source cannot actually be checked from supplied provenance/browser access, the evidence reviewer must report that gap rather than certify it. A plain HTTP text call does not gain browser access automatically.

## Prepare inputs

Use `factory/brief.example.json` as a schema example. The brief fixes subject, audience, chosen goal, outcome mode, risk/safety boundaries and truthful narrator. An informed author has no personal-history claims. A verified person may have author-specific, source-supported claims only.

`factory/research.example.json` is deliberately UNVERIFIED and NOT research ready for generation. Replace it with real source-backed material. `prompts/research-agent.md` defines research.json; preserve detailed banks/synthesis/source locators for human audit. Do not convert a URL, `SUPPORTED` label, count floor or source file's existence into verification. Every excerpt and inference requires checking. Sources that are illustrations cannot establish empirical claims.

For a cross-iteration successor, research now starts from a deterministic guidance artifact rather than from memory. Prepare the brief, run `python3 scripts/factory.py research-guidance --learning-from BASELINE_RUN --brief BRIEF --out GUIDANCE`, and give GUIDANCE to the research lead before retrieval. Its research.json must bind `guidance_sha256`/`baseline_run` and provide one explicit `gap_resolutions` entry for every inherited research gap. `prepare --learning-from ...` recomputes this guidance and fails if research was produced against a different/stale packet.

```bash
python3 scripts/factory.py prepare --run baseline-topic-a --brief path/to/brief.json --research path/to/research.json
```

Add `--parent RELEASE-ID` when comparing to an existing champion. Use null/no parent only for an explicitly registered initial baseline. Preparation snapshots actual files, including uncommitted prompt changes, and records their digests. It does not read `.env`, old master plans or reference books. A missing/incomplete manifest blocks recovery. Altered inputs need a new run, not edits under runs/.

## Run one role at a time

```bash
python3 scripts/factory.py task --run baseline-topic-a --role evidence-reviewer --out /tmp/task.json
```

This makes no paid call. It verifies prerequisites and saves the exact task internally. Execute it only when authorized:

```bash
python3 scripts/factory.py execute --run baseline-topic-a --task /tmp/task.json --allow-paid
```

An isolated external agent can instead supply `response.json` and `metadata.json`:

```bash
python3 scripts/factory.py submit --run baseline-topic-a --task /tmp/task.json --response /tmp/response.json --metadata /tmp/metadata.json
```

Metadata has exactly model, family, route, harness, usage and latency_s. Do not fabricate fields or substitute zero for unknown usage/latency. Responses use exact shared schemas; PASS strings, terminal logs, unknown fields, invented quotes and incomplete provider results are not accepted. Review schemas are in the role prompts and executable `scripts/bc_factory/schema.py`.

Sequence: evidence-reviewer → planner → plan-reviewer. Then for each chapter: writer → chapter-reviewer → state-editor. Then book-editor → assemble → final-auditor → verify.

The evidence reviewer is a **bounded-plan readiness gate**, not a publication audit. It asks whether the frozen brief/research can support at least one safe evidence-honest plan. It must not require downstream manuscript/title/trademark/publication-clearance artifacts, and adjacent unsupported topics may be excluded rather than researched forever. Open questions can remain when they are outside the bounded argument.

If evidence review is `REVISE` or `BLOCKED` and research must change, preserve the failed run and prepare the revised dossier as a successor with:

```bash
python3 scripts/factory.py prepare --run NEW-ID --brief BRIEF --research REVISED-RESEARCH \
  --research-preflight PREFLIGHT --research-revision-of PRIOR-RUN
```

This freezes the previous independent evidence review into the successor task. The successor reviewer first verifies that finite blocking set and must not move the goalposts with new nice-to-have research; genuinely new findings are limited to newly revealed critical truth/safety contradictions. An accepted evidence review cannot be used as a research-revision parent.

```bash
python3 scripts/factory.py task --run baseline-topic-a --role writer --chapter 1 --out /tmp/writer.json
python3 scripts/factory.py task --run baseline-topic-a --role chapter-reviewer --chapter 1 --out /tmp/review.json
python3 scripts/factory.py task --run baseline-topic-a --role state-editor --chapter 1 --out /tmp/state.json
```

Execute/submit each task before requesting its dependent successor. For REVISE, create the next writer/planner task with `--round 2`, followed by the matching review round. Up to six draft rounds (initial plus five revisions) are available. Revision tasks carry the complete prior draft/plan and review history, so later rounds must preserve earlier repairs rather than regress or move the goalposts. Round 1 is comprehensive; later reviewers first verify inherited findings and may add a new finding only when the current revision introduced it, a repair exposed a previously masked material correctness/safety defect, or a critical truth/safety contradiction is genuinely newly visible. Unresolved findings stop the run; CAP is never acceptance. Repeated cap exhaustion is a system/convergence defect to diagnose, not a reason to churn through fresh memoryless successor runs. An accepted plan/chapter is immutable. Fix upstream or revise accepted content through the whole-book editor/new run.

A writer sees the actual preceding manuscript and text-supported state, not just the planned state. State records are design hypotheses supported by quotations, not measurements of a reader's mind. Context overflow must fail honestly or lead to an explicitly redesigned input strategy; no hidden truncation is implemented.

## Assembly and final verification

The book editor returns exact anchored replace/remove/move/merge operations. Ambiguous anchors fail. The assembler preserves a separate edited version and adds truthful authorship, scope, required introductory safety information and source notes. The independent auditor sees that exact final text plus every deterministic screening flag, not just the pre-edit draft. Important contextual safety advice must also remain in the narrative. Screening is a review queue, not proof of harm, plagiarism or truth.

A final-audit `REVISE` does not require a brand-new full factory run. The run converges in place through a bounded whole-book revision loop: the next book-editor round consumes the previous assembly plus the cumulative final-audit findings and applies only justified whole-book fixes — chapter anchors, exact-anchored front-matter repairs for title/reader-promise/limits/safety (safety narrowed, never deleted), retitle for plan-derived headers, and exact-anchored source-note repairs (relabel/scope fixes, whole-note removal only with the full note as anchor); the pipeline reassembles immutably and versioned (`assembly/assembly-rNN.json`, every version preserved); the next final-auditor round re-audits the new assembly against the finite inherited set. Earlier audit repairs remain constraints; successor reviewers may widen the set only for revision-caused defects or newly revealed critical truth/safety contradictions. A final-audit `BLOCKED` stops the run. Accepted evidence/plan/chapters/state, frozen research, and prior assemblies are never mutated — edits transform copies at assembly time. Rounds are bounded by `max_rounds`; unresolved defects stop the run and CAP is never acceptance. `complete()` requires the latest audit to ACCEPT the latest assembly.

A frozen active run that predates this architecture but holds a fixable `REVISE` audit continues without replaying upstream work through an explicit post-audit remediation run:

```bash
python3 scripts/factory.py prepare --remediation-of SOURCE-RUN --run NEW-ID \
  --brief SOURCE-BRIEF --research SOURCE-RESEARCH
```

The remediation run inherits the source's sealed tasks/results/assemblies/book byte-identical (bound by hash to the source manifest), copies no new research and consumes no fresh preflight, and only book-editor/final-auditor rounds continue there; upstream roles are refused. The source run is never mutated. Judgment, verification, promotion, and archiving always bind the latest ACCEPTED audit and accepted immutable assembly via `complete()`, never round 1 by convention.

```bash
python3 scripts/factory.py assemble --run baseline-topic-a
python3 scripts/factory.py task --run baseline-topic-a --role final-auditor --out /tmp/final-audit.json
# Execute/submit the audit, then:
python3 scripts/factory.py verify --run baseline-topic-a
python3 scripts/factory.py status --run baseline-topic-a
```

Zero exit status and COMPLETE_UNRELEASED mean the workflow completed its checks. They do not authorize publication or assert efficacy. INCOMPLETE/error returns exit code 2. There is no successful PANEL DONE for missing work.

## Factory-learning cycles

Factory-level changes are now a sealed runtime workflow, separate from per-book `learning-next.json` and separate from release promotion.

1. Run the Factory Learner on training-subject artifacts; it names only generic holdout requirements, never exact test topics.
2. Run the independent Factory-Learning Reviewer.
3. Before edits, seal both outputs and actual execution metadata:
   `python3 scripts/factory.py factory-learning-register --cycle CYCLE --learner LEARNER.json --learner-metadata LEARNER-META.json --review REVIEW.json --reviewer-metadata REVIEWER-META.json`
4. Implement only the approved paths, commit the intervention, then freeze the actual Git diff:
   `python3 scripts/factory.py factory-learning-freeze-change --cycle CYCLE`
5. Only after that freeze, run the read-only Factory Holdout Selector and submit at least two exact unseen topics:
   `python3 scripts/factory.py factory-learning-holdout-submit --cycle CYCLE --selection HOLDOUT.json --metadata SELECTOR-META.json`
   Runtime rejects training-topic overlap, reuse of any topic revealed by a previous cycle, and selectors from the learner/reviewer families.
6. Register the confirmatory transfer experiment on exactly that held-out set, then bind it:
   `python3 scripts/factory.py factory-learning-bind-experiment --cycle CYCLE --experiment EXPERIMENT`
   Runtime verifies parent/candidate factory hashes against the pre-intervention and frozen-intervention states and rejects undeclared changed paths.
7. After all blinded/reversed judgments, run:
   `python3 scripts/factory.py factory-learning-decide --cycle CYCLE`

`KEEP_FACTORY_CHANGE` is an internal engineering decision only. It requires strict held-out transfer evidence but does not require or replace human release calibration, never updates `factory/champion.json`, and never establishes reader efficacy. Publication still uses the separate release gate below.

## Experiments and promotion

See loop/PROGRAM.md and factory/experiment.example.json. First prepare all paired runs with frozen per-arm inputs; register a confirmatory specification before writing any chapters. Each arm is one factory across all subjects. Follow the paired input/model policy. A plan-affecting intervention must explicitly set freeze_plan=false; do not describe a regenerated-plan study as a writer-only comparison.

```bash
python3 scripts/factory.py register-experiment --spec path/to/experiment.json
python3 scripts/factory.py pair-task --experiment study-001 --pair subject-a-1 --order AB --out /tmp/pair.json
python3 scripts/factory.py pair-submit --experiment study-001 --pair subject-a-1 --order AB --response /tmp/judgment.json --metadata /tmp/judge-meta.json
# Repeat with order BA and all preregistered independent generation pairs.
python3 scripts/factory.py decide --experiment study-001 --calibration path/to/real-calibration.json
```

`pair-execute --allow-paid` is available for a configured independent provider. Calibration data must refer to the exact frozen instrument hash and actual judge model/family, at least two identified human raters, required controls and retained case artifact hashes. The code validates supplied rating consistency, not the identity of humans or veracity of submitted claims. Retain the underlying original cases/ratings and review them. `factory/calibration.json` remains PENDING until real data exist.

Promotion requires KEEP_ELIGIBLE and a human approval from factory/release-approval.example.json bound to the actual chosen book hashes. Health/high-risk work needs appropriately qualified review. First registered candidate per subject is selected by a fixed rule, not cherry-picked after scores.

```bash
python3 scripts/factory.py promote --experiment study-001 --release release-001 --calibration path/to/real-calibration.json --approval path/to/human-approval.json
```

The tool checks that the current champion is the declared parent, builds the immutable release, then atomically advances factory/champion.json. It does not publish externally, overwrite historical books or make Git commits. Inconclusive/exploratory/fixture data never promote. A released code snapshot is preserved separately from the current development checkout.

## Recovery and portability

Use status to locate the first missing/invalid dependency. Result files include input and output hashes; existence alone cannot skip work. A stale lock is not stolen automatically: inspect the recorded PID/host context and remove it only after confirming the process is gone. Provider failures do not create complete results. Use a new explicitly authorized attempt; do not repeatedly sample judges until one passes.

Execution code must match the frozen run. To run with its code snapshot, invoke `runs/ID/snapshot/scripts/factory.py --repo /absolute/repository ...`; do not silently execute a different algorithm over old tasks. Read-only artifact verification does not reinterpret old author-similarity reports as new measurements.

```bash
python3 scripts/factory.py archive --output ../Belief-changer-v2-full.zip
```

The archive includes the full working source tree and retained historical research/manuscripts, excluding `.git`, real environment/private-key files, caches and archive output. ARCHIVE-MANIFEST.json contains file hashes. A sidecar records the ZIP hash; extraction and CRC checks complement the regression suite. Third-party assets remain under their own rights and may not be publicly redistributed merely because present in a repository.

### Portable full-repository archives

The ZIP builder materializes internal regular-file symlinks as copies of their targets, recording each alias in `ARCHIVE-MANIFEST.json`. This preserves the two historical reference aliases on systems that cannot restore ZIP symlinks. External, broken, directory and credential-targeting symlinks fail the archive build. Runtime run-input paths still reject all symlinks.


## v2.1 mandatory research access
Before every real `prepare`, complete docs/RESEARCH-ACCESS.md and supply `--research-preflight /external/path/subject-preflight.json`. Fill research.json.coverage with the separate web/Reddit/X/recovery-forum lanes. Earlier prepare examples above require this additional argument for non-fixture runs. Offline demonstrations remain fixtures. The repository now targets main only; old chapters and trial traces were compacted while decisions, changes, curated research and vision remain.
