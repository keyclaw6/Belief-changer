#!/usr/bin/env bash
# Self-contained stage daemon. Usage: daemon.sh <name> <command...>
# Launched inside RunWithCredentials so the detached child inherits the
# credential env vars; returns immediately. Progress via $LOG, exit code
# via $DONE file. Never logs credential values.
set -u
NAME=$1; shift
DIR=${LOOP_DAEMON_DIR:-"$(cd "$(dirname "$0")" && pwd)/../../.loop-work/daemons"}
mkdir -p "$DIR"
LOG=$DIR/$NAME.log
DONE=$DIR/$NAME.exit
PIDF=$DIR/$NAME.pid
if [ -f "$PIDF" ] && kill -0 "$(cat "$PIDF")" 2>/dev/null; then
  echo "daemon $NAME already running (pid $(cat "$PIDF"))"; exit 0
fi
rm -f "$DONE"
nohup bash -c "$*; echo \$? > '$DONE'" > "$LOG" 2>&1 &
echo $! > "$PIDF"
echo "daemon $NAME started (pid $!) — log: $LOG"
