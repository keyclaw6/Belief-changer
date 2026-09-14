# Hypothesis — Iteration 052 (supervised audit probe 2 of 2)

## Meta-question (discovery side)

Does v2.1 materially improve what the loop can LEARN from research, or
does it merely add paperwork? 051 covered promotion statistics; 052
covers research discovery. Narrow reading of 051 is accepted: it showed
one-pair inference too noisy to promote, not that all nine hypotheses
were good. The 050 "exoneration" is treated here as investigator
judgment, not evidence.

## H-052 (two-part conjunction; missing essential leg yields REFUTE)

v2.1 materially improves the research side of the loop:

- (A) Its coverage/preflight gates mechanically block old research
  packages the old system marked complete/PASS despite omitting
  required social lanes and recording access blocks without cover.
- (B) Its source/inference path stops an actual historical overreach —
  an animal-model → human-efficacy inference on Pitchers-2010-class
  material (quit-porn exa-neuroscience.md) — from becoming usable
  empirical support before planning.

## Historical grounding (no invented flaws)

- quit-sugar research-log.md:68: Reddit (r/sugarfree, r/keto,
  r/diabetes) "rejected as direct source; reachable mirrors/blogs used
  instead" under a rights gate; no X lane anywhere. Final bank audit:
  all banks PASS. Access blocks (cdc.gov/nhsinform/mayoclinic HTTP 403)
  recorded as "not a coverage loss" (:67).
- quit-smoking research-log.md:30: "Reddit excluded (rights gate)"; wave-3
  counts "clears ≥100" etc. treated as floors cleared; no X lane.
- quit-porn exa-neuroscience.md: Pitchers 2010 (male rats, PMC2970635)
  with explicit GAP "Extrapolation from rats to humans requires caution;
  does not test pornography specifically" (:13); Nestler 2001 (:25) and
  Pitchers 2013 (:37) carry equivalent animal-model GAPs. The old files
  handled this correctly — the probe must NOT invent a fake old flaw.
  The overbroad variant below is labeled synthetic-adversarial and tests
  current code only.
- Old bank packets (e.g. quit-smoking bank-07 M-001..M-040) carry Claim /
  Grade / Scope / Permitted / Prohibited / URL / Date, but no v2
  verification state, counterevidence list, rights_basis, excerpt, or
  retrieved_at; sources/README.md states most S-IDs are "ledger
  locators" with full packets only for S-001/S-009.

## Preregistered support / falsification

A1 (mechanical): a dossier faithful to the old lane structure — real
porn ExaSearch query strings as web queries (research-log.md:26-34);
reddit/x lanes with zero executed queries and no reachable-source
scarcity trail (rights-gate exclusion is neither access failure nor
scarcity) — MUST FAIL validate_coverage with a named FactoryError; a
non-live preflight MUST return BLOCKED and be rejected by
validate_preflight; prepare(fixture=False) without preflight MUST raise.
Positive control: a well-formed 4-lane dossier passes (existing
CoverageTests pattern, rerun in-probe).

A2 (schema strictness): lossless normalization of M-013 (Cochrane),
the Pitchers-2010 entry, and locator-only S-012 is impossible without
inventing verification / counterevidence / rights_basis /
excerpt+retrieved_at — facts not present in the old files. A dossier
leaving those keys absent MUST FAIL validate_research (exact_keys).
Record the field inventory either way.

B (inference boundary): the caveated Pitchers normalization MUST PASS
validate_research (it is well-formed), and the labeled adversarial
variant with the caveat stripped from permitted_inference MUST ALSO be
tested: if production validate_research rejects it mechanically, note
the reason (B supported mechanically). Otherwise run the production
fixture-run chain: planner task before evidence ACCEPT MUST raise
(sequencing holds); then submit a structurally valid evidence-reviewer
ACCEPT with empty findings on the overbroad dossier — if it passes
validate_review and unblocks planner, B FAILS: the catch depends on an
untested semantic reviewer (no runs/ in tree; calibration PENDING; no
test asserts permitted_inference semantics), not on a mechanical
guarantee.

Verdict rule: SUPPORT iff A1, A2 and B all hold. If B fails while A
holds, verdict is REFUTE with the partial structural gain explained
(A = paperwork that bites; inference judgment remains unproven). If A1
fails (gates accept the old omission), verdict is REFUTE for the
stronger reason that the gates are weaker than claimed.

## Limitations (labeled)

Frozen replay only: preflight independently BLOCKED (all live checks
false); no live X/Reddit/browser, no logins, no paid generation, no
external judge, no human calibration. The fixture-run chain isolates
inference handling, not live coverage. Carr-distance scores are not
promotion evidence. No reader-efficacy claim.

```
parent: 66967521d11e0b53ba6500071728c8cc1086e110
instrument: production validators (schema.py, research_access.py, runs.py) on retained historical research
```
