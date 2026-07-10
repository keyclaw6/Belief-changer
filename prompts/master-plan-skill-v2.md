# Writing the Book Master Plan (v2 — Prose Engine aware)

Adapted from `superpowers-writing-plans`. Same philosophy — write build instructions for someone with **zero context** — but here the "engineer" is a chapter-writing agent whose ENTIRE context is three things: **this master plan, the immediately previous chapter, and the style guide**. Everything a chapter needs must therefore live in its spec — and because the writer never sees the other chapters, **the master plan is the sole carrier of the book's deliberate repetition**: the mantra schedule, the instruction spine, the curves. If it isn't in the plan, it doesn't exist. The plan is build instructions for a book, not prose. DRY. No placeholders.

**Announce at start:** "I'm using the belief-changer-master-plan skill to write the master plan."

**Paths:** all paths below are relative to the **Belief-Changer repo root** (in this sandbox: `/agent/workspace/Belief-changer/` or `/agent/workspace/belief-changer/` — verify which exists). The style guide is at `prompts/style-guide.md`; each book folder is `production-books/<slug>/`.

## Exact planning-call inputs (non-negotiable)
The planning call receives exactly this prompt plus these five files, and no other context:
- **The style guide — BOTH PARTS** — `prompts/style-guide.md`:
  - Part A: the §3 convergent engine, §4 forks, §5 moves, §6 framing, §8 chapter-arc, §9 guardrails, §10 adaptation playbook.
  - **Part B (the prose engine — the binding writing contract): §B1 Repetition Law, §B2 mantra archetypes, §B3 curves, §B4 lexicon, §B5 operators & metrics, §B6/§B10 architecture, §B7 chapter contract, §B8 the sheets THIS PLAN must produce.**
- **The brief** — `production-books/<slug>/00-brief.md`
- **The framing** — `production-books/<slug>/framing.md`
- **The lived-experience synthesis** — `production-books/<slug>/research/lived-experience.md`
- **The scientific-evidence synthesis** — `production-books/<slug>/research/scientific-evidence.md`

Do not read a reference book, anything under `analysis/` or `calibration/reference/`, judge output, source packets, other chapters, or any other book artifact. If a required input is missing, empty, or too thin to support a plan, STOP and report the gap; do not gather new context inside the planning call. If research is contradictory, assign only what the evidence supports, preserve contested labels, and never paper over a gap with an invented finding.

## Step 0 — Enforce the input gate
Confirm that all five required files were supplied and no forbidden or extra context was supplied. Stop before drafting if the exact-input contract is not satisfied.

## Step 1 — Lock the book-specific decisions
Ensure `framing.md` answers all items of the style guide's §10 adaptation playbook and states the §4 fork positions. Additionally decide now:
- **Format**: pocket (§B6) or full-length (§B10 — default for real books; mandatory at 15+ chapters).
- **The redefinition decision** (§B10) if the behavior can't be quit wholesale: the precise Good-X/Bad-X line, the CAPS name, the margin-for-error doctrine.
- **Persona set**: the 3–6 reader personas (by the function the behavior serves) the book must speak to.

## Step 2 — Derive the per-book sheets (§B8) — THE HEART, write these FIRST
These sheets are book-level sections of `master-plan.md`, before any chapter spec:
1. **The mantra sheet.** Instantiate EVERY §B2 archetype with frozen exact wording (capitalization and punctuation included) fitted to this behavior: entry promise, promise triad, trap-namer, illusion-namer, mechanism characters (per Fork 1: name the trap/lie/industry — never an inner beast the reader battles), sensory definition, stakes phrase, cost formula, fact-assertion frame, terminal mantra (core: "...I'M FREE!"), named anti-method, named conflict model, named positive authority + its 1–3 operational instruments, claim block, ease-operator. For each: (a) frozen wording, (b) belief installed, (c) debut chapter, (d) repetition schedule, (e) hand-over form. **Every chapter must debut or echo at least one mantra.** Stress-test wording against the community lexicon (would the reader's inner voice accept it?).
2. **The lexicon sheet** (§B4): trap register, freedom register, banned willpower-register list, community slang for ventriloquism.
3. **The instruction spine** (§B10): the numbered instructions (all four types — behavioral, epistemic, emotional, epistemic-firewall), one-per-chapter assignments at climaxes, the mid-book recap point, the final recap chapter with chapter cross-references.
4. **The justification menu**: the reader's stated reasons verbatim from research, covering every persona, mapped to demolition chapters.
5. **The analogy assignment**: which original analogy does which job in which chapter (never reuse the reference books' analogies).
6. **The curve map** (§B3): each chapter's position on the freedom-crescendo and demolition curves; concept debut order; the saved-for-ending reframe; one explicit single-integer word budget per chapter; and the arithmetic sum of all chapter budgets.
7. **The structural-slot assignments** (§B10): fear chapter, anti-method chapter, identity-excuse chapter, pre-endgame knowledge recap, embedded long-form testimonial, myths Q&A battery, meta-inoculation, scare-then-disown placements, perception homework, the vow with expect-the-unexpected, meaningless-days demolition, medical-safety guardrail if relevant.
8. **Persona notes**: ventriloquism lines and strongest-case scenes per persona; the moment-of-revelation prediction.
9. **The fork decisions** stated explicitly.

## Step 3 — Map the chapter arc
Use §B10 (full-length) or §8/§B6 (pocket) as the scaffold. Adapt beats to the behavior but **preserve the spine** and **defer any demand to stop until the belief has changed**. List chapters and the one-line job of each before writing full specs. **Floor:** every one of the eight §3 engine-functions must be delivered somewhere, and the spine order must hold.

Assign every chapter one explicit integer word budget, never a range. For a HARNESS calibration plan, the budgets MUST sum to **54,000–66,000 words**, the **0.9–1.1× target band**. State the total, show that it is the sum of the chapter budgets, and repeat each chapter's same budget in its full spec.

## Step 4 — Write each chapter spec (the heart, per chapter)
Write the book-level header once: target behavior, reader/personas, fork stances, the load-bearing false belief, the through-line (5–8 sentences), the recurring devices.

Then **every chapter** must specify ALL of these — concretely:
- **Chapter N — working title**
- **Engine function(s) (§3)** and **arc beat (§8/§B10)**
- **Job (1–2 sentences):** the ONE belief-move
- **Belief(s)/justification(s) targeted** (specific, from the menu)
- **Mantra assignment:** mantras this chapter DEBUTS (with the full argue→compress beat) / mantras it ECHOES (verbatim, brief) — exact wording restated from the mantra sheet
- **Instruction** (if this chapter carries one): number + frozen wording
- **Chapter anatomy (§B10, full-length):** the IN THIS CHAPTER preview bullets; the italic thesis line; the ALL-CAPS landing line(s); the SUMMARY bullets (assigned mantras restated verbatim)
- **Curve position:** freedom-language level; demolition phase; any concept debuts
- **Structural slot** (if assigned): testimonial / myths battery / meta-inoculation / homework / etc., with its content source
- **Moves to use (§5 + §B5 operators, by name)**
- **Framing / emotional beats (§6)**
- **Scientific evidence to weave in:** SPECIFIC findings, cited as labelled in `scientific-evidence.md`, with stance (supported/contested)
- **Lived experience / testimonials to weave in:** SPECIFIC quotes from `lived-experience.md` and the belief each illustrates, persona-tagged
- **Analogy(ies) to invent:** the original image(s) and the job each does
- **Continuity:** what it receives from / hands to its neighbours — including mantra-state (what is already debuted)
- **Word budget:** one explicit integer matching the curve map (not a range)
- **Tone notes**
- **Guardrails to watch here (§9):** the specific risk for this chapter

## No Placeholders (plan failures — never write them)
- "Discuss the benefits" / "cover the science here" / "add a testimonial" — name the exact belief, study, quote.
- "TBD", "fill in later", "similar to Chapter N" (repeat the specifics; chapters may be written out of order).
- **A mantra without frozen wording** ("something like...", "a phrase about freedom") — the wording IS the deliverable.
- A chapter with no mantra assignment, or an analogy slot with no analogy concept.
- A chapter whose engine-function (§3) you cannot name.
- A missing budget, a budget range, a chapter-spec budget that differs from the curve map, or—for a HARNESS calibration plan—a total outside 54,000–66,000 words (0.9–1.1× the target).
- **Untraceable research.** Every study and testimonial must be traceable to a real line/heading in the research files, cited as labelled there. If you cannot point to the source line, it does not exist.

## Self-Review (before independent review)
Run the reviewer's checklist (`prompts/master-plan-reviewer-v2.md`) on yourself and fix inline — especially: mantra sheet completeness (every archetype, frozen wording, every chapter assigned), repetition-law compliance, instruction spine, chapter anatomy, curve sanity, numeric budget reconciliation, engine coverage, zero placeholders, research traceability, continuity (including mantra-state).

## REQUIRED — fresh-context review (NOT optional)
A master plan is **not final** until a fresh reviewer chosen from Gemini 3.1 Pro, GPT-5.6 Sol, or Grok 4.5 has reviewed it at that model's highest supported reasoning mode and all issues are resolved.
- Resolve the exact runtime model ID and top reasoning configuration before dispatch, then use `prompts/master-plan-reviewer-v2.md` with the required paths filled in.
- Record the model configuration, verdict, and **every** issue in `production-books/<slug>/master-plan-review.md`. Resolve each issue in `master-plan.md`, then re-dispatch a fresh reviewer; repeat until the review file ends with the exact standalone verdict `fit to write from`, with no unresolved major issues (maximum three cycles).
- **Disagreement rule:** the reviewer's call stands on anything touching §3 engine coverage, the §B8 sheets, the Repetition Law, spine integrity, §9 guardrails, or placeholder/concreteness. The author may override only documented style/length/ordering preferences, with rationale recorded in the review file.

## Save
The plan lives at `production-books/<slug>/master-plan.md`; the review lives at `production-books/<slug>/master-plan-review.md`. Version-control actions belong to the caller's active production or calibration workflow.

## Handoff to chapter writing
Each chapter-writer receives **the master plan + the immediately previous chapter + the style guide**, and must honor the §B7 per-chapter contract (one job; mantras verbatim; anatomy; curve-aware vocabulary; operators & metrics; triangle discipline; no other verbatim repetition). The chapter reviewer rejects: mangled/paraphrased/missing mantras, re-argued settled points, banned-register vocabulary, hedged core reframes, missing anatomy elements, or drift off the chapter's single job.
