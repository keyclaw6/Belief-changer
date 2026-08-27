# Hypothesis — Iteration 012

source: hypothesizer (from 011 traces)

## Failure evidence

011 voice-emotion merged **10 blocking `instruction-paperwork`** (A 5, B 5) and **3 blocking `factory-speech`** on the same frozen spine strings (subset of merged 6). Judges quote plan-frozen compliance paste at emotional peaks:

- A ch06 / I-05 debut: `"5. IGNORE ANY ADVICE THAT CONFLICTS WITH THIS METHOD — INCLUDING DIETS, WILLPOWER TIPS, AND STORIES FROM PEOPLE WHO QUIT BY SUFFERING; IF YOU HAVE DIABETES, AN EATING DISORDER, OR ARE UNDER MEDICAL NUTRITION THERAPY, CONTINUE TO FOLLOW YOUR CLINICIAN'S ADVICE ON FOOD AND MEDICATION — THIS BOOK DOES NOT REPLACE MEDICAL CARE."`
- A/B ch18 final checklist (**8/10** blocking): `"**5. IGNORE ANY ADVICE… this book does not replace medical care.**"`; `"**7. DO NOT USE SUBSTITUTES… this is not medical advice.**"`; `"**11. FORGIVE A BLIP… this method does not override medical care.**"`
- B ch15 / A/B ch18 on I-06: `"6. NEVER DOUBT YOUR DECISION TO QUIT BAD SUGAR — Once you make the vow, never reopen the question; referral to clinician exception as in I-05 still applies."`

Cluster spread: systemic paperwork (C06 A, C15 B, C18 both); positional factory-speech on I-06 (C15 B, C18 both). Belief/journey/book-arc hold 18/18 both books.

## Root cause

Trace analysis pins both KEEP clusters to the **plan instruction spine**. The factory rule that causes this is `prompts/master-plan-skill-v2.md` § Lexicon and instruction spine: *"Any instruction that could conflict with qualified clinical care must contain its safety exception in the frozen wording."* That fuses safety tails and ID cross-refs into frozen instruction rows, then the writer's verbatim-recap license pastes them into ALL-CAPS peaks. Unchanged across 009–011 while the plan artifact was reused.

## Targeted fix

**File:** `prompts/master-plan-skill-v2.md` — replace the instruction-spine paragraph (see `change.diff`).

**Why this component:** Trace names plan as root; this plan-skill sentence is the upstream factory rule. Regenerating the plan is required (artifact is not the hypothesis).

## Predicted impact

**What will improve:** Regenerated plan removes inline liability language from I-05/I-07/I-11 and the I-06 `as in I-05` cross-ref. **`instruction-paperwork` blocking** at C06/C15/C18 must fall in **both** replicates. **`factory-speech` blocking** on I-06 ID cross-ref at C15/C18 must fall in **both**.

**What might regress:** Clinical limits could surface less prominently if advisory routing is thin.

**How we'll know it worked:** voice-emotion `instruction-paperwork` blocking merged near 0 (from 10) in both books; no blocking `factory-speech` on `as in I-05` at C15/C18 in either replicate; belief/journey/book-arc remain PASS.
