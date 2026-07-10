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

## Research-arm summary

| Arm | Freely chosen strategy / subagents | Model / reasoning / allowance | Accepted sources | Verified quotes | Coverage and quality | Rejected yield | Reviewer verdict |
|---|---|---|---|---|---|---|---|
| H-010 first pass | 16 model-controlled high-context web searches | DeepSeek V4 Pro / `xhigh` / 10,860 authorized | 0 | 0 | Search breadth visible; no delivered bank artifact | 79 discovery annotations and 654 characters of process narration | Not reviewable; recovery synthesis running |
