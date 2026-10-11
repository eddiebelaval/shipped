#!/bin/bash
# Edition Desk launcher (launchd, every 30 minutes).
# The desk runs from a clean worktree pinned to the PUSHED origin/main, so what runs
# unattended is what was reviewed and pushed, never the dirty main checkout.
# Shared state (content/editions, content/image-ledger.json, ops alerts) stays in the main checkout.
set -u
MAIN="$HOME/Development/id8/shipped"
WT="$HOME/Development/.worktrees/shipped/edition-desk"
[ -e "$MAIN/ops/EDITION-DESK-PAUSED" ] && { echo "paused"; exit 0; }
if [ ! -e "$WT/.git" ]; then
  mkdir -p "$(dirname "$WT")"
  git -C "$MAIN" worktree add -q --detach "$WT" origin/main || exit 1
fi
git -C "$WT" fetch -q origin main || exit 1
git -C "$WT" checkout -q -f --detach origin/main || exit 1
git -C "$WT" reset -q --hard origin/main || exit 1
git -C "$WT" clean -qfd || exit 1   # nothing unreviewed ever runs: the worktree is exactly origin/main
if [ ! -d "$WT/pipeline/node_modules" ]; then
  ln -s "$MAIN/pipeline/node_modules" "$WT/pipeline/node_modules"
fi
export SHIPPED_CONTENT="$MAIN/content" SHIPPED_OPS="$MAIN/ops"
exec /usr/bin/python3 "$WT/pipeline/scripts/edition-desk.py" run
