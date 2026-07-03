# init-baseline-specs

## Why
The repo is being restructured agents-native. Its method and pipeline are already practiced and documented in prose (`README.md`, `docs/VISION.md`, `prompts/style-guide.md`, the production-books layout), but that prose is not machine-checkable or authoritative. This founding change turns the already-true practice into four baseline spec domains so future agent runs read spec before changing behavior, and so the truth hierarchy in `AGENTS.md` has a real layer 1.

Only what is already true practice is specified — nothing aspirational. The website, audiobook, and translation machinery are explicitly out of scope (skeleton only).

## What Changes
Establishes four new spec domains from scratch (no prior baselines exist):
- `method-integrity` — the non-negotiable method rules (non-shaming, willpower-free, original-content-only, evidence grading, source traceability).
- `book-pipeline` — the artifact contract of the production flow (brief → research → synthesis → framing → master plan → chapters), one requirement per artifact.
- `publishing` — the gate from production to published.
- `languages` — English-first skeleton.

## Capabilities

### New Capabilities
- Method integrity is spec-enforced, not prose-only.
- The production pipeline's artifact contract is explicit and path-stable.
- Publishing is founder-gated; published artifacts are immutable.
- Language expansion is a deliberate spec change, not an ad-hoc edit.

### Modified Capabilities
_(none — no prior baselines to modify.)_

## Impact
- Affected: all writing/research agent runs now have a spec layer to read first.
- No existing content is altered; `books/`, `production-books/`, `prompts/` are untouched (byte-for-byte preserved per the restructuring hard rules).
- On archive, baselines are created at `openspec/specs/<domain>/spec.md`.
