# PIPELINE.md — Shipped.

> The data-flow source of truth. Where every `.md` file lives, how weekly content moves through the pipeline, and what command writes what.
> Companion to: VISION, SPEC, BUILDING, STYLE, FORMULA, RUBRIC, TRACKER.

---

## The one-line invariant

Every file for a given week lives in **`content/articles/issue-NN/`** plus two top-level files (`content/issue-NN-wip.md`, `content/issue-NN-{slug}.md`). Nothing else. No scattered inputs. No hidden staging.

---

## Directory map

```
shipped/content/
├── FORMULA.md         Weekly skeleton: sections, word budgets, inventory minimums.
├── STYLE.md           Voice rules. Kill list. Approved moves.
├── RUBRIC.md          Grading rubric (v2). Seven dimensions, 28 points.
├── TRACKER.md         Master inventory: every article, every issue, current status.
├── PIPELINE.md        This file.
│
├── index.md           Public series archive (readers hit this).
│
├── issue-02-wip.md           Working doc for the current week. Metadata, locks,
│                              decisions, Thursday checklist. Graduates at lock.
├── issue-02-presence.md      Canonical issue. The file the renderer reads.
│                              Named after the locked slug (here: "presence").
│
└── articles/
    └── issue-02/
        ├── signal-report.md                   Monday research sweep.
        ├── claude-design-reception.md         Lead-story source (A 28/28).
        ├── conway-leak-analysis.md            Feature / B-story source.
        ├── trust-week-lovable.md              Investigation, half A.
        ├── trust-week-vercel.md               Investigation, half B.
        ├── presence-as-category.md            Companion option 1.
        ├── counter-signal-field-moved.md      Companion option 2.
        ├── also-shipped-*.md                  Three items.
        ├── openclaw-anthropic-return.md       Also Shipped.
        ├── quiet-claude-code-pro-test.md      Quiet on the Wire.
        ├── term-of-issue-presence.md          Term definition scaffold.
        ├── close-prep.md                      Close rhythm scaffold.
        ├── front-of-book-draft.md             Open prose + pre-flight checklist.
        ├── release-log-research.md            Release-log research window.
        ├── launch-copy.md                     Friday launch-day copy scaffold.
        ├── ship-checklist.md                  T-48h to T+24h ops checklist.
        ├── post-ship.md                       Saturday retrospective scaffold.
        ├── _highlights.jsonl                  Reader-drawer highlights (append-only).
        └── assets/                            Hero images, OG sources, PNGs, SVGs.
```

---

## The weekly data flow

```
Monday AM
  /shipped-signal                        writes -> articles/issue-NN/signal-report.md

Tue-Wed
  /shipped-wip                           writes -> articles/issue-NN/{topic}.md
                                                   issue-NN-wip.md (metadata, decisions)
  /shipped-dashboard                     reads  <- articles/issue-NN/*.md
                                                   issue-NN-wip.md
                                         writes -> articles/issue-NN/_highlights.jsonl
                                                   (via reader drawer)

Thu AM (lock)
  Eddie locks running order, slug, term  writes -> issue-NN-wip.md frontmatter

Thu PM (draft)
  /shipped-assemble                      reads  <- articles/issue-NN/*.md
                                                   issue-NN-wip.md
                                         writes -> issue-NN-{slug}.md
                                         (mechanical body extraction; no prose)
  /shipped-draft                         reads  <- issue-NN-{slug}.md
                                                   articles/issue-NN/*.md (voice notes)
                                                   STYLE.md, FORMULA.md
                                         writes -> issue-NN-{slug}.md
                                         (Eddie + Claude: human voice)

Thu PM (scrape)
  pnpm scrape                            writes -> pipeline/output/x-claudedevs/*.json
                                         reads  <- articles/issue-NN/release-log-research.md
                                         merges -> articles/issue-NN/release-log-research.md

Fri 7 AM
  Final scrape + release-log merge       writes -> issue-NN-{slug}.md Release Log section

Fri 8:55 AM
  /verify-shipped                        reads  <- issue-NN-{slug}.md
                                         gates:  URL, number, quote, date, voice
  /publish-shipped                       reads  <- issue-NN-{slug}.md
                                         writes -> ../id8labs/public/shipped/NN/index.html

Fri 9:00 AM
  Eddie: git commit && git push          writes -> live site

Sat
  /shipped-post-ship                     writes -> articles/issue-NN/post-ship.md
```

---

## Source-of-truth rules

1. **Every weekly .md lives under `articles/issue-NN/`.** Never scatter files across random directories. Never create a separate "drafts" folder. Never save to the pipeline output directory.
2. **The dashboard reads from `articles/issue-NN/`.** If you want to see a file on the dashboard, it must live there.
3. **The canonical (`issue-NN-{slug}.md`) is DERIVED from `articles/issue-NN/`.** The canonical is the output; the articles are the input.
4. **The renderer reads only the canonical.** It does not read `articles/issue-NN/` directly. The assemble step is the bridge.
5. **Nothing auto-edits the canonical without an explicit command.** The dashboard's `/api/move` edits `articles/issue-NN/` frontmatter, never the canonical.
6. **Highlights are append-only to `_highlights.jsonl`.** Never overwritten.

---

## Commands and what they touch

| Command | Reads | Writes |
|---|---|---|
| `/shipped-signal` | X feed, web | `articles/issue-NN/signal-report.md` |
| `/shipped-wip` | signal report, user input | `articles/issue-NN/{topic}.md`, `issue-NN-wip.md` |
| `/shipped-dashboard` (or `pnpm dashboard-dev`) | `articles/issue-NN/*.md`, `issue-NN-wip.md` | browser only; drag-drop edits article frontmatter |
| `/shipped-assemble` (new) | `articles/issue-NN/*.md`, `issue-NN-wip.md` | `issue-NN-{slug}.md` (canonical) |
| `/shipped-draft` | canonical, all articles, STYLE, FORMULA | `issue-NN-{slug}.md` (Eddie-voiced prose) |
| `pnpm scrape` | X API or Nitter, web | `pipeline/output/x-claudedevs/*.json`, `articles/issue-NN/release-log-research.md` |
| `pnpm render {canonical}` | `issue-NN-{slug}.md` | `../id8labs/public/shipped/NN/index.html`, `/tmp/shipped-render-output.html` |
| `/verify-shipped` | canonical | nothing (gate check) |
| `/publish-shipped` | canonical | `../id8labs/public/shipped/NN/`, stages to git |
| `/shipped-stop` | port 4321 | kills the dev server |

---

## The assemble step

Gap closed on 2026-04-22. Previously, going from `articles/issue-NN/*.md` to `issue-NN-{slug}.md` was a manual copy-paste operation.

`/shipped-assemble` (or `pnpm assemble --issue NN`) now does this mechanically:

1. Reads `issue-NN-wip.md` for frontmatter (slug, title, term, date, period).
2. Reads every `.md` in `articles/issue-NN/` and groups by `section:` frontmatter.
3. For each article, extracts the "shippable body" (everything before the first scaffolding H2).
4. Assembles into the canonical with the renderer-recognized section names (`## The Open`, `## The Lead Story`, etc.).
5. Preserves the existing Release Log if the canonical already exists; else injects a placeholder.
6. Writes `content/issue-NN-{slug}.md`.

Scaffolding H2s that mark the end of shippable body (and get stripped):

- `## Attribution caveats`
- `## How this fits the issue`
- `## For builders`
- `## The stake`
- `## Operator-layer implications` (and variants)
- `## Voice notes for ...`
- `## Voice budget ...`
- `## Named evidence`
- `## Open questions ...`
- `## Cross-references within the issue`
- `## The Close move it enables`
- `## Format note`
- `## Category groupings`
- `## Still pending`

The canonical produced by `/shipped-assemble` is a **draft-zero**, not shipping prose. Eddie still writes voice on Thursday via `/shipped-draft`. Assemble's job is to let the renderer preview the issue shape without manual paste.

---

## Auto-assemble on render

`pnpm render` now checks if the canonical exists:

- If yes, render it as-is (no reassembly; preserves Eddie's edits).
- If no, run assemble first to produce a draft-zero canonical, then render.

This lets `pnpm render content/issue-02-presence.md` "just work" even the first time after articles land. A future enhancement would re-assemble when any article is newer than the canonical (treat the canonical as a build artifact).

---

## Naming conventions

- Issue numbers: zero-padded two-digit (`01`, `02`, `10`).
- Slugs: lowercase, hyphenated (`the-shadow-release`, `presence`).
- WIP file: `issue-NN-wip.md` until Thursday lock. Slug-named at lock.
- Article filenames: `{topic-slug}.md` or `{section}-{topic}.md` for Also Shipped items.
- Asset files: PNG/SVG under `articles/issue-NN/assets/`.
- Highlights: append-only JSONL at `articles/issue-NN/_highlights.jsonl`.

---

## Drift watch

Anti-patterns to reject on sight:

1. A file for this week that does not live in `articles/issue-NN/`. Move it there.
2. Any command that writes outside `content/` or `pipeline/output/`.
3. A canonical that was edited by hand but never registered in the WIP or TRACKER.
4. A published issue with source articles still in `status: research` or `draft`. Must be flipped to `used` post-ship.
5. A `{slug}` that changed mid-week without a TRACKER entry noting why.

---

## Changelog

| Date | Change | Reason |
|---|---|---|
| 2026-04-22 | Initial draft. Codifies the flow after the manual assembly of Issue 02's canonical. Adds `/shipped-assemble` as a first-class step. | Closed the gap Eddie flagged: "we need a source of truth and a pipeline for where data .md files get pulled from." |
