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
