# REV-AUTH-SE-FITNESS — first-party follow-up retrieval

**Assignments:** `AUTH-SE-FITNESS-FU-01` through `FU-04`

**Retrieved (UTC):** 2026-07-10T20:56:30Z–2026-07-10T20:58:52Z

**Methods:** first-party-domain web search/open and direct unauthenticated GET
of `license.xml`. No question, answer, comment, profile, post timeline, search
result, data dump, API content result, or other user data was fetched. Response
cookies and request identifiers are not retained.

This is visible policy input for the independent specialist. The caller makes
no source-status decision.

## FU-01 — AUP purpose and automation scope

- **URL:** https://stackoverflow.com/legal/acceptable-use-policy
- **Version signal:** the page says the policy applies across the Network and,
  as of 2025-06-18, also to `stackoverflow.ai` and related services.
- **Relevant provision:** lines 127–132 prohibit automated systems from
  accessing or collecting Network content for listed purposes, including
  developing, testing, benchmarking, or improving generative-AI/LLM systems.
- **Exact exception excerpt:** “exempt from this policy if you have obtained
  express prior written consent”.
- **Named examples:** accessibility and a commercial license agreement; the
  page supplies a contact address for inquiries.
- **First-party clarification search:** official-domain queries for automated
  research, AI-assisted research, model evaluation/calibration, non-training
  book research, API exceptions, and content signals returned no legal/help
  clarification granting a research, quotation, nonprofit, or public-interest
  exception. The returned generative-AI posting help concerns authorship of
  answers, not automated data collection.

## FU-02 — API permission and robots relationship

- **API Terms URL:** https://stackoverflow.com/legal/api-terms-of-use
- **Throttle URL:** https://api.stackexchange.com/docs/throttle
- **Relevant terms:** the API is a programmatic interface, but users agree to
  both the API Agreement and Stack Exchange Terms. Attribution is mandatory;
  access may be terminated for breach.
- **Documentation facts:** default quota 10,000, dynamic `backoff` must be
  obeyed, and identical requests should not repeat more than once a minute.
- **Search result:** first-party API/legal documentation exposed no provision
  saying that the API overrides the AUP's purpose restriction, the site's
  `Disallow: /`, `search=no`, or `ai-train=no` signals, and no additional
  storage/deletion/redistribution permission for this project purpose.

## FU-03 — license and redistribution conditions

- **Fitness help:** https://fitness.stackexchange.com/help/licensing
- **Network help:** https://stackoverflow.com/help/licensing
- **Terms:** https://stackoverflow.com/legal/terms-of-service/public
- **Machine-readable license:** https://stackoverflow.com/license.xml
- **Direct response:** `200 OK`; server `Date: Fri, 10 Jul 2026 20:58:52
  GMT`; `Content-Type: application/rsl+xml`.
- **Complete `license.xml` body:**

```xml
<rsl xmlns="https://rslstandard.org/rsl">
    <content url="/">
        <terms>https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt</terms>
    </content>
</rsl>
```

- **License facts:** the help page assigns CC BY-SA 2.5, 3.0, or 4.0 by
  contribution date and says the applicable question/answer revision license
  appears on its timeline. The Terms describe subscriber content as perpetual
  and irrevocable and require attribution for public redistribution.
- **Unresolved by these documents:** the machine-readable root declaration
  does not state how to apply historical versions, third-party inclusions,
  comments, revisions, or deleted/anonymized contributions in a repository
  packet. Copyright reuse terms do not state an automated-access exception.

## FU-04 — deletion, data dump, and user data

- **Privacy:** https://stackoverflow.com/legal/privacy-policy
- **Account deletion:** https://stackoverflow.com/help/deleting-account
- **Post deletion:** https://stackoverflow.com/help/deleted-questions
- **Data dump:** https://stackoverflow.com/help/data-dumps
- **Account-deletion facts:** profile deletion deletes or anonymizes account
  information. The help page says answers/comments remain license-governed and
  have no user-generated-content erasure requirement.
- **Post-deletion facts:** deleted posts disappear for most users and normally
  leave search results, while authors, staff/moderators, and sufficiently
  privileged users may retain access; posts can later be undeleted.
- **Data-dump facts:** a new site dump is made available quarterly through
  account settings. Download requires checking an affirmation that the file is
  not intended for LLM training.
- **Privacy facts:** public usernames/profile fields may accompany public
  contributions; users have personal-data rights; Stack Exchange says public
  content may persist elsewhere after removal from its systems.
- **Unresolved by these documents:** no operational rule expressly authorizes
  this project to retain a stale username/profile link after account deletion
  or disassociation. No documented feed of deletions/anonymizations was found
  in the first-party API/data-dump material retrieved here.

## FU-05 — external authorization boundary

The model commissioned prior written project-specific authorization from Stack
Exchange. No message or request was sent: external outreach is outside this
read-only retrieval assignment and requires founder authority. The current
artifact contains no such authorization.
