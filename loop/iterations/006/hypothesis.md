## Failure evidence
Cluster 1 Factory scaffolding / speakable craft (residual) — systemic **voice 0/18 PASS in 005 (regression from 3/21 in 004)**. Voice-emotion FAIL every chapter; representative gaps quoted: C02 Gaps 1–2 `"A trap question"` (chapter-02.md line 16) + `"killer-line pair"` (line 112) + `future-pace` verb, C04 Gap 2, C06 Gap 1 `"the fact-assertion that seals it"`, C11 Gap 2 `future-pace`, C12 Gaps 1–3 `"the explicit disown you were promised"`, `"Each answer is two to six sentences"`, C13 Gap 2 `"We have demolished. Now we install the positive authority"`. Cluster 3 Persona codes — systemic C02–C06, C09, C17: voice C02 Gap1 `P-02 lives on that line`, C04 `P-04's 3pm desk`, C06 `Are you P-01? / P-02?`, C09 `P-02, this is your moment`, C17 `P-04 knows…` / `P-03's voice`. Both classes persist despite iter-005 literal closure of `future-pacing` hyphen, `One killer pair. Land it.`, `argue-to-compress` — mutated to verb/metadata forms.

## Root cause
Factory produces this because residual leaks now trace **upstream to plan-card speakable fields** embedded in runtime `chapter-*/user.txt`, contradicting the writer ban. Trace 005 evidence: iter-005 hypothesis correctly added silent-execution ban to `prompts/chapter-writer.md` and traces prove it landed (`traces/chapter-02/system.txt` lines 45–49, 75–77, 96–100 ban `trap question`, `killer-line/pair`, `future-pacing`). Upstream contradiction: C02 card `traces/chapter-02/chapter-card.md` line 4 `devices: trap question, pronoun triangle, killer-line pair` + `enacted discovery: trap question` (also `traces/chapter-02/user.txt` line 218 identical), C08 card `devices: fact-assertion, future-pacing, killer-line pair at inversion`, C12 card `2–6 sentence demolitions`, C04 card `encounter: P-04's 3pm desk` / `personas: P-02, P-01`. No existing plan-reviewer gate validates or sanitizes these fields; the model obeys card vocabulary at peaks over system ban. Twin cluster 3 shares same mechanism (persona IDs in card encounter/persona lines). Writer-prompt was root in 000–004; 005 moved layer to plan-card.

## Targeted fix
**File: `prompts/master-plan-reviewer-v2.md` — one causal change: add binding Speakable Card Sanitization Gate (and delete any allowance for verbatim craft/persona tokens in cards).**

Insert as new final checklist section (supersedes any generation-phase permission to write device/persona literals onto cards):

```markdown
### Gate 4 — Speakable Card Sanitization (BINDING — REJECT & REWRITE)

No Compact chapter card may contain reader-facing factory vocabulary. REJECT the plan if any card field (`devices`, `enacted discovery`, `encounter`, `personas`, `mantra`, `budget`, `scene` label) contains speakable craft/persona/template literals. Forbidden literals (case-insensitive, any hyphen/spacing/verb form): `trap question`, `killer-line`, `killer pair`, `killer-line pair`, `future-pac`, `fact-assertion`, `pronoun triangle`, `P-01` / `P-02` / `P-03` / `P-04`, `Warm rationale:`, `2–6 sentence`, `delivery budget`, `argue-to-compress`, `chapter verdict`.
- Replace with behavioral, experiential instruction that executes invisibly. Examples: instead of `devices: trap question` write `open with a present-tense lived moment where the reader catches themselves hiding/managing sugar and feels the trap without naming it`; instead of `personas: P-02` write `personas: the member who says "I don't keep it in the house" (never use P-xx ID)`.
- Persona/encounter fields may use only anonymous human handles (`the 3pm-desk parent`, `the evening grazer`), never `P-xx` IDs. If an `encounter:` line contains an ID, rewrite to handle and remove ID.
- Do not copy this gate's forbidden list into reader prose. Do not surface the gate name. After rewrite, re-validate card still delivers job with Carr register.
```

This is the only file edited. No change to `prompts/master-plan-skill-v2.md` (3-strike for re-argument class does not apply here; this is craft/persona class) and no repeat of iter-005 `prompts/chapter-writer.md` silent-execution wording.

**Why this component:** The writer ban already exists and traces prove it landed, but plan cards embedded in `user.txt` contradict it at runtime; the reviewer is the last gate before generation that can strip speakable device/persona/budget strings, while writer-prompt (iter-005) cannot close an upstream card source and plan-skill would generate the same strings.

## Predicted impact
**What will improve:** Clusters 1 and 3 will close because cards no longer prime the model with speakable craft labels and persona IDs — the same upstream source for both. Voice-emotion should rise from 0/18 because peaks no longer show `trap question` / `killer-line` / `future-pace` / `P-xx` ventriloquism; 005 headline literals stay closed and mutated forms stop.

**What might regress:** If reviewer over-strips, C10 Mantra-echo and C08/C07 behavioral cues could weaken; mitigated by translating to experiential instructions rather than deleting job.

**How we'll know it worked:** The owning voice judge no longer quotes craft labels or `P-xx` in gap excerpts, prose grep for `P-0[1-4]`, `trap question`, `killer-line`, `future-pac`, `fact-assertion`, `Warm rationale:` returns zero across 18 chapters, and voice PASS rate recovers from 0/18 while belief-mechanic stays 17–18/18.
