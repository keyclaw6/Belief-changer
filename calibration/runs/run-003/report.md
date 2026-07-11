# Run report — run-003

**Stage:** A **Scope:** Chapter 2 prose-only compression **Verdict:** FAIL

## What ran

Run-003 inherits run-002's accepted research, framing, normalized plan, and Chapter 1 unchanged. It also inherits Chapter 2 R3 as a semantically certified candidate: the fresh R3 reviewer found zero method, evidence, assignment, anatomy, safety, repetition, or continuity blockers, but rejected 3,761 words and 36.7% short sentences.

H-040 changes one variable. A fresh Opus 4.6 reasoning-none role performs a prose-only compression edit. It may cut, combine, locally reorder, and smooth the certified draft; it may not add or change semantic work. A fresh Sol `ultra` reviewer then judges the result from the normal blind chapter inputs. No shared prompt, plan, research, or rubric changes.

The run-boundary bird's-eye audit returned `GO`: this preserves the failed run boundary, tests one generic mechanism, and is the shortest path back to product prose.

## Pre-registered causal test

- **Observation:** whole-artifact Chapter 2 revisions expanded 3,341 → 3,611 → 3,761 words while short-sentence density remained 39.1% → 37.3% → 36.7%; final semantic blockers were zero.
- **Hypothesized mechanism:** simultaneous semantic repair and craft optimization makes coverage dominate deletion.
- **Lever:** a fresh prose-only compression objective after semantic certification.
- **Held constant:** all content assets, model, route, reasoning mode, continuity, reviewer, blindness, and metric targets.
- **Prediction:** one pass reaches 2,550–3,450 words, materially lowers short-sentence density toward ~20%, introduces no blocker, and receives `ACCEPT`.
- **Rival explanations:** any improvement may be an extra-call effect; failure may instead show Opus/no-reasoning constraint weakness.

## Results

Opus 4.6 at reasoning `none` produced a 3,236-word prose edit, cutting 525 words from the semantically certified R3. The first Sol review attempt encountered an infrastructure fault: its ephemeral helper spawn failed and it entered repeated empty waits without a verdict. It was terminated for nonproductive orchestration, not elapsed reasoning time. The identical blind review was rerun at Sol `ultra` with multi-agent orchestration disabled and no time, token, or reasoning limit.

The canonical fresh review returned `REVISE` with zero blocking defects. It certified M-09, I-02, every assigned definition/evidence boundary/scene/analogy/exercise/safety duty, anatomy, continuity, and repetition. The edit passed length but failed three craft measurements:

| Measure | run-002 R3 | H-040 edit | Target | Result |
|---|---:|---:|---:|---|
| Words | 3,761 | 3,236 | 2,550–3,450 | PASS |
| Short sentences | 36.7% | 33.2% | ~20% | FAIL |
| You/your | 23.4/1k | 19.5/1k | 25–33/1k | FAIL; regressed |
| Questions | 8.6% | 7.4% | 8–10% | FAIL; regressed |
| Mean sentence | 14.2 | 14.6 words | 15–17 | improved, still low |

### H-040 causal verdict

`MIXED`. Separating prose compression supported the length and semantic-preservation submechanisms, but refuted the one-pass ACCEPT prediction and did not sufficiently repair rhythm. The editor mainly deleted material; it did not recast enough distant “reader/book” narration or combine enough secondary fragments. Because it still received the full writer prompt, plan, and previous chapter, task/context interference remains plausible rather than demonstrated.

A false positive would call H-040 successful from word count alone despite the blind rejection. A false negative would ignore that semantic preservation and length both improved. The next discriminating test must separate context interference from the generic benefit of another measured edit.

## Gate verdict

FAIL. H-040 did not receive fresh `ACCEPT`; Chapter 2 remains unpromoted.

## Next amendment

H-041 runs two Opus 4.6/no-reasoning edit arms on the exact H-040 candidate and review with the same craft objective. The control retains full writer/plan/continuity context; the treatment receives only the style guide, certified candidate, and measured review. Fresh unrestricted Sol reviews judge both. This directly distinguishes context interference from a second-pass or better-feedback effect before any factory change is promoted.
