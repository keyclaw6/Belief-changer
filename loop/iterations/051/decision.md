# Decision — Iteration 051 (supervised audit probe 1 of 2)

**Verdict:** SUPPORT (H-051 holds on all preregistered legs; no falsifier fired)

## Hypothesis (from hypothesis.md)

The 041–050 zero-KEEP run is measurement variance (generation + judge draw
at one replicate pair per subject) meeting or exceeding the KEEP band —
not nine wrong theories. V2's conservative machinery is the structural
improvement: it stops noise from being promoted as learning.

## Intervention / probe (exact)

No live research (preflight independently BLOCKED, gate unbypassed), no
paid generation, no external judge, no human calibration, no book output.
Faithful frozen-artifact replay: an offline stdlib probe
(/tmp/probe_051.py, sha256 in evidence.json) recomputed every 042–050
PRIMARY evaluation from retained records and replayed the v2 promotion
gate on production code
(scripts/bc_factory/experiments.py::wilson_lower, file sha256 in
evidence.json). Probe exit 0 = all support legs hold.

## Artifacts used (hashes / locators)

- HEAD 66967521d11e0b53ba6500071728c8cc1086e110; tree verified clean
  before and after (git status empty except 051 additions + 2 bounded
  source files, listed below).
- loop/results.tsv (canonical machine rows; sha256 in evidence.json) —
  deficit series recomputed from it and cross-checked value-by-value
  against loop/iterations/0{42..50}/decision.md (all verdicts QUANTIFY,
  all observed after-values present in situ).
- PRIMARY bands from loop/iterations/0{42..50}/hypothesis.md "Predicted
  impact" sections (042 deficit ≤32/≤22; 043 missing ≤4/0; 044 ≤13/≤16;
  045 ≤24/≤22; 046 ≤22/≤19; 047 ≤15/≤21; 048 ≤26/≤26; 049 ≤21/≤26;
  050 ≤22/≤30).
- loop/iterations/050/decision.md:12-40 (same-text exhibit + exoneration).
- factory/calibration.json: PENDING_REAL_HUMAN_CALIBRATION;
  factory/champion.json: NO_VALIDATED_V2_CHAMPION (both read, neither
  modified).

## Observed result

- F1: 0/9 interventions meet PRIMARY on both subjects (042/046/050 split
  one subject each; 043/045/048/049 miss; 044/047 worsen ≥ band both →
  the two restores). Recomputed table in evidence.json:primary_eval.
- F2: 050 identical edits → sugar +28 vs smoking −12, opposite-sign
  band-scale moves, "050 edits exonerated … Root model for the delta".
- F3: 041→050 sugar 40→58 (worse), smoking 28→28 (flat) — nothing
  accumulated despite 5+ carried lines. Deficit-delta signs per
  intervention: 042(−,+), 043(−,−), 044(+,+), 045(−,−), 046(−,+),
  047(+,+), 048(−,0), 049(+,+), 050(+,−).
- F4: repo wilson_lower(3,3)=0.4385 and (2,2)=0.3424, both < 0.5 — v2
  cannot promote at campaign-001 sample sizes; wilson_lower(9,9)=0.7009
  passes, i.e. the specified larger allocation is the way out.
  Calibration PENDING independently blocks decide() today.
- A1/A2/A3: none fired. Strongest old both-books drop (010
  factory-speech −12/−11) does not exceed the regen swing (28/12);
  cross-instrument caveat recorded in evidence.json.

## Tests / gates

- bash scripts/check.sh: PASS (145 tests, was 141; +4 new), exit 0 —
  "software checks only; no efficacy or release claim."
- Probe script exit 0; result JSON stored as loop/iterations/051/
  evidence.json (6501 bytes).

## Long-run implication

V2.1 is a better *rejector* of false learning, not yet a demonstrated
better *finder* of true improvements: nine QUANTIFYs, two shared-harm
restores, zero releases is the machinery working as specified
(loop/PROGRAM.md). But gates don't create convergence — at n=1 pair per
subject with regen swings of ±12–28 against a max(25%, 4) band, the
expected trajectory is indefinite QUANTIFY. Convergence needs the
already-specified allocation (≥3 independent pairs/subject +
confirmatory replication + real calibration), which this audit could not
supply. Campaign-001's 2-book census KEEPs promoted moves inside this
same noise envelope — that is the concrete process regression v2's gate
now forbids.

## Residual uncertainty

Single-replicate deficits conflate generation and judge noise
(book-level repeatability never measured; iter-000 A/A showed
chapter-level sampling sensitivity). Carr-distance scores are
uncalibrated judge observations, not reader outcomes. 050's exoneration
and all trace attributions are investigator judgments. The 043
side-channel (deficit −6/−10 both while PRIMARY missed on wrong
ontology) shows metrics can co-move without causation — attribution
remains the weakest link.

## Modified / untracked files (no commit, no push; champion untouched)

- ADDED loop/iterations/051/hypothesis.md (preregistration)
- ADDED loop/iterations/051/evidence.json (machine-readable result)
- ADDED loop/iterations/051/decision.md (this file)
- ADDED scripts/eval/tests/test_iteration_evidence.py (4 regression tests)
- MODIFIED scripts/validate_repo.py (one line: 'evidence.json' joins the
  allowed loop/iterations filenames — the supervisor-ordered bundle
  otherwise violates the repo's own gate; flagged as a v2.1 rigidity
  finding, not a relaxation: unknown names are still rejected)
- Did NOT touch: factory/champion.json, factory/calibration.json,
  factory/config.json, loop/learnings.md, loop/ledger.md, any 000–050
  record, any release pointer. No branches created, no history rewritten.

**Next:** STOP. Do not begin 052 under this authorization.
