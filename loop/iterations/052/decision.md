# Decision — Iteration 052 (supervised audit probe 2 of 2)

**Verdict:** REFUTE (A holds; essential leg B fails; partial structural gain recorded)

## Hypothesis (from hypothesis.md)

H-052: v2.1 materially improves the research side of the loop — (A) its
coverage/preflight gates mechanically block old "complete" packages
despite omitted social lanes and access-block mislabeling, AND (B) its
source/inference path stops an actual historical overreach
(animal-model → human-efficacy inference on Pitchers-2010-class
material) from becoming usable empirical support before planning.
Preregistered rule: SUPPORT iff A1, A2 and B all hold; a missing
essential leg yields REFUTE.

## Historical artifacts (hashes in evidence.json:files; locators)

- production-books/quit-sugar/research/research-log.md:68 (Reddit
  r/sugarfree,r/keto,r/diabetes rejected, rights gate; no X lane),
  :67 (cdc/nhsinform/mayoclinic 403 "not a coverage loss"), :75-90
  (all-bank PASS audit), :31 (Reddit excluded, name-map).
- production-books/quit-smoking/research/research-log.md:30 (Reddit
  excluded, rights gate), :66-81 (count floors "cleared"), no X lane.
- production-books/quit-porn/research/sources/exa-neuroscience.md:5-13
  (Pitchers 2010, male rats, GAP "Extrapolation from rats to humans
  requires caution; does not test pornography specifically"), :17-25
  (Nestler 2001 drug-model GAP), :29-37 (Pitchers 2013 animal-only GAP).
  The old files handled this correctly; no fake old flaw was invented.
- production-books/quit-smoking/research/banks/bank-07-mechanism-science.md
  (M-packets carry Claim/Grade/Scope/Permitted/Prohibited/URL/Date; no
  verification/counterevidence/rights_basis/excerpt/retrieved_at) and
  sources/README.md ("Full packets exist for S-001 and S-009; remaining
  IDs are ledger locators").
- All three STATUS.json: LEGACY_RESEARCH_UNVALIDATED, recovery
  6a90ffcdddad3c908144014cc41e51d693df7f9e.

## Deterministic replay procedure (/tmp/probe_052.py, sha256 in evidence.json)

Production validators only (schema.validate_research,
research_access.validate_coverage/preflight, runs.prepare/Run.task/
submit on scaffolded tmp repos). Strict rule: normalized dossiers use
only facts/queries/URLs/claims explicitly in old files (porn ExaSearch
queries from research-log.md:26-34; Pitchers URL/claim/GAP verbatim);
scaffolding is labeled SCAFFOLD. The overbroad variant is labeled
synthetic-adversarial and tests current code only.

## What current gates caught (A HOLDS)

- A1: old-faithful dossier (web queries real; reddit/x zero queries, no
  scarcity trail) FAILS validate_coverage: "Every lane needs actual
  exploratory queries". Rights-gate scarcity label with zero queries
  still fails on the same rule. Non-live preflight returns BLOCKED (all
  twelve checks false); validate_preflight rejects it ("Live research
  access preflight is required before a non-fixture run");
  prepare(fixture=False) without preflight raises and creates no run.
  Positive control (well-formed 4-lane dossier) passes.
- A2: lossless normalization is impossible without inventing judgments:
  key-absent dossier FAILS validate_research with missing=
  [counterevidence, excerpt, locator, permitted_inference, population,
  prohibited_inferences, retrieved_at, rights_basis, verification].
  v2 forces inference boundaries to be WRITTEN DOWN — a genuine
  discovery improvement over bank packets' informal Permitted lines.

## What they did not catch (B FAILS — remaining failure mode)

- The caveated Pitchers normalization PASSES validate_research, and the
  caveat-stripped overbroad variant ("proves … lasting brain damage in
  human readers") PASSES TOO (prohibited_inferences:[] and
  counterevidence:[] satisfy the list checks) — schema enforces
  presence, never entailment. A hollow locator ("ledger-only; no
  excerpt retained") with paraphrase-as-excerpt likewise passes.
- Sequencing is real but insufficient: planner task before/without
  evidence ACCEPT raises ("Research needs independent evidence
  acceptance" — also verified post-REVISE), so workflow DOES force an
  independent review before planning. But a structurally valid
  evidence-reviewer ACCEPT with empty findings passes validate_review
  and unblocks planner — the overreach reaches planning mechanically.
- The semantic catch is entirely untested: zero tests assert
  permitted_inference semantics; no runs/ directory exists (evidence
  reviewer never executed outside fixtures); calibration PENDING.
  "Workflow requires semantic review" is established; "semantic review
  catches this" is not.
- Exploratory boundary: a one-query + rights-label fig leaf on reddit
  (all other lanes valid) PASSES validate_coverage — the gate forces a
  documented trail, not genuine lane substance.

## Supervisor verification precision

1) Direct historical evidence at commit cd730abc calls quit-porn
research "complete": production-books/quit-porn/README.md states
"Research is complete and stays valid" (identical text in the working
tree and at cd730abc).
2) Quit-sugar's retained research log has an all-bank PASS audit
(research-log.md:73-90) with Reddit excluded and no X lane, but no
exact status locator was cited declaring the entire package formally
COMPLETE — the formal-completeness claim is not made for quit-sugar.
3) Quit-smoking clearly records the Reddit exclusion and no X lane, but
its historical README at cd730abc still says `brief → researching` —
it is evidence of the old lane policy/omission, not of a formally
complete smoking package.
4) Therefore A1's valid mechanical result is narrower: v2.1 blocks the
historically observed omitted-lane pattern that the old research
process could permit, and it definitely would reject the directly
documented quit-porn-complete package for at least its missing X lane.
No claim is made that all three subjects were formally complete.

A2 clarification: A2 demonstrates stricter structured
provenance/inference-contract requirements (verification state,
bounded permitted_inference, prohibited lists, counterevidence,
rights basis, verbatim excerpt with locator), not by itself richer
discovery quality — the contracts force boundaries to be written,
not that the underlying inquiry was deeper.

## Tests / gates

- bash scripts/check.sh: PASS (145 tests), exit 0 — software checks
  only; no efficacy or release claim.
- Probe exit 0; verdict computed per preregistered rule from recorded
  validator outputs (evidence.json).

## Long-run implication for better-book probability

v2.1 raises the probability that future books rest on broader,
better-labeled research (mandatory web+Reddit+X+recovery lanes,
access-failure vs scarcity discipline, per-source inference contracts,
frozen preflight) — paperwork that bites: silent omission now fails
deterministically. But it does NOT raise the probability that a
plausible-sounding overreach is stopped before planning, because the
only checkpoint is a never-yet-run paid semantic review whose acuity is
unmeasured. Expected trajectory: fewer "thin dossier" failures,
unchanged exposure to "confident overclaim" failures until the reviewer
is calibrated against retained adversarial cases (e.g. the 052
Pitchers pair, which should enter the calibration case set).

## Untested live/social/judge/reader areas

Live preflight (BLOCKED, all checks false); real Reddit/X thread reads;
NopeCHA/CloakBrowser path; external reviewer independence and acuity;
judge calibration (needs ≥12 retained cases, 2+ human raters);
GSBS-control behavior; any reader outcome. Old Carr-distance scores
remain observations, never promotion evidence.

## Modified / untracked files (no commit, no push)

- ADDED loop/iterations/052/hypothesis.md, evidence.json, decision.md
- Preserved intact: 051 bundle, scripts/validate_repo.py one-line
  evidence.json allowance, scripts/eval/tests/test_iteration_evidence.py
- Did NOT touch: factory/champion.json, factory/calibration.json,
  factory/config.json, any release pointer, any 000–051 record, any
  historical research file. No branches, no history rewrite.

**Next:** STOP. Do not begin 053 under this authorization.
