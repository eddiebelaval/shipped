#!/usr/bin/env python3
"""
Shipped. — distribution receipt.

"Published to the web" and "drafted for the list" are two different things: the
release routines stage each edition as a Gmail draft (never auto-sent, that is
Eddie's gate), and a draft that silently failed to stage would leave the paper
on the web but off the mailing list with nothing to notice. The mailbox is not
git-visible, and scheduled routines in this org cannot reach Gmail, so the draft
cannot be checked after the fact from a cron job.

This drops a durable, git-visible trace instead: after a release routine stages
the draft, it calls this to write distribution/<stem>.json to the daily-pages
branch. The Night Desk then verifies the receipt deterministically, no mailbox
access required. The receipt records only that a draft was staged, never any
recipient address or message body.

Usage:
  record-distribution.py <stem> <cadence>
    stem     the edition stem, e.g. 2026-08-14 (daily) or 2026-33 (weekly)
    cadence  nightly | weekly | monthly

It fetches daily-pages, writes the receipt in a detached worktree, commits, and
pushes to daily-pages only. It never touches main or editorial content. Idempotent:
re-running for the same stem overwrites the receipt with a fresh timestamp.
"""
import json
import os
import pathlib
import subprocess
import sys
import tempfile
from datetime import datetime
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")


def repo_root():
    env = os.environ.get("SHIPPED_REPO")
    if env:
        return env
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else os.getcwd()


REPO = repo_root()


def git(*args, repo=REPO):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True)


def main():
    if len(sys.argv) != 3 or sys.argv[2] not in ("nightly", "weekly", "monthly"):
        print("usage: record-distribution.py <stem> <nightly|weekly|monthly>",
              file=sys.stderr)
        return 2
    stem, cadence = sys.argv[1], sys.argv[2]

    git("fetch", "origin", "daily-pages", "--quiet")
    wt = tempfile.mkdtemp(prefix="distro-receipt-")
    try:
        if git("worktree", "add", "-q", "--detach", wt, "origin/daily-pages").returncode:
            print("could not create a worktree", file=sys.stderr)
            return 1
        dist = pathlib.Path(wt) / "distribution"
        dist.mkdir(exist_ok=True)
        receipt = {
            "stem": stem,
            "cadence": cadence,
            "drafted": True,
            "drafted_at": datetime.now(ET).isoformat(),
        }
        (dist / f"{stem}.json").write_text(json.dumps(receipt, indent=2) + "\n")
        if not git("status", "--porcelain", repo=wt).stdout.strip():
            print(f"receipt for {stem} already current, nothing to push")
            return 0
        git("add", "distribution", repo=wt)
        git("-c", "user.name=Shipped Distributor", "-c", "user.email=eb@id8labs.tech",
            "commit", "-q", "-m", f"chore(distro): receipt for {cadence} {stem}", repo=wt)
        if git("push", "--quiet", "origin", "HEAD:daily-pages", repo=wt).returncode:
            print("receipt committed but the push failed", file=sys.stderr)
            return 1
        print(f"distribution receipt recorded for {cadence} {stem}")
        return 0
    finally:
        git("worktree", "remove", "--force", wt)
        git("worktree", "prune")


if __name__ == "__main__":
    sys.exit(main())
