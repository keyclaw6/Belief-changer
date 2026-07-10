# Deep-research bootstrap pilot

This pilot runs before the immutable `run-001` baseline. Its purpose is to make the research handoff executable and to version the resulting generic contract. None of its calls, outputs, or preliminary arm observations count as Stage A evidence.

## RP-000 — lead handoff preflight (failed)

- **Call ID:** `gen-1783695448-rncCEIxtMXRtDVRaHkwv`
- **Requested model / reasoning:** `openai/gpt-5.6-luna` / `max`
- **Actual model:** `openai/gpt-5.6-luna-20260709`
- **Exact inputs:** `prompts/research-agent.md` at `248a6b4` + `production-books/quit-sugar/00-brief.md`
- **Web/search:** none; lead planning call
- **Usage:** 2,709 prompt + 2,276 completion = 4,985 tokens; 2,070 reasoning tokens
- **Cost:** $0.0170415
- **Yield:** zero personas, assignments, sources, quotes, or filled cells
- **Disposition:** `ERROR — HANDOFF CAPABILITY CONTRACT`

### Returned content

> Research status: BLOCKED before collection. No research artifacts or accepted evidence were produced. The role reported that it could not inspect endpoint metadata, retrieve sources, write repository files, or merge worker returns.

### Autopsy

The endpoint and reasoning configuration had already been verified by the caller, and source retrieval was intentionally unnecessary for the lead's pre-collection matrix. The generic prompt nevertheless assigned invisible request-metadata inspection and repository persistence to the submodel. A bare OpenRouter completion therefore interpreted unavailable tools as a legitimate stop condition. This was not a Luna research-quality result and does not count toward H-009 or H-010.

The H-026 correction makes the caller own endpoint preflight, response metadata, and persistence while roles return artifact-ready blocks. The identical lead call is rerun before any collection; no source or quality conclusion is drawn from RP-000.

## RP-001 — corrected Luna lead, 6.5k cap (failed)

- **Call ID:** `gen-1783695731-XQzjvyIwDCUjI2cuEYK0`
- **Requested / actual model:** `openai/gpt-5.6-luna` `max` / `openai/gpt-5.6-luna-20260709`
- **Exact inputs:** corrected `prompts/research-agent.md` + the same brief
- **Usage / cost:** 2,915 prompt + 6,500 completion, all 6,500 completion tokens reported as reasoning; $0.042643
- **Yield:** zero visible content; `finish_reason=length`
- **Disposition:** `ERROR — COMPLETION CAP EXHAUSTED BY REASONING`

The correction changed the failure mechanism: reasoning summaries show the model constructing personas, communities, science families, and matrix rows rather than refusing for missing tools. The output cap was nevertheless consumed before any artifact appeared.

## RP-002 — corrected Luna lead, 20k cap (failed)

- **Call ID:** `gen-1783695847-YEBAZt4J8HtjVkdPJIwm`
- **Requested / actual model:** `openai/gpt-5.6-luna` `max` / `openai/gpt-5.6-luna-20260709`
- **Exact inputs:** identical to RP-001
- **Usage / cost:** 2,915 prompt + 20,000 completion, all 20,000 completion tokens reported as reasoning; $0.1202942
- **Yield:** zero visible content; `finish_reason=length`
- **Disposition:** `ERROR — REPEATED UNBOUNDED REASONING`

### RP-001/RP-002 autopsy and decision

The second corrected attempt tripled the completion headroom and reproduced the same zero-artifact mechanism. At the time, the operator stopped the broad Luna retry and moved the lead role to DeepSeek. The founder's later quality-only correction invalidates that economy-driven stop: these calls are execution autopsies, not model-quality evidence, and Luna must receive an unrestricted maximum-allowance architect or worker trial before H-009 is judged.

## RP-003 — DeepSeek lead draft (rejected at matrix gate)

- **Call ID:** `gen-1783696077-luPzjMU4bFe8vInL6ZsD`
- **Requested / actual model:** `deepseek/deepseek-v4-pro` `xhigh` / `deepseek/deepseek-v4-pro-20260423`
- **Provider / fingerprint:** Novita / `fp_9954b31ca7_prod0820_fp8_kvcache_20260402`
- **Exact inputs:** corrected research prompt + the unchanged brief
- **Usage / cost:** 3,030 prompt + 18,176 completion = 21,206 tokens; 14,894 reasoning tokens; $0.02368591008
- **Raw yield:** five provisional personas and 42 community/persona/bank rows; no source collection
- **Accepted yield:** zero rows; pre-collection matrix gate failed
- **Disposition:** `REJECTED — NON-RECONSTRUCTABLE / OUT-OF-SCOPE`

### Gate evidence and autopsy

The draft repeatedly replaced required source, query, model, and reasoning fields with `same`. Those cells cannot reconstruct a worker dispatch independently. It also chose an eating-disorder community for the evening persona even though eating-disorder treatment is a brief non-goal, and it named several communities without validating that they exist. The lead had optimized for compactness and topical resemblance rather than the protocol's replayable row contract.

H-027 makes the rule explicit in the generic research prompt: every row repeats every dispatch field, named communities must be verified, and non-goals exclude proxy populations. The exact prompt+brief lead call is rerun; the rejected draft is not persisted into the book workshop and no worker is dispatched from it.

## RP-004 — DeepSeek corrected lead transport failure

- **Call ID:** `gen-1783696511-yPU5nz0tpNX9plQEC0Ez`
- **Requested / actual model:** `deepseek/deepseek-v4-pro` `xhigh` / `deepseek/deepseek-v4-pro-20260423`
- **Usage / billing:** 3,651 prompt + 1,186 reasoning tokens; OpenRouter reported total cost $0 with $0.00362247312 upstream cost
- **Response state:** `finish_reason=null`, `native_finish_reason=null`, `content=null`
- **Disposition:** `ERROR — INCOMPLETE PROVIDER RESPONSE`; one identical retry allowed

No prompt or research conclusion is drawn from an incomplete transport response.

## RP-005 — DeepSeek corrected lead retry (rejected at matrix gate)

- **Call ID:** `gen-1783696586-07rmgwG6Tl3jIFkQtgx5`
- **Requested / actual model:** `deepseek/deepseek-v4-pro` `xhigh` / `deepseek/deepseek-v4-pro-20260423`
- **Usage / cost:** 3,155 prompt + 23,683 completion = 26,838 tokens; 20,582 reasoning tokens; $0.028693619808
- **Raw yield:** six personas and 14 compact matrix rows
- **Accepted yield:** zero rows; pre-collection matrix gate failed
- **Disposition:** `REJECTED — GROUPED BANKS / MUTABLE SOURCE SCOPES`

### H-027 refutation autopsy

The draft removed all `same` shorthand and avoided excluded clinical populations, so that part of the lever worked. It nevertheless placed Banks `1–5, 9, 10` in single cells, even though each bank requires its own accepted-item/source/verdict counters. It also embedded `if thin`, `supplement`, or additional communities inside queries and used broad labels such as “investigative journalism, academic,” so the worker's source boundary could change after dispatch. The prompt had required repeated fields but had not said that a bank cell must be one integer or that fallbacks must become new rows. H-027 is therefore refuted as written after an examined mechanism, and H-028 applies the narrower generic correction. No RP-005 row is dispatched.

## RP-006 — MiniMax lead call aborted on blindness discovery

- **Requested model / reasoning:** `minimax/minimax-m3` / reasoning enabled (endpoint exposes no effort ladder)
- **Inputs:** H-028 prompt state + brief blob `d09e50336379966b7ecd4813bba21371c011d7cd`
- **Response:** caller interrupted before a response or call ID was returned
- **Usage / cost:** unavailable
- **Disposition:** `ABORTED — BLINDNESS CONTAMINATION`

An independent audit found that the supposedly exact-input brief named the calibration reference and its repository paths and carried a reference-derived architecture target. The call was interrupted immediately. This and every earlier RP call received that same brief blob, so none is valid pipeline research or an H-009/H-010 quality observation. Their value is limited to handoff/tool behavior and failure diagnosis.

## Request-state reconstruction

All calls used exactly one user message containing the named research prompt followed by the named brief, no system message, and no web plugin for lead planning.

| Calls | Research-prompt state | Brief blob | Request config |
|---|---|---|---|
| RP-000 | committed blob `1a2bd486f90663790aa88ec0bee5e9cbff85da57` (`248a6b4`) | `d09e50336379966b7ecd4813bba21371c011d7cd` | Luna `max`, `max_tokens=6500` |
| RP-001 | RP-000 + H-026 caller/persistence paragraphs and exact allowed request IDs | same | Luna `max`, `max_tokens=6500` |
| RP-002 | same as RP-001 | same | Luna `max`, `max_tokens=20000` |
| RP-003 | same as RP-001 | same | DeepSeek `xhigh`, `max_tokens=30000` |
| RP-004/RP-005 | RP-003 + H-027 independently repeated fields/non-goal rule | same | DeepSeek `xhigh`, `max_tokens=30000` |
| RP-006 | blob `fcb1423db96b5929fcc3c2d23ed91e63ab282c9f` (adds H-028 one-bank/one-scope rule) | same | MiniMax reasoning enabled, `max_tokens=30000` |
| RP-007 | blob `2178b2e06749e5e465178c984eabd8113ae5c72c` (`ccbee2d`) | blob `a272394a8fd32787db145ebcb3327a8ba9094c0c` (`ccbee2d`) | MiniMax reasoning enabled, `max_tokens=30000` |
| RP-008 | blob `a58dcb0fca028a63727a31b8e1b437ffa853b360` (`5b1f217`) | blob `a272394a8fd32787db145ebcb3327a8ba9094c0c` (`5b1f217`) | DeepSeek `xhigh`, `max_tokens=30000` |
| RP-009 | same as RP-008 | same | DeepSeek `xhigh`, `max_tokens=60000` |

The exact uncommitted prompt additions are preserved in H-026/H-027/H-028 and the final versioned prompt diff. The API key was supplied only through the secure environment and is absent from all artifacts.

## Verbatim failure evidence

RP-000 returned: “Research status: BLOCKED before collection” and “No research artifacts or accepted evidence were produced,” then cited unavailable endpoint metadata, web retrieval, and filesystem capability.

RP-003 included rows such as:

> `| A‑1‑2 | W1 | same | P1 | 2 | ≥3 items from ≥2 sources | same | same | same | ... |`

RP-005 included a grouped bank cell and mutable scope:

> `| A-003 | W03 | Reddit r/loseit | 3. Mindless Grazer | 1–5, 9, 10 | ... | ... If thin, supplement with r/productivity or r/getdisciplined. ... |`

Those excerpts directly support the recorded matrix-gate autopsies; no rejected draft was promoted to the book workshop.

RP-007's visible response states:

> `19 assignments, 91 rows.`

Its plan then enumerates 12 lived-community assignments—two communities for each of six personas, seven banks per assignment—plus seven Bank 6–8 assignments. This is the raw basis for the Cartesian-growth diagnosis below.

## RP-007 — clean MiniMax lead (rejected: output-cap matrix explosion)

- **Call ID:** `gen-1783697696-Q9YjzSVhZnKRHPJSDLfz`
- **Requested / actual model:** `minimax/minimax-m3` reasoning enabled / `minimax/minimax-m3-20260531`
- **Provider:** Novita
- **Exact committed inputs:** `prompts/research-agent.md` and blinded brief at `ccbee2d`
- **Usage / cost:** 3,309 prompt + 30,000 completion = 33,309 tokens; 28,286 reasoning tokens; $0.03696534
- **Finish:** `length`
- **Raw visible yield:** six provisional personas, candidate source list, and a plan for 19 assignments / 91 matrix rows; the matrix itself was truncated
- **Accepted yield:** zero rows
- **Disposition:** `REJECTED — INCOMPLETE ARTIFACT / CARTESIAN MATRIX`

### RP-007 failure autopsy and H-029 correction

The prompt's atomic-cell correction worked in the model's plan: it explicitly intended one bank per row and no shorthand. But it interpreted each bank's `≥2 sources` floor as requiring two independent community assignments for every persona/bank. Six personas × two communities × seven lived banks, plus science/analogy rows, became 91 planned rows. The 30k top-reasoning call ended before the matrix was visible, so nothing was dispatchable. H-029 then tried to shrink the architecture; that lever is now retired because the founder requires quality-first persona/community breadth and maximum model allowance.

## RP-008 — clean DeepSeek lead (rejected: reasoning exhausted artifact budget)

- **Call ID:** `gen-1783698551-SjgiZf0QsEuCCb2mjeie`
- **Requested / actual model:** `deepseek/deepseek-v4-pro` `xhigh` / `deepseek/deepseek-v4-pro-20260423`
- **Provider:** StreamLake
- **Exact committed inputs:** prompt blob `a58dcb0fca028a63727a31b8e1b437ffa853b360` and blind-brief blob `a272394a8fd32787db145ebcb3327a8ba9094c0c` at `5b1f217`
- **Usage / cost:** 3,481 prompt + 30,000 completion = 33,481 tokens; 27,118 reasoning tokens; $0.033137082
- **Finish:** `length`
- **Raw visible yield:** four persona IDs, 22 complete atomic rows, and one partial row; output cuts off inside Persona D's Bank 2 row
- **Accepted yield:** zero rows because the matrix and validation notes are incomplete
- **Disposition:** `REJECTED — INCOMPLETE ARTIFACT / REASONING-BUDGET COLLISION`

### Verbatim shape evidence

The response began `# Research Log — Quit Sugar (Pre-collection Matrix)` and emitted rows such as:

> `| A-001 | W1 | Reddit r/sugarfree | A | 2 | ≥3 items, ≥2 sources | ... | deepseek/deepseek-v4-pro | xhigh | ... | CANDIDATE — VALIDATION REQUIRED |`

All visible rows keep one numeric bank and one fixed scope and repeat their query/model/reasoning fields. The fourth persona appears as `D-001`; no second community, grouped bank, shorthand, fallback, or excluded population appears in the returned artifact.

### RP-008 failure autopsy and H-030 correction

H-029 removed RP-007's Cartesian growth: the response used four personas and one primary community. The provider nevertheless counted internal reasoning and visible artifact against the same 30k completion cap. With 27,118 reasoning tokens, only about 2,882 tokens remained for the matrix, which ended mid-row with `finish_reason=length`. The artifact cannot be dispatched or operator-repaired. The later founder correction establishes that both this 30k cap and H-030's 60k cap were invalid experimental constraints; future calls use the endpoint maximum and agentic continuation.

## RP-009 — clean DeepSeek lead (rejected: complete-looking invalid matrix)

- **Call ID:** `gen-1783699118-9RUjVancYz8aWiHWJOrd`
- **Requested / actual model:** `deepseek/deepseek-v4-pro` `xhigh` / `deepseek/deepseek-v4-pro-20260423`
- **Provider:** StreamLake
- **Exact committed inputs:** prompt blob `a58dcb0fca028a63727a31b8e1b437ffa853b360` and blind-brief blob `a272394a8fd32787db145ebcb3327a8ba9094c0c`; identical to RP-008
- **Usage / cost:** 3,481 prompt + 15,970 completion = 19,451 tokens; 12,105 reasoning tokens; $0.018489762
- **Finish:** `stop`
- **Raw visible yield:** four personas, 31 matrix rows, and validation notes
- **Accepted yield:** zero rows because the matrix fails its own dispatch contract
- **Disposition:** `REJECTED — NON-RECONSTRUCTABLE / UNRESOLVED CONFIG / MULTI-SCOPE`

### Verbatim gate evidence

Most later lived rows contain only a query expression, unlike the first row's fixed sort/time/limit settings:

> `| A1 | W1 | Reddit r/sugarfree | Afternoon Slumper | 2 | ≥3 items, ≥2 sources | "sugar belief" OR ... | ... | CANDIDATE |`

The Bank 8 scope combines an archive, books, a lecture, and an industry source in one cell. Bank 6 is unresolved:

> `| A7 | W7 (later) | Synthesis of collected source packets (Banks 1-5) + inventive reasoning | ALL | 6 | ... | N/A ... | TBD | TBD | ... |`

The response's own validation note nevertheless says, `All rows are independently reconstructable—no ditto marks or implicit carry-forwards exist.`

### RP-009 failure autopsy and founder correction

The 60k cap removed RP-008's immediate truncation, but RP-009 still produced a false-positive self-audit. More importantly, the founder corrected the experiment's objective: the 30k and 60k limits were invalid because research quality—not tokens, cost, speed, or latency—is the only optimization target. These capped calls remain reconstructable execution autopsies but do not rank model quality.

No deterministic research validator, renderer, or state machine was implemented or committed. H-031 instead uses unrestricted top-reasoning persona, community, science, investigation, and adversarial-review subagents, followed by a lead that regenerates the complete architecture. Future calls receive the selected endpoint's maximum supported completion/output allowance; provider ceilings trigger agentic continuation or a larger-capacity endpoint, never task compression.

## RP-010 — first quality-first persona council pass (rejected: retrieval/synthesis disconnect)

### Transport and request reconstruction

All attempts used prompt blob `ca55eca9b759b69fbabb71410c74c646e6cd286f`, blind-brief blob `a272394a8fd32787db145ebcb3327a8ba9094c0c`, persona-focus blob `56a7af0303a918b5208d5534f1a09454834ad047`, and boundary commit `981b0a6`.

- OpenRouter beta `openrouter:web_search`/`web_fetch` server tools returned `404 Server tool request failed` before provider selection; search-only reproduced it. No model ran and no cost accrued.
- The deprecated-but-proven Exa web plugin with a requested one-million-token completion allowance returned `402`: the disposable key could pre-authorize about 416k completion tokens after web context. The caller rounded that down to 400k with continuation on `length`. The later founder correction rejects even that conservative rounding; RP-010 remains a failed execution diagnostic, and subsequent calls request the exact per-call hard allowance reported by the endpoint/key.
- Parasail then returned an upstream `429` before inference. The identical request moved to WandB's 1,048,576-token DeepSeek endpoint.

### Persona architect call

- **Call ID:** `gen-1783701212-0zysaeUKO565IUOjiaXp`
- **Requested / actual model:** `deepseek/deepseek-v4-pro` `xhigh` / `deepseek/deepseek-v4-pro-20260423`
- **Provider:** WandB
- **Request:** `max_tokens=400000` with continuation-on-length; Exa web plugin `max_results=25`; one message containing only the committed prompt, blind brief, and persona focus
- **Usage / cost:** 7,151 prompt + 12,405 completion = 19,556 tokens; 1,020 reasoning tokens; $0.07561214
- **Finish:** `stop`
- **Runtime metadata:** `calibration/pilots/council/persona-architect-meta.json`; the rejected output and raw annotations were later removed by RP-016's source-policy remediation
- **Disposition:** `REJECTED — UNVERIFIED / FABRICATED-LOOKING SOURCE CLAIMS`

The visible artifact proposed six thoughtful functional personas, but its 25 raw Exa annotations were dominated by unrelated current news and sports. None of the claimed Reddit/Medium community sources appeared in those annotations. The artifact nevertheless said its distinctions were grounded in captured, verifiable quotations and supplied plausible-looking URLs and verbatim-looking excerpts. Accepted source/quote/cell yield is zero.

### Independent reviewer call

- **Call ID:** `gen-1783702896-rzeIlyBzlBiSivQSn1gz`
- **Requested / actual model:** `minimax/minimax-m3` reasoning enabled / `minimax/minimax-m3-20260531`
- **Provider:** Parasail
- **Request:** `max_tokens=400000` with continuation-on-length; exact prompt + blind brief + complete candidate + raw annotations
- **Usage / cost:** 19,315 prompt + 11,094 completion = 30,409 tokens; 4,111 reasoning tokens; $0.01907658
- **Finish:** `stop`
- **Runtime metadata:** `calibration/pilots/council/persona-architect-review-meta.json`; the derivative review prose was later removed by RP-016
- **Verdict:** `RETURN FOR CORRECTION + COMMISSION A RETRIEVAL-VALIDATION SPECIALIST`

The reviewer independently found that the raw annotations had no overlap with the artifact's source URLs, no packet-backed quote existed, and collection must remain blocked. It also identified clinical-scope and persona-overlap questions for later evidence, then requested retrieval specialists rather than operator repair.

### H-032 correction

The failure mechanism is a retrieval/synthesis disconnect: one broad plugin query is not deep research, and the model filled the evidence vacuum with plausible prose. The next council version separates intelligent roles: a scout commissions focused retrieval subagents; those agents return exact URLs/excerpts; the specialist synthesizes only from their visible artifacts and may commission more; an independent reviewer audits the result. No deterministic research planner, renderer, or validator is added.

## RP-011 — corrected persona scout (passed scout boundary; retrieval pending)

- **Call ID:** `gen-1783703790-24ZIYBNxikb0KufbIxPH`
- **Requested / actual model:** `deepseek/deepseek-v4-pro` `xhigh` / `deepseek/deepseek-v4-pro-20260423`
- **Provider:** WandB
- **Exact inputs:** prompt SHA `e2d1e64ee9edc9b2bf4a59298277630a206f8749`, blind-brief SHA `a272394a8fd32787db145ebcb3327a8ba9094c0c`, and persona-focus SHA `2c109a01a7968cfa500135ff2f8979d69bddbebc`; the former boundary commit was removed by the authorized history sanitization
- **Allowance preflight:** the endpoint rejected 1,048,576 because input plus output exceeded its 1,048,576-token context; 1,043,000 then reached the disposable key's authorization gate, which reported an exact affordable maximum of 388,842. The inference request used `max_tokens=388842`, with mandatory continuation on `length`.
- **Usage / cost:** 4,541 prompt + 6,955 completion = 11,496 tokens; 3,624 reasoning tokens; $0.03210474
- **Finish:** `stop`
- **Artifacts:** `calibration/pilots/council/persona-scout-output.md` and `persona-scout-meta.json`
- **Visible yield:** ten model-designed retrieval assignments spanning dedicated quit-sugar discussion, adjacent recovery/weight-loss communities, long-form narratives, public comments, escape-route language, and cherished-use scenes; each names evidence to capture and gaps to revisit.
- **Disposition:** `PASS — SCOUT COMMISSION ONLY; NO PERSONA SYNTHESIS ACCEPTED`

The scout did not turn candidate communities into persona findings or supply invented quotations. Domain/community names and unverified scale/rationale claims in the commission are discovery leads only; none counts as evidence. H-032 remains `TESTING` until focused retrieval agents return visible source excerpts, a fresh specialist synthesizes exclusively from those artifacts, and an independent provenance reviewer accepts the result.

## RP-012 — A1 retrieval transport and raw-evidence validation (candidate; review pending)

### OpenRouter retrieval transport

The persona scout's A1 commission was dispatched to allowed retrieval agents at their full runtime allowance:

- MiniMax M3 reasoning enabled with Exa restricted to Reddit returned no annotations twice. The agents correctly returned zero evidence.
- The same focused MiniMax handoff without a domain filter returned 25 annotations, but all were personal blogs or other off-scope sites. The agent again returned zero accepted r/sugarfree evidence.
- Parallel returned `500` twice and Perplexity returned `500` before inference.
- Luna at `max` reasoning and its 128,000-token endpoint maximum received an exact model-commissioned `site:reddit.com/r/sugarfree "why I quit"` query, but Exa again returned no visible annotations. Luna returned zero evidence.

Exact transport metadata was removed with the unauthorized retrieval artifacts because it carried direct locators into the purged history. The failure mechanism remains: these were transport findings, not H-009 model-quality results, and all agents refused to invent sources when the retrieval layer failed.

### Caller-executed model commission

The caller then executed the retrieval agents' own query commission through the available web retriever. The now-removed raw artifact contained 33,449 bytes, 24 distinct URLs, and substantial visible r/sugarfree post/comment excerpts:

- **Artifact:** purged raw retrieval artifact; locator intentionally removed
- **Disposition:** `RAW — NOT ACCEPTED EVIDENCE`
- **Boundary:** the artifact itself records the exact query cluster, tool, retrieval time, and rule that only a later approved research model may accept or reject it.

This is transport, not a deterministic research planner: the scout and retrieval agents chose the community, query cluster, recursion, and required follow-ups. The caller executed the commissioned search and persisted its unchanged result.

### DeepSeek retrieval-validation specialist

- **Call ID:** `gen-1783705802-y7toSTraNWLbJWx5NffM`
- **Requested / actual model:** `deepseek/deepseek-v4-pro` `xhigh` / `deepseek/deepseek-v4-pro-20260423`
- **Provider:** WandB
- **Input:** exact prompt + blind brief + A1 commission + complete raw web artifact
- **Allowance preflight:** the endpoint reported 14,118 input tokens and a 1,034,458-token post-input maximum; the disposable key then reported an exact authorization ceiling of 359,736. The inference used `max_tokens=359736`, with continuation mandatory on `length`.
- **Usage / cost:** 13,118 prompt + 24,975 completion = 38,093 tokens; 12,363 reasoning tokens; $0.10973832
- **Finish:** `stop`
- **Runtime metadata:** summarized above; the locator-bearing metadata and rejected derivative artifact were removed by RP-016 and the authorized history sanitization
- **Candidate yield:** 12 accepted r/sugarfree threads and 66 proposed exact evidence items for Banks 1, 2, and 9, plus model-generated follow-up commissions.
- **Disposition:** `CANDIDATE — INDEPENDENT PROVENANCE REVIEW REQUIRED`

The candidate is not self-certified. A quick operator reading already exposes suspect `EXACT` rows whose displayed text contains inserted ellipses, so source/quote fidelity remains unproved. A fresh allowed top-reasoning reviewer receives the raw artifact and complete candidate and must correct it or commission more retrieval; no deterministic research validator is introduced.

## RP-013 — MiniMax adversarial provenance review (rejection passed; regeneration failed)

- **Call ID:** `gen-1783708749-ZWGeoVAsuLdpyneLvwam`
- **Requested / actual model:** `minimax/minimax-m3` reasoning enabled / `minimax/minimax-m3-20260531`
- **Provider:** Parasail
- **Inputs:** the quarantined raw retrieval and derivative candidate were removed; the review mechanism and outcome are preserved here without locators into purged objects
- **Allowance preflight:** 25,894 input tokens left an exact endpoint maximum of 1,022,682 completion tokens; the request used all 1,022,682.
- **Usage / cost:** 24,865 prompt + 15,399 completion = 40,264 tokens; 4,306 reasoning tokens; $0.02590758
- **Finish:** `stop`
- **Runtime metadata:** summarized above; the locator-bearing metadata and derivative review were removed by RP-016 and the authorized history sanitization
- **Verdict:** `REJECTED — REQUIRES CORRECTION`

The reviewer correctly found ten altered or mislocated `EXACT` items, unsupported frequency labels, thin captures, and missing packet fields. This validates the independent-review mechanism but not its proposed replacement. Its “corrected artifact” still uses shorthand such as “see raw artifact” and “all unchanged items remain,” changes curly apostrophes to straight ones inside purported exact quotes, records `endpoint maximum` rather than the exact allowance, and fills some provenance fields by inference. It also says no further A1/Q3 retrieval is required while marking multiple sources as requiring full-post retrieval.

Disposition: the DeepSeek candidate remains rejected, and MiniMax's replacement is not accepted. A fresh Luna `max` reviewer receives the raw artifact plus both complete model artifacts and must return either a genuinely complete evidence artifact or its own model-generated retrieval commission. H-032 remains `TESTING`; no operator row editing or deterministic validator is introduced.

## RP-014 — Luna second provenance review (passed rejection; commissioned direct retrieval)

- **Call ID:** `gen-1783709422-MGcc0DTDrp3pnTC0B9MN`
- **Requested / actual model:** `openai/gpt-5.6-luna` `max` / `openai/gpt-5.6-luna-20260709`
- **Provider:** OpenAI
- **Inputs:** the quarantined raw artifact and derivative candidate/review were removed; the second-review mechanism and outcome are preserved here without locators into purged objects
- **Request:** the Luna endpoint's full 128,000-token completion maximum; complete 37,424-token evidence/review chain delivered over curl stdin after two caller-side payload-construction failures that never reached a model
- **Usage / cost:** 37,424 prompt + 27,930 completion = 65,354 tokens; 25,380 reasoning tokens; $0.21435925
- **Finish:** `stop`
- **Runtime metadata:** summarized above; the locator-bearing metadata and derivative review were removed by RP-016 and the authorized history sanitization
- **Verdict:** `REJECT A1/Q3 AS PACKET-READY — DIRECTLY RETRIEVE ALL TWELVE FIXED URLS`

Luna independently rejected both prior artifacts. It found altered citation markers and punctuation, invented worker/query/event metadata, nonnumeric allowance fields, incorrect counts, snippet-only locators, and the contradiction between “no retrieval required” and mandatory full-post follow-ups. It returned a focused `A1/Q3-F01` commission with twelve fixed canonical Reddit URLs and direct-capture requirements. This is the next retrieval assignment; no operator-selected source or deterministic research plan is substituted.

Direct browser testing found the canonical Reddit HTML, old.reddit HTML, and JSON endpoints blocked by network security. The same model-commissioned URL's `/.rss` endpoint returned an Atom feed containing the post and comments. RP-016 subsequently invalidated this transport on source-policy grounds and stopped all further capture.

## RP-015 — A1/Q3-F01 direct Atom capture (invalidated: source authorization)

The caller executed Luna's twelve fixed direct-retrieval rows. Agent-browser discovered the viable Atom endpoint after canonical HTML, old Reddit HTML, and JSON were blocked. Rapid requests returned `429`; a descriptive user agent, Atom accept header, and one request per 50-second cooldown returned HTTP 200 for every URL.

- **Raw captures:** twelve purged direct-feed artifacts; locators intentionally removed
- **Total stored bytes:** 503,354
- **Integrity at capture time:** all twelve files passed `xmllint --noout`; the locator-bearing capture log was purged with them
- **Visible content:** direct Atom entries expose post/comment IDs, author or deleted state, comment permalinks, source timestamps, exact Unicode, and HTML-escaped post/comment text
- **Disposition:** `INVALID — UNAUTHORIZED RESEARCH ACCESS / RETENTION CONFLICT`

The response bodies were materially stronger than search snippets, but the caller first failed to record the wall-clock time or HTTP `Date` header for each request. More importantly, the subsequent policy audit invalidated the entire source path: Reddit's current research access, non-redistribution, retention, and deletion requirements conflict with unauthorized scraping and permanent open-git packets. The direct captures and derivative quote artifacts were removed from the current tree; none counts as evidence.

The founder proposed two stronger browser transports during this pilot. Source audits of H-033 (`keyclaw6/Webwright-Clockbrowser`) and H-034 (`human-browser-use`) rejected both shipped agent loops and rejected any live Reddit trial without written authorization. Their generic transports remain eligible only for controlled fixtures or an explicitly authorized source, and only if they produce a quality/reliability win with exact text/locator preservation and no deterministic research judgment.

## RP-016 — source-authorization gate (Reddit path stopped and purged)

Official policy review found:

- Reddit research requires explicit approval and the Reddit for Researchers program is the authorized research route.
- Research data collected outside that program violates the Responsible Builder Policy.
- Approved research data is project-limited, deletion-sensitive, and non-redistributable.
- Automated scraping without prior written consent is prohibited; stealth/fingerprint masking would compound the violation rather than solve it.

The open repository's durable raw-packet contract is incompatible with those defaults. Live Reddit retrieval stopped immediately. The current calibration pilot tree removes direct feeds, raw search results, unverified model quotations, and derivative evidence/review prose. Retained pilot artifacts are non-content runtime metadata, the model-owned retrieval commission, and `reddit-policy-autopsy.md`. H-033/H-034 may be source-audited and fixture-tested, but no live guardrail-evasion trial is permitted without Reddit-issued authorization covering the exact use.

The missing capability was a **source-authorization and retention gate before retrieval**. It is now added to the active OpenSpec, HARNESS, and research prompt. Topical depth does not override permission; the council must replace a blocked community with a terms-compatible source while preserving the same bank/persona quality bar.

No Reddit-derived item, quote, persona, or bank cell is accepted. Remote git history still contains the removed pilot artifacts; rewriting and force-pushing the dedicated branch is a destructive remediation that requires founder approval. Until resolved, the branch must not be merged.

## RP-017 — clean terms-compatible persona scout (candidate; review required)

- **Call ID:** `gen-1783713578-XE5uV6DC8UJrubKGwgF1`
- **Requested / actual model:** `deepseek/deepseek-v4-pro` `xhigh` / `deepseek/deepseek-v4-pro-20260423`
- **Provider:** WandB
- **Exact inputs:** research-prompt SHA `0f34e07acf44a448c5c463c0846b55b09861bfbc`, blind-brief SHA `a272394a8fd32787db145ebcb3327a8ba9094c0c`, and persona-focus SHA `2cb979ae7018b80d1898ed95155c518f0f71b1ba`; former boundary commit removed by history sanitization
- **Allowance preflight:** the 1,048,576-token endpoint reported 6,397 tokens of request text; the disposable key's exact remaining authorization ceiling for the routed call was 259,159 completion tokens. The request used all 259,159 with continuation mandatory on `length`.
- **Usage / cost:** 5,186 prompt + 16,360 completion = 21,546 tokens; 14,049 reasoning tokens; $0.06595644
- **Finish:** `stop`
- **Artifacts:** `persona-scout-terms-candidate.md` and `persona-scout-terms-candidate-meta.json`
- **Disposition:** `CANDIDATE COMMISSION — INDEPENDENT POLICY/QUALITY REVIEW REQUIRED`

The first identical request ran for roughly ten minutes and then lost its response to an HTTP/2 `INTERNAL_ERROR`; it returned no body, call ID, or usage record. The missing capability was a stable long-response transport, not more research structure. Reissuing the identical payload over HTTP/1.1 completed naturally. No prompt, model, reasoning setting, allowance, or input changed.

The clean scout excluded Reddit, remained in scout mode, created no personas or evidence, and commissioned five source families: Stack Exchange, open-license qualitative research, explicitly CC-licensed personal narratives, exploratory open-license communities, and a likely-rejected YouTube-comment probe. This supports the scout/specialist separation and the new source-policy boundary, but the commission is not self-certified. It calls Stack Exchange licensing “verified” without visible retrieval, permits limited-use copyrighted article excerpts despite the durable repository-packet gate, and makes unverified assumptions about Medium/Fediverse licensing. A fresh MiniMax M3 reasoning-enabled reviewer receives the exact candidate and must approve, fully regenerate, or commission policy retrieval; the operator does not edit the commission.

## RP-018 — MiniMax terms/provenance review (rejection passed; regeneration failed)

- **Call ID:** `gen-1783715273-0hf3y9WqMTiv67zJnu7H`
- **Requested / actual model:** `minimax/minimax-m3` reasoning enabled / `minimax/minimax-m3-20260531`
- **Provider:** Parasail
- **Exact inputs:** research-prompt SHA `0f34e07acf44a448c5c463c0846b55b09861bfbc`, blind-brief SHA `a272394a8fd32787db145ebcb3327a8ba9094c0c`, and candidate SHA `2e564c5251e30e7ded37adf3dae1036682dca6ac`; exact inline reviewer assignment and request hash are in the meta artifact
- **Allowance preflight:** 11,399 tokens of request text left a 1,037,177-token endpoint allowance; the disposable key's exact remaining authorization ceiling was 696,599 completion tokens. The request used all 696,599 with continuation mandatory on `length`.
- **Usage / cost:** 9,476 prompt + 18,139 completion = 27,615 tokens; 13,105 reasoning tokens; $0.02457888
- **Finish:** `stop`
- **Artifacts:** `persona-scout-terms-minimax-review.md` and `persona-scout-terms-minimax-review-meta.json`
- **Verdict:** original rejected; replacement also rejected

MiniMax independently found that the original candidate had no provisional persona set, bundled banks, missing matrix fields, weak numeric targeting, and insufficient demographic mitigation. The rejection mechanism therefore passed. Its full replacement nevertheless claimed an “independent policy verification” was complete despite receiving no retrieval artifacts; invented four personas and their language/beliefs before persona evidence; bundled multiple communities and later multiple banks after criticizing the same defect; used `endpoint maximum` rather than the numeric allowance; retained limited-use copyrighted packets; and marked the persona commission dispatch-ready. It also introduced candidate scientific/investigative lineages without retrieval.

The result repeats RP-013's pattern: MiniMax is a strong critic but its regeneration is not reliably self-consistent or provenance-safe. No row or persona is accepted. A fresh Luna `max` reviewer receives the complete DeepSeek candidate and MiniMax review and must either produce a clean policy-retrieval commission or reject the path. The operator does not repair the matrix.

## RP-019 — Luna decisive architecture review (passed; policy retrieval commissioned)

- **Call ID:** `gen-1783716208-OMhAqiU2830oOHAoTRcE`
- **Requested / actual model:** `openai/gpt-5.6-luna` `max` / `openai/gpt-5.6-luna-20260709`
- **Provider:** OpenAI
- **Exact inputs:** research-prompt SHA `0f34e07acf44a448c5c463c0846b55b09861bfbc`, blind-brief SHA `a272394a8fd32787db145ebcb3327a8ba9094c0c`, DeepSeek-candidate SHA `2e564c5251e30e7ded37adf3dae1036682dca6ac`, and MiniMax-review SHA `7656178641eddc8ab5390807f3b0acdb79fee5ec`; exact inline assignment and request hash are in the meta artifact
- **Request:** Luna endpoint's full 128,000-token completion allowance
- **Usage / cost:** 16,914 prompt + 36,074 completion = 52,988 tokens; 31,033 reasoning tokens; $0.23758575
- **Finish:** `stop`
- **Artifacts:** `persona-scout-terms-luna-review.md` and `persona-scout-terms-luna-review-meta.json`
- **Verdict:** `PASS — PRE-REGENERATION RETRIEVAL COMMISSION; RESEARCH BLOCKED BEFORE COLLECTION`

Luna rejected every unsupported URL, license, persona, source-count, quote, and `READY` claim. Its twenty-point audit independently found the missing tracks, unsupported policy verification, restrictive-source conflict, premature status, bundled scopes/banks, nonnumeric allowances, over-bundled invented personas, incomplete Banks 6–8, confirmation-biased queries, absent counterevidence, and non-goal screening gaps. It correctly refused to regenerate an architecture without evidence.

The model instead commissioned a policy-first pre-regeneration council: exact Stack Exchange and open-access scopes; independent authorization/retention audit; persona/community discovery; Bank 7 science including disconfirmation; Bank 8 investigation including counterevidence; and separate Bank 6 analogy retrieval. The commission explicitly forbids Stage A counting, source retrieval before policy validation, Reddit use, premature personas, and operator patching. Track B authorization must run first for each named source, then its visible policy artifacts may unlock the matching retrieval assignment. H-032 and H-035 remain `TESTING` until that evidence returns and a later fresh reviewer accepts the full architecture.

## RP-020 — REV-AUTH-SE-FITNESS policy retrieval (visible artifact; decision pending)

The caller executed Luna's exact first authorization assignment using only current first-party Stack Overflow/Stack Exchange policy pages and the exact Fitness `robots.txt`. No question, answer, comment, profile, search result, or other user content was fetched.

- **Artifact:** `calibration/pilots/council/rev-auth-se-fitness-retrieval.md`
- **First-party sources:** Fitness licensing help, Public Network Terms, Acceptable Use Policy, API Terms, API throttle documentation, Privacy Policy, and `fitness.stackexchange.com/robots.txt`
- **Direct transport result:** the Fitness robots endpoint returned `418`, `Disallow: /`, `search=no`, and `ai-train=no`
- **Material policy tension:** subscriber content carries Creative Commons reuse rights, but the AUP restricts automated content collection for generative-AI testing/improvement purposes and the API Terms incorporate network terms
- **Disposition:** `VISIBLE POLICY INPUT — NO CALLER VERDICT; LUNA MAX SPECIALIST REQUIRED`

The artifact records short unchanged excerpts, policy versions/locators, the complete robots body, and unresolved questions without copying user data or deciding the source status. This is transport/provenance work, not deterministic research judgment.

## RP-021 — Luna Fitness authorization decision (candidate; collection hold)

- **Call ID:** `gen-1783716899-F15TCfJRldUaCgAA0nB4`
- **Requested / actual model:** `openai/gpt-5.6-luna` `max` / `openai/gpt-5.6-luna-20260709`
- **Provider:** OpenAI
- **Exact inputs:** research-prompt SHA `0f34e07acf44a448c5c463c0846b55b09861bfbc`, blind-brief SHA `a272394a8fd32787db145ebcb3327a8ba9094c0c`, and policy-retrieval SHA `85de1881a5d6690374c43a8c4eca3edf025e4764`; exact inline assignment and payload hash are in the meta artifact
- **Allowance:** Luna endpoint maximum 128,000; disposable key's exact remaining authorization ceiling 95,625, all requested with continuation mandatory on `length`
- **Usage / cost:** 6,063 prompt + 9,000 completion = 15,063 tokens; 7,250 reasoning tokens; $0.061578
- **Finish:** `stop`
- **Artifacts:** `rev-auth-se-fitness-luna-decision.md` and `rev-auth-se-fitness-luna-decision-meta.json`
- **Status:** `CANDIDATE — VALIDATION REQUIRED; COLLECTION HOLD`

Luna rejected direct automated page retrieval, refused to infer that CC BY-SA or API availability authorizes this calibration purpose, and found raw retention, deletion/refresh, open-repository redistribution, and user-identifier handling unresolved. It commissioned four first-party read-only policy follow-ups and a fifth request for written project-specific Stack Exchange authorization. No user content may be fetched meanwhile.

The caller may execute the read-only policy follow-ups. Seeking written authorization is external communication and requires separate founder authority; it will not be sent implicitly. If first-party evidence cannot establish every required permission without it, Fitness is rejected and replaced rather than delaying or weakening the research depth target.

## RP-022 — Fitness first-party policy follow-ups (complete; Luna disposition pending)

The caller executed Luna's `AUTH-SE-FITNESS-FU-01` through `FU-04` using only first-party legal/help/API pages and the machine-readable license. No user content, post timeline, API content result, or data dump was fetched.

- **Artifact:** `rev-auth-se-fitness-followup-retrieval.md`
- **AUP result:** automated collection for developing, testing, benchmarking, or improving generative-AI/LLM systems requires express prior written consent; no first-party research/nonprofit/book-factory exception was found
- **API result:** programmatic access exists, but its terms incorporate Stack Exchange terms and expose no purpose-specific override
- **License result:** `license.xml` declares CC BY-SA 4.0; help materials preserve historical license-version rules; reuse rights do not state access permission
- **Deletion/data result:** account deletion anonymizes content; licensed answers/comments have no stated erasure requirement; dumps are quarterly and require a no-LLM-training affirmation; no deletion/anonymization refresh feed was found
- **External boundary:** `FU-05` written authorization was not requested because external outreach needs founder authority
- **Disposition:** `VISIBLE FOLLOW-UP INPUT — LUNA FINAL SOURCE STATUS REQUIRED`

The caller does not interpret whether calibration is prohibited AI testing/improvement. Luna receives the original policy capture, its prior decision, and this follow-up artifact and must decide the final source status or identify a genuinely new first-party gap.

## RP-023 — Luna final Fitness disposition (rejected; replacement commissioned)

- **Call ID:** `gen-1783717257-KoC2Z7LaM1IAjXNSKyXY`
- **Requested / actual model:** `openai/gpt-5.6-luna` `max` / `openai/gpt-5.6-luna-20260709`
- **Provider:** OpenAI
- **Exact inputs:** research-prompt SHA `0f34e07acf44a448c5c463c0846b55b09861bfbc`, blind-brief SHA `a272394a8fd32787db145ebcb3327a8ba9094c0c`, initial-policy SHA `85de1881a5d6690374c43a8c4eca3edf025e4764`, prior-decision SHA `76e43983d2ade7bae8bbf158fd094e2eca2b495f`, and follow-up SHA `70e9f24eb3458e781c204caf2f1b8f8276bdb85b`; exact assignment/payload hash is in the meta artifact
- **Allowance:** Luna endpoint maximum 128,000; disposable key's exact remaining authorization ceiling 85,362, all requested with continuation mandatory on `length`
- **Usage / cost:** 9,049 prompt + 7,111 completion = 16,160 tokens; 6,214 reasoning tokens; $0.0539765
- **Finish:** `stop`
- **Artifacts:** `rev-auth-se-fitness-final.md` and `rev-auth-se-fitness-final-meta.json`
- **Status:** `REJECTED`

Luna found independent failures on automated-research authorization, the direct access route, and durable deletion/user-data handling; CC reuse was insufficient and no written authorization exists. It prohibited Fitness page, API, dump, snippet, derivative, and source-packet use for this run and superseded the prior candidate status.

The model commissioned `REPL-SUGAR-FIRSTPERSON-AUTH-01`: policy-first discovery of at least three independent authorization-compatible first-person source families, with no user-content retrieval before each passes and no reduction in Banks 1–6, 9, 10, persona breadth, numeric floors, or qualitative depth. Stack Exchange and Reddit are excluded absent platform authorization. This is the next persona/community retrieval assignment.

## RP-024 — DeepSeek replacement-source scout (candidate; review required)

- **Call ID:** `gen-1783717636-MzuJVhoFDRgkqcrZuBKt`
- **Requested / actual model:** `deepseek/deepseek-v4-pro` `xhigh` / `deepseek/deepseek-v4-pro-20260423`
- **Provider:** WandB
- **Exact inputs:** research-prompt SHA `0f34e07acf44a448c5c463c0846b55b09861bfbc`, blind-brief SHA `a272394a8fd32787db145ebcb3327a8ba9094c0c`, and the focused assignment/payload hash in the meta artifact
- **Allowance:** endpoint post-input maximum 1,042,313; disposable key's exact remaining authorization ceiling 131,666, all requested with continuation mandatory on `length`
- **Usage / cost:** 5,103 prompt + 8,849 completion = 13,952 tokens; 7,813 reasoning tokens; $0.03967374
- **Finish:** `stop`
- **Artifacts:** `replacement-source-scout-deepseek.md` and `replacement-source-scout-deepseek-meta.json`
- **Disposition:** `CANDIDATE COMMISSION — REVIEW REQUIRED BEFORE RETRIEVAL`

The scout remained commission-only and created no source findings. It proposed broad discovery, per-domain policy retrieval, and independent authorization evaluation. It is not dispatch-ready: it imposes a first-30-results cap, requires entire search-result and policy-page capture before auditing those services' own terms, allows fair-use/dealing and anonymization to remain possible substitutes for explicit packet rights, prescribes sequential handoffs, and invented a future timestamp. No search or fetch from this commission runs before fresh review; the operator does not patch it.

## RP-025 — MiniMax replacement-source review (partial critique; regeneration failed)

- **Call ID:** `gen-1783718490-DRgH7rXS05m49dYCUuTG`
- **Requested / actual model:** `minimax/minimax-m3` reasoning enabled / `minimax/minimax-m3-20260531`
- **Provider:** AtlasCloud
- **Exact inputs:** research-prompt SHA `0f34e07acf44a448c5c463c0846b55b09861bfbc`, blind-brief SHA `a272394a8fd32787db145ebcb3327a8ba9094c0c`, and candidate SHA `07c4ef45e7cbbb3e733869dfbf507c00a5c7f6b9`; exact inline assignment and payload hash are in the meta artifact
- **Allowance:** endpoint post-input maximum 1,039,409; disposable key's exact remaining authorization ceiling 348,772, all requested with continuation mandatory on `length`
- **Usage / cost:** 7,399 prompt + 9,589 completion = 16,988 tokens; 6,130 reasoning tokens; $0.01369914
- **Finish:** `stop`
- **Artifacts:** `replacement-source-minimax-review.md` and `replacement-source-minimax-review-meta.json`
- **Verdict:** candidate rejected; replacement also rejected

MiniMax usefully identified missing junk-carb queries, non-goal filters, source-currency evidence, cross-link handling, shortlist/follow-up behavior, and the hard no-deletion/project-limited rule. Its full regeneration nevertheless retained the arbitrary first-30-results cap, pre-authorization raw SERP/full-policy capture, fair-use and pseudonymization escape routes, invented future timestamp, and sequential workflow. It added unsupported one-request-per-second limits, a real-user agent string that can misstate automation, pre-authorization activity checks, a fixed 24-month rejection rule, unsupported platform bans, and example persona labels without evidence.

The artifact is not executed. This again supports MiniMax as a useful critic but not a reliable self-correcting architecture reviewer. Luna receives the complete DeepSeek and MiniMax artifacts next; the operator patches nothing.

## RP-026 — Luna decisive replacement-source review (passed; channel audit commissioned)

- **Call ID:** `gen-1783718861-fZJNa6Kz1ILL6sLV24rs`
- **Requested / actual model:** `openai/gpt-5.6-luna` `max` / `openai/gpt-5.6-luna-20260709`
- **Provider:** OpenAI
- **Exact inputs:** research-prompt SHA `0f34e07acf44a448c5c463c0846b55b09861bfbc`, blind-brief SHA `a272394a8fd32787db145ebcb3327a8ba9094c0c`, DeepSeek SHA `07c4ef45e7cbbb3e733869dfbf507c00a5c7f6b9`, and MiniMax SHA `62ab7209a0fb94fc823879edbb761a38b31fc1d2`; exact inline assignment and payload hash are in the meta artifact
- **Allowance:** Luna endpoint maximum 128,000; disposable key's exact remaining authorization ceiling 67,471, all requested with continuation mandatory on `length`
- **Usage / cost:** 12,100 prompt + 31,045 completion = 43,145 tokens; 25,898 reasoning tokens; $0.20139425
- **Finish:** `stop`
- **Artifacts:** `replacement-source-luna-review.md` and `replacement-source-luna-review-meta.json`
- **Verdict:** `PASS — DISPATCHABLE PRELIMINARY AUTHORIZATION COMMISSION; CONTENT COLLECTION BLOCKED`

Luna independently rejected both candidates and caught the pre-authorization SERP/user-snippet capture, unaudited search engines/transports, raw-policy retention, fixed caps and thresholds, fair-use/anonymization escape routes, activity/persona inference, domain bundling, synthesis inside retrieval, missing independent review/logging, and unsupported policy dates. It replaced them with `REPL-SUGAR-POLICY-FIRST-02`, limited to policy, rights, license, and authorized metadata only.

The replacement has no fixed searches, candidates, agents, results, families, or closure quota; forbids user-content discovery; audits the discovery channel before use; requires one fixed candidate scope per later assignment; separates retrieval, authorization synthesis, and adversarial review; logs every event with zero bank cells; and preserves blocked gaps. The next exact assignment is `REPL-AUTH-CHANNEL-01`. No topical search can run until at least one discovery channel passes.

## RP-027 — MiniMax discovery-channel scout (candidate; escalation triggered)

- **Call ID:** `gen-1783719455-RHjAdp1JzcCOHDjqr0Va`
- **Requested / actual model:** `minimax/minimax-m3` reasoning enabled / `minimax/minimax-m3-20260531`
- **Provider:** Minimax
- **Exact inputs:** research-prompt SHA `0f34e07acf44a448c5c463c0846b55b09861bfbc`, blind-brief SHA `a272394a8fd32787db145ebcb3327a8ba9094c0c`, and the focused assignment/payload hash in the meta artifact
- **Allowance:** endpoint post-input maximum 1,042,363; disposable key's exact remaining authorization ceiling 169,527, all requested with continuation mandatory on `length`
- **Usage / cost:** 5,021 prompt + 10,819 completion = 15,840 tokens; 3,812 reasoning tokens; $0.01446174
- **Finish:** `stop`
- **Artifacts:** `channel-policy-scout-minimax.md` and `channel-policy-scout-minimax-meta.json`
- **Disposition:** `CANDIDATE COMMISSION — ESCALATION REQUIRED BEFORE REVIEW OR RETRIEVAL`

DeepSeek was preflighted first but not run: the disposable key could authorize only 58,457 completion tokens on the proven route, while MiniMax afforded 169,527. MiniMax was selected for larger quality headroom, not lower spend.

The scout stayed policy-only and declared no channel authorized, but its commission again violates the prerequisite it is meant to enforce: it sends raw policy text and even archived/search excerpts into normal `research/sources/` packets before the policy page's own retention/redistribution basis passes. It also redundantly reopens already rejected Reddit/Stack Exchange channels, prescribes a vast fixed channel list, treats a missing policy version date as an automatic block, and surfaces unresolved project distribution-license, raw-user-content, identifier, deletion, commercial-status, approval-record, mirror, adversarial-source, and transcription decisions.

The repository inspection confirmed the central ambiguity: no `LICENSE`, `COPYING`, `NOTICE`, package license field, or other outbound license declaration exists. The active packet contract nevertheless requires models to prove compatibility with “this open repository.” Together with three-plus consecutive source-authorization failures and the shrinking model-key ceilings, HARNESS §11 now requires a committed escalation and stop before another reviewer or retrieval call.

## Bootstrap closeout — bird's-eye autopsy (2026-07-11)

This bootstrap is closed. It is not a gate to another pilot.

An independent bird's-eye audit found 28 calibration commits, roughly 6,242
inserted lines, RP-000–RP-027, zero accepted sources, zero run rows, and zero
chapters. The early work proved model routing, blindness, quote-provenance review,
and the need to reject unauthorized evidence. The later work optimized a
mandatory council graph, atomic matrices, numeric floors, and policy recursion
before the simplest research loop had run. Models spent their intelligence
satisfying or criticizing the protocol rather than learning about the behavior.

Mechanism: the prompt and tests described the intended evidence process so
minutely that the schema became a deterministic research planner even though no
deterministic orchestration code existed. Requiring a complete bootstrap before
run-001 then made the bootstrap the product.

Founder correction: use the simplest end-to-end system first. One strong lead
gets the blind brief and outcome, chooses and runs its own subagents and web
research, produces source packets plus the two syntheses, and receives one fresh
independent review. Real research begins in run-001. Only observed research or
chapter failures justify later hypotheses and prompt amendments.

The 2026-07-11 boundary also declares the repository license, limits Git evidence
to minimum permitted rights/privacy-safe excerpts, retires the theoretical
endpoint-maximum stop, and preserves Reddit as excluded without authorization.
No pilot result counts as run evidence.
