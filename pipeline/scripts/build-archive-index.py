#!/usr/bin/env python3
"""
Shipped. — generate the daily-pages archive index from the branch itself.

Every page published to `daily-pages` is reachable from index.html, because the
index is DERIVED from the directory listing rather than hand-edited. Before
2026-08-05 it was hand-edited: it listed nine dailies, all from May, and had not
been touched since 2026-05-14 while 89 dailies, 12 weeklies, 2 monthlies and a
dispatch accumulated behind it. Roughly 95 published pages had no path in.

Same doctrine as backfill-subscribe.py: enforce at the BRANCH, not at each
generator. Three cloud routines publish here and none of them owns the index.
A derived index cannot go stale, cannot miss a page, and self-heals nightly.

Design tokens are READ OUT of pipeline/src/render/template.html at build time
(the `:root` block, the font link, the favicon) so the palette can never drift
from the single source of design truth. The layout is index-specific on purpose:
the template's component CSS describes a magazine issue, not an archive.

House rule: no em dashes (U+2014) and no en dashes (U+2013) anywhere. Asserted
before write, same as the routines' self-audit.

Usage:
  build-archive-index.py <checkout-root>              write index.html
  build-archive-index.py <checkout-root> --dry-run    report only, write nothing
"""
import argparse
import html
import pathlib
import re
import sys
from datetime import date, datetime, timedelta

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "src" / "render" / "template.html"
SNIPPET = HERE.parent / "src" / "render" / "subscribe-block.html"

SECTIONS = [
    ("anthropic-monthly", "Monthly", "monthly"),
    ("anthropic-weekly", "Weekly", "weekly"),
    ("anthropic-daily", "Daily", "daily"),
]

MONTHS = ("January February March April May June July "
          "August September October November December").split()


# ---------------------------------------------------------------- extraction

def strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def read_meta(text, prop):
    m = re.search(
        r'<meta\s+(?:property|name)=["\']' + re.escape(prop) + r'["\']\s+content=["\'](.*?)["\']',
        text, re.I | re.S)
    return html.unescape(m.group(1)).strip() if m else ""


def first_real_paragraph(text):
    """Fallback hook for the 33 early pages that carry no og:description."""
    body = text.split("</head>", 1)[-1]
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", body, re.S | re.I):
        t = strip_tags(m.group(1))
        # skip mastheads, datelines, nav crumbs, and the subscribe block's copy
        if len(t) >= 90 and "Shipped." not in t[:20] and "reading list" not in t:
            return t
    return ""


def dedash(s):
    """The house rule applies to what THIS page renders, whatever the source did.

    Hooks are lifted from pages published before the no-dash rule existed (the
    May run titles read "Shipped. Daily — May 06, 2026"). Rewriting history is
    not the job; not reprinting it here is.
    """
    return s.replace("—", ",").replace("–", " to ").replace("  ", " ")


def hook_for(text):
    """og:description first, but only when it is actually a sentence.

    Some pages carry a truncated one: 2026-08-04's is the single word "OpenAI".
    Absence was handled; degeneracy was not, so the index printed one-word
    summaries. Anything under 60 characters loses to the page's own opening
    paragraph if that is richer.
    """
    meta = dedash(re.sub(r"\s+", " ",
                         read_meta(text, "og:description")
                         or read_meta(text, "description")).strip())
    h = meta
    # Short, or cut off mid-thought (several are truncated at a word boundary
    # with no terminal punctuation). Either way the page's own opening beats it.
    if len(meta) < 80 or not meta.endswith((".", "!", "?")):
        para = dedash(re.sub(r"\s+", " ", first_real_paragraph(text)).strip())
        if len(para) > len(meta) * 1.25:
            h = para
    if len(h) > 190:
        h = h[:189].rsplit(" ", 1)[0].rstrip(",.;:") + "..."
    return h


def collect(root, subdir):
    d = root / subdir
    if not d.is_dir():
        return []
    out = []
    for page in sorted(d.glob("*.html"), reverse=True):
        text = page.read_text(encoding="utf-8", errors="replace")
        out.append({
            "stem": page.stem,
            "href": f"{subdir}/{page.name}",
            "hook": hook_for(text),
        })
    return out


# ------------------------------------------------------------------- labels

def daily_label(stem):
    try:
        d = date.fromisoformat(stem)
    except ValueError:
        return stem, ""
    return f"{d.day:02d}", d.strftime("%a")


def weekly_label(stem):
    try:
        y, w = stem.split("-")
        mon = date.fromisocalendar(int(y), int(w), 1)
    except (ValueError, TypeError):
        return f"Week {stem}", ""
    fri = mon + timedelta(days=4)
    if mon.month == fri.month:
        span = f"{MONTHS[mon.month - 1]} {mon.day:02d} to {fri.day:02d}"
    else:
        span = f"{MONTHS[mon.month - 1]} {mon.day:02d} to {MONTHS[fri.month - 1]} {fri.day:02d}"
    return f"Week {stem.split('-')[1]}", span


def monthly_label(stem):
    try:
        y, m = stem.split("-")
        return MONTHS[int(m) - 1], y
    except (ValueError, IndexError):
        return stem, ""


# --------------------------------------------------------------- gap report

def gaps(dailies, weeklies, monthlies, today):
    """Ops output only. The public page stays an archive, not a defect list."""
    have = {e["stem"] for e in dailies}
    parsed = sorted(s for s in have if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s))
    if not parsed:
        return []
    first = date.fromisoformat(parsed[0])
    lines = []

    # Stop at yesterday. Today's edition is not late until the 21:00 routine has
    # run, and daily-watchdog.sh already owns that question and pages on it.
    # Two systems reporting the same gap, one of them wrongly before 21:00, is
    # how a real alert gets trained into noise.
    missing, d = [], first
    while d < today:
        if d.isoformat() not in have:
            missing.append(f"{d.isoformat()} {d.strftime('%a')}")
        d += timedelta(days=1)
    if missing:
        lines.append(f"  daily gaps ({len(missing)}): {', '.join(missing)}")

    wk_have = {e["stem"] for e in weeklies}
    wk_missing, seen = [], set()
    d = first
    while d <= today:
        iso = d.isocalendar()
        stem = f"{iso[0]}-{iso[1]:02d}"
        if stem not in wk_have and stem not in seen and d.isoformat() in have:
            # the current week is not late until its Friday routine has fired
            if iso[:2] != today.isocalendar()[:2]:
                wk_missing.append(stem)
            seen.add(stem)
        d += timedelta(days=1)
    if wk_missing:
        lines.append(f"  weekly gaps ({len(wk_missing)}): {', '.join(wk_missing)}")

    mo_have = {e["stem"] for e in monthlies}
    mo_missing = [m for m in sorted({s[:7] for s in parsed})
                  if m not in mo_have and m != today.strftime("%Y-%m")]
    if mo_missing:
        lines.append(f"  monthly gaps ({len(mo_missing)}): {', '.join(mo_missing)}")

    return lines


# ------------------------------------------------------------------- render

def design_tokens():
    """Lift the palette, fonts and favicon out of the canonical template."""
    t = TEMPLATE.read_text(encoding="utf-8")

    root = re.search(r":root\{.*?\n\}", t, re.S)
    if not root:
        raise SystemExit("could not find the :root token block in template.html")

    links = [ln.strip() for ln in t.splitlines()
             if re.search(r'rel="(icon|preconnect|stylesheet)"', ln)]
    if not links:
        raise SystemExit("could not find the font/favicon links in template.html")

    return root.group(0), "\n".join(links)


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{
  background:var(--paper);color:var(--body);
  font-family:var(--sans);font-size:16px;line-height:1.6;
  -webkit-font-smoothing:antialiased;overflow-x:hidden;
}
::selection{background:var(--orange);color:#fff}
body::before{
  content:"";position:fixed;inset:0;pointer-events:none;z-index:1;opacity:.5;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='120' height='120' filter='url(%23n)' opacity='.038'/%3E%3C/svg%3E");
}
.pub-bar{
  position:sticky;top:0;z-index:20;background:var(--ink);color:var(--paper);
  display:flex;align-items:center;justify-content:space-between;gap:1rem;
  padding:.55rem 1.5rem;font-family:var(--narrow);
  font-size:10px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;
}
.pub-bar a{color:var(--paper);text-decoration:none;border-bottom:1px solid var(--orange);padding-bottom:1px}
.pub-bar-right{display:flex;gap:1.25rem;align-items:center}
.wrap{position:relative;z-index:2;max-width:50rem;margin:0 auto;padding:4.5rem 1.5rem 5rem}
.masthead{
  font-family:var(--disp);font-style:italic;font-weight:600;
  font-size:clamp(2.75rem,9vw,4.25rem);line-height:1;letter-spacing:-.03em;
  color:var(--ink);margin-bottom:.75rem;
}
.masthead .dot{color:var(--orange)}
.deck{color:var(--muted);font-size:1.0625rem;max-width:34rem;margin-bottom:.5rem}
.stat{
  font-family:var(--mono);font-size:11px;color:var(--gray);
  letter-spacing:.04em;margin-top:1.25rem;
}
.lede{
  margin:3rem 0 0;padding:1.75rem 0 0;border-top:3px solid var(--ink);
}
.lede-flag{
  font-family:var(--narrow);font-size:10px;font-weight:700;letter-spacing:.22em;
  text-transform:uppercase;color:var(--orange);margin-bottom:.6rem;
}
.lede a{text-decoration:none;color:var(--ink)}
.lede-title{
  font-family:var(--disp);font-size:clamp(1.5rem,4.5vw,2rem);font-weight:600;
  line-height:1.15;letter-spacing:-.02em;margin-bottom:.6rem;
}
.lede a:hover .lede-title{color:var(--orange)}
.lede-hook{color:var(--muted);font-size:1rem;max-width:38rem}
.sec{margin-top:3.5rem}
.sec-head{
  display:flex;align-items:baseline;gap:.75rem;
  padding-bottom:.5rem;border-bottom:2px solid var(--ink);margin-bottom:.25rem;
}
.sec-name{
  font-family:var(--narrow);font-size:11px;font-weight:700;letter-spacing:.22em;
  text-transform:uppercase;color:var(--ink);
}
.sec-count{font-family:var(--mono);font-size:10px;color:var(--gray)}
.grp{
  font-family:var(--narrow);font-size:10px;font-weight:600;letter-spacing:.18em;
  text-transform:uppercase;color:var(--gray);
  padding:1.5rem 0 .4rem;border-bottom:1px solid var(--hair-soft);
}
ul{list-style:none}
li{border-bottom:1px solid var(--hair-soft)}
li a{
  display:grid;grid-template-columns:3.25rem 1fr;gap:1rem;align-items:baseline;
  padding:.7rem 0;text-decoration:none;color:var(--ink);
}
li a:hover{background:var(--paper-shadow)}
.key{
  font-family:var(--mono);font-size:12px;color:var(--orange);
  font-weight:500;white-space:nowrap;
}
.key .sub{color:var(--gray);font-size:10px;margin-left:.3rem}
.title{font-weight:500;font-size:.9375rem;line-height:1.35}
.hook{
  color:var(--muted);font-size:.8125rem;line-height:1.45;margin-top:.15rem;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;
}
.colophon{
  margin-top:4.5rem;padding-top:1.5rem;border-top:1px solid var(--hair);
  font-family:var(--mono);font-size:11px;color:var(--gray);line-height:1.8;
}
.colophon a{color:var(--muted)}
@media (max-width:640px){
  .wrap{padding:3rem 1.15rem 4rem}
  li a{grid-template-columns:2.75rem 1fr;gap:.75rem}
  .pub-bar-hide-sm{display:none}
}
"""


def render(root, dailies, weeklies, monthlies, dispatches, built):
    tokens, links = design_tokens()

    total = len(dailies) + len(weeklies) + len(monthlies) + len(dispatches)
    span = ""
    stems = sorted(e["stem"] for e in dailies)
    if stems:
        try:
            d0 = date.fromisoformat(stems[0])
            span = f"{MONTHS[d0.month - 1]} {d0.day}, {d0.year}"
        except ValueError:
            pass

    p = []
    p.append('<div class="pub-bar">')
    p.append('<span>Shipped. Archive</span>')
    p.append('<span class="pub-bar-right">'
             f'<span class="pub-bar-hide-sm">{total} editions</span>'
             '<a href="#subscribe">Subscribe</a></span>')
    p.append('</div>')
    p.append('<div class="wrap">')
    p.append('<h1 class="masthead">Shipped<span class="dot">.</span></h1>')
    p.append('<p class="deck">The frontier AI labs, every night. Anthropic, OpenAI, '
             'Google DeepMind, Meta AI, Mistral, xAI. Every edition ever published, '
             'in one place.</p>')
    p.append(f'<p class="stat">{total} editions published since {span}</p>'
             if span else f'<p class="stat">{total} editions</p>')

    # The most recent daily gets the front page.
    if dailies:
        top = dailies[0]
        lbl = ""
        try:
            d = date.fromisoformat(top["stem"])
            lbl = f"{d.strftime('%A')}, {MONTHS[d.month - 1]} {d.day:02d}, {d.year}"
        except ValueError:
            lbl = top["stem"]
        p.append('<div class="lede"><div class="lede-flag">Latest edition</div>')
        p.append(f'<a href="{html.escape(top["href"])}">')
        p.append(f'<div class="lede-title">{html.escape(lbl)}</div>')
        if top["hook"]:
            p.append(f'<div class="lede-hook">{html.escape(top["hook"])}</div>')
        p.append('</a></div>')

    def section(name, count, rows):
        p.append('<div class="sec"><div class="sec-head">')
        p.append(f'<span class="sec-name">{name}</span>')
        p.append(f'<span class="sec-count">{count}</span>')
        p.append('</div>')
        p.extend(rows)
        p.append('</div>')

    def row(href, key, sub, title, hook):
        sub_html = f'<span class="sub">{html.escape(sub)}</span>' if sub else ""
        hook_html = f'<div class="hook">{html.escape(hook)}</div>' if hook else ""
        return (f'<li><a href="{html.escape(href)}">'
                f'<span class="key">{html.escape(key)}{sub_html}</span>'
                f'<span><span class="title">{html.escape(title)}</span>{hook_html}</span>'
                f'</a></li>')

    if monthlies:
        rows = ["<ul>"]
        for e in monthlies:
            name, year = monthly_label(e["stem"])
            rows.append(row(e["href"], year or e["stem"], "", f"{name} in review", e["hook"]))
        rows.append("</ul>")
        section("Monthly", f"{len(monthlies)}", rows)

    if weeklies:
        rows = ["<ul>"]
        for e in weeklies:
            wk, span_lbl = weekly_label(e["stem"])
            rows.append(row(e["href"], wk.replace("Week ", "W"), "",
                            span_lbl or wk, e["hook"]))
        rows.append("</ul>")
        section("Weekly", f"{len(weeklies)}", rows)

    if dailies:
        rows = []
        current = None
        for e in dailies:
            month = e["stem"][:7]
            if month != current:
                if current is not None:
                    rows.append("</ul>")
                try:
                    y, m = month.split("-")
                    heading = f"{MONTHS[int(m) - 1]} {y}"
                except (ValueError, IndexError):
                    heading = month
                rows.append(f'<div class="grp">{html.escape(heading)}</div><ul>')
                current = month
            day, wd = daily_label(e["stem"])
            try:
                dd = date.fromisoformat(e["stem"])
                title = f"{dd.strftime('%A')}, {MONTHS[dd.month - 1]} {dd.day:02d}"
            except ValueError:
                title = e["stem"]
            rows.append(row(e["href"], day, wd, title, e["hook"]))
        rows.append("</ul>")
        section("Daily", f"{len(dailies)}", rows)

    if dispatches:
        rows = ["<ul>"]
        for e in dispatches:
            rows.append(row(e["href"], "->", "", e["stem"].replace("-", " ").title(), e["hook"]))
        rows.append("</ul>")
        section("Dispatch", f"{len(dispatches)}", rows)

    snippet = SNIPPET.read_text(encoding="utf-8").replace("{{SOURCE}}", "shipped-archive")

    p.append('<div class="colophon">')
    p.append('Shipped. is published by id8Labs. '
             '<a href="https://id8labs.app/shipped">id8labs.app/shipped</a><br>')
    # Deliberately the newest edition's date, NOT the build date. This file is
    # rebuilt nightly by the branch sweep; stamping "now" would make it differ
    # every single night and commit a no-op, burying real archive changes in
    # daily noise. Derived from content, so it moves only when content moves.
    p.append(f'Archive current through {built}, generated from the daily-pages '
             'branch. Every published page is listed here by construction.')
    p.append('</div>')
    p.append('</div>')

    body = "\n".join(p) + "\n" + snippet

    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<meta name="color-scheme" content="light">\n'
        '<title>Shipped. Archive</title>\n'
        '<meta property="og:title" content="Shipped. Archive">\n'
        '<meta property="og:description" content="Every edition of Shipped., the '
        'frontier AI labs nightly. Anthropic, OpenAI, Google DeepMind, Meta AI, '
        'Mistral, xAI.">\n'
        '<meta property="og:url" content="https://eddiebelaval.github.io/shipped/">\n'
        f'{links}\n'
        f'<style>\n{tokens}\n{CSS}</style>\n'
        '</head>\n<body>\n'
        f'{body}\n'
        '</body>\n</html>\n'
    )


# --------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", help="checkout root holding anthropic-*/ dirs")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--today", default=None, help="override today (YYYY-MM-DD), for tests")
    args = ap.parse_args()

    root = pathlib.Path(args.root)
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 1
    if not TEMPLATE.exists():
        print(f"template not found: {TEMPLATE}", file=sys.stderr)
        return 1
    if not SNIPPET.exists():
        print(f"subscribe snippet not found: {SNIPPET}", file=sys.stderr)
        return 1

    monthlies = collect(root, "anthropic-monthly")
    weeklies = collect(root, "anthropic-weekly")
    dailies = collect(root, "anthropic-daily")

    dispatches = []
    dd = root / "dispatch"
    if dd.is_dir():
        for page in sorted(dd.glob("*/index.html")):
            text = page.read_text(encoding="utf-8", errors="replace")
            dispatches.append({
                "stem": page.parent.name,
                "href": f"dispatch/{page.parent.name}/index.html",
                "hook": hook_for(text),
            })

    total = len(dailies) + len(weeklies) + len(monthlies) + len(dispatches)
    if not total:
        print("no pages found; refusing to write an empty index", file=sys.stderr)
        return 1

    today = date.fromisoformat(args.today) if args.today else datetime.now().date()
    newest = dailies[0]["stem"] if dailies else today.strftime("%Y-%m-%d")
    out = render(root, dailies, weeklies, monthlies, dispatches, newest)

    bad = [c for c in ("—", "–") if c in out]
    if bad:
        print(f"dash self-audit FAILED: {bad!r} present; not writing", file=sys.stderr)
        return 1

    print(f"index: {total} page(s) linked "
          f"(daily {len(dailies)}, weekly {len(weeklies)}, "
          f"monthly {len(monthlies)}, dispatch {len(dispatches)})")
    print("dash self-audit: 0 found")

    report = gaps(dailies, weeklies, monthlies, today)
    if report:
        print("ARCHIVE GAPS (nothing was published for these; index links only what exists):")
        for line in report:
            print(line)
    else:
        print("archive gaps: none")

    if args.dry_run:
        print("dry-run: index.html not written")
        return 0

    (root / "index.html").write_text(out, encoding="utf-8")
    print(f"wrote {root / 'index.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
