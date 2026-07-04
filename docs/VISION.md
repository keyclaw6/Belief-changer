# Belief-Changer — Vision & Working Tracker

> Living document. **Part I is the canonical vision** — the product intent every change in this repo serves; read it before working here. Part II is the working tracker (pipeline design, status, decisions, open questions). Repo: github.com/keyclaw6/Belief-changer

---

# Part I — The Vision

## Founder's statement

Allen Carr's Easyway books have helped countless people change their beliefs and, through that, change their lives. The method is proven wherever it has been applied — and yet the original series covers only a handful of behaviors. There is so much pain in the world caused by beliefs that are quietly ruining people's lives, and far too few who can help. Easyway has helped a lot of people, but its scope is limited; we are here to broaden that scope.

Because LLMs have become so powerful, what was impossible before is now buildable: an Easyway-style **belief-change book generation machine** — free and available to everyone, able to produce a book for every belief people want to change. This is my contribution to the world: the way I help as many people as possible, together with helping myself.

## The core belief

**We act the way we believe.** In every moment a person chooses what they believe is their happiest available option. The problem is that beliefs about which option is happiest are frequently misaligned with reality — we act on an incomplete or distorted model of what each option actually costs and delivers.

*Example (junk food):* in the moment, you weigh only "this tastes good." You don't viscerally weigh the full consequence set — lost agility, weight gain, energy crashes, long-term health. If the true, complete consequence model were present at the moment of choice, you would choose differently — not through willpower or deprivation, but because the option would simply no longer look appealing.

**The only thing that changes behavior long-term is changing those beliefs.** Willpower, shame, and discipline fight the choice while leaving the belief that drives it untouched — which is why they fail. Correct the belief, and the behavior changes on its own: quitting stops feeling like sacrifice and starts feeling like **escape**. Allen Carr's Easyway proved this works in the real world (smoking above all). The Freedom Model — a non-12-step, non-disease-model framework for addiction — reaches the same conclusion: change happens when a person genuinely sees that the behavior no longer serves their happiness. The method is not the bottleneck; coverage is.

## The gap

Where an Easyway book exists, it works. But the catalog is tiny relative to the need. There is no equivalent high-quality resource for doom-scrolling social media, gaming, pornography and masturbation, complaining about things outside your control — and hundreds of other behaviors people struggle with alone. The need is vast, unmet, and — until now — unserveable.

## What we are building

A book **generation machine**, plus a **platform** that hands its output to the world:

- **Endless books** — one for every belief people want to change, produced by the agent pipeline (research → framing → master plan → chapters) under a founder-held quality bar.
- **Free for everyone, forever** — open-source and nonprofit. No paywall between a person and escape from a trap.
- **Every format** — EPUB e-book, in-browser reading, and audiobook. (Print-on-demand may follow where it extends reach.)
- **Every language** — AI translation makes every book available worldwide.
- **Every part built by agents** — research, writing, review, translation, narration, publishing. Humans set direction and hold the quality bar.

## The self-evolving library

A website hosts every book and turns readers into contributors, so the library improves and grows on its own:

1. **Feedback loop** — readers submit feedback and personal experiences on each book they've read; accepted feedback flows into the book's research banks and triggers a revision run. Books are version-controlled with public changelogs — they get better over time.
2. **Request loop** — anyone can request a book for a new behavior and contribute their personal experience of it. When enough people have requested a topic and contributed their experiences, the pipeline fires automatically and the site announces the new book.
3. **Splitting loop** — as a book's feedback spans more and more distinct situations, it splits into focused editions for specific personas and problems, so every reader finds the exact book matched to their situation.

End state: **thousands of books, in hundreds of languages, continuously improving — a belief-change system, not a shelf.**

## Beyond books

Once book generation is up and running: **guided courses connected to each book**, walking a person through surfacing and assessing their own current beliefs — deepening the belief-change journey the book begins.

## The mission

This tool is for the benefit of all humans on the planet. The measure of success is people freed from traps — never revenue, never engagement for its own sake. Warm to the person, harsh to the trap; escape, not sacrifice; free, for everyone, always.

*The operating rules that protect this vision live in `AGENTS.md`, `prompts/style-guide.md`, and `openspec/specs/method-integrity/`.*

---

# Part II — Working Tracker

## Content Generation Pipeline

**Four phases:**

1. **Research** — two distinct streams:
   - *(a) Lived experience:* a research agent mines forums/communities for how real people actually feel about the behavior and its downsides — so the book contains experiences that "hit home."
   - *(b) Scientific evidence:* gather studies on what the behavior actually does.
2. **Template / Structure** — a reusable understanding of how Easyway-style books are structured.
3. **Master Plan** — a long, detailed blueprint: what each chapter contains, which analogies to use where, the argument arc, etc.
4. **Generation** — chapter by chapter (see key insight below).

**★ Key design insight — anti-repetition context strategy.** Each chapter-writing call receives *exactly three things*:
- **The master plan** (always) → global oversight of the whole book.
- **The immediately previous chapter only** (not all prior chapters) → local continuity without drift.
- **A style guide** → consistent voice.

*Why this is smart:* LLMs over-repeat phrases and structures that sit in their context window. Feeding only the previous chapter preserves coherence while starving the model of the bulk context that drives repetition. The master plan keeps whole-book structure intact; the style guide keeps voice constant. This is a genuinely strong design choice and should be preserved.

**★★ Correction (mantra exception) — DECIDED.** The Easyway prose analysis (`analysis/easyway-prose-patterns.md`) showed Carr's method *depends* on deliberate, scheduled, **verbatim** repetition of a small set of fixed mantras ("nothing to lose and everything to gain", "FANTASTIC! I'M FREE!", the trap-namer, the illusion-namer, etc.). The anti-repetition context strategy suppresses exactly this, so the good repetition must be **specified, not emergent**: the master plan carries a per-book **mantra sheet** (frozen wording, debut chapter, repetition schedule, hand-over form) and every chapter sets or reinforces a mantra. **The law: mantras are repeated verbatim; everything else is never repeated verbatim.** See `prompts/style-guide.md` Part B.

---

## Orchestration Architecture

An **orchestrator** holds the master view and hands off to specialized sub-agents:
- Research agent(s)
- Reviewer agent
- Chapter-writing agent

**Flow:**
- Orchestrator runs research → reviews it → requests more research on weak spots.
- Orchestrator builds the master plan.
- For each chapter: orchestrator prompts the chapter-writer → calls the reviewer → if the reviewer flags issues, loops back to the writer → repeat until accepted → advance to the next chapter.

---

## MVP — Build Inside Hyperagent First

Fastest path to a working prototype: use **Hyperagent as the orchestrator now**, built from a skill + a file-management convention + good prompts. This sidesteps the standalone-framework decision entirely for v0.

**Concrete v0 workflow:**
1. Research → returns → orchestrator judges sufficiency.
2. If insufficient → launch another (targeted) research agent.
3. Produce a research document (saved to the repo).
4. When research is accepted → build the master plan.
5. Master plan refined/expanded by a research sub-agent.
6. Spawn chapter-writer → write Ch. 1 → save to a file in the repo.
7. Call peer-review agent → feedback → back to the writer → on acceptance, advance.
8. Repeat to the end of the book.

---

## Book Analysis — Approach (MVP Step 1)

**Goal:** Sub-agents analyze the foundational books (Easyway, The Freedom Model, + a third TBD) and produce one *editable* analysis document **per book** capturing the transferable mechanism — philosophy, method, approach, belief-change tactics, emotional framing — plus a catalog of analogies and verbatim memorable lines. The human curates each document (delete any point, add their own). Priority: philosophy, method, and framing over surface style.

**Documents:** one analysis document per book at `analysis/<book-slug>.md`, organized by **category, not by chapter**. Entries are **unnumbered bullets, each a single self-contained statement** (may be long) so any point can be deleted without renumbering. **No provenance / observation tags.** Strong, well-written sentences are **copied verbatim** in quotation marks. (Copyright is explicitly out of scope for this phase.)

**Processing model (round 2): chunked, fresh-context.** For each book, 2 Opus agents run in sequence (first half, then a *fresh* second-half agent); each reads ONE ~10-page window at a time, writes to the doc, then reads the next; a single agent covers at most half a book. The three books run in parallel. Each doc opens with a ranked **Core Signal** block, then category sections (most-important-first), plus a verbatim **Memorable Lines & Quotations** section. No **Cautions** section. Inclusion test: *would this help create a new belief-changing book?* (the master plan AND the prose), so powerful verbatim quotes are kept.
- *Round 1 (superseded):* one agent read each whole book in a single pass — produced flat, unprioritized output. Replaced by the chunked approach above.

**Inputs:** PDFs in `analysis/reference-books/` (grouped with their analyses); intermediate cleaned text + 10-page window files are regenerated locally from the PDFs (not committed).

**Prompt:** `prompts/book-analysis-agent.md` (v4 — chunked fresh-context; no Cautions; broadened inclusion test; tag-free, unnumbered single-statement bullets).

**Status — round 2 COMPLETE & committed (`abba9de`):**
- `analysis/easyway-caffeine.md` — Allen Carr, *The Easy Way to Quit Caffeine*
- `analysis/freedom-model.md` — *The Freedom Model for Addictions* (abridged), Slate/Scheeren/Dunbar
- `analysis/burgeon.md` — *Burgeon* (uncredited; quit-PMO/porn book, neuroregen.org)

Cross-book finding: all three run the same core Easyway engine — dismantle the perceived benefit so quitting feels like escape not sacrifice; freedom is immediate (no day-counting); the "pleasure" is only relief of self-created withdrawal.

**DECISION (resolved): keep the detailed round-2 reports as-is** — they are our deep reference instructions for each book; no condensation.

**Repo reorg:** reference PDFs/EPUB are grouped with their analyses under `analysis/reference-books/`; the root `books/` folder is retired in favor of `production-books/` (for books the pipeline generates). *(The binary move is now done via `git mv` + the `belief-changer-repo-push` skill's PAT, which can commit binaries — the old "GitHub UI only" constraint is lifted.)*

**Style guide v2 — `prompts/style-guide.md`:** restructured into Part A (method) + **Part B (the prose engine)**: the mantra system & repetition law, repetition-schedule curves, two-register lexicon sheets, sentence-operator toolkit with voice metrics, verified Carr book architecture, per-chapter writing contract, and the per-book sheets the master plan must carry (§B8). Research stage redesigned as slot-filling **raw material banks** with persona segmentation — `prompts/research-agent.md`. Prose-pattern analysis: `analysis/easyway-prose-patterns.md`. *(v1 description below kept for history:)*

**Style guide v1 (superseded) — `prompts/style-guide.md`:** the canonical writing prompt, distilled by an Opus sub-agent from all three reports. Contents: each book's philosophy → **the convergent 8-mechanism engine** (the heart) → **5 divergence "forks" with our house position** → belief-change toolkit → emotional-framing techniques → voice rules → an **Easyway-based, behavior-agnostic chapter-arc template** → guardrails → a per-behavior adaptation playbook → exemplars. **This is fed to every chapter-writer and used by the master-plan step.**

**Next:** build the master-plan prompt (consumes the style guide), then the chapter-writer + reviewer loop. Pick the MVP target behavior (gaming is the running candidate).

---

## Open Questions / Decisions Needed

**Q1 — Orchestration framework** (for the eventual standalone system). Two candidates (OpenCode dropped):
- *Forked PI (π) agent* — PI is extremely minimal (~30-line system prompt). Plan: fork it and strip/replace that prompt so we control 100% of what the book-creation agent receives; gives a hackable base **and** PI's interface for watching sub-agents. No native sub-agents, but a sub-agent plugin can be built/added.
- *OpenAI Agents SDK* — no baked-in prompts, purpose-built for orchestration; no UI out of the box.

**Q2 — Drawing principles & style from a *whole* book** (Easyway + The Freedom Model), given length. Now being actioned for the MVP — see "Book Analysis — Approach" above.

**Q3 — Search / research tooling.**
- *Provider:* User likes Grok's web search. **Finding:** that quality comes from xAI's *own proprietary web index* + real-time *X search* — NOT Google, Bing, Tavily, or Perplexity. Reachable via the xAI API's Live Search / `web_search` tool; there is no separable third-party engine to adopt.
- *Depth framework:* Separately, an open-source "deep research" framework is wanted to *drive deeper search* — naive agents search shallowly; a deep-research loop forces breadth + depth. This is orthogonal to the provider.
- *MVP:* the search tools already in Hyperagent (Exa neural search, web search, browser) are good enough for the MVP.

---

## Platform (website) — architecture (DECIDED 2026-07)

The delivery arm of the vision (Part I): every book as EPUB, in-browser reading, and audiobook, in every language, with the three community loops (feedback, request, splitting) making the library self-evolving. Architecture decisions:

- **Monorepo.** The site lives inside this repo (`/site`) alongside `production-books/` (content source of truth), `prompts/`, and `analysis/` — one place for full observability; the site builds directly from the book files, so a merged chapter is a deployed chapter.
- **Stack: Next.js (App Router) + TypeScript + Tailwind CSS** — chosen explicitly as the stack the coding agents are most fluent in; file-convention-driven, statically generates the library pages from the book markdown, API routes handle feedback/requests. Deploy on Vercel (or any Node host).
- **Data:** Postgres (Supabase or Neon) for feedback, requests, votes, thresholds. **Media:** EPUBs + audiobooks in object storage (S3/R2) behind a CDN — binaries never in git. **Book text** (all languages) stays as markdown in the repo: it IS the version control.
- **Build steps (agent-run):** markdown → EPUB (pandoc); markdown → audiobook (TTS per language); translation runs are pipeline jobs writing `production-books/<slug>/translations/<lang>/`.

---

## My Initial Reasoning (Preliminary — Not Decisions)

**On Q1 (framework):** The PI plan resolves the earlier objection. Forking PI and stripping its ~30-line system prompt gives full prompt control over a minimal, hackable base *and* keeps PI's interface for watching sub-agents — the best of both. So the real trade is now: **forked PI** (a working interactive agent loop + UI out of the box, at the cost of maintaining a fork and building the sub-agent plugin) vs **OpenAI Agents SDK** (cleaner orchestration primitives, but you build your own observability/UI). Both are viable; PI-fork gets you to a usable interactive tool faster, the SDK is the cleaner long-term library. Either way the **MVP defers this** — Hyperagent is the orchestrator for v0.

**On Q2 (style from a whole book):** You don't need the model to "hold" the whole book. The solution is a **distillation pass** that extracts a compact artifact capturing (1) the **method** — the argument structure, the reframes, the sequence — and (2) the **style** — voice, devices, recurring analogies. *That artifact is the "style guide" already planned.* **Separate METHOD from STYLE**, because the method (dismantling the perceived benefit so there's no feeling of sacrifice) is the real engine, not the prose. **Copyright flag:** extract method/voice and write *original* prose; do not reproduce substantial verbatim text. Ideas/methods aren't copyrightable; expression is — matters more given nonprofit public distribution. (This is the Book Analysis step now being built.)

**On Q3 (search):** Two separable things. (1) *Provider* — the "Grok feel" is xAI's proprietary index + X search; there's nothing underneath it to adopt, so replicating it means calling the xAI Live Search API directly (a production decision, not an MVP one). (2) *Depth* — an open-source deep-research framework solves a different problem: forcing an agent to search deep instead of shallow. For the MVP, the Exa + web + browser tools here are sufficient; keep the two research streams (lived experience vs scientific evidence) distinct.

---

## Considerations to Flag (So They're Not Lost)

- **Method ≠ style.** Easyway's power is its psychological *method* (remove the illusion of benefit so there's no feeling of sacrifice), not just its prose. Encode the method explicitly, separately from voice.
- **Non-shaming framing.** The method works precisely because it is *not* willpower- or shame-based. Generated books must avoid moralizing; reframe so the reader feels they're escaping a trap, not being lectured. Shame-based self-help tends to backfire.
- **Topic sensitivity.** Some targets (porn/masturbation, gaming) touch mental health; claims and framing need care, and the **goal should be explicit per book** (abstinence vs. moderation). Note: Easyway and The Freedom Model differ philosophically here (Freedom Model rejects the disease/abstinence-only model) — decide the stance per topic.
- **Copyright** — deferred. Out of scope for the analysis/MVP phase; revisit only before public distribution of generated books.
- **Evaluation.** "Reviewer accepts" needs explicit criteria — a rubric for what makes a chapter good (method fidelity, voice consistency, no repetition, does the argument land?). Buildable as a Hyperagent rubric and reused by the reviewer agent.

---

## Next Steps / Parking Lot

- Decide the **MVP target behavior** (gaming is the running example — a good first candidate).
- Run the **book analysis** for Easyway + The Freedom Model + the third book → produce editable method/style documents.
- Build the **distillation step** → produce a *method guide* + *style guide* artifact from the curated analyses.
- Define the **research skill** (which tools; the two streams).
- Define the **file/repo convention** (research doc, master plan, `chapters/`).
- Draft the **chapter-writer + reviewer prompts** and the review loop.
- Define the **chapter review rubric**.
- (Later) Verify tool specifics: xAI Live Search API, current open-source deep-research options, PI sub-agent plugin.
