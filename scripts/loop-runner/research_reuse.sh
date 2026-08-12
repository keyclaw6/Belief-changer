#!/usr/bin/env bash
# research_reuse.sh — the ONE deterministic handover in the loop.
#
# Decides whether the research stage must rerun for this iteration, or whether
# the last accepted research can be reused. Research is reused across
# iterations unless the hypothesis changed the research stage or the brief
# (PROGRAM.md Step 3). That decision is a pure function of WHICH file the
# hypothesis changed, so it belongs in code, not in a prompt.
#
# Usage: research_reuse.sh <changed-file-relative-path> [book-slug] [diff-file]
#   changed-file is the single editable file the hypothesis touched.
#   book-slug defaults to the calibration book, quit-sugar.
#   diff-file (optional) is loop/iterations/NNN/change.diff — used to scope a
#     config.yaml change to research keys only.
#
# Exit 0 and prints REUSE   -> reuse the last accepted research artifacts.
# Exit 0 and prints RERUN   -> the research stage must rerun.
#
# Fails SAFE to RERUN whenever there is nothing valid to reuse (a research
# trigger changed, or the ACTIVE book has no accepted research artifacts yet).
set -euo pipefail

changed_file="${1:-}"
book="${2:-quit-sugar}"
diff_file="${3:-}"
research_dir="production-books/${book}/research"

# Files whose change forces a research rerun:
#  - the research prompt itself
#  - the research keys in the config (only when the diff touches them)
#  - the book brief
is_research_trigger() {
  case "$1" in
    prompts/research-agent.md)        return 0 ;;
    loop/config.yaml)
      # config.yaml is the sole route/parameter authority for EVERY role, so a
      # change to it only forces a research rerun when the diff touches a
      # research key. A writer/planner/judge-only config change must NOT rerun
      # the slow deep-research stage. Default to RERUN when the diff is absent
      # or unreadable (fail safe).
      local diff_file="${2:-}"
      if [ -n "$diff_file" ] && [ -f "$diff_file" ]; then
        # A content line naming a research key forces a rerun. Content lines
        # start with a single +/- (file headers are +++/--- and are excluded
        # because their 2nd char differs).
        if grep -qE '^[+-].*(researcher_|research_)' "$diff_file"; then
          return 0
        fi
        return 1   # config changed, but no research key — reuse
      fi
      return 0       # no diff available — fail safe to RERUN
      ;;
    production-books/*/00-brief.md)   return 0 ;;
    */00-brief.md)                    return 0 ;;
    *)                                return 1 ;;
  esac
}

if [ -n "$changed_file" ] && is_research_trigger "$changed_file" "$diff_file"; then
  echo "RERUN"
else
  # REUSE is only valid if the ACTIVE book has accepted research to reuse.
  # A fresh checkout, a clean, or a baseline (nothing produced yet) has none —
  # fail SAFE to RERUN rather than silently hand the planner empty inputs.
  # Scoped to the active book (never a sibling book's research).
  if [ -d "$research_dir" ] && \
     find "$research_dir" -type f 2>/dev/null | grep -q .; then
    echo "REUSE"
  else
    echo "RERUN"
  fi
fi
