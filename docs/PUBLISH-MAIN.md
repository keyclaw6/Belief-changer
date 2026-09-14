# Publish the cleaned v2.1 delivery, leaving only main

This delivery includes the complete source state from `upgrade/truth-first-factory-v2` plus the researched access integration and authorized compaction. The upgrade already contains the known `campaign-001` and `main` ancestry. **The publication script does not mean GitHub has already been changed.** This session's connected GitHub/remote-computer tools were read-only, so final publication must run on your authenticated computer.

Unzip the delivery, open a terminal in `Belief-changer`, and inspect the plan:

```bash
python3 scripts/publish_main.py --destination "$HOME/Belief-changer-main-v21"
```

Apply with the same command plus `--apply`:

```bash
python3 scripts/publish_main.py --destination "$HOME/Belief-changer-main-v21" --apply
```

The destination must **not already exist**. Your existing checkouts, uncommitted work and local credentials are never reset or cleaned. The command requires Git, GitHub CLI (`gh`), Python 3.11+, bash and authenticated Git push/admin access to `keyclaw6/Belief-changer`. It uses your configured Git identity; when none is configured, it can derive a public noreply identity from your authenticated `gh` login. Alternatively pass both `--git-name` and `--git-email`.

The script first verifies the delivery's per-file checksums and all three reviewed remote branch heads. It creates a fresh clone, proves that main and campaign are ancestors of upgrade, fast-forwards its local main to upgrade, applies the verified clean source tree, runs the regression suite and complete offline demo, and commits. Before publishing it checks the remote heads again. GitHub currently defaults to `campaign-001`; the script changes the default to `main` immediately before publication. A **single atomic Git push** advances main and removes exactly `campaign-001` and `upgrade/truth-first-factory-v2`; deletion leases protect against concurrent updates. If GitHub rejects permissions, protection rules or atomic pushes, the script stops—there is no half-merge/delete fallback. The default-branch setting is a separate GitHub metadata operation, not part of the Git transaction. On a rejected push with unchanged refs, the script attempts to restore the previous default; if the network outcome is uncertain it stops for inspection rather than guessing.

Afterward it verifies that GitHub and its new local publication clone have only main and that all three prior heads remain ancestors. It does not delete branches or worktrees from unrelated existing local clones. Those can be pruned separately after saving their work. The script changes branch refs and the default branch only; it does not explicitly retarget or close pull requests. All previous branch commits remain reachable from main.

If branch heads changed since the delivery was made, the script deliberately refuses to proceed. Reconcile the new work before updating the expected heads. Do not bypass this guard with a force-push. If a test fails, nothing is pushed; inspect the newly created clone and test output. Choose a new nonexistent destination for a fresh attempt.

Compaction changes the current working tree, **not Git history**. Old manuscripts and traces remain recoverable from earlier commits, so a full-history clone may still be large. A new `--depth 1` clone after publication obtains the compact current tree. No history rewrite or deletion of original project vision is performed.

Software tests are offline. Publishing does not install browser services, log into X/Reddit, solve a live CAPTCHA, start a paid campaign or certify book effectiveness. Complete `docs/RESEARCH-ACCESS.md` before the next campaign.
