#!/bin/bash
#
# Shipped. — subscribe-block enforcement sweep.
#
# Three separate cloud routines publish to the daily-pages branch (nightly,
# weekly Fri, monthly 1st), each rendering HTML from its own prompt. Relying on
# all three to paste the subscribe block correctly, forever, is the same bet the
# repo already lost once: see pipeline/DAILY-ROUTINE-PROMPT.md, "the generator
# is the prompt" — instructions that live only in repo files do not reach the
# routines, and instructions that live only in prompts drift apart.
#
# So the block is enforced at the branch instead of at each generator. Every
# published page gets checked; anything missing the form gets it. Deterministic,
# covers all three routines and any future one, and self-heals if a prompt drifts.
#
# The nightly prompt also pastes the block directly (belt), which means the
# common case is this sweep finding nothing to do. This is the braces.
#
# Runs daily at 23:00 via com.id8labs.shipped-ensure-subscribe, after the 21:00
# nightly publish and before the 23:15 manifest refresh.
#
# Usage:
#   ensure-subscribe.sh            patch and push anything missing the block
#   ensure-subscribe.sh --dry-run  report only

set -euo pipefail

SHIPPED="${SHIPPED_ROOT:-/Users/eddiebelaval/Development/id8/shipped}"
LOG_DIR="$HOME/Library/Logs/shipped"
LOG="$LOG_DIR/ensure-subscribe.log"
WT="$(mktemp -d "${TMPDIR:-/tmp}/shipped-dp.XXXXXX")"

DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

mkdir -p "$LOG_DIR"

log() { printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" >> "$LOG"; }

# Always drop the worktree, including on failure — a stale one blocks the next run.
cleanup() {
  cd "$SHIPPED" 2>/dev/null || true
  git worktree remove --force "$WT" >/dev/null 2>&1 || rm -rf "$WT"
  git worktree prune >/dev/null 2>&1 || true
}
trap cleanup EXIT

die() { log "ABORT: $1"; echo "ensure-subscribe: $1" >&2; exit 1; }

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
command -v python3 >/dev/null 2>&1 || die "python3 not found on PATH"
git -C "$SHIPPED" rev-parse --git-dir >/dev/null 2>&1 || die "shipped repo not found at $SHIPPED"

cd "$SHIPPED"

git fetch --quiet origin daily-pages 2>>"$LOG" || die "could not fetch origin/daily-pages"

# Detached worktree: we never need a local branch, and detaching avoids
# colliding with a branch another session may already have checked out.
rm -rf "$WT"
git worktree add -q --detach "$WT" origin/daily-pages 2>>"$LOG" || die "worktree add failed"

if [ "$DRY_RUN" -eq 1 ]; then
  python3 "$SHIPPED/pipeline/scripts/backfill-subscribe.py" "$WT" --dry-run | tee -a "$LOG"
  exit 0
fi

OUT="$(python3 "$SHIPPED/pipeline/scripts/backfill-subscribe.py" "$WT")" || die "backfill failed: $OUT"
log "$OUT"

cd "$WT"
if git diff --quiet; then
  log "no change (every published page already carries the block)"
  exit 0
fi

COUNT="$(git diff --name-only | wc -l | tr -d ' ')"
git add -A
git -c user.name="Shipped. bot" -c user.email="eb@id8labs.tech" \
  commit -q -m "chore(pages): ensure subscribe block on $COUNT published page(s)" \
  -m "Added by ensure-subscribe.sh: a routine published without it." \
  2>>"$LOG" || die "commit failed"

# HEAD is detached at the fetched tip, so this pushes exactly what we patched.
if git push --quiet origin HEAD:daily-pages 2>>"$LOG"; then
  log "pushed: $COUNT page(s) repaired"
else
  die "push failed (branch moved? next run retries)"
fi
