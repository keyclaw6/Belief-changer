## Failure evidence

Lane `carr-distance`, both subjects — KEEP-eligible PRIMARY intersection (deficit 20/28; also missing 5/4, partial 6/5 in both; blocking 0 both).

Census 046: quit-sugar `score-deficit` 20 (score 80); quit-smoking `score-deficit` 28 (score 72). Words 56339/59487, floors met.

Trace-analysis 046 §3 Register gap, both-subjects signal:
- Sugar R2: drawer/kettle lyrical inventory vs blunt analogy.
- Smoking R2 main distance: CH-14 unconstrained outward-push invention → model-default Latinate → reviewer-mandated extension → no register gate.
- Voice literary-stylization 4/5 both carries the same diction.
- 046 decision: "§B5 never bans Latinate diction; reviewer has no register finding."

## Root cause

PRIMARY root: `prompts/style-guide.md` §B5 Plain Carr sentence bans fragments and belief-free catalogues but never bans Latinate abstraction or lyrical-inventory crescendos — both writers satisfy peaks with model-default Latinate.

Secondary root: `prompts/chapter-reviewer.md` has no register finding (verified: JOB/MANTRA/INSTRUCTION/ID/LENGTHEN/SHORTEN/HEADER/STOPPED-SHORT/UNASSIGNED-REFRAIN/RESERVED-REACH/RE-ARGUMENT/OVERCLAIM/SUMMARY only). Smoking vintage residue (E8/E22/E15/E24 on 037 cards) is plan-card level and 3-strike barred — not file-eligible here.

## Targeted fix

**Change 1 (PRIMARY)** — `prompts/style-guide.md` — class `carr-distance` `score-deficit` — component: §B5 Plain Carr sentence — both subjects. Replace:

> **Plain Carr sentence.** Write as one person talking across a table. Complete conversational sentences. Do not write fragment chains of three or more ("Blast never built. Blast billed. Film, thirst."). Do not write a paragraph of sensory catalogue with no belief verb. Invented private vocabulary is allowed only for the two named creatures and the frozen mantras — everyday words for everything else.

with:

> **Plain Carr sentence.** Write as one person talking across a table. Complete conversational sentences. Do not write fragment chains of three or more ("Blast never built. Blast billed. Film, thirst."). Do not write a paragraph of sensory catalogue with no belief verb. Never build a crescendo, peak, or verdict from Latinate abstraction (judgement, repose, homily, lucid, facilitate, contemplate, and their kin): build peaks only from short Anglo-Saxon plain words in blunt exclaimed verdict sentences. Invented private vocabulary is allowed only for the two named creatures and the frozen mantras — everyday words for everything else. Carr-native numbered ALL-CAPS instructions plus one spoken rationale line and the terminal mantra are exempt from this ban.

**Change 2** — `prompts/chapter-reviewer.md` — class `carr-distance` `score-deficit` — component: REGISTER finding + ACCEPT gate — both subjects. Within the same instruction replace:

> - `SUMMARY` — SUMMARY has more than three bullets, a bullet without the belief verb stating the belief that changed, or a token roll-call / instruction recap / preview list / study-design note. Quote the violating bullet; require at most three one-sentence belief bullets.
>
> No other finding types. No style notes. No "sounds like AI." No comparison
> to any other book. No warmth, tone, or voice coaching.

with:

> - `SUMMARY` — SUMMARY has more than three bullets, a bullet without the belief verb stating the belief that changed, or a token roll-call / instruction recap / preview list / study-design note. Quote the violating bullet; require at most three one-sentence belief bullets.
> - `REGISTER` — a peak, crescendo, or verdict built from Latinate abstraction instead of short Anglo-Saxon plain exclaimed bluntness (judgement, repose, homily, lucid, facilitate, contemplate, and their kin), or a lyrical inventory/catalogue standing in for a blunt analogy. Quote the Latinate passage; require a rewrite in plain everyday words ending in a short blunt verdict. Numbered ALL-CAPS instructions plus one rationale line and the terminal mantra are not `REGISTER`.
>
> No other finding types. No style notes. No "sounds like AI." No comparison
> to any other book. No warmth, tone, or voice coaching.

and within the same instruction replace:

> `ACCEPT` only when every check above is fine (length inside ±15% of B, job
> done and stopped and landed, assigned mantras/instructions verbatim, IDs
> resolved, no `HEADER`, no unassigned refrain, no reserved-later job, no
> re-argument, no overclaim, no SUMMARY violation).

with:

> `ACCEPT` only when every check above is fine (length inside ±15% of B, job
> done and stopped and landed, assigned mantras/instructions verbatim, IDs
> resolved, no `HEADER`, no unassigned refrain, no reserved-later job, no
> re-argument, no overclaim, no SUMMARY violation, no REGISTER violation).

**Why this component:** the trace names the §B5 Latinate permission plus reviewer register-blindness as the only both-subjects deficit minter outside plan-card, and plan-card edits are 3-strike forbidden.

Doctrine safety: bans Latinate abstraction only; exempts Carr-native ALL-CAPS + terminal mantra. No 039/040 replay, no header chase, no tight-shoes, no card-field/plan-skill/plan-reviewer-assignment edit, no route-every-limit, no model/route change. Pre-spend GSBS control: Carr's peaks are plain Anglo-Saxon blunt exclaimed verdicts — control does not fire. Smoking vintage needs a non-card mechanism or founder call — not proposed here.

## Predicted impact

PRIMARY: `carr-distance` `score-deficit` falls in BOTH subjects vs 046 (sugar 20→≤15, smoking 28→≤21, ≥25% and ≥4 band). Secondary: voice literary-stylization 4/5 falls; comparison missing 5/4 and partial 6/5 flat-to-noise.

What might regress: enforced bluntness could thin lyrical variety — mantra echoes and concrete-analogy scenes still carry repetition and pictures; capping crescendo diction could shorten peaks — LENGTHEN's unspent-encounter extension still carries length.

How we'll know it worked: PRIMARY deficit must fall in BOTH replicates, with neither R2 quoting a Latinate crescendo as main distance.

```
parent: 1002d7b5
instrument: 2026-09-06 Carr-distance panel
```
