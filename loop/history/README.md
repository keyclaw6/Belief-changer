# Compact campaign history

The founder requested deletion of intermediate experiment information on 2026-09-11. The current tree retains verdicts, hypotheses, actual change.diff files where they existed, aggregate results/learnings and final campaign summaries. `campaign-001.json` indexes all 51 numbered records, including baseline 000. Old paths quoted inside these historical records may no longer exist in the working tree; they are historical references, not current operating instructions.

Complete old artifacts remain recoverable from commit `6a90ffcdddad3c908144014cc41e51d693df7f9e` in existing Git history. No force-push/history purge is requested or performed. `compaction.json` documents removals and verifies that both original and current vision/strategy files were preserved byte-for-byte.

For new campaigns: keep active run evidence while it is being evaluated; store full evidence bundles outside the source tree or as explicitly retained release artifacts. After an authorized campaign close, retain decision, hypothesis, diff, input/output hashes and the external evidence-bundle locator. Never delete an active run merely to reduce counts and never fabricate metrics after compaction. Browser profiles, cookies and raw social captures are never source files.
