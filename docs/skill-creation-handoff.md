# Skill-Creation Handoff — Belief-Changer

Paste the prompt below into an agent that has skill-creation tools (CreateSkill / UpdateSkillAndScripts). It creates the 3 missing skills and applies 1 update, completing the Belief-Changer agent's toolkit for the MVP run.

---

```
You are setting up skills for the Belief-Changer project (github.com/keyclaw6/Belief-changer) — an open-source machine that writes Allen Carr "Easyway"-style belief-change books with AI agents. The pipeline: brief → research → framing → master plan (Opus-reviewed) → chapter loop (fresh-context writer + reviewer per chapter). Three skills exist already (belief-changer-deep-research, belief-changer-synthesize-research, belief-changer-master-plan). Your job: create 3 new skills and update 1 existing one, exactly as specified. Source materials live in the public repo — clone it with: git -c http.proxyAuthMethod=basic clone https://github.com/keyclaw6/Belief-changer.git (plain clone 407s against the sandbox proxy).

After creating/updating each skill, verify with GetKnowledgeDetails. When all four are done, attach the new skills to the "Belief-Changer" agent (its system prompt already references belief-changer-repo-push by name).

═══════════════════════════════════════════
SKILL 1 (CREATE) — belief-changer-repo-push
═══════════════════════════════════════════
- Name: belief-changer-repo-push
- Description: Push commits (including binaries) to the Belief-changer GitHub repo using a fine-grained PAT — for everything the text-only GitHub integration can't do (moving PDFs/EPUBs, bulk commits, audio artifacts, branch operations).
- Credential field: GITHUB_PAT (fine-grained PAT scoped to ONLY keyclaw6/Belief-changer, permission Contents: Read and write; the user enters the token in the credential UI — never in chat).
- Documentation: use the "Documentation" section of tools/repo-push/SKILL.md from the repo, verbatim.
- Script: skills/belief-changer-repo-push/push.sh — copy content from tools/repo-push/push.sh in the repo. Description: "Pushes the local Belief-changer clone to GitHub using the GITHUB_PAT credential (proxy-safe; token never echoed)."
- Tags: belief-changer, github, git, push, binaries, pat

═══════════════════════════════════════════
SKILL 2 (CREATE) — belief-changer-framing
═══════════════════════════════════════════
- Name: belief-changer-framing
- Description: Use to complete a Belief-Changer book's framing.md — the book-specific adaptation of the style guide (fork positions, redefinition decision, personas, mantra seeds) — after research is synthesized and before the master plan.
- Tags: belief-changer, framing, adaptation, forks, book-generation
- Documentation (verbatim):

# Completing the Book Framing

framing.md is where a book's hardest DECISIONS get made. It adapts the global style guide to one behavior and feeds the master plan directly. Bad framing = generic book.

**Announce at start:** "I'm using the belief-changer-framing skill to complete the framing."

**Paths** (relative to repo root, /agent/workspace/belief-changer/ or Belief-changer/): style guide at prompts/style-guide.md; the book at production-books/<slug>/.

## Inputs (read ALL before deciding anything)
- prompts/style-guide.md — Part A §3 engine, §4 forks, §10 playbook; Part B §B2 mantra archetypes, §B10 format & redefinition.
- The book's research: research/lived-experience.md + scientific-evidence.md (persona evidence, justifications verbatim, contested flags).
- Any same-topic reference analysis in analysis/ (e.g. burgeon.md for the quit-porn book) — ground fork decisions in what worked/failed there.
- The template structure already in the book's framing.md (v2 template) — fill it in place, every field, no placeholders left.

## Procedure
1. **Personas first** (3–6, by the FUNCTION the behavior serves), each with its load-bearing belief and dialect — from the research, not imagination.
2. **Format decision** (pocket §B6 vs full-length §B10 — default full-length).
3. **The redefinition decision** (§B10) if the behavior can't be quit wholesale: the precise Good-X/Bad-X line, the CAPS name, the definitional decree sentence, the margin-for-error doctrine. Compare how same-topic reference books drew the line before choosing.
4. **The §10 playbook**, every item, specific: load-bearing false belief; the inversion + rescuer-as-perpetrator image; justification list (verbatim from research); engineered villain; science weight; Fork 5 (void) decision; original analogies to invent; escape routes; strongest scene per persona; moment-of-revelation prediction per persona.
5. **Mantra seeds** (§B2): candidate frozen wordings for trap-namer, illusion-namer, mechanism characters (Fork 1: name the trap/lie/industry — never an inner beast), sensory definition (from real community descriptions), named anti-method, named conflict model, named positive authority + instruments, terminal mantra ("...I'M FREE!" core), claim block. The master plan freezes them; here they must be strong candidates that the community's inner voice would accept.
6. **Testimonial mapping**: which research quotes land which beliefs; the embedded long-form testimonial candidate.
7. **Fork positions** (§4), each with one-line rationale where not the house default.

## Non-negotiables
- Every claim/justification/quote traceable to the research files. Never invent.
- **SURFACE THE HIGH-STAKES DECISIONS TO THE USER before finalizing**: the redefinition line, the fork positions, and the terminal-mantra candidate. Present your recommendation + reasoning, get approval, then commit framing.md to main.

═══════════════════════════════════════════
SKILL 3 (CREATE) — belief-changer-chapter-loop
═══════════════════════════════════════════
- Name: belief-changer-chapter-loop
- Description: Use to write one chapter of a Belief-Changer book via the fresh-context writer + reviewer loop, after the master plan is "fit to write from". One chapter at a time, iterated to ACCEPT, then committed.
- Tags: belief-changer, chapter-writing, review-loop, anti-repetition, book-generation
- Documentation (verbatim):

# Running the Chapter Loop

Writes chapter N of production-books/<slug>/ using the anti-repetition design: the writer is a FRESH-context sub-agent that sees ONLY (style guide + master plan + immediately previous chapter). The orchestrator never writes chapters inline — context isolation IS the quality mechanism.

**Announce at start:** "I'm using the belief-changer-chapter-loop skill for chapter N."

## Preconditions
- master-plan.md exists and master-plan-review.md ends "fit to write from".
- Chapters 1..N-1 are ACCEPTED and committed. Never skip ahead; never parallelize adjacent chapters.

## The loop (repeat until ACCEPT, max 4 rounds)
1. **Write**: dispatch a fresh sub-agent with prompts/chapter-writer.md, filling [N], [WORKING TITLE], [SLUG]. It saves to production-books/<slug>/chapters/chapter-NN.md and reports its metrics + any spec gaps.
2. **Spec gaps?** If the writer reports a missing/ambiguous assignment (quote, study, mantra, analogy): STOP, fix master-plan.md (that's a planner defect), re-run the Opus master-plan reviewer on the changed spec if it's substantive, then restart this chapter's loop.
3. **Review**: dispatch a fresh sub-agent (strongest available model) with prompts/chapter-reviewer.md. It returns ACCEPT or REVISE with blocking defects + quality notes + measured metrics.
4. **REVISE** → send the writer (a fresh one, with the reviewer notes appended to its prompt) back to fix. Blocking defects are mechanical: mantra fidelity (character-exact), one job, anatomy, banned register, hedging, re-argument, continuity, traceability.
5. **ACCEPT** → commit the chapter to main immediately (message: feat(<slug>): chapter NN accepted — <title>), update the book README status, and proceed to chapter N+1.

## Escalate to the user (don't loop forever)
- 4 rounds without ACCEPT; or writer and reviewer deadlock on a master-plan ambiguity; or the chapter passes checks but reads generic (the "click" test fails) — show the draft + your diagnosis.
- Always pause at the quality gate the book's HANDOFF defines (e.g. after chapters 1–3 for the MVP) for human judgment before continuing.

═══════════════════════════════════════════
UPDATE 4 — belief-changer-master-plan (existing skill)
═══════════════════════════════════════════
The skill's documentation is already v2. But its bundled script master-plan-reviewer.md is still v1 in the database.
- Replace the script's content with the repo file prompts/master-plan-reviewer-v2.md (verbatim).
- New script description: "Opus sub-agent prompt for reviewing a drafted master plan against style guide Parts A and B — checks the B8 sheets (mantra sheet, instruction spine, curve map, lexicon, structural slots), repetition law, engine coverage, concreteness, and research traceability. Iterated to a 'fit to write from' verdict."
- Do not change the skill's documentation, name, or tags.

═══════════════════════════════════════════
PHASE 2 (do NOT create now — listed for the roadmap)
═══════════════════════════════════════════
Post-MVP platform skills, to be specced when the website work starts: belief-changer-epub-builder (pandoc markdown→EPUB), belief-changer-audiobook-builder (TTS per language, chunked), belief-changer-translate (per-language translation runs preserving the mantra sheet — mantras get ONE frozen translation each), belief-changer-site-deploy.

═══════════════════════════════════════════
VERIFY WHEN DONE
═══════════════════════════════════════════
1. GetKnowledgeDetails on each of the four — documentation present, scripts registered.
2. belief-changer-repo-push shows the GITHUB_PAT credential field (user fills the token in the UI; if credentialsConfigured is false, remind the user).
3. All belief-changer skills attached to the "Belief-Changer" agent.
4. Report a one-line status per skill.
```
