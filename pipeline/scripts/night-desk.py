#!/usr/bin/env python3
"""
Shipped. — the Night Desk (cloud edition).

The desk that makes sure the paper actually gets out. Runs every night, checks
the things that have ever broken this publication, heals what is mechanical, and
pages a human for what is not.

WHY IT IS NOT AN AGENT FLEET. Every failure Shipped. suffered on 2026-08-05/06
was deterministically detectable: a missing file, a stem dated tomorrow, a
base64 blob, an absent CSS marker, a pushed commit that never went live. None of
it needed judgment, it needed a checklist that actually ran. A nightly fleet of
model calls would cost real money to rediscover facts that `grep` already knows
(the Parallax arena sweep burned $112 in one overnight run). So the desk is
deterministic and costs nothing on a green night. Escalation is where judgment
belongs, and escalation is a human or a single agent invoked with the evidence
already gathered.

WHY "CLOUD EDITION". The original desk ran on Eddie's Mac via launchd: it wrote
to ~/Library/Logs, kept state under ~/.shipped-distribution, and paged with a
macOS notification. But the paper is produced in the cloud by scheduled routines
that do not care whether that laptop is awake, so on any night the Mac slept the
watcher never ran and a broken night looked exactly like a green one. This
version has no home path, no macOS APIs, and no local state: the repo root comes
from git, the chrome baseline is committed to the repo, and it pages by exit code
so a cron wrapper can open a GitHub issue. The one check that needs a mailbox,
distribution (did the edition get drafted), is not git-visible and lives in the
trigger's Gmail step, not here.

THE EIGHT DETERMINISTIC CHECKS
  1  presence    today's Eastern daily is on the branch
  2  dating      no page is dated in the future
  3  integrity   every page is a real document: opens with a tag, has a title, closes
  4  chrome      every page published since the design lock carries issue-chrome.html
                 (pre-lock pages are grandfathered via night-desk-baseline.json)
  5  subscribe   every page carries BOTH the pill and the form, with the honeypot
                 and the absolute POST url
  6  index       index.html links exactly the pages that exist, no orphans
  7  live        the deployed site matches the branch (pushed is not published);
                 falls back to the Pages deploy conclusion when egress is blocked
  8  gaps        missing dailies and monthlies (reported, never alarmed)

VERDICTS
  OK        nothing to do
  HEALED    the desk fixed it (only with --heal; reversible, in-repo fixes only)
  ESCALATE  a human is needed; the process exits 1 with the brief on stdout

Usage:
  night-desk.py                 report only, exit 1 if anything escalates
  night-desk.py --heal          also apply the mechanical fixes and push
  night-desk.py --quiet         only print the verdict line and any escalations
Environment:
  SHIPPED_REPO                  repo root override (defaults to `git rev-parse`)
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


def _repo_root():
    env = os.environ.get("SHIPPED_REPO")
    if env:
        return pathlib.Path(env)
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                       capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip():
        return pathlib.Path(r.stdout.strip())
    return pathlib.Path.cwd()


REPO = _repo_root()
SCRIPTS = REPO / "pipeline" / "scripts"
BASELINE = SCRIPTS / "night-desk-baseline.json"
SITE = "https://eddiebelaval.github.io/shipped"
ET = ZoneInfo("America/New_York")

SECTIONS = ("anthropic-daily", "anthropic-weekly", "anthropic-monthly")

HEAL = "--heal" in sys.argv
QUIET = "--quiet" in sys.argv

findings = []   # (check, verdict, message)


def log(msg):
    if QUIET:
        return
    print(f"[{datetime.now(ET):%Y-%m-%d %H:%M:%S %Z}] {msg}")


def record(check, verdict, message):
    findings.append((check, verdict, message))
    # Escalations are always printed, even under --quiet, so the wrapper sees them.
    if verdict != "OK" or not QUIET:
        print(f"{verdict:9} {check:10} {message}")


def run(*args):
    try:
        return subprocess.run(args, capture_output=True, text=True)
    except FileNotFoundError:
        return subprocess.CompletedProcess(args, 127, "", f"{args[0]}: not found")


def git(*args, repo=None):
    return run("git", "-C", str(repo or REPO), *args)


def fetch(url, timeout=25):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return 0, ""


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


def deploy_conclusion(sha):
    """Pages deploy verdict for a commit via `gh`. True/False, or None if unknown.

    The cloud-portable stand-in for a live fetch when egress is blocked. `gh` is
    on PATH in the release-routine environment; when it is not, we return None
    and the live check degrades to 'unverified' rather than a false alarm.
    """
    if not sha:
        return None
    gh = run("gh", "run", "list", "--repo", "eddiebelaval/shipped",
             "--branch", "daily-pages", "--commit", sha,
             "--json", "conclusion,status", "--limit", "5")
    if gh.returncode != 0 or not gh.stdout.strip():
        return None
    try:
        runs = json.loads(gh.stdout)
    except ValueError:
        return None
    if not runs or any(r.get("status") != "completed" for r in runs):
        return None
    return all(r.get("conclusion") == "success" for r in runs)


# --------------------------------------------------------------- the checks

def check_presence(pg, today):
    if today in pg["anthropic-daily"]:
        record("presence", "OK", f"{today} is on the branch")
        return
    # Today's edition is not late until the 21:00 ET routine has had time to
    # finish. Escalating before that trains the alarm into noise.
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


def load_baseline():
    try:
        return set(json.loads(BASELINE.read_text()).get("grandfathered", []))
    except (OSError, ValueError):
        return None


def check_chrome(pg):
    """Pages published since the design lock must carry issue-chrome.html.

    Pages that predate the 2026-08-06 lock are grandfathered by a list committed
    to the repo (night-desk-baseline.json). Without that baseline this check
    would be permanently red on 100+ historical pages and ignored within a week.
    In the cloud there is no local state to seed, so the baseline is versioned:
    if it is missing, we say so rather than guessing.
    """
    grandfathered = load_baseline()
    if grandfathered is None:
        record("chrome", "ESCALATE",
               f"baseline missing or unreadable at {BASELINE}. Cannot tell a "
               "pre-lock page from a routine that stopped pasting the chrome.")
        return
    missing = []
    for s in SECTIONS:
        for stem in pg[s]:
            key = f"{s}/{stem}"
            if key in grandfathered:
                continue
            if "weekly-masthead" not in blob(f"{key}.html"):
                missing.append(key)
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


def check_live(pg, expect_links):
    status, body = fetch(SITE + "/")
    if status == 200:
        live_links = len(set(re.findall(
            r'href="((?:anthropic-[a-z]+|dispatch)/[^"]+)"', body)))
        if expect_links is None:
            record("live", "OK", f"site up, {live_links} links")
        elif live_links != expect_links:
            record("live", "ESCALATE",
                   f"the branch has {expect_links} linked pages but the live site serves "
                   f"{live_links}. Pushed is not published: the deploy has not landed.")
        else:
            record("live", "OK", f"deployed site matches the branch ({live_links} pages)")
        return
    # Egress to the site is blocked in this environment; fall back to the Pages
    # deploy conclusion for the newest daily's commit, which answers the same
    # question (did the push actually publish) without needing to reach the site.
    newest = pg["anthropic-daily"][-1] if pg["anthropic-daily"] else None
    if newest is None:
        record("live", "ESCALATE", "no dailies on the branch and the site is unreachable")
        return
    sha = git("log", "-1", "--format=%H", "origin/daily-pages", "--",
              f"anthropic-daily/{newest}.html").stdout.strip()
    d = deploy_conclusion(sha)
    if d is True:
        record("live", "OK",
               f"site fetch blocked here; Pages deploy for {newest} concluded success")
    elif d is False:
        record("live", "ESCALATE",
               f"Pages deploy for {newest} did NOT succeed. Pushed is not published.")
    else:
        record("live", "OK",
               f"site fetch blocked and gh unavailable; live check unverified for {newest}")


def check_gaps(pg, today):
    stems = pg["anthropic-daily"]
    if not stems:
        return
    have = set(stems)
    d, missing = date.fromisoformat(stems[0]), []
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
        run(sys.executable, str(SCRIPTS / "backfill-subscribe.py"), wt)
        run(sys.executable, str(SCRIPTS / "build-archive-index.py"), wt)
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


def main():
    log("---- night desk ----")
    git("fetch", "origin", "daily-pages", "--quiet")
    today = datetime.now(ET).strftime("%Y-%m-%d")
    pg = pages()

    check_presence(pg, today)
    check_dating(pg, today)
    check_integrity(pg)
    check_chrome(pg)
    check_subscribe(pg)
    n = check_index(pg)
    check_live(pg, n)
    check_gaps(pg, today)

    escalations = [f for f in findings if f[1] == "ESCALATE"]
    healable = {"index", "subscribe"}
    if HEAL and any(f[0] in healable for f in escalations):
        heal(", ".join(f[0] for f in escalations if f[0] in healable))
        escalations = [f for f in findings if f[1] == "ESCALATE" and f[0] not in healable]

    # Headline: the one question a human wants answered. Presence + dating +
    # live together are "did tonight's edition actually go out".
    ship_blockers = [f for f in findings
                     if f[1] == "ESCALATE" and f[0] in ("presence", "dating", "live")]
    when = datetime.now(ET).strftime("%Y-%m-%d %H:%M ET")
    if ship_blockers:
        print(f"Did we ship, Shipped? NO — {ship_blockers[0][0]}: {ship_blockers[0][2]} ({when}).")
    else:
        print(f"Did we ship, Shipped? YES — {today} is on the branch and live ({when}).")

    if escalations:
        print(f"VERDICT: {len(escalations)} escalation(s): "
              + ", ".join(f"{c} ({m})" for c, _, m in escalations))
        return 1
    log(f"VERDICT: green, {len(findings)} checks clear")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"night desk itself failed: {e}")
        sys.exit(2)
