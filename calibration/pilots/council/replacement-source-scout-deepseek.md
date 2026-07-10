# Retrieval Commission — REPL-SUGAR-FIRSTPERSON-AUTH-01

**Assignment ID:** REPL-SUGAR-FIRSTPERSON-AUTH-01  
**Worker ID (scout):** REPL-DISCOVERY-01  
**Date:** 2026-07-11T00:00:00Z  
**Status:** COMMISSIONED — no user content retrieved yet  
**Arms allowed:** DeepSeek V4 Pro (`deepseek/deepseek-v4-pro` at `xhigh`), MiniMax M3 (`minimax/minimax-m3` reasoning enabled), GPT-5.6 Luna (`openai/gpt-5.6-luna` at `max`). Caller selects and verifies exact runtime model ID and top reasoning config before dispatch.

## Objective
Discover **authorization-compatible replacement source families** that can provide first-person sugar/junk-carb recovery and experience material for Banks 1–6, 9, and 10. The commissioned retrieval subagents must:
- identify at least three independent candidate families;
- verify each candidate’s legal and technical compliance with the repository’s open-source, persistent-retention, and redistribution requirements (§1a);
- deliver enough compliant sources to meet or exceed the original numeric and qualitative depth targets (distinct personas, ≥2 sources per persona-bank, etc.) without Reddit, Stack Exchange, or any unauthorized platform.

### Hard constraints (repeated for each subagent)
- **No Reddit or Stack Exchange** unless explicit platform authorization already exists (it does not — these are banned).
- No user-content retrieval before the candidate source’s access terms, robots/access controls, automation permission, license/excerpt rights, and retention/deletion obligations are verified and marked `READY` by the lead.
- No stealth, spoofing, mirrors, workarounds, or alternate endpoints to bypass access controls or rate limits.
- Every accepted URL must support **permanent Git retention** and **redistribution of raw captures and excerpt packets** in this open repository. A source that forbids this or requires deletion refreshing is rejected; do not propose an alternative storage design unless separately approved.
- All retrieved policy pages and search result excerpts must be captured as visible artifacts with timestamps and URLs.
- The retrieval subagent must record its exact endpoint model ID, reasoning config, max output allowance, search settings, and any usage/cost in the returned metadata (the caller will provide the final numbers; the agent reports what it used if visible).

## Retrieval assignments

Dispatch the following sub-assignments in order, feeding the visible artifacts of each completed assignment into the next. The scout (this commission) provides no pre-learned sources; all discovery must be web-retrieved.

---

### Assignment 1: Broad candidate community discovery
**Retrieval Query ID:** `REPL-DISC-01`  
**Focused question:** What active online communities (forums, groups, blogs, video/audio channels, open-license repositories) host first-person discussions or personal stories about quitting sugar, sugar addiction, sugar detox, or junk-food cravings?  
**Exclude:** Reddit, Stack Exchange, any paywalled or private group that cannot be lawfully accessed, and any platform already known to have blanket prohibitions against scraping/retention.  
**Search queries (use multiple engines if possible):**
- “quit sugar forum”
- “sugar addiction support group”
- “I quit sugar stories”
- “sugar free journey blog”
- “sugar cravings community”
- “sugar detox discussion”
- “breaking sugar addiction forum”
- “sugar free living group”
- “how I overcame sugar addiction”
- “sugar recovery testimonial”
- “sugar addiction personal story”
- “sugar free living blog”
- “sugar addiction help site:healthunlocked.com”
- “quitting sugar site:myfitnesspal.com”
- “sugar addiction site:facebook.com/groups” (but only note existence; do not scrape Facebook content)
- “sugar free forum site:discourse.org”
- “sugar detox stories site:medium.com”
- “sugar addiction podcasts”
- “sugar recovery YouTube”
- “sugar addiction open access”
- “sugar addiction personal narratives public domain”

**Method:** Run these queries on a standard web search engine (Google, Bing, DuckDuckGo) at top reasoning allowed. Save the **exact search result page text** (titles, snippets, URLs) for the first 30 results per query. Do not click into user-content pages yet. Record search settings (engine, date filters if any, region, safe search).  
**Output artifact:** `candidate-communities-raw.md` containing:
- a table of all unique candidate community URLs with: candidate name, base domain, snippet from search result, and a brief “type” tag (independent forum, hosted community on large platform, personal blog, podcast, open repository, etc.).
- full search result captures as references.
**Model/reasoning:** Use one of the allowed arms at maximum output allowance. Record configuration in output metadata.
**Do not evaluate authorization yet.** This is purely existence/topical fit discovery. If a candidate seems highly relevant but its snippets mention “Reddit” or “Stack Exchange”, discard it.

---

### Assignment 2: Policy document retrieval
**Retrieval Query ID:** `REPL-POLICY-01`  
**Focused question:** What are the formal access terms, robots controls, API/automation rules, content licensing, retention/deletion requirements, and redistribution rights for each candidate domain discovered in Assignment 1?  
**Input:** The list of candidate community URLs from Assignment 1’s output. Include the top-level domain for each (e.g., `example.com`).  
**Method:** For each distinct base domain that hosts at least one candidate community, fetch the following URLs (if they exist) **using direct HTTP GET requests**:
1. `https://<domain>/robots.txt`
2. `https://<domain>/terms-of-service` or `/terms` or `/tos` or `/legal/terms`
3. `https://<domain>/privacy-policy` or `/privacy` or `/legal/privacy`
4. Any API terms page: look for `/api`, `/developers`, `/developer-terms`, or search the site’s footer.
5. If the platform is a major social network (Facebook, YouTube, Twitter/X, Instagram, TikTok), also fetch their publicly documented Developer Policies, Content Usage Guidelines, and Platform Terms. Search “<platform> developer policy” and “<platform> content redistribution policy”.
6. If the candidate is a federated/self-hosted community (e.g., Mastodon, Lemmy, Discourse), fetch the instance’s About, Terms, and Copyright pages as well as the software project’s default license.
7. For any candidate that appears to be an open-license repository (e.g., Internet Archive, Wikimedia Commons, Project Gutenberg), fetch the relevant collection’s rights statement.
8. For personal blogs or independent sites, look for a stated copyright notice, Creative Commons badge, or a “reuse policy”. If none is found, note “no explicit license found”.

**Capturing:** Save the **entire raw text** of each fetched page with the URL and retrieval timestamp. If a page is not found (404), record that. If access is blocked (403), record the block.  
**Output artifact:** A directory `policy-docs/` containing one file per captured page, and an index file `policy-index.md` that maps each candidate domain to the list of captured URLs, their response statuses, and any gaps.  
**Important:** Do not visit any page containing user-generated content. Stay strictly on policy/info pages.

---

### Assignment 3: Authorization evaluation and readiness recommendation
**Retrieval Query ID:** `REPL-EVAL-01`  
**Focused question:** Which of the candidate communities (identified in Assignment 1 and whose policies were retrieved in Assignment 2) can legally and practically serve as a source for first-person sugar-recovery material in this open-source research repository, meeting all the §1a criteria?  
**Input:** The candidate list from Assignment 1, the policy index from Assignment 2, and the raw policy page texts.  
**Method:** For each candidate community, analyze the collected policy documents and answer the following with direct quotes from the policies where possible:
1. **Automated access / bots:** Does `robots.txt` disallow crawling of the relevant sections? Are there specific API terms that grant or deny programmatic access? Are rate limits documented? If no explicit prohibition, but also no permission, note “implicit permission not established”.
2. **Quotation / excerpt rights:** What does the platform’s Terms of Service or Content License say about users’ copyright? Do users grant a license to the platform only, or also to third parties? Is there a statement allowing “quotation for review or research”? Is there a Creative Commons license on user content? If the jurisdiction allows fair use/dealing, note that but also note the risks of relying on it without platform indemnity.
3. **Retention & deletion:** Does the platform require deletion of user content upon user request (e.g., GDPR right to erasure)? If we store excerpts, can we comply? Does the platform itself have a data retention policy that would cause our stored copies to become stale?
4. **Redistribution / open-source commitment:** Does the platform’s license explicitly permit redistribution of excerpts in a public, version-controlled repository? If not, what is the strongest legal basis for doing so? Consider the repository’s hosting location and applicable law.
5. **User-data protection:** Do the excerpts we plan to capture contain personal data (usernames, profile links, real names)? Does the platform’s privacy policy allow us to republish those? If not, can we anonymize/pseudonymize? Note: the repository’s ethics require we avoid republishing direct personal identifiers; but even anonymized data may be regulated.
6. **Platform authorization programs:** Does the platform have a formal research access program, data licensing, or an academic partnership that could explicitly cover this use? If so, what are the requirements?
7. **Overall readiness:** Based on the above, assign a final verdict:
   - `READY` — we can lawfully and durably collect, retain, and redistribute excerpts from this source right now, with a clearly documented basis.
   - `CANDIDATE — CLARIFICATION NEEDED` — some terms are ambiguous or missing; requires human legal review or direct contact.
   - `REJECTED` — clear prohibitions, missing permissions, or technical blocks that cannot be worked around without violating §1a.

**Output artifact:** `authorization-evaluation.md` with a table row for each candidate community, including:
- community name and base URL
- type (forum, social media group, blog, etc.)
- policy URLs and versions consulted
- verdict
- detailed rationale with quotes
- specific conditions or restrictions that would apply (e.g., “must attribute”, “max 500 characters per quote”, “cannot store avatars”)
- any additional documentation needed before the lead can mark it `READY`.

**Follow-up needed?** If fewer than three candidate families reach `READY`, the evaluation should also suggest alternative discovery paths (e.g., “search for CC-licensed podcast transcripts”, “contact X organization for consent waivers”, “check university IRB-approved studies with published quotes”). These suggestions should be returned as potential new retrieval assignments.

---

## Commission delivery
Return all artifacts (the three output files) to the caller. The scout (this commission) does not require access to the artifact files; the caller will persist them and dispatch the assignments to retrieval subagents as written. The lead will later integrate the authorization-evaluation into the assignment matrix.

Do not proceed to user-content collection. Once the lead approves the `READY` sources, a separate collection worker will be assigned.

**Model/reasoning:** For each assignment above, the caller must use one of the three allowed arms at the top reasoning setting and max output allowance. The scout makes no binding recommendation on which arm to use; the caller chooses.

**End of commission.**
