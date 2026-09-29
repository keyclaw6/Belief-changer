---
name: upgrade
description: Upgrade or refactor the Belief-Changer repository itself—skills, prompts, factory runtime, autoresearch, harness/provider routing, research access, evaluation, state, tests, or documentation. Use before changing any repository behavior or architecture so changes are coherent, minimal, validated, and reviewed rather than patched ad hoc.
---

# Upgrade Belief Changer

Use this skill **before changing the Belief-Changer system itself**. It governs source/configuration changes: capabilities, skills, prompts, runtime code, provider/harness routing, autoresearch behavior, schemas, tests, documentation, and architectural cleanup. Normal immutable factory run artifacts produced under the existing runtime contract do not activate this skill unless their schema/process is being changed.

The goal is not more machinery. The goal is a more capable and reliable system with less accidental complexity. Prefer deleting, moving, consolidating, or clarifying existing material over adding another layer.

## Design principles

1. **Intelligence and elegance first.** Preserve room for agent reasoning. Encode only fragile mechanical invariants—identity, provider, sequencing, idempotency, immutable-state boundaries, or deterministic validation.
2. **One authoritative home + progressive disclosure.** Put each rule in the narrowest correct home and point to it instead of copying it across prompts/docs.
3. **Factory boundary stays clean.** One persistent top-level Pi Coding Agent owns the reusable book factory. Autoresearch remains outside Pi. Live model execution uses OpenCode Go only.
4. **Real failures drive upgrades.** Treat repeated friction, owner corrections, stalled loops, provider failures, and validation failures as evidence. Fix root causes rather than accumulating workarounds.
5. **Historical evidence stays historical.** Do not rewrite old hypotheses/decisions/results to match current architecture. Add explicit superseding state or abort records when necessary.
6. **Tests enforce mechanics, not taste.** Add focused tests for deterministic invariants. Do not convert model judgment into a synthetic scoring framework merely because something went wrong once.

## Put each change in the right home

- Cross-cutting runtime/authority invariants → `AGENTS.md`, sparingly.
- Reusable operational procedure → `skills/<name>/SKILL.md`.
- Rare detail, examples, or review prompts → that skill's one-level `references/`.
- Book-factory runtime semantics → `docs/FACTORY-V2.md`, `.pi/agents/`, `prompts/`, `scripts/bc_factory/`.
- Outer autoresearch semantics → `loop/PROGRAM.md`, `loop/prompts/`, `scripts/bc_autoresearch/`.
- Provider/runtime configuration → `factory/config.json` and the minimum directly connected runtime config.
- Deterministic invariants → code plus focused tests.
- Historical campaign evidence → `loop/iterations/` and other immutable history locations.

Before adding a rule, search for its current authoritative home. If it already exists, update that home and replace contradictory copies with a pointer.

## Agent Skills format

When creating, renaming, splitting, merging, or materially changing a skill, read [the Agent Skills reference](references/agent-skills-spec.md). Keep one coherent capability per skill and move conditional detail behind progressive disclosure.

For material skill changes, run the repository validation gate:
`bash scripts/check.sh`

If an Agent Skills validator is available in the current harness, use it additionally for skill-format changes. Do not block a useful upgrade merely because that optional validator is unavailable.

## Upgrade workflow

1. **Locate the current truth.** Read the directly involved implementation, contracts, tests, and connected callers/consumers. Use history only when it resolves an actual ambiguity or regression.
2. **Identify the failure mechanism.** State what is actually broken and why. Separate the observed failure from a guessed cause.
3. **Choose the smallest coherent change.** Prefer an existing rule/skill plus model reasoning over new state or orchestration. Remove stale paths when they are the source of ambiguity.
4. **Trace the blast radius.** Find directly connected configs, docs, tests, snapshots, wrappers, callers, and consumers that assume the old behavior.
5. **Design the context path.** Decide what must be globally known, what should load only when the capability activates, and what belongs in a rare reference.
6. **Implement and reconcile.** Change the authoritative home, remove contradictions, preserve unrelated proven behavior, and migrate direct dependents.
7. **Validate mechanics.** Run focused tests plus `bash scripts/check.sh`. Never ignore red validation merely because the intended change seems correct.
8. **Review material upgrades with bounded critics.** For a new/retired skill, provider/harness change, factory/autoresearch architecture change, or multi-path refactor, read [the bounded review prompts](references/review-prompts.md). Use independent critics when available; otherwise apply the same lenses yourself. Freeze one review target and keep review scope bounded.
9. **Integrate accepted findings once.** Fix material issues found by review, then perform a residual/coherence review. Do not enter endless review churn.
10. **Finish cleanly.** Inspect the final diff/tree as a whole. Remove obsolete files and stale references. Verify the new state is easier for the next capable agent to understand.

## Final review checklist

Before shipping, verify:

- **Value:** does this solve the real failure rather than document it?
- **Root cause:** did we eliminate the mechanism that created the problem?
- **Elegance:** is there a simpler design with fewer paths/rules/states?
- **One home:** is each invariant authoritative in one place?
- **Boundary:** are Pi factory, outer autoresearch, and host supervision still separated?
- **Provider:** is live model execution still OpenCode Go only?
- **Discovery:** can a fresh agent find the relevant skill without preloading implementation detail?
- **Historical integrity:** were old records preserved instead of silently rewritten?
- **Validation:** do focused tests and the full offline gate pass?
- **Cleanup:** were stale configs, wrappers, or contradictory instructions removed?
- **Future operator:** would the next capable agent know what to do without inheriting today's workaround story?

## Learning from corrections

An owner correction applies immediately to the current work. Then classify it:

- one-off incident → fix locally, do not create policy unless recurrence warrants it;
- reusable repository behavior → update the authoritative skill/runtime contract;
- deterministic invariant → enforce with focused code/tests;
- stale architecture → delete or migrate the old path rather than layering another warning over it.

Do not append long historical workaround prose to live skills. Rewrite the current procedure into the clean rule that should have existed before the failure. Git preserves history.
