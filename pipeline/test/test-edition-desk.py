#!/usr/bin/env python3
"""Edition Desk decisions: nothing ships unseen, approved sets publish, rejected slots drop."""
import importlib.util
import json
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


tmp = Path(tempfile.mkdtemp(prefix="edition-desk-test-"))
ed.EDITIONS = tmp
imgs = tmp / "anthropic-daily" / "2026-10-10" / "images"
imgs.mkdir(parents=True)


def setup(statuses, treatments=None):
    slots = {s: {"caption": s, "alt": s, **({"treatment": treatments[s]} if treatments and s in treatments else {})}
             for s in {f.rsplit("-", 1)[0] for f in statuses}}
    (imgs / "slots.json").write_text(json.dumps(slots))
    (imgs / "manifest.json").write_text(json.dumps({"images": {
        f: {"review": {"status": st}, "treatment": f.rsplit("-", 1)[1][:-4]} for f, st in statuses.items()}}))


try:
    check("no images yet: text-only", ed.ready_set("anthropic-daily", "2026-10-10"), [])

    setup({"cover-atkinson.png": "approved", "cover-halftone.png": "pending", "lead-atkinson.png": "pending"},
          {"cover": "halftone"})
    check("any drawn image pending: nothing ships", ed.ready_set("anthropic-daily", "2026-10-10"), [])

    setup({"cover-atkinson.png": "approved", "cover-halftone.png": "pending", "lead-atkinson.png": "approved"},
          {"cover": "atkinson"})
    check("an unpicked treatment never blocks", ed.ready_set("anthropic-daily", "2026-10-10"),
          ["cover-atkinson.png", "lead-atkinson.png"])

    setup({"cover-atkinson.png": "approved", "lead-atkinson.png": "rejected", "story-1-atkinson.png": "approved"})
    check("rejected slots drop, approved publish", ed.ready_set("anthropic-daily", "2026-10-10"),
          ["cover-atkinson.png", "story-1-atkinson.png"])
    check("status counts drawn images only", ed.image_status("anthropic-daily", "2026-10-10"),
          {"pending": 0, "approved": 2, "rejected": 1})

    check("images scoped per edition",
          ed.scope_images('<img src="img/a.png"><source srcset="img/b.png">', "2026-10-10"),
          '<img src="img/2026-10-10/a.png"><source srcset="img/2026-10-10/b.png">')

    md = "---\ntitle: x\n---\n## The Open\n\nAlpha beta gamma delta epsilon zeta eta theta iota.\n\n" \
         "## A. Models\n\n#### 2026-10-07 - Claude Haiku 5.5 ([source](https://x))\n`[MODEL]`\n\nBody.\n\n" \
         "**How to use:** Call the API with the model id today please now.\n"
    page_ok = ('<title>t</title>' + ed.MARKER + '<p>Alpha beta gamma delta epsilon zeta eta theta iota.</p>'
               '<b>Claude Haiku 5.5</b> Body. <b>How to use</b> Call the API with the model id today please now.'
               '<section id="subscribe">https://id8labs.app/api/newsletter/subscribe</section>')
    check("gate passes a faithful page", ed.parity_gate(md, page_ok), [])
    check("gate catches a dropped log entry", ed.parity_gate(md, page_ok.replace("Claude Haiku 5.5", "")),
          ["log entry missing: Claude Haiku 5.5"])
    check("gate catches a dash", ed.parity_gate(md, page_ok + chr(0x2014)), ["em/en dash on the page"])
    check("gate catches a second subscribe form", ed.parity_gate(md, page_ok + '<div id="subscribe">'),
          ["2 subscribe forms, expected 1"])
    check("gate catches a routine page (no paper marker)", ed.parity_gate(md, page_ok.replace(ed.MARKER, "")),
          ["paper layout marker missing"])
finally:
    shutil.rmtree(tmp)

print(f"\n{'ALL PASS' if not fails else f'{fails} FAILED'}")
raise SystemExit(1 if fails else 0)
