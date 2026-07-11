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
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

REPO = os.path.expanduser("~/Development/id8/shipped")
# Self-serve subscribers live in a PRIVATE repo (written by the subscribe
# endpoint); the public pipeline/recipients.json keeps config + manual entries.
# Both are merged in read_recipients(). Fetched with Eddie's local git auth.
SUBSCRIBERS_REPO = "eddiebelaval/shipped-subscribers"
SUBSCRIBERS_REF = "refs/remotes/shipped-subscribers/main"
HOME = os.path.expanduser("~/.shipped-distribution")
STATE_PATH = os.path.join(HOME, "seen.json")
APPLESCRIPT = os.path.join(HOME, "shipped-draft.applescript")
LOG_PATH = os.path.join(HOME, "distribute.log")
BASE_URL = "https://eddiebelaval.github.io/shipped"

# cadence -> (daily-pages subdir, subject prefix)
CADENCES = {
    "nightly": ("anthropic-daily", "Shipped. Daily"),
    "weekly": ("anthropic-weekly", "Shipped. Weekly"),
    "monthly": ("anthropic-monthly", "Shipped. Monthly"),
}


def log(msg):
    line = f"{datetime.now(timezone.utc).isoformat()}  {msg}"
    print(line)
    try:
        with open(LOG_PATH, "a") as f:
            f.write(line + "\n")
    except OSError:
        pass


def git(*args):
    return subprocess.run(
        ["git", "-C", REPO, *args],
        capture_output=True, text=True
    )


def load_state():
    try:
        with open(STATE_PATH) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_state(state):
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def read_json_at(ref_path):
    r = git("show", ref_path)
    if r.returncode != 0:
        log(f"{ref_path} not readable: {r.stderr.strip()}")
        return None
    try:
        return json.loads(r.stdout)
    except ValueError as e:
        log(f"{ref_path} parse error: {e}")
        return None


def subscribers_url():
    """Match the transport (SSH vs HTTPS) of origin so existing auth works."""
    r = git("remote", "get-url", "origin")
    origin = r.stdout.strip() if r.returncode == 0 else ""
    if origin.startswith("git@"):
        return f"git@github.com:{SUBSCRIBERS_REPO}.git"
    return f"https://github.com/{SUBSCRIBERS_REPO}.git"


def read_recipients():
    """Public file (config + manual entries) merged with the private
    self-serve list. Either source alone is enough; private wins on
    conflicts, dedupe is by email."""
    base = read_json_at("origin/main:pipeline/recipients.json")

    priv = None
    r = git("fetch", subscribers_url(), f"+main:{SUBSCRIBERS_REF}", "--quiet")
    if r.returncode != 0:
        log(f"private subscriber list not fetchable (using public only): {r.stderr.strip()}")
    else:
        priv = read_json_at(f"{SUBSCRIBERS_REF}:recipients.json")

    if base is None and priv is None:
        return None
    if priv is None:
        return base

    merged = dict(base or {})
    for key in ("send_mode", "from"):
        if priv.get(key):
            merged[key] = priv[key]
    by_email = {}
    for rec in (base or {}).get("recipients", []) + priv.get("recipients", []):
        email = (rec.get("email") or "").strip().lower()
        if email:
            by_email[email] = rec
    merged["recipients"] = list(by_email.values())
    return merged


def latest_stem(subdir):
    """Newest YYYY-* .html stem in a daily-pages subdir, or None."""
    r = git("ls-tree", "-r", "--name-only", "origin/daily-pages", subdir + "/")
    if r.returncode != 0:
        return None
    stems = []
    for path in r.stdout.splitlines():
        name = os.path.basename(path)
        if name.endswith(".html"):
            stems.append(name[:-5])
    return sorted(stems)[-1] if stems else None


def make_draft(sender, subject, body, bcc_list):
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

    state = load_state()
    drafted_any = False

    for cadence, (subdir, prefix) in CADENCES.items():
        stem = latest_stem(subdir)
        if not stem:
            continue
        if state.get(cadence) == stem:
            continue  # already drafted this page
        who = [r["email"] for r in recipients
               if cadence in r.get("cadences", []) and r.get("email")]
        if not who:
            # no recipients for this cadence; mark seen so we don't re-check forever
            state[cadence] = stem
            continue
        url = f"{BASE_URL}/{subdir}/{stem}.html"
        subject = pretty_subject(prefix, cadence, stem)
        body = (
            f"The latest {prefix} is up.\n\n"
            f"{url}\n\n"
            f"You are on the Shipped. reading list. Reply to this message to be removed.\n"
        )
        if make_draft(sender, subject, body, who):
            log(f"drafted {cadence} {stem} to {len(who)} recipient(s): {subject}")
            state[cadence] = stem
            drafted_any = True
        else:
            log(f"FAILED to draft {cadence} {stem}; will retry next run")

    save_state(state)
    if not drafted_any:
        log("no new pages to draft")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # never crash the launchd job
        log(f"unhandled error: {e}")
        sys.exit(1)
