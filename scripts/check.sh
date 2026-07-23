#!/usr/bin/env bash
# Canonical repo gate for the Belief-changer agents-native repo.
# Fail-fast: exits non-zero on the first violation. Trust real exit codes only.
# Usage: bash scripts/check.sh [repo_root]
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"
ROOT="$(pwd -P)"
status=0

PYTHON=()
if command -v python3 >/dev/null 2>&1 \
    && python3 -c 'import sys; raise SystemExit(sys.version_info.major != 3)' \
        >/dev/null 2>&1; then
  PYTHON=(python3)
elif command -v py >/dev/null 2>&1 \
    && py -3 -c 'import sys; raise SystemExit(sys.version_info.major != 3)' \
        >/dev/null 2>&1; then
  PYTHON=(py -3)
else
  echo "check.sh: no working Python 3 interpreter found" >&2
  exit 127
fi

# 1. Structural validator (AGENTS.md presence, docs cap, root allowlist, and
#    production-books required artifacts).
"${PYTHON[@]}" "$ROOT/scripts/validate_repo.py" "$ROOT" || status=$?

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

# 4. Stdlib regression tests for the deterministic evaluation instruments.
if [ -d "$ROOT/scripts/eval/tests" ]; then
  "${PYTHON[@]}" -m unittest discover -s "$ROOT/scripts/eval/tests" -p 'test_*.py' || status=$?
fi

exit "$status"
