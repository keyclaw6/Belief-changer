# Research Lead/Worker Protocol

## Mission

Fill ten behavior-specific raw-material banks with independent, source-traceable evidence. Research ends when every applicable community × persona × bank cell passes both its numeric floor and its qualitative test, never because of token use, cost, latency, or wall time. Do not write book prose.

## 1. Exact inputs and model gate

The agentic council uses these fresh-context handoffs and no others:

- an **architecture specialist** receives this prompt, the filled `production-books/<slug>/00-brief.md`, and one focused persona/community/science/investigation assignment;
- the **architecture lead** receives this prompt, the same brief, and the visible returned artifacts from its commissioned specialists;
- an **architecture reviewer** receives this prompt, the same brief, and the complete candidate architecture it must audit or regenerate;
- a **collection worker** receives this prompt, the same brief, and one focused assignment record from the approved architecture;
- the **synthesis lead** receives this prompt, the same brief, the approved research log, and accepted source packets from this run.

Do not provide any role with reference books, files under `analysis/`, calibration reference text, reference identity or paths, aggregate reference targets, run instructions, judge output, Allen Carr/Easyway derivatives, prose-pattern analysis, prior book prose, hidden chain-of-thought, or unrelated context from another agent. Visible council and worker artifacts from this run are allowed only in the handoffs above. The caller rejects an exact-input brief containing calibration/reference metadata before dispatch. If forbidden material appears, reject it and every dependent finding; its cells remain unfilled.

Research leads, workers, and research synthesis may use only these arms, at the runtime-reported highest reasoning mode:

| Arm | Allowed request model ID | Required top-reasoning configuration |
|---|---|---|
| DeepSeek V4 Pro | `deepseek/deepseek-v4-pro` | `xhigh` |
| MiniMax M3 | `minimax/minimax-m3` | reasoning enabled; no effort ladder |
| GPT-5.6 Luna | `openai/gpt-5.6-luna` | `max` |

The **caller**, not the language model inside the call, resolves endpoint metadata and verifies the exact request model ID and top reasoning configuration before dispatch. The caller gives every role the maximum completion/output allowance supported by the selected endpoint after input context; it never lowers reasoning or output allowance for cost, speed, or convenience. If a provider ceiling is reached, the caller continues the role agentically or selects a larger-capacity endpoint. Afterward the caller records the API response's actual model ID, request reasoning setting, usage, and cost in the returned artifact metadata, but those observations never rank or stop research. A role MUST NOT try to inspect invisible request metadata or treat lack of direct endpoint-metadata access as a blocker. The caller must not dispatch if it cannot perform this preflight, and must stop rather than substitute an unapproved model or lower mode. Opus is not a research model.

The caller is also the persistence boundary. A role may write files directly when its environment exposes repository tools; otherwise it returns complete artifact-ready Markdown blocks with their destination paths, and the caller persists them verbatim. Lack of direct filesystem access is not a blocker. Architecture specialists and reviewers SHOULD have source-retrieval capability when it can improve community/source discovery or verification; collection workers MUST have it and return their log events and packets as specified below.

## 2. Lead: build an agentic research council, then declare the assignment matrix

The lead is a research architect, not a lone summarizer. Before synthesis, the caller runs at least four separate fresh-context specialists—one each for persona discovery, community discovery, scientific-source mapping, and investigative-source mapping—on the allowed research arms at top reasoning with maximum supported output allowance. A separate adversarial architecture reviewer follows the lead synthesis. The lead and reviewer may request any number of additional agents whenever independent judgment or deeper coverage would improve quality.

The bank, matrix, log, and packet schemas are output/provenance contracts, not a prescribed chain of thought. Every agent chooses its own reasoning path, search strategy, exploration order, recursion, and additional subagent decomposition.

From the brief and council yield, identify **all materially distinct provisional personas**, segmented first by the function the behavior serves and second by materially different life situations. Three is a floor, not a ceiling. Never cap personas, communities, or assignments to save tokens, time, output length, or money; merge only personas that are substantively redundant. Identify the recovery/experience communities where each persona speaks in its own words and the independent scientific or investigative source families needed for Banks 7–8. Declare targets at least as strict as §4.

Before broad collection, write one row per planned community/source-scope × persona × bank cell at the top of `research/research-log.md`:

| Assignment ID | Worker ID | Community / source scope | Persona | Bank | Target | Query / search settings | Runtime model ID | Reasoning config | Max output allowance | Accepted items | Distinct sources | Qualitative verdict | Status / follow-up |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---|---|

An assignment may cover several rows only when it still names one focused community/source scope, an explicit persona scope, explicit bank slots and targets, its chosen query/search strategy, a worker ID, an allowed model configuration, and the endpoint's maximum output allowance. “Focused” defines subject responsibility only; it never limits reasoning, output, searches, time, spend, or the ability to commission more agents. Use `ALL` as the persona only for genuinely persona-neutral science; explain every `N/A`. Reject and focus any assignment missing a scope, persona, or bank.

In the numeric floors, a **source** means a distinct underlying URL/document, not a distinct community or worker. One community assignment can collect several independent URLs, but the lead should assign as many independent communities and workers as quality requires. Do not create duplicate rows merely to satisfy a numeric source floor, and do not suppress a valuable community merely to keep the matrix small. Return the complete artifact-ready persona list, matrix, and whatever validation notes are needed to preserve the council's judgment.

Every matrix row must be independently reconstructable: repeat the complete source scope, target, chosen query/search strategy, runtime request model ID, reasoning configuration, and maximum output allowance in that row. The `Bank` cell contains exactly one integer from `1` through `10`, never a range, list, or named sub-claim; repeat an assignment ID across separate rows when one worker covers several banks. Never use `same`, `as above`, ditto marks, or an implicit carry-forward. Each row names exactly one fixed community or one fixed scientific/investigative source family. Do not hide alternate, supplemental, fallback, or "if thin" communities in the scope or query; a follow-up source is a new declared row.

Treat the brief's non-goals as research-scope exclusions; do not mine a community whose defining condition is excluded from the book merely because some symptoms overlap. Any architecture role that cannot retrieve a named community labels it `CANDIDATE — VALIDATION REQUIRED`; it does not pretend to verify existence. Before worker dispatch, retrieval-capable specialists or the lead validate the canonical community URL and topical fit, replace invalid candidates, and change only validated rows to `READY`.

Before dispatch, a fresh top-reasoning research reviewer receives this prompt, the blind brief, and the complete candidate artifact. It audits persona coverage, source/community depth, query fit, blindness, reconstructability, model configurations, and every bank's qualitative sufficiency. If anything is weak, the reviewer returns a complete corrected artifact or commissions another specialist through the caller; it never asks the operator to patch rows by hand. Research workers run only after an independent reviewer says the architecture is genuinely strong enough.

Before returning any matrix, reject and replace every shorthand, out-of-scope population, multi-bank cell, vague source family, or assignment that bundles more than one focused community/source responsibility. Before collection, reject every named community still unvalidated or nonexistent.

## 3. Worker: collect provenance-preserving yield

Own the assigned community/source responsibility deeply. Follow promising leads and commission further agents whenever that improves evidence quality; record adjacent scopes as explicit follow-up assignments rather than silently blending provenance. Community work should reach first-person recovery or experience discussions; Banks 7–8 should use independent primary scientific or investigative sources where available. A search-result summary may guide discovery but is not evidence unless its exact returned excerpt is saved unchanged.

Every search, model call, accepted or rejected source capture, and URL revisit produces a chronological log event with its query and assignment IDs, tool/search settings, exact model/reasoning configuration, usage and cost when available, disposition and reason, output/source IDs, and cells filled.

Create one Markdown packet under `research/sources/` for each distinct accepted URL. Repeated visits enrich that packet and add log events; they never create another source file. Use this schema exactly:

```markdown
# <Source ID> — <Title>

- **Source ID:** <ID>
- **URL:** <canonical URL>
- **Title:** <page, thread, paper, transcript, or report title>
- **Retrieved (UTC):** <timestamp>
- **Community / source type:** <named community or source family>
- **Query ID:** <ID>
- **Assignment ID:** <ID>
- **Worker ID:** <ID>
- **Runtime model ID:** <exact ID>
- **Reasoning config:** <exact request setting>
- **Maximum output allowance:** <endpoint maximum after input context>
- **Search settings:** <engine, filters, date range, limits>
- **Research-log event IDs:** <IDs>
- **Disposition:** ACCEPTED

## Visit history

| Retrieved UTC | Assignment / worker | Query ID / query | Runtime model / reasoning / max output | Search settings | Capture IDs | Log event ID |
|---|---|---|---|---|---|---|

## Captured raw source text

### <Capture ID>
- **Retrieved (UTC):** <timestamp>
- **Source locator:** <page, section, paragraph, timestamp, post/comment URL, or equivalent>
- **Capture method:** <page text, transcript, PDF text, or exact search excerpt>

<unchanged retrieved excerpt or text>

## Evidence items

### <Evidence ID>
- **Evidence ID:** <ID>
- **Kind:** EXACT_QUOTE | INTERPRETATION
- **Text:** <evidence>
- **Capture ID:** <ID>
- **Locator:** <precise locator within the capture/source>
- **Persona tags:** <one or more>
- **Bank slots:** <one or more bank numbers>
- **Evidence grade:** SUPPORTED | MIXED | CONTESTED | N/A
- **Use / limits:** <what this supports and does not establish>
```

`EXACT_QUOTE` text must appear character-for-character in the named captured text and have a locator. If it cannot be verified, recapture it, convert it to an unquoted `INTERPRETATION`, or reject it. Interpretations still require supporting captured text and a locator. Never put quotation marks around an interpretation.

A worker returns its log events, complete source packets, accepted-source and verified-quote counts, filled matrix cells, usage/cost, rejected or unverifiable items with reasons, and remaining gaps. The lead validates and merges this yield; a worker's unsupported summary does not count.

## 4. Banks and Stage A coverage floor

The lead may raise but never lower these floors. Every selected persona must pass every applicable target; aggregate volume cannot hide a missing persona. Distinct URLs that reproduce the same underlying material count as one independent source.

| Bank | Raw material | Stage A numeric floor | Qualitative pass test |
|---|---|---|---|
| 1. Justification inventory | Stated reasons for the behavior, in community language | ≥3 items/persona from ≥2 sources | Top justifications are ranked; no credible common "but it gives me…" case is missing. |
| 2. Belief map | Beliefs beneath the reasons, including quitting costs and identity beliefs | ≥3 items/persona from ≥2 sources | Each persona has a ranked map with one evidence-backed keystone belief. |
| 3. Lived experience | Daily costs, lowest moments, failed attempts, relapse triggers, private arithmetic | ≥5 moments/persona from ≥2 sources | Each persona has several specific "that is exactly me" moments, not generic harms. |
| 4. Special moments | The behavior's most cherished or seductive scenes | ≥3 items/persona from ≥2 sources | The strongest scene per persona is vivid enough for later credit reassignment. |
| 5. Escape routes | Moderation, delay, substitution, exception, and "different for me" rationalizations | ≥3 items/persona from ≥2 sources | Every escape route found in failed-attempt stories has an exact community instance. |
| 6. Analogy candidates | Original images that perform a belief-change job | ≥2 original candidates for every expected move | Candidates fit the behavior's texture and clearly perform their named job; sourced and invented elements are distinguished. |
| 7. Mechanism and science | Loop, withdrawal/restlessness, escalation, self-created low, sensory description | Every candidate claim graded and backed by ≥2 independent sources, or explicitly `CONTESTED` | The inversion and sensory low can be stated concretely without overstating evidence. |
| 8. Villain dossier | How demand is engineered: mechanics, business model, recruitment, mythology | ≥3 independently sourced mechanisms | Engineered demand is demonstrated, not asserted. |
| 9. Community lexicon | Slang, euphemisms, self-descriptions, native phrasing | ≥8 terms/persona with frequency/context notes | A community member would accept the resulting reader voice as native. |
| 10. Freedom testimonies | Surprises after stopping, recovery texture, revelation moments, concrete gains | ≥3 items/persona from ≥2 sources | A moment of revelation and credible freedom trajectory can be predicted per persona. |

For Bank 6, cover at least the applicable jobs of mechanism inversion, false attribution, choice dissolution, borrowed energy/self-created low, recalibrated baseline, engineered trap, and the void/freedom question. An invented analogy must be labeled `INVENTED`, cite packets that ground its behavior-specific texture, and never be misattributed to a source.

## 5. Coverage and follow-up gate

After each pass, the lead updates accepted counts, distinct-source counts, and the qualitative verdict in every matrix row. Duplicate URLs, unverifiable quotes, rejected sources, unsupported interpretations, and evidence outside the assigned scope do not count.

Research may close only when:

- every applicable persona/bank row meets its declared numeric target;
- every row's qualitative verdict is `PASS`;
- every counted item traces to an accepted packet;
- every exact quote passes character-for-character verification;
- every source/call/search event and rejection is logged.

For each failing row, issue a fresh targeted follow-up assignment naming the exact community/source responsibility, persona, bank, missing quantity or quality, chosen search strategy, worker, model configuration, and maximum output allowance. Append it to the matrix and repeat the quality review. If evidence remains unavailable, report the unresolved row and keep research blocked; never fill it by invention.

## 6. Two-file synthesis

Only after the coverage gate passes, synthesize accepted packets into:

- `research/lived-experience.md`: Banks **1–6, 9, and 10**. Every bullet names its bank, persona tags, and supporting source IDs.
- `research/scientific-evidence.md`: Banks **7–8**. Every bullet names its bank, supporting source IDs, and `SUPPORTED`, `MIXED`, or `CONTESTED`.

Every source ID must resolve to its packet. Preserve material disagreements as `CONTESTED`; do not average them away. Bank 6 invented candidates still cite the packets grounding their behavior-specific texture. Remove or re-source any untraceable bullet. Framing remains blocked until both files pass this traceability check.

For model or orchestration comparisons, hold only the blind brief, substantive research objective, exclusions, and quality bar fixed. Every arm chooses its own search strategy, exploration order, tools, subagents, reasoning, and output depth. Record exact runtime IDs/configs, maximum output allowance, actual strategies, usage/cost, accepted sources, verified quotes, cells filled, and rejected/unverifiable yield. Rank only by research quality: community/persona coverage, source depth, quote fidelity, insight, scientific rigor, and synthesis quality. Cost, tokens, and latency are descriptive and never selection criteria.
