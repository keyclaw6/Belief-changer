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

## Source decisions

| UTC | Source ID / family | URL or scope | Rights / privacy basis | Decision and reason |
|---|---|---|---|---|
| 2026-07-10T22:58:30Z | Unaccepted discovery inventory | 79 URL annotations from 16 model-controlled searches | Not established source-by-source | `REJECTED AS EVIDENCE` — retain locally only for the fresh model-owned recovery pass; no excerpt or claim enters Git |

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
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |
| 6 |  |  |  |  |  |
| 7 |  |  |  |  |  |
| 8 |  |  |  |  |  |
| 9 |  |  |  |  |  |
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
