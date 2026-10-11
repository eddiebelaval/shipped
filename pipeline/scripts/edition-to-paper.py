"""Shipped. edition page (daily / weekly / monthly) -> paper-layout issue markdown.

The cloud routines publish every edition as HTML in the locked class vocabulary
(issue-chrome.html, audited by the routine's chrome gate). The markdown they
compose is not kept, so the published page is the one durable source. This
reads that page and writes the issue shape the magazine renderer's paper front
(DESIGN.md Rev 6) reads: the first feature is the lead, further features and
the also-items are Also Shipped, quiet / close / release log carry over.

usage: python edition-to-paper.py PAGE_HTML OUT_MD --section anthropic-daily --stem 2026-10-10
Prints a JSON summary (words, stories, log entries) for the parity gate.
"""
import argparse, json, re
from html.parser import HTMLParser

VOID = {"br", "img", "meta", "link", "hr", "input", "source", "wbr", "col", "area", "base", "embed", "param", "track"}
SKIP = {"script", "style", "svg"}
EDITION = {"anthropic-daily": ("Daily Edition", "Daily"), "anthropic-weekly": ("Weekly Edition", "Weekly"),
           "anthropic-monthly": ("Monthly Edition", "Monthly")}
LOG_TAGS = {"MODEL", "API", "CODE", "APPS", "SDK", "SDK-PY", "SDK-TS", "NEWS", "RESEARCH"}


class Node:
    def __init__(self, tag, attrs, parent=None):
        self.tag, self.attrs, self.parent, self.kids = tag, dict(attrs), parent, []

    @property
    def classes(self):
        return (self.attrs.get("class") or "").split()

    def find_all(self, cls=None, tag=None):
        out = []
        for k in self.kids:
            if isinstance(k, Node):
                if (cls is None or cls in k.classes) and (tag is None or k.tag == tag):
                    out.append(k)
                out.extend(k.find_all(cls, tag))
        return out

    def find(self, cls=None, tag=None):
        r = self.find_all(cls, tag)
        return r[0] if r else None

    def lines(self):
        """Text split at <br>, minus any labelled child span (e.g. feature-right-label)."""
        out, cur = [], []
        for k in self.kids:
            if isinstance(k, Node) and k.tag == "br":
                out.append(clean("".join(cur))); cur = []
            elif isinstance(k, Node) and any(c.endswith("-label") for c in k.classes):
                continue
            else:
                cur.append(k if isinstance(k, str) else k.text())
        out.append(clean("".join(cur)))
        return [x for x in out if x]

    def text(self):
        return clean("".join(k if isinstance(k, str) else (" " if k.tag == "br" else k.text()) for k in self.kids))


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = self.cur = Node("root", [])
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        n = Node(tag, attrs, self.cur)
        self.cur.kids.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_endtag(self, tag):
        if tag in SKIP:
            self.skip = max(0, self.skip - 1)
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        if not self.skip:
            self.cur.kids.append(data)


def clean(s):
    return re.sub(r"\s+", " ", s).strip()


def md(node):
    """Inline HTML -> markdown (links, bold, italic, code, line breaks)."""
    if isinstance(node, str):
        return node
    inner = "".join(md(k) for k in node.kids)
    t = node.tag
    if t == "br":
        return " "
    if t == "a" and node.attrs.get("href"):
        return f"[{clean(inner)}]({node.attrs['href']})"
    if t in ("strong", "b"):
        return f"**{clean(inner)}**" if clean(inner) else ""
    if t in ("em", "i"):
        return f"*{clean(inner)}*" if clean(inner) else ""
    if t == "code":
        return f"`{inner}`"
    return inner


def cmd(node):
    return clean(md(node)) if node is not None else ""


def paras(node):
    """Block text of a container: its <p> children, or its own text if it has none."""
    if node is None:
        return []
    ps = [cmd(p) for p in node.find_all(tag="p")]
    ps = [p for p in ps if p]
    return ps or ([cmd(node)] if cmd(node) else [])


def words(s):
    return len(re.findall(r"[A-Za-z0-9][\w'.$%-]*", re.sub(r"\]\([^)]*\)", "]", s)))


def q(s):
    return '"' + s.replace("\\", "").replace('"', "'") + '"'


def next_sibling_prose(fo):
    """The .prose that follows a .feature-opener (inside the next .prose-well)."""
    sibs = [k for k in fo.parent.kids if isinstance(k, Node)]
    for n in sibs[sibs.index(fo) + 1:]:
        if "feature-opener" in n.classes:
            return None
        p = n if "prose" in n.classes else n.find("prose")
        if p is not None:
            return p
    return None


def iso_date(section, stem):
    """A real calendar date for the renderer: the day itself, the week's Friday, the month's last day."""
    import calendar, datetime
    if section == "anthropic-weekly":
        y, w = map(int, stem.split("-"))
        return datetime.date.fromisocalendar(y, w, 5).isoformat()
    if section == "anthropic-monthly":
        y, m = map(int, stem.split("-"))
        return datetime.date(y, m, calendar.monthrange(y, m)[1]).isoformat()
    return stem


def convert(page, section, stem):
    t = Tree(); t.feed(page)
    root = t.root
    body = root.find(tag="body") or root
    edition, short = EDITION[section]

    dateline = {}
    dl = body.find("weekly-dateline")
    for sp in (dl.find_all(tag="span") if dl else []):
        b = sp.find(tag="b")
        if b:
            dateline[b.text().lower()] = clean(sp.text()[len(b.text()):])
    window = dateline.get("window") or dateline.get("week") or dateline.get("month") or stem
    cover_line = cmd(body.find("weekly-cover-line"))
    title_tag = root.find(tag="title")
    title = title_tag.text() if title_tag else f"Shipped. {short}, {stem}"

    oq = body.find("open-quote")
    open_quote = oq.text() if oq else ""  # plain: its <em> nests inside the italic line
    open_paras = paras(body.find("open-prose"))

    stories = []  # (title, deck, paragraphs)
    for fo in body.find_all("feature-opener"):
        ft = fo.find("feature-title")
        lead_in = []
        meta = fo.find("feature-meta")
        if meta is not None:  # the fact box: Source, Area, Disclosure
            parts = [cmd(sp) for sp in meta.find_all(tag="span") if cmd(sp)]
            if not parts:  # routines vary: bare <b> labels, one fact per label
                parts = [x.strip() for x in re.split(r"(?=\*\*[^*]+:\*\*)", cmd(meta)) if x.strip()]
            if parts:
                lead_in.append("*" + " · ".join(parts).replace("*", "") + "*")
        right = fo.find("feature-right")
        if right is not None and right.lines():
            label = right.find("feature-right-label")
            lead_in.append(f"**{label.text() if label else 'By the numbers'}:** " + "; ".join(right.lines()) + ".")
        stories.append((ft.text() if ft else "", cmd(fo.find("feature-deck")), lead_in + paras(next_sibling_prose(fo))))
    for it in body.find_all("also-item"):
        ps = paras(it.find("also-item-body"))
        src = cmd(it.find("also-item-source"))
        if src:
            ps.append(f"*{src.strip('*')}*")
        stories.append((it.find("also-item-title").text() if it.find("also-item-title") else "", "", ps))
    stories = [s for s in stories if s[0] and s[2]]
    if not stories:
        raise SystemExit("edition-to-paper: no feature or also-item with text; refusing to write an empty front")

    quiet = paras(body.find("quiet-body"))
    qt = body.find("quiet-title")
    if quiet and qt is not None and qt.text():
        quiet.insert(0, f"*{qt.text()}*")
    close = [n.text() for n in body.find_all("close-line")] + [n.text() for n in body.find_all("close-final")]

    log_md, letter, n_entries = [], "A", 0
    for sec in body.find_all("log-section"):
        entries = []
        for e in sec.find_all("log-entry"):
            tag_el = next((s for s in e.find_all(tag="span") if "log-tag" in s.classes), None)
            tag = tag_el.text().upper() if tag_el else "NEWS"
            title_el = e.find("log-entry-title")
            a = title_el.find(tag="a") if title_el else None
            date = e.find("log-entry-date").text() if e.find("log-entry-date") else stem
            link = f" ([source]({a.attrs['href']}))" if a is not None and a.attrs.get("href") else ""
            block = [f"#### {date} - {title_el.text() if title_el else 'Untitled'}{link}",
                     f"`[{tag if tag in LOG_TAGS else 'NEWS'}]`", "", cmd(e.find("log-entry-body"))]
            for cls, label in (("log-entry-how", "How to use:"), ("log-entry-why", "Why it matters:")):
                val = re.sub(r"^\*\*[^*]+\*\*\s*", "", cmd(e.find(cls)))
                if val:
                    block += ["", f"**{label}** {val}"]
            entries.append("\n".join(block) + "\n")
        if not entries or letter > "G":
            continue
        n_entries += len(entries)
        deck = sec.find("log-cat-deck")
        cat = sec.find("log-cat-name")
        log_md.append(f"## {letter}. {cat.text() if cat else 'Releases'}\n\n"
                      + (f"*{deck.text()}*\n\n" if deck is not None and deck.text() else "") + "\n".join(entries))
        letter = chr(ord(letter) + 1)

    lead_title, lead_deck, lead_paras = stories[0]
    date = iso_date(section, stem)
    parts = [f"""---
issue: 90
title: {q(title)}
date: {date}
period: {q(window)}
status: published
masthead: Shipped.
layout: paper
edition: {edition}
issue_label: {q(f"{short} · {window}")}
deck: {q(cover_line or lead_deck)}
weather: {q(close[-1] if close else '')}
edition_section: "{section}"
edition_stem: "{stem}"
---
""", "## The Open\n", *([f"*{open_quote.strip('*')}*\n"] if open_quote else []), *[p + "\n" for p in open_paras],
        "## The Lead Story\n", f"# {lead_title}\n", *([f"**{lead_deck.strip('*')}**\n"] if lead_deck else []),
        *[p + "\n" for p in lead_paras]]
    if stories[1:]:
        parts.append("## Also Shipped\n")
        for s_title, s_deck, s_paras in stories[1:]:
            parts += [f"### {s_title}\n", *([f"**{s_deck.strip('*')}**\n"] if s_deck else []), *[p + "\n" for p in s_paras]]
    if quiet:
        parts += ["## Quiet on the Wire\n", *[p + "\n" for p in quiet]]
    if close:
        parts += ["## The Close\n", *[c + "\n" for c in close]]
    parts += log_md
    src_words = sum(words(x) for x in [open_quote, *open_paras, *[p for s in stories for p in s[2]], *quiet, *close])
    return "\n".join(parts), {"title": title, "lead": lead_title, "stories": len(stories) - 1,
                              "log_entries": n_entries, "words": src_words}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page"); ap.add_argument("out")
    ap.add_argument("--section", required=True, choices=sorted(EDITION)); ap.add_argument("--stem", required=True)
    a = ap.parse_args()
    out, summary = convert(open(a.page, encoding="utf-8").read(), a.section, a.stem)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(out)
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
