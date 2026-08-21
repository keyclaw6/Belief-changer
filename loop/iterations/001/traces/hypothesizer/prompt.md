# Hypothesizer call

## Contract prompt (system)
```
# Hypothesizer

You are the hypothesizer for the book factory auto-tuning loop. You receive
the trace analysis (causal clusters mapped to factory components) and the
accumulated learnings from previous iterations. Your job: propose ONE causal
change that will close the highest-priority cluster.

## Your inputs

1. **Trace analysis** — causal clusters with root components and evidence
2. **Learnings** — `loop/learnings.md` (what was tried, what worked, what
   failed)
3. **Current factory state** — the current editable prompts and config

## Your task

Propose exactly ONE hypothesis using the 4-field evidence contract:

## Failure evidence
[Quote the specific judge findings behind the causal cluster. What exactly
is wrong with our output? Be precise — quote passages, name the cluster and
its spread.]

## Root cause
[Why does the factory produce this cluster? Reference the trace analysis
evidence. Be specific about which file and which section is responsible.]

## Targeted fix
[The exact change. Which file. Which section. Write the actual replacement
text or diff. One causal change only.]

**Why this component:** [One sentence: why fix THIS component rather than
a different one?]

## Predicted impact
[What will improve: "Cluster X will close because..."]
[What might regress: "This could weaken Y because..."]
[How we'll know it worked: "The owning judge should now see..."]

## Rules

- **Check learnings first.** Never repeat a hypothesis that already failed.
  If a similar approach was tried and reverted, explain why THIS time is
  different (different root cause, different target, different mechanism).

- **One causal change.** Edit one file. Multiple hunks are allowed only to
  replace a canonical instruction and delete or redirect exact duplicates
  of that same instruction. Do not change a second behavior.

- **Follow the diagnosis.** Target the root component named by the trace
  analyzer unless you can quote trace evidence that contradicts it. Do not
  rerank components through a generic upstream preference.

- **Prefer subtraction.** Delete or replace the instruction that caused the
  failure. Add a new rule only when no existing instruction can be made
  correct, and name the current text that the addition supersedes.

  Not: "Add another certainty rule to style-guide.md."

  Instead: "Replace [quoted causal instruction] with [exact text], and
  delete its exact duplicate in the same file."

- **Predict specifically.** Not "voice will improve." Instead: "The voice
  judge will no longer find the auditor register in opening passages
  because the planner no longer instructs an evidence-policy opening."

## Priority ordering

If multiple clusters exist, prioritize:
1. Systemic clusters that block belief change (the reader's belief doesn't
   shift, across many chapters)
2. Clusters that break the cumulative journey or the arc (book-arc lane)
3. Clusters in voice effect (reads like AI instead of landing Carr's effects)
4. Everything else

## Output

Write the complete hypothesis in the 4-field format above. Nothing else.

```

## User message
```
## Founder inbox hypothesis (single change, already applied)
# Hypothesis: Writer scaffold firewall — research-ledger vocabulary never surfaces in reader prose

**Change:** `prompts/chapter-writer.md` (evidence-honesty clause, ~line 48):
"Preserve every evidence grade …" → internally hold grades/limits to govern
claim scope, and never surface ledger vocabulary in reader-facing text (no
ledger/source IDs, no SUPPORTED/MIXED/CONTESTED grades, no persona codes, no
scene/mantra/device-code strings, no internal drafting or craft labels, no
"Permitted/Prohibited inference … limit" headings) — convert each boundary
into plain Carr-voice prose. Applied 2026-08-17 after dual-subagent root-cause
verification (reports: /tmp/opencode/rca-report.md, /tmp/opencode/rca-verify.md).

**Because:** Baseline 000 trace analysis, clusters 1–2: chapters transcribed
plan evidence-ledger rows and research taxonomy verbatim into reader prose
(worst: chapters 08, 09, 10, 14 — full ledger dumps/recaps, e.g.
chapter-08.md:283, chapter-14.md:280–298). Root cause is factory-internal:
the plan legitimately carries IDs/grades for traceability, and the writer
contract's "preserve" wording made the writer transcribe them. Writer calls
were forensically pure — no harness contamination.

**Prediction:** Regenerated chapters contain zero ledger IDs, grades, persona
codes, or drafting labels in prose (voice-emotion lane's "evidence-grading
register" failure class disappears); belief-mechanic stays PASS (evidence
honesty is preserved internally, only the register changes); no lane shows a
material regression. Research and plan are reused unchanged (change touches
only the writing stage).


## Previous iteration's trace analysis
# Trace Analysis — Iteration 000 (Quit Sugar)

**Scope:** 54 chapter judgments + book-arc + 3 A/A judgments; accepted plan (`traces/plan.md`); generation traces for C01/C02; research synthesis. **learnings.md is at baseline** (no prior iterations), so the 3×-component persistent rule does not trigger; no PERSISTENT flag.

## Cluster summary

| Causal cluster | Spread | Judge sources | Root component | Priority reason |
|----------------|--------|---------------|----------------|-----------------|
| 1. Evidence-grading scaffold leaked verbatim into reader prose | systemic (nearly every evidence-bearing chapter; both standard + AA ch01) | voice C01(note), C02-G2, C04-G1, C05-G2, C07-G3, C10-G3, C11-G1/2/3, C12-G1/2/3, C13-G1/3/4, C14-G1, C15-G2, C16-G1/G4, C17-G1, C01-AA-G1; reader C03-G1, C04-G1/2, C07-G1, C08-G1, C09-G1/2, C10-G1, C11-G1, C13-G1, C14-G1/2, C15-G1, C17-G1; belief C13(reg.note), C04(hedge note) | **writer-prompt** | Scientifically the book's voice is *correct* except here, but this breaks the Carr earned-authority register at the emotional climaxes of nearly every chapter — the central deliverable of the method. Most pervasive defect in the run. |
| 2. Factory-internal taxonomy & drafting scaffolding leaked into reader prose | systemic (spans voice-emotion C02/C04/C05/C07/C08/C10/C11/C16/C17/C18; reader C06) | voice C02(note), C04-G2, C05-G1/G2, C07-G1/2/4, C08-G1/2, C10-G1/2/4, C11-G4/5, C16-G2/3/4, C17-G2/3/4/5, C18-G1/2/3; reader C06-G1/2; belief C10(note) | **writer-prompt** | Exposes the factory's scene/persona/instruction/mantra codes and craft directives ("Killer-line pair.", "S-01", "P-03", "as Carr does") at the exact peaks the reader must feel as one person speaking. Second-most systemic failure; directly destroys the one-person voice. |
| 3. Cross-chapter re-argument of settled scenes/evidence instead of invoke-by-token | positional across front (C01→C02) and mid (C05→C11); arc-level | book-arc Gap1/2; reader C02-G1/2/3; voice C02-G2; reader C15-G2 (caged lion/seatbelt/triad at C14) | **plan** | The plan schedules the same scene (S-04, S-09) and evidence (E-11; E-01/E-03) into adjacent/straddling chapters with no echo-not-rebuild rule for scenes/evidence; the book stalls its opening and re-defeats its decisive scene twice. |
| 4. Local grammatical/lexical fabrication in chapter 2 | local (C02) | voice C02-G1/G3 | **model** | Broken grammar ("We trapped.") and garbled coinages ("marksman-shipped") at the blame-removal and shame-ending peaks; inputs adequate, so it is generation-level. Lowest priority; local. |

---

## Cluster 1 — Evidence-grading scaffold leaked verbatim into reader prose

**Judge sources:** voice-emotion C01 (the 14%/12% "evidence-report" drift), C02 Gap 2, C04 Gap 1, C05 Gap 2, C07 Gap 3, C10 Gap 3, C11 Gaps 1/2/3, C12 Gaps 1/2/3, C13 Gaps 1/3/4, C14 Gap 1, C15 Gap 2, C16 Gaps 1/4, C17 Gap 1, C01-AA Gap 1; reader-journey C03 Gap 1 (TO column), C04 Gaps 1/2, C07 Gap 1, C08 Gap 1, C09 Gaps 1/2, C10 Gap 1, C11 Gap 1, C13 Gap 1, C14 Gaps 1/2, C15 Gap 1, C17 Gap 1; belief-mechanic C13 (register note) and C04 (hedge note).

**Shared symptom:** Reader-facing prose carries the implementation-level evidence taxonomy verbatim — `SUPPORTED/MIXED/CONTESTED`, `Permitted inference / Prohibited inference`, `Safety`/`Scope`/`Empirical limit`, evidence IDs (`E-07`, `E-13`, `E-19`), and clinical-consent vocabulary (`DSM-5`, `self-report`, `cross-species`, `animal microdialysis`, `population-level`) — usually at the emotional climax. voice C04 Gap 1 quotes the decisive phrasing: *"this is the grade, the scope, the safety limit you must keep with you … So the mechanism is SUPPORTED/MIXED, not a diagnosis for you. The permitted inference is this … The prohibited inference is that every slump is medical hypoglycemia requiring sugar."* voice C16 Gap 1: *"That is E-07, SUPPORTED, rat model, author characterization. Permitted inference … Prohibited inference …"* voice C14 Gap 1: *"That is CONTESTED, perspective review … That is SUPPORTED, animal microdialysis … `Seems to' stays."*

**Distinct effects:** (a) The reader is **audited**, not relieved — voice C13: *"at the peak of the memory-reassignment … the prose stops being one person talking and becomes an audit against a research rubric."* (b) Judge reader C14 Gap 2 notes the cumulative **hedge-reversal**: certainty is stated and immediately walked back ("It is not yet proven … we claim only … not settled fact"), so the ready-gate chapter that must compound conviction instead re-negotiates it. (c) reader C08/C09/C10/C11 additionally record the block is **placed after the inversion peak** rather than as its engine ("a sudden drop from escape-elation to analytical receipt"), i.e. placement is part of the same dumping habit. (d) The same defect reproduces in the A/A variant (voice C01-AA Gap 1: *"On validated self-report scales for highly palatable foods — not a medical diagnosis, just people's own answers …"*), so it is not specific to the main model run.

**Root component:** writer-prompt.

**Evidence:** The writer-prompt system contract (`chapter-01/system.txt` / `chapter-01/prompt.md`), "Method and voice"), lines 48–53: *"Evidence honesty outranks force. **Preserve every evidence grade, provenance status, permitted inference, prohibited inference, empirical limit, and safety limit** assigned by your card's evidence-ledger entries."* There is no accompanying instruction to *render* those fields into plain Carr prose or to keep them out of the reader voice. The style guide — the reusable craft rule — says the opposite of what lands: §9 **Never**: *"Never bog the prose down in a literature review. Quarantine citations; keep the argument clean and emotional"* and Fork 3: *facts arrive as "The fact is…", never as hedged citations*. So the craft rule already demands clean register, but the writer-prompt's mandatory "Preserve every evidence grade … permitted inference …" overrides it with no translation/rendering rule — the requirement to keep the grading tongue is absent at the point of execution. The downstream landing wrong is identical across responses (verified in `chapter-02/response.md` lines 120–125, the `SUPPORTED … within that self-report boundary … What must you not take? … Do not turn a model into a diet plan` block, and `chapter-01/response.md` line 46).

**Mechanism:** The plan/evidence ledger stores grades + permitted/prohibited-inference language (present in the writer's inputs). The writer-prompt then *commands* the writer to "preserve every evidence grade … permitted inference, prohibited inference, empirical limit, and safety limit" without telling it to translate these into the reader's idiom or quarantine them (per style-guide §8/§9). The model obeys the command literally, seasoning every factual beat with the proof-roster. Because the prompt-outweighs-guide relationship makes the grading mandatory-but-untranslated, the required move (clean, confident Carr register) first goes absent/wrong in the writer-prompt, not the model. The style guide is adequate and was itself present; it was overridden.

*Adjacent note (not separately rooted):* the plan-frozen clinical advisory reads as consent paperwork (voice C13 Gap 2, C15 Gap 1: *"referral to clinician exception as in I-05 still applies"*, *"If you have diabetes, an eating disorder, are under medical nutrition therapy, or take medication affected by diet …"*). Its legalese is plan-era frozen wording; the *cross-references* inside it are the Cluster-2 leak. Judges consistently ranked this secondary to the grading apparatus.

---

## Cluster 2 — Factory-internal taxonomy & drafting scaffolding leaked into reader prose

**Judge sources:** voice-emotion C02 (craft terms), C04 Gap 2 (`P-02 / P-04`), C05 Gaps 1/2 (`Killer-line pair.` `Short sentences` `That is E-13` `That is S-01 … the flagship illusion-exposer`), C07 Gaps 1/2/4 (`Short sentences for the peak. Land and stop.` `Killer-line pair. Build, then verdict.` `S-01` `I hear you, P-03` `the axis switch we installed`), C08 Gaps 1/2 (`Killer-line pair. Build, then verdict.` `Future-pace with me.`), C10 Gaps 1/2/4 (`I will land this at full force, as Carr does` `This is S-12` `He was the P-02 in your book` `That is the indictment widened and the blame relocated`), C11 Gaps 4/5 (`Because P-03 does not only eat in the dark. P-03 eats when love is in the room.` `Carr used it`), C16 Gaps 2/3/4 (`The sentence is ALL-CAPS … on purpose` `That is M-07, your canonical sensory definition. It debuts` `Fork 5`), C17 Gaps 2/3/4/5 (`Are you P-02, the in-denial moderate …` `So we enact the second half of I-09 — the script we were assigned` `S-13 is short` `exactly as frozen, verbatim`), C18 Gaps 1/2/3 (`the argue-to-compress beat made visible` `referral to clinician exception as in I-05 still applies` `We call it S-13` `the second valence of M-10` `terminal mantra`); reader-journey C06 Gaps 1/2 (`Build, then cut.` `Short sentences again, clustered for the peak.` `That is S-02 … the house-party gatecrasher`).

**Shared symptom:** Internal fabrication identifiers and drafting/production notes surface verbatim in the delivered reader text, typically at the peak beats the prose must feel *happening to* the reader: scene codes (`S-01`/`S-02`/`S-09`/`S-12`/`S-13`), persona codes (`P-02`/`P-03`/`P-04`), instruction IDs (`I-05`, `I-09`), mantra IDs/metadata (`M-07`, `M-10`, "debut", "terminal mantra"), craft directives ("Killer-line pair. Build, then verdict.", "Short sentences for the peak. Land and stop.", "Future-pace with me.", "argue-to-compress beat made visible"), and meta-commentary naming the method's author ("as Carr does", "Carr used it").

**Distinct effects:** (a) reader C06 Gap 1 records the most damaging breaker — *"they are yanked out of the story and shown the staging … the reader, mid-trance, is handed the playwright's margin note."* (b) voice C07 Gap 2: at the rescuer-is-perpetrator reveal, *"the reader's surrender should feel spontaneous … it reads as a rehearsed staging cue."* (c) voice C18 Gap 1: *"the argue-to-compress beat made visible … a craft deck is being narrated … the reader is watching the factory, not being handed freedom."* (d) voice C16 Gap 3: the mantra-label itself destroys the recognition it must achieve — *"You are told it is 'M-07, your canonical sensory definition' that 'debuts' … research-report identification."* (e) voice C10 Gap 1: naming "Carr" as a third party injects an academic wall, *"the method's author as an external object discussed between two other people."*

**Root component:** writer-prompt.

**Evidence:** The system contract hands the writer the technique inventory it then emits: `chapter-01/system.txt` line 87 *"one killer-line pair per major argument"*, and lines 80–87 listing *"future-pacing," "ventriloquism," "pronoun triangle"* as devices; the plan's §7 cards and §4 carry the `S-0x`, `P-0x`, `I-0x`, `M-0x`/`FT-0x` IDs verbatim into the writer's inputs. Neither the system contract nor the style-guide contains any rule that these internal identifiers and drafting cues must be *translated to the reader's idiom or stripped before submission*. The style guide's nearest guardrail (§7 "Coin a small, proprietary vocabulary … a memorable name or two the reader will think in afterward") is a *reader-facing* coinage instruction and gives no ban on leaking the `P`/`S`/`I`/`M` codes. The failure first becomes possible in the writer-prompt: it carries the codes and technique names into the runtime but does not forbid their literal emission.

**Mechanism:** The plan cards and style guide are full of machine-facing codes and craft names. The writer-prompt supplies no "never surface internal identifiers; execute the device invisibly" rule. The model therefore resolves the intended move (e.g. a compression, an analogy, an instruction) by *announcing its own machinery* instead of performing it. All sources agree the surrounding warmth/force is strong; the failure is exclusively that the drafting geometry survives into the spoken voice.

---

## Cluster 3 — Cross-chapter re-argument of settled scenes/evidence instead of invoke-by-token

**Judge sources:** book-arc Gap 1 (C01→C02) and Gap 2 (C05→C11); reader-journey C02 Gaps 1/2/3; voice-emotion C02 Gap 2; reader-journey C15 Gap 2 (re-argues C14's caged lion/seatbelt/triad).

**Shared symptom:** Two consecutive/straddling chapters execute the same scene and the same evidence end-to-end rather than the later one invoking the settled verdict by token. book-arc Gap 1: *"C02 replays C01's confidence-trick scene, its first-sweet-as-love content, and its conned-not-foolish verdict almost from scratch, and it re-delivers the same self-report prevalence figure as new evidence,"* quoting C01: *"On validated self-report scales, about 14% of adults and about 12% of children …"* and C02 near-verbatim: *"pooled findings show about 14% of adults and about 12% of children …"*. reader C02 Gap 2: *"the chapter re-walks a scene, imagery and even the closing verdict that C01 already executed and closed."* book-arc Gap 2: *"C05 already plays the warm-cinema scene and fully executes the reassignment … C11 then replays the identical dark-cinema/friends-laughing/chocolate scene … and re-fetches both E-03 and the C04-flagship lived line E-01."*

**Distinct effects:** (a) reader C02 Gap 1: at the trap reveal the reader is *"pulled out of the emotional scene and dropped into a grades-lecture … Conversion on this point is already banked."* (b) book-arc Gap 2: the book "re-defeats" its strongest scene twice, softening its own denied pinnacle. (c) reader C15 Gap 2 records the same mechanism in the back half: the hand-off chapter *"re-argues at length the caged lion, seatbelt, and triad — settled C14 work that the card marks for token echo."* (d) Minor plan-design note: reader C14 Gap 3 finds the readiness gate's binary "ready or re-read" off-ramp under-pushes the "champing at the bit" landing; this is a plan-card design thread, secondary here.

**Root component:** plan.

**Evidence:** The accepted plan's §7 cards explicitly assign the same artifacts to both chapters in each pair. C01 card: *"evidence: E-11 (not uniquely weak) … scene: S-04 confidence-trick (job: dissolve shame before argument)."* C02 card: *"evidence: E-11, E-08 (schedule removes choice) … scene: S-04 confidence-trick (dissolve choice), S-12 boiling frog."* Likewise C05: *"scene: S-09 cinema fragment (reassign celebration) … evidence: E-03, E-13"* and C11: *"scene: S-09 (strongest scene full) … evidence: E-01, E-03."* The plan's repetition law (§ mantra sheet + style guide §B1–B2) — "echo is brief, never re-argued" — applies only to **mantras and frozen tokens**, not to scenes (S-0x) or evidence ledger rows (E-0x). So the plan provides no invoke-by-token contract for the two artifact types it itself duplicates across adjacent chapters. Downstream confirmation: `chapter-02/response.md` re-narrates the first-sweet confidence trick (lines 57–93) and the full 14%/12% block (lines 120–121) that `chapter-01/response.md` already landed (lines 74–94, 46).

**Mechanism:** The plan schedules the same scene and the same evidence into two adjacent/straddling chapter cards with no continuity guard ("if already deployed, invoke by token; do not rebuild"). The cards faithfully echo that schedule. Since only mantras carry the echo-not-rebuild doctrine while scenes/evidence carry none, the writer of the second chapter in each pair rebuilds the settled move from scratch — duplicating, not escalating. This slows the front of the book and re-defeats the strongest-case scene a second time at the point where it should be met once, at full force.

---

## Cluster 4 — Local grammatical/lexical fabrication in chapter 2

**Judge sources:** voice-emotion C02 Gap 1 and Gap 3.

**Shared symptom:** At two emotional peaks the prose emits syntactically-broken or garbled English that reads as a generation slip rather than one person speaking. voice C02 Gap 1: *"Do you feel the shift? **We trapped.** You escape. That is the pronoun rule of this book and it is the truth."* — *"active-voice transitive … means 'we caught something in a trap,' the opposite of the intended 'we were trapped.'"* voice C02 Gap 3: *"Do you blame a mark for being **marksman-shipped**?"* and *"Let me **ventriloquize** your mind for a second"* — *"a coherent-garble word (no native speaker says 'being marksman-shipped')"* and *"a lecture-hall verb dropped into a moment meant for gentle recognition."*

**Distinct effects:** Both breaks occur exactly where the chapter must remove blame and name the trap in warm, grammatically-whole company; the reader registers an editing error / machine assembly at the pivots of the shame-relief arc.

**Root component:** model.

**Evidence:** The inputs here are adequate and mutually consistent: no plan, card, style-guide, or writer-prompt field issues these wordforms ("We trapped." is the compressed mangle of "We all were trapped"; "marksman-shipped" is a neologism for "swindled"; "ventriloquize" is the plan's own technique verb misapplied). The upstream artifacts contain nothing that would *instruct* these; the plan/style-guide/chapter-card carry the correct semantics but the response fails to execute them cleanly.

**Mechanism:** At the trap-naming and shame-ending peaks, the model compresses and generates under the emotional load, dropping a function word ("We [all were] trapped") and fabricating a malformed token ("marksman-shipped"). Because no upstream component supplied or demanded these, and they are local, purely lexical/syntactic, and confined to one chapter, the first point of failure is generation, not any specification.

---

*verify:* Cluster 3's C15 re-argument overlaps Cluster 1's C15 (graded hump at the surge); the re-argument portion (caged lion/seatbelt/triad rebuilt) is rooted in the plan's back-half scene scheduling, the graded-hump portion in the writer-prompt. No cross-iteration persistence applies (learnings baseline). Four clusters, one root per cluster assigned.


## Learnings
# Auto-Tuning Loop — Learnings

> Every iteration (pass or fail) appends here. The loop never repeats a failed hypothesis.
> Format: iteration number, date, hypothesis, what changed, what happened, verdict, lesson.

---

### iter-000 — BASELINE
**Hypothesis:** none — baseline (no hypothesis, no change); establish the accepted state of the factory.
**Change:** (none — full fresh run: research → plan → 18 chapters → panel → A/A → trace analysis)
**Verdict:** BASELINE
**Lesson:** The factory's belief-mechanic work is solid (18/18 PASS) and the book arc lands (book-arc PASS); the recurring material failure is the *voice lane* — evidence-grading scaffold and factory-internal taxonomy (S/P/I/M codes, craft directives) leak verbatim into reader prose at emotional peaks. Root: writer-prompt over-orders ("preserve every evidence grade … permitted/prohibited inference") with no translate-or-strip rule; and no ban on surfacing internal identifiers. Secondary: plan schedules the same scene/evidence (S-04/E-11; S-09/E-01/E-03) into adjacent chapters causing cross-chapter re-argument; a local model error in C02. Hood: 4 causal clusters; Cluster 1 and 2 (both writer-prompt) dominate the voice lane.
**Next direction:** hypothesize one causal change — writer-prompt: replace "preserve every evidence grade/permitted-prohibited inference …" with a rule that translates each evidence-limits constraint into plain Carr register (or quarantines it), and forbid surfacing internal identifiers/draft directives in reader prose. Then rerun full book and re-judge the voice lane.

Baseline established. Top causal clusters: (1) evidence-grading scaffold leaked verbatim into reader prose — writer-prompt — systemic; (2) factory-internal taxonomy & drafting scaffolding leaked into reader prose — writer-prompt — systemic; (3) cross-chapter re-argument of settled scenes/evidence instead of invoke-by-token — plan — positional; (4) local grammatical/lexical fabrication in chapter 2 — model — local.

**A/A noise observation:** chapter 01 run 1 = PASS across all three lanes; chapter 01 run 2 (identical inputs, regenerated) = belief-mechanic PASS + reader-journey PASS + voice-emotion FAIL (one material gap: the evidence-grading register at the shame-removal peak). The material failure-class set **differs** between the two runs (run 1: none; run 2: one voice class = Cluster 1 evidence-grading leak). This calibrates "material": the dominant systemic cluster is present across many chapters but its *appearance in any single chapter is sampling-sensitive* — the same chapter can pass or fail the voice lane on a re-run. Decisions must be made on the failure-class set across the book, never on a single chapter's instance.



## Current editable factory files
prompts/style-guide.md, prompts/research-agent.md, prompts/master-plan-skill-v2.md, prompts/master-plan-reviewer-v2.md, prompts/chapter-writer.md, loop/config.yaml

Formalize this single change as the manifest iteration-001 hypothesis per your 4-field contract. Its one-causal-change and never-repeat guards still apply.
```
