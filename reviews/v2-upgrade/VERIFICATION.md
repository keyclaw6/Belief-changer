# Factory v2 upgrade verification

Base: `cd730abc9d902f6394a529144ce54c400ae50751` on campaign-001.
Upgrade branch: `upgrade/truth-first-factory-v2`.

## Executed checks

- All **75 offline regression tests passed** on the full repository. The mandatory gate also validates runtime contracts, compiles the Python code, tests the CLI and confirms the legacy continuation hook is disabled.
- A complete synthetic two-chapter pipeline passed: evidence gate, plan/review, sequential draft/review/state, whole-book edit, assembly, independent-shaped final audit and complete verification. Live model calls: **0**. This is a software fixture, not a generated research book.
- The exact frozen code snapshot independently verified the same assembled manuscript hash.
- Calling the legacy judge without a v2 run returned exit 2 and explicitly made no model calls. It did not print PANEL DONE.
- Original tracked iterations, research, reference assets and production manuscripts have no diff against the base commit. Legacy books are explicitly marked unvalidated for v2.
- Replaced operational contracts are archived. The archive README is the retirement notice; the original README is preserved as `ORIGINAL-README.md`.
- Real environment credentials are no longer tracked on this branch. The encrypted local .env remains on the computer; the repository and ZIP supply .env.example instead. Historical Git history has not been rewritten.
- ZIP tests validate credential exclusions, CRC integrity, fixed timestamps and reproducible content hashes. The full repository ZIP is generated and checked by the CI workflow.

## Not claimed

No paid generation campaign, independent live-provider compatibility test, human calibration, qualified health/rights review, source-by-source re-verification or reader-outcome study was performed. Software gate success does not prove better prose, medical safety, copyright clearance or belief-change effectiveness. The external evaluator is deliberately unconfigured; release is blocked until the documented independent evaluation and actual review requirements are met.

See `verification.json` and the accompanying raw logs. `docs/UPGRADE-MAP.md` maps each audited problem to its implementation and tests. `docs/FACTORY-V2.md` explains operation and remaining setup. The GitHub workflow records verification of the committed tree and publishes the complete credential-free ZIP artifact.
