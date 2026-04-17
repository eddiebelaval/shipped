# Shipped.

A weekly magazine for builders who can't — or won't — stay glued to social media, aggregating the week's Anthropic releases into one read that's worth the time.

**Live:** [id8labs.app/shipped](https://id8labs.app/shipped)
**Published by:** [id8Labs](https://id8labs.app)
**Cadence:** Every Friday, 9 AM ET.

---

## What this repo contains

- **`VISION.md`** — what Shipped. is, who it's for, what's in and out of v1.
- **`SPEC.md`** — the technical architecture, invariants, and build contract.
- **`BUILDING.md`** — the build log. How Shipped. came together.
- **`content/`** — the canonical markdown copy for each issue, plus the style guide, design system, and the launch artifacts. Source of truth.
- **`pipeline/`** — the build system. Scrapes Anthropic releases, renders the magazine HTML, verifies every claim, and stages output for human-gated publish.

## How it works

```
content/issue-NN-*.md
        ↓
pipeline: scrape → render → verify → stage
        ↓
../id8labs/public/shipped/NN/index.html
        ↓
Eddie commits and pushes → Vercel deploys
```

The pipeline never publishes on its own. The human at `git push` is the final gate, always.

## Running the pipeline

```sh
cd pipeline
pnpm install
pnpm scrape              # refresh the @claudedevs feed
pnpm render <issue.md>   # markdown → HTML
pnpm verify <issue.md>   # attestation gates only
pnpm publish <issue.md>  # full pipeline: scrape + render + verify + stage
pnpm test                # renderer + verifier tests
```

The publish command **stages** changes in `../id8labs/public/shipped/`. It does not commit and it does not push. That's the human's job.

## The verifier

The core of the pipeline. Before any issue ships, every claim passes through four gates:

1. **URL liveness** — every link resolves (with a fragile-domain allowlist for sources that block scrapers).
2. **Number attestation** — numeric claims are fetched from their source and compared.
3. **Quote attestation** — fuzzy-match against source text.
4. **Date attestation** — dates confirmed in source.

Plus a voice gate that reads `content/STYLE.md` and fails on forbidden phrases.

A gate failure blocks publish. See `SPEC.md` for the full contract.

## Fork it

If you want to do this for your own domain — your own ecosystem, your own releases — fork this repo. The pipeline is general; only the scraper target and the style guide are Anthropic-specific. Open an issue if you run into something that needs generalizing.

## License

MIT. See `LICENSE`.

---

_Shipped. is published by id8Labs. The human at `git push` is the final gate._
