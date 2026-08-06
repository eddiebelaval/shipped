#!/usr/bin/env python3
"""
Shipped. — render a weekly or monthly issue in the CANONICAL issue design.

The design is locked to anthropic-weekly/2026-31, chosen by Eddie on 2026-08-06
as the standard after an audit showed the three cadences had drifted into three
different looks. All of its chrome lives in pipeline/src/render/issue-chrome.html
and is pasted verbatim; this renderer only supplies markup in that file's class
vocabulary. Changing the design means changing that file, and every cadence that
pastes it inherits the change. Same enforcement pattern as subscribe-block.html.

House rules asserted before write: no em dashes (U+2014), no en dashes (U+2013),
exactly one subscribe block, no unbound {{SOURCE}}.

Usage:
  render-issue.py <content.json> <out.html>
"""
import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
CHROME = HERE.parent / "src" / "render" / "issue-chrome.html"
SNIPPET = HERE.parent / "src" / "render" / "subscribe-block.html"

SEP = "&nbsp;&#183;&nbsp;"


def rich(s):
    """Escape, then re-enable [text](url) links, <em>, <br>, and named entities.

    Escaping first and re-enabling a small allowlist keeps arbitrary markup out
    of the page while letting the content files use the same separator entities
    the standard page uses. Without the entity step the dot separators render as
    the literal text "&nbsp;&#183;&nbsp;" in every kicker.
    """
    s = html.escape(s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = s.replace("&lt;em&gt;", "<em>").replace("&lt;/em&gt;", "</em>")
    s = s.replace("&lt;br&gt;", "<br>")
    s = re.sub(r"&amp;(nbsp|#\d{2,5}|#x[0-9a-fA-F]{2,5});", r"&\1;", s)
    return s


def paras(items):
    return "\n".join(f"<p>{rich(p)}</p>" for p in items)


def build(c):
    o = []
    pb = c["pub_bar"]

    o.append('<nav class="pub-bar">')
    o.append('  <div class="pub-bar-left">')
    o.append('    <span class="pub-bar-mark">Shipped<span class="dot">.</span></span>')
    o.append('    <span class="pub-bar-sep pub-bar-hide-sm"></span>')
    o.append(f'    <span class="pub-bar-meta pub-bar-hide-sm">{html.escape(pb["meta"])} {SEP} '
             '<a href="https://id8labs.app/shipped" class="pub-bar-link">id8Labs</a></span>')
    o.append('  </div>')
    o.append('  <div class="pub-bar-right">')
    o.append(f'    <span class="pub-bar-folio pub-bar-hide-sm">{html.escape(pb["folio_label"])} '
             f'<b>{html.escape(pb["folio"])}</b></span>')
    o.append('    <span class="pub-bar-sep pub-bar-hide-sm"></span>')
    o.append(f'    <span class="pub-bar-meta pub-bar-hide-sm">{html.escape(pb["range"])}</span>')
    o.append('    <a href="#subscribe" class="pub-bar-cta">Subscribe</a>')
    o.append('  </div>')
    o.append('</nav>')

    o.append('<header class="weekly-header">')
    o.append(f'  <div class="weekly-kicker">{rich(c["kicker"])}</div>')
    o.append('  <div class="weekly-masthead">Shipped<span class="dot">.</span></div>')
    o.append(f'  <div class="weekly-cover-line">{rich(c["cover_line"])}</div>')
    o.append('  <div class="weekly-dateline">')
    for k, v in c["dateline"]:
        o.append(f'    <span><b>{html.escape(k)}</b> {html.escape(v)}</span>')
    o.append('  </div>')
    o.append('</header>')

    op = c["open"]
    o.append('<section class="open-section">')
    o.append('  <div class="section" style="padding-top:72px">')
    o.append('    <div class="section-folio"><div class="section-folio-left">')
    o.append('      <div class="folio"><div class="ruler"></div><b>The Open</b></div>')
    o.append('      <span class="section-folio-sub">Front of book</span>')
    o.append('    </div></div>')
    o.append('    <div class="open-grid"><div class="open-lead">')
    o.append(f'      <div class="open-quote">{rich(op["quote"])}</div>')
    o.append(f'      <div class="open-prose">{paras(op["prose"])}</div>')
    o.append('    </div></div>')
    o.append('  </div>')
    o.append('</section>')

    for f in c["features"]:
        o.append('<div class="feature-opener">')
        o.append(f'  <div class="vert-label">{html.escape(f["label"])}'
                 f'<span class="vert-num">{html.escape(f["num"])}</span></div>')
        o.append('  <div class="feature-heading">')
        o.append(f'    <div class="feature-kicker">{rich(f["kicker"])}</div>')
        o.append(f'    <h2 class="feature-title">{rich(f["title"])}</h2>')
        o.append(f'    <div class="feature-deck">{rich(f["deck"])}</div>')
        if f.get("meta"):
            rows = "<br>".join(f'<b>{html.escape(k)}</b> {rich(v)}' for k, v in f["meta"])
            o.append(f'    <div class="feature-meta">{rows}</div>')
        o.append('  </div>')
        if f.get("right"):
            o.append('  <div class="feature-right">')
            o.append(f'    <span class="feature-right-label">'
                     f'{html.escape(f.get("right_label", "By the numbers"))}</span>')
            o.append("<br><br>".join(rich(x) for x in f["right"]))
            o.append('  </div>')
        o.append('</div>')

        o.append('<div class="prose-well">')
        if f.get("marginalia"):
            o.append(f'  <div class="prose-marginalia">{rich(f["marginalia"])}</div>')
        o.append(f'  <div class="prose drop-cap drop-cap-orange">{paras(f["prose"])}</div>')
        o.append('</div>')

    if c.get("also"):
        a = c["also"]
        o.append('<section class="section">')
        o.append('  <div class="section-folio"><div class="section-folio-left">')
        o.append(f'    <div class="folio"><div class="ruler"></div><b>{html.escape(a["folio"])}</b></div>')
        o.append(f'    <span class="section-folio-sub">{html.escape(a["sub"])}</span>')
        o.append('  </div></div>')
        for it in a["items"]:
            o.append('  <div class="also-item">')
            o.append(f'    <div class="also-item-kicker">{rich(it["kicker"])}</div>')
            title = (f'<a href="{html.escape(it["href"])}">{rich(it["title"])}</a>'
                     if it.get("href") else rich(it["title"]))
            o.append(f'    <div class="also-item-title">{title}</div>')
            o.append(f'    <div class="also-item-body">{rich(it["body"])}</div>')
            o.append('  </div>')
        o.append('</section>')

    if c.get("close"):
        cl = c["close"]
        o.append('<section class="close-section">')
        o.append(f'  <div class="close-kicker">{rich(cl["kicker"])}</div>')
        o.append('  <div class="close-stack">')
        for line in cl["lines"]:
            o.append(f'    <div class="close-line">{rich(line)}</div>')
        o.append('    <div class="close-coda-start">')
        o.append(f'      <div class="close-final">{rich(cl["final"])}</div>')
        o.append('    </div>')
        o.append('  </div>')
        o.append('  <div class="close-mark">&#x25cf;</div>')
        o.append('</section>')

    lg = c["log"]
    o.append('<div class="log-divider" id="log">')
    o.append(f'  <div class="log-divider-kicker">Back of Book {SEP} Reference</div>')
    o.append('  <h2 class="log-divider-title">The <em>Release</em> Log</h2>')
    o.append(f'  <p class="log-divider-sub">{rich(lg["deck"])}</p>')
    o.append('</div>')
    for s in lg["sections"]:
        o.append('<div class="log-section">')
        o.append('  <div class="log-cat-head">')
        o.append(f'    <div class="log-cat-name">{html.escape(s["name"])}</div>')
        o.append(f'    <div class="log-cat-count"><b>{html.escape(s["count"])}</b> {html.escape(s["unit"])}</div>')
        o.append('  </div>')
        o.append(f'  <div class="log-cat-deck">{rich(s["deck"])}</div>')
        o.append('  <div class="log-entries">')
        for e in s["entries"]:
            o.append('    <div class="log-entry">')
            o.append('      <div class="log-entry-left">')
            o.append(f'        <div class="log-entry-date">{html.escape(e["date"])}</div>')
            o.append(f'        <span class="log-tag {html.escape(e["tag"])}">'
                     f'{html.escape(e["tag_label"])}</span>')
            o.append('      </div>')
            o.append('      <div>')
            t = (f'<a href="{html.escape(e["href"])}">{rich(e["title"])}</a>'
                 if e.get("href") else rich(e["title"]))
            o.append(f'        <div class="log-entry-title">{t}</div>')
            o.append(f'        <div class="log-entry-body">{rich(e["body"])}</div>')
            o.append('      </div>')
            o.append('    </div>')
        o.append('  </div>')
        o.append('</div>')

    co = c["colophon"]
    o.append('<footer class="colophon"><div class="colophon-inner">')
    o.append('  <div class="colophon-mast">')
    o.append('    <div class="colophon-word">Shipped<span class="dot">.</span></div>')
    o.append(f'    <div class="colophon-tag">{rich(co["tag"])}</div>')
    o.append('  </div>')
    o.append('  <div class="colophon-body">')
    o.append('    <div class="colophon-col"><h4>Masthead</h4>')
    for k, v in co["masthead"]:
        o.append(f'      <p><b>{html.escape(k)}</b> {rich(v)}</p>')
    o.append('    </div>')
    o.append('    <div class="colophon-col"><h4>Sources</h4>')
    for n, u in co["sources"]:
        o.append(f'      <p><a class="colophon-link" href="{html.escape(u)}">{html.escape(n)}</a></p>')
    o.append('    </div>')
    o.append('  </div>')
    o.append('</div></footer>')

    return "\n".join(o)


def render(c):
    chrome = CHROME.read_text(encoding="utf-8")
    body = build(c) + "\n" + SNIPPET.read_text(encoding="utf-8").replace(
        "{{SOURCE}}", c["source_tag"])
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<meta name="color-scheme" content="light">\n'
        f'<title>{html.escape(c["title"])}</title>\n'
        f'<meta property="og:title" content="{html.escape(c["title"])}">\n'
        f'<meta property="og:description" content="{html.escape(c["og"])}">\n'
        f'<meta property="og:url" content="{html.escape(c["url"])}">\n'
        f'<meta name="twitter:title" content="{html.escape(c["title"])}">\n'
        f'{chrome}\n</head>\n<body>\n{body}\n</body>\n</html>\n'
    )


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    for p in (CHROME, SNIPPET):
        if not p.exists():
            print(f"missing partial: {p}", file=sys.stderr)
            return 1

    c = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = render(c)

    bad = [ch for ch in ("—", "–") if ch in out]
    if bad:
        print(f"dash self-audit FAILED: {bad!r} present; not writing", file=sys.stderr)
        return 1
    if out.count('id="subscribe"') != 1 or "{{SOURCE}}" in out:
        print("subscribe-block audit FAILED", file=sys.stderr)
        return 1

    front = out.split('class="log-divider"')[0]
    words = len(re.sub(r"<[^>]+>", " ", front.split("</head>")[-1]).split())

    pathlib.Path(sys.argv[2]).write_text(out, encoding="utf-8")
    print(f"wrote {sys.argv[2]}")
    print("dash self-audit: 0 found")
    print(f"subscribe block: present, source {c['source_tag']}")
    print(f"chrome: issue-chrome.html pasted verbatim ({len(CHROME.read_text())} bytes)")
    print(f"front-of-book word count: {words}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
