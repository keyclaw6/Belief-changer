# Channel-Policy Retrieval Commission

```
Destination path: research/channels/REPL-AUTH-CHANNEL-01-commission.md
Status: SCOUT OUTPUT — NO FETCHES PERFORMED
```

---

## 0. Mode declaration

This artifact is a **scout-stage retrieval commission only**. The scout has not opened, fetched, inspected, cached, mirrored, or otherwise touched any user content, candidate post, comment, thread, search snippet, feed item, transcript, or archived record. No community, platform, API endpoint, or document is declared authorized in this artifact. Every authorization claim must be re-validated by a downstream retrieval subagent against a *current* policy document, regardless of any prior protocol date.

If a downstream agent believes authorization can be established from memory, that belief is to be treated as unverified and the channel is to be marked `CHANNEL — CLARIFICATION NEEDED`.

---

## 1. Brief recap relevant to channel selection

The research objective is raw-material collection for a general-adult book on quitting refined/added sugar and the craving–snack loop. The architecture will need, at minimum:

- **Banks 1–6, 9, 10 (lived experience / community language):** first-person recovery and experience text from affected adults. Will need permissive, durable, redistribution-allowed community or open-license text.
- **Bank 7 (mechanism and science):** peer-reviewed or authoritative scientific sources on the sugar/carb loop, withdrawal, sensory profile, escalation, and self-created low. Strongly favors open access and stable canonical URLs.
- **Bank 8 (villain dossier — engineered demand):** primary industry documents, internal memos, trade publications, regulatory filings, marketing analyses, and investigative journalism on product engineering, formulation, and marketing of added sugar.
- **Cross-cutting:** archival (Wayback), search, citation (Crossref/OpenAlex), and rights-metadata registries (DOAJ, DOAB, CC Catalog, OpenAlex) needed to verify licenses, locate primary copies, and prove provenance.

This brief is therefore unusually broad in channel needs: heavy social/community + heavy scientific/regulatory + heavy investigative/industry. Channel authorization must be evaluated with that mix in mind.

---

## 2. Commission scope and non-scope

**In scope for the next retrieval subagent(s):**

- Identifying and validating the *current* access/automation/redistribution policy of every named channel.
- Locating, capturing, and quoting (verbatim, with version date) the *policy document itself* — not the channel's user content.
- Recording official policy URL, version date or effective date, the section/heading that addresses each authorization question (automation, API, scraping, retention, redistribution, deletion, project-limited or revocable terms), and the open-license markers where they exist.
- Producing a `CHANNEL POLICY` packet per channel at `research/sources/<channel-id>.md` using the standard packet schema in §3, restricted to the policy text and its metadata (no user content).

**Explicitly out of scope for this commission:**

- Any topical, community, user-content, post, comment, thread, transcript, feed item, search snippet, or archived content fetch.
- Any Reddit, Reddit-derivative, or unofficial-Reddit-scraper interaction, including public RSS, public JSON endpoints, search snippet captures, or Wayback-Machine mirrors of Reddit. The next agent is to confirm the *current* state of Reddit's research access program (see §6.1), not assume the 2026-07-10 framing in the brief.
- Any fingerprint spoofing, identity rotation, stealth transport, or access-control bypass.
- Any non-policy content capture from a channel whose policy has not yet been validated.

**Open-ended by design:**

- Query strategy, agent count, recursion, ordering, and time/spend are delegated to the next agent. Quality — defined as authorization evidence depth, policy-statement fidelity, and version freshness — is the only optimizer.

---

## 3. Standard channel-policy packet schema

The retrieval subagent is to produce exactly one Markdown packet per distinct channel-policy URL, conforming to:

```markdown
# <Channel ID> — <Channel name>

- **Source ID:** <ID>
- **URL:** <canonical policy URL, e.g. https://.../terms or /robots.txt or /api/license>
- **Title:** <policy document title>
- **Retrieved (UTC):** <timestamp>
- **Channel / source type:** <channel family and subfamily>
- **Access / retention basis:** <license name, version, link; or "TBD — not yet established">
- **Deletion / refresh obligations:** <none | scheduled | revocable | per-request | TBD>
- **Query ID:** <ID>
- **Assignment ID:** REPL-AUTH-CHANNEL-01
- **Worker ID:** <subagent ID>
- **Runtime model ID:** <exact ID>
- **Reasoning config:** <exact request setting>
- **Maximum output allowance:** <endpoint maximum after input context>
- **Search settings:** <engine, filters, date range, limits>
- **Research-log event IDs:** <IDs>
- **Disposition:** ACCEPTED | REJECTED | CHANNEL — CLARIFICATION NEEDED

## Policy checks performed

| Authorization question | Policy section / heading | Verbatim answer (or "not addressed") | Compliance for this project |
|---|---|---|---|

(Required rows: automation / API use, robots/access controls, rate limits, permitted fields/endpoints, retention rights, redistribution rights, deletion/refresh duties, project-limited or revocable terms, current policy version date.)

## Captured raw policy text

### <Capture ID>
- **Retrieved (UTC):** <timestamp>
- **Source locator:** <section, heading, paragraph anchor>
- **Capture method:** <direct page text | PDF text | archived snapshot | exact search excerpt>

<unchanged retrieved excerpt>

## Evidence items

### <Evidence ID>
- **Evidence ID:** <ID>
- **Kind:** EXACT_QUOTE | INTERPRETATION
- **Text:** <evidence>
- **Capture ID:** <ID>
- **Locator:** <precise locator within the capture>
- **Persona tags:** N/A — policy-only
- **Bank slots:** N/A — policy-only
- **Evidence grade:** SUPPORTED | MIXED | CONTESTED | N/A
- **Use / limits:** <what this authorizes or restricts; what remains unverified>
```

Every quoted policy sentence must be character-for-character in the named capture and locator must point to the section/paragraph.

---

## 4. Channel families and sub-channels to investigate

The next agent is to investigate **all** of the following, may add any others it discovers through policy pages, robots.txt, or registry cross-references, and is to report on gaps with reasons rather than silently dropping channels. Each sub-channel should be evaluated independently — a parent platform's general policy does not authorize a sub-product without separate validation.

For each sub-channel, the next agent should record: parent platform, sub-product, canonical policy URL discovered, version/effective date, and disposition.

### 4.1 General web search engines (community & topical discovery)

Purpose: locate forums, threads, articles, blog posts, news, podcasts, videos. Risk: even when search snippets themselves are not retained as evidence, the search index policy governs mass retrieval and may impose rate or reuse limits.

Sub-channels to evaluate (each is its own channel):
- Google Programmable Search Engine / Custom Search JSON API (paid, with TOS)
- Bing Web Search API (Microsoft)
- DuckDuckGo (no first-party search API; evaluate any documented partner endpoint)
- Brave Search API
- You.com Search API
- Kagi (paid, private)
- Mojeek (independent index, evaluate any documented API)
- Marginalia.nu (independent, evaluate)
- Yandex (evaluate, with note on data residency and current sanctions posture if relevant)
- Baidu (evaluate, with same note)

Policy questions specific to this family: snippet-redistribution rights, caching rights, attribution requirements, prohibition on constructing derivative databases, prohibition on training or fine-tuning, rate limits, project-limited or paid-tier revocation.

### 4.2 Open scholarly infrastructure (Bank 7)

Purpose: locate and cite primary scientific evidence on sugar/carbohydrate mechanisms, withdrawal, sensory science, neuroscience, and epidemiology.

Sub-channels to evaluate:
- PubMed / NCBI Entrez / E-utilities API (NIH public domain for MeSH; abstract/license varies by journal)
- Europe PMC (open access subset; REST API; full-text license varies)
- OpenAlex (open catalog of scholarly works; open data license; API)
- Crossref REST API (Funder Registry, license URL in deposit metadata)
- Semantic Scholar Graph API (open for non-commercial; check current terms)
- Unpaywall API (open data, used to find open-access copies)
- CORE API (aggregator of open-access research)
- DOAJ (Directory of Open Access Journals — license metadata)
- DOAB (Directory of Open Access Books)
- OAPEN Library
- arXiv (preprint server; specific license per paper)
- bioRxiv / medRxiv (preprint; license per paper)
- SSRN (license per paper)
- OpenCitations COCI / COCI API
- OSF (Open Science Framework; license per project)
- Zenodo (license per record)
- Figshare (license per record)
- PsyArXiv, SocArXiv, MedArXiv (preprint servers)
- ClinicalTrials.gov (public domain; API)
- WHO ICTRP (International Clinical Trials Registry Platform)
- Cochrane Library (open access for some reviews; check current model)
- BMJ Open, PLOS, eLife, F1000Research (fully OA; per-journal policy still required)
- JBI (Joanna Briggs Institute) EBP database
- Nutrition Evidence Library (USDA, archived — locate current status)

Policy questions specific to this family: API terms, mass-download limits, redistribution of abstracts, license per record (verify via Crossref / Unpaywall / DOAJ before retention), version-of-record vs preprint, embargo status.

### 4.3 Health authority and regulatory science (Bank 7)

Purpose: authoritative position statements, dietary guidelines, GRAS notices, risk assessments, and clinical guidance.

Sub-channels to evaluate:
- WHO publications and API
- CDC
- NIH (including NIDDK, NIDA, NHLBI)
- FDA (including GRAS notice inventory, 21 CFR)
- EFSA
- Health Canada
- NHS / Public Health England / UK Office for Health Improvement and Disparities
- NICE
- Dietary Guidelines for Americans (USDA/HHS, current edition)
- EFSA Scientific Opinions (open access)
- The Cochrane Collaboration outputs that are gold or green open access
- AHRQ Evidence Reports

Policy questions: public-domain status of government works (with jurisdiction caveat — US Federal works are generally not subject to copyright; UK Crown copyright has specific reuse terms; EU has reuse Decision 2011/833/EU), API access terms, embargo periods on derivative databases, language restrictions, version freshness.

### 4.4 Industry documents and primary investigative sources (Bank 8)

Purpose: trace the engineering of sugar demand — formulation, marketing, executive memos, trade-secret filings, and academic-industry relationships.

Sub-channels to evaluate:
- UCSF Industry Documents Library — Food Industry Documents subarchive
- UCSF Truth Tobacco Industry Documents (the "tobacco playbook" often cross-applies)
- UCSF Drug Industry Document Archive (cross-check for sugar-drug industry overlap)
- The Sugar Association archive / public relations materials
- World Sugar Research Organisation publications
- Sugar Industry Foundation (historical)
- International Sugar Research Foundation (historical)
- Center for Science in the Public Interest (CSPI) reports
- Action on Sugar publications
- BMJ investigations archive (e.g., the Kearns/Schillinger sugar-industry funding series)
- JAMA Internal Medicine investigations archive
- The Guardian and Observer investigative series on sugar (open web; check license)
- ProPublica (open articles, specific license)
- Reuters Investigates
- AP Investigations
- Bureau of Investigative Journalism
- The Intercept
- DocumentCloud (hosted primary documents; per-document license)
- MuckRock (FOIA archive; per-document status)
- GovernmentAttic.org
- CourtListener / RECAP (US federal court documents; PACER vs RECAP redistribution rules)
- PACER (US federal courts; access fees and redistribution rights)
- US Right to Know (FOIA outputs; license per document)
- FOIA.gov
- USAspending.gov (grant and contract data)
- OpenSecrets (US political finance data)
- Lobbying disclosures (US Senate LDA / House)
- EU Transparency Register
- EFSA register of questions / applications
- FDA GRAS notice inventory and FOIA reading room
- USDA Sugar Program documentation
- WTO dispute documents (e.g., sugar disputes)
- ICC, OECD, FAO, Codex Alimentarius (sugar standards)
- ISO standards (sensory evaluation of sweeteners; subscription required — note for the lead)

Policy questions specific to this family: per-document copyright (industry documents are typically still owned by the disclosing entity unless transferred), FOIA public-domain status in the disclosing jurisdiction, journalist copyright in commissioned investigations, embargo and redaction status, repository redistribution rights (UCSF, DocumentCloud, MuckRock, CourtListener each have distinct terms).

### 4.5 Open-license content registries (rights metadata)

Purpose: verify licenses, locate primary copies, support Bank 6 invent-but-source claims, and prove packet provenance.

Sub-channels to evaluate:
- Creative Commons Catalog API and license deeds (CC BY, CC BY-SA, CC BY-NC, CC BY-NC-SA, CC BY-ND, CC BY-NC-ND, CC0)
- Open Data Commons licenses registry
- GNU Free Documentation License (GFDL) project pages
- Public Domain Mark / Public Domain tools
- Open Source Initiative (OSI) license list
- SPDX License List
- RightsStatements.org (cultural heritage rights statements)
- Europeana Data Exchange Agreement
- Digital Public Library of America (DPLA) API
- HathiTrust (rights database)
- Internet Archive metadata and license pages
- Wikimedia REST API and Wikimedia Commons licensing policy
- Wikidata license
- Wikisource (public-domain emphasis; per-text status)

Policy questions: registry API terms, mass-export rights, license-version compatibility, marking requirements, attribution-format requirements, share-alike contagion.

### 4.6 Web archiving and cached content discovery

Purpose: locate archived snapshots, confirm temporal claims, recover pages that have moved or been deleted (after current-page authorization is established).

Sub-channels to evaluate:
- Internet Archive / Wayback Machine (CDX API, Memento API, savepagenow, mass-download policy)
- Common Crawl (open dataset, open license on the crawl itself; document-level rights remain with publishers)
- archive.today / archive.is (rights of archive copies)
- Google Cache (evaluate current status; service has been intermittently restricted)
- Bing Cache
- Per-site sitemaps (for site: discovery, not caching)

Policy questions: archival-copy copyright (varies by jurisdiction; EU has TDM exception with carve-outs; US has more limited fair-use arguments), attribution, deletion/refresh, mass-mirroring rights, and the specific Wayback Machine ToS that governs *retrieval* versus *rehosting* of captures.

### 4.7 Open access book and longform platforms

Purpose: locate full-text open books on sugar, addiction mechanisms, food systems, and willpower research that may serve as community-facing raw material or corroborating science.

Sub-channels to evaluate:
- Open Library (Internet Archive) — per-book borrow vs read API
- Project Gutenberg (public domain in the US; check for non-US works)
- Standard Ebooks (CC0 reformatting; underlying text status varies)
- Wikisource
- OAPEN / DOAB (academic open-access books)
- JSTOR Open Access community
- HathiTrust full-text access (public-domain, in-copyright, and large-scale computational access tracks)
- Internet Archive Scholar
- PubBook / NCBI Bookshelf
- DOAB and OAPEN discovery APIs
- Knowledge Unlatched (open monographs)
- Open Textbook Library
- OER Commons
- Wikibooks

Policy questions: per-book license, jurisdictional copyright (Project Gutenberg US-centric), TDM-research access, download limits, redistribution.

### 4.8 Discussion platforms, Q&A, and forum families

Purpose: first-person recovery and experience text. This is the family with the highest authorization risk and the largest number of channels that have changed their research access posture in recent years.

Sub-channels to evaluate (each independently; do not assume parent-platform terms cover a sub-product):

**Closed / restricted research programs (verify current status; do not assume any blanket authorization):**
- Reddit (current status of Reddit for Researchers program; current Data API terms; third-party researcher agreements; whether the current research program, if any, permits the access/retention/redistribution contract required by this repository)
- Stack Exchange Data Explorer / Stack Exchange API
- Quora — evaluate any documented research endpoint; flag if none
- X / Twitter (X API paid tiers, current research access program status, retention rights under current ToS)
- Facebook / Meta (CrowdTangle discontinuation, Content Library API, current academic access program)
- Instagram (Meta Content Library)
- TikTok Research API (current availability)
- YouTube (YouTube Research API; standard Data API terms)
- Discord (no first-party research API; community-level authorization is not platform authorization)
- Telegram public channels (TOS, mass-fetch limits)
- WhatsApp (no public API)
- Substack (public RSS; per-publication license)
- Medium (per-post license; evaluate)

**Open / forum-like platforms that warrant evaluation:**
- MetaFilter (community-run, evaluate member/commercial research access)
- Slashdot (open; low volume for this topic)
- Hacker News (open; Y Combinator terms)
- LessWrong / Alignment Forum (open; per-post license)
- Everything2 (CC-BY-NC)
- Boards.ie, Reddit alternatives such as Lemmy instances and Kbin (each instance independent)
- Discourse-based open forums (per-instance policy)
- phpBB and vBulletin forums (per-site, no global policy)
- Sugar/nutrition-specific forums: Whole30 forum (private; per-site), "I Quit Sugar" community (Sarah Wilson; per-site), Diet Doctor forum (per-site), r/quitsugar/r/sugarfree/r/keto Reddit alternatives on other platforms (per-site)
- 12-step and recovery forums (e.g., OA — Overeaters Anonymous; private membership, per-site)

Policy questions specific to this family: per-platform research API, retention rights (most forbid raw redistribution), user-identifier anonymization requirements, deletion/refresh duties, commercial vs non-commercial tier, project-limited terms, and *whether* the project intends to commit raw user text to an open repository at all (this is a yes/no gate at the lead/architect level that the channel policy cannot resolve alone — see §6.6).

### 4.9 Reviews, recipes, and consumer-platform text (low-priority, special handling)

Purpose: Bank 4 "special moments" and Bank 9 "lexicon" — natural-language scenes of sugar use as described by adults in everyday contexts.

Sub-channels to evaluate:
- Allrecipes (per-license; review text)
- Serious Eats (per-license)
- NYT Cooking (paid; limited redistribution)
- Substack food writers (per-post)
- Amazon product reviews (Amazon review policies; per-locale ToS)
- Yelp reviews (Yelp ToS and Content License; specific anti-scraping clauses)
- TripAdvisor (ToS; specific anti-scraping)
- Google Maps reviews (ToS)
- Apple App Store / Google Play reviews (ToS)
- Trustpilot (ToS)
- Goodreads reviews (ToS)
- Letterboxd reviews (ToS)
- IMDb reviews (ToS)
- eBird, iNaturalist (CC on user contributions; per-project)

Policy questions: scraping prohibition clauses, snippet rights, retention and republication, anonymization, deletion/refresh. Most of these channels *forbid* committed retention of raw user text. The next agent should expect a high rejection rate and report it.

### 4.10 Data, statistics, and food composition (Bank 7, 8)

Purpose: epidemiological, intake, and product-composition data.

Sub-channels to evaluate:
- USDA FoodData Central (public domain in the US)
- Open Food Facts (open database license; API)
- CodeX Alimentarius standards
- EFSA Comprehensive European Food Consumption Database
- WHO Global Health Observatory
- OECD Health Statistics
- IHME Global Burden of Disease (GHDx) and IHME data visualization tools
- Our World in Data (CC-BY)
- World Bank Open Data
- UN Data
- FAOSTAT
- USDA Economic Research Service (public domain)
- Nielsen / IRI / Mintel / Statista (paid; *do not* assume they fit the open-repository contract — flag as not eligible)
- Euromonitor (paid)
- Innova Market Insights (paid)
- Numerator (paid)

Policy questions: license per dataset, attribution, share-alike contagion (Our World in Data and Open Food Facts require attribution; share-alike must be checked at the license level), embargo on derivative databases, mass-redistribution clauses.

### 4.11 Patents, trademarks, and regulatory filings (Bank 8)

Purpose: trace product-engineering claims about sugar, hyper-palatability, and the "bliss point."

Sub-channels to evaluate:
- USPTO (open; bulk data)
- Google Patents (per-record; image and text reuse terms)
- WIPO PATENTSCOPE
- EPO Espacenet (Open Patent Services API)
- EUIPO (trademarks)
- UK IPO
- WIPO Global Brand Database
- Trademark Electronic Search System (US TESS)
- FDA Orange Book
- FDA GRAS Notice Inventory
- EPA chemical listings (for context, e.g., HFCS production)
- USDA AMS sugar program reports

Policy questions: API terms, mass-download limits, redistribution of bibliographic data, image rights, derivative-database rights.

### 4.12 FOIA, court, and government records (Bank 8, supporting)

Purpose: recover primary documents supporting the villain dossier.

Sub-channels to evaluate:
- MuckRock (per-request; license per released document)
- GovernmentAttic.org (per-document)
- CourtListener / RECAP (per-document; PACER redistribution rules)
- PACER (US federal courts; access fees; redistribution)
- US state court records (per-jurisdiction; some open, some paywalled)
- US state FOIA reading rooms (per-agency)
- EU documents access (per-institution)
- UK WhatDoTheyKnow
- Canada Open Canada
- Australia Right to Information

Policy questions: per-jurisdiction copyright, exemption categories, fee structure, rehosting rights.

### 4.13 Podcast, video, and transcript services

Purpose: Bank 4 (special moments), Bank 8 (industry voices), Bank 9 (lexicon).

Sub-channels to evaluate:
- YouTube (standard Data API; YouTube Research API if available)
- YouTube-DL and similar — *do not* use; treat any tool that bypasses YouTube ToS as forbidden.
- Podcast Index API (open)
- Listen Notes API
- Spotify (for audio, ToS)
- Apple Podcasts (no public research API; per-show RSS where available)
- Substack podcast feeds (per-publication)
- Internet Archive TV News Archive (research use, license)
- C-SPAN Video Library
- Bloomberg, FT, WSJ audio (paid, restricted)
- BBC Sounds (UK-specific)
- Podchaser
- Common Crawl podcast index
- Whisper / transcription tools (the *transcription* of a publicly posted podcast is a derivative work; the channel policy governs the source, not the transcription tool, but the lead must decide transcription policy before any worker runs Whisper over restricted content)

Policy questions: download rights, transcript-derivative rights, redistribution, attribution.

### 4.14 Encyclopedic and reference text

Purpose: cross-checking definitions, dates, and claim provenance; not for retention as evidence.

Sub-channels to evaluate:
- Wikipedia (CC-BY-SA; per-page attribution; share-alike contagion)
- Wikimedia Commons (per-file license)
- Wikidata (CC0)
- Encyclopædia Britannica (paid; restricted)
- Scholarpedia (CC-BY-NC-SA)
- Stanford Encyclopedia of Philosophy (per-article)

Policy questions: share-alike contagion, attribution formatting, version pinning, snapshot stability.

### 4.15 Research infrastructure and citation chokepoints

Purpose: tool-side; for the next agent's own research operations, not content channels.

Sub-channels to evaluate:
- Zotero (per-library export; per-item license from upstream)
- Internet Archive Scholar
- Connected Papers, Inciteful, Litmaps (paid; not for retention)
- Rayyan (for screening, not retention)
- Covidence (for screening, not retention)
- Various reference manager APIs

Policy questions: API terms, export limits, mass-import.

---

## 5. Cross-cutting policy investigations

The next agent is to treat the following as separate, named investigations, each producing its own packet if material is found:

1. **Reddit research program, current status.** The protocol dated 2026-07-10 names a "Reddit for Researchers" approval regime. The next agent is to confirm whether such a program currently exists, what it requires, what it permits, and whether its output contract matches the repository's open-source commitment. The next agent is to capture the *current* Reddit Terms of Service, the *current* Reddit Data API Terms, the *current* Privacy Policy, the *current* Public Content Policy, and any *current* researcher-program page. If the program exists, the channel stays `CHANNEL — CLARIFICATION NEEDED` for the architecture lead until an executed agreement is produced. If it does not, the channel is `REJECTED` for this run and the next agent is to confirm that no alternate official channel (e.g., a public-data API under permissive terms) is available. The brief's date does not bind the next agent; the next agent is to capture the *date of the policy document retrieved* and to state explicitly whether the document is current.
2. **Stack Exchange research program, current status.** Stack Exchange historically provided Data Dump and Data Explorer access. The next agent is to confirm the current terms, the data-dump status, and the redistribution rights for derived analyses. Note that user content on the network is CC-BY-SA.
3. **Meta/Facebook academic access, current status.** CrowdTangle was discontinued. The Meta Content Library has its own current researcher-access program. The next agent is to confirm the *current* state, eligibility, and redistribution rights.
4. **X / Twitter API, current status.** Current paid tiers, current research tier (if any), retention, and redistribution. Note: standard tier terms typically forbid raw redistribution.
5. **YouTube Research API, current status.** Current availability; quota; redistribution.
6. **Common Crawl license, current status.** The dataset itself has an open license; the documents in it do not. The next agent is to record this distinction precisely so a future worker does not assume the dataset license covers the document text.
7. **Wayback Machine redistribution, current status.** Current Internet Archive terms for researchers; the line between *retrieval* and *rehosting*; and the *notice-and-takedown* posture.
8. **UCSF Industry Documents Library redistribution, current status.** The next agent is to capture the current deposit licenses for the Food Industry Documents subarchive and confirm that internal industry documents are either in the public domain, donated to UCSF with redistribution rights, or otherwise covered.
9. **OpenAlex, Crossref, Unpaywall, CORE — open-science API terms, current.** These are usually permissive but each has a current ToS; capture it.
10. **Public-domain status verification.** For US Federal documents, the next agent is to confirm that the *specific document* was prepared by a US Federal employee in the course of duties or is otherwise in the public domain. For UK Crown copyright works, the next agent is to capture the Open Government Licence version that applies. For EU documents, the next agent is to confirm Decision 2011/833/EU reuse terms or its successor.
11. **Share-alike contagion mapping.** For any CC-BY-SA source, the next agent is to flag whether the share-alike clause is compatible with the repository's open-source license, and to surface this to the lead for an architectural decision.
12. **Per-site terms, generic.** For any forum, blog, or community site discovered that is not in the named list, the next agent is to fetch and capture the site's Terms of Service, Privacy Policy, and any robots.txt, and to mark the channel `CHANNEL — CLARIFICATION NEEDED` rather than proceed.

---

## 6. Open questions for the architecture lead (pre-resolution)

These cannot be answered by a channel-policy worker. The lead is to surface explicit positions before any content fetch is dispatched:

1. **Open-source repository commitment.** Confirm that the project's distribution license is an OSI-approved open-source license, and identify the specific license. Several share-alike and non-commercial sources can only be retained if the repository license is compatible.
2. **Raw user content commitment.** Confirm whether the repository will commit raw user-generated text (full posts, comments, reviews) to a public Git repository, or only derived synthesis. The answer changes which channels can be authorized: most community ToS forbid raw-text commitment regardless of project license.
3. **User-identifier handling.** Confirm the anonymization policy (pseudonymization, hash IDs, no IDs at all) and whether the project will retain a private mapping table. Several platforms require either anonymization or contract-bound non-redistribution.
4. **Refresh and deletion obligations.** Confirm whether the project has committed to deletion on request, scheduled re-fetch, or no refresh. Per-request obligations are common in academic researcher programs.
5. **Commercial vs non-commercial research use.** Confirm the project's status. Several channels (e.g., YouTube Research API, certain Meta tiers, certain RSS aggregators) gate on this.
6. **Per-channel approval ledger.** Confirm that any channel requiring a signed, project-specific agreement (Reddit for Researchers, Meta Content Library, YouTube Research API) will be tracked with a separate approval record in `research/channels/approvals/` and that the *agreement PDF* will be retained as a packet — separate from the platform's public ToS — before any content fetch.
7. **Mirror-and-purge policy.** If a channel's only feasible access is a mirror (e.g., Wayback), confirm whether the project will mirror-and-purge (capture to working store, summarize, do not commit raw) or mirror-and-commit.
8. **Adversarial sources.** Confirm that the project intends to retrieve industry, regulatory, and FOIA materials that the disclosing party may prefer not to redistribute. Some of these documents are posted on platforms with the disclosing party's copyright, and the project must decide between (a) summary-only with citation, (b) committed short-quote with citation, (c) committed long-quote under a fair-use/fair-dealing rationale. The answer depends on the publishing jurisdiction.
9. **Transcription policy.** Confirm whether transcription of restricted audio/video is treated as a derivative work governed by the source channel's terms. Most platforms say yes.

---

## 7. Decision rules the next agent must follow

1. **No content fetch without a current, captured policy.** The next agent may not run a topical, community, or scientific search against a channel whose current policy has not been captured and recorded in a packet.
2. **Version freshness gate.** If a policy document has no version date or effective date, the next agent is to mark the channel `CHANNEL — CLARIFICATION NEEDED` and report the gap.
3. **No assumption from a parent platform's general terms.** Each sub-product or sub-channel is its own evaluation.
4. **No use of any unofficial scraper, mirror, or transport that bypasses the channel's access controls.** Wayback Machine snapshots are permissible *only* if the source channel is itself authorized, and *only* for archival confirmation, never as a substitute for the source.
5. **No use of fingerprint spoofing, identity rotation, or stealth transport.** Any tool that requires this is a veto, not a workaround.
6. **Log every policy fetch, every search, every call, every URL revisit, every acceptance and rejection.** Log events go in the research log; accepted policy URLs become packets; rejected URLs are logged with reason.
7. **Refuse to make a final authorization decision.** The next agent returns policy evidence; the architecture lead makes the authorization decision in context of the project's distribution commitments. Disposition values are `ACCEPTED` (for the policy document itself as a packet) and `CHANNEL — CLARIFICATION NEEDED` or `REJECTED` (for the channel as a source of research evidence). These two dispositions are independent: a policy document can be ACCEPTED as a packet while the channel it describes remains `CHANNEL — CLARIFICATION NEEDED` for content.
8. **Commission more agents freely.** If a channel family is large, the next agent is to split it into multiple sub-agents rather than produce a thin policy capture.
9. **Do not invent policy positions.** If a policy is silent on a question, the next agent is to record "not addressed" verbatim, not infer a permissive or restrictive answer.
10. **Treat the protocol's 2026-07-10 date as a starting reference, not a current fact.** Recheck live.

---

## 8. Reporting template the next agent is to return

The next agent's return to the lead is to be a structured Markdown block with these sections:

- **Run metadata:** assignment ID, worker ID, runtime model ID, reasoning config, max output allowance, start/end UTC, total policy URLs fetched, total packets produced.
- **Per-channel disposition table:** one row per channel evaluated, with policy URL, version date, current status, and the lead's open question that remains.
- **Captured policy packets:** the standard schema from §3, one per channel.
- **Log events:** chronological, including all rejections.
- **Gaps and follow-up suggestions:** channels that should be re-evaluated, channels that should be added, channels that should be permanently rejected.
- **Open questions for the lead:** re-stating §6 where new ones emerged.

---

## 9. Quality bar (re-stated for the next agent)

The protocol's quality bar is the only optimizer. Cost, tokens, latency, time, and per-agent output are descriptive. The next agent is to spend what is required to:

- capture the *current* policy text for every channel in §4 that is plausibly useful, not just the first one in each family;
- record the *current* version/effective date for every policy;
- separately evaluate each named sub-product of Reddit, Stack Exchange, Meta, X, and YouTube;
- capture the *current* state of the Reddit research program, including whether it exists in any form the repository's contract can use;
- flag share-alike and non-commercial contagion risks to the lead before the architect's licensing decision is made.

If a channel cannot be validated under this bar, it stays unvalidated and the lead is informed. The next agent is not to optimize for closure.

---

*End of commission. No fetches performed. No channel declared authorized.*
