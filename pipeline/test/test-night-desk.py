#!/usr/bin/env python3
"""Prove every Night Desk alarm fires. Injects each real 2026-08 failure."""
import importlib.util
import sys
from datetime import datetime

spec = importlib.util.spec_from_file_location(
    "nd", "/Users/eddiebelaval/Development/id8/shipped/pipeline/scripts/night-desk.py")
nd = importlib.util.module_from_spec(spec)
sys.argv = ["nd", "--quiet"]
spec.loader.exec_module(nd)

TODAY = "2026-08-06"
GOOD = ('<!DOCTYPE html><html><head><title>x</title></head><body>'
        '<div class="weekly-masthead">Shipped</div>'
        '<a class="pub-bar-cta">Subscribe</a>'
        '<section id="subscribe"><input name="website">'
        'https://id8labs.app/api/newsletter/subscribe</section>'
        '</body></html>')

fails = 0


def run(name, fn, expect):
    global fails
    nd.findings.clear()
    fn()
    got = [f for f in nd.findings if f[1] == "ESCALATE"]
    ok = (len(got) > 0) == expect
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    for c, v, m in nd.findings:
        print(f"        {v}: {m[:120]}")
    if not ok:
        fails += 1


def with_blob(mapping, default=GOOD):
    nd.blob = lambda p: mapping.get(p, default)


# --- 1. presence: today missing, and it is past the publish window ----------
class LateClock(datetime):
    @classmethod
    def now(cls, tz=None):
        return datetime(2026, 8, 6, 22, 0, tzinfo=nd.ET)


real_dt = nd.datetime
nd.datetime = LateClock
run("presence: today missing at 22:00 ET",
    lambda: nd.check_presence({"anthropic-daily": ["2026-08-05"]}, TODAY), True)
nd.datetime = real_dt

run("presence: today missing at midday is NOT an alarm",
    lambda: nd.check_presence({"anthropic-daily": ["2026-08-05"]}, TODAY), False)

# --- 2. dating: the 2026-08-05 bug ----------------------------------------
run("dating: page stamped tomorrow",
    lambda: nd.check_dating({"anthropic-daily": ["2026-08-05", "2026-08-07"]}, TODAY), True)

# --- 3. integrity: the base64 page ----------------------------------------
with_blob({"anthropic-daily/2026-08-06.html": "PCFET0NUWVBFIGh0bWw+Cg=="})
run("integrity: base64-encoded page",
    lambda: nd.check_integrity({"anthropic-daily": ["2026-08-06"],
                                "anthropic-weekly": [], "anthropic-monthly": []}), True)

with_blob({"anthropic-daily/2026-08-06.html": '<meta charset="UTF-8"><title>x</title>'})
run("integrity: no doctype and unclosed",
    lambda: nd.check_integrity({"anthropic-daily": ["2026-08-06"],
                                "anthropic-weekly": [], "anthropic-monthly": []}), True)

# --- 4. chrome: a routine stops pasting the locked design -------------------
with_blob({"anthropic-daily/2026-08-06.html": GOOD.replace("weekly-masthead", "my-own-masthead")})
run("chrome: new page free-hands its CSS",
    lambda: nd.check_chrome({"anthropic-daily": ["2026-08-06"], "anthropic-weekly": [],
                             "anthropic-monthly": []}, {"pre_lock_pages": []}), True)

# --- 5. subscribe: the dead-button pages -----------------------------------
with_blob({"anthropic-weekly/2026-30.html":
           '<!DOCTYPE html><html><head><title>x</title></head><body>'
           '<a class="pub-bar-cta">Subscribe</a></body></html>'})
run("subscribe: Subscribe pill anchored to nothing",
    lambda: nd.check_subscribe({"anthropic-daily": [], "anthropic-weekly": ["2026-30"],
                                "anthropic-monthly": []}), True)

with_blob({"anthropic-daily/2026-08-06.html": GOOD.replace('<input name="website">', "")})
run("subscribe: honeypot stripped from the form",
    lambda: nd.check_subscribe({"anthropic-daily": ["2026-08-06"], "anthropic-weekly": [],
                                "anthropic-monthly": []}), True)

with_blob({"anthropic-daily/2026-08-06.html":
           GOOD.replace("https://id8labs.app/api/newsletter/subscribe", "/api/newsletter/subscribe")})
run("subscribe: POST url made relative (404s on github.io)",
    lambda: nd.check_subscribe({"anthropic-daily": ["2026-08-06"], "anthropic-weekly": [],
                                "anthropic-monthly": []}), True)

# --- 6. index: a page exists but nothing links to it -----------------------
with_blob({"index.html": '<a href="anthropic-daily/2026-08-05.html">x</a>'})
nd.git = lambda *a, **k: type("R", (), {"stdout": "", "returncode": 0})()
run("index: published page unreachable from the index",
    lambda: nd.check_index({"anthropic-daily": ["2026-08-05", "2026-08-06"],
                            "anthropic-weekly": [], "anthropic-monthly": []}), True)

# --- 7. live: pushed but not published -------------------------------------
nd.fetch = lambda u, timeout=25: (200, '<a href="anthropic-daily/2026-08-05.html">x</a>')
run("live: branch has more pages than the deployed site", lambda: nd.check_live(106), True)

nd.fetch = lambda u, timeout=25: (503, "")
run("live: the site itself is down", lambda: nd.check_live(1), True)

print()
print("ALL ALARMS PROVEN" if fails == 0 else f"{fails} ALARM(S) DID NOT FIRE")
sys.exit(1 if fails else 0)
