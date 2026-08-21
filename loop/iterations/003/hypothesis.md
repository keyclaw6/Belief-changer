## Failure evidence
Cluster 5 — Cross-chapter re-argument (mutated Cluster 4) — systemic/positional (mid + late), book-arc still FAIL despite iter-002 closure of 001 symptoms. Judge sources: book-arc Gap 2 (Sunlit Table re-litigation) + Gap 3 (Willpower Method re-install at plan Ch.14), corroborated by voice C12-Gap2. Gap 2: C6 installs full verdict "Dopamine is not pleasure. Wanting is not liking." then C11 rebuilds second full section "THE BRAIN'S QUIET TRICK: WANTING IS NOT LIKING" (chapter-12 lines 184–194) on same E-05/E-06 ground. Gap 3: C1 already defines Willpower Method at length, then plan Ch.14 opens "Let me define it exactly… the Willpower Method is any method that says…" (~40 lines, chapter-15 lines 38–44) as a full re-install despite card listing only echo M-11. Same failure class as 001 (settled material re-argued), different triggers — not flagged as S-xx duplicate in 002 but as mechanism row re-assignment and anti-method job text.

## Root cause
Factory produces this because `prompts/master-plan-skill-v2.md` § Compact chapter cards permits it. The bullets `- the primary persuasive job declaration and the objection or justification it resolves` and `- evidence-ledger IDs, including the limits the chapter must preserve` allow any E-ID to be re-listed as owned evidence and any job to be declared as `enacted transition — dissected/re-defined` even when that verdict was already landed. Trace evidence: Ch.11 card (`traces/chapter-12/chapter-card.md` line 8) re-lists `E-05, E-06 (wanting/liking)` after Ch.6 card already debuts E-05 for full demolition; Ch.14 card (`traces/chapter-15/chapter-card.md` lines 1–2) job = "willpower's mechanics dissected" while mantra line says echo M-11 only — job contradicts echo-only intent. The skill's repetition law governs card authoring but does not constrain chapter-job text or evidence re-list scope, and it allows speakable echo parentheticals (Cluster 1) to be written onto the card. Writer executes card faithfully and rebuilds.

## Targeted fix
Edit ONE file: `prompts/master-plan-skill-v2.md` — section `### Compact chapter cards`.

Replace the two permissive bullets with constrained versions and add a binding rule that supersedes them (no other file touched). Diff:

```diff
- - the primary persuasive job declaration and the objection or justification it resolves;
+ - the primary persuasive job declaration and the objection or justification it resolves — if the verdict was already landed in an earlier card (e.g., wanting/liking mechanism E-05/E-06, Willpower Method definition), this job MUST be declared as token-only echo by ID, never as enacted transition — dissected / installed / re-defined / rebuilt;
...
- - evidence-ledger IDs, including the limits the chapter must preserve;
+ - evidence-ledger IDs, including the limits the chapter must preserve — any ID already used to land a full demolition may appear later only as ID-only token echo (≤1 sentence reference by ID, no rebuilt demo, no speakable parenthetical template such as 'recalled by name' or 'by name in one sentence here'), never as owned evidence for a new demolition;
```

Add immediately after the bullet list, before "These are semantic authorities…":

`A card may never re-own a settled verdict for a second full demolition. Settled evidence rows and settled jobs are invoked by ID token only. Cards must not write human-readable echo instructions onto the card; the ID annotation itself is the instruction. This rule supersedes the prior unrestricted evidence-list and job-declaration bullets.`

This is not the reverted iter-002 sentence (mantra/scene/evidence debut-once + "echo token ≤1 sentence") — that sentence is not on the factory and is not reused. This time the mechanism binds the *chapter job declaration* and *evidence re-list annotation* and bans speakable parentheticals on the card itself, which iter-002 left unconstrained.

**Why this component:** The trace names root component plan-card, and the card is authored by master-plan-skill-v2.md — fixing the writer prompt cannot stop the card from assigning a full rebuild job or re-owning E-05/E-06.

## Predicted impact
What will improve: Cluster 5 will close because Sunlit Table (Ch.11) and Willpower (Ch.14) cards can no longer legally own E-05/E-06 or declare a dissect/re-define job after Ch.6/Ch.1 land them — later chapters must invoke wanting/liking and Willpower Method by token only, leaving book-arc Gaps 2–3 without re-argument. Cluster 1 will also close as side-effect because the ban on speakable parentheticals removes the "recalled by name here / by name in one sentence here" template at the source.

What might regress: If the rule is over-strict, a later chapter that legitimately needs to extend a mechanism with new E-IDs could be forced to token-only echo; the reviewer gate must distinguish new inference from repeated demolition.

How we'll know it worked: The owning book-arc judge should no longer flag a second full wanting/liking section in C11 or a 40-line Willpower definition in C14, and should record token-only recalls (≤1 sentence, ID-referenced, no parenthetical) instead; voice C15–C18 should no longer literalize echo-law placeholders.
