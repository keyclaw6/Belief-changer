# Run Ledger — factory calibration

One row per run, newest last. Details live in each run's `report.md`; this is the
cross-run view the founder reads. Win-rate = overall pairwise incl. half-ties;
detect = real-Carr detection accuracy (0.5 ≈ indistinguishable).
The final row is also the compaction-safe live compass: update its last artifact,
next artifact, active hypothesis, and blocker at every artifact boundary—not only
when a run ends.

| run | date | stage | scope | last accepted artifact / judgment | next product artifact | win-rate | detect | gate / blocker | active hypothesis | generic lever? | amendment or resume action |
|-----|------|-------|-------|-----------------------------------|-----------------------|----------|--------|----------------|-------------------|----------------|----------------------------|
| run-001 | 2026-07-11 | A | research + framing + plan | research R4 and framing R2 accepted; plan rejected 0/3 | normalized plan | n/a | n/a | FAIL — plan 0/3 | H-010 supported; H-005 confounded | yes | H-039 normalize planner/reviewer to one source of truth |
| run-002 | 2026-07-11 | A | normalized plan + Chapters 1–3 | Chapter 2 R3: `REVISE`, zero blockers; Chapter 1 accepted | run-003 prose-only compression of certified Chapter 2 | n/a | n/a | FAIL — Chapter 2 rejected 3/3 on craft metrics | H-039 mixed | yes | H-040 isolate post-semantic prose convergence |
| run-003 | 2026-07-11 | A | Chapter 2 prose-only compression | compression review: `REVISE`, zero blockers; 3,236 words | run-004 full/minimal context A/B on exact candidate | n/a | n/a | FAIL — length passed, prose metrics failed | H-040 mixed | yes | H-041 isolate editor-context interference |
| run-004 | 2026-07-11 | A | Chapter 2 editor-context A/B | run boundary + direction audit: `GO`; exact candidate/review frozen | Opus full-context and minimal-context Chapter 2 edits | n/a | n/a | IN PROGRESS — controlled H-041 arms | H-041 | yes | no shared-asset change |
