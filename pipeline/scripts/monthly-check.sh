#!/usr/bin/env bash
#
# Shipped. — Monthly issue heartbeat
# Runs on the 1st of each month at 09:00 local (see com.id8labs.shipped-monthly.plist).
#
# What it does:
#   1. Computes the month that just ended (YYYY-MM).
#   2. Checks whether content/anthropic-monthly/YYYY-MM.md exists and its status.
#   3. Emits a macOS desktop notification:
#        - missing  -> "Monthly due: generate <Month> issue"
#        - draft    -> "Monthly drafted, awaiting editorial/ship"
#        - published-> "Monthly shipped"
#
# It does NOT generate content, auto-publish, auto-commit, or modify anything.
# A good monthly needs a research + voice pass (gaps the daily files don't cover),
# which is a Claude session, not a shell cron. This is a read-only nudge only.
# Generation recipe: content/anthropic-monthly/README.md

set -euo pipefail

PIPELINE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$PIPELINE_ROOT/.." && pwd)"
MONTHLY_DIR="$REPO_ROOT/content/anthropic-monthly"
LOG_DIR="$HOME/Library/Logs/shipped"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/monthly.log"

ts() { date "+%Y-%m-%d %H:%M:%S"; }
log() { echo "[$(ts)] $*" >> "$LOG"; }

log "---- monthly check start ----"

# The month that just ended. On the 1st, `date -v-1m` lands in the prior month.
PREV_MONTH="$(date -v-1m "+%Y-%m")"           # e.g. 2026-05
PREV_MONTH_LABEL="$(date -v-1m "+%B %Y")"     # e.g. May 2026
ISSUE_FILE="$MONTHLY_DIR/$PREV_MONTH.md"

log "target month: $PREV_MONTH ($PREV_MONTH_LABEL) -> $ISSUE_FILE"

STATUS="MISSING"
if [ -f "$ISSUE_FILE" ]; then
  # status: comes from the YAML frontmatter (draft | published | archived)
  FM_STATUS="$(grep -m1 -E '^status:' "$ISSUE_FILE" | awk '{print $2}' | tr -d '[:space:]')"
  case "${FM_STATUS:-}" in
    published) STATUS="PUBLISHED" ;;
    draft)     STATUS="DRAFT" ;;
    archived)  STATUS="ARCHIVED" ;;
    *)         STATUS="DRAFT" ;;
  esac
fi

log "status: $STATUS"

case "$STATUS" in
  MISSING)
    TITLE="Shipped. Monthly due"
    SUBTITLE="$PREV_MONTH_LABEL not generated"
    BODY="Run the monthly generation for $PREV_MONTH_LABEL. Recipe: content/anthropic-monthly/README.md"
    SOUND="Basso"
    ;;
  DRAFT)
    TITLE="Shipped. Monthly"
    SUBTITLE="$PREV_MONTH_LABEL drafted"
    BODY="$PREV_MONTH.md is staged (draft). Editorial pass + ship gate remain."
    SOUND="Pop"
    ;;
  PUBLISHED)
    TITLE="Shipped. Monthly"
    SUBTITLE="$PREV_MONTH_LABEL shipped"
    BODY="$PREV_MONTH.md is published. Nothing to do."
    SOUND="Glass"
    ;;
  ARCHIVED)
    TITLE="Shipped. Monthly"
    SUBTITLE="$PREV_MONTH_LABEL archived"
    BODY="$PREV_MONTH.md is archived."
    SOUND="Glass"
    ;;
esac

BODY_ESC="$(echo "$BODY" | sed 's/"/\\"/g')"

osascript <<APPLESCRIPT
display notification "$BODY_ESC" with title "$TITLE" subtitle "$SUBTITLE" sound name "$SOUND"
APPLESCRIPT

log "notify sent: $TITLE | $SUBTITLE | STATUS=$STATUS"
log "STATUS: ${STATUS}"
log "---- monthly check done ----"
