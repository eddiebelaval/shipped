#!/usr/bin/env python3
"""Archive editions (May to October 2026 templates) convert to the paper without losing a word or a link.

Each fixture is the smallest shape of a real archive template the converter once dropped content from.
"""
import importlib.util
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("e2p", HERE.parent / "scripts" / "edition-to-paper.py")
e2p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e2p)
spec = importlib.util.spec_from_file_location("ed", HERE.parent / "scripts" / "edition-desk.py")
ed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ed)

fails = 0


def check(name, got, want):
    global fails
    ok = got == want
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + ("" if ok else f"\n      got  {got!r}\n      want {want!r}"))


def conv(body, stem="2026-05-06", section="anthropic-daily"):
    md, summary = e2p.convert(f"<html><head><title>Shipped. Daily</title></head><body>{body}</body></html>", section, stem)
    return md, summary


ENTRY = ('<div class="log-entry"><div class="log-entry-meta"><span class="log-date">2026-05-06</span>'
         '<span class="log-tag tag-code">CODE</span></div><div class="log-entry-title">'
         '<a href="https://example.com/cc">Claude Code 2.1.132</a></div>'
         '<div class="log-entry-summary"><p>Adds a setting.</p><p>Update via <code>claude update</code>.</p></div></div>')

# May 2026: one-line read, untitled lead paragraphs, lettered category header, log with no log-section.
md, s = conv('<header class="masthead"><span class="masthead-dateline">Daily | May 06</span></header>'
             '<p class="one-liner">Anthropic held its first developer conference today.</p>'
             '<div class="lead-body"><p>The keynote opened in San Francisco at 09:00 PT. It ran long.</p><p>Second para.</p></div>'
             '<div class="log-area-header"><span class="log-area-letter">C</span> <span class="log-area-name">Claude Code</span></div>'
             + ENTRY)
check("May: read becomes the Open", "Anthropic held its first developer conference today." in md.split("## The Lead Story")[0], True)
check("May: masthead dateline is furniture", "Daily | May 06" in md, False)
check("May: untitled lead headlined by its first sentence", s["lead"], "The keynote opened in San Francisco at 09:00 PT")
check("May: log body kept from log-entry-summary", "Adds a setting. Update via `claude update`." in md, True)
check("May: category letter dropped", "## A. Claude Code" in md, True)

# A release-log-only day: the top entry leads the front.
md, s = conv('<section class="log-section"><div class="log-cat-head"><div class="log-cat-name">Claude Code</div></div>'
             + ENTRY + '</section>')
check("log-only: first entry leads", s["lead"], "Claude Code 2.1.132")
check("log-only: entry stays in the log", s["log_entries"], 1)

# Empty categories read in Quiet; several categories in one section keep their own names.
md, s = conv('<div class="feature-opener"><h2 class="feature-title">Lead</h2></div><div class="prose-well"><div class="prose"><p>Lead body.</p></div></div>'
             '<div class="log-section"><div class="log-cat-head"><div class="log-cat-name">E. Agent SDKs</div></div>'
             '<div class="log-cat-deck">No SDK releases confirmed in window.</div></div>'
             '<section class="log-section"><div class="log-cat-head"><div class="log-cat-name">Claude Code</div></div>' + ENTRY
             + '<div class="log-cat-head"><div class="log-cat-name">News</div></div>' + ENTRY.replace("Claude Code 2.1.132", "Item two") + '</section>')
check("empty category note reads in Quiet", "*Agent SDKs:* No SDK releases confirmed in window." in md, True)
check("two categories in one section both named", ("## A. Claude Code" in md, "## B. News" in md), (True, True))

# The Dig: a folio-headlined section and a dig-item-label headline, beside a feature lead.
md, s = conv('<div class="feature-opener"><h2 class="feature-title">Opus</h2></div><div class="prose-well"><div class="prose"><p>Lead.</p></div></div>'
             '<section class="section"><div class="section-folio"><span class="section-folio-label">The Dig</span>'
             '<span class="section-folio-sub">API: Three Changes</span></div><div class="prose"><p>Dig one.</p></div></section>'
             '<div class="prose-well"><div class="prose"><div class="dig-item-label">AlphaFold team restructuring</div><p>Dig two.</p></div></div>')
check("Dig: folio headline kept", "### API: Three Changes" in md, True)
check("Dig: dig-item-label text kept", "AlphaFold team restructuring" in md, True)

# Quiet as a list; a How line inside the body; a labelled how line keeps its label.
md, s = conv('<div class="feature-opener"><h2 class="feature-title">Lead</h2></div><div class="prose-well"><div class="prose"><p>Lead.</p></div></div>'
             '<div class="quiet-body"><p>One release.</p><ul><li>The $65B Series H at $965B.</li></ul></div>'
             '<section class="log-section"><div class="log-cat-name">Code</div><div class="log-entry">'
             '<div class="log-entry-title"><a href="https://example.com/x">v2</a></div>'
             '<div class="log-entry-body"><p>Fixes.</p><p><strong>How to use:</strong> claude update</p></div>'
             '<div class="log-entry-how"><b>Key fixes</b>Network drops.</div></div></section>')
check("Quiet list items kept", "The $65B Series H at $965B." in md, True)
check("in-body How line becomes the How", "**How to use:** claude update" in md, True)
check("labelled how line keeps its label", "Key fixes: Network drops." in md, True)

# A release log written as a table (weekly 2026-30).
md, s = conv('<div class="feature-opener"><h2 class="feature-title">Lead</h2></div><div class="prose-well"><div class="prose"><p>Lead.</p></div></div>'
             '<table><thead><tr><th>Date</th><th>Area</th><th>Release</th><th>Notes</th></tr></thead><tbody>'
             '<tr><td>2026-07-20</td><td>CODE</td><td><a href="https://example.com/c">Claude Code v2.1.216</a></td><td>Faster.</td></tr>'
             '<tr><td>2026-07-24</td><td>DEPRECATION</td><td>Opus 4.7 Fast Mode removed</td><td>Gone.</td></tr></tbody></table>',
             stem="2026-30", section="anthropic-weekly")
check("log table rows become entries", s["log_entries"], 2)
check("DEPRECATION tag kept", "`[DEPRECATION]`" in md, True)

# The gate: a link the paper prints once where the routine printed it twice still passes; a dropped link holds.
src = ('<div class="also-item"><div class="also-item-title"><a href="https://x.com/a">T</a></div>'
       '<div class="also-item-source"><a href="https://x.com/a">x.com</a></div></div>')
# The real 10-14/10-15 fold: the paper unlinks the headline and keeps the link on the source line.
check("link parity: linked headline folds into its source line", [p for p in ed.source_parity(src, '<h3>T</h3><a href="https://x.com/a">x.com</a>') if "link" in p], [])
check("link parity: missing link holds", any("link missing" in p for p in ed.source_parity(src, "<p>T x.com</p>")), True)

# A link dropped from a story is caught even when the same URL survives in the release log.
src2 = ('<div class="prose"><p>Read <a href="https://x.com/s1">the S-1 filing</a> today.</p></div>'
        '<div class="log-entry-title"><a href="https://x.com/s1">S-1 filed</a></div>')
check("link parity: body link dropped, log keeps URL -> held",
      any("dropped from its words" in p for p in ed.source_parity(src2, '<p>Read the S-1 filing today.</p><a href="https://x.com/s1">S-1 filed</a>')), True)
check("link parity: widened link (whole log title) passes",
      [p for p in ed.source_parity('<div class="log-entry-title">Delayed (<a href="https://x.com/g">9to5Google</a>)</div>',
                                   '<a href="https://x.com/g">Delayed (9to5Google)</a>') if "link" in p], [])

# Coverage: a paragraph the converter dropped is caught; furniture is not demanded.
cov_src = ('<body><nav class="pub-bar">Subscribe now please</nav><div class="cover-top">Week 26 cover box</div>'
           '<p>The edition says this.</p><p>And this too.</p></body>')
check("coverage: furniture not demanded", ed.source_coverage(cov_src, "<p>The edition says this. And this too.</p>"), [])
check("coverage: dropped paragraph caught", ed.source_coverage(cov_src, "<p>The edition says this.</p>"),
      ["source text missing: And this too."])
finally_ok = fails == 0
print("\nALL PASS" if finally_ok else f"\n{fails} FAILED")
raise SystemExit(0 if finally_ok else 1)
