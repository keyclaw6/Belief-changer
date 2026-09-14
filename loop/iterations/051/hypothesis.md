# Hypothesis — Iteration 051 (supervised audit probe 1 of 2)

## Meta-question

Is the v2.1 architecture a better SEARCH-AND-LEARNING PROCESS than
campaign-001 — not just better software? This probe tests one structural
claim: that v2's conservative machinery (preregistered PRIMARY, QUANTIFY on
splits/misses, restore-on-shared-harm, Wilson both-subjects promotion bar,
human-calibration requirement) stops measurement noise from being promoted
as learning, where campaign-001 promoted within-noise moves as KEEPs.

## H-051 (falsifiable)

The 041–050 drive's zero-KEEP outcome is caused by measurement variance
(generation + judge draw at one replicate pair per subject) meeting or
exceeding the preregistered KEEP band (deficit drop ≥25% AND ≥4, both
subjects) — not by nine consecutive wrong causal theories. At this
allocation the loop's expected long-run trajectory is indefinite QUANTIFY
(stall); convergence requires the already-specified larger allocation
(≥3 independent pairs/subject + confirmatory replication, loop/PROGRAM.md),
not sharper single-shot hypotheses.

## Preregistered evidence rules (frozen artifacts only, no live calls)

Support (all must hold):
- F1: 0 of 9 interventions (042–050) meet their preregistered PRIMARY band
  on both subjects (predicted bands from loop/iterations/0{42..50}/
  hypothesis.md; observed from loop/iterations/0{42..50}/decision.md and
  the canonical machine rows in loop/results.tsv).
- F2: same-factory-text regen exhibit — 050's identical edits move sugar
  deficit +28 (crash, edits exonerated) while smoking moves −12
  (band-met), i.e. opposite-sign band-scale moves with no factory-text
  difference between subjects (loop/iterations/050/decision.md:33-36).
- F3: no accumulation — cumulative 041→050 deficit goes sugar 40→58
  (worse) and smoking 28→28 (flat) despite 5+ carried-forward lines.
- F4 (gate replay on production code): the repo's own
  scripts/bc_factory/experiments.py::wilson_lower returns < 0.5 for
  (3,3) and (2,2) wins, and factory/calibration.json is PENDING — so v2's
  decide() blocks any campaign-001-sized promotion today.

Falsification (any one refutes noise-dominance as the whole story):
- A1: ≥1 of 042–050 meets its PRIMARY band on both subjects.
- A2: cumulative 041→050 deficit declines on both subjects.
- A3: any campaign-001 KEEP shows a both-books drop exceeding the largest
  same-text regen swing (|Δ| = 28 sugar / 12 smoking).

## Limitations (labeled)

Frozen-artifact replay/ablation only: no live research (preflight
independently BLOCKED, research gate unbypassed), no paid generation, no
external judge (external profile null), no human calibration
(factory/calibration.json PENDING). Single-replicate deficits conflate
generation noise with judge noise — book-level repeatability was never
measured. Carr-distance scores are uncalibrated judge observations, never
reader-efficacy evidence; old Carr-distance scores are not promotion
evidence. Trace-analysis attributions (e.g. 050 "exoneration") are
investigator judgments, not independent measurements.

```
parent: 66967521d11e0b53ba6500071728c8cc1086e110
instrument: frozen replay of 2026-09-06 Carr-distance panel records + v2 offline gates
```
