#!/usr/bin/env bash
#
# Install the Shipped. automation jobs into launchd.
# Run once. Re-running is idempotent.
#
# What gets installed:
#   - com.id8labs.shipped-friday   → Friday 7 AM scraper refresh
#   - com.id8labs.shipped-notify   → Friday 8:55 AM publish-window reminder
#   - com.id8labs.shipped-nightly  → Daily 9 PM dashboard + status notification
#   - com.id8labs.shipped-monthly  → 1st of month 9 AM monthly-issue heartbeat
#
# No job auto-publishes or generates content. The human at git push remains the final gate.

set -euo pipefail

PIPELINE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LAUNCHD_DIR="$HOME/Library/LaunchAgents"
LOG_DIR="$HOME/Library/Logs/shipped"

mkdir -p "$LAUNCHD_DIR"
mkdir -p "$LOG_DIR"

JOBS=("com.id8labs.shipped-friday" "com.id8labs.shipped-notify" "com.id8labs.shipped-nightly" "com.id8labs.shipped-monthly")

echo "Installing Shipped. cron jobs..."

for job in "${JOBS[@]}"; do
  src="$PIPELINE_ROOT/cron/$job.plist"
  dst="$LAUNCHD_DIR/$job.plist"

  if [[ ! -f "$src" ]]; then
    echo "  ✗ Source plist missing: $src"
    exit 1
  fi

  # Unload if already loaded (idempotent)
  if launchctl print "gui/$(id -u)/$job" >/dev/null 2>&1; then
    echo "  · Unloading existing $job"
    launchctl bootout "gui/$(id -u)" "$dst" 2>/dev/null || true
  fi

  # Copy + load
  cp "$src" "$dst"
  launchctl bootstrap "gui/$(id -u)" "$dst"
  echo "  ✓ Installed $job"
done

echo ""
echo "Installed jobs (next run times):"
for job in "${JOBS[@]}"; do
  next=$(launchctl print "gui/$(id -u)/$job" 2>/dev/null | grep -E "next runtime" | head -1 | sed 's/^[[:space:]]*//')
  echo "  · $job — $next"
done

echo ""
echo "Logs: $LOG_DIR"
echo "Manual run for testing:"
echo "  cd $PIPELINE_ROOT && pnpm scrape --days 7"
echo "  bash $PIPELINE_ROOT/scripts/monthly-check.sh   # test the monthly heartbeat"
echo ""
echo "To uninstall:"
echo "  bash $PIPELINE_ROOT/scripts/uninstall-cron.sh"
