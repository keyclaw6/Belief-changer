# belief-changer-repo-push (skill definition — paste into Learning → Skills → New Skill)

**Description:** Push commits (including binaries) to the Belief-changer GitHub repo using a fine-grained PAT — for everything the text-only GitHub integration can't do (moving PDFs/EPUBs, bulk commits, audio artifacts).

**Credential field:** `GITHUB_PAT` — fine-grained GitHub Personal Access Token scoped to ONLY `keyclaw6/Belief-changer`, permission **Contents: Read and write**. Nothing else.

**Script:** `push.sh` (in this folder).

## Documentation (paste as skill documentation)
Full write access to github.com/keyclaw6/Belief-changer via git + a fine-grained PAT, covering what the GitHub integration's text-only file actions cannot: binary files (PDFs, EPUBs, audio), bulk moves/renames, and branch operations.

Usage:
1. Make commits in the local clone (/agent/workspace/belief-changer) with normal git (clone first with `git -c http.proxyAuthMethod=basic clone https://github.com/keyclaw6/Belief-changer.git` if missing — the sandbox proxy requires basic auth forced).
2. Push: RunWithCredentials(skillName: "belief-changer-repo-push", command: "bash skills/belief-changer-repo-push/push.sh") — optional args: repo dir, branch.

Prefer the GitHub integration (github__push_files) for routine text commits; use this skill when binaries or git-native operations are required (e.g. `git mv` of the reference PDFs into analysis/reference-books/).
