# Shipped. — Release Distribution

The release routines (Nightly / Weekly / Monthly Anthropic sweeps) publish to the
`daily-pages` branch and deploy via GitHub Pages. They can also stage a copy to a
list of people who asked to follow along.

## The list — two files, one merge

The list lives in two places because this repo is **public** and subscriber
names + emails are not:

1. **`pipeline/recipients.json`** (this repo, public) — distribution config
   (`send_mode`, `from`) plus manual entries. Only add someone here with their
   explicit OK; git history is permanent.
2. **`eddiebelaval/shipped-subscribers` → `recipients.json`** (private repo) —
   the self-serve list. The subscribe endpoint
   (`pipeline/api/newsletter/subscribe.ts`, deployed to Vercel) commits new
   subscribers here. It bootstraps the file on first subscribe, so the private
   repo just has to exist.

`distribute-local.py` fetches both and merges them: recipients dedupe by email
(private wins), and a `send_mode`/`from` set in the private file overrides the
public one. Either file alone is enough — if the private repo is unreachable
the job logs it and runs on the public file only.

Shared shape:

```json
{
  "send_mode": "draft",
  "from": "eb@id8labs.tech",
  "recipients": [
    { "name": "Jane Doe", "email": "jane@example.com", "cadences": ["weekly", "monthly"] }
  ]
}
```

- **`recipients[]`** — `name`, `email`, and which `cadences` they want
  (`nightly`, `weekly`, `monthly`). Weekly-only is the sane default for most people;
  nightly is firehose.
- **`send_mode`**:
  - `draft` (default) — the routine creates a **Gmail draft** addressed to the matching
    recipients. Nothing leaves the outbox until Eddie reviews and hits send.
  - `off` — no distribution. The routine just publishes the page.
  - `send` — auto-send. **Do not set this until Eddie explicitly decides to.** Emailing
    people is outward-facing and stays on the human gate by default.

## Architecture: publish in the cloud, draft on the Mac

Distribution runs in TWO halves because the cloud routines cannot reach Gmail.

**Why split:** the claude.ai Gmail connector is interactively authenticated. The
Nightly/Weekly/Monthly routines run headless in Anthropic's cloud (CCR), where
interactive connectors are absent. Verified 2026-06-08: a routine run published the
page fine but staged zero drafts. So distribution moved to a local job.

**Half 1, cloud (the routines):** publish the rendered page to `daily-pages` and print
the public URL. They carry a best-effort draft step that no-ops in the cloud; the real
distribution is Half 2.

**Half 2, local (`pipeline/scripts/distribute-local.py`):** runs on Eddie's Mac via
launchd (`com.id8labs.shipped-distribute`, daily ~22:45 ET, after the nightly 21:00 and
weekly Fri 22:00 routines publish). It:

1. `git fetch` (no checkout) and reads the public `recipients.json` from `origin/main`,
   the private list from `shipped-subscribers` (same git auth as origin, SSH or HTTPS
   to match), and the latest page stem per cadence from `origin/daily-pages`.
2. For each cadence with a NEW page (tracked in `~/.shipped-distribution/seen.json` so it
   never double-drafts) and at least one matching recipient, builds the public URL.
3. Stages a Mail.app DRAFT via `shipped-draft.applescript` (sender = the `from` field,
   recipients on BCC, subject + intro + URL). It NEVER sends. Eddie reviews and hits send.
4. If `send_mode` is `off` it does nothing; if `send` it still only drafts (the local job
   has no send path, by design, so the outward gate stays human).

**Install (local, one-time):** copy `distribute-local.py` and `shipped-draft.applescript`
to `~/.shipped-distribution/`, copy the plist to `~/Library/LaunchAgents/`, then
`launchctl load`. The launchd job uses the local copies, not the repo tree.

## Design language

Pages render in the canonical Shipped. light design lifted from
`pipeline/src/render/template.html` (warm-white `#FAF8F4`, orange `#FF6B35`, Fraunces
display, Archivo body, Archivo Narrow flags, paper grain). Routines must not invent their
own palette. Type identity ratified 2026-06-08 (DESIGN.md Rev 5.0).
