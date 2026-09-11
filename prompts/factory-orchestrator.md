# Factory orchestrator — version 2

Read AGENTS.md, docs/FACTORY-V2.md and loop/PROGRAM.md. Work through explicit, inspectable stage tasks. Do not run a continuous hidden optimizer. Do not send mail, change model routes, mutate historical manuscripts or publish output as a side effect.

1. Research deeply, retaining bank/synthesis provenance. Prepare a v2 brief.json and research.json with truthful narrator and explicit scope. Legacy research/plans are unvalidated inputs, not automatic acceptance.
2. `python3 scripts/factory.py prepare --run ID --brief BRIEF --research RESEARCH` freezes the inputs, active code, contracts and provider config. A new run is required after an upstream change.
3. Use `task` to make the independent evidence-reviewer request; execute only with explicit paid authorization, or give the frozen task to the configured isolated role and use `submit` with its real metadata. No output file may substitute for the result protocol.
4. Planner → plan-reviewer. On REVISE, next explicit round; on ACCEPT, freeze that plan. Never overwrite production-books/master-plan.md while experimenting.
5. For each chapter in order: writer → chapter-reviewer. REVISE permits the next round, never CAP-as-ACCEPT. After ACCEPT, run state-editor from the actual delivered text. The next chapter receives all preceding delivered chapters/state records.
6. Run book-editor on the complete accepted manuscript; `assemble` applies exact edits and adds authorship/safety/source notes. Run independent final-auditor on that exact assembled text. Unresolved defects block completion.
7. `verify --run ID` must exit zero before reporting factory completion. Its COMPLETE_UNRELEASED status is not publication or proof of effectiveness. The optimizer uses separate preregistered pairwise tasks and promotion gates.

Roles return strict JSON; narrative prose remains natural in its text field. Store the actual model, family, route, harness and usage (null when unknown). External reviews must not fall back to the generating family. On context overflow, transport failure or invalid output, retain the failed unit as unfinished; never truncate inputs silently, print a success marker or skip ahead. Inspect `status`; do not infer success from file presence or elapsed time.
