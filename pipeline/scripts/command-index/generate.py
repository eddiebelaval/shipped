#!/usr/bin/env python3
"""
The Command Index — generator.

Builds a single, searchable, Shipped.-styled HTML reference of every slash
command available in this Claude Code install, across three streams:

  1. Built-in   — Anthropic's native Claude Code commands + bundled skills
                  (seeded from builtins.json; the "keeps coming" stream,
                  reconciled weekly against code.claude.com/docs/en/commands).
  2. Plugin     — commands shipped by installed plugins / marketplaces
                  (Anthropic-published marketplaces flagged distinctly).
  3. Custom     — id8Labs' own commands in ~/.claude/commands/.

Deterministic. No network, no LLM. Safe to run on a cron. The intelligence
layer (refresh-builtins.md) only touches builtins.json; this script renders.

Usage:
  python3 generate.py [--out DIR]

Outputs (into --out, default ./output):
  command-index.html   self-contained page
  command-index.json   the merged data model (for tooling / diffs)
"""
import os, re, sys, json, html, datetime, subprocess
from pathlib import Path

HOME = Path.home()
CLAUDE = HOME / ".claude"
CUSTOM_CMD_DIR = CLAUDE / "commands"
CUSTOM_SKILL_DIR = CLAUDE / "skills"
PLUGINS_CACHE = CLAUDE / "plugins" / "cache"   # installed plugins only (not the browse catalog)
HERE = Path(__file__).resolve().parent

# Marketplaces published by Anthropic (from known_marketplaces.json owners).
ANTHROPIC_MARKETPLACES = {
    "claude-code-plugins",          # anthropics/claude-code
    "claude-plugins-official",      # anthropics/claude-plugins-official
    "claude-for-financial-services",# anthropics/financial-services
    "claude-for-legal",             # anthropics/claude-for-legal
    "knowledge-work-plugins",       # anthropics/knowledge-work-plugins
}

# Display order for built-in / custom categories.
CATEGORY_ORDER = [
    "Session & Context", "Model & Reasoning", "Usage & Cost",
    "Config & Terminal", "Memory & Project", "Extensibility",
    "Code & Review", "Background & Parallel", "Web & Remote",
    "Account & System", "Discover & Social", "Research & Workflows",
    "Uncategorized",
]

# ----------------------------------------------------------------------------
# Description extraction
# ----------------------------------------------------------------------------
def clean(text):
    if not text:
        return ""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)   # md links -> text
    text = re.sub(r"`([^`]+)`", r"\1", text)               # inline code
    text = re.sub(r"[*_#>]+", "", text)                    # md emphasis/heading marks
    text = re.sub(r"<[^>]+>", "", text)                    # stray html
    text = re.sub(r"\s+", " ", text).strip()
    return text

def first_sentence(text, cap=170):
    text = clean(text)
    # keep it to a sentence-ish lead
    m = re.split(r"(?<=[.!?])\s", text, maxsplit=1)
    lead = m[0] if m else text
    if len(lead) > cap:
        lead = lead[:cap - 1].rstrip() + "…"
    return lead

def parse_frontmatter(raw):
    if not raw.startswith("---"):
        return {}, raw
    end = raw.find("\n---", 3)
    if end == -1:
        return {}, raw
    block = raw[3:end].strip("\n")
    body = raw[end + 4:]
    fm = {}
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            k, v = m.group(1).lower(), m.group(2).strip()
            v = v.strip('"').strip("'")
            fm[k] = v
    return fm, body

def extract_command(md_path, fallback_name):
    try:
        raw = md_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return fallback_name, ""
    fm, body = parse_frontmatter(raw)

    name = fm.get("name") or fallback_name
    name = name.strip()
    if not name.startswith("/"):
        name = "/" + name.lstrip("/")

    desc = fm.get("description")
    if not desc:
        # Look for an H1 like "# /ship - Complete Feature" or "# Title"
        h1 = None
        para = None
        for line in body.splitlines():
            s = line.strip()
            if not s:
                continue
            if s.startswith("#"):
                if h1 is None:
                    h1 = s.lstrip("#").strip()
                continue
            if not s.startswith(("```", "|", "-", "*", ">")):
                para = s
                break
        if h1:
            m = re.match(r"^/?[\w:-]+\s*[-—:]\s*(.+)$", h1)
            if m:
                desc = m.group(1)
            elif para:
                desc = para
            else:
                desc = h1
        elif para:
            desc = para
    return name, first_sentence(desc or "")

# ----------------------------------------------------------------------------
# Scanners
# ----------------------------------------------------------------------------
def scan_custom():
    """id8Labs' own slash surface: commands/ (subtype command) + skills/ (subtype skill)."""
    out = []
    # commands
    skip = {"readme", "getting-started", "which-command", "command-map", "license"}
    if CUSTOM_CMD_DIR.exists():
        for p in sorted(CUSTOM_CMD_DIR.rglob("*.md")):
            if p.stem.lower() in skip:
                continue
            name, desc = extract_command(p, "/" + p.stem)
            out.append({
                "name": name, "desc": desc, "stream": "custom",
                "category": "Commands  (~/.claude/commands)", "subtype": "command",
                "source": "id8Labs", "owner": "id8labs", "plugin": None, "marketplace": None,
            })
    # skills (each dir/SKILL.md)
    if CUSTOM_SKILL_DIR.exists():
        for p in sorted(CUSTOM_SKILL_DIR.glob("*/SKILL.md")):
            slug = p.parent.name
            name, desc = extract_command(p, "/" + slug)
            # frontmatter 'name' on skills is a Title; prefer the slug for the invocation
            name = "/" + slug
            out.append({
                "name": name, "desc": desc, "stream": "custom",
                "category": "Skills  (~/.claude/skills)", "subtype": "skill",
                "source": "id8Labs", "owner": "id8labs", "plugin": None, "marketplace": None,
            })
    # de-dupe by name, keep first
    seen, dedup = set(), []
    for c in out:
        if c["name"] in seen:
            continue
        seen.add(c["name"]); dedup.append(c)
    return dedup

def scan_plugins():
    """Installed plugins only (cache/). Indexes both commands/ and skills/."""
    out = []
    if not PLUGINS_CACHE.exists():
        return out
    best = {}  # (marketplace, plugin, name) -> record; first (sorted) wins

    def add(marketplace, plugin, name, desc, subtype):
        key = (marketplace, plugin, name)
        if key in best:
            return
        best[key] = {
            "name": name, "desc": desc, "stream": "plugin",
            "category": plugin, "subtype": subtype,
            "owner": "anthropic" if marketplace in ANTHROPIC_MARKETPLACES else "community",
            "plugin": plugin, "marketplace": marketplace,
            "source": f"{plugin}@{marketplace}",
        }

    # commands: any *.md under a commands/ dir
    for p in sorted(PLUGINS_CACHE.rglob("*.md")):
        rel = p.relative_to(PLUGINS_CACHE).parts
        if len(rel) < 4 or "commands" not in rel or "skills" in rel:
            continue
        name, desc = extract_command(p, "/" + p.stem)
        add(rel[0], rel[1], name, desc, "command")

    # skills: each skills/<name>/SKILL.md -> /plugin:skill (qualified, unambiguous)
    for p in sorted(PLUGINS_CACHE.rglob("SKILL.md")):
        rel = p.relative_to(PLUGINS_CACHE).parts
        if len(rel) < 4 or "skills" not in rel:
            continue
        plugin, skill = rel[1], p.parent.name
        _, desc = extract_command(p, "/" + skill)
        add(rel[0], plugin, f"/{plugin}:{skill}", desc, "skill")

    return list(best.values())

def load_builtins():
    data = json.loads((HERE / "builtins.json").read_text())
    meta = data.get("_meta", {})
    out = []
    for c in data["commands"]:
        out.append({
            "name": c["name"], "desc": c.get("desc", ""), "stream": "builtin",
            "category": c.get("category", "Uncategorized"),
            "subtype": c.get("subtype", "command"),
            "owner": "anthropic", "plugin": None, "marketplace": None,
            "source": "Claude Code",
        })
    return out, meta

def claude_version():
    try:
        v = subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=10)
        return v.stdout.strip().split(" ")[0] or "unknown"
    except Exception:
        return "unknown"

# ----------------------------------------------------------------------------
# Rendering
# ----------------------------------------------------------------------------
def esc(s):
    return html.escape(s or "", quote=True)

def cat_sort_key(cat):
    return (CATEGORY_ORDER.index(cat) if cat in CATEGORY_ORDER else 999, cat.lower())

def render_command_row(c):
    badge = ""
    if c["subtype"] == "skill":
        badge = '<span class="ci-badge ci-badge-skill">skill</span>'
    text = " ".join(filter(None, [c["name"], c["desc"], c.get("plugin") or "", c.get("source") or ""])).lower()
    src = ""
    if c["stream"] == "plugin":
        owner = "Anthropic" if c["owner"] == "anthropic" else "Community"
        src = f'<span class="ci-src">{esc(c["plugin"])} <span class="ci-dot">&middot;</span> {owner}</span>'
    return (
        f'<div class="ci-cmd" data-stream="{c["stream"]}" data-owner="{c["owner"]}" data-text="{esc(text)}">'
        f'<div class="ci-cmd-head">'
        f'<button class="ci-name" data-copy="{esc(c["name"])}" title="Copy">{esc(c["name"])}</button>'
        f'{badge}{src}'
        f'</div>'
        f'<div class="ci-desc">{esc(c["desc"])}</div>'
        f'</div>'
    )

def render_grouped(records, group_key, group_label_fn, sort_groups):
    groups = {}
    for c in records:
        groups.setdefault(group_key(c), []).append(c)
    blocks = []
    for g in sort_groups(groups.keys()):
        items = sorted(groups[g], key=lambda c: c["name"].lower())
        rows = "\n".join(render_command_row(c) for c in items)
        blocks.append(
            f'<div class="ci-group">'
            f'<div class="ci-group-head"><span class="ci-group-name">{esc(group_label_fn(g))}</span>'
            f'<span class="ci-group-count">{len(items)}</span></div>'
            f'<div class="ci-group-body">{rows}</div>'
            f'</div>'
        )
    return "\n".join(blocks)

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Command Index &mdash; Shipped.</title>
<meta name="description" content="A living reference of every Claude Code slash command: Anthropic built-ins, plugin commands, and id8Labs custom commands. Regenerated automatically.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;0,9..144,900;1,9..144,400&family=Archivo:wght@300;400;500;600;700;800;900&family=Archivo+Narrow:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --orange:#FF6B35;--ink:#0b0b0b;--paper:#fafaf7;--paper-shadow:#f2f0e8;
  --body:#2a2a2a;--muted:#5a5a5a;--gray:#8a8a8a;
  --hair:rgba(11,11,11,0.12);--hair-soft:rgba(11,11,11,0.06);--hair-hard:rgba(11,11,11,0.22);
  --disp:'Fraunces','Times New Roman',serif;--sans:'Archivo',system-ui,sans-serif;
  --narrow:'Archivo Narrow','Archivo',sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--body);font-family:var(--sans);
  font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased;}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:1000;opacity:.28;mix-blend-mode:multiply;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' seed='3'/><feColorMatrix values='0 0 0 0 0.02  0 0 0 0 0.02  0 0 0 0 0.02  0 0 0 0.22 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:0 28px}

/* publication bar */
.pub-bar{display:flex;align-items:center;justify-content:space-between;height:46px;
  border-bottom:1px solid var(--hair);font-family:var(--narrow);
  text-transform:uppercase;letter-spacing:.14em;font-size:11px;color:var(--gray)}
.pub-bar .brand{color:var(--ink);font-weight:600}
.pub-bar .brand .dot{color:var(--orange)}

/* cover */
.cover{padding:64px 0 28px}
.kicker{font-family:var(--narrow);text-transform:uppercase;letter-spacing:.24em;
  font-size:12px;color:var(--gray);font-weight:600}
.kicker .num{color:var(--orange)}
.title{font-family:var(--disp);font-variation-settings:"opsz" 144;font-weight:500;
  font-size:clamp(48px,8vw,92px);line-height:.96;letter-spacing:-.025em;color:var(--ink);
  margin:18px 0 0;text-shadow:.4px .5px .8px rgba(0,0,0,.06)}
.title .dot{color:var(--orange)}
.deck{font-family:var(--disp);font-weight:400;font-size:clamp(18px,2.4vw,23px);
  line-height:1.5;color:var(--muted);max-width:680px;margin:20px 0 0}
.cover-rule{height:1px;background:var(--hair);margin:34px 0 0}

/* by the numbers */
.btn-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:0;border-bottom:1px solid var(--hair);margin-top:0}
.btn-item{padding:26px 24px 26px 0;border-right:1px solid var(--hair-soft)}
.btn-item:last-child{border-right:none}
.btn-num{font-family:var(--disp);font-weight:600;font-size:54px;line-height:.9;color:var(--ink);letter-spacing:-.03em}
.btn-num small{font-size:22px;color:var(--orange);font-weight:600}
.btn-label{font-family:var(--narrow);text-transform:uppercase;letter-spacing:.16em;
  font-size:10.5px;color:var(--gray);margin-top:10px;font-weight:600}

/* controls */
.controls{position:sticky;top:0;z-index:50;background:var(--paper);
  padding:18px 0 14px;border-bottom:1px solid var(--hair);margin-top:6px}
.search-row{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.search{flex:1;min-width:240px;position:relative}
.search input{width:100%;font-family:var(--mono);font-size:15px;color:var(--ink);
  background:#fff;border:1px solid var(--hair-hard);border-radius:7px;padding:12px 14px 12px 38px;outline:none}
.search input:focus{border-color:var(--orange)}
.search .mag{position:absolute;left:13px;top:50%;transform:translateY(-50%);color:var(--gray);font-size:15px}
.tabs{display:flex;gap:6px;flex-wrap:wrap}
.tab{font-family:var(--narrow);text-transform:uppercase;letter-spacing:.1em;font-size:12px;font-weight:600;
  color:var(--muted);background:#fff;border:1px solid var(--hair);border-radius:999px;padding:9px 16px;cursor:pointer}
.tab[aria-pressed="true"]{background:var(--ink);color:#fff;border-color:var(--ink)}
.tab .c{color:var(--gray);margin-left:6px;font-family:var(--mono);font-size:11px}
.tab[aria-pressed="true"] .c{color:rgba(255,255,255,.6)}
.count-line{font-family:var(--mono);font-size:12px;color:var(--gray);margin-top:10px}
.count-line b{color:var(--orange)}

/* stream sections */
.stream{padding:44px 0 8px}
.stream-flag{font-family:var(--narrow);text-transform:uppercase;letter-spacing:.2em;
  font-size:12px;font-weight:700;color:var(--gray);display:flex;align-items:baseline;gap:12px;
  padding-bottom:10px;border-bottom:2px solid var(--ink)}
.stream-flag .big{font-family:var(--disp);font-weight:600;font-size:30px;color:var(--ink);letter-spacing:-.02em;text-transform:none}
.stream-flag .meta{margin-left:auto;font-weight:600;color:var(--gray)}
.stream-note{font-family:var(--disp);font-size:16px;color:var(--muted);max-width:720px;margin:14px 0 4px;line-height:1.55}

.ci-group{margin:26px 0 0}
.ci-group-head{display:flex;align-items:baseline;gap:10px;padding:14px 0 8px;border-bottom:1px solid var(--hair)}
.ci-group-name{font-family:var(--narrow);text-transform:uppercase;letter-spacing:.13em;font-size:13px;font-weight:700;color:var(--ink)}
.ci-group-count{font-family:var(--mono);font-size:11px;color:var(--gray)}
.ci-group-body{display:grid;grid-template-columns:1fr 1fr;gap:0}
@media(max-width:760px){.ci-group-body{grid-template-columns:1fr}.btn-strip{grid-template-columns:1fr 1fr}.btn-item{border-right:none;border-bottom:1px solid var(--hair-soft)}}

.ci-cmd{padding:14px 24px 14px 0;border-bottom:1px solid var(--hair-soft)}
.ci-cmd-head{display:flex;align-items:center;gap:9px;flex-wrap:wrap}
.ci-name{font-family:var(--mono);font-size:14px;font-weight:500;color:var(--ink);
  background:transparent;border:0;padding:0;cursor:pointer;letter-spacing:-.01em}
.ci-name:hover{color:var(--orange)}
.ci-name::after{content:"copy";font-family:var(--narrow);font-size:9px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--gray);margin-left:7px;opacity:0;transition:opacity .12s}
.ci-cmd:hover .ci-name::after{opacity:1}
.ci-name.copied::after{content:"copied";color:var(--orange);opacity:1}
.ci-badge{font-family:var(--narrow);text-transform:uppercase;letter-spacing:.08em;font-size:9px;font-weight:700;
  padding:2px 6px;border-radius:3px}
.ci-badge-skill{background:var(--orange);color:#fff}
.ci-src{font-family:var(--narrow);text-transform:uppercase;letter-spacing:.07em;font-size:10px;color:var(--gray);margin-left:auto}
.ci-src .ci-dot{color:var(--hair-hard)}
.ci-desc{font-size:13.5px;line-height:1.5;color:var(--muted);margin-top:4px;max-width:46ch}

.ci-empty{display:none;font-family:var(--disp);font-size:20px;color:var(--muted);padding:60px 0;text-align:center}

/* colophon */
.colophon{margin-top:60px;border-top:2px solid var(--ink);padding:30px 0 70px;
  font-family:var(--mono);font-size:12px;color:var(--gray);line-height:1.7}
.colophon b{color:var(--ink);font-weight:500}
.colophon a{color:var(--orange);text-decoration:none}
.colophon .row{margin-top:6px}
.hide{display:none !important}
</style>
</head>
<body>
<div class="wrap">
  <div class="pub-bar">
    <span class="brand">Shipped<span class="dot">.</span></span>
    <span>Reference &middot; The Command Index</span>
  </div>

  <header class="cover">
    <div class="kicker">REFERENCE <span class="num">&middot;</span> CLAUDE CODE __VERSION__ <span class="num">&middot;</span> __DATE_LABEL__</div>
    <h1 class="title">The Command<br>Index<span class="dot">.</span></h1>
    <p class="deck">Every slash command in this install, in one place. The ones Anthropic ships with Claude Code, the ones plugins add, and the ones id8Labs built. They keep coming; this page keeps up.</p>
    <div class="cover-rule"></div>
  </header>

  <section class="btn-strip">
    <div class="btn-item"><div class="btn-num">__TOTAL__</div><div class="btn-label">Commands indexed</div></div>
    <div class="btn-item"><div class="btn-num">__BUILTIN__</div><div class="btn-label">Anthropic built-in</div></div>
    <div class="btn-item"><div class="btn-num">__PLUGIN__</div><div class="btn-label">From __PLUGINCOUNT__ plugins</div></div>
    <div class="btn-item"><div class="btn-num">__CUSTOM__</div><div class="btn-label">id8Labs custom</div></div>
  </section>

  <div class="controls">
    <div class="search-row">
      <label class="search"><span class="mag">&#9906;</span>
        <input id="q" type="search" placeholder="Search commands &mdash; name, purpose, plugin&hellip;" autocomplete="off" spellcheck="false">
      </label>
      <div class="tabs" id="tabs">
        <button class="tab" data-stream="all" aria-pressed="true">All <span class="c">__TOTAL__</span></button>
        <button class="tab" data-stream="builtin" aria-pressed="false">Built-in <span class="c">__BUILTIN__</span></button>
        <button class="tab" data-stream="plugin" aria-pressed="false">Plugins <span class="c">__PLUGIN__</span></button>
        <button class="tab" data-stream="custom" aria-pressed="false">Custom <span class="c">__CUSTOM__</span></button>
      </div>
    </div>
    <div class="count-line"><b id="shown">__TOTAL__</b> shown</div>
  </div>

  __SECTIONS__

  <div class="ci-empty" id="empty">No commands match that search.</div>

  <footer class="colophon">
    <div class="row"><b>The Command Index</b> &mdash; a living back-of-book reference from Shipped., the magazine on what Anthropic ships.</div>
    <div class="row">Generated <b>__DATE_LABEL__</b> from Claude Code <b>__VERSION__</b>. Built-ins sourced from <a href="https://code.claude.com/docs/en/commands">code.claude.com/docs/en/commands</a> &middot; changelog <a href="https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md">anthropics/claude-code</a>.</div>
    <div class="row">Regenerated automatically: a weekly local scan refreshes plugin + custom commands; a weekly routine reconciles Anthropic built-ins as new ones ship. Click any command name to copy it.</div>
  </footer>
</div>
<script>
(function(){
  var q=document.getElementById('q'),tabs=document.getElementById('tabs'),
      shown=document.getElementById('shown'),empty=document.getElementById('empty'),
      cmds=Array.prototype.slice.call(document.querySelectorAll('.ci-cmd')),
      groups=Array.prototype.slice.call(document.querySelectorAll('.ci-group')),
      streams=Array.prototype.slice.call(document.querySelectorAll('.stream')),
      stream='all',term='';
  function apply(){
    var n=0,t=term.trim().toLowerCase(),toks=t?t.split(/\s+/):[];
    cmds.forEach(function(el){
      var okS=stream==='all'||el.getAttribute('data-stream')===stream;
      var txt=el.getAttribute('data-text');
      var okT=true;for(var i=0;i<toks.length;i++){if(txt.indexOf(toks[i])===-1){okT=false;break;}}
      var vis=okS&&okT;el.classList.toggle('hide',!vis);if(vis)n++;
    });
    groups.forEach(function(g){
      var any=g.querySelectorAll('.ci-cmd:not(.hide)').length;
      g.classList.toggle('hide',!any);
      var c=g.querySelector('.ci-group-count');if(c)c.textContent=any;
    });
    streams.forEach(function(s){
      var any=s.querySelectorAll('.ci-cmd:not(.hide)').length;
      s.classList.toggle('hide',!any);
    });
    shown.textContent=n;empty.style.display=n?'none':'block';
  }
  q.addEventListener('input',function(){term=q.value;apply();});
  tabs.addEventListener('click',function(e){
    var b=e.target.closest('.tab');if(!b)return;
    stream=b.getAttribute('data-stream');
    tabs.querySelectorAll('.tab').forEach(function(t){t.setAttribute('aria-pressed',t===b?'true':'false');});
    apply();
  });
  document.addEventListener('click',function(e){
    var b=e.target.closest('.ci-name');if(!b)return;
    var v=b.getAttribute('data-copy');
    navigator.clipboard&&navigator.clipboard.writeText(v).then(function(){
      b.classList.add('copied');setTimeout(function(){b.classList.remove('copied');},1100);
    });
  });
  apply();
})();
</script>
</body>
</html>
"""

def build():
    out_dir = HERE / "output"
    if "--out" in sys.argv:
        out_dir = Path(sys.argv[sys.argv.index("--out") + 1]).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    builtins, bmeta = load_builtins()
    plugins = scan_plugins()
    custom = scan_custom()
    records = builtins + plugins + custom

    total = len(records)
    n_builtin, n_plugin, n_custom = len(builtins), len(plugins), len(custom)
    plugin_count = len({(c["marketplace"], c["plugin"]) for c in plugins})
    n_anthropic_plugins = len({(c["marketplace"], c["plugin"]) for c in plugins if c["owner"] == "anthropic"})

    now = datetime.datetime.now()
    date_label = now.strftime("%B %-d, %Y") if os.name != "nt" else now.strftime("%B %d, %Y")
    version = claude_version()

    # ---- sections ----
    sections = []

    # Built-in
    bi = render_grouped(
        builtins,
        group_key=lambda c: c["category"],
        group_label_fn=lambda g: g,
        sort_groups=lambda ks: sorted(ks, key=cat_sort_key),
    )
    sections.append(
        f'<section class="stream" data-stream="builtin">'
        f'<div class="stream-flag"><span class="big">Built-in</span> Anthropic &middot; Claude Code'
        f'<span class="meta">{n_builtin} commands</span></div>'
        f'<p class="stream-note">Native commands and bundled skills that ship inside Claude Code. '
        f'This is the stream that keeps growing: Anthropic adds commands with most releases, and this section '
        f'is reconciled weekly against the official reference.</p>{bi}</section>'
    )

    # Plugins (group by marketplace, then plugin) — sort Anthropic marketplaces first
    def mk_label(m):
        owner = "Anthropic" if m in ANTHROPIC_MARKETPLACES else "Community"
        return f"{m}  ({owner})"
    by_mkt = {}
    for c in plugins:
        by_mkt.setdefault(c["marketplace"], []).append(c)
    def mkt_sort(ms):
        return sorted(ms, key=lambda m: (0 if m in ANTHROPIC_MARKETPLACES else 1, m.lower()))
    plugin_blocks = []
    for m in mkt_sort(by_mkt.keys()):
        inner = render_grouped(
            by_mkt[m],
            group_key=lambda c: c["plugin"],
            group_label_fn=lambda g: g,
            sort_groups=lambda ks: sorted(ks, key=str.lower),
        )
        owner = "Anthropic" if m in ANTHROPIC_MARKETPLACES else "Community"
        plugin_blocks.append(
            f'<div class="ci-mkt"><div class="ci-group-head" style="border-bottom:2px solid var(--hair-hard)">'
            f'<span class="ci-group-name" style="font-size:14px">{esc(m)}</span>'
            f'<span class="ci-group-count">{owner} &middot; {len(by_mkt[m])}</span></div>{inner}</div>'
        )
    sections.append(
        f'<section class="stream" data-stream="plugin">'
        f'<div class="stream-flag"><span class="big">Plugins</span> Marketplaces &amp; packs'
        f'<span class="meta">{n_plugin} commands &middot; {plugin_count} plugins</span></div>'
        f'<p class="stream-note">Commands added by installed plugins. {n_anthropic_plugins} plugins come from '
        f'Anthropic-published marketplaces (finance, legal, sales, engineering and more); the rest are community packs.</p>'
        f'{"".join(plugin_blocks)}</section>'
    )

    # Custom
    cu = render_grouped(
        custom,
        group_key=lambda c: "id8Labs commands",
        group_label_fn=lambda g: g,
        sort_groups=lambda ks: list(ks),
    )
    sections.append(
        f'<section class="stream" data-stream="custom">'
        f'<div class="stream-flag"><span class="big">Custom</span> id8Labs'
        f'<span class="meta">{n_custom} commands</span></div>'
        f'<p class="stream-note">Commands defined in <code>~/.claude/commands/</code> &mdash; the portfolio\'s own '
        f'workflow verbs. Refreshed on every scan as new ones are written.</p>{cu}</section>'
    )

    page = PAGE
    repl = {
        "__VERSION__": version, "__DATE_LABEL__": date_label,
        "__TOTAL__": str(total), "__BUILTIN__": str(n_builtin),
        "__PLUGIN__": str(n_plugin), "__CUSTOM__": str(n_custom),
        "__PLUGINCOUNT__": str(plugin_count),
        "__SECTIONS__": "\n".join(sections),
    }
    for k, v in repl.items():
        page = page.replace(k, v)

    (out_dir / "command-index.html").write_text(page, encoding="utf-8")
    (out_dir / "command-index.json").write_text(json.dumps({
        "generated": now.isoformat(timespec="seconds"),
        "claude_version": version,
        "totals": {"all": total, "builtin": n_builtin, "plugin": n_plugin,
                   "custom": n_custom, "plugins": plugin_count,
                   "anthropic_plugins": n_anthropic_plugins},
        "builtins_meta": bmeta,
        "commands": records,
    }, indent=2), encoding="utf-8")

    print(f"OK  total={total}  builtin={n_builtin}  plugin={n_plugin} ({plugin_count} plugins)  custom={n_custom}")
    print(f"    -> {out_dir/'command-index.html'}")
    print(f"    -> {out_dir/'command-index.json'}")

if __name__ == "__main__":
    build()
