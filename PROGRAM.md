# PROGRAM — causal-bundle factory loop

> **PAUSED BY RF-00.** Before RF-23 is `READY`, recover only from
> `openspec/changes/redesign-book-factory/tasks.md`; do not resume the historical
> reward loop from `loop/results.tsv` or `loop/learnings.md`. Every legacy
> write-capable entrypoint runs `scripts/loop/legacy_guard.py` before resolving
> models, networks, configuration, or outputs. Pre-RF-23 work is limited to
> implementation checks, isolated H-F04 calibration, and authorized RF-21/RF-22
> planning or commissions inside an RF-02 candidate snapshot.

The loop tests one causal hypothesis through the linked artifacts required to
instantiate it. It does not optimize one file or one averaged reward.

## 0. Recovery and context

Read this file, `AGENTS.md`, both vision files, the redesign ledger, and the last
valid line of `loop/causal-bundle-results.jsonl`. The root operator handles only
paths, hashes, compact verdicts, owner routes, and decisions. Fresh agents read
or generate all chapter, opening, book, and reference prose. Reference-bearing
calibration material stays outside generation and promotion contexts.

## 1. Route law

- Claude Opus 4.6, reasoning disabled, writes chapters through OpenRouter.
- DeepSeek V4 Pro performs research through OpenRouter at top reasoning.
- Framing, planning, commissioning, review, evaluation, and audit use fresh native
  agents. GPT‑5.6 Sol and all GPT models NEVER route through OpenRouter; the
  earlier MiniMax writer note is RESCINDED.
- Missing credited `OPENROUTER_API_KEY` blocks chapter generation, not setup,
  calibration, planning, commissioning, or record validation.

## 2. One run

Before any model call, declare one hypothesis, its causal chain, the linked
changed bundle, frozen variables, decisive falsifier, and exact input IDs or
hashes. Unrelated changes start another run.

Execute this order without adding another lifecycle:

1. **Candidate isolation** — use RF-02 to snapshot accepted configuration and
   product; pin that operation root for every later read and write.
2. **Generation** — after the required plan and commission gates pass, generate
   the selected chapters in order under the declared frozen variables.
3. **Frozen batch** — use RF-11 to freeze every selected first draft before any
   review or revision.
4. **Grounded review** — use RF-12 for source, safety, originality, ownership,
   non-shaming, no-willpower, and near-copy integrity. A material failure rejects.
5. **Developmental review** — use RF-13 on the complete frozen opening for
   transition, specificity, emotional movement, escalation, and handoff.
6. **Blind evaluation** — freeze independent chapter-effect and whole-opening
   verdicts from two fresh contexts. Evaluators receive no condition,
   provenance, history, scores, reference identity, or ordinary reference prose.
7. **Owner routing** — use RF-14 to send any accepted defect to its earliest
   owner and invalidate only causally downstream work.
8. **Decision** — keep integrity, reader effect, sequence, and Carr-craft
   diagnosis separate. Integrity or near-copy failure rejects; material judge
   disagreement is `INCONCLUSIVE`. Carr craft runs only after blind evidence is
   frozen and cannot promote by itself. Non-mantra repetition is a repair signal.
9. **Atomic promotion** — reject without changing accepted bytes, or use RF-02
   to promote the exact tested configuration and product together after every
   required gate and named-human approval passes.

## 3. Minimal record

Append one JSON line to `loop/causal-bundle-results.jsonl` only when the decision
is known. Its exact fields are: hypothesis, causal chain, changed bundle, frozen
variables, input IDs/hashes, the four evidence layers, decision, and falsifier.
Validate the schema and committed dry run with:

```
python3 -m unittest scripts.eval.tests.test_experiment_record
```

`loop/results.tsv`, `loop/learnings.md`, and old scores remain historical. Never
compare their rewards numerically with this lineage. Raw evidence remains in the
existing isolated evidence paths; the result line stores only compact outcomes.

## 4. H-F04 calibration exception

RF-20 calibration uses two disjoint blind contracts: an absolute observer sees
one content and reports belief-change sufficiency; an anonymous A/B comparator
reports only relative preference. Neither verdict schema accepts the other, and
absolute output never enters a comparator prompt. A matched reference may appear
only as an anonymous, non-promotable calibration candidate outside generation.

RF-20 is `BLOCKED` by a terminal failed lineage; the canonical outcome and hashes
live only in the `rf20-attempt-5` row of `calibration/runs/LEDGER.md`. Do not retry
or reinterpret that lineage. RF-21 remains blocked until a newly founder/root-
approved calibration lineage passes.
