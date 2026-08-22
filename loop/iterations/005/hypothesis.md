## Failure evidence
Cluster 6 — Factory scaffolding in reader prose — systemic 18/21 voice-emotion FAIL in iter-004 (down from 6/20 PASS in 003 to 3/21 PASS). Judges quote speakable craft/factory diction at emotional peaks as failure: C07 Gap 1 `“One killer pair. Land it.”` and `“Try the masking falsification exercise with me now… brief staging, not willpower”`; C02 Gap 1 `“Future-pacing for a moment”`; C15 Gap 1 `“Let me land this chapter's verdict”`; C06 Gaps 1-4 meta-framing/production jargon; C11 Gap 1 meta-commentary; C14 Gaps 1-2 curriculum announcement/token staging; C19 Gap 2 factory token checklist; C20–C21 instruction/meta recap. Same persistent class as 000 Cl.2, 001 Cl.1, 002 Cl.2, 003 Cl.7 — now dominant voice lane.

## Root cause
`prompts/chapter-writer.md` Binding chapter craft + Method and voice create a dual contract that teaches speakable craft labels. `Method and voice` line: `“answer with two or three trap questions whose only honest answer concedes the point”`; Binding craft bullet 2: `“A debut gets its full argue-to-compress beat; an echo is brief and is never re-argued”`; bullet 7: `“Use fact-assertion, self-answered questions, trap questions, ventriloquism, inversion, one killer-line pair per major argument, reassurance–challenge, future-pacing, permission paradox, credit reassignment…”`; lines 91-93 `“one killer-line pair per major argument”`. Ban at lines 53-55 forbids ledger/device codes but coexists with these speakable instructions, so the model obeys them literally and writes the labels at peaks. Trace analyzer confirms downstream `chapter-08.md` line 136 verbatim leak and `traces/chapter-*/system.txt` unchanged. Not iter-001 evidence-honesty clause (different clause — this is Binding craft diction, which learnings marks as unpaid).

## Targeted fix
File: `prompts/chapter-writer.md` — one causal change: make craft execute silently and delete speakable craft diction. Replace canonical instruction and delete its exact duplicates in the same file.

**Hunk 1 — Method and voice paragraph 4:** Replace
`Ventriloquize the strongest reader objection, answer with two or three trap questions whose only honest answer concedes the point, perform the credit inversion, and land one short verdict.`
with
`Ventriloquize the strongest reader objection, answer in a way that leaves only one honest answer, perform the credit inversion, and land one short verdict. Execute all craft silently — never write craft labels, device names, persona codes, beat names, or assignment language (trap question, killer-line/pair, argue-to-compress, future-pacing, device, brief staging, your card assigns, persona codes P-01…P-04) in reader prose.`

**Hunk 2 — Binding chapter craft bullet 2:** Replace
`A debut gets its full argue-to-compress beat; an echo is brief and is never re-argued.`
with
`A debut gets its full argument-then-compression rendered as lived reader experience with no beat label; an echo is brief and is never re-argued. Never surface the beat/device name.`

**Hunk 3 — Binding chapter craft bullet 7:** Replace
`Use at least one card-assigned concrete analogy or scene to do the argumentative job your card declares for it. Use fact-assertion, self-answered questions, trap questions, ventriloquism, inversion, one killer-line pair per major argument, reassurance–challenge, future-pacing, permission paradox, credit reassignment, and warm imperative instruction where your card assigns them.`
with
`Use at least one card-assigned concrete analogy or scene to do the argumentative job your card declares for it. Execute assigned rhetorical moves silently in Carr voice — render them as direct lived experience and verdict only; never label, count, or announce the move (no “killer pair,” “trap question,” “future-pacing,” “device,” “beat,” etc.) and never write meta-commentary about the assignment.`

No other file touched. This supersedes the prior speakable wording; evidence-honesty clause from iter-001 is untouched.

**Why this component:** Voice-emotion owns 18/21 FAIL from writer-prompt speakable craft (5-iteration persistent root per trace), while plan-skill re-argument has 3 consecutive REVERTs and must pivot per learnings — fixing writer-prompt execution-silently closes the dominant voice lane without repeating the failed plan-skill class.

## Predicted impact
What will improve: Cluster 6 (and overlapping Cluster 9 device-label leaks like C07 `killer pair`/`brief staging` and C02 `Future-pacing`) will close because the writer no longer has speakable templates to ventriloquize; voice-emotion PASS should rise from 3/21 toward 000-baseline plus, and Cluster 10 persona-code surfacing will reduce as the silent-execution ban now explicitly covers `P-01…P-04` and `your card assigns`.
What might regress: Trap-question force could soften if the model renders “only honest answer” too vaguely without the explicit 2-3 question scaffold; mitigated because the card still assigns the job and the replacement retains the functional requirement without the label.
How we'll know it worked: The voice-emotion judges in C01–C07, C09–C12, C14–C15, C19–C21 should no longer quote `killer pair`, `argue-to-compress`, `trap question`, `future-pacing`, `brief staging`, or `chapter verdict` as failure evidence; those gaps disappear while belief 21/21 holds.
