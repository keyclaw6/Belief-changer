## Failure evidence

Lane `carr-distance`, book scope, both subjects — the only KEEP-eligible class present in both (sugar `score-deficit` 40, smoking 28; no blocking anywhere; comparison `partial` 3/4 and `missing` 0/2 are not in both; no noted class ≥12 in both).

Reason 3 of both 041 Carr-distance reports names the same cluster:

- Sugar: *"If you live with diabetes or pre-diabetes, take medicine that affects blood sugar or appetite, are pregnant, live with a past or present eating difficulty, or have any medical condition where changing what you eat could carry risk, talk to your clinician first…"* vs *"FOLLOW ALL THE INSTRUCTIONS"* — "ours inserts repeated mid-argument clinician disclaimers".
- Smoking: *"If you feel ill or worried about stopping, speak to your clinician; I give no medical orders here"* vs *"If you have any difficulties contact your nearest Allen Carr's EASYWAY center"* — "ours inserts repeated mid-argument clinician disclaimers that break the voice where Carr never leaves the method and routes difficulty back to the method."

Spread (grep of 041 chapters): sugar 12/13 chapters carry a clinician/doctor/not-a-diet disclaimer (CH-04 *"I am not your clinician and this is not care for teeth or blood or weight"*, CH-05 *"I prescribe no meals, no portions, no windows. I am not your clinician."*, CH-06 same again); smoking 9/14 (CH-06 *"for anything medical, speak to your own clinician, I give no medical orders"*, CH-07 and CH-09 verbatim repeats of the same sentence). Carr: GSBS has one such line in the whole book (ch. 17, *"If you are on medication, talk to your GP"*), at the quit; Easyway smoking routes difficulty to the method, never to a doctor.

The other four 041 reasons (appendix scare, soft-contract promise, fragment-chain sensory catalogue, private vocabulary) are already addressed by the unmeasured CH-01 card rule + Part B plain-Carr text in the files; 042 regenerates plans and chapters so those fire. The clinician cluster is the one reason those rules do **not** close, because its seed is still live in the same files.

## Root cause

Three factory instructions jointly produce one disclaimer per chapter:

1. `prompts/chapter-writer.md`, Method and voice, evidence-honesty bullet: *"Add one short spoken clause only when a hard fact would otherwise be taken as a sentence on this reader."* sits two sentences before the new (unmeasured) *"never write a mid-argument clinician disclaimer."* The writer is licensed to speak one relief clause per hard fact and told to internally hold every ledger row's *safety limit*; every 037 ledger row ends *"…; honour CA-SAFE"* (sugar: 20 rows, e.g. *"anyone with diabetes / medication follows clinician; honour CA-SAFE"*). Spark cashes the license as exactly the clinician sentence the judge quotes. The ban and the license coexist; the license wins at the peak.
2. `prompts/master-plan-skill-v2.md`, Compact chapter cards: *"method, safety, and originality guardrails specific to this move (safety-limit IDs and originality only…)"* and Lexicon/instruction spine: *"cards cite the advisory ID in their safety guardrails field only."* Result in both 037 plans: **every** card carries `guardrails: safety CA-SAFE …` (sugar CH-05 *"no diet prescription"*, CH-06 *"no eating plan, no good-food / bad-food moralising"* → the writer's *"I prescribe no meals… this is not a diet"*). The advisory is routed 13/14 times instead of once.
3. `prompts/style-guide.md` §B10 *Hard facts, then relief*: *"One short spoken clause only if the scare would otherwise be taken as a personal sentence."* — the same license, duplicated in the writer's second runtime input.

Carr's own relief clause is a method disown (*"I don't want you to use this information to be frightened"*), not a referral. The factory converts "one spoken clause" into a clinician referral because the only spoken-safety text it holds is CA-SAFE.

## Targeted fix

**Change 1 (PRIMARY)** — `prompts/chapter-writer.md` — class `carr-distance` `score-deficit` — component: Method and voice, evidence-honesty bullet — both subjects. Replace

> Honour those limits by not overclaiming. Never narrate study design, grades, or methods — in the body or in SUMMARY. Add one short spoken clause only when a hard fact would otherwise be taken as a sentence on this reader. Clinical and eating-disorder limits live in one front-matter note (the plan-wide advisory). Never paste CA-SAFE / CA-01 / PRACTICAL SAFETY GUARDRAIL titles mid-chapter, never add "this notice is not part of the belief argument," and never write a mid-argument clinician disclaimer.

with

> Honour those limits by not overclaiming and by saying nothing about them. Never narrate study design, grades, or methods — in the body or in SUMMARY. When a hard fact would otherwise read as a sentence on this reader, the only spoken relief is Carr's: tell the reader not to change from fear, and that the method takes care of it. A safety limit or the plan-wide advisory on your card is held silently — never spoken as a clinician referral, "speak to your doctor," "I give no medical orders," "I am not your clinician," "this is not a diet," "I prescribe nothing," or any sentence about what this book does not advise. The clinician referral appears in the book exactly once, as the front-matter advisory, plus one plain sentence at the vow only when that card assigns it. Never paste CA-SAFE / CA-01 / PRACTICAL SAFETY GUARDRAIL titles mid-chapter and never add "this notice is not part of the belief argument."

**Change 2** — `prompts/master-plan-skill-v2.md` — class `carr-distance` `score-deficit` — component: Compact chapter cards, guardrails bullet — both subjects. Replace

> - method, safety, and originality guardrails specific to this move (safety-limit IDs and originality only — never speakable register/job operators, never a boxed CA-SAFE/CA-01 title);

with

> - originality guardrails specific to this move (never speakable register/job operators, never a boxed CA-SAFE/CA-01 title). The clinical advisory ID is cited on exactly two cards: the card that prints the boxed front-matter advisory, and the vow card, which may assign one plain spoken sentence telling a reader on medication to involve their doctor. No other card carries a safety field; ledger safety limits are held by the writer silently and are never restated on cards;

and delete its duplicate in Lexicon and instruction spine: the clause *"cards cite the advisory ID in their safety guardrails field only — "* (the sentence continues *"they never paste the boxed workshop title…"* unchanged).

**Change 3** — `prompts/style-guide.md` — class `carr-distance` `score-deficit` — component: §B10 structural slot *Hard facts, then relief* — both subjects. Replace

> One short spoken clause only if the scare would otherwise be taken as a personal sentence.

with

> The only spoken relief is Carr's own: tell the reader not to change from fear. Never a clinician referral or a sentence about what this book does not advise.

**Why this component:** the judge quotes writer sentences, and the writer's own bullet currently contains both the ban and the license that overrides it — deleting the license is the subtraction that lets the already-present ban act; Changes 2–3 remove the two upstream feeds so the ban is not fighting 13 cards and a duplicate rule.

Retry status: none of 020–040 touched this instruction; not a replay. Pre-spend GSBS control: `carr-distance` on GSBS as both texts (must be 100/0); construct check on GSBS chapter-17's single GP line at the quit — the proposed rule permits exactly that placement, so the control does not fire. Bound to `parent:` below; the 042 delta also includes the unmeasured CH-01 + Part B rules (recorded, cannot be separated).

## Predicted impact

PRIMARY: Carr-distance `score-deficit` falls in BOTH subjects vs 041 (sugar 40 → ≤32, smoking 28 → ≤22), with Reason 3 no longer a clinician-disclaimer quote in either report. Secondary (recorded, not decisive): voice noted `factory-speech` 6/9 falls (mid-argument clinician disclaimers are in that class's definition); grep of `clinician|doctor|not a diet|I prescribe` drops from 12/13 and 9/14 chapters to ≤2 chapters each. Comparison `partial` 3/4 is remeasured on regenerated plans and predicted flat-to-noise; no change targets it.

What might regress: the sugar book loses per-chapter diet/eating-disorder hedges, so reviewer `OVERCLAIM` may fire more often on CH-04–06 nutrition facts (it governs facts, not the promise — that is the intended route); if the front-matter advisory is not printed because the plan-writer puts it on no card, the book carries zero medical caveat — Change 2 names the owning cards to prevent that. Residual sugar distance (private Nibbler/Sweet Con vocabulary vs Carr's Little/Big Monster, also G04-M1 PARTIAL) is a Fork 1 style-guide design choice, one-book in 041, and is not touched here.

How we'll know it worked: `score-deficit` must fall in BOTH replicates (any drop is material for this class per Step 6), and neither Carr-distance report may quote a clinician referral outside the front-matter advisory or the vow.

```
parent: 4e71f6e9418c2fd2900ec3b32ba0fb462f2000a3
instrument: 2026-09-06 Carr-distance panel
```
