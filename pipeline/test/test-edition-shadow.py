#!/usr/bin/env python3
"""Edition Desk shadow: the routine's own markdown renders the paper and is compared with the HTML route."""
import importlib.util
import json
import re
import shutil
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ed", HERE.parent / "scripts" / "edition-desk.py")
ed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ed)

fails = 0


def check(name, got, want):
    global fails
    ok = got == want
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + ("" if ok else f"\n      got  {got!r}\n      want {want!r}"))


FIX = HERE / "fixtures" / "shadow"
tmp = Path(tempfile.mkdtemp(prefix="edition-shadow-test-"))
real_editions, real_ops, real_md, real_log = ed.EDITIONS, ed.OPS, ed.routine_md, ed.LOG
try:
    ed.EDITIONS, ed.OPS, ed.LOG = tmp / "editions", tmp / "ops", tmp / "desk.log"  # never the real desk log
    ed.SHADOW_LEDGER = ed.OPS / "edition-shadow.jsonl"
    d = ed.folder("anthropic-daily", "2026-10-15")
    d.mkdir(parents=True)
    shutil.copy(FIX / "source.html", d / "source.html")
    shutil.copy(FIX / "edition.md", d / "edition.md")
    body = (FIX / "edition.md").read_text().split("\n---\n", 1)[1]

    def run(md):
        ed.routine_md = lambda s, t: md
        st = {}
        ed.shadow("anthropic-daily", "2026-10-15", st, (d / "source.html").read_text())
        return json.loads(ed.SHADOW_LEDGER.read_text().splitlines()[-1])

    good = ('---\ndate: 2026-10-15\ntitle: "Shipped., Thursday, October 15, 2026"\n'
            'deck: "Meta releases 816 billion parameters for free, and the rest of the frontier recalibrates."\n'
            'period: "Oct 14 to Oct 15"\nweather: "The race is not only about who ships the best model anymore."\n---\n' + body)
    v = run(good)
    check("routine md in the paper shape: AGREE", (v["result"], v.get("problems")), ("AGREE", []))

    v = run((FIX / "routine-2026-10-12.md").read_text())
    check("freeform routine md (2026-10-12): SHAPE, never rendered", v["result"], "SHAPE")

    dropped = re.sub(r"^### Grok Voice.*?(?=^### )", "", good, flags=re.M | re.S)
    v = run(dropped)
    check("md missing a story the page has: DISAGREE", v["result"], "DISAGREE")
finally:
    ed.EDITIONS, ed.OPS, ed.routine_md, ed.LOG = real_editions, real_ops, real_md, real_log
    shutil.rmtree(tmp, ignore_errors=True)

print("\nALL PASS" if not fails else f"\n{fails} FAILED")
raise SystemExit(1 if fails else 0)
