# Research Log — Quit Sugar

Record what happened without prescribing how the lead must think or delegate.
Use stable source IDs (`S-001`) throughout. Unavailable usage or cost is `n/a`,
never zero.

## Model and subagent calls

One row per substantive model call. Describe the model-chosen objective and
strategy plainly; link visible output artifacts.

| UTC | Call / role | Objective and model-chosen strategy | Requested → actual model | Reasoning | Requested / authorized output | Finish | Usage / cost | Visible outputs | Disposition |
|---|---|---|---|---|---|---|---|---|---|
| 2026-07-10T22:58:30Z | `gen-1783724310-NWdwghQhnTEZGjH0Hn5e` / run-001 lead | DeepSeek chose and executed 16 web searches across lived experience, mechanisms, moderation, freedom, industry, and persona signals | `deepseek/deepseek-v4-pro` → `deepseek/deepseek-v4-pro-20260423` (provider reported `OpenAI`) | `xhigh` | endpoint request 384,000 → key ceiling / actual request 10,860 | `stop` | 122,890 prompt; 1,642 completion; 676 reasoning; 16 web searches; $0.096341292 | 79 URL annotations remained in the local response; response prose was 654 characters of progress narration | `FAILED ARTIFACT` — search transport worked but no packets, syntheses, coverage audit, or commissions were returned; zero evidence accepted |
| 2026-07-10T23:02:00Z | `gen-1783724520-oomt2mtaOUB9wjUrdrU7` / recovery selector | MiniMax chose a cross-bank subset from all 79 titles/URLs so the key-limited next context would not be operator-selected | `minimax/minimax-m3` → `minimax/minimax-m3-20260531` (`DeepInfra`) | enabled | endpoint request 131,072 → key ceiling / actual request 7,719 | `length` | 5,336 prompt; 7,719 completion; 5,614 reasoning; $0.01083288 | Partial 16-source ranking retained locally | `CONTINUED` — ranking truncated and overclaimed rights for a forum and book mirrors; no evidence accepted |
| 2026-07-10T23:17:36Z | `gen-1783725456-hyCb2tvlFULvhR9ct2g9` / selector continuation | Finish ranking and independently correct every unsupported reuse-rights claim | `minimax/minimax-m3` → `minimax/minimax-m3-20260531` (`DeepInfra`) | enabled | endpoint request 131,072 → key ceiling / actual request 6,816 | `stop` | 6,335 prompt; 4,781 completion; 3,322 reasoning; $0.00637818 | Corrected local rights audit and focused science/lived-experience/industry retrieval commissions | `PASS AS COMMISSION` — dropped the deletion-sensitive forum and unauthorized book mirrors; still zero accepted evidence pending direct retrieval |
| 2026-07-10T23:32:20Z | `/root/birds_eye_calibration` / science retrieval subagent | Resolve the model-selected human mechanism gaps from canonical publications; distinguish independent studies from duplicate releases and preserve contrary results | Codex subagent → runtime model not exposed | n/a | n/a | complete | n/a | `sources/S-001` through `S-006`; six verified minimal excerpts | `PASS AS RETRIEVAL` — six sources accepted with study-specific limits; the two institutional dessert releases count as one lineage and only the Cologne release is retained |

## Source decisions

| UTC | Source ID / family | URL or scope | Rights / privacy basis | Decision and reason |
|---|---|---|---|---|
| 2026-07-10T22:58:30Z | Unaccepted discovery inventory | 79 URL annotations from 16 model-controlled searches | Not established source-by-source | `REJECTED AS EVIDENCE` — retain locally only for the fresh model-owned recovery pass; no excerpt or claim enters Git |
| 2026-07-10T23:32:20Z | S-001 | https://pmc.ncbi.nlm.nih.gov/articles/PMC5174153/ | CC BY 4.0 | `ACCEPTED` — critical review supports the narrow 2016 finding that direct human sugar-addiction evidence was sparse; broad addiction claims remain contested |
| 2026-07-10T23:32:20Z | S-002 | https://pmc.ncbi.nlm.nih.gov/articles/PMC7774304/ | Minimal attributed quotation under the official author-manuscript notice; third-party material excluded from the repository CC grant | `ACCEPTED` — useful qualified metabolic review; high/hypercaloric exposure and animal-to-human limits must remain attached |
| 2026-07-10T23:32:20Z | S-003 | https://uni-koeln.de/en/research/research-news/detail-forschungsmeldung-en/dessertmagen-entsteht-im-gehirn | Minimal attributed quotation for research/criticism; standard institutional copyright | `ACCEPTED` — mouse circuit plus limited human imaging signal; the Max Planck release was rejected as a duplicate summary of the same study |
| 2026-07-10T23:32:20Z | S-004 | https://www.mdpi.com/2072-6643/17/17/2718 | CC BY 4.0; anonymous participant excerpt without indirect identifiers | `ACCEPTED` — preliminary first-person distinctions among pleasure, routine, boredom, environment, hunger, and control; only seven participants |
| 2026-07-10T23:32:20Z | S-005 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8479585/ | CC BY | `ACCEPTED` — randomized human trial supplies a useful null whole-cohort result and qualified BMI/sex interactions; it does not establish craving or addiction |
| 2026-07-10T23:32:20Z | S-006 | https://www.research-collection.ethz.ch/items/b9f7f82c-0634-4178-aed6-6eb17a6ce06e | CC BY-NC-ND 4.0; minimal unmodified quotation retained under its original license and excluded from the repository CC grant | `ACCEPTED WITH LICENSE LIMIT` — repeated-exposure result is specific to a combined high-fat/high-sugar intervention and cannot isolate sugar |

## Personas discovered

| Persona ID | Function served / defining context | Evidence source IDs | Thin spots |
|---|---|---|---|
|  |  |  |  |

## Final bank audit

Counts are diagnostics, not quotas. A bank passes only when its material is
specific, nonredundant, source-traceable, and strong enough for belief-changing
framing across every applicable persona.

| Bank | Applicable personas | Source IDs / verified quotes | Strongest insight | Remaining gap | Verdict |
|---|---|---|---|---|---|
| 1 | Preliminary sweet-tooth / pleasure-seeking contexts | S-004 | Participants distinguish pleasure from other motives | One seven-person qualitative study is not enough; lived-experience retrieval and reviewer pending | PROVISIONAL |
| 2 |  |  |  |  |  |
| 3 | Preliminary routine, boredom, environmental, and perceived-control contexts | S-004 | Multiple triggers coexist within the same participants | Needs broader first-person evidence and persona synthesis | PROVISIONAL |
| 4 | Preliminary post-meal / restaurant pleasure context | S-004 | Dessert can be anticipated before the main meal is chosen | Needs independent scenes across different registers | PROVISIONAL |
| 5 | Preliminary perceived-control context | S-004 | Taste blocking sometimes prompted more deliberate choice | Intervention cannot establish durable moderation or quitting | PROVISIONAL |
| 6 |  |  |  |  |  |
| 7 | ALL where qualified; post-meal, SSB, habitual-snack, and subgroup contexts | S-001, S-002, S-003, S-005, S-006 | Human evidence resists a blanket addiction story while identifying narrower metabolic, learning, sensory, and post-meal mechanisms | Independent synthesis and review pending; several findings are mixed, preclinical, combined fat+sugar, or exposure-specific | PROVISIONAL |
| 8 | ALL | none from S-001–S-006 | Science packet does not establish engineered demand | Requires independent industry evidence | GAP |
| 9 | Preliminary language of sweet-tooth, routine, boredom, environment, and control | S-004 | Participants supply distinct motive categories rather than one generic craving label | Needs broader communities/registers | PROVISIONAL |
| 10 |  |  |  |  |  |

## Rejected or unresolved yield

Record only failures that affect research quality, provenance, rights/privacy,
or the next decision. Include the mechanism and the follow-up taken.

- Luna `max` preflight requested its 128,000-token endpoint maximum; the supplied
  key returned an exact 6,299-token ceiling, so no Luna model ran.
- DeepSeek `xhigh` preflight requested the 384,000-token endpoint maximum; the
  key returned 10,860, which the actual call used in full.
- Autopsy: the server-side search loop consumed the substantive turn and ended
  after progress narration even though `finish_reason=stop`. The smallest
  correction is a fresh allowed synthesis call over model-selected visible
  annotations—not a new role graph, matrix, or prompt framework.
- Passing all annotation text to MiniMax exceeded the key's prompt-token ceiling.
  MiniMax therefore selected the subset from the complete title/URL inventory;
  its first response hit `length` and was continued. The continuation explicitly
  retracted unsupported reuse claims, rejected the forum and book mirrors, and
  commissioned three direct retrieval tasks now running in parallel.

## Research-arm summary

| Arm | Freely chosen strategy / subagents | Model / reasoning / allowance | Accepted sources | Verified quotes | Coverage and quality | Rejected yield | Reviewer verdict |
|---|---|---|---|---|---|---|---|
| H-010 first pass | 16 model-controlled high-context web searches | DeepSeek V4 Pro / `xhigh` / 10,860 authorized | 0 | 0 | Search breadth visible; no delivered bank artifact | 79 discovery annotations and 654 characters of process narration | Not reviewable; recovery synthesis running |
| H-010 recovery selection | Model-ranked inventory, then mandatory continuation and rights correction | MiniMax M3 / reasoning enabled / 7,719 then 6,816 authorized | 0 | 0 | Produced concrete science, lived-experience, and industry retrieval gaps without a fixed matrix | Initial rights overclaim corrected; no source content accepted from snippets | Retrieval commissions dispatched |
| H-010 science retrieval | One fresh retrieval subagent followed the model-selected gaps and chose canonical sources | Codex subagent / runtime model and allowance not exposed | 6 | 6 | Bank 7 has a qualified human/preclinical evidence base; S-004 also seeds Banks 1, 3, 4, 5, and 9 | Duplicate Max Planck release excluded; no Bank 8 evidence; no broad sugar-addiction claim accepted | Synthesis reviewer pending |
