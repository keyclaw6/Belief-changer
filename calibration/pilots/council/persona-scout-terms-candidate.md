# Persona Architecture Retrieval Commission (Scout Mode)

**Council role:** Architecture Scout (Persona focus)  
**Mode:** **SCOUT** — no retrieval artifacts supplied; producing a retrieval commission only.  
**Objective:** Decompose persona discovery for “Quit Sugar” into focused, authorization-safe retrieval assignments that will yield source-traceable evidence covering Banks 1–6, 9, and 10, supporting later synthesis by the persona specialist.

The artifact below is a **retrieval commission document** ready for the architecture lead and reviewer to audit, augment, and then dispatch to retrieval subagents. It does **not** synthesize personas, cite URLs, or invent quotations. Every proposed source scope states an explicit access/retention basis; sources that cannot support durable open-repository packets are flagged for rejection per §1a. Reddit is excluded entirely per the Reddit Research Authorization requirement.

---

## 1. Retrieval assignments at a glance

| Assignment ID | Source scope | Access / retention basis | Persona coverage | Target banks | Search / query cluster | Expected minimum yield |
|---|---|---|---|---|---|---|
| PA-RET-01 | Stack Exchange network (Fitness, Health, Psychology & Neuroscience, Seasoned Advice, Parenting, Personal Productivity, etc.) | CC BY-SA 4.0 (verified per-page) | All—discover from narratives | 1,2,3,4,5,6,9,10 | Site‑scoped queries on sugar addiction, cravings, quit attempts, relapse, daily routines; personal‑story‑rich threads | 20 distinct Q&A pages |
| PA-RET-02 | Open‑access qualitative research in PubMed Central and other open journals (PLOS ONE, BMC Public Health, etc.) | Article‑specific open license (CC BY, CC BY‑SA, CC0); restrict to full‑text‑redistributable papers | Derived from participant quotes with demographic context | 1,2,3,4,5,9,10 | Sugar + addiction/craving/habit + qualitative/phenomenology; free full text, 2015–2026 | 8 studies, 50+ direct participant quotes |
| PA-RET-03 | Personal blogs / Medium stories with an explicit Creative Commons license (CC BY, CC BY‑SA, CC0) | Author‑declared CC license; verify on each page | All, with deliberate effort to capture underepresented life situations (parents, shift workers, older adults, etc.) | 1,2,3,4,5,9,10 | “quit sugar” / “sugar addiction” + “Creative Commons” or license‑filtered search; manual verification | 10 distinct blog-style narratives |
| PA-RET-04 | Exploratory: non‑Reddit open‑license forums or communities (e.g., Fediverse instances with CC content, select Discourse instances with permissive terms) | Must be verified by worker; default reject if unclear | Whatever available | 1,2,3,4,5,9,10 | Discovery queries; flag for lead if a forum appears promising but license is unconfirmed | 0–5 sources (only if verified) |
| PA-RET-05 | Supplementary: YouTube comments on CC‑licensed videos (if any) | Very likely non‑redistributable; worker confirms legal status; default reject | Negligible unless clear permission found | – | “quit sugar” + YouTube CC filter; comments only if covered by CC | Likely zero |

**Gap coverage note:** PA‑RET‑01 and PA‑RET‑02 are the high‑confidence pillars. PA‑RET‑03 adds breadth across life situations. PA‑RET‑04 and PA‑RET‑05 are speculative; the architecture reviewer may prune or replace them after the first retrieval pass.

---

## 2. Detailed retrieval assignment sheets

### PA-RET-01: Stack Exchange deep dive

- **Source scope:** Stack Exchange network sites: `fitness.stackexchange.com`, `health.stackexchange.com`, `psychology.stackexchange.com`, `cooking.stackexchange.com` (Seasoned Advice), `productivity.stackexchange.com`, `parenting.stackexchange.com`, and any other SE site where sugar‑habit discussions appear.
- **Access / retention basis:** All user‑submitted content on the Stack Exchange network is irrevocably licensed under [CC BY‑SA 4.0](https://stackoverflow.com/help/licensing). This license permits sharing, adapting, and redistributing for any purpose, provided proper attribution is given. The full text of captured pages can be committed to the public repository. *Worker must*: (a) verify the licence link / footer on each captured page, (b) note the exact URL and version, (c) check for any “community wiki” marking (which does not alter the CC BY‑SA status).
- **Persona discovery focus:** All personas—function (energy, stress relief, comfort, reward, social, boredom, etc.) × life situation (student, office worker, parent, shift worker, retiree, etc.). No pre‑fabricated persona set; derive from the data.
- **Target banks (with evidence examples):**
  - **Bank 1 (Justifications):** Stated reasons for eating sugar, e.g., “I need the energy boost in the afternoon”, “It’s my only treat after a long day.”
  - **Bank 2 (Belief map):** Implicit beliefs like “sugar is the only way to stay alert”, “without dessert, meals feel incomplete”, “quitting means I’ll be miserable forever.”
  - **Bank 3 (Lived experience):** Specific low moments, failed attempts, relapse triggers, private arithmetic (“I told myself I’d only have one but ended up finishing the packet…”).
  - **Bank 4 (Special moments):** The most cherished/romanticised sugar scenes—the afternoon chocolate bar, the ice‑cream at night, the pastry with coffee.
  - **Bank 5 (Escape routes):** Moderation rules, substitution tricks, exception‑making (“I’ll just have it on weekends”, “I’ll eat fruit instead”, “I deserve this after what I went through”).
  - **Bank 6 (Analogy candidates):** Any original, non‑scientific comparisons community members use (e.g., “sugar is like a loan shark for energy”).
  - **Bank 9 (Community lexicon):** Slang, euphemisms, self‑descriptions (e.g., “sugar monster”, “carb coma”, “sugar crash”, “hangry” in context).
  - **Bank 10 (Freedom testimonies):** Accounts of life after quitting—surprising changes, revelations, concrete gains.
- **Search / query strategy:**
  - Use the Stack Exchange site‑specific search or Google `site:` searches with broad keywords: `sugar addiction`, `quit sugar`, `sugar cravings`, `can't stop eating sugar`, `sugar binge`, `sugar detox`, `sugar withdrawal`, `break sugar habit`.
  - Also search for personal‑story triggers: `"I eat sugar when"`, `"I need sugar to"`, `"why can't I quit"`, `"I tried moderation"`, `"it makes me feel"`, `"my lowest point"`, `"the moment I realized"`, `"I failed at"`.
  - Prioritise **questions** where the asker describes a personal struggle and **answers** that include first‑person narrative (look for phrases like “in my experience”, “this is what happened to me”). Skip purely technical or citation‑only answers.
  - Scan comments on questions and answers—they often contain the most candid mini‑narratives.
  - Capture the full expanded page (all answers + comments) for each qualifying thread; if paginated, fetch all pages of the same thread.
  - Record exact search strings, tools used, and date/time of each retrieval.
- **Capture method:** Full page HTML or cleaned Markdown, depending on worker tooling. Store under `research/sources/` with unique source IDs.
- **Evidence extraction (to be performed by worker inline or noted for later specialist):**
  - For each full capture, extract **exact quotes** with SE permalink (answer ID, comment ID).
  - Tag each quote with preliminary descriptive tags (e.g., “stress‑relief”, “parent”, “failed‑attempt”, “special‑moment‑chocolate”).
  - Where a quote spans more than one bank, tag all applicable banks.
- **Expected output:** 20+ source packets (each one thread), log events, extracted evidence items.

---

### PA-RET-02: Open‑access qualitative research

- **Source scope:** PubMed Central (PMC) free‑full‑text subset, plus peer‑reviewed open‑access journals known for qualitative health studies (PLOS ONE, BMC Public Health, Appetite (if open), Journal of Health Psychology, etc.). Only articles with an open license allowing redistribution (CC BY, CC BY‑SA, CC0, or public domain) may be captured in full; for others, capture only short direct quotes under fair‑dealing research, marking them as limited‑use.
- **Access / retention basis:** Each article’s license must be verified on the publisher page or PMC entry. Preferred: CC BY (creativecommons.org/licenses/by/4.0/) or CC0. **Full‑text repository deposit** only for these. For restrictive licenses (e.g., CC BY‑NC‑ND, standard copyright), do **not** commit the full article; only short verbatim quotes with full citation are allowed (and those packets must note the redistribution limitation). If a restrictive article contains exceptionally rich persona data, flag it for the lead to consider seeking author/publisher permission.
- **Persona discovery focus:** Derive personas from demographically contextualised participant statements. Look for studies covering diverse populations: adolescents, university students, low‑income adults, pregnant women, shift workers, retirees, etc.
- **Target banks:** Same as PA‑RET‑01, but with the caveat that participant quotes are often anonymised and may lack the rich chatty detail of forums. Prioritise studies that present lengthy quotes or thematic analysis of in‑depth interviews.
- **Search / query strategy:**
  - PubMed Central: `("sugar" OR "sugary" OR "sweet") AND (addict* OR craving OR compulsive OR habit OR dependency) AND (qualitative OR interview* OR "focus group" OR phenomenolog* OR "lived experience" OR "thematic analysis" OR "grounded theory")`. Apply filter: “Free full text”. Publication years: 2015‑2026.
  - For other databases (PLOS, BMC): use the same keyword clusters.
  - Screen abstracts: must involve participants **describing their own sugar consumption experiences** (not just dietary recall). Exclude purely epidemiological or nutritional studies.
  - Retrieve the full text of all short‑listed articles (as PDF or HTML).
  - For licensing verification, check the article’s copyright line and the journal’s open‑access policy.
- **Capture method:**
  - For fully‑open articles: save the complete text (structured, with sections). Include the first page clearly showing the CC license.
  - For non‑open articles: copy only the `Results` and `Discussion` sections that contain participant quotes, and store as an “excerpts” capture. The source packet must state “Limited: full text not redistributable; only short quotes under research exception.”
- **Evidence extraction:** For every direct participant quote, record the page/paragraph, participant pseudonym (if any), demographic details provided, and the bank slots it supports.
- **Expected output:** 8+ source packets (articles or excerpt‑only summaries), 50+ distinct participant quotes.

---

### PA-RET-03: CC‑licensed personal blogs and Medium stories

- **Source scope:** Independently hosted blogs and Medium.com posts that explicitly bear a Creative Commons license.
- **Access / retention basis:** Creative Commons license (CC BY, CC BY‑SA, CC0). The license notice must appear on the page (footer, side‑bar, or post‑specific). Medium articles sometimes have a “license” indicator; if absent, the post is All Rights Reserved and cannot be committed.
- **Persona discovery focus:** Fill life‑situation gaps. Stack Exchange and qualitative studies may under‑capture personas like the low‑income single parent relying on cheap sweets, the retiree with ingrained habits, the shift worker using sugar to manage sleep disruption, or the stay‑at‑home partner snacking throughout the day.
- **Target banks:** 1,2,3,4,5,9,10 (and incidental analogy candidates).
- **Search / query strategy:**
  - Google with combinations: `"I quit sugar" blog "Creative Commons"`, `"my sugar addiction" "CC BY"`, `"sugar addiction" "personal story" CC`, `"life without sugar" "CC0"`.
  - Use dedicated CC search portals (e.g., `search.creativecommons.org`) if they index blogs.
  - For Medium: manually search `site:medium.com "sugar" "CC BY"` or browse stories tagged “Sugar”, “Sugar‑free”, “Addiction” and check the bottom of each story for license info. This is more laborious but essential.
  - Also try: `"quitting sugar" "recovery" blog license`.
  - Aim for a diverse sample: e.g., a mother writing about sugar and kids, a male office worker, a retiree, a student.
- **Capture method:** Save the entire blog post as plain text/Markdown (including the license notice). If paginated, capture all parts. Save as one source packet per URL.
- **Evidence extraction:** As with PA‑RET‑01. Additionally, note the author’s self‑declared demographics (age, job, family situation) to enrich persona mapping.
- **Expected output:** 10 source packets.

---

### PA-RET-04: Exploratory open‑license forums

- **Source scope:** Any active online community where people discuss sugar addiction and the terms of service or content license explicitly permit third‑party reproduction.
- **Access / retention basis:** Must meet the repository‑packet contract. Worker must locate the site’s Terms of Use, Privacy Policy, or content license, and verify that user‑submitted text can be stored and redistributed. If it states “by posting you grant us a worldwide, non‑exclusive license” without extending rights to the public, it is insufficient.
- **Persona coverage:** TBD.
- **Target banks:** 1,2,3,4,5,9,10.
- **Search / discovery strategy:**
  - Explore known openly‑licensed communities: the Fediverse (Mastodon, Lemmy, Peertube) where some instances adopt CC‑based content licenses. Search for hashtags `#quittingsugar`, `#sugaraddiction`, `#sugarfree` on public timelines; check instance rules for content licensing.
  - Look at “Discourse” forums that have added a CC license to their content. Search for `“sugar addiction” forum "creative commons"`.
  - Check “Tildes.net” (https://tildes.net) – content is publicly readable, but licensing terms need verification.
  - If a promising source is found but its license is ambiguous, **do not capture**; instead, create a brief note describing the community, URL, and why it’s promising, and flag for the lead to request permission or obtain a waiver.
- **Capture method:** Only after license confirmation; then capture thread pages as full text.
- **Expected output:** 0–5 source packets (may be zero). This assignment is a probe; its success is not required for Stage A coverage.

---

### PA-RET-05: YouTube comments (low priority, likely dead‑end)

- **Source scope:** Comment sections of YouTube videos that are both about quitting sugar AND are published under a Creative Commons license (YouTube allows creators to mark CC BY when uploading).
- **Access / retention basis:** The video itself is CC‑licensed, but YouTube’s Terms of Service and the CC license’s treatment of “derivative works” make comment redistribution legally uncertain. Comments are not explicitly covered by the CC BY license, and YouTube’s ToS grants YouTube (not the public) broad rights. Therefore, **default reject**.
- **Target banks:** – (if miraculously found to be permissible, treat as supplementary).
- **Query:** Use YouTube’s filter “Creative Commons” for search terms `quit sugar`, `sugar addiction my story`, etc. Open a few videos and inspect the license. Then examine the comment threads.
- **Capture method:** None unless worker after research provides a clear legal basis (e.g., the creator explicitly states comments are also CC‑licensed).
- **Expected output:** Most likely zero. Package any legal research and recommendations for the lead.

---

## 3. General worker instructions

- **Arms and reasoning:** Allowed models: `deepseek/deepseek-v4-pro` (xhigh), `minimax/minimax-m3` (reasoning enabled), `openai/gpt-5.6-luna` (max). The caller will assign one and provide the endpoint’s maximum output allowance. Do not lower reasoning depth or output length for speed/cost.
- **Logging:** Every search, call, source capture, and revisit must produce a chronological log event (see protocol schema). Even rejected sources get log entries with reason.
- **Source packets:** Follow the **§3 schema** exactly. One packet per distinct URL. Repeated visits enrich the same packet, not a new one.
- **Evidence items:** All quotes must be verifiable against the captured raw source text. Use `EXACT_QUOTE` with precise locator (URL + selector/element ID). Convert to `INTERPRETATION` only when text is paraphrased and cannot be matched character‑for‑character. No quotation marks around interpretations.
- **Persona tagging:** Tag each evidence item with preliminary functional+life‑situation tags based on the content (e.g., `#function-energy`, `#life-parent`). These are working labels; the specialist will later consolidate into formal personas.
- **Exclusion strictness:**
  - **No** Allen Carr, Easyway, or referenced‑methods content.
  - **No** communities whose defining condition is an excluded non‑goal (eating‑disorder treatment, diabetes management, medical nutrition therapy). However, an individual thread/post may be used if its core topic is everyday sugar compulsivity, even if the poster mentions a comorbidity; use judgment.
- **Retention & deletion obligations:** If a source requires periodic deletion or restricts data retention, reject it (unless a compliant out‑of‑repo storage design is approved, which is not the default). All accepted sources must be free of retention/destruction duties that conflict with indefinite Git storage.
- **Gap and follow‑up:** If a source appears promising but its access/retention basis cannot be confirmed, do **not** rely on it. Instead, document the attempted verification and the unresolved policy gap in a log event and move on. The lead may later attempt to obtain explicit permission.
- **Duplicate URLs:** The same underlying URL across different search queries is only one source. Workers should coordinate (or the worker can de‑duplicate within its own assignment). If two assignments capture the same URL, the later one enriches the earlier packet.

## 4. Blind spots, risks, and recommendations for the lead

- **Demographic skew:** Stack Exchange users skew young, male, tech‑literate. Open‑access studies often recruit university populations. Bloggers are typically articulate and health‑conscious. We may underrepresent low‑income, non‑English‑speaking, or digitally‑excluded personas. Recommend the lead commission a future pass targeting communities in other languages (e.g., Spanish‑speaking forums with open licensing) or partner with a community organisation for interviews (with explicit consent for open‑data release).
- **No Reddit, no large‑scale social media:** The Reddit exclusion eliminates the single largest hub of sugar‑addiction narratives. While Stack Exchange and blogs can meet the numeric floors, qualitative depth may require additional targeted work. The lead should watch for thinness in Banks 3, 4, and 5 (lived experience, special moments, escape routes). If present, commissioning a dedicated source scout to find an alternative openly‑licensed community is advisable.
- **Bank 6 (analogies):** Community‑generated analogies may be sparse apart from Stack Exchange and blogs. The final architecture will need to supplement with `INVENTED` analogies, which must be clearly documented as such and grounded in the captured behavior‑theme.
- **Bank 8 (villain dossier) and Bank 7 (mechanism science):** These are out of persona scope and will be addressed by separate scientific/investigative specialists (per the council design). They do not need persona data.
- **Recommendation for reviewer:** Before dispatch, the reviewer should: (a) verify the feasibility of the Stack Exchange assignment (the site’s current robots.txt and rate‑limits may require polite crawling; ensure the worker has appropriate tooling), (b) confirm that the open‑access article filter will yield enough participant quotes, (c) decide whether to prune PA‑RET‑04/05 or expand them.

---

## 5. Immediate next actions

1. This commission is hand‑off to the **architecture lead**.  
2. The lead will integrate it with the other scout tracks (community discovery, science mapping, investigative mapping), fill the assignment matrix, and submit the combined architecture to the **architecture reviewer**.  
3. The reviewer will audit persona coverage, source depth, and license compliance; if acceptable, the lead will dispatch the retrieval workers.  
4. Workers produce source packets and logs; the persona specialist (same agent in synthesis mode) will then build the actual persona set from the accepted evidence.

**End of retrieval commission.**
