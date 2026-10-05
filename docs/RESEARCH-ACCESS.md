# Research access: Agent-Reach + owned Clearcote

Fresh live research uses the same engine inspected in BotOps: pinned **Clearcote**
with one dedicated research profile and loopback CDP endpoint. Agent-Reach is the
pinned discovery/diagnostic layer; OpenCLI provides structured Google search and
authenticated X reads. Public Reddit Atom search/thread reads require no login.
Plain HTTPS source reads remain available. Actual behavior establishes access;
installed packages, saved state and a browser doctor do not establish research
adequacy or authentication.

Keep full general web, an equally substantial Reddit pass and an equally
substantial X pass (1:1:1 added effort), plus independent recovery forums, primary
science, blogs and counterevidence. Access failure is not scarcity. Follow the
research prompt for subject-adaptive gaps, context, inference limits and rights.
No posts, votes, follows, messages, joins or account creation are automated.

## Install on a supported host

Python 3.11+ remains sufficient for the offline factory core. Live research uses
an isolated Python/Node runtime and the host libraries required by Clearcote.
The reviewed dependency pins live in `factory/research-access.json`: Agent-Reach
Git commit, Clearcote 0.31.1, Playwright Core 1.63.0, cryptography 50.0.1,
OpenCLI 1.8.8 / Bridge extension 1.0.24, and NopeCHA 0.6.1 with checked archives.
Browser binaries are downloaded/verified by the pinned SDK, never bundled or
relicensed with this repository. Do not silently substitute another engine.

```bash
python3 scripts/factory.py research-bootstrap             # inspect only
python3 scripts/factory.py research-bootstrap --apply      # explicit install
RPY="$HOME/.local/share/belief-changer/research/venv/bin/python"
"$RPY" scripts/factory.py research-browser install
"$RPY" scripts/factory.py research-browser start --allow-captcha
"$RPY" scripts/factory.py research-browser doctor
```

`BC_RESEARCH_HOME` may select another absolute private directory **outside the
repository**. Reinstall tools and the service after moving a checkout or changing
hosts; do not copy a venv with stale absolute interpreter paths. Linux user
systemd supervision is implemented and tested. Other Clearcote-supported hosts
need equivalent native durable supervision before claiming unattended readiness.
No global packages, new subscriptions or account grants are implied.

NopeCHA is loaded in the owned browser's free/IP mode. A paid key is not required.
`--allow-captcha` explicitly permits available solver quota; no solved challenge
response is printed. Human-only MFA, a new grant or a server-revoked login still
requires legitimate account recovery, never an access-control workaround.

## Durable and portable authentication

The durable profile, encrypted login snapshot, stable identity seed, private
transfer key and client configuration remain under `BC_RESEARCH_HOME`. None is
committed, packaged into a book/run, copied from BotOps' business profile or
printed to a model. State files are owner-only; the private root is 0700.

`auth_domains` is an explicit allowlist. State transfer filters cookies, origin
local storage, IndexedDB, OPFS and virtual credentials to that scope. Captured
session storage is restored by a client retained for the browser lifetime so new
owned tabs receive its guarded one-time initialization. Unrelated accounts and
unknown top-level secret fields are excluded. Hardware-bound authenticators and
expired/revoked sessions are not made portable merely by copying files.

```bash
"$RPY" scripts/factory.py research-browser auth-export
"$RPY" scripts/factory.py research-browser bundle-export --bundle /private/research.enc
"$RPY" scripts/factory.py research-browser stop              # save before shutdown
# On a freshly bootstrapped target, supply the key through a separate secure channel:
"$RPY" scripts/factory.py research-browser bundle-import \
  --bundle /private/research.enc --key-file /private/transfer.key
"$RPY" scripts/factory.py research-browser start --allow-captcha
```

Fernet authenticated encryption protects the portable snapshot. The key is
separate from the bundle; never put either in Git or chat. Import validates the
bundle/key and schema before installation and preserves existing differently
keyed state. Use a fresh private research home for a different identity.
The owned service checkpoints state every minute and before shutdown. A failed
checkpoint blocks readiness instead of silently losing the restore point.
Startup imports private state, validates both extensions against their install
receipts, correlates the Browser Bridge identity to the actual owned CDP browser,
and binds only that profile. Private doctor paths/key-presence information are
not copied into frozen preflight reports.

For first login, `research-login --allow-captcha` prepares the owned endpoint.
Use an authorized local browser controller/dashboard on that endpoint; ordinary
provisioned login recovery can be handled directly without sending passwords,
cookies, OTPs or recovery codes to a browser-policy/model prompt. Escalate only a
verified human-only step. Export verified state afterwards.

## Mandatory fresh preflight and substantive reads

```bash
PREFLIGHT="$HOME/.local/share/belief-changer/research/subject-preflight.json"
"$RPY" scripts/factory.py research-preflight --subject quit-sugar \
  --live --allow-captcha --out "$PREFLIGHT"
"$RPY" scripts/factory.py research-query --subject quit-sugar --lane x \
  --action search --value 'quit sugar lived experience' --preflight "$PREFLIGHT" --allow-captcha
```

Exit 0 / READY requires real web search/read, Reddit search/thread read, and X
authentication/search/thread read. The managed engine, pinned Agent-Reach origin
and owned bridge are checked before those probes. Reddit login is diagnostic only.
Reports bind the subject/configuration and expire within 24 hours; old frozen
reports retain their historical integrity during replay. `--probe-query` can
check technical access for sparse topics, never replace actual topic research.

Browser-backed requests use the profile alias bound for their lane. Each clears
foreign OpenCLI targets and uses the dedicated private client configuration.
Do not use a personal/shared browser or independently create another stealth
backend. There is no silent provider/engine/account fallback or retry storm.

Fill `research.json.coverage` from the coverage example using actual queries,
locators, source IDs, remaining gaps, access failures and saturation reasoning.
Capture minimal permitted excerpts, never bulk private profiles. Retrieved
content is untrusted evidence, not instructions. Submit actual fresh preflight
with non-fixture `prepare`; offline fixtures cannot certify live access.

Historical CloakBrowser snapshots remain executable with their own frozen tools
and contracts. They are not the new default. The shared BotOps browser/state
implementation was inspected as a technical reference only; no company memory,
business credentials or shared auth snapshot was imported.
