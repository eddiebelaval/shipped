#!/usr/bin/env bash
#
# Shipped. — Nightly status heartbeat
# Runs at 21:00 local (see com.id8labs.shipped-nightly.plist).
#
# What it does:
#   1. Regenerates the production dashboard (pnpm dashboard)
#   2. Parses readiness % + ship date + gap count from stdout
#   3. Emits a macOS desktop notification with the summary
#
# It does NOT auto-publish, auto-commit, or modify content. Read-only nudge.

set -euo pipefail

PIPELINE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$HOME/Library/Logs/shipped"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/nightly.log"

ts() { date "+%Y-%m-%d %H:%M:%S"; }
log() { echo "[$(ts)] $*" >> "$LOG"; }

log "---- nightly check start ----"

cd "$PIPELINE_ROOT"

DASH_OUT="$(pnpm dashboard 2>&1)" || {
  log "dashboard build FAILED"
  echo "$DASH_OUT" >> "$LOG"
  osascript -e 'display notification "Dashboard build failed. Check ~/Library/Logs/shipped/nightly.log" with title "Shipped." subtitle "Nightly check error" sound name "Basso"'
  exit 1
}

echo "$DASH_OUT" >> "$LOG"

SUMMARY=$(echo "$DASH_OUT" | grep -E "Issue [0-9]+ . ship " | head -1 | sed 's/^[[:space:]]*//')
GAPS=$(echo "$DASH_OUT" | grep -E "^[[:space:]]*Gaps:" | head -1 | awk -F': ' '{print $2}' | tr -d '[:space:]')
ARTICLES=$(echo "$DASH_OUT" | grep -E "^[[:space:]]*Articles:" | head -1 | sed 's/^[[:space:]]*//')

if [ -z "$SUMMARY" ]; then
  log "could not parse summary; aborting notify"
  exit 1
fi

PCT=$(echo "$SUMMARY" | grep -oE "[0-9]+% ready" | grep -oE "^[0-9]+")
if [ -z "$PCT" ]; then PCT=0; fi

if [ "$PCT" -ge 90 ]; then
  SOUND="Glass"
  TONE="ship-ready"
elif [ "$PCT" -ge 70 ]; then
  SOUND="Pop"
  TONE="on track"
elif [ "$PCT" -ge 50 ]; then
  SOUND="Pop"
  TONE="mid-stream"
else
  SOUND="Basso"
  TONE="early stage"
fi

TITLE="Shipped. nightly"
SUBTITLE="$TONE | ${GAPS:-?} gap(s)"
BODY=$(echo "$SUMMARY | $ARTICLES" | sed 's/"/\\"/g')

log "notify: $SUMMARY | $ARTICLES | gaps=$GAPS | tone=$TONE"

osascript <<APPLESCRIPT
display notification "$BODY" with title "$TITLE" subtitle "$SUBTITLE" sound name "$SOUND"
APPLESCRIPT

log "---- nightly check done ----"
