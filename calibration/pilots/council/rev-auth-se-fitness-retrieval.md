# REV-AUTH-SE-FITNESS — caller retrieval artifact

**Assignment:** Current terms, content license, robots/access controls,
API/automation rules, retention, deletion, redistribution, and user-data basis
for `fitness.stackexchange.com`.

**Retrieved (UTC):** 2026-07-10T20:52:23Z–2026-07-10T20:55:00Z
**Methods:** caller web search/open over first-party Stack Overflow / Stack
Exchange pages; direct unauthenticated GET of the exact Fitness `robots.txt`.
No question, answer, comment, profile, search-result content, or other user data
was fetched.

This is visible policy input for an allowed research model. The caller makes no
`READY`/`REJECTED` decision and does not treat a license as access permission.

## POL-01 — site-specific content-license help

- **URL:** https://fitness.stackexchange.com/help/licensing
- **Network equivalent opened:** https://stackoverflow.com/help/licensing
- **Observed:** the Fitness help URL resolved; the network help text says,
  “all publicly accessible user contributions are licensed under Creative
  Commons Attribution-ShareAlike”.
- **Version facts:** it assigns CC BY-SA 2.5 before 2011-04-08, 3.0 from that
  date until 2018-05-02, and 4.0 on or after 2018-05-02. It says the applicable
  question/answer revision license is on the post timeline.
- **Locator:** heading `What is the license for the content I post?`, network
  page lines 80–88 in the caller capture.

## POL-02 — Public Network Terms

- **URL:** https://stackoverflow.com/legal/terms-of-service/public
- **Version:** last updated 2025-11-13.
- **Observed facts:** the terms bind all Public Network access and incorporate
  the Acceptable Use Policy and Privacy Policy. They distinguish Stack Overflow
  content from subscriber content, route API use through the API Terms, and
  describe subscriber content as perpetually and irrevocably CC-licensed.
- **Exact excerpt:** “all Public Content you contribute is available for public
  copy and redistribution”.
- **Locators:** lines 103–110, 137–158, and 191–196 in the caller capture.

## POL-03 — Acceptable Use Policy

- **URL:** https://stackoverflow.com/legal/acceptable-use-policy
- **Version signal:** page says the policy applies across the Network and, as
  of 2025-06-18, also to `stackoverflow.ai` and related services.
- **Observed facts:** the content-scraping/bot section restricts automated
  systems that access or collect Network content for three listed purposes,
  including harmful volume and generative-AI development uses.
- **Exact purpose excerpt:** “testing, indexing, benchmarking, or improving any
  generative AI, chatbot, large language, or machine learning tool”.
- **Other relevant facts:** it prohibits disruption and disclosure of
  non-manifestly-public identifying information, including usernames.
- **Locators:** lines 101, 110–112, and 127–131 in the caller capture.

## POL-04 — API Terms and throttles

- **Terms URL:** https://stackoverflow.com/legal/api-terms-of-use
- **Throttle URL:** https://api.stackexchange.com/docs/throttle
- **Observed facts:** API use is programmatic but incorporates the Stack
  Exchange Terms; applications must attribute the Network; access may be
  terminated on breach. The documented default daily quota is 10,000, dynamic
  `backoff` values must be followed, and semantically identical calls should not
  repeat more than once per minute.
- **Exact attribution excerpt:** “visually indicate that the Stack Exchange
  Network is the source”.
- **Locators:** API Terms lines 88–99; throttle documentation lines 1–10.

## POL-05 — Fitness robots response

- **URL:** https://fitness.stackexchange.com/robots.txt
- **Request:** unauthenticated HTTP/1.1 GET from the calibration environment.
- **Response:** `418 I'm a teapot`; server `Date: Fri, 10 Jul 2026 20:52:23
  GMT`; `Content-Type: text/plain`; `Cache-Control: private, no-store`.
- **Response body, complete:**

```text
License: https://stackoverflow.com/license.xml

User-agent: *
Content-signal: search=no, ai-train=no
Disallow: /
```

No challenge cookie or other response identifier is retained in this artifact.

## POL-06 — Privacy Policy

- **URL:** https://stackoverflow.com/legal/privacy-policy
- **Version:** last updated 2025-12-10.
- **Observed facts:** Public Network question, answer, profile, and reputation
  content may contain public username/profile information; questions, answers,
  or comments may later be deleted; public content is also made available via
  the API and Creative Commons data dump.
- **Exact persistence excerpt:** “such content, once public, cannot often be
  removed from public view”.
- **Locators:** lines 86–112, 119–142, and 186–203 in the caller capture.

## Unresolved questions for the policy specialist

- Whether this factory-calibration research is within the AUP's prohibited
  generative-AI testing/improvement purpose.
- Whether the authorized API route can be used for that purpose despite the AUP
  incorporated by the API Terms.
- Whether `Disallow: /` and the content signals rule out direct page retrieval
  independently of copyright permissions.
- Whether subscriber-content licensing and attribution allow durable packet
  redistribution for the exact contribution date/version while satisfying
  user-data handling and deletion obligations.
- Whether any official data dump or separately licensed product would fit the
  exact open-repository contract and research purpose.
