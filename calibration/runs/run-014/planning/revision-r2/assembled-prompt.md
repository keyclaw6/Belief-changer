You are the master-planning revision agent for one universal belief-change book factory run. Everything following this wrapper consists of the complete permitted inputs for this task. Use only those inputs. Revise the complete plan intelligently in response to the review, resolve both review blockers, and preserve all sound architecture. Return only one complete, self-contained master plan—never a diff, patch, progress note, critique, or explanation outside the plan. Do not access the filesystem, tools, subagents, network, outside knowledge, prior work, or any material not present below.

===== BEGIN PERMITTED INPUT 1/8: prompts/master-plan-skill-v2.md =====
# Writing the Book Master Plan — normalized agentic blueprint

You are the book's master planner. Own the architecture. Think as deeply and creatively as needed; choose your own planning approach. Your deliverable is a coherent build brief for strong chapter writers, not a transcript of your reasoning and not a deterministic state machine.

## Exact planning-call inputs (non-negotiable)

The planning call receives exactly this prompt plus these five files, and no other context:

- The complete style guide — `prompts/style-guide.md`
- The brief — `production-books/<slug>/00-brief.md`
- The accepted framing — `production-books/<slug>/framing.md`
- The accepted lived-experience synthesis — `production-books/<slug>/research/lived-experience.md`
- The accepted scientific-evidence synthesis — `production-books/<slug>/research/scientific-evidence.md`

Do not read a reference book, anything under `analysis/` or `calibration/reference/`, calibration reference text, judge output, source packets, other chapters, or another book artifact. If a required input is missing, empty, too thin, or accompanied by forbidden context, STOP and report the exact-input contract failure. Do not gather new context inside planning.

## Mission

Produce the single authoritative `production-books/<slug>/master-plan.md` from which a fresh writer can create every chapter while seeing only the style guide, this plan, and the immediately previous chapter.

The plan must be specific enough to write from and lean enough to remain coherent. Define every shared book decision once under a stable ID. Chapter cards reference those IDs. Never maintain two sources of truth.

Do not include your scratch work, a review checklist, or claims that you checked yourself.

## Required blueprint

Use whatever organization best expresses the book, while making the following semantic content unambiguous.

### Book core

Lock the target behavior, one reader expressed through 3–6 functional personas, the load-bearing false belief, through-line, format, all five fork decisions, the redefinition and margin-for-error doctrine if needed, the clinical/eating-disorder safety perimeter, the strongest pro-behavior scene, the destination state, and one fresh ending reframe.

Preserve the method: escape not sacrifice, non-shaming, no willpower, no fear as motive, immediate freedom after belief change, autonomy, original prose, and no inner creature to battle.

### Compact evidence ledger

Carry only evidence the book may actually use. Give each entry a stable ID and enough payload for an isolated writer:

- the finding, lived account, reader line, or justification;
- exact source ID;
- `SUPPORTED`, `MIXED`, or `CONTESTED` for science, or the correct lived-outcome tier;
- scope and context;
- permitted inference;
- prohibited inference.

Exact quotations must match the synthesis. Interpretations stay unquoted. Do not copy a full synthesis or duplicate evidence inside chapter cards.

### Mantra sheet

Choose and consolidate 6–10 original frozen mantras that deserve repetition. Define each once with:

- stable ID and exact wording;
- the belief or emotional job it installs;
- debut chapter ID;
- echo chapter IDs;
- hand-over form in the final movement.

Mantras are routed by chapter, not by occurrence arithmetic. Chapter cards reference mantra IDs and never repeat the frozen wording.

### Lexicon and instruction spine

Define the book-specific trap register, freedom register, banned willpower register, and source-grounded reader dialect once.

Define each numbered instruction once with a stable ID, frozen wording, owning chapter, and recap placement. Any instruction that could conflict with qualified clinical care must contain its safety exception in the frozen wording.

### Arc and length

Choose the chapter count and architecture that best deliver the behavior-specific belief change. Treat this spine as whole-book functions whose composition, merging, emphasis, and order belong to your judgment, not as a chapter-per-function template: trust and participation → dissolve loaded choice → switch the evaluation axis → demolish benefits → expose the inversion → close escape routes → widen the indictment where supported → meet the strongest scene → demystify → knowledge/readiness gate → chosen threshold → relapse-proof → ordinary life.

Every argument-bearing chapter must be composition-feasible within its budget as one completed, value-bearing correction to what the reader believes the behavior gives, costs, means, or requires, grounded only in evidence and logic that chapter owns. The opening movement, taken as a whole, must complete a value-bearing correction rather than consist entirely of setup for later persuasion. A completed correction must make the prior valuation less credible now through the chapter's owned evidence or logic; naming the belief, cataloguing its assigned jobs, posing unanswered questions, or promising later examination is setup, not completion. Trust, definition, scope, safety, recap, bridge, and hand-off functions may support or consolidate that movement without becoming a second thesis. A chapter serving a necessary non-argument function need not invent a belief correction, but it must be lean enough for its budget and must advance, protect, or hand over the surrounding persuasive movement rather than replace it or merely defer it.

Use your judgment to merge, reshape, move, or omit material that cannot meet this boundary honestly and compellingly.

Map concept debuts, qualitative demolition and freedom curves, structural responsibilities that genuinely apply, instruction placements, the saved ending reframe, and one integer word budget per chapter.

For a HARNESS calibration plan, chapter budgets must sum exactly to 54,000–66,000 words. State the arithmetic sum. Length is planned, not hoped for.

### Compact chapter cards

Give every chapter a stable ID, number, and working title, then specify only its semantic work order:

- the chapter's one belief job and the objection or justification it resolves when it is argument-bearing, or its necessary definition, safety, recap, bridge, or hand-off function when it is not;
- arc position and qualitative curve position;
- target persona IDs and the reader voice or scene that makes the move land;
- evidence-ledger IDs, including the limits the chapter must preserve;
- mantra IDs debuted and echoed;
- instruction ID, if any;
- one or more concrete scene/analogy IDs and the argumentative job each performs;
- structural responsibility, if any;
- method, safety, and originality guardrails specific to this move;
- continuity intent: what understanding it receives and hands forward;
- one integer word budget matching the arc table.

The writer derives `IN THIS CHAPTER`, the italic thesis, section flow, ALL-CAPS landing, SUMMARY, sentence rhythm, and analogy density from the style guide. Do not prewrite those prose elements in the plan.

## Normalization law

Do not create:

- exact mantra occurrence counts;
- a second mantra audit or cumulative state matrix;
- repeated full mantra, instruction, evidence, persona, or slot text in chapter cards;
- prewritten previews, theses, landings, or SUMMARY prose;
- a single-use phrase ledger;
- duplicated chapter-to-persona or chapter-to-slot matrices;
- generic style-guide rules copied into every card;
- a deterministic planning procedure, renderer, or validator.

A missing semantic requirement is a plan defect. A missing duplicate representation is not.

## Evidence and originality boundary

Use only the supplied syntheses. Preserve every evidence grade, outcome tier, source limit, and uncertainty. Never invent a source, quote, author experience, medical result, efficacy claim, mechanism, or authority conflict.

The plan may assign an evidence-unavailable treatment when a familiar structural move is unsupported. It must not create filler to make every generic slot appear.

## Fresh review gate

The plan is not final until a fresh reviewer from Gemini 3.1 Pro, GPT-5.6 Sol, or Grok 4.5 at its highest supported reasoning mode reviews the exact permitted inputs plus the candidate and records `master-plan-review.md` ending with the standalone line:

`fit to write from`

Resolve genuine blocking issues and re-dispatch a fresh reviewer, up to three cycles. Reviewer preferences about prose, ordering, or extra bookkeeping do not override a coherent model-owned architecture unless they expose method-integrity, evidence-honesty, blindness, missing-context, safety, length, or whole-book coherence failures.

## Output

Return only the complete master-plan document. It lives at `production-books/<slug>/master-plan.md`; the review lives at `production-books/<slug>/master-plan-review.md`. Version-control actions belong to the caller.
===== END PERMITTED INPUT 1/8: prompts/master-plan-skill-v2.md =====

===== BEGIN PERMITTED INPUT 2/8: prompts/style-guide.md =====
# The Belief-Changer Style Guide & Writing Prompt (v2)

**Status:** Canonical, reusable craft asset for the whole project — behavior-agnostic by design. v2 adds **Part B: The Prose Engine**, derived from full computational + close-reading analyses of Allen Carr's *The Easy Way to Quit Caffeine* (`analysis/easyway-prose-patterns.md`) and — v2.1 — *Good Sugar Bad Sugar* (`analysis/sugar-prose-patterns.md`), which validated every Part B pattern at 3.5× length and contributed the full-length architecture (§B10). Part A (the method) is distilled from the original three reference books.

**Who reads this:** (1) Every chapter-writing agent, before drafting any chapter. (2) The master-plan step, when architecting a new book for a target behavior — the master plan must produce the per-book sheets defined in §B8.

**The one job of every book we write:** Move the reader to a frame of mind where, whenever they think about the target behavior, they feel *relief and freedom that they no longer do it* — so that stopping feels like **escaping a trap, not sacrificing a pleasure**. We change the belief; the behavior then changes on its own, without willpower and without shame.

**THE REPETITION LAW (governs everything):** *Mantras are repeated VERBATIM, routed by chapter exactly as frozen in the master plan's single mantra sheet. Everything else is never repeated verbatim.* (Full system: §B1–§B2.)

**Structure:** **PART A — THE METHOD** (the worldview, the engine, the forks, the moves, the arc). **PART B — THE PROSE ENGINE** (the binding writing contract: the mantra system, repetition schedule, lexicon, sentence operators, per-chapter contract). Where Part B is more specific, Part B wins.

---

# PART A — THE METHOD

## 0. How to use this guide

- **Read sections 1–4 to absorb the worldview.** You cannot write convincing belief-change prose unless you yourself hold the model: people already choose what they believe is their happiest option; the behavior persists because the belief about it is wrong; correct the belief and desire collapses. Internalize the *convergent engine* (§3) above all.
- **Use §5–§7 as your live toolkit while drafting** — the argument moves, the emotional framing, the voice rules. Reach for them by name.
- **Use §8 as the skeleton** — the chapter-arc template, built on the caffeine book's proven sequence, adapted to any behavior. The master-plan step builds each book's outline from this.
- **Keep §9 (guardrails) open at all times.** These are the lines that, if crossed, break the method. Most failure modes are guardrail violations.
- **Use §10 before you write a single word for a new target behavior** — the adaptation playbook converts every move to gaming, doom-scrolling, sugar, etc.
- **Echo §11 (exemplar lines) in spirit, never in letter.** We write original prose. These show the *shape* of a killer line; produce your own.

A note on the word "prompt": this document is long on purpose. Density beats brevity here. When you draft, you are not summarizing this guide — you are executing it.

---

## 1. The three philosophies (each book's engine)

For each source, two questions: **Why does the behavior persist?** and **How does change happen?** Hold all three in your head as a spectrum; we stand at their convergence (§3) and choose deliberately where they diverge (§4).

### 1A. Allen Carr's Easyway (the caffeine book) — *the canonical structure*

- **Why the behavior persists:** A **belief**, not a chemical need. Two monsters. The **Little Monster** is a trivial, near-imperceptible physical withdrawal that "complains" when unfed. The **Big Monster** is the lifelong **brainwashing** — from family, advertising, society — that interprets the Little Monster's twinge as proof the substance gives pleasure or relief. The whole trap is a single back-to-front error: *the brain mistakes the substance as relieving a discomfort that the substance itself created.* You never rise above baseline; each dose only briefly returns you toward the non-addict normal you had before you ever started, then guarantees the low returns. "The boost comes from the reality that caffeine creates a low."
- **How change happens:** Kill the Big Monster (correct the belief) and the Little Monster starves to death on its own — easily. The method is explicitly **"counter-brainwashing."** Strip every justification (taste, energy, focus, sociability, "the norm," habit) by **reassigning the credit** to its true source (the situation, the body, the moment), demolish the illusion of "free choice" as a confidence trick, then stage the quit as a **celebratory ritual** ("the final shot") that confers freedom as an **instant identity**. The whole second half is **relapse-proofing**: guard the belief, never reopen the decision, reframe (don't suppress) the thought, rejoice at a dead enemy, refuse substitutes, pity (don't envy) users, forgive slips, change nothing else in life.
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

7. **Freedom is available immediately and is an identity, not a sentence.** You are free the moment the belief changes — "day 1," "the moment of your final shot," not at some future milestone. Reject "one day at a time" and day-counting as willpower-era devices that keep the behavior alive as something still being missed. (Carr and Burgeon explicit; Freedom Model via "the quit" that needs no maintenance.)

8. **Relapse-proof by guarding the belief, not the behavior.** After the change, the only real danger is mental: reopening the question, mourning a "lost friend," feeling deprived, catastrophizing a slip. Pre-load the reader against each. A slip is feedback or a warning, never a failure. (All three: Carr's 15 instructions; Freedom Model's lapse-as-feedback; Burgeon's anti-perfectionism.)

**If a passage you write does not serve one of these eight, cut it or rewrite it until it does.**

---

## 4. Divergences — the spectrum, and OUR chosen position

The three books genuinely disagree on several mechanisms. A writer must know the spectrum to avoid contradicting themselves, and must know where *we* stand. Our positions below are the project's house style; follow them unless a specific book's master plan overrides for a good reason.

### Fork 1 — Is there an "inner monster" to personify, or not?
- **Carr:** Yes — the Little Monster is a vivid, near-living parasite you "starve to death" and whose "death throes" you "revel in." Personification makes the craving *external* and *winnable*.
- **Burgeon:** Explicitly **rejects** this — a "monster" creates a "Me vs Them" fight with an "imaginary enemy"; "it was me all along." You don't fight, you understand.
- **OUR POSITION:** **Externalize the *belief/brainwashing/industry*, but do NOT personify the craving as a creature the reader must battle.** We keep Carr's power of naming an enemy (the trap, the engineered hooks, the implanted lie) while keeping Burgeon's insight that fighting your own mind is exhausting and self-defeating. Name the *trap*; dissolve the *craving* by understanding. If you ever use a "monster"-like device, make it the **industry/the lie**, not an internal beast the reader wrestles. (This also fits the Freedom Model's "craving is an activity you choose," not a force attacking you.)

### Fork 2 — Total abstinence, or radical autonomy (moderation allowed)?
- **Carr & Burgeon:** **Total cessation** is the only stable state. One "special" exception means the belief is intact; moderation makes the thing more precious (forbidden-fruit) and guarantees creep. "Unplug every cord."
- **Freedom Model:** **Radical autonomy** — explicitly permits moderation or even continued heavy use; refuses all authority over the reader's goal; success = the reader freely choosing what they see as best.
- **OUR POSITION:** **Lead with the autonomy stance to build trust and ownership, but let the logic drive toward total freedom as the obviously easier, more stable choice — without ever *commanding* it.** We never bark "you must quit." We dismantle the belief so thoroughly that moderation loses its rationale (Carr's pincer: "if there's no benefit to doing it often, there's no point doing it occasionally either"), and we let the reader arrive at totality themselves (Burgeon's self-discovery). The reader keeps the dignity of choosing; the prose makes freedom the choice that any clear-eyed person would make. **Hold the autonomy frame and the total-freedom destination in the same hand** — this is our signature synthesis. Never resolve it into either nagging (pure Carr command) or wishy-washy "do whatever" (a misread of the Freedom Model that abandons the reader).

### Fork 3 — How much neuroscience / hard fact?
- **Carr:** Light, vivid, illustrative (spider webs, the insecticide fact) — facts as *perception-shifters*, never a literature review, and always de-escalated so they don't read as scare-mongering.
- **Freedom Model:** Cites named studies as *escape-route closers* (you can look them up; blocks "you're making this up"), but disowns fear as a motivator.
- **Burgeon:** Details dopamine downregulation, the Coolidge Effect, etc. — then **explicitly subordinates it**: "your brain does not care about negatives when it is in a reactionary state." Quarantines raw citations to a back-matter appendix to keep the prose clean.
- **OUR POSITION:** **Use science to make the trap *visible*, then immediately state that knowing-the-harms is not what frees you.** Facts serve perception, never fear. Keep the prose emotionally clean; if a book needs hard citations, quarantine them in an appendix (Burgeon's model). Every fact must earn its place by exposing the illusion (mechanism 2 of the engine), not by frightening the reader into compliance — fear-based quitting is loss-framed and relapses.

### Fork 4 — Is the conventional "cure" an ally or the villain?
- **Carr:** The villain is the *substance + industry*; he doesn't much attack other quit programs except to say willpower is the wrong method.
- **Freedom Model & Burgeon:** The **recovery/self-help apparatus itself** is a primary villain — it manufactures fragility, fear, and the "need," and tracking-your-own-recovery is disguised pleasure-seeking.
- **OUR POSITION:** **Name the engineered trap (industry, algorithm, product design) as the external villain, and treat willpower/shame-based "recovery" as the well-meaning *wrong method* that kept the reader stuck** — without turning the book into a culture-war polemic against treatment. We borrow the Freedom Model's liberating "you were deceived, be angry at the deceiver" without adopting its full anti-recovery crusade. Keep the reader's gaze on the trap they're escaping and the bad *method* they were sold, not on a tribal enemy.

### Fork 5 — Replace the void, or just walk away?
- **Carr:** "Change nothing else in your life" — inhabit the old contexts confidently to prove freedom; no elaborate replacement needed (the body's natural baseline returns on its own).
- **Burgeon:** You **must** build a positive replacement (environment redesign + transmutation) or the compulsion migrates into the hole left behind.
- **Freedom Model:** Drop the vigilance entirely; the needed capacities are already inside you.
- **OUR POSITION:** **Behavior-dependent.** For purely chemical/consumptive behaviors with a true natural baseline (caffeine, sugar, nicotine), lean Carr — reassure that the body simply returns to normal and avoidance/over-engineering is unnecessary. For behaviors that occupy *time, identity, or a coping function* (gaming, doom-scrolling, porn), lean Burgeon — name the root craving, and give a concrete positive direction so freedom isn't an empty hole. The master plan must decide this per book and state it. **Default: address the root and offer a positive direction whenever the behavior fills time or soothes an emotion.**

---

## 5. The belief-change toolkit (argument moves)

These are the method's moves — the actual machinery of changing a mind. Use them by name. Most chapters deploy several. Order roughly follows the arc (§8).

### 5.1 Pre-build trust before any argument
- **Origin myth / lived proof.** Open with a credible personal escape (the author or a composite) — ideally someone who quit overnight, easily, after years of failure. Establishes the "easy" expectation before defenses engage.
- **Voice the reader's skepticism first.** "Too good to be true? That was my reaction too." Naming the disbelief neutralizes it.
- **The reluctant convert.** A skeptic who succeeded *against their own expectations* is far more persuasive than an enthusiast. Use composite testimonials this way.
- **Warm complicity.** Ally with the reader's desire to stop against the behavior: "Of course you want to stop — that's why you're here. I don't blame you."

### 5.2 Convert the reader from audience to participant
- **Sequenced commitments ("instructions").** Carr's device: a short list of small agreements the reader accepts up front (keep an open mind; don't quit yet; start happy). Compliance becomes self-enforcing — later resistance reads as breaking one's own agreement. *Adapt for our autonomy stance: frame these as invitations/requests for the experiment, not commands.*
- **Defer the behavior change.** Explicitly tell the reader **not to quit or cut down until they've finished the book.** This removes the threat of immediate sacrifice so the belief can change first. This is one of the most powerful moves in the canon — it disarms the reader's whole defensive crouch.
- **The no-risk frame.** "Nothing to lose and everything to gain," repeated. Lowers the cost of reading on.
- **Make the reader an investigator.** "Question what you think you know." They are not being converted; they are investigating — so the conclusion feels like *theirs* (Burgeon's self-discovery; the Freedom Model's "no conviction lasts like the one you work out yourself").

### 5.3 Dissolve "free choice" without assigning blame
- **The confidence-trick reframe.** You weren't foolish; you were *conned*. You chose the first exposure on false information ("phoney information"), then the trap removed your choice. Strips both shame and the "but I choose this" defense in one move.
- **The "who's in charge?" logic trap.** "If you wanted to quit a hobby you enjoy, would you need a book on how to stop?" The mere fact the reader holds this book proves they are not freely choosing. Self-evident, unanswerable, non-accusatory.
- **(Freedom Model counter-balance):** Where Carr says "your choice was taken away," the Freedom Model says "it was always your choice — for the happier option." **Our synthesis:** the *first* exposure and the *continuation* were choices made on false beliefs about the payoff; correct the beliefs and the choice re-opens. This keeps agency (no victimhood) AND removes shame (the beliefs were installed, not invented by the reader).

### 5.4 Switch the evaluation axis
- **From "does it do more harm than good?" to "what good is there at all?"** Refuse the harm-vs-benefit debate (which you can lose to a study). Demand the behavior justify a *positive* benefit — a debate it cannot win once the benefit is shown to be illusory.
- **"Doing TO you vs. doing FOR you."** Capitalize the prepositions. The behavior is doing plenty TO you; it is doing nothing FOR you. Instantly legible two-column ledger.

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
- **A celebratory final act**, not a deprivation. The "final shot" taken with a solemn vow, attention forced onto the behavior's ugliness so the reader exits on *disgust and resolve, not nostalgia*. Cross into freedom on a high of joy.
- **Gate on readiness, not a schedule.** "Do you feel ready? You should be champing at the bit. If not, re-read." Behavior change follows genuine belief change; lingering reluctance is a signal to re-read the *doctrine*, never to summon willpower.
- **Confer freedom as an instant identity.** "Don't wait to be free — you already are." A clearly marked "you are free as of now" kills the corrosive doubt of "when am I actually free?"
- **(Our autonomy synthesis):** stage the threshold as the reader's own decision, and pair Carr's ritual with Burgeon's non-prescriptive close — offer the rite, don't *order* it. The reader steps through the door; we never shove.

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
- **Wound and bandage in the same breath.** When you deliver a hard truth ("you're addicted"), immediately soothe it ("don't panic — the trap is easy to break once you see it"). Never leave the reader in dread.
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
- **Anti-guru, peer-to-peer.** We are not an authority issuing verdicts from above; we are a fellow escapee handing over a key. (Burgeon's register; the Freedom Model's renounced authority.) This is essential to our autonomy stance.
- **Short, blunt verdict-sentences after a build-up.** Let the cadence perform the certainty. "It's the other way around." "Don't wait to be free — you already are." Land the point, then stop.
- **Plain, confident, repetitive refrains.** Repeat key promises verbatim like a chorus ("nothing to lose and everything to gain"; "escape, not sacrifice") to embed them.
- **Rhetorical questions that close escape routes.** Make the reader keep catching themselves in self-contradiction and concede the point internally.
- **Coin a small, proprietary vocabulary** — a memorable name or two the reader will think in afterward (Carr's Little/Big Monster; Burgeon's "Pang," "energy vampires"). Once named, a concept can be invoked in a phrase. *Per Fork 1, name the trap/belief, not an inner beast.* Define loaded words on our terms early (redefine "failure," "giving up," "self-love," "success") to install our interpretive lens.
- **Concrete analogy over abstraction, every time.** The tradition runs on vivid, everyday images (see §11). When you must explain a mechanism, reach for a picture, not a definition.
- **Anecdote as gentle proof, not data.** A lived human story carries an abstract point better than statistics. Use sparingly and warmly.
- **ALL-CAPS for the few real climaxes and the core commitments** — used sparingly, it gives the prose a scannable spine and makes key beliefs shout off the page. Do not overuse.
- **Confessional vulnerability buys credibility.** The author's own humiliating moment (cake from the trash; 100-a-day habit; years of relapse) proves the principle and signals "I will never look down on you."
- **Never moralize.** No "you should be ashamed," no lecturing, no purity. Good and bad are reframed as *what leads to freedom vs. what leads back into the trap* — not virtue vs. vice.

---

## 8. The structural / chapter-arc template (built on the caffeine book)

The caffeine book's architecture is our proven scaffold. Below is its sequence, generalized to **any** behavior. The **master-plan step uses this to lay out a book's chapters**; chapter-writers use it to know *where in the arc* their chapter sits and what job it must do. The arc has two halves — **first half: diagnose the trap; second half: widen the indictment, then land the quit and relapse-proof.** Behavior change is deferred until the belief is changed.

> Adapt freely: not every behavior needs every beat, some merge, and the master plan may reorder for a specific behavior. But preserve the *spine*: trust → participation → dissolve choice → switch the axis → demolish each benefit → diagnose the inversion → close escape routes → widen the indictment → reassign the strongest scene → demystify → stage the quit → relapse-proof → push into life.

### FRONT MATTER — Trust & expectation (before any argument)
- Establish pedigree and an "easy" expectation. Origin myth / lived escape. Voice the reader's skepticism and answer it. Set the emotional expectation: adventure, ease, no doom. (§5.1, §6)

### CH. 1 — Invitation & the instructions
- Convert audience → participant. The small sequenced agreements (open mind, don't quit yet, start happy). The no-risk frame. State the goal as an *emotion* ("happy to be free"). Establish the autonomy stance: this is the reader's own investigation. (§5.2)

### CH. 2 — "Is this even a problem?" — dissolve choice & complacency
- The confidence-trick reframe + the "who's in charge?" trap to dissolve the illusion of free choice without blame. Normalize the harm at the societal scale ("when everyone's sick, no one calls it a disease") so the reader stops trusting their sense of "normal." Remove shame; name the trap. (§5.3)

### CH. 3 — Switch the evaluation axis
- Refuse "harm vs. benefit"; demand "what benefit at all?" Introduce "doing TO vs FOR you." Set up the demolition to come. (§5.4)

### CH. 4 — Demolish the benefits one by one
- Collect the reader's justifications verbatim; demolish each by isolating the variable and reassigning credit. This may span multiple chapters for a behavior with many rationalizations. Leave no foothold. (§5.5)

### CH. 5 — The mechanism: the inversion
- The core inversion (the high is relief from a self-created low; you never beat baseline). The rescuer-as-perpetrator image. Separate the trivial physical part from the dominant belief part. Name the brainwashing and who installed it. (§5.6)

### CH. 6 — Close the escape routes
- Foreclose cut-down, "keep the special ones," quit-tomorrow, weaning. Pre-script and pre-discredit the reader's future rationalizations. Land on the totality logic (drive toward total freedom via the autonomy-respecting pincer, per Fork 2). (§5.7)

### CH. 7 — Widen the indictment (the manufacture of desire)
- Expose the engineered trap: the industry/platform/algorithm, the predatory recruitment, the "manufacture of desire." Reframe the behavior's actual mechanism as a misfiring or self-harming process (the body's danger-response; the dopamine flood "cooking the machine"). Re-code the symptoms the behavior claims to fix as the body's protective warning lights. (§5.6 deepened; §6 awe)

### CH. 8 — The strongest case, met head-on
- Take the single most seductive pro-behavior scene and reassign every drop of its pleasure to its true source ("sneaking a ride"). A hands-on demonstration that the mind accepts falsehood as true (Carr's optical-illusion tables) primes the reader to distrust the felt "benefit." (§5.5)

### CH. 9 — Demystify; (for time/identity behaviors) name the root & the positive vision
- Reframe "addiction" as a simple, correctable misunderstanding — stripping the disease-for-life dread. For behaviors that fill time/identity/emotion (per Fork 5): name the **root craving** beneath the surface behavior and erect the **positive vision** of what real life/connection looks like, so freedom is a richer life gained, not a void. (Burgeon's "Love"/"Neurology" pivot.)

### CH. 10 — The quit (the ritual / the chosen threshold)
- Gate on readiness. Stage the celebratory final act with attention on the behavior's ugliness. Confer freedom as an instant identity. Pair the rite with the non-prescriptive, autonomy-respecting close. Predict the reader's first "moment of revelation" (the situation where the desire simply won't cross their mind). (§5.9)

### CH. 11 — Relapse-proofing (the back-half doctrine)
- The full §5.10 set: never reopen the decision; pink-elephant reframe; dead-enemy-not-lost-friend; ban substitutes & police phrasing; pity not envy; don't evangelize; forgive slips. Plus the behavior-appropriate environment/transmutation guidance (Fork 5).

### CLOSE — Push the reader into life
- End on an outward imperative ("get on with enjoying your life") and a consolidated, scannable checklist of the instructions/understandings — converting the read into action and leaving a portable manual to return to. Reframe the whole effort as *growth*, not quitting. (§5; Burgeon's "Burgeon = to grow.")

### Two recurring structural devices to reuse
- **Quarantine hard evidence** (raw citations, stats) into a back-matter appendix so the main prose stays emotionally clean (Burgeon).
- **Consolidated checklists** at the end — the framing rules and the post-quit rules — turn a one-time read into a reusable reference and reinforce the "follow the experiment" frame to the last page (Carr).

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
- **Make the reader reach the conclusion.** Ask more than you assert. Self-derived conviction is the only durable kind.
- **Gain-frame the alternative.** Stopping = acquiring a better life.

### Never (the failure modes)
- **Never shame, lecture, moralize, or express contempt for the reader.** Instant trust death and a relapse driver.
- **Never use fear as the primary motivator.** Scare-quitting is loss-framed and relapses. Facts serve perception, not terror.
- **Never demand willpower or "just stop."** That's the wrong method we're replacing.
- **Never let "instead"/"I can't have X"/"giving up" stand** — they smuggle deprivation back in. Police your own phrasing as strictly as the reader's.
- **Never personify the craving as a beast the reader must battle** (per Fork 1) — externalize the *belief/industry*, dissolve the craving by understanding.
- **Never concede a single real, irreplaceable benefit to the behavior** — one surviving "good reason" re-powers the whole trap ("unplug every cord").
- **Never make freedom contingent on time, streaks, or day-counting** — that keeps the behavior alive as something still missed.
- **Never catastrophize a slip** — that triggers the all-or-nothing collapse. But never let a slip *license* a deliberate repeat either.
- **Never bark commands** ("you MUST quit"). Hold the autonomy frame; let the logic make freedom the obvious choice (per Fork 2).
- **Never bog the prose down in a literature review.** Quarantine citations; keep the argument clean and emotional.
- **Never overpromise grandiose gains** ("superpowers"). Frame the alternative's "benefits" largely as *the absence of the harm* plus a real, believable positive — so the reader isn't set up for a disillusioned relapse when fireworks don't arrive.
- **Never tell the reader to white-knuckle-avoid triggers** as the strategy. Either inhabit old contexts confidently (Carr) or redesign environment as support (Burgeon) — but avoidance-as-resistance silently concedes the behavior still holds power.

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
List every reason a user of *this* behavior gives ("it relaxes me," "it's how I socialize," "it's the only thing that's mine," "everyone does it," "it's harmless," "I've earned it"). Each gets a §5.5 demolition: isolate the variable, reassign the credit. Plan one demolition per justification.

### Step 4 — Identify the engineered villain (the manufacture of desire)
Who profits and how was the hook built? (Game studios and variable-ratio reward loops and "engagement"; social platforms and infinite-scroll + notification design; food engineers and bliss-point formulation; the porn industry and the Coolidge-effect novelty machine.) This is the external villain the reader can be angry at — channeling anger away from self-shame.

### Step 5 — Decide the physical/chemical reality and how light to go on science (Fork 3)
Is there a real withdrawal (and how trivial)? What's the neuroscience that makes the trap *visible*? Decide how much, and quarantine citations. Always subordinate fact to belief-change.

### Step 6 — Decide: natural baseline, or root + replacement? (Fork 5)
Does this behavior have a clean natural baseline the body returns to (lean Carr: "change nothing else"), or does it fill time/identity/emotion (lean Burgeon: name the **root craving** — love/superiority/pleasure/risk or the behavior's analog — and supply a **positive direction** and environment redesign)? **Default to root + positive direction for any time-filling or emotion-soothing behavior.** State the decision.

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
- **The autonomy/permission close:** *"You can do whatever you want. But will you?"* → Granting the freedom to relapse proves the desire is gone.
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
- [ ] Did I **ask more than I asserted**, letting the reader reach the conclusion?
- [ ] Are my **analogies original** to this behavior (not lifted from caffeine/porn)?
- [ ] Did I avoid **fear-as-motivator**, **commands**, **"instead"/"giving up" phrasing**, and **inner-monster personification**?
- [ ] If this is a back-half chapter, does it **guard the belief** and **pre-forgive slips** without licensing them?
- [ ] Does it sound like a **fellow escapee handing over a key**, not an authority issuing verdicts?


---
---

# PART B — THE PROSE ENGINE (how Carr actually writes)

> **Status:** Derived from a full computational + close-reading analysis of *The Easy Way to Quit Caffeine* (see `analysis/easyway-prose-patterns.md`). Part A gives you the worldview and the argument; **Part B is the binding writing contract** — it governs the actual sentences. Where Part B is more specific than Part A, Part B wins.
>
> Everything here is **behavior-agnostic**. Anything behavior-specific lives in the master plan's per-book sheets (§B8), which the master-plan step derives using this section plus the research banks.

---

## B1. THE REPETITION LAW (the one rule that reconciles everything)

Easyway prose is built on deliberate, scheduled, *verbatim* repetition of a small set of fixed phrases — and on the near-total absence of accidental repetition everywhere else. Our pipeline's context strategy (chapter writer sees only the master plan + the previous chapter) suppresses accidental repetition by design. That means the deliberate repetition **cannot emerge on its own — it must be specified**. Hence:

**THE LAW: Mantras are repeated VERBATIM, in the chapters routed by the master plan's single mantra sheet. Everything else is never repeated verbatim.**

- A mantra is an incantation. Its power comes from arriving in *exactly* the same words every time, so it accumulates weight and eventually fires in the reader's head unprompted. **Paraphrasing a mantra kills it.** If the mantra sheet says "you have nothing to lose and everything to gain," you may not write "there's no downside, only upside."
- Conversely, any striking sentence that is *not* a mantra must appear once and only once in the book. If you find yourself rebuilding an argument the master plan says a previous chapter already made, invoke its mantra token instead of re-arguing it.
- The chapter writer never invents a new mantra and never alters one. Missing or mangled mantras are reviewer-blocking defects.
- The master plan defines each mantra once and routes it by debut/echo chapter IDs. It does not count exact occurrences, duplicate the wording in every chapter card, or maintain a second audit/state matrix. Natural placement inside the assigned chapter belongs to the writer; fidelity belongs to the chapter reviewer.

---

## B2. The Mantra System

### The lifecycle (how a belief gets installed)

Every core belief in the book runs the same four-stage lifecycle:

1. **ARGUE** — the belief gets one full treatment in its debut chapter: the argument, the analogy, the emotional landing. This happens exactly once.
2. **COMPRESS** — within or at the end of the debut, the belief is crystallized into a fixed phrase: the mantra. The compression should feel like the chapter's conclusion arriving in portable form.
3. **REPEAT** — later chapters re-invoke the mantra verbatim, *without re-arguing it*. Each repetition is brief — a clause, a reminder, a drumbeat — and lands in a new context, which is what generalizes the belief.
4. **HAND OVER** — in the book's final movement, the mantra is explicitly given to the reader as a thought script: "whenever you think X, replace it with [mantra]." The book ends by transferring its own voice into the reader's inner monologue.

### Candidate mantra archetypes (the planner chooses and consolidates)

The master plan derives a per-book **mantra sheet** of six to ten model-chosen frozen phrases adapted to the target behavior. The table is a repertoire of jobs, not a demand for one separate phrase per row: consolidate compatible jobs, omit jobs that the evidence or architecture does not need, and keep only phrases strong enough to earn repetition. Each chapter debuts or echoes at least one routed mantra (§B7). Placement rules below are qualitative craft guidance, not occurrence-count arithmetic.

| Archetype | Job | Carr's instance (reference) | Placement rule |
|---|---|---|---|
| **The entry promise** | Risk-reversal that buys the reader's compliance with the instructions; deployed at the exact moments the reader is asked to believe something outrageous | "you have absolutely nothing to lose and everything to gain" | First 10% of the book, 2–3×; may return once near the quit |
| **The promise triad** | The impossible-sounding contract, stated with total confidence | "easily, immediately and permanently" | Front matter + method chapter; heavily front-loaded, then assumed |
| **The trap-namer** | The central metaphor that makes stopping an *escape*, not a sacrifice | "the caffeine trap" → ours: "the [X] trap" | Debuts early, frequency *rises* toward the exit chapters |
| **The illusion-namer** | A fixed dyad/phrase that names the perceived benefit so it can be referenced and demolished as a single object | "a genuine pleasure or crutch" | Debuts in the axis-switch chapter; thereafter the perceived benefit is *only ever* called by this token |
| **The mechanism characters** | Named, proprietary vocabulary for the two-part mechanism (physical loop + belief), so one word re-invokes the whole argument | "the little monster" / "the big monster" — *per Fork 1, ours names the trap/lie/industry, never an inner beast to battle* | Debut in the mechanism chapter (~30% mark); recur to the last page |
| **The sensory definition** | A canonical adjective-string describing the behavior's discomfort/withdrawal, repeated identically so the reader re-labels their own body in our words | "a mild, empty, slightly insecure, slightly uptight feeling" | Debuts in mechanism chapter; repeated whenever withdrawal/craving is mentioned, including in the final instructions |
| **The stakes phrase** | A dual-valence time-horizon phrase used as BOTH threat and reward | "for the rest of your life" (hooked... / free...) | Spread throughout; both valences must appear |
| **The cost formula** | The fixed word-triple naming the addict's permanent state | "tired, run down and lethargic" | Recurs wherever the behavior's ongoing cost appears |
| **The fact-assertion frame** | Not a phrase about the behavior but a repeated *operator* that trains the reader to receive reframes as settled fact | "The fact is..." | Evenly spread; ~1 per 1,000 words |
| **The replacement thought (terminal mantra)** | The thought script the reader keeps forever; what to think whenever the behavior crosses their mind. ALL-CAPS, exclamatory, joyful | "FANTASTIC! I'M FREE!" | Debuts in the instructions (final 15%) and repeats there 3–5×; it is the book's final word on the subject |
| **The named anti-method** | The enemy METHOD (not just the enemy substance): every past failure is reattributed to it, never to the reader | "the willpower method" (38× in the sugar book; defined formally in ch. 1, owns its own chapter) | Defined early; recurs wherever failure, sacrifice, or "hard to quit" appears; signature image: pushing on the door's hinges |
| **The named conflict model** | Names the addict's torn state and gives it a geometry whose resolution is built in: both ropes belong to the trap | "the tug-of-war (of fear)" (23×) | Debuts with the trap chapters; owns the fear chapter; echoed until the quit |
| **The named positive authority** | The alternate authority the reader obeys AFTER the brainwashing is gone — paired with 1–3 operational instruments (tests, gauges, rules-of-thumb) so freedom comes with tools, not just beliefs | "Nature's Guide" + the raw-test, the 0–20 hunger gauge, primary/secondary foods | Own chapter(s) early-mid; instruments delivered mid-book; becomes the post-quit operating manual |
| **The claim block** | The full-sentence promise repeated verbatim as a set-piece (a mantra at paragraph scale) | "Eat as much of your favourite foods as you want, whenever you want... without willpower or feeling deprived" | Planted in ch. 1; re-quoted 2–3× mid-book; returns in ALL-CAPS at the pre-quit pivot |
| **The ease-operator** | The recurring clause that closes every loop by restating the contract's ease | "All you have to do is follow (all) the instructions." (13×) | Sprinkled throughout; especially at chapter ends and after hard arguments |

### Mantra sheet format (lives in the master plan)

For each mantra, define once: **(a)** frozen exact wording — including capitalization and punctuation; **(b)** the job or consolidated archetypes; **(c)** the belief it installs; **(d)** debut chapter; **(e)** echo chapter IDs; **(f)** hand-over form. Chapter cards reference mantra IDs; they do not repeat the wording or prescribe occurrence counts.

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

## B5. The sentence-operator toolkit (reach for these by name)

Voice metrics first — the reviewer checks these (per ~1,000 words unless noted):

- Direct address: ~25–33 "you/your" per 1,000 words; "we" present throughout (see triangle below). (Caffeine book: 28.3/1k; sugar book: 32.8/1k.)
- **Questions: 8–10% of all sentences.**
- **~20% of sentences under 8 words**, clustered at argument peaks.
- Average sentence ~15–17 words. At least one concrete analogy per ~600 words.
- ALL-CAPS: instructions, the terminal mantra, and 2–4 peak moments per book — no more.

**The pronoun triangle (non-shaming machine):** **"I"** = the guide's authority — testimony, promises, warnings. **"we"** = every description of falling into and living in the trap — the confession voice that makes ruthless critique shame-free because the author is inside it. **"you"** = instructions, promises, and the escape. **Falling into the trap is "we"; escaping it is "you."**

The operators:

1. **Fact-assertion** — deliver reframes as flat settled fact: "The fact is..." / "The reality is..." Never hedge ("studies suggest," "many people find" are banned for core claims).
2. **Self-answered question** — ask, then answer immediately with total confidence: "Do you want to stop? Of course you do – that's why you're reading this book."
3. **Trap question** — a question whose only honest answer concedes the argument: "If you genuinely choose it, why would you need this book?"
4. **Ventriloquism** — quote the reader's inner voice in quotation marks (their justifications, their future temptations) and answer it. Early: print the full justification menu as quotes, then demolish one per chapter. Late: pre-play the future tempting thought so it arrives pre-refuted.
5. **The inversion** — "It's not X, it's Y": "It causes the aggravation; it doesn't relieve it." "It's you that's [the benefit], not the [behavior]." Often capped with: "It's the other way around."
6. **Killer-line pair** — two short mirrored sentences at the peak: build-up, then verdict. One per major argument, no more.
7. **Reassurance–challenge cycle** — *schedule* the reader's disbelief: name it ("I know this is hard to accept"), welcome it, re-invite the open mind. Doubt is never ignored; it is pre-empted on a cadence.
8. **Future-pacing** — predict the reader's specific upcoming thoughts, situations, and the named **moment of revelation**. Every prediction that lands transfers authority to the claims that can't be verified.
9. **Permission paradox** — explicitly permit the behavior while reading ("carry on exactly as normal until you finish"). Disarms resistance and proves this isn't willpower.
10. **Credit reassignment scene** — take a cherished scene, strip the behavior out of it, show the pleasure was the scene all along ("it was only ever sneaking a ride").
11. **Instruction voice** — numbered, imperative, ALL-CAPS headline, each instruction followed by its warm rationale. Instructions are thought-substitution rules: "rather than think [old thought], think [mantra]."

---

## B6. The book architecture (Carr's structure, verified against the source)

> **Format note:** §B6 describes the compressed pocket-book architecture. For full-length books (15+ chapters), §B10 — the empirically verified full-length architecture (chapter anatomy, instruction spine, redefinition move, structural slots) — takes precedence.

Part A §8's arc stands. The verified caffeine book adds these structural specifics the master plan must honor:

- **Front matter carries the authority dossier** (origin story, scale of the method's success, the skeptical-convert testimony of the narrator) *and* the full contract: the promise triad, the entry promise, and the five reading instructions — before any argument.
- **The justification menu appears early and verbatim** — the reader's stated reasons printed as a quoted list ("It helps me concentrate." / "It's sociable." / ...), which then becomes the table of contents for the demolition phase: one short chapter per justification, each ending with its credit reassigned.
- **Chapters are short and single-purpose** (the caffeine book averages ~400 words per section under punchy titles, many phrased as questions or as the reader's own words: "Maybe I'll quit tomorrow"). One reframe per chapter; land it; stop.
- **The mechanism chapter (~30% in) is the hinge** — it debuts the mechanism characters and the sensory definition, splits the trivial physical component from the dominant belief component, and everything after it leans on its vocabulary.
- **The strongest case is met head-on, late** — after the easy demolitions, the single most seductive scene gets its own chapter and a hands-on perception demo (an experiential proof that the reader's felt certainty can be flatly wrong).
- **The quit is a staged ritual**: readiness gate ("by now you should be champing at the bit — if not, review the text again"), the ceremonial final act with a solemn vow, instant conferral of freedom ("you're free the moment you finish — don't wait to be free, you already are"), and the warning against the two relapse doors (the bad-day rescue offer; the "just one can't hurt" thought).
- **The back half is instruction-dense**: the numbered post-quit instructions ARE the relapse-proofing, each one a pre-played scenario + thought script.
- **The book ends with verbatim recap lists** of both instruction sets, then a single outward push into life. The last content the reader sees is the portable manual plus the terminal mantra.

---

## B7. The per-chapter writing contract

Every chapter delivered by a chapter writer must satisfy ALL of:

1. **One job.** The chapter makes exactly one belief-move (from the master plan), lands it, and stops. No second thesis.
2. **One mantra set or reinforced.** The chapter either *debuts* a mantra (full argue→compress lifecycle) or *echoes* assigned mantras verbatim at natural moments — per the chapter's mantra assignment in the master plan. Echoes are brief; never re-argue a debuted mantra.
3. **Curve-aware vocabulary.** Use the lexicon registers; respect where the chapter sits on the freedom-crescendo and demolition curves (a mid-book chapter doesn't bathe in freedom language; a final-quarter chapter does).
4. **At least one concrete analogy or scene** doing the chapter's argumentative work (from the master plan's analogy assignment or the analogy bank).
5. **Operator-rich, metric-true prose** per §B5 (questions ~10%, killer-pair at the peak, ventriloquism where the reader would object, no hedging).
6. **Triangle discipline**: "we" for the trap, "you" for the escape, "I" for testimony and instruction.
7. **Non-shaming and gain-framed throughout** (Part A guardrails all apply).
8. **No verbatim repetition of anything except mantras** and no re-argument of previous chapters' settled points — invoke their tokens instead.

The reviewer rejects a chapter that: mangles or paraphrases a mantra; misses its mantra assignment; re-argues settled material; uses banned-register vocabulary; hedges a core reframe; or drifts off its single job.

---

## B8. What the master plan must carry (one source of truth)

Because chapter writers see only the master plan + previous chapter + this guide, the plan must carry all book-specific meaning without copying the same decision into competing representations. Define each shared item once under a stable ID; chapter cards reference those IDs.

1. **Book core** — target, reader/personas, load-bearing false belief, through-line, fork decisions, redefinition and margin, safety perimeter, strongest-case scene, and saved ending reframe.
2. **Compact evidence ledger** — only material the book may use, each item with source ID, grade or outcome tier, scope/limit, and permitted/prohibited inference.
3. **Mantra sheet** — 6–10 original frozen phrases defined once, with belief, debut chapter ID, echo chapter IDs, and hand-over form.
4. **Lexicon** — trap and freedom registers, banned register, and source-grounded reader dialect.
5. **Instruction spine** — each frozen instruction defined once, its chapter ID, recap points, and any clinical/safety exception inside wording that may travel alone.
6. **Arc and budget map** — chapter order and one-line jobs, concept debuts, qualitative freedom/demolition curves, structural-slot ownership, saved reframe, one integer budget per chapter, and the exact sum.
7. **Compact chapter cards** — one belief job; target personas/objections; evidence-ledger IDs; scene or original-analogy ID and its argumentative job; mantra debut/echo IDs; instruction ID if any; structural responsibility; guardrails; continuity intent; integer budget.

Do **not** add occurrence-count arithmetic, a separate mantra audit, cumulative state matrices, repeated full mantra/evidence text, duplicated persona or slot tables, single-use phrase ledgers, prewritten chapter previews/theses/landings/SUMMARY prose, or generic style-guide rules copied into every card. The chapter writer creates the anatomy and prose from §B5, §B7, and §B10; the chapter reviewer judges the actual text.

---

## B9. Pre-flight checklist (Part B additions — run with Part A §12)

- Every mantra in this chapter's assignment present, **verbatim**, correctly cased and punctuated?
- Did I debut anything the master plan says was already debuted? (If so, compress to its token.)
- Any banned-register words? Any hedged core claims?
- Question rate ~10%? A killer-pair at the peak? Sentences under 8 words present?
- "We" for the trap, "you" for the escape — checked?
- Does the chapter's freedom-language level match its position on the crescendo?
- Would this chapter still make stopping feel like *escape* if read in isolation?

---

## B10. The full-length book architecture (validated on *Good Sugar Bad Sugar*, ~60K words)

The pocket-book format (§B6) compresses these away; at full length Carr often runs them explicitly. The planner decides which slots genuinely serve this behavior, evidence, and arc, and records any material omission with a rationale. Do not create unsupported content merely to fill a slot. Source analysis: `analysis/sugar-prose-patterns.md`.

### The chapter anatomy (every chapter, no exceptions)
1. **"IN THIS CHAPTER"** — bullet preview of the chapter's section headings.
2. **Italic thesis line** — the chapter's reframe in one sentence.
3. **Body** — ONE belief-move, built through titled sections, landing on ALL-CAPS verdict lines.
4. **The chapter's instruction** (when assigned) — delivered at the climax, numbered cumulatively.
5. **"SUMMARY"** — clipped bullets restating the chapter's claims, carrying assigned mantras VERBATIM.

The reader meets every reframe at least twice per chapter (argued + recapped). **Previews and summaries are licensed recap zones — exempt from the no-verbatim-repetition rule, exactly like mantras.**

This anatomy is a chapter-writing requirement, not prewritten plan prose. The chapter card supplies the semantic work order; the writer creates the headings, thesis, landing, and SUMMARY, and the chapter reviewer judges them in the completed chapter.

### The instruction spine
- The plan defines each frozen instruction once and routes it to one chapter card by ID; cards and audit tables do not copy it.
- Instructions are **doled out one per chapter at the chapter's climax**, numbered cumulatively (the sugar book has 12 across 20 chapters).
- Include all four types: behavioral ("don't quit yet"), epistemic ("keep an open mind"), emotional ("begin with elation"), and **epistemic firewalls** ("ignore any advice that conflicts with the method", "ignore anyone who quit by willpower", "avoid the influence of other addicts") — explicitly quarantining future belief-threats.
- **Mid-book recap**: the instructions-so-far re-listed verbatim once (~25% mark).
- **The final chapter is the recap**: nothing but the numbered instructions with chapter cross-references ("8. NEVER DOUBT YOUR DECISION TO QUIT. (CH9)") plus a gate for page-skippers ("if you've jumped straight to this page, the method will not work — go back to Chapter 1").

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
- **The pre-endgame knowledge recap** (immediately before the quit chapters): a "• You know that..." litany re-stating every installed belief — the book audits its own installation before firing.
- **The embedded long-form testimonial** ("In his own words — [name]"): 1–2 pages of first-person escape story with concrete numbers and sensory details, including an authority-conflict arc where the reader-surrogate prevails. Drawn from the research banks' freedom testimonies; written original.
- **The myths Q&A battery**: a rapid-fire annex (chapter appendix) — each myth as a quoted reader-voice line, each demolished in 2–6 sentences.
- **The meta-inoculation**: ventriloquize the strongest objection TO THE METHOD ITSELF ("how do I know it's not YOU brainwashing me?") and answer it (counter-brainwashing; "question both sides — don't accept it blindly").
- **Scare-then-disown**: where hard facts must appear, deliver them, then explicitly disown fear as the motivator ("I don't want you to use this information to be frightened — understand it, then put it behind you"). The fact does its perception work; the loss-frame is removed.
- **Perception homework**: 1–3 physical exercises the reader performs (the sensory immersion in the genuine pleasure; the falsification test on the illusory one; the audit exercise). The belief change is enacted, not just read.
- **The vow with "expect the unexpected"**: the final ritual includes guided sensory disgust-attention, the solemn vow with visualization, instant conferral ("CONGRATULATIONS! YOU'VE WON!") — and pre-loads future danger moments INTO the vow ("fix these thoughts now while they are vivid, so when the memory fades the resolution does not"). Plus the **meaningless-days demolition**: no New Year's, no landmark days — STOP NOW.
- **Practical-safety guardrail** (when the behavior touches medication/health): a boxed advisory routing medical specifics to a professional, kept outside the belief argument.
===== END PERMITTED INPUT 2/8: prompts/style-guide.md =====

===== BEGIN PERMITTED INPUT 3/8: production-books/quit-sugar/00-brief.md =====
# Brief — Quit Sugar (working title)

## Target behavior
Compulsive consumption of refined/added sugar and junk carbs ("bad sugar") — the craving–snacking loop and its grip, not nutrition pedantry.

## Reader / audience
An adult who feels trapped in the sugar loop; has tried diets, moderation rules, and willpower and watched them all fail; suspects something is wrong with the whole approach. General adult edition (one clear reader).

## Goal & stance — decide explicitly (style guide §4 forks)
Forks are decided in `framing.md`; expected axes are listed here but not preempted:
- **Outcome (Fork 2):** autonomy-led total freedom vs explicit moderation — where the Bad-Sugar line sits IS the redefinition decision.
- **Void (Fork 5):** natural baseline vs positive replacement — <framing>
- **Science weight (Fork 3):** <framing>
- **Villain (Fork 4):** the engineered trap to name (sugar industry / product engineering) — <framing>
- **Inner state (Fork 1):** externalize the belief/industry; do NOT personify the craving — confirmed (house law).

## The load-bearing false belief (style guide §10, step 1)
<one sentence, fixed in framing: what the reader believes bad sugar GIVES them — expected neighborhood: "sugar is a pleasure/treat/energy-lift that makes life sweeter and I'd be deprived without it">

## Scope / non-goals
Covers the everyday sugar/junk-carb trap for a general adult reader. Non-goals: medical nutrition therapy, diabetes management advice, eating-disorder treatment (crisis-pointer territory, not method territory), weight-loss-program mechanics.
===== END PERMITTED INPUT 3/8: production-books/quit-sugar/00-brief.md =====

===== BEGIN PERMITTED INPUT 4/8: production-books/quit-sugar/framing.md =====
# Framing — Quit Sugar

## Format & scope decisions (Part B)

- **Format:** full-length (§B10). The redefinition, evidence firewall, competing outcome states, six functional personas, and medical/eating-disorder safety perimeter require the full-length architecture. All §B10 structural slots apply, but their chapter placement belongs in the master plan.
- **Primary outcome:** desire-level freedom from the BAD SUGAR decision loop—not weight loss, dietary perfection, metabolic treatment, or a streak of controlled behavior.
- **Primary reader:** one general adult who is tired of anticipating, bargaining, restricting, lapsing, and starting over. The personas below are functional versions of that reader, not separate editions.
- **Scope:** two-tiered. Core sugar-sweetened drinks, confectionery, desserts, sweet baked goods, and sweet snacks are categorically in scope. Genuinely gray-zone refined savoury snacks enter the scope only when they function as discretionary rewards, rescues, grazing, or automatic nibbles rather than ordinary meal food.
- **Non-goals:** diabetes management, medical nutrition therapy, eating-disorder treatment, weight-loss-program mechanics, calorie targets, low-carbohydrate doctrine, or eliminating every source of dietary sugar.

### Redefinition decision (§B10)

The book needs an operational redefinition because eating and carbohydrates cannot be quit wholesale. “Good” and “bad” are method labels, not moral judgments or claims that all listed foods have identical biochemical effects. The definition has a categorical core and a behavior-resolved edge.

**GOOD SUGAR:** sugars and starches found in ordinary nourishment, including whole fruit, vegetables, legumes, nuts, plain dairy, and ordinary meal staples such as oats, rice, potatoes, bread, and pasta. Their sugar or carbohydrate molecules do not bring them into the target category.

**BAD SUGAR:** either of the following:

1. **The categorical core:** a product conventionally consumed as a sugar-sweetened drink, confection, dessert, sweet baked good, or added-sugar sweet snack—including products sweetened with sugar, honey, or syrup.
2. **The gray savoury edge:** a genuinely ambiguous refined savoury snack functioning as a discretionary reward, rescue, graze, or automatic nibble rather than ordinary meal food.

Core examples include soda and other sugar-sweetened drinks, sugar-sweetened coffee or tea, sweets, biscuits, cakes, pastries, ice cream, dessert products, and prominently sweetened cereals or bars. Hunger, care, celebration, convenience, homemade status, or a “natural,” organic, dark, low-sugar, or healthier label cannot move a core item outside the line.

Behavioral-role inquiry applies only at the genuinely gray refined-savoury edge. It can bring an ambiguous item inside BAD SUGAR; it can never exempt a core drink, confection, dessert, sweet baked good, or sweet snack.

Small incidental ingredients in an ordinary meal do not make that meal BAD SUGAR. Nor does this definition assert that a sweet drink, a biscuit, and a refined savoury snack have identical physiology. The core is named directly to prevent motive-based renegotiation; behavioral role resolves only the savoury boundary.

**Definitional decree:** **Throughout this book, whenever I say sugar, a sugar hit, or quitting sugar, take me to mean BAD SUGAR as defined here—not fruit, ordinary meals, or every carbohydrate.**

**Totality inside the line:** the destination is no planned BAD SUGAR doses. It is practical total freedom, not a vow of molecular purity or a declaration that the reader has lost the right to choose. Moderation remains the reader’s legal and moral option, but the book does not present recurring exceptions and negotiations as desire-level freedom.

**Margin-for-error doctrine — the Molecule Margin:** the target is an intentional category of choices, not chemical purity. A trace ingredient, uncertain restaurant sauce, accidental bite, or genuine classification mistake is not a deliberate return and does not mean the reader has failed. Notice it, learn from it if useful, and continue from the choice already made. The margin covers accidents and honest ambiguity; it does not turn planned exceptions into accidents.

**Conditional-bonus extensions:** 100% juice, dried fruit, non-nutritive sweeteners, alcohol, caffeine, and other adjacent indulgences are not required quits and do not define success in this book. A reader may later examine whether one is carrying a similar reward script, but that optional inquiry neither alters the primary BAD SUGAR line nor expands the definition of success. Whole fruit and ordinary meal carbohydrates are explicitly protected from category creep.

**Safety perimeter:** medical glucose, prescribed nutrition, treatment for diabetes or another metabolic condition, pregnancy-related dietary advice, and eating-disorder care sit outside the method. Medical instructions outrank the book. No epistemic-firewall instruction may tell a reader to disregard qualified clinical care.

### Persona set

| Persona | Function and load-bearing belief | Dialect |
|---|---|---|
| **The Sweet-Reward Reader** | Taste, dessert, sweet drinks, or a quick lift seem to provide a special pleasure that life would lose without them. | “I go back for the taste.” “There’s always room for dessert.” “I earned this.” |
| **The Restriction Veteran** | Denial is expected to produce obsession, and one lapse is expected to turn the whole attempt into failure. | “If I deny myself, it comes back worse.” “I was doing well, then I blew it.” |
| **The Context Carrier** | Stress, sadness, boredom, social expectations, convenience, and recurring access make sugar seem like the only realistic option in the moment. | “It was there.” “Everyone else ordered.” “I had no time.” “We eat our emotions.” |
| **The Informed Household Translator** | Better labels, distrust of products, or an achievable reduction may help, but knowledge can slide into hidden-sugar anxiety or household moralizing. | “I check the label.” “Homemade must be better.” “I could manage one less spoon.” |
| **The Managed-Truce Maintainer** | Daily boundaries and resets have produced real relief, so perpetual management may seem like the best freedom available. | “My plan works, but it never clocks off.” “I reset at the next meal.” |
| **The Decision-Tax Escapee** | Previous abstinence preserved dreams, bargaining, or a stash for later; what this reader wants now is irrelevance rather than prohibition. | “I don’t want a perfect streak. I want the debate to stop.” |

## §10 Adaptation playbook

### 1. Load-bearing false belief

**BAD SUGAR gives me a special pleasure, reward, comfort, or quick lift that ordinary food and ordinary life cannot provide, so removing it would leave me deprived.**

The book attacks uniqueness, ownership, and necessity—not the reader’s honesty. Sweet taste can be pleasant, and sugar contains calories. Neither fact proves that BAD SUGAR owns the pleasure of a celebration, provides an irreplaceable form of energy, resolves distress, or deserves a permanent place in the reader’s decision catalog.

### 2. Illusory benefit → true mechanism

**The inversion:** the learned sweet-reward script assigns BAD SUGAR a job—reward this effort, rescue this mood, complete this meal, mark this celebration. Repeated rehearsal of that proposition teaches anticipatory attention: imagining, scanning, postponing, bargaining, and later assigning the item credit. A menu, display, routine, or occasion may activate the familiar loop. Eating the item may end that episode of anticipation, and the resulting quiet can appear to prove that the assigned job was real.

BAD SUGAR can add a brief pleasant taste. It does not thereby create the occasion’s larger pleasure or establish an irreplaceable rescue.

**Core formulation:** **The learned sweet-reward script, strengthened by repeated rehearsal, opens the loop; BAD SUGAR may close that episode and receive credit for a special pleasure or rescue it did not uniquely provide.**

This is principally a belief, attention, learning, and attribution model. It is not a claim that a sugar dose universally teaches anticipation, that every person follows one craving loop, that ordinary sugar consumption is established clinical addiction, that every craving is physiological withdrawal, or that every dose causes a biochemical crash.

**Rescuer-as-perpetrator image — the dessert pager:** imagine that repeated rehearsal of the dessert script has trained you to carry a pager through dinner. A familiar cue makes it buzz. Eating dessert may silence it, and the silence is credited as proof that dessert completed the meal. But the learned expectation issued the summons. The pleasant taste is real; the supposed need for closure was rehearsed.

### 3. Justifications to demolish

| Reader’s justification | Book-specific demolition |
|---|---|
| **“I go back for the taste.”** | Do not deny the sensation. Separate a brief pleasant taste from the claim that the product supplies unique, lasting value. Reassign the larger pleasure to appetite, sensory capacity, the meal, and the setting. |
| **“There’s always room for dessert.”** | Dessert attention beginning before the main meal shows that a learned category has become active, not that the body has proved an additional need. The menu can activate an anticipated decision before hunger has reported anything. |
| **“I earned it.” / “I deserve a reward.”** | The accomplishment, effort, rest, recognition, and permission to stop working are the reward. Sugar is the ceremonial receipt, not the wage. |
| **“I feel weak; I need sugar.”** | Calories are real, but BAD SUGAR is not their unique source. Actual hunger belongs to ordinary eating; tiredness may call for food, rest, or medical attention. Persistent weakness is not material for a belief argument. |
| **“It brings me joy.”** | Preserve the reality of joy while auditing its sources. Company, leisure, anticipation, care, ritual, pleasant taste, and relief from work need not be collapsed into one product’s achievement. |
| **“If I deny myself, it turns up somewhere else and worse.”** | Agree about suppression: controlling behavior while preserving the belief in a lost reward can intensify bargaining. That is evidence against the deprivation method, not evidence that BAD SUGAR is necessary. |
| **“One lapse proves I can’t do this.”** | One event does not contain a command to continue. The collapse comes from the interpretation—“I have ruined it”—not from a universal one-bite mechanism. |
| **“It’s social.”** | Belonging comes from attention, hospitality, shared time, and participation. Dessert can accompany those things without creating them. |
| **“Birthdays and holidays need it.”** | The people, history, surprise, generosity, and shared pause make the occasion special. BAD SUGAR stands under borrowed confetti. |
| **“It calms me when I’m stressed, sad, bored, or lonely.”** | Validate the distress. The pause, permission, sensory interruption, and act of care may be real; the underlying condition remains. Sugar is not entitled to the credit for every part of the pause. |
| **“It was the only convenient thing.”** | Convenience explains why a product entered the hand, not what special benefit it supplied. A default lane is not a need and not proof of powerlessness. |
| **“I was hungry.”** | Eating is essential; a core sweet drink, confection, dessert, baked sweet, or sweet snack remains BAD SUGAR regardless of hunger. Ordinary appetite belongs to ordinary food. Only a genuinely gray refined-savoury snack needs the meal-or-hit inquiry. |
| **“It’s just habit.”** | Repetition explains the route and cue. It does not establish a benefit or remove agency. |
| **“I can control it if I make better rules.”** | The reader may choose rules, but anticipating, bargaining, and resetting are costs. The question is not whether moderation is possible; it is whether keeping sugar important is preferable to closing the question. |
| **“Only weekends, restaurants, vacations, or special occasions.”** | Exceptions preserve the proposition that BAD SUGAR upgrades the best moments. Reassign those moments before discussing frequency. |
| **“This version is natural, homemade, organic, dark, low-sugar, or healthier.”** | Ingredients may differ, and the book must not pretend otherwise. If the product remains a core sweet drink, confection, dessert, baked sweet, or sweet snack, the label does not move it outside BAD SUGAR. Behavioral role decides only a genuinely gray refined-savoury case. |
| **“I’ll keep some for after the diet.”** | A future stash is deferred compensation. It reveals suppression because the imagined special reward remains intact. |
| **“I reset at the next meal, so it’s fine.”** | A reset can be useful within a managed truce and must not be mocked. It is nevertheless management, not evidence that desire and decision tax have disappeared. |
| **“I’m addicted and powerless.”** | Validate the felt pull without turning one person’s analogy into a diagnosis. The accepted evidence does not establish ordinary human sugar addiction. The book needs no disease identity to examine a belief and reopen choice. |
| **“Fruit is sugar too, so quitting is impossible.”** | Apply the definition. Whole fruit and ordinary food are outside BAD SUGAR; molecular equivalence is not the behavioral target. |
| **“A little hidden sugar means I failed.”** | Apply the Molecule Margin. The method guards the meaning of a deliberate choice, not ingredient-list perfection. |
| **“One less spoon is enough.”** | Reduction may be achievable and useful; accepted evidence supports receptivity to that idea, not durable freedom. Do not ridicule harm reduction, but do not rename an early step as the book’s destination. |
| **“I need a substitute for the treat I’ve lost.”** | A consolation product can preserve the belief that the real reward is missing. Ordinary food and genuine pleasures are not consolation substitutes: no special or irreplaceable pleasure has been confiscated, even though pleasant tastes still exist. |

### 4. Engineered villain — documented commercial optimization and observed availability

**Named villain:** **the Demand Machine**.

The Demand Machine names the deliberate commercial practices supported by specific historical records: formulation work, product testing, packaging and promotion, and integrated marketing intended to improve appeal, salience, or demand. It is not a claim that one coordinated present-day machine controls every product or setting. It does not include a retailer, workplace, café, vending site, or other access point merely because food is present there.

**Documented optimization — evidence of specific intent:**

- A 1985 RJR record documents formulation work involving taste, smell, appearance, flavour libraries, and ingredient combinations, including an expressed objective of leaving consumers wanting more (S-013).
- Documentary evidence records numerous product tests on children while developing named children’s drink flavours under historical tobacco-company ownership (S-018).
- FTC records document integrated youth-directed food marketing by major marketers across television, packaging, in-store campaign channels, online media, events, and cross-promotions, alongside company research into children’s influence on purchases (S-015, S-016).

These records support deliberate optimization within their historical, actor-specific scope. They do not establish that every product or company follows the same practice, that testing caused craving or overeating, or that product appeal proves clinical addiction.

**Observed recurring availability — context without intent:**

- Participants described indulgent foods or sweetened products appearing repeatedly in cafés, supermarkets, workplaces, free leftovers, vending machines, gas stations, and time-constrained travel (S-020, S-022).
- Those accounts establish recurring visibility, convenience, and constraint in particular settings. They do not establish coordinated placement, engineered demand, or intent by retailers, employers, workplaces, cafés, vending operators, gas stations, or other access points.

The distinction is load-bearing: some historical manufacturers and marketers deliberately optimized product appeal, testing, and promotion. Separately, people reported encountering products repeatedly in ordinary environments. The first is documented intent. The second is observed context.

The book may say that recurring availability can keep an option visible and reduce the time available for deliberation. It may not convert availability into proof of manipulation, claim that every current product was designed to cause addiction, or suggest that birthdays and social customs were manufactured by industry.

Historical tobacco ownership associations are context, not proof of sugar-specific intent or present practice (S-017, S-018). The publication-payment letter supports only that payment was conditioned on manuscript acceptance; it does not establish fabricated findings or corrupted conclusions (S-014). Neither should become a sensational centerpiece.

### 5. Physical/chemical reality + science weight

**Science weight:** light in the main prose, claim-graded in a back-matter evidence appendix. Scientific claims retain their `SUPPORTED`, `MIXED`, or `CONTESTED` stance; the main prose translates those grades into plain language rather than flattening them into certainty. Science makes distinctions visible. It does not frighten the reader into compliance.

**Withdrawal decision:** sugar-specific physiological withdrawal in ordinary adults is not established by the accepted evidence. The book must not invent a withdrawal timeline, call withdrawal trivial, or present reported battle, dreams, fatigue, headaches, or daily craving management as proof of a universal syndrome. Subjective difficulty is real without settling its mechanism.

**Facts the prose may use carefully:**

- Broad claims of established human sugar addiction remain contested; one critical review found little supporting human evidence (S-001).
- Sweet taste can affect reported pleasure, but pleasure findings are not equivalent to addiction (S-004, S-005).
- Repeated exposure can alter some food-response or associative-learning measures, but the available studies do not isolate sugar consistently or establish escalating compulsion (S-006, S-019).
- Mouse circuit evidence does not establish the same causal mechanism in humans; one human trial found no whole-cohort sucrose-versus-sucralose food-cue BOLD difference (S-003, S-005).
- A controlled ultra-processed-food trial found greater intake and weight gain, but the responsible product feature was unknown (S-019).
- Reviews of substantial fructose or sugar-sweetened-beverage exposure describe pathways relevant to hepatic insulin resistance, but this cannot be generalized to whole fruit, every carbohydrate, occasional consumption, or ordinary craving (S-002).
- BAD SUGAR supplies calories and can taste pleasant. The argument is that it provides no unique or irreplaceable pleasure, rescue, or energy source—not that chemistry and sensation are imaginary.

**Forbidden science claims:**

- “Sugar is cocaine,” “sugar is heroin,” or any settled clinical-addiction equation.
- A universal dopamine hijack, crash, tolerance, or withdrawal story.
- A fixed number of days until cravings or taste “reset.”
- “One bite restarts the addiction.”
- “All carbohydrates are sugar,” “fruit is the same as soda,” or “all refined food is poison.”
- Guaranteed weight loss, metabolic repair, mental clarity, or taste change.
- Universal claims that food companies currently use one addiction formula.
- Using rodent findings as direct proof of human compulsion.
- Treating the learned anticipatory loop as a universal pharmacological effect of a sugar dose.

Where health facts appear, use the **scare-then-disown** move immediately: the purpose is to clarify the target and expose overconfident stories, not to make the reader afraid of food.

### 6. Fork 5 decision — natural baseline

**Choice:** natural baseline, expressed as a return to ordinary eating rather than a replacement program.

BAD SUGAR is a bounded consumptive subset. Removing it does not create an empty calendar, erase an identity, or eliminate food. Ordinary meals, hunger, taste, pleasure, celebrations, rest, and connection remain. The book therefore must not install a new regimen, hobby system, trigger-avoidance life, or nutritional identity.

This does not mean ignoring the functions sugar has been carrying. During belief correction, when a reader has assigned it reward, comfort, stimulation, or belonging, the prose returns credit to the actual need and source. It does not assert a single hidden root craving or prescribe a replacement for every emotion.

**Positive direction:** ordinary eating plus direct ownership of actual pleasures—rest as rest, celebration as celebration, company as company, and food as food.

**Temporary Compass decision:** the Ordinary Eating Compass is a teaching metaphor, not a lifelong authority or dashboard. Its checks help while the reader is learning the BAD SUGAR line and correcting misassigned credit. As those distinctions become ordinary, the named checks should become unnecessary and fall away. If every meal still requires classification, auditing, label surveillance, or boundary rehearsal, the book has recreated managed truce rather than desire-level freedom.

No universal taste reset is promised. The report that fruit tasted sweeter belongs to one person’s testimony and remains a subjective possibility, not an expected mechanism.

### 7. Behavior-specific analogies to invent

| Original image | Job |
|---|---|
| **The dessert pager** | Repeated rehearsal of the sweet-reward script teaches the summons; a cue activates it, and consumption may silence the current anticipation and receive excess credit. |
| **Borrowed confetti** | Dessert stands beneath a celebration and claims the sparkle supplied by people and occasion. |
| **The paper medal** | After effort, sugar prints a ceremonial token and claims it produced the accomplishment. |
| **The default conveyor** | Recurring visibility and convenience move an option into view without proving coordinated placement, anyone’s intent, powerlessness, or need. |
| **The menu pop-up** | A visible option activates a learned decision window; freedom is the window ceasing to demand attention, not clicking “no” forever. |
| **The velvet display case** | Rationing and special-day rules can make a small portion more symbolically precious than it was before. |
| **The label costume rack** | A new label can change ingredients without moving a core sweet item outside the line; behavioral role answers only a genuinely gray refined-savoury case. |
| **The customs desk for molecules** | Ingredient perfection recruits the reader into endless border checks; the Molecule Margin restores the operational line. |
| **A typo, not a deleted manuscript** | An accidental bite or lapse does not erase the reader’s understanding or dictate the next sentence. |
| **Removing a billboard from a road** | Leaving BAD SUGAR does not create a hole requiring replacement; the road and destination were there already. |
| **The two-tollbooth road** | The sugar standoff makes continuing appear costly and stopping appear costly. Once imagined deprivation is exposed as a false toll, only one real cost remains. |

None of these images may be presented as biomedical proof, a claim about a universal mechanism, or evidence of commercial intent. They compress attribution, attention, learning, and decision logic.

### 8. This behavior’s escape routes to foreclose

- **Cutting down forever:** acknowledge that reduction can be useful, then distinguish it from closing the daily question.
- **Weekends, birthdays, restaurants, holidays, and vacations:** show that the exception preserves the belief that special moments require a sweet upgrade.
- **Exercise-earned sugar:** return credit to movement, achievement, appetite, and rest.
- **Stress-only or illness-only sugar:** validate distress while refusing to make sugar its qualified treatment.
- **Liquid-only, dessert-only, or snack-only exceptions:** apply the BAD SUGAR definition consistently.
- **Natural, organic, homemade, honey, syrup, dark chocolate, low-sugar, or “healthier” versions:** acknowledge ingredient differences, but keep every core sweet drink, confection, dessert, baked sweet, and sweet snack inside the categorical line. Apply behavioral-role inquiry only to a genuinely gray refined-savoury snack.
- **Sugar-free consolation products:** leave them outside the required quit, but expose “this is what I must settle for now” as deprivation language.
- **A stash for after the challenge:** identify deferred reward and desire-preserving suppression.
- **Tapering as a compulsory medical necessity:** no accepted evidence supports a universal sugar-withdrawal requirement. The reader retains autonomy, but prolonged rationing can keep attention and anticipation central.
- **The perfect start date:** no New Year, Monday, birthday, or cleared cupboard is inherently meaningful. Readiness is conceptual, not calendrical.
- **Hidden-sugar purity:** invoke the Molecule Margin.
- **One lapse means collapse:** pre-script the thought and classify it as the deprivation method’s all-or-nothing interpretation.
- **“I got away with it, so planned exceptions are safe”:** forgiveness removes shame; it does not turn a lapse into evidence for a benefit.
- **Daily boundaries and resets as the only possible endpoint:** honour managed-truce relief while naming its continuing labour accurately.
- **“I am powerless around displays”:** recurring access can create a default lane, not a command. Its presence also does not prove the intent of the place where it appears.
- **“Fruit is sugar too”:** enforce the redefinition and prevent scope inflation.
- **Medical necessity used loosely:** distinguish prescribed glucose or clinical dietary requirements from a discretionary sugar hit, without second-guessing clinicians.

### 9. Strongest / most seductive scene to meet head-on

| Persona | Scene | Credit reassignment |
|---|---|---|
| **Sweet-Reward Reader** | A restaurant meal where the dessert menu is checked before the main course, followed by the first sweet bite. | Admit the taste; return leisure, appetite, service, and occasion to their real sources. The menu activated a learned anticipation before dessert quieted it. |
| **Restriction Veteran** | The first sweet item after weeks of denial, experienced as enormous relief. | The largest relief may be the end of restriction and self-surveillance. The deprivation method created the pressure that the bite appears to release. |
| **Context Carrier** | A late, stressful day ending at a petrol station, vending machine, workplace table, or birthday gathering. | Separate recurring access, fatigue, social belonging, and the need for a pause. Convenience explains selection; it supplies neither a unique benefit nor evidence of placement intent. |
| **Informed Household Translator** | Choosing a homemade or better-labelled sweet drink or treat as an expression of care. | Preserve the care. Product knowledge can improve ingredients without moving a core item outside BAD SUGAR or making sweetness the carrier of love. No caregiver shame. |
| **Managed-Truce Maintainer** | Holiday pie enjoyed within boundaries, followed by a practiced reset. | Concede that the system may provide genuine relief and structure. Then ask the correct question: does the reader want a workable truce, or freedom from having to negotiate and reset? |
| **Decision-Tax Escapee** | The imagined first dessert after a long restrictive period, with a stash waiting for the finish line. | The fantasy is compensation for deprivation. The desired relief is release from the rule—not evidence that dessert owns a missing pleasure. |

### 10. The moment of revelation to predict

These are future-paced possibilities, not guaranteed outcomes or efficacy claims.

| Persona | Ordinary proof-point |
|---|---|
| **Sweet-Reward Reader** | They notice a dessert menu and realize they did not scan it in advance or begin an internal argument. |
| **Restriction Veteran** | BAD SUGAR is present and the absence of a battle—not successful resistance—is what feels new. |
| **Context Carrier** | A late shift, birthday, or restaurant meal remains complete without a private sugar negotiation. |
| **Informed Household Translator** | A household choice is made calmly, without turning the label into a purity test or the child’s food into a moral verdict. |
| **Managed-Truce Maintainer** | A vacation or special occasion passes without boundary rehearsal, compensation, or a planned reset. |
| **Decision-Tax Escapee** | They realize an ordinary week has passed without budgeting, postponing, or debating dessert. |

The shared revelation is not “I resisted.” It is “There was nothing to settle.”

## Mantra seeds (§B2 — candidate frozen wordings)

The master plan may reject a candidate before freezing, but it must not paraphrase any wording it accepts.

| Archetype | Candidate frozen wording | Belief installed |
|---|---|---|
| **Redefinition token** | `BAD SUGAR` | The book targets a defined subset with a categorical sweet core and a behavior-resolved savoury edge—not food or carbohydrate as a whole. |
| **Entry promise** | `You can test whether BAD SUGAR owns any special or irreplaceable pleasure, without denying pleasant taste or giving up your right to choose.` | Reading is an autonomous investigation that concedes sensation while testing claims of uniqueness and necessity. |
| **Promise triad** | `without deprivation, without battle, and without a lifetime of rules` | The intended outcome differs from suppression and managed truce. |
| **Trap-namer** | `the sugar trap` | Stopping is an escape from a learned loop. |
| **Illusion-namer** | `a special pleasure or rescue` | The disputed benefit is unique ownership and necessity, not the existence of taste. |
| **Sensory definition** | `a nagging, bargaining, slightly urgent sense that this moment is missing something` | The craving experience is recognized without being called withdrawal or personified as an attacker. |
| **Stakes phrase** | `every ordinary day` | The loop and the freedom both live mainly in unremarkable moments. |
| **Cost formula** | `anticipating, bargaining, and starting over` | The primary cost is recurring decision labour. |
| **Fact-assertion frame** | `The crucial distinction is this:` | Core conceptual distinctions arrive clearly while scientific claims retain their grades. |
| **Named anti-method** | `the deprivation method` | Past failure belongs to behavior control that preserved the lost-reward belief, not to weak character. |
| **Named conflict model** | `the sugar standoff` | Continuing seems costly while stopping seems like deprivation; removing the imagined loss ends the conflict. |
| **Named positive authority** | `the Ordinary Eating Compass` | A temporary learning lens returns authority to ordinary nourishment and actual pleasure, then naturally falls out of use. |
| **Ease-operator** | `When the benefit loses its credit, the battle loses its job.` | The work is belief correction, not resistance. |
| **Terminal mantra** | `WHAT A RELIEF — THE SUGAR TRAP IS OVER. I'M FREE!` | A sugar thought becomes a cue for relief rather than suppression. |
| **Claim block** | `You can close the daily sugar debate without policing every molecule, fighting yourself, or treating one accidental bite as failure.` | The complete promise: decision quiet, no inner battle, and a non-catastrophic margin for error. |

### Mechanism characters

These are named mechanisms, not inner creatures:

- **`the sweet-reward script`** — the learned proposition that effort, distress, meals, or celebrations require BAD SUGAR; repeated rehearsal gives that proposition anticipatory force.
- **`the open loop`** — anticipatory attention and bargaining once the learned script has been activated.
- **`the Demand Machine`** — the documented commercial pattern of formulation, testing, packaging, promotion, and marketing used by specific historical actors to improve appeal or demand. Recurring environmental availability is a separate observed context, not evidence that a generic access point belongs to the machine.

None may be described as a beast, parasite, voice with independent agency, neurological entity established by the evidence, or proof of universal commercial coordination.

### Temporary learning lenses of the Ordinary Eating Compass

The following are selective teaching devices, not tracking rituals, lifelong practices, or conditions of success:

- **`the meal-or-hit check`** — used only for a genuinely gray refined-savoury snack: “Is this borderline item serving ordinary eating, or functioning as a discretionary reward, rescue, graze, or automatic nibble?” It cannot exempt a categorical core item.
- **`the pleasure-source audit`** — used on selected cherished or seductive scenes while the belief is being corrected: identify which parts belong to pleasant taste, people, rest, ritual, accomplishment, hunger, or relief; deny nothing and misassign nothing.
- **`the Molecule Margin`** — invoked when an actual accident, incidental ingredient, or honest ambiguity occurs, so the reader does not convert it into panic, failure, or permission creep.

These lenses succeed by becoming unnecessary. They are not scheduled, scored, or run at every meal. The pleasure-source audit retires when credit returns naturally to its sources; the meal-or-hit check retires when the savoury edge is obvious; the Molecule Margin remains a quiet interpretive principle, not a reason to inspect every ingredient.

## How to use the personal experiences

### Outcome-language firewall

These labels describe different accounts. They are not a universal staircase, clinical categories, or evidence that every reader will progress from one to another.

| State | Required wording | Prohibited inference |
|---|---|---|
| **SUPPRESSION** | Behavior was reduced or absent while desire, battle, dreams, bargaining, or a future stash remained active. | Do not call it freedom, withdrawal, or proof that abstinence universally backfires. |
| **MANAGED TRUCE** | Real relief coexisted with daily actions, boundaries, exceptions, and resets. | Do not dismiss the relief, call the person a failure, or present the account as desire absence or program efficacy. |
| **EARLY SIGNALS** | A short intervention produced better choices, a perceived craving shift, campaign receptivity, or anticipated future change. | Do not call it durable freedom or observed long-term behavior. |
| **DESIRE-LEVEL FREEDOM** | One author self-reported not missing desserts, less decision labour, and a year without added sugar across major holidays. | Do not generalize efficacy, probability, mechanism, universal ease, or a moderation result. This remains one bounded self-report. |

### Experience-to-belief mapping

| Account | Structural use | Belief or distinction served |
|---|---|---|
| **Dessert-menu anticipation and return for taste** (S-004, S-009) | Early justification menu and strongest taste scene. | Lets the reader hear their own mind before pleasant taste is separated from unique life value. |
| **Reward, deserving, weakness, stress, sadness, boredom, loneliness, and social prompting** (S-022) | Benefit demolitions and context sections. | Shows the range of jobs assigned to sugar without asserting a single causal mechanism. |
| **Six-week battle followed by two weeks of better choices** (S-020) | Anti-method and evidence-language sections. | An early signal after suppression; not durable freedom. |
| **Weeks of doing well followed by a lapse and daily consumption** (S-020) | Lapse inoculation. | Exposes lapse-collapse interpretation without teaching that one lapse must cause collapse. |
| **Displays, workplace food, vending, time pressure, and travel access** (S-020, S-022) | Default-conveyor and context material only. | Recurring availability can increase visibility and convenience without removing agency. These accounts do not establish design or intent at any location and do not supply the Demand Machine’s optimization evidence. |
| **Knowledge changed anticipated behavior; one-less-spoon messaging felt achievable** (S-007, S-012) | Knowledge and myths material. | Supports receptivity and anticipated change only. |
| **Caregiver changed a child’s drinks and checked labels** (S-010) | Household safety and redefinition material. | Illustrates household translation, not the caregiver’s own abstinence or freedom. |
| **Product distrust plus a homemade-drink substitution** (S-011) | Label-costume escape route. | Shows why a change in source or label must not be coded automatically as sugar freedom. |
| **Soda described with addiction language** (S-008) | Identity-excuse and science-firewall material. | Validates felt compulsion while refusing to turn analogy into diagnosis. |
| **Relief paired with daily management, boundaries, and resets; the same account separately reports keeping weight off, more or less, for 15-plus years** (S-021) | Managed-truce contrast and anti-shame material. | Honours genuine relief while distinguishing it from desire-level freedom and commercial-program efficacy. |
| **Earlier dessert-free attempt with dreams and a stash for later** (S-023) | Suppression contrast within the embedded testimonial. | Shows behavior absence with desire preserved in one person’s earlier attempt. |
| **Later year without added sugar, no reported missing of desserts, less decision tax, and ordinary passage through holidays** (S-023) | The sole long-form desire-level-freedom testimony. | Illustrates possibility, not probability or proof of method. |

### Emotional notes

- Never tell a reader that sweet taste was imaginary. The sharper claim is that the product received far more credit than the sensation can support.
- Treat suppression as an understandable product of the deprivation method, not stupidity.
- Treat managed truce as a legitimate chosen outcome with real relief. The book offers a different target; it does not seize the right to rename another person’s experience.
- Early signals create curiosity, not certainty.
- The desire-level account supplies possibility only. Its evidentiary limitation must appear beside it, not in distant endnotes.
- Keep caregiver material free of guilt, purity, and judgment about children’s bodies.
- When anger appears, direct it toward documented commercial optimization and the deprivation story—not toward the reader, family members, clinicians, retailers, employers, workplaces, access points, hospitality, or people who still eat BAD SUGAR.
- The emotional destination is quiet relief, not dietary pride, superiority, disgust toward other people, or a “clean eater” identity.
- Never use weight change as the emotional payoff.
- An accidental bite receives calm interpretation. A planned return receives honest curiosity, not punishment.

### “This is exactly me” lines

These are original ventriloquism grounded in the packets. They must not be presented as verbatim participant quotations.

- **Early justification menu:** “I check dessert before I have even chosen dinner.”
- **Restriction material:** “If I say no, it only gets louder.”
- **Lapse inoculation:** “I did well for weeks; then one thing became something every day.”
- **Context material:** “At work, at the till, or on the road, it is simply the next thing in front of me.”
- **Household material:** “I know how to read the label. I still need a line I can live with.”
- **Managed-truce contrast:** “My plan works, but it never clocks off.”
- **Suppression contrast:** “I am not eating it, but I am saving it for the person I will be when this is over.”
- **Desire-level target:** “I don’t want a perfect streak. I want the debate to stop.”
- **Revelation future-pace:** “Nothing was forbidden. It simply did not need a decision.”

### Long-form embedded testimonial candidate

**Slot title:** *In his own words — when the dessert debate went quiet*

Use only the S-023 author, anonymized unless a cleared name is available. Build the account in original prose from these verified elements:

1. Before the later change, he reported spending at least two hours each week debating dessert.
2. An earlier four-month dessert-free attempt involved nighttime dreams and a stash kept for after the diet. Label this **SUPPRESSION**.
3. In the later account, he reported twelve months without added sugar across birthdays and major holidays.
4. He reported not missing desserts, feeling better physically and mentally, and removing dessert from his active decision catalog while not describing it as metaphysically forbidden. Label this **ONE SELF-REPORT OF DESIRE-LEVEL FREEDOM**.
5. He reported fruit tasting sweeter. Keep this explicitly subjective and do not convert it into a universal taste-reset claim.

The arc is a **method-conflict arc**—desire-preserving restriction versus a later change in how dessert was valued—not an invented conflict with a clinician or authority figure. Do not add dialogue, causes, medical outcomes, weight changes, program details, or sensory facts absent from the packet.

Place a limitation box beside the testimony:

> This is one person’s self-report, not a trial and not evidence that the book’s method works for everyone. It illustrates a possible distinction between not eating sugar and no longer missing it.

No second account may be framed as desire-level freedom. Other accounts remain suppression, managed truce, early signal, anticipated behavior, caregiver behavior, or contextual evidence.

## Fork positions (style guide §4) for this book

| Fork | Position | Rationale |
|---|---|---|
| **Fork 1 — inner monster** | Externalize **the learned and repeatedly rehearsed sweet-reward script**, **the sugar trap**, and the narrowly evidenced **Demand Machine**. Never personify craving as an inner creature. | The reader’s experience is understood and reclassified, not fought. The evidence does not justify inventing a physical sugar entity or attributing anticipation universally to a dose. |
| **Fork 2 — abstinence or autonomy** | Autonomy-led practical total freedom inside the BAD SUGAR line: no planned doses, no command, no molecular-purity vow. | Moderation remains available, and managed truce is respected, but repeated exceptions preserve the benefit question. The prose lets the reader choose to close it. |
| **Fork 3 — science weight** | Light, graded science in the prose; full claim-and-limits treatment in an appendix. | Human sugar-addiction and withdrawal claims are unsettled. Science must expose distinctions without supplying fear or counterfeit certainty. |
| **Fork 4 — villain** | The external villain is the documented side of **the Demand Machine**; the internalized wrong method is **the deprivation method**. Recurring environmental availability remains a separate context observation. | Specific historical formulation, testing, and marketing optimization deserve scrutiny. S-020/S-022 do not establish intent by retailers, workplaces, or generic access points, and treatment itself is not the villain. |
| **Fork 5 — void or baseline** | Natural baseline, with **the Ordinary Eating Compass** and its instruments used only as temporary teaching scaffolding. No replacement system remains. | BAD SUGAR is a bounded consumptive subset. Ordinary eating, celebration, comfort, rest, and connection remain; the Compass fulfils its purpose by becoming unnecessary rather than creating lifelong vigilance. |
===== END PERMITTED INPUT 4/8: production-books/quit-sugar/framing.md =====

===== BEGIN PERMITTED INPUT 5/8: production-books/quit-sugar/research/lived-experience.md =====
# Lived Experience — Quit Sugar

Synthesize accepted source packets only. The persona map is functional: each persona serves one reader pattern or outcome role rather than duplicating the same people as separate context characters.

## Persona map

| Persona ID | Function served / defining context | Applicable banks | Source IDs |
|---|---|---|---|
| P-01 | Pleasure/taste/reward adult: sugar or sweet drinks are described through taste, dessert, reward, energy, or joy; one soda account uses addiction language for a felt pull, not a diagnosis or mechanism. | 1, 2, 3, 4, 9 | S-004, S-008, S-009, S-022 |
| P-02 | Restriction–backfire adult: denial becomes a battle, and a lapse can be interpreted as collapse. | 2, 3, 5, 10 | S-020 |
| P-03 | Context-and-access adult: consumption is linked with emotion, social expectation, convenience, time pressure, and availability. | 3, 4, 5, 9 | S-020, S-022 |
| P-04 | Belief-shifting and label-aware adult: knowledge, product distrust, or an achievable step changes anticipated behavior or household choices. | 2, 5, 10 | S-007, S-011, S-012 |
| P-05 | Caregiver/household translator: applies beverage guidance to a child’s drinks and labels. | 5 | S-010 |
| P-06 | Managed-truce maintainer: reports substantial relief while still using daily management, boundaries, and resets. | 2, 3, 5, 6, 9, 10 | S-021 |
| P-07 | Desire-level freedom reporter: reports not missing desserts, reduced decision tax, a changed decision catalog, and ordinary passage through holidays. | 2, 3, 4, 5, 6, 10 | S-023 |

## Interpretive distinctions

These are analytic labels for different packet accounts, not a universal staircase.

- **SUPPRESSION:** behavior is reduced or removed while desire remains active. S-020 includes denial, an initial battle, and lapse-collapse; S-023 describes an earlier four-month attempt that left dreams and a stash for later. Sources: S-020#E-001, S-020#E-002, S-020#E-003, S-023#E-004.
- **MANAGED TRUCE:** relief is real, but maintaining it still involves daily work, boundaries, and resets. This is the shape of S-021, not desire-level freedom and not evidence of general efficacy. Sources: S-021#E-002, S-021#E-004, S-021#E-005, S-021#E-006.
- **EARLY SIGNALS:** a short-intervention shift, perceived craving change, or anticipated future behavior. These do not establish durable freedom. Sources: S-007#E-001, S-020#E-002, S-020#E-008.
- **DESIRE-LEVEL FREEDOM:** one author’s self-report of no longer missing desserts, spending less mental effort deciding, and removing desserts from the decision catalog across a year. This remains one self-report. Sources: S-023#E-001, S-023#E-002, S-023#E-003, S-023#E-006.

## Outcome-tier ledger

| Outcome tier | Packet signal | What it supports | What it does not support |
|---|---|---|---|
| Caregiver behavior | P-05; S-010#E-001 | Reported changes to a child’s drinks and label checking. | The caregiver’s own abstinence or freedom. |
| Campaign receptivity | P-04; S-012#E-001 | One campaign example felt achievable. | Implementation or sustained change. |
| Anticipated behavior | P-04; S-007#E-001 | Knowledge changed one participant’s expectation about returning to former favourites. | Observed long-term behavior. |
| Short-intervention shift | P-02; S-020#E-002, S-020#E-008 | Better choices or a perceived craving shift during a short study. | Durable recovery. |
| Daily management / managed truce | P-06; S-021#E-002, S-021#E-005, S-021#E-006 | Relief coexisting with continuing maintenance. | Commercial-program efficacy or desire absence. |
| Durable self-reported freedom | P-07; S-023#E-001, S-023#E-002, S-023#E-006 | One account of a year without added sugar and reduced decision burden. | General efficacy or a universal result. |

## Bank 1 — Justification Inventory

- [Bank 1] A small qualitative interview study records pleasure, routine, boredom, environment, social access, hunger, and perceived control as distinct reported reasons for continuing; one participant said, “There’s always room for dessert. If I go out for dinner, I have to look at the dessert menu before I order my mains.” This is anticipatory dessert attention, not a universal requirement. — Persona IDs: P-01 — Source IDs: S-004#E-001

- [Bank 1] A student described returning to soft drinks after trying to reduce them because of taste: “I tried to cut down on soft drinks, but I start drinking them again for the taste.” — Persona IDs: P-01 — Source IDs: S-009#E-001

- [Bank 1] In one Middle Eastern Canadian community, participants linked sweets with feeling rewarded or deserving after effort, and one participant linked feeling weak with a sugar craving. These are participant beliefs, not physiological findings. — Persona IDs: P-01 — Source IDs: S-022#E-005

- [Bank 1] Nell contrasted foods expected to bring joy with later physical and emotional misery. This is a commercial wellness testimonial and a lived comparison, not efficacy evidence. — Persona IDs: P-06 — Source IDs: S-021#E-008

- [Bank 1] One participant ate an extra slice after tennis and afternoon tea despite not being hungry, attributing the choice to taste. — Persona IDs: P-01, P-03 — Source IDs: S-020#E-005

- [Bank 1] A public-housing resident used addiction language for soda: “people get addicted to drugs, some of us are addicted to soda.” The phrase captures reported compulsion and analogy, not a clinical diagnosis or mechanism; it is grouped with P-01 as a sweet-drink appeal account, not a separate explanatory layer. — Persona IDs: P-01 — Source IDs: S-008#E-001

## Bank 2 — Belief Map

- [Bank 2] **Keystone belief:** sugar or sweetened products appear to offer taste, pleasure, reward, or joy that would be lost on stopping, making return seem worth the cost. This is a cross-source synthesis of reported beliefs, not a universal truth; the managed-truce account is kept separate rather than folded into this belief. — Persona IDs: P-01, P-03, P-06 — Source IDs: S-004#E-001, S-009#E-001, S-021#E-008, S-022#E-005

- [Bank 2] One participant held a deprivation/backfire belief: “If I deny myself something it turns up somewhere else and worse.” The packet explicitly limits this to one participant. — Persona IDs: P-02 — Source IDs: S-020#E-001

- [Bank 2] Nell described earlier dieting as not addressing underlying cravings and connected perceived lack of willpower with shame. This frames the failed attempt as a character judgment rather than establishing a universal cause. — Persona IDs: P-06 — Source IDs: S-021#E-003

- [Bank 2] The available identity language is self-description or self-judgment rather than a validated clinical identity: soda was described through addiction language, while dieting failure was associated with lack of willpower and shame. Neither establishes addiction as the correct explanation. — Persona IDs: P-01, P-06 — Source IDs: S-008#E-001, S-021#E-003

- [Bank 2] One shopper explained avoiding commercial sweet beverages through distrust of their ingredients: “I don’t really buy any (drinks). I believe they are just made of sugar and coloring…” The associated homemade-drink substitution must not be coded as sugar abstinence. — Persona IDs: P-04 — Source IDs: S-011#E-001

- [Bank 2] **EARLY / ANTICIPATED SIGNAL:** At week 12, one participant said, “but now that I know I definitely don’t think I’ll go back to most of them.” This is anticipated future behavior after knowledge, not observed long-term abstinence. — Persona IDs: P-04 — Source IDs: S-007#E-001

- [Bank 2] **CAMPAIGN RECEPTIVITY:** One food-bank client found a one-less-spoon example personally achievable: “it did make me think well, I could actually do that” — a receptivity signal, not implementation. — Persona IDs: P-04 — Source IDs: S-012#E-001

- [Bank 2] **SUPPRESSION:** S-020 records denial as a battle and a lapse that expanded into daily consumption; S-023 records an earlier four-month attempt in which desire remained active. These accounts show behavior control with desire intact, not universal failure or withdrawal. — Persona IDs: P-02, P-07 — Source IDs: S-020#E-001, S-020#E-002, S-020#E-003, S-023#E-004.

- [Bank 2] **MANAGED TRUCE:** S-021 combines a strong relief metaphor with a report that Nell kept weight off, more or less, for “15 plus years,” and a separate description of daily actions to keep cravings at bay. Relief and ongoing management coexist; this is not desire-level freedom. — Persona IDs: P-06 — Source IDs: S-021#E-001, S-021#E-002

- [Bank 2] **DESIRE-LEVEL FREEDOM:** In the later account, S-023 reports not missing desserts and describes removing them from the decision catalog while leaving future desserts theoretically not forbidden. This is one self-report, not a general moderation result. — Persona IDs: P-07 — Source IDs: S-023#E-001, S-023#E-006

## Bank 3 — Lived-Experience Bank

- [Bank 3] A failed reduction attempt returned to taste: the student tried to cut down on soft drinks and then resumed them. — Persona IDs: P-01 — Source IDs: S-009#E-001

- [Bank 3] A participant described the first six weeks of reduction as a battle before reporting better choices in the final two weeks. The endpoint was eight weeks, not durable freedom. — Persona IDs: P-02 — Source IDs: S-020#E-002

- [Bank 3] Another participant described doing well for weeks before one lapse became a week in which there was something every day. This is one lapse account, not a rule that one lapse must become collapse. — Persona IDs: P-02 — Source IDs: S-020#E-003

- [Bank 3] Before changing dessert intake, the S-023 author reported spending at least two hours each week debating whether to eat dessert. — Persona IDs: P-07 — Source IDs: S-023#E-003

- [Bank 3] The earlier four-month dessert-free attempt included nighttime dreams and a stash intended for after the diet, indicating desire-preserving abstinence in that account. — Persona IDs: P-07 — Source IDs: S-023#E-004

- [Bank 3] Participants described café displays, supermarket availability, workplace food, free leftovers, and vending access as ordinary consumption contexts. The study concerns indulgent foods and beverages broadly, not sugar alone or industry intent. — Persona IDs: P-03 — Source IDs: S-020#E-004

- [Bank 3] Stress, staying late at work, sadness, and birthday expectations were described as situations in which resistance weakened. These are participant accounts from a short intervention, not general trigger prevalence. — Persona IDs: P-03 — Source IDs: S-020#E-006

- [Bank 3] Participants in one community associated sweetened products with nervousness or stress, sadness, boredom, loneliness, and filling an emotional void. These are situational descriptions, not causal evidence. — Persona IDs: P-03 — Source IDs: S-022#E-002

- [Bank 3] Gas-station sweets, vending machines, lack of time, late driving, and not wanting to prepare food were described as physical or constraint contexts. — Persona IDs: P-03 — Source IDs: S-022#E-004

- [Bank 3] Nell identified vacations, illness, alcohol, restaurant outings, and special occasions as situations requiring extra management. This is one commercial-testimonial account, not a general trigger list. — Persona IDs: P-06 — Source IDs: S-021#E-004

## Bank 4 — Special-Moments Inventory

- [Bank 4] One participant described dessert as socially prompted at a restaurant: “It’s a social thing, we were at the restaurant and someone with us ordered dessert.” — Persona IDs: P-03 — Source IDs: S-022#E-001

- [Bank 4] Birthdays, visiting or receiving friends and relatives, and shared meals were identified as social contexts for sweetened-product consumption in one community. — Persona IDs: P-03 — Source IDs: S-022#E-003

- [Bank 4] One participant reported eating an extra slice after tennis and afternoon tea despite not being hungry because of taste, showing how an apparently complete occasion could still be credited with an additional sensory payoff. — Persona IDs: P-01, P-03 — Source IDs: S-020#E-005

- [Bank 4] One small interview study included dessert-menu attention around dinner as a pleasure and routine context. It does not establish that dessert is necessary before a meal. — Persona IDs: P-01 — Source IDs: S-004#E-001

- [Bank 4] Holiday and special-event settings were described in one account as occasions involving pie and sugary snacks, with extra management needed around looser periods. — Persona IDs: P-06 — Source IDs: S-021#E-007

- [Bank 4] The S-023 author reported passing birthdays, Halloween, Thanksgiving, Christmas, and Valentine’s Day during a year without added sugar. This is a self-reported freedom account, not evidence that social occasions are easy for everyone. — Persona IDs: P-07 — Source IDs: S-023#E-002

## Bank 5 — Escape-Route Inventory

- [Bank 5] Denial was described as making the wanted food return elsewhere and worse. This is a participant’s backfire belief, not a general rule against abstinence. — Persona IDs: P-02 — Source IDs: S-020#E-001

- [Bank 5] A participant’s lapse account moved from weeks of doing well to daily indulgence after one lapse. The evidence supports documenting lapse-collapse thinking, not teaching catastrophic lapse expectations. — Persona IDs: P-02 — Source IDs: S-020#E-003

- [Bank 5] Nell described vacations, illness, alcohol, restaurants, and special occasions as periods requiring extra management, then described returning to her usual plan at the next meal or next day. This is one person’s reset practice, not general moderation evidence. — Persona IDs: P-06 — Source IDs: S-021#E-004, S-021#E-005

- [Bank 5] The same commercial account included personal boundaries around checkout candy and packaged trigger foods. These boundaries belong to one person’s maintenance practice and are not elevated into a universal trigger-management rule. — Persona IDs: P-06 — Source IDs: S-021#E-006

- [Bank 5] The earlier S-023 attempt preserved an exception-for-later route through a stash of sweets after the diet. This illustrates desire remaining active, not a universal feature of abstinence. — Persona IDs: P-07 — Source IDs: S-023#E-004

- [Bank 5] **CAREGIVER BEHAVIOR:** After nutrition advice, one caregiver reported giving a child more water, changing the child’s drinks, and checking sugar labels. This is household behavior, not the caregiver’s own freedom testimony. — Persona IDs: P-05 — Source IDs: S-010#E-001

- [Bank 5] **CAMPAIGN RECEPTIVITY:** One food-bank client considered a one-less-spoon example achievable. The source supports receptivity only; it does not support implementation or durability. — Persona IDs: P-04 — Source IDs: S-012#E-001

- [Bank 5] **ANTICIPATED BEHAVIOR:** New knowledge led one week-12 participant to expect less return to formerly favourite foods. The source omits post-study behavior and does not establish long-term change. — Persona IDs: P-04 — Source IDs: S-007#E-001

- [Bank 5] Product distrust led one shopper to avoid purchased sweet beverages and report a homemade-drink substitution, but the packet warns that the substitute may contain unrecognised sugar. — Persona IDs: P-04 — Source IDs: S-011#E-001

## Bank 6 — Analogy Bank

Excluded from this bank: addiction-as-explanation, one-chink floodgate, false-emergency battery, and unopened-sleeve rule.

- [Bank 6] Release-from-jail image: “I feel like I've been let out of jail.” — Origin: SOURCED | Job: name the felt relief of obsessive food thoughts becoming less dominant. Limits: one named interviewee’s metaphor; not a clinical claim or universal outcome. — Persona IDs: P-06 — Source IDs: S-021#E-001

- [Bank 6] Decision-catalog image: “eliminate them from my decision catalog” — Origin: SOURCED | Job: expose repeated decision tax and distinguish removing an option from declaring it forbidden. Limits: one author’s phrasing; not a general moderation result. — Persona IDs: P-07 — Source IDs: S-023#E-006

- [Bank 6] Default-lane image: repeated cafés, vending access, supermarkets, and time constraints can be pictured as a non-intentional default lane that appears in the path before deliberate choice. — Origin: INVENTED | Job: externalize access and decision friction without implying powerlessness, craving personification, industry intent, or a trigger-management rule. — Persona IDs: P-03 — Source IDs: S-020#E-004, S-022#E-004

## Bank 9 — Community Lexicon

- [Bank 9] “cash wrap food” names checkout-line candy in one named interview. Frequency / context: single participant’s phrase; not a clinical category or universal term. — Persona IDs: P-06 — Source IDs: S-021#E-006

- [Bank 9] “carb window” names one participant’s phrase for a café-display context. Frequency / context: single participant; the study’s personalisable intervention label does not establish compartmentalization or broader community usage. — Persona IDs: P-03 — Source IDs: S-020#E-007

- [Bank 9] “eat our emotions” and “salt person” preserve participant phrasing about emotional eating and food preference. Frequency / context: one community study; neither is a general native-language claim. — Persona IDs: P-03 — Source IDs: S-022#E-006

- [Bank 9] “sugar craving” appears in a participant’s account of feeling weak and wanting sugar. Frequency / context: participant phrasing and belief, not physiological evidence. — Persona IDs: P-01 — Source IDs: S-022#E-005

- [Bank 9] “people get addicted to drugs, some of us are addicted to soda.” Frequency / context: one anonymous resident’s analogy for soda craving; not a clinical diagnosis or explanatory mechanism. — Persona IDs: P-01 — Source IDs: S-008#E-001

## Bank 10 — Freedom Testimonies

- [Bank 10] **SUPPRESSION, NOT FREEDOM:** In the earlier four-month dessert-free attempt, the S-023 author reported nighttime dreams and a stash for later. Desire remained active even while behavior was restricted. — Persona IDs: P-07 — Source IDs: S-023#E-004

- [Bank 10] **SHORT-INTERVENTION SIGNAL:** One S-020 participant described the first six weeks as a battle and then reported better choices during the final two weeks. This is an eight-week endpoint, not durable freedom. — Persona IDs: P-02 — Source IDs: S-020#E-002

- [Bank 10] **PERCEIVED EARLY SIGNAL:** One participant associated stronger resolve with noticing a shift in cravings. The packet limits this to one perception and does not establish durable recovery. — Persona IDs: P-03 — Source IDs: S-020#E-008

- [Bank 10] **ANTICIPATED BEHAVIOR:** At week 12, one participant expected not to return to most formerly favourite foods after gaining new knowledge. This is an expectation about future behavior, not an observed outcome. — Persona IDs: P-04 — Source IDs: S-007#E-001

- [Bank 10] **MANAGED TRUCE:** Nell said, “I feel like I've been let out of jail.” The relief is paired in the same account with daily actions to keep sugar cravings at bay, personal boundaries, and resets after exceptions. — Persona IDs: P-06 — Source IDs: S-021#E-001, S-021#E-002, S-021#E-005, S-021#E-006

- [Bank 10] **DESIRE-LEVEL FREEDOM, ONE SELF-REPORT:** The S-023 author wrote, “Instead, I found myself not missing desserts. And really, I felt better physically and mentally.” He also reported twelve months without added sugar, including major holidays. — Persona IDs: P-07 — Source IDs: S-023#E-001, S-023#E-002

- [Bank 10] **DESIRE-LEVEL FREEDOM, DECISION-TAX SHIFT:** The same author contrasted at least two hours each week of debating dessert with removing desserts from his decision catalog while not describing them as permanently forbidden. — Persona IDs: P-07 — Source IDs: S-023#E-003, S-023#E-006

- [Bank 10] The S-023 account also included a subjective report that fruit tasted sweeter after the change. This is a personal sensory report, not evidence of a general taste-bud or physiological reset. — Persona IDs: P-07 — Source IDs: S-023#E-005
===== END PERMITTED INPUT 5/8: production-books/quit-sugar/research/lived-experience.md =====

===== BEGIN PERMITTED INPUT 6/8: production-books/quit-sugar/research/scientific-evidence.md =====
# Scientific Evidence — Quit Sugar

Synthesize accepted source packets only. Grades apply to the claim as written. Human testimony remains lived evidence; commercial testimony is not efficacy evidence. Scientific persona tags are thematic relevance tags wherever they extend beyond the lived-experience persona table; they do not create additional lived-experience personas or alter the seven-persona functional map.

## Bank 7 — Mechanism & Science Bank

- [Bank 7] [CONTESTED] A broad claim that ordinary human sugar consumption constitutes an established addiction remains unsettled: the critical review states, “We find little evidence to support sugar addiction in humans.” Human imaging and intervention findings do not by themselves demonstrate clinical addiction. — Persona IDs: ALL — Source IDs: S-001#E-001, S-005#E-001, S-006#E-001 — Limits / disagreement: S-001 emphasizes sparse human evidence and deprivation-shaped rodent work; S-005 found no whole-cohort sucrose-versus-sucralose BOLD difference; S-006 combined fat and sugar and did not study clinical compulsion.

- [Bank 7] [MIXED] Qualitative evidence supports multiple reported maintenance pathways—taste, pleasure, routine, boredom, environment, social access, hunger, and perceived control—but does not quantify their causal importance or establish a single human craving loop. — Persona IDs: P-01, P-03 — Source IDs: S-004#E-001, S-009#E-001 — Limits / disagreement: S-004 involved seven self-selected adults and a small gymnema intervention; S-009 involved nineteen students at one Saudi university and did not test solutions or durable cessation.

- [Bank 7] [MIXED] Repeated exposure can alter food-response or associative-learning measures in some experimental settings, but the packet set cannot assign such effects to sugar alone or equate them with escalating compulsion. — Persona IDs: ALL — Source IDs: S-006#E-001, S-019#E-001 — Limits / disagreement: S-006 changed fat and sugar together, used a small normal-weight sample, and had a comparator differing in protein; S-019 found greater intake and weight gain on an ultra-processed diet but stated that the responsible feature was unknown.

- [Bank 7] [MIXED] A sweet-intake neural circuit has causal evidence in mice, while human translation remains limited; a separate human trial found, “We did not observe significant differences in BOLD signal to any food cue contrasts” in the whole cohort. — Persona IDs: P-01, P-03 — Source IDs: S-003#E-001, S-005#E-001 — Limits / disagreement: S-003’s causal manipulation was in mice and human imaging did not establish the complete causal circuit; S-005 found prespecified BMI/sex interactions despite no whole-cohort effect.

- [Bank 7] [MIXED] Substantial dietary fructose or sugar-sweetened-beverage exposure is reviewed as promoting hepatic insulin resistance through several pathways, but this does not establish that fruit, every carbohydrate, occasional sugar, or ordinary craving has the same effect. — Persona IDs: ALL — Source IDs: S-002#E-001, S-019#E-001 — Limits / disagreement: S-002 includes unusually high or hypercaloric exposures and is not evidence for every sugar source; S-019’s controlled ultra-processed-food trial did not isolate fructose or sugar as the responsible feature.

- [Bank 7] [MIXED] Sweet taste and palatability can affect reported pleasure or food-response measures, but those effects are not equivalent to addiction: blocking sweet taste reduced reported pleasure in a small qualitative intervention, while the sucrose-versus-sucralose trial found no whole-cohort food-cue BOLD difference. — Persona IDs: P-01 — Source IDs: S-004#E-001, S-005#E-001 — Limits / disagreement: S-004 did not establish ordinary craving mechanisms or quitting efficacy; S-005’s subgroup interactions do not create a universal sugar-specific effect.

- [Bank 7] [MIXED] Human reports of battle, daily craving management, or difficulty after restriction establish subjective difficulty in particular accounts, not physiological withdrawal or restlessness. — Persona IDs: P-02, P-06 — Source IDs: S-001#E-001, S-020#E-002, S-021#E-002 — Limits / disagreement: S-001 warns that rodent withdrawal and binge findings arose largely from intermittent access and deprivation; S-020 is a short qualitative process evaluation; S-021 is one commercial wellness testimonial and does not establish withdrawal.

## Bank 8 — Villain Dossier

- [Bank 8] [SUPPORTED] Historical records document product-level demand optimization: an RJR report described formulation through taste, smell, appearance, flavour libraries, and ingredient combinations, including “The ideal, Winter says, is "to leave people wanting more."”; a documentary analysis reported that new children’s drink flavours were developed through numerous product tests on children. — Persona IDs: P-01, P-03, P-05 — Source IDs: S-013#E-001, S-018#E-001 — Limits / disagreement: These are documented historical practices and objectives; they do not establish addiction, deception, clinical harm, current universal practice, or actual overeating.

- [Bank 8] [SUPPORTED] Youth-directed food marketing was documented as integrated across television, packaging, in-store, Internet, event, and cross-promotional channels, while company research reported children’s role in purchase decisions and marketing’s promotion of “pester power.” — Persona IDs: P-05 — Source IDs: S-015#E-001, S-016#E-001 — Limits / disagreement: The FTC reports document expenditures, techniques, and company research; they do not establish a universal causal effect on obesity or adult consumption.

- [Bank 8] [MIXED] Historical tobacco ownership was associated with a higher likelihood that sampled foods were classified as fat-and-sodium hyper-palatable, and related documentary evidence describes tobacco-owned children’s drink development practices. — Persona IDs: P-01, P-05 — Source IDs: S-017#E-001, S-018#E-001 — Limits / disagreement: S-017 reports a historical ownership association among sampled products, not design intent, addiction, absolute risk, sugar-specific effects, or current company practice; S-018 does not establish that product testing caused craving or overeating.

- [Bank 8] [MIXED] Availability and convenience can place sweet or indulgent foods in repeated paths through cafés, supermarkets, workplaces, vending machines, gas stations, and time-constrained travel. — Persona IDs: P-01, P-03 — Source IDs: S-020#E-004, S-022#E-004 — Limits / disagreement: S-020 and S-022 are qualitative context evidence, not causal access studies; these observations do not establish industry intent, powerlessness, or that social celebrations were engineered demand.

- [Bank 8] [SUPPORTED] An archival industry letter documents a publication-payment condition: “the remainder to be delivered when you notify me that the manuscript has been accepted for publication.” This supports only that the remaining payment was tied to manuscript acceptance; it does not establish fabricated results, concealed funding, or altered conclusions. — Persona IDs: P-04 — Source IDs: S-014#E-001 — Limits / disagreement: S-014 is one letter and supports no inference beyond the documented payment condition.
===== END PERMITTED INPUT 6/8: production-books/quit-sugar/research/scientific-evidence.md =====

===== BEGIN PERMITTED INPUT 7/8: calibration/runs/run-014/planning/master-plan-r1.md =====
# Master Plan — *The Sugar Debate Is Over*

## 1. Book core

| ID | Locked decision |
|---|---|
| **BC-01 — Target** | Compulsive consumption of refined or added sugar and junk-carbohydrate products inside the defined **BAD SUGAR** line: the anticipation, bargaining, reward, rescue, grazing, and restarting loop—not nutrition purity. |
| **BC-02 — Primary outcome** | Desire-level freedom from the BAD SUGAR decision loop: no planned doses, no felt deprivation, no daily negotiation, and no identity built around dietary control. |
| **BC-03 — One reader** | A general adult tired of diets, moderation rules, restriction, lapses, resets, and constant decisions, represented through six functional personas below. |
| **BC-04 — Load-bearing false belief** | BAD SUGAR gives me a special pleasure, reward, comfort, or quick lift that ordinary food and ordinary life cannot provide, so removing it would leave me deprived. |
| **BC-05 — Through-line** | The sweet-reward script assigns BAD SUGAR jobs that belong to taste, appetite, rest, care, achievement, company, ritual, convenience, or the end of anticipation. Rehearsal opens a decision loop; eating may close that episode and receive excess credit. The deprivation method preserves that credit and turns stopping into a battle. Return the credit, and the apparent sacrifice disappears. |
| **BC-06 — Format** | Full-length belief-change book: 23 numbered chapters plus a compact evidence appendix; 60,000 planned words. |
| **BC-07 — Method doctrine** | Escape, not sacrifice; no shame, willpower, fear, command, inner creature, dietary purity, or promised bodily transformation. Pleasant taste and calories are real; unique ownership, necessity, and irreplaceability are the claims on trial. Freedom begins when those claims lose credibility, not after a streak or physiological countdown. |
| **BC-08 — Authority posture** | No author escape story, method-success rate, clinical pedigree, or scale claim is available. The opening earns trust through reader recognition, transparent outcome distinctions, bounded lived accounts, and explicit permission to question the book. First-person guide language may promise honesty or frame an inquiry but may not invent testimony. |
| **BC-09 — Strongest pro-behavior scene** | A restaurant meal in which the dessert menu is checked before the main course, followed by the anticipated first sweet bite. Admit the taste; return leisure, appetite, service, company, and occasion to their sources; use the prior anticipation to illuminate the learned decision loop without treating one account as universal. |
| **BC-10 — Destination state** | Ordinary eating and ordinary occasions with BAD SUGAR absent from the active decision catalog. A menu, birthday, late shift, or accidental ingredient can occur without resistance, pride, panic, compensation, or a planned reset. The felt proof is: there was nothing to settle. |
| **END-01 — Saved ending reframe** | **The returned seat at the table:** ending the sugar debate does not remove a pleasure; it returns attention to the meal, the people, and the moment. The recovered space is attention, not a void requiring a substitute. Debut only in CH-22; CH-23 compresses its meaning through the final instructions without re-arguing it. |

### Functional personas

These are facets of one reader, not separate audiences.

| ID | Function |
|---|---|
| **PER-01 — Sweet-Reward Reader** | Treats taste, dessert, sweet drinks, reward, or a quick lift as a special pleasure life would lose. Corresponds to lived persona P-01. |
| **PER-02 — Restriction Veteran** | Expects denial to intensify desire and interprets one lapse as collapse. Corresponds to P-02. |
| **PER-03 — Context Carrier** | Assigns sugar jobs involving stress, sadness, boredom, social expectation, convenience, access, or lack of time. Corresponds to P-03. |
| **PER-04 — Informed Household Translator** | Uses labels, homemade alternatives, household rules, or achievable reductions but risks purity anxiety or caregiver moralizing. Combines P-04 and P-05. |
| **PER-05 — Managed-Truce Maintainer** | Has obtained genuine relief through boundaries and resets but still pays continuing management costs. Corresponds to P-06. |
| **PER-06 — Decision-Tax Escapee** | Wants irrelevance rather than prohibition and has learned that behavior absence can coexist with dreams, bargaining, or a reward saved for later. Corresponds to P-07. |

### Fork decisions

| ID | Position |
|---|---|
| **F-01 — Inner state** | Externalize the sugar trap, sweet-reward script, deprivation method, and narrowly evidenced Demand Machine. Never portray craving as a creature, attacker, parasite, or independent neurological agent. |
| **F-02 — Outcome** | Lead with full autonomy and let the logic point toward practical total freedom inside the BAD SUGAR line: no planned doses. Moderation remains the reader’s right, and managed truce is treated honestly, but neither recurring exceptions nor perpetual negotiation is renamed desire-level freedom. |
| **F-03 — Science** | Light, claim-graded science in the narrative; compact source-and-limit treatment in Appendix A. Science distinguishes plausible, mixed, and contested stories. It never supplies fear, certainty, or the book’s central mechanism. |
| **F-04 — Villain** | The external villain is the actor-specific, historically documented side of the **Demand Machine**. The internalized wrong method is the **deprivation method**. Ordinary availability is a separate context observation; clinicians, retailers, workplaces, hosts, and treatment are not villains. |
| **F-05 — Afterward** | Natural baseline: ordinary eating, appetite, celebration, rest, pleasure, and connection remain. The Ordinary Eating Compass is temporary teaching scaffolding that succeeds by disappearing. No replacement regimen, tracking practice, or new dietary identity remains. |

## 2. Redefinition, margin, and safety

### DEF-01 — Method labels

“Good” and “bad” describe the method’s operational line. They are not moral judgments about food, bodies, caregivers, or people who eat differently.

### DEF-02 — GOOD SUGAR

Sugars and starches found in ordinary nourishment, including whole fruit, vegetables, legumes, nuts, plain dairy, and ordinary meal staples such as oats, rice, potatoes, bread, and pasta. Their sugar or carbohydrate molecules do not bring them into the target category.

### DEF-03 — BAD SUGAR

Either:

1. **Categorical core:** a product conventionally consumed as a sugar-sweetened drink, confection, dessert, sweet baked good, or added-sugar sweet snack, including products sweetened with sugar, honey, or syrup.
2. **Gray savoury edge:** a genuinely ambiguous refined savoury snack functioning as a discretionary reward, rescue, graze, or automatic nibble rather than ordinary meal food.

Hunger, care, celebration, convenience, homemade status, or a natural, organic, dark, low-sugar, or healthier label cannot exempt a categorical core item. Behavioral-role inquiry applies only at the genuinely gray refined-savoury edge. Small incidental ingredients in an ordinary meal do not make that meal BAD SUGAR.

### DEF-04 — Definitional decree

**Throughout this book, whenever I say sugar, a sugar hit, or quitting sugar, take me to mean BAD SUGAR as defined here—not fruit, ordinary meals, or every carbohydrate.**

### DEF-05 — Totality inside the line

The destination is no planned BAD SUGAR doses. This is practical total freedom, not molecular purity, a medical rule, or loss of the reader’s right to choose.

### DEF-06 — Molecule Margin

A trace ingredient, uncertain restaurant sauce, accidental bite, or genuine classification mistake is not a deliberate return and does not constitute failure. Notice it, learn if useful, and continue from the choice already made. The margin covers accidents and honest ambiguity; it never converts planned exceptions into accidents.

### DEF-07 — Conditional extensions

Whole fruit and ordinary meal carbohydrates remain protected. Juice, dried fruit, non-nutritive sweeteners, alcohol, caffeine, and adjacent indulgences are not required quits and do not define success. They may be examined later only as autonomous, optional questions.

### SAFE-01 — Clinical and eating-disorder perimeter

- Medical glucose, prescribed nutrition, diabetes or metabolic treatment, pregnancy-related dietary instructions, and eating-disorder care are outside the method.
- Qualified clinical instructions always outrank the book.
- Persistent weakness, concerning symptoms, or medical uncertainty must not be resolved through a belief argument.
- The book provides no calorie target, weight-loss program, carbohydrate doctrine, medical nutrition therapy, or eating-disorder treatment.
- If the framework intensifies food fear, restriction, ingredient surveillance, or an eating-disorder pattern, the reader is directed away from self-experimentation and toward qualified care. Immediate danger belongs with local emergency or crisis support.
- Household material may clarify the operational line but may not diagnose, frighten, shame, or prescribe for children.
- No epistemic-firewall instruction may isolate a reader from clinicians or qualified care.

## 3. Compact evidence ledger

### Lived evidence

| ID | Payload and exact source | Tier and scope | Permitted inference | Prohibited inference |
|---|---|---|---|---|
| **EV-L01** | Dessert anticipation, taste, and return: “There’s always room for dessert. If I go out for dinner, I have to look at the dessert menu before I order my mains.” A student said, “I tried to cut down on soft drinks, but I start drinking them again for the taste.” One participant attributed an extra slice after tennis to taste. Sources: S-004#E-001, S-009#E-001, S-020#E-005. | **NON-OUTCOME LIVED JUSTIFICATION.** Small, context-bound accounts. | Voice taste honestly; show anticipatory attention and the credit assigned to it. | No universal dessert need, causal loop, clinical compulsion, or quitting result. |
| **EV-L02** | Participants connected sweets with reward or deserving after effort; one connected feeling weak with a “sugar craving.” Source: S-022#E-005. | **NON-OUTCOME LIVED BELIEF.** One community study. | Show jobs readers assign to sugar. | No physiological energy need, prevalence estimate, or withdrawal claim. |
| **EV-L03** | Stress, staying late, sadness, birthdays, nervousness, boredom, loneliness, social prompting, and an emotional void appeared in participant accounts. Sources: S-020#E-006, S-022#E-001, S-022#E-002, S-022#E-003. | **NON-OUTCOME LIVED CONTEXT.** Particular qualitative accounts. | Build recognizable emotional and social scenes; distinguish the pause or belonging from the product. | No single root craving, causal prevalence, or claim that sugar created the underlying distress. |
| **EV-L04** | “If I deny myself something it turns up somewhere else and worse.” A separate participant described weeks of doing well before one lapse became something every day. Sources: S-020#E-001, S-020#E-003. | **SUPPRESSION.** Individual accounts. | Illustrate deprivation belief and lapse-collapse interpretation. | No rule that practical total freedom backfires or that one bite causes continued consumption. |
| **EV-L05** | One participant described six weeks as a battle and better choices during the final two weeks; another perceived a craving shift during the short intervention. Sources: S-020#E-002, S-020#E-008. | **EARLY SIGNALS — SHORT INTERVENTION.** Eight-week endpoint or subjective perception. | Show that effort and early change can coexist; preserve curiosity. | No durable freedom, physiological reset, efficacy, or universal timeline. |
| **EV-L06** | “I feel like I've been let out of jail.” The same commercial account described daily actions, personal boundaries, difficult occasions, and next-meal or next-day resets. Sources: S-021#E-001, S-021#E-002, S-021#E-004, S-021#E-005, S-021#E-006. | **MANAGED TRUCE.** One commercial testimonial. | Honour genuine relief while distinguishing continued management from desire absence. | No commercial-program efficacy, general outcome, failure label, or proof that management is unnecessary for everyone. |
| **EV-L07** | An earlier four-month dessert-free attempt included nighttime dreams and a stash intended for after the diet. Source: S-023#E-004. | **SUPPRESSION.** One author’s earlier self-report. | Contrast behavior absence with reward belief and deferred compensation. | No universal effect of restriction, withdrawal syndrome, or proof that total freedom is impossible. |
| **EV-L08** | The later account reported at least two hours per week debating dessert, then twelve months without added sugar through major holidays. “Instead, I found myself not missing desserts. And really, I felt better physically and mentally.” The author described removing desserts from the decision catalog without metaphysical prohibition and subjectively reported fruit tasting sweeter. Sources: S-023#E-001, S-023#E-002, S-023#E-003, S-023#E-005, S-023#E-006. | **DESIRE-LEVEL FREEDOM — ONE SELF-REPORT.** | Illustrate a possible difference between suppression and decision quiet. | No general efficacy, probability, universal ease, mechanism, medical outcome, weight claim, moderation result, or expected taste reset. |
| **EV-L09** | Knowledge changed one participant’s anticipated future behavior; a one-less-spoon example felt achievable to one campaign recipient. Sources: S-007#E-001, S-012#E-001. | **EARLY SIGNALS — ANTICIPATED BEHAVIOR / CAMPAIGN RECEPTIVITY.** | Respect reduction and knowledge as potentially useful beginnings. | No implementation, durability, desire absence, or proof that reduction is the final destination. |
| **EV-L10** | A caregiver reported changing a child’s drinks, offering more water, and checking sugar labels. Source: S-010#E-001. | **CAREGIVER BEHAVIOR.** | Illustrate household translation and the need for a usable line. | No evidence of the caregiver’s own freedom, child outcome, or warrant for household moralizing. |
| **EV-L11** | One shopper distrusted purchased sweet beverages and used a homemade-drink substitute that could still contain unrecognized sugar. Source: S-011#E-001. | **NON-OUTCOME LIVED BELIEF.** | Show that source and label changes do not automatically resolve the target category. | No abstinence, freedom, ingredient equivalence, deception, or health outcome. |
| **EV-L12** | A resident said, “people get addicted to drugs, some of us are addicted to soda.” A separate account connected dieting failure with perceived lack of willpower and shame. Sources: S-008#E-001, S-021#E-003. | **NON-OUTCOME IDENTITY LANGUAGE.** | Validate felt pull and character judgment as lived experiences. | No clinical diagnosis, disease mechanism, permanent identity, or proof that treatment is mistaken. |

### Scientific and commercial evidence

| ID | Finding and exact source | Grade and scope | Permitted inference | Prohibited inference |
|---|---|---|---|---|
| **EV-S01** | “We find little evidence to support sugar addiction in humans.” Imaging and intervention findings do not independently establish clinical addiction. Sources: S-001#E-001, S-005#E-001, S-006#E-001. | **CONTESTED.** Broad ordinary-human-sugar-addiction claim remains unsettled. | State that settled addiction language exceeds the accepted evidence. | Neither claim that addiction is proven nor that every diagnosis, vulnerability, or felt compulsion is false. |
| **EV-S02** | Repeated exposure altered some food-response or associative-learning measures, while an ultra-processed-food trial found greater intake and weight gain without identifying the responsible product feature. Sources: S-006#E-001, S-019#E-001. | **MIXED.** Fat and sugar changed together; comparators and samples limit attribution. | Say repeated exposure can affect some measured responses and that product effects need careful attribution. | No sugar-only mechanism, escalating compulsion, universal script, or claim that ultra-processing proves sugar addiction. |
| **EV-S03** | A sweet-intake circuit had causal evidence in mice; a human trial reported, “We did not observe significant differences in BOLD signal to any food cue contrasts” in the whole cohort. Sources: S-003#E-001, S-005#E-001. | **MIXED.** Mouse causality and limited human translation; subgroup interactions do not establish universality. | Use to demonstrate why animal, subgroup, and whole-cohort findings must remain distinct. | No universal dopamine circuit, hijack, crash, or rodent-to-human causal transfer. |
| **EV-S04** | Blocking sweet taste reduced reported pleasure in a small qualitative intervention; a sucrose-versus-sucralose trial found no whole-cohort food-cue BOLD difference. Sources: S-004#E-001, S-005#E-001. | **MIXED.** Pleasure findings are not addiction findings. | Concede that sweet taste can affect reported pleasure. | No inference that taste is imaginary, irreplaceable, addictive, or proof of the book’s efficacy. |
| **EV-S05** | Reports of battle, difficulty, or daily craving management establish subjective difficulty in particular accounts, not physiological withdrawal. Sources: S-001#E-001, S-020#E-002, S-021#E-002. | **MIXED.** Rodent deprivation work and human lived reports do not establish ordinary-adult sugar withdrawal. | Validate difficulty while leaving mechanism open. | No withdrawal timeline, trivialization, headaches/fatigue claims, “reset,” or tapering necessity. |
| **EV-S06** | Reviews of substantial fructose or sugar-sweetened-beverage exposure discuss pathways relevant to hepatic insulin resistance; an ultra-processed-food trial did not isolate sugar as the responsible feature. Sources: S-002#E-001, S-019#E-001. | **MIXED.** Some exposures were unusually high or hypercaloric. | Give narrowly scoped health context, immediately disowned as the motive. | No generalization to whole fruit, every carbohydrate, occasional consumption, ordinary craving, guaranteed repair, or weight outcome. |
| **EV-V01** | Historical records documented formulation around taste, smell, appearance, flavour libraries, and ingredient combinations. One objective was: `The ideal, Winter says, is "to leave people wanting more."` Documentary evidence also described numerous product tests on children during named drink development. Sources: S-013#E-001, S-018#E-001. | **SUPPORTED.** Actor-specific historical practices and objectives. | Establish deliberate appeal and demand optimization by documented actors. | No addiction, deception, clinical harm, actual overeating, or current universal practice. |
| **EV-V02** | FTC records documented youth-directed food marketing across television, packaging, in-store, online, events, and cross-promotions, alongside company research into children’s influence and “pester power.” Sources: S-015#E-001, S-016#E-001. | **SUPPORTED.** Documented expenditures, techniques, and company research. | Show that some marketing deliberately pursued salience and demand. | No universal causal effect on obesity, adult behavior, or every company and product. |
| **EV-V03** | Participants encountered indulgent foods or sweet products repeatedly in cafés, supermarkets, workplaces, free leftovers, vending machines, gas stations, and time-constrained travel. Sources: S-020#E-004, S-022#E-004. | **MIXED.** Qualitative context evidence, not causal access research. | Say recurring availability can keep an option visible and shorten deliberation. | No coordinated placement, retailer or employer intent, powerlessness, or proof that social customs were engineered. |

## 4. Mantra sheet

| ID | Frozen wording | Job and installed belief | Debut | Echo chapters | Final hand-over |
|---|---|---|---|---|---|
| **M-01** | `You can test whether BAD SUGAR owns any special or irreplaceable pleasure, without denying pleasant taste or giving up your right to choose.` | Entry promise and outcome-neutral investigation. | CH-01 | CH-03, CH-18, CH-19 | Used at the threshold as permission to choose from understanding rather than obedience. |
| **M-02** | `without deprivation, without battle, and without a lifetime of rules` | Promise triad distinguishing freedom from suppression and managed truce. | CH-01 | CH-05, CH-06, CH-18, CH-22, CH-23 | Becomes the reader’s diagnostic for whether the belief work is complete. |
| **M-03** | `the sugar trap` | Names the learned structure so stopping feels like escape. | CH-01 | CH-04, CH-05, CH-06, CH-08, CH-13, CH-16, CH-17, CH-18, CH-19, CH-20, CH-21, CH-22, CH-23 | Names what is over whenever an old cue appears. |
| **M-04** | `a special pleasure or rescue` | Names the disputed benefit without denying taste or calories. | CH-03 | CH-07, CH-08, CH-09, CH-10, CH-11, CH-12, CH-14, CH-15, CH-16, CH-18, CH-19 | Gives the reader a compact test for future benefit claims. |
| **M-05** | `a nagging, bargaining, slightly urgent sense that this moment is missing something` | Recognizes the subjective experience without calling it withdrawal or an attacker. | CH-08 | CH-15, CH-16, CH-18, CH-20, CH-21 | Lets the reader label the sensation as an old learned interpretation, not an order. |
| **M-06** | `anticipating, bargaining, and starting over` | Names the decision-tax cost. | CH-01 | CH-05, CH-06, CH-07, CH-12, CH-16, CH-18, CH-22 | Reminds the reader why perpetual management is not the destination sought here. |
| **M-07** | `When the benefit loses its credit, the battle loses its job.` | Compresses the belief-change method and removes willpower. | CH-05 | CH-08, CH-09, CH-10, CH-11, CH-12, CH-14, CH-15, CH-16, CH-17, CH-18, CH-19, CH-20, CH-21 | Directs lingering struggle back to the relevant belief rather than toward force. |
| **M-08** | `You can close the daily sugar debate without policing every molecule, fighting yourself, or treating one accidental bite as failure.` | Full claim block: totality, no inner battle, and margin for error. | CH-02 | CH-06, CH-18, CH-19, CH-22, CH-23 | Serves as the final compact description of the method’s destination. |
| **M-09** | `WHAT A RELIEF — THE SUGAR TRAP IS OVER. I'M FREE!` | Terminal replacement thought: a sugar thought becomes a cue for relief. | CH-20 | CH-21, CH-22, CH-23 | Printed as the reader’s permanent thought script and as the book’s final line. |
| **M-10** | `every ordinary day` | Moves the stakes away from dramatic diets and toward routine decision quiet. | CH-12 | CH-16, CH-22, CH-23 | Hands ordinary, unmonitored life back to the reader as the real arena of freedom. |

## 5. Lexicon and instruction spine

### Lexicon

**LX-01 — Definition tokens**

- **BAD SUGAR**, **GOOD SUGAR**, **Molecule Margin**: governed solely by DEF-01–DEF-07.
- **Sugar hit** or **planned dose**: a unit of deliberate decision-loop behavior, not a pharmacological or diagnostic claim.

**LX-02 — Trap register**

- the sugar trap
- the sweet-reward script
- the open loop
- the deprivation method
- the sugar standoff
- the decision tax
- the Demand Machine
- the menu pop-up
- the default conveyor
- the velvet display case
- borrowed credit
- planned exception
- deferred reward

**LX-03 — Mechanism terms**

- **Sweet-reward script:** the learned proposition that effort, distress, meals, or celebrations require BAD SUGAR.
- **Open loop:** anticipatory attention and bargaining after that proposition becomes active.
- **Sugar standoff:** continuing appears costly while stopping appears to carry an imagined deprivation cost.
- **Demand Machine:** only the documented formulation, testing, packaging, promotion, and marketing practices of specific historical actors. Availability alone does not place a setting inside it.
- **Ordinary Eating Compass:** temporary teaching lens for applying the operational line and returning credit to actual sources.
- **Meal-or-hit check:** only for a genuinely gray refined-savoury item; never an exemption test for a categorical core item.
- **Pleasure-source audit:** a temporary audit of selected cherished scenes, not a daily tracking practice.

**LX-04 — Freedom register**

Escape, free, freedom, relief, quiet, released attention, close the question, ordinary eating, ordinary pleasure, direct ownership, complete occasion, reader-owned choice, practical total freedom, get on with the moment.

**LX-05 — Banned willpower and purity register**

Do not use as the book’s own framing:

- give up, sacrifice, abstain, resist, stay strong, discipline, white-knuckle, trying to stop
- cold turkey, one day at a time, recovery journey, streak, detox, cleanse
- cheat, clean eater, guilty pleasure, good person, bad person
- sugar addict, poison, cocaine, heroin, dopamine hijack, biochemical crash
- taste reset, withdrawal countdown, one bite restarts it
- all carbohydrates are sugar, fruit is the same as soda
- “instead” or consolation language that implies a confiscated reward

These terms may appear only in quoted or ventriloquized beliefs that the chapter immediately corrects.

### Source-grounded reader dialect

These are original reader-voice lines grounded in the syntheses, not participant quotations.

| ID | Frozen reader voice | Primary personas |
|---|---|---|
| **RD-01** | “I check dessert before I have even chosen dinner.” | PER-01 |
| **RD-02** | “If I say no, it only gets louder.” | PER-02 |
| **RD-03** | “I did well for weeks; then one thing became something every day.” | PER-02 |
| **RD-04** | “At work, at the till, or on the road, it is simply the next thing in front of me.” | PER-03 |
| **RD-05** | “I know how to read the label. I still need a line I can live with.” | PER-04 |
| **RD-06** | “My plan works, but it never clocks off.” | PER-05 |
| **RD-07** | “I am not eating it, but I am saving it for the person I will be when this is over.” | PER-02, PER-06 |
| **RD-08** | “I don’t want a perfect streak. I want the debate to stop.” | PER-06 |
| **RD-09** | “Nothing was forbidden. It simply did not need a decision.” | PER-06 |

The phrases “cash wrap food,” “eat our emotions,” and “sugar craving” may be used only as explicitly local or individual dialect, never as universal community or clinical terminology.

### Numbered instruction spine

| ID | Frozen wording | Owner | Recap |
|---|---|---|---|
| **I-01** | **KEEP YOUR CHOICE AND BEGIN WITH RELIEF. Continue eating as you normally do while you read unless qualified clinical care requires something different; do not begin a new restriction campaign for this book.** | CH-01 | CH-06, CH-23 |
| **I-02** | **USE THE BAD SUGAR LINE, NOT MOLECULAR PANIC. Whole fruit, ordinary meals, and ordinary carbohydrates are outside this book’s target; qualified medical, pregnancy-related, or eating-disorder care always outranks this method.** | CH-02 | CH-06, CH-23 |
| **I-03** | **QUESTION BOTH SIDES. Test whether BAD SUGAR owns a special or irreplaceable benefit; do not accept this book, a label, an advertisement, or a familiar rule blindly, and never disregard qualified clinical care.** | CH-03 | CH-06, CH-23 |
| **I-04** | **SEPARATE CHOICE FROM CHARACTER. Notice the belief and its apparent payoff without calling yourself weak, broken, or powerless.** | CH-04 | CH-06, CH-23 |
| **I-05** | **DO NOT USE THE DEPRIVATION METHOD. Do not control BAD SUGAR while preserving it as a lost reward; if restriction is clinically prescribed, follow qualified care without turning it into a character test.** | CH-05 | CH-06, CH-23 |
| **I-06** | **OBSERVE ONE OPEN LOOP; DO NOT TRACK YOURSELF. Once, notice the cue and the job you expected BAD SUGAR to do, then let the observation go; this is a learning exercise, not a monitoring regimen.** | CH-08 | CH-23 |
| **I-07** | **AUDIT ONE CHERISHED SCENE. Credit pleasant taste, people, rest, ritual, appetite, and occasion accurately; deny nothing and let BAD SUGAR keep only what it truly supplied.** | CH-15 | CH-23 |
| **I-08** | **CHOOSE ONLY WHEN THE BENEFIT HAS LOST ITS CREDIT. If BAD SUGAR still feels like a sacrifice, revisit the chapter that owns that belief; do not recruit willpower or override qualified care.** | CH-18 | CH-23 |
| **I-09** | **CROSS THE LINE ONLY BY YOUR OWN CHOICE. If you are ready, choose no planned BAD SUGAR doses from this point; medical glucose, prescribed nutrition, and qualified clinical care are outside this choice and always take priority.** | CH-19 | CH-23 |
| **I-10** | **WHEN BAD SUGAR CROSSES YOUR MIND, DO NOT SUPPRESS THE THOUGHT. Let it cue the freedom thought, then return to what you were doing.** | CH-20 | CH-23 |
| **I-11** | **TREAT AN ACCIDENT AS INFORMATION, NOT A VERDICT. Apply the Molecule Margin to traces, accidental bites, and honest ambiguity; a planned exception remains a choice, and one event never commands the next.** | CH-21 | CH-23 |
| **I-12** | **LET THE COMPASS DISAPPEAR. Eat ordinary food, inhabit ordinary occasions, and own their real pleasures; do not turn freedom into label surveillance, a consolation program, or a new dietary identity.** | CH-22 | CH-23 |

## 6. Scene and analogy bank

### Original analogies

| ID | Image and argumentative job |
|---|---|
| **AN-01 — Dessert pager** | Rehearsal trains an expectation to buzz; eating can silence the present anticipation and be credited with completing the meal. Compresses learning and attribution, not physiology. |
| **AN-02 — Borrowed confetti** | BAD SUGAR stands under a celebration and claims sparkle supplied by people, history, generosity, and shared pause. |
| **AN-03 — Paper medal** | Sugar prints a ceremonial token after effort and claims it produced the achievement, rest, or recognition. |
| **AN-04 — Default conveyor** | Availability moves an option into view without proving need, powerlessness, placement intent, or coordinated manipulation. |
| **AN-05 — Menu pop-up** | A visible option activates a learned decision window; freedom is the window ceasing to demand attention, not clicking “no” forever. |
| **AN-06 — Velvet display case** | Rationing and special-day rules can make a portion symbolically precious while leaving its supposed benefit intact. |
| **AN-07 — Label costume rack** | A different label may change ingredients without moving a categorical core item outside DEF-03. |
| **AN-08 — Customs desk for molecules** | Ingredient perfection recruits endless border checks; DEF-06 restores the operational line. |
| **AN-09 — Typo, not a deleted manuscript** | An accidental bite or lapse does not erase understanding or dictate the next choice. |
| **AN-10 — Removing a billboard from a road** | Leaving BAD SUGAR removes a demand on attention; it does not remove the road, destination, meals, or life. |
| **AN-11 — Two-tollbooth road** | The sugar standoff charges a real toll for continuing and an imagined deprivation toll for stopping. Remove the false toll and the conflict changes. |
| **AN-12 — One bright note claiming the whole song** | A pleasant taste cannot claim ownership of an entire meal, occasion, relationship, or emotional change. |
| **AN-13 — Borrowed pause** | Sugar accompanies a break and claims the rest, permission, and sensory interruption that constituted the pause. |
| **AN-14 — A label is not a lock** | A self-description can name an experience without proving a permanent mechanism or closing choice. |
| **AN-15 — Calendar square** | A Monday, birthday, or New Year carries no special power to make an understood choice real. |
| **AN-16 — Canceled calendar alert** | A familiar thought can recur after its old purpose has ended; its appearance does not create a task. |

### Concrete scenes

| ID | Scene and allowed function |
|---|---|
| **SC-01 — Weekly dessert debate** | The bounded S-023 report of at least two hours each week deciding about dessert; establishes decision tax without front-loading the full testimony. |
| **SC-02 — Clinical boundary contrast** | A hypothetical contrast between prescribed glucose or nutrition and a discretionary sugar hit; protects SAFE-01 without second-guessing care. |
| **SC-03 — Battle, lapse, and managed plan** | EV-L04–EV-L07 contrast suppression and managed truce without turning them into a universal sequence. |
| **SC-04 — Taste return** | The soft-drink return and extra-slice accounts in EV-L01; tests what “for the taste” can and cannot prove. |
| **SC-05 — Earned sweetness** | EV-L02’s reward, deserving, effort, and weakness beliefs; separates accomplishment and nourishment from ceremonial sugar. |
| **SC-06 — The borrowed pause** | EV-L03’s stress, sadness, boredom, late work, or loneliness contexts; validates the need while auditing the product’s credit. |
| **SC-07 — Social dessert** | Restaurant prompting, birthdays, visits, and shared meals from EV-L03; returns belonging to people and participation. |
| **SC-08 — Late road and workplace table** | EV-V03’s vending, gas-station, workplace, café, and time-pressure contexts; demonstrates visibility without intent or compulsion. |
| **SC-09 — Documented optimization desk** | EV-V01 and EV-V02’s formulation, testing, packaging, and marketing records; makes actor-specific intent concrete. |
| **SC-10 — Care in a different package** | EV-L10 and EV-L11’s label checking, drink changes, distrust, and homemade substitution; protects care while testing category logic. |
| **SC-11 — Restaurant best case** | BC-09, reserved for CH-15. |
| **SC-12 — The preserved exception** | Holiday resets, special boundaries, and the stash for after the diet from EV-L06 and EV-L07. |
| **SC-13 — “Addicted to soda”** | EV-L12’s identity language; validates felt pull while separating description from diagnosis. |
| **SC-14 — When the debate went quiet** | Full S-023 method-conflict account: earlier suppression versus later self-reported desire-level freedom. |
| **SC-15 — Reader-owned threshold** | An optional final encounter or deliberate non-purchase in which the reader observes the script, the actual sensory contribution, and the decision tax before choosing. No forced consumption or invented disgust. |
| **SC-16 — Accident or ambiguity** | A trace ingredient, restaurant sauce, accidental bite, or honest gray-edge mistake used to apply DEF-06. |
| **SC-17 — Ordinary revelation** | A menu, late shift, household choice, vacation, or ordinary week passes without private negotiation. A future possibility, never a guaranteed milestone. |

## 7. Arc, curves, structural ownership, and length

### Curve doctrine

- **Demolition curve:** low but value-bearing in CH-01–CH-03; rises through choice and anti-method; peaks from CH-07 through CH-17; falls sharply during readiness and threshold.
- **Freedom curve:** an opening promise pulse; deliberately restrained through the demolition middle; rises in CH-16–CH-18; dominates CH-19–CH-23. The final movement carries more freedom-register language than the preceding movements combined.
- **Ease curve:** front-loaded in CH-01, then assumed rather than continually defended.
- **Cumulative concepts:** named concepts join the permanent vocabulary after debut. Later chapters invoke them rather than re-arguing them.
- **Appendix curve:** neutral, precise, and claim-graded; it does not interrupt the narrative argument with fear.
- **Ending:** END-01 remains fresh until CH-22. CH-23 adds no new argument.

### Arc and budget table

| Unit | Working title and one-line job | Concept debuts | Curves: demolition / freedom | Structural ownership and instruction | Words |
|---|---|---|---|---|---:|
| **CH-01** | **The Debate Can End** — Past battles indict the target and method, not the reader’s character. | sugar trap; decision tax | Low / promise | Trust, contract, evidence-honest authority; I-01 | 2,400 |
| **CH-02** | **Draw the Line Around the Trap** — Define the target, margin, Compass, and clinical perimeter. | BAD SUGAR; GOOD SUGAR; Molecule Margin; Ordinary Eating Compass | Low / promise-low | Redefinition; practical-safety guardrail; I-02 | 2,800 |
| **CH-03** | **Pleasant Is Not the Same as Necessary** — Switch from sensation to ownership and irreplaceability. | special pleasure or rescue | Rising / low | Meta-inoculation; I-03 | 2,500 |
| **CH-04** | **Who Priced the Choice?** — Preserve agency while exposing the false deprivation toll. | sugar standoff | Medium / low | Autonomy/choice synthesis; I-04 | 2,400 |
| **CH-05** | **The Deprivation Method** — Explain why restraint can preserve the reward belief. | deprivation method | Medium-high / low | Anti-method chapter; I-05 | 2,800 |
| **CH-06** | **Fear Has Put Up Two Tollbooths** — Collapse fear of failure and fear of success into the same false conflict. | none | Medium / low | Fear chapter; mid-book recap of I-01–I-05 | 2,300 |
| **CH-07** | **Taste and the Menu Pop-Up** — Taste does not prove unique value, and anticipation does not prove need. | menu pop-up | High / suppressed | First benefit demolition | 2,500 |
| **CH-08** | **The Dessert Pager** — Install the belief-attention-attribution mechanism. | sweet-reward script; open loop | Peak / suppressed | Mechanism hinge; I-06 | 3,000 |
| **CH-09** | **The Paper Medal** — Return reward credit to effort, achievement, rest, and recognition. | paper medal | Peak / suppressed | Reward demolition | 2,400 |
| **CH-10** | **Who Owns the Pause?** — Return comfort credit to the pause and the underlying need. | borrowed pause | Peak / suppressed | Comfort demolition | 2,500 |
| **CH-11** | **Borrowed Confetti** — Return social and celebratory value to people and occasion. | borrowed confetti | Peak / suppressed | Social-benefit demolition | 2,500 |
| **CH-12** | **The Default Conveyor** — Hunger, habit, and convenience explain selection, not special benefit or powerlessness. | default conveyor; meal-or-hit check | Peak / suppressed | Context demolition | 2,600 |
| **CH-13** | **The Demand Machine** — Widen the indictment only as far as actor-specific records permit. | Demand Machine | Peak / low | Engineered-villain chapter | 2,800 |
| **CH-14** | **Labels in Costume** — Protect the categorical line from label changes, purity drift, and household moralizing. | label costume rack; customs desk | High / low | Redefinition reinforcement | 2,600 |
| **CH-15** | **The Best Dessert in the House** — Meet and reassign the strongest pro-sugar scene. | pleasure-source audit | Peak / rising | Strongest-case scene; perception homework; I-07 | 3,000 |
| **CH-16** | **The Velvet Display Case** — Close recurring-exception routes without mocking reduction or managed truce. | velvet display case | Peak / rising | Escape-route closure | 3,000 |
| **CH-17** | **A Label Is Not a Lock** — Demystify powerlessness and overconfident science without disputing care. | evidence firewall | High / rising | Identity-excuse chapter; myths Q&A; scare-then-disown | 2,800 |
| **CH-18** | **When the Dessert Debate Went Quiet** — Use one bounded testimony and a knowledge audit to gate readiness. | none | Falling / high | Embedded testimonial; pre-endgame knowledge recap; I-08 | 3,300 |
| **CH-19** | **The Chosen Threshold** — Offer a reader-owned, immediate crossing with no calendar magic. | chosen threshold | Low / high | Vow with expect-the-unexpected; I-09 | 2,800 |
| **CH-20** | **A Thought Is Not a Summons** — Convert sugar thoughts and social exposure from threats into relief cues. | terminal freedom thought | Minimal / crescendo | Relapse-proofing I; I-10 | 2,400 |
| **CH-21** | **A Typo, Not a Deleted Manuscript** — Forgive accidents and lapses without converting them into permission. | none | Minimal / crescendo | Relapse-proofing II; I-11 | 2,300 |
| **CH-22** | **An Ordinary Seat at the Table** — Retire the Compass and return the reader to ordinary life. | END-01; Compass retirement | Minimal / crescendo | Ordinary-life hand-off; I-12 | 2,100 |
| **APP-A** | **What the Evidence Can and Cannot Say** — Quarantine grades, source IDs, and scientific limits. | none | Neutral / neutral | Evidence appendix | 1,400 |
| **CH-23** | **Your Portable Manual** — Recap instructions and hand over the terminal thought. | none | None / terminal | Final instruction recap and page-skip gate | 800 |

**Arithmetic:**  
2,400 + 2,800 + 2,500 + 2,400 + 2,800 + 2,300 + 2,500 + 3,000 + 2,400 + 2,500 + 2,500 + 2,600 + 2,800 + 2,600 + 3,000 + 3,000 + 2,800 + 3,300 + 2,800 + 2,400 + 2,300 + 2,100 + 1,400 + 800 = **60,000 words**.

## 8. Compact chapter cards

### CH-01 — The Debate Can End

- **Belief job:** Correct “my failed rules prove I am weak or sugar is uniquely powerful” into “the behavior was targeted while its reward status remained intact.”
- **Arc/curve:** Trust and participation; demolition low, freedom promise.
- **Reader:** PER-02, PER-05, PER-06; RD-08.
- **Evidence:** EV-L04, EV-L06, EV-L08. Preserve individual-account and one-self-report limits.
- **Mantras:** Debut M-01, M-02, M-03, M-06.
- **Instruction:** I-01.
- **Scenes/analogies:** SC-01 makes decision tax tangible; AN-11 previews the false stopping cost without completing the later fear argument.
- **Structural responsibility:** Evidence-honest trust contract. Briefly distinguish suppression, managed truce, and desire-level freedom without presenting a universal staircase.
- **Guardrails:** No invented origin myth, author experience, success scale, guarantee, or claim that every diet fails. Do not front-load health fear.
- **Continuity:** Receives skepticism and exhaustion; hands forward permission to investigate a precisely bounded target.
- **Budget:** 2,400 words.

### CH-02 — Draw the Line Around the Trap

- **Function:** Establish DEF-01–DEF-07 and SAFE-01 so totality can mean a clear behavioral category rather than fear of food.
- **Arc/curve:** Definition and safety; demolition low, freedom promise-low.
- **Reader:** PER-04, PER-02; RD-05.
- **Evidence:** EV-L10, EV-L11 only as boundary and household context; preserve non-outcome limits.
- **Mantras:** Debut M-08.
- **Instruction:** I-02.
- **Scenes/analogies:** AN-08 exposes molecular overreach; SC-02 separates clinical necessity from the discretionary target.
- **Structural responsibility:** Box DEF-03, DEF-04, DEF-06, and SAFE-01. Debut the Ordinary Eating Compass as temporary.
- **Guardrails:** No moral good/bad distinction, carbohydrate doctrine, ingredient equivalence, caregiver shame, or clinician conflict. Behavioral-role inquiry cannot exempt a core item.
- **Continuity:** Receives open participation; hands forward one stable line against which every benefit claim can be tested.
- **Budget:** 2,800 words.

### CH-03 — Pleasant Is Not the Same as Necessary

- **Belief job:** Resolve “it tastes good, therefore it gives me something important I would lose.”
- **Arc/curve:** Evaluation-axis switch; demolition rising, freedom low.
- **Reader:** PER-01, PER-04; RD-01.
- **Evidence:** EV-L01, EV-S04. Preserve the distinction between reported pleasure and addiction or necessity.
- **Mantras:** Debut M-04; echo M-01.
- **Instruction:** I-03.
- **Scenes/analogies:** AN-12 separates one sensory note from the whole occasion.
- **Structural responsibility:** Meta-inoculation: voice “How do I know this book is not simply replacing one dogma with another?” and answer through falsifiable questions, evidence grades, and permission to disagree.
- **Guardrails:** Never deny pleasant taste or calories. Do not hedge the value distinction, but retain scientific uncertainty. No fear or false fairness that secretly commands agreement.
- **Continuity:** Receives the operational line; hands forward a clean distinction between sensation and owned life value.
- **Budget:** 2,500 words.

### CH-04 — Who Priced the Choice?

- **Belief job:** Resolve “I choose sugar, so there is no trap” without replacing agency with powerlessness.
- **Arc/curve:** Loaded-choice dissolution; demolition medium, freedom low.
- **Reader:** PER-01, PER-03, PER-05.
- **Evidence:** EV-L02, EV-L03, EV-L12 as examples of attributed payoffs and identity language, not causal proof.
- **Mantras:** Echo M-03.
- **Instruction:** I-04.
- **Scenes/analogies:** AN-11 shows how an imagined deprivation toll distorts the apparent price of stopping.
- **Structural responsibility:** Debut the sugar standoff. Choice remains real; the valuation guiding it can be learned, rehearsed, and corrected.
- **Guardrails:** No claim that choice was literally removed, no blame, no universal con, and no creature or brain mechanism. Do not attack readers who knowingly choose moderation.
- **Continuity:** Receives the pleasure/necessity distinction; hands forward the wrong-method question.
- **Budget:** 2,400 words.

### CH-05 — The Deprivation Method

- **Belief job:** Resolve “restriction feels hard because BAD SUGAR is necessary” by showing how behavioral control can preserve the lost-reward belief.
- **Arc/curve:** Anti-method; demolition medium-high, freedom low.
- **Reader:** PER-02, PER-05, PER-06; RD-02, RD-06, RD-07.
- **Evidence:** EV-L04, EV-L06, EV-L07. Preserve the individual and commercial-testimonial limits.
- **Mantras:** Debut M-07; echo M-02, M-03, M-06.
- **Instruction:** I-05.
- **Scenes/analogies:** SC-03 supplies the suppression/truce contrast; AN-06 shows how restriction can preserve symbolic value.
- **Structural responsibility:** Dedicated anti-method chapter. Reframe past effort as evidence of effort spent on the wrong task, not weak character.
- **Guardrails:** Do not claim all restriction backfires, ridicule useful boundaries, or place medically prescribed restriction inside the indictment.
- **Continuity:** Receives the distorted valuation; hands forward the two fears created by prior battle and imagined loss.
- **Budget:** 2,800 words.

### CH-06 — Fear Has Put Up Two Tollbooths

- **Belief job:** Resolve fear of failure and fear of success: one remembers battle, the other anticipates deprivation, and both inherit the deprivation method’s valuation.
- **Arc/curve:** Fear chapter; demolition medium, freedom low.
- **Reader:** PER-02, PER-05, PER-06; RD-02, RD-06.
- **Evidence:** EV-L04 and EV-L06 as bounded emotional context only.
- **Mantras:** Echo M-02, M-03, M-06, M-08.
- **Instruction:** No new instruction; recap I-01–I-05 verbatim.
- **Scenes/analogies:** AN-11 performs the complete fear correction.
- **Structural responsibility:** Fear-of-failure and fear-of-success chapter plus the sole mid-book instruction recap.
- **Guardrails:** Do not promise universal ease, frighten the reader with consequences, or treat lingering fear as disobedience.
- **Continuity:** Receives the anti-method diagnosis; hands forward a reader ready to test the claimed benefits directly.
- **Budget:** 2,300 words.

### CH-07 — Taste and the Menu Pop-Up

- **Belief job:** Resolve “I return for taste, therefore taste proves lasting or unique value.”
- **Arc/curve:** First benefit demolition; demolition high, freedom suppressed.
- **Reader:** PER-01; RD-01.
- **Evidence:** EV-L01, EV-S04. Preserve small-sample and non-mechanistic limits.
- **Mantras:** Echo M-04, M-06.
- **Instruction:** None.
- **Scenes/analogies:** SC-04 supplies the lived objection; AN-05 distinguishes anticipatory attention from hunger or need.
- **Structural responsibility:** Introduce the menu pop-up without yet completing the flagship mechanism or strongest restaurant scene.
- **Guardrails:** Admit taste plainly. Do not universalize dessert anticipation, imply the participant was irrational, or turn sweet pleasure into addiction evidence.
- **Continuity:** Receives the axis switch; hands forward the question of why anticipation can feel like proof.
- **Budget:** 2,500 words.

### CH-08 — The Dessert Pager

- **Belief job:** Install the core inversion: the sweet-reward script can open an anticipatory loop, and BAD SUGAR may close that episode and receive excess credit.
- **Arc/curve:** Mechanism hinge; demolition peak, freedom suppressed.
- **Reader:** All personas.
- **Evidence:** EV-L01, EV-L02, EV-S02, EV-S03. Every mixed or lived limit remains adjacent.
- **Mantras:** Debut M-05; echo M-03, M-04, M-07.
- **Instruction:** I-06.
- **Scenes/analogies:** AN-01 performs the mechanism; AN-05 supplies the cue-to-decision transition.
- **Structural responsibility:** Debut sweet-reward script and open loop at roughly one-third of the book.
- **Guardrails:** Present a belief, attention, learning, and attribution model—not a universal pharmacological loop. No dopamine hijack, crash, withdrawal, creature, or claim that every dose teaches anticipation.
- **Continuity:** Receives taste and anticipation as separate facts; hands forward a reusable credit-reassignment model.
- **Budget:** 3,000 words.

### CH-09 — The Paper Medal

- **Belief job:** Resolve “I earned it” by returning the reward to accomplishment, permission to stop, recognition, rest, appetite, and self-respect.
- **Arc/curve:** Reward demolition; demolition peak, freedom suppressed.
- **Reader:** PER-01, PER-03.
- **Evidence:** EV-L02.
- **Mantras:** Echo M-04, M-07.
- **Instruction:** None.
- **Scenes/analogies:** SC-05 embodies the deserving belief; AN-03 shows sugar claiming an achievement it did not produce.
- **Structural responsibility:** Complete the effort/reward correction without branching into emotional comfort.
- **Guardrails:** No contempt for rituals, no claim that calories are unreal, and no character judgment about using food as reward.
- **Continuity:** Receives the mechanism; hands forward the same attribution test for emotional rescue.
- **Budget:** 2,400 words.

### CH-10 — Who Owns the Pause?

- **Belief job:** Resolve “sugar calms or comforts me” by returning credit to stopping, sensory interruption, care, rest, and permission while respecting the underlying distress.
- **Arc/curve:** Comfort demolition; demolition peak, freedom suppressed.
- **Reader:** PER-03; locally use “eat our emotions” as individual dialect.
- **Evidence:** EV-L03.
- **Mantras:** Echo M-04, M-07.
- **Instruction:** None.
- **Scenes/analogies:** SC-06 validates the difficult moment; AN-13 separates the pause from what accompanied it.
- **Structural responsibility:** Emotional-benefit demolition.
- **Guardrails:** Do not claim sugar caused the distress, prescribe one replacement for every emotion, minimize loneliness or sadness, or treat persistent symptoms as a belief problem.
- **Continuity:** Receives the reward audit; hands forward credit reassignment in social settings.
- **Budget:** 2,500 words.

### CH-11 — Borrowed Confetti

- **Belief job:** Resolve “dessert creates belonging or makes celebration complete.”
- **Arc/curve:** Social-benefit demolition; demolition peak, freedom suppressed.
- **Reader:** PER-01, PER-03, PER-04, PER-05.
- **Evidence:** EV-L03 and EV-L08’s holiday passage only as bounded possibility.
- **Mantras:** Echo M-04, M-07.
- **Instruction:** None.
- **Scenes/analogies:** SC-07 makes social prompting concrete; AN-02 returns value to people, history, care, and shared pause.
- **Structural responsibility:** Celebration and belonging correction.
- **Guardrails:** No blame toward hosts, families, cultures, caregivers, or people eating dessert. Do not promise that occasions will immediately feel easy for everyone.
- **Continuity:** Receives emotional credit reassignment; hands forward the practical objections of hunger, habit, and access.
- **Budget:** 2,500 words.

### CH-12 — The Default Conveyor

- **Belief job:** Resolve “I was hungry, it was there, or it is habit—therefore it was needed or unavoidable.”
- **Arc/curve:** Context demolition; demolition peak, freedom suppressed.
- **Reader:** PER-03, PER-04; RD-04.
- **Evidence:** EV-L02, EV-V03. Preserve the distinction between context and intent.
- **Mantras:** Debut M-10; echo M-04, M-06, M-07.
- **Instruction:** None.
- **Scenes/analogies:** SC-08 shows recurring access; AN-04 separates visibility from need or powerlessness.
- **Structural responsibility:** Introduce the meal-or-hit check solely for the gray savoury edge.
- **Guardrails:** Hunger belongs to ordinary eating; persistent weakness belongs outside the belief argument. Do not infer retailer, workplace, or vending intent. Never use role inquiry to exempt a core item.
- **Continuity:** Receives the benefit demolitions; hands forward the narrower question of documented commercial intent.
- **Budget:** 2,600 words.

### CH-13 — The Demand Machine

- **Belief job:** Replace self-blame with an accurate account of documented commercial optimization, without converting every encounter into conspiracy or compulsion.
- **Arc/curve:** Widened indictment; demolition peak, freedom low.
- **Reader:** PER-01, PER-03, PER-04.
- **Evidence:** EV-V01, EV-V02, EV-V03.
- **Mantras:** Echo M-03.
- **Instruction:** None.
- **Scenes/analogies:** SC-09 makes actor-specific intent visible; AN-04 contrasts documented optimization with ordinary availability.
- **Structural responsibility:** Engineered-villain chapter.
- **Guardrails:** Keep historical period, actor, objective, and outcome distinct. No claim of addiction, deception, current universal practice, retailer intent, or causal obesity effect.
- **Continuity:** Receives the context/intention distinction; hands forward the reader’s attempt to escape through labels and better versions.
- **Budget:** 2,800 words.

### CH-14 — Labels in Costume

- **Belief job:** Resolve “natural, homemade, organic, dark, low-sugar, or better-labelled means the item no longer belongs inside the line.”
- **Arc/curve:** Boundary consolidation; demolition high, freedom low.
- **Reader:** PER-04; RD-05.
- **Evidence:** EV-L10, EV-L11.
- **Mantras:** Echo M-04, M-07.
- **Instruction:** None.
- **Scenes/analogies:** SC-10 protects care while testing the category; AN-07 handles label changes; AN-08 prevents hidden-sugar purity.
- **Structural responsibility:** Reinforce DEF-03, DEF-06, DEF-07, and the temporary status of the Compass.
- **Guardrails:** Ingredient differences remain real. No caregiver blame, child-body judgment, source-based exemption, or expansion to fruit and ordinary meals.
- **Continuity:** Receives the Demand Machine’s documented limits; hands forward a stable line for the strongest cherished scene.
- **Budget:** 2,600 words.

### CH-15 — The Best Dessert in the House

- **Belief job:** Resolve the strongest case: “This restaurant dessert genuinely completes one of my best experiences.”
- **Arc/curve:** Strongest-case confrontation; demolition peak, freedom rising.
- **Reader:** PER-01, PER-03, PER-05, PER-06; RD-01.
- **Evidence:** EV-L01, EV-L03. Preserve their lived, non-universal status.
- **Mantras:** Echo M-04, M-05, M-07.
- **Instruction:** I-07.
- **Scenes/analogies:** SC-11 carries the chapter; AN-01 invokes the installed mechanism without re-arguing it; AN-12 separates taste from the whole occasion.
- **Structural responsibility:** Strongest pro-behavior scene and primary perception homework.
- **Guardrails:** Admit the first bite’s pleasant taste. Invent no participant dialogue or sensory fact. Do not claim every menu activates a loop.
- **Continuity:** Receives every attribution tool; hands forward a reader whose most seductive scene no longer anchors an exception.
- **Budget:** 3,000 words.

### CH-16 — The Velvet Display Case

- **Belief job:** Resolve “I can keep weekends, holidays, restaurants, better versions, a stash, or managed resets without preserving sugar’s importance.”
- **Arc/curve:** Escape-route closure; demolition peak, freedom rising.
- **Reader:** PER-02, PER-04, PER-05, PER-06; RD-06, RD-07.
- **Evidence:** EV-L04, EV-L06, EV-L07, EV-L09.
- **Mantras:** Echo M-03, M-04, M-05, M-06, M-07, M-10.
- **Instruction:** None.
- **Scenes/analogies:** SC-12 supplies exceptions, resets, and deferred compensation; AN-06 shows symbolic inflation.
- **Structural responsibility:** Foreclose cutting down forever, special occasions, earned sugar, liquid-only or dessert-only exceptions, better labels, consolation products, a stash, compulsory tapering, perfect dates, and managed truce as the only conceivable endpoint.
- **Guardrails:** Reduction may be useful; managed truce may be chosen; neither is mocked. Do not claim exceptions inevitably escalate or that tapering is medically wrong. Keep DEF-06 separate from planned exceptions.
- **Continuity:** Receives the strongest-case demolition; hands forward the final identity and science objections.
- **Budget:** 3,000 words.

### CH-17 — A Label Is Not a Lock

- **Belief job:** Resolve “I am addicted or powerless, so no change in valuation can matter” without denying subjective difficulty, diagnosis, vulnerability, or care.
- **Arc/curve:** Demystification; demolition high, freedom rising.
- **Reader:** PER-01, PER-02, PER-05.
- **Evidence:** EV-L12, EV-S01, EV-S03, EV-S05, EV-S06.
- **Mantras:** Echo M-03, M-07.
- **Instruction:** None.
- **Scenes/analogies:** SC-13 validates the identity language; AN-14 separates description from permanent mechanism.
- **Structural responsibility:** Identity-excuse chapter; rapid myths Q&A; scare-then-disown. Myths include settled sugar addiction, dopamine hijack, universal withdrawal, one-bite restart, fruit equivalence, all-carbohydrate claims, guaranteed outcomes, and universal industry design.
- **Guardrails:** The accepted evidence supplies no population-scale genetic or personality comparison, so the historical-evidence operator must not be fabricated. Use conceptual separation and graceful concession: clinically relevant conditions can coexist with this bounded inquiry, and care remains authoritative. Any health fact is immediately disowned as the motive.
- **Continuity:** Receives closed escape routes; hands forward a complete, uncertainty-honest body of knowledge for the readiness gate.
- **Budget:** 2,800 words.

### CH-18 — When the Dessert Debate Went Quiet

- **Function:** Audit whether the reader understands the difference between behavior control and changed valuation; do not add a new argument.
- **Arc/curve:** Knowledge/readiness bridge; demolition falling, freedom high.
- **Reader:** All personas, especially PER-02 and PER-06; RD-07, RD-08.
- **Evidence:** EV-L07 and EV-L08; EV-L06 may supply a respectful managed-truce contrast.
- **Mantras:** Echo M-01, M-02, M-03, M-04, M-05, M-06, M-07, M-08.
- **Instruction:** I-08.
- **Scenes/analogies:** SC-14 provides the embedded long-form account.
- **Structural responsibility:** Write *In his own words — when the dessert debate went quiet* as a 1–2 page original first-person account limited to verified elements, followed by a “You know that…” installation audit. Place the one-self-report limitation immediately beside it.
- **Guardrails:** No invented dialogue, causes, clinician conflict, sensory details, program information, weight result, medical result, or efficacy implication. Fruit tasting sweeter remains subjective. The conflict is suppression versus later valuation, not reader versus authority.
- **Continuity:** Receives the full argument; hands forward either conceptual readiness or a specific chapter to revisit.
- **Budget:** 3,300 words.

### CH-19 — The Chosen Threshold

- **Belief job:** Resolve “I need a perfect day, forced certainty, or a period of proving myself before I am free.”
- **Arc/curve:** Reader-owned threshold; demolition low, freedom high.
- **Reader:** All personas.
- **Evidence:** EV-L08 only as possibility, never proof.
- **Mantras:** Echo M-01, M-03, M-04, M-07, M-08.
- **Instruction:** I-09.
- **Scenes/analogies:** SC-15 stages the optional rite; AN-15 removes calendar magic.
- **Structural responsibility:** Readiness gate, chosen vow, expect-the-unexpected, and immediate conferral of freedom. Preload difficult future moments while understanding is vivid.
- **Guardrails:** No command, forced final consumption, forced disgust, taste denial, meaningless date, withdrawal prediction, or clinical conflict. Attention may expose packaging, anticipation, brevity, and decision tax; it may not invent ugliness.
- **Continuity:** Receives installed knowledge; hands forward an immediate identity and a way to interpret the first returning thought.
- **Budget:** 2,800 words.

### CH-20 — A Thought Is Not a Summons

- **Belief job:** Resolve “thinking about sugar means I still want it or must suppress it.”
- **Arc/curve:** Relapse-proofing I; demolition minimal, freedom crescendo.
- **Reader:** PER-01, PER-03, PER-05, PER-06.
- **Evidence:** EV-L03 and EV-V03 only as familiar contexts, not mechanisms.
- **Mantras:** Debut M-09; echo M-03, M-05, M-07.
- **Instruction:** I-10.
- **Scenes/analogies:** AN-16 shows a residual thought without a task; SC-17 supplies future social and ordinary contexts.
- **Structural responsibility:** Reframe rather than suppress; remove envy without judging others; reject consolation phrasing; discourage evangelizing.
- **Guardrails:** Do not portray others as inferior or suffering by definition. Adjacent sweeteners remain outside the required quit. No trigger avoidance or thought-policing regimen.
- **Continuity:** Receives immediate freedom; hands forward the harder case of an actual accidental or chosen event.
- **Budget:** 2,400 words.

### CH-21 — A Typo, Not a Deleted Manuscript

- **Belief job:** Resolve “one accident or lapse means failure” while blocking “I got away with it, therefore planned exceptions are beneficial.”
- **Arc/curve:** Relapse-proofing II; demolition minimal, freedom crescendo.
- **Reader:** PER-02, PER-04, PER-05, PER-06; RD-03.
- **Evidence:** EV-L04, EV-L06, EV-L07.
- **Mantras:** Echo M-03, M-05, M-07, M-09.
- **Instruction:** I-11.
- **Scenes/analogies:** SC-16 distinguishes accident, ambiguity, lapse, and planned return; AN-09 removes catastrophe.
- **Structural responsibility:** Slip forgiveness and Molecule Margin hand-over.
- **Guardrails:** No universal one-bite mechanism, shame, “blown it” framing, or permission creep. A planned return is met with honest curiosity about the surviving benefit belief, not punishment.
- **Continuity:** Receives the thought reframe; hands forward ordinary life without vigilance.
- **Budget:** 2,300 words.

### CH-22 — An Ordinary Seat at the Table

- **Function:** Hand the reader back to ordinary eating and ordinary life; remove the scaffolding rather than create a replacement system.
- **Arc/curve:** Ordinary-life close; demolition minimal, freedom crescendo.
- **Reader:** All personas, especially PER-04 and PER-06; RD-08, RD-09.
- **Evidence:** EV-L08 as bounded possibility only.
- **Mantras:** Echo M-02, M-03, M-06, M-08, M-09, M-10.
- **Instruction:** I-12.
- **Scenes/analogies:** SC-17 future-paces possible revelation; AN-10 establishes natural baseline; END-01 supplies the fresh final reframe.
- **Structural responsibility:** Retire the meal-or-hit check and pleasure-source audit once distinctions are ordinary. Keep the Molecule Margin only as a quiet interpretive principle.
- **Guardrails:** No guaranteed revelation, taste reset, health improvement, weight change, superpower, substitute program, dietary pride, or clean-eater identity.
- **Continuity:** Receives a guarded belief; hands forward a life-facing conclusion and a portable reference.
- **Budget:** 2,100 words.

### APP-A — What the Evidence Can and Cannot Say

- **Function:** Provide a compact, claim-graded evidence firewall rather than a second persuasive argument.
- **Evidence:** EV-S01–EV-S06 and EV-V01–EV-V03, with exact grades, source IDs, scopes, and prohibited inferences.
- **Organization:** Addiction and withdrawal; taste and repeated exposure; mouse/human translation; health exposure limits; documented commercial optimization; availability versus intent.
- **Mantras/instructions:** None.
- **Structural responsibility:** Back-matter evidence quarantine.
- **Guardrails:** No flattening MIXED or CONTESTED claims, new sources, health recommendations, raw fear, bibliography invention, or verbatim reuse of narrative prose.
- **Continuity:** Receives the emotionally complete narrative; hands the reader a transparent reference before the final portable manual.
- **Budget:** 1,400 words.

### CH-23 — Your Portable Manual

- **Function:** Nothing new: recap the numbered instructions with owning-chapter cross-references and transfer the book’s voice to the reader.
- **Arc/curve:** Final hand-over; no demolition, terminal freedom.
- **Reader:** All personas.
- **Evidence:** None.
- **Mantras:** Echo M-02, M-03, M-08, M-09.
- **Instruction:** Reproduce I-01–I-12 verbatim in numerical order with chapter references.
- **Scenes/analogies:** END-01 remains implicit in I-12; no new scene or analogy is developed.
- **Structural responsibility:** Begin with a page-skip gate directing readers who bypassed the argument to CH-01. End after the portable list with M-09 as the final line.
- **Guardrails:** No new claim, rationale, exception, testimonial, promise, or summary argument.
- **Continuity:** Receives the completed book and hands over a self-contained internal script.
- **Budget:** 800 words.
===== END PERMITTED INPUT 7/8: calibration/runs/run-014/planning/master-plan-r1.md =====

===== BEGIN PERMITTED INPUT 8/8: calibration/runs/run-014/planning/master-plan-r1-review.md =====
1. **CH-18 — “In his own words — when the dessert debate went quiet.”** The card requires a 1–2 page “original first-person account,” but EV-L07/EV-L08 provide only bounded facts and a few exact quotations. An isolated writer would have to invent the subject’s voice and present paraphrase as his words, violating evidence ownership. Convert the slot to a third-person editorial case narrative using only ledgered facts and exact quotations, and remove the “In his own words” framing.

2. **M-10 routing is contradictory.** The mantra sheet routes `every ordinary day` to CH-23 and gives it a final hand-over function, while the CH-23 card assigns only M-02, M-03, M-08, and M-09. This leaves the final writer choosing between two authoritative instructions. Add M-10 to the CH-23 card, or remove CH-23 and its final hand-over from M-10’s authoritative routing.

needs changes first
===== END PERMITTED INPUT 8/8: calibration/runs/run-014/planning/master-plan-r1-review.md =====
