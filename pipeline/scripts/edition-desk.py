#!/usr/bin/env python3
"""Shipped. Edition Desk: gives every new daily / weekly / monthly the newspaper front.

Eddie's call (2026-10-11): editions get the Rev 6 paper front WITH images, and
each edition's images wait for his approval. The cloud routines stay the
publisher of record and keep publishing on time in the locked chrome; this desk
runs locally after them (launchd, every 30 minutes):

  1. CONVERT   a new routine page on daily-pages -> content/editions/<section>/<stem>/edition.md
  2. IMAGES    image-desk.py finds fresh images for it (pending review)
  3. PUBLISH   the text-only paper front (no image ships unseen), after the parity gate
  4. QC        image-qc.py grades every drawn image against Eddie's bar and
               approves or rejects it (Eddie, 2026-10-11: "i want out of the
               loop here. i need to trust you for QC")
  5. UPGRADE   once every image in the edition is decided, re-render with the
               approved ones and publish again. Rejected slots get one redo
               from the image desk; after that they are dropped.

`review` still opens the human desk for a spot check; it is no longer a gate. The routine page is
kept as source.html, so a failed gate never loses the edition: daily-pages
keeps the routine's page and the desk escalates.

usage:
  edition-desk.py run [--dry-run] [--no-images] [--retry] [--only SECTION/STEM]
  edition-desk.py review SECTION/STEM      open the image review desk for one edition
  edition-desk.py rollback SECTION/STEM    restore the routine's page and pause the edition
  edition-desk.py status
"""
import argparse, datetime, hashlib, html, importlib.util, json, os, re, shutil, subprocess, sys, tempfile, time, urllib.request
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
PIPELINE = SCRIPTS.parent
REPO = PIPELINE.parent
# Data lives in the main checkout even when the code runs from the clean release worktree
# (edition-desk-launch.sh): editions, the image ledger and ops alerts are shared state.
CONTENT = Path(os.environ.get("SHIPPED_CONTENT", REPO / "content"))
OPS = Path(os.environ.get("SHIPPED_OPS", REPO / "ops"))
EDITIONS = CONTENT / "editions"
PAGES = "https://eddiebelaval.github.io/shipped"
LOG = Path.home() / "Library" / "Logs" / "shipped" / "edition-desk.log"
SECTIONS = ("anthropic-daily", "anthropic-weekly", "anthropic-monthly")
# Every edition gets the paper (Eddie, 2026-10-15: "all editions, all issues"). Images start at the
# 2026-10-11 cutover; the archive before it runs text-only (no image desk for 180 back editions).
IMAGES_FROM = {"anthropic-daily": "2026-10-10", "anthropic-weekly": "2026-41", "anthropic-monthly": "2026-10"}
MARKER = '<meta name="shipped-layout" content="paper">'
MAX_REDOS = 1
DASHES = re.compile("[" + chr(0x2014) + chr(0x2013) + "]")


ESCALATIONS = []


def log(msg):
    if "ESCALATE" in msg:
        ESCALATIONS.append(msg.strip())
    line = f"{datetime.datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def git(*args, repo=None, check=False):
    # REPO is read at call time, never bound as a default: a default captured at import let a
    # test that patched REPO push to the real daily-pages (2026-10-11).
    r = subprocess.run(["git", *args], cwd=repo or REPO, capture_output=True, text=True)
    if check and r.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r


def notify(title, message):
    msg = message[:180].replace('"', "'")
    subprocess.run(["osascript", "-e", f'display notification "{msg}" with title "{title}"'], capture_output=True)


# ---------------------------------------------------------------- state

def folder(section, stem):
    return EDITIONS / section / stem


def load_state(section, stem):
    p = folder(section, stem) / "edition.json"
    return json.loads(p.read_text()) if p.exists() else {}


def save_state(section, stem, st):
    p = folder(section, stem) / "edition.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(st, indent=1) + "\n")


def branch_pages():
    git("fetch", "origin", "daily-pages", "--quiet")
    out = {}
    for s in SECTIONS:
        r = git("ls-tree", "--name-only", "origin/daily-pages", s + "/")
        out[s] = sorted(Path(p).stem for p in r.stdout.splitlines()
                        if p.endswith(".html") and Path(p).stem[:1].isdigit())
    return out


def blob(section, stem):
    r = git("show", f"origin/daily-pages:{section}/{stem}.html")
    return r.stdout if r.returncode == 0 else ""


# ---------------------------------------------------------------- images

def manifest(section, stem):
    p = folder(section, stem) / "images" / "manifest.json"
    return json.loads(p.read_text()).get("images", {}) if p.exists() else {}


def _press():
    spec = importlib.util.spec_from_file_location("image_press", SCRIPTS / "image-press.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def drawn(section, stem):
    """{file: review status} for the images the front will actually draw (image-press in_use)."""
    m = manifest(section, stem)
    if not m:
        return {}
    files = _press().in_use(str(folder(section, stem) / "images"), {"images": m})
    # A file never rendered is never drawn (the renderer falls back to the atkinson print).
    return {f: m[f].get("review", {}).get("status", "pending") for f in files if f in m}


def image_status(section, stem):
    counts = {"pending": 0, "approved": 0, "rejected": 0}
    for s in drawn(section, stem).values():
        counts[s] = counts.get(s, 0) + 1
    return counts


def ready_set(section, stem):
    """The approved images to publish, or [] while any drawn image is still pending review."""
    d = drawn(section, stem)
    return [] if "pending" in d.values() else sorted(f for f, s in d.items() if s == "approved")


def press_python():
    """An interpreter that can press images (numpy + Pillow); a venv python3 on PATH often cannot."""
    for py in ("/usr/bin/python3", "/opt/homebrew/bin/python3", sys.executable):
        if os.path.exists(py) and subprocess.run([py, "-c", "import numpy, PIL"], capture_output=True).returncode == 0:
            return py
    raise RuntimeError("no python3 with numpy + Pillow for the image press")


def run_image_desk(md):
    cmd = [press_python(), str(SCRIPTS / "image-desk.py"), str(md)]
    if not os.environ.get("OPENAI_API_KEY"):
        cmd.append("--no-generate")  # Wikimedia only; generation needs the key in this job's environment
    try:
        r = subprocess.run(cmd, cwd=PIPELINE, capture_output=True, text=True, timeout=1800)
    except subprocess.TimeoutExpired:
        return False, "timed out after 30 minutes"
    tail = (r.stdout + r.stderr).strip().splitlines()[-3:]
    return r.returncode == 0, " | ".join(tail)


# ---------------------------------------------------------------- render + gate

def render(md, out):
    cmd = ["npx", "tsx", "src/render/edition-cli.ts", str(md), str(out), "--approved-only"]
    r = subprocess.run(cmd, cwd=PIPELINE, capture_output=True, text=True, timeout=300)
    if r.returncode:
        raise RuntimeError(f"render failed: {(r.stderr or r.stdout).strip()[-400:]}")


def plain(page):
    page = re.sub(r"<(script|style|svg)[\s\S]*?</\1>", " ", page)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", page)))


def norm(s):
    """Letters and digits only: inline tags and punctuation spacing never decide a match."""
    return re.sub(r"[^a-z0-9]", "", html.unescape(s).lower())


def parity_gate(md_text, page):
    """Every paragraph and log title of the edition must reach the page, and the house rules hold."""
    problems = []
    text = norm(plain(page))
    for block in re.split(r"\n\s*\n", md_text.split("---", 2)[2]):
        b = block.strip()
        if not b or b.startswith(("## ", "`[")):
            continue
        if b.startswith("#### "):
            title = re.sub(r"^#### \S+ - ", "", b.splitlines()[0])
            title = re.sub(r"\s*\(\[source\]\([^)]*\)\)\s*$", "", title)
            if norm(title) not in text:
                problems.append(f"log entry missing: {title[:60]}")
            continue
        b = re.sub(r"^\*\*(How to use|Why it matters):\*\*\s*", "", b)  # the page sets these labels apart
        flat = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", b)
        flat = re.sub(r"^#+ |[*`]", "", flat).strip()
        if norm(flat) and norm(flat) not in text:
            problems.append(f"text missing: {flat[:60]}")
    for href in re.findall(r"\]\(([^)\s]+)\)", md_text.split("---", 2)[2]):
        if f'href="{href}"' not in page and f'href="{html.escape(href, quote=True)}"' not in page:
            problems.append(f"link missing: {href[:80]}")
    if DASHES.search(page):
        problems.append("em/en dash on the page")
    forms = page.count('id="subscribe"')
    if forms != 1:
        problems.append(f"{forms} subscribe forms, expected 1")
    if "id8labs.app/api/newsletter/subscribe" not in page:
        problems.append("subscribe POST url missing")
    if MARKER not in page:
        problems.append("paper layout marker missing")
    if "<title>" not in page:
        problems.append("no <title>")
    return problems


# Content blocks of a routine page, in its locked class vocabulary. Kickers, folios and the
# colophon are chrome the paper redraws; everything here is the edition's own words.
SOURCE_BLOCKS = ("weekly-cover-line", "open-quote", "open-prose", "feature-title", "feature-deck", "feature-meta",
                 "feature-right", "prose", "also-item-title", "also-item-body", "also-item-source", "quiet-title",
                 "quiet-body", "close-line", "close-final", "log-cat-name", "log-entry-title", "log-entry-body",
                 "log-entry-how", "log-entry-why")


NUM = re.compile(r"(?<![\w.])\$?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?")
# Numbers the paper template prints on every edition (page folios, the wordmark's year line, counts the
# template computes). Measured from renders; a figure outside source + this set is a changed figure.
CHROME_HREFS = set(re.findall(r'href="(https?://[^"{]+)"', (PIPELINE / "src" / "render" / "template.html").read_text()
                                + (PIPELINE / "src" / "render" / "subscribe-block.html").read_text()))
CHROME_NUMS = {"9", "144", "4"}  # colophon: "Fraunces, optical sizes 9 to 144", "DESIGN.md (Rev 4)"
CHROME_PHRASES = re.compile(r"\b(\d+) (?:words|entries|sections|releases in the log)\b|\bReleases (\d+)\b|\b(0\d) Report by\b|\b(1):1 mirror\b")


FRONT_ONLY = {"weekly-cover-line"}
FRONT_OPEN = '<section class="pf" id="top">'
FRONT_CLOSE = "</section>\n<script>(function(){function f(){"
FRONT_CHROME = re.compile(r'<div class="pf-ears">[\s\S]*?</div>|<(figure|nav)\b[\s\S]*?</\1>|<(?:div|span|p|a) class="pf-(?:ears|motto|flag|kick|sect|jump[^"]*|pin|more|tag)"[\s\S]*?</(?:div|span|p|a)>'
                          r'|<style[\s\S]*?</style>|<b>\d\d-\d\d</b>')


def split_front(page):
    """(front, inside): the paper front section, and the rest of the page."""
    i = page.find(FRONT_OPEN)
    j = page.find(FRONT_CLOSE, i)
    if i < 0 or j < 0:
        return "", page
    return page[i:j], page[:i] + page[j:]


def front_lines(front):
    """The edition's words on the front (headline, deck, teasers, log titles), chrome and figures removed."""
    body = FRONT_CHROME.sub(" ", front)
    body = re.sub(r"</(p|h\d|div|li|a|article|aside|header)>|<br\s*/?>", "\n", body)
    return [ln for ln in (re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip() for x in body.split("\n")) if ln]


def front_check(front, source_page, md_text, extra=""):
    """Every line on the front must be the edition's own words, verbatim (a teaser is a prefix of its paragraph)."""
    allowed = norm(plain(source_page)) + "|" + norm(md_text.split("---", 2)[-1]) + "|" + norm(extra)
    return [f"front line not in the edition: {ln[:70]}" for ln in front_lines(front) if norm(ln) and norm(ln) not in allowed]


def md_plain(s):
    return re.sub(r"[*`]", "", re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)).strip()


def edition_parts(md_text):
    """What the front must show, read from edition.md: lead, deck, weather, stories, log entries."""
    head, body = md_text.split("---", 2)[1:]
    fm = {k: v.strip().strip('"') for k, v in re.findall(r"^(\w+):\s*(.*)$", head, re.M)}
    secs = {m.group(1).strip(): m.group(2) for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", body, re.M | re.S)}
    lead = secs.get("The Lead Story", "")
    lead_title = next((l[2:].strip() for l in lead.splitlines() if l.startswith("# ")), "")
    lead_body = lead.split(f"# {lead_title}", 1)[-1]
    stories = [(c.partition("\n")[0].strip(), c.partition("\n")[2]) for c in re.split(r"^### ", secs.get("Also Shipped", ""), flags=re.M)[1:]]
    log = re.findall(r"^#### (\S+) - (.+?)(?: \(\[source\]\([^)]*\)\))?\n`\[([A-Z-]+)\]`", body, re.M)
    return fm, lead_title, lead_body, stories, log


def front_structure(front, md_text):
    """The front, slot by slot, against edition.md: headline, deck, weather, each teaser under its own
    title, the log box rows in the renderer's order, the counts and the date in the ears."""
    fm, lead_title, lead_body, stories, log = edition_parts(md_text)
    p = []
    txt = lambda frag: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", frag))).strip()
    one = lambda pat: (re.search(pat, front, re.S) or [None, ""])[1]
    if norm(txt(one(r'<header class="pf-head">.*?<h2>(.*?)</h2>'))) != norm(md_plain(lead_title)):
        p.append("front headline is not the lead's")
    if fm.get("deck") and norm(txt(one(r'<p class="pf-deck">(.*?)</p>'))) != norm(md_plain(fm["deck"])):
        p.append("front deck differs")
    if fm.get("weather") and norm(txt(one(r'<p class="pf-weather">(.*?)</p>'))) != norm(md_plain(fm["weather"])):
        p.append("front weather line differs")
    teaser = norm(txt(one(r'<div class="pf-body">(.*?)</div>\s*(?:<a class="pf-jump|</article>)')))
    if not teaser or not norm(md_plain(lead_body)).startswith(teaser):
        p.append("lead teaser is not the start of the lead story")
    blocks = re.findall(r'<div class="pf-story">(.*?)</div>\s*(?:<a class="pf-jump" href="#also">Continued inside</a>\s*)?</div>', front, re.S)
    if len(blocks) != min(3, len(stories)):
        p.append(f"front shows {len(blocks)} stories, edition has {min(3, len(stories))} for the front")
    for (title, body), blk in zip(stories, blocks):
        if norm(txt(one_in(blk, r"<h3>(.*?)</h3>"))) != norm(md_plain(title)):
            p.append(f"story headline out of place: {title[:50]}")
        t = norm(txt(one_in(blk, r'<div class="pf-sm">(.*)')))
        if not t or not norm(md_plain(body)).startswith(t):
            p.append(f"teaser is not the start of its own story: {title[:50]}")
    inside_titles = [txt(x) for x in re.findall(r'<a href="#also">(.*?)</a>', one(r'<div class="pf-inside">(.*?)</div>'))]
    if [norm(x) for x in inside_titles] != [norm(md_plain(t)) for t, _ in stories[3:]]:
        p.append("Also inside list differs")
    rows = [(d, norm(txt(t)), g) for d, t, g in re.findall(r'<div class="pf-row"><b>([^<]*)</b>(.*?)<span class="pf-tag">([^<]*)</span></div>', front, re.S)]
    want_rows = [(d[5:], norm(md_plain(t)), g) for d, t, g in sorted(log, key=lambda e: e[0], reverse=True)[:6]]
    if rows != want_rows:
        p.append("log box rows differ from the release log")
    n = len(log)
    if f"All {n} entries" not in front or f"{n} releases in the log" not in front:
        p.append(f"log counts differ (edition has {n})")
    try:
        import datetime as _dt
        d = _dt.date.fromisoformat(fm.get("date", ""))
        if f"{d.strftime('%b')} {d.day}, {d.year}" not in txt(one(r'<div class="pf-ears">(.*?)</div>')):
            p.append("ears date differs")
    except ValueError:
        p.append("edition date unreadable")
    return p


def one_in(fragment, pat):
    m = re.search(pat, fragment, re.S)
    return m.group(1) if m else ""


def md_sections(md_text):
    body = md_text.split("---", 2)[2]
    return {m.group(1).strip(): m.group(2) for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", body, re.M | re.S)}


def md_paras(text):
    return [norm(md_plain(b)) for b in re.split(r"\n\s*\n", text.strip()) if b.strip() and norm(md_plain(b))]


def md_log(md_text):
    """[(date, title, url, tag, body, how, why)] from the edition's release log, in order."""
    out = []
    for block in re.split(r"^#### ", md_text, flags=re.M)[1:]:
        head, _, rest = block.partition("\n")
        m = re.match(r"(\S+) - (.+?)(?: \(\[source\]\(([^)]+)\)\))?\s*$", head)
        if not m:
            continue
        rest = re.split(r"^## ", rest, flags=re.M)[0]
        tag = (re.search(r"`\[([A-Z-]+)\]`", rest) or [None, ""])[1]
        rest = re.sub(r"`\[[A-Z-]+\]`", "", rest)
        how = (re.search(r"\*\*How to use:\*\* (.*)", rest) or [None, ""])[1]
        why = (re.search(r"\*\*Why it matters:\*\* (.*)", rest) or [None, ""])[1]
        body = re.split(r"\*\*(?:How to use|Why it matters):\*\*", rest)[0]
        out.append((m.group(1), norm(md_plain(m.group(2))), m.group(3) or "", tag.lower(),
                    norm(md_plain(body)), norm(md_plain(how)), norm(md_plain(why))))
    return out


def inside_structure(page, md_text):
    """Read the rendered INSIDE back into its parts and require each to equal edition.md, in order:
    the Open, the lead's paragraphs, every Also Shipped story's title with its own paragraphs, Quiet,
    the Close, and every log entry field by field (date, title, link, tag, body, how, why). Words
    present somewhere are not enough: each must sit under its own title."""
    spec = importlib.util.spec_from_file_location("e2p", SCRIPTS / "edition-to-paper.py")
    e2p = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(e2p)
    _, inside = split_front(page)
    t = e2p.Tree(); t.feed(inside)
    secs = md_sections(md_text)
    ptext = lambda n: norm(n.text())
    probs = []

    lead_md = secs.get("The Lead Story", "")
    title = next((l[2:].strip() for l in lead_md.splitlines() if l.startswith("# ")), "")
    prose = t.root.find("prose")
    if prose is None or [ptext(x) for x in prose.find_all(tag="p")] != md_paras(lead_md.split(f"# {title}", 1)[-1]):
        probs.append("inside lead paragraphs differ from the edition")

    stories, cur = [], None
    for sec in t.root.find_all(tag="section"):
        if "also shipped" in norm(sec.text()[:200]).replace("shipped", " shipped") or "alsoshipped" in norm(sec.text()[:120]):
            pr = sec.find("prose")
            for k in (pr.kids if pr is not None else []):
                if isinstance(k, e2p.Node) and k.tag == "h3":
                    cur = [norm(k.text().rstrip(".")), []]; stories.append(cur)
                elif isinstance(k, e2p.Node) and k.tag == "p" and cur is not None:
                    cur[1].append(ptext(k))
            break
    want = [[norm(md_plain(c.partition("\n")[0].strip().rstrip("."))), md_paras(c.partition("\n")[2])]
            for c in re.split(r"^### ", secs.get("Also Shipped", ""), flags=re.M)[1:]]
    if stories != want:
        probs.append("inside Also Shipped differs (a body under the wrong title, or a story changed)")

    qb = t.root.find("quiet-body")
    if secs.get("Quiet on the Wire") and (qb is None or [ptext(x) for x in qb.find_all(tag="p")] != md_paras(secs["Quiet on the Wire"])):
        probs.append("inside Quiet on the Wire differs")
    cl = [ptext(x) for x in t.root.find_all("close-line")]
    if secs.get("The Close") and cl != md_paras(secs["The Close"]):
        probs.append("inside Close differs")

    got = []
    for e in t.root.find_all("log-entry"):
        d = re.sub(r"\D", "", e.find("log-entry-date").text()) if e.find("log-entry-date") else ""
        tl = e.find("log-entry-title")
        a = tl.find(tag="a") if tl is not None else None
        tg = next((x.text() for x in e.find_all(tag="span") if "log-tag" in x.classes), "")
        how = re.sub(r"^How to use:?", "", e.find("log-entry-how").text()) if e.find("log-entry-how") else ""
        why = re.sub(r"^Why it matters:?", "", e.find("log-entry-why").text()) if e.find("log-entry-why") else ""
        got.append((d, ptext(tl) if tl else "", (a.attrs.get("href", "").lstrip("#") and a.attrs.get("href", "")) if a is not None else "", norm(tg),
                    ptext(e.find("log-entry-body")) if e.find("log-entry-body") else "", norm(how), norm(why)))
    want_log = [(re.sub(r"\D", "", d), ti, u, norm(tg), b, h, w) for d, ti, u, tg, b, h, w in md_log(md_text)]
    if got != want_log:
        bad = next((i for i, (x, y) in enumerate(zip(got, want_log)) if x != y), min(len(got), len(want_log)))
        probs.append(f"inside release log differs at entry {bad + 1} of {len(want_log)}")
    return probs


def link_check(page, source_page, md_text):
    """No link on the page the edition never had (template chrome and in-page anchors excepted)."""
    allowed = set(re.findall(r'href="([^"]+)"', source_page)) | set(re.findall(r"\]\(([^)\s]+)\)", md_text))
    allowed |= CHROME_HREFS
    allowed = allowed | {html.escape(h, quote=True) for h in allowed}
    stray = sorted({h for h in re.findall(r'href="([^"]+)"', page)
                    if h not in allowed and not h.startswith(("#", "data:", PAGES))})
    out = [f"link not in the edition: {h[:80]}" for h in stray]
    # Each link's words must point where the edition pointed them (no "wrong article" swaps).
    pairs = lambda h: {(norm(html.unescape(re.sub(r"<[^>]+>", "", t))), html.unescape(u))
                       for u, t in re.findall(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', h, re.S)}
    ok = pairs(source_page) | {(norm(md_plain(t)), u) for t, u in re.findall(r"\[([^\]]+)\]\(([^)\s]+)\)", md_text)}
    ok |= {(norm(md_plain(t)), u) for t, u in re.findall(r"^#### \S+ - (.+?) \(\[source\]\(([^)]+)\)\)", md_text, re.M)}
    texts = {}
    for t, u in ok:
        texts.setdefault(t, set()).add(u)
    for t, u in pairs(page):
        if t in texts and u not in texts[t] and not u.startswith(("#", PAGES)) and u not in CHROME_HREFS:
            out.append(f"link points elsewhere: '{t[:40]}' -> {u[:60]}")
    return out


def source_parity(source_page, page, extra=""):
    """Diff the ROUTINE page against the render: every block's full text (every number) and every link.

    A converter drop or a changed figure cannot hide behind edition.md this way.
    """
    spec = importlib.util.spec_from_file_location("e2p", SCRIPTS / "edition-to-paper.py")
    e2p = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(e2p)
    t = e2p.Tree(); t.feed(source_page)
    front, inside = split_front(page)
    text = norm(plain(inside))  # the teaser repeats paragraphs; the inside must carry every word itself
    full = norm(plain(page))
    missing, want_links, want_nums, want_pairs = [], {}, {}, []
    blocks = [(cls, node) for cls in SOURCE_BLOCKS for node in t.root.find_all(cls)]
    ids = {id(n) for _, n in blocks}

    def nested(node):  # a block inside another block is counted with its parent, never twice
        p = node.parent
        while p is not None:
            if id(p) in ids:
                return True
            p = p.parent
        return False

    def section_of(node):
        p = node.parent
        while p is not None and "log-section" not in p.classes:
            p = p.parent
        return p

    for cls, node in blocks:
        if cls == "log-cat-name" and (section_of(node) is None or section_of(node).find("log-entry") is None):
            continue  # an empty category's name; its note, if any, reads in Quiet
        if cls == "feature-meta":
            units = [sp.text() for sp in node.find_all(tag="span")] or [node.text()]
        elif cls == "feature-right":
            units = node.lines()
        else:
            units = [p.text() for p in node.find_all(tag="p")] or [node.text()]
        for u in units:
            u = re.sub(r"^(How to use|Why it matters):?\s*", "", u)
            if cls == "log-cat-name":
                u = e2p.category_name(u)  # the paper letters its own sections
            # The cover line is the front's deck by design; everything else must be inside.
            scope = full if cls in FRONT_ONLY else text
            if norm(u) and norm(u) not in scope:
                missing.append(f"{cls}: {u[:60]}")
        if nested(node) or cls in FRONT_ONLY:  # nested: counted with the parent; front-only: text checked whole
            continue
        for a in node.find_all(tag="a"):
            href = a.attrs.get("href", "")
            if href:
                want_links[href] = want_links.get(href, 0) + 1
                want_pairs.append((cls, norm(a.text()), href))
        def words(x):  # the block's own words; a kicker or label inside it is furniture the paper redraws
            if isinstance(x, str):
                return x
            if x is not node and e2p.legacy_chrome(x):
                return " "
            return "".join(words(k) if not (isinstance(k, e2p.Node) and k.tag == "br") else " " for k in x.kids)
        for n in NUM.findall(words(node)):
            want_nums[n] = want_nums.get(n, 0) + 1
    # Titles keep the routine's order inside (a swap of two headlines changes no words, only meaning).
    for cls in ("also-item-title", "log-entry-title"):
        pos, last = [], -1
        for node in t.root.find_all(cls):
            k = norm(node.text())
            at = text.find(k, last + 1) if k else -1
            if k and at < 0:
                missing.append(f"{cls} out of order: {node.text()[:50]}")
            last = max(last, at)
    # Presence, not count: the paper folds a linked headline and its source line into one link
    # (10-14 and 10-15 sat in the old design on "source 2, page 1"). A dropped link is still caught.
    for href, n in want_links.items():
        got = page.count(f'href="{html.escape(href, quote=True)}"') + (page.count(f'href="{href}"') if html.escape(href, quote=True) != href else 0)
        if got == 0:
            missing.append(f"link missing: {href[:80]} (source {n}, page {got})")
    # Each link must keep its own words: the same URL surviving elsewhere (the log) does not cover a link
    # dropped from a story. Only a linked headline may fold into its story's source line (10-14, 10-15).
    page_pairs = {(norm(html.unescape(re.sub(r"<[^>]+>", "", t))), html.unescape(u))
                  for u, t in re.findall(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', page, re.S)}
    for cls, text, href in want_pairs:
        # The paper may widen a link (a log title links whole, "Gemini delayed (9to5Google)"), never drop it.
        if not text or any(u == href and text in t for t, u in page_pairs):
            continue
        if cls in ("also-item-title", "feature-title") and any(u == href for _, u in page_pairs):
            continue
        missing.append(f"link dropped from its words: '{text[:40]}' -> {href[:60]}")
    page_nums = {}
    for n in NUM.findall(plain(inside)):
        page_nums[n] = page_nums.get(n, 0) + 1
    for n, c in want_nums.items():
        if page_nums.get(n, 0) < c:
            missing.append(f"figure missing: {n} (source {c}, page {page_nums.get(n, 0)})")
    # A number the routine never printed is a changed figure (chrome numbers come from the source too).
    allowed = set(NUM.findall(plain(source_page) + " " + extra)) | CHROME_NUMS
    allowed |= {str(int(x)) for x in allowed if x.isdigit()}  # "May 06" prints as "May 6"  # extra: running images' captions + credits
    allowed |= set(re.findall(r'class="log-cat-count"><b>(\d+)</b>', page))  # entries per log section
    for m in CHROME_PHRASES.finditer(plain(page)):  # counts the template computes (words, entries, sections)
        allowed.add(next(g for g in m.groups() if g))
    stray = sorted(n for n in page_nums if n not in allowed)
    if stray:
        missing.append("figures not in the source: " + ", ".join(stray[:8]))
    return missing


def source_coverage(source_page, page):
    """Every text block of the routine page reaches the paper, whatever template wrote it (the archive
    from May to August 2026 predates the class vocabulary source_parity reads). Furniture aside."""
    spec = importlib.util.spec_from_file_location("e2p", SCRIPTS / "edition-to-paper.py")
    e2p = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(e2p)
    t = e2p.Tree(); t.feed(source_page)
    text = norm(plain(page))
    missing = []

    # The paper prints these in its own format (ISO dates, the tag set, its own counts); the other gates check them.
    reformatted = re.compile(r"(^|-)(date|tag|tags|count|meta)$")
    refmt = lambda n: any(reformatted.search(c) for c in n.classes)
    has_refmt = lambda n: any(isinstance(k, e2p.Node) and (refmt(k) or has_refmt(k)) for k in n.kids)
    label = re.compile(r"^(How to use|How to|Why it matters)\s*:?\s*")

    def walk(n):
        for k in n.kids:
            if not isinstance(k, e2p.Node) or e2p.legacy_chrome(k) or refmt(k):
                continue
            # A category header is structure (the paper letters its own sections); its entries are checked one by one.
            if e2p.CATEGORY & set(k.classes) or any(isinstance(x, e2p.Node) and any(c.endswith("-letter") for c in x.classes) for x in k.kids):
                continue
            if re.match(r"^\s*sources?\b", k.text(), re.I) and len(k.text()) < 60:
                continue  # a "Sources drawn from" footer heading
            if re.match(r"^\s*(\d+\s+(items?|entries|releases?)|\d+\s+of\s+\d+|[\w.-]+\.[a-z]{2,}[\w/.-]*(\s*·\s*[\w.-]+\.[a-z]{2,}[\w/.-]*)+)\s*$", k.text()):
                continue  # counters ("2 items", "01 of 03") and bare domain lists are furniture
            if re.match(r"^\s*[\w-]+(\.[\w-]+)+\.?[a-z]{2,}\S*\s*·", k.text()) and k.text().count(" · ") >= 2:
                continue  # a page-level "sources" line: domain · domain · ...
            if k.tag == "thead":
                continue  # a log table's column heads
            if k.tag in ("table", "tbody"):
                walk(k)
                continue
            if k.tag in ("p", "li", "h1", "h2", "h3", "h4", "tr") or (not e2p.has_block(k) and not e2p.has_chrome(k) and not has_refmt(k)):
                raw = e2p.category_name(k.text()) if e2p.CATEGORY & set(k.classes) else label.sub("", k.text())
                u = norm(raw)
                if u and u not in text:
                    missing.append(f"source text missing: {k.text()[:60]}")
            else:
                walk(k)
    walk(t.root.find(tag="body") or t.root)
    return missing


def image_text(want, images_dir):
    """Captions and credits of the images that will run: their figures are the image desk's, not the routine's."""
    slots = json.loads((images_dir / "slots.json").read_text()) if (images_dir / "slots.json").exists() else {}
    man = json.loads((images_dir / "manifest.json").read_text()).get("images", {}) if (images_dir / "manifest.json").exists() else {}
    return " ".join(f"{slots.get(f.rsplit('-', 1)[0], {}).get('caption', '')} {man.get(f, {}).get('credit', '')}" for f in want)


def image_gate(page, want, images_dir):
    """Each running image sits in its own figure with its own slot's caption and credit."""
    problems = []
    slots = json.loads((images_dir / "slots.json").read_text()) if (images_dir / "slots.json").exists() else {}
    man = json.loads((images_dir / "manifest.json").read_text()).get("images", {}) if (images_dir / "manifest.json").exists() else {}
    figs = re.findall(r'<figure class="pf-fig[^"]*">([\s\S]*?)</figure>', page)
    for f in want:
        slot = f.rsplit("-", 1)[0]
        fig = next((x for x in figs if f'img/{f}"' in x), None)
        if fig is None:
            problems.append(f"image missing: {f}")
            continue
        others = {g.rsplit("-", 1)[0] for g in re.findall(r'img/([\w-]+\.png)"', fig)} - {slot}
        if others:
            problems.append(f"image {f} shares a figure with {sorted(others)}")
        alt = slots.get(slot, {}).get("alt", "")
        # Compare decoded text: renderers spell an apostrophe &apos;, &#x27; or raw (weekly 2026-41 held on this).
        alts = [html.unescape(a) for a in re.findall(r'<img [^>]*alt="([^"]*)"', fig)]
        if alt and html.unescape(alt) not in alts:
            problems.append(f"alt text wrong for {f}")
        cap = re.search(r"<figcaption[^>]*>([\s\S]*?)</figcaption>", fig)
        want_cap = f"{slots.get(slot, {}).get('caption', '')} {man.get(f, {}).get('credit', '')}"
        if not cap or norm(plain(cap.group(1))) != norm(want_cap):
            problems.append(f"caption or credit wrong for {f}: {want_cap[:60]}")
    return problems


def scope_images(page, stem):
    """Images sit in <section>/img/<stem>/ on the branch, so editions never collide."""
    return page.replace('src="img/', f'src="img/{stem}/').replace('srcset="img/', f'srcset="img/{stem}/')


# ---------------------------------------------------------------- publish

BATCH = None  # run --batch: {"wt": worktree, "done": [(section, stem)]}; one commit and one push for the run


def publish(section, stem, page, img_dir, note):
    if BATCH is not None:  # stage only; cmd_run commits, pushes and verifies the whole batch once
        dest = Path(BATCH["wt"]) / section
        dest.mkdir(parents=True, exist_ok=True)
        (dest / f"{stem}.html").write_text(page)
        tgt = dest / "img" / stem
        if tgt.exists():
            shutil.rmtree(tgt)
        if img_dir.exists() and any(img_dir.iterdir()):
            shutil.copytree(img_dir, tgt)
        BATCH["done"].append((section, stem))
        return True
    wt = tempfile.mkdtemp(prefix="edition-desk-")
    try:
        git("worktree", "add", "-q", "--detach", wt, "origin/daily-pages", check=True)
        dest = Path(wt) / section
        (dest / f"{stem}.html").write_text(page)
        tgt = dest / "img" / stem
        if tgt.exists():
            shutil.rmtree(tgt)
        if img_dir.exists() and any(img_dir.iterdir()):
            shutil.copytree(img_dir, tgt)
        git("add", "-A", section, repo=wt)
        if not git("status", "--porcelain", repo=wt).stdout.strip():
            return True
        git("-c", "user.name=Edition Desk", "-c", "user.email=eb@id8labs.tech", "commit", "-q",
            "-m", f"feat(editions): {section}/{stem} paper front ({note})", repo=wt, check=True)
        r = git("push", "--quiet", "origin", "HEAD:daily-pages", repo=wt)
        if r.returncode:
            raise RuntimeError(f"push failed: {r.stderr.strip()[:200]}")
        return True
    finally:
        git("worktree", "remove", "--force", wt)
        git("worktree", "prune")


def push_batch(batch):
    """One commit and one push for every edition the run staged, then every page checked live."""
    wt, done = batch["wt"], batch["done"]
    git("add", "-A", *SECTIONS, repo=wt)
    if not git("status", "--porcelain", repo=wt).stdout.strip():
        return
    git("-c", "user.name=Edition Desk", "-c", "user.email=eb@id8labs.tech", "commit", "-q",
        "-m", f"feat(editions): {len(done)} editions in the paper front (archive backfill)", repo=wt, check=True)
    r = git("push", "--quiet", "origin", "HEAD:daily-pages", repo=wt)
    if r.returncode:
        raise RuntimeError(f"batch push failed: {r.stderr.strip()[:200]}")
    log(f"  pushed {len(done)} editions in one commit; checking each live")
    pending, deadline = list(done), time.time() + 900
    while pending and time.time() < deadline:
        pending = [(s, t) for s, t in pending if not is_live(s, t)]
        if pending:
            time.sleep(30)
    for s, t in pending:
        log(f"  ESCALATE {s}/{t}: pushed but not live after 15 minutes (PUBLISH UNVERIFIED)")
    log(f"  batch live check: {len(done) - len(pending)}/{len(done)} OK")


def is_live(section, stem):
    try:
        url = f"{PAGES}/{section}/{stem}.html?desk={int(time.time())}"
        return MARKER in urllib.request.urlopen(url, timeout=20).read().decode()
    except Exception:
        return False


def verify_live(section, stem, wait=300):
    url = f"{PAGES}/{section}/{stem}.html?desk={int(time.time())}"
    deadline = time.time() + wait
    while time.time() < deadline:
        try:
            if MARKER in urllib.request.urlopen(url, timeout=20).read().decode():
                return True
        except Exception:
            pass
        time.sleep(20)
    return False


def build(section, stem, st, want, dry):
    """Render with approved images only, gate, publish. Returns True when the page went out."""
    d = folder(section, stem)
    out_dir = Path(tempfile.mkdtemp(prefix="edition-render-"))
    try:
        out = out_dir / "index.html"
        render(d / "edition.md", out)
        page = out.read_text()
        problems = parity_gate((d / "edition.md").read_text(), page)
        # The converter turns the routine's "Oct 14" log dates into ISO dates the template prints as "2026 · 10 · 14".
        log_dates = " ".join(re.findall(r"^#### (\d{4}-\d{2}-\d{2})", (d / "edition.md").read_text(), re.M)).replace("-", " ")
        # The paper prints the edition's own stem ("2026-23") in its ears and brief.
        problems += source_parity((d / "source.html").read_text(), page, image_text(want, d / "images") + " " + log_dates + " " + stem.replace("-", " "))
        problems += source_coverage((d / "source.html").read_text(), page)
        problems += image_gate(page, want, d / "images")
        md_text = (d / "edition.md").read_text()
        src = (d / "source.html").read_text()
        problems += front_check(split_front(page)[0], src, md_text, image_text(want, d / "images"))
        problems += link_check(page, src, md_text)
        problems += front_structure(split_front(page)[0], md_text)
        problems += inside_structure(page, md_text)
        if problems:
            st["gate_failure"] = {"key": [st.get("source_sha"), want], "problems": problems[:10]}
            log(f"  ESCALATE gate held {section}/{stem}: " + "; ".join(problems[:5]))
            notify("Shipped. Edition Desk", f"{section}/{stem}: paper front held, {problems[0]}")
            return False
        imgs = sorted((out_dir / "img").glob("*.png")) if (out_dir / "img").exists() else []
        note = f"{len(imgs)} approved images" if imgs else "text-only, images awaiting review"
        if dry:
            (d / "preview.html").write_text(page)  # relative img/ paths resolve against images/ copies below
            if imgs:
                shutil.copytree(out_dir / "img", d / "img", dirs_exist_ok=True)
            log(f"  [dry-run] gate passed; would publish {section}/{stem} ({note}); preview at {d / 'preview.html'}")
            return False
        publish(section, stem, scope_images(page, stem), out_dir / "img", note)
        live = True if BATCH is not None else verify_live(section, stem)  # a batch verifies after its one push
        log(f"  published {section}/{stem} ({note}); live check: {'OK' if live else 'UNVERIFIED'}")
        if not live:
            log(f"  ESCALATE {section}/{stem}: pushed but not live after 5 minutes (PUBLISH UNVERIFIED)")
            notify("Shipped. Edition Desk", f"{section}/{stem}: pushed but not live after 5 minutes")
        st["published_images"] = want
        st["render_key"] = render_key()
        st["published_at"] = datetime.datetime.now().isoformat(timespec="seconds")
        st.pop("gate_failure", None)
        return True
    finally:
        shutil.rmtree(out_dir, ignore_errors=True)


# ---------------------------------------------------------------- the run

def source_key(page):
    """The routine page plus the converter itself: a converter fix re-converts every edition."""
    conv = (SCRIPTS / "edition-to-paper.py").read_bytes()
    return hashlib.sha256(page.encode() + b"\0" + conv).hexdigest()[:16]


def render_key():
    """The renderer itself (template + render code): a layout fix re-publishes every live edition."""
    h = hashlib.sha256()
    for f in sorted((PIPELINE / "src" / "render").rglob("*")):
        if f.is_file() and f.suffix in (".ts", ".html"):
            h.update(f.read_bytes())
    return h.hexdigest()[:16]


def convert(section, stem, page, st):
    d = folder(section, stem)
    d.mkdir(parents=True, exist_ok=True)
    (d / "source.html").write_text(page)
    r = subprocess.run([sys.executable, str(SCRIPTS / "edition-to-paper.py"), str(d / "source.html"),
                        str(d / "edition.md"), "--section", section, "--stem", stem],
                       capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"convert failed: {r.stderr.strip()[-300:]}")
    summary = json.loads(r.stdout)
    if st.get("lead") and st["lead"] != summary["lead"] and (d / "images").exists():
        shutil.rmtree(d / "images")  # a different lead story gets different pictures
        st.pop("image_attempts", None)
    st.update(source_sha=source_key(page), lead=summary["lead"],
              converted=summary, redos=0)
    st.pop("published_images", None)
    log(f"{section}/{stem}: converted ({summary['stories']} stories, {summary['log_entries']} log entries)")


def images(section, stem, st):
    md = folder(section, stem) / "edition.md"
    counts = image_status(section, stem)
    if not manifest(section, stem) and st.get("image_attempts", 0) < 3:
        st["image_attempts"] = st.get("image_attempts", 0) + 1
        ok, tail = run_image_desk(md)
        log(f"  image desk: {'ok' if ok else 'FAILED'} {tail}")
    elif counts["rejected"] and not counts["pending"] and st.get("redos", 0) < MAX_REDOS:
        st["redos"] = st.get("redos", 0) + 1
        st["qc_attempts"] = 0
        ok, tail = run_image_desk(md)
        log(f"  image desk redo: {'ok' if ok else 'FAILED'} {tail}")
    if image_status(section, stem)["pending"] and st.get("qc_attempts", 0) < 3:
        st["qc_attempts"] = st.get("qc_attempts", 0) + 1
        qc(section, stem, st)


def qc(section, stem, st):
    """Claude QC holds the image gate (Eddie, 2026-10-11: "i want out of the loop here")."""
    spec = importlib.util.spec_from_file_location("image_qc", SCRIPTS / "image-qc.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    try:
        res = mod.review(folder(section, stem) / "images", str(folder(section, stem) / "edition.md"),
                         log=lambda line: log(line))
    except Exception as e:  # images stay pending, the edition stays text-only, the desk says so
        log(f"  ESCALATE image QC failed for {section}/{stem}: {e}")
        notify("Shipped. Edition Desk", f"{section}/{stem}: image QC failed, running text-only")
        return
    st["qc_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    log(f"  image QC: {sum(ok for ok, _ in res.values())} approved, {sum(not ok for ok, _ in res.values())} rejected")


def process(section, stem, a):
    page = blob(section, stem)
    if not page:
        return
    st = load_state(section, stem)
    if st.get("paused"):
        return
    try:
        ours = MARKER in page
        key_now = source_key(page)
        if a.retry:
            st.pop("convert_failure", None)
        if not ours and st.get("convert_failure") == key_now:
            return  # this exact page already failed to convert; it waits for a converter fix or --retry
        if not ours and st.get("source_sha") != key_now:
            try:
                convert(section, stem, page, st)  # a new edition, or the routine re-published it
            except Exception as e:
                # Held once per page version, not re-tried (and re-alerted) every tick (2026-10-12: a
                # daily re-rendered in a retired template failed every run).
                st["convert_failure"] = key_now
                raise RuntimeError(f"convert held: {e}") from e
            st.pop("convert_failure", None)
        elif not ours:
            st.pop("published_images", None)      # the routine page is live again over ours
        if not (folder(section, stem) / "edition.md").exists():
            return
        if not a.no_images and stem >= IMAGES_FROM[section]:
            images(section, stem, st)

        want = ready_set(section, stem)  # nothing ships until every drawn image is decided
        if a.retry:
            st.pop("gate_failure", None)
        key = [st.get("source_sha"), want]
        held = st.get("gate_failure", {}).get("key") == key
        stale = st.get("render_key") != render_key()
        if (not ours or st.get("published_images") != want or stale) and not held:
            log(f"{section}/{stem}: building ({len(want)} approved images)" if want else f"{section}/{stem}: building text-only")
            try:
                build(section, stem, st, want, a.dry_run)
            except Exception as e:  # a failed render or push holds like a failed gate: no retry storm
                st["gate_failure"] = {"key": key, "problems": [f"build failed: {e}"[:300]]}
                raise
    finally:
        # Caps, attempts and holds persist on every exit, or a failing edition retries without limit.
        if folder(section, stem).exists():
            save_state(section, stem, st)


PAUSE = OPS / "EDITION-DESK-PAUSED"
ALERT = OPS / "EDITION-DESK-ALERT.md"


def cmd_run(a):
    if PAUSE.exists():
        log(f"paused ({PAUSE} exists); nothing runs")
        return
    global BATCH
    pages = branch_pages()
    todo = [(s, stem) for s in SECTIONS for stem in pages[s]]
    if a.only:
        todo = [t for t in todo if "/".join(t) == a.only]
    if a.batch and not a.dry_run:
        BATCH = {"wt": tempfile.mkdtemp(prefix="edition-desk-batch-"), "done": []}
        git("worktree", "add", "-q", "--detach", BATCH["wt"], "origin/daily-pages", check=True)
    try:
        for section, stem in todo:
            try:
                process(section, stem, a)
            except Exception as e:  # one bad edition never blocks the others
                log(f"  ESCALATE {section}/{stem}: {e}")
                notify("Shipped. Edition Desk", f"{section}/{stem}: {str(e)[:120]}")
        if BATCH is not None and BATCH["done"]:
            push_batch(BATCH)
    finally:
        if BATCH is not None:
            git("worktree", "remove", "--force", BATCH["wt"])
            git("worktree", "prune")
            BATCH = None
    if a.dry_run:
        return
    # Editions still held keep the alert standing even on a quiet run.
    for sec in SECTIONS:
        for d in sorted((EDITIONS / sec).glob("*")) if (EDITIONS / sec).exists() else []:
            gf = load_state(sec, d.name).get("gate_failure")
            if gf and not any(f"{sec}/{d.name}" in e for e in ESCALATIONS):
                ESCALATIONS.append(f"HELD {sec}/{d.name}: {gf['problems'][0]}")
    # A standing alert Night Desk reads every night: written on escalation, cleared on a clean run.
    if ESCALATIONS:
        ALERT.parent.mkdir(exist_ok=True)
        ALERT.write_text("# Edition Desk alert\n\n" + "\n".join(f"- {e}" for e in ESCALATIONS)
                         + "\n\nRunbook: pipeline/EDITION-DESK.md\n")
    elif ALERT.exists():
        ALERT.unlink()


def cmd_rollback(a):
    """Put the routine's own page back: the newest version of the file without the paper marker.

    Reverting the newest desk commit is wrong in general: a desk revert or a second (image) publish
    sits on top. Restoring the routine's version is right in every case, and the edition is paused
    so the next run cannot re-publish it.
    """
    section, stem = a.edition.split("/")
    path = f"{section}/{stem}.html"
    git("fetch", "origin", "daily-pages", "--quiet", check=True)
    # The routine's page is the newest version WITHOUT the paper marker, whoever committed it: the
    # 23:00 sweep ("Shipped. bot") also rewrites paper pages, so authorship cannot decide it.
    routine = want = None
    for h in git("log", "--format=%H", "origin/daily-pages", "--", path, check=True).stdout.split():
        body = git("show", f"{h}:{path}").stdout
        if body and MARKER not in body:
            routine, want = h, body
            break
    if not routine:
        sys.exit(f"no routine version of {path} on daily-pages")
    live = git("show", f"origin/daily-pages:{path}").stdout
    imgs_live = git("ls-tree", "--name-only", "origin/daily-pages", f"{section}/img/{stem}/").stdout.strip()
    st = load_state(section, stem)
    st["paused"] = True  # first, so no run re-publishes between here and the push
    save_state(section, stem, st)
    if live == want and not imgs_live:
        print(f"{path} already is the routine's page ({routine[:7]}); paused it, nothing to push")
        return
    wt = tempfile.mkdtemp(prefix="edition-rollback-")
    try:
        git("worktree", "add", "-q", "--detach", wt, "origin/daily-pages", check=True)
        (Path(wt) / path).write_text(want)
        if (Path(wt) / section / "img" / stem).exists():
            shutil.rmtree(Path(wt) / section / "img" / stem)
        git("add", "-A", section, repo=wt)
        git("-c", "user.name=Edition Desk", "-c", "user.email=eb@id8labs.tech", "commit", "-q",
            "-m", f"revert(editions): {section}/{stem} back to the routine page ({routine[:7]})", repo=wt, check=True)
        r = git("push", "--quiet", "origin", "HEAD:daily-pages", repo=wt)
        if r.returncode:
            raise RuntimeError(f"push failed: {r.stderr.strip()[:200]}")
        log(f"rolled back {section}/{stem} to {routine[:7]}; edition paused")
    finally:
        git("worktree", "remove", "--force", wt)
        git("worktree", "prune")


def cmd_review(a):
    section, stem = a.edition.split("/")
    imgs = folder(section, stem) / "images"
    if not (imgs / "manifest.json").exists():
        sys.exit(f"no images for {a.edition} yet")
    print(f"Review desk for {a.edition}. Approve or reject every image; "
          "the Edition Desk publishes the approved set on its next run (within 30 minutes).")
    port = free_port()  # a desk left running for another edition must never be the one that opens
    url = f"http://127.0.0.1:{port}"
    subprocess.Popen(["/bin/sh", "-c", f"sleep 2; openfront {url} || open {url}"])
    os.execv(sys.executable, [sys.executable, str(SCRIPTS / "image-press.py"), "serve", str(imgs), "--port", str(port)])


def free_port(start=8794):
    import socket
    for port in range(start, start + 20):
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    raise SystemExit("no free port for the review desk")


def cmd_status(a):
    for s in SECTIONS:
        for d in sorted((EDITIONS / s).glob("*")) if (EDITIONS / s).exists() else []:
            st = load_state(s, d.name)
            c = image_status(s, d.name)
            gate = st.get("gate_failure", {}).get("problems", [""])[0]
            print(f"{s}/{d.name}: published_images={st.get('published_images')} pending={c['pending']} "
                  f"approved={c['approved']} rejected={c['rejected']}" + (f" HELD: {gate}" if gate else ""))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("run")
    r.add_argument("--dry-run", action="store_true")
    r.add_argument("--no-images", action="store_true")
    r.add_argument("--only")
    r.add_argument("--retry", action="store_true", help="re-try editions a failed gate is holding")
    r.add_argument("--batch", action="store_true", help="one commit and one push for the whole run (archive backfill)")
    v = sp.add_parser("review")
    v.add_argument("edition")
    rb = sp.add_parser("rollback", help="restore the routine's page for one edition and pause it")
    rb.add_argument("edition")
    sp.add_parser("status")
    a = ap.parse_args()
    {"run": cmd_run, "review": cmd_review, "status": cmd_status, "rollback": cmd_rollback}[a.cmd](a)


if __name__ == "__main__":
    main()
