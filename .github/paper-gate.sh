#!/usr/bin/env bash
# paper-gate.sh - hold the deploy while any edition page is not in the paper layout.
#
# Why (2026-10-19): two publishers write daily-pages. The cloud routine pushes its
# own page in the OLD layout (~21:17 ET), then the local Edition Desk re-publishes
# it as the paper front a few minutes later. Every push deployed, so the old design
# went live every night until the desk caught up. This gate makes the desk the only
# thing that can put an edition on the site: a push that leaves any edition page
# without the paper marker does not deploy, and the site stays on the last good
# deploy until the desk's paper push arrives (that push deploys everything).
#
# Prints hold=true|false to $GITHUB_OUTPUT when set, and to stdout always.
# Usage: paper-gate.sh [site-root]   (default: current directory)
set -euo pipefail

root="${1:-.}"
marker='<meta name="shipped-layout" content="paper">'
held=0

for section in anthropic-daily anthropic-weekly anthropic-monthly; do
  [ -d "$root/$section" ] || continue
  for f in "$root/$section"/*.html; do
    [ -e "$f" ] || continue
    if ! grep -qF "$marker" "$f"; then
      echo "not paper yet: ${f#"$root"/}"
      held=$((held + 1))
    fi
  done
done

if [ "$held" -gt 0 ]; then
  echo "HOLD: $held edition page(s) not in the paper layout; waiting for the Edition Desk"
  result=true
else
  echo "paper gate: every edition page is paper"
  result=false
fi

echo "hold=$result"
if [ -n "${GITHUB_OUTPUT:-}" ]; then
  echo "hold=$result" >> "$GITHUB_OUTPUT"
fi
