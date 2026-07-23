# Shipped. — Home of Record

> One magazine. One home. Everything points here.
>
> Audited and consolidated 2026-06-08.

## The home

**`https://id8labs.app/shipped`** is the canonical, public home of Shipped.

- **The hub** (all issues, newest first): `https://id8labs.app/shipped`
- **An issue**: `https://id8labs.app/shipped/{NN}` — e.g. `/shipped/04`

`id8labs.app` is the live id8Labs domain. `id8labs.tech` is email-only and does
**not** serve web — never link Shipped there. Every issue's `<link rel="canonical">`
and `og:url` already resolve to `id8labs.app/shipped/{NN}`; every outbound message
(launch copy, social, email) advertises the same.

## How the pieces fit (no duplicate homes)

**Three streams feed the hub**, and they arrive by different routes. All three
must stay current or `id8labs.app/shipped` understates what has been published.

**1. Numbered magazine issues** — the marquee editions, written by hand.

```
content/issue-NN-*.md            source of truth for an issue (this repo)
        │  pipeline render
        ▼
id8labs/public/shipped/NN/       the published issue page  →  id8labs.app/shipped/NN
id8labs/public/shipped/archive.html   the hub ARCHIVE (was index.html until the
                                      dynamic /shipped route took the index slot)
        │  pipeline sync-manifest (derives from the archive)
        ▼
id8labs/lib/shipped/issues.data.ts   AUTO-GENERATED mirror of the archive
        │  consumed by
        ▼
/shipped hub + /writing feed + homepage featured slot
```

**2. Daily editions and 3. weekly/monthly sweeps** — published by the routines to
the `daily-pages` branch, served from GitHub Pages, mirrored into the hub by a
manifest builder:

```
shipped repo, origin/daily-pages branch
  anthropic-daily/YYYY-MM-DD.html      the daily editions
  anthropic-weekly/YYYY-WW.html        the weekly sweeps
  anthropic-monthly/YYYY-MM.html       the monthly roundups
        │  id8labs/scripts/build-daily-manifest.mjs
        ▼
id8labs/lib/shipped/dailies.data.ts   AUTO-GENERATED
id8labs/lib/shipped/sweeps.data.ts    AUTO-GENERATED
        │  consumed by
        ▼
/shipped hub — "The daily editions." and "The sweeps." sections
```

The archive (`public/shipped/archive.html`) is the source of truth for the
numbered issues; the `daily-pages` branch is the source of truth for dailies and
sweeps. Nothing on the hub is hand-maintained.

**Keeping streams 2 and 3 current is automated — it has to be.** The manifest
builder is not part of any publish path (the routines run in the cloud; the
builder reads a local git checkout), so for five weeks nothing ran it: on
2026-07-23 the hub advertised 40 dailies ending Jun 15 while 77 were live
through Jul 22, and every weekly and monthly sweep was a public page nothing
linked to. `id8labs/scripts/refresh-shipped-manifest.sh` now runs daily at 23:15
(`com.id8labs.shipped-manifest-refresh`), regenerating both files and pushing
only if they changed. If the hub ever looks thin again, read
`~/Library/Logs/shipped/manifest-refresh.log` first.

## Every place Shipped is referenced, and what it is

| Place | Role | Canonical? |
|---|---|---|
| `id8labs.app/shipped` | The hub (all issues) | **Yes — the home** |
| `id8labs.app/shipped/{NN}` | An issue | **Yes** |
| `id8labs.app/writing` (Magazine filter) | Unified feed listing; links out to `/shipped/{NN}` | Mirror of the hub |
| `eddiebelaval.github.io/shipped/anthropic-daily/{date}` | A daily edition | **Yes — the daily home** |
| `eddiebelaval.github.io/shipped/anthropic-weekly/{YYYY-WW}` | A weekly sweep | **Yes** |
| `eddiebelaval.github.io/shipped/anthropic-monthly/{YYYY-MM}` | A monthly roundup | **Yes** |
| `id8labs/public/shipped/` | Rendered HTML the hub/issues are served from | Build artifact |
| `id8labs/lib/shipped/*.data.ts` | AUTO-GENERATED manifests (issues, dailies, sweeps) | Never hand-edit |
| `shipped/content/` (this repo) | Markdown source of each issue | Source |
| `shipped/content/index.md` | Repo-local archive table; defers to the hub | Mirror |
| `github.com/eddiebelaval/shipped` | Pipeline + content source (MIT) | Source repo |
| `id8labs/app/admin/newsletter/shipped` | Subscriber metrics dashboard (internal) | Not a publication home |

## Link rules (so all links point to the same place)

In the id8labs site, build Shipped links through the single helpers in
`lib/shipped/issues.ts` — never hand-type a URL:

- `getShippedIssueHref(NN)` → `/shipped/NN` (relative, in-site links)
- `getShippedIssueUrl(NN)` → `https://id8labs.app/shipped/NN` (emails / outbound messages)
- `SHIPPED_HUB_URL` → `https://id8labs.app/shipped` (the hub)

In launch copy and messages that go out, the issue link is always
`id8labs.app/shipped/{NN}` and the magazine link is `id8labs.app/shipped`.

## Cadence

Ships **Friday 9 AM ET** (human-gated push). Not 5 PM — that string was stale
wherever it appeared and has been corrected.
