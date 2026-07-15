# redesign-book-factory — implementation ledger

This is the durable, authoritative to-do list for the whole-factory redesign.
It is not a product-iteration ledger. `loop/results.tsv` and
`loop/learnings.md` remain historical evidence from the retired campaign until
RF-19 starts a new lineage.

Task count: **32**, with stable IDs `RF-00` through `RF-31`. RF-00 is the first
executable implementation task; the change-package approval state is tracked
separately below and is not an implementation item.

## Fixed boundary

- Authoritative repository: `/home/kab/Belief-changer/Belief-changer` only.
  The outer clone is stale and MUST NOT be read from or edited.
- Ledger created from `main` at
  `4d7c6eae4fed49003eda36b7b2e96b8eff885f44`.
- Review source: *Whole-Factory Review — Diagnosis, Redesign, and Next
  Experiments*, SHA-256
  `2e2d3b4ce2d7f81ffbe902a52a7771616b4ee9d7e0c7154a9eaf52d6ef042ade`.
- `iter-007` is the last scored product; `iter-004` is the historical
  best-scoring accepted snapshot. Neither proves a stable product improvement.
- The current production chapters are the rejected `iter-007` diagnostic prose
  while the iteration-7 style amendment was reverted.
- `main` also contains the paused, unscored iteration-8 style amendment:
  current style blob `72710b8bdd1ac0ecaddfaa9abb36b28926993df9`,
  pre-iteration-8 blob `ee3653fb0fefaf87b348706c6e0f7ab4e576d6e6`.
- Retired `calibration/runs/` is read-only archaeology. Do not resume it.
- Missing OpenRouter credit/key is not a blocker for RF-00 through RF-22. It
  becomes a real external dependency only when RF-23 generates Opus prose.
- **Operator stop law effective now; RF-00 mechanizes it:** the current
  `PROGRAM.md` loop MUST NOT run
  or generate/mutate any plan, commission, chapter, or production product before
  RF-23 is explicitly `READY`. Before then, no chapter prose may be generated.
  Allowed pre-RF-23 work is implementation verification, read-only inspection,
  isolated anonymous H-F04 calibration, and the redesign-controlled RF-21/RF-22
  plan/commission candidates inside RF-02's isolated snapshot after their own
  dependencies pass.

## Global invariants

1. Hold every item against `docs/BOOK-FACTORY-VISION.md`; no agent may change it.
2. Preserve original prose, reference blindness during generation, source
   traceability, evidence honesty, medical safety, non-shaming framing, and the
   willpower-free method. Preserve the isolated word-sequence near-copy hard gate
   against the matched reference; no score may override it.
3. Preserve the stable production-book core paths. `commissions/` is additive.
4. Keep sugar-only constructs out of generic contracts.
5. The root orchestrator does not implement and never reads whole chapters,
   whole books, or reference prose. Fresh agents do all prose-heavy work and
   return compact evidence. Founder/human reading means the founder or another
   named human, not a simulated root reading.
6. One ledger item at a time: implementation agent -> independent reviewer ->
   `REVISE` feedback to the implementation agent until `PASS`.
7. Commit and push straight to `main` only after reviewer `PASS`, one logical
   conventional commit per item. Preserve unrelated worktree changes.
8. Every behavior change follows this active OpenSpec delta; every new test
   cites the scenario it proves or is marked infrastructure.
9. `bash scripts/check.sh` must pass for every implementation item. Product
   experiments also run their item-specific gates.
10. Demonstrated current-state findings, supported generalizations, and
    untested hypotheses remain explicitly distinguished. A completed
    implementation is not evidence that its product hypothesis worked.
11. No dashboard, direction audit, preregistration bureaucracy, per-call
    micro-ledger, or intermediate-artifact win may be added without a failing
    acceptance test that requires it.
12. `prompts/style-guide.md` is founder-owned. Any edit, including restoring an
    earlier blob, requires a recorded explicit founder instruction naming that
    change; backlog inclusion alone is not approval.
13. H-F04's only reference exception is anonymous reference-as-candidate
    calibration: evaluators are blind to identity/provenance, outputs are
    isolated, and no reference text or verdict may flow into generation.

## State and attempt protocol

Allowed status values: `TODO`, `READY`, `IN_PROGRESS`, `REVIEW`, `REVISE`,
`BLOCKED`, `CONDITIONAL`, `DONE`, `SKIPPED`. At most one item may be
`IN_PROGRESS`, `REVIEW`, or `REVISE`.

For every attempt, replace the compact attempt fields with the date, agent ID,
scoped result, reviewer verdict, and remaining defect. `Commit / push` records
the accepted commit SHA after it exists; a following ledger checkpoint may add
the SHA without reopening the implementation verdict.

## Change-package review state

- Package state: `PASS`
- Executor repair passes: `2`; latest: 2026-07-14 added an executable,
  dependency-first legacy-loop guard task and its spec/design traceability.
- Independent review attempts: `3`; latest verdict: `PASS`; verifier confirmed
  32/32 dependency closure to RF-00, complete legacy-entrypoint inventory scope,
  resolution of every prior finding, and passing repository gates.
- Accepted package commit subject: `spec(factory): approve whole-factory redesign`.
  The exact commit SHA is intentionally reported after creation rather than
  embedded self-referentially.
- No RF implementation task is complete. RF-00 remains the first implementation
  task, and RF-01 remains blocked on explicit founder direction.

## Phase 0 — authorize, pause, and resolve the baseline

### RF-00 — Install the fail-closed legacy product-generation guard

- [x] Mechanically block every legacy generation/promotion path before RF-23 readiness.
- Status: `DONE`
- Evidence class / report: demonstrated exposed harness path; §§5 cause 3 and 7
  action 3; independent verifier P0.
- Problem / root cause: the OpenSpec pause is currently declarative while
  `PROGRAM.md` and legacy `scripts/loop/` entrypoints remain callable, so an old
  iteration can reach a model/network call or mutate product/config before the
  redesign is ready.
- Exact scoped change: inventory every legacy entrypoint that can generate or
  promote plans, commissions, chapters, or production configuration; add one
  fail-closed readiness guard to each and to `PROGRAM.md`. Default and pre-RF-23
  invocations stop before endpoint/model/network resolution and before any
  product, config, score, or ledger write. The only permitted execution path is
  an explicit redesign authorization that verifies the requested RF stage,
  RF-23 readiness for prose generation, and a candidate root isolated from the
  accepted production/config paths; it MUST NOT act as a bypass for the legacy
  current-product path.
- Likely files: `PROGRAM.md`, all write-capable entrypoints discovered under
  `scripts/loop/` (at minimum `run_iteration.py` and promotion/gate paths), one
  smallest shared guard only if multiple callers prove it necessary, and focused
  tests under `scripts/eval/tests/`.
- Acceptance: an automated pre-ready invocation exits nonzero before a stubbed
  model/network function can run and leaves product/config/score/ledger fixture
  hashes unchanged; a static inventory test fails if a write-capable legacy
  entrypoint lacks the guard; authorization targeting accepted production paths
  is rejected; an explicitly authorized RF-23-ready dry-run targeting an
  isolated candidate fixture reaches the dispatch boundary and can write only
  inside that fixture.
- Verification: no-network guard tests covering every inventoried entrypoint,
  before/after fixture hashes, authorized-isolation test,
  `bash scripts/check.sh`.
- Dependencies: independent `PASS` on this OpenSpec change package. RF-00 MUST
  be the first implementation commit; RF-01 and every later task depend on it
  directly or transitively.
- Implementation attempts: `4`; latest: 2026-07-14
  `/root/rf00_recovery_executor` — repaired review attempt 2's remaining P0:
  every concrete chapter, score, judge-task, and gate-ledger output now rejects
  an existing multiply linked file immediately before mutation; focused hard-
  link escape and valid-write controls pass, with full review still pending.
- Review attempts: `3`; history: 2026-07-14 `REVISE` — concrete symlink leaves,
  ambiguous ledger parsing, and helper-hidden writes escaped verification;
  2026-07-14 `REVISE` — an existing multiply linked output could mutate an
  outside inode; 2026-07-14 `PASS` — manual and focused replay confirmed all
  findings fixed, 14/14 focused and 91/91 full tests, strict OpenSpec, diff and
  size gates, three guarded mains, and four output-checked mutators.
- Commit / push: accepted subject `feat(loop): fail closed during factory
  redesign`; exact SHA is captured at the next ledger checkpoint to avoid
  impossible self-reference.

### RF-01 — Resolve the paused iteration-8 style baseline with the founder

- [ ] Obtain an explicit founder choice before editing or freezing the style baseline.
- Status: `BLOCKED`
- Evidence class / report: demonstrated boundary mismatch; review basis, §4
  iter-007, §5 cause 3; repository governance audit.
- Problem / root cause: `main` contains an unscored style amendment, so H-F01
  cannot honestly claim style rules were frozen.
- Exact scoped change: ask the founder to choose explicitly between (a) restoring
  the pre-iteration-8 blob by one reviewed commit or (b) retaining current blob
  `72710b8...` as H-F01's frozen style baseline. Do not edit the founder-owned
  guide until that choice is recorded. If restore is approved, remove only the
  paused coaching/permission amendment without destructive checkout.
- Likely files: `prompts/style-guide.md`, this ledger state only.
- Acceptance: founder instruction and chosen baseline hash are recorded. Restore
  path requires `ee3653fb0fefaf87b348706c6e0f7ab4e576d6e6`; retain path requires
  no style diff and records `72710b8bdd1ac0ecaddfaa9abb36b28926993df9` as the
  fixed H-F01 input. No other prompt, plan, research, or chapter changes.
- Verification: approval reference, hash check, focused diff if authorized,
  `bash scripts/check.sh`.
- Dependencies: RF-00 and explicit founder instruction. Current blocker:
  no specific restore/retain approval has been given.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.

### RF-02 — Isolate candidate configuration and product atomically

- [x] Make rejection incapable of changing current production or accepted config.
- Status: `DONE`
- Evidence class / report: demonstrated; §§1, 5 cause 3, 7 action 3, 10.
- Problem / root cause: current gate reverts selected assets but leaves generated
  chapters, producing a configuration/product mismatch.
- Exact scoped change: snapshot accepted configuration and product before a run;
  write candidate config and prose only under an experiment snapshot; implement
  one promotion action that moves both together; rejection leaves current bytes
  untouched.
- Likely files: `scripts/loop/gate.py`, `scripts/loop/run_iteration.py`, focused
  tests under `scripts/eval/tests/`, `loop/` snapshot conventions.
- Acceptance: automated fixtures prove reject = byte-identical current product
  and config; accept = exact tested pair promoted; interrupted promotion fails
  closed; old iteration evidence remains readable.
- Verification: targeted atomic-promotion tests, `bash scripts/check.sh`.
- Dependencies: RF-00. MUST finish before RF-23 treatment generation.
- Implementation attempts: `8`; latest: 2026-07-14
  `/root/rf02_completion_owner` — the real no-endpoint writer branch now prints
  the complete shell-safe pinned resume command with no secrets, and every new
  RF-02 code file is at most 260 lines. The exact fallback path has regression
  coverage.
- Review attempts: `8`; latest verdict / findings: `PASS` — prior manual-fallback
  and file-size findings are resolved; 30/30 focused and 120/120 full tests,
  strict OpenSpec, and diff checks passed, with core recovery, promotion, and
  binding scenarios accepted.
- Commit / push: `c2b1935b62d71ef504b874ee9f9e4ed9cf638c06`
  (`feat(loop): isolate candidate product atomically`).

## Phase 1 — repair the upstream intervention contract

### RF-03 — Enforce a completed subject contract

- [x] Require the primary and subordinate beliefs before downstream work.
- Status: `DONE`
- Evidence class / report: demonstrated gap; §§1, 5 cause 1, 7 action 1.
- Problem / root cause: the brief leaves the load-bearing false belief unresolved
  and does not provide a small belief set against which research and planning
  can be judged.
- Exact scoped change: add reader-language primary belief, three-to-five
  subordinate beliefs, destination, exclusions, and safety perimeter to the
  template and enforce a no-placeholder downstream gate.
- Likely files: `production-books/_template/00-brief.md`, pipeline validation or
  focused contract tests; current quit-sugar values are deferred to RF-21.
- Acceptance: missing/placeholder fields stop framing and planning; a complete
  non-sugar sample passes; no sugar-specific category enters the template.
- Verification: scenario tests for “incomplete subject contract”,
  `bash scripts/check.sh`.
- Dependencies: RF-00.
- Implementation attempts: `3`; latest: 2026-07-14
  `/root/rf03_subject_contract_owner` — normalized terminal `.?!` only for
  whole-value sentinel matching and rejected values composed solely of that
  punctuation while preserving substantive punctuated reader language.
- Review attempts: `3`; latest verdict / findings: `PASS` — generic required
  fields, non-sugar passing control, unresolved-sentinel and false-positive
  controls, 8/8 focused and 128/128 full tests, strict OpenSpec, and diff checks
  all passed with no actionable findings.
- Commit / push: `3c61c3908d211c498f7b61683f5246f1cb07e19a`
  (`feat(pipeline): enforce completed subject contracts`).

### RF-04 — Add intervention-ready evidence units and belief coverage

- [x] Preserve source discipline while making synthesis usable by interventions.
- Status: `DONE`
- Evidence class / report: demonstrated transport loss; §§2–3, 5 cause 2,
  7 target stage 1.
- Problem / root cause: rich situations and reader language are compressed into
  generic synthesis/plan IDs before they reach the chapter.
- Exact scoped change: require supported units containing situation, reader
  wording, implicated belief, emotion, permitted/prohibited inference, and
  source locator; retain DeepSeek V4 Pro for breadth and use an independent
  high-reasoning evidence editor from another family for synthesis audit; audit
  coverage against the brief belief set, not packet quota. Preserve the current
  pre-Git rights/privacy gate for access, minimum excerpt, retention,
  redistribution, attribution, privacy basis, deletion sensitivity, and personal
  data. Do not regenerate quit-sugar research for H-F01.
- Likely files: `prompts/research-agent.md`,
  `production-books/_template/research/{lived-experience.md,scientific-evidence.md}`,
  focused contract tests.
- Acceptance: every unit traces to source; unsupported fields are omitted rather
  than invented; gaps route to research; sample units transfer to smartphone and
  fear subjects; rejected rights/privacy material is neither tracked nor counted
  as evidence coverage.
- Verification: traceability/coverage fixtures, `bash scripts/check.sh`.
- Dependencies: RF-03.
- Implementation attempts: `3`; latest: 2026-07-14
  `/root/rf04_evidence_units_owner` — rejected exact whole-value rights/privacy
  sentinels by field while preserving attribution-only `n/a`, substantive
  explanations, and all 47 legacy locators.
- Review attempts: `3`; latest verdict / findings: `PASS` — 25/25 focused and
  134/134 full tests, strict OpenSpec and diff checks, downstream stage gate,
  structured source binding, rights/privacy matrix, and 47/47 legacy locators
  all passed with no actionable findings.
- Commit / push: `50d3763844c54788828d59b356ed8cd11825129d`
  (`feat(research): enforce intervention-ready evidence units`).

### RF-05 — Encode the belief graph, reader journey, and earned authority

- [x] Make framing decide the cumulative intervention before planning.
- Status: `DONE`
- Evidence class / report: supported generalization; §§5 causes 1 and 6, 7
  action 1, 8.
- Problem / root cause: framing inventories beliefs and forks without resolving
  one causal reader journey or an evidence-honest alternative to fabricated
  Carr authority.
- Exact scoped change: require a compact belief graph and per-chapter entering
  belief, subject-specific encounter, discovery, emotional turn, leaving belief,
  handoff, reserved work, and authority strategy grounded in recognition,
  bounded lived patterns, and logic. Use a high-reasoning native planner (Sol or
  equivalent), not the writer model.
- Likely files: `production-books/_template/framing.md`, planning contract tests;
  current quit-sugar framing is deferred to RF-21.
- Acceptance: adjacent states form a causal chain; authority never depends on
  invented pedigree or unsupported danger; two contrasting subject examples
  validate genericity.
- Verification: independent framing-review fixture, `bash scripts/check.sh`.
- Dependencies: RF-03, RF-04.
- Implementation attempts: `2`; latest: 2026-07-14
  `/root/rf05_framing_owner` — added a hash-bound independent complete-framing
  semantic review before planning, field-aware unresolved sentinels, normalized
  state identity, reproduced authority probes, and corrected test traceability.
- Review attempts: `2`; latest verdict / findings: `PASS` — hash-bound semantic
  review and bypass probes block unsafe authority; sentinel and state identity
  repairs pass; 25/25 focused and 145/145 full tests, strict OpenSpec, and diff
  checks are clean with no actionable findings.
- Commit / push: accepted subject
  `feat(framing): enforce causal reader journeys`;
  `a73ee7e9f0d6d89a34be7bd8da6cd5b9eaf5b14a`.

### RF-06 — Make master-plan cards enact reader transitions

- [x] Replace topic/coverage jobs and catalogue-now-demolish-later jobs.
- Status: `DONE`
- Evidence class / report: primary demonstrated cause; §§3, 5 cause 1, 7 action
  1, 8.
- Problem / root cause: Chapter 3's J-01–J-22 prospectus is explicitly planned;
  cards can name topics or future work instead of completing a change now.
- Exact scoped change: require the seven semantic reader-state fields in every
  argument-bearing card, preserve evidence/continuity/budgets, and prohibit
  setup or catalogue as the primary persuasive job. Keep cards semantic, not
  prose templates or mechanical section schemas.
- Likely files: `prompts/master-plan-skill-v2.md`, plan contract tests; current
  quit-sugar cards are deferred to RF-21.
- Acceptance: fixtures reject catalogue/setup cards and accept three distinct,
  cumulative modes; no duplicated plan-wide inventories; no new style metrics.
- Verification: planner-contract tests, `bash scripts/check.sh`.
- Dependencies: RF-05.
- Implementation attempts: `2`; latest: 2026-07-14
  `/root/rf06_plan_cards_owner` — bound total and per-card budgets, card-only
  semantic content and canonical inventories, and plan transitions to the
  accepted framing journey.
- Review attempts: `2`; latest verdict / findings: `PASS` — positive exact-sum
  budgets, semantic-card exclusivity, accepted-framing binding, 11/11 focused
  and 156/156 full tests, strict OpenSpec, and diff checks passed with no
  actionable findings.
- Commit / push: accepted subject
  `feat(planning): enforce reader-state chapter cards`;
  `960f84d8d150b416344cd54562b12248a8d23cca`.

### RF-07 — Make plan review a blocking cumulative reader walk

- [x] Enforce `fit to write from` without a one-cycle waiver.
- Status: `DONE`
- Evidence class / report: demonstrated governance failure; §§1, 5 causes 1 and
  4, 7 action 1.
- Problem / root cause: writing proceeded from a plan whose own review said
  changes were required, and reviewer detection lacked enforceable routing.
- Exact scoped change: simulate the first-three and whole-book reader walk;
  reject three setup chapters, deferred catalogues, duplicate modes, exit states
  that mean only “keep reading”, and unresolved writer-facing authority; block
  commissioning until the standalone verdict is `fit to write from`.
- Likely files: `prompts/master-plan-reviewer-v2.md`, plan gate/runtime tests.
- Acceptance: every blocking fixture ends `needs changes first`; only a clean
  cumulative plan ends `fit to write from`; runtime refuses all other verdicts.
- Verification: plan-review fixtures, `bash scripts/check.sh`.
- Dependencies: RF-06.
- Implementation attempts: `3`; latest: 2026-07-14
  `/root/rf07_plan_review_owner` — repaired review attempt 2's remaining P1 by
  recognizing whitespace- or hyphen-separated `not[-yet]-reviewed` markers while
  preserving resolved-negation controls; exact regressions and all gates pass.
- Review attempts: `3`; latest verdict / findings: `PASS` — unfinished whitespace
  and hyphen variants block; exact native reviewer, plan/framing hashes,
  standalone verdict, and commissioning gate verified; 27 focused and 161 full
  tests pass with strict OpenSpec and clean diff checks; no findings.
- Commit / push: `ccfb895be6bb251aac9273f9a2e45f6aff84b22b`
  (`feat(planning): block commissioning on plan review`).

## Phase 2 — repair handoffs, drafting, and review

### RF-08 — Extend the existing commissioner contract

- [x] Carry reader state and assigned source texture without creating a mini-plan.
- Status: `DONE`
- Evidence class / report: supported interface candidate, not proven solution;
  §§6 item 9, 7 action 2, 8.
- Problem / root cause: the existing commissioner is promising but lacks the
  newly binding reader-state contract, and retired runs prove commission alone
  does not prevent invention.
- Exact scoped change: modify—not replace—the commissioner to carry received and
  leaving belief, grounded situation/wording, permitted mechanism, emotional
  turn, limits, exact tokens, handoff, and reserved work; retain natural-language
  form and `COMMISSION BLOCKED`; assign the role to a fresh high-reasoning
  commissioning editor.
- Likely files: `prompts/chapter-commissioner.md`, commissioner fixtures.
- Acceptance: self-sufficient commission has no unresolved ID or unassigned
  work, quotes only allowed source/frozen text, contains no outline/prose, and
  blocks conflicts rather than repairing them silently.
- Verification: grounded and blocked commission fixtures, `bash scripts/check.sh`.
- Dependencies: RF-06, RF-07.
- Implementation attempts: `3`; latest: 2026-07-14
  `/root/rf08_commission_contract_owner` — repaired review attempt 2 by treating
  `P-*` and `AU-*` as canonical assigned IDs, forcing any `GAP-*` to block, and
  permitting exact quote spans embedded in assigned belief values while
  preserving whole-value and arbitrary-quote controls; 8 focused and 169 full
  tests pass with strict OpenSpec and clean diff checks.
- Review attempts: `3`; latest verdict / findings: `PASS` — independent final
  rereview confirmed canonical IDs, assigned provenance, valid quote boundaries,
  exact blocking, and no anatomy/drafting leakage; 8/8 focused and 169/169 full
  tests, strict OpenSpec, and diff checks pass with no findings.
- Commit / push: `d6d2f23e7a18562fa4abfc29cf0a77344bfc2d27`
  (`feat(commissions): enforce grounded chapter contracts`).

### RF-09 — Add commission storage, generation, and whole-set audit

- [x] Activate `production-books/<slug>/commissions/chapter-NN.md` as a gate.
- Status: `DONE`
- Evidence class / report: supported remedy with known failure risk; §§6, 7
  action 2, 8.
- Problem / root cause: commissioner exists only as a prompt; current runtime has
  no canonical commission artifact, assigned-packet resolver, set audit, or stop.
- Exact scoped change: add the template/output path, generate from accepted plan
  plus only assigned packets, audit all selected commissions together for
  grounding/ownership/continuity, and fail closed on `COMMISSION BLOCKED`.
- Likely files: `production-books/_template/`, `prompts/chapter-commissioner.md`,
  minimal orchestration under `scripts/loop/`, tests.
- Acceptance: no writing call occurs before all selected commissions pass;
  unassigned packets never enter a call; blocked set preserves previous product.
- Verification: context-capture and blocked-set tests, `bash scripts/check.sh`.
- Dependencies: RF-02, RF-08.
- Implementation attempts: `2`; latest: 2026-07-14
  `/root/rf09_commission_runtime_owner` — bound eligibility to the exact
  post-commission candidate pair and rejected invalid selection/book identity
  before candidate access or callbacks.
- Review attempts: `2`.
  - Review 1: `NEEDS CHANGES` — receipt omitted the exact post-commission pair
    hash; empty, duplicate, or invalid selected chapters were accepted; selected
    book identity was not canonicalized before filesystem or validator access.
  - Review 2: `PASS` — no findings; 44/44 focused and 175/175 full tests, strict
    OpenSpec, diff, and code-size gates pass.
- Commit / push: accepted subject
  `feat(commissions): gate complete commission sets`;
  `b430e4e075c7bf941fe808b1081fdcd93f402e5d`.

### RF-10 — Shrink the writer contract and runtime context

- [x] Switch semantic authority from full plan/style to commission.
- Status: `DONE`
- Evidence class / report: primary supported hypothesis; §§1, 5 causes 2 and 7,
  7 action 2.
- Problem / root cause: writers search an 87 KB style guide and whole-book plan
  while lacking assigned source texture.
- Exact scoped change: make `chapter-writer.md` a compact generic method/craft
  contract and assemble only it + authoritative commission + previous chapter.
  Preserve current H-F01 craft/style rules exactly; do not add a style amendment,
  raw reference, judge feedback, full plan/style, or unassigned packet.
- Likely files: `prompts/chapter-writer.md`, `scripts/loop/run_iteration.py`,
  `scripts/eval/tests/test_pipeline_contract.py` or focused runtime tests.
- Acceptance: captured writer input contains exactly three permitted inputs,
  resolves no plan IDs, fails on missing/blocked commission, and preserves API
  chapter/spec-gap output handling; the full style guide remains available to
  planners and editorial reviewers but never enters the writer call.
- Verification: exact-input tests, `bash scripts/check.sh`.
- Dependencies: RF-09.
- Implementation attempts: `4`; latest: 2026-07-14
  `/root/rf10_writer_context_owner` — registering manual authority as declared
  operation metadata in a durable `WRITER_HANDOFF` transition, binding the full
  pre-handoff pair inventory with exact selected-draft exemptions, and proving
  the real seal/verify/promotion path without promoting the receipt; 13/13
  focused, 54/54 affected, and 188/188 full tests pass with strict OpenSpec,
  diff, compile, and size gates (shellcheck unavailable).
- Review attempts: `4`.
  - Review 1: `NEEDS CHANGES` — mutable authority could be reread after
    eligibility; the compact contract omitted the one-mantra minimum; descending
    unique selections reached commission validation.
  - Review 2: `NEEDS CHANGES` — the final model callback could mutate authority
    before its output was written; manual handoff authority was not persisted
    and replay-verified before sealing.
  - Review 3: `NEEDS CHANGES` — the receipt was undeclared at real seal; handoff
    provenance could be downgraded by deleting the receipt/token; only contract,
    commissions, and audit—not the complete pair inventory with
    selected-draft-only exemptions—were replay-bound.
  - Review 4: `PASS` — no findings; 49/49 affected and 188/188 full tests,
    strict OpenSpec, diff, compile, and size gates pass.
- Commit / push: accepted subject
  `feat(writing): enforce commission-only writer context`; exact SHA
  `eb8e8ece668101763651e497bedd14a50a848e0d`.

### RF-11 — Freeze complete first-draft batches before review

- [x] Snapshot all selected drafts before any review or revision.
- Status: `DONE`
- Evidence class / report: retained operating lesson; §§6 item 8, 7 stages 5–7,
  10.
- Problem / root cause: chapter-by-chapter review can mutate context and hide the
  original batch needed for causal comparison.
- Exact scoped change: generate selected chapters in order for previous-chapter
  continuity, then immutable-snapshot the complete batch; reject early review,
  overwrite, or partial-batch evaluation.
- Likely files: `scripts/loop/run_iteration.py`, snapshot helpers/tests under
  `scripts/loop/` and `scripts/eval/tests/`.
- Acceptance: reviewers cannot start before all hashes exist; later repairs do
  not alter frozen first drafts; interrupted generation resumes without mixing
  configurations.
- Verification: batch state-machine fixtures, `bash scripts/check.sh`.
- Dependencies: RF-02, RF-10.
- Implementation attempts: `4`; latest: 2026-07-15
  `/root/rf11_draft_batch_owner` — final accepted-root lifecycle reads now
  require exact canonical mode `0444`, while atomic staging reads retain their
  distinct owner/safety handling so pending recovery remains replayable.
  Regressions reject `0644`, `0400`, and `0440` anchors in both `NEVER_STARTED`
  and `STARTED/COMMITTED` through load, seal, verify, and recovery paths; all
  transition-kill recoveries end at `0444`. Dedicated RF-11 tests pass 18/18,
  the affected RF-02/RF-10/RF-11 suite passes 72/72, and the 206/206 full
  repository gate, strict OpenSpec, diff, compile, and size gates pass
  (shellcheck unavailable).
- Review attempts: `4`.
  - Review 1: `NEEDS CHANGES` — an accepted model callback could be repeated
    across crash windows because response bytes were not durably bound before
    return; batch start could be downgraded into generic RF-02 handling by
    removing its batch metadata; frozen evidence accepted non-writable modes
    instead of requiring exact canonical `0444`.
  - Review 2: `NEEDS CHANGES` — after partial progress, deleting the complete
    first-draft evidence and clearing batch/start metadata could downgrade a
    manual operation to `WRITER_HANDOFF` or an API operation to `CANDIDATE`,
    restoring generic RF-02 seal, verify, and recovery semantics because no
    durable lifecycle anchor outside candidate-local state remembered start.
  - Review 3: `NEEDS CHANGES` — final lifecycle anchors were content- and
    owner-checked but did not require exact canonical mode `0444`, so altered
    `0644`, `0400`, or `0440` anchors remained readable as valid operation
    authority.
  - Review 4: `PASS` — no findings; 18/18 dedicated, 78/78 affected, and
    206/206 full tests, strict OpenSpec, diff, compile, and size gates pass.
- Commit / push: accepted subject
  `feat(writing): freeze complete first-draft batches`; exact SHA
  `405bc7b33f4e3da1e16f130bb23e388625a9fa84`.

### RF-12 — Implement blocking grounded review

- [x] Separate truth/safety/ownership audit from literary development.
- Status: `DONE`
- Evidence class / report: demonstrated reviewer sight gap; §§5 cause 4, 7
  action 2, 8.
- Problem / root cause: the current source-blind reviewer is asked to verify
  evidence and may pass unresolved blockers after two cycles.
- Exact scoped change: add a fresh grounded-review prompt/input contract for
  draft + commission + assigned packets + evidence/safety rules; output exact
  source locators and owning stage; source, safety, originality, and ownership
  blockers cannot be waived by cycle cap. Use a strong reviewer family distinct
  from the writer.
- Likely files: new focused prompt under `prompts/`, review orchestration, tests.
- Acceptance: fixtures catch invention, inference broadening, packet conflict,
  safety breach, and owner leakage; clean grounded chapter passes; unresolved
  blocker stops product evaluation.
- Verification: grounded-review contract fixtures, `bash scripts/check.sh`.
- Dependencies: RF-08, RF-09, RF-11.
- Implementation attempts: `4`; latest: 2026-07-15
  `/root/rf12_grounded_review_owner` — preserved every prior closure and upgraded
  the H-F04 receipt to schema 2, binding each canonical summary's local device,
  inode, and single-link identity alongside its path, bytes, mode, control role,
  replica identities, and complete instrument configuration. Product preflight
  validates the receipt-bound identity before reading either control summary, so
  a byte-identical atomic replacement has zero downstream side effects and cannot
  regenerate authority outside constrained H-F04 finalization. Verification:
  12/12 focused, 62/62 affected, and 229/229 full tests; canonical gate, strict
  OpenSpec, compile, structural, diff, and file-size checks pass.
- Review attempts: `4`.
  - Review 1: `NEEDS CHANGES` — whole-packet leakage, incomplete replay identity,
    non-durable callback dispatch, free-text finding routes, and an unguarded
    `judge_panel.py` product route. All five were closed in attempt 2.
  - Review 2: `NEEDS CHANGES` — product mode accepted arbitrary self-described
    control summaries, including external and synthetic files, and validated them
    only after product reads and output creation. Attempt 3 derives only the
    receipt-bound canonical H-F04 authority and rejects unsafe or stale evidence
    with zero product side effects.
  - Review 3: `NEEDS CHANGES` — the receipt bound summary paths, bytes, hashes,
    modes, roles, and configuration but not stable local file identity, allowing a
    byte-identical single-link `0444` inode replacement after finalization.
    Attempt 4 binds and prechecks device/inode/link identity.
  - Review 4: `PASS` — no findings; 12/12 focused, 62/62 affected, and 229/229
    full tests, strict OpenSpec, diff, compile, and size gates pass.
- Commit / push: accepted subject
  `feat(review): enforce blocking grounded review`; exact SHA
  `36dd57b2d4ab5c244b1e82a4147f4a566254223a`.

### RF-13 — Implement reference-blind whole-opening developmental review

- [x] Judge the frozen sequence against planned reader states.
- Status: `DONE`
- Evidence class / report: supported remedy; §§3, 5 cause 4, 7 action 2.
- Problem / root cause: current review is chapter-local and checklist-heavy, so
  repeated modes, weak cumulative movement, and deferred transformation survive.
- Exact scoped change: add a separate fresh reviewer that sees the complete
  selected batch plus reader-state cards/commissions, no reference or history,
  and reports failed transitions, specificity, emotional movement, variation,
  continuity, and exact stage owner. Use a strong reviewer family distinct from
  the writer and grounded-review context.
- Likely files: new focused prompt under `prompts/`, orchestration, tests.
- Acceptance: fixture identifies scope→trap→inventory as a sequence failure even
  when chapters are locally adequate; does not audit source claims without need;
  output is owner-routable and compact.
- Verification: developmental-review fixtures, `bash scripts/check.sh`.
- Dependencies: RF-11.
- Implementation attempts: `6`; latest: 2026-07-15
  `/root/rf13_developmental_review_owner` — retained the valid writing-owned
  repeated-cadence case and added a separate exact scope→trap→inventory
  acceptance fixture. Its three distinct commissions and 805–809-word drafts
  are token-valid and locally enact their own authoritative transitions, while
  their cards explicitly move only from mapping scope, to naming a trap, to a
  catalogue reserved for later demolition. The complete opening therefore
  fails truthfully as a planning-owned deferred-transformation sequence through
  the captured native wrapper; exact spans, task inputs, forbidden-content
  isolation, and route are asserted. Verification: 17/17 dedicated, 65/65
  affected, and 246/246 full tests pass; strict OpenSpec, compile, diff,
  whitespace, and file-size gates pass (shellcheck unavailable).
- Review attempts: `6`.
  - Review 1: `NEEDS CHANGES` — (1) the native reviewer ran from candidate-local
    state, exposed experiment paths, and did not prove rejection of every tool
    event or a sanitized transport; (2) RF-13 lacked a non-downgradable
    accepted-root lifecycle binding operation/generation/task/call/transport/raw/
    receipt authority into recovery, sealing, and deletion/tamper checks; (3)
    synthetic token fixtures did not prove the real three-chapter
    scope→trap→inventory failure or a cumulative clean sequence through the native
    wrapper; (4) findings did not require one exact meaningful span per affected
    chapter or reject duplicate semantic findings, chapters, and transitions.
    Attempt 2 closes all four findings.
  - Review 2: `NEEDS CHANGES` — (1) runtime inventory covered files but not every
    directory entry, so undeclared empty or nested directories and their exact
    structure were not validated; (2) the semantic chapters repeated one common
    padding paragraph and therefore did not demonstrate genuinely distinct,
    locally adequate scope→trap→inventory and cumulative-control prose. Attempt
    3 closes both findings; independent rereview remains pending.
  - Review 3: `NEEDS CHANGES` — C-01, C-02, and C-03 changed only target/source
    identity while inheriting the same C-01 no-prior premise, entering/leaving
    belief, and handoff. That made the purported clean cumulative PASS and stalled
    sequence failure internally non-authoritative. Attempt 4 supplies and checks
    a distinct cumulative commission set; independent rereview remains pending.
  - Review 4: `NEEDS CHANGES` — (1) all six semantic drafts omitted their own
    assigned frozen token, so the writer contract and mocked grounded/developmental
    passes were internally invalid; (2) the stalled chapters did not enact their
    own commissions, making the failure chapter-local and falsely planning-owned
    rather than a genuine whole-sequence defect. Attempt 5 enforces exact token
    fidelity and locally complete chapters whose repeated execution is a
    writing-owned cumulative failure; independent rereview remains pending.
  - Review 5: `NEEDS CHANGES` — the repeated-cadence case was valid but replaced,
    rather than proved, RF-13's recorded scope→trap→inventory acceptance case.
    Attempt 6 retains that regression and adds the exact separate executable
    scenario: locally adequate chapters faithfully execute defective cards whose
    complete opening defers transformation, so the earliest truthful owner is
    planning; independent rereview remains pending.
  - Review 6: `PASS` — independent normal review returned no findings; the exact
    scope→trap→inventory acceptance case, retained repeated-cadence regression,
    native task isolation, lifecycle/runtime durability, and truthful owner
    routing were accepted.
- Commit / push: accepted subject
  `feat(review): enforce whole-opening developmental review`; exact SHA deferred
  until the root agent creates the commit.

### RF-14 — Route defects to the earliest owning stage

- [x] Replace `SPEC GAP:`-only routing and broaden all owner labels.
- Status: `DONE`
- Evidence class / report: demonstrated intelligence loss; §§4 chains 1–4,
  5 cause 4, 7 actions 2–3.
- Problem / root cause: detected plan/research/context defects are translated
  into prose rules or proceed because only a writer marker triggers upstream work.
- Exact scoped change: define and enforce owners `brief`, `research/synthesis`,
  `framing`, `plan`, `commission/context`, `prose`, `revision`, `evaluation`;
  route reviewer and judge findings to the earliest owner; invalidate only
  downstream artifacts.
- Likely files: review prompts, `scripts/loop/run_iteration.py`,
  `scripts/loop/judges.py`, `PROGRAM.md` later finalized in RF-19, tests.
- Acceptance: fixtures route catalogue to plan, missing support to research,
  packet leakage to commission, wording defect to prose; no grounded blocker
  advances and no unrelated artifact regenerates.
- Verification: routing/invalidation tests, `bash scripts/check.sh`.
- Dependencies: RF-12, RF-13.
- Implementation attempts: `3`; final verification: focused 20/20, affected
  110/110, full 257/257; strict OpenSpec, diff, compile, and size gates pass.
  - Attempt 1: established the canonical eight-owner vocabulary, receipt-bound
    reviewer/judge routes, and exact owner-plus-downstream regeneration scope.
  - Attempt 2: made API/manual writer refusals durable and routed judges from all
    parsed findings before the top-five presentation cutoff.
  - Attempt 3: enforced one canonical refusal serialization and added the
    hash-bound monotonic operation-level refusal anchor.
- Review attempts: `3`.
  - Review 1: `NEEDS_CHANGES` — the live writer refusal was not a durable
    resumable route, and judge routing ignored upstream findings below the
    top-five display cutoff.
  - Review 2: `NEEDS_CHANGES` — refusal JSON accepted noncanonical
    serializations, and coordinated descriptor/evidence deletion could remove
    the terminal writer route.
  - Review 3: `PASS` — independent normal review returned no findings.
- Commit / push: accepted subject
  `feat(routing): route defects to earliest owner`; exact SHA deferred until the
  root agent creates the commit.

### RF-15 — Add defect-scoped repair and editorial escalation

- [ ] Repair accepted prose defects without whole-artifact resampling.
- Status: `TODO`
- Evidence class / report: hypothesis H-F03 and retained lesson; §§5 cause 4,
  7 stage 7, 9 H-F03.
- Problem / root cause: current revisions mix integrity, plan, and prose defects;
  failures can resample the chapter or silently proceed.
- Exact scoped change: original writer receives frozen draft + prose-owned defect
  list for one scoped repair; upstream findings return upstream; only one failed
  targeted repair permits a distinct editorial synthesis pass; preserve before/
  after diffs and introduce no unrelated rewrite.
- Likely files: `prompts/chapter-writer.md` revision mode or one small revision
  prompt, review orchestration, tests.
- Acceptance: repair fixture changes only named spans/defects, introduces no new
  grounded failure, and escalates exactly once; no automatic full rewrite.
- Verification: repair-flow fixtures, `bash scripts/check.sh`.
- Dependencies: RF-12, RF-13, RF-14.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.

## Phase 3 — align evaluation and experiment governance

### RF-16 — Add blind chapter-effect and whole-opening instruments

- [ ] Measure belief transition and cumulative sequence directly.
- Status: `TODO`
- Evidence class / report: supported generalization, instrument unvalidated;
  §§5 cause 5, 7 action 3, 9 H-F04.
- Problem / root cause: six Carr-distance craft dimensions omit explicit
  before/after belief, subject specificity, mechanism credibility, and opening
  coherence.
- Exact scoped change: add one compact blind product-effect rubric with chapter
  and sequence modes; require entering/leave belief, enacted discovery,
  specificity, credibility, emotion, escalation, and handoff; condition labels,
  provenance, scores, and history stay hidden. H-F04 may submit reference prose
  only as an anonymous candidate with identity and ground-truth context hidden;
  ordinary product evaluation receives no reference prose.
- Likely files: `calibration/judges/product-effect-rubric.md`,
  `scripts/loop/judges.py`, `scripts/loop/score.py`, tests.
- Acceptance: emits chapter pair tasks and whole-opening tasks; validates compact
  structured verdicts; cannot reveal treatment identity; anonymous H-F04 inputs
  are isolated and cannot flow into generation or promotion.
- Verification: prompt-blindness/schema tests, `bash scripts/check.sh`.
- Dependencies: RF-00.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.

### RF-17 — Separate integrity, effect, sequence, and craft decisions

- [ ] Demote Carr composite and non-mantra repetition to their proper roles.
- Status: `TODO`
- Evidence class / report: demonstrated proxy mismatch; §§5 cause 5, 7 action 3,
  8.
- Problem / root cause: one averaged likeness score and placeholder epsilon can
  override product effect; non-mantra 12-grams can null otherwise useful evidence.
- Exact scoped change: hard-gate source/safety/originality/method integrity;
  preserve the existing word-sequence near-copy tripwire against matched
  reference chapters as an isolated non-overridable hard gate;
  decide reader effect and sequence separately; run Carr rubric afterward as
  craft diagnosis; make non-mantra repetition a repair signal and retain exact
  assigned-mantra checking at chapter/publication acceptance; retain only loose
  length sanity rather than fine-grained prose metrics as a product gate.
- Likely files: `scripts/loop/score.py`, `scripts/loop/gate.py`,
  `calibration/judges/carr-likeness-rubric.md` only as necessary to label its
  diagnostic role, tests.
- Acceptance: likeness alone cannot promote; integrity failure always rejects;
  a near-copy tripwire failure always rejects; reference text remains isolated
  from generation and blind evaluators; repetition signal does not erase blind
  results; result object exposes all four layers without an averaged master
  reward; loose length sanity remains visible.
- Verification: decision-table tests, `bash scripts/check.sh`.
- Dependencies: RF-02, RF-16.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.

### RF-18 — Establish judge independence, owner routing, and variance bounds

- [ ] Make decisive evaluation independent enough to support promotion.
- Status: `TODO`
- Evidence class / report: demonstrated uncertainty; §§4 alternative
  explanations, 5 cause 5, 7 action 3.
- Problem / root cause: same-family `k=2`, unmeasured repeats, narrow asset tags,
  and placeholder epsilon make small score movements uninterpretable.
- Exact scoped change: support two fresh independent judge contexts and, where
  available, two model families or one family plus named human; broaden
  suggestion owners; measure repeat agreement/variance; remove epsilon from the
  new lineage rather than inventing a new threshold.
- Likely files: `scripts/loop/judges.py`, `loop/config.yaml`, result schemas,
  focused tests.
- Acceptance: independent task IDs and raw verdicts are preserved; owner labels
  cover every stage; disagreement comparable to effect yields `INCONCLUSIVE`,
  not promotion.
- Verification: aggregation/disagreement fixtures, `bash scripts/check.sh`.
- Dependencies: RF-14, RF-16, RF-17.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.

### RF-19 — Replace the one-asset PROGRAM with a causal-bundle run contract

- [ ] Start a new minimal results lineage governed by one hypothesis, not one file.
- Status: `TODO`
- Evidence class / report: critical demonstrated governance cause; §§1, 5 cause
  3, 7 action 3.
- Problem / root cause: the frozen one-asset loop prevents changes at the causal
  owner and records rejected product as current.
- Exact scoped change: rewrite the runbook for linked change sets, frozen
  variables, candidate isolation, batch/review/evaluation order, owner routing,
  falsification, and minimal records; create a new results lineage and never
  compare it numerically with old rewards; retain call discipline and root
  context protection.
- Likely files: `PROGRAM.md`, `loop/config.yaml`, new-lineage `loop/results.tsv`
  and `loop/learnings.md` handling, supporting tests.
- Acceptance: one dry-run record contains only hypothesis/chain, changes, frozen
  variables, input IDs, four evidence layers, decision, falsifier; no old reward
  comparison; no loop bureaucracy added.
- Verification: record-schema/dry-run tests, `bash scripts/check.sh`.
- Dependencies: RF-02, RF-11, RF-14, RF-17, RF-18.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.

## Phase 4 — validate instruments before billable generation

### RF-20 — Run H-F04 on frozen prose

- [ ] Calibrate the new product instrument without generating chapters.
- Status: `TODO`
- Evidence class / report: untested hypothesis H-F04; §§9 H-F04, 10.
- Problem / root cause: the new rubric cannot govern H-F01 merely because its
  fields look aligned with the vision.
- Exact scoped change: recover frozen complete iter-004 and iter-007 Chapters
  1–3 plus matched references inside fresh prose-reading agents; submit each
  matched reference only as an anonymous candidate with provenance hidden; score
  blind chapter effect and whole-opening sequence, then assess agreement, high
  reference ceiling, and whether safety strengths remain separate from effect.
- Likely files: isolated experiment outputs under the new lineage; no production
  prose, prompts, or references committed.
- Acceptance: repeat agreement is adequate for the predeclared decision rule;
  reference establishes a strong sequence ceiling; high disagreement produces
  an instrument revision task rather than a product run; calibration artifacts
  cannot promote or enter any generation context.
- Verification: raw verdict completeness, independent calibration review,
  `bash scripts/check.sh`.
- Dependencies: RF-16, RF-17, RF-18, RF-19.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.

## Phase 5 — H-F01 bounded control/treatment experiment

### RF-21 — Build and accept the quit-sugar treatment reader journey

- [ ] Complete the brief, framing, first-three cards, and blocking plan review.
- Status: `TODO`
- Evidence class / report: H-F01 treatment, not a proven improvement; §§7
  action 1, 9 H-F01, 10.
- Problem / root cause: current opening is scope → trap label → benefit catalogue.
- Exact scoped change: using existing accepted research only, complete the
  primary/subordinate beliefs; design three distinct reader transitions; revise
  only causally required first-three plan material; remove J-01–J-22 prospectus;
  preserve fixed background unless invalidated; use a native high-reasoning plan
  writer and independent cross-family plan reviewer; obtain `fit to write from`.
- Likely files: candidate copies of
  `production-books/quit-sugar/{00-brief.md,framing.md,master-plan.md,master-plan-review.md}`
  inside the isolated treatment snapshot established by RF-02.
- Acceptance: distinct entering/leaving belief and sugar-specific encounter per
  chapter; no primary work deferred; no adjacent duplicate mode; blind card-only
  reader can describe cumulative transformation; plan verdict is fit; accepted
  production plan and chapters remain byte-identical before promotion.
- Verification: independent plan review and reader-state matrix; no root prose
  reading; `bash scripts/check.sh`.
- Dependencies: RF-01, RF-02, RF-03, RF-05, RF-06, RF-07, RF-19, RF-20.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.

### RF-22 — Generate and audit the three H-F01 treatment commissions

- [ ] Produce a clean, self-sufficient commission set before writing.
- Status: `TODO`
- Evidence class / report: H-F01 treatment; §§7 action 2, 8, 10.
- Problem / root cause: treatment cannot test context transport without an
  audited assigned-packet handoff; commissions alone previously invented.
- Exact scoped change: generate Chapter 1–3 commissions from accepted treatment
  plan and only assigned existing packets; independently audit them together for
  source grounding, no unresolved IDs, ownership, state handoffs, limits, and no
  mini-plan/prose.
- Likely files: isolated
  `production-books/quit-sugar/commissions/chapter-{01,02,03}.md` treatment
  artifacts and audit output.
- Acceptance: all three pass; any conflict returns to its owner and regenerates
  only invalidated commissions; `COMMISSION BLOCKED` stops RF-23.
- Verification: packet-to-commission trace matrix by fresh agents,
  `bash scripts/check.sh`.
- Dependencies: RF-08, RF-09, RF-21.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.

### RF-23 — Generate fresh frozen control and treatment batches

- [ ] Produce all six first drafts under fixed model and research conditions.
- Status: `TODO`
- Evidence class / report: H-F01 experiment execution; §10.
- Problem / root cause: historical-vs-fresh comparison would confound the handoff
  treatment with generation variance.
- Exact scoped change: generate fresh control Chapters 1–3 using current plan +
  full-plan runtime and fresh treatment Chapters 1–3 using accepted commissions;
  same Opus 4.6, reasoning disabled, temperature 0.7, output budget, source
  corpus, safety rules, approximate word budgets; freeze all six before review.
- Likely files: isolated experiment snapshots under `loop/`; production chapters
  remain unchanged.
- Acceptance: exact input/config hashes; no reference/revision/judge feedback;
  complete immutable batches; the total H-F01 path RF-21–RF-25 stays within the
  declared 40-call ceiling.
- Verification: snapshot hashes and context-capture audit by fresh agents,
  `bash scripts/check.sh`.
- Dependencies: RF-02, RF-10, RF-11, RF-22. External dependency:
  working `OPENROUTER_API_KEY` with sufficient credit.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.

### RF-24 — Ground-audit all six H-F01 drafts

- [ ] Enforce integrity before any preference or craft evaluation.
- Status: `TODO`
- Evidence class / report: H-F01 hard gate; §§7 action 2, 10.
- Problem / root cause: exciting but invented treatment prose would produce a
  false success, as retired commission runs demonstrated.
- Exact scoped change: fresh grounded agents audit each frozen draft against its
  own assigned authority, source packets, safety, originality, non-shaming, and
  no-willpower requirements; run the existing isolated word-sequence near-copy
  checker against each matched reference without exposing reference text to the
  agents; do not revise first drafts.
- Likely files: isolated grounded verdicts and compact trace matrices only.
- Acceptance: all three treatment drafts pass; any material treatment integrity
  or near-copy failure is decisive H-F01 failure; unsupported empirical/mechanism
  claims do not increase relative to control; near-copy results are recorded for
  all six drafts and cannot be overridden by later votes.
- Verification: six complete grounded verdicts, cross-agent audit review,
  `bash scripts/check.sh`.
- Dependencies: RF-12, RF-23.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.

### RF-25 — Decide H-F01 blindly, diagnose craft, and promote atomically

- [ ] Run the decisive comparison and record support/refutation/inconclusive.
- Status: `TODO`
- Evidence class / report: H-F01 decisive test; §§9–10.
- Problem / root cause: the planning/context hypothesis needs a same-run product
  decision, not another prompt-quality judgment.
- Exact scoped change: two blind votes per matched chapter; two blind
  whole-opening comparisons; freeze results; then run reference-sighted Carr
  craft diagnosis; founder/named human directly reads winning and losing
  openings; root receives compact verdict only; promote config+product together
  only on full success.
- Likely files: isolated verdicts, new-lineage result/learnings row, atomic gate
  snapshot; current production only changes on accepted promotion.
- Acceptance: treatment integrity passes, wins at least 5/6 chapter votes and
  both sequence votes, readers identify three distinct state changes/discoveries,
  no setup/catalogue primary job, no increased unsupported claims, and founder/
  human confirms. Three-or-fewer votes, no sequence win, or integrity failure is
  failure; large disagreement is inconclusive. Interpret mixed outcomes by
  owner: specificity without belief effect weakens transport; effect with
  evidence regression indicts commission/audit; faithful no-difference triggers
  RF-29 rather than another wording amendment.
- Verification: independent result auditor recomputes decision from raw verdicts
  and hashes; reference never leaked upstream; `bash scripts/check.sh`.
- Dependencies: RF-13, RF-16, RF-17, RF-18, RF-19, RF-24.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.

## Phase 6 — causal follow-ups and generalization

### RF-26 — Run H-F02 planning-only ablation when informative

- [ ] Isolate reader-state planning from commission/context transport.
- Status: `CONDITIONAL`
- Evidence class / report: untested H-F02; §9 H-F02.
- Problem / root cause: H-F01 bundles the two strongest linked causes and may not
  reveal which produced improvement.
- Exact scoped change: with same research/model, compare revised reader-state
  plan under current full-plan writer runtime against fresh current-plan control.
- Likely files: isolated experiment snapshots and verdicts; no accepted config
  changes without the standard gate.
- Acceptance: trigger only if H-F01 supports the bundle but causal attribution
  matters or budget requires the cheaper ablation; use the same integrity/effect/
  sequence decision layers.
- Verification: preregistered frozen variables in minimal run record, independent
  result audit, `bash scripts/check.sh`.
- Dependencies: RF-25 outcome.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.

### RF-27 — Run H-F03 revision-flow A/B

- [ ] Compare current general rewrite with grounded/developmental scoped repair.
- Status: `CONDITIONAL`
- Evidence class / report: untested H-F03; §§7 stage 7, 9 H-F03.
- Problem / root cause: better first drafts do not prove the new repair flow
  resolves more blockers with fewer regressions.
- Exact scoped change: copy one frozen accepted-authority batch; apply current
  general reviewer/rewrite to control and split review + defect-scoped repair to
  treatment; audit and compare blind.
- Likely files: isolated revision experiment snapshots/verdicts.
- Acceptance: treatment resolves more named blockers with smaller diffs, no new
  grounded defects, and no loss of energy/specificity; otherwise reject or revise
  the repair design.
- Verification: before/after defect and regression matrices, independent result
  audit, `bash scripts/check.sh`.
- Dependencies: RF-15, RF-25; requires an integrity-passing frozen batch.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.

### RF-28 — Test intentional chapter-anatomy variation

- [ ] Remove identical visible anatomy only as its own post-H-F01 hypothesis.
- Status: `CONDITIONAL`
- Evidence class / report: secondary cause, not established primary cause; §§3,
  5 cause 7, 7 action 1, 8.
- Problem / root cause: mandatory preview–thesis–instruction–summary anatomy may
  flatten modes, but changing it during H-F01 would confound the handoff test.
- Exact scoped change: after H-F01, and only with recorded founder approval,
  allow semantic chapter needs to vary visible anatomy while retaining clarity,
  mantras/instructions where assigned, and method integrity; no broad style
  rewrite.
- Likely files: `prompts/style-guide.md`, `prompts/chapter-writer.md`, focused
  reviewer rules/tests.
- Acceptance: founder approval is recorded before edit; paired test shows greater
  mode variation without loss of transition, continuity, or integrity; otherwise
  revert. H-F01 style bytes remain frozen through RF-25.
- Verification: focused diff, paired blind review, `bash scripts/check.sh`.
- Dependencies: RF-25 and explicit founder approval.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.

### RF-29 — Compare writer models only if the repaired handoff is insufficient

- [ ] Test writer prior after upstream fidelity is demonstrated.
- Status: `CONDITIONAL`
- Evidence class / report: unresolved assumption; §§7 unresolved assumptions,
  8 conclusions weakened, 10 failure interpretation.
- Problem / root cause: retired runs show Opus invention, but changing models
  before H-F01 would confound planning and transport.
- Exact scoped change: trigger only if treatment cards/commissions are faithful
  yet product remains generic, preparatory, or invented; compare writer models on
  identical accepted commissions/settings as far as model APIs allow.
- Likely files: isolated model-comparison snapshots/records; model config changes
  only after accepted result.
- Acceptance: same inputs, grounded audits, blind product evaluation, and no
  reference leakage; no “best model” claim from a single unreplicated chapter.
- Verification: input-equivalence audit and independent result review,
  `bash scripts/check.sh`.
- Dependencies: RF-25 failure analysis.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.

### RF-30 — Validate transfer on two contrasting subjects

- [ ] Test compulsive smartphone checking and fear of flying openings.
- Status: `TODO`
- Evidence class / report: unresolved cross-subject assumption; §§7–9.
- Problem / root cause: sugar consumption cannot establish reliability for
  continuous digital cues and episodic non-consumption fear.
- Exact scoped change: after sugar success, run three-chapter openings through
  the accepted factory for smartphone checking and fear of flying, with new
  subject-specific research and no sugar/addiction category transplant.
- Likely files: new `production-books/<slug>/` workshops and isolated experiment
  records under existing stable paths.
- Acceptance: both pass subject contract, grounding, distinct reader transitions,
  whole-opening sequence, originality/safety, and founder/human reading; generic
  prompts contain no sugar-only constructs.
- Verification: cross-subject evidence matrices by fresh agents, standard gates,
  `bash scripts/check.sh`.
- Dependencies: RF-25 success and any causally required RF-26–RF-29 result.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.

### RF-31 — Pass the complete-book readiness gate and close the change

- [ ] Demonstrate whole-book coherence before claiming the factory vision.
- Status: `TODO`
- Evidence class / report: unresolved whole-book assumption; §§2, 7 unresolved
  assumptions, 9–10.
- Problem / root cause: three openings cannot prove 60,000-word coherence,
  mantra/repetition value, final editorial quality, or founder-free publishability.
- Exact scoped change: generate at least one complete book through the accepted
  flow; grounded-audit all chapters, developmental-review whole-book state and
  emotional sequence, validate mantra/repetition complexity, run blind sampled
  effect plus reference-sighted diagnostic, keep traceability machine-facing and
  produce source notes/end matter without evidence-process narration in the
  voice, and require founder publication review. Archive this OpenSpec change
  only after implemented scenarios pass.
- Likely files: accepted production book, reviews/evaluation records, OpenSpec
  specs on archive; no published artifact mutates in place.
- Acceptance: coherent complete book, all integrity gates green, no unresolved
  owner defects, founder says it is publishable without manual chapter rescue,
  contrasting-subject evidence remains valid, and `openspec verify/archive`
  workflow passes.
- Verification: independent whole-book agents return compact matrices; founder
  direct-reading verdict; `openspec validate redesign-book-factory --strict`;
  `bash scripts/check.sh`.
- Dependencies: RF-27 as applicable, RF-28 as applicable, RF-30.
- Implementation attempts: `0`; latest: `—`.
- Review attempts: `0`; latest verdict / findings: `—`.
- Commit / push: `—`.
