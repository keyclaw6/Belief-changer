#!/usr/bin/env bash
# research_reuse.sh — the ONE deterministic handover in the loop.
#
# Decides whether the research stage must rerun for this iteration, or whether
# the last accepted research can be reused. Research is reused across
# iterations unless the hypothesis changed the research stage or the brief
# (PROGRAM.md Step 3). That decision is a pure function of WHICH file the
# hypothesis changed, so it belongs in code, not in a prompt.
#
# Usage: research_reuse.sh <changed-file-relative-path>
#   changed-file is the single editable file the hypothesis touched
#   (loop/iterations/NNN/change.diff's target).
#
# Exit 0 and prints REUSE   -> reuse the last accepted research artifacts.
# Exit 0 and prints RERUN   -> the research stage must rerun.
#
# Fails SAFE to RERUN whenever there is nothing valid to reuse (a research
# trigger changed, or no accepted research artifacts exist on disk yet).
set -euo pipefail

changed_file="${1:-}"

# Files whose change forces a research rerun:
#  - the research prompt itself
#  - the config (it carries researcher model/route/params)
#  - the book brief
is_research_trigger() {
  case "$1" in
    prompts/research-agent.md)        return 0 ;;
    loop/config.yaml)                 return 0 ;;
    production-books/*/00-brief.md)   return 0 ;;
    */00-brief.md)                    return 0 ;;
    *)                                return 1 ;;
  esac
}

if [ -n "$changed_file" ] && is_research_trigger "$changed_file"; then
  echo "RERUN"
else
  # REUSE is only valid if accepted research actually exists to reuse. A fresh
  # checkout, a clean, or a baseline (nothing produced yet) has none — fail
  # SAFE to RERUN rather than silently hand the planner empty inputs.
  if ls production-books/*/research/ >/dev/null 2>&1 && \
     find production-books/*/research/ -type f 2>/dev/null | grep -q .; then
    echo "REUSE"
  else
    echo "RERUN"
  fi
fi
