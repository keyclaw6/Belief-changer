# Iteration-2 readiness — decision: BLOCKED on live research access

## Refresh findings (2026-09-16, all retrieved with provenance envelopes)

- Smoking: current Cochrane e-cigarette review is now v11 (2026, pub11):
  high-certainty vs NRT maintained, moderate-certainty SAE similarity (was
  inconclusive), longer trials still needed. A 2026 overview of EC cessation
  reviews (Wu et al., Addiction) maps evidence/gaps. Relapse-prevention
  review is current at pub6 (May-2019 horizon; conclusions unchanged).
- Sugar: refined OpenAlex 2023+ behavior-trial trail is a second honest
  negative (mechanistic/neuroimaging/GLP-1 adjacent only; no selectable human
  sugar-reduction behavior-change trial). YFAS 2024 correction still
  subscription-walled (re-verified).
- Dossiers built and gate-validated in session scratch
  (`research-quit-smoking-iter2.json`: 26 sources incl. new SM-R10, R2→pub11,
  R8→pub6 with verbatim-grounded excerpts; `research-quit-sugar-iter2.json`:
  26 sources plus the negative-trail envelope). Retrieval envelopes cached in
  the local (gitignored) phase-1 ledger.

## Blocker

No Iteration-2 run can be prepared: the research-access gate requires a READY
live preflight ≤24h old, and two live probes (2026-09-16 ~07:20 and ~08:55
UTC) return BLOCKED — Reddit/X auth exit 77 (sessions expired 2026-09-15;
bridge daemon itself healthy), general-web search returning no usable rows.
No credentials, keys, or sessions exist in this environment, and logins are
owner-interactive by contract. No retry storm was run.

## Needed to resume

Owner/local repair outside this session: restore signed-in Chromium/OpenCLI
bridge sessions (X + Reddit logins) and re-verify web search, then run a
fresh live preflight per subject. On a READY preflight, prepare the two
Iteration-2 runs from the validated dossiers above and run the full
autonomous pipeline (evidence → plan → chapters → editor → assemble →
independent audit with wrapper-flag triage → verify), then judgment round 2.
Study tally stands at 2 complete books + 1 judgment round; target remains
exactly 4 + 2. No books, runs, or reviews were manufactured around the wall.
