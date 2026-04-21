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
