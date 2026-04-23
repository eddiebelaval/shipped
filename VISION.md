# VISION.md — Shipped.

> _Draft — Eddie edits in his voice. Everything below is reconstructed from our conversations; replace any sentence where the wording isn't yours._

---

## One-liner

**Shipped. is a weekly magazine for builders who can't — or won't — stay glued to social media, aggregating the week's Anthropic releases into one read that's worth the time.**

## Who it's for

Builders using Anthropic's platform (Claude API, Claude Code, the SDKs, the research) who:

- Step away from X/Twitter for 30 minutes and come back feeling behind.
- Don't want to turn their feed into a release tracker.
- Want the week's signal without the week's noise.
- Would pay for curation if it were this good — but it's free because the pipeline is cheap to run.

The reader is technical. They don't need concepts defined. They need links that go somewhere real, numbers that match the source, and a voice that respects their time.

## Why this, why now

The pace of releases in the Anthropic ecosystem is blinding. In the three weeks before Issue 01 shipped, Anthropic pushed **56 distinct releases** across models, Claude Code, SDKs, and research. X and Reddit cover them in fragments. Nobody ties the week together.

Shipped. is the tie.

The format — a magazine, not a feed — is the point. A magazine says: someone curated this, someone took responsibility for its quality, you can read it cover-to-cover and stop.

## What Shipped. is

- **Weekly.** Every Friday at 9 AM ET.
- **Written, not auto-generated.** The pipeline scrapes; the front-of-book is written.
- **Verified.** Every claim — every URL, number, quote, and date — passes through an attestation gate before it publishes. Nothing ships that can't be sourced. The verifier is the moat.
- **Eye-candy.** Real typography. Magazine layout. Not another Substack.
- **A voice you'd want to be your own.** Dry, confident, never breathless. No "EPIC." No "thrilled to." No "ushers in."
- **Open-source from day one.** The pipeline is public. Anyone can fork it and do this for themselves.

## What Shipped. is NOT

- Not a news aggregator. News aggregators die. This is a magazine.
- Not a release notes dump. The Release Log is for completeness; the front-of-book is the point.
- Not auto-posted. The human at `git push` is the final gate, always.
- Not a podcast, a video series, or a book — yet. (See roadmap.)

## Scope for v1 (Issues 01–04)

**In:**

- English + Spanish editions. Miami context: Spanish earns its slot. **Issue 03 is the ES pilot** (moved from Issue 02 on 2026-04-20 — editorial load for 02 was already heavy with Claude Design + Trust Week coverage; splitting focus would have broken the quality bar). The renderer takes `(markdown, lang)` and produces per-language HTML.
- The verifier, hardened. Per-language number-format tolerance. Known-fragile domain allowlist for sources that block scraper user agents.
- Weekly cadence, never skipped.

**Not in:**

- Portuguese. Earns its slot after ES proves out.
- Video ("how Shipped is made"). Deferred, not killed. High-value eventually; low-priority now.
- Additional scraped sources (other labs, community projects). Anthropic-only until the signal is clear.

## In-flight — Issue 02 → Issue 03 launch (Apr 24 → May 1)

Three initiatives carried over to Issue 03's Friday May 1 launch, captured here so the triad reflects reality:

### Email engine (building Mon–Thu)

Automated weekly send, fires Friday 9 AM ET as part of the gate-open ship model (below). Stack: Resend for delivery, Supabase (`newsletter_subscribers` with the `lists` column) for the subscriber list, React Email for templates, Vercel Cron for the trigger. Format: **full inline magazine in the email body** — not a digest, not a "read on web" teaser. The reader opens the email and has the whole issue. Mobile-safe typography (Georgia + system-sans fallbacks since Fraunces won't load reliably in email clients), tables for layout, preheader text pulled from the deck, one-click unsubscribe per RFC 8058 (Gmail/Yahoo required).

### Gate-open ship model

The shipped magazine moves from *last-minute Friday push* to *stage Thursday, gate opens Friday*. Refinement: the editor does the final read and git push Thursday evening at their pace; the issue lives at its direct URL (`id8labs.app/shipped/NN/`) unlisted. At Friday 9 AM ET a Vercel Cron fires `/api/shipped/publish/cron`, which marks the issue public on the archive, fires the email, and logs the send. Friday morning becomes a clock event, not a typing event. Human gate preserved (Thursday push); Friday morning risk removed.

### Language settings — EN canonical, PR edition

The pipeline architecture already assumes `(markdown, lang) → html`. Issue 03 is the Spanish (Puerto Rican flavor) pilot. The edition ships alongside EN — same canonical, translated from EN, at `id8labs.app/shipped/NN/es/` or equivalent route. The verifier runs per-language with number-format tolerance (commas vs. periods, currency). Translation is human-assisted (Eddie's native register, not a machine-dump). PT and other locales earn slots after PR proves out.

## Roadmap beyond v1

### Podcast (exploring — real signal)
The WhatsApp group flagged it. It's worth planning, not building, yet. Open questions: audio-first or video-first? Solo narrator or guest conversation? Weekly companion to the magazine or a separate beat? Not answered.

### Video — "How Shipped is made"
One evergreen video pinned to `/shipped`. Not a weekly BTS series (which would become a second production line we'd skip by week 3). Ships when it ships.

### Translation pipeline, full
After ES proves out, extend to PT, then other languages the audience asks for. Architecture supports it from day one — `(md, lang) → html`.

### Programmatic OG card generation
Today, OG cards are hand-produced. When translation lands, we'll need per-language covers. `@chenglou/pretext` is on the [technology watchlist](./pipeline/TECHNOLOGY_WATCHLIST.md) for this.

## Moat

Three things, in order of defensibility:

1. **The verifier.** Anyone can scrape. Almost nobody publishes verified. Every claim attested to its source before the magazine ships is a different kind of product than a digest.
2. **The voice.** Style guide is strict (see `content/STYLE.md`). Builders recognize writing that takes the reader seriously.
3. **The weekly cadence.** Shipped. exists every Friday. That's the product.

## Auto-ops, human-voice

The pipeline may automate any mechanical operation — scraping, grading, scheduling, staging, routing, state tracking, readiness scoring, next-action resolution. The pipeline **shall not** generate prose, assign editorial judgment, or make attribution decisions. Those are the editor's, every issue, every line.

This is the difference between a fully automated *operations* layer and a fully automated *magazine*. Only the former. The latter would kill the moat.

When a tool proposes an editorial action — *"retrofit the counter-frame in this article,"* *"add an operator-takeaway section here"* — it produces **scaffolding**: section headers, structural prompts, references to STYLE.md moves. It does not produce the words that ship. A writer — human — does that, every time.

The practical rule:

- Automate the **when, what state, what's missing, what's next.**
- Never automate the **what it says.**

If a future tool sits on this line and feels ambiguous about which side it's on, default to manual. The moat is the voice. The voice is yours.

## Success signals

**Leading (first 4 weeks):**
- Does Issue 02 ship on time with ES pilot?
- Verifier catches ≥1 error that would have shipped without it.
- WhatsApp group shares Issue 02 unprompted.

**Lagging (by Issue 10):**
- Repeat readers. Someone subscribing to Shipped. because they read last week's issue is the real signal.
- Inbound from builders asking "how do I do this for my own domain?"
- One external contributor who isn't in the WhatsApp group.

## Non-negotiables

- Friday, 9 AM ET. Every week.
- The verifier runs, or the issue doesn't ship.
- Voice stays tight. The style guide is the contract.
- The human pushes git. Never automated.
- Auto-ops, human-voice. Automate the mechanics. Write the words.
