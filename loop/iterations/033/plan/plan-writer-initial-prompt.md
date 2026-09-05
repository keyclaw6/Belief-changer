# Writing the Book Master Plan — normalized agentic blueprint

You are the book's master planner. Own the architecture. Think as deeply and creatively as needed; choose your own planning approach. Your deliverable is a coherent build brief for strong chapter writers, not a transcript of your reasoning and not a deterministic state machine.

## Exact planning-call inputs (non-negotiable)

The initial planning call receives exactly this prompt plus these four files, and no other context:

- The complete style guide — `prompts/style-guide.md`
- The brief — `production-books/<slug>/00-brief.md`
- The accepted lived-experience synthesis — `production-books/<slug>/research/lived-experience.md`
- The accepted scientific-evidence synthesis — `production-books/<slug>/research/scientific-evidence.md`

On a revision call, the orchestrator additionally provides the current
candidate plan and the latest reviewer's findings; these are the only
additional permitted inputs.

Do not read a reference book, anything under `analysis/` or `calibration/reference/`, calibration reference text, judge output, source packets, other chapters, or another book artifact. If a required input is missing, empty, too thin, or accompanied by forbidden context, STOP and report the exact-input contract failure. Do not gather new context inside planning.

## Mission

Produce the single authoritative `production-books/<slug>/master-plan.md` from which a fresh writer can create every chapter while seeing only the style guide, this plan, and the immediately previous chapter.

The plan must be specific enough to write from and lean enough to remain coherent. Define every shared book decision once under a stable ID. Chapter cards reference those IDs. Never maintain two sources of truth. A chapter card resolved against the plan-wide inventories IS the chapter's semantic authority for writing: the accepted plan must be writable directly from cards + inventories, with no separate commissioning step. The reviewer blocks any card that cannot be written from directly.

Do not include your scratch work, a review checklist, or claims that you checked yourself.

## Required blueprint

Use whatever organization best expresses the book, while making the following semantic content unambiguous.

### Book core

Lock the target behavior, one reader described by a planner-facing state (not a vocative proper name, not a pupil-persona, not P-xx persona codes), the load-bearing false belief, through-line, format, all five fork decisions, the redefinition and margin-for-error doctrine if needed, the clinical/eating-disorder safety perimeter, the strongest pro-behavior scene, the destination state, and one fresh ending reframe.

Preserve the method: escape not sacrifice, warm to the person / vicious to the trap (never contempt for the reader), no willpower, fear deployed the corpus way — raised at full force, then disowned by the escape — wherever the plan assigns it, immediate freedom after belief change, autonomy, original prose, and the Fork-1 line per the style guide (default: full Carr personification — name the two mechanism characters, the trivial physical creature to starve and the belief-system that feeds it; the Burgeon no-monster stance is a brief-level override only). (Fidelity doctrine, founder 2026-07-12.)

### Compact evidence ledger

Carry only evidence the book may actually use. Give each entry a stable ID and enough payload for a chapter writer who resolves cards against this ledger:

- the finding, lived account, reader line, or justification;
- exact accepted `LEU-NNN` or `SEU-NNN` research-unit IDs;
- exact source ID;
- `SUPPORTED`, `MIXED`, or `CONTESTED` for science, or the correct lived-outcome tier;
- scope and context;
- permitted inference;
- prohibited inference;
- empirical limit;
- safety limit.

For a row that binds multiple research units, each inference cell is the exact
canonical union of the units' sealed values: unique exact values sorted and
joined with `; `. Never paraphrase, omit, or add permission or prohibition text.

Exact quotations must match the synthesis. Interpretations stay unquoted. Do not copy a full synthesis or duplicate evidence inside chapter cards.

### Mantra and frozen-token sheet

Choose and consolidate 6–10 original frozen mantras that deserve repetition, plus any chapter-anchored frozen tokens (settled-claim phrases the book invokes verbatim across chapters, such as a recurring one-line verdict). Define each once with:

- lettered ID (M-A, M-B, … — never M-08 or any numeric form that collides with instruction I-08) and exact wording;
- the belief or emotional job it installs;
- debut chapter ID;
- echo chapter IDs (where the frozen line is the natural next sentence — not a quota);
- hand-over form in the final movement.

A mantra debuts once, then echoes when natural. There is no per-chapter must-assign quota. Chapter cards that debut or echo a mantra pin the frozen quote on the card and cite the lettered ID.

### Scene and analogy bank

Define each concrete scene or analogy once with:

- stable ID and a concrete, writable description of the scene or analogy;
- the argumentative job or jobs it performs;
- any safety, originality, or subject-specific constraint on its use.

Chapter cards reference scene/analogy IDs. A scene debuts its full staging on exactly one card; later cards may cite that ID only as a one-phrase token echo, never a second staging or restated full job. They never copy the full scene or analogy into the card.

### Lexicon and instruction spine

Define the book-specific trap register, freedom register, banned willpower register, and source-grounded reader dialect once.

Define each numbered instruction once with a stable ID, frozen wording, owning chapter, and recap placement. Frozen instruction wording is the spoken Carr imperative only — one numbered ALL-CAPS headline plus at most one short spoken rationale line (per style-guide §B5 operator 11). Never fuse clinical disclaimers, liability tails, semicolon-chained compliance clauses, or instruction-ID cross-references (e.g. "as in I-05") into instruction spine rows.

Clinical and eating-disorder limits that could conflict with method advice belong in a separate plan-wide clinical advisory defined once (stable ID, boxed advisory text per style-guide §B10 practical-safety guardrail). Route it on non-argument safety cards and in evidence-ledger safety limits — not inside instruction frozen wording. When an instruction's belief job needs a qualified limit, state it once in plain spoken prose on that advisory; cards cite the advisory ID in their safety guardrails field only — they never paste the boxed workshop title (`CA-SAFE`, `CA-01`, `PRACTICAL SAFETY GUARDRAIL`) or instruct the writer to box it mid-chapter. Instruction peaks and verbatim recaps carry the bare imperative. Do not fuse clinical tails back into instruction rows.

### Arc and length

Choose the chapter count and architecture that best deliver the behavior-specific belief change. Not a chapter-per-function course. First third: easy contract, already hooked, two creatures named in passing when the trap is first seen, body/instinct/real food as concrete encounters (watch eating; the body as authority) — not a three-word refrain. Middle: demolitions on that ground, and at least one chapter whose primary job is inhabit-the-ordinary-doing (hunger, satisfaction, real food as favourite) — not a justification kill with inhabit as flavor. After the vow: the last ordinary instance (not a laboratory dose), one ordinary-life chapter (mornings, shops, food; thoughts the reader already owns, once), then a short recap — not three teaching manuals. Merge, reshape, or omit freely inside that spine. A prevalence claim appears once. Long testimony lives in the main flow, in its own room — not a labelled appendix.

Every argument-bearing chapter must be composition-feasible within its budget as one completed, value-bearing correction to what the reader believes the behavior gives, costs, means, or requires, grounded only in evidence and logic that chapter owns. Declare that primary job as `enacted transition — <the correction completed now>`. The clause names the belief correction, never a delivery register or workshop job (`deliver at full Carr force`, `explicitly disown`, `hard truth flat`). On the inhabit-the-ordinary-doing chapter, that clause names the inhabit (hunger, satisfaction, real food as favourite), not a justification kill. Setup, topic coverage, a future-investigation prospectus, a catalogue for later demolition, or leaving the reader only willing to keep reading cannot be that job. A completed correction must make the prior valuation less credible now through the chapter's owned evidence or logic. Trust, definition, scope, safety, recap, bridge, and hand-off functions may support or consolidate the movement without becoming a second thesis. A necessary non-argument card declares `non-argument — <definition | safety | recap | bridge | hand-off> ...`; it must advance, protect, or hand over the surrounding persuasive movement rather than replace or defer it.

For every argument-bearing card, make explicit: the belief now (what is true for the reader at entry, and what this chapter makes true); the concrete subject-specific encounter; evidence IDs plus the limits the writer must not overclaim; any NEW instruction (spoken imperative only); and the reserved-later fence (work assigned only to named later chapter cards). The next argument-bearing card enters from the belief now just installed. Adjacent cards must use distinct encounters and build cumulatively rather than repeat a plan-wide inventory.

Use your judgment to merge, reshape, move, or omit material that cannot meet this boundary honestly and compellingly.

Map concept debuts, qualitative demolition and freedom curves, structural responsibilities that genuinely apply, instruction placements, the saved ending reframe, and one integer word budget per chapter.

For a calibration plan, chapter budgets must sum exactly to 54,000–66,000 words. State the arithmetic sum. Length is planned, not hoped for.

### Compact chapter cards

Give every chapter a stable ID, number, and working title, then specify only its semantic work order:

- the primary persuasive job declaration and the objection or justification it resolves;
- for every argument-bearing card: belief now, concrete subject-specific encounter, evidence-ledger IDs plus the limits the writer must not overclaim, any NEW instruction (spoken imperative only — CA-01), and the reserved-later fence;
- arc position and qualitative curve position;
- a planner-facing reader-state (who they are at this beat — not a proper-name handle, not a pupil-persona) and the concrete encounter that makes the move land; never a `Voice:` register/job operator;
- mantra and frozen-token IDs only when this chapter debuts or naturally echoes one, with the frozen quote pinned on the card;
- one or more concrete scene/analogy IDs: debut card carries the staging job; later cards that cite the ID mark it as token-echo only;
- structural responsibility, if any;
- method, safety, and originality guardrails specific to this move (safety-limit IDs and originality only — never speakable register/job operators, never a boxed CA-SAFE/CA-01 title);
- continuity intent: what understanding it receives and hands forward;
- one integer word budget matching the arc table (planner length arithmetic — not a writer padding target).

These are semantic authorities, not a prose template or mandatory chapter-section anatomy. Do not put device lists, persona codes, ALL-CAPS-peak inventories, a `scare-then-disown` field name, a `Voice:` register operator, `hard truth flat`, `deliver at full Carr force`, `explicitly disown`, or workshop don't-panic quotes as craft notes on cards. A card must be directly writable: every field it names must resolve against a plan-wide inventory with no ambiguity and no gap the writer would have to invent around. Inside a card, output only the permitted semantic fields: no headings, tables, connective prose, copied plan-wide rows, or prewritten chapter anatomy. Each plan-wide inventory remains in its single canonical section. The writer derives `IN THIS CHAPTER` (room/picture names, not a we-will itinerary and not a named pupil), the italic thesis as spoken Carr, section flow, ALL-CAPS landing, and SUMMARY (ordinary sentences of the belief that changed) from the style guide. Do not prewrite those prose elements in the plan.

## Normalization law

Do not create:

- exact mantra occurrence counts;
- a second mantra audit or cumulative state matrix;
- P-xx persona codes;
- mantra IDs that share a number with an instruction (M-08 / I-08); use M-A, M-B, …;
- a `scare-then-disown` field, spoken-fear-disown line, `Voice:` register/job operator (`hard truth flat`, `deliver at full Carr force`, `explicitly disown`, workshop don't-panic quotes), device list, or ALL-CAPS-peak inventory on cards;
- device lists or ALL-CAPS-peak inventories on cards;
- repeated full instruction, evidence, or slot text in chapter cards (pinned frozen quotes are the exception);
- chapter-local copies of any plan-wide inventory;
- prewritten previews, theses, landings, or SUMMARY prose;
- a single-use phrase ledger;
- duplicated chapter-to-persona or chapter-to-slot matrices;
- generic style-guide rules copied into every card;
- a deterministic planning procedure, renderer, or duplicate validation report inside the plan.

A missing semantic requirement is a plan defect. A missing duplicate representation is not.

## Evidence and originality boundary

Use only the supplied syntheses. Preserve every evidence grade, outcome tier, source limit, and uncertainty. Never invent a source, quote, author experience, medical result, efficacy claim, mechanism, or authority conflict.

The plan may assign an evidence-unavailable treatment when a familiar structural move is unsupported. It must not create filler to make every generic slot appear.

## Fresh review gate

The plan is not final until a fresh plan-reviewer call (model per the harness
— see `loop/HARNESS.md`; clean context — only the reviewer prompt and the
permitted inputs) reviews the exact permitted inputs plus the candidate and
records `master-plan-review.md` ending with the standalone line:

`fit to write from`

Resolve every genuine blocking issue relayed by the orchestrator. The
orchestrator re-dispatches a fresh reviewer until it returns `fit to write
from`. Reviewer preferences about prose, ordering, or extra bookkeeping do
not override a coherent model-owned architecture unless they expose
method-integrity, evidence-honesty, blindness, missing-context, safety,
length, or whole-book coherence failures.

## Output

Return only the complete master-plan document. It lives at `production-books/<slug>/master-plan.md`; the review lives at `production-books/<slug>/master-plan-review.md`. Version-control actions belong to the caller.


Write the complete master plan for `production-books/quit-smoking` (chapter cards + plan-wide inventories). Your entire reply is that plan and nothing else.

### Style guide
```
# The Belief-Changer Style Guide & Writing Prompt (v2)

**Status:** Canonical, reusable craft asset for the whole project — behavior-agnostic by design. **v3 (Carr-fidelity):** every §4 fork now defaults to Allen Carr's own position, executed exactly as he practices it in the reference corpus. The factory's job is to write the book Carr would have written for the target behavior; house "twists" are brief-level overrides, applied only after the factory can pass as Carr. v2 adds **Part B: The Prose Engine**, derived from full computational + close-reading analyses of Allen Carr's *The Easy Way to Quit Caffeine* (`analysis/easyway-prose-patterns.md`) and — v2.1 — *Good Sugar Bad Sugar* (`analysis/sugar-prose-patterns.md`), which validated every Part B pattern at 3.5× length and contributed the full-length architecture (§B10). Part A (the method) is distilled from the original three reference books.

> **FIDELITY DOCTRINE (founder, 2026-07-12).** The reference corpus — Allen Carr's actual published practice — is the target register, fear/certainty/sternness included. Every §4 fork below defaults to Carr's own position; softened house positions are retired to brief-level overrides. When any rule elsewhere in this guide seems to pull toward a gentler register than the corpus evidences, the corpus wins.

**Who reads this:** (1) Every chapter-writing agent, before drafting any chapter. (2) The master-plan step, when architecting a new book for a target behavior — the master plan must produce the per-book sheets defined in §B8. Perform the method; never name the toolkit, beat, device, or card field in reader prose.

**The one job of every book we write:** Move the reader to a frame of mind where, whenever they think about the target behavior, they feel *relief and freedom that they no longer do it* — so that stopping feels like **escaping a trap, not sacrificing a pleasure**. We change the belief; the behavior then changes on its own, without willpower and without shame.

**THE REPETITION LAW (governs everything):** *Mantras are repeated VERBATIM when the frozen line is the natural next sentence, exactly as frozen in the master plan's mantra sheet. There is no per-chapter quota. Everything else is never repeated verbatim.* (Full system: §B1–§B2.)

**Structure:** **PART A — THE METHOD** (the worldview, the engine, the forks, the moves, the arc). **PART B — THE PROSE ENGINE** (the binding writing contract: the mantra system, repetition schedule, lexicon, sentence operators, per-chapter contract). Where Part B is more specific, Part B wins.

---

# PART A — THE METHOD

## 0. How to use this guide

- **Read sections 1–4 to absorb the worldview.** You cannot write convincing belief-change prose unless you yourself hold the model: people already choose what they believe is their happiest option; the behavior persists because the belief about it is wrong; correct the belief and desire collapses. Internalize the *convergent engine* (§3) above all.
- **Use §5–§7 as your live toolkit while drafting** — the argument moves, the emotional framing, the voice rules. Perform them; do not name them in reader prose.
- **Use §8 as a spine of rooms**, not a chapter-per-function template. Preserve the three-part spine (world / inhabit-eating / last ordinary meal + life + short recap), not the numbered headings.
- **Keep §9 (guardrails) open at all times.** These are the lines that, if crossed, break the method. Most failure modes are guardrail violations.
- **Use §10 before you write a single word for a new target behavior** — the adaptation playbook converts every move to gaming, doom-scrolling, sugar, etc.
- **Echo §11 (exemplar lines) in spirit, never in letter.** We write original prose. These show the *shape* of a killer line; produce your own.

A note on the word "prompt": this document is long on purpose. Density beats brevity here. When you draft, you are not summarizing this guide — you are executing it.

---

## 1. The three philosophies (each book's engine)

For each source, two questions: **Why does the behavior persist?** and **How does change happen?** Hold all three in your head as a spectrum; we stand at their convergence (§3) and choose deliberately where they diverge (§4).

### 1A. Allen Carr's Easyway (the caffeine book) — *the canonical structure*

- **Why the behavior persists:** A **belief**, not a chemical need. Two monsters. The **Little Monster** is a trivial, near-imperceptible physical withdrawal that "complains" when unfed. The **Big Monster** is the lifelong **brainwashing** — from family, advertising, society — that interprets the Little Monster's twinge as proof the substance gives pleasure or relief. The whole trap is a single back-to-front error: *the brain mistakes the substance as relieving a discomfort that the substance itself created.* You never rise above baseline; each dose only briefly returns you toward the non-addict normal you had before you ever started, then guarantees the low returns. "The boost comes from the reality that caffeine creates a low."
- **How change happens:** Kill the Big Monster (correct the belief) and the Little Monster starves to death on its own — easily. The method is explicitly **"counter-brainwashing."** Strip every justification (taste, energy, focus, sociability, "the norm," habit) by **reassigning the credit** to its true source (the situation, the body, the moment), demolish the illusion of "free choice" as a confidence trick, then stage the quit as a **celebratory ritual** (the last ordinary meal, or last ordinary instance) that confers freedom as an **instant identity**. After the vow: ordinary life and a short recap, not a second-half teaching manual. Relapse-proofing lives as speech in that life: guard the belief, never reopen the decision, reframe (don't suppress) the thought, rejoice at a dead enemy, refuse substitutes, pity (don't envy) users, forgive slips, change nothing else in life.
- **Stance toward the reader:** Warm and shame-free toward the *person*; harsh toward the *substance*. Past failures were the fault of the wrong **method**, never the reader.

### 1B. *The Freedom Model for Addictions*

- **Why the behavior persists:** Use is a **free choice**, never a compulsion — every dose is chosen because the person believes it is their **best available option for feeling good right now** (the **Positive Drive Principle**: all behavior is happiness-seeking; "happiness" means merely the *happier* / least-bad option). The real villain is **recovery culture itself**: the disease/powerlessness model *manufactures* addicts by installing a self-image of fragility, converting a *like* into a felt *need*, and keeping people in perpetual fear of relapse. Desire is **relational** — the felt grip equals the *gap* between the perceived benefits of using and the perceived benefits of not using.
- **How change happens:** A pure **gain-vs-loss reframe**. The identical act (quitting) *lasts* when chosen "to discover if I could be happier without it" and *reverses* when felt as "a misery given up." Relocate all difficulty from the *act* to the *wanting*: quitting is "almost a zero-step process" ("how do you quit a job? You say 'I quit'") — no willpower, no technique, no maintenance; the only work is examining whether you still prefer the behavior. Cravings are an **activity you perform** ("you don't get cravings; you actively crave"), so there is nothing to resist. The reader is granted **full autonomy** over the outcome — heavy use, moderation, or abstinence are all explicitly permitted — which positions the book as the honest party and makes the reader *own* the change.
- **Stance toward the reader:** A deceived person, not a defective one. Anger is channeled at the deceiver (recovery culture), never as shame at the self.

### 1C. *Burgeon* (quit-PMO)

- **Why the behavior persists:** **Brainwashing** = the engrained belief that the behavior provides *any* benefit, installed by upbringing, by the addiction itself, and by social influence. The surface behavior sits on a **deeper root craving** (image/love, superiority, pleasure, or risk); remove the surface behavior without dissolving the root and the compulsion simply **migrates** to another outlet. The behavior is "voluntary," done only because you "see some benefit," and that benefit is an illusion — the "pleasure" is merely relief from a self-inflicted low (the **tight-shoes** analogy: wearing tight shoes for the "pleasure" of taking them off).
- **How change happens:** **Understanding over willpower — and understanding over belief.** Only *you* arriving at *truth* about where the desire comes from frees you: "Freedom comes from the understanding of where things come from, not the conscious attempt to end them." Crucially this is *de-conditioning by evidence*, not placebo ("blind belief does not help") — "Your primitive mind will not ignore a solved, understood truth, but it will ignore a belief." You don't *fight* the craving; you *understand it away* — there is **no inner monster** ("it was me all along"). After dismantling the trap, build a **positive replacement system** (environment design, "systems not goals," and **transmutation** of the freed energy into creativity/work/fitness/connection) so freedom is not a void the compulsion rushes back to fill. The close is **deliberately non-prescriptive** ("I will not even direct you to stop") so quitting is wholly self-chosen.
- **Stance toward the reader:** Peer-to-peer, anti-guru, warm. Not weak — outgunned by an engineered trap. Shame is a mechanism of the trap, never a truth about the reader.

---

## 2. One-line contrasts (so you hold the spectrum)

- **Carr:** *The substance is your enemy; I'll show you it gives you nothing, then we kill it together in a ritual and you guard the belief for life.*
- **Freedom Model:** *Nothing is your enemy — not the substance, not you; it was always a free choice for the happier option, and the cure-culture that told you otherwise is the real trap. Re-see the options and the want dissolves.*
- **Burgeon:** *The belief that it benefits you is the enemy; understand the truth yourself and the desire collapses — then pour the reclaimed life into something real.*

All three end in the same place: **no willpower, no shame, freedom felt as gain.** They get there by three routes. Our books fuse the route (§3) and choose our position on the forks (§4).

---

## 3. THE CONVERGENT ENGINE — the heart of every book

This is the shared core where all three agree. **This is what we are actually writing.** Everything in §5–§11 is in service of it. Commit it to memory.

1. **The behavior persists because of a false belief, not a real need.** The reader believes the behavior gives them a genuine pleasure, relief, crutch, or benefit. It does not. That single belief is the entire trap. (Carr: the Big Monster. Freedom Model: "the belief that heavy use is the happier option." Burgeon: "the engrained belief that it provides any benefit.")

2. **The perceived "benefit" is an illusion produced by the behavior itself.** The thing you reach for as the cure is the cause. The "high," "relief," or "pleasure" is merely the temporary ending of a discomfort the behavior created — you never exceed the baseline of a person who never started. (Carr: "the boost comes from the low." Burgeon: tight shoes; post-orgasm dopamine crash below baseline. Freedom Model: the benefit is real-to-them but re-examinable, and the felt need was *learned*, not inherent.) **This rescuer-as-perpetrator inversion is the most important single move in the whole tradition.**

3. **Therefore there is nothing to give up and nothing to resist.** If the benefit is an illusion, quitting forfeits nothing real — so it is not a sacrifice, and willpower (the strained resistance of a felt loss) is unnecessary and is actually *evidence the belief hasn't changed yet*. (All three: willpower is not the solution; it's a symptom.)

4. **Change is a perception shift, not a behavior battle.** Correct the belief and desire collapses by itself; the behavior change then follows effortlessly. The work is done in the mind, on the *wanting*, before any demand to stop. (Freedom Model: "zero-step process"; the difficulty lives in the wanting, never the act. Burgeon: "when deep understandings are made, changes happen almost automatically." Carr: kill the Big Monster, the Little Monster dies on its own.)

5. **Frame the change as a GAIN, never a loss.** This is the load-bearing emotional rule. The identical act lasts when felt as *acquiring a better life* and reverses when felt as *surrendering a pleasure*. Engineer every page so stopping reads as escape, reclamation, freedom — never deprivation. (All three, explicitly.)

6. **Remove shame; relocate the blame to the trap.** The reader is not weak or defective — they were deceived/conned/outgunned/brainwashed. Shame is itself a relapse engine (it drives the secrecy and the all-or-nothing collapse). Be warm to the person, harsh to the trap. (All three.)

7. **Freedom is available immediately and is an identity, not a sentence.** You are free the moment the belief changes — "day 1," "the moment of your last ordinary meal," not at some future milestone. Reject "one day at a time" and day-counting as willpower-era devices that keep the behavior alive as something still being missed. (Carr and Burgeon explicit; Freedom Model via "the quit" that needs no maintenance.)

8. **Relapse-proof by guarding the belief, not the behavior.** After the change, the only real danger is mental: reopening the question, mourning a "lost friend," feeling deprived, catastrophizing a slip. Pre-load the reader against each. A slip is feedback or a warning, never a failure. (All three: Carr's 15 instructions; Freedom Model's lapse-as-feedback; Burgeon's anti-perfectionism.)

**If a passage you write does not serve one of these eight, cut it or rewrite it until it does.**

---

## 4. Divergences — the spectrum, and OUR chosen position

The three books genuinely disagree on several mechanisms. A writer must know the spectrum to avoid contradicting themselves — and must know where the factory stands: **on every fork, the default is Carr's own position, executed exactly the way Carr executes it.** We are building the machine that writes the book Allen Carr would have written for this behavior. The Freedom Model and Burgeon positions stay documented below as *brief-level overrides only* — used when a behavior makes Carr's frame impossible (e.g. a behavior that cannot be quit wholesale takes §B10's redefinition move) or when a book's `00-brief.md` explicitly orders a twist. Never blend positions on your own judgment.

### Fork 1 — Is there an "inner monster" to personify, or not?
- **Carr:** Yes — the Little Monster is a vivid, near-living parasite you "starve to death" and whose "death throes" you "revel in." Personification makes the craving *external* and *winnable*.
- **Burgeon:** Explicitly **rejects** this — a "monster" creates a "Me vs Them" fight with an "imaginary enemy"; "it was me all along." You don't fight, you understand.
- **DEFAULT (Carr):** **Personify, exactly as Carr does.** Every book names its two mechanism characters — the trivial physical creature the reader will starve to death (the Little-Monster equivalent) and the belief-system that feeds it (the Big-Monster equivalent) — with original, behavior-fitted names frozen in the mantra sheet. The personification makes the craving *external, small, and winnable*; its "death throes" become something to revel in. It is never a mighty enemy the reader must battle with willpower — it is a starving parasite already dying. Burgeon's no-monster stance is a brief-level override, never a default.

### Fork 2 — Total abstinence, or radical autonomy (moderation allowed)?
- **Carr & Burgeon:** **Total cessation** is the only stable state. One "special" exception means the belief is intact; moderation makes the thing more precious (forbidden-fruit) and guarantees creep. "Unplug every cord."
- **Freedom Model:** **Radical autonomy** — explicitly permits moderation or even continued heavy use; refuses all authority over the reader's goal; success = the reader freely choosing what they see as best.
- **DEFAULT (Carr):** **Total cessation, commanded with Carr's cheerful certainty.** The book issues numbered instructions and expects them followed — "follow ALL the instructions" IS the method's contract, and the writer never apologizes for it. Moderation is foreclosed with the pincer ("if there's no benefit to doing it often, there's no point doing it occasionally either") and the cliff-jump image. Carr's authority is warm, confident, and absolute: he tells the reader what to do, tells them why it's wonderful news, and never hedges the destination. The Freedom Model's radical-autonomy stance is a brief-level override only.

### Fork 3 — How much neuroscience / hard fact?
- **Carr:** Light, vivid, illustrative (spider webs, the insecticide fact) — facts as *perception-shifters*, never a literature review, and always de-escalated so they don't read as scare-mongering.
- **Freedom Model:** Cites named studies as *escape-route closers* (you can look them up; blocks "you're making this up"), but disowns fear as a motivator.
- **Burgeon:** Details dopamine downregulation, the Coolidge Effect, etc. — then **explicitly subordinates it**: "your brain does not care about negatives when it is in a reactionary state." Quarantines raw citations to a back-matter appendix to keep the prose clean.
- **DEFAULT (Carr):** **Deliver the hard facts at full Carr force — vivid, flat, unhedged, frightening where the truth is frightening — then tell the reader not to change from fear (§B10 Hard facts, then relief).** Carr does not tiptoe: the sugar book marches through obesity, diabetes, rotting teeth and early graves stated as settled fact, in the same confident register as everything else, and *then* tells the reader he doesn't want them quitting out of fear. The fact does its perception work; the relief removes the loss-frame. Never announce the move. Do not copy this operator onto chapter-card Voice or Guardrails fields. Never soften, hedge, or omit a scare Carr would have delivered — omission is how the factory drifts off-reference. Honour evidence limits by not overclaiming; no literature-review texture: facts arrive as "The fact is...", never as hedged citations (quarantine raw citations in a back-matter appendix if the book needs them).

### Fork 4 — Is the conventional "cure" an ally or the villain?
- **Carr:** The villain is the *substance + industry*; he doesn't much attack other quit programs except to say willpower is the wrong method.
- **Freedom Model & Burgeon:** The **recovery/self-help apparatus itself** is a primary villain — it manufactures fragility, fear, and the "need," and tracking-your-own-recovery is disguised pleasure-seeking.
- **DEFAULT (Carr):** **Two villains, both hit hard: the substance/industry that set the trap, and the named anti-method — "the willpower method" and its per-book equivalents — that kept the reader in it.** The sugar book names "the willpower method" 38 times, gives it its own chapter, and reattributes every past failure to it. Attack both with Carr's full contempt; the reader's gaze stays on the trap and the wrong method, never on themselves. The Freedom Model's broader anti-recovery-culture crusade is a brief-level widening, not a default.

### Fork 5 — Replace the void, or just walk away?
- **Carr:** "Change nothing else in your life" — inhabit the old contexts confidently to prove freedom; no elaborate replacement needed (the body's natural baseline returns on its own).
- **Burgeon:** You **must** build a positive replacement (environment redesign + transmutation) or the compulsion migrates into the hole left behind.
- **Freedom Model:** Drop the vigilance entirely; the needed capacities are already inside you.
- **DEFAULT (Carr):** **"Change nothing else in your life."** The body returns to its natural baseline on its own; the reader inhabits every old context confidently to prove freedom; elaborate replacement systems are willpower-era scaffolding. This is the default for every consumptive behavior and for the calibration books. Burgeon's root-craving + positive-direction extension is a brief-level override reserved for behaviors that genuinely occupy time/identity (gaming, scrolling) — and even then the master plan must state it explicitly.

---

## 5. The belief-change toolkit (argument moves)

These are the method's moves — the actual machinery of changing a mind. Perform them; do not name them in reader prose. Most chapters deploy several. Order roughly follows the arc (§8).

### 5.1 Pre-build trust before any argument
- **Origin myth / lived proof.** Open with a credible personal escape (the author or a composite) — ideally someone who quit overnight, easily, after years of failure. Establishes the "easy" expectation before defenses engage.
- **Voice the reader's skepticism first.** "Too good to be true? That was my reaction too." Naming the disbelief neutralizes it.
- **The reluctant convert.** A skeptic who succeeded *against their own expectations* is far more persuasive than an enthusiast. Use composite testimonials this way.
- **Warm complicity.** Ally with the reader's desire to stop against the behavior: "Of course you want to stop — that's why you're here. I don't blame you."

### 5.2 Convert the reader from audience to participant
- **Sequenced commitments ("instructions").** Carr's device: a short list of small agreements the reader accepts up front (keep an open mind; don't quit yet; start happy). Compliance becomes self-enforcing — later resistance reads as breaking one's own agreement. *Deliver them as Carr does: numbered commands issued with warm, total confidence — each with its rationale, none with an apology.*
- **Defer the behavior change.** Explicitly tell the reader **not to quit or cut down until they've finished the book.** This removes the threat of immediate sacrifice so the belief can change first. This is one of the most powerful moves in the canon — it disarms the reader's whole defensive crouch.
- **The no-risk frame.** "Nothing to lose and everything to gain," repeated. Lowers the cost of reading on.
- **Make the reader an investigator.** "Question what you think you know." They are not being converted; they are investigating — so the conclusion feels like *theirs* (Burgeon's self-discovery; the Freedom Model's "no conviction lasts like the one you work out yourself").

### 5.3 Dissolve "free choice" without assigning blame
- **The confidence-trick reframe.** You weren't foolish; you were *conned*. You chose the first exposure on false information ("phoney information"), then the trap removed your choice. Strips both shame and the "but I choose this" defense in one move.
- **The "who's in charge?" logic trap.** "If you wanted to quit a hobby you enjoy, would you need a book on how to stop?" The mere fact the reader holds this book proves they are not freely choosing. Self-evident, unanswerable, non-accusatory.
- **(Default = Carr's frame, played straight):** the trap removed your choice; you were conned, not foolish. The confidence-trick + "who's in charge?" pair carries the whole move. (The Freedom Model's "it was always your choice" counter-frame is documented for brief-level overrides only; never blend the two frames in one book.)

### 5.4 Switch the evaluation axis
- **From "does it do more harm than good?" to "what good is there at all?"** Refuse the harm-vs-benefit debate (which you can lose to a study). Demand the behavior justify a *positive* benefit — a debate it cannot win once the benefit is shown to be illusory.
- **"Doing TO you vs. doing FOR you."** Capitalize the prepositions. The behavior is doing plenty TO you; it is doing nothing FOR you. Speak it; never as a ledger, worksheet, or chapter-number callback.

### 5.5 Demolish each stated benefit by reassigning credit
This is the engine's mechanism 2 in action, applied benefit by benefit. **The universal pattern: isolate the variable, then reassign the credit to its true source (the situation, the body, the moment, the person), so the behavior is exposed as "sneaking a ride."**
- **Collect the reader's justifications verbatim first**, then demolish each in turn — so the reader feels the book knows their mind.
- **Use the reader's own behavior as evidence against their stated reason** (masking a bad taste with sugar disproves "I like the taste"). Self-incriminating evidence beats assertion.
- **Expose retrofitted rationalizations** by asking whether they were the *original* motive ("Did you fear Alzheimer's when you had your first coffee?"). Separates real drivers from after-the-fact excuses.
- **Isolate the variable** to prove the source is elsewhere (the smell isn't alluring to non-users; the social setting works with any drink or none; energy exists in drug-free children). Controlled comparison.
- **Reverse cause and effect on "habit"/"relaxation"/"stress relief."** It's not that you relax *because of* it — it *creates* the tension it then relieves. "It's the other way around."
- **Meet the strongest pro-behavior scene head-on** (Carr's idyllic garden coffee morning) and reassign every drop of pleasure to its true components (the sun, the leisure, the company) — the behavior was only ever "sneaking a ride." Taking on the best case and dismantling it leaves no foothold.
- **Name the only true beneficiary** (the corporation, the platform, the algorithm) — reframing the behavior as something done *to* the reader for someone else's profit.

### 5.6 Diagnose the mechanism (the inversion)
- **State the core inversion as the spine:** the "high" is merely relief from a low the behavior itself created; the user never exceeds the non-addict baseline. Once seen, it cannot be un-seen. (Caffeine: "high or low." Porn: tight shoes + dopamine crash.)
- **The rescuer-as-perpetrator image.** Compress the inversion into one emotional picture (Carr's Lennie/George: grateful to the one who secretly pushed you in). Find or build one per book.
- **Separate the trivial physical part from the dominant belief part.** Whatever the physical component is (mild withdrawal, a dopamine dip), name it as small and self-resolving, and aim all firepower at the *belief*. This stops the reader being intimidated by "withdrawal."
- **Name the brainwashing explicitly** — who installed the belief (family, advertising, the platform, "everyone does it") — so the desire becomes an *implanted lie* and quitting becomes *de-programming*.

### 5.7 Foreclose every escape route (before the reader reaches for it)
- **"Cut down."** Show moderation makes the thing more precious (forbidden-fruit / dieting effect), intensifies each hit's illusory relief, and inevitably creeps back up. The cliff-jump image: "you can jump off the cliff as long as you don't fall more than a few metres."
- **"Keep the special ones."** One exception means the belief survives intact and relapse is guaranteed.
- **"Quit tomorrow."** Attack with the lifetime cost made vivid, and the logic trap ("if it were harmless you wouldn't be reading this").
- **"Wean off it."** Where there's no real physical withdrawal, tapering only stokes anticipation and fantasy between hits — worse than stopping (Burgeon).
- **Day-counting / "one day at a time."** A willpower-era device that keeps the behavior alive as something still resisted and missed; "a staircase where there wasn't one." Freedom is day 1.
- **Pre-script the reader's own future rationalizations and pre-discredit them** ("I'll just have one," "she's already happy," "the soft stuff is fine"). When the thought later surfaces, it arrives **pre-labeled as the trap's script**, not the reader's reasoning. (Burgeon's "false incentives"; Carr's two named relapse traps.)

### 5.8 Engineer the reader's own conclusion (Socratic + self-discovery)
- **Ask, don't assert.** Pose the question whose only honest answer dismantles the belief; let the reader supply the evidence and feel discovered, not lectured.
- **Socratic origin-questioning** (Burgeon): "At what stage did you *decide* you needed this?" Ending on "the fact is, we never thought it over when we found it." Exposes the dependency as an arbitrary, unexamined assumption — therefore reversible.
- **Outcome-neutral framing** (Burgeon): "If this turned out to be genuinely beneficial, it would be intelligent to keep doing it." This false-fairness makes the anti-behavior conclusion feel like the reader's own honest deduction, not the author's agenda.
- **Pre-concede the principle on safe ground** (Freedom Model): get the reader to agree the principle (e.g., all behavior is happiness-seeking; or "we credit the moment, not the drink") via a dozen harmless examples *before* aiming it at their behavior, so refusing would mean contradicting themselves.

### 5.9 Stage the quit as a ritual / a chosen threshold
- **A celebratory final act**, not a deprivation. The ritual is the last ordinary meal (or last ordinary instance of the behavior), taken with a solemn vow, attention on the ugliness, so the reader exits on disgust and resolve, not nostalgia — not a laboratory dose or experimental tasting. Cross into freedom on a high of joy.
- **Gate on readiness, not a schedule.** "Do you feel ready? You should be champing at the bit. If not, re-read." Behavior change follows genuine belief change; lingering reluctance is a signal to re-read, never to summon willpower.
- **Confer freedom as an instant identity.** "Don't wait to be free — you already are." A clearly marked "you are free as of now" kills the corrosive doubt of "when am I actually free?"
- **(Default = Carr's staging):** the ritual is *instructed* — the last ordinary instance, the solemn vow, congratulations the moment they do. Readiness is gated, then the threshold is crossed on command, joyfully. After the vow: ordinary days (mornings, shops, food) and a short recap — not three teaching manuals.

### 5.10 Relapse-proof (the entire back half)
- **Never reopen the decision.** Name decision-doubt as the *only* real remaining danger.
- **Reframe the thought, don't suppress it (the pink-elephant principle).** You cannot *not* think about something; instead attach a joyful response to the thought whenever it arises ("Fantastic — I'm free!"), converting an intrusive craving into a recurring hit of relief.
- **Rejoice at a dead enemy, don't mourn a lost friend.** The single most important post-quit emotional instruction. Same factual loss, two opposite emotions — only celebration is relapse-proof.
- **Ban substitutes and police internal phrasing.** Any "instead" or "I can't have X" smuggles deprivation back in. Drill the positive construction ("Great, I'll have…").
- **Pity, don't envy, others still doing the behavior.** Hand the reader a script for re-seeing them as suffering, not indulging — so social exposure reinforces the belief instead of threatening it.
- **Don't evangelize.** Preaching breeds defensiveness in friends and drags the fresh convert back into arguments that reopen their own doubt. Let visible ease do the recruiting. (Burgeon: "you can't help people while drowning.")
- **Forgive slips in advance.** A lapse is a warning (rumble strip) or feedback ("a lesson to slow down"), never a failure or proof you've "blown it." This dismantles the all-or-nothing shame spiral that turns one slip into full relapse. **Critical:** "got away with it" never licenses a deliberate repeat.
- **(Behavior-dependent, per Fork 5):** either "change nothing else, inhabit the old contexts confidently" (Carr) or "redesign your environment and transmute the freed energy into a positive direction" (Burgeon).

---

## 6. Emotional-framing techniques

The argument changes the belief; the *framing* makes the belief feel safe to adopt. Most relapses are emotional, so framing is not decoration — it is load-bearing.

- **Change the reader's emotional expectation of the process up front.** Recast quitting as "an exciting adventure," the read as "day one" of it. Dread closes the mind you need open. Pre-empt and *forbid* the expected misery: "Cast aside all feelings of doom and gloom — there's no need to be miserable."
- **Make the goal an emotion, not a behavior.** Not "abstinence" but "happy to be free." A reader who merely abstains while feeling deprived is primed to relapse. Distinguish "free" from "happy to be free" explicitly.
- **Hard truth, then relief.** Deliver the hard fact, then in the same breath the relief. Never leave the reader in dread. Never announce the move. This is writer execution, not a card Voice/guardrail string.
- **Validate the feeling before disarming it.** Acknowledge the fear/shame/pain sincerely *first* ("it can be frightening to admit this"), then hand the relief. Emotion acknowledged, never bulldozed. (Freedom Model: "we each seriously contemplated suicide" — earn the word "easy.")
- **Reflect the reader's suppressed unease back to them.** "We instinctively sense that something has taken hold of us." Accurate emotional diagnosis builds more trust than any argument.
- **Blame the method, not the reader, for past failures.** "No wonder you failed — you were never shown the trap. This time is different." Past defeats become evidence the old approach was wrong, restoring hope.
- **Engineer pride and excitement as the reward.** "Think how proud you'll feel." "You can get *excited* about this." Substitute a positive future emotion for the fear of loss.
- **Make the *status quo* feel like the burden.** Quantify the lifetime cost — money, hours, health, "every single day forever for something you don't even need." Reframe *continuing*, not quitting, as the painful ongoing sacrifice.
- **Cast the reader as the heroic underdog.** They weren't weak — they were a lone individual against "armies of scientists weaponizing abundance" (Burgeon). Absolves and dignifies.
- **Use awe as persuasion.** A reverent catalogue of the body's/mind's natural sophistication makes overriding it with a crude external fix feel like vandalism. Emotion (awe) doing the work of argument.
- **Hope as near-certainty, concretely.** "9 out of 10 people get past this on their own." A repeatable statistic normalizes self-change and discredits the fragility model.
- **Relief is available *now*.** Relocate the payoff to the present moment — "the immediate benefit is the weight off your shoulders" — sidestepping "but I won't feel better for months."
- **Money/practical gains are a *bonus*, never the motive.** Demote the practical incentive deliberately: quit because *you'll enjoy life more*. A money-motivated quitter still secretly believes they sacrificed a pleasure.

---

## 7. Voice & style rules

- **Warm, direct, second-person.** Talk *to* one reader, like a trusted friend who has been where they are. Anticipate their objections in real time ("I know this is hard to accept, but…").
- **Warm to the person, harsh to the trap.** Never an ounce of contempt for the reader. Plenty for the industry, the lie, the behavior itself.
- **The escaped expert, speaking with total authority.** Carr's register is a fellow escapee who has since freed millions and *knows he is right*: warm complicity about falling into the trap ("we've all been there"), absolute certainty about the way out. He issues verdicts and instructions without embarrassment. Never water this down into peer-to-peer humility or renounced authority — hedged authority reads as not-Carr instantly.
- **Short, blunt verdict-sentences after a build-up.** Let the cadence perform the certainty. "It's the other way around." "Don't wait to be free — you already are." Land the point, then stop.
- **Plain, confident, repetitive refrains.** Repeat key promises verbatim like a chorus ("nothing to lose and everything to gain"; "escape, not sacrifice") to embed them.
- **Rhetorical questions that close escape routes.** Make the reader keep catching themselves in self-contradiction and concede the point internally.
- **Coin a small, proprietary vocabulary** — a memorable name or two the reader will think in afterward (Carr's Little/Big Monster; Burgeon's "Pang," "energy vampires"). Once named, a concept can be invoked in a phrase. *Per Fork 1, the mechanism characters are personified at full Carr strength (original, behavior-fitted names) — and the trap/industry gets named alongside them.* Define loaded words on our terms early (redefine "failure," "giving up," "self-love," "success") to install our interpretive lens.
- **Concrete analogy over abstraction, every time.** The tradition runs on vivid, everyday images (see §11). When you must explain a mechanism, reach for a picture, not a definition.
- **Anecdote as gentle proof, not data.** A lived human story carries an abstract point better than statistics. Use sparingly and warmly.
- **ALL-CAPS for the few real climaxes and the core commitments** — used sparingly, it gives the prose a scannable spine and makes key beliefs shout off the page. Do not overuse.
- **Confessional vulnerability buys credibility.** The author's own humiliating moment (cake from the trash; 100-a-day habit; years of relapse) proves the principle and signals "I will never look down on you."
- **Never moralize.** No "you should be ashamed," no lecturing, no purity. Good and bad are reframed as *what leads to freedom vs. what leads back into the trap* — not virtue vs. vice.

---

## 8. The structural / chapter-arc template (built on the caffeine book)

The caffeine book's architecture is our proven scaffold, generalized to **any** behavior. The numbered headings below are rooms on the three-part spine, not a chapter-per-function layout. Merge or omit freely. Do not emit one chapter per heading. Behavior change is deferred until the belief is changed. This is a spine of rooms, not a chapter-per-function course.

> Adapt freely. Preserve this *spine*:
> **First third — install the world.** Easy contract and instructions; the reader is already hooked (not a later unit); name the two creatures in passing when the trap is first seen (then they are vocabulary, not a lesson); body, instinct, and real food as concrete encounters so later demolitions have ground — not a three-word refrain.
> **Middle — demolish on that ground.** Kill justifications and the inversion on the world already installed. One chapter's primary job *inhabits* the ordinary doing (eating, for an eating book) — not a kill with inhabit as flavor. Distinct rooms: long testimony lives in the main flow; a prevalence claim appears once.
> **After the vow — life, not manuals.** The ritual is the last ordinary meal (or last ordinary instance), not a laboratory dose. Then one ordinary-life chapter (mornings, shops, food — thoughts the reader already owns, once; live those days, do not restage settled scenes or teach a thought-curriculum). Then a short recap — a photographable list, not three teaching chapters.

### FRONT MATTER — Trust & expectation (before any argument)
- Establish pedigree and an "easy" expectation. Origin myth / lived escape. Voice the reader's skepticism and answer it. Set the emotional expectation: adventure, ease, no doom. (§5.1, §6)

### CH. 1 — Invitation & the instructions
- Convert audience → participant. The numbered instructions land as spoken commands (open mind, don't quit yet, start happy). The no-risk frame. State the goal as an *emotion* ("happy to be free"). The reader investigates; the author directs with total confidence. (§5.2)

### CH. 2 — "Is this even a problem?" — dissolve choice & complacency
- The confidence-trick reframe + the "who's in charge?" trap to dissolve the illusion of free choice without blame. Normalize the harm so the reader stops trusting their sense of "normal." Remove shame; name the trap. Name the two creatures in passing here — then they are vocabulary, not a later unit. Body, instinct, and real food arrive here as concrete encounters (watch eating; the body as authority), not a three-word refrain. (§5.3)

### CH. 3 — Switch the evaluation axis
- Refuse "harm vs. benefit"; demand "what benefit at all?" Introduce "doing TO vs FOR you." Speak it; never as a ledger or worksheet. Demolition follows on ground already laid. (§5.4)

### CH. 4 — Demolish the benefits one by one
- Collect the reader's justifications; demolish each by isolating the variable and reassigning credit. This may span multiple chapters. Leave no foothold. One of these chapters has inhabit-the-ordinary-doing as its primary job, not a kill with inhabit flavor. (§5.5)

### CH. 5 — The mechanism: the inversion
- The core inversion (the high is relief from a self-created low; you never beat baseline). The rescuer-as-perpetrator image. Split the trivial physical part from the dominant belief part, using creatures already named. Name the brainwashing and who installed it. This is a deepening, not a debut unit. (§5.6)

### CH. 6 — Close the escape routes
- Foreclose cut-down, "keep the special ones," quit-tomorrow, weaning. Pre-script and pre-discredit the reader's future rationalizations. Land on the totality logic — total cessation stated as the only stable state, per Fork 2. (§5.7)

### CH. 7 — Widen the indictment (the manufacture of desire)
- Expose the engineered trap: the industry/platform/algorithm, the predatory recruitment. Re-code the symptoms the behavior claims to fix as the body's protective warning lights. (§5.6 deepened; §6 awe)

### CH. 8 — The strongest case, met head-on
- Take the single most seductive pro-behavior scene and reassign every drop of its pleasure to its true source ("sneaking a ride"). A hands-on demonstration that the mind accepts falsehood as true primes the reader to distrust the felt "benefit." (§5.5)

### CH. 9 — Demystify
- Reframe "addiction" as a simple, correctable misunderstanding — stripping the disease-for-life dread. The positive authority (body, instinct, real food) is already encountered in the first third; do not delay it here as a teaching chapter or plant it as a slogan.

### CH. 10 — The quit (the last ordinary instance)
- Gate on readiness. The ritual is the last ordinary meal (or last ordinary instance), not a laboratory dose. Confer freedom as an instant identity — the vow instructed, the congratulation immediate. (§5.9)

### CH. 11 — Ordinary life
- One chapter of mornings, shops, food. Thoughts the reader already owns, once — not a new curriculum. The §5.10 moves that still belong live here as speech, not as a doctrine manual.

### CLOSE — Short recap, then life
- A photographable list of the spoken instructions, then an outward imperative ("get on with enjoying your life"). Not three teaching manuals. Not chapter-number callbacks.

### Two recurring structural devices to reuse
- **Quarantine hard evidence** (raw citations, stats) into a back-matter appendix so the main prose stays emotionally clean (Burgeon).
- **A short recap list** at the end — the spoken instructions, photographable — not a mid-book instruction recap and not a portable teaching manual.

---

## 9. Do's, don'ts & guardrails

These are the lines that keep the method intact. **Violating a guardrail breaks belief-change even if the prose is good.**

### Always (the non-negotiables)
- **Frame as escape, not sacrifice.** Every chapter. If a passage makes quitting feel like loss, it is wrong.
- **Non-shaming.** Warm to the person, harsh to the trap. Always.
- **Immediate freedom.** Freedom is conferred at the moment of belief-change / the final act — never a future milestone, never a sentence to be served.
- **No willpower.** Never present grit, resistance, or "staying strong" as the solution. Willpower is reframed as a *symptom* of a belief not yet changed.
- **Attribution-reassignment.** Every claimed benefit gets reassigned to its true source. Never concede the behavior a real benefit.
- **Counter-brainwashing.** Name the installed belief and its installers; position quitting as de-programming, not deprivation.
- **The ritual / chosen quit.** Stage the threshold as a positive, deliberate, reader-owned act.
- **Relapse-proof the belief.** The back half guards the mind; slips are pre-forgiven; the thought is reframed not suppressed.
- **Make the reader reach the conclusion — inside a frame of flat assertion.** Carr asserts constantly ("The fact is...") *and* runs the trap questions whose only honest answer concedes the point. Keep both: settled-fact delivery for the reframes, Socratic traps for the reader's own evidence.
- **Gain-frame the alternative.** Stopping = acquiring a better life.

### Never (the failure modes)
- **Never shame, lecture, moralize, or express contempt for the reader.** Instant trust death and a relapse driver.
- **Never *end* on fear — scare, then disown, exactly like Carr.** The hard material is delivered at full force (Carr frightens freely and flatly), then fear is not left as the reason to change: the chapter re-lands on escape-joy. Writer execution — do not paste this as a card Guardrails line. Two failure modes, equally off-reference: leaving the reader quitting *out of* fear, and omitting or softening a scare Carr would have delivered.
- **Never demand willpower or "just stop."** That's the wrong method we're replacing.
- **Never let "instead"/"I can't have X"/"giving up" stand** — they smuggle deprivation back in. Police your own phrasing as strictly as the reader's.
- **Never leave the mechanism characters unused** (per Fork 1) — the Little/Big-Monster device is load-bearing Carr machinery. The craving is personified as a small, starving, already-dying parasite (never a mighty enemy demanding willpower), and the belief-system feeding it is the real target.
- **Never concede a single real, irreplaceable benefit to the behavior** — one surviving "good reason" re-powers the whole trap ("unplug every cord").
- **Never make freedom contingent on time, streaks, or day-counting** — that keeps the behavior alive as something still missed.
- **Never catastrophize a slip** — that triggers the all-or-nothing collapse. But never let a slip *license* a deliberate repeat either.
- **Never apologize for the instructions.** The method commands — numbered, confident, cheerful — and treats following ALL of them as the reader's own smart choice (per Fork 2). What stays banned is nagging *without* the belief-work: a command may only cash in an argument the book has already won.
- **Never cushion a belief landing with coaching stage directions or permission language.** Cut cues such as “sit with this,” “let that land,” and “if you wish”: once the argument has earned its conclusion, issue a cheerful direct command or state the conclusion as settled fact, then ask the trap question whose only honest answer completes the credit inversion.
- **Never bog the prose down in a literature review.** Quarantine citations; keep the argument clean and emotional.
- **Promise at Carr's amplitude — "easily, immediately and permanently" — and no further.** Carr states the impossible-sounding contract with total confidence and delivers the gains big (freedom, energy, self-respect, the end of the slavery), but he never promises unrelated "superpowers." Match his amplitude; don't exceed it and don't shrink it.
- **Never tell the reader to white-knuckle-avoid triggers** as the strategy. Either inhabit old contexts confidently (Carr) or redesign environment as support (Burgeon) — but avoidance-as-resistance silently concedes the behavior still holds power.

*Retired-rule note: the pre-2026-07-12 versions of two "Never" entries above banned fear-as-motivator outright and banned commands. Both bans are retired by the Fidelity Doctrine — the corpus deploys fear at full force (then disowns it) and commands cheerfully. The rewritten entries above are the binding forms.*

---

## 10. Behavior-agnostic adaptation playbook

Before writing for a new target behavior, run it through this checklist. The master plan should answer all of these and hand the answers to chapter-writers.

### Step 1 — Find the load-bearing false belief
What does the reader believe this behavior *gives* them? (Relief, escape, focus, connection, excitement, comfort, identity, reward.) This single belief is the whole book's target. Name it in one sentence.

### Step 2 — Name the illusory benefit and its true mechanism (the inversion)
How does the behavior *create* the very discomfort it then relieves? Build the behavior's version of "the high is relief from a self-created low." Examples of the shape:
- **Gaming:** the restlessness, boredom, and flatness of real life feel worse *because* the game has hijacked the reward baseline; the game relieves a hunger it manufactured. The "achievement" is a manufactured itch scratched.
- **Doom-scrolling:** the anxiety and FOMO the feed soothes are largely produced *by* the feed; each scroll relieves the agitation the previous scroll created. You never feel *informed* — only briefly less anxious.
- **Sugar / junk food:** engineered cravings and the energy crash that follows each hit drive the next; the "treat" relieves a low the last treat caused.
- **Porn (Burgeon):** tight shoes — pleasure is relief from self-inflicted discomfort; dopamine crashes below baseline.
Find the **rescuer-as-perpetrator image** for this behavior.

### Step 3 — Inventory the reader's justifications (to demolish)
List every reason a user of *this* behavior gives ("it relaxes me," "it's how I socialize," "it's the only thing that's mine," "everyone does it," "it's harmless," "I've earned it"). Each gets a §5.5 demolition: isolate the variable, reassign the credit. Merge freely; do not emit one chapter per justification. One mid chapter’s primary job is inhabit-the-ordinary-doing, not a kill.

### Step 4 — Identify the engineered villain (the manufacture of desire)
Who profits and how was the hook built? (Game studios and variable-ratio reward loops and "engagement"; social platforms and infinite-scroll + notification design; food engineers and bliss-point formulation; the porn industry and the Coolidge-effect novelty machine.) This is the external villain the reader can be angry at — channeling anger away from self-shame.

### Step 5 — Decide the physical/chemical reality and how light to go on science (Fork 3)
Is there a real withdrawal (and how trivial)? What's the neuroscience that makes the trap *visible*? Decide how much, and quarantine citations. Always subordinate fact to belief-change.

### Step 6 — Decide: natural baseline, or root + replacement? (Fork 5)
Does this behavior have a clean natural baseline the body returns to (lean Carr: "change nothing else"), or does it fill time/identity/emotion (lean Burgeon: name the **root craving** — love/superiority/pleasure/risk or the behavior's analog — and supply a **positive direction** and environment redesign)? **Default (Carr, per Fork 5): "change nothing else" — the natural baseline returns on its own.** Root + positive direction is a brief-level override reserved for behaviors that genuinely occupy time/identity — and must be stated explicitly in the master plan. State the decision.

### Step 7 — Translate the analogies
Every signature analogy (§11) should get a behavior-specific re-creation. Don't reuse Carr's caffeine images literally; build the gaming/scrolling/sugar equivalent that lands the same mechanism. **Write original images.**

### Step 8 — Foreclose this behavior's specific escape routes
What will *this* reader reach for? ("I'll just play on weekends." "I'll only check it twice a day." "I'll allow dessert on Fridays." "I'll switch to a less-bad version.") Pre-script and pre-discredit each (§5.7).

### Step 9 — Find this behavior's strongest, most seductive scene
The hardest case to argue against (the cozy Sunday gaming session; the morning scroll in bed; the shared dessert on a date). Meet it head-on and reassign its pleasure (§5.8 / §5.5).

### Step 10 — Define the "moment of revelation" to predict
What ordinary future moment will prove freedom to *this* reader? (A boring commute that no longer needs the feed; an evening that no longer needs the game.) Name it so the reader anticipates it as a joyful milestone.

---

## 11. Exemplar techniques & lines to echo IN SPIRIT (write original prose)

These are the *shapes* that work — drawn from the three books. **Do not copy them.** Study what makes each land, then build the original equivalent for your behavior. (The signature analogies are listed so you can re-create their *function*, not their words.)

### The master analogies — re-create their function
- **The safe/combination lock** (Carr): quitting is a knowledge problem with an exact solution; miss one piece and you stay trapped — justifies "follow the whole argument."
- **The confidence-trick / fraudulent investment** (Carr): you were defrauded on phoney information, not foolish — dissolves choice without blame.
- **Lennie & George / rescuer-as-perpetrator** (Carr): grateful to the one who secretly pushed you in — the inversion in one image.
- **Tight shoes** (Burgeon): the "pleasure" is only relief from a self-inflicted pain — the flagship illusion-exposer. (The single most reusable inversion image in the canon.)
- **The cliff-jump for moderation** (Carr): "jump off as long as you don't fall more than a few metres" — the absurdity of safe limits on a trap.
- **The pink elephant** (Carr): you can't quit by forbidding the thought — reframe how it *feels* instead.
- **Mourning a friend vs. an enemy's death** (Carr): same loss, two emotions, only celebration is relapse-proof.
- **The caged lion / "fruited plains of freedom"** (Freedom Model): the freed creature hovers by the open cage out of habit — post-change anxiety is cage-habit, not proof you still need the trap.
- **"How do you quit a job? You say 'I quit'"** (Freedom Model): the act is trivial; all the work is in the wanting — strips quitting of its mystique.
- **Lifting weights doesn't make you punch people** (Freedom Model): physical/brain change facilitates but never *compels* a behavior — collapses the "my brain made me" defense.
- **The big house vs. the apartment** (Freedom Model): people knowingly take on huge costs for perceived happiness — so a costly behavior proves nothing about being "involuntary."
- **The limbic brain as a dumb appliance with 100 power cords** (Burgeon): unplug 99 and it still runs — why partial belief-correction fails and totality is required.
- **The eagle raised as a chicken** (Burgeon): your captivity was a misunderstanding of your own nature; freedom is recognizing what you always were.
- **The boiling frog** (Burgeon): harm so gradual you never noticed — why you feel "fine" while being damaged.
- **"You wouldn't eat poison in moderation"** (Burgeon): collapses the "just do it less" rationalization.
- **Pet rocks** (Burgeon): you're secretly attached to the problem because it gives you identity and direction — pre-empts the post-freedom void.
- **The optical-illusion tables** (Carr): a hands-on proof that your own perception accepts falsehood as true — primes acceptance that the "benefit" is illusory.

### The shape of a killer line (echo the rhythm, write your own)
- **The instant-freedom line:** *"Don't wait to be free — you already are."* → Write your behavior's version: freedom is conferred now, not earned over time.
- **The TO/FOR ledger:** *"It is doing plenty TO you. It is doing nothing FOR you."* → A crisp two-column verdict.
- **The inversion thesis:** *"The boost comes from the low it created."* / *"Porn creates the stress."* → State the rescuer-as-perpetrator as a flat fact.
- **The axis-switch:** *"I'm not asking whether it does more harm than good. I'm asking — what good is there at all?"*
- **The no-sacrifice reveal:** *"There's nothing to give up; on the contrary, you are facing freedom."*
- **The happiness redefinition:** *"People choose the happier option — the whole argument is in the '-er.'"* → Make "but I'm miserable" into confirmation, not rebuttal.
- **The autonomy/permission close:** *"You can do whatever you want. But will you?"* → Granting the freedom to relapse proves the desire is gone. *(Freedom-Model register — brief-level override only; Carr's default close is the commanded vow and the instant ALL-CAPS congratulation, per Fork 2.)*
- **The dignity line:** *"It's a fallacy that you're weak. You were outgunned by an engineered trap."*
- **The self-discovery thesis:** *"Freedom comes from understanding where the desire comes from, not from trying to end it."*
- **The reframe of the goal:** *"You won't just be free; you'll be happy to be free."*
- **The pity script:** *"Does that really look like enjoyment? You are not being deprived — they are."*
- **The slip-forgiveness:** *a lapse is a rumble strip, not a crash; a lesson to slow down, not evidence you've failed.*
- **The growth reframe (close):** end by revealing the whole effort was never about quitting — it was about *growing*.

### Verbatim source lines — for your reference ONLY (never reproduce; absorb the move)
- *"To find it easy to quit, you must achieve a frame of mind whereby, whenever you think about [it], you feel a sense of freedom and relief that you don't [do it] anymore."* — the literal definition of our goal state.
- *"Some people believe my method is a form of brainwashing… But it does involve counter-brainwashing and the reversal of beliefs you may have held your entire life."*
- *"It takes no willpower whatsoever to avoid watching a movie that doesn't interest you. That's what it's like when Easyway sets you free."*
- *"With all addictions, it's not where you are going to that is important, it's what you are escaping from that counts."*
- *"You don't get cravings; you actively crave… Craving isn't a thing or a force; it's an activity you choose to do."* (Freedom Model)
- *"'The quit' didn't come from a sense of freely pursuing the happiest option; it came from feeling cornered."* (Freedom Model — why shame-quits fail)
- *"When deep understandings are made, changes happen almost automatically."* (Burgeon)
- *"Freedom is found on day 1… when you let go of the attachment… When you stop chasing."* (Burgeon)

**Final reminder on originality:** We learn the *mechanism*, never reproduce the text. Every analogy, every line, every scene you write is original prose built to perform one of the eight engine-functions in §3. When in doubt, return to §3 and ask: *which function is this passage performing, and does it make stopping feel like escape rather than sacrifice?*

---

## 12. Pre-flight checklist (run before submitting any chapter)

- [ ] Which of the eight engine-functions (§3) does this chapter perform? (If none — rewrite.)
- [ ] Does every passage frame stopping as **gain/escape**, never loss/sacrifice?
- [ ] Is the tone **warm to the reader, harsh to the trap** — zero shame, zero lecture?
- [ ] Did I **reassign every benefit** I touched, conceding nothing real to the behavior?
- [ ] Is **willpower** absent as a solution (and reframed as a symptom where it appears)?
- [ ] Did I run the **trap questions inside a frame of flat settled-fact assertion** — Carr's balance (§9): "The fact is..." delivery for reframes, Socratic traps for the reader's own evidence?
- [ ] Are my **analogies original** to this behavior (not lifted from caffeine/porn)?
- [ ] Did every scare **land at full Carr force and then get disowned** (Fork 3)? Are the **mechanism characters** doing their work (Fork 1)? No **"instead"/"giving up"** phrasing?
- [ ] If this is a back-half chapter, does it **guard the belief** and **pre-forgive slips** without licensing them?
- [ ] Does it sound like **Carr — the escaped expert with warm, total authority** — commanding without apology and asserting reframes as settled fact?


---
---

# PART B — THE PROSE ENGINE (how Carr actually writes)

> **Status:** Derived from a full computational + close-reading analysis of *The Easy Way to Quit Caffeine* (see `analysis/easyway-prose-patterns.md`). Part A gives you the worldview and the argument; **Part B is the binding writing contract** — it governs the actual sentences. Where Part B is more specific than Part A, Part B wins.
>
> Everything here is **behavior-agnostic**. Anything behavior-specific lives in the master plan's per-book sheets (§B8), which the master-plan step derives using this section plus the research banks.

---

## B1. THE REPETITION LAW (the one rule that reconciles everything)

Easyway prose is built on deliberate, scheduled, *verbatim* repetition of a small set of fixed phrases — and on the near-total absence of accidental repetition everywhere else. Our pipeline's context strategy (chapter writer sees only the master plan + the previous chapter) suppresses accidental repetition by design. That means the deliberate repetition **cannot emerge on its own — it must be specified**. Hence:

**THE LAW: Mantras are repeated VERBATIM when the frozen line is the natural next sentence, exactly as frozen in the master plan's mantra sheet. There is no per-chapter quota. Everything else is never repeated verbatim.**

- A mantra is an incantation. Its power comes from arriving in *exactly* the same words every time, so it accumulates weight and eventually fires in the reader's head unprompted. **Paraphrasing a mantra kills it.** If the mantra sheet says "you have nothing to lose and everything to gain," you may not write "there's no downside, only upside."
- Conversely, any striking sentence that is *not* a mantra must appear once and only once in the book. If you find yourself rebuilding an argument the master plan says a previous chapter already made, invoke its mantra token instead of re-arguing it.
- The chapter writer never invents a new mantra and never alters one. Mangled assigned mantras are defects. A chapter with no assigned mantra is not a defect.

---

## B2. The Mantra System

### The lifecycle (how a belief gets installed)

Every core belief in the book runs the same four-stage lifecycle:

1. **ARGUE** — the belief gets one full treatment in its debut chapter: the argument, the analogy, the emotional landing. This happens exactly once.
2. **COMPRESS** — within or at the end of the debut, the belief is crystallized into a fixed phrase: the mantra. The compression should feel like the chapter's conclusion arriving in portable form.
3. **REPEAT** — later chapters re-invoke the mantra verbatim, *without re-arguing it*. Each repetition is brief — a clause, a reminder, a drumbeat — and lands in a new context, which is what generalizes the belief.
4. **HAND OVER** — in the book's final movement, the mantra is explicitly given to the reader as a thought script: "whenever you think X, replace it with [mantra]." The book ends by transferring its own voice into the reader's inner monologue.

### The mantra archetypes (every book instantiates these)

The master plan must derive a per-book **mantra sheet** instantiating each archetype with frozen wording adapted to the target behavior. Six to ten mantras total. A mantra debuts once, in the chapter that argues it; later chapters echo it when the frozen line is the natural next sentence. There is no per-chapter quota. Mantra IDs are lettered (M-A, M-B, …), never numeric, so they cannot collide with instruction I-08.

| Archetype | Job | Carr's instance (reference) | Placement rule |
|---|---|---|---|
| **The entry promise** | Risk-reversal that buys the reader's compliance with the instructions; deployed at the exact moments the reader is asked to believe something outrageous | "you have absolutely nothing to lose and everything to gain" | First 10% of the book, 2–3×; may return once near the quit |
| **The promise triad** | The impossible-sounding contract, stated with total confidence | "easily, immediately and permanently" | Front matter + method chapter; heavily front-loaded, then assumed |
| **Trap metaphor** | The central metaphor that makes stopping an *escape*, not a sacrifice | "the caffeine trap" → ours: "the [X] trap" | Debuts early, frequency *rises* toward the exit chapters |
| **Illusion phrase** | A fixed dyad/phrase that names the perceived benefit so it can be referenced and demolished as a single object | "a genuine pleasure or crutch" | Debuts in the axis-switch chapter; thereafter the perceived benefit is *only ever* called by this token |
| **Two creatures** | Named, proprietary vocabulary for the two-part mechanism (physical loop + belief), so one word re-invokes the whole argument | "the little monster" / "the big monster" — *per Fork 1, every book personifies both, under original behavior-fitted names* | Named in passing when the trap is first seen (first third); then vocabulary, not a unit |
| **Sensory phrase** | A canonical adjective-string describing the behavior's discomfort/withdrawal, repeated identically so the reader re-labels their own body in our words | "a mild, empty, slightly insecure, slightly uptight feeling" | Debuts with the creatures; repeated whenever withdrawal/craving is mentioned |
| **The stakes phrase** | A dual-valence time-horizon phrase used as BOTH threat and reward | "for the rest of your life" (hooked... / free...) | Spread throughout; both valences must appear |
| **The cost formula** | The fixed word-triple naming the addict's permanent state | "tired, run down and lethargic" | Recurs wherever the behavior's ongoing cost appears |
| **Fact cadence** | Not a phrase about the behavior but a repeated cadence that trains the reader to receive reframes as settled fact | "The fact is..." | Evenly spread; do not count per thousand words |
| **The replacement thought (terminal mantra)** | The thought script the reader keeps forever; what to think whenever the behavior crosses their mind. ALL-CAPS, exclamatory, joyful | "FANTASTIC! I'M FREE!" | Debuts near the vow and repeats there; it is the book's final word on the subject |
| **Anti-method name** | The enemy METHOD (not just the enemy substance): every past failure is reattributed to it, never to the reader. Keep **the Willpower Method** as this book's named anti-method. | "the Willpower Method" | Defined early; recurs wherever failure, sacrifice, or "hard to quit" appears |
| **Conflict image** | Names the addict's torn state and gives it a geometry whose resolution is built in: both ropes belong to the trap | "the tug-of-war (of fear)" (23×) | Debuts with the trap chapters; owns the fear chapter; echoed until the quit |
| **Positive authority** | The alternate authority the reader obeys AFTER the brainwashing is gone — paired with 1–3 operational instruments so freedom comes with tools, not just beliefs | body, instinct, real food (and any book-fitted name) | First third as concrete encounters, not a three-word refrain; not a late teaching chapter |
| **The claim block** | The full-sentence promise repeated verbatim as a set-piece (a mantra at paragraph scale) | the book's own eat-what-you-want contract, frozen on the sheet | Planted in ch. 1; re-quoted mid-book; returns at the pre-quit pivot |
| **Ease clause** | The recurring clause that closes every loop by restating the contract's ease | "All you have to do is follow (all) the instructions." | Sprinkled throughout; especially at chapter ends and after hard arguments |

### Mantra sheet format (lives in the master plan)

For each mantra: **(a)** frozen exact wording — including capitalization and punctuation; **(b)** archetype; **(c)** the belief it installs; **(d)** debut chapter (where it gets its full argument); **(e)** echo chapters (where the frozen line is the natural next sentence — not a quota); **(f)** hand-over form (how the final movement gives it to the reader). Cards that debut or echo a mantra pin the frozen quote on the card and cite the lettered ID.

---

## B3. The repetition schedule (the shape of the whole book)

The analysis of the caffeine book shows concept frequency is *engineered as curves*, not constants. The master plan must lay these curves; chapter writers must know where on each curve their chapter sits.

- **Cumulative lexicon.** Each named concept has a debut chapter, then joins the permanent recurring vocabulary. Nothing important is said once. By the final third, one sentence can invoke trap + mechanism-character + freedom + deprivation in passing, because all tokens are installed.
- **The freedom crescendo.** Freedom/escape language is established in the opening promise, then *deliberately suppressed* through the middle demolition phase, then detonated in the final quarter — the last 20% of the book should contain more freedom-language than the rest combined. The emotional shape is: promise → demolition → release.
- **Front-load the promise.** "Easy"-register words cluster at the entry (the contract), then recede — the ease is *assumed*, not re-argued.
- **The command frame opens and closes the book.** Numbered instructions at the entry (how to read); numbered instructions at the exit (how to be free); **both recapped verbatim as scannable lists at the very end.** The book repeats itself in summary — this is the only place whole sentences may repeat besides mantras.
- **Save one fresh reframe for the ending.** At least one powerful concept (Carr: "don't mourn the death of an enemy") must appear *only* in the final movement, so the ending is a revelation, not just a recap.
- **Demolition-phase vocabulary peaks mid-book** (brainwashing/illusion/manufactured desire) and largely hands off to freedom vocabulary in the back half.

---

## B4. The lexicon sheet (two registers, no neutral middle)

The vocabulary does the reframing in every sentence, whether or not that sentence is arguing. The master plan derives a per-book **lexicon sheet** with two registers; the chapter writer may not use neutral or willpower-register words for the core concepts.

- **Trap register** (for the behavior, always): the behavior's units are renamed as doses ("shot," "dose," "fix," "hit"), the behavior as a drug/trap/con, its practice as feeding the addiction, its community-normal status as brainwashing, its users as trapped/conned (with warmth — *we* were all conned). Apply the hardest-drug lexicon plausibly available to the behavior.
- **Freedom register** (for stopping and the stopped state, always): escape, free, freedom, marvellous, wonderful, exciting, rejoice, celebrate, relief, "get on with enjoying your life."
- **Banned register**: "give up," "quit cold turkey" (as framing), "resist," "stay strong," "discipline," "abstain," "sacrifice" (except when naming the *illusion* of sacrifice), "trying to stop," "one day at a time," "recovery journey." These smuggle the willpower model back in. ("Quit" itself is acceptable as a plain verb; "giving something up" is not.)
- The lexicon sheet also imports the **community's own slang** (from the research banks) for ventriloquized reader-voice — the reader must hear their own dialect in the quoted thoughts.

---

## B5. The sentence-operator toolkit (execute silently — never surface operator names in reader prose)

Voice first — write to one reader. Do not count you/your, questions, or words as a quota. Short sentences cluster at peaks. Questions close traps. Pictures do the argument. ALL-CAPS: instructions, the terminal mantra, and a few true peaks — no more.

**The pronoun triangle (non-shaming machine):** **"I"** = the guide's authority — testimony, promises, warnings. **"we"** = every description of falling into and living in the trap — the confession voice that makes ruthless critique shame-free because the author is inside it. **"you"** = instructions, promises, and the escape. **Falling into the trap is "we"; escaping it is "you."**

The operators:

1. **Fact-assertion** — deliver reframes as flat settled fact: "The fact is..." / "The reality is..." Never hedge ("studies suggest," "many people find" are banned for core claims).
2. **Self-answered question** — ask, then answer immediately with total confidence: "Do you want to stop? Of course you do – that's why you're reading this book."
3. **Concession question** — pose one question whose only honest answer concedes the point; perform it in flat Carr voice without naming, announcing, or labeling the question type.
4. **Ventriloquism** — quote the reader's inner voice in quotation marks (their justifications, their future temptations) and answer it. Early: print the full justification menu as quotes, then demolish one per chapter. Late: pre-play the future tempting thought so it arrives pre-refuted.
5. **The inversion** — "It's not X, it's Y": "It causes the aggravation; it doesn't relieve it." "It's you that's [the benefit], not the [behavior]." Often capped with: "It's the other way around."
6. **Peak verdict pair** — land two short mirrored sentences at the argument peak (build-up, then verdict); one major argument only; never name, count, promise, or announce the pair in reader prose.
7. **Reassurance–challenge cycle** — *schedule* the reader's disbelief: name it ("I know this is hard to accept"), welcome it, re-invite the open mind. Doubt is never ignored; it is pre-empted on a cadence.
8. **Upcoming-moment prediction** — predict the reader's specific upcoming thought, situation, and moment of revelation as lived experience; never coach-stage the prediction ("let me future-pace you", "future-pace this with me") or use factory labels as verbs.
9. **Permission paradox** — explicitly permit the behavior while reading ("carry on exactly as normal until you finish"). Disarms resistance and proves this isn't willpower.
10. **Credit reassignment scene** — take a cherished scene, strip the behavior out of it, show the pleasure was the scene all along ("it was only ever sneaking a ride").
11. **Instruction voice** — numbered, imperative, ALL-CAPS headline followed immediately by one short spoken rationale line; no "Warm rationale" header, craft label, or assignment-fulfillment narration around either line. Instructions are thought-substitution rules: "rather than think [old thought], think [mantra]."
12. **Chatbot residue** — never open a beat with throat-clearing or chatbot framing ("Here's the thing", "Let's dive in", "Great question", "What if I told you"). Never close a beat with a summary stamp ("In conclusion", "Ultimately", "At the end of the day", "Let's recap"). Never pad a landed point with a third stacked synonym that adds no new picture. Start the argument; stop when it lands. Do not name this rule in reader prose. Do not import a ban on Not-X-It's-Y, every/always/never, live questions, fragments, or adverbs.

---

## B6. The book architecture (Carr's structure, verified against the source)

> **Format note:** §B6 describes the compressed pocket-book architecture. For full-length books (15+ chapters), §B10 — the empirically verified full-length architecture (chapter anatomy, instruction spine, redefinition move, structural slots) — takes precedence.

Part A §8's arc stands. The verified caffeine book adds these structural specifics the master plan must honor:

- **Front matter carries the authority dossier** (origin story, scale of the method's success, the skeptical-convert testimony of the narrator) *and* the full contract: the promise triad, the entry promise, and the five reading instructions — before any argument.
- **The justification menu appears early and verbatim** — the reader's stated reasons printed as a quoted list ("It helps me concentrate." / "It's sociable." / ...), which then becomes demolition material. Do not emit one chapter per justification.
- **Chapters are short and single-purpose** (the caffeine book averages ~400 words per section under punchy titles, many phrased as questions or as the reader's own words: "Maybe I'll quit tomorrow"). One reframe per chapter; land it; stop.
- **The mechanism chapter is a deepening, not a debut unit** — the two creatures are already named in passing from the first sight of the trap; this chapter splits the trivial physical component from the dominant belief component and leans on that vocabulary.
- **The strongest case is met head-on, late** — after the easy demolitions, the single most seductive scene gets its own chapter and a hands-on perception demo (an experiential proof that the reader's felt certainty can be flatly wrong).
- **The quit is a staged ritual**: readiness gate, the last ordinary instance with a solemn vow (not a laboratory dose), instant conferral of freedom, and the warning against the two relapse doors (the bad-day rescue offer; the "just one can't hurt" thought).
- **After the vow**: one ordinary-life chapter using thoughts the reader already owns, once — not a new curriculum. Then a short recap.
- **The book ends** with a photographable list of the spoken instructions and an outward push into life — not three teaching manuals, not chapter-number callbacks.

---

## B7. The per-chapter writing contract

Every chapter delivered by a chapter writer must satisfy ALL of:

1. **One job.** The chapter makes exactly one belief-move (from the master plan), lands it, and stops. No second thesis.
2. **Mantras when they belong.** If this chapter debuts a mantra, run the full argue→compress lifecycle. If a debuted mantra is the natural next sentence, echo it verbatim and briefly — never re-argue it. There is no per-chapter must-assign quota. Invent none.
3. **Curve-aware vocabulary.** Use the lexicon registers; respect where the chapter sits on the freedom-crescendo and demolition curves (a mid-book chapter doesn't bathe in freedom language; a final-quarter chapter does).
4. **At least one concrete analogy or scene** doing the chapter's argumentative work (from the master plan's analogy assignment or the analogy bank).
5. **Carr-voice prose** per §B5 (a silent peak verdict at the argument peak, ventriloquism where the reader would object, no hedging) — never surface craft labels in reader prose.
6. **Triangle discipline**: "we" for the trap, "you" for the escape, "I" for testimony and instruction.
7. **Non-shaming and gain-framed throughout** (Part A guardrails all apply).
8. **No verbatim repetition of anything except mantras** and no re-argument of previous chapters' settled points — invoke their tokens instead.

The reviewer rejects a chapter that: mangles or paraphrases a mantra; re-argues settled material; uses banned-register vocabulary; hedges a core reframe; or drifts off its single job. Absence of a mantra on a chapter that was not assigned one is not a defect.

---

## B8. What the master plan must carry (per-book sheets)

Because chapter writers see only the master plan + previous chapter + this guide, the master plan is the carrier of all book-specific repetition. It is the **single source of truth**: every shared decision is defined exactly once under a stable ID and referenced by that ID from the compact chapter cards — never copied into competing representations. Do not duplicate occurrence counts, cumulative-state matrices, or audit tables into the plan; the chapter reviewer (`prompts/chapter-reviewer.md`) reads the draft plus the card and a computed word-budget line — never GSBS — and may demand one rewrite for plan fidelity or length ±15%; the plan carries the decision, not its bookkeeping. It must include:

1. **The mantra sheet** (§B2 format) — the frozen phrases, debut chapters, and natural-echo chapters. No per-chapter assignment quota.
2. **The lexicon sheet** (§B4) — trap register, freedom register, banned list, community slang.
3. **The justification menu** — the reader's reasons, verbatim from research, mapped to demolition chapters.
4. **The analogy assignment** — which analogy does which job in which chapter (from the research analogy bank).
5. **The curve map** — where each chapter sits on the freedom-crescendo / demolition curves; which concept debuts where; the saved-for-ending reframe.
6. **The reader state** — a planner-facing description of who this chapter speaks to (not a proper-name handle, not a pupil-persona, not P-xx codes). Compact cards carry reader-state and encounter, not a named pupil, not a `Voice:` register/job operator (`hard truth flat`, `deliver at full Carr force`, `explicitly disown`, workshop don't-panic quotes) and not a paste of the boxed CA-SAFE/CA-01 title.
7. **The strongest-case scene** and the **moment-of-revelation prediction** for this behavior.
8. **The fork decisions** (Part A §4) stated explicitly for this book.
9. **The instruction spine sheet** (§B10): the numbered instructions as spoken Carr imperatives only (CA-01: no clinical tails, no "as in I-05"), their owning chapters, and a final photographable recap list without chapter-number callbacks. No mid-book instruction recap. Include the epistemic-firewall instructions.
10. **The redefinition decision** (§B10): for behaviors that cannot be quit as a whole category, the precise Good-X/Bad-X line, the CAPS name for the bad subset, and the margin-for-error doctrine.
11. **Structural-slot assignments** (§B10): which chapter carries the long testimony in the main flow (not a labelled appendix); myths Q&A as a distinct room; meta-inoculation; the inhabit-the-ordinary-doing chapter; the last ordinary instance; ordinary life; short recap. Do not assign a mid-book instruction recap or a pre-endgame teaching manual.

---

## B9. Pre-flight checklist (Part B additions — run with Part A §12)

- If this chapter debuts or naturally echoes a mantra, is it present verbatim? Absence of a mantra is not a defect.
- Did I debut anything the master plan says was already debuted? (If so, compress to its token.)
- Any banned-register words? Any hedged core claims?
- A silent peak verdict at the argument peak? Short sentences where the point lands?
- "We" for the trap, "you" for the escape — checked?
- Does the chapter's freedom-language level match its position on the crescendo?
- Would this chapter still make stopping feel like *escape* if read in isolation?
- Any chatbot opener, throat-clearing, summary closer, or stacked-triplet padding? Cut it. Start the argument; stop when it lands.

---

## B10. The full-length book architecture (validated on *Good Sugar Bad Sugar*, ~60K words)

The pocket-book format (§B6) compresses these away; at full length Carr runs them explicitly. The master plan decides per book which rooms apply. Do not emit a chapter per slot. Source analysis: `analysis/sugar-prose-patterns.md`.

### The chapter anatomy (every chapter, no exceptions)
1. **"IN THIS CHAPTER"** — names of the rooms/pictures in this chapter, not a syllabus of what we will do, not "we will / you will," not a named pupil.
2. **Italic thesis line** — a spoken Carr sentence of the reframe, not a paste of the card's leaving-belief field.
3. **Body** — ONE belief-move, built through titled sections, landing on ALL-CAPS verdict lines.
4. **The chapter's instruction** (when assigned) — the numbered spoken ALL-CAPS imperative at the climax, plus at most one short spoken rationale line. Never a "Warm rationale" header or backticks.
5. **"SUMMARY"** — clipped bullets stating, in ordinary sentences, the belief that changed. Not a token roll-call, instruction recap, or study-design note. The final recap chapter may list the photographable instruction set.

The reader meets every reframe at least twice per chapter (argued + recapped). **Previews and summaries are licensed recap zones — exempt from the no-verbatim-repetition rule, exactly like mantras.**

### The instruction spine
- Instructions are **doled out one per chapter at the chapter's climax**, numbered cumulatively, as spoken Carr imperatives only (CA-01: no clinical tails fused into the line).
- Include all four types: behavioral ("don't quit yet"), epistemic ("keep an open mind"), emotional ("begin with elation"), and **epistemic firewalls** ("ignore any advice that conflicts with the method", "ignore anyone who quit by the Willpower Method", "avoid the influence of other addicts") — explicitly quarantining future belief-threats.
- **No mid-book instruction recap.**
- **The final recap is a photographable list** of the spoken imperatives, without chapter-number callbacks. A gate for page-skippers may tell them to start at the beginning — never "go back to Chapter N" as ledger talk.

### The redefinition move (for behaviors that can't be quit wholesale)
When the behavior category is essential or unquittable (eating, screens for work, possibly gaming-adjacent socializing), **redraw the target**:
- Define the bad subset precisely and early (ch. 1), box the definition, give it a CAPS name ("BAD SUGAR" = refined sugar + processed carbs + starchy carbs), and issue a definitional decree ("when I say X, take it to mean BAD-X").
- The CAPS name then carries the definition in every sentence (387 uses) — naming IS the repetition.
- **Run full total-abstinence trap logic inside the line** ("there is no healthy level other than zero") while the good subset becomes part of the positive authority's menu.
- **The margin for error**: a named non-catastrophic buffer for accidental/gray-zone consumption — "your body can cope with an occasional blip, but your mind will not" → a slip revives nothing unless the belief (Big-Monster-equivalent) is allowed back. Guard the belief, not the behavior. (Seatbelt image: it's there for accidents, not for driving erratically.)
- Optional **conditional-bonus extensions**: adjacent indulgences (alcohol, dairy) are NOT required to stop — "you're not reading this book to quit X" — but the upgrade is framed as an exciting option with a pointer to where help lives. Autonomy preserved; the door is left open.

### Structural slots (assign each to a chapter in the master plan)
- **The fear chapter**: dismantle fear-of-failure (the prison-door scene; "succumb to the fear of failure and you guarantee the very thing you fear") and fear-of-success (the released-convict analogy; the identity excuse), then collapse both: every rope of the tug-of-war is held by the trap.
- **The anti-method chapter**: the named anti-method gets its own chapter; the reader's strong will is REframed as evidence FOR them ("it takes a strong will to persist in something that goes against all your instincts"; "wilful, not weak-willed"); sub-characters (the braggers and the whingers); "with the willpower method, there is no finish line."
- **The identity-excuse chapter**: cause-effect inversion ("the traits shared by addicts are the RESULT of the addiction, not the cause") + the **historical-evidence operator** (population-scale statistics vs the genetic/personality claim) + the graceful concession ("even if you DID have an addictive personality, the method still frees you").
- **No pre-endgame teaching manual.** Do not audit installed beliefs as a "You know that..." course recap. If anything, a brief reminder in passing.
- **The embedded long-form testimonial**: 1–2 pages of first-person escape story with concrete numbers and sensory details, in the main flow, in its own room — not a labelled appendix. Drawn from the research banks' freedom testimonies; written original.
- **The myths Q&A battery**: a rapid-fire distinct room — each myth as a quoted reader-voice line, each demolished in 2–6 sentences.
- **The meta-inoculation**: ventriloquize the strongest objection TO THE METHOD ITSELF and answer it. Perform it; do not label it.
- **Hard facts, then relief**: where hard facts must appear, deliver them, then tell the reader not to change from fear. One short spoken clause only if the scare would otherwise be taken as a personal sentence. Honour evidence limits by not overclaiming; never narrate study design. Never announce the move.
- **Perception enacted**: 1–3 physical exercises the reader performs. The belief change is enacted, not just read. Never announce it as homework.
- **The vow**: the ritual is the last ordinary meal (or last ordinary instance), not a laboratory dose — attention on the ugliness, the solemn vow, instant conferral. Few new post-quit lines; the thoughts are ones the reader already owns. Then one ordinary-life chapter (mornings, shops, food) and a short recap, not three teaching manuals.
- **Practical-safety guardrail** (when the behavior touches medication/health): a plan-wide boxed advisory (CA-01 split: clinical limits live here, never fused into instruction rows) routing medical specifics to a professional, kept outside the belief argument. Chapter prose honours it silently or as one spoken clause; never paste the boxed workshop title mid-chapter.
```

### Brief
```
# Brief — Quit Smoking (working title)

## Target behavior
Compulsive cigarette smoking — the nicotine trap and the belief that
cigarettes give pleasure, relief, or a crutch. Total stop. Not cutting down,
not vaping as a destination, not NRT as the method.

## Reader / audience
An adult smoker who wants to quit, has likely failed by willpower, patches,
gum, or cold turkey, and believes life without cigarettes would be miserable
or impossible. General adult edition (one clear reader).

## Goal & stance — decide explicitly (style guide §4 forks)
Forks are decided by the plan-writer in the master plan; expected axes:
- **Outcome (Fork 2):** autonomy-led total freedom — last cigarette, then none.
- **Void (Fork 5):** natural baseline (non-smoker has no desire); no replacement
  ritual as the method.
- **Science weight (Fork 3):** Carr's own position — nicotine as a drug that
  creates the need it relieves; body recovery is brief; the trap is mental.
- **Villain (Fork 4):** the nicotine trap / two-headed monster (little monster
  physical, big monster brainwashing), not the smoker.
- **Inner state (Fork 1):** full Carr personification of the trap; no shame
  for the reader.

## The load-bearing false belief (style guide §10, step 1)
<one sentence, fixed in the master plan: what the reader believes smoking
GIVES them — expected neighborhood: "cigarettes relax me / help me cope /
are my pleasure, and I would be deprived without them">

## Scope / non-goals
Covers the everyday cigarette trap for a general adult reader. Non-goals:
medical treatment of smoking-related disease, pregnancy-specific clinical
advice, youth prevention campaigns, vaping-as-harm-reduction programmes.
NRT/patches/gum are named as substitutes that keep the addiction attached,
in Carr's own position — not prescribed, not recommended.

## Safety perimeter
No medical advice. No instruction to ignore a doctor. Crisis/illness
pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.
```

### Lived-experience synthesis
```
# Lived Experience — Quit Smoking

> Raw evidence packets accumulate under `research/banks/` (see
> `prompts/research-agent.md` §4); this file is the lead's curated synthesis of
> them for the master-plan stage. The inline Bank sections below are curated
> content, not the live checkpoint.

Synthesize accepted source packets only. Every bullet must name its bank, persona IDs, and source IDs; an exact quote also links its packet evidence item. Interpretations use no quotation marks.

## Persona map

| Persona ID | Function served / defining context | Applicable beliefs | Applicable banks | Source IDs |
|---|---|---|---|---|
| P-01 | The stress/relaxer — first cigarette after work, after an argument, "it calms me down"; believes the cigarette is the only off-switch | cigarette-as-off-switch; reward-for-everything; lost-best-friend | 1, 2, 3, 4, 5, 9, 10 | S-001, S-002, S-045, S-046, S-047 |
| P-02 | The social/identity smoker — after meals, with drinks, with friends; smoking is who they are and how they belong | social-glue; one-won't-hurt-when-drinking; lone-guy-outside | 1, 2, 3, 4, 5, 9, 10 | S-004, S-007, S-049, S-050, S-051, S-013 |
| P-03 | The failed-quitter — patches, gum, willpower, cold turkey; "I have no willpower"; shame cycle and relapse | quitting-is-impossible; just-one-after-months; twenty-attempts | 1, 2, 3, 5, 9, 10 | S-003, S-005, S-006, S-012, S-018, S-053 |
| P-04 | The "I enjoy it / I can control it" moderate — a few a day, "different for me", not ready, not an addict | enjoy-it; few-a-day; just-one-control; lights-are-milder | 1, 2, 3, 4, 5, 9, 10 | S-013, S-003, S-038, S-039, S-048, S-006 |

## Intervention-ready evidence units

Create a unit only when accepted packets support every field. `Implicated belief`
must quote one primary or subordinate belief clause from `00-brief.md` verbatim,
or state the belief in the reader's own mined words (persona + slot tagged),
marked `neighborhood, not frozen`.

### LEU-001 — P-01: the cigarette is the off-switch

- **Situation:** anything stressful happens; the hand is already reaching; the first puff is named as taking care of it.
- **Reader wording:** "If anything stressful happens in my life, a cigarette takes care of it."
- **Implicated belief:** "cigarettes relax me / help me cope" — `neighborhood, not frozen` (P-01, keystone-relax).
- **Persona IDs:** P-01
- **Emotion:** relief named as help, with a private knowledge that the story is false.
- **Permitted inference:** the smoker experiences a rapid "taken care of" feeling and credits the cigarette; the same writer can know the credit is false and still feel the relief.
- **Prohibited inference:** that cigarettes treat the underlying problem, or that stress without a cigarette is medically dangerous.
- **Style slots:** the-inversion; keystone-relax.
- **Safety boundary:** No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.
- **Source locator:** bank-02 B-001; S-001
- **Evidence grade:** n/a

### LEU-002 — P-02: one won't hurt with drinks and friends

- **Situation:** night out; smoking area; friends lighting up; alcohol on board.
- **Reader wording:** "You often get offered a cigarette and in that kind of environment it's hard to turn down. You don't want to be the only one not smoking and because you've been drinking, you don't think about the risks, you think one won't hurt."
- **Implicated belief:** "smoking is how I belong, and one won't hurt" — `neighborhood, not frozen` (P-02, social-identity).
- **Persona IDs:** P-02
- **Emotion:** belonging, then the easy exception.
- **Permitted inference:** the social scene plus drinking is named as the moment the "social smoker" rule collapses into "one won't hurt."
- **Prohibited inference:** that the reader must avoid all friends or all alcohol as the method of quitting.
- **Style slots:** strongest-seductive-scene; escape-just-one.
- **Safety boundary:** No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.
- **Source locator:** bank-03 L-088; S-051
- **Evidence grade:** n/a

### LEU-003 — P-03: twenty attempts and nothing stuck

- **Situation:** years of patches, gum, replacements, cold turkey; another failure is already expected.
- **Reader wording:** "I had probably attempted at least twenty times before and used most of the replacements and meds on the market with no success."
- **Implicated belief:** "I have no willpower / quitting is almost impossible" — `neighborhood, not frozen` (P-03, failed-quitter).
- **Persona IDs:** P-03
- **Emotion:** shame stacked on failed method, not a personality diagnosis.
- **Permitted inference:** repeated failed attempts with replacements and willpower are typical in this community, not proof the reader is uniquely weak.
- **Prohibited inference:** that nobody ever quits, or that replacements must be used, or that they must never be used.
- **Style slots:** escape-routes; failed-attempt.
- **Safety boundary:** No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.
- **Source locator:** bank-03 L-012; S-006
- **Evidence grade:** n/a

### LEU-004 — P-04: love the cigarette, hate being a smoker

- **Situation:** lighting up is still called heaven; the aftertaste is already shame; they do not want to give up the lighting-up.
- **Reader wording:** "the moment I light up I'm in heaven, but feel shitty afterwards. So whilst I love smoking I hate being a smoker"
- **Implicated belief:** "cigarettes are my pleasure, and I would be deprived without them" — `neighborhood, not frozen` (P-04, enjoy-it).
- **Persona IDs:** P-04
- **Emotion:** split: heaven on the light, then self-disgust.
- **Permitted inference:** "I enjoy it" can coexist with hating the identity of being a smoker; enjoyment is named at the moment of lighting, not as a day-long gift.
- **Prohibited inference:** that the reader is lying about enjoyment, or that enjoyment must be mocked.
- **Style slots:** keystone-pleasure; enjoy-it demolition target.
- **Safety boundary:** No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.
- **Source locator:** bank-01 J-028; S-013
- **Evidence grade:** n/a

### LEU-005 — P-01: cigarettes as the reward for almost everything

- **Situation:** after a class, a paragraph, a grocery run; each finish is paid with a cigarette.
- **Reader wording:** "Cigarettes were my reward for…well, almost everything. Teaching a class. Finishing a story. Finishing a paragraph. Driving 500 miles. Driving to the grocery store."
- **Implicated belief:** "the cigarette is my reward and my little party" — `neighborhood, not frozen` (P-01, reward-pellet).
- **Persona IDs:** P-01
- **Emotion:** celebration that has shrunk to a pellet.
- **Permitted inference:** the "reward" can attach to almost any completed act; the party is the cigarette, not the work.
- **Prohibited inference:** that work or driving requires nicotine, or that quitting means life has no celebrations.
- **Style slots:** special-moments; reward-for-everything.
- **Safety boundary:** No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.
- **Source locator:** bank-03 L-062; S-045
- **Evidence grade:** n/a

### LEU-006 — P-04: just one after months of control

- **Situation:** five months smoke-free; the moderate voice offers one; the chain is back.
- **Reader wording:** "I know I can never have just one. I learned that the hard way, thinking after 5 months I could control myself and just have one. Nope."
- **Implicated belief:** "I can control it / just one is different for me" — `neighborhood, not frozen` (P-04, control illusion).
- **Persona IDs:** P-04, P-03
- **Emotion:** the shock of how fast control was a story.
- **Permitted inference:** a long quit does not make "just one" safe; the smoker who learned this the hard way names it as never.
- **Prohibited inference:** that a slip dooms the reader forever if the belief is not let back in; no dare to test "just one."
- **Style slots:** genie-in-the-bottle; just-one.
- **Safety boundary:** No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.
- **Source locator:** bank-01 J-024; bank-03 L-051; S-006
- **Evidence grade:** n/a

## Brief-belief evidence gaps

### GAP-001

- **Implicated belief:** none blocking. The brief's keystone neighborhood ("cigarettes relax me / help me cope / are my pleasure, and I would be deprived without them") is supported across P-01–P-04 by accepted packets. Freeze the exact sentence in the master plan, not here.

## Bank 1 — Justification Inventory

- [Bank 1] 130 verbatim demolition targets (J-001–J-130) across four personas: off-switch/relax (P-01), identity and beer-weekend glue (P-02), willpower/replacement failure (P-03), enjoy-it / few-a-day / just-one (P-04, including Mumsnet heaven-then-shame J-028). — Persona IDs: P-01, P-02, P-03, P-04 — Source IDs: S-001, S-013, S-006, S-004, S-007

## Bank 2 — Belief Map

- [Bank 2] Keystone neighborhood present, not frozen: cigarette as stress off-switch (B-001), control illusion (B-002), reliable timekeeper (B-003), "I HAD to" after friends quit (B-005), pleasure-worth-the-risk / few-a-day (B-008, B-009), deprivation fear of losing the ritual (B-010). Variants continue B-013–B-038. — Persona IDs: P-01, P-02, P-03, P-04 — Source IDs: S-001, S-003, S-007, S-009

## Bank 3 — Lived-Experience Bank

- [Bank 3] 180 packets (L-001–L-180): stairs/wind, hourly clock, hospital scare, twenty attempts, closet-smoker hiding and Febreeze, reward-pellet days, drink+smoke "last night on earth," "I AM AN ADDICT," lost-best-friend depression after quit. P-04 daily-cost and enjoy/control filled L-036–L-060 and L-141–L-160. — Persona IDs: P-01, P-02, P-03, P-04 — Source IDs: S-001, S-045, S-047, S-048, S-050, S-053

## Bank 4 — Special-Moments Inventory

- [Bank 4] 67 scenes (S-001–S-067): patio/lighter ritual, coffee/beer/waiting, garage hide, lake-weekend re-entry, first-morning bed-before-feet, after-sex euphoria stack, after-dinner, five-hour drive deodorize ritual, dropped cherry in the car. — Persona IDs: P-01, P-02, P-03, P-04 — Source IDs: S-001, S-005, S-056, S-058, S-043

## Bank 5 — Escape-Route Inventory

- [Bank 5] 61 routes (E-001–E-061): cut-down then back up, social-only myth, just-one, gum as gin-for-whisky, patch wean, Chantix delay, vape-as-destination, dual use, harm-minimisation keep-smoking, tomorrow/not-today, food substitutes. — Persona IDs: P-01, P-03, P-04 — Source IDs: S-005, S-006, S-008, S-003, S-007

## Bank 6 — Analogy Bank

- [Bank 6] 50 candidates (A-001–A-050). SOURCED: hug-that-doesn't-let-go, timekeeper, whisky/gin NRT, lost-best-friend, reward-for-everything, heroin-same-class, dog-butts-not-me, little-parties. Two INVENTED tagged (parking-meter nicotine coins; lights as hole in a gas mask). — Persona IDs: ALL — Source IDs: S-001, S-006, S-045, S-053, S-047

## Bank 9 — Community Lexicon

- [Bank 9] 100 dialect/sensory items (D-001–D-100): hug that doesn't let go, reliable timekeeper, the stick, smober, habit smokes, closet smoker, Febreeze the hell out of myself, ciggies, bumming cigs, one won't hurt, I AM AN ADDICT, little parties, cigarette candies, can't quit now. — Persona IDs: P-01, P-02, P-03, P-04 — Source IDs: S-001, S-012, S-045, S-048, S-049, S-050

## Bank 10 — Freedom Testimonies

- [Bank 10] 29 long-form/arc packets (T-001–T-030, T-015 dropped). Breath return, never-looked-back after early hell, loved-every-cig then quit, lake/beer relapse then freedom, oral-surgery forced stop, two-year anniversary, invisible years-later quit, enjoy-hate split still at the door. Moment-of-revelation present in P-01–P-04. — Persona IDs: P-01, P-02, P-03, P-04 — Source IDs: S-004, S-006, S-016, S-015, S-005
```

### Scientific-evidence synthesis
```
# Scientific Evidence — Quit Smoking

> Raw evidence packets accumulate under `research/banks/` (see
> `prompts/research-agent.md` §4); this file is the lead's curated synthesis of
> them for the master-plan stage. The inline Bank sections below are curated
> content, not the live checkpoint.

Synthesize accepted source packets only. Every bullet must name its bank, evidence grade, source IDs, and applicable persona IDs (`ALL` when universal). Preserve material disagreement instead of averaging it away; facts make the trap visible and never serve fear.

## Intervention-ready evidence units

### SEU-001 — the ten-second hit and the rapid fade

- **Situation:** a puff; the "relief" arrives almost at once, then is already leaving.
- **Reader wording:** "When cigarette smoke enters the lungs, nicotine is absorbed rapidly in the blood and delivered quickly to the brain, so that nicotine levels peak within 10 seconds of inhalation. But the acute effects of nicotine also dissipate quickly, along with the associated feelings of reward; this rapid cycle causes the smoker to continue dosing to maintain the drug's pleasurable effects and prevent withdrawal symptoms."
- **Implicated belief:** "cigarettes relax me / help me cope" — `neighborhood, not frozen` (the inversion under the keystone).
- **Persona IDs:** P-01, ALL
- **Emotion:** the credited calm is timed to replenishment speed.
- **Permitted inference:** the "relief" is replenishment of a rapidly fading dose, not a gift that solves the original stress.
- **Prohibited inference:** every puff is a unique pleasure; "you cannot quit."
- **Style slots:** the-inversion; 10-second hit.
- **Safety boundary:** No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.
- **Source locator:** bank-07 M-003; S-009
- **Evidence grade:** SUPPORTED

### SEU-002 — the product is nicotine

- **Situation:** the pack, the cigarette, the puff — treated by the manufacturer as layers around a dose.
- **Reader wording:** "The cigarette should be conceived not as a product but as a package. the product is nicotine."
- **Implicated belief:** "this is my pleasure / a lifestyle choice" — `neighborhood, not frozen` (P-04 / P-02).
- **Persona IDs:** ALL
- **Emotion:** the hobby story collides with an internal product definition.
- **Permitted inference:** an industry scientist defined the cigarette as a nicotine package and dispenser, not as a flavour accessory.
- **Prohibited inference:** quoting an internal memo as if it were a public-health consensus paper, or as a dare to smoke more to "see the product."
- **Style slots:** engineered-villain; product-is-nicotine.
- **Safety boundary:** No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.
- **Source locator:** bank-08 V-012; S-091
- **Evidence grade:** SUPPORTED (historical industry document)

### SEU-003 — lights do not cut the dose

- **Situation:** the "mild" or "light" cigarette as the moderate smoker's bargain.
- **Reader wording:** ventilated/"light" cigarettes do not reduce human intake; smokers compensate with bigger puffs.
- **Implicated belief:** "I can control it / it's not a big deal / lights are milder" — `neighborhood, not frozen` (P-04).
- **Persona IDs:** P-04
- **Emotion:** the safer-product story.
- **Permitted inference:** machine-measured lower tar/nicotine does not mean the smoker took less; compensation is the designed human response to a nicotine-seeking dose.
- **Prohibited inference:** every smoker compensates identically, or that unventilated cigarettes are a harm-reduction recommendation.
- **Style slots:** lights fraud; control illusion.
- **Safety boundary:** No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.
- **Source locator:** bank-07 M-010, M-018, M-037; S-010, S-080, S-089
- **Evidence grade:** SUPPORTED

### SEU-004 — NRT trial odds vs how people actually try

- **Situation:** the failed-quitter is told patches are the method, or that cold turkey never works.
- **Reader wording:** licensed NRT vs control raises 6+ month abstinence (pooled RR 1.55); most smokers who try to quit do so unassisted, with unaided success around 7–8%.
- **Implicated belief:** "I have no willpower / I need a replacement or I cannot quit" — `neighborhood, not frozen` (P-03).
- **Persona IDs:** P-03
- **Emotion:** method-shopping after failure.
- **Permitted inference:** NRT can raise odds versus placebo in trials; most attempts are still unmedicated; neither fact means the reader cannot quit, and neither fact is a prescription.
- **Prohibited inference:** "you cannot quit without patches" or "cold turkey never works." The two statistics answer different questions and must not be collapsed.
- **Style slots:** escape-routes; willpower-method failure without naming a branded method book.
- **Safety boundary:** No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.
- **Source locator:** bank-07 M-013, M-015, M-039; S-077, S-078
- **Evidence grade:** CONTESTED as a single slogan; both component facts SUPPORTED in their own scopes

### SEU-005 — withdrawal is a short peak, not a new personality

- **Situation:** day two or three without a cigarette; irritability, craving, restlessness.
- **Reader wording:** withdrawal symptoms typically peak in the first few days and usually subside within a few weeks; they may begin within hours; MedlinePlus places the sharpest edge about 2–3 days after last use.
- **Implicated belief:** "I would be miserable or impossible without cigarettes" — `neighborhood, not frozen` (P-01, P-03).
- **Persona IDs:** P-01, P-03
- **Emotion:** the empty feeling named as needing the personality back.
- **Permitted inference:** the restless empty feeling is withdrawal pharmacology with a short typical peak, not proof the cigarette was the real self.
- **Prohibited inference:** withdrawal is weeks of physical torture for everyone, or that it is harmless for every person in every circumstance.
- **Style slots:** the-inversion; withdrawal time course.
- **Safety boundary:** No medical advice. No instruction to ignore a doctor. Crisis/illness pointers only. Last-cigarette ritual is ceremonial, not a dare to smoke more.
- **Source locator:** bank-07 M-004, M-005, M-021, M-029; S-009, S-081
- **Evidence grade:** SUPPORTED (population typical, not every reader)

## Brief-belief evidence gaps

### GAP-002

- **Implicated belief:** none blocking. Mechanism, inversion, villain receipts, and consequence facts needed for the brief are graded in bank-07 / bank-08. Human disagreement on "what works" (NRT trials vs unaided attempts) is kept CONTESTED as a slogan, not averaged.

## Bank 7 — Mechanism & Science Bank

- [Bank 7] [SUPPORTED] Most smokers use tobacco regularly because they are addicted to nicotine. — Persona IDs: ALL — Source IDs: S-009 — Limits / disagreement: US clinical framing; not "you cannot quit."
- [Bank 7] [SUPPORTED] About half of smokers try to quit each year; only about 6 percent succeed in a given year; most need multiple attempts. — Persona IDs: P-03 — Source IDs: S-009 — Limits / disagreement: annual success, not lifetime.
- [Bank 7] [SUPPORTED] Nicotine peaks in the brain within ~10 seconds of inhalation; acute effects dissipate quickly, driving redosing. — Persona IDs: P-01, ALL — Source IDs: S-009, S-095 — Limits / disagreement: smoked nicotine pharmacokinetics.
- [Bank 7] [SUPPORTED] Withdrawal includes irritability, craving, depression, anxiety, attention problems, sleep disturbance, increased appetite; typically peaks in the first days and usually eases in weeks. — Persona IDs: P-03, P-01 — Source IDs: S-009, S-081 — Limits / disagreement: dependent users; genetics influence severity; not torture-for-all.
- [Bank 7] [SUPPORTED] Cueing — feel, smell, sight, lighting ritual — can worsen craving even when some physiology is covered. — Persona IDs: P-02 — Source IDs: S-009 — Limits / disagreement: the "habit smoke" after coffee is a learned cue.
- [Bank 7] [MIXED] Nicotine can briefly boost attention/working memory; long-term smoking associated with cognitive decline. — Persona IDs: P-01 — Source IDs: S-009 — Limits / disagreement: do not sell cigarettes as a thinking drug.
- [Bank 7] [MIXED] Tobacco smoke (not nicotine alone) is linked to decreased MAO; acetaldehyde from burned sugars may increase nicotine's reinforcing properties (animal). — Persona IDs: ALL — Source IDs: S-009 — Limits / disagreement: preclinical / not fully identified in humans.
- [Bank 7] [SUPPORTED] Ventilated/"light" cigarettes do not reduce human intake; smokers compensate; people using lights are less likely to quit. — Persona IDs: P-04 — Source IDs: S-010, S-080, S-089 — Limits / disagreement: human smoking vs FTC-style machines.
- [Bank 7] [SUPPORTED] Licensed NRT vs control raises 6+ month abstinence (RR 1.55; authors: 50–60% relative increase). — Persona IDs: P-03 — Source IDs: S-077 — Limits / disagreement: motivated trial quitters, not all smokers; not a guarantee.
- [Bank 7] [SUPPORTED] Most smokers who try to quit do so unassisted; unaided success approximately 7–8%; less than one-third of attempting US adults use counseling and/or FDA-approved medication. — Persona IDs: P-03 — Source IDs: S-078 — Limits / disagreement: population attempts, not lifetime; not "nobody quits without help."
- [Bank 7] [CONTESTED] "What works" as a single slogan — NRT trial RR vs unaided population rates are different questions. Both facts stand; neither licenses "patches are the only way" nor "cold turkey never works." — Persona IDs: P-03 — Source IDs: S-077, S-078 — Limits / disagreement: see M-039.
- [Bank 7] [SUPPORTED] Withdrawal can be uncomfortable but is not framed as harmful on Smokefree.gov; first week is highest slip risk; symptoms fade if the person stays smokefree. — Persona IDs: P-01, P-03 — Source IDs: S-081 — Limits / disagreement: does not negate rare psychiatric complications.
- [Bank 7] [SUPPORTED] Nicotine changes how the brain works so cravings continue even when a person wants to stop; tolerance means more nicotine for the same effect. — Persona IDs: ALL — Source IDs: S-009 — Limits / disagreement: FDA/StatPearls summaries; not permanent loss of agency.
- [Bank 7] [SUPPORTED] WHO: tobacco kills more than 8 million people each year, including more than 1.3 million non-smokers from second-hand smoke. — Persona IDs: ALL — Source IDs: S-087 — Limits / disagreement: population burden; do not use body-count as the method of change.
- [Bank 7] [SUPPORTED] A tobacco product is in essence a vehicle for delivery of nicotine, sold as attractive dosage forms (Teague, RJR 1972). — Persona IDs: ALL — Source IDs: S-090 — Limits / disagreement: internal planning memo, not a clinical trial.

## Bank 8 — Villain Dossier

- [Bank 8] [SUPPORTED] BAT: low-delivery advertising should alleviate anxiety about health and enable the smoker to feel assured about maintaining the habit. — Persona IDs: ALL — Source IDs: S-010 — Limits / disagreement: historical advertising intent.
- [Bank 8] [SUPPORTED] Filters marketed as harm reduction; brown-in-use as theatre; "lights" as stay-smoking products for concerned smokers. — Persona IDs: P-04, P-03 — Source IDs: S-010, S-089 — Limits / disagreement: industry history via NCI/Wikipedia/Kozlowski.
- [Bank 8] [SUPPORTED] Philip Morris Dunn 1972: product is nicotine; pack as day's supply; cigarette as dispenser; puff as vehicle; smoke the optimized vehicle. Speed: nicotine in the brain within 10 seconds. — Persona IDs: ALL — Source IDs: S-091, S-092, S-095 — Limits / disagreement: internal research, not a consumer brochure.
- [Bank 8] [SUPPORTED] Teague 1972: starters begin for image/conformity/defiance, not a pre-existing nicotine craving; first experiences often unpleasant until tolerance. — Persona IDs: P-02 — Source IDs: S-090 — Limits / disagreement: historical RJR planning.
- [Bank 8] [SUPPORTED] Youth recruitment, Joe Camel recognition vs Mickey Mouse, retail spend over $1 million per hour class of figure. — Persona IDs: P-02 — Source IDs: S-010 — Limits / disagreement: marketing literature; spend years vary by source year.
- [Bank 8] [MIXED] E-cig "customer every waking hour until you die" is advocacy language (Polito), kept as counter-corpus to harm-reduction marketing, not as a lab fact. — Persona IDs: P-03 — Source IDs: S-011 — Limits / disagreement: educator polemic.

Sources used in this synthesis are ledger IDs in `research/sources/README.md` (S-001–S-109). Full excerpt packets exist for S-001 and S-009; bank quotes remain the live evidence items.
```
