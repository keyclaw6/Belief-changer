## Context

The current research prompt defines ten useful banks but not an executable handoff: it does not assign focused workers, map their yield into source files/log rows/syntheses, or make sufficiency measurable. The calibration harness also requires fresh-context blindness, exact quote provenance, no Easyway-derived research, and model-arm accounting.

Three OSS candidates were inspected at current HEAD: LangChain `open_deep_research` (`408da44`), `Research-Agent` (`b30eed2`), and the smolagents UI fork (`9c3da13`). They provide generic fan-out or connectors, but none natively carries community × persona × bank-slot assignments, quote-to-raw-source verification, the factory file contract, or explicit top-reasoning payloads for all allowed research models. Adopting one now would add a framework and replace its central schemas, prompts, persistence, and output path before the prompt-level baseline exists.

## Goals / Non-Goals

**Goals:**

- Produce deep, community-grounded, source-traceable research through fresh focused workers.
- Make research completion a visible coverage decision rather than a token/time guess.
- Preserve the existing `research/sources/`, log, and two-synthesis file contract.
- Compare research models and later orchestration arms using reconstructable quality and yield evidence; usage/cost are descriptive only.
- Keep every research/planning sub-call blind to reference books and `analysis/`.

**Non-Goals:**

- Building a general research UI, crawler platform, vector database, or persistent agent service.
- Adding an OSS dependency before it beats the prompt-structured baseline.
- Writing final book prose during research or exposing community usernames in published prose.
- Changing the chapter writer's three-input anti-repetition contract.

## Decisions

### 1. Use prompt-structured lead/worker handoffs for run-001

The council uses at least four separate architecture specialists—persona discovery, community discovery, scientific-source mapping, and investigative-source mapping—with explicit blind handoffs. Specialists receive `prompts/research-agent.md`, the book brief, and one focus assignment; the architecture lead receives the same prompt/brief plus their visible returned artifacts; an independent reviewer receives the prompt/brief plus the complete candidate architecture; collection workers receive the prompt/brief plus one approved assignment; and the synthesis lead receives the prompt/brief plus the approved log and accepted packets. No role receives hidden reasoning or unrelated agent context. “Focused” bounds subject responsibility, never reasoning, output, searches, subagent count, time, or spend. The lead commissions missing-slot follow-ups and performs synthesis only after the coverage gate passes.

Each matrix row represents exactly one numeric bank and one fixed community or source family, and repeats its complete scope, target, query settings, model ID, and reasoning configuration. Shorthand, bank ranges, and conditional fallback communities are not reconstructable. Brief non-goals constrain community selection, so an excluded clinical or special population cannot silently become a proxy source for a general reader.

Coverage-source counts refer to distinct URLs/documents, not distinct communities or workers. The lead uses every materially distinct persona and every community that improves research quality. It does not duplicate assignments merely to satisfy a numeric source floor, but it never suppresses a useful persona, community, worker, or source to reduce output size or cost.

Because the first architecture call may have no web access, named communities are candidates rather than facts. A retrieval-capable lead validation pass resolves their canonical URLs and topical fit before any row becomes dispatch-ready. A separate fresh top-reasoning research reviewer audits and, when needed, fully regenerates the architecture before dispatch. Calibration identity, reference paths, and reference-derived targets remain operator/run metadata and never enter the exact-input brief.

This is H-010's own-build arm. H-011 does not adopt an OSS framework for run-001: the audited candidates require substantial forks and bring unrelated UI, deployment, RAG, export, or cloud stacks. Useful agentic ideas—parallel fan-out, specialist delegation, adversarial review, and URL ledgers—remain eligible when they improve research quality.

### 2. Make the existing files the orchestration boundary

No database or new stable artifact is introduced. Each distinct URL becomes one descriptive file under `research/sources/`; repeated visits enrich that file rather than creating duplicates. Each source packet records source ID, URL, title, retrieval date, community/source type, query/assignment ID, model and reasoning config, captured raw excerpt, and evidence items. Each evidence item separates exact quotation from interpretation and carries persona tags, bank slots, and a locator.

The research log starts with the assignment/coverage matrix and appends one row per search/call/source capture, including model config, usage/cost when available, output files, and accept/reject status. This preserves replayability without making orchestration code the source of truth.

The caller performs endpoint-metadata preflight and persists returned artifact blocks. Bare model calls cannot inspect their own request payload or mutate the caller's filesystem, so those are caller responsibilities rather than research-role completion gates. The actual model ID returned by the endpoint, request reasoning setting, usage, and cost are added from the API response; research content is persisted verbatim.

### 3. Treat quote exactness as a gate

A quote is usable only when it appears verbatim in the captured source excerpt or archived raw text. Search-result summaries may guide discovery but are not quote evidence unless their returned excerpt is saved unchanged. Unverifiable wording is either recaptured from the page or recorded as an interpretation without quotation marks. Community identities are not needed: source context is retained locally, while final prose paraphrases/anonymizes.

### 4. Map all ten banks into the two downstream syntheses

`lived-experience.md` carries Banks 1–6, 9, and 10; `scientific-evidence.md` carries Banks 7–8. Every synthesized bullet includes source IDs, persona tags where applicable, and its bank number. Scientific bullets retain SUPPORTED/MIXED/CONTESTED. This lets framing and planning consume every bank without widening their exact input sets.

### 5. Declare numeric coverage before research begins

The lead may raise targets, but the Stage A default floor is:

- Banks 1–5 and 10: at least three source-backed items per persona from at least two distinct sources; Bank 3 requires five lived moments per persona.
- Bank 9: at least eight source-backed community terms per persona, with frequency/context notes.
- Bank 6: at least two original candidates for every belief-change move the plan expects; sourced and invented analogies are labeled separately.
- Bank 7: every candidate scientific claim has an evidence grade and at least two independent sources, or is explicitly CONTESTED.
- Bank 8: at least three independently sourced mechanisms showing how demand is engineered.

All selected personas must clear their applicable rows. Three personas are a floor, not a ceiling; the lead and independent reviewer include every materially distinct function or life-situation pattern. A numeric floor does not override the prompt's qualitative sufficiency tests; both must pass.

### 6. Keep model arms explicit and at top reasoning

Allowed research arms are DeepSeek V4 Pro (`xhigh`), MiniMax M3 (reasoning enabled; no effort ladder reported), and GPT‑5.6 Luna (`max`). Each receives the maximum endpoint-supported completion/output allowance and may use as many agentic follow-ups as quality requires. Exact runtime IDs, request configuration, maximum output allowance, actual strategy, usage, accepted source count, verified quote count, bank/persona cells filled, and rejected/unverifiable items are recorded. Arm comparisons hold the blind brief, substantive objective, exclusions, and quality bar fixed while each model chooses its own search path, tools, and subagents. Rank community/persona coverage, source depth, verified quotes, belief-changing insight, scientific rigor, and synthesis quality. Cost, tokens, and latency never affect selection.

### 7. Preserve calibration-specific commit and blindness behavior

Research, framing, planning, review, and writing never receive reference text, `analysis/`, or judge outputs. The style guide remains the only reference-derived carrier. Calibration chapters are not committed individually to `main`; the complete reconstructable run is committed on `calibration-lab` per HARNESS §6.

## Risks / Trade-offs

- **Community pages are deleted, blocked, or JS-only** → save the retrieved excerpt and metadata immediately; use browser capture or another independent source before accepting a quote.
- **More workers increase duplicate yield** → one-file-per-URL merging plus the lead's coverage matrix makes duplicates visible and non-counting.
- **Numeric quotas reward filler** → require distinct sources, exact evidence, and the existing qualitative sufficiency test for every bank.
- **Search plugins return shallow snippets** → assign community-specific follow-up workers and reject snippets that cannot support the claimed slot.
- **Prompt orchestration needs more independent judgment** → add fresh specialist and adversarial-review agents; adopt an OSS agent framework only if it improves research depth or reliability without replacing model judgment.
- **Model-arm comparisons confound search breadth and synthesis** → hold the blind objective and quality bar constant, record each arm's freely chosen strategy, and report raw-yield and synthesis measures separately.

## Migration Plan

1. Update the delta specs and validate the change strictly.
2. Rewrite the research prompt and research templates to encode the lead/worker/source/coverage contract.
3. Remove forbidden reference inputs and Opus plan-review requirements from planning assets; make the brief an explicit framing input.
4. Run an unrestricted quality-first H-010/H-009 research pilot, record failures, and correct the agentic prompt/handoffs before full run-001 research.
5. Commit and push the blinded brief, prompt, and workshop schemas; bootstrap calls remain under `calibration/pilots/` and contribute no Stage A evidence.
6. Create and execute run-001 through the unchanged downstream file contract. Rollback is a revert of the pre-run contract commit; no stored data migration is required.
