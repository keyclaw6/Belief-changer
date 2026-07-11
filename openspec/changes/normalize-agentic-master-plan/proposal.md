## Why

Run-001 exhausted all three master-plan review cycles without producing a chapter even though every candidate contained a coherent 24-chapter arc, all eight method engines, all required structural slots, and an exact 62,000-word budget. The blocking defects came from asking a strong planner to duplicate the same decisions across occurrence-count audits, mantra tables, chapter cards, summaries, continuity state, evidence copies, and slot matrices; the contract became a bookkeeping product instead of a book blueprint.

## What Changes

- Replace the denormalized master-plan contract with one model-owned source of truth: shared book decisions are defined once and compact chapter cards reference them.
- Keep the quality-bearing requirements: blindness, method integrity, exact-input isolation, false belief and fork decisions, redefinition and safety boundaries, a compact graded evidence ledger, 6–10 original frozen mantras with chapter-level debut/echo routing, an exact instruction spine, coherent chapter jobs and arc, persona/evidence/scene assignments, and integer word budgets with an exact valid sum.
- Remove required occurrence arithmetic, audit/state matrices, repeated full mantra text, prewritten chapter previews/theses/landings/SUMMARY prose, duplicated persona/slot tables, single-use phrase ledgers, and generic style rules restated in every chapter card.
- Make fresh plan review outcome-based. It blocks method-integrity, evidence-honesty, blindness, length, missing-context, or incoherent-architecture failures; it does not demand duplicated representations or pre-review prose mechanics that belong to the chapter writer and reviewer.
- Keep the existing `master-plan.md` and `master-plan-review.md` paths and the `fit to write from` gate.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `book-pipeline`: Normalize the master-plan artifact and review gate around one model-owned blueprint rather than redundant deterministic bookkeeping while preserving exact inputs, writer isolation, and the fresh-review requirement.

## Impact

- Generic method assets: `prompts/style-guide.md`, `prompts/master-plan-skill-v2.md`, `prompts/master-plan-reviewer-v2.md`, and the chapter-writer handoff wording in `prompts/chapter-writer.md`.
- Stable artifact templates: `production-books/_template/master-plan.md`, `production-books/_template/master-plan-review.md`.
- Calibration contract and diagnostics: `calibration/HARNESS.md`, pipeline contract tests, H-039/run-002 manifests.
- No folder-layout, provider, model-role, research, framing, chapter-input, publishing, or public API change.
