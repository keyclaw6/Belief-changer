# Bounded review prompts for Belief-Changer upgrades

Load this reference only for a **material repository upgrade** when independent review is useful. Reviewers are critics, not implementers. They do not edit, commit, push, mutate external systems, or broaden the task into unrelated cleanup.

## Common scope guard

Use this block in every review:

> READ-ONLY review. Do not edit files, commit, push, mutate external systems, or expand into unrelated cleanup. The supplied frozen review target is authoritative. Review only the explicit in-scope paths plus directly connected callers, consumers, tests, routing/docs, and authoritative rules needed to judge the change. Prefer deletion/simplification over added machinery. Distinguish a real defect from a stylistic preference.

## Round 1 review lanes

Use lanes 1–3 by default when independent reviewers are available. Add lane 4 for real harness/provider portability risk and lane 5 when deterministic code/state changed.

### 1. Elegance and architecture

> Is this the smallest coherent change? Find duplicated rules, needless files/state/code, accidental framework growth, or places where model reasoning was replaced by brittle prescription. Check progressive disclosure and whether live context grew without broad value.

### 2. Correctness and connected-system coherence

> Trace the direct blast radius. Find contradictions, stale pointers, broken assumptions, missing migrations, incompatible frozen-runtime expectations, or behavior that now differs across connected paths.

### 3. Capability discovery and prompt/context design

> Can a fresh capable agent discover and correctly use the changed capability without loading unnecessary context? Check the skill frontmatter, skills catalog, any truly global routing pointer, and the split between SKILL.md core procedure and references.

### 4. Runtime/provider portability

> Check that the portable core still uses one persistent Pi Coding Agent for the book factory and OpenCode Go only for live model execution. Identify leaked assumptions about a host, alternate provider, CLI worker, scheduler, browser, or bridge. Host conveniences must not become alternate truth paths.

### 5. Mechanical correctness

> Review only deterministic mechanics: state transitions, idempotency, parsing, provider routing, immutable boundaries, retry/circuit-breaker behavior, tests, and failure handling. Verify code enforces exactly the intended invariant without encoding subjective judgment.

## Reviewer output contract

Return at most 8 findings:

- **HIGH** — correctness, authority, data-loss, provider/runtime, or major architecture defect.
- **MEDIUM** — meaningful coherence, discovery, portability, or avoidable-complexity problem.
- **LOW** — only concrete and cheap issues; omit taste-only suggestions.

Each finding: problem → why it matters → exact path(s) → smallest fix.

End with `CLEAN ENOUGH: yes|no`.

## Round 2 residual review

After accepted fixes, freeze the new target and review only residual contradictions, regressions caused by the fixes, duplicated authority, broken routing, or directly connected inconsistencies. Do not reopen resolved stylistic preferences.

Stop after round two when there are no material findings. A third round is justified only for a HIGH/MEDIUM issue that required another meaningful architecture change.
