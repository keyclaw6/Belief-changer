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
- **Every part built by agents — and run by agents.** Research, writing, review, translation, narration, publishing — and the organization itself: feedback triage, reader correspondence, site telemetry and reporting, page deployment. Agents are the project's employees and maintainers from the start; humans set direction and hold the quality bar. This is how a tiny team helps millions.

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

## Adopted Plan — Build & Launch (DECIDED 2026-07-10)

The Build & Launch Proposal (five-layer architecture: factory → library → platform → evolution engine → quality; sequenced launch L0–L3) is **adopted with founder amendments** and recorded here. Deliberately **not** openspec changes yet: *prove the factory first; spec changes land stage-by-stage as each part is actually built.*

**The five layers (adopted):**
1. **Factory** — the book pipeline (research → framing → master plan → chapters), a file-contract state machine in this repo; any competent agent environment can run it from files alone.
2. **Library** — books as versioned markdown (golden copy = English); EPUB (pandoc), audiobook (TTS), translations as pipeline jobs that translate + freeze the §B8 book sheets (one frozen mantra translation per language) before chapters.
3. **Platform** — static site from book markdown (every chapter an indexable page; read/download/listen with no signup, no tracking), Postgres for feedback/requests/votes, object storage + CDN for binaries.
4. **Evolution engine** — the three loops as scheduled agent jobs: feedback → research banks → revisions; requests → new book at threshold (contributed experiences seed the lived-experience bank); splitting on persona seams.
5. **Quality** — laddered evals (objective scripts → blind judge panels), outcome surveys once live, three learning tiers (book banks → style guide [founder-gated] → catalog).

**PRIME FOCUS (before all else): the factory must reliably produce books of real Easyway quality — the universal Easyway-book creation machine.** Everything else (site, loops, languages, launch) waits on this proof.

**The calibration program** — prove the factory against ground truth by generating a book Carr already wrote, and tuning until parity:
- **Target:** a covered behavior so the real book is the benchmark. **Primary candidate: sugar/eating** (*Good Sugar Bad Sugar* is already in `analysis/reference-books/` with its prose patterns extracted in `analysis/sugar-prose-patterns.md`). *Smoking* is the canonical alternative if the founder supplies the text. **Caffeine** (also in-repo, analyzed) is **reserved untouched as the Stage C generalization target**.
- **Stage A — chapter parity (cheap loop):** generate chapters 1–3 of the calibration book; blind-compare against the real book's chapters 1–3; diagnose, amend, regenerate. Most tuning iterations happen here.
- **Stage B — full-book parity (expensive loop):** generate the whole book; evaluate length, chapter arc, flow, mantra schedule across the book, the ending; iterate to parity — then push to surpass (win-rate > 50% on the click/flow dimensions, judged blind).
- **Stage C — universality gate:** a fresh factory run on the second covered topic (caffeine) with **zero topic-specific tuning**; parity without new amendments proves the "any belief" machine. Only then do novel-topic books proceed.
- **Evaluation stack:** (a) **objective scripts** — word/chapter counts vs target, mantra-schedule compliance (frozen wording appears on schedule), within-book verbatim-repetition detector (the anti-repetition law), n-gram overlap vs the real book (originality guard), voice metrics from style guide Part B; (b) **blind comparative judge panels** — fresh-context judges score unlabeled ours-vs-real chapter pairs on: the click, flow, warmth/non-shaming, mantra discipline, absence of generic-self-help smell; position-swapped, multi-judge; (c) **replicated native judging** — the current Stage-A baseline uses two fresh same-model Sol-ultra replica identities, with both A/B orders collapsed within identity; this is independent replication, not cross-family evidence; (d) founder spot-reads as an optional anchor, never a required gate.
- **Amendment protocol:** every run = a run manifest (writer/judge models, prompt + skill versions, parameters) + a run report, committed. The tuner amends method assets (style guide, plan templates, writer/reviewer prompts) on **calibration branches**; the canon style guide on `main` stays founder-approved — winning amendments merge in founder-reviewed batches. Each judged gap maps to the method asset that owns it.
- **Environments:** the repo is the state machine, so the loop runs anywhere. **Operator: the founder's GPT 5.6 Sol environment runs all calibration runs** (run-001 onward) from `PROGRAM.md` (root) — the loop was rebuilt 2026-07-12/13 after the run-001–014 autopsy (`PROGRAM.md` + `loop/` + `scripts/loop/` + `scripts/eval/`: the fixed operator loop, its config/results/learnings, the reference-anchored rubric judge, and the objective eval suite). Hyperagent built and maintains the loop and is the escalation point. **Model access is route-restricted:** H-F01 uses OpenRouter only for the six fixed Muse Spark 1.1 Thinking chapter calls, with no fallback; DeepSeek research also uses OpenRouter. GPT/OpenAI, Gemini, Grok, planning, reviewing, auditing, and judging never use it. **H-F01 writer FIXED: Muse Spark 1.1 Thinking with high reasoning, temperature `0.7`, and `max_tokens: 16000`, identically across control and treatment**; the current product judges are fresh native GPT 5.6 Sol subagents at `ultra`, while other non-writer arms require an authorized native or direct route. **Doctrines (founder, 2026-07-10):** (1) *prompts over determinism* — LLMs underestimate LLM intelligence, incl. their own; optimize with prompts and clever handoffs, deterministic code only for measurement/gates or after an autopsied prompt-level failure; (2) *research goes deep* — structured multi-subagent decomposition into recovery/experience communities (single-long-prompt is the baseline to beat; `prompts/research-agent.md` carries the depth doctrine and the 10× floors); (3) *failure autopsies required* — nothing REFUTED without an examined why; (4) *MLflow all-or-nothing* — if adopted, full depth (tracing, params/metrics/artifacts, prompt registry, comparison UI). **The operator executes the loop and has no authority over its design** (`PROGRAM.md`, the judge rubric, scoring, and thresholds are frozen; grievances go to the harness-debt list in `loop/learnings.md`) — the run-001–014 autopsy (2026-07-12) showed operator design-authority converts product time into process time. Founder gates remain on canon `main` and method integrity — now defined as **Carr-fidelity**: the factory matches Allen Carr's own practice (including his full-force scares, commands, and certainty) before any house twist is applied.

**Q1 CLOSED (2026-07-10, revised from the proposal):** the factory becomes a **standalone custom harness — its own product** — built on the OpenAI Agents SDK or a PI fork (base chosen after the first calibration runs reveal the real requirements). Not required for the first runs: Hyperagent + the GPT 5.6 environment carry the loop until the harness product stabilizes. Rationale: the auto-research/calibration loop ultimately needs an environment we fully control — no host system prompt underneath — stable and usable outside Hyperagent.

**Agent-run organization (decided principle):** the project is operated by agents as its employees/maintainers from the get-go — site telemetry reports to an agent; feedback handling, reader email, and page deployments are agent-run; humans set direction and hold the gates. This is a scale requirement, not a flourish.

**Translation & revision QA (decided — supersedes the proposal's community-reviewer idea):** **no human review layer for translations, at any scale.** Agents translate and agents QA (frozen mantra sheets per the languages spec); reader feedback surfaces real errors and fixes ship fast. The English **golden copy revs frequently** as personal experiences accumulate — **speed is our advantage** — and translations follow the golden copy automatically. *(Flagged tension to resolve when we get there: the publishing spec's founder gate vs high-frequency multi-language revisions — likely resolution: gate English golden versions; translations auto-follow. Needs a spec change when the translation pipeline is built.)*

**Sequencing:** `production-books/quit-porn/` is **paused at framing** until Stage C passes; its research stays valid and it becomes the first novel-topic book of the proven factory.

**Deferred decisions** (not before an English calibration book exists): public name/domain, beta outreach identity, donations, age-gating, TTS voices, request-loop thresholds, analytics stance confirmation.

---

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

**Q1 — Orchestration framework — CLOSED (2026-07-10).** Decided in the Adopted Plan above: a standalone custom harness built as **its own product**, on the OpenAI Agents SDK or a PI fork; the base is picked after the first calibration runs reveal the real requirements. Original candidates kept for history:
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

*(Superseded by the Adopted Plan at the top of Part II — kept for history.)*

- Decide the **MVP target behavior** (gaming is the running example — a good first candidate).
- Run the **book analysis** for Easyway + The Freedom Model + the third book → produce editable method/style documents.
- Build the **distillation step** → produce a *method guide* + *style guide* artifact from the curated analyses.
- Define the **research skill** (which tools; the two streams).
- Define the **file/repo convention** (research doc, master plan, `chapters/`).
- Draft the **chapter-writer + reviewer prompts** and the review loop.
- Define the **chapter review rubric**.
- (Later) Verify tool specifics: xAI Live Search API, current open-source deep-research options, PI sub-agent plugin.
