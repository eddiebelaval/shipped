#!/bin/bash
# Edition Desk launcher (launchd every 30 minutes, and the documented way to run the desk by hand).
#   edition-desk-launch.sh [edition-desk.py run args, e.g. --only anthropic-daily/2026-10-10]
# The desk runs from a clean worktree pinned to the PUSHED origin/main, so what runs is what was
# reviewed and pushed, never the dirty main checkout. Shared state (content/editions,
# content/image-ledger.json, ops alerts) stays in the main checkout.
set -u
MAIN="$HOME/Development/id8/shipped"
WT="$HOME/Development/.worktrees/shipped/edition-desk"
LOCK="$MAIN/ops/.edition-desk.lock"
ALERT="$MAIN/ops/EDITION-DESK-LAUNCHER-ALERT.md"  # Night Desk escalates every "- " line in it
FAILS="$MAIN/ops/.edition-desk-launcher-fails"    # one line per consecutive failed tick; a good tick deletes it
FAIL_LIMIT=3                                      # failed ticks in a row (15 min at the 5-minute cadence) before escalating

alert_header() {
  [ -e "$ALERT" ] || printf '# Edition Desk launcher alert (runbook pipeline/EDITION-DESK.md)\n\n' > "$ALERT"
}

# Failure lines describe current state, so they go when the launcher recovers. Other lines (a stale lock
# cleared after a crashed run) are events and stay until someone deletes the file.
drop_failure_lines() {
  [ -e "$ALERT" ] || return 0
  grep -v -- 'launcher failed' "$ALERT" > "$ALERT.tmp"
  mv "$ALERT.tmp" "$ALERT"
  grep -q '^- ' "$ALERT" || rm -f "$ALERT"
}

clear_failures() {
  rm -f "$FAILS"
  drop_failure_lines
}

# One failed tick is logged and retried by the next tick. FAIL_LIMIT in a row escalates, and the alert
# is rewritten (not appended) each tick so a long outage stays one line.
fail() {
  mkdir -p "$MAIN/ops"
  printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M')" "$1" >> "$FAILS"
  n=$(wc -l < "$FAILS" | tr -d ' ')
  if [ "$n" -lt "$FAIL_LIMIT" ]; then
    echo "launcher failed ($n of $FAIL_LIMIT ticks before escalating): $1" >&2
    exit 1
  fi
  since=$(head -1 "$FAILS" | cut -c1-16)
  drop_failure_lines
  alert_header
  printf -- '- ESCALATE %s launcher failed %s ticks in a row since %s: %s\n' "$(date '+%Y-%m-%d %H:%M')" "$n" "$since" "$1" >> "$ALERT"
  [ "$n" -eq "$FAIL_LIMIT" ] && [ -z "${EDITION_DESK_QUIET:-}" ] &&
    osascript -e "display notification \"launcher failed $n ticks in a row: $1\" with title \"Shipped. Edition Desk\"" >/dev/null 2>&1
  exit 1
}

[ -e "$MAIN/ops/EDITION-DESK-PAUSED" ] && { echo "paused"; exit 0; }

# One run at a time: a hand run during a timer run must not reset the worktree under it.
mkdir -p "$MAIN/ops"
if ! mkdir "$LOCK" 2>/dev/null; then
  # A lock older than 2 hours is a crashed run (kill -9, reboot): say so, clear it, carry on.
  if [ -n "$(find "$LOCK" -maxdepth 0 -mmin +120 2>/dev/null)" ]; then
    alert_header
    printf -- '- ESCALATE %s stale lock cleared (a run died holding it)\n' "$(date '+%Y-%m-%d %H:%M')" >> "$ALERT"
    rmdir "$LOCK" && mkdir "$LOCK" || fail "could not clear the stale lock"
  else
    echo "another Edition Desk run holds $LOCK"; exit 0
  fi
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

if [ ! -e "$WT/.git" ]; then
  mkdir -p "$(dirname "$WT")"
  git -C "$MAIN" worktree add -q --detach "$WT" origin/main || fail "could not create the release worktree"
fi
git -C "$WT" fetch -q origin main || fail "git fetch origin main"
git -C "$WT" checkout -q -f --detach origin/main || fail "checkout origin/main"
git -C "$WT" reset -q --hard origin/main || fail "reset to origin/main"
git -C "$WT" clean -qfd || fail "clean the release worktree"
if [ ! -e "$WT/pipeline/node_modules" ]; then
  ln -s "$MAIN/pipeline/node_modules" "$WT/pipeline/node_modules"
fi
export SHIPPED_CONTENT="$MAIN/content" SHIPPED_OPS="$MAIN/ops"
/usr/bin/python3 "$WT/pipeline/scripts/edition-desk.py" run "$@" || fail "edition-desk.py exited $?"
clear_failures
