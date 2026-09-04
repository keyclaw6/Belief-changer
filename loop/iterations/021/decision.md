# Decision — Iteration 021

**Verdict:** INCONCLUSIVE

**Hypothesis:** PRIMARY writer-prompt previous-chapter closed-list so chapter N cannot re-run N−1 (`re-argument` journey). No secondary. Plan reused (019).

**Predicted:** journey `re-argument` falls in BOTH vs 019 (A 7→<7, B 5→<5).

**Observed:**

| Signal | 019 A | 021 A | 019 B | 021 B |
|---|---|---|---|---|
| journey re-argument (PRIMARY) | 7 | **6** | 5 | **7** |
| belief re-argument | 3 | 5 | 1 | 7 |
| book-arc re-argument | 3 | 3 | 2 | 7 |
| factory-speech noted | 6 | 15 | 21 | 8 |
| blocking (all lanes) | 0 | 0 | 0 | 0 |
| voice/belief/journey/arc PASS | all | all | all | all |

**Targeted cluster:** journey `re-argument` improved in A only (7→6). B rose 5→7. One book, not both.

**Veto:** none. No new blocking class in both books. `trap-question-label` A-only (noise).

**Prediction accuracy:** partial (A hit by 1; B miss and worse). Trace: assembled writer prompt still ends with the old "handoff seam" assignment from `write_replicate.py`, contradicting the hypothesized clause.

**Factory change:** not promoted. Records kept. 019 accepted snapshot remains on campaign-001.
