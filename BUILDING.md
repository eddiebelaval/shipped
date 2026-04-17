# BUILDING.md — Shipped.

> The build log. Where Shipped. came from, in order.

---

## Origin

The idea came from a real pain: I'd leave X for 30 minutes and come back feeling behind on the Anthropic ecosystem. In three weeks before Issue 01 shipped, Anthropic pushed **56 distinct releases** — models, Claude Code versions, SDKs, research, launches. X and Reddit cover them in fragments. Nobody ties the week together.

I wanted the week in one read.

## The Day: 2026-04-16

The entire first version — concept, design, pipeline, and Issue 01 copy — was built in a single day. About 10 hours, 1 PM to 11 PM.

### Afternoon: Concept + Design (1 PM – 5 PM)

| Time | Artifact | What landed |
|---|---|---|
| 1:12 PM | `content/index.md` | Series concept |
| 1:21 PM | `content/STYLE.md` | Voice rules. The forbidden phrases list: `EPIC`, "thrilled to," "ushers in," "game-changing," "industry-leading." Plus the "X isn't Y, it's Z" budget. |
| 2:16 PM | `content/MOCKUP.html` | First visual pass |
| 2:37 PM | `masthead.svg`, `masthead-small.svg` | Logo treatment |
| 2:40 PM | `content/branding-snippets.html` | Brand system |
| 2:42 PM | `content/DESIGN.md` | 72KB design spec — colors, type, layout, print analogies |
| 2:43 PM | `content/MOCKUP-v2-temp100.html` | Second mockup iteration |
| 2:51 PM | `content/H1-OPTIONS.html` | Headline variants |
| 2:57 PM | `content/MASTHEAD-VARIANTS.html` | Masthead variants |
| 3:04 PM | `content/BENCHMARKS.html` | Layout benchmarks |
| 4:57 PM | `content/LAUNCH-COPY.md` | Social copy for launch night |

Nine design iterations in about 90 minutes. Rapid, disposable, convergent.

### Evening: Pipeline (8:35 PM – 9 PM)

The pipeline was built in roughly 25 minutes using a Director/Builder pattern — Claude designed the architecture, Codex executed scoped tasks against the spec.

| Time | Module | Purpose |
|---|---|---|
| 8:35 PM | `package.json`, `tsconfig.json` | Pipeline skeleton |
| 8:38 PM | `src/orchestrate/` | Chains scrape + render + verify + stage |
| 8:46 PM | `src/scrape/` | @claudedevs X feed → JSON |
| 8:47 PM | `src/verify/` | The lying-prevention layer |
| 8:49 PM | `pipeline/README.md` | Architecture doc |
| 8:56 PM | `src/render/` | Markdown → magazine HTML |
| 8:58 PM | `node_modules/` | Deps installed |

### Night: Issue 01 (9 PM – 11 PM)

| Time | Artifact | What landed |
|---|---|---|
| 9:07 PM | `content/issue-00-the-founding.md` | 57KB: front-of-book + release log for 56 items |
| 9:08 PM | `content/SHIP-NOW.md` | Launch checklist |
| 10:54 PM | `content/MOCKUP-FINAL.html` | Final polished mockup (170KB) |

## Launch: 2026-04-17 (Friday)

Issue 01 shipped to `id8labs.app/shipped/01/` early Friday morning. Commits:

- `aea397e` — Launch Shipped. — Issue 01: The Shadow Release
- `5073c15` — Replace Shipped. Issue 01 OG card with magazine-cover treatment
- `0926abc` — Fix Shipped. Issue 01 mobile layout (iPhone 13 mini, 375px)
- `3feddeb` — Cache-bust Shipped. Issue 01 OG card via og-v2.png
- `104dd8f` — Cache-bust Shipped. Issue 01 OG card via og-v3.png

The two cache-busting commits captured an operational lesson: **Vercel's edge caches static-asset 404 responses as `immutable` for a year**. If a crawler hits a new asset path before the deploy propagates, that 404 freezes at the edge. The only reliable fix is a fresh path — `og-v2.png` → `og-v3.png`. The old og.png is still serving a stale 37KB version at the edge, permanently. This is a gotcha worth remembering for any new asset path.

## Repo extraction: 2026-04-17 morning

The first-day build split Shipped. across three locations:
- Pipeline → `id8/tool-factory/scrapers/shipped/`
- Content → `id8/knowledge/series/shipped/`
- Output → `id8/id8labs/public/shipped/`

By Friday morning, the WhatsApp feedback group was asking for more languages, a video, and a podcast. Shipped. had become a thing, and it needed its own home.

The extraction decisions:
1. **One public repo, MIT-licensed.** Show the work; let other builders fork it.
2. **Pipeline + content in the new repo.** Output stays in `id8labs/` (that's the deploy target; Vercel still serves from there).
3. **Clean-slate history.** The build was one day old. The origin is documented here. No `git filter-repo` surgery needed.
4. **Triad from day one.** VISION, SPEC, BUILDING. The scope fence and the moat should be writable targets, not re-inferred each week.

## Operational lessons (first-day edition)

- **Voice gate pays off immediately.** STYLE.md's forbidden-phrase list caught two phrases in the first-pass front-of-book I would have shipped.
- **Verifier tooling has false positives for bare integers.** `1M`, `16`, `17`, `23` got flagged as number claims when they weren't. Known; fix slated for the Issue 02 tooling pass.
- **Some authoritative sources block scraper user agents.** `red.anthropic.com`, Axios, Medium all 403 against our UA even when the content is live in a browser. Fragile-domain allowlist is the right fix.
- **OG image URLs are land mines.** See the og.png / og-v2.png / og-v3.png saga above. New asset paths only reach the edge cleanly if no crawler pre-fetched them during the deploy window.
