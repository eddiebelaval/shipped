#!/usr/bin/env python3
"""
Shipped. — "Did we ship, Shipped?"

The evening sweep. It runs a little after the release routines and asks the one
question that matters that night: did the edition that was due actually go out?

WHY THIS EXISTS, WHEN THE NIGHT DESK ALREADY DOES NINE CHECKS.
The Night Desk (pipeline/scripts/night-desk.py) is the full checklist, but it was
built to run on Eddie's Mac via launchd. The paper is produced in the cloud by
scheduled routines that do not care whether that laptop is awake. So on any night
the Mac is asleep, the watcher that is supposed to notice a miss never runs, and
a green night and a broken night look identical from where a human sits: a quiet
inbox. The only cloud check that survives a closed laptop is the pipeline
health-check, and it runs the NEXT MORNING and only speaks up on failure. Nobody
gets a same-evening answer.

This script is that answer. It is deterministic, cloud-portable (no hard-coded
home path, no macOS APIs), and cheap on a green night. It confirms three things
about every edition that was due by the time it runs:

  presence   the edition is on the daily-pages branch
  dating     its <title> carries tonight's Eastern date, not tomorrow's
  deploy     the GitHub Pages deploy for that commit concluded success
             (pushed is not published)

It prints a one-line verdict and exits 0 when we shipped, 1 when we did not, so a
wrapper (a cron trigger, a CI step, a human at a terminal) can alert on the miss
and stay quiet on the win. It never publishes, never pushes, never sends mail.
It only reads git and, when `gh` is on PATH, the Actions API.

Usage:
  did-we-ship.py            report + verdict, exit 1 if anything did not ship
  did-we-ship.py --json     also emit a machine-readable summary on the last line
  did-we-ship.py --quiet    only print the final verdict line
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
BRANCH = "origin/daily-pages"

JSON = "--json" in sys.argv
QUIET = "--quiet" in sys.argv

# Grace buffers: an edition is not "missing" until its routine has had time to
# run and its Pages deploy has had time to finish. These match the release cron
# times plus render+deploy slack, and keep the alarm from crying wolf.
DAILY_DUE = (21, 35)     # nightly fires 21:00 ET; due by 21:35
WEEKLY_DUE = (22, 30)    # weekly fires Fri 22:00 ET; due by 22:30
MONTHLY_DUE = (10, 45)   # monthly fires 1st 10:00 ET; due by 10:45

findings = []  # (section, stem, ok, detail)


def sh(*args):
    try:
        return subprocess.run(args, capture_output=True, text=True)
    except FileNotFoundError:
        return subprocess.CompletedProcess(args, 127, "", f"{args[0]}: not found")


def repo_root():
    r = sh("git", "rev-parse", "--show-toplevel")
    return r.stdout.strip() if r.returncode == 0 else os.getcwd()


ROOT = repo_root()


def git(*args):
    return sh("git", "-C", ROOT, *args)


def after(now, due):
    """Is `now` (ET) at or past today's due time?"""
    return (now.hour, now.minute) >= due


def branch_has(path):
    return git("cat-file", "-e", f"{BRANCH}:{path}").returncode == 0


def blob(path):
    r = git("show", f"{BRANCH}:{path}")
    return r.stdout if r.returncode == 0 else ""


def last_commit_for(path):
    r = git("log", "-1", "--format=%H", BRANCH, "--", path)
    return r.stdout.strip()


def deploy_ok(sha):
    """Best-effort: did the Pages deploy for this commit succeed?

    Uses `gh` if available (the release routines run where gh works). Returns
    True/False on a definite answer, or None when we cannot tell (gh missing,
    no run yet) so the caller can treat it as unverified rather than a miss.
    """
    if not sha:
        return None
    gh = sh("gh", "run", "list", "--repo", "eddiebelaval/shipped",
            "--branch", "daily-pages", "--commit", sha,
            "--json", "conclusion,status", "--limit", "5")
    if gh.returncode != 0 or not gh.stdout.strip():
        return None
    try:
        runs = json.loads(gh.stdout)
    except ValueError:
        return None
    if not runs:
        return None
    if any(r.get("status") != "completed" for r in runs):
        return None  # still deploying; not a failure yet
    return all(r.get("conclusion") == "success" for r in runs)


def check(section, stem, expect_date_str):
    path = f"{section}/{stem}.html"
    if not branch_has(path):
        findings.append((section, stem, False, "not on the branch"))
        return
    html = blob(path)
    m = re.search(r"<title>([^<]*)</title>", html)
    title = m.group(1) if m else ""
    if expect_date_str and expect_date_str not in title:
        findings.append((section, stem, False,
                         f"title date wrong (title: {title!r})"))
        return
    d = deploy_ok(last_commit_for(path))
    if d is False:
        findings.append((section, stem, False, "on branch but Pages deploy failed"))
    elif d is None:
        findings.append((section, stem, True, "on branch, dated ok; deploy unverified"))
    else:
        findings.append((section, stem, True, "on branch, dated ok, deploy green"))


def main():
    git("fetch", "origin", "daily-pages", "--quiet")
    now = datetime.now(ET)

    # Daily: due every night.
    if after(now, DAILY_DUE):
        stem = now.strftime("%Y-%m-%d")
        mast = now.strftime("%A, %B %d, %Y")   # "Friday, August 14, 2026"
        check("anthropic-daily", stem, mast)
    else:
        if not QUIET:
            print(f"daily not due yet (now {now:%H:%M} ET, due {DAILY_DUE[0]:02d}:{DAILY_DUE[1]:02d})")

    # Weekly: due Friday night. ISO year-week stem, e.g. 2026-33.
    if now.weekday() == 4 and after(now, WEEKLY_DUE):
        check("anthropic-weekly", now.strftime("%G-%V"), None)

    # Monthly: due on the 1st, covering the PREVIOUS month; stem is prev month.
    if now.day == 1 and after(now, MONTHLY_DUE):
        prev = (now.replace(day=1) - timedelta(days=1))
        check("anthropic-monthly", prev.strftime("%Y-%m"), None)

    misses = [f for f in findings if not f[2]]

    if not QUIET:
        if not findings:
            print("nothing due yet this evening; nothing to confirm.")
        for section, stem, ok, detail in findings:
            print(f"  {'ok ' if ok else 'NO '} {section}/{stem}: {detail}")

    when = now.strftime("%Y-%m-%d %H:%M ET")
    if not findings:
        verdict = f"Did we ship, Shipped? — nothing due yet ({when})."
        code = 0
    elif not misses:
        editions = ", ".join(f"{s.split('-')[-1]} {stem}" for s, stem, _, _ in findings)
        verdict = f"Did we ship, Shipped? YES — {editions} ({when})."
        code = 0
    else:
        why = "; ".join(f"{s}/{stem}: {d}" for s, stem, _, d in misses)
        verdict = f"Did we ship, Shipped? NO — {why} ({when})."
        code = 1

    print(verdict)
    if JSON:
        print(json.dumps({
            "shipped": code == 0,
            "checked_at": now.isoformat(),
            "editions": [
                {"section": s, "stem": stem, "ok": ok, "detail": d}
                for s, stem, ok, d in findings
            ],
        }))
    return code


if __name__ == "__main__":
    sys.exit(main())
