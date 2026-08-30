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

A mantra debuts once, then echoes when natural. There is no per-chapter must-assign quota. Debut cards pin the exact wording once in plain text (no markdown backticks) and cite the lettered ID. Echo cards cite the lettered ID only — no pinned quote, no backticks, no multi-token paste inventory.

**Echo density on cards:** At most two mantra IDs on any chapter card — any mix of debut and echo. The final recap card that photographably lists the instruction set is the only exception (it may cite the terminal mantra and hand-over echoes already owned). Never assign three or more echo IDs on one card. On a vow, gate, or ritual-detonation card (structural responsibility includes readiness gate, last ordinary instance, solemn vow, or instant freedom conferral): at most one echo ID plus any debut for that card; do not stack creature-name or trap-metaphor echoes (mechanism characters, trap labels, sensory slugs) — those are already settled; the vow card owns the terminal thought and instructions, not a creature roll-call.

**Echo schedule on the sheet:** Spread echo chapter IDs across the arc so no single late chapter inherits every unsettled creature token. Echo chapters are where one frozen line is the natural next sentence — not a chapter quota and not a bundle to clear at the vow.

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

For a calibration plan, use 15 chapters. Chapter budgets must sum exactly to 54,000–66,000 words. State the arithmetic sum. Length is planned, not hoped for.

### Compact chapter cards

Give every chapter a stable ID, number, and working title, then specify only its semantic work order:

- the primary persuasive job declaration and the objection or justification it resolves;
- for every argument-bearing card: belief now, concrete subject-specific encounter, evidence-ledger IDs plus the limits the writer must not overclaim, any NEW instruction (spoken imperative only — CA-01), and the reserved-later fence;
- arc position and qualitative curve position;
- a planner-facing reader-state (who they are at this beat — not a proper-name handle, not a pupil-persona) and the concrete encounter that makes the move land; never a `Voice:` register/job operator;
- mantra and frozen-token IDs only when this chapter debuts or naturally echoes one: debut pins exact wording once in plain text; echo cites the lettered ID only — never markdown backticks, never three or more mantra IDs on one card, never multiple creature/trap-token echoes on a vow/gate/ritual card (at most one echo plus any debut there);
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
- repeated full instruction, evidence, or slot text in chapter cards (debut pinned quotes in plain text are the exception; echo cards cite ID only; never three or more mantra IDs on one card outside the final recap);
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


Revise the candidate master plan using only the reviewer's findings. Your entire reply is the complete replacement master plan and nothing else.

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
- **Ask.** The question is the next sentence. Let the reader supply the evidence and feel discovered, not lectured.
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
- **Make the reader reach the conclusion — inside a frame of flat assertion.** Carr asserts constantly ("The fact is...") and asks. Keep both: settled-fact delivery for the reframes, questions for the reader's own evidence.
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
- **Never cushion a belief landing with coaching stage directions or permission language.** Cut cues such as “sit with this,” “let that land,” “if you wish,” “Let me show you,” “plainly and kindly,” “I want you to feel,” “Stay with me,” “Now I want you to feel”: once the argument has earned its conclusion, issue a cheerful direct command or state the conclusion as settled fact, then ask. The question is the next sentence.
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
- **The safe/combination lock** (Carr): quitting is a knowledge problem with an exact solution; miss one piece and you stay trapped — **planner-facing only**. Spoken instruction list lives on the front-matter instruction block and the final photographable recap, not as a mid-arc coda on demolition cards.
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
- [ ] Did I assert the reframe as settled fact, then ask — Carr's balance (§9): "The fact is..." delivery for reframes, questions for the reader's own evidence?
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

For each mantra: **(a)** frozen exact wording in plain text — including capitalization and punctuation, never markdown backticks; **(b)** archetype; **(c)** the belief it installs; **(d)** debut chapter (where it gets its full argument); **(e)** echo chapters (where the frozen line is the natural next sentence — spread across the arc, not a per-chapter quota and never a bundle cleared on the vow card); **(f)** hand-over form (how the final movement gives it to the reader). Debut cards pin that wording once in plain text and cite the lettered ID. Echo cards cite the lettered ID only. No chapter card carries three or more mantra IDs; vow/gate/ritual cards carry at most one echo plus any debut.

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
3. **Concession question** — ask; the question is the next sentence. Perform it in flat Carr voice without naming, announcing, or labeling the question type.
4. **Ventriloquism** — quote the reader's inner voice in quotation marks (their justifications, their future temptations) and answer it. Early: print the full justification menu as quotes, then demolish one per chapter. Late: pre-play the future tempting thought so it arrives pre-refuted.
5. **The inversion** — "It's not X, it's Y": "It causes the aggravation; it doesn't relieve it." "It's you that's [the benefit], not the [behavior]." Often capped with: "It's the other way around."
6. **Peak verdict pair** — land two short mirrored sentences at the argument peak (build-up, then verdict); one major argument only; never name, count, promise, or announce the pair in reader prose.
7. **Reassurance–challenge cycle** — *schedule* the reader's disbelief: name it ("I know this is hard to accept"), welcome it, re-invite the open mind. Doubt is never ignored; it is pre-empted on a cadence.
8. **Upcoming-moment prediction** — predict the reader's specific upcoming thought, situation, and moment of revelation as lived experience; never coach-stage the prediction ("let me future-pace you", "future-pace this with me") or use factory labels as verbs.
9. **Permission paradox** — explicitly permit the behavior while reading ("carry on exactly as normal until you finish"). Disarms resistance and proves this isn't willpower.
10. **Credit reassignment scene** — take a cherished scene, strip the behavior out of it, show the pleasure was the scene all along ("it was only ever sneaking a ride").
11. **Instruction voice** — numbered, imperative, ALL-CAPS headline followed immediately by one short spoken rationale line; no "Warm rationale" header, craft label, or assignment-fulfillment narration around either line. Instructions are thought-substitution rules: "rather than think [old thought], think [mantra]."

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

Because chapter writers see only the master plan + previous chapter + this guide, the master plan is the carrier of all book-specific repetition. It is the **single source of truth**: every shared decision is defined exactly once under a stable ID and referenced by that ID from the compact chapter cards — never copied into competing representations. Do not duplicate occurrence counts, cumulative-state matrices, or audit tables into the plan; the chapter reviewer judges the actual text, so the plan carries the decision, not its bookkeeping. It must include:

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
- **The identity-excuse chapter**: cause-effect inversion ("the traits shared by addicts are the RESULT of the addiction, not the cause") + the graceful concession ("even if you DID have an addictive personality, the method still frees you"). Shame-removal is one person in the room, not population-scale statistics or survey-method narration.
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
# Brief — Quit Sugar (working title)

## Target behavior
Compulsive consumption of refined/added sugar and junk carbs ("bad sugar") — the craving–snacking loop and its grip, not nutrition pedantry.

## Reader / audience
An adult who feels trapped in the sugar loop; has tried diets, moderation rules, and willpower and watched them all fail; suspects something is wrong with the whole approach. General adult edition (one clear reader).

## Goal & stance — decide explicitly (style guide §4 forks)
Forks are decided by the plan-writer in the master plan; expected axes are listed here but not preempted:
- **Outcome (Fork 2):** autonomy-led total freedom vs explicit moderation — where the Bad-Sugar line sits IS the redefinition decision.
- **Void (Fork 5):** natural baseline vs positive replacement — <master plan>
- **Science weight (Fork 3):** <master plan>
- **Villain (Fork 4):** the engineered trap to name (sugar industry / product engineering) — <master plan>
- **Inner state (Fork 1):** full Carr personification — the two mechanism characters, original behavior-fitted names frozen in the mantra sheet (style guide v3 default).

## The load-bearing false belief (style guide §10, step 1)
<one sentence, fixed in the master plan: what the reader believes bad sugar GIVES them — expected neighborhood: "sugar is a pleasure/treat/energy-lift that makes life sweeter and I'd be deprived without it">

## Scope / non-goals
Covers the everyday sugar/junk-carb trap for a general adult reader. Non-goals: medical nutrition therapy, diabetes management advice, eating-disorder treatment (crisis-pointer territory, not method territory), weight-loss-program mechanics.
```

### Lived-experience synthesis
```
# Lived Experience — Quit Sugar

> Raw evidence packets accumulate under `research/banks/` (see
> `prompts/research-agent.md` §4); this file is the lead's curated synthesis of
> them for the master-plan stage. The inline Bank sections below are curated
> content, not the live checkpoint.

Synthesize accepted source packets only. Every bullet must name its bank, persona IDs, and source IDs; an exact quote also links its packet evidence item. Interpretations use no quotation marks.

## Persona map

| Persona ID | Function served / defining context | Applicable beliefs | Applicable banks | Source IDs |
|---|---|---|---|---|
| P-01 | The loss-of-control binger — night/weekend binges, secret or hiding eating, one-bite-becomes-the-box, shame cycle, failed diets & restriction diets | forbidden-is-must-have; one-bite-becomes-the-box; broken-self; "I was born this way" | 1, 2, 3, 4, 5, 9, 10 | BM-1..BM-2x, J-*, E-*, SM-*, LX-*, F-* |
| P-02 | The in-denial moderate — "just a treat", "I'm fine", daily grazing that never reads as a problem | moderation-negotiation; "I don't keep it in the house"; carve-out | 1, 2, 3, 4, 5, 9, 10 | E-1..E-40 (bank-1), E-1..E-11 (bank-2), LX-*, F-* |
| P-03 | The comfort/identity eater — sugar as reward, love, coping, nostalgia; the "I deserve it" moment | food=love; deserve-it reward; stress-cope | 1, 2, 3, 4, 5, 9, 10 | B-001..B-0xx, SM-*, LX-*, F-* |
| P-04 | The energy-crash yo-yoer — sugar as energy lift & concentration fix; 3pm slumps, productivity dips, lift–crash as fuel | lift-is-fuel; need-sugar-to-function; support-crash; rollercoaster | 2, 3, 4, 5, 9, 10 | B-001..B-014, SM-2xx, LX-P04, F-* |

## Intervention-ready evidence units

Create a unit only when accepted packets support every field. `Implicated belief`
must quote one primary or subordinate belief clause from `00-brief.md` verbatim,
or state the belief in the reader's own mined words (persona + slot tagged),
marked `neighborhood, not frozen`.

### LEU-001 — P-04: sugar is the fuel that gets me through the afternoon

- **Situation:** mid-afternoon; the energy dip arrives and the yo-yoer reaches for a sweet top-up, telling themselves it is how they function.
- **Reader wording:** "I would have something quick and sweet but now know that will only give a short term lift which will inevitably be followed by a fast drop."
- **Implicated belief:** "sugar is an energy lift that makes me functional" — `neighborhood, not frozen` (P-04).
- **Persona IDs:** P-04
- **Emotion:** exhaustion dressed as need, then shame at the loop.
- **Permitted inference:** the lift–crash cycle is self-described by recovered writers; the "fuel" misreads a spike-then-drop as genuine energy.
- **Prohibited inference:** that every reader has clinically low blood sugar, or that sugar is ever real "fuel."
- **Style slots:** the-inversion; mantra sensory definition.
- **Safety boundary:** no medical diagnosis claims from these lived-experience quotes.
- **Source locator:** bank-02 B-003
- **Evidence grade:** n/a

### LEU-002 — P-01: one bite becomes the box

- **Situation:** an evening in; a "tiny sliver" or a single biscuit is allowed on a moderation rule, then the box is empty.
- **Reader wording:** "I just crave sweets and when i eat them, i feel like i cant stop."
- **Implicated belief:** "once I start I can't stop" / "it has to be all or nothing" — `neighborhood, not frozen` (P-01).
- **Persona IDs:** P-01
- **Emotion:** powerlessness, then shame and regret.
- **Permitted inference:** the craving, once triggered, carries the binge; the loss-of-control is the trap's signature.
- **Prohibited inference:** that sugar condemns anyone to helplessness permanently.
- **Style slots:** genie-in-the-bottle; the-one-bite.
- **Safety boundary:** no pathological labeling of the reader.
- **Source locator:** bank-02 BM-3
- **Evidence grade:** n/a

### LEU-003 — P-03: the deserved reward

- **Situation:** after stress, a hard day, or a small victory; the moment the reader pays themselves with a sweet because they deserve it.
- **Reader wording:** "celebrating, rewarding myself, going to the cinema, etc with chocolate."
- **Implicated belief:** "sugar is a reward/love I've earned and would be deprived without" — `neighborhood, not frozen` (P-03).
- **Persona IDs:** P-03
- **Emotion:** the belief that it is affection and self-care.
- **Permitted inference:** dessert as self-payment for virtue is a community-named frame; the reward-frame keeps the loop alive.
- **Prohibited inference:** that no one may ever enjoy sweet food.
- **Style slots:** the-treat; deserve-it.
- **Safety boundary:** do not moralize sweetness as universally forbidden.
- **Source locator:** bank-09 LX-158
- **Evidence grade:** n/a

## Brief-belief evidence gaps

Record each unsupported brief belief once across the two syntheses. A gap blocks
planning until research supplies a complete, traceable unit.

### GAP-001

- **Implicated belief:** none blocking. All planned brief-belief clauses are supported by accepted packets across P-01..P-04.

## Bank 1 — Justification Inventory

- [Bank 1] The justification menu is rich across P-01 (J-*) and P-02 (E-1..E-40): moderation-negotiation ("just a treat", "once a week is fine"), the carve-out ("I don't keep it in the house"), and the "it's fuel, not a treat" P-04 frame. — Persona IDs: P-01, P-02 — Source IDs: J-*, E-*

## Bank 2 — Belief Map

- [Bank 2] Keystone marked: sugar as deserved reward / forbidden must-have / energy fuel. P-04 variants now solid: "I need sugar to function", the support-crash fuel ("what I eat to get me through"), the rollercoaster ("I want to get off the roller coaster"), the need-to-eat-now crash ("I-need-to-eat-something-RIGHT-NOW feeling"). — Persona IDs: P-04 (B-001..B-014), P-01 (BM-*), P-03 (B-001..B-0xx), P-02 (E-*)

## Bank 3 — Lived-Experience Bank

- [Bank 3] Daily costs, failed attempts, triggers, shame cycle are deep for P-01 and P-03: the regret ("I feel upset that I'm doing it and regret it the moment I stop"), the child-conditioned food=love origin, the "it almost worked" rescue-belief failure. — Persona IDs: P-01, P-03 — Source IDs: E-*

## Bank 4 — Special-Moments Inventory

- [Bank 4] Seductive scenes per persona, including P-04's 3pm reward moment (SM-2xx) and P-03's celebration/reward scenes (SM-001..SM-006). — Persona IDs: P-01..P-04 — Source IDs: SM-*

## Bank 5 — Escape-Route Inventory

- [Bank 5] Every route the behavior offers is inventoried in-voice (R-1..R-94): moderation, delay, substitution, "just once", dessert-is-the-point-of-the-day. P-03/P-04 routes are the thinner sub-lane. — Persona IDs: P-01, P-02 — Source IDs: R-*

## Bank 6 — Analogy Bank

- [Bank 6] SOURCED and INVENTED candidates (A-01..A-86). Examples: "carbs are inherently lonely… invite company over" (house-party-gatecrasher analogy); "the only way to win is not to play." — Persona IDs: ALL — Source IDs: A-01, A-02

## Bank 9 — Community Lexicon

- [Bank 9] 168-item dialect/sensory lexicon across all four personas (LX-001..LX-161 + remaining): "the roller coaster", "sugary somethings… to get me through", "'treat'… when you feel you deserve one", "I've managed to be good this week". — Persona IDs: P-01..P-04 — Source IDs: LX-*

## Bank 10 — Freedom Testimonies

- [Bank 10] 87 freedom testimonies incl. long-form escape arcs (F-01..F-87): the honesty-of-result ("how well you feel when you are able to avoid sweet cravings"), the restart-button reset, the honest willpower wobble (the first weeks) followed by stability, and the "you don't have to give them up once your body acclimates" future-proofing. — Persona IDs: ALL — Source IDs: F-01, F-02, F-03, F-33, F-34
```

### Scientific-evidence synthesis
```
# Scientific Evidence — Quit Sugar

> Raw evidence packets accumulate under `research/banks/` (see
> `prompts/research-agent.md` §4); this file is the lead's curated synthesis of
> them for the master-plan stage. The inline Bank sections below are curated
> content, not the live checkpoint.

Synthesize accepted source packets only. Every bullet must name its bank, evidence grade, source IDs, and applicable persona IDs (`ALL` when universal). Preserve material disagreement instead of averaging it away.

- [Bank 7] [SUPPORTED] The intermittent-binge sugar model demonstrates bingeing, withdrawal, craving, and cross-sensitization behaviorally with sugar as the reinforcer (animals). — Persona IDs: ALL (P-01 weighted) — Source IDs: S-1 — Limits: rat model, intermittent 12-h access; translates cautiously to humans.
- [Bank 7] [SUPPORTED] Each sugar binge releases dopamine in the nucleus accumbens, re-triggering the reward circuit (animals). — Persona IDs: ALL — Source IDs: S-2, S-8 — Limits: animal microdialysis; magnitude smaller than drugs of abuse.
- [Bank 7] [SUPPORTED] Withdrawal after sugar bingeing involves low accumbens dopamine with a rise in opposing transmitter — a real measured dip after the sugar (animals). — Persona IDs: ALL — Source IDs: S-3 — Limits: opiate-like, naloxone-precipitated; human "sugar withdrawal" not a diagnosis.
- [Bank 7] [SUPPORTED] The overall neurochemical dependency is characterized by the pro-addiction lab itself as "mild but well-defined." — Persona IDs: ALL — Source IDs: S-4 — Limits: rat model; small magnitude; defuses fear without denying a grip.
- [Bank 7] [SUPPORTED] Intermittent access drives escalation and binge volume; ad-lib access does not produce dependency signs — the schedule is the trap's form. — Persona IDs: P-01, P-02 — Source IDs: S-5, S-9 — Limits: animal control-group comparison; echoes the human diet-binge yo-yo.
- [Bank 7] [SUPPORTED] The sugar loop runs on the body's own opioid system (naloxone-precipitated signs) and on cue/reactivity circuits, giving a neural analogue for lingering, cue-driven craving. — Persona IDs: ALL — Source IDs: S-6, S-7 — Limits: rodent; no human physiologic withdrawal proven.
- [Bank 7] [CONTESTED] Leading Cambridge neuroscientists argue the animal bingeing reflects the access pattern, not sugar neurochemistry, and human evidence is thin — "sugar is addictive" is an open scientific question, not consensus. — Persona IDs: ALL — Source IDs: S-11, S-29 — Limits: perspective review; both camps grant binge behaviors occur under intermittent access; dopamine ≠ pleasure (wanting/liking distinction).
- [Bank 7] [SUPPORTED] Populations meet addiction-like criteria for highly palatable food on validated scales (pooled prevalence ~14% adults / 12% children, comparable to alcohol/tobacco); "you are not uniquely weak." — Persona IDs: ALL — Source IDs: S-12, S-14 — Limits: self-report; not a DSM-5 diagnosis.
- [Bank 7] [MIXED] Refined carbohydrates/fats evoke striatal dopamine akin to addictive substances; the fat+sugar combo "seems to have" a supra-additive effect. — Persona IDs: ALL (P-01) — Source IDs: S-13, S-26 — Limits: cross-species comparisons; "seems to" = interpretation, not proof.
- [Bank 7] [SUPPORTED] Longitudinal cohort work links higher sugar intake from sweets with higher later odds of common mental disorder in men — the daily treat predicts future mood, not relief; reverse causation was checked and not found. — Persona IDs: P-03, P-04 — Source IDs: S-15 — Limits: observational; men only for incident CMD.
- [Bank 7] [SUPPORTED] WHO sets a <10%/50g daily free-sugar ceiling and a <5% "additional benefit" target because current consumption far exceeds both. — Persona IDs: ALL — Source IDs: S-16, S-74 — Limits: population-level recommendation; not "sugar is toxic at any dose."
- [Bank 7] [SUPPORTED] Institutional summaries link high added-sugar intake with higher heart/stroke risk via liver overload, raised blood pressure, chronic inflammation, and appetite-control bypass — the lift is deferred load, not free energy. — Persona IDs: ALL — Source IDs: S-17, S-63 — Limits: population-level causal language; teaspoon figures approximate.
- [Bank 7] [SUPPORTED] Side-by-side: WHO dental-caries mechanism (free sugars → plaque acid → decay; the cavity is a real bodily stake) and the clear WHO healthy-diet guidance. — Persona IDs: ALL — Source IDs: S-20, S-58, S-59, S-60, S-61 — Limits: caries is mechanism claim; other factors (fluoride, brushing) mediate.
- [Bank 7] [SUPPORTED/MIXED] Post-meal reactive hypoglycemia gives a mechanism for the "3pm crash": the lift IS insulin working, and the same surge can produce a real after-dip for P-04 — but everyday slumps are NOT clinically low glucose. — Persona IDs: P-04, P-02 — Source IDs: S-21, S-43 — Limits: symptoms often without measured ≤55 mg/dL hypoglycemia; RH in healthy non-diabetics is contested; clinical hypoglycemia is characterized as rare.
- [Bank 7] [SUPPORTED] Glucose is a nutrient the body manufactures from protein and glycerol — sugar is not an essential import, so eliminating it is not deprivation. — Persona IDs: ALL — Source IDs: S-22 — Limits: supports clean-baseline; not a prescription of ketogenic diets.
- [Bank 7] [SUPPORTED] HP-food withdrawal is modeled (animals) and scale-measured in humans, with symptoms peaking at 2–5 days after cutting down then passing — a time-limited hump, not a lifelong fight. — Persona IDs: ALL — Source IDs: S-23, S-25 — Limits: human evidence preliminary + retrospective; the hump is days-long, small-scale.
- [Bank 7] [CONTESTED] Two adolescent sugar-sweetened-beverage abstinence experiments genuinely disagree on whether withdrawal improves or worsens symptoms — honest line: the evidence is split. — Persona IDs: P-01, P-02 — Source IDs: S-24 — Limits: teens, SSB only, 3-day windows.
- [Bank 7] [MIXED] Reward-circuit crowding/blunting (hypodopaminergic tolerance) is a named mechanism for escalation — "why am I not enjoying it like before / I need the family size now"; but the cue-driven hyper-reactivity to wrappers/smells is what fires before the bite. — Persona IDs: P-01, P-03 — Source IDs: S-26, S-27 — Limits: much imaging in obesity/BED; interpretation consistent with, not proven by, imaging.

## Brief-belief evidence gaps

### GAP-002

- **Implicated belief:** none blocking. Every mechanism the book needs is graded and supported/contested with counter-source stated in bank-07 (S-1..S-75) and consequences in bank-08 (V-*).

Sources used in this synthesis are one packet per distinct URL, written to `research/sources/` per the schema in `research/sources/README.md`. The non-PMC additions (S-44..S-75) bring the single-domain share of bank-07 to 49.33% (8 domains), satisfying the ≤50% §6 floor.
```

### Current candidate plan
```
# Master Plan — Quit Sugar

## 1. Book Core

**Target behavior:** Compulsive consumption of BAD SUGAR — refined/added sugar and junk carbs eaten as a craving–snacking loop. Not nutrition pedantry, not all carbohydrates.

**Planned reader (planner-facing state):** An adult who grazes and binges on sweet food and junk carbs most days, has failed at diets, rules and moderation, feels uneasy shame and loss of control but still tells themselves it is a treat, fuel or reward they would be deprived without. Not a proper-name persona, not a code.

**Load-bearing false belief:** BAD SUGAR is a genuine pleasure, treat and energy lift that makes life sweeter and without it I would be deprived.

**Through-line:** Rescue-as-perpetrator — the lift is relief from a low BAD SUGAR itself created; you never rise above the normal of a person who never ate it. Each dose briefly ends the discomfort the previous dose caused, then guarantees it returns.

**Format:** Full-length (15 chapters, ~60,000 words), single general-adult reader, one continuous belief-change arc.

**Destination state:** Whenever the reader thinks about BAD SUGAR they feel relief and freedom that they no longer do it — stopping is felt as escape, not sacrifice. Behaviour then changes on its own without willpower or shame.

**Strongest pro-behaviour scene (to meet head-on):** The deserved reward — cinema / sofa / celebration evening where chocolate and sweets are the love, the treat, the point of the moment. Family film night with the bowl in the middle.

**Fresh ending reframe (saved for final movement only):** You did not give up sweetness — you recovered it. Real food is the sweet food; BAD SUGAR had been blocking the taste.

---

### Fork Decisions (Style Guide §4 — Carr defaults)

**Fork 1 — Inner monster:** DEFAULT CARR. Full personification with original behaviour-fitted names. Two characters frozen as mantas: the trivial physical creature to starve (the Sugar Imp) and the belief-system that feeds it (the Sweet Con).

**Fork 2 — Abstinence vs autonomy:** DEFAULT CARR. Total cessation of BAD SUGAR commanded with cheerful certainty. Moderation foreclosed with pincer and cliff-jump logic. The book issues numbered instructions and expects them followed.

**Fork 3 — Neuroscience / hard fact:** DEFAULT CARR. Deliver hard facts at full Carr force — vivid, flat, frightening where true — then disown fear as the reason to change. Facts arrive as The fact is… never as literature review. Raw citations quarantined to appendix.

**Fork 4 — Villain:** DEFAULT CARR. Two villains hit hard: the engineered trap (sugar industry, bliss-point formulation, variable access design) and the named anti-method (the Willpower Method) to which every past failure is reattributed. Warm to person, vicious to trap.

**Fork 5 — Void:** DEFAULT CARR. Change nothing else in your life. The body's natural baseline returns on its own; inhabit every old context confidently to prove freedom. No elaborate replacement system. Positive direction is tasting real food again, not a new identity scaffold.

### Redefinition and Margin-for-Error

**Redefinition:** Early (Ch1) boxed definition with CAPS name. When this book says sugar, take it to mean BAD SUGAR = added/refined sugar, processed junk carbs and starchy carbs engineered to spike and crash. GOOD CARBS and natural sweetness in whole foods, fruit and vegetables are not BAD SUGAR and stay on the menu. The CAPS name carries the definition in every sentence thereafter. Total-abstinence trap logic runs inside the line: there is no healthy level of BAD SUGAR other than zero.

**Margin-for-error doctrine:** Your body can cope with an occasional accidental blip, but your mind cannot allow it. A slip of BAD SUGAR does not revive addiction unless the Sweet Con is allowed back. Guard the belief, not the bite. Seatbelt image: the buffer is there for accidents, not for driving erratically. An intentional one revives the trap because the belief is intact.

**Conditional-bonus extensions:** Alcohol and dairy are not required to quit to be free of BAD SUGAR. The book frames reducing them as an exciting upgrade available after freedom, with pointer to where help lives, preserving autonomy.

### Clinical / Eating-Disorder Safety Perimeter

**CA-01 — Practical Safety Guardrail** — Boxed advisory held once, plan-wide. Text: This book is about escaping the BAD SUGAR trap for the general adult reader. It is not medical advice, not diabetes management and not eating-disorder treatment. If you have diabetes, take prescribed medication, have a history of disordered eating, or any medical condition affected by what you eat, talk to your clinician before changing what you eat. If you need help with eating distress, contact a qualified professional or crisis support in your country. Do not use this book to impose restriction or punishment around food.

All clinical limits that could conflict with method advice live in CA-01 and in evidence-ledger safety limits, never fused into instruction wording. Chapter cards cite CA-01 in safety guardrails only — never paste the boxed title mid-chapter. Prose honours CA-01 silently or with one short spoken clause.

---

## 2. Compact Evidence Ledger

Each row carries only what the book may use. Writer resolves cards against IDs below.

**E-01 — Intermittent-access binge model**
Finding: Intermittent 12-h sugar access produces bingeing, withdrawal signs, craving and cross-sensitization behaviourally with sugar as reinforcer. Lived analogue: one-bite-becomes-the-box.
IDs: SEU-001 | Source: S-1 | Grade: SUPPORTED | Scope: rats, intermittent-access model | Permitted inference: schedule drives binge pattern; moderation-negotiation mirrors intermittent access | Prohibited inference: proves human sugar is addictive in the clinical sense | Empirical limit: animal model translates cautiously | Safety limit: do not label reader as addict by diagnosis; CA-01

**E-02 — Dopamine hit per binge**
Finding: Each sugar binge releases dopamine in nucleus accumbens, re-triggering reward circuit.
IDs: SEU-002 | Sources: S-2; S-8 | Grade: SUPPORTED | Scope: animal microdialysis | Permitted inference: each hit re-triggers the loop it claims to relieve | Prohibited inference: binge equals drug-magnitude high | Empirical limit: magnitude smaller than drugs of abuse | Safety limit: describe as wanting circuit, not proof of compulsion; CA-01

**E-03 — Measured dip after sugar (withdrawal analogue)**
Finding: After sugar bingeing, low accumbens dopamine with rise in opposing transmitter — a real dip after the sugar.
IDs: SEU-003 | Source: S-3 | Grade: SUPPORTED | Scope: naloxone-precipitated, opiate-like in rats | Permitted inference: the low follows the dose; the rescue creates the need | Prohibited inference: human sugar withdrawal is a diagnosis | Empirical limit: rodent; human physiologic withdrawal not proven | Safety limit: call it a mild dip, not a detox sentence

**E-04 — Mild but well-defined**
Finding: Lab characterizes overall neurochemical dependency as mild but well-defined.
IDs: SEU-004 | Source: S-4 | Grade: SUPPORTED | Scope: same rat model | Permitted inference: the physical part is small and self-resolving; fear of withdrawal is outsized | Prohibited inference: there is no grip at all | Empirical limit: small magnitude | Safety limit: use to defuse fear, not to minimize lived difficulty

**E-05 — Schedule is the trap form**
Finding: Intermittent access drives escalation and binge volume; ad-lib access does not produce dependency signs.
IDs: SEU-005 | Sources: S-5; S-9 | Grade: SUPPORTED | Scope: animal control-group comparison | Permitted inference: yo-yo restriction creates binge; diet-binge cycle mirrors lab schedule | Prohibited inference: sugar itself is inert | Empirical limit: animal; echoes human dieting pattern only | Safety limit: do not prescribe meal timing; CA-01

**E-06 — Opioid and cue circuits**
Finding: Sugar loop runs on the body's own opioid system and on cue/reactivity circuits — neural analogue for lingering, cue-driven craving to wrappers and smells.
IDs: SEU-006 | Sources: S-6; S-7 | Grade: SUPPORTED | Scope: rodent | Permitted inference: a sight or smell can fire want before hunger | Prohibited inference: proven human pharmacologic dependence | Empirical limit: rodent; no human physiologic withdrawal proven | Safety limit: frame as cue habit, not disease

**E-07 — Contested addictive status**
Finding: Leading Cambridge review argues bingeing reflects access pattern, not sugar neurochemistry; human evidence thin — sugar is addictive is open question, not consensus; dopamine = wanting not liking.
IDs: SEU-007 | Sources: S-11; S-29 | Grade: CONTESTED | Scope: perspective review | Permitted inference: present disagreement honestly; both camps grant binge behaviours under intermittent access | Prohibited inference: claim consensus either way | Empirical limit: interpretation, not data | Safety limit: do not use to keep reader trapped in debate

**E-08 — Population scale is not personal weakness**
Finding: Populations meet addiction-like criteria for highly palatable food on validated scales (pooled ~14% adults / 12% children, comparable to alcohol/tobacco).
IDs: SEU-008 | Sources: S-12; S-14 | Grade: SUPPORTED | Scope: self-report, not DSM-5 diagnosis | Permitted inference: you are not uniquely weak; many feel trapped | Prohibited inference: reader meets clinical diagnosis | Empirical limit: scale-measured, not diagnosed | Safety limit: use once for dignity; do not pathologize; CA-01

**E-09 — The treat predicts future mood**
Finding: Higher sugar intake from sweets associated with higher later odds of common mental disorder in men; reverse causation checked and not found.
IDs: SEU-009 | Source: S-15 | Grade: SUPPORTED | Scope: longitudinal cohort, men only for incident CMD | Permitted inference: the daily treat predicts low mood rather than relieves it; rescuer-as-perpetrator for mood | Prohibited inference: sugar causes depression in all readers | Empirical limit: observational, men only | Safety limit: do not diagnose mood; CA-01

**E-10 — WHO ceiling**
Finding: WHO sets <10% / 50g daily free-sugar ceiling and <5% additional benefit target; current intake far exceeds both.
IDs: SEU-010 | Sources: S-16; S-74 | Grade: SUPPORTED | Scope: population recommendation | Permitted inference: normal intake is far above guidance; normal is not natural | Prohibited inference: any dose is toxic | Empirical limit: population guideline | Safety limit: not a prescribed intake for reader; CA-01

**E-11 — The lift is deferred load**
Finding: High added-sugar intake linked with higher heart/stroke risk via liver overload, raised pressure, chronic inflammation and appetite-control bypass.
IDs: SEU-011 | Sources: S-17; S-63 | Grade: SUPPORTED | Scope: institutional summary, population level | Permitted inference: the energy lift carries a real bodily load | Prohibited inference: predict individual cardiac event | Empirical limit: teaspoon figures approximate; causal language is population level | Safety limit: deliver flat then disown fear; no personal prognosis

**E-12 — Cavity mechanism**
Finding: Free sugars → plaque acid → decay; the cavity is a real bodily stake alongside clear healthy-diet guidance.
IDs: SEU-012 | Sources: S-20; S-58; S-59; S-60; S-61 | Grade: SUPPORTED | Scope: mechanism claim | Permitted inference: sugar does concrete bodily harm while claiming to be harmless | Prohibited inference: sugar alone causes decay without other factors | Empirical limit: fluoride and brushing mediate | Safety limit: no dental advice beyond mechanism

**E-13 — 3pm crash mechanism and limit**
Finding: Post-meal reactive physiology can produce a dip after a sugar surge; everyday slumps often occur without measured low glucose; clinical hypoglycemia is rare.
IDs: SEU-013 | Sources: S-21; S-43 | Grade: SUPPORTED/MIXED | Scope: physiology in healthy non-diabetics contested | Permitted inference: the lift IS insulin working and can produce the crash P-04 blames on need for more sugar; Its the other way around | Prohibited inference: every reader has clinical low blood sugar requiring sugar | Empirical limit: symptoms often without ≤55 mg/dL; RH in non-diabetics contested | Safety limit: never diagnose; CA-01

**E-14 — No essential import**
Finding: Glucose is manufactured by the body from protein and glycerol — sugar is not an essential import.
IDs: SEU-014 | Source: S-22 | Grade: SUPPORTED | Scope: metabolism | Permitted inference: eliminating BAD SUGAR is not deprivation; body has alternate source | Prohibited inference: prescribe ketogenic diet | Empirical limit: supports clean baseline, not a diet plan | Safety limit: CA-01

**E-15 — Time-limited hump**
Finding: Highly palatable food withdrawal in animals and scale-measured in humans peaks at 2–5 days after cutting down then passes — days-long hump, not lifelong fight.
IDs: SEU-015 | Sources: S-23; S-25 | Grade: SUPPORTED | Scope: animal model + preliminary retrospective human | Permitted inference: any physical discomfort is brief and starves if not refed | Prohibited inference: everyone will feel strong withdrawal | Empirical limit: human evidence preliminary | Safety limit: do not promise zero sensation; frame as mild and brief

**E-16 — Split evidence on short abstinence**
Finding: Two adolescent SSB abstinence experiments disagree on whether withdrawal improves or worsens symptoms.
IDs: SEU-016 | Source: S-24 | Grade: CONTESTED | Scope: teens, SSB only, 3-day windows | Permitted inference: evidence is genuinely split on short windows | Prohibited inference: claim proven withdrawal syndrome | Empirical limit: narrow population and window | Safety limit: use to avoid overclaim

**E-17 — Crowding / blunting and hyper-reactivity**
Finding: Reward-circuit crowding/blunting (hypodopaminergic tolerance) named for escalation — needing family size — and cue-driven hyper-reactivity to wrappers/smells that fires before the bite.
IDs: SEU-017 | Sources: S-26; S-27 | Grade: MIXED | Scope: much imaging in obesity/BED | Permitted inference: why enjoyment fades and wanting spikes at cues | Prohibited inference: proves irreversible brain damage | Empirical limit: consistent with imaging, not proven by it | Safety limit: do not catastrophize brain

**L-01 — The fuel that isn't**
Finding: Mid-afternoon belief that sweet top-up is how I function; recovered writers describe lift-then-fast-drop.
Reader line: I would have something quick and sweet but now know that will only give a short term lift which will inevitably be followed by a fast drop
IDs: LEU-001 | Source: bank-02 B-003 | Grade: STRONG LIVED PATTERN | Scope: P-04 energy yo-yoer, office afternoons | Permitted inference: lift–crash cycle is self-described; fuel misreads spike as energy | Prohibited inference: every reader has clinically low sugar | Empirical limit: lived testimony, not physiology | Safety limit: no medical diagnosis; CA-01

**L-02 — One bite becomes the box**
Finding: Permission for a tiny sliver or single biscuit on a moderation rule ends with the box empty; triggered craving carries the binge.
Reader line: I just crave sweets and when i eat them, i feel like i cant stop
IDs: LEU-002 | Source: bank-02 BM-3 | Grade: STRONG LIVED PATTERN | Scope: loss-of-control evenings | Permitted inference: one exception reignites the trap; the one-bite carries the binge | Prohibited inference: anyone is permanently helpless | Empirical limit: testimony | Safety limit: no pathologizing label

**L-03 — The deserved reward**
Finding: Stress, hard day or small victory paid with sweets because I deserve it; dessert as self-payment for virtue.
Reader line: celebrating, rewarding myself, going to the cinema, etc with chocolate
IDs: LEU-003 | Source: bank-09 LX-158 | Grade: STRONG LIVED PATTERN | Scope: reward/identity moments, celebrations | Permitted inference: reward-frame keeps loop alive; treat is paying yourself with the cause | Prohibited inference: no one may ever enjoy sweet food at all | Empirical limit: testimony | Safety limit: do not moralize sweetness as universally forbidden

---

## 3. Mantra and Frozen-Token Sheet

Mantras are repeated verbatim when the frozen line is the natural next sentence. Debut pins exact wording once in plain text; echo cites ID only. No backticks.

**M-A — Entry promise**
Wording: you have nothing to lose and everything to gain
Belief job: risk-reversal to buy compliance with instructions when claim sounds impossible
Debut: C-01 | Echo: C-06, C-13 | Hand-over: spoken as the reader's own check — whenever doubt says why try, replace with this line

**M-B — Promise triad**
Wording: easily, immediately and permanently
Belief job: impossible-sounding contract stated with total confidence; freedom is now, not earned
Debut: C-01 | Echo: C-13 | Hand-over: reader's shorthand for the contract — I stopped easily, immediately and permanently

**M-C — Trap metaphor**
Wording: the Sugar Trap
Belief job: central metaphor turning stopping into escape, not sacrifice
Debut: C-02 | Echo: C-07, C-14 | Hand-over: name for quick re-label — that's the Sugar Trap talking

**M-D — Little creature**
Wording: the Sugar Imp
Belief job: externalizes the trivial physical gnawing as a small starving parasite already dying
Debut: C-02 | Echo: C-07, C-13 | Hand-over: feeling labelled as the Sugar Imp's death throes to rejoice in

**M-E — Big creature**
Wording: the Sweet Con
Belief job: names the belief-system that feeds the Imp — the brainwashing about pleasure, treat, fuel and reward
Debut: C-03 | Echo: C-07 | Hand-over: thought labelled as the Sweet Con's script, not my reasoning

**M-F — Illusion phrase**
Wording: a genuine pleasure or treat
Belief job: fixed dyad so perceived benefit can be referenced and demolished as single object; thereafter benefit is only called by this token
Debut: C-03 | Echo: C-05, C-09 | Hand-over: reader's test — is this a genuine pleasure or treat, or the Imp being fed

**M-G — Terminal mantra**
Wording: FANTASTIC! I'M FREE!
Belief job: replacement thought the reader keeps forever whenever BAD SUGAR crosses their mind
Debut: C-13 | Echo: C-14, C-15 | Hand-over: explicit instruction — whenever you think of BAD SUGAR, think FANTASTIC! I'M FREE!

**M-H — Stakes phrase**
Wording: for the rest of your life
Belief job: dual-valence time horizon — threat as trapped, reward as free — same words, opposite emotion
Debut: C-08 | Echo: C-14 | Hand-over: reader's horizon check — hooked for the rest of your life vs free for the rest of your life

**Frozen tokens (chapter-anchored settled claims invoked verbatim):**
- T-01 tug-of-war of fear — the addict's torn state whose both ropes belong to trap
- T-02 the Willpower Method — named anti-method to which every past failure is reattributed
- T-03 body, instinct and real food — positive authority triad with operational tools

---

## 4. Scene and Analogy Bank

Each scene debuts its full staging on exactly one card; later cites are token-echo only.

**SC-01 — Tight shoes**
Description: Wearing tight shoes all day for the relief of taking them off; the relief is not pleasure, only ending self-inflicted pain.
Job: Flagship illusion-exposer for rescuer-as-perpetrator. Constraint: must be rendered with sugar-specific sensory detail, not abstract.

**SC-02 — House-party gatecrasher**
Description: Carbs are inherently lonely and invite company; BAD SUGAR gatecrashes any meal and then claims it made the party.
Job: Credit reassignment for meals and sociability. Constraint: keep comedic, not shaming.

**SC-03 — Boiling frog**
Description: Frog in slowly heating water never notices harm because rise is gradual; feels fine while being cooked.
Job: Explain why reader feels fine while trapped; gradual escalation. Constraint: deliver hard fact at full force, then immediate relief per Fork 3; do not leave in dread.

**SC-04 — Confidence trick / fraudulent investment**
Description: Polite con artist sells phoney information, takes money, trap removes choice; victim was conned, not foolish.
Job: Dissolve free choice without blame. Constraint: warm to reader, vicious to con.

**SC-05 — Insect and spider web**
Description: Fly feels free between strands, each sweet hit is another almost-invisible strand; by the time web is felt, flight is gone.
Job: Visualize trap building invisibly. Constraint: original prose, not literal caffeine image.

**SC-06 — Caged lion with open door**
Description: Lion freed but hovers by open cage out of habit; anxiety after escape is cage-habit, not proof of need.
Job: Post-change anxiety as habit, not need. Constraint: use only after vow.

**SC-07 — Film-night bowl (strongest case)**
Description: Saturday sofa, film, family, big bowl of sweets in the middle — the most seductive sugar scene the reader calls love and treat.
Job: Hands-on credit reassignment; pleasure stripped to company, warmth, story. Constraint: staging belongs to C-09 only; later cites token only.

**SC-08 — 3pm office rollercoaster**
Description: Office at 3pm: vending machine hum, sticky mouth, heavy eyelids; the sugar lift and crash as a rollercoaster you pay to ride and then pay to get off.
Job: Demolish energy-fuel justification with lived sensory string. Constraint: honour empirical limit of E-13/RH contested status.

**SC-09 — Supermarket aisle as pharmacy**
Description: Supermarket aisle re-seen as a bright pharmacy where every packet is a dose in tasty packaging; you pity the queue.
Job: Pity-not-envy reframe for ordinary life. Constraint: not moralizing shoppers.

**SC-10 — Limbic switchboard with many cords**
Description: Primitive brain as appliance with many power cords; unplugging most still leaves it running; all cords must be pulled.
Job: Explain why one remaining belief keeps trap alive; totality logic. Constraint: distinct from creature staging.

---

## 5. Lexicon and Instruction Spine

**Trap register (always for BAD SUGAR):** BAD SUGAR, dose, fix, hit, feed, trap, con, brainwashing, Sugar Trap, Sugar Imp, Sweet Con. Behaviour is feeding the Imp; community-normal is brainwashing; users are trapped/conned with warmth.

**Freedom register (always for stopping):** escape, free, freedom, marvellous, wonderful, exciting, rejoice, celebrate, relief, get on with enjoying your life.

**Banned willpower register (never as solution):** give up, resist, stay strong, discipline, abstain, sacrifice (except to name illusion), trying to stop, one day at a time, recovery journey, quit cold turkey as framing. Quit as plain verb is allowed; giving something up is not.

**Community dialect (ventriloquized reader voice, source-grounded):** the roller coaster, to get me through, quick and sweet, short term lift then fast drop, I just can't stop, once I start I can't stop, one bite, the box, treat when you deserve one, I've been good this week, I don't keep it in the house, just a treat, once a week is fine.

### Instruction Spine (frozen spoken imperatives)

Each instruction is one ALL-CAPS headline plus at most one short spoken rationale line. Owned by one chapter, recapped photographably in C-15 without chapter-number callbacks. No clinical tails, no ID cross-references, no semicolon chains.

**I-01 — C-01**
KEEP AN OPEN MIND
You cannot judge until you have finished.

**I-02 — C-01**
CARRY ON EATING AS NORMAL UNTIL YOU FINISH THIS BOOK
Do not try to cut down yet; the belief must change first.

**I-03 — C-01**
BEGIN WITH A FEELING OF ELATION
You are about to escape, not suffer.

**I-04 — C-02**
FOLLOW ALL THE INSTRUCTIONS
All you have to do is follow all the instructions.

**I-05 — C-04**
NEVER THINK I CAN'T HAVE BAD SUGAR — THINK GREAT, I'M FREE
There is nothing to give up.

**I-06 — C-07**
IGNORE ANY ADVICE THAT CONFLICTS WITH THIS METHOD
If it contradicts escape, it keeps you trapped.

**I-07 — C-10**
IGNORE ANYONE WHO STOPPED BY THE WILLPOWER METHOD
Their struggle is not your guide.

**I-08 — C-10**
AVOID THE INFLUENCE OF OTHER USERS WHILE YOU READ
Brainwashing is contagious.

**I-09 — C-13**
TAKE YOUR LAST ORDINARY DOSE AND MAKE THE SOLEMN VOW
Do not wait to be free — you already are.

**I-10 — C-13**
NEVER REOPEN THE DECISION
The tug-of-war ends the moment you stop pulling.

**I-11 — C-14**
REJOICE AT A DEAD ENEMY, NEVER MOURN A LOST FRIEND
Whenever you think of BAD SUGAR, think FANTASTIC! I'M FREE!

**I-12 — C-14**
IF YOU SLIP, FORGIVE IT AND GUARD THE BELIEF
A blip revives nothing unless you let the Sweet Con back.

Final photographable list in C-15 repeats I-01 through I-12 verbatim as the twelve lines above, without chapter callbacks, followed by outward imperative: Now get on with enjoying your life.

---

## 6. Arc and Length

**Chapter count:** 15

**Architecture:** First third installs world (contract, already hooked, creatures named in passing, body/instinct/real food as concrete encounters). Middle demolishes on that ground; one chapter inhabits ordinary eating. After vow: last ordinary dose, one ordinary-life chapter, short recap.

| Ch | Working Title | Words |
|---|---|---|
| 1 | The Invitation | 3200 |
| 2 | Already Hooked | 3800 |
| 3 | What Does It Do For You? | 3400 |
| 4 | The Energy Lie | 4200 |
| 5 | The Treat That Isn't | 4200 |
| 6 | Hunger You Can Trust | 4600 |
| 7 | How the Trap Works | 4400 |
| 8 | Who Built This Trap | 4200 |
| 9 | The Sweetest Evening | 4600 |
| 10 | Fear and the Willpower Method | 4200 |
| 11 | Myths on a Plate — Q&A | 3800 |
| 12 | Before the Last Bite | 4400 |
| 13 | The Last Ordinary Dose | 3800 |
| 14 | Mornings, Shops, Tables | 4200 |
| 15 | Free For Good | 3000 |
| **Total** | | **60000** |

Arithmetic sum: 3200+3800+3400+4200+4200+4600+4400+4200+4600+4200+3800+4400+3800+4200+3000 = 60000. Within 54,000–66,000.

**Curve map:**
- Freedom crescendo suppressed mid-book, detonated last 20% (C-13 to C-15 carry more freedom register than rest combined).
- Demolition vocabulary (brainwashing, illusion, trap) peaks C-03 to C-09, hands off to freedom after C-10.
- Ease front-loaded C-01, then assumed.
- Prevalence claim appears once in C-02.
- Long testimony lives in main flow in C-12, not appendix.
- Myths Q&A distinct room in C-11.
- Meta-inoculation in C-10.
- Inhabit-the-ordinary-doing primary job in C-06 only.
- Saved-for-ending reframe (you recovered sweetness) appears only in C-15.

Concept debuts: creatures in C-02; positive authority body/instinct/real food in C-02 as encounters; inversion in C-07; strongest scene in C-09; anti-method in C-10; fear dismantled in C-10; vow in C-13.

---

## 7. Compact Chapter Cards

**C-01 — The Invitation**
Non-argument — definition & trust
New instructions: I-01, I-02, I-03 at climax
Reader-state: sceptical adult who has tried everything and expects another diet lecture; needs risk-reversal to keep reading
Concrete encounter: the exact promise reading this book will not demand willpower, with origin story in passing
Mantra: debut M-A you have nothing to lose and everything to gain, debut M-B easily, immediately and permanently — pinned in plain text with IDs
Scene: SC-04 confidence trick as brief trust image (debut)
Structural responsibility: front-matter authority dossier and contract; five reading instructions land here
Guardrails: warm to person, no hedging of promise; do not moralize; honour CA-01 silently
Continuity: delivers open mind and permission to continue as normal; hands forward a reader willing to investigate
Word budget: 3200
Reserved-later fence: creatures and body/real food not taught here; reserved to C-02; benefits not demolished here; reserved to C-04/C-05; mechanism not argued here

**C-02 — Already Hooked**
Enacted transition — the reader stops believing they freely choose BAD SUGAR and sees they were conned into a trap they already live in
Belief now: entry believes I choose this and could stop if I wanted; exit knows the trap removed choice and feels normal only because trapped
Concrete encounter: inventory of yesterday's grazing and hiding the packet, watching normal as not normal
Evidence: E-05 schedule drives binge (do not overclaim human diagnosis), E-08 prevalence once (you are not uniquely weak), L-02 one-bite box | Limits: do not diagnose addiction; do not use prevalence as efficacy claim; E-05 animal only
New instruction: I-04 FOLLOW ALL THE INSTRUCTIONS
Reserved-later fence: evaluation-axis switch reserved to C-03; fuel and reward kills reserved to C-04/C-05; inversion reserved to C-07
Arc: first third, trap language rising
Reader-state: person who says I don't overdo it but recognizes the grazing description; encounter makes hidden pattern visible
Mantra: debut M-C the Sugar Trap, debut M-D the Sugar Imp — pinned with IDs
Scene: SC-05 spider web (debut), SC-03 boiling frog (debut, brief)
Structural: named creatures in passing when trap first seen; body/instinct/real food as concrete encounter (watch eating, body as authority — not refrain)
Guardrails: CA-01; original prose; dissolve choice without blame; split physical trivial from belief target already
Continuity: receives willing investigator; hands forward trap vocabulary and Imp name for reuse
Word budget: 3800

**C-03 — What Does It Do For You?**
Enacted transition — the reader switches the question from does it do more harm than good to what good is there at all and sees it does plenty TO them and nothing FOR them
Belief now: entry still weighs harm vs benefit; exit demands a single genuine benefit and finds none
Concrete encounter: printed justification menu in reader's own dialect quoted back
Evidence: E-10 WHO ceiling (do not prescribe), E-12 cavity mechanism, L-03 reward frame | Limits: do not claim any dose toxic; cavity mechanism mediated by fluoride/brushing
New instruction: none (instruction gap preserves rhythm)
Reserved-later fence: energy-fuel demolition reserved to C-04; reward demolition to C-05; inhabit eating to C-06; hard facts widening to C-08
Arc: first third to middle hinge
Reader-state: negotiator ready to bargain benefits; encounter forces justification to justify itself
Mantra: debut M-E the Sweet Con, debut M-F a genuine pleasure or treat — pinned with IDs
Scene: SC-02 gatecrasher (debut)
Structural: evaluation-axis switch chapter; installs illusion phrase as sole token for benefit thereafter
Guardrails: never concede one real benefit; no ledger/worksheet; CA-01
Continuity: receives trap names; hands forward switched axis and illusion token
Word budget: 3400

**C-04 — The Energy Lie**
Enacted transition — the reader stops believing BAD SUGAR is fuel and sees the 3pm lift is a loan with interest that creates the crash
Belief now: entry believes I need sugar to function and to get through; exit knows the quick sweet drives the fast drop
Concrete encounter: 3pm desk, vending machine, the sticky mouth and heavy eyelids after the hit
Evidence: E-13 crash mechanism (honour contested / no clinical hypo), E-11 lift is deferred load, L-01 lift-then-drop line | Limits: do not diagnose low blood sugar; everyday slump is not clinical hypoglycemia; E-11 population level only
New instruction: I-05 NEVER THINK I CAN'T HAVE BAD SUGAR — THINK GREAT, I'M FREE (first thought-substitution rule)
Reserved-later fence: treat/reward kill reserved to C-05; inhabit hunger reserved to C-06; cue hyper-reactivity reserved to C-07
Arc: demolition rising
Reader-state: afternoon yo-yoer who lives the roller coaster; encounter re-labels their own body in Imp words
Mantra: echo M-F (one echo only)
Scene: SC-08 rollercoaster (debut staging) — carries sensory string
Guardrails: vivid hard fact then relief in same breath; original prose; CA-01; do not overclaim physiology
Continuity: receives switched axis; hands forward fuel-killed belief
Word budget: 4200

**C-05 — The Treat That Isn't**
Enacted transition — the reader stops believing BAD SUGAR is a reward or love they deserve and sees it as paying themselves with the cause of the feeling they want to reward
Belief now: entry believes chocolate is love and I deserve it after a hard day; exit knows treat was self-payment in the trap's currency
Concrete encounter: cinema queue, birthday cake, going to the shop for sweets after being good this week
Evidence: L-03 deserved reward, E-09 sweets predict later low mood in men (men only, observational), E-17 crowding/blunting why enjoyment fades | Limits: E-09 men only, do not generalize to all or claim causation; E-17 MIXED imaging limit
New instruction: none
Reserved-later fence: inhabit real food reserved to C-06; mood reframe not extended beyond permitted; industry widening reserved to C-08
Arc: demolition peak
Reader-state: comfort eater whose identity is wrapped in treating; encounter exposes reward as trap script
Mantra: echo M-F
Scene: SC-10 limbic switchboard (debut) for totality — why one treat keeps cord plugged
Guardrails: dismantle food-equals-love brainwashing; name who installed it; warm to reader
Continuity: receives fuel-killed; hands forward treat-killed
Word budget: 4200

**C-06 — Hunger You Can Trust**
Enacted transition — the reader inhabits natural hunger, satisfaction and real food as favourite in itself, not as a kill with inhabit flavour
Belief now: entry believes hunger is an emergency needing a quick fix and vegetables are deprivation; exit feels hunger as a mild friendly signal and real food as satisfying favourite
Concrete encounter: watching eating — a simple meal eaten when hungry, noticing clean appetite, taste returning, the pause where satisfaction arrives
Evidence: E-14 glucose manufactured (not deprivation), E-15 time-limited hump 2–5 days (brief), L-01 contrast | Limits: E-14 not a keto prescription; E-15 preliminary retrospective
New instruction: none
Reserved-later fence: mechanism inversion reserved to C-07; industry and health facts reserved to C-08; strongest scene reserved to C-09
Arc: middle — inhabit pivot; demolition vocabulary briefly recedes
Reader-state: person who has forgotten what true hunger and satisfaction feel like under grazing; encounter re-introduces instinct
Mantra: echo M-A
Scene: no new trap analogy; this chapter's scene is the ordinary meal itself (inhabit)
Structural responsibility: the one chapter whose primary job is inhabit-the-ordinary-doing
Guardrails: no three-word refrain; body/instinct/real food as concrete encounters, not slogan; CA-01
Continuity: receives fuel and treat killed; hands forward positive authority lived experience for later demolitions
Word budget: 4600

**C-07 — How the Trap Works**
Enacted transition — the reader grasps the inversion: the high is relief from a low BAD SUGAR created and the Sweet Con feeds the Sugar Imp
Belief now: entry sees cravings as personal weakness; exit sees trivial Imp starving and dominant Sweet Con as real target
Concrete encounter: tracing a single loop — dose, brief relief, dip, cue fires, want returns — never above baseline
Evidence: E-01 binge model, E-02 dopamine re-trigger, E-03 dip after sugar, E-04 mild but well-defined, E-06 opioid/cue circuits, E-17 hyper-reactivity to wrappers | Limits: honour animal limits and CONTESTED status E-07 not used to claim consensus; do not overclaim magnitude vs drugs
New instruction: I-06 IGNORE ANY ADVICE THAT CONFLICTS WITH THIS METHOD (first epistemic firewall)
Reserved-later fence: hard health facts and industry widening reserved to C-08; strongest scene reserved to C-09; escalation and morning-afternoon specifics not re-argued later
Arc: mechanism deepening, not debut unit
Reader-state: person who fears withdrawal as big monster; encounter shrinks physical to trivial and enlarges belief to target
Mantra: echo M-C, echo M-D (within two limit, plus M-E cited as token reference without counting as mantra echo) — strictly two mantra IDs on card: M-C and M-D used; M-E handled as creature token already settled
Scene: SC-01 tight shoes (debut full staging); SC-10 token echo only if needed
Structural: mechanism chapter as deepening using vocabulary already named
Guardrails: deliver with total authority; reassurance–challenge cycle for disbelief; CA-01; do not narrate study design
Continuity: receives positive authority and kills; hands forward mechanism understanding
Word budget: 4400

**C-08 — Who Built This Trap**
Enacted transition — the reader stops blaming themselves and sees the engineered manufacture of desire that profits from their hunger
Belief now: entry believes craving is my character; exit knows armies of food engineers weaponized abundance and variable access
Concrete encounter: walking the supermarket aisle reading packets; children's cereals, bliss-point ads from childhood
Evidence: E-05 schedule, E-11 deferred load, E-12 cavity, E-08 prevalence as dignity once only if not used in C-02 | Limits: do not predict individual disease; use E-11 at population level; deliver hard facts then immediate relief
New instruction: none
Reserved-later fence: strongest seductive scene reserved to C-09; fear and willpower method reserved to C-10
Arc: widening indictment; demolition peak handing to freedom
Reader-state: person ready to relocate anger from self to industry; encounter gives external villain with warmth intact
Mantra: debut M-H for the rest of your life — pinned with ID
Scene: SC-03 token echo, SC-05 token echo; no new full staging
Guardrails: awe for body's sophistication as persuasion; two-villain structure; CA-01
Continuity: receives mechanism; hands forward external blame shift
Word budget: 4200

**C-09 — The Sweetest Evening**
Enacted transition — the reader meets the strongest case head-on and reassigns every drop of its pleasure to the evening itself — BAD SUGAR was only sneaking a ride
Belief now: entry believes film night without sweets would be bleak; exit feels the warmth was the people and story, sweets were the tax
Concrete encounter: film-night bowl in the middle, hands reaching, the after taste and sticky regret vs same evening with real food enjoyed
Evidence: L-03 reward, E-17 why enjoyment fades, E-02 re-trigger | Limits: do not claim no one enjoys sweet flavour at all; prohibited inference from L-03
New instruction: none
Reserved-later fence: fear dismantling and anti-method reserved to C-10; myths reserved to C-11
Arc: late demolition, perception proof late
Reader-state: person who guards one special occasion as proof they cannot be free; encounter takes best case and leaves no foothold
Mantra: echo M-F
Scene: SC-07 film-night bowl (full staging debut) + optical-illusion-style hands-on perception demo that felt certainty can be flatly wrong
Guardrails: credit reassignment scene must show situation, body, moment as true sources; do not moralize pleasure
Continuity: receives wide indictment; hands forward strongest case demolished
Word budget: 4600

**C-10 — Fear and the Willpower Method**
Enacted transition — the reader stops fearing failure and success and sees the Willpower Method itself as the second trap with no finish line
Belief now: entry fears I will fail or I am someone who needs this; exit knows fear-of-failure and fear-of-success are both ropes held by the trap
Concrete encounter: prison-door scene and released-convict analogy lived through; braggers and whingers in willpower culture observed
Evidence: E-04 mild but well-defined to defuse dread, E-15 brief hump | Limits: do not promise zero sensation; honour preliminary nature of E-15
New instructions: I-07 IGNORE ANYONE WHO STOPPED BY THE WILLPOWER METHOD, I-08 AVOID THE INFLUENCE OF OTHER USERS WHILE YOU READ — both at climax (two instructions allowed across chapter flow but each is a separate climax beat; card lists both as new)
Reserved-later fence: myths battery reserved to C-11; testimony reserved to C-12
Arc: fear chapter + anti-method chapter merged; last demolition before pivot
Reader-state: willful person who has tried strong will and failed; needs reframe that strong will to persist proves strength, not weakness
Mantra: echo M-H (if not over limit) — actually this card carries two new instructions so mantra echo limited to at most one plus any debut — this card debuts no mantra, so at most one echo: M-H
Scene: SC-06 caged lion (brief debut) for fear-of-success
Structural responsibility: anti-method chapter, fear-of-failure / fear-of-success collapse, meta-inoculation (ventriloquize strongest objection to method and answer it without labeling it)
Guardrails: reframe strong will as evidence for them; sub-characters braggers/whingers; blame method not reader; CA-01
Continuity: receives strongest case killed; hands forward freedom from fear and method
Word budget: 4200

**C-11 — Myths on a Plate — Q&A**
Enacted transition — the reader's remaining escape thoughts are pre-played and pre-discredited as Sweet Con scripts, leaving no route back
Belief now: entry still holds back-pocket myths (cut down, keep special ones, quit tomorrow, wean off, natural sugar is fine, I need it for my brain); exit hears each as the trap's line with instant answer
Concrete encounter: rapid-fire quoted myths in reader dialect answered in 2–6 sentences each
Evidence: E-05 cut-down makes precious (intermittent escalation), E-15 weaning worsens, E-13 not a hypo emergency, E-14 no essential need, E-07 contested status for honesty | Limits: honour E-16 split where relevant; do not overclaim brain need
New instruction: none
Reserved-later fence: testimony and readiness gate reserved to C-12; ritual reserved to C-13
Arc: close escape routes; distinct room
Reader-state: negotiator reaching for loopholes; encounter closes each before it is reached for
Mantra: no mantra (absence not defect) — keeps echo density spread
Scene: SC-10 token echo only for totality; SC-08 token echo only
Structural responsibility: myths Q&A battery as distinct room; pre-script future rationalizations
Guardrails: each myth as quoted reader voice, demolished flat; do not create new teaching manual; CA-01
Continuity: receives fear dismantled; hands forward closed escape routes
Word budget: 3800

**C-12 — Before the Last Bite**
Enacted transition — the reader stops waiting for the perfect time and feels ready — champing at the bit — to take the last ordinary dose
Belief now: entry lingers will it work for me; exit feels concrete proof that easy escape has happened to people like them and predicts their own moment of revelation
Concrete encounter: a boring commute / Tuesday evening / shop queue that will soon prove freedom without needing a fix
Evidence: L-01, L-02, L-03 lived patterns as stability proof; E-15 brief hump as honesty about first days | Limits: testimony not data; do not promise superpowers; honour E-15 preliminary
New instruction: none (readiness gate is structural, not instructional)
Reserved-later fence: ritual vow reserved to C-13; ordinary-life chapter reserved to C-14
Arc: pre-vow pivot
Reader-state: person on threshold needing permission to trust belief change already won
Mantra: none (echo density held)
Scene: no new analogy; embedded long-form testimonial 1–2 pages with concrete numbers and sensory details in main flow, not appendix
Structural responsibility: long testimony in main flow; readiness gate (if not ready, re-read); upcoming-moment prediction; gate for page-skippers to start at beginning
Guardrails: anecdote as gentle proof; original prose; CA-01; do not narrate study design; revel in Imp's death throes as positive
Continuity: receives closed routes; hands forward readiness
Word budget: 4400

**C-13 — The Last Ordinary Dose**
Enacted transition — the reader crosses the threshold, makes the solemn vow and is instantly free — not becoming free over time
Belief now: entry is ready but still thinking when will I be free; exit knows I already am free as of this dose
Concrete encounter: the last ordinary dose taken with attention on the ugliness, vow spoken, congratulation immediate — not a laboratory tasting
Evidence: E-04 mild but well-defined, E-15 brief | Limits: do not promise zero sensation; honour brief hump
New instructions: I-09 TAKE YOUR LAST ORDINARY DOSE AND MAKE THE SOLEMN VOW, I-10 NEVER REOPEN THE DECISION
Reserved-later fence: ordinary life lived days reserved to C-14; recap reserved to C-15; no new teaching after vow
Arc: vow / ritual detonation; freedom detonated
Reader-state: person at gates of prison, turning to fruited plains; needs instant identity conferral
Mantra: debut M-G FANTASTIC! I'M FREE! — pinned in plain text with ID; echo M-A (at most one echo plus debut on vow card — so echo M-A)
Scene: SC-06 token echo only; no new full staging
Structural responsibility: last ordinary instance (not laboratory dose), solemn vow, instant conferral, warning against two relapse doors (bad-day rescue offer; just one cannot hurt)
Guardrails: confer freedom as identity now; gate on readiness not schedule; pity-not-envy seeding; CA-01; at most one echo plus debut on this card
Continuity: receives readiness; hands forward free identity
Word budget: 3800

**C-14 — Mornings, Shops, Tables**
Enacted transition — the reader lives ordinary days and finds thoughts they already own are enough to stay free without a new curriculum
Belief now: entry worries how will I cope in my old life; exit lives a morning, a shop, a meal and discovers the old contexts prove freedom
Concrete encounter: waking without the hunt, shopping without the aisle's pull, eating a satisfying meal where real food is sweet
Evidence: no new evidence; invoke tokens only | Limits: do not re-argue settled demolitions
New instructions: I-11 REJOICE AT A DEAD ENEMY, NEVER MOURN A LOST FRIEND, I-12 IF YOU SLIP, FORGIVE IT AND GUARD THE BELIEF (thought-reframe and slip-forgiveness as speech)
Reserved-later fence: recap reserved to C-15 only
Arc: ordinary-life; freedom crescendo
Reader-state: newly free person needing to inhabit life without being taught; needs pity-not-envy script and pink-elephant reframe lived, not lectured
Mantra: echo M-C, echo M-G (two IDs — within limit)
Scene: SC-09 pharmacy aisle (full staging debut) — re-seeing shoppers as trapped not indulging
Structural responsibility: one ordinary-life chapter using thoughts reader already owns, once — not a new thought-curriculum; do not restage settled scenes
Guardrails: rehearsal as speech not doctrine; pre-forgive slips without licensing repeat; CA-01; do not white-knuckle avoid triggers — inhabit confidently
Continuity: receives vow; hands forward lived freedom
Word budget: 4200

**C-15 — Free For Good**
Non-argument — recap & hand-off
New instruction: none (recap lists I-01 to I-12 verbatim as photographable list)
Reader-state: free person who needs the whole method in a pocket list and an outward push into life
Concrete encounter: looking back over the trap seen plain, looking forward to getting on with enjoying life — not three teaching manuals
Mantra: echo M-G (terminal hand-over) — only one echo on this final recap exception may cite hand-over mantra
Scene: no new scene; no staging; token mentions only
Structural responsibility: short recap — photographable instruction list without chapter-number callbacks; outward imperative; saved fresh reframe delivered here only (you recovered sweetness)
Guardrails: clipped summary bullets state belief that changed in ordinary sentences; not token roll-call or study note; no mid-book instruction recap; CA-01
Continuity: receives ordinary life; hands over to life itself
Word budget: 3000
Reserved-later fence: none — this is the hand-off

---

*Plan is single source of truth. Chapter writers resolve every card against the inventories above with no separate commissioning step.*
```

### Reviewer findings
```
## Metadata
- **reviewer_prompt:** `prompts/master-plan-reviewer-v2.md`
- **plan_path:** `production-books/quit-sugar/master-plan.md`
- **plan_sha256:** `11d430c9ef2d39132365b1d9544773c6a7aee07eb70ac0beb16f47c6fcc02328`

## Findings

**first_three_cumulative_walk:** PASS — C-01 installs contract now (I-01–I-03, M-A/M-B pinned, SC-04 debut, BAD SUGAR decree in §1). C-02 persuades now (conned-not-choosing, M-C/M-D, body/instinct/real-food encounters, E-05/E-08/L-02). C-03 enacts axis switch now (M-E/M-F, SC-02, E-10/E-12/L-03) — not three deferred-setup chapters.

**whole_book_cumulative_walk:** BLOCK — plan | C-10, C-13 | SC-06 constraint is “use only after vow,” but C-10 assigns brief debut and C-13 token echo only — finished book either breaks post-vow scene ownership or pre-empts the cage-habit job. Smallest fix: drop SC-06 from C-10; debut SC-06 on C-14 for post-change anxiety; keep C-10 on prison-door/released-convict only.

**writer_facing_authority:** BLOCK — plan | whole-book, C-11 | No plan-wide justification menu mapped to owning demolition cards (style-guide B8); C-03 quotes a menu with no ownership map. C-11 cites E-15 for “weaning worsens” but E-15 payload is time-limited hump only — writer cannot resolve limits. Smallest fix: add verbatim menu with card ownership (fuel→C-04, treat→C-05, social→C-03/SC-02, etc.); reassign weaning myth to E-05 and/or E-16 with card limits.

**method_evidence_safety_originality:** PASS — Carr forks explicit; warm-to-reader/harsh-to-trap; willpower-free; fear disowned after hard facts on demolition cards; CA-01 guardrailed; CONTESTED/MIXED rows carry limits; margin-for-error present; original creature/scene bank.

**architecture_and_length:** PASS — 15 chapters; budgets sum 60,000; first third installs contract, hooked trap, creatures, body/real-food ground by C-02; C-06 inhabit-primary; post-vow spine is C-13 ritual / C-14 ordinary life / C-15 recap; curves and destination declared.

**gate_4_speakable_card_sanitization:** BLOCK — plan | §2 L-01, E-13 | P-04 persona codes appear in evidence-ledger scope/inference rows that cards resolve (L-01 on C-04/C-06/C-12; E-13 on C-04) — forbidden planner-to-writer leakage. Smallest fix: replace P-04 with reader-state wording in those ledger rows.

**brief_alignment:** PASS — Target behavior, reader, scope/non-goals, and load-bearing false belief match `00-brief.md`; fork axes decided in plan §1.

**research_ledger_alignment:** PASS — Card-cited E-01–E-17 and L-01–L-03 rows trace to research syntheses with grade, permitted/prohibited inference, and safety limits; no orphan testimony IDs on cards.

needs changes first
```
