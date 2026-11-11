# Shipped. Pipeline

The build system for the **Shipped.** weekly magazine. Scrapes Anthropic releases, renders the magazine HTML, verifies every claim against its source, and stages for human-gated git push.

**Never auto-publishes.** The human at `git push` is the final gate.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    THE WEEKLY PIPELINE                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  THU PM   /shipped --draft                                  │
│           writes knowledge/series/shipped/issue-NN.md       │
│           (markdown copy, hand-curated by Claude + Eddie)   │
│                                                             │
│  FRI 7AM  pnpm scrape                                       │
│           fetches @claudedevs tweets from past 7d           │
│           writes output/x-claudedevs/{date}.json            │
│                                                             │
│  FRI 8AM  /shipped --refresh-log                            │
│           merges scraper output into Release Log            │
│                                                             │
│  FRI 8:30 Eddie reviews markdown on his terms               │
│                                                             │
│  FRI 8:55 pnpm publish issue-NN.md                          │
│           = scrape (cached) + render + verify + stage       │
│           ↳ render → id8labs/public/shipped/NN/index.html   │
│           ↳ verify → blocks if any claim fails attestation  │
│           ↳ stage  → git add (NEVER commit, NEVER push)     │
│                                                             │
│  FRI 9AM  Eddie git commit + push (HUMAN GATE)              │
│           Vercel auto-deploys ~2 min later                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Components

| Module | Path | Purpose |
|---|---|---|
| **Renderer** | `src/render/` | Markdown → HTML magazine. Template extracted from MOCKUP-FINAL.html. |
| **Verifier** | `src/verify/` | The lying-prevention layer. URL liveness, number-claim attestation, quote attestation, date attestation. Blocks publish on any failure. |
| **Scraper** | `src/scrape/` | Frontier-labs X feeds → JSON output. Sources in order: X MCP → X API → Nitter. `--enrich` adds an MCP search sweep for cross-lab signal. Cross-references against existing Release Log. |
| **Orchestrator** | `src/orchestrate/` | Chains scrape → render → verify → stage. The `pnpm publish` entry point. |

## Scripts

```bash
pnpm install           # First-time setup
pnpm scrape            # Run X scraper standalone
pnpm render <file.md>  # Render an issue without verifying
pnpm verify <file.md>  # Run verification gates only
pnpm publish <file.md> # Full pipeline: scrape + render + verify + stage
pnpm test              # Run test suite (verifier and renderer)
```

## Environment

```
X_MCP_URL=...                 # X MCP server endpoint (PREFERRED source; tried first)
X_MCP_BEARER_TOKEN=...        # Auth for the X MCP server
X_MCP_TIMELINE_TOOL=...       # Optional override (default: get_user_posts)
X_MCP_SEARCH_TOOL=...         # Optional override (default: search_posts)
X_API_BEARER_TOKEN=...        # X API v2 token (fallback after MCP; then Nitter)
SHIPPED_X_ENRICH=on|off       # Run the MCP search sweep in the orchestrator (default: on)
SHIPPED_DEPLOY_PATH=...       # Default: ../../../id8labs/public/shipped
SHIPPED_KNOWLEDGE_PATH=...    # Default: ../../../knowledge/series/shipped
```

### X MCP — the preferred source + enrichment

The scraper resolves a feed through three sources in order: **X MCP → X API → Nitter.**
X's MCP server is read-only and dependency-free here — `src/scrape/x-mcp.ts` speaks
JSON-RPC 2.0 over MCP Streamable HTTP with built-in `fetch`, the same posture as the
X API client. No `@modelcontextprotocol/sdk` dependency.

Beyond pulling a lab's own timeline, the MCP unlocks **enrichment**: a `--enrich`
search sweep that pulls posts *about* each lab's products from anyone — the cross-lab
and third-party signal a single feed never sees. This is the structural answer to the
recurring "issue collapsed to two paragraphs" failure (see `content/DAILY.md`): the
front-of-book digs deeper when there's more real signal to dig through, and lever 6
(cross-lab contrast) needs exactly this wider net. Enrichment is MCP-only and a
graceful no-op when `X_MCP_URL` is unset, so the pipeline degrades cleanly to the
X API / Nitter path.

```bash
pnpm scrape --enrich                 # timeline + MCP search sweep (default terms)
pnpm scrape --search "Claude Code"   # explicit term, repeatable (implies --enrich)
pnpm scrape --no-mcp                 # force the X API / Nitter path
```

## The verification gates

Every gate must pass for `pnpm publish` to stage changes. Any failure exits non-zero with details printed.

| Gate | What it does |
|---|---|
| **URL liveness** | HEAD-requests every link in the issue. Fails on 4xx/5xx. |
| **Number attestation** | For each numeric claim with a source link nearby, fetches the source and confirms the number appears (with tolerance). |
| **Quote attestation** | For each quoted attribution, fetches the source and fuzzy-matches the quote string. |
| **Date attestation** | For each "shipped on YYYY-MM-DD" claim, confirms the source page mentions that date. |
| **Voice gate** | Scans for STYLE.md forbidden phrases. EPIC, "thrilled to," etc. |
| **"X isn't Y" overuse** | Counts the formula. Fails if more than 1 occurrence. |
| **Orange budget** | Counts orange-rendered objects. Fails if budget exceeded. |

## Failure modes

- **Verifier fails:** Stage is aborted. Eddie reviews the failure log, fixes the markdown, re-runs.
- **Scraper sources unreachable:** X MCP → X API → Nitter are tried in order; each failure is logged and the next is tried. If all fail, an empty result with `failureReason` is written and the pipeline continues (the X feed is supplemental, not blocking).
- **Renderer template missing:** Hard fail. Pipeline can't proceed.
- **Git working tree dirty in id8labs:** Hard fail. Pipeline refuses to stage on top of unrelated changes.

## What this pipeline does NOT do

- Does not commit. Ever.
- Does not push. Ever.
- Does not auto-deploy.
- Does not modify the original markdown in `knowledge/series/shipped/` (read-only source).
- Does not call Anthropic's API for generation. The writer agent (Claude) generates the markdown via `/shipped`; this pipeline only renders + verifies it.

## Versioning

| Version | Status | Notes |
|---|---|---|
| 0.1.0 | Foundation laid | Tonight (Apr 16). Skeleton for renderer, verifier, scraper. |
| 0.2.0 | Verifier shippable | Target: Tue Apr 21. URL + number + quote attestation working. |
| 0.3.0 | Renderer shippable | Target: Wed Apr 22. End-to-end render of Issue #01 markdown matches hand-built HTML. |
| 0.4.0 | Scraper integrated | Target: Thu Apr 23. @claudedevs tweets in source pool. |
| 1.0.0 | First autonomous run | Target: Fri Apr 24. Issue #02 ships via `pnpm publish` + Eddie's `git push`. |
