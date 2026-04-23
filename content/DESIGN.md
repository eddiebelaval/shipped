# Shipped. — Design System

The visual identity spec for `id8labs.app/shipped/`. Read this before touching a pixel.

**Sibling documents:** `STYLE.md` (voice), `index.md` (archive)
**Lives inside:** id8Labs Next.js app (`/app/shipped/`)
**Design law:** id8Labs DESIGN.md applies everywhere this document is silent.

---

## Revision History

### Revision 5 — PLANNED (triggered after Issue 03 ships, 2026-05-01)

Eddie's brief, captured Thu 2026-04-23 AM pre-Issue-02-lock:

> "When we're in a good place we need have a design.md created. It should be created off of 3 issues for triangulation and variety. We need to be able to go in many directions. This design keeps us in style/theme with room to explore and come back home."

**What Rev 5 does:**

1. **Triangulates from three shipped issues** (Issue 01 "The Shadow Release," Issue 02 "Presence," Issue 03 TBD) rather than deriving the spec primarily from Issue 01's founding visual direction.
2. **Identifies variable surfaces** — the places where issue-to-issue variation is *sanctioned* (cover treatment, hero illustration, chart aesthetic, section ornaments, drop-cap color, masthead micro-variants).
3. **Identifies constant surfaces** — the load-bearing identity elements that must NOT vary (masthead logo, body typography, page grid, trust markers, footer, warm-white stock + ink feel).
4. **Builds the "explore / come home" protocol** — a documented range of motion: per-issue visual decisions sit inside a bounded palette and furniture set. Each issue picks from the range. The range itself is the identity.
5. **Captures emergent patterns** — what Rev 4 called a "spec" is actually a set of decisions made for Issue 01. Rev 5 refactors those decisions into *principles + variants* by observing what held and what wanted to change across three issues.

**Trigger conditions:**
- Issue 03 shipped and visible at `id8labs.app/shipped/03/`
- At least one visual element deliberately varied between Issue 01 and Issue 02 or 03 (hero chart treatment is the current candidate — Mythos bar in Issue 01 vs. whatever Issue 02/03 run)
- Eddie's read-through of all three side-by-side, noting what "felt like Shipped." and what drifted

**Methodology (Rev 5 authoring pass):**
1. Pull all three covers + front-of-book hero treatments + one representative interior spread per issue. Compare.
2. Tag every visible design decision. Mark each as either CONSTANT (appears identically in all three) or VARIANT (differs across at least one).
3. For each VARIANT, name the range. Document what's sanctioned and what's out-of-bounds.
4. For each CONSTANT, confirm it's load-bearing — if a constant could vary without losing the identity, it's actually a variant in disguise; re-classify.
5. Rewrite Rev 4's prescriptive sections as principle-plus-range, not as a single specified value.

**What Rev 5 does NOT do:**
- Does not retire Rev 4 as gospel. Rev 4 remains the default when Rev 5 is silent.
- Does not ship with Issue 03. Rev 5 is authored *from* Issue 03's release, not *for* it.
- Does not prescribe the variants. The variants are observed from what the three issues actually shipped, not invented ahead of time.

**Placeholder status:** brief captured; authoring deferred. Revision block will be filled in during the week of 2026-05-04 after Issue 03 is live.

---

### Revision 4 — 2026-04-16

Brand & Texture Pass. Eddie's feedback on Rev 3: "this is just fantastic. only thing I'd flag is I want a list of sources. and I want Shipped to be branded. the title to have more style to it. I want to feel like I'm opening a magazine. maybe we need texture or some kind of something. We're 90% there."

**What changed in Rev 4:**

1. **Masthead becomes a logo mark** — "Shipped." is no longer typeset text. It is a designed SVG asset (`masthead.svg`, `masthead-small.svg`) with optical kerning per glyph, a hand-tuned period drawn as a geometric circle rather than a typographic glyph, and four size lockups with adjusted spacing for each context. See Section X: Brand & Texture for full spec.

2. **Warm-white page background** — `#ffffff` replaced by `#FAF8F4` (warm off-white, uncoated stock feel) as the primary page background. Cards, code blocks, and sidebar boxes float at pure `#ffffff` on top of the warm base. The contrast between the warm page and the cooler card surfaces is intentional — it mimics paper against a slightly brighter printed element.

3. **Paper grain texture** — SVG `feTurbulence` noise filter at 3% opacity applied to the layout root. Barely visible. Felt as texture. Technique: inline SVG data URI for CSS background-image (no external PNG dependency). See Section X for exact implementation.

4. **Ink-feel text shadow** — `text-shadow: 0.4px 0.5px 0.8px rgba(0,0,0,0.06)` applied to display headlines (48px+) and front-of-book body text. Simulates ink absorption into uncoated stock. Imperceptible in isolation; changes the register of the letterforms when felt across a full page.

5. **Drop cap ink-bleed** — The Lead Story orange drop cap gains a secondary shadow `0.5px 0.6px 1.0px rgba(180,60,15,0.15)` — same orange ink spreading on paper, not a drop shadow. Stamped feel, not a pasted glyph.

6. **Paper hairline rules** — Section dividers replaced from uniform `rgba(0,0,0,0.10)` to a gradient hairline that fades at both ends, mimicking printed rules on uncoated stock.

7. **Edge vignette** — A `radial-gradient` ::before overlay at 4% maximum opacity applied to the issue cover and archive index hero. Implies the page has physical edges. Not applied to component-level elements.

**New files from Rev 4:**
- `masthead.svg` — Master logo mark (96px render target, 520×120 viewBox)
- `masthead-small.svg` — Small lockup (38px render target, 220×48 viewBox)
- `branding-snippets.html` — Visual catalog: masthead at 4 sizes, texture comparisons, ink-feel samples

---

### Revision 3 — 2026-04-16

Magazine Density Pass. Eddie's feedback on Rev 2: "feels really light. nothing like a magazine. I want more graphics. I want more copy. 3 weeks was a long time. in this world these guys shipped a lot. this is not it yet."

**What changed in Rev 3:**

1. **Full furniture system designed** — 12 new magazine components specified. The publication now has the visual vocabulary to carry 7,000 words of density without feeling like a wall of text.
2. **Drop caps** — 4-line Libre Baskerville drop cap at every feature opener. Lead Story drop cap is orange. Everything else is ink.
3. **Table of Contents** — Wired-style front-of-book ToC. Wall of headlines. First scroll after the cover.
4. **By the Numbers** — Vertical stat infographic. Big Libre Baskerville display numbers with Barlow Condensed kickers. Horizontal rule separators.
5. **Sidebar Box** — Boxed editorial aside. `#fafafa` background, left border accent, internal type hierarchy.
6. **Feature Section Header** — Full-scale feature openers with "FEATURE" kicker, large Libre Baskerville headline, deck. Distinct from short-form section heads.
7. **Comparison Table** — Benchmark data treatment. Monospaced but editorial. Bar-as-typography for the Mythos benchmark chart.
8. **Timeline Graphic** — Dense horizontal/vertical release timeline. 56 events deserve to feel like 56 events.
9. **Term of the Issue Box** — Dictionary-entry sidebar. Headword in Libre Baskerville italic, definition in Inter.
10. **Code Block (leveled up)** — Wired-sidebar weight. Title bar, line numbers, language label.
11. **Section Ornaments / Dividers** — Fleuron ✦, em-dashes, large numerical section markers, hairline rule system.
12. **Quote Attribution** — Magazine-style attribution block for named quotes in investigation pieces.
13. **Vulnerabilities List** — Editorial tabular treatment for the Glasswing zero-days sidebar.
14. **Orange expansion** — Drop cap on Lead Story elevated to orange (5th orange object, earned). Everything else holds the line.

### Revision 2 — 2026-04-16

Three open tensions resolved after editorial direction from Eddie:

**1. Data model split (Tension 1 → resolved)**
Frontmatter schema now specifies `fob_content` and `log_content` as separate keys. See Section 12.1 for full schema. The rendering system reads the key, not the heading text.

**2. Orange usage (Tension 2 → resolved)**
Orange (`#FF6B35`) is in the system, disciplined to four objects. Full rationale and object list in Section 14: Orange Usage Rules. Anything not on that list stays mono, permanently.

**3. POP refinements (Tension 3 → resolved)**
White-canvas mode turned up: display headline to 80px desktop, pull-quote to 28px with a tighter column, inter-section breathing room increased. Changes inline throughout — search `[REV2]` to find each affected value.

---

## 1. Concept Statement

**Shipped.** is *The New Yorker* if The New Yorker covered Anthropic — and its back-of-book was a reference manual that engineers actually grep on Tuesday mornings.

This is not a blog. It's not a newsletter. It's a magazine that happens to run on the same lab coat as id8Labs. The front-of-book is slow, editorial, opinionated — the kind of writing that earns your thirty minutes. The back-of-book is fast, indexed, exhaustive — the kind of reference that earns a bookmark. Both halves require different visual registers. Both must feel like they belong to the same publication.

The visual strategy to hold them together is **typographic authority**. Not color. Not imagery. Not motion. Typography is the personality system here. A refined serif for editorial gravity. A condensed grotesque for the machine-language of tags and kickers. Inter carrying the id8Labs lab coat underneath both. In mono palette, these three voices — literary, mechanical, systematic — create enough register contrast to make the front feel different from the back without needing a different URL.

The aesthetic reference is the working journalist's desk: the legal pad with the handwritten thesis at the top, the stack of technical reference materials below it, the browser tab with the Wired feature still open. Everything matters. Nothing decorates.

**The density principle (added Rev 3):** Magazines are dense. Not cramped — dense. There's a difference. Cramped means no breathing room. Dense means the page rewards looking: multiple visual elements per scroll, headlines stacked before copy blooms, sidebars running alongside prose. The New Yorker is dense. Wired is dense. MIT Technology Review is dense. Shipped. should be dense. Rev 2 was too precious with whitespace. Rev 3 earns the whitespace that remains by packing in what precedes it.

---

## 2. Typography Stack

### The Case for Two Additions to Inter

id8Labs uses Inter exclusively. That's correct for the lab — it signals engineer, not editor. But Shipped. is a publication housed *inside* the lab. It uses the lab's infrastructure but has its own editorial identity, the way a magazine's website lives inside a media company's CMS but doesn't look like the CMS.

The constraint is this: **no additions to the global id8Labs system**. These fonts load only on `/shipped/*` routes. Inter remains the global foundation. The two additions are scoped, conditional, and earn their place.

---

### Font 1: Libre Baskerville (Google Fonts, display + body)

**Why Libre Baskerville, not a premium alternative:**
It is sourced from Google Fonts (zero hosting complexity, no license risk), it was designed for screen legibility at text sizes (not just display), and it carries the weight of editorial authority without the preciousness of, say, Freight Text or Chronicle Display. The New Yorker uses a comparable optical-size serif for body copy. The Financial Times uses a comparable serif for its editorial voice. This is the genre convention. We're borrowing the convention, not reinventing it.

It earns its place in Shipped. on three grounds:
1. Editorial headlines at 48px–80px have a gravity that Inter cannot produce at the same size. Inter is an engineer's typeface. Libre Baskerville is a journalist's typeface. The difference matters when the opening line is *"I woke up this morning and Milo wasn't talking to me."*
2. Body text in the front-of-book reads better in a serif when paragraph density is moderate and the prose is literary. At 18–19px with 1.75 line-height, Libre Baskerville in a 680px column is Wired's feature well. Inter in the same setting is a changelog.
3. The period in "Shipped." — the logo itself — reads with more finality in a serif. The mark is load-bearing.

**Roles:** Display hero (issue cover headline), drop caps, section headings (front-of-book only), body text (front-of-book only), pull-quotes, Term of the Issue headword, By the Numbers display numerals.

---

### Font 2: Barlow Condensed (Google Fonts, mechanical voice)

**Why Barlow Condensed:**
The Release Log needs a visual language that says *machine*, not *essay*. Category tags like `[MODEL]`, `[API]`, `[CODE]` need to feel like circuit board labels. Kickers above section titles need the uppercase confidence of a newspaper's section flag. Barlow Condensed at 400–600 weight, all-caps, with aggressive letter-spacing (+1.5px to +3px) does this without conflict. It's the mechanical counterpart to Libre Baskerville's literary register, and both sit cleanly above Inter's systematic floor.

Linear uses a condensed grotesque for system-status labels. The Financial Times uses a narrow sans for section flags and datelines. This is established typographic grammar for exactly this problem.

**Roles:** Category tags, kicker text (section flags), feature kicker ("FEATURE", "INVESTIGATION", "SURVEY"), issue number, dateline, "Release Log" section header, table of contents labels, By the Numbers kicker labels, Timeline date markers. Never body text. Never headings.

---

### Complete Type Scale

All sizes are for desktop. Mobile scaling follows the responsive section.

| Role | Font | Size | Weight | Tracking | Line Height | Color | Notes |
|------|------|------|--------|----------|-------------|-------|-------|
| **Issue Display** [REV2] | Libre Baskerville | **80px** | 700 | -1.5px | 1.02 | `#1a1a1a` | Cover line headline only |
| **Feature Headline** [REV3] | Libre Baskerville | **44–56px** | 700 | -1.0px | 1.05 | `#1a1a1a` | Feature openers (Glasswing, Agent Stack) |
| **Section Head (FoB)** | Libre Baskerville | 32px | 700 | -0.5px | 1.15 | `#1a1a1a` | Lead Story, Also Shipped titles |
| **Subhead (FoB)** | Libre Baskerville | 22px | 700 | -0.25px | 1.20 | `#1a1a1a` | Secondary editorial heads |
| **By the Numbers Display** [REV3] | Libre Baskerville | **64–80px** | 700 | -1.5px | 1.0 | `#1a1a1a` | Big stat number |
| **ToC Headline** [REV3] | Libre Baskerville | 18px | 700 | -0.2px | 1.20 | `#1a1a1a` | ToC entry title |
| **Issue Kicker** | Barlow Condensed | 12px | 600 | +3.0px | 1.0 | `#898989` | UPPERCASE. "ISSUE #00 — APRIL 18, 2026". Issue number in `#FF6B35` |
| **Section Flag** | Barlow Condensed | 11px | 600 | +2.5px | 1.0 | `#898989` | UPPERCASE. "THE LEAD STORY", "ALSO SHIPPED" |
| **Feature Kicker** [REV3] | Barlow Condensed | 13px | 700 | +3.0px | 1.0 | `#898989` | UPPERCASE. "FEATURE", "INVESTIGATION", "SURVEY" |
| **ToC Label** [REV3] | Barlow Condensed | 9px | 700 | +2.0px | 1.0 | `#898989` | UPPERCASE. "THE LEAD STORY", "ALSO SHIPPED" |
| **By the Numbers Kicker** [REV3] | Barlow Condensed | 11px | 600 | +2.0px | 1.0 | `#898989` | UPPERCASE stat label |
| **Category Tag** | Barlow Condensed | 10px | 700 | +1.5px | 1.0 | varies (see tags) | `[MODEL]`, `[API]`, `[CODE]`, etc. |
| **Log Entry Title** | Inter 600 | 16px | 600 | -0.2px | 1.30 | `#1a1a1a` | Release Log h4 titles |
| **Log Entry Date** | Inter 500 | 13px | 500 | normal | 1.0 | `#898989` | `2026-04-16` datestamps |
| **Body (FoB)** | Libre Baskerville | 18–19px | 400 | normal | 1.75 | `#404040` | Editorial prose only |
| **Body (BoB)** | Inter | 15px | 400 | normal | 1.60 | `#404040` | Release Log summaries, How to use |
| **Sidebar Body** [REV3] | Inter | 14px | 400 | normal | 1.60 | `#404040` | Sidebar box prose |
| **Masthead** | SVG mark (masthead.svg / masthead-small.svg) | See Section X.1 | 700 | optical | 1.0 | `#1a1a1a` / `#FF6B35` period | [REV4] Logo asset, not typeset text. Four size lockups defined in Section X. |
| **Pullquote** [REV2] | Libre Baskerville | **28px** | 400 italic | normal | 1.40 | `#1a1a1a` | Up from 22–24px |
| **Code** | JetBrains Mono | 13px | 400 | normal | 1.60 | `#1a1a1a` | Same as id8Labs system |
| **Code Inline** | JetBrains Mono | 13px | 400 | normal | inherit | `#1a1a1a` | Backtick inline code |
| **Caption / Meta** | Inter | 13px | 400 | normal | 1.40 | `#898989` | Issue date, period, source links |
| **Term Headword** [REV3] | Libre Baskerville | 20px | 400 italic | normal | 1.20 | `#1a1a1a` | Term of the Issue box headword |
| **Term Pronunciation** [REV3] | Inter | 13px | 400 | normal | 1.0 | `#898989` | /ˌʃæ.doʊ rɪˈliːs/ |
| **Quote Attribution** [REV3] | Inter | 13px | 500 | +0.5px | 1.0 | `#6b6b6b` | "— Igor Tsyganskiy, Microsoft" |
| **Timeline Date** [REV3] | Barlow Condensed | 10px | 600 | +1.5px | 1.0 | `#898989` | Date markers on the timeline graphic |
| **Archive Index Title** | Libre Baskerville | 22px | 700 | -0.2px | 1.25 | `#1a1a1a` | Issue card title on /shipped index |
| **Footer Flag** | Barlow Condensed | 10px | 600 | +2.0px | 1.0 | `#898989` | UPPERCASE. "SHIPPED. — A WEEKLY MAGAZINE" |

---

## 3. Masthead Treatment

The masthead is the brand mark. It appears in three contexts: the navigation, the issue cover, and the archive index.

**[REV4] The masthead is a logo, not type.** As of Revision 4, "Shipped." is no longer typeset text. It is a designed SVG asset. See Section X.1 for the full rationale and construction notes. Files: `masthead.svg` (master), `masthead-small.svg` (nav/footer). The rendered appearance is identical to the typeset version — the difference is in the intentionality of the construction: optical kerning per glyph, period as a drawn geometric circle rather than a typographic leftover.

**The period is the design decision.** "Shipped." is not "Shipped" — the period is intentional punctuation, a finality mark. In the SVG mark, the period is a perfect circle drawn at 1.4× the natural Baskerville period size, sitting at the optical baseline. It says: done. Released. No revision needed. It is the only object in the mark drawn from scratch rather than adapted from the typeface.

**[REV2] The period wears the orange.** "Shipped" renders in `#1a1a1a`. The period circle fills `#FF6B35`. This is the only color in the masthead. The rationale: the period is the brand's thesis condensed to a glyph — it earns the accent. The word doesn't. This is the id8Labs dynoc color used as a signature, not a flood. See Section 14 for the complete orange rules.

### In Navigation (persistent, slim bar above issue content)
```
Shipped.    ←   "Shipped" Libre Baskerville 20px 700 #1a1a1a,
                "." same spec but color: #FF6B35
```
Left-aligned. Single line. No tagline. On the right side of this bar: "By id8Labs" in Inter 13px weight 400, `#898989`, with a thin separator. This is the parent-publication signal — not a badge, just a credit.

Separator between masthead and "By id8Labs": `1px solid rgba(0,0,0,0.12)`, height 14px, vertically centered.

The navigation bar sits *above* the site's main Header on Shipped. pages — it's a publication bar, not a site nav. It uses a `1px solid rgba(0,0,0,0.08)` bottom border to separate from the content below. Background: `#ffffff`. Sticky on scroll? No — it should disappear as you scroll. The issue content takes over. Pull-to-top reveals it.

### In Cover (issue hero)
```
SHIPPED.    ←   Barlow Condensed 13px 600, +2.5px tracking,
                #898989, UPPERCASE (period stays gray — this is
                the mechanical voice, not the editorial mark)
```
The masthead on the cover is the *kicker* above the display headline, not the hero itself. This is deliberate. The cover headline — the issue's lead story title — is the visual anchor. "SHIPPED." above it acts as a flag. This is how magazine covers work: the magazine name is recognized, not displayed. In the Barlow Condensed kicker, the period stays `#898989` — the orange period belongs to the editorial masthead register, not the mechanical kicker register.

### In Archive Index
```
Shipped.    ←   "Shipped" Libre Baskerville 40px 700 #1a1a1a,
                "." color: #FF6B35
```
Full masthead at the top of `/shipped` before the issue grid. With the tagline beneath it in Inter 17px weight 400, `#6b6b6b`: *A weekly magazine on what Anthropic is releasing.*

---

## 4. Cover / Hero Treatment (Issue Page)

The issue cover is typographic. No photography. No illustration. No generated imagery. The cover earns its visual weight through type hierarchy, grid, and breathing room alone. This is intentional — it signals that the writing is the product.

### Structure (top to bottom)

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   SHIPPED.                    ISSUE #00  APRIL 16, 2026 │
│   ─────────────────────────────────────────────────── ─ │
│                                                         │
│   THE FOUNDING ISSUE                                    │
│                                                         │
│   The Shadow                                            │
│   Release                                               │
│                                                         │
│   Three weeks of Anthropic, in one read.               │
│                                                         │
│   ─────────────────────────────────────────────────────│
│   April 16, 2026 · 3 weeks in review   FoB  │  Log    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Breakdown:**

**Line 1 (Masthead + Issue Info):** Two-column flex row.
- Left: "SHIPPED." — Barlow Condensed 13px 600, `#898989`, uppercase, +2.5px tracking
- Right: "ISSUE #00  ·  APRIL 16, 2026" — "#00" in `#FF6B35` (see Section 14), rest Barlow Condensed 11px 600, `#898989`, uppercase, +1.5px tracking
- Full-width `1px solid rgba(0,0,0,0.10)` divider below

**Line 2 (Kicker / Issue Descriptor):** Optional. "THE FOUNDING ISSUE" — Barlow Condensed 11px 600, `#898989`, uppercase, +2.5px tracking, 24px top padding after divider.

**Line 3 (Display Headline) [REV2]:** The issue's editorial title.
- Libre Baskerville **80px** weight 700, `#1a1a1a`, letter-spacing -1.5px, line-height 1.02
- Left-aligned within a 780px max-width column
- Responsive: 80px at desktop, 52px at tablet, 38px at mobile
- Cover top padding increased from 80px to **96px** to give the enlarged headline room to breathe

**Line 4 (Deck / Subhead):** The issue's one-sentence subhead.
- Libre Baskerville 20px weight 400, `#6b6b6b`, line-height 1.55
- 20px top spacing from headline (up from 16px — the bigger headline needs more separation)

**Horizontal rule:** `1px solid rgba(0,0,0,0.10)`, full column width, 40px vertical margin (up from 32px)

**Line 5 (Period + Jump Nav):** Optional inline navigation for long issues.
- "April 16, 2026  ·  3 weeks in review" — Inter 13px 400, `#898989`
- On the right: two text-style buttons, "Front-of-book" and "Release Log" — Inter 13px 500, `#1a1a1a`, with a thin underscore on hover. These jump to anchors.

**Cover container geometry [REV2]:**
- Max-width: 780px, centered in the content well
- Vertical padding: **96px** top, **80px** bottom (up from 80/64 — the larger display headline earns more air)
- Background: `#ffffff`
- No decorative borders. No card. White on white.

---

## 5. Editorial Section Components (Front-of-Book)

The front-of-book is a single-column essay. 780px max-width. 18-19px Libre Baskerville body. The section components are punctuation in the prose — they separate without breaking the rhythm.

### 5.1 — The Open (80–150 words, hook)

No special component. This is straight prose. Libre Baskerville 18px 400 `#404040` line-height 1.75.

The only visual signal that this is "The Open" is a **Section Flag** above it:

```
THE OPEN
────────
```

Flag: Barlow Condensed 11px 600, `#898989`, uppercase, +2.5px tracking.
Thin rule below the flag: `1px solid rgba(0,0,0,0.08)`, width 40px (not full-width — it's a short flag, not a divider).
12px gap between flag and body.

---

### 5.2 — The Lead Story (200–300 words, with punchline isolation)

Section Flag as above: "THE LEAD STORY"

**Section headline:** Libre Baskerville 32px 700, `#1a1a1a`, letter-spacing -0.5px, line-height 1.15. This is the lead's story title. 24px below the flag.

**[REV3] Drop Cap — Lead Story opener:**

The first letter of The Lead Story body text renders as a drop cap. 4-line drop cap, Libre Baskerville 700, color `#FF6B35` (orange — the only orange drop cap in the publication, reserved for the lead). All other feature drop caps are `#1a1a1a`.

```css
.drop-cap-lead::first-letter {
  font-family: var(--font-editorial);
  font-size: 4.6em;          /* scales to ~82px at 18px body */
  font-weight: 700;
  float: left;
  line-height: 0.82;
  padding-right: 8px;
  padding-top: 6px;
  color: #FF6B35;            /* orange — lead story only. Object 5 in Section 14 */
  margin-top: 4px;
  /* [REV4] Ink-bleed — stamped feel on warm-white background */
  text-shadow: 0.5px 0.6px 1.0px rgba(180, 60, 15, 0.15);
}

.drop-cap::first-letter {
  font-family: var(--font-editorial);
  font-size: 4.6em;
  font-weight: 700;
  float: left;
  line-height: 0.82;
  padding-right: 8px;
  padding-top: 6px;
  color: #1a1a1a;            /* ink — all other feature openers */
  margin-top: 4px;
}
```

**Body:** Libre Baskerville 18px 400 `#404040`.

**Punchline Isolation (Move B) — the key component [REV2]:**

When the writer isolates a punchline, the sentence renders in its own block. The vertical rule is orange — the single warmest object in 1,800 words of cool mono prose. The pull-quote text is enlarged to 28px.

```css
.shipped-pullquote {
  font-family: 'Libre Baskerville', Georgia, serif;
  font-size: 28px;
  font-weight: 400;
  font-style: italic;
  line-height: 1.40;
  color: #1a1a1a;
  margin: 56px 0;
  padding: 0 0 0 28px;
  border-left: 4px solid #FF6B35;
  max-width: 600px;
}
```

---

### 5.3 — Feature Section Header [REV3]

For longer features (Glasswing Investigation, The Agent Stack, Survey pieces), the opener deserves a full-scale treatment beyond the standard Section Flag + Head.

```
INVESTIGATION                    ← Barlow Condensed 13px 700, +3.0px tracking, #898989, uppercase
─────────────────────────────    ← 1px solid rgba(0,0,0,0.10), full column width

The Glasswing Bet                ← Libre Baskerville 44–56px 700, #1a1a1a, tracking -1.0px
How twelve companies got Mythos  ← Libre Baskerville 19px 400, #6b6b6b, line-height 1.55
before anyone else — and what
it cost them.

by Eddie Belaval                 ← Inter 13px 400, #898989
```

**CSS spec:**
```css
.feature-header {
  margin-bottom: 48px;
  padding-bottom: 40px;
  border-bottom: 1px solid rgba(0,0,0,0.08);
}
.feature-kicker {
  font-family: var(--font-mechanical);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 3.0px;
  color: #898989;
  text-transform: uppercase;
  display: block;
  margin-bottom: 16px;
}
.feature-headline {
  font-family: var(--font-editorial);
  font-size: 48px;
  font-weight: 700;
  color: #1a1a1a;
  letter-spacing: -1.0px;
  line-height: 1.05;
  margin-bottom: 16px;
}
.feature-deck {
  font-family: var(--font-editorial);
  font-size: 19px;
  font-weight: 400;
  color: #6b6b6b;
  line-height: 1.55;
  max-width: 620px;
  margin-bottom: 16px;
}
.feature-byline {
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 400;
  color: #898989;
}
```

---

### 5.4 — Also Shipped (3–5 sections, 60–100 words each)

Section Flag: "ALSO SHIPPED"

Each sub-section has its own mini-heading:

```
### Glasswing got built.
```

**Sub-section head:** Libre Baskerville 22px 700, `#1a1a1a`, letter-spacing -0.25px, line-height 1.20.

A thin horizontal rule separates each sub-section from the next: `1px solid rgba(0,0,0,0.06)`, full column width, 32px vertical margin.

Body: Libre Baskerville 18px 400.

---

### 5.5 — Quiet on the Wire (50–80 words)

Section Flag: "QUIET ON THE WIRE"

Body text only. No sub-sections. No heading beyond the flag. The brevity is the visual signal.

One design addition: this section has a subtle left indent of 24px (via `padding-left: 24px`), no border, no background. It reads like a note at the bottom of a page. Small, aside, worth catching.

---

### 5.6 — The Close (rhythm closer, three beats)

Section Flag: "THE CLOSE"

The Close renders differently from all other body text. Three short sentences. Each on its own line. Extra inter-paragraph spacing (28px between each sentence-paragraph instead of standard 24px). The last line gets 400 weight italic.

```css
.shipped-close p {
  font-family: 'Libre Baskerville', Georgia, serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 1.60;
  color: #1a1a1a;
  margin-bottom: 28px;
}
.shipped-close-final {
  font-style: italic;
  color: #1a1a1a;
}
```

---

## 6. Release Log Entry Component (Back-of-Book)

The Release Log is reference material. The design goal is: scannable at speed, deep on demand.

### Section Header

```
THE RELEASE LOG
───────────────────────────────────────
A 1:1 mirror of every Anthropic release in the window.
```

"THE RELEASE LOG" in Barlow Condensed 14px 600, `#1a1a1a`, uppercase, +2.5px tracking.
Thin rule at full column width below it.
Subline in Inter 15px 400 `#898989`.

---

### Category Section Divider

Each category (Models, API, Claude Code, etc.) opens with:

```css
.log-category-header {
  display: flex;
  align-items: baseline;
  gap: 10px;
  padding: 32px 0 12px 0;
  border-bottom: 1px solid rgba(0,0,0,0.10);
}
.log-category-letter {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 2px;
  color: #898989;
  text-transform: uppercase;
}
.log-category-name {
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 2.5px;
  color: #1a1a1a;
  text-transform: uppercase;
}
```

---

### Individual Entry

```css
.log-entry {
  padding: 24px 0;
  border-bottom: 1px solid rgba(0,0,0,0.06);
}
.log-entry-date {
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 500;
  color: #898989;
  letter-spacing: 0.2px;
  font-feature-settings: 'tnum';
}
.log-entry-title {
  font-family: 'Inter', sans-serif;
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  letter-spacing: -0.2px;
  line-height: 1.30;
}
.log-entry-title a {
  color: inherit;
  text-decoration: none;
  border-bottom: 1px solid rgba(0,0,0,0.15);
  padding-bottom: 1px;
  transition: border-color 0.15s ease;
}
```

---

### Category Tags [REV2]

```css
.log-tag { font-family: 'Barlow Condensed', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; padding: 2px 7px; border-radius: 3px; }
.log-tag--model      { background: #FF6B35; color: #ffffff; }   /* Orange — flagship inflection */
.log-tag--api        { background: #404040; color: #ffffff; }
.log-tag--code       { background: #595959; color: #ffffff; }
.log-tag--apps       { background: #737373; color: #ffffff; }
.log-tag--sdk-py     { background: #e5e5e5; color: #1a1a1a; }
.log-tag--sdk-ts     { background: #ebebeb; color: #1a1a1a; }
.log-tag--research   { background: #f5f5f5; color: #404040; border: 1px solid rgba(0,0,0,0.12); }
.log-tag--news       { background: #f5f5f5; color: #404040; border: 1px solid rgba(0,0,0,0.12); }
.log-tag--deprecation { background: #fafafa; color: #898989; border: 1px solid rgba(0,0,0,0.15); }
```

---

### Code Blocks (Release Log) — Leveled Up [REV3]

Code blocks are no longer plain `fafafa` containers. They now carry a title bar with the language label — the Wired sidebar treatment for code.

```css
.log-code-block-wrap {
  margin: 8px 0 12px 0;
  border: 1px solid rgba(0,0,0,0.10);
  border-radius: 6px;
  overflow: hidden;
}
.log-code-block-title {
  background: #f0f0f0;
  border-bottom: 1px solid rgba(0,0,0,0.08);
  padding: 6px 14px;
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #898989;
  display: flex;
  justify-content: space-between;
}
.log-code-block {
  background: #fafafa;
  padding: 16px 18px;
  overflow-x: auto;
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 400;
  line-height: 1.60;
  color: #1a1a1a;
  -webkit-overflow-scrolling: touch;
}
```

---

## 7. Magazine Furniture — New Components (Rev 3)

This section specifies the 12 new furniture pieces that bring Shipped. to magazine density. Each piece has a designated scroll-position in the issue.

---

### 7.1 — Table of Contents [REV3]

The ToC appears immediately below the cover — first scroll. It's a wall of headlines, not a nav list. This is Wired's issue structure: the ToC tells you what's in the book before you crack the spine.

**Structure:**

```
TABLE OF CONTENTS                ← Barlow Condensed 11px 700, +3.0px tracking, #898989, uppercase
─────────────────────────────    ← 1px solid rgba(0,0,0,0.10), full width

THE LEAD STORY                   ← Barlow Condensed 9px 700, +2.0px tracking, #898989
Opus 4.7, and the chart          ← Libre Baskerville 18px 700, #1a1a1a
that wasn't about Opus 4.7       
The model ships. The bar         ← Inter 13px 400, #898989, italic
it can't beat comes with it.     

INVESTIGATION                    ← Barlow Condensed 9px 700, +2.0px tracking, #898989
The Glasswing Bet                ← Libre Baskerville 18px 700, #1a1a1a
How twelve companies got Mythos  ← Inter 13px 400, #898989, italic
before anyone else.              

... (3-5 entries total)
```

**CSS spec:**
```css
.toc-wrap {
  max-width: 780px;
  margin: 0 auto;
  padding: 0 24px 0;
}
.toc-header {
  font-family: var(--font-mechanical);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 3.0px;
  color: #898989;
  text-transform: uppercase;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(0,0,0,0.10);
  display: block;
  margin-bottom: 0;
}
.toc-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  border-bottom: 1px solid rgba(0,0,0,0.08);
}
.toc-entry {
  padding: 20px 0;
  border-right: 1px solid rgba(0,0,0,0.06);
  border-bottom: 1px solid rgba(0,0,0,0.06);
  padding-right: 24px;
  padding-left: 0;
}
.toc-entry:nth-child(even) {
  padding-left: 24px;
  padding-right: 0;
  border-right: none;
}
.toc-entry-section {
  font-family: var(--font-mechanical);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 2.0px;
  color: #898989;
  text-transform: uppercase;
  display: block;
  margin-bottom: 6px;
}
.toc-entry-title {
  font-family: var(--font-editorial);
  font-size: 18px;
  font-weight: 700;
  color: #1a1a1a;
  letter-spacing: -0.2px;
  line-height: 1.20;
  display: block;
  margin-bottom: 6px;
  text-decoration: none;
}
.toc-entry-title:hover { color: #404040; }
.toc-entry-tease {
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 400;
  font-style: italic;
  color: #898989;
  line-height: 1.45;
}
```

**Mobile:** Collapses from 2-column to 1-column at 680px. Entries stack vertically.

---

### 7.2 — By the Numbers [REV3]

Vertical stat infographic. Big number in Libre Baskerville display (64–80px), kicker above in Barlow Condensed, brief context line below in Inter. Horizontal rules separate each stat. The column runs 360px wide max — this is a sidebar-width component, not full-column.

**Placement:** Runs alongside or below the lead story, before the feature openers. First magazine "graphic" the reader sees.

```
BY THE NUMBERS               ← Barlow Condensed 11px 700, +3.0px tracking, #898989

────────────────────────────

CLAUDE CODE VERSIONS         ← Barlow Condensed 11px 600, +2.0px tracking, #898989
26                           ← Libre Baskerville 80px 700, #1a1a1a, tracking -1.5px
In 21 days.                  ← Inter 14px 400, #404040

────────────────────────────

CYBERSECURITY BENCHMARK      ← label
83.1%                        ← display
Mythos on CyberGym.          ← context

────────────────────────────

MODEL CREDITS PLEDGED        ← label
$100M                        ← display
To Glasswing partners.       ← context

────────────────────────────

OLDEST BUG FOUND             ← label
27 years                     ← display
OpenBSD. Found by Mythos.    ← context
```

**CSS spec:**
```css
.by-the-numbers {
  max-width: 380px;
  margin: 48px 0;
  border-top: 2px solid #1a1a1a;
  padding-top: 20px;
}
.btn-header {
  font-family: var(--font-mechanical);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 3.0px;
  color: #898989;
  text-transform: uppercase;
  display: block;
  margin-bottom: 20px;
}
.btn-item {
  padding: 20px 0;
  border-top: 1px solid rgba(0,0,0,0.10);
}
.btn-item:first-of-type { border-top: none; }
.btn-label {
  font-family: var(--font-mechanical);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 2.0px;
  color: #898989;
  text-transform: uppercase;
  display: block;
  margin-bottom: 4px;
}
.btn-number {
  font-family: var(--font-editorial);
  font-size: 72px;
  font-weight: 700;
  color: #1a1a1a;
  letter-spacing: -2px;
  line-height: 0.95;
  display: block;
  margin-bottom: 6px;
}
.btn-context {
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 400;
  color: #404040;
  line-height: 1.45;
}
```

**On desktop:** Float right alongside the lead story prose (if layout allows), or run as a full-width strip in a two-column flex grid with the lead story on the left (680px) and stats on the right (260px).

---

### 7.3 — Sidebar Box [REV3]

The editorial aside. Used for tangential context, term definitions, "The Mythos Bar" benchmark chart, vulnerability lists, quick footnotes that would break prose flow. Boxed, distinct, readable inline.

**Spec:**
```css
.sidebar-box {
  background: #fafafa;
  border: 1px solid rgba(0,0,0,0.08);
  border-left: 3px solid #1a1a1a;   /* ink left rule — the editorial authority mark */
  border-radius: 0 4px 4px 0;
  padding: 20px 20px 20px 20px;
  margin: 32px 0;
}
.sidebar-box-title {
  font-family: var(--font-mechanical);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2.5px;
  color: #898989;
  text-transform: uppercase;
  display: block;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(0,0,0,0.08);
}
.sidebar-box-body {
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 400;
  color: #404040;
  line-height: 1.60;
}
.sidebar-box-body p { margin-bottom: 10px; }
.sidebar-box-body p:last-child { margin-bottom: 0; }
```

**Variants:**
- Default: `border-left: 3px solid #1a1a1a` — standard editorial aside
- Lead Story sidebar ("The Mythos Bar"): `border-left: 3px solid #FF6B35` — the one sidebar in the issue that gets the orange treatment. This is the chart that matters. The rule signals it.

---

### 7.4 — Comparison Table [REV3]

Used for benchmark data (Opus 4.7 vs GPT-5.4 vs Gemini 3.1 Pro vs Mythos). Monospaced cells, clean rules, editorial weight. The bar-as-typography variant is preferred for benchmarks where you want the visual comparison to speak.

**Bar-as-typography approach (The Mythos Bar):**

Instead of a traditional chart, render the bars as CSS elements within the table. This keeps the typography system — no images, no canvas, no SVG required.

```css
.benchmark-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-family: 'Inter', sans-serif;
}
.benchmark-table th {
  font-family: var(--font-mechanical);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #898989;
  text-align: left;
  padding: 8px 12px 8px 0;
  border-bottom: 1px solid rgba(0,0,0,0.10);
}
.benchmark-table td {
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 400;
  color: #404040;
  padding: 10px 12px 10px 0;
  border-bottom: 1px solid rgba(0,0,0,0.06);
  vertical-align: middle;
}
.benchmark-table tr:last-child td { border-bottom: none; }
.benchmark-model-name {
  font-weight: 500;
  color: #1a1a1a;
  min-width: 160px;
}
.benchmark-score {
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 400;
  color: #1a1a1a;
  min-width: 60px;
}
.benchmark-bar-cell { width: 100%; }
.benchmark-bar-track {
  background: #f0f0f0;
  border-radius: 2px;
  height: 8px;
  position: relative;
  overflow: hidden;
}
.benchmark-bar-fill {
  height: 100%;
  border-radius: 2px;
  background: #1a1a1a;
  transition: width 0.3s ease;
}
/* Mythos row — the model you can't have */
.benchmark-table tr.mythos-row td { background: rgba(0,0,0,0.02); }
.benchmark-table tr.mythos-row .benchmark-bar-fill { background: #FF6B35; }
.benchmark-table tr.mythos-row .benchmark-model-name { color: #1a1a1a; }
.benchmark-table tr.mythos-row .benchmark-score { color: #FF6B35; }
/* The Mythos score gets orange — only orange number in the entire publication */
```

**The Mythos row:** Orange bar fill, orange score number. This is the data point that is the thesis of the issue. It earns color. Everything else stays ink.

---

### 7.5 — Timeline Graphic [REV3]

26 versions of Claude Code in 21 days. 56+ releases in the window. The timeline is a feature-worthy graphic — it should make density visible.

**Treatment:** Vertical timeline with date markers on the left, release bullets on the right. Not a horizontal scroller (too hidden on mobile) — a vertical spine that rewards scrolling.

```css
.timeline-wrap {
  margin: 40px 0;
  position: relative;
}
.timeline-header {
  font-family: var(--font-mechanical);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 3.0px;
  color: #898989;
  text-transform: uppercase;
  display: block;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(0,0,0,0.10);
}
.timeline-spine {
  position: absolute;
  left: 72px;
  top: 0;
  bottom: 0;
  width: 1px;
  background: rgba(0,0,0,0.10);
}
.timeline-row {
  display: flex;
  gap: 0;
  align-items: flex-start;
  min-height: 32px;
  margin-bottom: 2px;
}
.timeline-date {
  font-family: var(--font-mechanical);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 1.0px;
  color: #898989;
  text-transform: uppercase;
  width: 72px;
  flex-shrink: 0;
  padding-top: 3px;
  text-align: right;
  padding-right: 16px;
}
.timeline-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #1a1a1a;
  flex-shrink: 0;
  margin-top: 5px;
  margin-right: 14px;
  position: relative;
  z-index: 1;
}
.timeline-dot--model { background: #FF6B35; }   /* model releases get orange dot */
.timeline-dot--minor {
  background: #ffffff;
  border: 1px solid rgba(0,0,0,0.25);
}
.timeline-content {
  flex: 1;
  padding-bottom: 12px;
}
.timeline-title {
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: #1a1a1a;
  line-height: 1.30;
  margin-bottom: 2px;
}
.timeline-desc {
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 400;
  color: #898989;
  line-height: 1.40;
}
```

**Density rule:** Show all 15–20 most significant events. Minor patch versions (no features) collapse to a single "v2.1.88–v2.1.86: patch cluster" entry. The visual tells the story of velocity.

---

### 7.6 — Term of the Issue Box [REV3]

A dictionary-entry-style component. Appears in the sidebar or between sections. One term per issue. Issue #00: "shadow release."

```
shadow release
/ˌʃæ.doʊ rɪˈliːs/ noun

A model announced alongside a flagship that surpasses it but remains
unavailable to the public. The shadow sets the ceiling; the flagship
sets the floor. The space between them is the new normal.

— Coined in this issue.
```

**CSS spec:**
```css
.term-box {
  border: 1px solid rgba(0,0,0,0.10);
  border-top: 2px solid #1a1a1a;
  padding: 20px 20px 16px;
  margin: 40px 0;
  max-width: 480px;
}
.term-headword {
  font-family: var(--font-editorial);
  font-size: 20px;
  font-weight: 400;
  font-style: italic;
  color: #1a1a1a;
  display: block;
  margin-bottom: 2px;
}
.term-pronunciation {
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 400;
  color: #898989;
  display: block;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(0,0,0,0.06);
}
.term-definition {
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 400;
  color: #404040;
  line-height: 1.60;
  margin-bottom: 12px;
}
.term-attribution {
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 400;
  font-style: italic;
  color: #898989;
}
```

---

### 7.7 — Quote Attribution [REV3]

For named quotes in investigation pieces (Glasswing, governance analysis). Magazine-style, not blockquote-style. The attribution is as important as the quote.

```
"The threats Mythos found would have taken
our teams years to discover manually."

— Igor Tsyganskiy, CTO, Microsoft
```

**CSS spec:**
```css
.named-quote {
  margin: 32px 0;
  padding-left: 20px;
  border-left: 2px solid rgba(0,0,0,0.12);
}
.named-quote-text {
  font-family: var(--font-editorial);
  font-size: 18px;
  font-weight: 400;
  font-style: italic;
  color: #1a1a1a;
  line-height: 1.55;
  margin-bottom: 10px;
}
.named-quote-attribution {
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #6b6b6b;
  letter-spacing: 0.5px;
}
.named-quote-attribution::before { content: "— "; }
```

---

### 7.8 — Vulnerabilities List [REV3]

For the Glasswing sidebar enumerating what Mythos found. Tabular but editorial — not a database dump.

```
WHAT MYTHOS FOUND              ← Barlow Condensed label

OpenBSD kernel (1997)          ← Inter 14px 600
27-year-old memory management  ← Inter 13px 400, #898989
bug. Exploitable remotely.     

FFmpeg codec decoder (2009)    ← Inter 14px 600
16-year-old integer overflow   ← Inter 13px 400, #898989
in video stream parsing.       

Linux kernel privilege chain   ← Inter 14px 600
Multi-step escalation from     ← Inter 13px 400, #898989
user to ring-0. Active kernel. 
```

**CSS spec:**
```css
.vuln-list {
  margin: 16px 0;
}
.vuln-list-header {
  font-family: var(--font-mechanical);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2.0px;
  color: #898989;
  text-transform: uppercase;
  display: block;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(0,0,0,0.08);
}
.vuln-item {
  padding: 10px 0;
  border-bottom: 1px solid rgba(0,0,0,0.06);
}
.vuln-item:last-child { border-bottom: none; }
.vuln-name {
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 2px;
}
.vuln-desc {
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 400;
  color: #898989;
  line-height: 1.45;
}
```

---

### 7.9 — Section Ornaments / Dividers [REV3]

Magazines breathe with ornamental rhythm. These are the punctuation marks of the physical layout.

**The fleuron:** Unicode ✦ (Black Four Pointed Star) or ❧ (Floral Heart). Used as section separators within long features. Centered, Libre Baskerville 14px, `#898989`.

```css
.ornament {
  text-align: center;
  font-family: var(--font-editorial);
  font-size: 14px;
  color: #c0c0c0;
  margin: 48px auto;
  display: block;
  letter-spacing: 12px;
}
/* Usage: <span class="ornament">✦ ✦ ✦</span> */
```

**Large numerical section marker:** For multi-part investigations, a large ordinal number floated left signals the section break.

```css
.section-number {
  font-family: var(--font-editorial);
  font-size: 120px;
  font-weight: 700;
  color: rgba(0,0,0,0.05);
  line-height: 1;
  float: left;
  margin-right: 20px;
  margin-bottom: -20px;
  margin-top: -20px;
  letter-spacing: -4px;
}
```

**Em-dash separator (light use):**

```css
.em-separator {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 40px 0;
  color: rgba(0,0,0,0.12);
  font-family: var(--font-editorial);
  font-size: 16px;
}
.em-separator::before,
.em-separator::after {
  content: '';
  flex: 1;
  height: 1px;
  background: rgba(0,0,0,0.08);
}
```

---

## 8. Density Rules (Rev 3 Addition)

These rules govern how dense each "scroll" of the issue should feel. A "scroll" is approximately 800px of vertical content at desktop.

### Per-scroll targets

| Scroll position | Visual elements expected |
|----------------|--------------------------|
| Scroll 0 (cover) | Cover headline, deck, jump nav. Clean entry moment. |
| Scroll 1 (ToC) | Full ToC grid — wall of headlines. Density starts here. |
| Scroll 2 (By the Numbers) | 4-stat infographic alongside The Open prose. Two columns of content. |
| Scroll 3 (Lead Story opener) | Drop cap, prose, Mythos Bar sidebar. Three visual layers. |
| Scroll 4 (Lead Story continued) | Pull-quote, prose. At least one sidebar box. |
| Scroll 5 (Feature opener: Glasswing) | Full feature header (kicker, 48px headline, deck, byline), drop cap, prose. |
| Scroll 6 (Glasswing continued) | Named quote, vulnerabilities list, prose. |
| Scroll 7 (Survey / Agent Stack) | Feature header, drop cap, code block, sidebar. |
| Scroll 8 (Timeline) | Full 21 Days / 56 Releases timeline graphic. Dense visual. |
| Scroll 9 (Cowork / Papers) | Section flags, sub-section heads, prose. Lighter — the reader is resting. |
| Scroll 10–12 (Quiet / Close / Term) | Term of the Issue box, The Close, ornament. Landing zone. |
| Scroll 13+ (Release Log) | Dense reference. Category headers, entries, tags, code blocks. |

### Vertical rhythm grid (Rev 3)

| Context | Spacing |
|---------|---------|
| Cover padding (top) | 96px |
| Cover padding (bottom) | 80px |
| Between major sections (cover → ToC, ToC → By the Numbers, etc.) | 64px |
| Between front-of-book sections (flag → body) | 48px |
| Between also-shipped sub-sections | 32px |
| Feature header bottom padding | 40px |
| By the Numbers items | 20px top padding each |
| Pull-quote vertical margin | 56px top/bottom |
| Sidebar box margin | 32px top/bottom |
| Term box margin | 40px top/bottom |
| Timeline row spacing | 2px (dense — the closeness is the point) |
| Named quote margin | 32px top/bottom |
| Ornament margin | 48px top/bottom |
| Release Log entry padding | 24px top/bottom |
| Between release log category sections | 40px top padding |

---

## 9. Grid and Spacing System

Shipped. inherits the id8Labs 8px base unit and spacing scale. The editorial column is narrower than the id8Labs standard to support comfortable long-form reading.

### Column Structure

| Zone | Width | Usage |
|------|-------|-------|
| Editorial column | 680px max | Front-of-book body text (at 18-19px serif) |
| Content column | 780px max | Issue cover, section headings, release log |
| Wide column | 1000px max | Reserved (archive grid, potential future) |
| Container | 1200px max | Inherited from id8Labs |

**Two-column layout (Rev 3 addition):** The By the Numbers + Lead Story opener can use a two-column flex grid on desktop only. Left: 680px editorial column. Right: 260px stat column. At 780px breakpoint, the stat column drops below the prose.

```css
.two-col-editorial {
  display: flex;
  gap: 48px;
  align-items: flex-start;
  max-width: 980px;
  margin: 0 auto;
}
.two-col-prose { flex: 1; max-width: 640px; }
.two-col-sidebar { width: 260px; flex-shrink: 0; }
@media (max-width: 780px) {
  .two-col-editorial { flex-direction: column; }
  .two-col-sidebar { width: 100%; }
}
```

---

## 10. Mobile Treatment

Mobile is a primary use case. Eddie reads on his phone. The Release Log is used on Tuesdays at a desk and also in a Slack message as a shared link. Both must work at 375px+.

### Mobile Typography Adjustments [REV2]

| Role | Desktop | Mobile |
|------|---------|--------|
| Issue display headline | **80px** | **44px** |
| Feature headline | **48px** | **32px** |
| Section head (FoB) | 32px | 24px |
| Pullquote | **28px** | **22px** italic |
| By the Numbers display | 72px | 48px |
| Body (FoB) | 18–19px | 17px |
| Log entry title | 16px | 15px |
| Log entry summary | 15px | 14px |
| Category tag | 10px | 10px (unchanged) |
| Masthead (cover kicker) | 13px | 11px |

### Mobile Layout Adjustments

- Cover: headline drops to 44px, deck to 17px, vertical padding from 96px → 48px
- ToC: 2-column → 1-column at 680px breakpoint
- By the Numbers: full-width, single column, numbers at 48px
- Feature headers: headline drops to 32px
- Sidebar boxes: full-width inline — no floating
- Front-of-book: editorial column goes full-width with 20px side padding
- Pullquote: `padding-left` drops from 28px to 20px, `border-left` stays 4px orange
- Timeline: full-width vertical, date column compresses to 52px
- Release Log entries: full-width, 24px side padding, no changes to internal structure
- Code blocks: `overflow-x: auto` already specified — horizontal scroll on mobile
- Category tags: same size, same treatment
- Archive index: 2-col → 1-col at `md:` breakpoint (768px)

---

## 11. Archive Index Page (`/shipped`)

The archive is the issue back-catalog. Every issue is a card. The page communicates *publication*, not *blog*.

### Page Header

```
Shipped.                   ← "Shipped" Libre Baskerville 40px 700 #1a1a1a,
                              "." color: #FF6B35
A weekly magazine on what Anthropic is releasing.
                           ← Inter 17px 400, #6b6b6b
Published every Friday at 5 PM ET.
                           ← Inter 14px 400, #898989
```

Below: a thin full-width `1px solid rgba(0,0,0,0.08)` rule, 48px margin below it.

### Issue Cards

2-column grid at desktop, 1-column at mobile. 32px gap.

Each card:
- Background: `#ffffff`
- Shadow: id8Labs standard card shadow (`rgba(0,0,0,0.08) 0px 0px 0px 1px, rgba(0,0,0,0.06) 0px 1px 3px -1px, rgba(0,0,0,0.04) 0px 4px 8px -4px`)
- Border-radius: 10px
- Padding: 28px

---

## 12. Issue File Structure & Data Model

### 12.1 — Frontmatter Schema

Every issue file uses this frontmatter structure. The `fob_content` and `log_content` keys are the structural delimiter that drives the rendering split.

```yaml
---
issue: "00"
title: "The Founding Issue — The Shadow Release"
headline: "The Shadow Release"
deck: "Three weeks of Anthropic, in one read."
date: "2026-04-16"
period_start: "2026-03-27"
period_end: "2026-04-16"
period_label: "3 weeks in review"
status: "dry-run"
masthead: "Shipped."
toc:
  - section: "THE LEAD STORY"
    title: "Opus 4.7, and the chart that wasn't about Opus 4.7"
    tease: "The model ships. The bar it can't beat comes with it."
    anchor: "#lead"
  - section: "INVESTIGATION"
    title: "The Glasswing Bet"
    tease: "How twelve companies got Mythos before anyone else."
    anchor: "#glasswing"
  - section: "SURVEY"
    title: "21 Days, 56 Releases"
    tease: "What Claude Code becoming an IDE looks like from the changelog."
    anchor: "#timeline"
  - section: "TERM OF THE ISSUE"
    title: "shadow release"
    tease: "A word for the thing Anthropic does now."
    anchor: "#term"
by_the_numbers:
  - label: "CLAUDE CODE VERSIONS"
    number: "26"
    context: "In 21 days."
  - label: "CYBERSECURITY BENCHMARK"
    number: "83.1%"
    context: "Mythos on CyberGym."
  - label: "MODEL CREDITS PLEDGED"
    number: "$100M"
    context: "To Glasswing partners."
  - label: "OLDEST BUG FOUND"
    number: "27 yrs"
    context: "OpenBSD. Found by Mythos."
fob_content: |
  ...
log_content: |
  ...
---
```

---

## 13. Design Tensions — Resolved

### Tension 1: Front-of-book font mode switch — RESOLVED
**Decision:** Option C extended. Structured frontmatter with `fob_content` and `log_content` keys. The rendering system reads the key; the section wrapper sets the context.

### Tension 2: The Orange — RESOLVED
**Decision:** Orange is in. See Section 14 for the complete rules. Five objects in Rev 3.

### Tension 3: Essay vs. Magazine body type — NOTE PRESERVED
The existing `/writing/[slug]` route uses a dark-mode-leaning treatment. Shipped. is explicitly light-mode, white-canvas. The mode switch when navigating between the two is intentional.

### Tension 4 (Rev 3): Whitespace vs. density — RESOLVED
**Decision:** Be generous where it earns something. The cover still breathes — that's intentional, it's the entry moment. Inside the issue, density is expected and rewarded. The ToC is a wall. The By the Numbers is tightly packed. The feature openers expand the type scale, not the whitespace.

---

## 14. Orange Usage Rules

**The accent:** `#FF6B35` — id8Labs dynoc orange. In Shipped., it appears on exactly five objects. Nothing else. No exceptions without a revision to this section.

### The Five Objects

**Object 1: The period in "Shipped."**
- Where: masthead (nav bar, archive index header)
- Rationale: The period is the brand's thesis condensed to a glyph.

**Object 2: The issue number on the cover kicker and archive card**
- Where: "#00", "#01", etc. within the "ISSUE #00 · DATE" kicker line
- Rationale: Serial identity. Scannable at a glance.

**Object 3: The pull-quote vertical rule**
- Where: `border-left` of `.shipped-pullquote` — `4px solid #FF6B35`
- Rationale: The punchline earns the mark.

**Object 4: The `[MODEL]` category tag**
- Where: `.log-tag--model` background — `background: #FF6B35; color: #ffffff`
- Rationale: A new model is a capability inflection. Orange signals "hot."

**Object 5: The Lead Story drop cap [REV3]**
- Where: `::first-letter` of the Lead Story opening paragraph only
- Spec: `color: #FF6B35` on the drop cap character — Libre Baskerville 700, 4-line height
- Rationale: The Lead Story is the editorial core of the issue. The orange drop cap is a visual editorial decision — it marks the entrance to the most important piece of writing in the publication. Every other feature drop cap is `#1a1a1a`. Only the lead gets the orange. This is the difference between the editorial center and everything around it.

**Object 6: The Mythos row in benchmark tables [REV3]**
- Where: `.benchmark-table tr.mythos-row .benchmark-bar-fill` and `.benchmark-score`
- Spec: `background: #FF6B35` on bar fill; `color: #FF6B35` on the score number
- Rationale: The Mythos bar is the thesis of Issue #00. The model you can't have. Orange on the bar and score makes the gap visible — it's data that earns color.

**Note:** Objects 5 and 6 were added in Rev 3 as the density pass revealed two new moments of editorial weight that justified the accent. The discipline holds: if you're tempted to add another object, ask whether it carries the same editorial weight as these six. If the answer is no, the answer is no.

### What Does Not Get Orange

Everything else. Specifically:
- Body text links (use the `border-bottom` underline treatment)
- Section flags and kickers (stay `#898989`)
- Feature kickers (stay `#898989` — "INVESTIGATION" is mechanical, not editorial)
- Headings (never)
- The "Read issue →" CTA link (stays `#1a1a1a`)
- Code blocks (stay `#fafafa` / `#1a1a1a`)
- Timeline dots for non-model events (stay `#1a1a1a`)
- Named quote attribution (stays `#6b6b6b`)
- Sidebar box border-left (stays `#1a1a1a` — the ink rule is editorial authority, not warmth)

---

## X. Brand & Texture

This section was added in Revision 4. It governs the masthead as a brand asset and the full texture system that makes Shipped. feel like a magazine rather than a webpage.

---

### X.1 — The Masthead Mark

The masthead is no longer typeset text. It is a designed SVG asset.

**Files:**
- `masthead.svg` — Master lockup (96px render target, 520×120 viewBox). Use for: cover hero, archive index header.
- `masthead-small.svg` — Small lockup (38px render target, 220×48 viewBox). Use for: navigation bar, footer credit.

**Construction rationale:**

The typographic period in Libre Baskerville 700 at 80px is a font artifact. It is not a designed object — it is the leftover after the uppercase and lowercase glyphs are drawn. The period is Shipped.'s thesis condensed to a single mark. It should be drawn, not inherited.

The period in both SVG files is a perfect circle — not an ellipse, not a font glyph. It sits at the optical baseline (not the mathematical baseline) and is drawn at 1.4× the size a Baskerville period would render at the same font size. Color: `#FF6B35` — the only color in the mark.

The letterforms in the master SVG are individually positioned using manual `x` offsets to apply optical kerning beyond what the font's kern table provides. At 96px rendering, Baskerville's default spacing opens certain pairs (S-h, p-p) in ways that make the mark read as words rather than a logo. The per-glyph placement closes those gaps.

**Four size lockups:**

| Context | SVG file | CSS height | Notes |
|---------|----------|------------|-------|
| Cover / hero | `masthead.svg` | `height: 80px` | With ink-feel text-shadow |
| Archive index header | `masthead.svg` | `height: 48px` | With ink-feel text-shadow |
| Navigation bar | `masthead-small.svg` | `height: 24px` | No ink-feel (too small) |
| Footer | `masthead-small.svg` | `height: 16px` | Color: #898989, period at 80% opacity |

**In Next.js:** Use `<Image>` component for the SVG files. For the nav bar, an inline SVG is preferred to avoid a network request on every page load.

**The period color rule:** In the editorial register (nav masthead, archive header), the period is `#FF6B35` — this is Object 1 in Section 14. In the mechanical/kicker register (cover flag "SHIPPED."), the period stays `#898989` — it's in the Barlow Condensed context, not the editorial context. The orange period belongs to the mark; the mechanical kicker inherits the kicker color. This distinction is documented in Section 3 and preserved in the SVG assets.

---

### X.2 — Page Background: Warm White

**Primary page background:** `#FAF8F4`

This replaces `#ffffff` as the background for all issue content areas. It is a warm off-white — approximately what photographers call "natural white" rather than "tungsten white." At a normal reading distance it registers as white. Side-by-side with pure white, it reads as paper.

**Secondary (cards, code blocks, sidebar boxes):** `#ffffff`

The contrast between warm page (#FAF8F4) and cool card (#ffffff) is intentional. It reads like a printed element lifted off the page — a sidebar box, a code sample — that has a slightly different paper stock than the surrounding page. This effect is strongest for sidebar boxes and the `.term-box` component.

**Color values:**
```
Page background:    #FAF8F4   (warm off-white — uncoated stock)
Cards / code:       #FFFFFF   (pure white — floats above the page)
Table background:   #F8F6F2   (optional — for dense reference tables, slightly cooler than page)
```

**CSS variable update (add to `:root`):**
```css
:root {
  --page-warm:   #FAF8F4;
  --page-cool:   #FFFFFF;
  --page-table:  #F8F6F2;
}
```

Update `body { background: var(--page-warm); }` in the `/shipped/layout.tsx` CSS.

---

### X.3 — Paper Grain Texture

**Technique:** SVG `feTurbulence` filter embedded as CSS `background-image` data URI.

This approach has zero external dependencies, renders at native resolution on retina displays, and does not require a PNG sprite or network request.

**Implementation:**

```css
/* Apply to: .shipped-page-root (the layout wrapper for all /shipped/* content) */
.shipped-page-root {
  background-color: #FAF8F4;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Cfilter id='grain'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='400' height='400' filter='url(%23grain)' opacity='0.03'/%3E%3C/svg%3E");
}
```

**Parameters to know:**
- `baseFrequency: 0.65` — Fine grain. Increase to 0.80 for coarser texture; decrease to 0.50 for softer.
- `numOctaves: 4` — Layered noise for natural variation. Do not reduce below 3.
- `opacity: 0.03` — 3%. This is the maximum. At 4% the texture becomes visible as grain rather than felt as paper. At 2% it disappears entirely on most displays.
- `type: fractalNoise` — Natural variation. Use `turbulence` for a more aggressive industrial feel; `fractalNoise` is correct for paper.

**Do not apply grain to:** Cards, code blocks, sidebar boxes, the `.nav-bar`, Release Log entries. These use `--page-cool (#ffffff)` and sit visually above the grained page. Applying grain to both the base and the floating elements removes the layering effect.

---

### X.4 — Edge Vignette

A radial gradient `::before` pseudo-element that darkens the corners of the page, suggesting physical paper depth.

**Apply to:** Issue cover container, archive index page hero only. Not to component-level elements.

```css
/* Applied to .cover and .archive-hero via the .page-vignette modifier class */
.page-vignette {
  position: relative;
  overflow: hidden;
}
.page-vignette::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse at 50% 50%,
    transparent 55%,
    rgba(0,0,0,0.04) 100%
  );
  pointer-events: none;
  z-index: 1;
}
.page-vignette > * {
  position: relative;
  z-index: 2;
}
```

**Maximum opacity: 4%.** At 5% it starts to look like a CSS shadow effect rather than a paper characteristic.

---

### X.5 — Ink-Feel Text Shadow

Simulates ink absorption into uncoated stock. Printed letterforms on uncoated paper have a slight spread at the edges — the ink absorbs into the fibers and the dots from the press have a fractional bleed radius.

**For display headlines (48px and above):**
```css
text-shadow: 0.4px 0.5px 0.8px rgba(0,0,0,0.06);
```

**For body text (front-of-book only, 18–19px Libre Baskerville):**
```css
text-shadow: 0.4px 0.5px 0.8px rgba(0,0,0,0.06);
/* Same values — at body size the effect is subtler due to smaller letterforms */
```

**For pull-quotes (28px italic):**
```css
text-shadow: 0.4px 0.5px 0.8px rgba(0,0,0,0.05);
/* Slightly lower opacity — italic letterforms have more visual movement already */
```

**Do not apply to:**
- Type below 24px (reads as rendering blur, not texture)
- Inter (the id8Labs system font — ink-feel is editorial serif only)
- Barlow Condensed kickers and flags
- Code blocks
- Release Log (back-of-book) — that section is reference material, not editorial prose

**The key constraint:** At 6% opacity on a warm-white background, the shadow is imperceptible in isolation. It is only felt across a full paragraph or page of text. This is correct behavior. If you can clearly see the shadow on a single letter at normal reading size, the opacity is too high.

---

### X.6 — Drop Cap Ink-Bleed

The Lead Story orange drop cap gets a secondary shadow treatment that simulates the ink bleeding slightly into the paper fibers at the edges of the letterform.

```css
/* Replace the existing .drop-cap-lead::first-letter text-shadow with this: */
.drop-cap-lead::first-letter {
  font-family: var(--font-editorial);
  font-size: 4.6em;
  font-weight: 700;
  float: left;
  line-height: 0.82;
  padding-right: 8px;
  padding-top: 6px;
  color: #FF6B35;
  margin-top: 4px;
  /* Rev 4 addition: */
  text-shadow: 0.5px 0.6px 1.0px rgba(180, 60, 15, 0.15);
  /* Shadow color is #B43C0F at 15% opacity — desaturated dark version of #FF6B35.
     Not black. The ink is the same color as the letter, just denser at the bleed edge. */
}
```

**Why `rgba(180, 60, 15, 0.15)` and not `rgba(0,0,0,0.10)`:**
A black shadow on an orange letter would read as an artificial 3D lift. The shadow must be in the same color family as the letterform — the darker burnt orange at low opacity simulates the same ink pooling at the edge of the press mark. This effect is most visible where the orange meets the warm-white page (#FAF8F4) — the slight temperature contrast between the warm orange and the near-warm background makes the bleed perceptible.

**Black drop caps** (all feature openers other than the Lead Story) do not need the ink-bleed treatment — the color contrast between `#1a1a1a` and `#FAF8F4` is already high enough to read as printed. The bleed treatment on those would add noise, not warmth.

---

### X.7 — Paper Hairline Rules

Section dividers are upgraded from uniform `rgba(0,0,0,0.10)` lines to gradient hairlines that fade at both ends.

```css
/* Replace all section divider rules with this: */
.paper-rule {
  height: 1px;
  background: linear-gradient(
    to right,
    rgba(0,0,0,0.02),
    rgba(0,0,0,0.12) 15%,
    rgba(0,0,0,0.10) 50%,
    rgba(0,0,0,0.12) 85%,
    rgba(0,0,0,0.02)
  );
  border: none;
}
```

**Apply to:**
- Cover kicker row divider
- ToC section rule (`.toc-header` border-bottom)
- Between-section dividers in front-of-book
- Feature header rule (`.feature-header` border-bottom)

**Do not change:**
- Release Log entry dividers (those are structural separators, not editorial ornaments — keep uniform `rgba(0,0,0,0.06)`)
- Sidebar box border-left (that's a component rule, not a page rule)
- The full-bleed rule after the cover kicker row (use standard — that one reads better with mechanical precision)

---

### X.8 — Texture Application Map

A complete guide to where each technique applies in the component hierarchy.

| Component | Warm BG | Grain | Vignette | Ink Shadow | Paper Rule |
|-----------|---------|-------|----------|------------|------------|
| Page layout root | YES | YES | NO | NO | NO |
| Issue cover | YES (inherited) | YES (inherited) | YES | Headlines only | YES |
| Nav bar | YES | NO | NO | NO | Bottom: YES |
| ToC | YES (inherited) | YES (inherited) | NO | NO | YES |
| By the Numbers | YES (inherited) | YES (inherited) | NO | NO | YES |
| Feature headers | YES (inherited) | YES (inherited) | NO | Headline only | YES |
| Front-of-book body | YES (inherited) | YES (inherited) | NO | YES | YES |
| Pull-quotes | YES (inherited) | YES (inherited) | NO | YES (0.05) | NO (border-left) |
| Lead Story drop cap | YES (inherited) | YES (inherited) | NO | Ink-bleed (orange) | NO |
| Sidebar box | #FFFFFF (overridden) | NO | NO | NO | NO |
| Code block | #FAFAFA (overridden) | NO | NO | NO | NO |
| Release Log | YES (inherited) | YES (inherited) | NO | NO | NO |
| Log entries | YES (inherited) | YES (inherited) | NO | NO | NO (structural) |
| Archive index | YES | YES | YES (hero) | Headline only | YES |
| Archive cards | #FFFFFF (overridden) | NO | NO | NO | NO |

---

*Section X added in Revision 4 — 2026-04-16. Iris, id8Labs AI designer.*

---

## 15. Implementation Notes for Next.js

### Route Structure

```
app/
  shipped/
    page.tsx               ← Archive index — /shipped
    layout.tsx             ← Shipped. layout (pub bar, fonts scoped here)
    [issue]/
      page.tsx             ← Issue page — /shipped/00
      components/
        ShippedCover.tsx
        ShippedTOC.tsx
        ShippedByTheNumbers.tsx
        ShippedSection.tsx
        ShippedFeatureHeader.tsx
        ShippedPullquote.tsx
        ShippedSidebarBox.tsx
        ShippedBenchmarkTable.tsx
        ShippedTimeline.tsx
        ShippedTermBox.tsx
        ShippedNamedQuote.tsx
        ShippedVulnList.tsx
        ShippedClose.tsx
        LogEntry.tsx
        LogCategoryHeader.tsx
        LogTag.tsx
        LogCodeBlock.tsx
```

### Font Loading (Scoped to /shipped/*)

```tsx
import { Libre_Baskerville, Barlow_Condensed } from 'next/font/google'

const libreBaskerville = Libre_Baskerville({
  weight: ['400', '700'],
  style: ['normal', 'italic'],
  subsets: ['latin'],
  variable: '--font-editorial',
  display: 'swap',
})

const barlowCondensed = Barlow_Condensed({
  weight: ['400', '600', '700'],
  subsets: ['latin'],
  variable: '--font-mechanical',
  display: 'swap',
})
```

---

## 16. Reference Provenance

Design decisions in this document draw from the following reference systems:

| Decision | Source |
|----------|--------|
| Table of Contents — 2-column wall of headlines | Wired issue structure, The Atlantic digital ToC |
| By the Numbers — large display numerals with kickers | MIT Technology Review data graphics; The Economist statistical sidebars |
| Drop cap — float left, 4-line, serif | New Yorker and Harper's feature openers; The Atlantic lead stories |
| Orange drop cap on lead only | The Economist's red drop cap on leaders (editorials); reserved for the house's most important editorial position |
| Feature header (kicker + 48px headline + deck + byline) | Wired feature well; The Atlantic magazine format |
| Comparison table with bar-as-typography | Financial Times chart typography; Stripe's usage of typographic data in blog posts |
| Term of the Issue box | Dictionary entry format per Oxford/Merriam-Webster digital; McSweeney's editorial asides |
| Named quote attribution | Magazine journalism standard — Harper's, The New Yorker |
| Vulnerabilities list | Editorial table format per Wired security coverage |
| Timeline vertical spine | MIT Technology Review timelines; Linear's changelog visual format |
| Section ornaments (fleurons) | New Yorker typographic ornaments; McSweeney's section breaks |
| Density rules per scroll | Wired, MIT Tech Review, The Atlantic — all target 3+ visual elements per scroll in features |
| Two-column prose + stat sidebar | New Yorker "Dept. of..." column with sidebar; Financial Times feature well |
| Serif editorial body type for long-form | The New Yorker web, Financial Times, Stripe editorial |
| Condensed grotesque for kickers / flags | Newspaper section flags; Linear's system label language |
| Monochrome tonal tag system | Cal.com badge system; Vercel semantic badge variants |
| 680px editorial column width | Robert Bringhurst CPL standard; New Yorker and Atlantic web columns |
| Orange period as brand signature | id8Labs DESIGN.md dynoc accent; The Economist red brand mark |

---

*DESIGN.md — Revision 4 updated by Iris, id8Labs AI designer. April 16, 2026.*
*Revision 3 authored April 16, 2026. Revision 2 authored April 16, 2026. Revision 1 authored April 16, 2026.*
*Sister document to STYLE.md. Both evolve together.*
