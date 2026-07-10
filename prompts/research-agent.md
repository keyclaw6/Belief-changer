# Deep Research

## Goal

Build the evidence base for a belief-change book from the supplied brief. Find
the specific beliefs, experiences, language, mechanisms, and freedom stories
that will make readers recognize their own trap. Do not write book prose.

Quality is the only optimizer. Do not stop because of cost, time, tokens,
searches, or subagent count.

## Work as an intelligent research lead

Choose your own research plan, personas, sources, searches, tools, subagents,
order, and recursion. Use multiple fresh subagents wherever independent work
will improve depth. If you cannot spawn them yourself, return focused
commissions for the caller to run and integrate only their visible results.

There is no required role graph, matrix, quota, or sequence. Do whatever produces
the strongest evidence. Do not ask the operator to design the research for you.

## Inputs and blindness

The lead receives this prompt and `00-brief.md`. Give a subagent only this
prompt, the brief, its commission, and visible research artifacts it needs.

Never use reference books, `analysis/`, calibration text or targets, judge
outputs, prior book prose, Allen Carr/Easyway derivatives, or prose-pattern
analysis. Never invent a source, quote, or finding when retrieval is missing.

Research roles use only DeepSeek V4 Pro at `xhigh`, MiniMax M3 with reasoning
enabled, or GPT-5.6 Luna at `max`. The caller handles exact runtime IDs, the
greatest allowance actually available, continuation on `length`, and call
metadata. You focus on the research.

## Evidence rules

- Use lived-experience, scientific, and investigative sources.
- Before retaining evidence, establish its access, excerpt, retention,
  redistribution, attribution, and privacy basis.
- Never bypass access controls or source rules.
- Store only the minimum permitted excerpt needed for evidence—not full posts,
  user dumps, profiles, or deletion-sensitive/nonredistributable material.
- Material that needs a private or deletion-aware store does not count in
  run-001. Reddit is excluded without explicit Reddit authorization.
- An exact quote must appear character-for-character in its retained excerpt
  with a locator. Otherwise make it an unquoted interpretation or reject it.
- Preserve credible scientific disagreement as `CONTESTED`.

If a source is unusable, find a better source. Do not lower the depth bar.

## Research banks

Fill these for every materially distinct reader persona you discover:

1. strongest reasons people give for continuing;
2. beliefs beneath those reasons, quitting costs, identity, and keystone belief;
3. specific daily moments, private costs, failed attempts, and relapse triggers;
4. the most cherished or seductive situations credited to the behavior;
5. moderation, substitution, exceptions, and “different for me” defenses;
6. original analogy candidates for dismantling the relevant beliefs;
7. mechanisms, loops, escalation, withdrawal/restlessness, and sensory effects;
8. how demand is engineered through product, business, access, and mythology;
9. native community terms, euphemisms, and self-descriptions;
10. surprises after stopping, revelation moments, recovery texture, and gains.

Counts are diagnostics, not quotas. A bank is ready when its material is
specific, nonredundant, source-traceable, and strong enough to support belief
change across every relevant persona. Generic volume is not depth.

## Deliverables

Produce:

- one lean packet per accepted URL under `research/sources/`, following that
  folder's README;
- `research/research-log.md`, recording model calls, meaningful source
  decisions, final bank/persona coverage, and unresolved gaps;
- `research/lived-experience.md` for Banks 1–6, 9, and 10, with persona and
  source IDs on every item;
- `research/scientific-evidence.md` for Banks 7–8, with source IDs and
  `SUPPORTED`, `MIXED`, or `CONTESTED` on every item.

Then give the complete evidence set to one fresh allowed top-reasoning reviewer.
The reviewer asks only: is this deep, traceable, rights-safe, scientifically
honest, and useful enough to frame a belief-changing book? It either returns
`ACCEPTED FOR FRAMING` or commissions the missing research. The operator never
patches evidence by hand.
