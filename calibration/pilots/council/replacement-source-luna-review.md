# Decisive verdict

**Reject both commissions as non-dispatchable. No candidate source is `READY`, no user-content collection may begin, and no matrix cell may be counted.**

Neither commission satisfies the required policy-first gate, and both contain unsupported assumptions that the reviewer cannot accept without visible retrieval artifacts.

## Material failures

| Requirement | DeepSeek commission | MiniMax revision |
|---|---|---|
| Authorization before discovery | Searches result pages containing user-content snippets before authorization. “Do not click” is not enough. | Same failure. It searches and stores snippets before authorization. |
| Search-engine access | Assumes Google/Bing/DuckDuckGo automation, retention, and redistribution are permitted. | Same failure; “real-user User-Agent” may be fingerprint spoofing and is not permission. |
| Search-result retention | Requires saving the first 30 result pages per query without verifying the search engine’s terms. | Same failure. Search snippets are not evidence or a substitute for packet rights. |
| Uncapped quality | Imposes fixed query lists, a 30-result limit, and a three-family objective. | Adds an arbitrary 24-month activity threshold and still treats three families as a discovery target. |
| Source authorization | Allows policy retrieval before the transport and policy-page retention basis is established. | Same failure, including direct requests to guessed policy paths. |
| Policy-page retention | Requires entire raw policy pages before verifying that those pages may be committed and redistributed. | Same failure. |
| Rights to user material | Treats fair use/fair dealing, public visibility, anonymization, or platform terms as possible readiness bases. Those do not satisfy the packet contract. | Same failure. The evaluation explicitly permits reliance on fair use as the strongest basis. |
| Project-limited/revocable access | The first commission does not enforce the project-limited/revocable-access hard line. | Adds the hard line, but still permits premature discovery and does not require item-level rights. |
| Activity verification | No valid activity gate. | Attempts to inspect front pages and recent posts before `READY`; that is prohibited. `Last-Modified` is not proof of community activity. |
| Scope | Sugar-only; omits junk/refined carbs. | Improves this, but permits extracting an “in-scope portion” from communities whose defining condition is an excluded population. |
| Personas | Does not identify all materially distinct provisional personas. | Infers life situations from snippets and policy indicators rather than visible first-person evidence. |
| Source scope | Uses domains and “families” rather than one fixed, reconstructable community/source scope per assignment. | Same problem; a domain-level policy does not authorize every instance, page, author, or item. |
| Scout/synthesis separation | The retrieval evaluator is asked to make the authorization synthesis and readiness decision. | Same failure. A retrieval worker should return evidence; the architecture specialist/lead evaluates it. |
| Independent review | No complete adversarial specialist/reviewer handoff is built into the commission. | Same failure. |
| Event logging | Does not require a chronological event for every search, fetch, revisit, model call, rejection, and disposition. | Same failure. |
| Matrix reconstructability | Does not create the required community × persona × single-bank rows with repeated authorization, target, query, model, and output fields. | Same failure. |
| Current-policy evidence | Relies on claimed dates and policy status without caller-verified runtime evidence. | Same failure. |
| Reddit and other restricted sources | The exclusion is directionally correct, but search-result discovery can still expose and retain derived material. | Same failure unless the source is not queried, fetched, or counted at all. |

The revised commission is therefore not a safe replacement. The complete replacement below is limited to **policy and authorized metadata discovery**. It does not retrieve, inspect, or count user content.

---

# Replacement Retrieval Commission — `REPL-SUGAR-POLICY-FIRST-02`

**Status:** Dispatchable preliminary authorization commission only  
**Worker scope:** Potential first-person sources for Banks 1–6, 9, and 10  
**Content status:** No user content may be searched, fetched, inspected, quoted, or counted  
**Inputs:** This protocol and the blind book brief only  
**Prior candidates:** None are trusted or prevalidated  
**Banks 7–8:** Out of scope for this commission; first-person material must not be used as scientific or investigative evidence  
**Matrix status:** This is not a research-log matrix assignment. `Persona` and `Bank` are `N/A — authorization-only; no cell may be filled.`

## Mission

Discover potential source scopes through **authorized policy, rights, license, and metadata channels**, then obtain visible evidence sufficient for the architecture lead to decide whether a source can legally and durably support later content collection.

The commission must:

1. verify the access and retention basis of every discovery channel;
2. discover potential source scopes only from authorized metadata or rights registries;
3. retrieve only official policy, license, rights, API, robots, privacy, deletion, and source-description material;
4. obtain explicit evidence covering automation, exact content rights, permanent Git retention, raw-capture redistribution, excerpt redistribution, privacy obligations, and deletion duties;
5. keep every candidate at `CANDIDATE — VALIDATION REQUIRED` or `CANDIDATE — CLARIFICATION NEEDED` until visible evidence supports `READY`;
6. continue without a fixed number of candidates, searches, agents, queries, or results;
7. return every gap as a complete follow-up assignment rather than asking an operator to edit rows.

This commission must not claim that any source is suitable merely because it is public, discoverable, active, indexed, anonymized, covered by permissive `robots.txt`, or available through an API.

---

## Non-negotiable pre-content rules

### 1. Caller preflight

Before dispatching each subassignment, the caller must record:

- exact runtime request model ID;
- exact top reasoning configuration;
- endpoint maximum output allowance after input context;
- worker ID;
- assignment ID;
- permitted retrieval tool or API;
- tool/API terms covering automation;
- retention and redistribution basis for returned metadata and captures.

Only these arms are permitted:

- `deepseek/deepseek-v4-pro` at `xhigh`;
- `minimax/minimax-m3` with reasoning enabled;
- `openai/gpt-5.6-luna` at `max`.

The caller must not dispatch with a placeholder, lower setting, reduced output allowance, or unapproved model. A role does not need to inspect invisible endpoint metadata.

### 2. Search-channel authorization

No search engine, browser automation layer, API, registry, crawler, or HTTP transport is assumed to be authorized.

Before using a discovery channel, a retrieval worker must obtain visible evidence of:

- permitted automation or API use;
- applicable robots and access controls;
- rate limits;
- use and retention rights for returned URLs and metadata;
- redistribution rights for any retained response;
- deletion or refresh duties;
- the official policy URL and its current version or effective date.

A permissive robots file is not a copyright license or an automation grant. A public search result is not permission to retain its snippet.

If a search provider does not permit the required automated access and durable retention, do not use it. Do not substitute a browser, mirror, unofficial endpoint, rotating identity, spoofed User-Agent, or another transport.

Use an honest automation-identifying User-Agent where the authorized tool requires one. Do not present automation as ordinary human browsing.

### 3. Permitted preliminary material

Before a source is cleared, workers may retrieve only:

- official terms, legal, privacy, API, developer, license, rights, copyright, deletion, or research-access pages;
- official robots or access-control documents;
- official source catalogs or collection metadata;
- official source-owner About or collection-description pages that contain no user posts, comments, profiles, or embedded user content;
- metadata responses from a registry or API whose own retention rights have passed the channel gate.

Workers must not retrieve:

- posts, comments, threads, replies, user profiles, author pages containing posts, transcripts, video or audio content, RSS item bodies, search snippets, or archived copies of content;
- public content from a platform merely because it is visible without login;
- any Reddit material without a current written Reddit agreement or documented Reddit for Researchers approval covering the exact access, retention, deletion, and output contract;
- any Stack Exchange material, or any other excluded platform, unless a later approved assignment establishes the required authorization.

If a policy or About page contains embedded user-generated material, stop, record the block, and do not retain that material.

### 4. No fixed quota or closure threshold

There is no fixed number of:

- queries;
- search engines;
- candidates;
- source families;
- independent workers;
- policy pages;
- retrieval agents;
- results per query;
- life situations;
- `READY` families.

The workers and architecture specialist choose their own search strategy, exploration order, query expansion, and additional agent decomposition. Seed concepts from the brief may guide discovery, but no prescribed query list or “first 30 results” rule applies.

Research may not stop because of cost, tokens, latency, time, or a three-family threshold. This preliminary commission may close only when the architecture specialist and adversarial reviewer find that authorized discovery channels have been explored sufficiently for the question, or when every remaining path is blocked or unauthorized. Any remaining coverage problem must remain visible.

---

# Dispatch plan

Each row below is a separate focused assignment. The caller must create a fully populated runtime dispatch record for it. A later candidate-specific assignment is a new assignment; it must not be hidden inside an “all domains,” “fallback,” or “if thin” instruction.

| Assignment ID | Worker ID | Focused responsibility | Permitted scope | Output |
|---|---|---|---|---|
| `REPL-AUTH-CHANNEL-01` | `REPL-AUTH-CHANNEL-W01` | Verify discovery-channel authorization | Search/API/registry policy only; no candidate content | Channel authorization ledger and policy captures |
| `REPL-AUTH-METADATA-01` | `REPL-AUTH-METADATA-W01` | Discover potential source scopes | Only channels that passed `REPL-AUTH-CHANNEL-01`; licensed metadata only | Candidate metadata registry |
| `REPL-AUTH-POLICY-<unique>` | `REPL-AUTH-POLICY-W<unique>` | Verify one candidate source scope | One fixed canonical source scope; official policy/rights metadata only | Candidate policy evidence packet and gaps |
| `REPL-AUTH-SPECIALIST-01` | `REPL-AUTH-SPECIALIST-W01` | Synthesize visible authorization evidence | All returned channel, metadata, and policy artifacts; no user content | Complete authorization ledger and follow-ups |
| `REPL-AUTH-REVIEW-01` | `REPL-AUTH-REVIEW-W01` | Adversarial audit | Complete candidate ledger plus every visible artifact | Complete corrected ledger or additional assignments |

For every row, the runtime record must repeat:

- the complete fixed scope;
- access and retention basis;
- `Persona: N/A — policy-only authorization work, not a matrix row`;
- `Bank: N/A — no source evidence and no cell filling`;
- the worker’s chosen query/search strategy;
- exact model ID;
- exact reasoning configuration;
- endpoint maximum output allowance.

---

## Assignment 1 — Authorized discovery-channel audit

**Assignment ID:** `REPL-AUTH-CHANNEL-01`  
**Focused question:** Which search, API, catalog, or open-license registry channels may be used for policy-only or metadata-only discovery with durable retention in this repository?

The worker may search for and retrieve official channel documentation, but must not search for or retrieve topical user content.

For every proposed channel, capture:

- canonical policy URL;
- policy version, effective date, or page update date;
- retrieval timestamp;
- automation permission;
- API terms and rate limits;
- robots/access requirements;
- permitted fields and endpoints;
- retention and deletion obligations;
- rights to retain and redistribute returned URLs and metadata;
- whether raw response capture may be committed;
- any project-limited, revocable, or refresh-required terms;
- exact relevant excerpts with character-accurate locators.

If a channel’s terms are ambiguous, it is not approved. Mark it `CHANNEL — CLARIFICATION NEEDED` and do not use it for candidate discovery.

### Output

`research/preliminary/channel-authorization.md`

No channel may be called approved solely because it is publicly reachable or because its robots file does not prohibit crawling.

---

## Assignment 2 — Authorized metadata-only candidate discovery

**Assignment ID:** `REPL-AUTH-METADATA-01`  
**Focused question:** Which potential source scopes appear, from authorized metadata alone, to concern first-person adult experience of refined sugar, junk carbs, craving, snacking, quitting, or recovery?

Use only channels approved in Assignment 1.

The worker may inspect:

- catalog records;
- license fields;
- official collection descriptions;
- canonical URLs;
- source-type metadata;
- permitted audience or subject metadata;
- permitted update or availability metadata.

The worker must not inspect the content behind a candidate URL.

Each candidate must be recorded as one fixed source scope, not merely a base domain. Record the exact:

- candidate ID;
- canonical URL and redirect chain;
- instance, collection, author, feed, or path where relevant;
- source owner or publisher;
- source type;
- official metadata URL;
- official description establishing provisional topical fit;
- whether the source is user-generated, creator-authored, archival, academic, or another type;
- license field and its scope;
- metadata capture ID;
- underlying-material identity and possible syndication duplicates;
- current status;
- unresolved authorization and scope gaps.

A candidate whose defining subject is diabetes management, medical nutrition therapy, eating-disorder treatment, or weight-loss-program mechanics must not be mined merely because it contains overlapping sugar language. A separately defined, independently authorized in-scope collection may be evaluated only as a new source scope with its own evidence and assignment.

Do not infer personas from titles, snippets, demographics, or policy pages. Any audience signal is a provisional hypothesis, not persona evidence.

### Output

`research/preliminary/candidate-metadata.md`

No candidate discovered here is a counted source, accepted URL, quote, or bank item.

---

## Assignment 3 — Candidate-specific policy and rights verification

Create one new assignment for each candidate source scope. Do not bundle multiple communities, instances, authors, or collections under one domain-level assignment.

**Focused question:** Does this exact source scope have a documented basis for the required access, raw capture, excerpt packet, permanent Git retention, and public redistribution?

The worker may retrieve only official policy and metadata pages whose access and retention basis has been established. It must not retrieve user content.

For each candidate, verify separately:

1. canonical existence and source ownership;
2. permitted automated method;
3. robots and access controls;
4. API or developer terms;
5. item-level or author-level content license;
6. whether the license covers exact raw captures and excerpt packets;
7. whether it permits permanent public Git retention;
8. whether it permits redistribution in this open repository;
9. attribution, share-alike, notice, or excerpt limits;
10. deletion, refresh, withdrawal, privacy, and erasure duties;
11. whether access is project-limited or revocable;
12. whether a platform license is only a license to the platform rather than to third parties;
13. whether usernames, profile links, avatars, or other personal data may be retained;
14. whether any research approval or written agreement covers the exact output contract;
15. whether the source’s official description is in scope for the brief;
16. whether an authorized activity or availability signal exists, if the source is being proposed as an active community.

A public page, permissive robots file, API response, platform terms of service, anonymization plan, fair-use theory, or search snippet is insufficient by itself.

### Required disposition

- `READY` only if every required condition is supported by visible, current evidence.
- `CANDIDATE — VALIDATION REQUIRED` when canonical scope, topical fit, or policy evidence is incomplete.
- `CANDIDATE — CLARIFICATION NEEDED` when explicit permission, license scope, or retention terms require direct confirmation.
- `REJECTED — UNAUTHORIZED` when automation, access, or content rights are absent or prohibited.
- `REJECTED — PACKET CONTRACT FAIL` when deletion refreshes, revocable/project-limited access, or redistribution restrictions conflict with permanent repository packets.
- `REJECTED — OUT-OF-SCOPE` when the source scope is defined by an excluded population or method.

Do not use a universal 24-month activity rule. A static, licensed source may remain useful if its source type is a blog, archive, book, or other durable collection. Conversely, a source may not be called an active community unless an authorized, current activity signal supports that description. `Last-Modified` alone is not proof of user activity.

### Policy capture rule

A policy page may be retained as a raw artifact only when the policy-page access and redistribution basis itself permits that retention. Otherwise:

- do not commit its raw text;
- record the URL, status, retrieval metadata, and the reason raw retention was not permitted;
- do not mark the candidate `READY`.

Do not use fair use, fair dealing, citation, or anonymization as a substitute for the policy-artifact retention requirement.

### Output

Create one policy-evidence file per distinct accepted policy URL:

`research/preliminary/policy-evidence/<Policy Capture ID>.md`

Each file must contain:

```markdown
# <Policy Capture ID> — <Title>

- **Policy Capture ID:** <ID>
- **URL:** <canonical URL>
- **Title:** <title>
- **Source scope:** <one fixed candidate scope>
- **Retrieved (UTC):** <caller-verified timestamp>
- **Policy version / effective date:** <value or not stated>
- **HTTP status:** <status>
- **Access / retention basis:** <exact documented basis>
- **Deletion / refresh obligations:** <none, or exact obligation>
- **Retrieval method:** <authorized method>
- **Runtime model ID:** <exact ID>
- **Reasoning config:** <exact setting>
- **Maximum output allowance:** <endpoint maximum>
- **Search / fetch settings:** <exact settings>
- **Capture hash:** <hash where available>
- **Disposition:** ACCEPTED | BLOCKED | REJECTED

## Captured policy text

### <Capture ID>
- **Locator:** <section or paragraph>
- **Capture method:** <authorized page or policy capture>
- **Exact excerpt:** <character-accurate excerpt, only where retention is authorized>

## Gaps

- <unresolved issue and why it prevents READY>
```

A policy fact without a visible capture or official artifact is not accepted.

---

# Architecture specialist and adversarial review

## Specialist — `REPL-AUTH-SPECIALIST-01`

The specialist receives only:

- this protocol;
- the blind brief;
- the visible channel artifacts;
- the visible candidate metadata;
- the visible policy captures;
- the chronological retrieval log.

It must not fill bank cells or use unsupported summaries. It returns:

`research/preliminary/authorization-ledger.md`

The ledger must list every candidate and repeat:

- exact fixed source scope;
- canonical URL;
- source type;
- scope-fit basis;
- current policy URLs and versions;
- automation basis;
- license or written-permission basis;
- raw-capture permission;
- packet-redistribution permission;
- retention/deletion obligations;
- personal-data restrictions;
- activity or availability evidence, if applicable;
- duplicate/syndication relationships;
- status;
- evidence IDs;
- gaps;
- complete follow-up assignments.

The specialist may commission additional retrieval workers. Every such assignment must have its own ID, worker, fixed scope, authorization basis, strategy, runtime model, reasoning configuration, and maximum output allowance.

## Reviewer — `REPL-AUTH-REVIEW-01`

The reviewer receives the complete ledger and every visible artifact. It must independently audit:

- whether any candidate was searched or fetched before its channel gate;
- search-engine/API authorization;
- robots and access-control compliance;
- policy-page retention;
- exact rights to user material;
- permanent Git retention;
- deletion and refresh obligations;
- project-limited or revocable access;
- item-level license scope;
- personal-data handling;
- canonical URL and source-scope precision;
- non-goal exclusions;
- duplicate-source handling;
- unsupported activity or persona claims;
- model IDs, reasoning settings, and maximum output allowances;
- chronological event completeness;
- whether any candidate was marked `READY` without visible evidence.

The reviewer returns a complete corrected ledger, not patch instructions. If evidence is weak, it commissions more retrieval through the caller or leaves the candidate unresolved. It must not ask the operator to edit rows manually.

---

# Required chronological research log

`research/preliminary/authorization-research-log.md`

Every search, model call, policy fetch, URL revisit, accepted or rejected capture, block, and follow-up must be logged in chronological order:

| Event ID | UTC | Assignment ID | Worker ID | Action | Query / URL | Tool and search settings | Runtime model ID | Reasoning config | Max output | Disposition and reason | Capture/output IDs | Cells filled |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|

For this commission, `Cells filled` must be `0` for every event.

The worker must return:

- accepted policy-capture count;
- rejected or blocked capture count;
- verified policy-excerpt count;
- accepted content-source count: `0`;
- verified content-quote count: `0`;
- filled bank cells: `0`;
- usage and cost when available;
- remaining authorization gaps.

Usage, cost, tokens, and latency are descriptive only and must not determine continuation or ranking.

---

# Readiness gate

A candidate may be marked `READY` only when the visible artifacts establish all of the following:

- the exact canonical source scope exists;
- the scope is in the brief;
- the access method is authorized;
- robots and technical controls permit that method;
- the exact material has an item-level, author-level, public-domain, or written-permission basis;
- the basis permits raw capture;
- the basis permits excerpt-packet creation;
- the basis permits permanent Git retention;
- the basis permits redistribution in this open repository;
- no deletion refresh or cache-scrubbing obligation conflicts with permanent retention;
- access is not project-limited or revocable in a way that conflicts with the packet contract;
- privacy and personal-data duties are satisfied;
- current policy versions and retrieval timestamps are recorded;
- the source is not an excluded population or method;
- duplicates and syndicated copies are identified;
- any required activity signal was obtained through an authorized channel.

The following never establishes `READY` on its own:

- public visibility;
- an accessible URL;
- permissive robots;
- a platform’s license to operate or display user content;
- an API that returns text;
- fair use or fair dealing;
- anonymization or pseudonymization;
- removal of usernames;
- a search-engine snippet;
- an academic or research label;
- a claimed moderator or individual-author permission that does not cover the platform’s access, retention, deletion, and redistribution contract.

Reddit remains unavailable unless the required written Reddit authorization is visible and current. No Reddit search, fetch, snippet, feed, mirror, or derived material may be used while that evidence is absent.

---

# Handoff after this commission

This commission does not identify final personas and does not establish Stage A coverage. The architecture lead must separately run the required persona, community, scientific, and investigative tracks. It must identify all materially distinct provisional personas before broad collection and must not infer them from policy metadata.

Only after the authorization reviewer approves a source may the lead:

1. validate the exact canonical source scope and topical fit;
2. create the required matrix rows;
3. create one row per fixed community/source scope × persona × single bank;
4. repeat the full authorization basis, target, query strategy, runtime model, reasoning configuration, and maximum output allowance in every row;
5. dispatch a collection worker with the exact packet schema;
6. count only accepted URLs and character-verified excerpts.

No “source family” row may bundle multiple communities, domains, authors, instances, or banks. If authorization remains unavailable, the relevant cells stay blocked and the unresolved gap is reported rather than filled by invention.
