## Failure evidence

**PRIMARY scope: both subjects — voice `factory-speech`.** The 039 census records **13 noted occurrences in quit-sugar** and **8 noted + 2 blocking occurrences in quit-smoking**.

The decision identifies the recurring instruction-landing cluster:

- Smoking CH-03: **“3. BEGIN BY FEELING GREAT TO BE ESCAPING”**, still blocking for both `factory-speech` and `instruction-paperwork`.
- Sugar CH-09: **“10. IGNORE ANYONE WHO QUIT BY WILLPOWER”**, previously blocking factory-speech, now classified as noted willpower-lexicon.
- The attempted reviewer repair missed its intended surface: **“HEADER fired on `IN THIS CHAPTER` openings, not on the numbered-instruction surface.”**

The reader-effect hypothesis is that an inventory entry interrupts the argument where an earned command should complete it. These examples establish recurrence across subjects, **not** that all 23 factory-speech occurrences share this cause. Smoking CH-07’s “evidence-bound qualification inside the primary-job verdict” is a separate manifestation, left untouched here.

The supplied trace-analysis is empty; these quotations come from the decision’s preserved findings. Comparison `missing` is present in both subjects (1/3), but no missing move or affected passage is identified in the supplied diagnosis. Rather than invent a comparison repair, this hypothesis targets the documented, both-subject, ≥8-noted factory-speech cluster.

## Root cause

**Candidate root component: `prompts/chapter-writer.md` — Full-length chapter anatomy, item 5.**

The writer is explicitly told:

> “When an instruction is assigned: the numbered ALL-CAPS spoken imperative at the climax, followed by at most one short spoken rationale line.”

This specifies the command’s display and a possible **following** explanation, but does not require the preceding argument to establish why that particular action follows. A writer can satisfy the anatomy with an inserted inventory item and a generic tail.

Learnings rule out another header-removal experiment: 032, under Spark 1.3/composer-2.5 census judging, removed numbering and supplied an ordinal announcement that itself became factory-speech. The 039 reviewer ownership test also failed under that instrument. This proposal retains numbering and exact wording; its new mechanism is **generation-time placement at the concrete decision the argument has just resolved**, rather than a downstream exemption test.

## Targeted fix

**Change 1 (PRIMARY) — `prompts/chapter-writer.md` — voice `factory-speech` — Full-length chapter anatomy, item 5 — targets quit-sugar and quit-smoking — replacement text.**

Replace item 5 in full with:

```text
5. When an instruction is assigned, make its exact numbered ALL-CAPS
   imperative complete the concrete decision the preceding body passage
   has resolved. Place it immediately after that passage, not as a separate
   inventory entry attached to the chapter's general verdict. The passage
   must make clear what the reader now understands about this particular
   action and why it follows; use the argument already owned by this card,
   not a new proof of earlier work. Preserve every assigned instruction's
   exact wording and number. Do not announce its ordinal, label its arrival,
   or append a generic rationale: the preceding passage supplies the reason.
   Omit this element when no instruction is assigned. The final
   photographable instruction recap remains a list.
```

Leave reviewer `HEADER`, frozen-token requirements, evidence rules, and all other anatomy items unchanged.

**Why this component:** The decision shows that the reviewer did not engage the targeted instruction surface, while the writer’s anatomy directly commissions that surface without specifying its concrete argumentative connection.

## Predicted impact

**PRIMARY:** factory-speech, blocking plus noted, falls in both subjects: **13 → ≤11 sugar; 10 → ≤8 smoking**, with smoking’s instruction-landing blocker predicted to disappear. Readers should experience the command as the consequence of their changed understanding rather than a switch into instruction-sheet prose.

Secondary `instruction-paperwork` may fall in smoking; this is recorded, not decisive.

**What might regress:** Requiring a preceding connection could encourage re-argument or verbose explanation. Preserving exact commands could also leave some inventory texture unchanged. Monitor `re-argument`, `compliance-missing`, and the 48,000-word floor.

**How we’ll know it worked:** The PRIMARY class count must fall materially in **both replicates**, not merely lose numbering-related grep hits. Because 039 was restored, also compare against accepted 037 totals **10/5**; recovery from a rejected run alone is not evidence of improvement over the accepted factory.
