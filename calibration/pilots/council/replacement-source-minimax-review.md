
## Review Verdict

The commission is broadly aligned with §1a, the scout/synthesis split, and the blindness and model-autonomy requirements, but it is not yet genuinely safe and sufficient to dispatch. Six material gaps: (1) search queries are sugar-only and miss the "junk carbs" half of the target behavior; (2) no scope-fit filter against the brief's non-goals (medical nutrition therapy, diabetes management advice, eating-disorder treatment, weight-loss-program mechanics); (3) no active-status requirement, so a candidate could be topically perfect but long dead; (4) the "discard if mentions Reddit" rule is too aggressive and would discard independent sites that happen to be cross-linked; (5) no explicit shortlist, no minimum ready-families target, and no formalized fallback when zero or fewer than three families reach `READY`; (6) the retention/redistribution test does not enforce the "no deletion refresh, no project-limited access" hard line in §1a. Returning the complete corrected commission below.

I do not patch rows; I return the full replacement. No user content is accessed or fetched by this review. No retrieval subagents were commissioned by me.

---

# Retrieval Commission — REPL-SUGAR-FIRSTPERSON-AUTH-01 (REVISED)

**Assignment ID:** REPL-SUGAR-FIRSTPERSON-AUTH-01  
**Worker ID (scout):** REPL-DISCOVERY-01  
**Date:** 2026-07-11T00:00:00Z  
**Status:** COMMISSIONED — no user content retrieved yet  
**Arms allowed:** DeepSeek V4 Pro (`deepseek/deepseek-v4-pro` at `xhigh`), MiniMax M3 (`minimax/minimax-m3` reasoning enabled), GPT-5.6 Luna (`openai/gpt-5.6-luna` at `max`). Caller selects and verifies exact runtime model ID and top reasoning config before dispatch. Scout makes no binding arm recommendation.

## Objective

Discover **authorization-compatible replacement source families** that can provide first-person sugar/junk-carb recovery and experience material for Banks 1–6, 9, and 10. The commissioned retrieval subagents must:
- identify at least three independent candidate families whose discussions are still active in 2026 and span at least two materially different life situations (so the lead can later segment ≥3 personas);
- verify each candidate's legal and technical compliance with the repository's open-source, persistent-retention, and redistribution requirements (§1a);
- deliver enough compliant sources to meet or exceed the original numeric and qualitative depth targets (≥2 sources per persona-bank cell, etc.) without Reddit, Stack Exchange, or any unauthorized platform.

### Hard constraints (repeated for each subagent)
- **No Reddit or Stack Exchange** unless explicit platform authorization already exists (it does not — these are banned). A candidate *cross-linked from* Reddit is not disqualified; a candidate that *is* Reddit is.
- No user-content retrieval before the candidate source's access terms, robots/access controls, automation permission, license/excerpt rights, and retention/deletion obligations are verified and marked `READY` by the lead.
- No stealth, spoofing, mirrors, workarounds, or alternate endpoints to bypass access controls or rate limits.
- Every accepted URL must support **permanent Git retention** and **redistribution of raw captures and excerpt packets** in this open repository. A source that requires deletion refreshes, project-limited access, or forbids raw redistribution is rejected; no alternative storage design is approved.
- All retrieved policy pages and search result excerpts must be captured as visible artifacts with timestamps and URLs.
- The retrieval subagent records exact endpoint model ID, reasoning config, max output allowance, search settings, and any usage/cost visible at runtime (the caller provides final numbers; the agent reports what it used).
- **Rate limit:** no more than one search query per second per engine; no more than one policy fetch per second per domain. A blocked transport is reported, not retried through a different transport.

---

## Retrieval assignments

Dispatch in order. The output of each assignment is the visible input to the next. The scout provides no pre-learned sources; all discovery is web-retrieved.

---

### Assignment 1: Broad candidate community discovery

**Retrieval Query ID:** `REPL-DISC-01`  
**Focused question:** What active online communities, blogs, open-license repositories, podcast feeds, or self-hosted forums host first-person discussions or personal stories about quitting refined sugar, breaking the sugar/snack craving loop, or recovering from junk-carb compulsion? Search must cover both the **sugar** and the **junk-carb / refined-carb** sides of the target behavior.

**Scope-fit filter (apply during discovery, refine during evaluation):** the candidate's primary content must be first-person experience of the craving/snacking loop, the trap, or the recovery arc. Sources that are *primarily* medical nutrition therapy, diabetes management, eating-disorder treatment, or weight-loss-program mechanics are out of scope and are noted as such — they are not banned as sources, but they are tagged "OUT-OF-SCOPE — DIABETES" etc. so the lead can decide whether any sub-thread remains in scope. Sources focused on children's sugar intake are tagged separately ("PARENT-FRAMED") so the lead can decide whether that persona segment is materially distinct from the general adult reader.

**Excluded platforms (banned without platform authorization):** Reddit, Stack Exchange, Quora (treat as banned unless their data partnership is later approved), Discord servers (private, no programmatic access), closed Facebook groups, Telegram groups, any private Discord/Slack/WhatsApp community. **Not blanket-banned, but require careful policy evaluation in Assignment 2:** Facebook (public pages only — not user content), YouTube (channel descriptions, public transcripts of creator's own speech, not user comments), Medium (per-article license), Substack (per-author), personal WordPress/Blogger/Typepad blogs, self-hosted Discourse and Lemmy/Mastodon instances, podcast RSS feeds, Internet Archive, Wikimedia Commons, university press / open-access journal article author-deposited copies.

**Search queries (sugar side):**
- "quit sugar forum"
- "sugar addiction support group"
- "I quit sugar stories"
- "sugar free journey blog"
- "sugar cravings community"
- "sugar detox discussion"
- "breaking sugar addiction forum"
- "sugar free living group"
- "how I overcame sugar addiction"
- "sugar recovery testimonial"
- "sugar addiction personal story"
- "sugar free living blog"
- "sugar addiction help site:healthunlocked.com"
- "quitting sugar site:myfitnesspal.com" (note: MFP forums are not public — flag as candidate only, expect REJECT in Assignment 3)
- "sugar detox stories site:medium.com"
- "sugar addiction podcasts"
- "sugar recovery YouTube channel"
- "sugar addiction open access"
- "sugar addiction personal narratives public domain"

**Search queries (junk-carb / refined-carb side — required, do not skip):**
- "quit carbs forum"
- "low carb journey blog"
- "keto journey personal story"
- "I quit carbs community"
- "carb addiction recovery"
- "refined carb cravings"
- "processed carb addiction stories"
- "bread pasta sugar addiction"
- "carbohydrate addiction forum"
- "junk food cravings community"
- "stopped eating sugar and flour"
- "sugar and flour free blog"

**Search queries (open-license / archive side):**
- "sugar addiction site:archive.org"
- "sugar recovery site:wikibooks.org"
- "sugar addiction site:wikiversity.org"
- "sugar addiction open access journal author manuscript"
- "qualitative study sugar quitting"
- "phenomenological study sugar addiction"

**Method:** Run the queries on a standard web search engine (Google, Bing, DuckDuckGo) at top reasoning allowed. Use a real-user User-Agent string (the standard one the caller's tooling provides); do not rotate identities. Save the **exact search result page text** (titles, snippets, URLs) for the first 30 results per query. Do not click into user-content pages yet. Record search settings (engine, date filters if any, region, safe search) and the exact query that produced each result set.

**De-duplication:** normalize URLs (strip tracking parameters, force https, lowercase host); collapse near-duplicates; produce a final list of distinct candidate URLs and the *unique base domains* that host them.

**Output artifact:** `candidate-communities-raw.md` containing:
- the full search result captures (engine, query, timestamp, top 30 raw results per query);
- a de-duplicated table of unique candidate URLs with: candidate name, base domain, snippet from search result, a "type" tag (independent forum, hosted community on large platform, personal blog, podcast feed, open repository, academic author manuscript, etc.);
- a separate column flagging the scope-fit verdict per candidate (`IN-SCOPE`, `OUT-OF-SCOPE — DIABETES`, `OUT-OF-SCOPE — ED`, `OUT-OF-SCOPE — WEIGHT-LOSS`, `OUT-OF-SCOPE — MEDICAL`, `PARENT-FRAMED`, `INCONCLUSIVE`);
- the unique base domains list, which feeds Assignment 2.

**Model/reasoning:** Caller's choice from the three allowed arms at top reasoning and max output allowance. Record configuration in output metadata.

**Do not evaluate authorization yet.** This is existence, activity, and scope-fit discovery. If a candidate is `OUT-OF-SCOPE` for the brief's purpose, it is still captured — it just won't be a primary source.

---

### Assignment 2: Policy document retrieval

**Retrieval Query ID:** `REPL-POLICY-01`  
**Focused question:** What are the formal access terms, robots controls, API/automation rules, content licensing, retention/deletion requirements, and redistribution rights for each candidate base domain discovered in Assignment 1?

**Input:** The list of unique base domains from Assignment 1's output.

**Method:** For each distinct base domain that hosts at least one candidate community, fetch the following URLs (if they exist) **using direct HTTP GET requests with a real-user User-Agent**:

1. `https://<domain>/robots.txt`
2. `https://<domain>/terms-of-service`, `/terms`, `/tos`, or `/legal/terms`
3. `https://<domain>/privacy-policy`, `/privacy`, or `/legal/privacy`
4. Any API terms page: look for `/api`, `/developers`, `/developer-terms`, or search the site's footer.
5. **Platform-specific fetches when the candidate is a major social network** (Facebook public pages, YouTube, Twitter/X, Instagram, TikTok): also fetch the platform's publicly documented Developer Policies, Content Usage Guidelines, and Platform Terms via web search ("<platform> developer policy", "<platform> content redistribution policy").
6. **Federated / self-hosted community** (Mastodon, Lemmy, Discourse, PieFed, etc.): fetch the instance's About, Terms, and Copyright pages, and the software project's default license.
7. **Open-license repository candidates** (Internet Archive, Wikimedia Commons, Project Gutenberg, university open-access repositories): fetch the collection's rights statement.
8. **Personal blogs / independent sites:** look for a stated copyright notice, Creative Commons badge, or a "reuse policy." If none is found, note "no explicit license found" — the site is still in play, but the evaluation will need to rely on the platform's default legal regime plus the author's implicit copyright.

**Hard limits:**
- Stay strictly on policy / info / API / developer / about / terms / privacy / copyright / license / robots pages. **Do not visit any page containing user-generated content.**
- Do not bypass robots.txt. If `robots.txt` disallows `/legal/` or similar, record the block and try the next listed policy URL; do not route around.
- One fetch per second per domain.
- If a page is not found (404) or blocked (403), record the status and continue. A blocked transport is not retried through a different transport.

**Capturing:** Save the **entire raw text** of each fetched page with the URL and retrieval timestamp. For HTML pages, save the rendered text and a note about any linked assets (logos, fonts) that were not captured.

**Output artifact:**
- a directory `policy-docs/` containing one file per captured page, named `<domain>__<page-slug>.md`;
- an index file `policy-index.md` that maps each candidate domain to the list of captured URLs, HTTP status, fetch timestamp, and any gaps.

---

### Assignment 3: Authorization evaluation, activity check, scope-fit re-verification, and shortlist

**Retrieval Query ID:** `REPL-EVAL-01`  
**Focused question:** Which of the candidate communities can lawfully and durably serve as a source for first-person sugar-recovery material in this open-source research repository, meeting all the §1a criteria — including activity in 2026, scope-fit to the brief, and the no-deletion-refresh / no-project-limited-access hard line?

**Input:** The candidate list from Assignment 1 (with scope-fit tags), the policy index from Assignment 2, and the raw policy page texts.

**Method — four sub-checks per candidate:**

**Sub-check A — Active status (mandatory; a stale community is not a source):**
- For each candidate, look for a "last post" or "last updated" signal. For forums: the most recent thread or post date on the front page or in a relevant sub-forum. For blogs: the most recent post date. For podcasts: the most recent episode date. For YouTube: the most recent upload date on the channel.
- If no activity signal is observable without scraping user content, record that and use the page's `Last-Modified` HTTP header as a fallback signal (cite both).
- Reject as `STALE` if no activity in the last 24 months (relative to 2026-07-11). Reject as `UNVERIFIABLE` if no activity signal is obtainable at all.

**Sub-check B — Scope-fit to the brief:**
- Confirm the candidate's primary content is first-person experience of the craving-snacking loop on refined sugar and/or junk carbs, not the excluded categories (medical nutrition therapy, diabetes management, eating-disorder treatment, weight-loss-program mechanics).
- If the candidate is `PARENT-FRAMED` or focuses on children's intake, the lead will later decide whether that constitutes a materially distinct persona from the general adult reader; the scout just records the tag.
- If scope-fit is mixed (e.g., 60% diabetes management, 40% personal experience of the craving loop), record the mix and recommend whether the personal-experience portion is large and distinct enough to be a primary source on its own, or only a supplementary source.

**Sub-check C — Authorization (§1a hard line):**
For each candidate, analyze the collected policy documents and answer with direct quotes where possible:

1. **Automated access / bots:** Does `robots.txt` disallow crawling of the relevant sections? Are API terms documented? Are rate limits documented? If neither prohibition nor explicit permission, record "implicit permission not established."
2. **Quotation / excerpt rights:** Does the platform's ToS / content license grant users a license to the platform only, or also to third parties? Is there a fair-use / fair-dealing carve-out acknowledged by the platform? Is there a Creative Commons badge on the user content (Medium, Wikimedia)? Note: the repository will still apply its own ethics (no direct personal identifiers republished; usernames pseudonymized where present), but the platform's own contract is the first question.
3. **Retention & deletion (HARD LINE):** Does the platform require deletion of user content upon user request (GDPR Article 17, equivalent regimes, or platform-specific "right to be forgotten")? If we store excerpts, can we comply without scrubbing the repository on a refresh cycle? If the platform's deletion regime requires us to delete-on-request or to refresh-our-cache, **the source is rejected** under §1a — the hard line is "no deletion refresh." The repository's packet contract is permanent Git retention.
4. **Redistribution / open-source commitment:** Does the platform's license explicitly permit redistribution of excerpts in a public, version-controlled repository? If not, what is the strongest legal basis (fair use / fair dealing, explicit CC, author waiver)? Consider the repository's hosting location and applicable law.
5. **Project-limited or revocable research access (HARD LINE):** Does the platform offer a research data program that requires project registration, requires deletion, or limits use to a named project? If so, the source is **rejected** under §1a — "project-limited or revocable research access" cannot satisfy the packet contract without a separately approved storage design, and no such design is approved.
6. **User-data protection:** Do the planned excerpts contain personal data (usernames, profile links, real names, avatars)? Does the platform's privacy policy allow republishing? The repository will pseudonymize usernames and strip avatars regardless; the question here is whether the *underlying content* may be retained at all.
7. **Platform authorization programs:** Does the platform have a formal research access program or academic partnership? If so, what are the requirements? If the program's terms satisfy the hard line (no deletion refresh, no project-limited use, allows permanent retention and redistribution), the source may be eligible. If not, the source is rejected.
8. **Overall readiness verdict:** Assign exactly one of:
   - `READY` — lawful and durable collection, retention, and redistribution right now, with documented basis. Hard line passes. Activity signal present. Scope-fit holds.
   - `CANDIDATE — CLARIFICATION NEEDED` — some terms are ambiguous, missing, or require direct contact with the platform or a community moderator. Lead must commission follow-up contact, not bypass.
   - `REJECTED — UNAUTHORIZED` — clear prohibition, missing permission, deletion-refresh regime, or project-limited access that cannot satisfy the packet contract. Hard line fails.
   - `REJECTED — STALE` — no activity in 24 months. Hard line fails on currency.
   - `REJECTED — OUT-OF-SCOPE` — primarily medical / diabetes / ED / weight-loss; not a primary source for the brief.

**Sub-check D — Persona-coverage and shortlist:**
- Tag each `READY` candidate with the life-situation / function-of-behavior signals visible from the discovery snippets and any policy-page indicators (e.g., "long-term daily sugar user", "parent quitting for the family", "perimenopausal woman quitting sugar", "fitness/performance-motivated quitter", "chronic relapser", "12-step / recovery-movement participant").
- The lead will later segment personas; the scout's job here is to surface diversity, not to lock personas.
- Produce a **shortlist of at least three `READY` candidate families spanning at least two materially different life situations.** If fewer than three families reach `READY`, the evaluation must also produce a **follow-up proposal** (see below).

**Output artifact:** `authorization-evaluation.md` containing:
- a per-candidate table with: community name, base URL, type, scope-fit tag, activity signal (date + source), policy URLs and versions consulted, the eight sub-check answers (with direct quotes), overall verdict, and any conditions or restrictions (e.g., "must attribute", "max 500 characters per quote", "no avatar capture", "pseudonymize usernames", "exclude any post marked with [personal] tag").
- a `READY` shortlist (≥3 families, ≥2 life situations) with a per-family recommendation of how many independent URLs the collection worker should aim to capture and which banks each family is best suited to serve.
- a follow-up proposal **only if** the shortlist has fewer than three `READY` families. The proposal must name:
  1. additional discovery queries (e.g., "CC-licensed podcast transcripts via Internet Archive", "academic author-deposited copies in university open-access repositories", "open-license book chapters on sugar addiction in PubMed Central or OAPEN", "interview-based qualitative studies with first-person quotes published under CC-BY");
  2. platforms whose data-partnership or research-program terms would have to be evaluated (e.g., "check if HealthUnlocked has a research API and what its terms are", "check if MyFitnessPal has any public research-access path");
  3. direct-consent fallback — only if a candidate community's moderators are reachable and the run is willing to do documented consent outreach (the run is **not** willing to do this implicitly; the proposal just records the option);
  4. an honest declaration of which Banks are likely unfillable if `READY` count stays low, so the lead can surface the gap rather than fill it by invention.

**Hard line in the evaluation output:** any candidate whose hard line (Sub-check C items 3 and 5) is not passed is **not** marked `READY`, regardless of how strong the topical fit is. Evidence depth never excuses an unauthorized source.

---

## Commission delivery

Return all three artifacts to the caller:
1. `candidate-communities-raw.md`
2. `policy-docs/` directory and `policy-index.md`
3. `authorization-evaluation.md` (with the `READY` shortlist and, if needed, the follow-up proposal)

The scout does not access user content and does not write source packets. The caller persists the artifacts and dispatches collection workers only against the `READY` shortlist. A separate collection worker will be commissioned per `READY` family with the full protocol-required matrix row, source-authorization basis, and runtime configuration.

**Model/reasoning:** For each assignment above, the caller must use one of the three allowed arms at the top reasoning setting and max output allowance. The scout makes no binding recommendation on which arm to use; the caller chooses, and the caller's preflight verifies the exact runtime model ID and reasoning configuration before dispatch. If a provider ceiling is reached, the caller continues the role agentically or selects a larger-capacity endpoint — research does not stop on capacity.

**End of commission.**
