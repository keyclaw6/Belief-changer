# REV-AUTH-SE-FITNESS — Authorization and Retention Decision

**Status: CANDIDATE — VALIDATION REQUIRED**

**Collection hold:** Do not retrieve Fitness questions, answers, comments, profiles, search results, or other user content. Do not create a source packet, count evidence, or mark any matrix row `READY`.

The visible artifact establishes potentially relevant licensing information, but it does not establish permission for this research method, durable raw-capture retention, deletion handling, or open-repository redistribution.

## Evidence-grounded assessment

| Requirement | Evidence | Finding |
|---|---|---|
| Canonical source identity | The Fitness licensing URL resolved, and the exact Fitness `robots.txt` URL was retrieved. | The site exists as a source candidate. Topical content fit was not assessed, consistent with the instruction not to retrieve user content. |
| Direct page access | `POL-05` returned `418 I'm a teapot`; its complete body contains `User-agent: *`, `Content-signal: search=no, ai-train=no`, and `Disallow: /`. | The direct automated page-retrieval route is **not authorized on the current evidence**. No retry, alternate transport, stealth method, or bypass is permitted. |
| Automated research use | `POL-03` says the bot/content-scraping section restricts automated access or collection for listed purposes, including “testing, indexing, benchmarking, or improving any generative AI, chatbot, large language, or machine learning tool.” | It is unresolved whether this factory-calibration research falls within a prohibited purpose. Permission cannot be inferred. |
| API route | `POL-04` documents programmatic API use, attribution, quotas, backoff, and termination for breach, but says API use incorporates the Network Terms. | API availability and throttles do **not** establish that this purpose is permitted, that the API overrides the robots/content signals, or that durable repository capture is allowed. |
| Quotation and excerpt rights | `POL-01` reports that publicly accessible user contributions are licensed under CC BY-SA, with the applicable version depending on the contribution/revision date. `POL-02` states: “all Public Content you contribute is available for public copy and redistribution.” | There is a plausible copyright/licensing basis, but the artifact does not establish the exact license notice and conditions for any eventual contribution, nor whether those rights authorize this automated collection and retention contract. |
| Raw retention | `POL-06` says public content may be available through the API and data dump, but questions, answers, and comments may later be deleted. | No basis establishes that raw captures may be retained indefinitely in Git. The required “no deletion obligations” condition is not verified. |
| Deletion and refresh | `POL-06` states: “such content, once public, cannot often be removed from public view,” while also noting that content may later be deleted. | The artifact does not resolve whether deleted material must be removed from repository packets, whether refreshes are required, or whether an exception applies to durable redistribution. |
| Open-repository redistribution | `POL-02` supports public copy and redistribution; `POL-01` identifies CC BY-SA. | Potentially supportable, but not certified. Attribution, share-alike, deletion, user-data, and AUP requirements remain unresolved. |
| User-data status | `POL-06` says public questions, answers, profiles, and reputation content may contain public usernames/profile information. | Future captures may contain user identifiers. No content was fetched, but a compliant minimization, retention, deletion, and redistribution basis is not established. |
| Authorization basis | The artifact expressly says the caller makes no authorization decision and identifies unresolved questions. | **No verified project-specific authorization or written agreement is present.** |

## Why this is not `READY`

The CC BY-SA and public-redistribution statements address potential content rights; they do not by themselves authorize:

1. automated collection for this particular research purpose;
2. use of the API despite the current `robots.txt` response and content signals;
3. durable retention of raw captures and derivative excerpts in an open repository;
4. retention after deletion or policy changes; or
5. redistribution of public usernames or other user-linked material.

The current evidence therefore fails the source-authorization and retention gate. The direct crawler/page route is rejected for this run. The overall source remains a candidate only because the artifact does not conclusively resolve whether an expressly permitted API or written-authorized route exists.

## Required first-party validation commissions

No user content should be fetched during these commissions.

### `AUTH-SE-FITNESS-FU-01` — AUP purpose and automation scope

Retrieve the complete current content-scraping/bot provisions from:

- `https://stackoverflow.com/legal/acceptable-use-policy`

Also retrieve any current first-party legal/help clarification that explicitly addresses automated research, AI-assisted research, model evaluation/calibration, or non-training book research.

Required findings:

- whether this project’s purpose is covered by the listed generative-AI restriction;
- whether any research, quotation, or public-interest exception exists;
- whether an API request is treated differently from page scraping;
- the current effective date and any applicable exceptions.

If no first-party clarification answers the project-specific purpose question, record it as unresolved rather than interpreting the clause.

### `AUTH-SE-FITNESS-FU-02` — API permission and robots relationship

Retrieve the current relevant provisions from:

- `https://stackoverflow.com/legal/api-terms-of-use`
- `https://api.stackexchange.com/docs/throttle`
- other official Stack Exchange API documentation only

Determine whether:

- the API is an authorized route when the site’s `robots.txt` says `Disallow: /`;
- `search=no` and `ai-train=no` apply to API collection;
- automated research collection is permitted for this purpose;
- storage, excerpting, deletion, and redistribution are governed by additional API rules.

Quota, attribution, and backoff documentation alone must not be treated as permission.

### `AUTH-SE-FITNESS-FU-03` — License and redistribution conditions

Retrieve current first-party policy materials from:

- `https://fitness.stackexchange.com/help/licensing`
- `https://stackoverflow.com/help/licensing`
- `https://stackoverflow.com/license.xml`
- `https://stackoverflow.com/legal/terms-of-service/public`

Determine:

- the operative license statement for public user contributions;
- attribution and share-alike requirements;
- whether raw captures and derivative excerpt packets may be committed to and redistributed from an open repository;
- treatment of revisions and deleted contributions;
- whether any subscriber-content distinction affects Fitness public content.

No individual posts or post timelines should be opened.

### `AUTH-SE-FITNESS-FU-04` — Privacy, deletion, and user-data obligations

Retrieve current first-party policy and official data/API documentation concerning:

- deletion of questions, answers, comments, profiles, and usernames;
- API or data-dump treatment of deleted material;
- retention and refresh obligations;
- redistribution of public usernames or profile-linked information;
- any required redaction or data-minimization measures.

Use:

- `https://stackoverflow.com/legal/privacy-policy`
- official Stack Exchange API/data-dump documentation only.

### `AUTH-SE-FITNESS-FU-05` — Written project-specific authorization

Request written authorization through an official Stack Overflow/Stack Exchange legal or research channel covering the exact:

- research purpose;
- permitted access method;
- automation and rate limits;
- raw-text capture and retention;
- quotation and derivative packet creation;
- open-repository redistribution;
- attribution/share-alike treatment;
- deletion and refresh handling;
- user-identifier handling;
- duration and revocation terms.

A moderator, community, or individual-author permission would not resolve this platform-level authorization question.

## Final disposition rule

Change this source to `READY` only if first-party policy or written authorization confirms all of the following:

- a permitted access route exists without bypassing `robots.txt`, content signals, or access controls;
- the research purpose is allowed;
- raw captures and derivative excerpts may be durably retained and redistributed in this repository;
- deletion/refresh duties are either explicitly absent or covered by an approved compliant design; and
- user-data handling is authorized and operationally defined.

If any of those conditions is denied, or if no adequate authorization is obtained, mark `fitness.stackexchange.com` **REJECTED** and replace it with an authorization-compatible source.
