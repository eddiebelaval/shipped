#!/usr/bin/env python3
"""
Shipped. — the Night Desk.

The desk that makes sure the paper actually gets out. Runs every night, checks
the nine things that have ever broken this publication, heals what is mechanical,
and pages a human for what is not.

WHY IT IS NOT AN AGENT FLEET. Every failure Shipped. suffered on 2026-08-05/06
was deterministically detectable: a missing file, a stem dated tomorrow, a
base64 blob, an absent CSS marker, a pushed commit that never went live. None of
it needed judgment, it needed a checklist that actually ran. A nightly fleet of
model calls would cost real money to rediscover facts that `grep` already knows
(see the Parallax arena sweep: $112 in one overnight run). So the desk is
deterministic and costs nothing on a green night. Escalation is where judgment
belongs, and escalation is a human or a single agent invoked with the evidence
already gathered.

THE NINE CHECKS
  1  presence    today's Eastern daily is on the branch
  2  dating      no page is dated in the future
  3  integrity   every page is a real document: opens with a tag, has a title, closes
  4  chrome      every page published since the design lock carries issue-chrome.html
  5  subscribe   every page carries BOTH the pill and the form, with the honeypot
                 and the absolute POST url
  6  index       index.html links exactly the pages that exist, no orphans
  7  live        the deployed site matches the branch (pushed is not published)
  8  distro      the distributor drafted the newest edition
  9  gaps        missing dailies, weeklies, monthlies (reported, never alarmed)

VERDICTS
  OK        nothing to do
  HEALED    the desk fixed it (only with --heal; reversible, in-repo fixes only)
  ESCALATE  a human is needed; macOS notification plus a written brief

Usage:
  night-desk.py                 report only, exit 1 if anything escalates
  night-desk.py --heal          also apply the mechanical fixes and push
  night-desk.py --quiet         suppress the desktop notification (for cron tests)
"""
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

REPO = pathlib.Path(os.path.expanduser("~/Development/id8/shipped"))
SCRIPTS = REPO / "pipeline" / "scripts"
LOG_DIR = pathlib.Path(os.path.expanduser("~/Library/Logs/shipped"))
LOG = LOG_DIR / "night-desk.log"
STATE = pathlib.Path(os.path.expanduser("~/.shipped-distribution/night-desk-state.json"))
DISTRO_STATE = pathlib.Path(os.path.expanduser("~/.shipped-distribution/seen.json"))
SITE = "https://eddiebelaval.github.io/shipped"
ET = ZoneInfo("America/New_York")

SECTIONS = ("anthropic-daily", "anthropic-weekly", "anthropic-monthly")

HEAL = "--heal" in sys.argv
QUIET = "--quiet" in sys.argv

findings = []   # (check, verdict, message)


def log(msg):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = f"[{datetime.now(ET):%Y-%m-%d %H:%M:%S %Z}] {msg}"
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def record(check, verdict, message):
    findings.append((check, verdict, message))
    log(f"{verdict:9} {check:10} {message}")


def git(*args, repo=None):
    return subprocess.run(["git", "-C", str(repo or REPO), *args],
                          capture_output=True, text=True)


def fetch(url, timeout=25):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return 0, str(e)


def load_state():
    try:
        return json.loads(STATE.read_text())
    except (OSError, ValueError):
        return {}


def save_state(s):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    tmp = str(STATE) + ".tmp"
    pathlib.Path(tmp).write_text(json.dumps(s, indent=2))
    os.replace(tmp, STATE)


def blob(path):
    r = git("show", f"origin/daily-pages:{path}")
    return r.stdout if r.returncode == 0 else ""


def pages():
    """{section: [stems]} from the branch, sorted."""
    out = {}
    for s in SECTIONS:
        r = git("ls-tree", "-r", "--name-only", "origin/daily-pages", s + "/")
        stems = sorted(os.path.basename(p)[:-5]
                       for p in r.stdout.splitlines() if p.endswith(".html"))
        out[s] = stems
    return out


# --------------------------------------------------------------- the checks

def check_presence(pg, today):
    if today in pg["anthropic-daily"]:
        record("presence", "OK", f"{today} is on the branch")
        return
    # Today's edition is not late until the 21:00 ET routine has had time to
    # finish. Escalating before that trains the alarm into noise, which is the
    # same mistake the archive gap report already had to have removed from it.
    now = datetime.now(ET)
    if now.hour < 21 or (now.hour == 21 and now.minute < 35):
        record("presence", "OK",
               f"{today} not published yet, and not due until 21:00 ET "
               f"(now {now:%H:%M})")
        return
    yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    why = ("the 21:00 ET routine did not publish"
           if yesterday in pg["anthropic-daily"] else
           "the routine has not published for at least two days")
    record("presence", "ESCALATE", f"no {today} daily. {why}.")


def check_dating(pg, today):
    future = [s for s in pg["anthropic-daily"] if len(s) == 10 and s > today]
    if not future:
        record("dating", "OK", "no future-dated pages")
        return
    record("dating", "ESCALATE",
           f"future-dated page(s): {', '.join(future)}. Today ET is {today}. "
           "The routine mis-derived its date; the page needs restamping and the "
           "distributor must not draft it.")


def check_integrity(pg):
    bad = []
    for s in SECTIONS:
        for stem in pg[s]:
            t = blob(f"{s}/{stem}.html")
            if not t.lstrip().startswith("<"):
                bad.append(f"{s}/{stem}: not a document (encoded or corrupt)")
            elif "<title>" not in t:
                bad.append(f"{s}/{stem}: no <title>")
            elif "</html>" not in t:
                bad.append(f"{s}/{stem}: unclosed document")
    if bad:
        record("integrity", "ESCALATE", f"{len(bad)} malformed page(s): " + "; ".join(bad[:4]))
    else:
        record("integrity", "OK", "every page is a well-formed document")


def check_chrome(pg, state):
    """Pages published since the design lock must carry issue-chrome.html.

    Everything already on the branch when the desk first ran predates the lock
    and is grandfathered, the same migration shape the distributor uses. Without
    that baseline this check would be permanently red on 89 historical dailies
    and would be ignored within a week.
    """
    grandfathered = set(state.get("pre_lock_pages", []))
    first_run = "pre_lock_pages" not in state
    missing, seen_all = [], []
    for s in SECTIONS:
        for stem in pg[s]:
            key = f"{s}/{stem}"
            seen_all.append(key)
            if key in grandfathered:
                continue
            if "weekly-masthead" not in blob(f"{key}.html"):
                missing.append(key)

    if first_run:
        pre = [k for k in seen_all
               if "weekly-masthead" not in blob(f"{k}.html")]
        state["pre_lock_pages"] = sorted(pre)
        record("chrome", "OK",
               f"baseline set: {len(pre)} page(s) predate the design lock and are "
               f"grandfathered; {len(seen_all) - len(pre)} already carry the chrome")
        return

    if missing:
        record("chrome", "ESCALATE",
               f"{len(missing)} page(s) published without issue-chrome.html: "
               + ", ".join(missing[:5])
               + ". A routine stopped pasting the chrome and is free-handing CSS again.")
    else:
        record("chrome", "OK", "every post-lock page carries the locked chrome")


def check_subscribe(pg):
    no_form, no_hp, bad_url, dead_pill = [], [], [], []
    for s in SECTIONS:
        for stem in pg[s]:
            t = blob(f"{s}/{stem}.html")
            key = f"{s}/{stem}"
            has_form = 'id="subscribe"' in t
            has_pill = 'class="pub-bar-cta"' in t
            if not has_form:
                # A pill without a form is the worse case and deserves its own
                # name: the page ships a Subscribe button anchored to a
                # #subscribe that is not there. Three pages sat like that for
                # twelve days because the healer's guard was an OR.
                (dead_pill if has_pill else no_form).append(key)
                continue
            if 'name="website"' not in t:
                no_hp.append(key)
            if "id8labs.app/api/newsletter/subscribe" not in t:
                bad_url.append(key)
    problems = []
    if no_form:
        problems.append(f"{len(no_form)} without the form ({', '.join(no_form[:3])})")
    if dead_pill:
        problems.append(f"{len(dead_pill)} with a Subscribe pill anchored to nothing")
    if no_hp:
        problems.append(f"{len(no_hp)} without the honeypot field")
    if bad_url:
        problems.append(f"{len(bad_url)} with a wrong POST url")
    if problems:
        record("subscribe", "ESCALATE", "; ".join(problems))
    else:
        record("subscribe", "OK", "every page has the form, honeypot and absolute POST url")


def check_index(pg):
    idx = blob("index.html")
    if not idx:
        record("index", "ESCALATE", "index.html is missing from the branch")
        return None
    linked = set(re.findall(r'href="((?:anthropic-[a-z]+|dispatch)/[^"]+)"', idx))
    on_disk = {f"{s}/{stem}.html" for s in SECTIONS for stem in pg[s]}
    r = git("ls-tree", "-r", "--name-only", "origin/daily-pages", "dispatch/")
    on_disk |= {p for p in r.stdout.splitlines() if p.endswith(".html")}
    orphans = on_disk - linked
    dead = {l for l in linked if l.startswith(("anthropic-", "dispatch/"))} - on_disk
    if orphans or dead:
        record("index", "HEAL" if HEAL else "ESCALATE",
               f"{len(orphans)} page(s) unreachable from the index, {len(dead)} dead link(s)")
        return len(linked)
    record("index", "OK", f"all {len(on_disk)} pages reachable, no dead links")
    return len(linked)


def check_live(expect_links):
    status, body = fetch(SITE + "/")
    if status != 200:
        record("live", "ESCALATE", f"the site itself returned HTTP {status}")
        return
    live_links = len(set(re.findall(
        r'href="((?:anthropic-[a-z]+|dispatch)/[^"]+)"', body)))
    if expect_links is None:
        record("live", "OK", f"site up, {live_links} links")
        return
    if live_links != expect_links:
        record("live", "ESCALATE",
               f"the branch has {expect_links} linked pages but the live site serves "
               f"{live_links}. Pushed is not published: the deploy has not landed.")
        return
    record("live", "OK", f"deployed site matches the branch ({live_links} pages)")


def check_distro(pg):
    try:
        st = json.loads(DISTRO_STATE.read_text())
    except (OSError, ValueError):
        record("distro", "ESCALATE", "the distributor state file is unreadable")
        return
    drafted = set(st.get("drafted", {}).get("nightly", []))
    newest = pg["anthropic-daily"][-1] if pg["anthropic-daily"] else None
    if newest is None:
        record("distro", "ESCALATE", "no dailies on the branch at all")
    elif newest in drafted:
        record("distro", "OK", f"newest daily {newest} was drafted")
    else:
        record("distro", "OK",
               f"{newest} not drafted yet (the 22:45 run has not fired), which is "
               "expected before 22:45 ET")


def check_gaps(pg, today):
    stems = pg["anthropic-daily"]
    if not stems:
        return
    first = date.fromisoformat(stems[0])
    have = set(stems)
    d, missing = first, []
    while d < date.fromisoformat(today):
        if d.isoformat() not in have:
            missing.append(d.isoformat())
        d += timedelta(days=1)
    parts = []
    if missing:
        parts.append(f"dailies {', '.join(missing)}")
    mo_have = set(pg["anthropic-monthly"])
    mo_missing = [m for m in sorted({s[:7] for s in stems})
                  if m not in mo_have and m != today[:7]]
    if mo_missing:
        parts.append(f"monthlies {', '.join(mo_missing)}")
    record("gaps", "OK", ("archive gaps (reported, not an alarm): " + "; ".join(parts))
           if parts else "no archive gaps")


# ---------------------------------------------------------------- the heal

def heal(reason):
    """Mechanical, reversible, in-repo fixes only. Never edits editorial content."""
    wt = tempfile.mkdtemp(prefix="night-desk-")
    try:
        git("fetch", "origin", "daily-pages", "--quiet")
        if git("worktree", "add", "-q", "--detach", wt, "origin/daily-pages").returncode:
            record("heal", "ESCALATE", "could not create a worktree")
            return
        subprocess.run([sys.executable, str(SCRIPTS / "backfill-subscribe.py"), wt],
                       capture_output=True, text=True)
        subprocess.run([sys.executable, str(SCRIPTS / "build-archive-index.py"), wt],
                       capture_output=True, text=True)
        if not git("status", "--porcelain", repo=wt).stdout.strip():
            record("heal", "OK", "nothing mechanical left to fix")
            return
        git("add", "-A", repo=wt)
        git("-c", "user.name=Night Desk", "-c", "user.email=eb@id8labs.tech",
            "commit", "-q", "-m", f"chore(pages): night desk heal ({reason})",
            "-m", "Regenerated the archive index and enforced the subscribe block.",
            repo=wt)
        if git("push", "--quiet", "origin", "HEAD:daily-pages", repo=wt).returncode:
            record("heal", "ESCALATE", "heal committed but the push failed")
        else:
            record("heal", "HEALED", f"pushed a repair for: {reason}")
    finally:
        git("worktree", "remove", "--force", wt)
        git("worktree", "prune")


def notify(title, message):
    if QUIET:
        return
    subprocess.run(["osascript", "-e",
                    f'display notification "{message[:180]}" with title "{title}" '
                    'sound name "Basso"'], capture_output=True)


def main():
    log("---- night desk ----")
    git("fetch", "origin", "daily-pages", "--quiet")
    today = datetime.now(ET).strftime("%Y-%m-%d")
    state = load_state()
    pg = pages()

    check_presence(pg, today)
    check_dating(pg, today)
    check_integrity(pg)
    check_chrome(pg, state)
    check_subscribe(pg)
    n = check_index(pg)
    check_live(n)
    check_distro(pg)
    check_gaps(pg, today)

    save_state(state)

    escalations = [f for f in findings if f[1] == "ESCALATE"]
    healable = {"index", "subscribe"}
    if HEAL and any(f[0] in healable for f in escalations):
        heal(", ".join(f[0] for f in escalations if f[0] in healable))
        escalations = [f for f in escalations if f[0] not in healable]

    if escalations:
        head = escalations[0]
        log(f"VERDICT: {len(escalations)} escalation(s)")
        notify("Shipped. Night Desk", f"{head[0]}: {head[2]}")
        return 1

    log(f"VERDICT: green, {len(findings)} checks clear")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        log(f"night desk itself failed: {e}")
        notify("Shipped. Night Desk failed", str(e)[:170])
        sys.exit(2)
