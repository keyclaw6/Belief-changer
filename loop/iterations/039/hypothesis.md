## Failure evidence

**PRIMARY scope: both subjects — voice `factory-speech`.** The 038 decision identifies a blocking occurrence in each book:

- Quit-sugar, CH-09: **“10. IGNORE ANYONE WHO QUIT BY WILLPOWER”** — described as a “numbered mantra echo.”
- Quit-smoking, CH-03: **“3. BEGIN BY FEELING GREAT TO BE ESCAPING”** — described as a “numbered instruction header.”

The decision concludes:

> “Blocking FAILs are numbered instruction/mantra headers, not evidence-bound speech.”

The class totals are **10 in sugar (1 blocking + 9 noted)** and **8 in smoking (1 blocking + 7 noted)**. The blocking cluster spans two chapters across both subjects; the remaining noted occurrences are not established as the same surface form.

The supplied trace-analysis is empty. These are passage quotations and diagnoses preserved in the decision, not an independently available full judge rationale. The hypothesized reader failure is that the climax presents an inventory entry instead of a command arising from the reader’s newly changed understanding.

## Root cause

**Candidate root component: `prompts/chapter-reviewer.md`, Output / `HEADER` exception.**

The current instruction explicitly exempts:

> “A numbered ALL-CAPS instruction plus one spoken rationale line is not `HEADER`.”

That exemption tests formatting and the presence of a rationale, not whether the command belongs to this chapter or follows from its argument. It can therefore protect both a numbered echo presented as another instruction and an instruction header with a generic explanatory tail.

The writer’s anatomy requires numbered commands, but numbered commands are not inherently defective. The narrower problem is the reviewer’s unconditional exemption for that surface format.

Learnings constrain the repair: 032, scored under Spark 1.3 with composer-2.5 census judges, removed numbering and substituted **“So here is my sixth instruction:”**, which became new factory-speech. This proposal does **not** retry that replacement or the 030 opening-header mechanism. It replaces the existing exemption with an ownership-and-earned-landing test; legitimate numbered commands remain.

## Targeted fix

**Change 1 (PRIMARY) — `prompts/chapter-reviewer.md` — voice `factory-speech` — Output / `HEADER` finding — targets quit-sugar and quit-smoking — replacement text.**

Replace the complete existing `HEADER` bullet:

```text
- `HEADER` — the draft opens with the workshop header `IN THIS CHAPTER`, or it prints a numbered plan-index with no spoken body. A numbered ALL-CAPS instruction plus one spoken rationale line is not `HEADER`.
```

with:

```text
- `HEADER` — the draft opens with the workshop header `IN THIS CHAPTER`, or presents a plan-inventory entry instead of an earned spoken command. For each numbered instruction outside the final photographable recap, check that this card assigns it as NEW and that the immediately preceding argument makes its particular imperative the reader's warranted next conclusion; a generic rationale line does not establish either condition. Quote the header and the passage that should earn it. If it is an assigned echo rather than a new instruction, require the frozen words to remain verbatim as a brief spoken sentence in the current context, without an inventory number or a new-instruction announcement. If it is a new instruction, preserve its number and exact imperative, but replace the generic lead-in or rationale with the concrete connection to the argument already made; do not rebuild an earlier proof or announce the instruction's ordinal in words. A numbered command that meets these conditions, and the final photographable instruction recap, are not HEADER.
```

Leave the existing ACCEPT gate and all other findings unchanged.

**Why this component:** The reviewer explicitly shelters the diagnosed format, so replacing that exemption addresses the acceptance gap without suppressing legitimate command authority or adding another global vocabulary ban.

## Predicted impact

**PRIMARY:** voice `factory-speech` falls in **both subjects**, counting blocking plus noted: sugar **10 → ≤8**, smoking **8 → ≤6**, with blocking **1 → 0 in each**. The reader should encounter either a brief contextual reminder or a command earned by the argument—not an instruction-sheet interruption.

**What might regress:** The ownership test could misclassify legitimate instruction recaps or weaken an imperative through unnecessary connective prose. The replacement therefore preserves exact wording, valid numbering, and the final recap exception. Monitor instruction compliance, re-argument, and both books’ **48,000-word floor**.

**How we’ll know it worked:** The PRIMARY class count must fall materially in **both replicates**, including removal of both blocking occurrences. Header grep, reviewer ACCEPT rates, or voice-lane PASS alone do not decide KEEP. Since 038 was restored, also report results against accepted 037 totals (**10/5**) so recovery from the rejected run is not mistaken for improvement over the accepted factory.
