#!/usr/bin/env python3
"""render-daily.py - the ART desk for Shipped. Daily.

Renders an anthropic-daily markdown issue into the house HTML template
(warm paper, Fraunces, Archivo, orange). Self-contained single file out.

This closes the gap that kept the daily render cloud-only: the engine
(Editor-in-Chief chain) can now render locally and deploy.

Usage:
    render-daily.py <issue.md> [-o out.html]

The chrome (head/CSS/pub-bar/footer shell) is reused verbatim from
src/render/daily-chrome.html so the output is pixel-faithful to the live
house template. Only the article body is regenerated from the markdown.
"""
import re, sys, html, datetime, argparse, os

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = os.path.join(HERE, "..", "src", "render", "daily-chrome.html")

TAG_CLASS = {  # release-log category -> css tag class + label
    "MODEL": "model", "API": "api", "CODE": "code", "SDK": "sdk",
    "SDK-PY": "sdk", "SDK-TS": "sdk", "NEWS": "news", "RESEARCH": "research",
}

def inline(s):
    """Markdown inline -> HTML. Order matters: links, then code, bold, italic."""
    s = s.strip()
    # links [text](url)  (before escaping; capture then placeholder)
    links = []
    def _link(m):
        links.append((m.group(1), m.group(2)))
        return f"\x00L{len(links)-1}\x00"
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link, s)
    # code `x`
    codes = []
    def _code(m):
        codes.append(m.group(1)); return f"\x00C{len(codes)-1}\x00"
    s = re.sub(r"`([^`]+)`", _code, s)
    s = html.escape(s)
    # bold **x**
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    # italic *x*
    s = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\w)", r"<em>\1</em>", s)
    # restore code/links
    for i, c in enumerate(codes):
        s = s.replace(f"\x00C{i}\x00", f"<code>{html.escape(c)}</code>")
    for i, (t, u) in enumerate(links):
        s = s.replace(f"\x00L{i}\x00", f'<a href="{html.escape(u)}">{html.escape(t)}</a>')
    return s

def parse(md):
    # strip frontmatter
    md = re.sub(r"^---.*?---\s*", "", md, flags=re.S)
    lines = md.split("\n")
    doc = {"masthead": "", "dateline": "", "read": "", "lead_label": "The Lead",
           "lead": [], "dig": [], "quiet": [], "log": [], "sources": [], "generated": ""}
    # masthead line: "Shipped. Daily, Tuesday, June 10, 2026"
    for ln in lines[:6]:
        m = re.match(r"Shipped\.\s*Daily,\s*(.+)", ln.strip())
        if m:
            doc["dateline"] = m.group(1).strip(); break
    section = "read"
    cur_dig = None
    cur_cat = None
    cur_entry = None
    i = 0
    # the opening turn = first non-empty paragraph after the masthead line, before first '---'
    body_started = False
    for ln in lines:
        raw = ln.rstrip()
        s = raw.strip()
        if s.startswith("Shipped. Daily,"):
            body_started = True; continue
        if not body_started:
            continue
        if s == "---":
            continue
        if s.startswith("## "):
            h = s[3:].strip().lower()
            if h.startswith("lead"):
                section = "lead"; doc["lead_label"] = "The Lead"
            elif h.startswith("the dig"):
                section = "dig"
            elif h.startswith("quiet"):
                section = "quiet"
            elif h.startswith("release log"):
                section = "log"
            else:
                section = "other"
            continue
        if section == "read":
            if s and not doc["read"]:
                doc["read"] = s
            continue
        if section == "lead":
            if s: doc["lead"].append(s)
            continue
        if section == "dig":
            if s.startswith("### "):
                cur_dig = {"title": s[4:].strip(), "body": []}
                doc["dig"].append(cur_dig)
            elif s and cur_dig is not None:
                cur_dig["body"].append(s)
            continue
        if section == "quiet":
            if s: doc["quiet"].append(s)
            continue
        if section == "log":
            if s.startswith("### "):  # category
                cur_cat = {"name": re.sub(r"^[A-G]\.\s*", "", s[4:].strip()), "entries": []}
                doc["log"].append(cur_cat); cur_entry = None
            elif s.startswith("#### "):  # entry header: date - title ([src](url))
                head = s[5:].strip()
                m = re.match(r"(\d{4}-\d{2}-\d{2})\s*[—-]\s*(.+)", head)
                date, title = (m.group(1), m.group(2)) if m else ("", head)
                lm = re.search(r"\[([^\]]+)\]\(([^)]+)\)\s*$", title)
                url = lm.group(2) if lm else ""
                title = re.sub(r"\s*\(\[[^\]]+\]\([^)]+\)\)\s*$", "", title).strip()
                try:
                    d = datetime.date.fromisoformat(date)
                    dshort = d.strftime("%b %d")
                except Exception:
                    dshort = date
                cur_entry = {"date": dshort, "title": title, "url": url, "tag": "", "body": [], "how": []}
                if cur_cat: cur_cat["entries"].append(cur_entry)
            elif s.startswith("`[") and s.endswith("]`"):
                if cur_entry: cur_entry["tag"] = s.strip("`[]")
            elif s.startswith("**How to use"):
                if cur_entry: cur_entry["how_on"] = True
            elif s:
                if cur_entry is None: continue
                if cur_entry.get("how_on"):
                    cur_entry["how"].append(s)
                else:
                    cur_entry["body"].append(s)
            continue
    # sources + generated from the footer lines
    for ln in lines:
        s = ln.strip()
        m = re.match(r"-\s*(https?://\S+)", s)
        if m: doc["sources"].append(m.group(1))
        g = re.search(r"[Rr]e-?shipped\s+(\S+)|[Gg]enerated\s+(\S+)", s)
    return doc

def render_lead(paras):
    out = []
    for p in paras:
        out.append(f"    <p>{inline(p)}</p>")
    return "\n".join(out)

def render_dig(items):
    blocks = []
    for it in items:
        body = "\n".join(f"    <p>{inline(p)}</p>" for p in it["body"])
        blocks.append(
            f'  <div class="daily-lead-sub">\n'
            f'    <div class="daily-lead-subhead">{inline(it["title"])}</div>\n'
            f'{body}\n  </div>')
    return "\n".join(blocks)

def render_log(cats):
    out = []
    for cat in cats:
        n = len(cat["entries"])
        rel = "release" if n == 1 else "releases"
        entries = []
        for e in cat["entries"]:
            tag = e.get("tag", "")
            tagcls = TAG_CLASS.get(tag.upper(), "code")
            title = f'<a href="{html.escape(e["url"])}">{inline(e["title"])}</a>' if e["url"] else inline(e["title"])
            body = inline(" ".join(e["body"]))
            how = ""
            if e["how"]:
                how = f'\n        <div class="log-entry-how">\n          <b>How to use</b>\n          {inline(" ".join(e["how"]))}\n        </div>'
            entries.append(
                f'    <div class="log-entry">\n'
                f'      <div class="log-entry-left">\n'
                f'        <div class="log-entry-date">{html.escape(e["date"])}</div>\n'
                f'        <span class="log-tag {tagcls}">{html.escape(tag)}</span>\n'
                f'      </div>\n'
                f'      <div>\n'
                f'        <div class="log-entry-title">{title}</div>\n'
                f'        <div class="log-entry-body">{body}</div>{how}\n'
                f'      </div>\n'
                f'    </div>')
        out.append(
            f'<div class="log-section">\n'
            f'  <div class="log-cat-head">\n'
            f'    <div class="log-cat-name">{html.escape(cat["name"])}</div>\n'
            f'    <div class="log-cat-count"><b>{n}</b>&nbsp;{rel}</div>\n'
            f'  </div>\n'
            f'  <div class="log-entries">\n' + "\n\n".join(entries) + "\n  </div>\n</div>")
    return "\n\n".join(out)

def render(md, generated_iso):
    doc = parse(md)
    chrome = open(CHROME, encoding="utf-8").read()
    pre = chrome[:chrome.index('<div class="daily-head">')]
    # patch pub-bar date to the issue dateline (keep it current)
    pre = re.sub(r'(<span class="pub-bar-meta">)[^<]*(</span>)',
                 lambda m: m.group(1) + html.escape(doc["dateline"]) + m.group(2), pre, count=1)
    dig_html = ""
    if doc["dig"]:
        dig_html = (
            '\n<div class="daily-lead">\n'
            '  <div class="daily-lead-label">The Dig</div>\n'
            '  <div class="daily-lead-body">\n' + render_dig(doc["dig"]) + "\n  </div>\n</div>\n")
    quiet_html = "\n".join(f"    <p>{inline(p)}</p>" for p in doc["quiet"])
    src_html = "\n      &nbsp;&#xB7;&nbsp;\n".join(
        f'      <a href="{html.escape(u)}">{html.escape(re.sub("^https?://","",u))}</a>' for u in doc["sources"])
    # extra CSS for the Dig sub-blocks (kept inline, scoped, additive)
    extra_css = (
        "<style>\n.daily-lead-sub{max-width:1280px;margin:0 auto;padding:0 28px 8px}\n"
        ".daily-lead-subhead{font-family:var(--disp);font-style:italic;font-size:23px;"
        "color:var(--ink);margin:28px 0 12px;letter-spacing:-.01em}\n"
        ".daily-lead-sub p{font-family:var(--disp);font-size:19px;line-height:1.66;"
        "color:var(--body);max-width:760px;margin:0 auto 18px;font-variation-settings:'opsz' 14}\n"
        "</style>\n")
    middle = (
        '<div class="daily-head">\n'
        f'  <div class="daily-kicker">Anthropic Daily &nbsp;&#xB7;&nbsp; {html.escape(doc["dateline"].split(",",1)[-1].strip())}</div>\n'
        '  <div class="daily-masthead">Shipped<span class="dot">.</span></div>\n'
        f'  <div class="daily-dateline">Daily &nbsp;&#xB7;&nbsp; {html.escape(doc["dateline"])}</div>\n'
        f'  <div class="daily-read">{inline(doc["read"])}</div>\n'
        '</div>\n\n'
        '<div class="daily-lead">\n'
        f'  <div class="daily-lead-label">{html.escape(doc["lead_label"])}</div>\n'
        '  <div class="daily-lead-body">\n' + render_lead(doc["lead"]) + '\n  </div>\n</div>\n'
        + dig_html + "\n"
        + render_log(doc["log"]) + "\n\n"
        '<div class="quiet-section">\n'
        '  <div class="quiet-head">\n'
        '    <div class="quiet-kicker">Quiet on the Wire</div>\n'
        '    <div class="quiet-title">Watch<em>.</em></div>\n'
        '  </div>\n'
        f'  <div class="quiet-body">\n{quiet_html}\n  </div>\n</div>\n\n'
        '<div class="ornament">&#x2022; &nbsp; &#x2022; &nbsp; &#x2022;</div>\n\n'
        '<footer class="daily-foot">\n'
        '  <div class="daily-foot-inner">\n'
        '    <div class="daily-foot-brand">Shipped<span class="dot">.</span></div>\n'
        '    <div class="daily-foot-meta">\n'
        f'      <div>Generated {html.escape(generated_iso)}</div>\n'
        f'      <div>Anthropic Daily, {html.escape(doc["dateline"].split(",",1)[-1].strip())}</div>\n'
        '      <div><a href="https://id8labs.app/shipped">id8labs.app/shipped</a></div>\n'
        '    </div>\n'
        '    <div class="daily-foot-sources">\n'
        '      <b>Sources used this sweep:</b>\n      &nbsp;\n'
        f'{src_html}\n'
        '    </div>\n'
        '  </div>\n'
        '</footer>'
    )
    return pre.replace("</head>", extra_css + "</head>", 1) + middle + "\n\n</body>\n</html>"

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("md")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--generated", default=None, help="ISO generated stamp")
    a = ap.parse_args()
    md = open(a.md, encoding="utf-8").read()
    gen = a.generated or (os.environ.get("DAILY_GENERATED_ISO") or "")
    out = render(md, gen)
    dest = a.out or os.path.splitext(a.md)[0] + ".html"
    open(dest, "w", encoding="utf-8").write(out)
    print(f"rendered -> {dest} ({len(out)} bytes)")
