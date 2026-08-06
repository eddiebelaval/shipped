#!/usr/bin/env python3
"""
Shipped. local distribution job.

The cloud release routines (Nightly/Weekly/Monthly) publish pages to the
`daily-pages` branch but cannot reach Gmail from the headless cloud environment.
This job runs on Eddie's Mac, where Mail.app (eb@id8labs.tech) works, and stages
a Mail.app DRAFT for any freshly published page to the matching recipients.

Draft only. Never sends. State-tracked so it never double-drafts the same page.

Schedule: launchd com.id8labs.shipped-distribute, daily ~22:45 ET (after the
nightly 21:00 and weekly Fri 22:00 routines publish; the monthly 1st-10:00 page
is picked up that same evening).

This file is THE source of truth. ~/.shipped-distribution/distribute-local.py is
a symlink to it. Before 2026-08-05 the two were separate copies that had already
diverged, so edits made here were dead code and launchd kept running the other one.

--- 2026-08-05: two bugs this rewrite exists to kill ---

1. HIGH-WATER-MARK SKIP. The old version tracked one stem per cadence and only
   ever looked at `sorted(stems)[-1]`. Any page that appeared out of order, or
   was backfilled below the mark, was skipped permanently and silently. Worse:
   on 2026-08-05 the nightly routine published a page dated 2026-08-06 (it took
   its stem from a UTC clock at 21:25 ET). Under the old logic that future stem
   would have become the high-water mark, so the REAL 2026-08-06 edition the
   next night would have compared equal and never been drafted. One wrong date
   would have cost two editions. State is now a SET of drafted stems.

2. SILENT ABSENCE. When the routine did not run at all (2026-07-26, 2026-07-30)
   the job logged "no new pages to draft" and exited 0. That is a source going
   blind and reporting green. It now PAGES: a macOS notification plus a MISSING
   line in the log when today's Eastern daily is not on the branch.

A future-dated nightly stem is never drafted. It is reported as an anomaly and
left undrafted, so the tripwire keeps firing until someone restamps the page.
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

REPO = os.path.expanduser("~/Development/id8/shipped")
HOME = os.path.expanduser("~/.shipped-distribution")
STATE_PATH = os.path.join(HOME, "seen.json")
LOCAL_RECIPIENTS = os.path.join(HOME, "recipients.json")
APPLESCRIPT = os.path.join(HOME, "shipped-draft.applescript")
LOG_PATH = os.path.join(HOME, "distribute.log")
BASE_URL = "https://eddiebelaval.github.io/shipped"

ET = ZoneInfo("America/New_York")

# A bad state file must not be able to spawn a hundred drafts. Anything over the
# cap is deferred to the next run, never dropped, and always named in the log.
MAX_DRAFTS_PER_RUN = 3

# cadence -> (daily-pages subdir, subject prefix)
CADENCES = {
    "nightly": ("anthropic-daily", "Shipped. Daily"),
    "weekly": ("anthropic-weekly", "Shipped. Weekly"),
    "monthly": ("anthropic-monthly", "Shipped. Monthly"),
}

DRY_RUN = "--dry-run" in sys.argv


def log(msg):
    line = f"{datetime.now(timezone.utc).isoformat()}  {'[dry-run] ' if DRY_RUN else ''}{msg}"
    print(line)
    try:
        with open(LOG_PATH, "a") as f:
            f.write(line + "\n")
    except OSError:
        pass


def page(title, message):
    """Surface a failure where Eddie will actually see it, not just in a log."""
    log(f"PAGE: {title}: {message}")
    if DRY_RUN:
        return
    try:
        subprocess.run(
            ["osascript", "-e",
             f'display notification "{message}" with title "{title}" sound name "Basso"'],
            capture_output=True, text=True, timeout=20,
        )
    except (OSError, subprocess.SubprocessError) as e:
        log(f"notification failed: {e}")


def git(*args):
    return subprocess.run(
        ["git", "-C", REPO, *args],
        capture_output=True, text=True
    )


def load_state():
    """Return {cadence: set(stems)}, migrating the pre-2026-08-05 format.

    Old format was {cadence: "<highest stem drafted>"}. Migrating it to a set
    means seeding with every stem at or below that mark, so the archive is not
    re-blasted on first run under the new logic.
    """
    try:
        with open(STATE_PATH) as f:
            raw = json.load(f)
    except (OSError, ValueError):
        raw = {}

    if raw.get("version") == 2:
        return {c: set(raw.get("drafted", {}).get(c, [])) for c in CADENCES}

    drafted = {}
    for cadence, (subdir, _) in CADENCES.items():
        mark = raw.get(cadence)
        if isinstance(mark, str) and mark:
            drafted[cadence] = {s for s in all_stems(subdir) if s <= mark}
            log(f"migrated {cadence} state: high-water {mark} -> "
                f"{len(drafted[cadence])} stem(s) marked drafted")
        else:
            drafted[cadence] = set()
    return drafted


def save_state(drafted):
    if DRY_RUN:
        return
    payload = {"version": 2, "drafted": {c: sorted(s) for c, s in drafted.items()}}
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(payload, f, indent=2)
    os.replace(tmp, STATE_PATH)


def read_recipients():
    # Prefer the locally-synced list (Supabase -> sync-recipients.mjs, run by
    # com.id8labs.shipped-recipients-sync just before this job). Fall back to
    # git origin/main for backward compatibility if the local file is absent.
    if os.path.exists(LOCAL_RECIPIENTS):
        try:
            with open(LOCAL_RECIPIENTS) as f:
                return json.load(f)
        except (OSError, ValueError) as e:
            log(f"local recipients.json unreadable ({e}); falling back to git")
    r = git("show", "origin/main:pipeline/recipients.json")
    if r.returncode != 0:
        log(f"recipients.json not readable on origin/main: {r.stderr.strip()}")
        return None
    try:
        return json.loads(r.stdout)
    except ValueError as e:
        log(f"recipients.json parse error: {e}")
        return None


def all_stems(subdir):
    """Every YYYY-* .html stem in a daily-pages subdir, sorted ascending."""
    r = git("ls-tree", "-r", "--name-only", "origin/daily-pages", subdir + "/")
    if r.returncode != 0:
        log(f"cannot list {subdir} on origin/daily-pages: {r.stderr.strip()}")
        return []
    stems = []
    for path in r.stdout.splitlines():
        name = os.path.basename(path)
        if name.endswith(".html"):
            stems.append(name[:-5])
    return sorted(stems)


def make_draft(sender, subject, body, bcc_list):
    if DRY_RUN:
        log(f"would draft: {subject} -> {len(bcc_list)} recipient(s)")
        return True
    bcc = ",".join(bcc_list)
    r = subprocess.run(
        ["osascript", APPLESCRIPT, sender, subject, body, bcc],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        log(f"osascript failed: {r.stderr.strip()}")
        return False
    return True


def pretty_subject(prefix, cadence, stem):
    # stem is YYYY-MM-DD (nightly), YYYY-WW (weekly), YYYY-MM (monthly)
    try:
        if cadence == "nightly":
            d = datetime.strptime(stem, "%Y-%m-%d")
            return f"{prefix}, {d.strftime('%B %d, %Y')}"
        if cadence == "weekly":
            return f"{prefix}, Week {stem}"
        if cadence == "monthly":
            d = datetime.strptime(stem, "%Y-%m")
            return f"{prefix}, {d.strftime('%B %Y')}"
    except ValueError:
        pass
    return f"{prefix}, {stem}"


def audit_nightly(stems):
    """Absence and future-dating are both anomalies. Neither may pass quietly.

    Returns the set of stems that must NOT be drafted (future-dated ones).
    """
    today = datetime.now(ET).strftime("%Y-%m-%d")
    present = set(stems)

    future = {s for s in stems if len(s) == 10 and s > today}
    if future:
        page("Shipped. daily",
             f"Future-dated page on daily-pages: {', '.join(sorted(future))}. "
             f"Today ET is {today}. Not drafting it.")

    if today not in present:
        yesterday = (datetime.now(ET) - timedelta(days=1)).strftime("%Y-%m-%d")
        detail = f"No {today} page on daily-pages."
        if future:
            detail += " A future-dated page exists, so the routine likely mis-derived its date."
        elif yesterday in present:
            detail += " The 21:00 ET routine did not publish tonight."
        page("Shipped. did not ship", detail)

    return future


def main():
    # fetch without touching the working tree / current branch
    git("fetch", "origin", "daily-pages", "main", "--quiet")

    recips = read_recipients()
    if recips is None:
        log("no recipients config; exiting")
        return
    mode = recips.get("send_mode", "draft")
    if mode == "off":
        log("send_mode=off; nothing to do")
        return
    sender = recips.get("from", "eb@id8labs.tech")
    recipients = recips.get("recipients", [])

    drafted = load_state()
    drafted_any = False

    for cadence, (subdir, prefix) in CADENCES.items():
        stems = all_stems(subdir)
        if not stems:
            continue

        blocked = audit_nightly(stems) if cadence == "nightly" else set()

        who = [r["email"] for r in recipients
               if cadence in r.get("cadences", []) and r.get("email")]

        pending = [s for s in stems if s not in drafted[cadence] and s not in blocked]
        if not pending:
            continue

        if not who:
            # no recipients for this cadence; mark seen so we don't re-check forever
            drafted[cadence].update(pending)
            continue

        if len(pending) > MAX_DRAFTS_PER_RUN:
            deferred = pending[:-MAX_DRAFTS_PER_RUN]
            pending = pending[-MAX_DRAFTS_PER_RUN:]
            log(f"{cadence}: {len(deferred)} page(s) over the per-run cap, deferred to "
                f"the next run (not dropped): {', '.join(deferred)}")

        for stem in pending:
            url = f"{BASE_URL}/{subdir}/{stem}.html"
            subject = pretty_subject(prefix, cadence, stem)
            body = (
                f"The latest {prefix} is up.\n\n"
                f"{url}\n\n"
                f"You are on the Shipped. reading list. Reply to this message to be removed.\n"
            )
            if make_draft(sender, subject, body, who):
                log(f"drafted {cadence} {stem} to {len(who)} recipient(s): {subject}")
                drafted[cadence].add(stem)
                drafted_any = True
            else:
                log(f"FAILED to draft {cadence} {stem}; will retry next run")

    save_state(drafted)
    if not drafted_any:
        log("no new pages to draft")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # never crash the launchd job
        log(f"unhandled error: {e}")
        page("Shipped. distribution failed", str(e)[:180])
        sys.exit(1)
