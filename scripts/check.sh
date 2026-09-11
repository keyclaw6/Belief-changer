#!/usr/bin/env bash
# Mandatory, offline v2 gate. No provider keys or paid calls are used.
set -euo pipefail
ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
cd "$ROOT"
PYTHON="${PYTHON:-python3}"
"$PYTHON" -c 'import sys; assert sys.version_info >= (3, 11), "Python 3.11+ required"'
"$PYTHON" scripts/validate_repo.py .
"$PYTHON" -m compileall -q scripts/bc_factory scripts/factory.py scripts/eval/tests
"$PYTHON" -m unittest discover -s scripts/eval/tests -p 'test_*.py' -v
"$PYTHON" scripts/factory.py --help >/dev/null
"$PYTHON" .cursor/hooks/loop-continue.py self-check
printf '\nOFFLINE GATE PASSED — software checks only; no efficacy or release claim.\n'
