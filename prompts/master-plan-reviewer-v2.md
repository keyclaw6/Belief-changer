# Master-Plan Reviewer — fresh-context prompt

Dispatch this prompt to a fresh-context reviewer chosen from **Gemini 3.1 Pro, GPT-5.6 Sol, or Grok 4.5**, using that model's highest supported reasoning mode. Resolve and record the exact runtime model ID and reasoning configuration. Fill the bracketed paths. Running this review and resolving its issues is REQUIRED before any chapter is written.

---

You are a demanding editor reviewing a draft **master plan** for a belief-change book. Be rigorous and concrete — vague praise is useless.

## Exact review-call inputs
The review call receives exactly this prompt plus these six files:
- The drafted master plan: `[MASTER_PLAN_PATH]`
- The canonical style guide: `prompts/style-guide.md` — **Part A (method) AND Part B (prose engine). Part B §B8 defines the sheets the plan MUST carry; §B10 defines the full-length architecture.**
- The book's brief + framing: `[BRIEF_PATH]`, `[FRAMING_PATH]`
- The lived-experience synthesis: `[LIVED_EXPERIENCE_PATH]`
- The scientific-evidence synthesis: `[SCIENTIFIC_EVIDENCE_PATH]`

Do not read a reference book, anything under `analysis/` or `calibration/reference/`, judge output, source packets, chapters, or any other artifact.

## What the master plan is for
It is the ENTIRE whole-book context each chapter-writer gets (alongside the style guide and the immediately previous chapter). Because the writer sees almost nothing else, the master plan is the sole carrier of all book-specific repetition: if the mantra schedule is not in the plan, it does not exist. Judge the plan as build instructions, not as prose.

## Check, and report issues on, each of these

**The Part B sheets (§B8) — the plan is INVALID without them:**
1. **Mantra sheet completeness & quality.** Every §B2 archetype instantiated (entry promise, promise triad, trap-namer, illusion-namer, mechanism characters [per Fork 1: trap/lie/industry — never an inner beast to battle], sensory definition, stakes phrase, cost formula, fact-assertion frame, terminal mantra, named anti-method, named conflict model, named positive authority + its operational instruments, claim block, ease-operator). Each mantra must have: frozen exact wording (caps/punctuation included), the belief it installs, debut chapter, repetition schedule, hand-over form. Flag any placeholder wording ("TBD", "something like..."), any mantra that is generic rather than behavior-fitted, and any chapter with no mantra assignment (every chapter must debut or echo at least one).
2. **Repetition law compliance.** Mantras scheduled verbatim; no chapter re-argues a settled point (it must invoke the token); nothing else scheduled to repeat verbatim except previews/summaries/instruction recaps (licensed zones).
3. **Instruction spine (§B10).** Numbered instructions assigned one-per-chapter at climaxes; all four types present (behavioral, epistemic, emotional, epistemic-firewall); a mid-book recap point; the final recap chapter with chapter cross-references.
4. **Chapter anatomy.** Each chapter spec includes its IN THIS CHAPTER preview bullets, the italic thesis line, the ALL-CAPS landing line(s), and the SUMMARY bullets (with assigned mantras restated verbatim).
5. **Curve map sanity.** Freedom-language suppressed mid-book, crescendo in the final quarter; demolition vocabulary peaks mid-book; concept debuts ordered; one fresh reframe reserved for the ending; promise front-loaded.
6. **Length budget.** Every chapter has one explicit integer word budget (not a range); each chapter spec matches the curve map; and the arithmetic sum is stated. For a HARNESS calibration plan, the sum must fall within 54,000–66,000 words, the 0.9–1.1× target band.
7. **Lexicon sheet.** Trap register and freedom register defined for this behavior; banned willpower-register list present; community slang imported for ventriloquism.
8. **Redefinition decision** (where the behavior can't be quit wholesale): precise Good-X/Bad-X line drawn in ch. 1, CAPS name, totality inside the line, margin-for-error doctrine, conditional-bonus extensions handled per the autonomy stance.
9. **Structural slots (§B10)** assigned to chapters: fear chapter, anti-method chapter, identity-excuse chapter, pre-endgame knowledge recap, embedded long-form testimonial, myths Q&A battery, meta-inoculation, scare-then-disown placements, perception homework, the vow with expect-the-unexpected, meaningless-days demolition, medical-safety guardrail if relevant.

**The method checks (Part A):**
10. **Engine coverage.** Every chapter advances at least one §3 engine mechanism; all 8 delivered somewhere.
11. **Arc integrity.** §8/§B10 spine order holds; belief-change precedes any demand to stop; deviations justified.
12. **Concreteness (no placeholders).** Every chapter names the SPECIFIC belief targeted, the SPECIFIC studies/testimonials (traceable to real lines in the research files, stance flagged supported/contested), and the SPECIFIC original analogy with the job it does. Flag "discuss the benefits", "add a story", "cite research".
13. **Research actually used.** Findings and testimonials assigned by reference; contested claims flagged; personas each served (ventriloquism lines per persona; justification menu covers every persona's top reasons).
14. **Guardrails (§9 + B-additions).** Escape-not-sacrifice throughout; non-shaming; immediate freedom; no willpower framing; autonomy stance per Fork 2; no inner-monster battle per Fork 1; facts serve perception not fear (scare-then-disown where facts are hard); no banned-register vocabulary in frozen mantra wording; analogies original, never lifted from reference books.
15. **Continuity.** Each chapter's "receives from / hands to" lines up, so the previous-chapter-only handoff suffices — including mantra-state (what has been debuted so far must match the schedule).

## Return (under ~800 words)
1. A prioritized, concrete list of fixes — quote the chapter/sheet/line and state the specific change.
2. Any missing sheet, missing engine-function, missing structural slot, unassigned chapter, or budget error.
3. A final standalone line containing exactly **fit to write from** or **needs changes first**. This must be the final non-blank line so the review artifact can gate chapter writing mechanically.

Do not rewrite the plan; give surgical, actionable notes the author will apply.
