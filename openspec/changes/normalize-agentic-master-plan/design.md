## Context

The current master-plan contract denormalizes one book decision into several exact representations: a shared sheet, an audit table, chapter-specific copied wording, prewritten anatomy, a cumulative state table, and reviewer arithmetic. Run-001 demonstrated the failure mode across three uncapped Sol `ultra` cycles: substantive arc coverage was present in every plan, while each review found a new contradiction between copies. Chapter writers already receive the full master plan and style guide, so duplicated copies do not add context; they add disagreement surfaces.

## Goals / Non-Goals

**Goals:**

- Make `master-plan.md` one model-owned semantic blueprint with one authoritative location per decision.
- Preserve enough behavior-specific evidence, arc, mantra, instruction, persona, scene, safety, and length context for an isolated chapter writer.
- Make the fresh plan review judge the blueprint's ability to produce a method-safe, evidence-honest, coherent book.
- Reach a real chapter quickly enough that further calibration is driven by prose and judge evidence.

**Non-Goals:**

- Weakening method-integrity, blindness, evidence, role-model, exact-input, length, or fresh-review gates.
- Changing the production-book folder contract or chapter-writer context boundary.
- Adding a deterministic plan renderer, validator, schema engine, retry graph, or orchestration framework.
- Optimizing cost, latency, output length, or reasoning usage.

## Decisions

### One authoritative representation per decision

Book-wide decisions live once in compact named sections. Chapter cards reference mantra, evidence, instruction, persona, and structural-slot IDs instead of copying their contents. This preserves precise handoff while removing cross-table synchronization.

Alternative rejected: retain exhaustive duplicated sheets and add a validator. That would encode the failed bookkeeping system in software and contradict the prompts-over-determinism doctrine.

### Plan outcomes, not prewritten chapter prose

Each chapter card fixes its single belief job, arc position, target personas, evidence IDs and limits, original scene/analogy job, mantra debut/echo IDs, instruction ID when any, safety notes, and integer word budget. It does not prewrite the chapter's preview, thesis, landing, SUMMARY, sentence metrics, or exact occurrence counts. The chapter writer applies the style guide; the chapter reviewer tests the actual prose.

Alternative rejected: remove the master plan or fresh review. Whole-book arc, deliberate repetition, and isolated-writer context still need an accepted blueprint.

### Compact evidence ledger

Claims and lived material needed by writers are defined once with their grade, permitted/prohibited inference, limit, and source ID. Chapter cards reference ledger IDs. The plan must not copy a research synthesis wholesale or reproduce the same evidence payload in multiple chapter cards.

### Outcome-based plan review

The reviewer blocks a plan for blindness, method-integrity, evidence-honesty, missing-context, invalid length, unsafe instructions, or incoherent whole-book architecture. It may identify a semantic contradiction between authoritative entries, but it must not demand a deleted duplicate representation, exact occurrence arithmetic, or prewritten prose anatomy.

## Risks / Trade-offs

- **A compact card omits context a writer genuinely needs** → Chapter review and Stage A scores falsify H-039; restore only the missing semantic field, not duplicated state.
- **ID references become vague** → Require every referenced ID to resolve to one authoritative entry and let the intelligent reviewer judge sufficiency.
- **Outcome review becomes permissive** → Preserve explicit blocking dimensions and the exact `fit to write from` gate.
- **Removing plan-level prose mechanics reduces style fidelity** → The style guide remains in every writer call, and chapter anatomy/prose density remain chapter-review criteria where real text exists.

## Migration Plan

Update the generic spec, style-guide planning clauses, planner prompt, reviewer prompt, templates, harness, and contract tests as one H-039 lever. Do not promote any run-001 candidate. Create run-002 from the accepted research and framing, regenerate only plan and downstream chapters, and compare the observed gate behavior with H-039's prediction.

Rollback is the parent commit containing the complete run-001 failure artifacts and previous assets.

## Open Questions

None before run-002. New fields are admitted only after a concrete chapter or judge failure demonstrates missing semantic context.
