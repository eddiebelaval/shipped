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
LOG_TAGS = {"MODEL", "API", "CODE", "APPS", "SDK", "SDK-PY", "SDK-TS", "NEWS", "RESEARCH", "DEPRECATION"}


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


def blocks_in(node):
    out = []
    for k in node.kids:
        if isinstance(k, Node):
            if k.tag in ("p", "li", "h2", "h3", "h4", "h5"):
                out.append(k)
            elif k.tag == "div" and not has_block(k) and k.text() and not legacy_chrome(k):
                out.append(k)  # a text-only div in a story (a sources line) is a paragraph too
            else:
                out.extend(blocks_in(k))
    return out


def paras(node):
    """Block text of a container: its <p> children, or its own text if it has none."""
    if node is None:
        return []
    # <p>, list items and subheads (as a bold line), in reading order
    ps = [f"**{cmd(p).strip('*')}**" if p.tag[0] == "h" and cmd(p) else cmd(p) for p in blocks_in(node)]
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


MONTHS = {m: i for i, m in enumerate(("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"), 1)}


def log_date(raw, stem):
    """A release-log date as YYYY-MM-DD, whatever the routine wrote ("2026-10-12", "Oct 12",
    "October 12, 2026", "10-12"). The renderer only reads ISO dates; anything else rendered an
    empty log (daily 2026-10-12, held by the gate). Year comes from the edition when missing."""
    import datetime
    raw = re.sub(r"\s+", " ", raw).strip()
    ed_year = int(stem[:4])
    tail = stem[5:7] if len(stem) >= 7 and stem[4] == "-" and stem[5:7].isdigit() else ""
    if len(stem) == 7 and tail and int(tail) > 12:  # a weekly stem, YYYY-WW
        ed_month = datetime.date.fromisocalendar(ed_year, int(tail), 5).month
    else:
        ed_month = int(tail) if tail else 12
    m = re.match(r"^(\d{4})-(\d{2})(?:-(\d{2}))?$", raw)
    if m:
        return raw
    m = re.match(r"^([A-Za-z]{3})[a-z]*\.? (\d{1,2})(?:, (\d{4}))?$", raw)
    if m and m.group(1).lower() in MONTHS:
        mo, d = MONTHS[m.group(1).lower()], int(m.group(2))
        y = int(m.group(3)) if m.group(3) else (ed_year - 1 if mo > ed_month + 1 else ed_year)
        return datetime.date(y, mo, d).isoformat()
    m = re.match(r"^(\d{1,2})[-/](\d{1,2})$", raw)
    if m:
        mo, d = int(m.group(1)), int(m.group(2))
        return datetime.date(ed_year - 1 if mo > ed_month + 1 else ed_year, mo, d).isoformat()
    m = re.match(r"^(\d{4}) · (\d{2}) · (\d{2})$", raw)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return iso_date_fallback(stem)


def iso_date_fallback(stem):
    return stem if re.match(r"^\d{4}-\d{2}-\d{2}$", stem) else f"{stem[:4]}-01-01"


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


LOG_HOW = ("log-entry-how", "log-entry-howto", "log-entry-how-to", "how-to-use", "how-to")
LOG_META = ("log-entry-title", "log-entry-date", "log-date", "log-tag", "log-entry-meta", "log-entry-left", "entry-meta",
            "log-entry-why", "tag", "entry-date", "entry-tag") + LOG_HOW


def md_lines(node):
    """Like Node.lines, but each line keeps its links and emphasis as markdown."""
    out, cur = [], []
    for k in node.kids:
        if isinstance(k, Node) and k.tag == "br":
            out.append(clean("".join(cur))); cur = []
        elif isinstance(k, Node) and any(c.endswith("-label") for c in k.classes):
            continue
        else:
            cur.append(md(k))
    out.append(clean("".join(cur)))
    return [x for x in out if x]


def first_of(e, classes):
    return next((e.find(c) for c in classes if e.find(c) is not None), None)


def log_body(e):
    """The entry's own words: every paragraph outside the title, date, tag and how/why lines (so an
    attribution line, 'Reported by ...', stays with its entry)."""
    out = []

    def walk(n):
        for k in n.kids:
            if isinstance(k, Node) and not any(c in LOG_META for c in k.classes):
                if k.tag in ("p", "li") or (not has_block(k) and k.text()):
                    out.append(cmd(k))
                else:
                    walk(k)
    walk(e)
    return [x for x in out if x]


def log_block(e, stem):
    """One release-log entry as edition markdown, whichever template wrote it."""
    tag_el = next((s for s in e.find_all(tag="span") if "log-tag" in s.classes), None)
    tag = tag_el.text().upper() if tag_el else "NEWS"
    title_el = e.find("log-entry-title")
    a = title_el.find(tag="a") if title_el else None
    date_el = first_of(e, ("log-entry-date", "log-date"))
    date = log_date(date_el.text() if date_el is not None else "", stem)
    link = f" ([source]({a.attrs['href']}))" if a is not None and a.attrs.get("href") else ""
    block = [f"#### {date} - {title_el.text() if title_el else 'Untitled'}{link}",
             f"`[{tag if tag in LOG_TAGS else 'NEWS'}]`", "", ""]
    body = []
    hows, whys, extra = [], [], []
    for x in log_body(e):  # a "How to use:" paragraph inside the body is the entry's How line
        lab = norm_label(re.sub(r"[*:].*$", "", x.lstrip("*"))[:20]) if x.startswith(("**How", "How to", "**Why", "Why it")) else ""
        if lab in ("howtouse", "howto"):
            hows.append(how_value(x))
        elif lab == "whyitmatters":
            whys.append(how_value(x))
        else:
            body.append(x)
    block[3] = " ".join(body)
    # Every how/why line, not just the first: a labelled extra ('Key fixes: ...') joins the body.
    for node in [x for x in e.find_all() if set(x.classes) & set(LOG_HOW) | ({"log-entry-why"} & set(x.classes))]:
        raw = cmd(node)
        val = how_value(raw)
        if not val:
            continue
        if "log-entry-why" in node.classes or norm_label(raw[:20]).startswith("whyitmatters"):
            whys.append(val)
        elif val != raw or norm_label(raw[:12]).startswith("howto"):
            hows.append(val)
        else:
            extra.append(val)
    if extra:
        block[3] = " ".join(x for x in [block[3], *extra] if x)
    if hows:
        block += ["", f"**How to use:** {' '.join(hows)}"]
    if whys:
        block += ["", f"**Why it matters:** {' '.join(whys)}"]
    return "\n".join(block) + "\n"


CATEGORY = {"log-cat-name", "log-category-label", "log-category-header", "log-area-header", "log-section-header",
            "area-header", "daily-log-cat-name", "log-cat-title"}


def how_value(text):
    """A how/why line minus a label the paper prints itself; any other label ('Key fixes', 'Install')
    is the edition's own words and stays, as 'Key fixes: ...'."""
    m = re.match(r"^\*\*([^*]+)\*\*:?\s*(.*)$", text) or re.match(r"^(How to use|How to|Why it matters)\s*:?\s*(.*)$", text)
    if not m:
        return text
    label, rest = m.group(1).strip().rstrip(":"), m.group(2)
    if norm_label(label) in ("howtouse", "howto", "whyitmatters"):
        return rest
    return f"{label}: {rest}" if rest else label


def norm_label(s):
    return re.sub(r"[^a-z]", "", s.lower())


def category_name(text):
    """'C · Claude Code' / 'C Claude Code' -> 'Claude Code': the paper letters the sections itself."""
    return re.sub(r"^[A-Z](?:\s*[·.:])?\s+(?=[A-Z])", "", text).strip()


# Page furniture in the archive templates: bars, kickers, folios, forms, asides. Never the edition's words.
LEGACY_CHROME = re.compile(r"^(pub-bar|ship-sub|colophon|footer|labs-bar|lab-chip|log-header|log-divider|log-cat-head|"
                           r"shipped-mark|section-flag|section-folio|masthead-|daily-meta|subscribe|prose-aside|prose-marginalia|"
                           r"cover-top|daily-footer|d-ts|d-sources|source-list|open-aside|aside-item|area-tag|dig-head$|sources-footer|cover-bottom|cover-spine|cover-huge-num|vert-label)"
                           r"|(^|-)(kicker|folio|dateline|count|label|ts)$")
LEGACY_SKIP_TAGS = {"nav", "footer", "form", "button", "title", "script", "style", "svg"}  # not head: a page that never closes <head> holds everything in it
BLOCK_TAGS = {"div", "p", "section", "article", "ul", "ol", "li", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "header", "table"}


def legacy_chrome(n):
    if "dig-item-label" in n.classes or (n.tag in ("h1", "h2", "h3", "h4") and "dig-head" in n.classes):
        return False  # a Dig story's headline, not furniture
    return n.tag in LEGACY_SKIP_TAGS or any(LEGACY_CHROME.search(c) for c in n.classes)


def has_chrome(n):
    return any(isinstance(k, Node) and (legacy_chrome(k) or has_chrome(k)) for k in n.kids)


def is_heading(n):
    if not n.text():
        return False
    if n.tag in ("h1", "h2", "h3", "h4"):
        return True
    if any(c.endswith("title") and not c.startswith("log-") for c in n.classes) or "dig-item-label" in n.classes or "also-item-head" in n.classes:
        return True
    # A paragraph that is nothing but a bold run is a headline (July 2026 prose wells).
    if n.tag == "p":
        kids = [k for k in n.kids if not (isinstance(k, str) and not k.strip())]
        return len(kids) == 1 and isinstance(kids[0], Node) and kids[0].tag in ("strong", "b")
    return False


def has_block(n):
    return any(isinstance(k, Node) and (k.tag in BLOCK_TAGS or has_block(k)) for k in n.kids)


def legacy_units(n, out, ctx):
    """The page's words in reading order: ('h'|'p'|'quiet'|'close'|'log', node, category)."""
    for k in n.kids:
        if not isinstance(k, Node):
            continue
        if legacy_chrome(k):  # a category name can sit inside furniture (log-cat-head)
            c = next((x for x in k.find_all() if CATEGORY & set(x.classes)), None)
            if c is not None and c.text():
                ctx["cat"] = category_name(c.text())
            continue
        cl = set(k.classes)
        if "log-entry" in cl:
            out.append(("log", k, ctx["cat"]))
        elif cl & CATEGORY or (k.tag == "div" and "log-category" in cl and not k.find("log-entry")):
            ctx["cat"] = category_name(k.text()) or ctx["cat"]
        elif "log-cat-deck" in cl:
            out.append(("deck", k, ctx["cat"]))
        elif cl & {"close-line", "close-final"}:
            out.append(("close", k, None))
        elif "quiet-body" in cl or ("quiet" in cl and k.find("quiet-body") is None and not k.find("quiet-title")):
            out.append(("quiet", k, None))
        elif "quiet-title" in cl:
            out.append(("quiet-title", k, None))
        elif is_heading(k):
            out.append(("h", k, None))
        elif k.tag in ("p", "li", "blockquote") or (not has_block(k) and not has_chrome(k) and len(k.text().split()) >= 4):
            out.append(("p", k, None))
        else:
            legacy_units(k, out, ctx)


def dig_stories(body, used):
    out, head, deck = [], [None], [""]

    def walk(n):
        for k in n.kids:
            if isinstance(k, Node) and "section-folio" in k.classes and k.find("section-folio-sub") is not None \
                    and "dig" in (k.find("section-folio-label").text().lower() if k.find("section-folio-label") else ""):
                head[0] = k.find("section-folio-sub").text() or head[0]  # The Dig's headline rides in the folio
            if not isinstance(k, Node) or legacy_chrome(k):
                continue
            cl = set(k.classes)
            if cl & {"feature-opener", "also-item", "log-section", "quiet-section", "quiet-body", "cover", "log-entry"}:
                continue
            if "prose" in cl and id(k) not in used:
                if head[0] is not None and paras(k):
                    out.append((head[0], deck[0], paras(k)))
                    deck[0] = ""
                continue
            if any(c.endswith("-deck") for c in cl) and not cl & {"cover-deck", "feature-deck", "log-cat-deck"}:
                deck[0] = cmd(k)
                continue
            if is_heading(k) and k.tag != "p":
                head[0], deck[0] = k.text(), ""
                continue
            walk(k)
    walk(body)
    return out


def first_sentence(text):
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    head = (m.group(1) if m else text).strip().rstrip(".")  # a headline takes no full stop
    if len(head) > 90:  # a long sentence heads the story with its first clause
        cut = re.match(r"(.{30,90}?)[:;,](\s|$)", head)
        if cut:
            head = cut.group(1).strip()
    return head


def legacy(body, stem):
    units = []
    legacy_units(body, units, {"cat": "Releases"})
    open_paras, stories, quiet, close, cats = [], [], [], [], []
    for kind, n, cat in units:
        if kind == "log":
            if not cats or cats[-1][0] != cat:
                cats.append((cat, []))
            cats[-1][1].append(log_block(n, stem))
        elif kind == "deck":  # a log category's note ("No SDK releases in window") reads in Quiet
            if cmd(n):
                quiet.append(f"*{cat}:* {cmd(n)}")
        elif kind == "close":
            close.append(n.text())
        elif kind == "quiet":
            quiet += paras(n)
        elif kind == "quiet-title":
            quiet.append(f"*{n.text()}*")
        elif kind == "h":
            stories.append([n.text(), "", []])
        elif kind == "p":
            text = cmd(n)
            if text:
                (stories[-1][2] if stories else open_paras).append(text)
    # A headline with nothing under it reads as a line of the story before it.
    kept = []
    for t, d, ps in stories:
        if ps:
            kept.append((t, d, ps))
        elif kept:
            kept[-1][2].append(f"**{t}**")
        else:
            open_paras.append(f"**{t}**")
    stories = kept
    if stories and len(open_paras) >= 3:
        # A lead with no headline of its own (only a "Lead" folio) ahead of headlined stories.
        lead = open_paras[1:]
        open_paras = open_paras[:1]
        stories.insert(0, (first_sentence(re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", lead[0]).replace("*", "")), "", lead))
    if not stories and len(open_paras) >= 2:
        # No headline anywhere: the one-line read stays the Open, the paragraphs after it are the lead.
        lead = open_paras[1:]
        open_paras = open_paras[:1]
        stories = [(first_sentence(re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", lead[0]).replace("*", "")), "", lead)]
    if not stories and cats:
        # A release-log-only day: the first entry leads the front (it stays in the log too).
        top = cats[0][1][0]
        head, _, rest = top.partition("\n")
        m = re.match(r"#### \S+ - (.+?)(?: \(\[source\]\(([^)]+)\)\))?$", head)
        body_md = [x for x in re.sub(r"`\[[A-Z-]+\]`", "", rest).split("\n\n") if x.strip()]
        if m:
            src = [f"*[Source]({m.group(2)})*"] if m.group(2) else []
            stories = [(m.group(1), "", [x.strip() for x in body_md] + src)]
    if not stories and len(open_paras) == 1:
        stories = [(first_sentence(re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", open_paras[0]).replace("*", "")), "", open_paras)]
        open_paras = []
    while len(cats) > 26:  # the renderer letters log sections A to Z; fold the tail into the last
        cat, es = cats.pop()
        cats[-1][1].extend(es)
    log_md = [f"## {chr(ord('A') + i)}. {cat}\n\n" + "\n".join(es) for i, (cat, es) in enumerate(cats)]
    return {"open": open_paras, "stories": stories, "quiet": quiet, "close": close,
            "log_md": log_md, "n_entries": sum(len(es) for _, es in cats)}


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
    cover_line = cmd(body.find("weekly-cover-line")) or cmd(body.find("cover-deck"))
    title_tag = root.find(tag="title")
    title = title_tag.text() if title_tag else f"Shipped. {short}, {stem}"

    oq = body.find("open-quote")
    open_quote = oq.text() if oq else ""  # plain: its <em> nests inside the italic line
    open_paras = paras(body.find("open-prose")) or paras(body.find("open-lead"))
    if not open_paras:  # the one-line read, under the name each archive template gave it
        rd = next((body.find(c) for c in ("the-read-text", "daily-the-read", "daily-read", "daily-lede", "one-liner", "cover-deckline")
                   if body.find(c) is not None), None)
        open_paras = paras(rd)
    dl = body.find("cover-deckline")  # the cover's second line leads the Open
    if dl is not None and cmd(dl) and cmd(dl) not in open_paras:
        open_paras.insert(0, cmd(dl))

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
            lead_in.append(f"**{label.text() if label else 'By the numbers'}:** " + "; ".join(md_lines(right)) + ".")
        stories.append((ft.text() if ft else "", cmd(fo.find("feature-deck")), lead_in + paras(next_sibling_prose(fo))))
    # The Dig (July 2026): secondary stories, each a headline then its own .prose, outside any feature.
    used = {id(next_sibling_prose(fo)) for fo in body.find_all("feature-opener")}
    if stories:  # only beside a feature lead; a page without one reads through legacy()
        stories += dig_stories(body, used)
    for box in body.find_all("sidebar-box"):  # weekly June-July 2026: Also Shipped as sidebar cards
        bt = box.find("sidebar-box-title")
        if bt is not None and bt.text():
            stories.append((bt.text(), "", paras(box.find("sidebar-box-body"))))
    for it in body.find_all("also-item") + body.find_all("also-entry"):
        it_title = first_of(it, ("also-item-title", "also-item-head", "also-entry-title", "also-body-title"))
        bnode = first_of(it, ("also-item-body", "also-entry-body", "also-body"))
        ps = [x for x in paras(bnode) if not (it_title is not None and x == cmd(it_title))]
        src = cmd(it.find("also-item-source"))
        if src:
            ps.append(f"*{src.strip('*')}*")
        # Some routines link the headline itself instead of a source line; keep that link or the parity gate holds.
        a = it_title.find(tag="a") if it_title else None
        href = a.attrs.get("href", "") if a is not None else ""
        if href and href not in src:
            ps.append(f"*[Source]({href})*")
        stories.append((it_title.text() if it_title else "", "", ps))
    stories = [s for s in stories if s[0] and s[2]]

    quiet = paras(body.find("quiet-body"))
    qt = body.find("quiet-title")
    if quiet and qt is not None and qt.text():
        quiet.insert(0, f"*{qt.text()}*")
    close = [n.text() for n in body.find_all("close-line")] + [n.text() for n in body.find_all("close-final")]

    log_md, letter, n_entries = [], "A", 0
    for sec in body.find_all("log-section"):
        entries = [log_block(e, stem) for e in sec.find_all("log-entry")]
        if not entries:  # a quiet category ("0 releases") reads as a line of Quiet on the Wire
            cat, deck = sec.find("log-cat-name"), sec.find("log-cat-deck")
            if cat is not None and cat.text():
                quiet.append(f"*{category_name(cat.text())}:* {cmd(deck)}" if deck is not None and cmd(deck) else f"*{category_name(cat.text())}*")
            continue
        if letter > "Z":  # the paper letters A to Z; a later section's entries join Z
            log_md[-1] += "\n" + "\n".join(entries)
            n_entries += len(entries)
            continue
        n_entries += len(entries)
        deck = sec.find("log-cat-deck")
        cat = sec.find("log-cat-name")
        log_md.append(f"## {letter}. {category_name(cat.text()) if cat else 'Releases'}\n\n"
                      + (f"*{deck.text()}*\n\n" if deck is not None and deck.text() else "") + "\n".join(entries))
        letter = chr(ord(letter) + 1)

    if (not n_entries and body.find("log-entry") is not None) or \
            any(len(sec.find_all("log-cat-name")) > 1 for sec in body.find_all("log-section")):
        # An archive release log outside log-section containers, or several categories in one section.
        leg = legacy(body, stem)
        log_md, n_entries = leg["log_md"], leg["n_entries"]
    linked = lambda tr: len(tr.find_all(tag="td")) >= 3 and tr.find_all(tag="td")[2].find(tag="a") is not None
    log_rows = [tr for tbl in body.find_all(tag="table") if any(linked(r) for r in tbl.find_all(tag="tr"))
                for tr in tbl.find_all(tag="tr") if len(tr.find_all(tag="td")) >= 3]
    if not n_entries and log_rows:  # weeklies 2026-21/22/30: the release log as a table (date, area, release, notes)
        rows = []
        for tr in log_rows:
            td = tr.find_all(tag="td")
            a = td[2].find(tag="a")
            link = f" ([source]({a.attrs['href']}))" if a is not None and a.attrs.get("href") else ""
            tag = td[1].text().upper()
            rows.append(f"#### {log_date(td[0].text(), stem)} - {td[2].text()}{link}\n`[{tag if tag in LOG_TAGS else 'NEWS'}]`\n\n"
                        + (cmd(td[3]) if len(td) > 3 else "") + "\n")
        if rows:
            log_md, n_entries = ["## A. Releases\n\n" + "\n".join(rows)], len(rows)
    if stories and body.find("feature-opener") is None:
        # Also-items but no feature lead: the archive template carries more prose than the also-items;
        # read it generically when that keeps more of the edition's paragraphs.
        leg = legacy(body, stem)
        if sum(len(x[2]) for x in leg["stories"]) + len(leg["open"]) > sum(len(x[2]) for x in stories) + len(open_paras):
            stories = []
    if not stories:
        # An archive page from before the locked template (May to early August 2026): read it generically.
        leg = legacy(body, stem)
        stories, quiet, close = leg["stories"], leg["quiet"] or quiet, leg["close"] or close
        open_quote, open_paras = "", leg["open"] or open_paras
        if not n_entries:
            log_md, n_entries = leg["log_md"], leg["n_entries"]
        if not stories:
            raise SystemExit("edition-to-paper: no feature, also-item, prose or log entry; refusing to write an empty front")

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
