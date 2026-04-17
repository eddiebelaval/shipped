# SPEC.md — Shipped.

> The technical architecture, invariants, and build contracts for the Shipped. magazine pipeline.

---

## System shape

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SHIPPED. PIPELINE                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  scrape     @claudedevs X feed (7d window)                          │
│             → pipeline/output/x-claudedevs/{date}.json              │
│                                                                     │
│  author     Claude + Eddie hand-curate front-of-book copy           │
│             → content/issue-NN-{slug}.md                            │
│                                                                     │
│  render     markdown (+ lang) → magazine HTML                       │
│             → ../id8labs/public/shipped/NN/index.html               │
│                                                                     │
│  verify     URL liveness + number/quote/date attestation +          │
│             voice gate                                              │
│             → passes or blocks; nothing ships on fail               │
│                                                                     │
│  stage      git add (NEVER commit, NEVER push)                      │
│             Human pushes from id8labs/ on Friday 9 AM ET            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Repo layout

```
shipped/
├── VISION.md, SPEC.md, BUILDING.md  ← Triad (at root)
├── README.md, LICENSE (MIT)
├── TECHNOLOGY_WATCHLIST.md          ← tools we've evaluated, not yet installed
├── content/                         ← canonical source of truth (markdown + design assets)
│   ├── index.md                     ← series index
│   ├── STYLE.md                     ← voice rules (the forbidden phrases list)
│   ├── DESIGN.md                    ← design system for the magazine
│   ├── issue-NN-{slug}.md           ← one file per issue; canonical copy
│   ├── {lang}/issue-NN-{slug}.md    ← translations (future: es/, pt/)
│   └── {mockups, mastheads, snippets, launch-copy} ← design artifacts
└── pipeline/                        ← the build system
    ├── package.json                 ← @id8labs/shipped-pipeline
    ├── src/
    │   ├── scrape/                  ← @claudedevs feed → JSON
    │   ├── render/                  ← markdown → HTML magazine
    │   ├── verify/                  ← attestation gates
    │   └── orchestrate/             ← scrape + render + verify + stage
    ├── cron/                        ← scheduled lifecycle
    ├── scripts/                     ← dev utilities
    └── test/                        ← renderer + verifier tests
```

## The four gates

Every issue passes through the verifier before staging. A gate failure blocks publish.

### 1. URL liveness
- Fetches every link.
- Fails on 4xx/5xx.
- 10s timeout, concurrency 8.
- **Known issue:** some domains (e.g. `red.anthropic.com`, Axios, Medium) block the verifier's user agent and return 403 to live URLs. These are on a fragile-domain allowlist that marks them as "can't verify, don't fail."

### 2. Number-claim attestation
- For each numeric claim with a source link within 3 paragraphs, fetches the source and confirms the number appears.
- Formatting tolerance: `$100M` matches `$100 million` matches `100M dollars`.
- **Planned:** per-language tolerance — `$100M` ≈ `100 millones` ≈ `100 milhões`.

### 3. Quote attestation
- Fuzzy match (80% word-overlap threshold) of quoted strings against source plain text.
- Flags below threshold as WARN; below 60% as FAIL.

### 4. Date attestation
- "shipped on YYYY-MM-DD" style claims fetched and confirmed in source.

### Voice gate (not a verifier gate, a style check)
- Scans markdown for `STYLE.md` forbidden phrases: `EPIC`, "thrilled to," "ushers in," "game-changing," "industry-leading," etc.
- Counts "X isn't Y, it's Z" formula — fails if more than 1 in front-of-book.

## Invariants

These do not change without a VISION.md amendment.

1. **Human-gated publish.** The pipeline stages (`git add`). The human runs `git commit && git push`. Never automated.
2. **Verifier runs on every issue.** No bypass flag. If the verifier can't run (network down), publish is blocked.
3. **Markdown is the source of truth.** HTML is always a function of `(md, lang)`. No HTML-only edits.
4. **English is the canonical language.** All translations start from `issue-NN-{slug}.md`. Translation changes do not modify EN copy.
5. **Voice gate is immutable mid-issue.** You can amend STYLE.md between issues. You cannot amend it to pass an issue that's failing.

## Data flow

### Input → markdown
- `pipeline/output/x-claudedevs/{date}.json` — raw scraper output, one file per run.
- `content/issue-NN-{slug}.md` — the canonical issue, with front-matter, front-of-book, and release log.

### Markdown → HTML
- `pipeline/src/render/template.ts` — the magazine template.
- `pipeline/src/render/sections/` — per-section renderers (front-of-book, release log, sources).
- Output: `../id8labs/public/shipped/NN/index.html`.

### Translation (v2+)
- `content/{lang}/issue-NN-{slug}.md` — translated copy.
- Renderer called with `lang` parameter → `../id8labs/public/shipped/NN/{lang}/index.html`.
- Verifier runs per-language with lang-specific number/date formatting tolerance.

## Publishing contract

The renderer **always** writes to `../id8labs/public/shipped/` (relative to the `shipped/` repo root). This is hard-coded by design — it enforces the split:

- **`shipped/`** = pipeline + content (this repo, open source).
- **`id8labs/`** = the deploy target (site repo, the thing Vercel sees).

Never host the magazine directly from `shipped/`. Never build HTML anywhere but `id8labs/public/shipped/`.

## Versioning

- `shipped/` repo follows semver for the pipeline (`package.json`).
- Each issue has a monotonic number (`01`, `02`, ...) and a slug (`the-shadow-release`).
- Issue markdown is immutable after publish. Corrections happen via a new commit with a `[corr]` prefix and a note at the bottom of the issue.

## Dependencies

Current (installed):
- `remark`, `remark-frontmatter`, `remark-parse`, `remark-stringify`, `unified` — markdown processing.
- `gray-matter`, `yaml` — frontmatter.
- `tsx`, `typescript` — dev.

Watchlist (evaluated, not installed):
- See `pipeline/TECHNOLOGY_WATCHLIST.md`.

## Environment

- `ANTHROPIC_API_KEY` — not currently used; reserved for future LLM-assisted translation/editing steps.
- No secrets required for the basic pipeline. All sources are public.

## Testing

- Renderer tests: `pipeline/test/render.test.ts` — snapshot-ish tests against known markdown.
- Verifier tests: `pipeline/test/verify.test.ts` — per-gate fixtures covering pass, warn, fail cases.
- Run: `cd pipeline && pnpm test`.
