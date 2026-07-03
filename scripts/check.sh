#!/usr/bin/env bash
# Canonical repo gate for the Belief-changer agents-native repo.
# Fail-fast: exits non-zero on the first violation. Trust real exit codes only.
# Usage: bash scripts/check.sh [repo_root]
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"
ROOT="$(pwd -P)"
status=0

# 1. Structural validator (AGENTS.md size, code size, docs cap, root allowlist,
#    production-books required artifacts).
python3 "$ROOT/scripts/validate_repo.py" "$ROOT" || status=$?

# 2. shellcheck on scripts/ if available (non-fatal if the tool is absent).
if command -v shellcheck >/dev/null 2>&1; then
  shellcheck "$ROOT"/scripts/*.sh || status=$?
else
  echo "check.sh: shellcheck not installed — skipping (install for static shell checks)" >&2
fi

# 3. Tests, when code with a test runner exists.
if [ -f "$ROOT/scripts/test" ] && [ -x "$ROOT/scripts/test" ]; then
  "$ROOT/scripts/test" || status=$?
fi

exit "$status"
