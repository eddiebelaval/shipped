#!/usr/bin/env bash
#
# Shipped. — daily publish watchdog
# Runs at 21:40 local ET (see cron/com.id8labs.shipped-daily-watchdog.plist),
# after the 21:00 cloud routine has had ~40 minutes to publish and before the
# 22:45 distribute job.
#
# It asks ONE question: is today's Eastern-dated daily on `daily-pages`?
#
# Why it exists. On 2026-07-26 and 2026-07-30 the routine did not run and
# nothing said so. On 2026-08-05 it ran but derived its stem from a UTC clock
# at 21:25 ET, published `2026-08-06.html` (titled "Thursday, August 6") with
# Aug 5 content inside, and the 2026-08-05 edition was never written. In all
# three cases every heartbeat on this machine stayed green: nightly-check.sh
# watches the WEEKLY magazine dashboard and knows nothing about the daily, and
# distribute-local.py logged "no new pages to draft" and exited 0.
#
# distribute-local.py now carries the same tripwire, but that one only fires if
# the distribute job itself runs. This is the independent eye.
#
# Read-only. Never commits, never publishes, never sends.

set -euo pipefail

REPO="$HOME/Development/id8/shipped"
LOG_DIR="$HOME/Library/Logs/shipped"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/daily-watchdog.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] $*" >> "$LOG"; }

notify() { # title, message
  osascript -e "display notification \"$2\" with title \"$1\" sound name \"Basso\"" \
    >/dev/null 2>&1 || log "notification failed"
}

cd "$REPO" || { log "FAIL: repo not found at $REPO"; exit 1; }

if ! git fetch origin daily-pages --quiet 2>/dev/null; then
  log "FAIL: could not fetch origin/daily-pages"
  notify "Shipped. watchdog blind" "Cannot reach origin/daily-pages. The daily is unverified tonight."
  exit 1
fi

TODAY="$(TZ=America/New_York date +%F)"
STEMS="$(git ls-tree -r --name-only origin/daily-pages anthropic-daily/ \
  | sed -n 's#.*/\(20[0-9-]*\)\.html#\1#p' | sort)"

# A stem dated later than today is the 2026-08-05 signature: the routine used a
# UTC clock. It is always wrong, and left alone it also poisons the distributor's
# high-water mark, so it costs tomorrow's edition too.
FUTURE="$(echo "$STEMS" | awk -v t="$TODAY" '$0 > t')"

if [ -n "$FUTURE" ]; then
  ONE="$(echo "$FUTURE" | tr '\n' ' ' | sed 's/ $//')"
  log "ANOMALY: future-dated page(s) on daily-pages: $ONE (today ET is $TODAY)"
  notify "Shipped. published a future date" "$ONE on daily-pages, today is $TODAY. Restamp it."
fi

if echo "$STEMS" | grep -qx "$TODAY"; then
  log "OK: $TODAY present on daily-pages"
  exit 0
fi

if [ -n "$FUTURE" ]; then
  REASON="A future-dated page exists, so the routine mis-derived its date."
else
  REASON="The 21:00 ET routine did not publish."
fi

log "MISSING: no $TODAY page on daily-pages. $REASON"
notify "Shipped. did not ship" "No $TODAY daily. $REASON"
exit 1
