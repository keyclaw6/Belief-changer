#!/usr/bin/env bash
# Credential-holder job runner. Launched ONCE via RunWithCredentials (inherits
# the skill credentials in env) and then executes queued jobs indefinitely,
# making the campaign immune to credential-tool flapping.
# Queue protocol (plain files, written by the orchestrator with no creds):
#   queue/pending/<name>.job   — bash script to execute
#   queue/running/<name>.job   — moved here while executing
#   queue/done/<name>.exit     — exit code when finished
#   queue/logs/<name>.log      — stdout+stderr
#   queue/STOP                 — touch to shut the runner down
# Never logs credential values.
set -u
Q=${LOOP_QUEUE_DIR:-"$(cd "$(dirname "$0")" && pwd)/../../.loop-work/queue"}
mkdir -p "$Q/pending" "$Q/running" "$Q/done" "$Q/logs"
echo "queue runner up (pid $$) $(date -u +%FT%TZ)" > "$Q/runner.status"
while true; do
  [ -f "$Q/STOP" ] && { echo "stopped $(date -u +%FT%TZ)" >> "$Q/runner.status"; exit 0; }
  job=$(ls "$Q/pending" 2>/dev/null | head -1)
  if [ -n "${job:-}" ]; then
    name="${job%.job}"
    mv "$Q/pending/$job" "$Q/running/$job"
    echo "running $name $(date -u +%FT%TZ)" >> "$Q/runner.status"
    bash "$Q/running/$job" > "$Q/logs/$name.log" 2>&1
    echo $? > "$Q/done/$name.exit"
    mv "$Q/running/$job" "$Q/done/$job"
    echo "finished $name exit=$(cat "$Q/done/$name.exit") $(date -u +%FT%TZ)" >> "$Q/runner.status"
  else
    sleep 5
  fi
done
