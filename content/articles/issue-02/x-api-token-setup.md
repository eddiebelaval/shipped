---
title: "Setup: X API v2 bearer token for the Shipped. scraper"
issue: 2
section: ops
status: research
created: 2026-04-22
updated: 2026-04-22
grade_override: true
grade_override_reason: "Operational setup doc. Not editorial. OVR."
---

# Setup: X API v2 bearer token for the Shipped. scraper

> The scraper at `shipped/pipeline/src/scrape/` tries the X API v2 first, then falls back to Nitter mirrors. Nitter is dead as of April 2026 (every public mirror we've tested returns empty or 404). So if X_API_BEARER_TOKEN is unset, the scraper returns 0 tweets and the Release Log has to be built from web research. This is fine as a fallback but slow. Setting a token takes 10 minutes and makes Thursday night's top-off scrape a single command.

## What the scraper needs

- A **bearer token** (not full OAuth). Read-only, app-level.
- Access to **v2 `/tweets/search/recent`** (7-day lookback window).
- Rate limit: `300 requests / 15-min / app` on Basic. Basic tier is free or $100/mo depending on cadence.

Basic-tier is almost certainly enough: one scrape per week hits maybe 40 requests.

## Steps (you do this, I can't)

### 1. Create the app in the X developer portal

```
1. Visit developer.x.com (or developer.twitter.com; same place).
2. Sign in with the Shipped. / id8Labs account.
3. Click "Projects & Apps" > "Overview".
4. Create a Project if one does not exist (name: "Shipped. magazine").
5. Inside the Project, create an App (name: "shipped-scraper").
6. Choose the Basic tier. Free tier may NOT include /tweets/search/recent.
```

### 2. Generate the bearer token

```
7. In the App's "Keys and Tokens" tab, click "Generate" under "Bearer Token".
8. Copy the token once. It will not be shown again. If you lose it, regenerate.
```

### 3. Store it where the scraper reads

The scraper reads `X_API_BEARER_TOKEN` from the environment. Store it in a gitignored `.env` file:

```bash
# shipped/pipeline/.env   (gitignored)
X_API_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAA_your_token_here
```

Verify `.env` is in the gitignore:

```bash
cd /Users/eddiebelaval/Development/id8/shipped
grep -E "^\.env$|^pipeline/\.env$" .gitignore || echo ".env" >> pipeline/.gitignore
```

### 4. Teach the scraper to load dotenv

The current scraper reads `process.env.X_API_BEARER_TOKEN` but does not auto-load `.env`. Two options:

**Option A: Export before running.**
```bash
cd /Users/eddiebelaval/Development/id8/shipped/pipeline
set -a; source .env; set +a
pnpm scrape --days 1 --dry
```

**Option B: Add dotenv to the script entry.** Edit `pipeline/src/scrape/cli.ts` line 1 to import dotenv:

```typescript
import 'dotenv/config';   // first line
import { scrapeClaudedevs } from './index.js';
```

Then `pnpm add dotenv` in the pipeline directory.

Option B is cleaner; Option A is zero-dep.

### 5. Dry-run to verify

```bash
cd /Users/eddiebelaval/Development/id8/shipped/pipeline
pnpm scrape --days 1 --dry
```

Expected output:

```
[scrape] X API: authenticated
[scrape] @claudedevs: N tweets in last 1d
[scrape] (dry-run, no output written)
```

Not expected:

- `X_API_BEARER_TOKEN not set; skipping X API` (token is unset or not loaded)
- `401 Unauthorized` (token is invalid or app lacks the scope)
- `429 Too Many Requests` (you hit the rate limit; wait 15 min)

### 6. Production run

Once the dry-run works, the Thursday night top-off is one command:

```bash
cd /Users/eddiebelaval/Development/id8/shipped/pipeline
pnpm scrape --days 7
```

Output appends to `articles/issue-NN/release-log-research.md`. Re-run `pnpm assemble --issue NN` to pull the new entries into the canonical under the right A–G category (auto-categorizer handles the mapping).

## Rotation cadence

- Rotate the bearer token every 90 days. Set a calendar reminder.
- If the token leaks (git history, accidental log, screenshot on a stream), regenerate immediately. Old token dies at rotation.
- Never share the token in a DM, email, or PR description. Use 1Password (or similar) to pass it between devices.

## Rate-limit notes

- Basic tier: 300 reqs / 15 min / app. One `/tweets/search/recent` call returns up to 100 results. For a 7-day window on @claudedevs the scraper typically makes 1 to 3 requests total. You will not hit the ceiling.
- If X ever bumps you to Elevated (they sometimes audit), the ceiling rises. Same scraper code works.

## Why not OAuth

OAuth (user context) would let the scraper act on behalf of the Shipped. account. We don't want that. Bearer tokens are scoped to the app, read-only, safer to rotate.

## If X dies or becomes hostile

Three fallbacks, in preference order:

1. **Alternative scraper**: [scrape.do](https://scrape.do), [ScraperAPI](https://www.scraperapi.com), [Browse AI](https://www.browse.ai) all have Twitter/X scraping as a service. Paid, but lets you continue without a direct API.
2. **Manual pull**: visit x.com/claudedevs weekly, copy tweets by hand into `release-log-research.md`. Works for a 7-day window in 10 minutes.
3. **Web-research fallback**: the current state. Use releasebot.io + GitHub CHANGELOG + primary outlets. Slower and less complete, but lives.

Document whichever you land on in `PIPELINE.md`.

## Open TODOs

- [ ] Create X dev account if not already one for id8Labs.
- [ ] Create Project + App.
- [ ] Generate bearer token.
- [ ] Store in `shipped/pipeline/.env`.
- [ ] Run dry-run to verify.
- [ ] Update PIPELINE.md with the "token is set" status line.
