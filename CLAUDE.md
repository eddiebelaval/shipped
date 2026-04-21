# CLAUDE.md — Shipped.

> The entry point for any Claude session working in this repo.
> Read this file first. Then read whatever it points you to.

---

## What this project is

**Shipped.** is a weekly magazine covering Anthropic releases. Published by id8Labs. Ships every Friday at 9 AM ET.

The pipeline scrapes, the front-of-book is written, the verifier prevents lies, and the human pushes git. That sequence does not change.

**Live site:** id8labs.app/shipped
**Repo:** github.com/eddiebelaval/shipped (this repo — pipeline + content, MIT)
**Deploy target:** sibling repo `id8labs/` (what Vercel sees)

---

## The triad — read order

These three docs at repo root define the project. Read them in this order when you need full context. For most tasks, this file is enough.

1. **VISION.md** — why Shipped. exists, who it's for, scope, moat, non-negotiables
2. **SPEC.md** — pipeline architecture, verification gates, invariants, data flow
3. **BUILDING.md** — build log, origin story, operational lessons

---

## Invariants

These are load-bearing. Violating any of them is a hard stop.

1. **Human-gated publish.** The pipeline stages (`git add`). Eddie runs `git commit && git push`. Never automated. Never bypassed.
2. **Verifier runs on every issue.** No bypass flag. If the verifier can't run, publish is blocked.
3. **Markdown is the source of truth.** HTML is always a function of `(md, lang)`. No HTML-only edits.
4. **English is the canonical language.** Translations start from the EN file. Translation changes never modify EN copy.
5. **Voice gate is immutable mid-issue.** STYLE.md can be amended between issues. It cannot be amended to pass an issue that's currently failing.
6. **The period is part of the name.** Always render as `Shipped.` — never `Shipped` without the period.

---

## File conventions

### Content files

```
content/issue-NN-{slug}.md      — canonical issue (e.g., issue-00-the-founding.md)
content/issue-NN-wip.md         — working document before slug is assigned
content/articles/issue-NN/      — source articles that feed into an issue
content/STYLE.md                — voice rules, forbidden phrases, approved moves
content/DESIGN.md               — design system (colors, type, layout)
content/index.md                — series archive
TRACKER.md                      — article inventory + per-issue rollup (see below)
```

### Source articles

Source articles are the raw material that feeds each issue. They live in `content/articles/issue-NN/` and track through three stages: **research → draft → used**. Each article has frontmatter linking it to an issue and a section.

See `TRACKER.md` for the full inventory and per-issue rollup. See the tracker for the frontmatter spec and naming conventions.

### Issue frontmatter (required)

```yaml
---
issue: 02
slug: presence                    # assigned at running-order lock (Thursday)
title: "The Product Turn"         # assigned at running-order lock
status: draft                     # values: dry-run | draft | published | archived
ship_date: 2026-04-24
running_order_locked: false       # flips to true on Thursday lock
---
```

### Naming rules

- Issue numbers are zero-padded two digits: `01`, `02`, `10`
- Slugs are lowercase, hyphenated: `the-shadow-release`, `presence`
- WIP files use `wip` as the slug until Thursday lock
- Published issues are immutable. Corrections go in a new commit with `[corr]` prefix

### Pipeline files

```
pipeline/src/scrape/        — @claudedevs feed → JSON
pipeline/src/render/        — markdown → HTML magazine
pipeline/src/verify/        — attestation gates (URL, number, quote, date, voice)
pipeline/src/orchestrate/   — chains scrape + render + verify + stage
pipeline/output/            — scraper output (gitignored)
```

---

## Working patterns

### When writing or editing issue copy

1. Read `content/STYLE.md` before generating any prose. Re-read the voice training corpus if tone drifts.
2. Write to the WIP file (`content/issue-NN-wip.md`) or the local draft. Never write directly to a published issue file.
3. Follow the section order from STYLE.md: Cover Line → Open → Lead Story → Also Shipped → Quiet on the Wire → The Close → Release Log.
4. Every numeric claim needs a source link within 3 paragraphs. Every quote needs attribution. The verifier will catch you if you don't.
5. Run the voice gate mentally before outputting: no forbidden phrases, max 1 "X isn't Y, it's Z" in the front-of-book.

### When working on the pipeline

1. Read `SPEC.md` for architecture and gate definitions.
2. Read `pipeline/README.md` for scripts and environment setup.
3. Tests live in `pipeline/test/`. Run with `cd pipeline && pnpm test`.
4. Never hard-code paths. Use the environment variables in `.env.example`.
5. The renderer always writes to `../id8labs/public/shipped/`. This is by design — enforces the repo split.

### When researching for an issue

1. Read the current WIP file to understand what's already known and what's still open.
2. Signal reports go in a separate file (e.g., `issue-02-signal-report-YYYY-MM-DD.md`), not in the WIP.
3. Every claim needs a primary source URL. "I read somewhere" is not a source.
4. Attribute carefully: "reported by [outlet]" not "announced by [company]" unless it's an official announcement.
5. Convert all dates to absolute format (YYYY-MM-DD). "Last Thursday" decays; "2026-04-17" doesn't.

---

## The editorial workflow

See `EDITORIAL.md` for the full lifecycle of an issue from signal to ship.

**Quick reference — the week's rhythm:**

| When | What | Who |
|---|---|---|
| Mon–Wed | Signal collection, research, WIP updates | Claude + Eddie |
| Thursday | Running order locks. Slug assigned. Prose begins. | Eddie decides, Claude drafts |
| Thursday PM | `pnpm scrape` for Release Log data | Pipeline |
| Friday 7 AM | Final scrape run | Pipeline |
| Friday 8 AM | Release Log merged, copy reviewed | Eddie |
| Friday 8:55 AM | `pnpm publish` — render + verify + stage | Pipeline |
| Friday 9 AM | `git commit && git push` | Eddie (human gate) |

---

## Voice — the short version

Full rules in `content/STYLE.md`. The essentials:

- **Kill rule:** If it sounds like a press release, kill it. If it sounds like a LinkedIn post, kill it twice.
- **Forbidden:** EPIC, "thrilled to," "ushers in," "game-changing," "industry-leading," "synergies," "robust solution," "best-in-class," "unveiled," "empowers users to," "leverage."
- **Budget:** Max 1 "X isn't Y, it's Z" per issue.
- **Tone:** Dry, confident, never breathless. Opinions stated, never hedged. Sentence length varies aggressively.
- **Personality:** Rolling Stone meets Wired. The byline is a person, not a publication.

---

## What NOT to do

- Never commit or push on Eddie's behalf. Stage only.
- Never modify a published issue file. Corrections are new commits with `[corr]` prefix.
- Never amend STYLE.md to pass a failing issue.
- Never fabricate a source, a quote, or a number. The verifier exists because this matters.
- Never skip the voice gate. If copy has a forbidden phrase, fix the copy — don't rationalize the phrase.
- Never auto-generate the front-of-book without Eddie's editorial direction. The pipeline scrapes; the front-of-book is curated.

---

## Dependencies and environment

```bash
# Pipeline setup
cd pipeline && pnpm install

# Key scripts
pnpm scrape            # Run X scraper standalone
pnpm render <file.md>  # Render without verifying
pnpm verify <file.md>  # Verification gates only
pnpm publish <file.md> # Full pipeline: scrape + render + verify + stage
pnpm test              # Renderer + verifier tests
```

No secrets required for basic pipeline operation. All sources are public.
`ANTHROPIC_API_KEY` is reserved for future LLM-assisted translation steps.

---

## Drift watch

Known inconsistencies to resolve:

- `content/index.md` says "Friday 5 PM ET" — **stale**. Canonical time is **Friday 9 AM ET** per VISION.md and pipeline README.
- Issue 01 shipped from the pre-extraction repo (`id8/knowledge/series/shipped/`). Its canonical copy doesn't exist in `content/` yet. Issue 00 (`issue-00-the-founding.md`) is the founding dry-run.
