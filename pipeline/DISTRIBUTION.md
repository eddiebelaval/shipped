# Shipped. — Release Distribution

The release routines (Nightly / Weekly / Monthly Anthropic sweeps) publish to the
`daily-pages` branch and deploy via GitHub Pages. They can also stage a copy to a
list of people who asked to follow along.

## The list

`pipeline/recipients.json`:

```json
{
  "send_mode": "draft",
  "from": "eb@id8labs.tech",
  "recipients": [
    { "name": "Jane Doe", "email": "jane@example.com", "cadences": ["weekly", "monthly"] }
  ]
}
```

- **`recipients[]`** — add a friend with `name`, `email`, and which `cadences` they want
  (`nightly`, `weekly`, `monthly`). Weekly-only is the sane default for most people;
  nightly is firehose.
- **`send_mode`**:
  - `draft` (default) — the routine creates a **Gmail draft** addressed to the matching
    recipients. Nothing leaves the outbox until Eddie reviews and hits send.
  - `off` — no distribution. The routine just publishes the page.
  - `send` — auto-send. **Do not set this until Eddie explicitly decides to.** Emailing
    people is outward-facing and stays on the human gate by default.

## How the routine uses it

After publishing the page to `daily-pages`, each release routine:

1. Reads `pipeline/recipients.json`.
2. Filters `recipients[]` to those whose `cadences` include this routine's cadence.
3. If the filtered list is empty, or `send_mode` is `off`, it does nothing further.
4. If `send_mode` is `draft` and a Gmail connector is attached, it creates one draft
   (To: the filtered recipients, or BCC for privacy on larger lists) with the public URL
   and the rendered page. It never sends.
5. If it cannot create a draft for any reason, it prints the recipient list and the public
   URL in its final message so Eddie can forward manually. It never silently drops them.

## Design language

Pages render in the canonical Shipped. light design lifted from
`pipeline/src/render/template.html` (warm-white `#fafaf7`, orange `#FF6B35`, Fraunces
display, Archivo body, paper grain). Routines must not invent their own palette.
