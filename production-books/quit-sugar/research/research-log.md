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
| 2026-07-10T23:31:48Z | `/root/muse_spark_route` / lived-experience retrieval subagent | Resolve first-person evidence gaps through rights-safe adult qualitative sources across distinct social and geographic registers | Codex subagent → runtime model not exposed | n/a | n/a | complete | n/a | `sources/S-007` through `S-012`; six rendered-page-verified excerpts | `PASS AS RETRIEVAL` — six CC BY sources accepted; durable total-abstinence, male, and older-adult recovery remain thin |
| 2026-07-10T23:43:55Z | `/root/license_rewrite_review` / industry retrieval subagent | Resolve engineered-demand evidence from primary corporate records, compulsory-process reports, documentary analysis, and an anti-overclaim constraint | Codex subagent → runtime model not exposed | n/a | n/a | complete | n/a | `sources/S-013` through `S-019`; seven verified minimal excerpts | `PASS AS RETRIEVAL` — direct historical formulation, sponsorship, testing, and marketing evidence accepted with narrow limits; tobacco-only and rights-incompatible material excluded |
| 2026-07-10T23:48:01Z | `gen-1783727281-DGWbLOKCwbPyU0li0Mj4` / first full synthesis | Build both artifact-ready syntheses from all 19 accepted packets, choosing the persona map and bank structure without new retrieval | `minimax/minimax-m3` → `minimax/minimax-m3-20260531` (`Minimax`) | enabled | endpoint request 131,072 → key/provider ceiling / actual request 12,569 | `stop` | 11,911 prompt; 11,239 completion; 4,497 reasoning; $0.01703274 | Candidate lived/science syntheses retained locally; SHA-256 `42be9884ed7d5887fe4decd13a6f19d57e63ef72a84168515525d96dabba2e5c` | `REJECTED BY REVIEW` — useful gap discovery, but exact-quote normalization, unsupported motives/personas, and two unsafe analogies made it unfit for framing; not promoted to live files |
| 2026-07-10T23:51:31Z | `gen-1783727491-VDFMZmKFPggmujWzOQ4j` / fresh synthesis reviewer | Audit every packet-to-claim link, exact quote, persona tag, scientific grade, and analogy in the complete candidate | `deepseek/deepseek-v4-pro` → `deepseek/deepseek-v4-pro-20260423` (`StreamLake`) | `xhigh` | endpoint request 384,000 → key/provider ceiling / actual request 11,185 | `length` | 18,168 prompt; 11,185 completion; 11,185 reasoning; $0.021160836 | Complete packet-by-packet audit in preserved reasoning; no visible verdict before the boundary | `CONTINUED` — the audit independently found quote mismatches and unsupported S-006/S-008/S-007 claims; continuation required |
| 2026-07-10T23:57:32Z | `gen-1783727852-8KfUpnb3H8osXQuG4bWY` / provider-state continuation probe | Continue the completed audit from provider-supplied reasoning state | `deepseek/deepseek-v4-pro` → `deepseek/deepseek-v4-pro-20260423` (`StreamLake`) | `xhigh` | endpoint request 384,000 → key/provider ceiling / actual request 7,131 | `stop` | 198 prompt; 1,485 completion; 1,305 reasoning; $0.001653696 | Hallucinated requests for nonexistent “Packet 3/7/11” | `REJECTED PROVIDER CONTINUATION` — prompt usage proved the provider ignored the preserved reasoning state; this output is not a review verdict |
| 2026-07-10T23:58:59Z | `gen-1783727939-aOKiMHSWZ7kN5Ca4yHrO` / visible-reasoning review continuation | Finish the same audit with its complete prior reasoning replayed as visible input | `deepseek/deepseek-v4-pro` → `deepseek/deepseek-v4-pro-20260423` (`StreamLake`) | `xhigh` | endpoint request 384,000 → key/provider ceiling / actual request 6,814 | `stop` | 11,379 prompt; 1,901 completion; 1,648 reasoning; $0.007924482 | Decisive `MORE RESEARCH REQUIRED` verdict and whole-synthesis regeneration commission | `PASS AS REVIEW` — preserve packets, regenerate both syntheses model-owned, then re-audit quote fidelity and claim grounding |
| 2026-07-10T23:53:00Z | `/root/synthesis_birds_eye` / independent bird’s-eye audit | Test whether the candidate is genuinely fit to frame from rather than merely schema-complete | Codex subagent → runtime model not exposed | n/a | n/a | complete | n/a | Ranked audit of quote fidelity, source overreach, persona universals, analogy integrity, and thin banks | `REJECTED CANDIDATE` — only 8/19 excerpts remained character-for-character; Bank 10, keystone voice, and special-moment coverage remain material risks after regeneration |

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
| 2026-07-10T23:31:48Z | S-007 | https://doi.org/10.1017/jns.2026.10118 | CC BY 4.0; coded participant locator only | `ACCEPTED` — knowledge-linked anticipated non-return at week 12; not observed long-term abstinence |
| 2026-07-10T23:31:48Z | S-008 | https://doi.org/10.1186/s12889-025-22391-2 | CC BY 4.0; anonymous excerpt without demographic inference | `ACCEPTED` — native soda-addiction language; not clinical or mechanistic proof |
| 2026-07-10T23:31:48Z | S-009 | https://doi.org/10.3389/fnut.2024.1388918 | CC BY 4.0; pseudonym used only as locator | `ACCEPTED` — concrete failed reduction and taste-triggered return in a young-adult register |
| 2026-07-10T23:31:48Z | S-010 | https://doi.org/10.1007/s10995-025-04075-w | CC BY 4.0; coded caregiver locator only | `ACCEPTED` — reported household substitution and label checking; not caregiver abstinence or durable change |
| 2026-07-10T23:31:48Z | S-011 | https://doi.org/10.3390/ijerph23060799 | CC BY 4.0; minimized translated participant context | `ACCEPTED` — commercial-drink distrust in an Accra household-shopping register; not product-composition or industry-intent proof |
| 2026-07-10T23:31:48Z | S-012 | https://doi.org/10.3390/ijerph16030413 | CC BY 4.0; minimum fragment from a coded food-bank participant | `ACCEPTED` — a concrete reduction step felt achievable; implementation and durability unknown |
| 2026-07-10T23:43:55Z | S-013 | https://www.industrydocuments.ucsf.edu/docs/nxwv0087 | Minimal attributed fair-use quotation under UCSF archive guidance | `ACCEPTED WITH FAIR-USE LIMIT` — direct 1985 formulation objective; no addiction or actual-overeating claim |
| 2026-07-10T23:43:55Z | S-014 | https://www.industrydocuments.ucsf.edu/docs/hyxk0230 | Minimal attributed fair-use text; no image reproduction | `ACCEPTED WITH FAIR-USE LIMIT` — remaining sponsor payment tied to manuscript acceptance; distortion remains unproved |
| 2026-07-10T23:43:55Z | S-015 | https://www.ftc.gov/reports/marketing-food-children-adolescents-review-industry-expenditures-activities-self-regulation-federal | Public-domain FTC-authored text; third-party material excluded | `ACCEPTED` — compulsory-process evidence of large-scale integrated youth marketing; no obesity-causation claim |
| 2026-07-10T23:43:55Z | S-016 | https://www.ftc.gov/reports/review-food-marketing-children-adolescents-follow-report | Public-domain FTC-authored text; aggregate company research only | `ACCEPTED` — company-reported child-request effects; historical and not a universal causal estimate |
| 2026-07-10T23:43:55Z | S-017 | https://pubmed.ncbi.nlm.nih.gov/37682074/ | Minimal attributed fair-use abstract quotation; excluded from repository CC grant | `ACCEPTED WITH FAIR-USE LIMIT` — retrospective historical association; no design-intent or current-practice claim |
| 2026-07-10T23:43:55Z | S-018 | https://pmc.ncbi.nlm.nih.gov/articles/PMC6890456/ | Minimal attributed fair-use BMJ quotation; excluded from repository CC grant | `ACCEPTED WITH FAIR-USE LIMIT` — documentary evidence for four historical tobacco-owned drink brands; no industry-wide generalization |
| 2026-07-10T23:43:55Z | S-019 | https://www.nih.gov/news-events/nih-research-matters/eating-highly-processed-foods-linked-weight-gain | Public-domain NIH-authored text | `ACCEPTED AS CONSTRAINT` — controlled trial found increased intake but did not identify the responsible product feature; no sugar-specific or intentional-engineering inference |

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
| 1 | Sweet-tooth / pleasure-seeking and taste-driven young-adult contexts | S-004, S-009 | Pleasure, routine, and taste appear as distinct credited benefits and return triggers | Coverage remains narrow and synthesis/reviewer pending | PROVISIONAL |
| 2 | Knowledge-responsive, soda-identifying, low-income household, student, and caregiver contexts | S-007, S-008, S-011, S-012 | Beliefs range from addiction identity and ingredient distrust to changed vulnerability and achievable steps | Keystone belief and persona synthesis pending | PROVISIONAL |
| 3 | Routine, boredom, environment, failed-reduction, and household-change contexts | S-004, S-009 | Concrete trigger and failed-attempt evidence now spans more than one register | Private costs and durable recovery remain thin | PROVISIONAL |
| 4 | Post-meal / restaurant pleasure and taste-driven soft-drink contexts | S-004, S-009 | Anticipated dessert and taste-triggered return provide two specific seductive situations | Family, work, celebration, and older-adult scenes remain thin | PROVISIONAL |
| 5 | Perceived control, household substitution, and achievable incremental reduction | S-004, S-010, S-012 | Evidence distinguishes substitution and moderation strategies from actual durable freedom | Exception rationales and long-term outcomes remain thin | PROVISIONAL |
| 6 | All grounded personas | none directly; analogy candidates must be invented from accepted beliefs | Evidence base can ground original analogies without claiming a sourced metaphor | Synthesis and reviewer must judge usefulness | PROVISIONAL GAP |
| 7 | ALL where qualified; post-meal, SSB, habitual-snack, and subgroup contexts | S-001, S-002, S-003, S-005, S-006, S-019 | Evidence resists a blanket addiction story while identifying narrower metabolic, learning, sensory, and post-meal findings; S-019 blocks a false product-feature claim | Independent synthesis/review pending; several findings are mixed, preclinical, combined fat+sugar, or exposure-specific | PROVISIONAL |
| 8 | ALL; especially childhood-onset and parent/caregiver contexts | S-013, S-014, S-015, S-016, S-017, S-018 | Primary and official records show narrow historical formulation, sponsor-payment, child-testing, and integrated-marketing mechanisms | Avoid industry-wide, current-practice, addiction, or causation generalizations; synthesis/reviewer pending | PROVISIONAL |
| 9 | Soda-identifying, sweet-tooth, routine, boredom, environment, and control contexts | S-004, S-008 | Native language distinguishes “addicted to soda” from several motive categories | Broader lexicon and frequency claims remain thin | PROVISIONAL |
| 10 | Knowledge-responsive adult and WIC caregiver contexts | S-007, S-010 | Two change/revelation moments are visible | Durable complete abstinence, post-quit gains, male, and older-adult recovery remain major gaps | GAP |

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
  commissioned the three direct retrieval tasks recorded above.
- Lived-experience retrieval rejected Reddit/forums, child-only studies, and
  staff-only quotations. A CC BY-NC-ND reduction study with useful direct quotes
  was not accepted in this pass; the fresh reviewer can decide whether a minimal
  quotation basis is necessary to repair the durable-recovery gap.
- Industry retrieval rejected NPR-derived material, unauthorized book mirrors,
  the terms-restricted IFF page, and tobacco-only Project Sunrise records. The
  latter cannot establish food engineering by analogy. FTC 2008/2012 are a
  longitudinal report family, and RJR/BMJ overlap is retained as primary record
  plus documentary triangulation rather than independent volume.
- First full-synthesis autopsy: retrieval succeeded; synthesis fidelity failed.
  MiniMax normalized exact Unicode/punctuation, converted thin evidence into
  stronger motives and synthetic universal personas, attributed a participant
  interpretation to S-006 that the experiment never reported, and proposed an
  infantilizing analogy plus a blame-adjacent mouse-to-human mechanism analogy.
  The smallest formal-review correction is full model-owned regeneration from
  the same packets, not operator line edits or another architecture. The fresh
  post-regeneration reviewer will decide whether the bird audit's durable-
  freedom, deprivation-voice, and special-moment gaps require one focused
  retrieval pass.
- DeepSeek's first review consumed its complete authorized output as reasoning.
  The provider ignored a reasoning-state continuation despite returning it in
  the response schema; replaying the complete reasoning as visible text produced
  a grounded verdict. The hallucinated intermediate continuation is excluded.

## Research-arm summary

| Arm | Freely chosen strategy / subagents | Model / reasoning / allowance | Accepted sources | Verified quotes | Coverage and quality | Rejected yield | Reviewer verdict |
|---|---|---|---|---|---|---|---|
| H-010 first pass | 16 model-controlled high-context web searches | DeepSeek V4 Pro / `xhigh` / 10,860 authorized | 0 | 0 | Search breadth visible; no delivered bank artifact | 79 discovery annotations and 654 characters of process narration | Not reviewable; recovery synthesis running |
| H-010 recovery selection | Model-ranked inventory, then mandatory continuation and rights correction | MiniMax M3 / reasoning enabled / 7,719 then 6,816 authorized | 0 | 0 | Produced concrete science, lived-experience, and industry retrieval gaps without a fixed matrix | Initial rights overclaim corrected; no source content accepted from snippets | Retrieval commissions dispatched |
| H-010 science retrieval | One fresh retrieval subagent followed the model-selected gaps and chose canonical sources | Codex subagent / runtime model and allowance not exposed | 6 | 6 | Bank 7 has a qualified human/preclinical evidence base; S-004 also seeds Banks 1, 3, 4, 5, and 9 | Duplicate Max Planck release excluded; no Bank 8 evidence; no broad sugar-addiction claim accepted | Synthesis reviewer pending |
| H-010 lived retrieval | One fresh retrieval subagent followed the model-selected gap and searched rights-safe adult qualitative studies across distinct registers | Codex subagent / runtime model and allowance not exposed | 6 | 6 | Banks 1–5, 9, and 10 now have concrete first-person material across UK, US, Saudi, and Ghanaian contexts | Long-term abstinence, post-quit gains, male, and older-adult recovery remain thin; child-only and incompatible sources excluded | Synthesis reviewer pending |
| H-010 industry retrieval | One fresh retrieval subagent followed the model-selected gap through primary archives, official reports, documentary analysis, and counterevidence | Codex subagent / runtime model and allowance not exposed | 7 | 7 | Bank 8 now has narrow, traceable historical formulation, sponsorship, testing, and marketing evidence; Bank 7 gains an anti-overclaim constraint | NPR, mirrors, IFF, Reddit, and tobacco-only transfer evidence excluded; duplicate lineages marked | Synthesis reviewer pending |
| H-010 first synthesis/review | MiniMax generated both syntheses from all packets; a fresh DeepSeek reviewer and independent bird audit examined the full candidate | MiniMax M3 / enabled / 12,569; DeepSeek V4 Pro / `xhigh` / 11,185 then 6,814 | 19 preserved | 19 packet excerpts; only 8 remained character-exact in candidate | Science/industry caution was mostly strong and the model exposed real gaps | Candidate overreached lived claims/personas and produced unsafe analogies; provider reasoning continuation failed once | `MORE RESEARCH REQUIRED` — regenerate both syntheses from the same packets, then fresh review |
