# Reddit source-policy autopsy — 2026-07-10

## Trigger

The A1 persona pilot followed model-generated retrieval commissions into Reddit. Search plugins failed, a caller web search returned snippets, and a rate-respecting Atom endpoint returned direct public post/comment feeds. Before packet acceptance, source audits of the founder-proposed browser transports exposed a permission and retention conflict.

No Reddit-derived evidence is accepted. No persona or bank cell is filled from the removed artifacts.

## Current authoritative policy evidence

- [Responsible Builder Policy](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy) requires explicit approval for Reddit data access, prohibits masking access and circumventing limits, says research outside the Reddit for Researchers program violates the policy, limits retention to immediate project need, and requires deletion-refresh compliance.
- [Developer Platform & Accessing Reddit Data](https://support.reddithelp.com/hc/en-us/articles/14945211791892-Developer-Platform-Accessing-Reddit-Data) identifies Reddit for Researchers as the authorized research route.
- [Reddit for Researchers Program](https://support.reddithelp.com/hc/en-us/articles/49381918834964-Reddit-for-Researchers-Program) prohibits redistribution, restricts access to the approved project, requires permanent deletion when the project ends, and supplies monthly deletion-aware updates.
- [User Agreement](https://redditinc.com/policies/user-agreement) prohibits automated collection except as permitted by the terms or a separate agreement and prohibits scraping without prior written consent.
- [Deletion guidance](https://support.reddithelp.com/hc/en-us/articles/24656943463828-What-happens-when-I-delete-my-data) requires third parties to stop displaying or using content deleted by Redditors or Reddit.

The factory's open Git packet contract is incompatible with those default research restrictions: git history is durable and redistributable, while Reddit research data is approval-bound, non-redistributable, deletion-sensitive, and project-limited.

## Failure mechanism

The research protocol treated topical relevance and quote provenance as sufficient source gates. It did not require a pre-retrieval check of access permission, automation method, retention/deletion duties, or whether raw source packets may be redistributed in an open repository. That omission allowed a technically successful but unauthorized transport pilot to progress too far.

Stealth tooling cannot solve this. Fingerprint masking or humanized browsing would attempt to evade a technical guardrail while leaving the authorization and retention conflict intact.

## Immediate remediation

- Live Reddit retrieval and the H-033/H-034 stealth trials are stopped.
- Direct feeds, search-result text, and derivative quote/review artifacts are removed from the current calibration pilot tree.
- Retained pilot artifacts are non-content runtime metadata, the model-owned retrieval commission, and this policy autopsy; none is accepted evidence.
- The research prompt, HARNESS, and active OpenSpec change now require a source-authorization and retention gate before retrieval.
- Reddit remains excluded unless an approved Reddit for Researchers project or a separate written agreement from Reddit expressly covers the exact access method, retention/deletion mechanism, and factory output contract.
- Research continues with terms-compatible first-person communities and sources; depth requirements do not fall.

## Legacy scope

This remediation governs the calibration pilot and all new factory research. Older production-book workshops contain legacy Reddit-derived research artifacts. They are not inputs to this calibration run and do not count as accepted evidence. Because production artifacts have separate immutability rules, repository-wide legacy removal or quarantine requires its own founder-approved remediation; this pilot's regression test intentionally covers the affected calibration paths rather than claiming a repository-wide purge.

## History-removal gap

The removed content was already pushed on the dedicated `calibration-lab` branch in earlier pilot commits. A normal deletion does not purge git history. Rewriting and force-pushing the branch is destructive and requires explicit founder approval; until then, the remote-history remediation remains open and no pull request or merge may expose that branch as acceptable.

## Hypothesis disposition

- H-032 remains `TESTING`: the scout/retrieval/reviewer separation successfully caught unsupported and altered evidence, but the source-permission gate was missing.
- H-033 and H-034 are live-Reddit `NO-GO` without Reddit-issued authorization covering the exact use. Their code may still be audited and tested on controlled fixtures; adoption requires a lawful quality/reliability win and no deterministic research judgment.
