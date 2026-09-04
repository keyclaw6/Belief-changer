#!/usr/bin/env bash
# PROGRAM §2 preflight battery: 18 judge calls (6 PASS-test, 6 repeatability,
# 6 voice-probe). Each judge call is a spawned `judge` sub-agent (pi
# subagent tool, `.pi/agents/judge.md`); model/reasoning from
# loop/config.yaml.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO=${BC_REPO:-"$(cd "$HERE/../.." && pwd)"}
CFG=$REPO/loop/config.yaml
IN=$REPO/loop/preflight/inputs
RUNS=${PREFLIGHT_RUNS_DIR:-$REPO/loop/preflight/runs}
JUDGES=$REPO/loop/judges
EFFORT=$(grep -E '^judge_reasoning:' "$CFG" | sed 's/^[^:]*: *//; s/ *#.*//')
MODEL=$(grep -E '^judge_model:' "$CFG" | sed 's/^[^:]*: *//; s/ *#.*//')
# Provider comes from config (judges stay on judge_route / OpenCode Go;
# Muse Spark is writer/planner only, never the judges); if
# config fails to declare it, stop rather than guess.
PROVIDER=$(grep -E '^judge_route:' "$CFG" | sed 's/^[^:]*: *//; s/ *#.*//')
[ -n "$PROVIDER" ] || { echo "run_preflight: judge_route missing from $CFG — refusing to guess a provider" >&2; exit 1; }
mkdir -p "$RUNS"

run_one() {  # judge input-file out-tag
  local judge=$1 input=$2 tag=$3
  [ -f "$RUNS/$tag/response.md" ] && { echo "skip $tag (done)"; return 0; }
  mkdir -p "$RUNS/$tag"
  pi --provider "$PROVIDER" --model "$MODEL" --thinking "$EFFORT" -p \
    "Use the subagent tool once with agent 'judge' and this task: rubric file $JUDGES/$judge.md, input file $input. Return your verdict exactly as the rubric requires, nothing else." \
    --no-session > "$RUNS/$tag/response.md" 2>/dev/null
}

pids=(); fail=0
launch() { run_one "$@" & pids+=($!); sleep 5; }  # stagger to avoid burst 403s

# PASS test: each chapter judge, twice
for j in belief-mechanic voice-emotion reader-journey; do
  for n in 1 2; do launch "$j" "$IN/pass-test-$j.md" "pass-test-$j-run$n"; done
done
for p in "${pids[@]}"; do wait "$p" || fail=1; done; pids=()

# Repeatability: each judge twice on identical generated chapter
for j in belief-mechanic voice-emotion reader-journey; do
  for n in 1 2; do launch "$j" "$IN/repeat-$j.md" "repeat-$j-run$n"; done
done
for p in "${pids[@]}"; do wait "$p" || fail=1; done; pids=()

# Voice honesty probe: six pairs, voice judge
for f in "$IN"/probe-*.md; do
  tag=$(basename "$f" .md)
  launch voice-emotion "$f" "$tag"
done
for p in "${pids[@]}"; do wait "$p" || fail=1; done

echo "=== verdict lines ==="
for d in "$RUNS"/*/; do
  tag=$(basename "$d")
  v=$(head -1 "$d/response.md" 2>/dev/null || echo MISSING)
  echo "$tag: $v"
done
exit $fail
