#!/usr/bin/env python3
"""
Render a Shipped. Monthly markdown issue into the magazine HTML design.

Reuses the exact <style> block from the weekly magazine template so the
monthly is pixel-consistent with the published issues. Maps the monthly's
sections (Open / Big Three / Landscape / Also Shipped / Quiet / Close /
Release Log) onto the magazine components.

Usage: python3 render-monthly.py <issue.md> <out.html>
"""
import re, html, sys, os

SUBSCRIBE_BLOCK = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "src", "render", "subscribe-block.html"
)


def _subscribe_block():
    """The shared subscribe snippet, bound to the monthly source tag.

    Same file the daily renderer and the backfill script use, so all three
    surfaces stay identical. Returns "" if the snippet is missing rather than
    failing the render — a monthly without a form still beats no monthly.
    """
    if not os.path.exists(SUBSCRIBE_BLOCK):
        return ""
    with open(SUBSCRIBE_BLOCK, encoding="utf-8") as fh:
        return "\n" + fh.read().replace("{{SOURCE}}", "shipped-monthly")

TEMPLATE = "/Users/eddiebelaval/Development/id8/shipped/pipeline/src/render/template.html"

MONTH_NAMES = {
    "01": "January", "02": "February", "03": "March", "04": "April",
    "05": "May", "06": "June", "07": "July", "08": "August",
    "09": "September", "10": "October", "11": "November", "12": "December",
}

TAG_CLASS = {
    "MODEL": "model", "API": "api", "CODE": "code", "APPS": "apps",
    "SDK": "sdk-py", "SDK-PY": "sdk-py", "SDK-TS": "sdk-ts", "SDK-JAVA": "sdk-py",
    "SDK/CLI": "api", "RESEARCH": "research", "RESEARCH/POLICY": "research",
    "NEWS": "news", "DEPRECATION": "deprecation",
}


def inline(s):
    """Convert a span of markdown to HTML (links, code, bold, italics)."""
    s = s.strip()
    # links [text](url)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
               lambda m: '<a href="%s">%s</a>' % (html.escape(m.group(2), quote=True), m.group(1)), s)
    # inline code
    s = re.sub(r'`([^`]+)`', lambda m: '<code>%s</code>' % html.escape(m.group(1)), s)
    # bold
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    # italics (single * not part of **)
    s = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', s)
    return s


def extract_css(tpl):
    """Grab the first (main design-system) <style>...</style> block."""
    m = re.search(r'<style>(.*?)</style>', tpl, re.S)
    return m.group(1) if m else ""


def parse(md):
    """Split frontmatter + body into H2 sections, each with H3 subsections."""
    fm = {}
    fmm = re.match(r'^---\n(.*?)\n---\n(.*)$', md, re.S)
    body = md
    if fmm:
        for line in fmm.group(1).split('\n'):
            if ':' in line:
                k, v = line.split(':', 1)
                fm[k.strip()] = v.strip()
        body = fmm.group(2)

    # Split by H2
    sections = []
    cur = None
    for line in body.split('\n'):
        h2 = re.match(r'^##\s+(.+?)\s*$', line)
        if h2 and not line.startswith('###'):
            if cur:
                sections.append(cur)
            cur = {"name": h2.group(1).strip(), "lines": []}
        elif cur is not None:
            cur["lines"].append(line)
    if cur:
        sections.append(cur)

    # Within each section, split into intro + H3 subsections
    for sec in sections:
        sub = []
        intro = []
        cursub = None
        for line in sec["lines"]:
            h3 = re.match(r'^###\s+(.+?)\s*$', line)
            if h3:
                if cursub:
                    sub.append(cursub)
                cursub = {"name": h3.group(1).strip(), "lines": []}
            elif cursub is not None:
                cursub["lines"].append(line)
            else:
                intro.append(line)
        if cursub:
            sub.append(cursub)
        sec["intro"] = intro
        sec["subs"] = sub
    return fm, sections


def paragraphs(lines):
    """Group lines into prose paragraphs, skipping rules/tables/blank-led notes."""
    out = []
    buf = []
    for line in lines:
        st = line.strip()
        if st == '' or st == '---':
            if buf:
                out.append(' '.join(buf))
                buf = []
            continue
        if st.startswith('|'):  # table row, handled elsewhere
            continue
        buf.append(st)
    if buf:
        out.append(' '.join(buf))
    return out


def find_section(sections, *names):
    for s in sections:
        for n in names:
            if n.lower() in s["name"].lower():
                return s
    return None


def render_prose_block(paras, marginalia, drop=False):
    """A prose-well column with optional drop-cap on first paragraph."""
    ps = []
    for i, p in enumerate(paras):
        cls = ' class="drop-cap drop-cap-orange"' if (drop and i == 0) else ''
        ps.append('<p%s>%s</p>' % (cls, inline(p)))
    return ('<div class="prose-well">'
            '<div class="prose-marginalia">%s</div>'
            '<div class="prose">%s</div>'
            '</div>') % (html.escape(marginalia), '\n'.join(ps))


def parse_table(lines):
    """Return list of [Date, TitleCell, TagCell, OnelinerCell] from a md table."""
    rows = []
    for line in lines:
        st = line.strip()
        if not st.startswith('|'):
            continue
        if re.match(r'^\|[\s:\-|]+\|?$', st):  # separator
            continue
        cells = [c.strip() for c in st.strip('|').split('|')]
        rows.append(cells)
    # drop header row (first)
    return rows[1:] if rows else []


def notes_from(lines):
    """Italic note lines like *Context...* or *[UNVERIFIED]...* under a category."""
    notes = []
    for line in lines:
        st = line.strip()
        if st.startswith('*') and st.endswith('*') and not st.startswith('|'):
            notes.append(st.strip('*').strip())
    return notes


def render_release_entry(cells):
    date = cells[0] if len(cells) > 0 else ''
    title_cell = cells[1] if len(cells) > 1 else ''
    tag_cell = cells[2] if len(cells) > 2 else ''
    summary = cells[3] if len(cells) > 3 else ''
    tag = re.sub(r'[\[\]]', '', tag_cell).strip()
    cls = TAG_CLASS.get(tag.upper(), 'api')
    title_html = inline(title_cell)
    return ('<div class="log-entry">'
            '<div class="log-entry-left">'
            '<span class="log-entry-date">%s</span>'
            '<span class="log-tag %s">%s</span>'
            '</div>'
            '<div><div class="log-entry-title">%s</div>'
            '<div class="log-entry-body">%s</div></div>'
            '</div>') % (html.escape(date), cls, html.escape(tag), title_html, inline(summary))


def main():
    src, out = sys.argv[1], sys.argv[2]
    md = open(src).read()
    tpl = open(TEMPLATE).read()
    css = extract_css(tpl)
    fm, sections = parse(md)

    month = fm.get("month", "")
    yr, mo = (month.split("-") + [""])[:2]
    month_label = "%s %s" % (MONTH_NAMES.get(mo, mo), yr)
    issue_num = fm.get("issue", "M01")
    ship_date = fm.get("ship_date", "")
    cover_line = ""
    # cover line is the **Cover line:** ... in the intro before THE OPEN
    cm = re.search(r'\*\*Cover line:\*\*\s*(.+)', md)
    if cm:
        cover_line = cm.group(1).strip()

    parts = []

    # PUB BAR
    parts.append(
        '<nav class="pub-bar"><div class="pub-bar-left">'
        '<span class="pub-bar-mark">Shipped<span class="dot">.</span></span>'
        '<span class="pub-bar-sep"></span>'
        '<span class="pub-bar-meta">Monthly &middot; what Anthropic shipped, by '
        '<a href="https://id8labs.app" class="pub-bar-link">id8Labs</a></span></div>'
        '<div class="pub-bar-right">'
        '<span class="pub-bar-folio pub-bar-hide-sm">Issue <b>%s</b></span>'
        '<span class="pub-bar-sep pub-bar-hide-sm"></span>'
        '<span class="pub-bar-meta pub-bar-hide-sm">%s</span>'
        '<a href="#subscribe" class="pub-bar-cta">Subscribe</a></div></nav>'
        % (html.escape(issue_num), html.escape(month_label)))

    # COVER
    release_count = 0
    log_sec = find_section(sections, "RELEASE LOG")
    if log_sec:
        for sub in log_sec["subs"]:
            release_count += len(parse_table(sub["lines"]))
    cover_bottom = (
        '<div class="cover-bottom">'
        '<div class="cover-bottom-cell"><span class="cover-bottom-label">Edition</span>'
        '<span class="cover-bottom-val"><b>Monthly</b></span></div>'
        '<div class="cover-bottom-cell"><span class="cover-bottom-label">Lead</span>'
        '<span class="cover-bottom-val">Opus <b>4.8</b></span></div>'
        '<div class="cover-bottom-cell"><span class="cover-bottom-label">Releases logged</span>'
        '<span class="cover-bottom-val"><b>%d</b></span></div>'
        '<div class="cover-bottom-cell"><span class="cover-bottom-label">Period</span>'
        '<span class="cover-bottom-val">%s</span></div></div>'
        % (release_count, html.escape(month_label)))
    parts.append(
        '<section class="cover" id="top"><div class="cover-grid"></div>'
        '<div class="cover-top"><div class="cover-top-left">'
        '<div class="cover-top-kicker">Monthly &nbsp;&middot;&nbsp; Issue <b>#%s</b> &nbsp;&middot;&nbsp; Anthropic</div>'
        '<div class="cover-top-sub">The month in what Anthropic shipped.</div></div>'
        '<div class="cover-top-right"><div><b>%s</b></div><div>Generated %s</div>'
        '<div>id8labs.app/shipped</div></div></div>'
        '<div class="cover-stage"><div class="cover-huge-num">%s</div>'
        '<div class="cover-stack"><span class="masthead-cover">Shipped<span class="dot">.</span></span>'
        '<h1 class="cover-deck">%s</h1>'
        '<p class="cover-deckline">%s &middot; the zoomed-out picture: every release, the big ones called out, '
        'and where the month leaves the landscape.</p></div></div>%s</section>'
        % (html.escape(issue_num), html.escape(month_label), html.escape(ship_date),
           html.escape(mo), inline(cover_line), html.escape(month_label), cover_bottom))

    # THE OPEN
    opn = find_section(sections, "THE OPEN")
    if opn:
        paras = paragraphs(opn["intro"] or opn["lines"])
        quote = paras[0] if paras else ""
        rest = paras[1:]
        rest_html = '\n'.join('<p>%s</p>' % inline(p) for p in rest)
        parts.append(
            '<section class="section open-section"><div class="section-folio">'
            '<div class="section-folio-left"><span class="section-folio-label">The Open</span>'
            '<span class="section-folio-sub">%s</span></div>'
            '<span class="folio"><span class="ruler"></span><b>01</b></span></div>'
            '<div class="open-grid"><div class="open-lead">'
            '<div class="open-quote">%s</div>'
            '<div class="open-prose">%s</div></div>'
            '<div class="open-aside"><b>This issue</b><br>%s<br><br><b>Lead</b><br>Claude Opus 4.8</div>'
            '</div></section>'
            % (html.escape(month_label), inline(quote), rest_html, html.escape(month_label)))

    # THE BIG THREE
    big = find_section(sections, "BIG THREE")
    if big:
        parts.append(
            '<div class="feature-opener"><div class="vert-label">Big Three'
            '<span class="vert-num">01&ndash;03</span></div>'
            '<div class="feature-heading"><div class="feature-kicker">The month\'s defining releases</div>'
            '<h2 class="feature-title">The <em>Big</em> Three</h2>'
            '<p class="feature-deck">Three releases that set the shape of the month.</p></div>'
            '<div class="feature-right"><span class="feature-right-label">Ranked</span>'
            'Capability, capacity, distribution &mdash; in that order.</div></div>')
        for i, sub in enumerate(big["subs"]):
            paras = paragraphs(sub["lines"])
            # heading line as a section folio
            parts.append(
                '<div class="prose-well"><div class="prose-marginalia">%02d</div>'
                '<div class="prose"><div class="open-quote" style="font-size:clamp(28px,3.4vw,44px);'
                'margin-bottom:28px;padding-bottom:20px">%s</div>%s</div></div>'
                % (i + 1, inline(sub["name"]),
                   '\n'.join('<p%s>%s</p>' % (' class="drop-cap"' if j == 0 else '', inline(p))
                             for j, p in enumerate(paras))))
            if i == 0 and paras:
                # a pull-quote after the first big story
                parts.append(
                    '<section class="pq-full"><div class="pq-full-inner">'
                    '<div class="pq-quote-mark">&ldquo;</div><div class="pq-body">'
                    '<div class="pq-text">A frontier model whose marquee feature is that it '
                    '<em>lies to you less.</em></div>'
                    '<div class="pq-att"><span>Claude Opus 4.8</span><b>May 28, 2026</b></div>'
                    '</div></div></section>')

    # THE LANDSCAPE
    land = find_section(sections, "LANDSCAPE")
    if land:
        deck = ""
        intro_paras = paragraphs(land["intro"])
        if intro_paras:
            deck = intro_paras[0]
        parts.append(
            '<div class="feature-opener"><div class="vert-label">Landscape'
            '<span class="vert-num">&infin;</span></div>'
            '<div class="feature-heading"><div class="feature-kicker">Zoomed out</div>'
            '<h2 class="feature-title">The <em>Landscape</em></h2>'
            '<p class="feature-deck">%s</p></div>'
            '<div class="feature-right"><span class="feature-right-label">State of AI</span>'
            'What the month says about where the field is heading.</div></div>'
            % inline(deck or "Where May leaves the field."))
        for sub in land["subs"]:
            paras = paragraphs(sub["lines"])
            parts.append(
                '<div class="prose-well"><div class="prose-marginalia">Essay</div>'
                '<div class="prose"><div class="open-quote" style="font-size:clamp(26px,3vw,40px);'
                'margin-bottom:24px;padding-bottom:18px">%s</div>%s</div></div>'
                % (inline(sub["name"]),
                   '\n'.join('<p>%s</p>' % inline(p) for p in paras)))

    # ALSO SHIPPED
    also = find_section(sections, "ALSO SHIPPED")
    if also:
        parts.append(
            '<section class="section"><div class="section-folio">'
            '<div class="section-folio-left"><span class="section-folio-label">Also Shipped</span>'
            '<span class="section-folio-sub">the rest of the month that mattered</span></div>'
            '<span class="folio"><span class="ruler"></span><b>04</b></span></div>')
        for sub in also["subs"]:
            paras = paragraphs(sub["lines"])
            body = ' '.join(paras)
            parts.append(
                '<div class="sidebar-box accent"><div class="sidebar-box-title">%s</div>'
                '<div class="sidebar-box-body"><p>%s</p></div></div>'
                % (inline(sub["name"]), inline(body)))
        parts.append('</section>')

    # QUIET ON THE WIRE
    quiet = find_section(sections, "QUIET ON THE WIRE")
    if quiet:
        paras = paragraphs(quiet["intro"] or quiet["lines"])
        parts.append(
            '<section class="quiet-section"><div class="quiet-head">'
            '<div class="quiet-kicker">Unconfirmed</div>'
            '<div class="quiet-title">Quiet on the <em>Wire</em></div></div>'
            '<div class="quiet-body">%s</div></section>'
            % '\n'.join('<p>%s</p>' % inline(p) for p in paras))

    # THE CLOSE
    close = find_section(sections, "THE CLOSE")
    if close:
        paras = paragraphs(close["intro"] or close["lines"])
        lines_html = '\n'.join('<div class="close-line">%s</div>' % inline(p) for p in paras[:-1])
        final = paras[-1] if paras else ""
        parts.append(
            '<section class="close-section"><div class="close-kicker">The Close</div>'
            '<div class="close-stack">%s<div class="close-coda-start">'
            '<div class="close-final">%s</div></div></div>'
            '<div class="close-mark">&middot; &middot; &middot;</div></section>'
            % (lines_html, inline(final)))

    # RELEASE LOG
    if log_sec:
        intro_sub = paragraphs(log_sec["intro"])
        sub_blurb = intro_sub[0] if intro_sub else "A 1:1 mirror of every confirmed Anthropic release this month."
        parts.append(
            '<section class="log-divider" id="log"><div class="log-divider-kicker">Back of Book</div>'
            '<h2 class="log-divider-title">The <em>Release</em> Log</h2>'
            '<p class="log-divider-sub">%s</p></section>' % inline(sub_blurb))
        for sub in log_sec["subs"]:
            rows = parse_table(sub["lines"])
            notes = notes_from(sub["lines"])
            cat_name = re.sub(r'^[A-H]\.\s*', '', sub["name"])
            entries = '\n'.join(render_release_entry(r) for r in rows)
            notes_html = ''.join(
                '<div class="log-entry-why" style="border-left-color:var(--gray);margin-top:8px">%s</div>'
                % inline(n) for n in notes)
            parts.append(
                '<section class="log-section"><div class="log-cat-head">'
                '<div class="log-cat-name">%s</div>'
                '<div class="log-cat-count"><b>%d</b>%s</div></div>'
                '<div class="log-entries">%s</div>%s</section>'
                % (html.escape(cat_name), len(rows),
                   'entries' if len(rows) != 1 else 'entry', entries, notes_html))

    # COLOPHON
    parts.append(
        '<footer class="colophon"><div class="colophon-inner">'
        '<div class="colophon-mast"><div class="colophon-word">Shipped<span class="dot">.</span></div>'
        '<div class="colophon-tag">Monthly edition. The month-scale read on what Anthropic shipped, '
        'by <a href="https://id8labs.app" class="colophon-link">id8Labs</a>.</div></div>'
        '<div class="colophon-body">'
        '<div class="colophon-col"><h4>Masthead</h4><p><b>Editor</b> Eddie Belaval</p>'
        '<p><b>Reporting</b> with the assistance of Claude</p><p><b>Voice</b> <em>STYLE.md</em></p>'
        '<p><b>Sourcing</b> daily + weekly digests, primary-source research</p></div>'
        '<div class="colophon-col"><h4>Typography</h4><p><b>Display</b> Fraunces</p>'
        '<p><b>Sans</b> Archivo</p><p><b>Narrow</b> Archivo Narrow</p><p><b>Mono</b> JetBrains Mono</p></div>'
        '<div class="colophon-col"><h4>This issue</h4><p><b>Edition</b> Monthly</p>'
        '<p><b>Issue</b> %s</p><p><b>Period</b> %s</p><p><b>Release log</b> %d entries</p>'
        '<p><b>Status</b> Draft</p></div></div>'
        '<div class="colophon-foot"><span>&copy; 2026 <a href="https://id8labs.app" class="colophon-link"><b>id8Labs</b></a> '
        '&nbsp;&middot;&nbsp; All rights reserved</span>'
        '<span>Set in Fraunces &amp; Archivo</span>'
        '<span class="hot">Next edition &mdash; first of next month</span></div></div></footer>'
        % (html.escape(issue_num), html.escape(month_label), release_count))

    doc = (
        '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        '<title>Shipped. Monthly &mdash; %s</title>'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;0,9..144,900;1,9..144,400;1,9..144,500&family=Archivo:wght@300;400;500;600;700;800;900&family=Archivo+Narrow:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
        '<style>%s</style></head><body>%s%s</body></html>'
        % (html.escape(month_label), css, '\n'.join(parts), _subscribe_block()))

    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as f:
        f.write(doc)
    print("wrote %s (%d bytes, %d release-log entries)" % (out, len(doc), release_count))


if __name__ == "__main__":
    main()
