#!/usr/bin/env bash
#
# The Command Index — deterministic weekly refresh.
#
# Re-scans the local install (Anthropic built-ins seed + installed plugin
# commands/skills + id8Labs custom commands/skills) and re-renders the page.
# No network, no LLM — safe on a cron. The "new Anthropic built-ins keep
# coming" intelligence lives in the separate /schedule routine that updates
# builtins.json (see refresh-builtins.md); this script just renders whatever
# builtins.json currently says, plus the live local scan.
#
# Wired by com.id8labs.shipped-command-index.plist (weekly, Fri 8:40am ET —
# 20 min before the Shipped ship window).

set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SHIPPED_ROOT="$(cd "$DIR/../../.." && pwd)"          # .../shipped
OUT_LOCAL="$SHIPPED_ROOT/pipeline/output"             # local preview (gitignored)
LOG_DIR="$HOME/Library/Logs/shipped"
LOG="$LOG_DIR/command-index.log"

# Deploy target: the sibling Next.js app Vercel serves, if present.
DEPLOY_DIR="$SHIPPED_ROOT/../id8labs/public/shipped/command-index"

mkdir -p "$OUT_LOCAL" "$LOG_DIR"

ts() { date "+%Y-%m-%d %H:%M:%S"; }
log() { echo "[$(ts)] $*" >> "$LOG"; }

log "command-index refresh starting"

if ! command -v python3 >/dev/null 2>&1; then
  log "RED python3 not found; aborting"
  echo "STATUS: RED — python3 missing"
  exit 1
fi

# Render into the local output dir.
if python3 "$DIR/generate.py" --out "$OUT_LOCAL" >>"$LOG" 2>&1; then
  log "rendered to $OUT_LOCAL/command-index.html"
else
  log "RED generate.py failed"
  echo "STATUS: RED — generation failed (see $LOG)"
  exit 1
fi

# Pull the headline counts back out of the JSON for the status line.
COUNTS="$(python3 - "$OUT_LOCAL/command-index.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
t=d["totals"]
print(f'{t["all"]} total / {t["builtin"]} builtin / {t["plugin"]} plugin / {t["custom"]} custom')
PY
)"
log "counts: $COUNTS"

# Mirror to the deploy dir when the sibling app is checked out next to shipped.
if [ -d "$(dirname "$DEPLOY_DIR")" ]; then
  mkdir -p "$DEPLOY_DIR"
  cp "$OUT_LOCAL/command-index.html" "$DEPLOY_DIR/index.html"
  cp "$OUT_LOCAL/command-index.json" "$DEPLOY_DIR/command-index.json"
  log "deployed to $DEPLOY_DIR (run: human-gated git commit && push from id8labs/)"
else
  log "deploy dir parent missing ($(dirname "$DEPLOY_DIR")); local-only this run"
fi

echo "STATUS: GREEN — $COUNTS"
log "command-index refresh done"
