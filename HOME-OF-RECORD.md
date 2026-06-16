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

```
content/issue-NN-*.md            source of truth for an issue (this repo)
        │  pipeline render
        ▼
id8labs/public/shipped/NN/       the published issue page  →  id8labs.app/shipped/NN
id8labs/public/shipped/index.html   THE HUB (archive of all issues)  →  id8labs.app/shipped
        │  pipeline sync-manifest (derives from the hub)
        ▼
id8labs/lib/shipped/issues.data.ts   AUTO-GENERATED mirror of the hub
        │  consumed by
        ▼
/writing feed + homepage featured slot   (one source → cannot drift from the hub)
```

The hub archive (`public/shipped/index.html`) is the **single source of truth** for
what has shipped. The unified `/writing` feed and the homepage no longer keep their
own hand-maintained list — they derive from the hub via `issues.data.ts`, which the
publish pipeline regenerates on every run (`pipeline/src/render/sync-manifest.ts`).
Add an issue by rendering it; the hub and the feed update together.

## Every place Shipped is referenced, and what it is

| Place | Role | Canonical? |
|---|---|---|
| `id8labs.app/shipped` | The hub (all issues) | **Yes — the home** |
| `id8labs.app/shipped/{NN}` | An issue | **Yes** |
| `id8labs.app/writing` (Magazine filter) | Unified feed listing; links out to `/shipped/{NN}` | Mirror of the hub |
| `id8labs/public/shipped/` | Rendered HTML the hub/issues are served from | Build artifact |
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
