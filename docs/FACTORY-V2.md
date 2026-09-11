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

```bash
python3 scripts/factory.py task --run baseline-topic-a --role writer --chapter 1 --out /tmp/writer.json
python3 scripts/factory.py task --run baseline-topic-a --role chapter-reviewer --chapter 1 --out /tmp/review.json
python3 scripts/factory.py task --run baseline-topic-a --role state-editor --chapter 1 --out /tmp/state.json
```

Execute/submit each task before requesting its dependent successor. For REVISE, create the next writer/planner task with `--round 2`, followed by the matching review round. Up to four draft rounds (initial plus three revisions) are available. Unresolved findings stop the run; CAP is never acceptance. An accepted plan/chapter is immutable. Fix upstream or revise accepted content through the whole-book editor/new run.

A writer sees the actual preceding manuscript and text-supported state, not just the planned state. State records are design hypotheses supported by quotations, not measurements of a reader's mind. Context overflow must fail honestly or lead to an explicitly redesigned input strategy; no hidden truncation is implemented.

## Assembly and final verification

The book editor returns exact anchored replace/remove/move/merge operations. Ambiguous anchors fail. The assembler preserves a separate edited version and adds truthful authorship, scope, required introductory safety information and source notes. The independent auditor sees that exact final text plus every deterministic screening flag, not just the pre-edit draft. Important contextual safety advice must also remain in the narrative. Screening is a review queue, not proof of harm, plagiarism or truth.

```bash
python3 scripts/factory.py assemble --run baseline-topic-a
python3 scripts/factory.py task --run baseline-topic-a --role final-auditor --out /tmp/final-audit.json
# Execute/submit the audit, then:
python3 scripts/factory.py verify --run baseline-topic-a
python3 scripts/factory.py status --run baseline-topic-a
```

Zero exit status and COMPLETE_UNRELEASED mean the workflow completed its checks. They do not authorize publication or assert efficacy. INCOMPLETE/error returns exit code 2. There is no successful PANEL DONE for missing work.

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
