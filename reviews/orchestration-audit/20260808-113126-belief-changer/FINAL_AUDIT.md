# Agent orchestration audit — Belief-changer factory (research + book-writing stages)

## Report header

- **Repository:** Belief-changer (/home/kab/Belief-changer)
- **Branch / revision:** main @ f9ceda5
- **Audit run:** 20260808-113126-belief-changer
- **Audit root:** `reviews/orchestration-audit/20260808-113126-belief-changer/`
- **Review date:** 2026-08-08
- **Lead auditor:** Codex coding agent (this session)
- **Skill:** agent-orchestration-auditor v1.3.0 (cloned from keyclaw6/agent-orchestration-quality-skills, /tmp/aog-skills-mqOugl)
- **Source integrity:** baseline clean; run wrote only the audit root (verified pre-commit, see §17)
- **Planned audit commit:** `audit(orchestration): 20260808-113126-belief-changer`
- **Overall conclusion:** **MATERIALLY AT RISK — not launch-ready.** 8 accepted findings: 4 HIGH (F-01..F-04), 4 MEDIUM (F-05..F-08). The factory's core review loop (plan-writer ⇄ plan-reviewer until "fit to write from") is not realizable as written, and the research stage's miner output contract is undefined. The chapter-writing stage itself is the healthiest surface and completes.

## Executive summary

The factory after the founder's simplification is structurally much closer to the target — zero deterministic validation, every role a spawned pi sub-agent, prompts as the only machinery, no commissioner/evidence-editor/framing residue in the live pipeline, and the route split (Command Code proxy vs OpenAI subscription) is consistent across AGENTS.md, PROGRAM, HANDOFF, config, and every `.pi` pin. The chapter-writing stage (W3) is coherent end to end: exact four inputs, refusal protocol, sequential rolling window.

But the system is not ready to run for real. The most serious defect is in planning: the plan-review revision loop cannot legally hand the plan and the reviewer's blockers back to the plan-writer — the writer's exact-input contract forbids any context beyond four files, so the first "needs changes first" verdict blocks the pipeline with no defined recovery. The research stage has an undefined miner write-target contract ("the ten banks on disk" vs per-URL source packets), a concurrent-write integrity hole, and a Reddit requirement that directly contradicts the active rights gate. The loop's own calibration premise is compromised: `loop/config.yaml` declares writer reasoning `high` and temperature `0.7` as sole authority, but the pi sub-agent spawn path cannot pass either value — a hypothesis that changes them cannot actually be tested. Stale chapter-reviewer instructions remain actionable for operators.

Healthy: route/model pins match config for all roles; the runbook's retry/escalation boundary for transport failures is explicit; unlimited depth is coherent everywhere; zero deterministic validation holds (no validator remains); the plan-writer's 4-input and chapter-writer's 4-input boundary contracts are explicit.

## 1. Scope and method

- **In scope:** research stage (research-agent.md, researcher.md, web_tools.py, sources/README.md, config research fields, round-1 history as residue evidence) and book-writing stage (master-plan-skill-v2, master-plan-reviewer-v2, chapter-writer, .pi wrappers, style-guide as loaded craft contract, PROGRAM §1/§3, config writer/planner fields, templates, production-books/README), plus cross-system authority/handoff and the pi spawn runtime.
- **Out of scope (consumers only, referenced):** judges, trace-analyzer, hypothesizer, loop/judges/*, loop/prompts/*; `scripts/check.sh`/`validate_repo.py` verified working (exit 0) as repo-health gates; `daemon.sh`/`queue_runner.sh` (documented optional VPS machinery); `calibration/` + archived preflight (history); `_rounds/round-1/` (seed history).
- **Method:** per agent-orchestration-auditor SKILL.md: source-of-truth map → system map → entity atomization → GPT-5.6 Terra medium reviewer fan-out (8 wave-1 reviewers incl. two dry-run simulators) → 3 isolated ambiguity interpreters → skeptical verifier → coverage closer → lead adjudication → this report.
- **Read-only:** no files outside the audit root written; no services called; no credentials exercised; no model calls.

## 2. Source-of-truth hierarchy

Declared chain: docs/VISION.md Part I → docs/BOOK-FACTORY-VISION.md → docs/AUTO-TUNING-LOOP.md → loop/PROGRAM.md (sole operational runbook) → loop/config.yaml (sole route/model/parameter authority; nothing overrides it) → prompts/.pi agents (implementation truth) → AGENTS.md (repo rules) → production-books (evidence). Historical material (calibration, analysis, archived preflight, round-1) excluded.

Unresolved authority: no general tie-breaker is declared for simultaneous activation of AGENTS.md rules, PROGRAM steps, and role prompts beyond config's parameter authority — this is where the Reddit (F-01) and xhigh (F-04) conflicts arise. Spec precedence was cross-verified by AOG-CONF-01 and AOG-BLOAT-01; a dedicated spec-archaeologist review was not run (limitation, §14).

## 3. System and role model

Orchestrator (pi coding agent session, MiniMax M3 in research phase via CC proxy) spawns one fresh sub-agent per role via the `subagent` tool: `researcher` (openai-sub gpt-5.6-luna:max; web_tools.py; writes packets/banks), `plan-writer` (commandcode Kimi-K3; 4 inputs → master-plan.md), `plan-reviewer` (commandcode gpt-5.6-luna; plan + 4 inputs → master-plan-review.md verdict), `chapter-writer` (commandcode meta/muse-spark-1.2-contributor; 4 inputs → chapter or refusal). Consumers: judge (openai-sub luna:high), trace-analyzer (openai-sub luna:high), hypothesizer (openai-sub sol:high). State ownership: research/ + plans + chapters + traces on the campaign branch. No role can recursively delegate (only the orchestrator holds `subagent`). See SYSTEM_MAP.md.

## 4. Reviewer work register

| Worker | Role | Assignment | Canonical specs read | Coverage | Output | Status |
|---|---|---|---|---|---|---|
| AOG-RES-01 | research entity reviewer | research stage surface | full set | 91 entities | workers/aog-res-01.md | PASS + C3 |
| AOG-PLAN-01 | planning entity reviewer | planning surface | full set | 52 entities | workers/aog-plan-01.md | PASS (xhigh dissent) |
| AOG-CHAP-01 | chapter-writing reviewer | writer surface + style guide | full set | 20 entities | workers/aog-chap-01.md | PASS + C4 |
| AOG-XSYS-01 | identity/boundary/authority | orchestrator + spawn runtime | full set | cross-role matrix | workers/aog-xs-01.md | C4, C9(→O-01), Q-01 |
| AOG-CONF-01 | instruction-conflict | all active layers | full set | layers | workers/aog-conf-01.md | C1, C4-part |
| AOG-BLOAT-01 | complexity/stale | inventories | full set | artifacts | workers/aog-bloat-01.md | C1, C8, C4-part |
| AOG-DRY-01 | dry-run W1 | research scenarios | full set | 5 traces | workers/aog-dry-01.md + dry-runs/w1 | C5, C6, C7 |
| AOG-DRY-02 | dry-run W2/W3 | planning + writing scenarios | full set | 6 traces | workers/aog-dry-02.md + dry-runs/w2,w3 | C2, O-01, C10 |
| AOG-AMB-01..03 | ambiguity interpreters (isolated) | E1-E4 | full set | 4 entities × 3 | workers/aog-amb-01..03.md | E1/E2/E3 material |
| AOG-VER-01 | skeptical verifier | all candidates | re-verified all | 10 candidates | workers/aog-ver-01.md | 8 ACCEPT, 2 REJECT |
| AOG-CLOSE-01 | coverage closer | audit-of-audit | full set | closure list | (verdict recorded) | NOT-READY → closed here |

## 5. Coverage

### Requirement coverage (16)

IMPLEMENTED 11 (R-001, R-003, R-005, R-007, R-008, R-009, R-011, R-012, R-013, R-015, R-016), PARTIAL 4 (R-004→F-06, R-006→F-02, R-010→F-04, R-014→O-04), CONFLICT 1 (R-002→F-01). Full ledger: coverage/REQUIREMENT_LEDGER.md.

### Entity coverage

Every behavior-bearing line in the in-scope surface is represented (grouped rows with exact anchors; full rows for authority-bearing candidates). Full ledger: coverage/ENTITY_LEDGER.md. Uncovered surface: none in scope; consumers (judges/trace/hypothesizer) declared out of scope.

### Workflow coverage

W1, W2, W3 each have terminal traces (happy + failure + edge) in dry-runs/. W4 (judges/trace/hypothesize) not simulated (out of scope, declared limitation).

## 6. Accepted findings

### F-01 — Research doctrine both requires and prohibits Reddit; no authorization path exists (HIGH, CONFIRMED-DEFECT)

- **Classification / severity / confidence:** CONFIRMED-DEFECT / HIGH / HIGH
- **Affected:** research lead + all researchers; research stage
- **Governing contract:** R-002; AGENTS.md:14; docs/AUTO-TUNING-LOOP.md:129
- **Evidence:** AGENTS.md:14 "must reach forums, Reddit..."; AUTO-TUNING-LOOP.md:129 "must go into forums, Reddit..."; prompts/research-agent.md:35 lists "Reddit and its reachable mirrors/archives" as target; :59-62 "Reddit is excluded without explicit Reddit authorization"; .pi/agents/researcher.md:24-25 repeats the exclusion
- **Mismatch:** a normal campaign has no explicit Reddit authorization; the founder-locked docs require Reddit reach, the active contracts prohibit it
- **Mechanism:** the lead cannot satisfy the mandate while obeying the rights gate; mirrors/archives are named but not declared equivalent to "must reach Reddit"; no process grants the authorization
- **Reachable scenario:** any research stage without a founder-issued authorization — i.e., every run today
- **Impact:** the required lived-experience lane is either skipped (fails the North Star) or the rights gate is violated; ambiguity panel confirmed two materially different readings
- **Cross-component:** completion criterion §7 (≥3 personas) does not itself require direct Reddit, so a mirror-only run can complete while arguably violating the mandate — unresolved by any higher source
- **Skeptical verification:** AOG-VER-01 ACCEPT ("mirrors do not literally satisfy the mandate")
- **Atomic next step:** declare whether authorized reachable Reddit mirrors/archives satisfy the "must reach Reddit" mandate, or define the authorization handoff (founder decision)
- **Acceptance test:** a research work order without direct-Reddit authorization has one unambiguous compliant source path
- **Shards:** aog-conf-01, aog-bloat-01, aog-amb-01..03 (E2), aog-ver-01

### F-02 — The plan-review revision loop is not realizable as written (HIGH, CONFIRMED-DEFECT)

- **Classification / severity / confidence:** CONFIRMED-DEFECT / HIGH / HIGH
- **Affected:** plan-writer, plan-reviewer, orchestrator; W2 planning
- **Governing contract:** R-005, R-006; PROGRAM.md:171-177 ("handing the plan back to the plan-writer until master-plan-review.md ends fit to write from")
- **Evidence:** prompts/master-plan-skill-v2.md:7-14 fixes the planning call to exactly four inputs and "no other context"; :143-150 "Resolve genuine blocking issues and re-dispatch a fresh reviewer, up to three cycles"; prompts/master-plan-reviewer-v2.md:98-109 "No review-cycle limit can waive a blocker"; PROGRAM.md:171-177
- **Mismatch:** after a `needs changes first` verdict, a fresh plan-writer call cannot legally receive the candidate plan or the reviewer's blockers (both are "other context"), and the plan is not among the four inputs; the 4th-cycle behavior contradicts across three sources
- **Mechanism:** the intended handoff actor (orchestrator) has no permitted payload; task-text and disk-read injections violate the exact-input contract (verified against spawn extension index.ts:294-330)
- **Reachable scenario:** every plan that needs a revision — the loop's primary design path
- **Impact:** W2 blocks at its first real revision; the founder's core "plan-writer looped against a reviewer until approved" design cannot execute as written
- **Cross-component:** ties into F-06 (scarcity→thin rejection) — both are orphaned handoff transitions
- **Skeptical verification:** AOG-VER-01 ACCEPT; ambiguity panel 3/3: continue-cycling is most likely but a hard-cap reading is plausible; no tie-breaker exists
- **Atomic next step:** define the revision-call contract — either allow the plan + review as revision inputs or move the review loop into the orchestrator's task context — and state the post-cycle-3 behavior (escalate vs continue)
- **Acceptance test:** a `needs changes first` verdict produces a compliant plan-writer revision call carrying the plan and blockers, and the gate re-runs until `fit to write from`
- **Shards:** aog-dry-02, aog-amb-01..03 (E3), aog-ver-01, aog-plan-01

### F-03 — Researcher sub-agents have no defined on-disk write target or format (HIGH, MATERIAL-RISK)

- **Classification / severity / confidence:** MATERIAL-RISK / HIGH / HIGH
- **Affected:** research orchestrator + researchers; W1; research→planning handoff
- **Governing contract:** R-003, R-004; SYSTEM_MAP research→planning boundary
- **Evidence:** prompts/research-agent.md:82-90 "returns its packets into the ten banks on disk (§5)"; :141-158 ten semantic banks but no files/schema; :212-218 only final syntheses + sources/; .pi/agents/researcher.md:9-10 "the exact output bank file to write"; :27-28 "Write every accepted packet into the assigned bank file (append, dedupe by source URL)"; sources/README.md:3-5 defines a packet as one file per URL under sources/
- **Mismatch:** miners are told to write "packets" to an unspecified bank file; the only concrete packet contract is per-URL files in sources/; the ambiguity panel diverged (aggregate bank files vs per-URL packets) — two competent readings with different file routing, cardinality, and state ownership
- **Mechanism:** a compliant lead cannot derive the promised exact bank-file path/format; runs can write incompatible artifacts, overwrite shared syntheses, or omit sources/ packets needed to validate exact quotes
- **Reachable scenario:** every research dispatch (PROGRAM.md:155-169)
- **Impact:** integration/audit against §6/§7 unreliable; planning can receive incomplete or prematurely-mutated syntheses
- **Skeptical verification:** AOG-VER-01 ACCEPT ("ten banks are semantic categories, not defined writable files; historic work orders show both packets and raw-bank lines, confirming the ambiguity")
- **Atomic next step:** define one explicit miner-write contract distinguishing per-source packets from bank entries, with a concrete non-conflicting target per dispatched work order
- **Acceptance test:** a fresh miner writes one valid sourced entry the lead can integrate and trace to a sources/ packet without editing a final synthesis
- **Shards:** aog-res-01, aog-amb-01..03 (E1), aog-ver-01

### F-04 — Config-declared parameters (reasoning, temperature) are not enforceable in the spawn path (HIGH, MATERIAL-RISK)

- **Classification / severity / confidence:** MATERIAL-RISK / HIGH / HIGH
- **Affected:** chapter-writer, plan-writer, plan-reviewer, research lead; campaign calibration provenance
- **Governing contract:** R-010; AGENTS.md:45-48; PROGRAM.md:37-39; founder route law (writer: reasoning high, temperature 0.7, no max_tokens)
- **Evidence:** loop/config.yaml:11-16 writer_reasoning: high + writer_temperature: 0.7; :64-65 plan_reviewer_reasoning: max; config comment :55 proxy accepts only low/medium/high/max; ~/.pi/agent/extensions/subagent/agents.ts:12-16,64-68 parses only tools+model; index.ts:294-327 invokes pi with only --model/--tools; .pi/agents/*.md pin model only (commandcode roles carry no reasoning suffix); no repo consumer reads writer_reasoning/writer_temperature; prompts/master-plan-skill-v2.md:143-145 additionally says "xhigh" while config says max
- **Mismatch:** config is declared the sole parameter authority, but the spawn path cannot pass reasoning or temperature; openai-sub roles enforce reasoning via the model-id suffix (:high/:max), CC roles (writer, planner, reviewer) cannot
- **Mechanism:** a config edit can claim a parameter change while spawned calls use pi/provider defaults; the run trace cannot prove the declared contract; temperature 0.7 (founder-locked) is never applied
- **Reachable scenario:** every writer/planner/reviewer spawn; any tuning iteration that hypothesizes a temperature or reasoning change
- **Impact:** invalidates causal attribution — the loop's core experiment cannot test what config claims to control; "xhigh" vs "max" is one symptom of the same unenforced-reasoning root
- **Skeptical verification:** AOG-VER-01 ACCEPT ("the standard spawned-role path supplies only model/tools/system prompt/task"; `:max` suffix covers the research miner only). AOG-PLAN-01's dissent (xhigh non-material) was overruled on the enforcement point, not the wording
- **Atomic next step:** either wire reasoning/temperature into the spawn path (extension or agent frontmatter) or remove the fields from the claimed authoritative config surface
- **Acceptance test:** changing writer_temperature/writer_reasoning changes the emitted request metadata; plan-reviewer reasoning is recorded as `max`
- **Shards:** aog-chap-01, aog-xs-01, aog-bloat-01, aog-conf-01, aog-ver-01

### F-05 — Concurrent researcher writes have no exclusivity or merge contract (MEDIUM, MATERIAL-RISK)

- **Classification / severity / confidence:** MATERIAL-RISK / MEDIUM / HIGH
- **Affected:** W1 parallel mining (up to 10)
- **Evidence:** research-agent.md:48-52,80-85; researcher.md:27-30 ("append, dedupe by URL"); sources/README.md:3-5 (same URL's packet enriched by repeated use)
- **Mechanism:** parallel read-dedupe-write can lose entries or corrupt packets; no lock, unique-writer, or merge protocol
- **Impact:** checkpoint guarantee (HANDOFF hard-won lesson 3) unenforceable under concurrency
- **Skeptical verification:** AOG-VER-01 ACCEPT
- **Atomic next step:** assign each bank/packet a unique owning work order (or an append-atomic write rule) before re-running parallel mining
- **Acceptance test:** two concurrent miners on adjacent work orders produce a loss-free, dedupe-correct bank
- **Shards:** aog-dry-01, aog-ver-01

### F-06 — "Genuine scarcity" termination can be rejected as thin downstream with no return path (MEDIUM, MATERIAL-RISK)

- **Classification / severity / confidence:** MATERIAL-RISK / MEDIUM / HIGH
- **Affected:** research lead → plan-writer handoff
- **Evidence:** research-agent.md:41-45,189-194 (scarcity endpoint, lead decides); master-plan-skill-v2.md:7-14 (plan-writer stops on thin input); PROGRAM.md:171-177 (no return-to-research transition)
- **Mechanism:** the lead may document scarcity and synthesize, but the mandatory next consumer must stop on thin input; neither operator nor founder is named as the scarcity decider; INCONCLUSIVE covers role/transport failure, not this contract conflict
- **Impact:** a blocked transition between the two stages with no defined recovery
- **Skeptical verification:** AOG-VER-01 ACCEPT
- **Atomic next step:** define the scarcity→thin-input transition (escalate to founder/operator or return to research)
- **Acceptance test:** a scarcity-marked synthesis reaching a thin-rejecting plan-writer has a defined terminal
- **Shards:** aog-dry-01, aog-ver-01

### F-07 — Bing search outage has no defined retry, alternate, or escalation (MEDIUM, MATERIAL-RISK)

- **Classification / severity / confidence:** MATERIAL-RISK / MEDIUM / HIGH
- **Affected:** W1 discovery; web_tools.py
- **Evidence:** web_tools.py:31-56 sole search backend, errors returned as data; research-agent.md:80-91 relentless discovery required; PROGRAM.md:46-54 no-fallback law governs model routes, not web tools
- **Mechanism:** a sustained Bing failure cannot honestly be called "genuine scarcity"; fetch only helps known URLs; no terminal defined
- **Impact:** W1 stalls with no defined terminal or escalation
- **Skeptical verification:** AOG-VER-01 ACCEPT
- **Atomic next step:** define retry/alternate-discovery or a founder-escalation rule for web-tool outages
- **Acceptance test:** a multi-hour Bing outage produces a documented escalation rather than an undefined stall
- **Shards:** aog-dry-01, aog-ver-01

### F-08 — Stale chapter-reviewer workflow remains actionable for operators (MEDIUM, MATERIAL-RISK)

- **Classification / severity / confidence:** MATERIAL-RISK / MEDIUM / HIGH
- **Affected:** operator guidance; production-books/README.md
- **Evidence:** prompts/chapter-reviewer.md:3 directs a post-draft writer-reviewer loop citing nonexistent PROGRAM §4.1 (PROGRAM.md:127-300 has §4 Steps 1-7, no §4.1); production-books/README.md:32 "a reviewer loop critiques each before moving on"; PROGRAM.md:179-212 defines writing as writer→judges with no revision cycle
- **Mismatch:** the removed reviewer stage survives as an actionable prompt and a current workflow instruction; AOG-CONF-01 deemed it inert (no live runbook reference), overruled by the verifier because README.md:32 is user-facing operating guidance for new books
- **Mechanism:** an operator following production-books/README.md can invoke the stale reviewer, create ungoverned revisions, and confuse its verdict with the calibrated judge process
- **Impact:** adds a non-calibrated, non-traced stage; dilutes the judge/trace decision path; this is the residue class the founder explicitly wants gone
- **Skeptical verification:** AOG-VER-01 ACCEPT ("inert in the campaign runner but not inert as user-facing operating guidance")
- **Atomic next step:** delete prompts/chapter-reviewer.md and fix production-books/README.md:32 to the writer→judges flow
- **Acceptance test:** repository search finds no operational chapter-review loop, §4.1 claim, or revise-through-reviewer instruction
- **Shards:** aog-bloat-01, aog-conf-01, aog-ver-01

## 7. Identity, boundary, authority, and provenance

- Coherent: research completion owned by the lead (§7 criterion); plan acceptance owned by the reviewer gate (BLOCK cannot be waived); judges are consumers, not decision owners; miners cannot recursively delegate (tool allowlist excludes `subagent`).
- Broken: W2 revision handback (F-02), scarcity→thin transition (F-06), refusal repair dispatch (O-01, rejected as finding but real label drift).
- Open: "escalate to the founder" (Q-01) has no defined delivery/acknowledgement mechanism in any script or the runbook — the fail-closed law exists only in prose.

## 8. Instruction conflicts and resolution paths

- Accepted: F-01 (Reddit require vs prohibit), F-02 (cycle cap vs no-waive vs until-accepted), F-04 (xhigh vs max; config authority unenforceable).
- Resolved as coherent: route/model split (all layers agree); plan-review five-file contract (intro is shorthand); research lead-vs-miner route wording; no-fallback copies consistent.
- Unresolved precedence: no general tie-breaker beyond config's parameter authority (documented in SOURCE_OF_TRUTH.md).

## 9. Ambiguity-panel results

- E1 (miner write target): MATERIAL — two+ readings, no higher source resolves (feeds F-03).
- E2 (Reddit): MATERIAL — mirrors-vs-direct changes termination and compliance (feeds F-01).
- E3 (plan-review cycle limit): MATERIAL but runbook-leaning — continue-cycling most likely per PROGRAM; hard-cap+escalate plausible (feeds F-02).
- E4 (refusal action code): resolved toward INCONCLUSIVE by PROGRAM — converted to observation O-01 (label promises repair the runbook does not deliver).

## 10. Agent Skills triggering and progressive disclosure

Not applicable to the factory surface (no Agent Skills format in the in-scope pipeline; .pi agent files are thin wrappers, not skills). The auditor skill itself was exercised for this run and its own progressive-disclosure structure worked as intended.

## 11. Complexity, duplication, and bloat

- Evidence-backed: the Reddit policy cluster (F-01) and the config-parameter surface (F-04) are duplicated rules that already diverge; the stale chapter-reviewer artifact (F-08) is dead weight with an actionable copy.
- Justified detail, not bloat: style-guide length (density is deliberate per its own note); no-fallback/route copies (boundary-protecting local repetition, consistent); _rounds/ seed material (explicitly retained by HANDOFF); daemon/queue scripts (documented optional).
- Minor: research-agent.md:84 "(§5)" cross-ref points at §4 (the ten-bank section); _template/master-plan-review.md:3 stale Sol comment (body current) — observations, not findings.

## 12. Orchestration dry runs

| Scenario | Verdict | Finding |
|---|---|---|
| DR-W1-happy (research baseline) | COMPLETES-WITH-RISK | F-05 |
| DR-W1-failA (miner transport) | COMPLETES-WITH-RISK | F-05 |
| DR-W1-failB (thin lane/scarcity) | BLOCKED | F-06 |
| DR-W1-failC (Bing outage) | UNDEFINED | F-07 |
| DR-W1-edge (concurrent writes) | UNDEFINED | F-05 |
| DR-W2-happy (planning + revision) | BLOCKED | F-02 |
| DR-W2-failB (persistent BLOCK) | UNDEFINED | F-02 |
| DR-W2-failC (spawn failure) | COMPLETES | — |
| DR-W3-happy (sequential writing) | COMPLETES | — |
| DR-W3-failA (writer refusal) | COMPLETES-WITH-RISK | O-01 |
| DR-W3-failC (spawn failure) | COMPLETES | — |
| DR-W3-edge (skipped alignment) | COMPLETES-WITH-RISK | rejected (C10) |

Full step-level traces: dry-runs/w1-research.md, w2-planning.md, w3-writing.md.

## 13. Rejected and downgraded candidates

Rejected (2, both verifier-verified): C9 (refusal action code → observation O-01; runbook defines capture→finding→INCONCLUSIVE, action code is a label); C10 (alignment freshness gate — rebuild is an explicit orchestrator duty; no-determinism is declared design). Downgraded: none. Disagreement recorded: AOG-PLAN-01 vs AOG-CONF-01 on xhigh materiality (resolved toward the enforcement finding F-04); AOG-CONF-01 vs AOG-BLOAT-01 on chapter-reviewer actionability (verifier confirmed F-08). No rejected-Low sample class existed (no Low candidates).

## 14. Unresolved questions and limitations

- Q-01: "Escalate to the founder" has no defined delivery mechanism (notification channel, handoff artifact, or acknowledgement). Smallest test: a documented executor failure trace showing the founder-facing escalation.
- Q-02: retry-budget wording conflict — HANDOFF.md:120-122 "3x 30/60/120s per PROGRAM" vs PROGRAM.md:71-74 "retried once"; nesting unspecified.
- Q-03: preflight outer pi session hard-codes `--provider commandcode` (run_preflight.sh:21) while the spawned judge route is governed by the agent pin `openai-sub` — verify at first battery run that the wrapper model resolves on the CC plan.
- Limitations: judges/trace/hypothesizer entity surfaces not reviewed (consumer scope); no dedicated spec-archaeologist shard (precedence cross-verified by two reviewers instead); static text review only — no live spawns or model calls; current syntheses/plans on disk are templates (baseline pending, so dry runs model the contracts, not an observed run).

## 15. Healthy areas

- Zero deterministic validation holds: no validator, grep gate, or deterministic handover check remains in the pipeline.
- Route pins: model/provider strings in all seven .pi agents match config and the two providers' registries (commandcode proxy + openai-sub both live).
- Chapter-writer contract: exact four inputs, canonical refusal, ch-01 exception, INCONCLUSIVE refusal handling — coherent end to end (W3 COMPLETES).
- Unlimited depth: search/fetch ceilings absent everywhere; web_tools trims are per-call payload bounds.
- Clean-context role calls: only the role prompt + listed inputs; no host system prompt (PROGRAM §1).
- Plan-writer's 4-input and plan-reviewer's 5-input boundary contracts are explicit and consistently stated.

## 16. Ordered atomic next steps

| Order | Finding/Question | Single objective | Smallest owner | Decision required | Acceptance test | Dependency |
|---:|---|---|---|---|---|---|
| 1 | F-02 | Make the plan-review revision loop executable | prompts/master-plan-skill-v2.md + PROGRAM §3 | founder: revision-call contract + post-3-cycle behavior | `needs changes first` → compliant revision call → `fit to write from` | none |
| 2 | F-04 | Make config's declared parameters real or remove them | loop/config.yaml + subagent extension or .pi frontmatter | founder: enforce vs declare-only | changing writer_temperature changes emitted request | none |
| 3 | F-03 | Define the miner write contract | prompts/research-agent.md + researcher.md + sources/README.md | founder/operator: bank-file vs sources/ packet convention | fresh miner writes one traceable entry without editing syntheses | none |
| 4 | F-01 | Resolve the Reddit mandate vs rights gate | AGENTS.md + AUTO-TUNING-LOOP + research prompts | founder: mirrors-satisfy vs authorization handoff | unambiguous compliant source path per work order | none |
| 5 | F-08 | Delete the stale chapter-reviewer workflow | prompts/chapter-reviewer.md + production-books/README.md | lead/operator | no reviewer-loop instruction remains | none |
| 6 | F-05 | Serialize/own bank writes | research dispatch contract | lead | loss-free concurrent mining | F-03 |
| 7 | F-06 | Define scarcity→thin transition | PROGRAM §3 | founder | defined terminal on thin rejection | none |
| 8 | F-07 | Define web-tool outage retry/escalation | web_tools.py + research prompt | lead | documented escalation on sustained outage | none |
| 9 | Q-01 | Define the founder-escalation delivery mechanism | PROGRAM + harness | founder | executor failure trace reaches the founder | none |
| 10 | Q-02/Q-03 | Reconcile retry wording; verify preflight wrapper route | PROGRAM/HANDOFF + run_preflight.sh | lead | single retry rule; first battery passes on final routing | none |

## 17. Source-integrity and commit readiness

Baseline: clean (no staged/unstaged/untracked changes). This run created only files under `reviews/orchestration-audit/20260808-113126-belief-changer/` (manifest, source-of-truth, system map, assignments, 14 worker shards, 3 ledgers, 3 dry-run records, adjudication ledger, this report). No production file changed; no accidental write incident. The audit root is ready to be staged as one audit-only commit; pre-existing working-tree state (none) must remain outside it.
