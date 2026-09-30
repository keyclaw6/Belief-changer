# Iteration 054 startup repair — research-access bridge

Before any 054 factory prepare or model generation, the fresh quit-sugar live preflight on committed runtime `ef14425d` exposed two access failures:

- structured general-web search: OpenCLI DuckDuckGo adapter exit 66;
- Reddit public search/read: OpenCLI Reddit adapter exit 1.

X auth/search/read and direct web reads were already healthy.

## Root-cause repair

The research-access bridge was updated without changing any factory writing prompt, model route, evaluator family, book input, or experimental hypothesis:

- general-web structured search now uses the working OpenCLI Google adapter;
- Reddit public search/thread reads use Reddit Atom feeds instead of the failing OpenCLI Reddit path;
- the bridge profile mapping is aligned with the known-good research profile;
- the public Reddit Atom path has bounded 429 handling and strict canonical URL/read guards;
- tests were updated at the actual adapter seam; one accidental live-network mock bug was corrected before acceptance.

This is startup infrastructure recovery under `skills/running-auto-research-loop/SKILL.md`, not a candidate factory intervention. Iteration 054 remains the unchanged-factory repeatability baseline defined in `hypothesis.md`.

## Validation

- focused research-access suite: 68 tests, PASS;
- mandatory `bash scripts/check.sh`: PASS, exit 0;
- fresh live quit-sugar preflight after repair: `READY`;
- bridge checks: web search/read, Reddit search/read, X auth/search/read all true;
- no alternate model provider, factory worker, or evaluator route introduced.

## Bounded upgrade review

Applied the upgrade review lenses to the frozen diff:

- elegance/architecture: replaces two broken upstream access adapters rather than adding fallback orchestration;
- connected-system coherence: docs, config, runtime and tests agree on the new bridge behavior;
- discovery/context: the existing research-access command surface is unchanged;
- runtime portability: Pi/OpenCode-Go factory boundary is untouched;
- mechanical correctness: input guards, bounded retry, backend labels and failure-closed semantics have regression coverage.

CLEAN ENOUGH: yes
