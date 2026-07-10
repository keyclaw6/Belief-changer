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

The second corrected attempt tripled the completion headroom and reproduced the same zero-artifact mechanism. The broad lead task induces Luna `max` to elaborate the full persona × bank matrix entirely in reasoning without reaching an answer. This is not evidence about source quality, but it is decisive orchestration-efficiency evidence: accepted cells and quotes per dollar are both zero after $0.1629372 of corrected calls. Per the harness failure rule, the same retry is stopped. The approved DeepSeek V4 Pro `xhigh` arm takes the lead role; Luna remains in the later small equal-assignment H-009 comparison so the broad-task failure is not overgeneralized.

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

The prompt's atomic-cell correction worked in the model's plan: it explicitly intended one bank per row and no shorthand. But it interpreted each bank's `≥2 sources` floor as requiring two independent community assignments for every persona/bank. Six personas × two communities × seven lived banks, plus science/analogy rows, became 91 planned rows. The 30k top-reasoning call ended before the matrix was visible, so nothing was dispatchable. This does not refute H-028 because no rows were returned for inspection. H-029 clarifies that sources are URLs/documents, caps the initial persona set at 3–4, and defers second communities until observed gaps.

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

H-029 removed RP-007's Cartesian growth: the response used four personas and one primary community. The provider nevertheless counted internal reasoning and visible artifact against the same 30k completion cap. With 27,118 reasoning tokens, only about 2,882 tokens remained for the matrix, which ended mid-row with `finish_reason=length`. The artifact cannot be dispatched or operator-repaired. H-030 preserves the committed prompt and `xhigh` setting and tests 60k completion headroom; it does not authorize more personas, communities, or prose.
