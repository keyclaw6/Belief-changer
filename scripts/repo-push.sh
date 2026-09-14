#!/usr/bin/env bash
# Push the local Belief-changer clone to GitHub using the PAT credential.
# Usage: push.sh [repo_dir] [branch]   (defaults: /agent/workspace/belief-changer, main)
# Requires env: GITHUB_PAT (injected by RunWithCredentials)
set -euo pipefail
REPO_DIR="${1:-/agent/workspace/belief-changer}"
BRANCH="${2:-main}"
[ -z "${GITHUB_PAT:-}" ] && { echo "ERROR: GITHUB_PAT not set (run via RunWithCredentials)"; exit 1; }
cd "$REPO_DIR"
git -c http.proxyAuthMethod=basic push "https://x-access-token:${GITHUB_PAT}@github.com/keyclaw6/Belief-changer.git" "HEAD:${BRANCH}"
echo "Pushed $(git rev-parse --short HEAD) to ${BRANCH}"
