#!/usr/bin/env python3
"""
Shipped. — render a weekly or monthly compilation page in the canonical design.

The three cloud routines free-hand their HTML from template.html every run, so
no two published pages share a class vocabulary. That is fine for a routine with
a model in the loop; it is not a way to backfill a gap by hand. This renderer
takes structured content and emits the canonical chrome deterministically.

Design tokens (the :root block, the font link, the favicon) are lifted out of
pipeline/src/render/template.html at build time, exactly as build-archive-index.py
does, so the palette can never drift from the single source of design truth.
The subscribe block is pasted from src/render/subscribe-block.html verbatim.

House rule enforced before write: no em dashes (U+2014), no en dashes (U+2013).

Usage:
  render-issue.py <content.json> <out.html>
"""
import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "src" / "render" / "template.html"
SNIPPET = HERE.parent / "src" / "render" / "subscribe-block.html"

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{background:var(--paper);color:var(--body);font-family:var(--sans);
  font-size:17px;line-height:1.65;-webkit-font-smoothing:antialiased;overflow-x:hidden}
::selection{background:var(--orange);color:#fff}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:1;opacity:.5;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='120' height='120' filter='url(%23n)' opacity='.038'/%3E%3C/svg%3E")}
.pub-bar{position:sticky;top:0;z-index:20;background:var(--ink);color:var(--paper);
  display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:.55rem 1.5rem;
  font-family:var(--narrow);font-size:10px;font-weight:600;letter-spacing:.22em;text-transform:uppercase}
.pub-bar a{color:var(--paper);text-decoration:none;border-bottom:1px solid var(--orange);padding-bottom:1px}
.pub-bar-right{display:flex;gap:1.25rem;align-items:center}
.wrap{position:relative;z-index:2;max-width:44rem;margin:0 auto;padding:4rem 1.5rem 5rem}
.masthead{font-family:var(--disp);font-style:italic;font-weight:600;
  font-size:clamp(2.5rem,8vw,3.75rem);line-height:1;letter-spacing:-.03em;color:var(--ink)}
.masthead .dot{color:var(--orange)}
.kicker{font-family:var(--narrow);font-size:10px;font-weight:700;letter-spacing:.24em;
  text-transform:uppercase;color:var(--orange);margin-bottom:.9rem}
.dateline{font-family:var(--mono);font-size:11px;color:var(--gray);letter-spacing:.04em;
  margin-top:.8rem;padding-bottom:1.75rem;border-bottom:3px solid var(--ink)}
.cover{font-family:var(--disp);font-size:clamp(1.6rem,4.6vw,2.3rem);font-weight:600;
  line-height:1.2;letter-spacing:-.02em;color:var(--ink);margin:2.25rem 0 2rem}
.sec{margin-top:3rem}
.sec-flag{font-family:var(--narrow);font-size:10px;font-weight:700;letter-spacing:.22em;
  text-transform:uppercase;color:var(--orange);padding-bottom:.45rem;
  border-bottom:1px solid var(--hair);margin-bottom:1.1rem}
.sec-title{font-family:var(--disp);font-size:1.4rem;font-weight:600;line-height:1.25;
  letter-spacing:-.015em;color:var(--ink);margin-bottom:.8rem}
p{margin-bottom:1.1rem}
p a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--orange)}
p a:hover{background:var(--paper-shadow)}
.entry{padding:1.25rem 0;border-bottom:1px solid var(--hair-soft)}
.entry-head{display:flex;align-items:baseline;gap:.6rem;margin-bottom:.35rem;flex-wrap:wrap}
.tag{font-family:var(--narrow);font-size:9px;font-weight:700;letter-spacing:.14em;
  text-transform:uppercase;background:var(--ink);color:var(--paper);padding:2px 6px}
.entry-date{font-family:var(--mono);font-size:11px;color:var(--gray)}
.entry-title{font-weight:600;font-size:1rem;line-height:1.35;color:var(--ink)}
.entry-title a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--orange)}
.entry-body{font-size:.9375rem;color:var(--muted);line-height:1.55}
.close-note{margin-top:2.5rem;padding:1.5rem 0 0;border-top:3px solid var(--ink);
  font-family:var(--disp);font-size:1.15rem;font-style:italic;line-height:1.45;color:var(--ink)}
.colophon{margin-top:3.5rem;padding-top:1.5rem;border-top:1px solid var(--hair);
  font-family:var(--mono);font-size:11px;color:var(--gray);line-height:1.9}
.colophon a{color:var(--muted)}
.colophon b{color:var(--body);font-weight:500}
@media (max-width:640px){.wrap{padding:2.75rem 1.15rem 4rem}body{font-size:16px}
  .pub-bar-hide-sm{display:none}}
"""


def tokens():
    t = TEMPLATE.read_text(encoding="utf-8")
    root = re.search(r":root\{.*?\n\}", t, re.S)
    if not root:
        raise SystemExit("no :root block in template.html")
    links = [ln.strip() for ln in t.splitlines()
             if re.search(r'rel="(icon|preconnect|stylesheet)"', ln)]
    if not links:
        raise SystemExit("no font/favicon links in template.html")
    return root.group(0), "\n".join(links)


def para(s):
    """Inline links written as [text](url)."""
    s = html.escape(s)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)


def render(c):
    root_css, links = tokens()
    p = []
    p.append('<div class="pub-bar"><span>Shipped. ' + html.escape(c["kicker"]) + '</span>'
             '<span class="pub-bar-right">'
             f'<span class="pub-bar-hide-sm">{html.escape(c["folio"])}</span>'
             '<a href="#subscribe">Subscribe</a></span></div>')
    p.append('<div class="wrap">')
    p.append(f'<div class="kicker">{html.escape(c["kicker"])}</div>')
    p.append('<h1 class="masthead">Shipped<span class="dot">.</span></h1>')
    p.append(f'<div class="dateline">{html.escape(c["dateline"])}</div>')
    p.append(f'<div class="cover">{para(c["cover_line"])}</div>')

    for s in c["sections"]:
        p.append('<div class="sec">')
        if s.get("flag"):
            p.append(f'<div class="sec-flag">{html.escape(s["flag"])}</div>')
        if s.get("title"):
            p.append(f'<div class="sec-title">{para(s["title"])}</div>')
        for t in s.get("paras", []):
            p.append(f"<p>{para(t)}</p>")
        for e in s.get("entries", []):
            p.append('<div class="entry"><div class="entry-head">')
            if e.get("tag"):
                p.append(f'<span class="tag">{html.escape(e["tag"])}</span>')
            if e.get("date"):
                p.append(f'<span class="entry-date">{html.escape(e["date"])}</span>')
            p.append("</div>")
            title = (f'<a href="{html.escape(e["href"])}">{para(e["title"])}</a>'
                     if e.get("href") else para(e["title"]))
            p.append(f'<div class="entry-title">{title}</div>')
            if e.get("body"):
                p.append(f'<div class="entry-body">{para(e["body"])}</div>')
            p.append("</div>")
        p.append("</div>")

    if c.get("close"):
        p.append(f'<div class="close-note">{para(c["close"])}</div>')

    p.append('<div class="colophon">')
    p.append(f'<b>{html.escape(c["colophon_line"])}</b><br>')
    p.append("Sources: " + ", ".join(
        f'<a href="{html.escape(u)}">{html.escape(n)}</a>' for n, u in c["sources"]) + "<br>")
    p.append('Published by id8Labs. <a href="https://id8labs.app/shipped">id8labs.app/shipped</a>')
    p.append("</div></div>")

    body = "\n".join(p) + "\n" + SNIPPET.read_text(encoding="utf-8").replace(
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
        f'{links}\n<style>\n{root_css}\n{CSS}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n'
    )


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    content = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = render(content)

    bad = [c for c in ("—", "–") if c in out]
    if bad:
        print(f"dash self-audit FAILED: {bad!r} present; not writing", file=sys.stderr)
        return 1
    if out.count('id="subscribe"') != 1 or "{{SOURCE}}" in out:
        print("subscribe-block audit FAILED", file=sys.stderr)
        return 1

    words = len(re.sub(r"<[^>]+>", " ", out.split('id="subscribe"')[0]).split())
    pathlib.Path(sys.argv[2]).write_text(out, encoding="utf-8")
    print(f"wrote {sys.argv[2]}")
    print("dash self-audit: 0 found")
    print("subscribe block: present, source " + content["source_tag"])
    print(f"word-count (front of book plus log, tags stripped): {words}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
