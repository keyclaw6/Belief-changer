# REV-AUTH-SE-FITNESS — Final Disposition

**Status: REJECTED**

**Collection hold:** Do not retrieve Fitness questions, answers, comments, profiles, search results, API content, data-dump content, or derivatives. Do not create a source packet, count evidence, or mark any Fitness row `READY`. The prior `CANDIDATE — VALIDATION REQUIRED` status is superseded.

## Basis

| Gate | Finding |
|---|---|
| Automated-research authorization | **Failed.** `FU-01` states that automated systems may not access or collect Network content for developing, testing, benchmarking, or improving generative-AI/LLM systems, with an exception only for “express prior written consent.” The first-party search found no exception for model calibration, AI-assisted research, or non-training book research. No project-specific consent exists. Permission cannot be inferred. |
| Access route | **Failed.** `POL-05` returned `418` with `Disallow: /`, `search=no`, and `ai-train=no`. `FU-02` found no first-party provision making the API override those restrictions or the AUP’s purpose limitation. API quota, attribution, and backoff rules describe operation, not authorization. |
| Copyright and quotation rights | **Insufficient.** `POL-01`/`FU-03` identify CC BY-SA licensing by contribution date, and `license.xml` declares CC BY-SA 4.0 for the root content. Those copyright terms do not authorize automated collection, override the AUP or access signals, or resolve historical revisions and deleted material. |
| Durable retention and deletion | **Failed.** `FU-04` says posts may disappear, may later be undeleted, and accounts may be deleted or anonymized. No operational deletion/refresh feed or rule authorizes retaining stale raw captures or profile-linked data in this repository. The packet contract therefore cannot be certified. |
| Written authorization | **Failed.** `FU-05` confirms that no project-specific authorization was requested or obtained. |

The license and public-redistribution statements address potential copyright permissions only. They do not establish a permitted access method, permission for this research purpose, or a durable retention and deletion basis. Even setting the precise AUP classification of this project aside, the access and retention gates independently fail.

## Replacement commission

**Assignment ID:** `REPL-SUGAR-FIRSTPERSON-AUTH-01`  
**Worker ID:** `REPL-DISCOVERY-01`  
**Purpose:** Discover authorization-compatible replacement source families for first-person sugar/junk-carb recovery and experience material formerly sought from Fitness Stack Exchange, preserving full coverage for Banks **1–6, 9, and 10** and all materially distinct personas selected by the architecture.

**Discovery method and restrictions:**

1. Begin with policy-first discovery: official terms, licensing, robots/access controls, API rules, automation provisions, retention, deletion, and redistribution terms.
2. Do not retrieve candidate user content until the source passes authorization and retention review.
3. Accept only sources with an explicitly verified permitted access route and a basis for durable raw-capture and excerpt redistribution in this repository. Project-limited, revocable, deletion-dependent, or unclear permissions fail unless an already approved compliant storage design exists.
4. Exclude Stack Exchange and Reddit absent the required platform-level authorization. Do not use search snippets, mirrors, stealth methods, alternate transports, or unofficial scrapers as evidence.
5. Identify at least three independent candidate source families, and retain enough validated families to meet or exceed the original per-persona numeric floors and qualitative tests. Each validated community receives separate focused matrix rows; no bundled or fallback scope.
6. After validation, collection workers must preserve exact excerpts, source packets, deletion obligations, rejected items, and all search events under the normal research-log contract.

**Required return:** candidate URL and canonical identity, topical fit, policy/version URLs, access and automation basis, license/quotation basis, retention and deletion terms, user-data handling, rejection reasons, and a recommendation of which candidates can become `READY`.

**Dispatch gate:** The caller must preflight an approved research arm at its highest reasoning configuration and record the exact runtime model ID, reasoning setting, and endpoint-maximum output allowance before dispatch. No worker should be dispatched with missing or substituted metadata.
