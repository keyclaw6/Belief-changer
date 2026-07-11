# Run report — run-010

**Stage:** A **Scope:** model-led semantic commissions + Chapter 1 A/B + conditional treatment Chapters 1–3 **Verdict:** FAIL — H-047 REFUTED

## What will run

A fresh Sol-ultra commissioner reads the complete canonical plan and one target chapter ID, then writes a focused natural-language semantic commission containing all and only the material that chapter's writer materially needs. It decides the useful form. It may not outline prose, prescribe reasoning steps, invent content, or include unrelated later material.

Separate fresh contexts produce commissions for Chapters 1–3. All three freeze before any prose call. One fresh Sol-ultra auditor compares them with the canonical plan and reports fidelity without repairing them.

Chapter 1 then runs a same-start blind A/B:

- control Opus sees the complete plan, reproducing run-009's input contract;
- treatment Opus sees the focused Chapter 1 commission instead of the complete plan.

Everything else is identical. Both drafts finish before either review. Reviewers see the canonical plan and neutral candidate, not the arm or commission.

If the treatment packet is faithful, its first draft has no target ownership blocker, and treatment Chapter 1 accepts within the normal fixed gate, the same already-frozen treatment contract continues through Chapters 2–3. Control is diagnostic only.

## Pre-registered causal test — H-047

- **Observation:** run-009 imported EV-04, C-05, and C-20 material from a valid 21-chapter plan despite an explicit ownership-priority rule.
- **Mechanism:** currently unowned but salient semantic inventory competes with the current card; reducing that competition through intelligent commissioning should improve ownership without reducing model judgment.
- **One lever:** focused model-authored semantic commission replacing the full plan in the writer context.
- **Prediction:** all packets are faithful; treatment Chapter 1 has zero target blockers while control repeats at least one; treatment Chapters 1–3 remain target-clean, converge on craft/length, and pass the full blind Stage-A gates.
- **Decision:** supported only if treatment beats control semantically and the complete treatment product passes. Refuted if a faithful treatment packet excludes the offending material but Opus recreates it, or at least two packets are materially unfaithful. Inconclusive if arms match, one packet defect makes the comparison unfair, or semantic improvement does not produce product quality.

Reviewer acceptance alone never promotes the lever.

## Anti-overfit and simplicity boundary

The commissioner prompt is behavior-agnostic and frozen. Packets are derived before prose results and never hand-edited. The commissioner does not become a database renderer, prose planner, or checklist generator; it is one intelligent fresh-context handoff. Mechanical slicing, another prohibition sentence, and a writer-model change are excluded.

Even success requires a zero-amendment stability run and the untouched caffeine holdout.

## Results

The experiment was preregistered at `3cc8d51`. The behavior-agnostic commissioner prompt froze unchanged at `a2f83da` (SHA-256 `1c07aa5df8ae65a6f4862cad1e76356215f99addb80d0c1edc59cceec593900b`). A fresh read-only contract critic returned GO: it found no specimen or chapter patch, fixed schema, prescribed reasoning procedure, or second-planner behavior.

Three separate fresh native Sol-ultra contexts then produced the pre-prose commission set:

| Target | Words | Frozen SHA-256 |
|---|---:|---|
| C-01 | 859 | `5c9237a669eebd805d4035be8463a187be9a75d203e7faf6600716dcf573eb46` |
| C-02 | 1,367 | `249f52790f4738a4435f6fd6bd11319e4e610cd8bbad29d41e67a1bc451fce5a` |
| C-03 | 1,135 | `9973aa598556ae4e088a875d8935a8cd690a56aec20aa0ce32e12a83601015b2` |

The first C-03 host attempt entered a broken ephemeral collaboration-wait loop despite `multi_agent` being disabled. It was terminated after producing no output and recorded as infrastructure failure. A fresh same-model/ultra retry added only `--ignore-user-config`; one child-spawn attempt failed, no child result entered, and the primary commissioner completed normally. No content input changed.

At that freeze boundary, no prose call had run.

### Packet-fidelity verdict

The fresh Sol-ultra audit returned **FAITHFUL** for C-01, **FAITHFUL** for C-02, and **ISOLATED DEFECT** for C-03; the set verdict is **ISOLATED DEFECT**.

C-03 says BAD SUGAR does not include accidents or honest ambiguity. The canonical plan instead keeps core membership categorical and uses DEF-05 to say accidental exposure or honest classification error is not a deliberate return or failure. This is a real semantic alteration. The frozen packet is not repaired.

The faithful C-01 packet allows the preregistered Chapter 1 control/treatment comparison to proceed. The C-03 defect remains a later full-product validity risk and prevents any unsupported success claim. H-047 is neither supported nor refuted by one isolated packet defect.

### Chapter 1 launch infrastructure

The live model catalog reconfirmed Opus 4.6 with 1,000,000 context, optional reasoning, and a 128,000 completion maximum. The disposable key had $2.3077 remaining. Both simultaneous 128,000-allowance requests returned HTTP 402 before inference because the key could authorize at most 100,308 completion tokens. No model ran and no charge or content resulted. Both arms retry at that exact shared ceiling; this remains far above the chapter budget and changes no content input.

### Chapter 1 first drafts

Both arms launched concurrently and completed before review. OpenRouter reported the same runtime model (`anthropic/claude-4.6-opus-20260205`), Anthropic provider, normal stop, and zero reasoning tokens for each.

| Arm | Semantic input | Words | Cost | Frozen SHA-256 |
|---|---|---:|---:|---|
| Control | complete canonical plan | 2,676 | $0.309670 | `36c477c6c856e2ed9ce3afcd9c2e4318dcc35278650aa9a8de4ea8a04c1b5417` |
| Treatment | faithful C-01 commission | 2,362 | $0.197855 | `9602cf8c442bddccae12cb89f1848cdc4893605f9409e8dad349fc016843dda5` |

The treatment is 18 words below the existing 2,380-word lower bound. That is recorded as a gate failure unless a pre-existing instrument says otherwise; it is not waived because the miss is small.

The required first-prose direction auditor returned **GO**: real candidates now exist for blind evaluation; the lever answers observed semantic leakage, is behavior-agnostic, and could operate unchanged on an unseen topic. The next action is objective and blind product evaluation.

### Evaluator repairs

The first objective pass exposed two generic instrument defects rather than book defects:

- the mantra parser understood only the retired bullet format, so the accepted normalized table produced an empty whitelist;
- licensed recap removal understood `## SUMMARY` but not the standalone `**SUMMARY**` form allowed by the writer contract.

Commits `2530973` and `b721e1b` repaired those parsers with legacy and negative tests. No threshold, prompt, packet, or chapter changed. The full gate rose from 36 to 41 passing tests. Rerunning the exact frozen candidates produced zero mechanical hard failures and zero reference-overlap for both.

### Objective and blind-review results

| Measure | Control | Treatment | Frozen target |
|---|---:|---:|---:|
| `wc -w` | 2,676 | 2,362 | 2,380–3,220 |
| Instrument words | 2,613 | 2,308 | — |
| Mean sentence words | 12.1 | 12.5 | 15–18 |
| Sentences under 8 words | 47.2% | 51.9% | 15–20% |
| Questions | 7.4% | 5.9% | 8–10% |
| Second-person terms / 1k | 46.3 | 49.8 | 25–33 |
| Mechanical `run_evals` | PASS | PASS | PASS |
| Blind Sol-ultra review | REVISE | REVISE | ACCEPT |

The mechanical pass means mantra schedules, repetition law after licensed-zone handling, and originality were clean. It does not override the binding craft measurements or semantic review. Both arms failed craft; treatment was worse on short-sentence density, questions, direct address, and length.

The neutral control review found C-11 fear-collapse and C-05 anti-method arguments, unsupported authority and causal inference, EV-07/C-16 testimony imported into C-01, assigned SC-08 omitted, and required anatomy missing.

The neutral treatment review found invented EV-06 gender and outcomes, an overextended C-16-reserved EV-08 account, C-05 anti-method drift, an unsupported comparison with bodily effects, M-06 case infidelity, missing landing anatomy, and severe craft imbalance.

Both reviewers completed before the operator mapped neutral candidates back to the arms. Neither saw the packet, experiment, other candidate, reference, history, or metrics.

## Causal verdict — H-047 REFUTED

The decisive preregistered condition fired: the C-01 commission was independently judged faithful and explicitly excluded unrelated evidence and later-chapter work, yet treatment Opus recreated the same ownership class. It invented evidence details and effects, expanded C-16-reserved testimony, and began C-05's anti-method argument. The treatment therefore had target blockers on its first draft and received `REVISE`.

The continuation gate required a faithful packet, zero first-draft target blockers, and Chapter 1 acceptance. It failed. No treatment revision, Chapter 2, Chapter 3, or judge-panel call ran. Continuing would have converted a clean falsification into post-hoc prompt tuning.

### Failure autopsy

The control's leakage was broader, so full-plan semantic competition may contribute to the failure's size. It is not sufficient as the cause: removing the full plan did not produce owned, evidence-bounded prose and did not improve craft. H-047 is refuted as a factory solution, not interpreted as proof that context never matters.

The next causal question is narrower. Both arms still received the complete 639-line style guide, whose planner-facing method and arc material exposes whole-book arguments and categorical mechanism language. Opus's own persuasive completion prior is the rival owner. Run-010 cannot distinguish style-context competition from model prior, so neither is promoted as the explanation yet.

The commissioner itself was not universally reliable: C-01 and C-02 were faithful, while C-03 converted DEF-05's non-failure margin into category exclusion. That isolated defect did not cause the C-01 result, but it blocks any claim that this handoff is production-ready.

Focused context also failed the chronic prose problem. Treatment reached 51.9% short sentences and 49.8 second-person terms per 1,000 words. Semantic focus cannot count as progress while the resulting chapter remains this far from the prose contract.

### Product and factory result

No run-010 chapter is promoted. The prior accepted Chapters 1–2 remain the last accepted product artifacts. The commissioner prompt and packets remain calibration evidence only; nothing is eligible for `main`.

Runs 008–010 now form three consecutive semantic runs without gate progress on the same ownership dimension. The §11 escalation is active again. The next move must come from a fresh direction audit and distinguish residual style-context competition from writer behavior; another prohibition sentence, Chapter 1 patch, packet repair, or unchanged commissioner retry is a no-go.

## Gate verdict

FAIL. H-047 is **REFUTED**. Treatment failed the preregistered first-draft ownership and acceptance conditions, so the run stopped before later chapters and Stage-A judging. No product or generic factory asset was promoted.
