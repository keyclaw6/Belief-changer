# Autoresearch operations review — 2026-10-01

## Scope and current owner boundary

This review changes operating machinery/instructions, not the scientific experiment. No autoresearch iteration, live book generation, paid experimental role call, browser login/preflight or recurring watchdog was started. Current execution stays STOPPED. W1–W4 remain inactive. Resume and the remaining scientific scope need the owner's decision together; no six-book approval is inferred from the historical preregistration.

## Verified causes, not reconstructed authority

| Evidence | Finding |
|---|---|
| `58595ef024a50226da02dc86dfe0b0d104177ded`, 2026-09-28 21:19:59 +0200, `loop/iterations/053/hypothesis.md` | Three screening replicates per subject; complete books were conditional on factory requirements. This is an agent-written protocol, not a human quotation approving six books. |
| `86f106af3814fb899be1e6b4c9fc4eecf99005e7`, 2026-09-28 21:20:07 +0200, `loop/state.md` | Records five-iteration campaign intent and one Pi per requested book. A Git author's “authorized” label is not independent human authorization for a changed allocation. |
| `ef14425d40373a5fd10f9cbc4d5dad40ef68ac41`, 2026-09-30 08:35:45 +0200 | Introduced iteration 054 with an unconditional 3 complete sugar + 3 complete smoking allocation. No human authorization source is attached to that expansion. |
| Pre-review working `loop/state.md` | Correctly called the first session completed/inactive, but also said “Starting the replacement session would violate the runtime invariant” and required resuming the same session into `iter054-sugar-b`. This confused same-book recovery with independent-book creation. |
| Old running skill | Banned replacement workers without book scope; repeated local failure/two no-progress wake-ups could exhaust repair authority. Startup, runtime, watchdog and scientific authority were mixed. |
| `loop/CONTINUE.md`, `loop/HARNESS.md` | Still required cloak-only research and claimed the evaluator was unset, contradicting working bridge configuration and configured DeepSeek. |
| Private `iter054-sugar-*/run.sh` scripts | Launch/session decisions lived outside Git. The sugar-b script correctly chose a new UUID, but its prompt unnecessarily loaded outer state/hypothesis/runner instructions into the factory. |
| Native job `belief-pi-iter054-sugar-a-r1-resume2` | Read-only inspection reported finished/stopped, exit 0, `supervisor=legacy-process`, `unit=null`. Old service/session descriptions must not override current native ownership. No old controller was restarted. |
| Initial `bash scripts/check.sh` | Failed immediately: `Intermediate campaign artifact re-entered source tree: loop/iterations/054/progress.json`. The handoff file used by current state was forbidden by the repository gate. |

The initial working tree contained staged/deleted `evidence.json`, staged/modified `loop/state.md`, the staged sugar-b preflight and untracked `progress.json`. The pre-existing checkpoint's original SHA-256 was `ab7b7f496f09904022745d4d982699d1eb1af3cdac4aa8747527b479367c7a16`. Its run/audit/convergence data is preserved; subject keys are normalized to actual hyphenated slugs, and explicit STOPPED/UNCONFIRMED authority is added. It is not falsely promoted to final SUPPORT/REFUTE evidence. The inherited preflight remains historical, not proof of current access or permission to spend.

## Targeted changes

`skills/running-auto-research-loop/SKILL.md` owns host lifecycle, scientific authority provenance, operational repair and optional watchdog re-entry. Continue/harness documents now point to that home rather than maintaining stale alternatives. Entry points, hypothesizer, upgrade review lens and factory-facing infrastructure wording agree: persistent session per book; new session for another independent book; repair the machinery without weakening science or model independence.

The existing outer CLI gains read-only `iteration-status` and a thin `launch-book` helper for prepared runs, implemented in `scripts/bc_autoresearch/operations.py`. The helper uses real PTY execution, native Pi sessions, a kernel-owned iteration lock, frozen snapshot context and the configured Go-only profiles. No daemon, new agent framework, second supervisor or retry state machine was introduced. The existing host durable command service still owns process survival. A stale lock file, dead unit receipt or completed session cannot by itself prevent the next book. A live child retains its lock even after the parent closes its descriptor. Completed verification is separate from a worker's successful exit; an untouched pending caller repair cannot be reported as repaired.

The existing `progress.json` is the compact scope/handoff home, not an additional competing store. Approval needs source/quotation fields and a hash bound to hypothesis/allocation; omitted or stale approval cannot silently launch. These checks enforce consistency, not cryptographic human identity: the host must read the actual source and verify that it grants the claimed scope. Prepared run counts and subjects are checked against that allocation. Scientific interpretation, exclusion validity and campaign accounting remain responsibilities of the existing outer controller, not a new automatic scientific decision system.

`validate_repo.py` accepts and validates compact progress checkpoints while retaining the final `evidence.json` schema. Tests exercise mechanics instead of relying only on wording assertions.

## Preserved boundaries and evidence

No writer/reader-state/plan/editor/evaluator quality contract, factory stage implementation, provider configuration, champion or calibration was changed. The factory-orchestrator wording changes concern returning infrastructure failures for repair, not authoring behavior. Immutable snapshots, negative findings, review caps and independent verification remain authoritative. Operational source changes have different hashes; they must not be described as byte-identical experimental conditions or used to rewrite existing snapshots.

The original 054 hypothesis remains byte-identical (SHA-256 `49f0568a9e8725fc086b498ad8e57c5225f9776120df3644d1a23a834df6acda`). `iter054-sugar-a-r1` remains `COMPLETE_UNRELEASED`, book SHA-256 `2ecaf1abd130d8c231a908cb08022a6f91c1071da3ace0c5e0615650281f1c1e`, factory digest `8efd8b09c01cd9aed9c75d9dbdbf5d6a59d0906d816bad720f24c52378008209`. Diagnostic `iter054-sugar-a`, full local run artifacts, old launch scripts and completed Pi session `363bee36-1634-4d2d-8aef-ef9fedf074e8` are preserved. Private/large run and session artifacts remain local under the existing retention policy, not silently copied into Git.

## Bounded review and verification

Applied the upgrade skill's correctness, simplicity, discovery, portability and runtime-mechanics review lenses directly; no paid reviewer was invoked. Follow-up review removed a circular block between two merely prepared books, and fixed the no-op caller-repair false-completion case. Recovery may inspect another prepared/paused book; only actual kernel ownership prevents concurrent launch.

The first full gate after the initial changes passed 249 tests. After the review fixes, `bash scripts/check.sh` passed all **250 tests**, exit 0, including **22 new operations regressions**. These cover scope provenance/binding, owner stop, prepared/completed-book handoff, actual PTY I/O, duplicate launch and inherited lock ownership, stale service metadata, repairable extension/provider wiring, Go-only routing, independent family, snapshot context and no-op caller-repair detection. Existing research-access and factory integrity regressions also passed.

Read-only `iteration-status --iteration 054` reports STOPPED, UNCONFIRMED and AWAIT_OWNER_RESUME. Re-running `factory.py verify --run iter054-sugar-a-r1` after all source edits returned COMPLETE_UNRELEASED with the unchanged book/factory hashes above. `git diff --check HEAD` exited 0. Active-contract searching found no remaining cross-book same-session mandate, two-repair stop rule, unset-evaluator claim or cloak-only requirement in the inspected entry points.

Offline tests do not certify live browser account readiness, provider availability, model quality or end-to-end autonomous performance; those were deliberately not exercised by this task. The report, compact inherited checkpoint and targeted source changes are committed together on main; the final user-facing closeout records the actual commit and push result.


## Second pass — native launch boundary (2026-10-01)

Rechecked commit `9a1d740a` against the installed Pi 0.99.2 executable and its actual subagent extension, rather than trusting the mocked launcher tests alone. Two additional defects were reproduced and corrected:

1. **Child context leakage:** a zero-network native probe put an unmistakable sentinel in the current repository's parent context while keeping the run snapshot unchanged. The parent correctly excluded it, but the native child loaded it (`parent.outerContext=false`, `child.outerContext=true`). Pi's supplied subagent example creates its own child argv without the parent's isolation flags. The launcher now derives a local per-book copy of that installed tool, narrowly replacing the child startup defaults and resolving its existing agent-discovery import. Both processes load the frozen contract; children retain their own role wrapper and do not inherit the orchestrator prompt. No shared Pi installation, new subagent framework or factory-writing contract was changed. Unsupported upstream entry-point changes require an explicit compatibility repair rather than silently reverting to ambient context.
2. **Effective model routing:** a model-specific `baseUrl` or `api` override passed the old launcher check even though it differed from the frozen provider configuration. Validation now checks the selected model and its override block as well as provider defaults, and rejects ambiguous duplicate model entries. Focused tests cover both override locations and endpoint/API changes before any worker starts.

The canonical launch example also selects the versioned Pi binary explicitly: the local `/home/kab/.local/bin/pi` shim invokes `mise use -g` before launch. Avoiding that shim prevents an incidental global tool-selection operation; it does not change the configured model or provider.

Added three focused operations tests and an opt-in installed-Pi test (`scripts/eval/tests/test_pi_startup.py`). The latter uses a temporary fixture repository, dummy authentication, a network namespace, the actual PTY driver, and the installed Pi/subagent code. Startup-only instrumentation captures parent/child context and route, then exits before inference. It is not a generated book, paid provider probe, or simulated claim of provider availability. The earlier exploratory shutdown hook did not stop Pi promptly; network isolation blocked those connection attempts. The retained test exits explicitly and completed without entering model execution.

Verification with the installed test enabled: `bash scripts/check.sh` passed **254 tests**, exit 0. Both real parent and child reported the frozen context, no ancestor sentinel, the same intended snapshot working directory, and the configured Muse/OpenCode Go model/API/endpoint. The native subagent dispatch exited successfully. The ordinary suite remains independent of an installed Pi and skips that one opt-in test.

Reproduction on this host (no credentials needed):

```bash
BC_PI_EXECUTABLE=/home/kab/.local/share/mise/installs/pi/0.99.2/pi/pi \
BC_PI_SUBAGENT_EXTENSION=/home/kab/.local/share/mise/installs/pi/0.99.2/pi/examples/extensions/subagent/index.ts \
bash scripts/check.sh
```

Scientific scope, the owner stop, hypothesis 054, prior run artifacts, provider configuration, champion and calibration remain untouched. This pass does not establish live research/browser access, paid generation or reader effectiveness. Its conclusions concern the tested operating boundaries.


## Third pass — crash reporting and execution replay (2026-10-01)

Review baseline: clean `main` at `89ab1cdf7a4ef2002d2b66141291e2d77b5c2c7c`.
The scope remains operations review only. No campaign continuation, book generation,
model inference, scope approval, W1–W4 activation or provider configuration change.

Two concrete failures were reproduced before fixing them:

1. **A killed native child was reported successful.** The installed Pi 0.99.2
   subagent tool used `resolve(code ?? 0)` for the process-close event. A signal-killed
   child has no numeric exit code; the test killed its own disposable child with
   SIGKILL, and the returned dispatch was `error=false, exitCode=0`. The existing
   per-book compatibility copy now maps that case to a nonzero failure. The shared
   Pi installation is unchanged, and the existing upstream-shape check covers this
   compatibility seam. This fixes failure reporting, not factory acceptance criteria.
2. **A completion between inspection and execution-lock acquisition could trigger
   another provider call.** The factory CLI checked task/result state before taking
   ownership. A deterministic fixture recorded the competing completion at that exact
   boundary and observed a second attempted call to the mocked provider. Reconciliation
   now occurs inside the lock, before any provider invocation. Repeating an already
   recorded exact task returns its original verified receipt. Changed tasks and damaged
   results fail closed without another call; immutable results are never overwritten.

The installed-Pi fixture now also loads a saved native-format session containing a
synthetic user message. The real parent restored the requested session ID and message;
its real child received a separate session without that transcript. This exercises native
resume rather than merely inspecting launch arguments. No assistant/factory role output
was fabricated. The tests use temporary repositories, dummy auth, disabled networking
and startup callbacks that exit before inference.

Validation after the code fixes: `bash scripts/check.sh` passed **261 tests**, including
all **three installed-Pi integration checks** (not skipped) and **five new execution
recovery regressions**. Exact deployment selection:

```bash
BC_PI_EXECUTABLE=/home/kab/.local/share/mise/installs/pi/0.99.2/pi/pi \
BC_PI_SUBAGENT_EXTENSION=/home/kab/.local/share/mise/installs/pi/0.99.2/pi/examples/extensions/subagent/index.ts \
bash scripts/check.sh
```

The residual review checked that no automatic retry, new service/controller/state file,
model substitution or changed book-quality rule was introduced. Scientific review gates
and immutable snapshots remain intact. Existing runs continue with their own snapshots;
this source upgrade does not silently retrofit historical runtime code. A successful
infrastructure test remains distinct from a live end-to-end campaign validation.


## Fourth pass — submission receipt recovery (2026-10-01)

Review baseline: clean `main` at `6c1b5a4f4dda6a5eb3e8b182fd9527098d96e845`.
The three prior operational fixes were already present; this pass did not recreate or
claim them as new work. Rechecked the relevant operating contracts, iteration 052–054
history, native Pi dispatch/session code, research preflight, state ownership, launcher,
factory task/result paths and tests. No autoresearch execution or paid inference was started.

Two remaining failures in the same CLI boundary were reproduced with network-isolated,
synthetic fixtures before editing production code:

1. Repeating a successful `submit` after losing its response returned `Result already
   exists` instead of the saved receipt. The preceding `execute` recovery fix did not
   cover this second, documented entry point.
2. `submit` did not acquire the per-task execution lock. A fixture holding that lock
   still admitted a concurrent submission, allowing publication while an execution
   owned the same task.

The existing `submit`/`execute` CLI branch now shares the existing per-task lock and
reconciles recorded results after acquisition. Exact retries return the original verified
receipt without altering the result. Submission replay additionally checks the original
response and actual metadata; different tasks/responses/metadata or corrupt records fail
closed. New submissions retain the existing semantic and independence validators. This
adds no controller, state file, automatic retry, scientific decision rule or model route.
`docs/FACTORY-V2.md` documents this one behavior in its existing recovery paragraph.

Added six focused submission regressions covering exact replay, changed response/metadata,
changed task, corrupt record, held execution lock and completion immediately before lock
acquisition. The focused recovery module passed all 11 tests. The full gate with the exact
installed Pi paths shown above passed **267 tests**, including the three actual installed-Pi
startup/dispatch/session checks, exit 0. Those native checks use dummy authentication,
network isolation and startup-only exits; they do not measure live provider availability.

Residual review confirmed that the shared lock removes the entry-point inconsistency
without moving orchestration into the factory or adding another retry mechanism. The
low-level `Run.submit` contract remains unchanged; factory agents use the documented CLI.
Old frozen runs retain their old CLI code. For those runs, inspect the persisted result
after an ambiguous response instead of mutating the snapshot or regenerating accepted work.

Read-only checks after the edits still report 054 as STOPPED / UNCONFIRMED /
AWAIT_OWNER_RESUME. `factory.py verify --run iter054-sugar-a-r1` still returns
COMPLETE_UNRELEASED with book hash
`2ecaf1abd130d8c231a908cb08022a6f91c1071da3ace0c5e0615650281f1c1e`
and the unchanged factory digest recorded above. The prior native job remains
finished/stopped, legacy-process, with no current systemd unit. Git comparison confirms
unchanged hypothesis/progress, owner stop, provider configuration, champion and Pi role
contracts. `git diff --check` passed. No browser login/preflight, new book, watchdog,
W1–W4 activation or scope approval occurred. Remaining human work is still the owner's
resume and actual remaining scientific scope, not permission to repair local machinery.


## Fifth pass — saved-session structure and recovery (2026-10-01)

Baseline: clean main at `1482e4bc90413ff0d60c186643e098add4d4b53e`, synchronized
with origin. Its full gate passed 267 tests before this change.

A valid session header was the launcher's only transcript check. Offline regressions
reproduced acceptance of a truncated JSON record, null/empty records, a second session
header and duplicate JSON keys in the body. Invalid UTF-8 produced an unhelpful raw
Unicode error instead. These are launcher findings; no claim is made that an actual
campaign lost context in one of these ways.

`operations.py` now streams through the saved JSONL structure before returning a resume
plan. It uses the existing strict JSON parser, preserves unknown typed extension records,
allows blank lines and a valid final record without a newline, and never rewrites or
salvages the session. Damaged input returns an actionable repair error without exposing
transcript text. The actual launch runs this check under the existing worker lock.

The runner skill's existing recovery paragraph now makes the ownership distinction
explicit: a read-only inspection may catch an active append, so reconcile ownership and
leave healthy workers alone. Once the old worker is fenced, preserve damaged history and
recover context from intact native history or frozen artifacts. This is operational repair,
not an automatic owner stop, new experiment, new book, or permission to regenerate accepted
content. No recovery framework, controller, state file or automatic deletion was introduced.

Three focused regressions cover malformed records in both inspection and enabled-launch
paths (the worker is mocked and never invoked), non-mutating acceptance of valid records,
and explicit fixture repair preserving session identity and scope. The operations module
passes 28 tests. The full gate with installed-Pi checks enabled passes **270 tests**, exit 0;
the existing three native checks cover valid startup/dispatch, killed-child reporting and
valid saved-session restoration. Repository validation and `git diff --check` pass. The
optional `skills-ref` executable is not installed.

An additional disposable native malformed-session probe was blocked by the host before
execution; it was not rerouted or counted as a successful test. Malformed-session protection
is verified at the launcher boundary, not through that unexecuted Pi scenario. Syntactic
validation also cannot prove that whole valid records were never lost, authenticate history,
or certify live model/browser availability. No experimental model calls were made.

Residual review checked the active-append distinction, unknown-record compatibility,
no session mutation, same-book recovery and preservation of the existing authority gates.
Read-only verification still reports iteration 054 STOPPED / UNCONFIRMED / AWAIT_OWNER_RESUME,
and `iter054-sugar-a-r1` COMPLETE_UNRELEASED with the unchanged book/factory hashes above.
The frozen hypothesis/progress, owner stop, factory implementation/prompts, Pi wrappers,
provider configuration and champion are unchanged. No book, watchdog or campaign resumed.


## Sixth pass — executable startup and actionable failures (2026-10-01)

Baseline: clean `main` at `b74b43aa7455689117d7ae2ee730d4ee8584abf8`; all 270 tests passed.
Reproduced two pre-model startup failures with disposable local executables: a relative
executable found by `shutil.which` became invalid after the launcher's snapshot `chdir`,
and a missing executable interpreter returned 127 with an empty console log. New tests
also reproduced the empty diagnostic for a failed working-directory change.

The launcher now makes the selected executable path absolute before changing directory,
without dereferencing its symlink or collapsing symlink/.. semantics. Failed child setup
records its phase, exception class and errno in the existing console log before exiting
127; it does not print raw exception text, argv or environment. No automatic retry, new
state/controller, permission rule, model route or factory-writing behavior was added.
The implementation diff is 11 lines; existing operating instructions remain applicable.

Three added regressions cover explicit relative paths and relative PATH lookup, executable
symlink preservation, and actual PTY startup failures with non-disclosing diagnostics.
The full gate passed **273 tests**, including all three installed-Pi startup/session checks;
repository validation and `git diff --check` passed. An extra standalone positive probe
was blocked before execution and is not counted as evidence or retried through another
route. The retained tests verify path selection and actual failure logging separately;
they do not certify live provider/browser readiness or a full autonomous campaign.

Residual review preserved the selected executable's filesystem semantics and all prior
locking, receipt, session and scope behavior. Iteration 054 remains STOPPED / UNCONFIRMED;
the completed book still verifies with the unchanged book/factory hashes above. Protected
experimental state, frozen factory code/prompts, Pi wrappers, configuration and champion
are unchanged. No live experimental model call, book, watchdog or campaign was started.


## Convergent review — recovery across the full operating lifecycle (2026-10-02)

Kristian requested continued review/fix/test cycles until a complete residual review had
no further concrete material findings, not another stop after the first repaired defect.
Baseline was clean `main` at `4e370499a8780f8d65c11702dfb7a4d8e4c7054a`, with 273 tests passing.

Four connected failure mechanisms were repaired without changing factory writing behavior:

- **Outer receipt recovery:** pair-submit/pair-execute did not share recovery behavior,
  and identical regression submissions acquired fresh timestamps. The existing CLI task
  lock now fences both pair entry points; exact retries recover the original verified
  receipt without another provider call or rewriting evidence. Regression submission
  reconciles under its existing lock. Conflicts, stale tasks and damaged seals still fail.
  `experiments.py` and the registered evaluator instrument were deliberately unchanged.
- **Cached decision evidence:** a stored ADVANCE could advance a baseline even after a
  judgment disappeared or its audit changed. Re-entry now checks the exact retained
  judgments, task bindings, both books and both audits before returning the stored
  conclusion or publishing a repair handoff. No scoring or scientific decision rule changed.
- **Same-book successors:** the launch prompt forbade the research-revision prepare the
  factory requires, while allocation counted every snapshot as another book. Existing
  manifest research/remediation links now identify one validated, unbranched logical book.
  Source findings remain retained, scope/model identities are checked, and a successor
  resumes the one saved session against its own snapshot. Pi may prepare the linked
  research successor and return; the host receives exact `next_run` and owns re-entry.
  Branching attempts, changed scope or ambiguous sessions require reconciliation rather
  than being hidden as one sample. Prior-iteration research does not share a book session.
- **Actual child ownership:** the upstream subagent spawn closed the inherited lock fd.
  The existing per-book compatibility copy now passes that same kernel lock to the actual
  role child. There is no new supervisor, lease store or daemon. A native startup-only
  test reproduced replacement lock acquisition while the child was alive before the fix;
  afterward it verifies the same lock inode survives all parent descriptor closures and
  becomes reusable only after the child exits.

Verification used existing temporary synthetic fixtures and no experimental inference.
The outer red run reproduced 7 failures plus 1 error; repaired focused outer tests passed
25 tests. Real frozen-run lineage fixtures reproduced invalid extra-book counting and
handoff contradictions, then the full operations module passed 37 tests. The four installed
Pi startup checks plus operations passed 41 tests. The final installed-runtime full gate
passed **287 tests**, exit 0. The ordinary portable gate also passed: 287 discovered,
283 passed and only the four explicitly opt-in installed-Pi checks skipped. Repository
validation and `git diff --check` passed. Fourteen focused tests were added in total.

An independent read-only Codex code reviewer examined the original frozen baseline and
identified the successor/allocation and actual-child ownership defects. After repairs,
the reviewer checked the exact baseline-plus-diff SHA-256
`ff131bc8d7f67e0439faa7b7259a529535cd4ee121b0583c4e362a544e42ae56`,
reconstructed all eight changed source/test/skill files, and returned **CLEAN ENOUGH: yes**
with no additional concrete material findings. That residual review covered lineage,
exclusions/branching, session/snapshot handoff, descriptor lifetime, repair authority,
receipt replay and cached evidence bindings. It was source/test inspection, not a second
independent execution of the test suite. Parent review also revisited the connected
research-access and entrypoint contracts. The code reviewer was not a Pi factory role or
an experimental evaluator; no factory provider configuration was altered to run it.

Read-only inspection still reports 054 STOPPED / UNCONFIRMED / AWAIT_OWNER_RESUME. The
retained `iter054-sugar-a-r1` verifies COMPLETE_UNRELEASED with the unchanged book/factory
hashes above, and the real read-only inventory identifies that one nonexcluded book.
AGENTS, factory code/prompts/configuration, Pi wrappers, frozen iteration state, evaluator
instrument and champion remain unchanged. No live book, preflight, watchdog, W1–W4 action
or campaign was started. Native tests isolate networking, use dummy authentication and
exit before inference. The clean residual review is a bounded operational-code conclusion,
not proof of live browser/provider availability, an end-to-end campaign, or reader efficacy.
