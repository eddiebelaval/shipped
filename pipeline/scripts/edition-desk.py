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
# The cutover: earlier editions keep the look they were published in.
FIRST = {"anthropic-daily": "2026-10-10", "anthropic-weekly": "2026-41", "anthropic-monthly": "2026-10"}
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
                        if p.endswith(".html") and Path(p).stem >= FIRST[s])
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
CHROME_NUMS = {"9", "144"}  # colophon: "Fraunces, optical sizes 9 to 144"
CHROME_PHRASES = re.compile(r"\b(\d+) (?:words|entries|sections|releases in the log)\b|\bReleases (\d+)\b")


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


def link_check(page, source_page, md_text):
    """No link on the page the edition never had (template chrome and in-page anchors excepted)."""
    allowed = set(re.findall(r'href="([^"]+)"', source_page)) | set(re.findall(r"\]\(([^)\s]+)\)", md_text))
    allowed |= CHROME_HREFS
    allowed = allowed | {html.escape(h, quote=True) for h in allowed}
    stray = sorted({h for h in re.findall(r'href="([^"]+)"', page)
                    if h not in allowed and not h.startswith(("#", "data:", PAGES))})
    return [f"link not in the edition: {h[:80]}" for h in stray]


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
    missing, want_links, want_nums = [], {}, {}
    blocks = [(cls, node) for cls in SOURCE_BLOCKS for node in t.root.find_all(cls)]
    ids = {id(n) for _, n in blocks}

    def nested(node):  # a block inside another block is counted with its parent, never twice
        p = node.parent
        while p is not None:
            if id(p) in ids:
                return True
            p = p.parent
        return False

    for cls, node in blocks:
        if cls == "feature-meta":
            units = [sp.text() for sp in node.find_all(tag="span")] or [node.text()]
        elif cls == "feature-right":
            units = node.lines()
        else:
            units = [p.text() for p in node.find_all(tag="p")] or [node.text()]
        for u in units:
            u = re.sub(r"^(How to use|Why it matters):?\s*", "", u)
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
        for n in NUM.findall(node.text()):
            want_nums[n] = want_nums.get(n, 0) + 1
    for href, n in want_links.items():
        got = page.count(f'href="{html.escape(href, quote=True)}"') + (page.count(f'href="{href}"') if html.escape(href, quote=True) != href else 0)
        if got < n:
            missing.append(f"link missing: {href[:80]} (source {n}, page {got})")
    page_nums = {}
    for n in NUM.findall(plain(inside)):
        page_nums[n] = page_nums.get(n, 0) + 1
    for n, c in want_nums.items():
        if page_nums.get(n, 0) < c:
            missing.append(f"figure missing: {n} (source {c}, page {page_nums.get(n, 0)})")
    # A number the routine never printed is a changed figure (chrome numbers come from the source too).
    allowed = set(NUM.findall(plain(source_page) + " " + extra)) | CHROME_NUMS  # extra: running images' captions + credits
    for m in CHROME_PHRASES.finditer(plain(page)):  # counts the template computes (words, entries, sections)
        allowed.add(m.group(1) or m.group(2))
    stray = sorted(n for n in page_nums if n not in allowed)
    if stray:
        missing.append("figures not in the source: " + ", ".join(stray[:8]))
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
        cap = re.search(r"<figcaption[^>]*>([\s\S]*?)</figcaption>", fig)
        want_cap = f"{slots.get(slot, {}).get('caption', '')} {man.get(f, {}).get('credit', '')}"
        if not cap or norm(plain(cap.group(1))) != norm(want_cap):
            problems.append(f"caption or credit wrong for {f}: {want_cap[:60]}")
    return problems


def scope_images(page, stem):
    """Images sit in <section>/img/<stem>/ on the branch, so editions never collide."""
    return page.replace('src="img/', f'src="img/{stem}/').replace('srcset="img/', f'srcset="img/{stem}/')


# ---------------------------------------------------------------- publish

def publish(section, stem, page, img_dir, note):
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
        problems += source_parity((d / "source.html").read_text(), page, image_text(want, d / "images"))
        problems += image_gate(page, want, d / "images")
        md_text = (d / "edition.md").read_text()
        src = (d / "source.html").read_text()
        problems += front_check(split_front(page)[0], src, md_text, image_text(want, d / "images"))
        problems += link_check(page, src, md_text)
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
        live = verify_live(section, stem)
        log(f"  published {section}/{stem} ({note}); live check: {'OK' if live else 'UNVERIFIED'}")
        if not live:
            notify("Shipped. Edition Desk", f"{section}/{stem}: pushed but not live after 5 minutes")
        st["published_images"] = want
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
        if not ours and st.get("source_sha") != source_key(page):
            convert(section, stem, page, st)      # a new edition, or the routine re-published it
        elif not ours:
            st.pop("published_images", None)      # the routine page is live again over ours
        if not (folder(section, stem) / "edition.md").exists():
            return
        if not a.no_images:
            images(section, stem, st)

        want = ready_set(section, stem)  # nothing ships until every drawn image is decided
        if a.retry:
            st.pop("gate_failure", None)
        key = [st.get("source_sha"), want]
        held = st.get("gate_failure", {}).get("key") == key
        if (not ours or st.get("published_images") != want) and not held:
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
    pages = branch_pages()
    todo = [(s, stem) for s in SECTIONS for stem in pages[s]]
    if a.only:
        todo = [t for t in todo if "/".join(t) == a.only]
    for section, stem in todo:
        try:
            process(section, stem, a)
        except Exception as e:  # one bad edition never blocks the others
            log(f"  ESCALATE {section}/{stem}: {e}")
            notify("Shipped. Edition Desk", f"{section}/{stem}: {str(e)[:120]}")
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
    v = sp.add_parser("review")
    v.add_argument("edition")
    sp.add_parser("status")
    a = ap.parse_args()
    {"run": cmd_run, "review": cmd_review, "status": cmd_status}[a.cmd](a)


if __name__ == "__main__":
    main()
