"""Shipped. image press: turn source photos into orange-ink dither art.

Two treatments, one ink (orange on paper):
  atkinson  the everyday treatment, any size, every photo inside the paper
  halftone  riso dot screen, covers and splash openers only, never below MIN_HALFTONE_PX

Every render is exposure-corrected so the ink coverage lands in a legible band,
then logged to manifest.json as PENDING. Nothing publishes until a human has
looked at every image at its real size and approved it.

usage:
  python image-press.py render SRC_DIR OUT_DIR [--halftone name,name] [--width 1200] [--halftone-width 1600]
  python image-press.py review OUT_DIR              writes OUT_DIR/review.html (every image, real size, metrics, credit)
  python image-press.py approve OUT_DIR FILE|all --by NAME [--note TEXT]
  python image-press.py reject OUT_DIR FILE --by NAME --note TEXT
  python image-press.py check OUT_DIR               exit 1 if any image IN USE is pending, rejected, or uncredited (publish gate)
  python image-press.py serve OUT_DIR [--port 8794]  clickable review desk: pick treatment per slot, approve, reject
  python image-press.py pick OUT_DIR SLOT atkinson|halftone

Credits: SRC_DIR/credits.json maps source name -> {credit, license, url}. An image with no
credit entry fails `check`. Dithering does not change a photo's license.
"""
import sys, os, json, math, glob, hashlib, argparse, datetime, html

try:  # render needs numpy + Pillow; check/approve/review run on stock python3 (the publish gate)
    import numpy as np
    from PIL import Image, ImageOps, ImageEnhance
except ImportError:
    np = None

PAPER = (250, 248, 244)
ORANGE = (238, 92, 40)   # a touch deeper than #FF6B35 so it reads as ink
PX = 2                                    # process at 1/PX, upscale nearest so the dot is visible
MIN_HALFTONE_PX = 700                     # halftone turns to mush below this rendered width

# Target ink coverage (share of the frame that is orange). Inside this band a photo stays legible.
TARGET = {"atkinson": 0.42, "halftone": 0.40}
LEGIBLE = (0.25, 0.60)
FLOOD_BLOCK, FLOOD_INK, FLOOD_SHARE = 16, 0.92, 0.18   # >18% of 16px blocks over 92% ink = flooded

# ── tone ──────────────────────────────────────────────────────────────

def load_gray(path, width):
    im = Image.open(path).convert("L")
    im = ImageOps.autocontrast(im, cutoff=1)
    im = ImageEnhance.Contrast(im).enhance(1.2)
    w = width // PX
    h = int(im.height * w / im.width)
    return np.asarray(im.resize((w, h), Image.LANCZOS), float) / 255.0

def gamma_for_mean(g, target_mean):
    """Binary-search a gamma so mean(g ** gamma) hits target_mean (auto exposure)."""
    lo, hi = 0.1, 8.0
    for _ in range(30):
        mid = math.sqrt(lo * hi)
        if (g ** mid).mean() > target_mean: lo = mid
        else: hi = mid
    return math.sqrt(lo * hi)

# ── treatments (return int array, 1 = ink) ────────────────────────────

def atkinson(g):
    g = g.copy(); h, w = g.shape; out = np.zeros(g.shape, dtype=np.uint8)
    for y in range(h):
        row = g[y]
        for x in range(w):
            old = row[x]; ink = old <= 0.5
            out[y, x] = ink
            e = (old - (0.0 if ink else 1.0)) / 8
            if x + 1 < w: row[x+1] += e
            if x + 2 < w: row[x+2] += e
            if y + 1 < h:
                if x > 0: g[y+1, x-1] += e
                g[y+1, x] += e
                if x + 1 < w: g[y+1, x+1] += e
            if y + 2 < h: g[y+2, x] += e
    return out

def halftone(g, cell=4, angle=45):
    h, w = g.shape; a = math.radians(angle)
    yy, xx = np.mgrid[0:h, 0:w]
    u = (xx*math.cos(a) + yy*math.sin(a)) / cell
    v = (-xx*math.sin(a) + yy*math.cos(a)) / cell
    d = np.hypot(u - np.round(u), v - np.round(v))
    r = np.sqrt(np.clip(1 - g, 0, 1)) * 0.72
    return (d < r).astype(np.uint8)

TREAT = {"atkinson": atkinson, "halftone": halftone}

def expose_and_dither(g, kind):
    """Auto exposure: pick a gamma so ink coverage lands on TARGET, then verify and correct once."""
    want = TARGET[kind]
    if kind == "halftone":  # cheap to render, so search gamma directly on measured coverage
        lo, hi = 0.1, 8.0
        for _ in range(24):
            mid = math.sqrt(lo * hi)
            if TREAT[kind](g ** mid).mean() > want: hi = mid
            else: lo = mid
        gam = math.sqrt(lo * hi); ink = TREAT[kind](g ** gam)
        return ink, gam, float(ink.mean())
    mean = 1 - want
    for _ in range(2):
        gam = gamma_for_mean(g, mean)
        ink = TREAT[kind](g ** gam)
        cov = float(ink.mean())
        if abs(cov - want) < 0.04: break
        mean = min(0.95, max(0.05, mean + (cov - want)))   # dithers drift; nudge and retry once
    return ink, gam, cov

# ── checks ────────────────────────────────────────────────────────────

def flags_for(ink, kind, width):
    f = []
    cov = ink.mean()
    if cov < LEGIBLE[0]: f.append(f"washed out: {cov:.0%} ink, under {LEGIBLE[0]:.0%}")
    if cov > LEGIBLE[1]: f.append(f"too heavy: {cov:.0%} ink, over {LEGIBLE[1]:.0%}")
    b = FLOOD_BLOCK // PX
    h, w = (ink.shape[0] // b) * b, (ink.shape[1] // b) * b
    blocks = ink[:h, :w].reshape(h // b, b, w // b, b).mean(axis=(1, 3))
    flooded = float((blocks > FLOOD_INK).mean())
    if flooded > FLOOD_SHARE: f.append(f"flooded: {flooded:.0%} of the frame is solid ink")
    if kind == "halftone" and width < MIN_HALFTONE_PX: f.append(f"halftone under {MIN_HALFTONE_PX}px")
    return f

def paint(ink):
    out = np.where(ink[..., None] == 1, np.array(ORANGE), np.array(PAPER)).astype(np.uint8)
    img = Image.fromarray(out)
    return img.resize((img.width * PX, img.height * PX), Image.NEAREST)

def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]

# ── manifest ──────────────────────────────────────────────────────────

def load_manifest(out):
    p = os.path.join(out, "manifest.json")
    return json.load(open(p)) if os.path.exists(p) else {"images": {}}

def save_manifest(out, m):
    json.dump(m, open(os.path.join(out, "manifest.json"), "w"), indent=2)

def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")

# ── commands ──────────────────────────────────────────────────────────

def cmd_render(a):
    if np is None: sys.exit("render needs numpy and Pillow: pip install numpy pillow")
    credits_path = os.path.join(a.src, "credits.json")
    credits = json.load(open(credits_path)) if os.path.exists(credits_path) else {}
    halftone_names = set(filter(None, (a.halftone or "").split(",")))
    if a.halftone_width < MIN_HALFTONE_PX:
        sys.exit(f"refused: halftone renders must be at least {MIN_HALFTONE_PX}px wide (asked {a.halftone_width})")
    m = load_manifest(a.out)
    for f in sorted(glob.glob(os.path.join(a.src, "*.jpg")) + glob.glob(os.path.join(a.src, "*.png"))):
        name = os.path.splitext(os.path.basename(f))[0]
        jobs = [("atkinson", a.width)]
        if name in halftone_names or "all" in halftone_names: jobs.append(("halftone", a.halftone_width))
        for kind, width in jobs:
            ink, gam, cov = expose_and_dither(load_gray(f, width), kind)
            fname = f"{name}-{kind}.png"; path = os.path.join(a.out, fname)
            paint(ink).save(path, optimize=True)
            digest = sha(path)
            prev = m["images"].get(fname, {})
            review = prev.get("review") if prev.get("sha") == digest else None  # changed pixels = re-review
            c = credits.get(name, {})
            m["images"][fname] = {
                "source": os.path.basename(f), "treatment": kind, "width": width,
                "gamma": round(gam, 3), "ink_coverage": round(cov, 3),
                "flags": flags_for(ink, kind, width),
                "credit": c.get("credit"), "license": c.get("license"), "source_url": c.get("url"),
                "sha": digest,
                "review": review or {"status": "pending", "by": None, "at": None, "note": ""},
            }
            fl = m["images"][fname]["flags"]
            print(f"{fname:28s} gamma {gam:5.2f}  ink {cov:4.0%}  {'FLAGS: ' + '; '.join(fl) if fl else 'ok'}")
    save_manifest(a.out, m)

def cmd_review(a):
    m = load_manifest(a.out)
    cards = []
    for fname, e in sorted(m["images"].items()):
        st = e["review"]["status"]
        fl = "".join(f"<li>{html.escape(x)}</li>" for x in e["flags"]) or "<li class=ok>no automatic flags</li>"
        cards.append(f"""
<section class="card {st}">
  <header><b>{fname}</b><span class="st">{st.upper()}</span></header>
  <div class="row">
    <figure><img src="{fname}" style="width:{min(e['width'], 1200)}px"><figcaption>real render width, {e['width']}px</figcaption></figure>
  </div>
  <div class="row small">
    <figure><img src="{fname}" style="width:320px"><figcaption>column size, 320px</figcaption></figure>
    <dl>
      <dt>Treatment</dt><dd>{e['treatment']}</dd>
      <dt>Ink coverage</dt><dd>{e['ink_coverage']:.0%} (legible band {LEGIBLE[0]:.0%} to {LEGIBLE[1]:.0%})</dd>
      <dt>Exposure gamma</dt><dd>{e['gamma']}</dd>
      <dt>Credit</dt><dd>{html.escape(e['credit'] or 'MISSING, cannot publish')}</dd>
      <dt>Checks</dt><dd><ul>{fl}</ul></dd>
      <dt>Approve</dt><dd><code>python image-press.py approve . {fname} --by Eddie</code></dd>
    </dl>
  </div>
</section>""")
    page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Shipped. Image Review</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,700;1,9..144,600&family=Archivo+Narrow:wght@500;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
<style>
body{{margin:0;background:#FAF8F4;color:#0b0b0b;font-family:'Archivo Narrow',sans-serif;padding:28px}}
h1{{font-family:Fraunces,serif;font-size:40px;margin:0}} h1 span{{color:#FF6B35}}
p.lede{{font-size:16px;color:#5a5a5a;max-width:760px}}
.card{{border-top:4px double #0b0b0b;padding:16px 0 28px;margin-top:18px}}
.card header{{display:flex;justify-content:space-between;font-size:15px;letter-spacing:.06em}}
.st{{font-weight:700;letter-spacing:.18em}} .pending .st{{color:#EE5C28}} .approved .st{{color:#2d6a2d}} .rejected .st{{color:#a11}}
img{{display:block;max-width:100%;image-rendering:pixelated;border:1px solid #0b0b0b}}
figure{{margin:12px 0}} figcaption{{font-size:12px;color:#5a5a5a;margin-top:4px}}
.small{{display:flex;gap:28px;flex-wrap:wrap;align-items:flex-start}}
dl{{display:grid;grid-template-columns:130px 1fr;gap:6px 14px;font-size:14px;margin:12px 0}} dt{{color:#5a5a5a}} dd{{margin:0}}
ul{{margin:0;padding-left:18px;color:#a11}} li.ok{{color:#2d6a2d;list-style:none;margin-left:-18px}}
code{{font-family:'JetBrains Mono',monospace;font-size:12px;background:rgba(238,92,40,.09);padding:1px 4px}}
</style></head><body>
<h1>Image review<span>.</span></h1>
<p class="lede">Every image, at its real size and at column size, before it publishes. Look for two things: can you tell what it is (legibility), and does it look like Shipped. (aesthetic). Automatic checks catch flooding and wash-out; they do not replace your eye.</p>
{''.join(cards)}
</body></html>"""
    open(os.path.join(a.out, "review.html"), "w").write(page)
    print(os.path.join(a.out, "review.html"))

def set_status(a, status):
    m = load_manifest(a.out)
    targets = list(m["images"]) if a.file == "all" else [a.file]
    for t in targets:
        if t not in m["images"]: sys.exit(f"unknown image: {t}")
        m["images"][t]["review"] = {"status": status, "by": a.by, "at": now(), "note": a.note or ""}
        print(f"{status}: {t}")
    save_manifest(a.out, m)

# ── slot picks (which treatment runs) ─────────────────────────────────

HALFTONE_SLOTS = ("cover", "lead")   # only slots shown at 700px+ may run halftone (lead becomes a full-width band)

def load_slots(out):
    p = os.path.join(out, "slots.json")
    return json.load(open(p)) if os.path.exists(p) else None

def treatment_of(slot, meta):
    return meta.get("treatment") or ("halftone" if slot == "cover" else "atkinson")

def in_use(out, m):
    """Files the paper will actually draw. Without slots.json (mockups), every image counts."""
    slots = load_slots(out)
    if slots is None: return sorted(m["images"])
    files = []
    for slot, meta in slots.items():
        files.append(f"{slot}-atkinson.png")                       # always: the small-screen fallback
        if treatment_of(slot, meta) == "halftone": files.append(f"{slot}-halftone.png")
    return files

def set_pick(out, slot, treatment):
    slots = load_slots(out) or {}
    if slot not in slots: raise ValueError(f"unknown slot: {slot}")
    if treatment not in ("atkinson", "halftone"): raise ValueError("treatment is atkinson or halftone")
    if treatment == "halftone":
        if slot not in HALFTONE_SLOTS: raise ValueError(f"halftone only runs at 700px+: {', '.join(HALFTONE_SLOTS)}")
        if f"{slot}-halftone.png" not in load_manifest(out)["images"]: raise ValueError(f"no halftone render for {slot}")
    slots[slot]["treatment"] = treatment
    json.dump(slots, open(os.path.join(out, "slots.json"), "w"), indent=2)

def cmd_pick(a):
    try: set_pick(a.out, a.slot, a.treatment)
    except ValueError as e: sys.exit(str(e))
    print(f"{a.slot}: {a.treatment}")

def cmd_check(a):
    m = load_manifest(a.out); bad = []
    files = in_use(a.out, m)
    for fname in files:
        e = m["images"].get(fname)
        if e is None: bad.append(f"{fname}: picked but never rendered"); continue
        if e["review"]["status"] != "approved": bad.append(f"{fname}: {e['review']['status']}")
        if not e.get("credit"): bad.append(f"{fname}: no credit")
        if e.get("license") == "generated" and "AI-generated" not in (e.get("credit") or ""):
            bad.append(f"{fname}: generated image not labeled AI-generated")
        if e["treatment"] == "halftone" and e["width"] < MIN_HALFTONE_PX: bad.append(f"{fname}: halftone under {MIN_HALFTONE_PX}px")
    if bad:
        print("IMAGE GATE BLOCKED\n  " + "\n  ".join(bad)); sys.exit(1)
    print(f"image gate clear: {len(files)} images in use, reviewed and credited")

# ── review desk (local, clickable) ────────────────────────────────────

DESK_HTML = r"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Shipped. Image Desk</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,700;1,9..144,500&family=Archivo+Narrow:wght@500;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
<style>
:root{--ink:#0b0b0b;--paper:#FAF8F4;--orange:#EE5C28;--muted:#5a5a5a;--ok:#1f6b3a;--bad:#a11}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:'Archivo Narrow',sans-serif}
header{position:sticky;top:0;z-index:5;background:var(--ink);color:var(--paper);display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center;padding:12px 20px}
header h1{font-family:Fraunces,serif;font-size:22px;margin:0}header h1 span{color:#FF6B35}
#gate{font-size:13px;letter-spacing:.14em;text-transform:uppercase;padding:5px 10px;border:1px solid rgba(250,248,244,.35)}
#gate.clear{background:var(--ok);border-color:var(--ok)}#gate.blocked{background:var(--orange);border-color:var(--orange);color:var(--ink)}
main{max-width:1320px;margin:0 auto;padding:10px 20px 80px}
.slot{border-top:4px double var(--ink);padding:18px 0 26px}
.top{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}
.top b{font-size:15px;letter-spacing:.18em;text-transform:uppercase}.st{font-weight:700;letter-spacing:.18em;font-size:13px}
.st.approved{color:var(--ok)}.st.pending{color:var(--orange)}.st.rejected{color:var(--bad)}
.subject{font-family:Fraunces,serif;font-style:italic;font-size:17px;color:var(--muted);margin:4px 0 12px}
.opts{display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap}
.opts button,.acts button{all:unset;cursor:pointer;font-size:13px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;padding:9px 14px;border:1px solid var(--ink)}
.opts button[aria-pressed=true]{background:var(--ink);color:var(--paper)}
.opts button:disabled{opacity:.35;cursor:not-allowed}
.stage img{display:block;width:100%;image-rendering:pixelated;border:1px solid var(--ink)}
.stage.col img{max-width:420px}
.cap{font-size:13px;color:var(--muted);margin-top:6px}.cap i{font-family:Fraunces,serif}
.flags{color:var(--bad);font-size:13px;margin-top:6px}
.acts{display:flex;gap:8px;align-items:center;margin-top:12px;flex-wrap:wrap}
.acts .ok{background:var(--ok);color:#fff;border-color:var(--ok)}.acts .no{border-color:var(--bad);color:var(--bad)}
.acts input{font:inherit;font-size:14px;padding:8px 10px;border:1px solid var(--ink);background:#fff;min-width:260px}
.note{font-size:12px;color:var(--muted)}
.hint{font-size:12px;color:var(--muted);margin-left:4px}
</style></head><body>
<header><h1>Image desk<span>.</span></h1><span id="gate">checking</span><span class="note" style="color:rgba(250,248,244,.7)">Pick the treatment that looks best, then approve. Rejecting sends the slot back to the desk.</span></header>
<main id="slots"></main>
<script>
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
async function api(path,body){const r=await fetch(path,{method:body?'POST':'GET',headers:{'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined});const j=await r.json();if(j.error)alertBar(j.error);return j}
function alertBar(msg){const g=document.getElementById('gate');g.textContent=msg;g.className='blocked'}
function draw(state){
  const g=document.getElementById('gate');g.textContent=state.gate.clear?'Gate clear':'Gate blocked: '+state.gate.problems.length;g.className=state.gate.clear?'clear':'blocked';g.title=state.gate.problems.join(' | ');
  document.getElementById('slots').innerHTML=state.slots.map(s=>{
    const showing=s.view||s.treatment;const f=s.files[showing];
    return `<section class="slot" data-slot="${s.slot}">
      <div class="top"><b>${s.slot}</b><span class="st ${s.status}">${s.status.toUpperCase()}</span></div>
      <div class="subject">${esc(s.subject)}</div>
      <div class="opts">
        <button data-pick="atkinson" aria-pressed="${s.treatment==='atkinson'}">Atkinson</button>
        <button data-pick="halftone" aria-pressed="${s.treatment==='halftone'}" ${s.files.halftone?'':'disabled title="halftone only runs at 700px+ (cover, lead)"'}>Halftone</button>
        ${s.slot==='lead'&&s.treatment==='halftone'?'<span class="hint">runs as a full-width band</span>':''}
      </div>
      <div class="stage ${s.slot.startsWith('story')?'col':''}"><img src="${f.file}?v=${f.sha}" alt=""></div>
      <div class="cap">${esc(s.caption)} <i>${esc(s.credit)}.</i> &middot; ink ${Math.round(f.ink*100)}%</div>
      ${f.flags.length?`<div class="flags">${f.flags.map(esc).join(' &middot; ')}</div>`:''}
      <div class="acts"><button class="ok" data-act="approved">Approve</button><button class="no" data-act="rejected">Reject</button><input placeholder="note (why, if rejecting)"></div>
    </section>`}).join('');
}
document.addEventListener('click',async e=>{
  const sec=e.target.closest('.slot');if(!sec)return;const slot=sec.dataset.slot;
  if(e.target.dataset.pick&&!e.target.disabled){draw(await api('/api/pick',{slot,treatment:e.target.dataset.pick}))}
  if(e.target.dataset.act){const note=sec.querySelector('input').value;draw(await api('/api/review',{slot,status:e.target.dataset.act,note}))}
});
api('/api/state').then(draw);
</script></body></html>"""

def desk_state(out):
    m = load_manifest(out); slots = load_slots(out) or {}
    rows = []
    for slot, meta in slots.items():
        t = treatment_of(slot, meta); files = {}
        for kind in ("atkinson", "halftone"):
            e = m["images"].get(f"{slot}-{kind}.png")
            if e and (kind == "atkinson" or slot in HALFTONE_SLOTS):
                files[kind] = {"file": f"{slot}-{kind}.png", "sha": e["sha"], "ink": e["ink_coverage"], "flags": e["flags"]}
        used = [f"{slot}-atkinson.png"] + ([f"{slot}-halftone.png"] if t == "halftone" else [])
        sts = {m["images"].get(f, {}).get("review", {}).get("status", "pending") for f in used}
        status = "rejected" if "rejected" in sts else ("approved" if sts == {"approved"} else "pending")
        a = m["images"].get(f"{slot}-atkinson.png", {})
        rows.append({"slot": slot, "subject": meta.get("subject"), "caption": meta.get("caption"), "credit": a.get("credit"),
                     "treatment": t, "files": files, "status": status})
    problems = []
    for f in in_use(out, m):
        e = m["images"].get(f)
        if not e or e["review"]["status"] != "approved": problems.append(f"{f}: {(e or {}).get('review', {}).get('status', 'missing')}")
    return {"slots": rows, "gate": {"clear": not problems, "problems": problems}}

def cmd_serve(a):
    import http.server, socketserver
    out = os.path.abspath(a.out)
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kw): super().__init__(*args, directory=out, **kw)
        def log_message(self, *x): pass
        def send_json(self, obj, code=200):
            b = json.dumps(obj).encode(); self.send_response(code)
            self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
        def do_GET(self):
            if self.path in ("/", "/index.html"):
                b = DESK_HTML.encode(); self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b); return
            if self.path == "/api/state": return self.send_json(desk_state(out))
            if not self.path.split("?")[0].endswith(".png"): return self.send_error(404)
            return super().do_GET()
        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            try:
                if self.path == "/api/pick":
                    set_pick(out, body["slot"], body["treatment"])
                elif self.path == "/api/review":
                    st = body["status"]
                    if st not in ("approved", "rejected"): raise ValueError("status is approved or rejected")
                    if st == "rejected" and not body.get("note"): raise ValueError("say why in the note before rejecting")
                    m = load_manifest(out); slots = load_slots(out) or {}
                    t = treatment_of(body["slot"], slots.get(body["slot"], {}))
                    for f in [f"{body['slot']}-atkinson.png"] + ([f"{body['slot']}-halftone.png"] if t == "halftone" else []):
                        if f in m["images"]:
                            m["images"][f]["review"] = {"status": st, "by": a.by, "at": now(), "note": body.get("note", "")}
                    save_manifest(out, m)
                else: return self.send_error(404)
            except (ValueError, KeyError) as e:
                return self.send_json({**desk_state(out), "error": str(e)})
            self.send_json(desk_state(out))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", a.port), H) as srv:
        print(f"image desk: http://127.0.0.1:{a.port}/  (Ctrl-C to stop)"); srv.serve_forever()

if __name__ == "__main__":
    p = argparse.ArgumentParser(); sp = p.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("render"); r.add_argument("src"); r.add_argument("out")
    r.add_argument("--halftone", default=""); r.add_argument("--width", type=int, default=1200)
    r.add_argument("--halftone-width", type=int, default=1600)
    v = sp.add_parser("review"); v.add_argument("out")
    for name in ("approve", "reject"):
        s = sp.add_parser(name); s.add_argument("out"); s.add_argument("file")
        s.add_argument("--by", required=True); s.add_argument("--note", required=(name == "reject"))
    c = sp.add_parser("check"); c.add_argument("out")
    k = sp.add_parser("pick"); k.add_argument("out"); k.add_argument("slot"); k.add_argument("treatment")
    d = sp.add_parser("serve"); d.add_argument("out"); d.add_argument("--port", type=int, default=8794); d.add_argument("--by", default="Eddie")
    a = p.parse_args()
    {"render": cmd_render, "review": cmd_review, "check": cmd_check, "pick": cmd_pick, "serve": cmd_serve,
     "approve": lambda a: set_status(a, "approved"), "reject": lambda a: set_status(a, "rejected")}[a.cmd](a)
