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
| run-002 | 2026-07-11 | A | normalized plan + Chapters 1–3 | master plan R3: `fit to write from`; no prose yet | Opus Chapter 1 R1 from accepted plan | n/a | n/a | BLOCKED — OpenRouter credit 402; Claude Pro OAuth 401 | H-039 downstream sufficiency | yes | refresh writer auth, then resume unchanged Opus baseline |
