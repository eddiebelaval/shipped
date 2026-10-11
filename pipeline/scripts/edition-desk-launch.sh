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
ALERT="$MAIN/ops/EDITION-DESK-ALERT.md"

fail() {
  mkdir -p "$MAIN/ops"
  printf '# Edition Desk alert\n\n- ESCALATE launcher failed: %s\n\nRunbook: pipeline/EDITION-DESK.md\n' "$1" > "$ALERT"
  osascript -e "display notification \"launcher failed: $1\" with title \"Shipped. Edition Desk\"" >/dev/null 2>&1
  exit 1
}

[ -e "$MAIN/ops/EDITION-DESK-PAUSED" ] && { echo "paused"; exit 0; }

# One run at a time: a hand run during a timer run must not reset the worktree under it.
mkdir -p "$MAIN/ops"
if ! mkdir "$LOCK" 2>/dev/null; then
  # A lock older than 2 hours is a crashed run (kill -9, reboot): say so, clear it, carry on.
  if [ -n "$(find "$LOCK" -maxdepth 0 -mmin +120 2>/dev/null)" ]; then
    printf '# Edition Desk alert\n\n- ESCALATE stale lock cleared (a run died holding it)\n' > "$ALERT"
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
