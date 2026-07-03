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

# 3. openspec strict validation of every active change (AGENTS.md mandates this).
#    No-op if the openspec CLI is absent (e.g. a fresh checkout before bootstrap)
#    or there are no active changes — the gate grows with the repo, not ahead of it.
if command -v openspec >/dev/null 2>&1; then
  for ch in "$ROOT"/openspec/changes/*/; do
    [ -d "$ch" ] || continue
    case "$ch" in */archive/*) continue;; esac
    name="$(basename "$ch")"
    openspec validate "$name" --strict >/dev/null 2>&1 || {
      echo "check.sh: openspec validate $name --strict FAILED" >&2
      openspec validate "$name" --strict >&2 2>&1 | tail -8 >&2
      status=1
    }
  done
else
  echo "check.sh: openspec not installed — skipping spec validation (run belief-changer-bootstrap)" >&2
fi

# 4. Tests, when code with a test runner exists.
if [ -f "$ROOT/scripts/test" ] && [ -x "$ROOT/scripts/test" ]; then
  "$ROOT/scripts/test" || status=$?
fi

exit "$status"
